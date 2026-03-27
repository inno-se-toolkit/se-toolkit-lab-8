# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish
tasks. It typically consists of these core stages:

 1 Perceive — Gather information from the environment (user input, tool outputs,        
   external data)
 2 Reason/Plan — Analyze the situation, determine goals, and decide on actions
 3 Act — Execute actions using available tools (file operations, API calls, shell       
   commands, etc.)
 4 Observe — Receive feedback from the actions taken
 5 Repeat — Continue the loop until the goal is achieved or a stopping condition is met 

This loop enables agents to:

 • Break complex tasks into steps
 • Adapt based on feedback
 • Use tools autonomously
 • Handle multi-turn workflows

In my case, each time you give me a task, I go through this loop: I understand your     
request, decide what tools might help, execute them, observe the results, and either    
complete the task or iterate further.

The sophistication of an agent depends on how well it can reason, what tools it has     
access to, and how effectively it can learn from observations within this loop.

operator@se-toolkit008:~/se-toolkit-lab-8/nanobot$ uv run nanobot agent -c ./config.json
 -m "What labs are available in our LMS?"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json

🐈 nanobot
Based on the lab tasks in your LMS system, here are the available labs:

Required Labs


 Lab     Title                                                                          
 ────────────────────────────────────────────────────────────────────────────────────── 
 Task 1  Set Up the Agent — Install nanobot, connect to LLM/LMS via MCP, write skill    
         prompts
 Task 2  Deploy the Agent and Add a Web Client — Docker gateway, WebSocket channel,     
         Flutter client
 Task 3  Give the Agent New Eyes — Structured logging, traces, observability MCP tools  
 Task 4  Diagnose a Failure and Make the Agent Proactive — Investigation, cron health   
         checks, bug fix
 Task 5  Merged into Task 4


Optional Labs


 Lab              Title                                                                 
 ────────────────────────────────────────────────────────────────────────────────────── 
 Optional Task 1  Add a Telegram Bot Client — Alternative client via Telegram (blocked  
                  from Russian VMs)


The LMS backend exposes these labs via MCP tools like lms_labs, lms_pass_rates, etc.,   
which your nanobot agent can query once configured.

Would you like details on a specific lab?

## Task 1B — Agent with LMS tools

operator@se-toolkit008:~/se-toolkit-lab-8$ cd nanobot && uv run nanobot agent -c ./config.json -m "What labs are
> available?"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json
                                                                                        
🐈 nanobot
Here are the labs available in your LMS:


 ID  Lab Title
 ───────────────────────────────────────────────────────────
 1   Lab 01 – Products, Architecture & Roles
 2   Lab 02 — Run, Fix, and Deploy a Backend Service
 3   Lab 03 — Backend API: Explore, Debug, Implement, Deploy
 4   Lab 04 — Testing, Front-end, and AI Agents
 5   Lab 05 — Data Pipeline and Analytics Dashboard
 6   Lab 06 — Build Your Own Agent
 7   Lab 07 — Build a Client with an AI Coding Agent
 8   lab-08


You're currently working on Lab 08 (The Agent is the Interface) — setting up nanobot,   
deploying it with a web client, adding observability tools, and making the agent        
proactive.

Would you like details on any specific lab, such as pass rates, completion rates, or top
learners?

## Task 1C — Skill prompt

operator@se-toolkit008:~/se-toolkit-lab-8$ cd nanobot && uv run nanobot agent -c ./config.json -m "Show me the scores"
Using config: /home/operator/se-toolkit-lab-8/nanobot/config.json
⠙ nanobot is thinking...
                                                                                        
🐈 nanobot
Which lab would you like to see scores for?

Available labs:


 ID  Lab   
 ──────────
 1   lab-01
 2   lab-02
 3   lab-03
 4   lab-04
 5   lab-05
 6   lab-06
 7   lab-07
 8   lab-08


Just say something like:

 • "lab-04"
 • "Show scores for lab-06"
 • "All labs" (I'll fetch an overview)

## Task 2A — Deployed agent

```
nanobot-1  | 2026-03-27 13:05:29.665 | INFO     | nanobot.channels.manager:_init_channels:54 - WebChat channel enabled
nanobot-1  | ✓ Channels enabled: webchat
nanobot-1  | 2026-03-27 13:05:30.605 | INFO     | nanobot_webchat.channel:start:72 - WebChat starting on 0.0.0.0:8765
nanobot-1  | 2026-03-27 13:05:32.412 | INFO     | nanobot.agent.tools.mcp:connect_mcp_servers:182 - MCP server 'lms': connected, 9 tools registered
nanobot-1  | 2026-03-27 13:05:32.412 | INFO     | nanobot.agent.loop:run:260 - Agent loop started
```

## Task 2B — Web client

**Flutter client accessible at:** `http://<your-vm-ip>:42002/flutter/`

**Login with:** `NANOBOT_ACCESS_KEY` (set in `.env.docker.secret`)

**Test conversation:**

```
Q: "What can you do in this system?"

A: I'm nanobot 🐈, your AI assistant. Here's what I can do in this system:

## Core Capabilities

### 📁 File & Workspace Operations
- Read, write, and edit files
- List directory contents (including recursive exploration)
- Execute shell commands (with safety limits)

### 🌐 Web & Information
- Search the web for information
- Fetch and extract content from URLs

### ⏰ Scheduling & Reminders
- Create one-time or recurring reminders
- Manage scheduled tasks via cron

### 🤝 Communication
- Send messages to specific channels (Telegram, Discord, etc.)
- Spawn subagents for complex or long-running tasks

### 🧠 Memory System
- Store important facts in long-term memory (MEMORY.md)
- Log events in a searchable history (HISTORY.md)

## Available Skills

| Skill | Description |
|-------|-------------|
| **memory** | Two-layer memory with grep-based recall |
| **lms** | Learning Management System integration |
| **clawhub** | Search/install skills from public registry |
| **skill-creator** | Create or update custom skills |
| **cron** | Schedule reminders and recurring tasks |

## LMS Integration

I can access a Learning Management System to:
- List labs and learners
- Check pass rates, completion rates, and timelines
- View group performance and top learners
- Trigger sync pipelines
```

**WebSocket test:**
```bash
docker exec se-toolkit-lab-8-nanobot-1 /app/.venv/bin/python -c "
import asyncio, websockets, json
async def test():
    async with websockets.connect('ws://caddy:80/ws/chat?access_key=my-secret-nanobot-key') as ws:
        await ws.send(json.dumps({'content': 'What labs are available?'}))
        print(await asyncio.wait_for(ws.recv(), timeout=30))
asyncio.run(test())
"
```

Response:
```json
{"type":"text","content":"Here are the available labs:\n\n1. **Lab 01** – Products, Architecture & Roles\n2. **Lab 02** — Run, Fix, and Deploy a Backend Service\n...","format":"markdown"}
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
