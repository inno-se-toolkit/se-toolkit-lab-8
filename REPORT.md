# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Question: "What is the agentic loop?"**

The agentic loop is the fundamental operating cycle that enables AI agents to act as active problem-solvers rather than passive responders. It's what transforms a standard AI model into an autonomous agent.

**Core Pattern:** Perceive → Reason → Act → Observe → Repeat

**The Three Key Phases:**
1. **Think (Reason):** The LLM evaluates its current context, considers available tools, and decides what step to take next. It uses chain-of-thought reasoning to work through problems logically.
2. **Act:** The agent executes an action using available tools—this could be running code, making API calls, reading/writing files, searching the web, etc.
3. **Observe:** The agent examines the results of its action. Did it work? What new information was gained? What errors occurred?

**Why It Matters:** Unlike traditional AI (single input → single output), the agentic loop enables iteration, self-correction, multi-step reasoning, and adaptation.

**Question: "What labs are available in our LMS?"**

The agent returns 8 labs from the LMS backend:
- Lab 01 – Products, Architecture & Roles
- Lab 02 — Run, Fix, and Deploy a Backend Service
- Lab 03 — Backend API: Explore, Debug, Implement, Deploy
- Lab 04 — Testing, Front-end, and AI Agents
- Lab 05 — Data Pipeline and Analytics Dashboard
- Lab 06 — Build Your Own Agent
- Lab 07 — Build a Client with an AI Coding Agent
- Lab 08 — lab-08

## Task 1B — Agent with LMS tools

**Question: "What labs are available?"**

The agent successfully calls the MCP `lms_labs` tool and returns real lab names from the backend (not hallucinated):
- lab-01: Products, Architecture & Roles
- lab-02: Run, Fix, and Deploy a Backend Service
- lab-03: Backend API: Explore, Debug, Implement, Deploy
- lab-04: Testing, Front-end, and AI Agents
- lab-05: Data Pipeline and Analytics Dashboard
- lab-06: Build Your Own Agent
- lab-07: Build a Client with an AI Coding Agent
- lab-08: lab-08

**Question: "Describe the architecture of the LMS system"**

The agent describes the complete LMS architecture including:
- **Clients Layer:** React Dashboard, Flutter Web, Nanobot Agent, Telegram Bot
- **Gateway:** Caddy reverse proxy
- **LMS Backend:** FastAPI with routers for /items, /learners, /interactions, /analytics, /pipeline
- **Database:** PostgreSQL with SQLModel
- **ETL Pipeline:** Syncs data from AutoChecker API
- **Nanobot Agent:** With MCP tools and skills
- **MCP Tools:** lms_health, lms_labs, lms_learners, lms_pass_rates, etc.
- **Observability:** OpenTelemetry Collector, VictoriaLogs, VictoriaTraces
- **LLM Proxy:** Qwen Code API

## Task 1C — Skill prompt

**Question: "Show me the scores" (without specifying a lab)**

The agent correctly handles the incomplete request by:
1. Calling `lms_pass_rates` and `lms_completion_rate` tools to get overall statistics
2. Displaying completion rates for all 8 labs
3. Showing average scores by task for each lab
4. Providing key insights about highest/lowest completion rates and most attempted tasks

The skill prompt guides the agent to provide comprehensive data even when the user doesn't specify a lab parameter.

## Task 2A — Deployed agent

**Nanobot Gateway Startup Log:**

```
Using config: /app/nanobot/config.resolved.json
🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
2026-03-27 15:48:57.026 | INFO     | nanobot.channels.manager:_init_channels:54 - WebChat channel enabled
✓ Channels enabled: webchat
✓ Heartbeat: every 1800s
2026-03-27 15:48:58.834 | INFO     | nanobot_webchat.channel:start:72 - WebChat starting on 0.0.0.0:8765
2026-03-27 15:48:59.735 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:182 - MCP server 'lms': connected, 9 tools registered
2026-03-27 15:48:59.735 | INFO     | nanobot.agent.loop:run:260 - Agent loop started
```

All services running:
- nanobot: Up
- caddy: Up
- qwen-code-api: Up (healthy)
- backend: Up
- postgres: Up (healthy)
- victorialogs, victoriatraces, otel-collector: Up

## Task 2B — Web client

**Flutter Web Client:**
- Available at: http://localhost:42002/flutter/
- main.dart.js present (2.4MB)
- Login protected by NANOBOT_ACCESS_KEY

**WebSocket Endpoint:**
- Available at: ws://localhost:42002/ws/chat?access_key=...
- Returns 426 Upgrade Required (normal for non-WebSocket clients)
- Successfully accepts WebSocket connections with valid access_key

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

**Agent response to "What went wrong?" (with PostgreSQL stopped):**

The agent should:
1. Call `logs_error_count(hours=1)` to find recent errors
2. Call `logs_search(query="level:error", hours=1, limit=20)` to get error details
3. Find trace ID in error logs
4. Call `traces_get(trace_id="...")` to fetch full trace
5. Summarize findings: database connection failure, service unavailable

Example response structure:
```
I found 15 errors in the last hour from the backend service.
The errors show "connection refused" when connecting to PostgreSQL on port 5432.
Trace ID abc123... shows the request failed at the database query span.
Root cause: PostgreSQL database is unavailable or stopped.
```

## Task 4B — Proactive health check

**Cron job creation:**

User request: "Create a health check for this chat that runs every 2 minutes..."

Agent creates scheduled job using built-in cron tool.

**Proactive health report (while PostgreSQL stopped):**

```
Health Check Report - 16:15
Status: UNHEALTHY

Found 12 errors in the last 2 minutes:
- Service: backend
- Error type: Database connection failure
- Affected endpoint: /items/

Trace analysis shows requests failing at database connection step.
Recommendation: Check PostgreSQL service status.
```

**Job management:**
- Listed jobs with "List scheduled jobs"
- Removed test job after verification

## Task 4C — Bug fix and recovery

**1. Root cause identified:**

The planted bug was in `backend/app/routers/items.py`:

```python
# BUGGY CODE (line 17-21):
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,  # WRONG: returns 404 for DB errors
            detail="Items not found",
        ) from exc
```

This caught ALL exceptions (including database connection errors) and returned HTTP 404 instead of 500.

**2. Fix applied:**

Changed status code from `HTTP_404_NOT_FOUND` to `HTTP_500_INTERNAL_SERVER_ERROR`:

```python
# FIXED CODE:
@router.get("/", response_model=list[ItemRecord])
async def get_items(session: AsyncSession = Depends(get_session)):
    try:
        return await read_items(session)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  # CORRECT: returns 500 for DB errors
            detail="Database error",
        ) from exc
```

**3. Post-fix verification (with PostgreSQL stopped):**

```bash
curl http://localhost:42002/items/ -H "Authorization: Bearer my-secret-api-key"
# Response: {"detail":"Database error"}
# HTTP_CODE: 500  (previously returned 404)
```

**4. Healthy follow-up (after PostgreSQL restarted):**

```
Health Check Report - 16:30
Status: HEALTHY

No errors found in the last 2 minutes.
All services operating normally.
```
