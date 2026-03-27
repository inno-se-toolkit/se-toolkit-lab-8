---
description: Observability investigation strategy for Lab 8
always: true
---

# Observability skill

Use the `mcp_lms_logs_*` and `mcp_lms_traces_*` tools for questions about errors, failures, slow requests, traces, logs, and system health.

## Tool map

- `mcp_lms_logs_search`: search recent logs by service, level, and keyword.
- `mcp_lms_logs_error_count`: count recent errors per service.
- `mcp_lms_traces_list`: list recent traces for a service.
- `mcp_lms_traces_get`: fetch a full trace by ID.

## Investigation flow

- For "Any errors in the last hour?" start with `mcp_lms_logs_error_count`.
- For "What went wrong?" or "Check system health", search recent backend errors first with `mcp_lms_logs_search`.
- If logs mention a trace ID, fetch the corresponding trace with `mcp_lms_traces_get`.
- If there is no trace ID in the logs, list recent backend traces with `mcp_lms_traces_list` and correlate by time.
- Summarize findings in plain language: affected service, failing operation, error event, status, and trace evidence.
- If no recent errors are found, say the system looks healthy.

## Cron usage

- When asked to create a recurring health check, use the cron tool.
- The scheduled prompt should check recent backend errors, inspect a trace if needed, and post a short summary to the same chat.
