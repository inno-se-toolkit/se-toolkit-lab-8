"""Stdio MCP server exposing observability tools for VictoriaLogs and VictoriaTraces."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel

from mcp_obs.observability import (
    LogsSearchParams,
    LogsErrorCountParams,
    TracesListParams,
    TracesGetParams,
    logs_search,
    logs_error_count,
    traces_list,
    traces_get,
)


TOOL_SPECS = [
    {
        "name": "logs_search",
        "description": "Search logs in VictoriaLogs using LogsQL query. Use LogsQL syntax with _time: for time range, severity:ERROR for errors, service.name for filtering.",
        "model": LogsSearchParams,
    },
    {
        "name": "logs_error_count",
        "description": "Count errors per service over a time window. Returns total count and breakdown by service.",
        "model": LogsErrorCountParams,
    },
    {
        "name": "traces_list",
        "description": "List recent traces for a service. Returns trace summaries with IDs that can be fetched in detail.",
        "model": TracesListParams,
    },
    {
        "name": "traces_get",
        "description": "Fetch a specific trace by ID. Use trace_id from logs or traces_list to get full span hierarchy.",
        "model": TracesGetParams,
    },
]


def _text(data: Any) -> list[TextContent]:
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, default=str))]


def create_server() -> Server:
    server = Server("observability")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(name=spec["name"], description=spec["description"], inputSchema=spec["model"].model_json_schema())
            for spec in TOOL_SPECS
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        spec = next((s for s in TOOL_SPECS if s["name"] == name), None)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        try:
            args = spec["model"].model_validate(arguments or {})
            if name == "logs_search":
                result = await logs_search(args)
            elif name == "logs_error_count":
                result = await logs_error_count(args)
            elif name == "traces_list":
                result = await traces_list(args)
            elif name == "traces_get":
                result = await traces_get(args)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
            return _text(result)
        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


def main() -> None:
    """Run the observability MCP server."""
    from mcp_obs.observability import VICTORIALOGS_URL, VICTORIATRACES_URL
    import os

    # Override URLs from environment if provided
    global VICTORIALOGS_URL, VICTORIATRACES_URL
    VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", VICTORIALOGS_URL)
    VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", VICTORIATRACES_URL)

    async def run() -> None:
        server = create_server()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
