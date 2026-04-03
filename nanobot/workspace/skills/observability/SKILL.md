---
name: observability
description: Use observability MCP tools to investigate errors, logs, and traces
always: true
---

# Observability Skill

You have access to observability tools that let you query VictoriaLogs (structured logs) and VictoriaTraces (distributed traces) for the LMS backend.

## Available Tools

- `mcp_obs_logs_error_count` — Count errors for a service over a time window. Use this FIRST when asked about errors to quickly check if there are any.
- `mcp_obs_logs_search` — Search logs using LogsQL. Use to find specific log entries, extract trace IDs, or investigate error details.
- `mcp_obs_traces_list` — List recent traces for a service. Returns trace IDs and operation summaries.
- `mcp_obs_traces_get` — Fetch a specific trace by ID. Use after finding a trace_id in logs to inspect the full request path.

## Strategy

### When user asks about errors (e.g., "any errors in the last hour?"):

1. Call `mcp_obs_logs_error_count` with the LMS backend service name and appropriate time window
2. If errors exist, call `mcp_obs_logs_search` to find the specific error entries and extract trace IDs
3. If you find a trace_id, call `mcp_obs_traces_get` to inspect the failing request path
4. Summarize findings concisely — don't dump raw JSON

### When user asks about a specific issue:

1. Use `mcp_obs_logs_search` with a targeted LogsQL query
2. Extract relevant trace IDs from log entries
3. Use `mcp_obs_traces_get` to trace the request flow
4. Report what you found in plain language

## Query Patterns

Common LogsQL queries:
- `_time:10m service.name:"Learning Management Service" severity:ERROR` — recent LMS errors
- `_time:1h service.name:"Learning Management Service" event:db_query` — database queries
- `trace_id:"<id>"` — all logs for a specific trace

## Response Style

- Keep responses concise and focused on what the user asked
- Summarize findings in plain language
- Only include technical details (trace IDs, query strings) when they help the user understand
- Never dump raw JSON — extract and explain the relevant parts
- If no errors found, say so clearly
