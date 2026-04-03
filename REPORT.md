# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

Command:
uv run nanobot agent -c ./config.json -m "Hello!"

Output:
[вставь сюда реальный вывод из терминала для Hello]

## Task 1B — Agent with LMS tools

Command:
uv run nanobot agent -c ./config.json -m "What labs are available?"

Output:
🐈 nanobot
I'll check what labs are available in the LMS system for you.

🐈 nanobot
Here are the available labs:

1 Lab 01 – Products, Architecture & Roles
2 Lab 02 — Run, Fix, and Deploy a Backend Service
3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4 Lab 04 — Testing, Front-end, and AI Agents
5 Lab 05 — Data Pipeline and Analytics Dashboard
6 Lab 06 — Build Your Own Agent
7 Lab 07 — Build a Client with an AI Coding Agent
8 Lab 08

Would you like more information about any specific lab?

## Task 1C — Skill prompt

Command:
uv run nanobot agent -c ./config.json -m "What tasks are in Lab 8?"

Output:
🐈 nanobot
I'll check what tasks are in Lab 8 for you. First, let me get more specific information about Lab 08 from the LMS system.

🐈 nanobot
I apologize for the confusion. Let me try to get information about Lab 8 using the available LMS functions. Since "lab-08" appears in the list of labs, I'll try to get more details about it:

🐈 nanobot
Let me try another approach to get information about Lab 8:

🐈 nanobot
Let me try to get more general information about Lab 8:

🐈 nanobot
I see that the web search didn't provide specific information about Lab 8 in the SE toolkit. Let me try to approach this differently. Since we know Lab 8 exists in the system, let me try to get information about it using other available methods:

🐈 nanobot
Let me try a more focused search for lab materials in the current workspace:

🐈 nanobot
Now I can see the structure better. Let me check the lab directory:

🐈 nanobot
Let me check the tasks directory:

🐈 nanobot
Let me check both required and optional tasks:

🐈 nanobot
Let me also check the optional tasks:

🐈 nanobot
Let me check if there are any lab-specific directories:

🐈 nanobot
Let me look for any markdown files that might contain information about Lab 8:

🐈 nanobot
Let me check the lab.md file in the wiki directory, as it might contain information about Lab 8:

🐈 nanobot
Perfect! Now I can see that we're in the se-toolkit-lab-8 repository. Let me check the README.md file to get more information about this specific lab:

🐈 nanobot
Now I have the information about Lab 8! Based on the README.md file, here are the tasks in Lab 8 - "The Agent is the Interface":

Required Tasks:

1 Task 1: Set Up the Agent — Install nanobot, configure Qwen API, add MCP tools, write skill prompt
2 Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket channel + Flutter chat UI
3 Task 3: Give the Agent New Eyes — Explore observability data, write log/trace MCP tools
4 Task 4: Diagnose a Failure and Make the Agent Proactive — Investigate a failure, schedule in-chat health checks, fix a planted bug

Optional Task:

5 Task 1: Add a Telegram Bot Client — Same agent, different interface

The lab focuses on building an AI agent (nanobot) that serves as an intelligent interface to the LMS system. Users can ask questions in natural language like "which lab has the lowest pass rate?" or "any errors in the last hour?" and the agent figures out which API calls to make.

The architecture includes the agent connecting to various components like the LMS backend, observability tools (logs/traces), and providing interfaces for different clients (browser, Telegram).
## Task 1B — Agent with LMS tools

Command:
uv run nanobot agent -c ./config.json -m "What labs are available?"

Output:
🐈 nanobot
I'll check what labs are available in the LMS system for you.

🐈 nanobot
Here are the available labs:

1 Lab 01 – Products, Architecture & Roles
2 Lab 02 — Run, Fix, and Deploy a Backend Service
3 Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4 Lab 04 — Testing, Front-end, and AI Agents
5 Lab 05 — Data Pipeline and Analytics Dashboard
6 Lab 06 — Build Your Own Agent
7 Lab 07 — Build a Client with an AI Coding Agent
8 Lab 08
## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

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
