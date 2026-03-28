# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### "What is the agentic loop?"

The agentic loop is the fundamental cycle that an AI agent follows to accomplish tasks autonomously. It typically consists of these core stages:

1. **Perceive** — Gather information about the current state (user input, environment, tool outputs, etc.)
2. **Reason/Plan** — Analyze the situation, determine goals, and decide what actions to take
3. **Act** — Execute actions using available tools (file operations, API calls, shell commands, etc.)
4. **Observe** — Receive feedback from the actions (success, failure, new information)
5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met

Key Characteristics:
- **Iterative** — The agent doesn't just respond once; it can take multiple steps
- **Goal-directed** — Each iteration moves toward completing an objective
- **Adaptive** — The agent adjusts its plan based on observations and feedback
- **Autonomous** — The agent decides what to do next without constant human guidance

### "What labs are available in our LMS?" (before MCP tools)

The agent could not access real LMS data. It explored local files and responded:

> Based on my exploration of the codebase, I can tell you about the labs available in the LMS:
> 
> The LMS stores labs as items with type="lab" in the database. Based on the code and test fixtures, the system supports multiple labs with identifiers like: lab-01, lab-02, lab-03, lab-04, etc.
> 
> To see which labs are currently available in your running LMS instance, you can query the API directly or use the MCP tool (if nanobot is configured with LMS tools).


## Task 1B — Agent with LMS tools

### "What labs are available?"

The agent successfully called the MCP tool and returned real lab data:

> Here are the available labs:
> 
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 – Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. lab-08

### "Is the LMS backend healthy?"

> Yes, the LMS backend is healthy! It's currently tracking 56 items.

### "Which lab has the lowest pass rate?"

The agent chained multiple tool calls to answer:

> Based on the completion rates for all labs:
> 
> | Lab | Completion Rate | Passed | Total |
> |-----|-----------------|--------|-------|
> | Lab 01 | 100.0% | 258 | 258 |
> | Lab 02 | 89.1% | 131 | 147 |
> | Lab 03 | 89.1% | 156 | 175 |
> | Lab 04 | 96.7% | 238 | 246 |
> | Lab 05 | 98.4% | 246 | 250 |
> | Lab 06 | 98.4% | 242 | 246 |
> | Lab 07 | 99.6% | 236 | 237 |
> | Lab 08 | 0.0% | 0 | 0 |
> 
> Lab 08 (lab-08) has the lowest pass rate at 0.0%, though this appears to be because no students have submitted yet (0 total submissions).
> 
> Among labs with actual submissions, Lab 02 and Lab 03 are tied for the lowest pass rate at 89.1%.

## Task 1C — Skill prompt

### "Show me the scores" (without specifying a lab)

With the LMS skill prompt, the agent now asks for clarification when the lab is not specified:

> Which lab would you like to see scores for?
> 
> 1. Lab 01 – Products, Architecture & Roles
> 2. Lab 02 — Run, Fix, and Deploy a Backend Service
> 3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
> 4. Lab 04 — Testing, Front-end, and AI Agents
> 5. Lab 05 – Data Pipeline and Analytics Dashboard
> 6. Lab 06 — Build Your Own Agent
> 7. Lab 07 — Build a Client with an AI Coding Agent
> 8. lab-08
> 
> Please let me know which lab you're interested in, or I can show you scores for all of them.

The skill prompt teaches the agent to:
- Call `mcp_lms_labs` first when a lab parameter is needed but not provided
- Ask the user to choose which lab
- Use interactive UI on supported channels for the choice

## Task 2A — Deployed agent

Nanobot gateway startup log excerpt:

```
nanobot-1  | Using config: /tmp/nanobot/config.resolved.json
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | ✓ Heartbeat: every 1800s
nanobot-1  | MCP server 'lms': connected, 9 tools registered
nanobot-1  | MCP server 'webchat': connected, 1 tools registered
```

## Task 2B — Web client

WebSocket test response:

```json
{
  "type": "text",
  "content": "Here are the available labs in the LMS:\n\n| ID | Title |\n|----|-------|\n| 1 | Lab 01 – Products, Architecture & Roles |\n| 2 | Lab 02 — Run, Fix, and Deploy a Backend Service |\n| 3 | Lab 03 — Backend API: Explore, Debug, Implement, Deploy |\n| 4 | Lab 04 — Testing, Front-end, and AI Agents |\n| 5 | Lab 05 – Data Pipeline and Analytics Dashboard |\n| 6 | Lab 06 — Build Your Own Agent |\n| 7 | Lab 07 — Build a Client with an AI Coding Agent |\n| 8 | lab-08 |\n\nWould..."
}
```

The Flutter web client is accessible at `http://localhost:42002/flutter`. Users can log in with `NANOBOT_ACCESS_KEY` and chat with the agent. The agent responds with real LMS backend data via MCP tools.

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
