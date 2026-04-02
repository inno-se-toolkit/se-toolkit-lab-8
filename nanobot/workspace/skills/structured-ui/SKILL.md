---
name: structured-ui
description: Use interactive UI messages on supported chat channels when the user needs to choose
always: true
---

# Structured UI Skill

Use interactive UI messages on supported chat channels when the next useful
step is a real user choice between multiple valid options.

## Strategy

- Prefer `mcp_webchat_ui_message` over a plain text list or follow-up question
  when the user needs to choose among multiple concrete options.
- Use interactive choices for selection tasks such as picking a lab, choosing
  from search results, selecting an action, or narrowing an ambiguous request.
- If there is only one sensible next option, respond normally instead of
  forcing a choice UI.
- If the interactive tool is unavailable on the current channel, fall back to a
  concise plain text question or list.

## Response style

- Do not send a separate plain text preamble such as "I'll check" before the
  interactive choice. Send the choice UI directly, or use one brief
  `composite` payload if short explanatory text is genuinely helpful.
- Use `type: "choice"` to present multiple options.
- Use `type: "confirm"` for a confirmation prompt.
- Use `type: "composite"` to combine explanatory text with an interactive part.
- Read the current chat ID from the runtime context and pass it as the
  `chat_id` argument so the payload is routed to the active WebSocket client.
