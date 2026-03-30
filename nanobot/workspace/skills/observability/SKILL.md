---
name: observability
description: Use observability MCP tools for logs and traces
always: true
---

Use observability MCP tools when the user asks about errors, failures, logs, traces, recent backend issues, "What went wrong?", or "Check system health".

Rules:

- For recent errors, start with `mcp_obs_logs_error_count` on a fresh narrow window.
- Prefer narrow time windows such as `2m`, `5m`, `10m`, `30m`, or `1h`.
- When investigating LMS/backend failures, first inspect the most likely failing service with `mcp_obs_logs_search` and `service_name` set to `Learning Management Service`.
- Look for the newest relevant error log and extract its `trace_id` if present.
- If a relevant `trace_id` is available, use `mcp_obs_traces_get` for that trace.
- Use `mcp_obs_traces_list` only when the user explicitly asks for recent traces or when logs do not contain a usable `trace_id`.
- Summarize findings concisely instead of dumping raw JSON.
- A good investigation answer should explicitly mention:
  - log evidence
  - trace evidence when available
  - the affected service
  - the failing operation or endpoint
  - the likely root cause
- For "What went wrong?" and "Check system health", do not answer from chat memory or prior summaries.
- For those prompts, always run fresh observability tool calls before answering.
- For "What went wrong?", perform a one-shot investigation:
  1. count recent errors
  2. inspect recent error logs for the most likely failing service
  3. extract the best recent `trace_id`
  4. inspect the matching trace
  5. return one short coherent explanation
- For "Check system health", check recent backend/LMS errors first. If there are no recent errors, say the system looks healthy. If there are errors, investigate them with logs and traces before answering.
- Do not dump raw JSON unless the user explicitly asks for it.
- When there are no matching recent errors, say so clearly.
