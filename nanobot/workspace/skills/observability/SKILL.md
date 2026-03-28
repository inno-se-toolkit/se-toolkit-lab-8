---
name: observability
description: Use observability tools to inspect logs and traces
always: true
---

# Observability Skills

You have access to the following MCP tools:

- `logs_search` – search logs with LogsQL
- `logs_error_count` – count errors per service in a time window
- `traces_list` – list recent traces for a service
- `traces_get` – get a specific trace by ID

When asked about errors or system health:
1. First use `logs_error_count` to see if there are recent errors.
2. If errors exist, use `logs_search` with a query that includes `severity:ERROR` and the relevant service.
3. Extract a `trace_id` from the error logs.
4. Use `traces_get` with that trace ID to examine the full request path.
5. Summarize your findings concisely – do not dump raw JSON.

Use the time window specified by the user (e.g., "last 10 minutes").

For the LMS backend, the service name is "Learning Management Service".

Example queries:
- Count errors: `_time:10m service.name:"Learning Management Service" severity:ERROR | stats count()`
- Search errors: `_time:10m service.name:"Learning Management Service" severity:ERROR`

Keep responses brief and helpful.
