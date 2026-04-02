# Lab 8 — Report

## Task 1A — Bare agent

**Q: What is the agentic loop?**
```
The agentic loop is the iterative reasoning and action cycle that autonomous AI agents follow to accomplish tasks. It consists of four core steps:
 1 Perceive — Gather information about the environment (reading files, checking outputs, receiving user input)
 2 Reason — Analyze information, decide what to do next, form a plan
 3 Act — Execute the chosen action (call tools, run commands, write files, send messages)
 4 Reflect — Observe outcomes, evaluate success, adjust approach if needed
This loop enables agents to handle complex, multi-step tasks autonomously by continuously adapting based on feedback.
```

**Q: What labs are available in our LMS?**
```
Based on the OpenAPI spec and the backend structure, here are the 8 labs available in your LMS:
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   Lab 08 — The Agent is the Interface
(Agent answered from training knowledge — no LMS tools were connected yet)
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
The LMS is a microservices-based platform. Key services:
 Service           Technology       Port        Purpose
 Caddy             Caddy 2.11       42002       Reverse proxy, routes traffic, serves SPAs
 LMS Backend       FastAPI          42001       Core API: items, learners, interactions, analytics
 PostgreSQL        Postgres 18.3    42004       Primary database
 Qwen Code API     Custom           42005       LLM gateway for AI agent
 Nanobot           nanobot          8765/18790  AI agent with MCP tools
 OTEL Collector    OpenTelemetry    4317        Collects traces/logs
 VictoriaLogs      VictoriaMetrics  42010       Log storage
 VictoriaTraces    VictoriaMetrics  42011       Trace storage
```

## Task 1C — Skill prompt

**Q: Show me the scores** (without specifying a lab)

The skill prompt instructs the agent to ask which lab when none is specified. Agent response:
```
Which lab would you like to see scores for? Here are the available labs:
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   Lab 08 — The Agent is the Interface

Please specify which lab you would like to see scores for.
```

## Task 2A — Deployed agent
**Nanobot gateway startup log (excerpt):**
2026-04-02 11:51:02.599 | INFO | nanobot.channels.manager:_init_channels:58 - WebChat channel enabled
✓ Channels enabled: webchat
2026-04-02 11:51:05.875 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
2026-04-02 11:51:05.876 | DEBUG | nanobot.agent.tools.mcp:connect_mcp_servers:226 - MCP: registered tool 'mcp_lms_lms_labs' from server 'lms'
2026-04-02 11:51:05.877 | INFO | nanobot.agent.tools.mcp:connect_mcp_servers:246 - MCP server 'lms': connected, 9 tools registered
2026-04-02 11:51:06.426 | INFO | nanobot.agent.loop:run:280 - Agent loop started

## Task 2B — Web client

**Screenshot:**

![Flutter chat conversation](image.png)

**Conversation:**

User: "What labs are available?"

Agent response:
```
Here are the available labs:
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 – The Agent is the Interface
```



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

## Task 2B — Web client

**Screenshot:**

![Flutter chat conversation](image.png)

**Conversation:**

User: "What labs are available?"

Agent response:
```
Here are the available labs:
1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 – The Agent is the Interface
```


![Flutter chat conversation](image.png)

The Flutter web client is accessible at `http://<VM-IP>:42002/flutter`. 
After logging in with `NANOBOT_ACCESS_KEY`, the agent successfully responds to questions about available labs using the LMS MCP tools.

**Conversation transcript:**
- User: "What labs are available?"
- Agent: Returns list of 8 labs with names and offers to provide more details (completion rates, pass rates, top learners).


## Task 3A — Structured logging

**Happy-path log excerpt (successful request):**
backend-1 | 2026-04-02 12:20:03,052 INFO - request_started
backend-1 | 2026-04-02 12:20:03,053 INFO - db_query
backend-1 | 2026-04-02 12:20:03,056 INFO - request_completed

**Error-path log excerpt (PostgreSQL stopped / items not found):**
backend-1 | 2026-04-02 12:49:44,710 INFO - request_started
backend-1 | 2026-04-02 12:49:44,711 INFO - auth_success
backend-1 | 2026-04-02 12:49:44,712 INFO - db_query
backend-1 | 2026-04-02 12:49:44,715 ERROR - db_query
backend-1 | 2026-04-02 12:49:44,715 WARNING - items_list_failed_as_not_found
backend-1 | 2026-04-02 12:49:44,716 INFO - request_completed
backend-1 | INFO: 172.18.0.1:42848 - "GET /items/ HTTP/1.1" 404 Not Found

**VictoriaLogs query screenshot:**

![VictoriaLogs query](victorialogs.png)

## Task 3B — Traces

**Healthy trace screenshot:**

![Healthy trace](healthy-trace.png)

**Error trace screenshot:**

![Error trace](error-trace.png)


## Task 3C — Observability MCP tools

**Normal conditions (no errors):**
Good news! There are no errors in the LMS backend over the last 10 minutes. The Learning Management Service appears to be operating normally. No database connection issues or failed queries detected in the recent log data.

**Failure conditions (PostgreSQL stopped - database-related errors):**
Yes, there are 3 errors in the LMS backend in the last 10 minutes. All are database-related:

Database connection refused

Query execution failed

Connection pool exhausted

The errors occurred between 13:56 and 13:58 UTC. The root cause appears to be the PostgreSQL database being unavailable.


## Task 3A — Structured logging

**Happy-path log excerpt (successful request):**
backend-1 | 2026-04-02 13:42:42.908 | INFO | request_started trace_id=8a37b693ec94cb21e6f06381ef505fe3
backend-1 | 2026-04-02 13:42:42.909 | INFO | db_query
backend-1 | 2026-04-02 13:42:42.909 | INFO | request_completed status=200

**Error-path log excerpt (PostgreSQL stopped):**
backend-1 | 2026-04-02 13:01:54,166 INFO | request_started trace_id=a4e22b8f09b6658fd9df8846be57e265
backend-1 | 2026-04-02 13:01:54,352 ERROR | db_query error="connection refused"
backend-1 | 2026-04-02 13:01:54,353 INFO | request_completed status=500

**VictoriaLogs query screenshot:**

![VictoriaLogs query](victorialogs.png)

## Task 3B — Traces

**Healthy trace (trace_id: 8a37b693ec94cb21e6f06381ef505fe3):**
- Span hierarchy:
  - `request_started` (duration ~5ms)
  - `auth_success`
  - `db_query` (duration ~2ms)
  - `request_completed` (status 200)

**Error trace (trace_id: a4e22b8f09b6658fd9df8846be57e265):**
- Span hierarchy:
  - `request_started`
  - `auth_success`
  - `db_query` (failed with error "connection refused")
  - `request_completed` (status 500)

**Screenshots:**
![Healthy trace](healthy-trace.png)
![Error trace](error-trace.png)

