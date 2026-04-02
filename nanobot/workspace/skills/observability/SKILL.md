# Observability Skill

You have access to observability tools for logs and traces:

## Log Tools (VictoriaLogs)
- `logs_search` - search logs with LogsQL syntax. Example: `_time:1h service.name:"Learning Management Service" severity:ERROR`
- `logs_error_count` - count errors per service over a time window

## Trace Tools (VictoriaTraces)
- `traces_list` - list recent traces for a service
- `traces_get` - fetch a specific trace by ID

## Rules
- When user asks "any errors", first use `logs_error_count` to check if errors exist
- If errors exist, use `logs_search` to find them and extract trace_id
- Use `traces_get` to inspect the full trace of an error
- Summarize findings concisely - don't dump raw JSON
- Keep responses helpful and actionable
