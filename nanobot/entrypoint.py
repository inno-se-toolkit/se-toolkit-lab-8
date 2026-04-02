#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path
config_path = "/app/nanobot/config.json"
resolved_path = "/tmp/config.resolved.json"
workspace = "/app/nanobot/workspace"
try:
    with open(config_path) as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"❌ Config not found: {config_path}")
    exit(1)
# Inject environment variables
if "LLM_API_KEY" in os.environ:
    config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
if "LLM_API_BASE_URL" in os.environ:
    config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
if "LLM_API_MODEL" in os.environ:
    config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]
if "NANOBOT_GATEWAY_CONTAINER_ADDRESS" in os.environ:
    config["gateway"]["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
if "NANOBOT_GATEWAY_CONTAINER_PORT" in os.environ:
    config["gateway"]["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])
if "channels" not in config:
    config["channels"] = {}
if "webchat" not in config["channels"]:
    config["channels"]["webchat"] = {"enabled": True, "allowFrom": ["*"]}
if "NANOBOT_WEBCHAT_CONTAINER_ADDRESS" in os.environ:
    config["channels"]["webchat"]["host"] = os.environ["NANOBOT_WEBCHAT_CONTAINER_ADDRESS"]
if "NANOBOT_WEBCHAT_CONTAINER_PORT" in os.environ:
    config["channels"]["webchat"]["port"] = int(os.environ["NANOBOT_WEBCHAT_CONTAINER_PORT"])
if "tools" not in config:
    config["tools"] = {}
if "mcpServers" not in config["tools"]:
    config["tools"]["mcpServers"] = {}
if "lms" not in config["tools"]["mcpServers"]:
    config["tools"]["mcpServers"]["lms"] = {
        "command": "python",
        "args": ["-m", "mcp_lms"],
    }
if "env" not in config["tools"]["mcpServers"]["lms"]:
    config["tools"]["mcpServers"]["lms"]["env"] = {}
if "NANOBOT_LMS_BACKEND_URL" in os.environ:
    config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = os.environ["NANOBOT_LMS_BACKEND_URL"]
if "NANOBOT_LMS_API_KEY" in os.environ:
    config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = os.environ["NANOBOT_LMS_API_KEY"]
if "webchat" not in config["tools"]["mcpServers"]:
    config["tools"]["mcpServers"]["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {},
    }
if "env" not in config["tools"]["mcpServers"]["webchat"]:
    config["tools"]["mcpServers"]["webchat"]["env"] = {}
if "NANOBOT_WEBCHAT_UI_RELAY_URL" in os.environ:
    config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCHAT_UI_RELAY_URL"] = os.environ["NANOBOT_WEBCHAT_UI_RELAY_URL"]
if "NANOBOT_WEBCHAT_UI_RELAY_TOKEN" in os.environ:
    config["tools"]["mcpServers"]["webchat"]["env"]["NANOBOT_WEBCHAT_UI_RELAY_TOKEN"] = os.environ["NANOBOT_WEBCHAT_UI_RELAY_TOKEN"]
if "obs" not in config["tools"]["mcpServers"]:
    config["tools"]["mcpServers"]["obs"] = {
        "command": "python",
        "args": ["-m", "mcp_obs"],
        "env": {},
    }
with open(resolved_path, "w") as f:
    json.dump(config, f, indent=2)
print(f"✅ Config resolved: {resolved_path}")
print(f"🚀 Starting nanobot gateway...")
# Use subprocess.run instead of os.execvp
subprocess.run(
    [
        "nanobot",
        "gateway",
        "--config",
        resolved_path,
        "--workspace",
        workspace,
    ],
    check=True,
)

