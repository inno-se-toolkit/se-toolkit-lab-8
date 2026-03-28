"""Entrypoint for nanobot gateway in Docker.

Resolves environment variables into config.json at runtime,
then execs into nanobot gateway.
"""

import json
import os
import sys
from pathlib import Path


def resolve_config() -> str:
    """Read config.json, override with env vars, write config.resolved.json."""
    config_path = Path(__file__).parent / "config.json"
    # Write resolved config to /tmp to avoid permission issues with bind mounts
    resolved_path = Path("/tmp/nanobot/config.resolved.json")
    resolved_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path) as f:
        config = json.load(f)

    # Override provider API key and base URL from env vars
    if api_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = api_key

    if api_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = api_base

    # Override agent model from env var
    if model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = model

    # Override gateway host and port from env vars
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host

    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)

    # Configure webchat channel from env vars
    if webchat_host := os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS"):
        if "channels" not in config:
            config["channels"] = {}
        config["channels"]["webchat"] = {
            "enabled": True,
            "host": webchat_host,
            "port": int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765")),
            "allowFrom": ["*"],
        }

    # Configure MCP servers - add mcp_webchat if not present
    if "tools" not in config:
        config["tools"] = {}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}

    # Add mcp_webchat MCP server for structured UI messages
    if ui_relay_url := os.environ.get("NANOBOT_UI_RELAY_URL"):
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {
                "NANOBOT_UI_RELAY_URL": ui_relay_url,
                "NANOBOT_UI_RELAY_TOKEN": os.environ.get(
                    "NANOBOT_UI_RELAY_TOKEN", "nanobot-webchat-token"
                ),
            },
        }

    # Override LMS MCP server env vars for Docker networking
    if "lms" in config["tools"]["mcpServers"]:
        if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
            config["tools"]["mcpServers"]["lms"]["env"][
                "NANOBOT_LMS_BACKEND_URL"
            ] = backend_url
        if api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = api_key

    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return str(resolved_path)


def main() -> None:
    """Resolve config and exec into nanobot gateway."""
    resolved_config = resolve_config()
    workspace = str(Path(__file__).parent / "workspace")

    # Ensure workspace subdirectories exist and are writable
    cron_dir = Path(workspace) / "cron"
    cron_dir.mkdir(parents=True, exist_ok=True)

    # Build the command
    cmd = [
        "nanobot",
        "gateway",
        "--config",
        resolved_config,
        "--workspace",
        workspace,
    ]

    # Exec into nanobot gateway - this replaces the Python process
    os.execvp("nanobot", cmd)


if __name__ == "__main__":
    main()
