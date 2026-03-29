"""Stdio MCP server exposing observability operations as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _LogsSearch(BaseModel):
    query: str = Field(
        description="LogsQL query string. Example: '_stream:{service=\"backend\"} AND level:error'"
    )
    limit: int = Field(default=100, ge=1, le=1000, description="Max log entries to return.")
    time_range: str = Field(
        default="1h",
        description="Time range for the query (e.g., '1h', '24h', '7d')."
    )


class _LogsErrorCount(BaseModel):
    time_range: str = Field(
        default="1h",
        description="Time window to count errors (e.g., '1h', '24h', '7d')."
    )


class _TracesList(BaseModel):
    service: str = Field(description="Service name to filter traces (e.g., 'backend').")
    limit: int = Field(default=10, ge=1, le=100, description="Max traces to return.")
    time_range: str = Field(
        default="1h",
        description="Time range for the query (e.g., '1h', '24h', '7d')."
    )


class _TracesGet(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _text(data: BaseModel | Sequence[BaseModel] | dict | list) -> list[TextContent]:
    """Serialize data to a JSON text block."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    elif isinstance(data, (dict, list)):
        payload = data
    else:
        payload = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearch) -> list[TextContent]:
    """Search logs using VictoriaLogs LogsQL query."""
    logs_url = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
    
    # Convert time range to seconds for VictoriaLogs
    time_range = args.time_range
    
    # Build query URL
    query_url = f"{logs_url}/select/logsql/query"
    params = {
        "query": args.query,
        "limit": args.limit,
    }
    
    # VictoriaLogs accepts time range as part of the query or via _time field
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(query_url, params=params)
            response.raise_for_status()
            # VictoriaLogs returns newline-delimited JSON
            lines = response.text.strip().split("\n") if response.text.strip() else []
            results = [json.loads(line) for line in lines if line.strip()]
            return _text({"logs": results, "count": len(results)})
        except httpx.HTTPError as e:
            return _text({"error": f"HTTP error: {type(e).__name__}: {e}"})
        except json.JSONDecodeError as e:
            return _text({"error": f"JSON decode error: {e}", "raw": response.text[:500]})


async def _logs_error_count(args: _LogsErrorCount) -> list[TextContent]:
    """Count errors per service over a time window."""
    logs_url = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
    
    # Query for errors across all services
    query = 'level:error OR level:ERROR OR "error" OR "ERROR"'
    query_url = f"{logs_url}/select/logsql/query"
    params = {
        "query": query,
        "limit": 1000,
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(query_url, params=params)
            response.raise_for_status()
            lines = response.text.strip().split("\n") if response.text.strip() else []
            logs = [json.loads(line) for line in lines if line.strip()]
            
            # Count errors by service
            error_counts: dict[str, int] = {}
            for log in logs:
                service = log.get("_stream", {}).get("service", "unknown")
                error_counts[service] = error_counts.get(service, 0) + 1
            
            return _text({
                "time_range": args.time_range,
                "total_errors": len(logs),
                "by_service": error_counts
            })
        except httpx.HTTPError as e:
            return _text({"error": f"HTTP error: {type(e).__name__}: {e}"})


async def _traces_list(args: _TracesList) -> list[TextContent]:
    """List recent traces for a service using VictoriaTraces Jaeger API."""
    traces_url = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")
    
    # VictoriaTraces Jaeger API endpoint
    query_url = f"{traces_url}/jaeger/api/traces"
    params = {
        "service": args.service,
        "limit": args.limit,
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(query_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract trace summaries
            traces_data = data.get("data", [])
            summaries = []
            for trace in traces_data[:args.limit]:
                trace_id = trace.get("traceID", "unknown")
                spans = trace.get("spans", [])
                start_time = spans[0].get("startTime", 0) if spans else 0
                duration = max((s.get("duration", 0) for s in spans), default=0)
                summaries.append({
                    "trace_id": trace_id,
                    "start_time": start_time,
                    "duration_us": duration,
                    "span_count": len(spans)
                })
            
            return _text({"traces": summaries, "count": len(summaries)})
        except httpx.HTTPError as e:
            return _text({"error": f"HTTP error: {type(e).__name__}: {e}"})
        except json.JSONDecodeError as e:
            return _text({"error": f"JSON decode error: {e}", "raw": response.text[:500]})


async def _traces_get(args: _TracesGet) -> list[TextContent]:
    """Fetch a specific trace by ID using VictoriaTraces Jaeger API."""
    traces_url = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")
    
    # VictoriaTraces Jaeger API endpoint for single trace
    query_url = f"{traces_url}/jaeger/api/traces/{args.trace_id}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(query_url)
            response.raise_for_status()
            data = response.json()
            return _text(data)
        except httpx.HTTPError as e:
            return _text({"error": f"HTTP error: {type(e).__name__}: {e}"})
        except json.JSONDecodeError as e:
            return _text({"error": f"JSON decode error: {e}", "raw": response.text[:500]})


# ---------------------------------------------------------------------------
# Registry: tool name -> (input model, handler, Tool definition)
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
    "Search logs in VictoriaLogs using LogsQL query. Use to find errors, warnings, or specific events.",
    _LogsSearch,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Use to quickly check if there are any errors.",
    _LogsErrorCount,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service from VictoriaTraces. Returns trace IDs with metadata.",
    _TracesList,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch a specific trace by ID from VictoriaTraces. Returns full trace with span hierarchy.",
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


async def main(logs_url: str | None = None, traces_url: str | None = None) -> None:
    os.environ.setdefault("VICTORIALOGS_URL", logs_url or "http://victorialogs:9428")
    os.environ.setdefault("VICTORIATRACES_URL", traces_url or "http://victoriatraces:10428")
    
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
