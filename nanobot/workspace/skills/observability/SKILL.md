# Observability Skill

You have access to observability tools for logs and traces.

## Log Tools (VictoriaLogs)
- `logs_search` - search logs with LogsQL syntax
- `logs_error_count` - count errors per service over a time window

## Trace Tools (VictoriaTraces)
- `traces_list` - list recent traces for a service
- `traces_get` - fetch a specific trace by ID

## When asked "What went wrong?" or "Check system health"
Follow this exact investigation flow:
1. Call `logs_error_count` with time_range "10m" to check for recent errors
2. Call `logs_search` with query `_time:10m service.name:"Learning Management Service" severity:ERROR` to find error details and extract a trace_id
3. Call `traces_get` with the most recent trace_id found in the logs
4. Write a concise summary that mentions:
   - What the log evidence shows (service, error type, count)
   - What the trace evidence shows (which span failed, operation name)
   - The root cause in plain language

Never dump raw JSON. Always summarize findings in 3-5 sentences.

## When asked "Any errors in the last X minutes?"
1. Call `logs_error_count` first
2. If errors exist, call `logs_search` to get details
3. If a trace_id is visible, call `traces_get`
4. Summarize concisely

## General rules
- Search logs before traces
- Extract trace_id from log results when available
- Keep responses helpful and actionable, not raw data dumps
