# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Prompt: What is the agentic loop?

The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core stages:

The Loop

1. Perceive — Gather information about the current state (read files, check outputs, observe environment)
2. Think/Reason — Analyze the situation, plan next steps, decide what to do
3. Act — Execute actions using available tools (write files, run commands, make API calls)
4. Observe — Check the results of the action, detect changes or errors
5. Repeat — Continue the loop until the goal is achieved or a stopping condition is met

Key Characteristics

- Autonomous — The agent drives the process without constant human input
- Iterative — Multiple passes through the loop may be needed
- Adaptive — Each iteration can adjust based on new information
- Goal-directed — The loop continues until the objective is met

Example in Practice

User: "Fix the bug in main.py"

Agent Loop:
1. Perceive → Read main.py to understand the code
2. Think → Identify the bug and plan a fix
3. Act → Edit the file with the correction
4. Observe → Run tests to verify the fix works
5. Repeat → If tests fail, go back to step 2

This loop is what distinguishes agentic systems from simple question-answer chatbots. Agents can take multi-step actions, recover from errors, and work toward complex goals independently.

### Prompt: What labs are available in our LMS?

Based on my exploration of the LMS workspace, here are the available labs in this system:

Lab 8 — The Agent is the Interface

This is the current lab you're working on. It has the following tasks:

Required Tasks:

1. Task 1 — Set Up the Agent (install nanobot, configure Qwen API, add MCP tools, write skill prompt)
2. Task 2 — Deploy and Connect a Web Client (Dockerize nanobot, add WebSocket channel + Flutter chat UI)
3. Task 3 — Give the Agent New Eyes (explore observability data, write log/trace MCP tools)
4. Task 4 — Diagnose a Failure and Make the Agent Proactive (investigate a failure, schedule in-chat health checks, fix a planted bug)

Optional Tasks:

1. Task 1 — Add a Telegram Bot Client (same agent, different interface)

System Architecture

The LMS system includes:

- LMS Backend — FastAPI application with PostgreSQL database
- Nanobot Agent — AI agent interface with tools and skills
- Web Client — Flutter-based chat UI at /flutter
- Observability Stack — OpenTelemetry Collector, VictoriaLogs, VictoriaTraces
- Platform Services — Caddy reverse proxy, Qwen Code API

The agent can query data about learners, items, and interactions through MCP tools, and can also access logs and traces for system health monitoring.

Would you like me to read the details of any specific task or explore a particular part of the system?

## Task 1B — Agent with LMS tools

### Prompt: What labs are available?

Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Would you like more details about any specific lab, such as completion rates, pass rates, or submission timelines?

### Prompt: Which lab has the lowest pass rate?

Based on the completion rates:

- Lab 01: 93.9% (108 passed / 115 total)
- Lab 02-08: 0.0% (0 passed / 0 total - no submissions yet)

Lab 01 has the lowest pass rate among labs that have actual submissions at 93.9%.

However, if we consider labs with no submissions (0% completion rate), then Labs 02-08 all have 0% pass rates because no students have submitted work for them yet.

If you're looking for the lab with the lowest pass rate among those with actual student attempts, Lab 01 is the only one with data, so it technically has both the highest and lowest pass rate among completed labs.

## Task 1C — Skill prompt

### Prompt: Show me the scores

There are 8 labs available. Which lab would you like to see scores for? Here are the options:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

Or would you like me to show scores for all labs, or perhaps the top learners across a specific lab?

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
