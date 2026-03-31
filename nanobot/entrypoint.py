"""Resolve Docker env vars into config.resolved.json and launch nanobot gateway."""

from __future__ import annotations

import json
import os

CONFIG_IN = "/app/nanobot/config.json"
CONFIG_OUT = "/app/nanobot/config.resolved.json"
WORKSPACE = "/app/nanobot/workspace"


def main() -> None:
    with open(CONFIG_IN) as f:
        config = json.load(f)

    # LLM provider
    api_key = os.environ.get("LLM_API_KEY", "")
    api_base = os.environ.get("LLM_API_BASE_URL", "")
    model = os.environ.get("LLM_API_MODEL", "")

    config.setdefault("providers", {}).setdefault("custom", {})
    if api_key:
        config["providers"]["custom"]["apiKey"] = api_key
    if api_base:
        config["providers"]["custom"]["apiBase"] = api_base
    if model:
        config.setdefault("agents", {}).setdefault("defaults", {})["model"] = model

    # Gateway
    gw_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "")
    gw_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "")
    config.setdefault("gateway", {})
    if gw_host:
        config["gateway"]["host"] = gw_host
    if gw_port:
        config["gateway"]["port"] = int(gw_port)

    # LMS MCP server env
    lms_url = os.environ.get("NANOBOT_LMS_BACKEND_URL", "")
    lms_key = os.environ.get("NANOBOT_LMS_API_KEY", "")
    mcp = config.setdefault("tools", {}).setdefault("mcpServers", {})
    mcp.setdefault("lms", {}).setdefault("env", {})
    if lms_url:
        mcp["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_url
    if lms_key:
        mcp["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_key

    # WebChat channel
    wc_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    wc_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")
    relay_host = "127.0.0.1"
    relay_port = 8766

    config.setdefault("channels", {})["webchat"] = {
        "enabled": True,
        "host": wc_host,
        "port": int(wc_port),
        "allowFrom": ["*"],
        "relayHost": relay_host,
        "relayPort": relay_port,
    }

    # WebChat MCP server — lets the agent send structured UI messages to the browser
    access_key = os.environ.get("NANOBOT_ACCESS_KEY", "")
    relay_url = f"http://{relay_host}:{relay_port}/ui-message"
    mcp["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {
            "NANOBOT_UI_RELAY_URL": relay_url,
            "NANOBOT_UI_RELAY_TOKEN": access_key,
        },
    }

    # Observability MCP server — VictoriaLogs and VictoriaTraces access
    logs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
    traces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")
    mcp["obs"] = {
        "command": "python",
        "args": ["-m", "mcp_obs"],
        "env": {
            "NANOBOT_VICTORIALOGS_URL": logs_url,
            "NANOBOT_VICTORIATRACES_URL": traces_url,
        },
    }

    with open(CONFIG_OUT, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {CONFIG_OUT}", flush=True)
    os.execvp(
        "nanobot",
        ["nanobot", "gateway", "--config", CONFIG_OUT, "--workspace", WORKSPACE],
    )


if __name__ == "__main__":
    main()
