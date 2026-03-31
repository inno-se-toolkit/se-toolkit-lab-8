"""Observability tools for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import httpx
from pydantic import BaseModel


VICTORIALOGS_URL = "http://localhost:9428"
VICTORIATRACES_URL = "http://localhost:10428"


class LogsSearchParams(BaseModel):
    query: str = "_time:10m"
    limit: int = 50


class LogsErrorCountParams(BaseModel):
    minutes: int = 60
    service: str | None = None


class TracesListParams(BaseModel):
    service: str = "Learning Management Service"
    limit: int = 10


class TracesGetParams(BaseModel):
    trace_id: str


async def logs_search(args: LogsSearchParams) -> list[dict]:
    """Search logs in VictoriaLogs using LogsQL query."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": args.query, "limit": args.limit},
        )
        response.raise_for_status()
        return response.json() if response.text else []


async def logs_error_count(args: LogsErrorCountParams) -> dict:
    """Count errors per service over a time window."""
    time_window = f"_time:{args.minutes}m"
    service_filter = f' service.name:"{args.service}"' if args.service else ""
    query = f"{time_window}{service_filter} severity:ERROR"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIALOGS_URL}/select/logsql/query",
            params={"query": query, "limit": 1000},
        )
        response.raise_for_status()
        logs = response.json() if response.text else []

        # Count by service
        counts: dict[str, int] = {}
        for log in logs if isinstance(logs, list) else []:
            service = log.get("service.name", "unknown")
            counts[service] = counts.get(service, 0) + 1

        return {"total_errors": sum(counts.values()), "by_service": counts, "query": query}


async def traces_list(args: TracesListParams) -> list[dict]:
    """List recent traces for a service."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces",
            params={"service": args.service, "limit": args.limit},
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", []) if isinstance(data, dict) else []


async def traces_get(args: TracesGetParams) -> dict:
    """Fetch a specific trace by ID."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{args.trace_id}"
        )
        response.raise_for_status()
        data = response.json()
        return data.get("data", [{}])[0] if isinstance(data, dict) else {}
