import json
import os
import sys
from pathlib import Path

def main():
    config_dir = Path("/app/nanobot")
    config_file = config_dir / "config.json"
    resolved_file = config_dir / "config.resolved.json"
    workspace_dir = config_dir / "workspace"
    venv_bin = Path("/app/.venv/bin")

    with open(config_file) as f:
        config = json.load(f)

    llm_api_key = os.environ.get("LLM_API_KEY", "")
    llm_api_base_url = os.environ.get("LLM_API_BASE_URL", "")
    llm_api_model = os.environ.get("LLM_API_MODEL", "")

    if llm_api_key:
        config["providers"]["custom"]["apiKey"] = llm_api_key
    if llm_api_base_url:
        config["providers"]["custom"]["apiBase"] = llm_api_base_url
    if llm_api_model:
        config["agents"]["defaults"]["model"] = llm_api_model

    gateway_host = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "")
    gateway_port = os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "")

    if gateway_host:
        config["gateway"]["host"] = gateway_host
    if gateway_port:
        config["gateway"]["port"] = int(gateway_port)

    # Task 3 — Add observability MCP server
    if "mcpServers" not in config.get("tools", {}):
        config["tools"]["mcpServers"] = {}
    
    config["tools"]["mcpServers"]["observability"] = {
        "command": "python",
        "args": ["-m", "mcp_observability"],
        "env": {
            "VICTORIALOGS_URL": os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"),
            "VICTORIATRACES_URL": os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")
        }
    }

    if "mcpServers" in config.get("tools", {}):
        for server_name, server_config in config["tools"]["mcpServers"].items():
            if "env" in server_config:
                for env_key in server_config["env"]:
                    runtime_value = os.environ.get(env_key)
                    if runtime_value:
                        server_config["env"][env_key] = runtime_value

    with open(resolved_file, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Resolved config written to {resolved_file}", file=sys.stderr)

    nanobot_exe = str(venv_bin / "nanobot")
    os.execv(nanobot_exe, [nanobot_exe, "gateway", "--config", str(resolved_file), "--workspace", str(workspace_dir)])

if __name__ == "__main__":
    main()
