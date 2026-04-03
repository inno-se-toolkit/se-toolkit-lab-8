#!/usr/bin/env python3
"""
Entrypoint for nanobot gateway in Docker.

Reads config.json, injects environment variables, writes config.resolved.json,
then execs into nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def main():
    # Paths
    app_dir = Path("/app")
    nanobot_dir = app_dir / "nanobot"
    config_path = nanobot_dir / "config.json"
    resolved_config_path = nanobot_dir / "config.resolved.json"
    workspace_dir = nanobot_dir / "workspace"

    # Read base config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Override provider settings from env vars
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    # Override gateway settings
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Override LMS MCP server settings
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")

    if lms_backend_url:
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
    if lms_api_key:
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key

    # Override webchat MCP server settings
    webchat_ui_relay_url = os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_URL")
    webchat_ui_relay_token = os.environ.get("NANOBOT_WEBCHAT_UI_RELAY_TOKEN")

    if webchat_ui_relay_url:
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCHAT_UI_RELAY_URL"] = webchat_ui_relay_url
    if webchat_ui_relay_token:
        config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCHAT_UI_RELAY_TOKEN"] = webchat_ui_relay_token

    # Override observability MCP server settings
    victorialogs_url = os.environ.get("NANOBOT_VICTORIALOGS_URL")
    victoriatraces_url = os.environ.get("NANOBOT_VICTORIATRACES_URL")

    if victorialogs_url:
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIALOGS_URL"] = victorialogs_url
    if victoriatraces_url:
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIATRACES_URL"] = victoriatraces_url

    # Write resolved config
    with open(resolved_config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Using config: {resolved_config_path}", file=sys.stderr)

    # Exec into nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", str(resolved_config_path), "--workspace", str(workspace_dir)])


if __name__ == "__main__":
    main()
