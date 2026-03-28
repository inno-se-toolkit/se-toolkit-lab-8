import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Конфигурация из переменных окружения
VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")

server = Server("mcp-obs")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="logs_search",
            description="Search logs with LogsQL query. Example query: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "LogsQL query string"},
                    "limit": {"type": "integer", "description": "Max number of results", "default": 20}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="logs_error_count",
            description="Count errors per service over a time window",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name (e.g., 'Learning Management Service')"},
                    "time_window": {"type": "string", "description": "Time window (e.g., '10m', '1h')", "default": "10m"}
                },
                "required": ["service"]
            }
        ),
        types.Tool(
            name="traces_list",
            description="List recent traces for a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name (e.g., 'Learning Management Service')"},
                    "limit": {"type": "integer", "description": "Max number of traces", "default": 10}
                },
                "required": ["service"]
            }
        ),
        types.Tool(
            name="traces_get",
            description="Get a specific trace by trace ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string", "description": "Trace ID (hex string)"}
                },
                "required": ["trace_id"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if not arguments:
        arguments = {}
    try:
        if name == "logs_search":
            query = arguments.get("query")
            limit = arguments.get("limit", 20)
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{VICTORIALOGS_URL}/select/logsql/query",
                    params={"query": query, "limit": limit}
                )
                resp.raise_for_status()
                data = resp.json()
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "logs_error_count":
            service = arguments.get("service")
            time_window = arguments.get("time_window", "10m")
            query = f'_time:{time_window} service.name:"{service}" severity:ERROR | stats count()'
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{VICTORIALOGS_URL}/select/logsql/query",
                    params={"query": query}
                )
                resp.raise_for_status()
                data = resp.json()
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "traces_list":
            service = arguments.get("service")
            limit = arguments.get("limit", 10)
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{VICTORIATRACES_URL}/select/jaeger/api/traces",
                    params={"service": service, "limit": limit}
                )
                resp.raise_for_status()
                data = resp.json()
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        elif name == "traces_get":
            trace_id = arguments.get("trace_id")
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}"
                )
                resp.raise_for_status()
                data = resp.json()
            return [types.TextContent(type="text", text=json.dumps(data, indent=2))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-obs",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
