#!/usr/bin/env python3
"""Nanobot gateway entrypoint with dynamic config resolution."""

import json
import os
import sys

def main():
    config_path = os.environ.get("NANOBOT_CONFIG", "/app/nanobot/config.json")
    resolved_path = "/app/nanobot/config.resolved.json"
    
    # Load base config
    with open(config_path) as f:
        config = json.load(f)
    
    # Resolve LLM provider settings from environment
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL")
    llm_api_model = os.environ.get("LLM_API_MODEL")
    
    if llm_api_key:
        if "custom" not in config.get("providers", {}):
            config["providers"]["custom"] = {}
        config["providers"]["custom"]["apiKey"] = llm_api_key
    
    if llm_api_base_url:
        if "custom" not in config.get("providers", {}):
            config["providers"]["custom"] = {}
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    
    if llm_api_model:
        if "defaults" not in config.get("agents", {}):
            config["agents"]["defaults"] = {}
        config["agents"]["defaults"]["model"] = llm_api_model
    
    # Resolve gateway settings from environment
    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT")
    
    if gateway_host:
        if "gateway" not in config:
            config["gateway"] = {}
        config["gateway"]["host"] = gateway_host
    
    if gateway_port:
        if "gateway" not in config:
            config["gateway"] = {}
        config["gateway"]["port"] = int(gateway_port)
    
    # Resolve webchat channel settings from environment
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    webchat_token = os.environ.get("NANOBOT_ACCESS_KEY")
    
    if webchat_host or webchat_port or webchat_token:
        if "channels" not in config:
            config["channels"] = {}
        if "webchat" not in config["channels"]:
            config["channels"]["webchat"] = {}
        if webchat_host:
            config["channels"]["webchat"]["host"] = webchat_host
        if webchat_port:
            config["channels"]["webchat"]["port"] = int(webchat_port)
        if webchat_token:
            config["channels"]["webchat"]["token"] = webchat_token
        config["channels"]["webchat"]["enabled"] = True
    
    # Resolve MCP servers settings from environment
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")
    
    if "mcpServers" not in config.get("tools", {}):
        config["tools"]["mcpServers"] = {}
    
    # LMS MCP server
    if lms_backend_url or lms_api_key:
        if "lms" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["lms"] = {
                "command": "python",
                "args": ["-m", "mcp_lms"],
            }
        if "env" not in config["tools"]["mcpServers"]["lms"]:
            config["tools"]["mcpServers"]["lms"]["env"] = {}
        if lms_backend_url:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key
    
    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"Using config: {resolved_path}")
    
    # Start gateway using uv run
    os.execvp("/usr/local/bin/uv", ["uv", "run", "--directory", "/app/nanobot", "nanobot", "gateway", "--config", resolved_path])

if __name__ == "__main__":
    main()
