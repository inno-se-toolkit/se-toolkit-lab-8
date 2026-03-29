from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("observability")

# VictoriaLogs and VictoriaTraces URLs (Docker internal network)
VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")


class LogsSearchArgs(BaseModel):
    query: str = Field(description="LogsQL query string, e.g., 'severity:ERROR' or 'service.name:backend'")
    limit: int = Field(default=100, ge=1, le=1000, description="Max results to return")


class LogsErrorCountArgs(BaseModel):
    service: str = Field(description="Service name, e.g., 'Learning Management Service'")
    hours: int = Field(default=1, ge=1, description="Time window in hours")


class TracesListArgs(BaseModel):
    service: str = Field(description="Service name to search traces for")
    limit: int = Field(default=20, ge=1, le=100, description="Max traces to return")


class TracesGetArgs(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch full details for")


async def logs_search(args: LogsSearchArgs) -> list[TextContent]:
    """Search logs using VictoriaLogs LogsQL query."""
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIALOGS_URL}/select/logsql/query"
        params = {"query": args.query, "limit": args.limit}
        resp = await client.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return [TextContent(type="text", text=resp.text)]


async def logs_error_count(args: LogsErrorCountArgs) -> list[TextContent]:
    """Count errors for a service over time window."""
    query = f'severity:ERROR AND service.name:"{args.service}"'
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIALOGS_URL}/select/logsql/query"
        params = {"query": query, "limit": 1000}
        resp = await client.get(url, params=params, timeout=30)
        resp.raise_for_status()
        lines = [l for l in resp.text.strip().split('\n') if l.strip()]
        result = {
            "service": args.service,
            "error_count": len(lines),
            "window_hours": args.hours
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def traces_list(args: TracesListArgs) -> list[TextContent]:
    """List recent traces for a service."""
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIATRACES_URL}/api/traces"
        params = {"service": args.service, "limit": args.limit}
        resp = await client.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        traces = data.get("data", [])
        result = [{"trace_id": t["traceID"], "spans": len(t["spans"])} for t in traces[:10]]
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def traces_get(args: TracesGetArgs) -> list[TextContent]:
    """Get a specific trace by ID."""
    async with httpx.AsyncClient() as client:
        url = f"{VICTORIATRACES_URL}/api/traces/{args.trace_id}"
        resp = await client.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return [TextContent(type="text", text=json.dumps(data.get("data", []), indent=2))]


# Register tools
TOOLS = {}

def register_tool(name: str, description: str, model: type[BaseModel], handler):
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    TOOLS[name] = (model, handler, Tool(name=name, description=description, inputSchema=schema))

register_tool("logs_search", "Search logs using LogsQL query. Use severity:ERROR for errors, service.name for specific service.", LogsSearchArgs, logs_search)
register_tool("logs_error_count", "Count errors for a service over time window", LogsErrorCountArgs, logs_error_count)
register_tool("traces_list", "List recent traces for a service", TracesListArgs, traces_list)
register_tool("traces_get", "Get full details of a specific trace by ID", TracesGetArgs, traces_get)


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = TOOLS.get(name)
    if not entry:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    model_cls, handler, _ = entry
    args = model_cls.model_validate(arguments or {})
    return await handler(args)


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
