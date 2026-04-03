"""HTTP client for VictoriaLogs and VictoriaTraces APIs."""

from __future__ import annotations

import json
from typing import Any

import httpx

from mcp_obs.settings import ObsSettings


class ObsClient:
    """Client for querying VictoriaLogs and VictoriaTraces."""

    def __init__(self, settings: ObsSettings) -> None:
        self.settings = settings
        self._http = httpx.AsyncClient(timeout=10.0)

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> "ObsClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # --- VictoriaLogs methods ---

    async def logs_search(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        """Search logs using LogsQL query."""
        url = f"{self.settings.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": limit}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        lines = resp.text.strip().split("\n")
        results = []
        for line in lines:
            if line.strip():
                try:
                    results.append(json.loads(line))
                except json.JSONDecodeError:
                    results.append({"raw": line})
        return results

    async def logs_error_count(
        self, service: str = "Learning Management Service", minutes: int = 60
    ) -> dict[str, Any]:
        """Count errors per service over a time window."""
        query = f'_time:{minutes}m service.name:"{service}" severity:ERROR'
        url = f"{self.settings.victorialogs_url}/select/logsql/query"
        params = {"query": query, "limit": 1000}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        lines = resp.text.strip().split("\n")
        count = sum(1 for line in lines if line.strip())
        return {
            "service": service,
            "time_window_minutes": minutes,
            "error_count": count,
            "query": query,
        }

    # --- VictoriaTraces methods ---

    async def traces_list(
        self, service: str = "Learning Management Service", limit: int = 10
    ) -> list[dict[str, Any]]:
        """List recent traces for a service."""
        url = f"{self.settings.victoriatraces_url}/select/jaeger/api/traces"
        params = {"service": service, "limit": limit}
        resp = await self._http.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        # Return simplified trace info
        result = []
        for trace in traces:
            spans = trace.get("spans", [])
            result.append(
                {
                    "traceID": trace.get("traceID"),
                    "span_count": len(spans),
                    "operations": [s.get("operationName") for s in spans[:5]],
                }
            )
        return result

    async def traces_get(self, trace_id: str) -> dict[str, Any]:
        """Fetch a specific trace by ID."""
        url = f"{self.settings.victoriatraces_url}/select/jaeger/api/traces/{trace_id}"
        resp = await self._http.get(url)
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        if not traces:
            return {"error": f"Trace {trace_id} not found"}
        trace = traces[0]
        spans = trace.get("spans", [])
        # Build span hierarchy summary
        span_summary = []
        for span in spans:
            tags = {t["key"]: t["value"] for t in span.get("tags", [])}
            span_summary.append(
                {
                    "operationName": span.get("operationName"),
                    "duration": span.get("duration"),
                    "tags": tags,
                    "has_error": any(
                        t.get("key") == "error" for t in span.get("tags", [])
                    ),
                }
            )
        return {
            "traceID": trace.get("traceID"),
            "span_count": len(spans),
            "spans": span_summary,
        }
