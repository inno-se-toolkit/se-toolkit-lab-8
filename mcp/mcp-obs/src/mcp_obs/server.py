import asyncio
import json
import os
from datetime import datetime, timedelta

import httpx
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Environment variables for Victoria services
VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

server = Server("mcp-obs")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="logs_search",
            description="Search logs by query and time range. Use LogsQL syntax. Example query: '_time:1h service.name:\"Learning Management Service\" severity:ERROR'",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "LogsQL query string"},
                    "limit": {"type": "integer", "description": "Maximum number of logs to return", "default": 50},
                    "time_range": {"type": "string", "description": "Time range like '1h', '30m', '24h'", "default": "1h"}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="logs_error_count",
            description="Count errors per service over a time window",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name to filter by", "default": "Learning Management Service"},
                    "time_range": {"type": "string", "description": "Time range like '1h', '30m'", "default": "1h"}
                },
            },
        ),
        types.Tool(
            name="traces_list",
            description="List recent traces for a service",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name to get traces for"},
                    "limit": {"type": "integer", "description": "Maximum number of traces", "default": 10}
                },
                "required": ["service"],
            },
        ),
        types.Tool(
            name="traces_get",
            description="Fetch a specific trace by its ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string", "description": "Trace ID to fetch"}
                },
                "required": ["trace_id"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent]:
    if not arguments:
        arguments = {}
    
    if name == "logs_search":
        query = arguments.get("query")
        limit = arguments.get("limit", 50)
        async with httpx.AsyncClient() as client:
            url = f"{VICTORIALOGS_URL}/select/logsql/query"
            params = {"query": query, "limit": limit}
            resp = await client.get(url, params=params)
            result = resp.text[:5000] if resp.status_code == 200 else f"Error: {resp.status_code}"
            return [types.TextContent(type="text", text=result)]
    
    elif name == "logs_error_count":
        service = arguments.get("service", "Learning Management Service")
        time_range = arguments.get("time_range", "1h")
        query = f'_time:{time_range} service.name:"{service}" severity:ERROR'
        async with httpx.AsyncClient() as client:
            url = f"{VICTORIALOGS_URL}/select/logsql/query"
            resp = await client.get(url, params={"query": query})
            if resp.status_code == 200:
                lines = resp.text.strip().split('\n')
                count = len([l for l in lines if l.strip()])
                return [types.TextContent(type="text", text=f"Found {count} errors in {service} over {time_range}")]
            return [types.TextContent(type="text", text=f"Error querying logs: {resp.status_code}")]
    
    elif name == "traces_list":
        service = arguments.get("service")
        limit = arguments.get("limit", 10)
        async with httpx.AsyncClient() as client:
            url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces"
            resp = await client.get(url, params={"service": service, "limit": limit})
            if resp.status_code == 200:
                data = resp.json()
                traces = data.get("data", [])
                result = f"Found {len(traces)} traces for service '{service}':\n"
                for trace in traces[:limit]:
                    trace_id = trace.get("traceID", "unknown")
                    spans = len(trace.get("spans", []))
                    result += f"  - {trace_id} ({spans} spans)\n"
                return [types.TextContent(type="text", text=result)]
            return [types.TextContent(type="text", text=f"Error: {resp.status_code}")]
    
    elif name == "traces_get":
        trace_id = arguments.get("trace_id")
        async with httpx.AsyncClient() as client:
            url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}"
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                trace = data.get("data", [{}])[0]
                spans = trace.get("spans", [])
                result = f"Trace {trace_id} has {len(spans)} spans:\n"
                for span in spans[:20]:
                    op = span.get("operationName", "unknown")
                    duration = span.get("duration", 0) / 1000
                    result += f"  - {op} ({duration:.2f}ms)\n"
                return [types.TextContent(type="text", text=result)]
            return [types.TextContent(type="text", text=f"Trace {trace_id} not found")]
    
    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-obs",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())

