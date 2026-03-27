"""Resolve container env vars into nanobot config and launch the gateway."""

from __future__ import annotations

import json
import os
from pathlib import Path


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _write_config(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    app_dir = Path(__file__).resolve().parent
    config_path = app_dir / "config.json"
    workspace = Path(_env("NANOBOT_WORKSPACE", str(app_dir / "workspace"))).resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    resolved = _load_config(config_path)

    defaults = resolved.setdefault("agents", {}).setdefault("defaults", {})
    defaults["workspace"] = str(workspace)
    defaults["model"] = _env("LLM_API_MODEL", defaults.get("model", "coder-model"))
    defaults["provider"] = "custom"

    provider = resolved.setdefault("providers", {}).setdefault("custom", {})
    provider["apiKey"] = _env("LLM_API_KEY", provider.get("apiKey", ""))
    provider["apiBase"] = _env(
        "LLM_API_BASE_URL",
        provider.get("apiBase", "http://localhost:42005/v1"),
    )

    gateway = resolved.setdefault("gateway", {})
    gateway["host"] = _env("NANOBOT_GATEWAY_CONTAINER_ADDRESS", gateway.get("host", "0.0.0.0"))
    gateway["port"] = int(_env("NANOBOT_GATEWAY_CONTAINER_PORT", str(gateway.get("port", 18790))))

    webchat = resolved.setdefault("channels", {}).setdefault("webchat", {})
    webchat["enabled"] = True
    webchat["host"] = _env("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", webchat.get("host", "0.0.0.0"))
    webchat["port"] = int(_env("NANOBOT_WEBCHAT_CONTAINER_PORT", str(webchat.get("port", 8765))))

    mcp_servers = resolved.setdefault("tools", {}).setdefault("mcpServers", {})
    lms = mcp_servers.setdefault("lms", {})
    lms_env = lms.setdefault("env", {})
    if _env("NANOBOT_LMS_BACKEND_URL"):
        lms_env["NANOBOT_LMS_BACKEND_URL"] = _env("NANOBOT_LMS_BACKEND_URL")
    if _env("NANOBOT_LMS_API_KEY"):
        lms_env["NANOBOT_LMS_API_KEY"] = _env("NANOBOT_LMS_API_KEY")
    if _env("NANOBOT_LOGS_URL"):
        lms_env["NANOBOT_LOGS_URL"] = _env("NANOBOT_LOGS_URL")
    if _env("NANOBOT_TRACES_URL"):
        lms_env["NANOBOT_TRACES_URL"] = _env("NANOBOT_TRACES_URL")

    resolved_path = app_dir / "config.resolved.json"
    _write_config(resolved_path, resolved)

    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_path),
            "--workspace",
            str(workspace),
        ],
    )


if __name__ == "__main__":
    main()
