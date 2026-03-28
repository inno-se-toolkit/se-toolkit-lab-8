import json
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
RESOLVED_PATH = BASE_DIR / "config.resolved.json"


def env(name: str, default=None):
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def set_nested(dct, keys, value):
    cur = dct
    for key in keys[:-1]:
        cur = cur.setdefault(key, {})
    cur[keys[-1]] = value


def main():
    cfg = json.loads(CONFIG_PATH.read_text())

    llm_api_key = env("LLM_API_KEY")
    llm_api_base = env("LLM_API_BASE_URL")
    llm_api_model = env("LLM_API_MODEL")
    gateway_host = env("NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    gateway_port = env("NANOBOT_GATEWAY_CONTAINER_PORT")
    lms_backend_url = env("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = env("NANOBOT_LMS_API_KEY")

    webchat_host = env("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = env("NANOBOT_WEBCHAT_CONTAINER_PORT")
    access_key = env("NANOBOT_ACCESS_KEY")

    ui_relay_host = env("NANOBOT_UI_RELAY_HOST", "127.0.0.1")
    ui_relay_port = env("NANOBOT_UI_RELAY_PORT", "8766")
    ui_relay_url = env("NANOBOT_UI_RELAY_URL", f"http://{ui_relay_host}:{ui_relay_port}/ui-message")
    ui_relay_token = env("NANOBOT_UI_RELAY_TOKEN", access_key or "")

    if llm_api_key is not None:
        set_nested(cfg, ["providers", "custom", "apiKey"], llm_api_key)
    if llm_api_base is not None:
        set_nested(cfg, ["providers", "custom", "apiBase"], llm_api_base)
    if llm_api_model is not None:
        set_nested(cfg, ["agents", "defaults", "model"], llm_api_model)
    if gateway_host is not None:
        set_nested(cfg, ["gateway", "host"], gateway_host)
    if gateway_port is not None:
        set_nested(cfg, ["gateway", "port"], int(gateway_port))

    if lms_backend_url is not None:
        set_nested(
            cfg,
            ["tools", "mcpServers", "lms", "env", "NANOBOT_LMS_BACKEND_URL"],
            lms_backend_url,
        )
    if lms_api_key is not None:
        set_nested(
            cfg,
            ["tools", "mcpServers", "lms", "env", "NANOBOT_LMS_API_KEY"],
            lms_api_key,
        )

    set_nested(cfg, ["channels", "webchat", "enabled"], True)
    set_nested(cfg, ["channels", "webchat", "allowFrom"], ["*"])
    if webchat_host is not None:
        set_nested(cfg, ["channels", "webchat", "host"], webchat_host)
    if webchat_port is not None:
        set_nested(cfg, ["channels", "webchat", "port"], int(webchat_port))

    cfg.setdefault("tools", {})
    cfg["tools"].setdefault("mcpServers", {})
    cfg["tools"]["mcpServers"]["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {
            "NANOBOT_UI_RELAY_URL": ui_relay_url,
            "NANOBOT_UI_RELAY_TOKEN": ui_relay_token,
        },
    }

    workspace_value = cfg.get("agents", {}).get("defaults", {}).get("workspace", "./workspace")
    workspace_path = Path(workspace_value)
    if not workspace_path.is_absolute():
        workspace_path = (BASE_DIR / workspace_path).resolve()

    RESOLVED_PATH.write_text(json.dumps(cfg, indent=2) + "\n")

    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(RESOLVED_PATH),
            "--workspace",
            str(workspace_path),
        ],
    )


if __name__ == "__main__":
    main()
