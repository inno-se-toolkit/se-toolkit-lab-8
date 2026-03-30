from __future__ import annotations

import json
from collections import Counter
from typing import Any

import httpx


def _quote(value: str) -> str:
    if any(ch.isspace() for ch in value) or ":" in value:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value


class ObservabilityClient:
    def __init__(self, logs_base_url: str, traces_base_url: str):
        self.logs_base_url = logs_base_url.rstrip("/")
        self.traces_base_url = traces_base_url.rstrip("/")

    async def _get_json(self, url: str, params: dict[str, Any] | None = None) -> Any:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def logs_query(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{self.logs_base_url}/select/logsql/query",
                params={"query": query, "limit": limit},
            )
            response.raise_for_status()
            lines = [line.strip() for line in response.text.splitlines() if line.strip()]

        results: list[dict[str, Any]] = []
        for line in lines:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                results.append({"_raw": line})
        return results

    async def logs_search(
        self,
        *,
        keyword: str | None = None,
        time_window: str = "10m",
        service_name: str | None = None,
        severity: str | None = None,
        event: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        parts = [f"_time:{time_window}"]
        if service_name:
            parts.append(f'service.name:{_quote(service_name)}')
        if severity:
            parts.append(f"severity:{severity.upper()}")
        if event:
            parts.append(f"event:{event}")
        if keyword:
            parts.append(_quote(keyword))

        query = " ".join(parts)
        rows = await self.logs_query(query, limit=limit)

        trimmed: list[dict[str, Any]] = []
        for row in rows:
            trimmed.append(
                {
                    "time": row.get("_time"),
                    "severity": row.get("severity"),
                    "service_name": row.get("service.name") or row.get("otelServiceName"),
                    "event": row.get("event") or row.get("_msg"),
                    "trace_id": row.get("trace_id") or row.get("otelTraceID"),
                    "span_id": row.get("span_id") or row.get("otelSpanID"),
                    "message": row.get("_msg"),
                }
            )

        return {"query": query, "count": len(trimmed), "results": trimmed}

    async def logs_error_count(
        self,
        *,
        time_window: str = "10m",
        service_name: str | None = None,
        limit: int = 200,
    ) -> dict[str, Any]:
        parts = [f"_time:{time_window}", "severity:ERROR"]
        if service_name:
            parts.append(f'service.name:{_quote(service_name)}')
        query = " ".join(parts)

        rows = await self.logs_query(query, limit=limit)
        counts = Counter(
            (row.get("service.name") or row.get("otelServiceName") or "unknown")
            for row in rows
        )

        return {
            "query": query,
            "total_errors": len(rows),
            "counts": dict(counts),
        }

    async def traces_list(self, *, service_name: str, limit: int = 10) -> dict[str, Any]:
        data = await self._get_json(
            f"{self.traces_base_url}/select/jaeger/api/traces",
            params={"service": service_name, "limit": limit},
        )

        traces = data.get("data", [])
        summaries: list[dict[str, Any]] = []
        for trace in traces:
            spans = trace.get("spans", [])
            processes = trace.get("processes", {})
            service_names = sorted(
                {
                    processes.get(span.get("processID", ""), {})
                    .get("serviceName", "unknown")
                    for span in spans
                }
            )
            summaries.append(
                {
                    "trace_id": trace.get("traceID"),
                    "span_count": len(spans),
                    "services": service_names,
                }
            )

        return {"count": len(summaries), "traces": summaries}

    async def traces_get(self, *, trace_id: str) -> dict[str, Any]:
        data = await self._get_json(
            f"{self.traces_base_url}/select/jaeger/api/traces/{trace_id}"
        )

        traces = data.get("data", [])
        if not traces:
            return {"trace_id": trace_id, "found": False, "spans": []}

        trace = traces[0]
        processes = trace.get("processes", {})
        spans = trace.get("spans", [])

        summarized_spans: list[dict[str, Any]] = []
        for span in spans:
            process = processes.get(span.get("processID", ""), {})
            tags = {
                tag.get("key"): tag.get("value")
                for tag in span.get("tags", [])
                if isinstance(tag, dict) and "key" in tag
            }
            summarized_spans.append(
                {
                    "span_id": span.get("spanID"),
                    "operation": span.get("operationName"),
                    "service_name": process.get("serviceName", "unknown"),
                    "start_time": span.get("startTime"),
                    "duration": span.get("duration"),
                    "tags": tags,
                }
            )

        summarized_spans.sort(key=lambda item: (item["start_time"] or 0))

        return {
            "trace_id": trace.get("traceID", trace_id),
            "found": True,
            "span_count": len(summarized_spans),
            "spans": summarized_spans,
        }
