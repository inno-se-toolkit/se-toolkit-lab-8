---
name: observability
description: Use observability tools to inspect logs and traces for the LMS stack and debug runtime failures.
---

# Observability Skill

Use this skill when the user asks about errors, failed requests, crashes, slow responses, deployment issues, logs, traces, or system health.

## When to use
Use observability tools for:
- backend errors
- nanobot errors
- websocket failures
- qwen-code-api failures
- caddy/proxy issues
- slow or failing requests
- trace inspection
- recent incident debugging

## Tool strategy
1. Start with logs when the user reports an error or failure.
2. Check traces when the problem involves request flow, latency, retries, or unclear root cause.
3. Focus on the relevant service first:
   - backend
   - nanobot
   - qwen-code-api
   - caddy
4. Prefer recent data and narrow the search by service name, error level, path, or keywords.
5. Summarize the likely cause clearly and suggest the next debugging step.

## Logs
Use observability log tools to:
- find recent errors
- filter by service
- filter by severity
- search by keywords like exception, traceback, timeout, unauthorized, internal server error

## Traces
Use observability trace tools to:
- inspect end-to-end request flow
- find slow spans
- identify retry loops
- identify the failing service in a request chain

## Heuristics
- If the user says “500”, “Internal Server Error”, or “crash”, check logs first.
- If the user says “slow”, “latency”, or “timeout”, check traces first, then logs.
- If websocket is failing, inspect nanobot and caddy logs/traces.
- If the model fails, inspect qwen-code-api logs/traces.
