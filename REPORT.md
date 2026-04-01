# Lab 8 — Report
Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Q: What is the agentic loop?**
```
The agentic loop is the iterative reasoning and action cycle that autonomous AI agents follow to accomplish tasks. It typically consists of these core steps:
 1 Perceive/Observation — The agent gathers information about its environment or current state (reading files, checking outputs, receiving user input).
 2 Reason/Plan — The agent analyzes the information, decides what to do next, and forms a plan or selects an action.
 3 Act — The agent executes the chosen action (calling a tool, running a command, writing a file, sending a message).
 4 Reflect/Learn — The agent observes the outcome of its action, evaluates success, and adjusts its approach if needed.
Then the loop repeats until the task is complete.
This loop enables agents to handle complex, multi-step tasks autonomously by continuously adapting based on feedback from their actions.
```

**Q: What labs are available in our LMS?**
```
The agent had no LMS tools at this stage and could not answer — it said it does not have access to the LMS system.
```

## Task 1B — Agent with LMS tools

**Q: What labs are available?**
```
Here are the 8 labs available in your LMS:
 ID  Lab Title
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   Lab 08 — The Agent is the Interface
```

**Q: Describe the architecture of the LMS system**
```
The LMS system consists of the following services:
- Backend API (FastAPI) — handles items, learners, interactions, analytics, pipeline endpoints
- PostgreSQL — primary database
- Caddy — reverse proxy serving the React dashboard and API
- React frontend — analytics dashboard
- ETL pipeline — syncs data from autochecker API
- Observability stack: VictoriaLogs, VictoriaTraces, OTel Collector
- Qwen Code API — LLM proxy
- Nanobot — AI agent interface
```

## Task 1C — Skill prompt

**Q: Show me the scores (without specifying a lab)**
```
The agent fetched all labs and returned a full table with completion rates and average scores per task for all 8 labs:
- Lab 01: 100.0% (258/258)
- Lab 02: 89.1% (131/147)
- Lab 03: 89.1% (156/175)
- Lab 04: 97.2% (239/246)
- Lab 05: 98.8% (247/250)
- Lab 06: 98.4% (242/246)
- Lab 07: 99.6% (238/239)
- Lab 08: 0.0% (0/0) — no submissions yet
```

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
