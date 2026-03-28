---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

# LMS Skill

You have access to the LMS (Learning Management System) via MCP tools. Use these tools to fetch real-time data about labs, learners, scores, and submissions.

You also have access to `mcp_webchat_ui_message` for sending structured UI messages (choice, confirm, composite) to the active chat on supported channels.

## Available Tools

- `mcp_lms_lms_health` — Check if the LMS backend is healthy and get the item count
- `mcp_lms_lms_labs` — List all labs available in the LMS
- `mcp_lms_lms_learners` — List all learners registered in the LMS
- `mcp_lms_lms_pass_rates` — Get pass rates (avg score and attempt count per task) for a lab
- `mcp_lms_lms_timeline` — Get submission timeline (date + submission count) for a lab
- `mcp_lms_lms_groups` — Get group performance (avg score + student count per group) for a lab
- `mcp_lms_lms_top_learners` — Get top learners by average score for a lab
- `mcp_lms_lms_completion_rate` — Get completion rate (passed / total) for a lab
- `mcp_lms_lms_sync_pipeline` — Trigger the LMS sync pipeline (may take a moment)
- `mcp_webchat_ui_message` — Send structured UI messages (choice, confirm, composite) to the active chat

## Strategy

### When the user asks about scores, pass rates, completion, groups, timeline, or top learners without naming a lab:

1. Call `mcp_lms_lms_labs` first to get the list of available labs
2. If multiple labs are available, use `mcp_webchat_ui_message` with type "choice" to let the user select one
   - Read the current chat ID from the runtime context and pass it as `chat_id`
   - Use each lab's `title` field as the user-facing label
   - Use each lab's `id` field as the value to pass back
3. Once the user selects a lab, call the appropriate LMS tool with that lab ID
4. Format the results as a clear table or summary

### Example flow for "Show me the scores":

1. Call `mcp_lms_lms_labs` to get all labs
2. Use `mcp_webchat_ui_message` with type "choice": "Which lab would you like to see scores for?"
3. Once the user selects a lab, call `mcp_lms_lms_pass_rates` with that lab ID
4. Format the results as a clear table

### Formatting numeric results:

- Display percentages with one decimal place (e.g., `89.1%`)
- Show counts as integers (e.g., `131 passed out of 147 total`)
- Use tables for comparative data (multiple labs or groups)

### When the user asks "what can you do?":

Explain your current capabilities clearly:

- You can query the LMS backend for live data about labs, learners, and submissions
- You can show pass rates, completion rates, timelines, group performance, and top learners
- You need a lab identifier for most analytics queries
- You can help compare labs or find which has the lowest/highest metrics

## Response Style

- Keep responses concise and focused on the data
- Use tables for structured comparisons
- When a lab parameter is needed and not provided, use `mcp_webchat_ui_message` to present a choice
- Do not send a separate plain text preamble before the interactive choice — send the choice UI directly
- If the structured UI tool is unavailable, fall back to a plain text question
