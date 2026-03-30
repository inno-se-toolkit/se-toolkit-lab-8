import json
import os
from pathlib import Path


APP_DIR = Path("/app/nanobot")
CONFIG_PATH = APP_DIR / "config.json"
RESOLVED_CONFIG_PATH = Path("/tmp/nanobot.config.resolved.json")
WORKSPACE_PATH = APP_DIR / "workspace"


def set_deep(obj, path, value):
    cur = obj
    for key in path[:-1]:
        if key not in cur or not isinstance(cur[key], dict):
            cur[key] = {}
        cur = cur[key]
    cur[path[-1]] = value


def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        config = json.load(f)

    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    webchat_port = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765"))
    relay_host = "127.0.0.1"
    relay_port = 8766
    relay_url = f"http://{relay_host}:{relay_port}"
    relay_token = os.environ.get("NANOBOT_ACCESS_KEY", "")

    env_map = {
        ("providers", "custom", "apiKey"): os.environ.get("LLM_API_KEY"),
        ("providers", "custom", "apiBase"): os.environ.get("LLM_API_BASE_URL"),
        ("agents", "defaults", "model"): os.environ.get("LLM_API_MODEL"),
        ("gateway", "host"): os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"),
        ("gateway", "port"): int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"]),
        ("channels", "webchat", "enabled"): True,
        ("channels", "webchat", "host"): webchat_host,
        ("channels", "webchat", "port"): webchat_port,
        ("channels", "webchat", "allowFrom"): ["*"],
        ("channels", "webchat", "relayHost"): relay_host,
        ("channels", "webchat", "relayPort"): relay_port,
        ("tools", "mcpServers", "lms", "env", "NANOBOT_LMS_BACKEND_URL"): os.environ.get("NANOBOT_LMS_BACKEND_URL"),
        ("tools", "mcpServers", "lms", "env", "NANOBOT_LMS_API_KEY"): os.environ.get("NANOBOT_LMS_API_KEY"),
        ("tools", "mcpServers", "webchat", "command"): "python",
        ("tools", "mcpServers", "webchat", "args"): ["-m", "mcp_webchat"],
        ("tools", "mcpServers", "webchat", "env", "NANOBOT_UI_RELAY_URL"): relay_url,
        ("tools", "mcpServers", "webchat", "env", "NANOBOT_UI_RELAY_TOKEN"): relay_token,
        ("tools", "mcpServers", "obs", "command"): "python",
        ("tools", "mcpServers", "obs", "args"): ["-m", "mcp_obs"],
        ("tools", "mcpServers", "obs", "env", "NANOBOT_VICTORIALOGS_URL"): os.environ.get("NANOBOT_VICTORIALOGS_URL"),
        ("tools", "mcpServers", "obs", "env", "NANOBOT_VICTORIATRACES_URL"): os.environ.get("NANOBOT_VICTORIATRACES_URL"),
    }

    for path, value in env_map.items():
        if value is not None:
            set_deep(config, path, value)

    with RESOLVED_CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(RESOLVED_CONFIG_PATH),
            "--workspace",
            str(WORKSPACE_PATH),
        ],
    )


if __name__ == "__main__":
    main()
