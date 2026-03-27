---
description: LMS tool strategy for Lab 8
always: true
---

# LMS skill

Use the `mcp_lms_*` tools whenever the user asks about labs, scores, learners, completion, sync, or system architecture.

## Tool map

- `mcp_lms_lms_health`: backend reachability and item count.
- `mcp_lms_lms_labs`: list available labs.
- `mcp_lms_lms_learners`: list learners.
- `mcp_lms_lms_pass_rates`: task-level pass rates for one lab.
- `mcp_lms_lms_timeline`: submission timeline for one lab.
- `mcp_lms_lms_groups`: group performance for one lab.
- `mcp_lms_lms_top_learners`: top learners for one lab.
- `mcp_lms_lms_completion_rate`: completion summary for one lab.
- `mcp_lms_lms_sync_pipeline`: trigger a data sync when the user explicitly asks to refresh data.

## Strategy

- If the user asks what labs are available, call `mcp_lms_lms_labs`.
- If the user asks for scores, pass rates, completion, timeline, groups, or top learners and does not specify a lab, first list the labs or ask which lab they mean.
- If the user asks about the LMS architecture, combine `mcp_lms_lms_health` and `mcp_lms_lms_labs` with the known system context: backend, PostgreSQL, Caddy, Qwen Code API, Nanobot, and the observability stack.
- Format percentages with one decimal place when possible and keep lists short.
- When the user asks "what can you do?", explain the current LMS and observability capabilities and mention that answers are grounded in tools.
