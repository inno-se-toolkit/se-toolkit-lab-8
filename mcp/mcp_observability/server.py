"""MCP server exposing VictoriaLogs and VictoriaTraces as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Sequence
from typing import Any
from datetime import datetime, timedelta

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# VictoriaLogs and VictoriaTraces endpoints
VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://localhost:9428")
VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://localhost:10428")


# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _LogsSearch(BaseModel):
    query: str = Field(
        default="_stream:{service=\"backend\"}",
        description="LogsQL query string (default: all backend logs)"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Max logs to return")
    hours: int = Field(default=1, ge=0, le=168, description="Time range in hours (0=all)")


class _LogsErrorCount(BaseModel):
    hours: int = Field(default=1, ge=1, le=168, description="Time window in hours")
    service: str = Field(default="", description="Filter by service name (optional)")


class _TracesList(BaseModel):
    service: str = Field(default="backend", description="Service name to filter traces")
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")
    hours: int = Field(default=1, ge=1, le=168, description="Time range in hours")


class _TracesGet(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _text(data: Any) -> list[TextContent]:
    """Serialize data to a JSON text block."""
    if isinstance(data, (dict, list)):
        text = json.dumps(data, ensure_ascii=False, default=str)
    else:
        text = str(data)
    return [TextContent(type="text", text=text)]


async def _http_get(url: str, params: dict | None = None) -> Any:
    """Make HTTP GET request."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearch) -> list[TextContent]:
    """Search logs using VictoriaLogs LogsQL query."""
    # Build time filter
    if args.hours > 0:
        start_time = (datetime.utcnow() - timedelta(hours=args.hours)).isoformat() + "Z"
        query = f"{args.query} && _time >= '{start_time}'"
    else:
        query = args.query
    
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {
        "query": query,
        "limit": args.limit,
    }
    
    try:
        result = await _http_get(url, params)
        # VictoriaLogs returns array of log entries
        return _text(result)
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaLogs query failed: {e}"})


async def _logs_error_count(args: _LogsErrorCount) -> list[TextContent]:
    """Count errors per service over a time window."""
    start_time = (datetime.utcnow() - timedelta(hours=args.hours)).isoformat() + "Z"
    
    # Build query to count errors
    base_query = 'level:error'
    if args.service:
        base_query = f'_stream:{{service="{args.service}"}} && level:error'
    
    query = f"{base_query} && _time >= '{start_time}'"
    
    url = f"{VICTORIALOGS_URL}/select/logsql/query"
    params = {
        "query": query,
        "limit": 10000,
    }
    
    try:
        result = await _http_get(url, params)
        # Count errors
        error_count = len(result) if isinstance(result, list) else 0
        
        # Group by service if possible
        service_counts = {}
        if isinstance(result, list):
            for entry in result:
                if isinstance(entry, dict):
                    svc = entry.get("_stream", {}).get("service", "unknown")
                    service_counts[svc] = service_counts.get(svc, 0) + 1
        
        return _text({
            "total_errors": error_count,
            "time_window_hours": args.hours,
            "errors_by_service": service_counts,
        })
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaLogs query failed: {e}"})


async def _traces_list(args: _TracesList) -> list[TextContent]:
    """List recent traces for a service."""
    # VictoriaTraces Jaeger-compatible API
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces"
    params = {
        "service": args.service,
        "limit": args.limit,
    }
    
    try:
        result = await _http_get(url, params)
        # Jaeger API returns {"data": [...]}
        traces = result.get("data", []) if isinstance(result, dict) else []
        
        # Simplify output
        summary = []
        for trace in traces[:args.limit]:
            summary.append({
                "trace_id": trace.get("traceID"),
                "spans": len(trace.get("spans", [])),
                "start_time": trace.get("startTime"),
                "duration_ms": trace.get("duration"),
            })
        
        return _text({"traces": summary, "total": len(traces)})
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaTraces query failed: {e}"})


async def _traces_get(args: _TracesGet) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    url = f"{VICTORIATRACES_URL}/jaeger/api/traces/{args.trace_id}"
    
    try:
        result = await _http_get(url)
        # Jaeger API returns {"data": [...]}
        traces = result.get("data", []) if isinstance(result, dict) else []
        
        if not traces:
            return _text({"error": f"Trace {args.trace_id} not found"})
        
        # Return full trace with spans
        trace = traces[0]
        return _text({
            "trace_id": trace.get("traceID"),
            "duration_ms": trace.get("duration"),
            "start_time": trace.get("startTime"),
            "spans": [
                {
                    "span_id": span.get("spanID"),
                    "operation": span.get("operationName"),
                    "service": span.get("process", {}).get("serviceName"),
                    "duration_ms": span.get("duration"),
                    "tags": span.get("tags", []),
                    "logs": span.get("logs", []),
                }
                for span in trace.get("spans", [])
            ],
        })
    except httpx.HTTPError as e:
        return _text({"error": f"VictoriaTraces query failed: {e}"})


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "logs_search",
    "Search logs in VictoriaLogs using LogsQL query. Returns matching log entries.",
    _LogsSearch,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Returns total count and breakdown by service.",
    _LogsErrorCount,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service from VictoriaTraces. Returns trace summaries.",
    _TracesList,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch a specific trace by ID from VictoriaTraces. Returns full trace with all spans.",
    _TracesGet,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
