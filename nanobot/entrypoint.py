#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        return json.load(f)

def override_config(config):
    # LLM provider
    api_key = os.environ.get("LLM_API_KEY")
    api_base = os.environ.get("LLM_API_BASE_URL")
    model = os.environ.get("LLM_API_MODEL")
    if api_key:
        config.setdefault("providers", {}).setdefault("custom", {})["apiKey"] = api_key
    if api_base:
        config.setdefault("providers", {}).setdefault("custom", {})["apiBase"] = api_base
    if model:
        config.setdefault("agents", {}).setdefault("defaults", {})["model"] = model

    # Gateway
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")
    if gateway_host:
        config.setdefault("gateway", {})["host"] = gateway_host
    if gateway_port:
        config.setdefault("gateway", {})["port"] = int(gateway_port)

    # MCP servers: update LMS env vars
    mcp_servers = config.setdefault("tools", {}).setdefault("mcpServers", {})
    lms = mcp_servers.get("lms", {})
    if "env" not in lms:
        lms["env"] = {}
    backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    if backend_url:
        lms["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
    backend_key = os.environ.get("NANOBOT_LMS_API_KEY")
    if backend_key:
        lms["env"]["NANOBOT_LMS_API_KEY"] = backend_key
    mcp_servers["lms"] = lms

    # WebSocket channel settings
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    channels = config.setdefault("channels", {})
    webchat = channels.setdefault("webchat", {})
    webchat["enabled"] = True
    if webchat_host:
        webchat["host"] = webchat_host
    if webchat_port:
        webchat["port"] = int(webchat_port)
    webchat["allowFrom"] = ["*"]

    # WebChat MCP server (mcp-webchat)
    webchat_mcp = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {}
    }
    ui_relay_url = os.environ.get("NANOBOT_UI_RELAY_URL", "http://localhost:42002")
    webchat_mcp["env"]["UI_RELAY_URL"] = ui_relay_url
    mcp_servers["webchat"] = webchat_mcp

    return config

def write_resolved_config(config):
    resolved_path = Path(__file__).parent / "config.resolved.json"
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    return resolved_path

def main():
    config = load_config()
    config = override_config(config)
    resolved_path = write_resolved_config(config)
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_path), "--workspace", str(Path(__file__).parent / "workspace")])

if __name__ == "__main__":
    main()
