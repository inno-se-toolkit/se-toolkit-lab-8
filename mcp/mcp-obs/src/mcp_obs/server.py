from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_obs.observability import ObservabilityClient

_logs_url: str = ""
_traces_url: str = ""

server = Server("obs")


class LogsSearchQuery(BaseModel):
    keyword: str | None = Field(default=None)
    time_window: str = Field(default="10m")
    service_name: str | None = Field(default=None)
    severity: str | None = Field(default=None)
    event: str | None = Field(default=None)
    limit: int = Field(default=20, ge=1, le=200)


class LogsErrorCountQuery(BaseModel):
    time_window: str = Field(default="10m")
    service_name: str | None = Field(default=None)
    limit: int = Field(default=200, ge=1, le=1000)


class TracesListQuery(BaseModel):
    service_name: str
    limit: int = Field(default=10, ge=1, le=50)


class TracesGetQuery(BaseModel):
    trace_id: str


def _client() -> ObservabilityClient:
    if not _logs_url:
        raise RuntimeError(
            "VictoriaLogs URL not configured. Set NANOBOT_VICTORIALOGS_URL."
        )
    if not _traces_url:
        raise RuntimeError(
            "VictoriaTraces URL not configured. Set NANOBOT_VICTORIATRACES_URL."
        )
    return ObservabilityClient(_logs_url, _traces_url)


def _text(data: Any) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False))]


async def _logs_search(args: LogsSearchQuery) -> list[TextContent]:
    result = await _client().logs_search(
        keyword=args.keyword,
        time_window=args.time_window,
        service_name=args.service_name,
        severity=args.severity,
        event=args.event,
        limit=args.limit,
    )
    return _text(result)


async def _logs_error_count(args: LogsErrorCountQuery) -> list[TextContent]:
    result = await _client().logs_error_count(
        time_window=args.time_window,
        service_name=args.service_name,
        limit=args.limit,
    )
    return _text(result)


async def _traces_list(args: TracesListQuery) -> list[TextContent]:
    result = await _client().traces_list(
        service_name=args.service_name,
        limit=args.limit,
    )
    return _text(result)


async def _traces_get(args: TracesGetQuery) -> list[TextContent]:
    result = await _client().traces_get(trace_id=args.trace_id)
    return _text(result)


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
    "Search VictoriaLogs by keyword, service, severity, event, and time window.",
    LogsSearchQuery,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count error logs per service over a time window.",
    LogsErrorCountQuery,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces for a service from VictoriaTraces.",
    TracesListQuery,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch and summarize a specific trace by trace ID from VictoriaTraces.",
    TracesGetQuery,
    _traces_get,
)


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


async def amain() -> None:
    global _logs_url, _traces_url
    _logs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "")
    _traces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "")
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


def main() -> None:
    asyncio.run(amain())
