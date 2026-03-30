# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

**Completed:**
- Created `nanobot/` project with `uv init nanobot`
- Installed `nanobot-ai` via `uv add nanobot-ai`
- Created `nanobot/config.json` with Qwen Code API configuration
- Agent responds to general questions

## Task 1B — Agent with LMS tools

**Completed:**
- Installed LMS MCP server: `uv add lms-mcp --editable ../mcp`
- Configured MCP server in `nanobot/config.json`:
  ```json
  "mcpServers": {
    "lms": {
      "command": "/root/.local/bin/uv",
      "args": ["run", "python", "-m", "mcp_lms"],
      "cwd": "/root/se-toolkit-lab-8/nanobot",
      "env": {
        "NANOBOT_LMS_BACKEND_URL": "http://localhost:42002",
        "NANOBOT_LMS_API_KEY": "lms-api-key"
      }
    }
  }
  ```
- Available tools: `lms_health`, `lms_labs`, `lms_learners`, `lms_pass_rates`, `lms_timeline`, `lms_groups`, `lms_top_learners`, `lms_completion_rate`, `lms_sync_pipeline`

**Test output - "What labs are available?":**
```
Here are the available labs in your LMS:

 ID  Lab Title
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   Lab 08 — The Agent is the Interface
```

## Task 1C — Skill prompt

**Completed:**
- Created `nanobot/workspace/skills/lms/SKILL.md` with:
  - Tool descriptions and when to use each
  - Parameter requirements
  - Usage strategy (start with right tool, handle missing lab params, format results)
  - Example interactions

## Task 2A — Deployed agent

**Completed:**
- Created `nanobot/entrypoint.py` - resolves environment variables and starts nanobot gateway
- Created `nanobot/Dockerfile` - single-stage build with uv
- Configured `docker-compose.yml` with nanobot service
- Configured `caddy/Caddyfile` with `/ws/chat` route

**Startup log excerpt:**
```
nanobot-1  | 🐈 Starting nanobot gateway version 0.1.4.post5 on port 18790...
nanobot-1  | 2026-03-27 20:35:13.507 | INFO - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-03-27 20:35:16.495 | DEBUG - MCP: registered tool 'mcp_lms_lms_health' from server 'lms'
nanobot-1  | ...
nanobot-1  | 2026-03-27 20:35:16.497 | INFO - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-03-27 20:35:14.348 | INFO - WebChat starting on 0.0.0.0:8765
```

## Task 2B — Web client

**Completed:**
- Added nanobot-websocket-channel as git submodule
- Installed nanobot-webchat in nanobot project
- Enabled webchat channel in config.json
- Configured client-web-flutter service in docker-compose.yml
- Configured Caddy to serve Flutter at `/flutter`

**Status:**
- Flutter app accessible at http://localhost:42002/flutter/ (HTTP 200)
- WebSocket endpoint at http://localhost:42002/ws/chat (HTTP 426 - Upgrade Required, expected for WebSocket)

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
