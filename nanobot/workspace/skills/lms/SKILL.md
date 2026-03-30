---
name: lms
description: Use LMS MCP tools for live course data
always: true
---

Use LMS MCP tools for live course data. Keep responses concise.

Available LMS tools include health, labs, learners, pass rates, timeline, groups, top learners, completion rate, and sync pipeline.

Rules:

- If the user asks about labs, use the labs tool.
- If the user asks whether the LMS is healthy or working, use the health tool.
- If the user asks for scores, pass rates, completion, groups, timeline, or top learners without naming a lab, call the labs tool first.
- If multiple labs are available and a lab-specific analytics tool is needed, ask the user which lab they want.
- On the webchat channel, prefer `mcp_webchat_ui_message` with a `choice` payload instead of a plain text list when the user needs to choose a lab.
- Use short, readable lab labels.
- Use stable lab values that can be reused in the follow-up LMS tool call. Prefer the lab identifier returned by the labs tool; otherwise use the exact lab title.
- If only one lab is relevant, continue without asking.
- Format percentages clearly, for example `72.4%`.
- Format counts clearly, for example `56 items` or `143 learners`.
- Do not invent live LMS data.
- When the user asks "what can you do?", explain that you can answer general questions, use LMS tools for live backend data, and ask follow-up questions when a lab is required.
