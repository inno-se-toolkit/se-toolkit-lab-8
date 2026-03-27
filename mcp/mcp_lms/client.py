"""Async HTTP client and models for LMS plus observability APIs."""

import json
import os
from datetime import UTC, datetime, timedelta

import httpx
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class HealthResult(BaseModel):
    status: str
    item_count: int | str = "unknown"
    error: str = ""


class Item(BaseModel):
    id: int | None = None
    type: str = "step"
    parent_id: int | None = None
    title: str = ""
    description: str = ""


class Learner(BaseModel):
    id: int | None = None
    external_id: str = ""
    student_group: str = ""


class PassRate(BaseModel):
    task: str
    avg_score: float
    attempts: int


class TimelineEntry(BaseModel):
    date: str
    submissions: int


class GroupPerformance(BaseModel):
    group: str
    avg_score: float
    students: int


class TopLearner(BaseModel):
    learner_id: int
    avg_score: float
    attempts: int


class CompletionRate(BaseModel):
    lab: str
    completion_rate: float
    passed: int
    total: int


class SyncResult(BaseModel):
    new_records: int
    total_records: int


class LogEntry(BaseModel):
    timestamp: str = ""
    service: str = ""
    level: str = ""
    event: str = ""
    message: str = ""
    trace_id: str = ""
    raw: dict[str, object] = {}


class ErrorCount(BaseModel):
    service: str
    count: int


class TraceSummary(BaseModel):
    trace_id: str
    service: str = ""
    operation: str = ""
    start_time: str = ""
    duration_ms: float = 0.0


class TraceSpan(BaseModel):
    span_id: str
    operation: str = ""
    service: str = ""
    start_time: str = ""
    duration_ms: float = 0.0
    tags: dict[str, str] = {}


class TraceDetail(BaseModel):
    trace_id: str
    spans: list[TraceSpan]


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------


class LMSClient:
    """Client for the LMS backend API."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        logs_url: str | None = None,
        traces_url: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self.logs_url = (logs_url or os.environ.get("NANOBOT_LOGS_URL") or "http://localhost:42010").rstrip("/")
        self.traces_url = (traces_url or os.environ.get("NANOBOT_TRACES_URL") or "http://localhost:42011").rstrip("/")

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(headers=self._headers, timeout=10.0)

    async def health_check(self) -> HealthResult:
        async with self._client() as c:
            try:
                r = await c.get(f"{self.base_url}/items/")
                r.raise_for_status()
                items = [Item.model_validate(i) for i in r.json()]
                return HealthResult(status="healthy", item_count=len(items))
            except httpx.ConnectError:
                return HealthResult(
                    status="unhealthy", error=f"connection refused ({self.base_url})"
                )
            except httpx.HTTPStatusError as e:
                return HealthResult(
                    status="unhealthy", error=f"HTTP {e.response.status_code}"
                )
            except Exception as e:
                return HealthResult(status="unhealthy", error=str(e))

    async def get_items(self) -> list[Item]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/items/")
            r.raise_for_status()
            return [Item.model_validate(i) for i in r.json()]

    async def get_learners(self) -> list[Learner]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/learners/")
            r.raise_for_status()
            return [Learner.model_validate(i) for i in r.json()]

    async def get_pass_rates(self, lab: str) -> list[PassRate]:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/pass-rates", params={"lab": lab}
            )
            r.raise_for_status()
            return [PassRate.model_validate(i) for i in r.json()]

    async def get_timeline(self, lab: str) -> list[TimelineEntry]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/analytics/timeline", params={"lab": lab})
            r.raise_for_status()
            return [TimelineEntry.model_validate(i) for i in r.json()]

    async def get_groups(self, lab: str) -> list[GroupPerformance]:
        async with self._client() as c:
            r = await c.get(f"{self.base_url}/analytics/groups", params={"lab": lab})
            r.raise_for_status()
            return [GroupPerformance.model_validate(i) for i in r.json()]

    async def get_top_learners(self, lab: str, limit: int = 5) -> list[TopLearner]:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/top-learners",
                params={"lab": lab, "limit": limit},
            )
            r.raise_for_status()
            return [TopLearner.model_validate(i) for i in r.json()]

    async def get_completion_rate(self, lab: str) -> CompletionRate:
        async with self._client() as c:
            r = await c.get(
                f"{self.base_url}/analytics/completion-rate", params={"lab": lab}
            )
            r.raise_for_status()
            return CompletionRate.model_validate(r.json())

    async def sync_pipeline(self) -> SyncResult:
        async with self._client() as c:
            r = await c.post(f"{self.base_url}/pipeline/sync")
            r.raise_for_status()
            return SyncResult.model_validate(r.json())

    async def logs_search(
        self,
        query: str = "",
        service: str = "",
        level: str = "",
        minutes: int = 60,
        limit: int = 20,
    ) -> list[LogEntry]:
        filters = [f"_time:{minutes}m"]
        if service:
            filters.append(f'_stream:{{service="{service}"}}')
        if level:
            filters.append(f"level:{level}")
        if query:
            filters.append(query)
        logsql = " AND ".join(filters)
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.get(
                f"{self.logs_url}/select/logsql/query",
                params={"query": logsql, "limit": str(limit)},
            )
            r.raise_for_status()
            payload = r.text.strip().splitlines()

        entries: list[LogEntry] = []
        for line in payload:
            if not line.strip():
                continue
            data = json.loads(line)
            entries.append(
                LogEntry(
                    timestamp=str(data.get("_time", "")),
                    service=str(data.get("service", "")),
                    level=str(data.get("level", "")),
                    event=str(data.get("event", "")),
                    message=str(data.get("_msg", data.get("body", ""))),
                    trace_id=str(
                        data.get("trace_id")
                        or data.get("traceID")
                        or data.get("TraceId")
                        or ""
                    ),
                    raw=data,
                )
            )
        return entries

    async def logs_error_count(
        self,
        minutes: int = 60,
        service: str = "",
    ) -> list[ErrorCount]:
        logs = await self.logs_search(service=service, level="error", minutes=minutes, limit=200)
        counts: dict[str, int] = {}
        for entry in logs:
            key = entry.service or "unknown"
            counts[key] = counts.get(key, 0) + 1
        return [ErrorCount(service=name, count=count) for name, count in sorted(counts.items())]

    async def traces_list(
        self,
        service: str = "backend",
        minutes: int = 60,
        limit: int = 10,
    ) -> list[TraceSummary]:
        end = datetime.now(UTC)
        start = end - timedelta(minutes=minutes)
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.get(
                f"{self.traces_url}/select/jaeger/api/traces",
                params={
                    "service": service,
                    "limit": str(limit),
                    "start": str(int(start.timestamp() * 1_000_000)),
                    "end": str(int(end.timestamp() * 1_000_000)),
                },
            )
            r.raise_for_status()
            data = r.json().get("data", [])
        summaries: list[TraceSummary] = []
        for trace in data:
            first = (trace.get("spans") or [{}])[0]
            process_id = first.get("processID", "")
            processes = trace.get("processes", {})
            process = processes.get(process_id, {})
            service_name = process.get("serviceName", "")
            duration_ms = float(first.get("duration", 0)) / 1000.0
            summaries.append(
                TraceSummary(
                    trace_id=str(trace.get("traceID", "")),
                    service=str(service_name),
                    operation=str(first.get("operationName", "")),
                    start_time=str(first.get("startTime", "")),
                    duration_ms=duration_ms,
                )
            )
        return summaries

    async def traces_get(self, trace_id: str) -> TraceDetail:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.get(f"{self.traces_url}/select/jaeger/api/traces/{trace_id}")
            r.raise_for_status()
            data = r.json().get("data", [])
        if not data:
            return TraceDetail(trace_id=trace_id, spans=[])
        trace = data[0]
        processes = trace.get("processes", {})
        spans: list[TraceSpan] = []
        for span in trace.get("spans", []):
            process = processes.get(span.get("processID", ""), {})
            tags = {
                str(tag.get("key", "")): str(tag.get("value", ""))
                for tag in span.get("tags", [])
            }
            spans.append(
                TraceSpan(
                    span_id=str(span.get("spanID", "")),
                    operation=str(span.get("operationName", "")),
                    service=str(process.get("serviceName", "")),
                    start_time=str(span.get("startTime", "")),
                    duration_ms=float(span.get("duration", 0)) / 1000.0,
                    tags=tags,
                )
            )
        return TraceDetail(trace_id=str(trace.get("traceID", trace_id)), spans=spans)


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def format_health(result: HealthResult) -> str:
    if result.status == "healthy":
        return f"\u2705 Backend is healthy. {result.item_count} items available."
    return f"\u274c Backend error: {result.error or 'Unknown'}"


def format_labs(items: list[Item]) -> str:
    labs = sorted(
        [i for i in items if i.type == "lab"],
        key=lambda x: str(x.id),
    )
    if not labs:
        return "\U0001f4ed No labs available."
    text = "\U0001f4da Available labs:\n\n"
    text += "\n".join(f"\u2022 {lab.title}" for lab in labs)
    return text


def format_scores(lab: str, rates: list[PassRate]) -> str:
    if not rates:
        return f"\U0001f4ed No scores found for {lab}."
    text = f"\U0001f4ca Pass rates for {lab}:\n\n"
    text += "\n".join(
        f"\u2022 {r.task}: {r.avg_score:.1f}% ({r.attempts} attempts)" for r in rates
    )
    return text
