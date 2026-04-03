"""Tool specifications for the observability MCP server."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from mcp.types import Tool
from pydantic import BaseModel


@dataclass
class ToolSpec:
    """Specification for an MCP tool."""

    name: str
    description: str
    model: type[BaseModel]
    handler: Callable[..., Any]

    def as_tool(self) -> Tool:
        properties = {}
        required = []
        for field_name, field_info in self.model.model_fields.items():
            properties[field_name] = {
                "type": "string" if field_info.annotation is str else "integer",
                "description": field_info.description or "",
            }
            if field_info.is_required():
                required.append(field_name)
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={"type": "object", "properties": properties, "required": required},
        )


# --- Request models ---

class LogsSearchParams(BaseModel):
    query: str = "LogsQL query string (e.g. '_time:10m severity:ERROR')"
    limit: int = 20


class LogsErrorCountParams(BaseModel):
    service: str = "Learning Management Service"
    minutes: int = 60


class TracesListParams(BaseModel):
    service: str = "Learning Management Service"
    limit: int = 10


class TracesGetParams(BaseModel):
    trace_id: str = "Trace ID to fetch"


# --- Tool specs ---

TOOL_SPECS: list[ToolSpec] = []
TOOLS_BY_NAME: dict[str, ToolSpec] = {}


def register_tool(
    name: str, description: str, model: type[BaseModel]
) -> Callable[[Callable], Callable]:
    """Decorator to register a tool specification."""

    def decorator(handler: Callable) -> Callable:
        spec = ToolSpec(name=name, description=description, model=model, handler=handler)
        TOOL_SPECS.append(spec)
        TOOLS_BY_NAME[name] = spec
        return handler

    return decorator


@register_tool(
    name="mcp_obs_logs_search",
    description="Search VictoriaLogs using LogsQL. Use to find specific log entries by keyword, service, or severity. Example query: '_time:10m service.name:\"Learning Management Service\" severity:ERROR'",
    model=LogsSearchParams,
)
async def logs_search(client, args: LogsSearchParams) -> list[dict[str, Any]]:
    return await client.logs_search(query=args.query, limit=args.limit)


@register_tool(
    name="mcp_obs_logs_error_count",
    description="Count errors for a service over a time window. Use to quickly check if there are recent errors before diving into details.",
    model=LogsErrorCountParams,
)
async def logs_error_count(client, args: LogsErrorCountParams) -> dict[str, Any]:
    return await client.logs_error_count(service=args.service, minutes=args.minutes)


@register_tool(
    name="mcp_obs_traces_list",
    description="List recent traces for a service. Returns trace IDs and operation summaries.",
    model=TracesListParams,
)
async def traces_list(client, args: TracesListParams) -> list[dict[str, Any]]:
    return await client.traces_list(service=args.service, limit=args.limit)


@register_tool(
    name="mcp_obs_traces_get",
    description="Fetch a specific trace by ID. Use after finding a trace_id in logs to inspect the full request path and identify where errors occurred.",
    model=TracesGetParams,
)
async def traces_get(client, args: TracesGetParams) -> dict[str, Any]:
    return await client.traces_get(trace_id=args.trace_id)
