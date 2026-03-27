#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

def main():
    config_dir = Path("/app/nanobot")
    config_path = config_dir / "config.json"
    resolved_path = config_dir / "config.resolved.json"
    workspace_dir = config_dir / "workspace"

    with open(config_path) as f:
        config = json.load(f)

    if "custom" in config.get("providers", {}):
        if api_key := os.environ.get("LLM_API_KEY"):
            config["providers"]["custom"]["apiKey"] = api_key
        if api_base := os.environ.get("LLM_API_BASE_URL"):
            config["providers"]["custom"]["apiBase"] = api_base

    if "gateway" in config:
        if host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
            config["gateway"]["host"] = host
        if port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
            config["gateway"]["port"] = int(port)

    if "channels" in config:
        if "webchat" not in config["channels"]:
            config["channels"]["webchat"] = {}
        webchat = config["channels"]["webchat"]
        webchat["enabled"] = os.environ.get("NANOBOT_WEBSOCKET_ENABLED", "true").lower() == "true"
        if allow_from := os.environ.get("NANOBOT_WEBSOCKET_ALLOW_FROM"):
            webchat["allow_from"] = allow_from.split(",")
        else:
            webchat["allow_from"] = ["*"]

    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            lms_config = config["tools"]["mcpServers"]["lms"]
            if "env" not in lms_config:
                lms_config["env"] = {}
            if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
                lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
            if backend_key := os.environ.get("NANOBOT_LMS_API_KEY"):
                lms_config["env"]["NANOBOT_LMS_API_KEY"] = backend_key

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    # Run nanobot gateway using the CLI app directly
    from nanobot.cli.commands import app
    import sys
    
    sys.argv = [
        "nanobot",
        "gateway",
        "--config",
        str(resolved_path),
        "--workspace",
        str(workspace_dir),
    ]
    app()

if __name__ == "__main__":
    main()
