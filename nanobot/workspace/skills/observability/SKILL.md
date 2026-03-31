---
name: observability
description: Use VictoriaLogs and VictoriaTraces to investigate errors and traces
always: true
---

# Observability Skill

Use observability MCP tools to investigate errors, logs, and traces in the system.

## Available tools

- `logs_search` — search logs in VictoriaLogs using LogsQL query
- `logs_error_count` — count errors per service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a specific trace by ID

## Strategy

- When the user asks about errors, start with `logs_error_count` for a quick overview
- Use `logs_search` to find specific error details and extract `trace_id` from error logs
- Use `traces_get` with the `trace_id` to see the full request flow and identify where it failed
- Summarize findings concisely — don't dump raw JSON

## LogsQL syntax

- Time range: `_time:10m` for last 10 minutes, `_time:1h` for last hour
- Severity: `severity:ERROR` for errors, `severity:WARNING` for warnings
- Service: `service.name:"Learning Management Service"`
- Combined: `_time:10m service.name:"Learning Management Service" severity:ERROR`

## Response format

- Start with a summary: "Found X errors in the last Y minutes"
- List affected services with counts
- If a trace is relevant, describe the failure point in plain language
- End with actionable insight if possible

## Example flow

1. User: "Any errors in the last hour?"
2. You: Call `logs_error_count(minutes=60)` → "Found 5 errors: 3 in Learning Management Service, 2 in backend"
3. If user asks for details: Call `logs_search(query='_time:10m severity:ERROR', limit=10)`
4. Extract `trace_id` from a relevant error log
5. Call `traces_get(trace_id="...")` to see the full failure context
6. Summarize: "The request failed at the database query step — PostgreSQL connection was closed"
