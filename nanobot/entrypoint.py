from __future__ import annotations

import json
import os
from pathlib import Path

from nanobot.config import Config, load_config
from nanobot.config.schema import MCPServerConfig
from pydantic import Field
from pydantic_settings import BaseSettings


APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"
RESOLVED_CONFIG_PATH = APP_DIR / "config.resolved.json"


class Settings(BaseSettings):
    llm_api_model: str = Field(..., alias="LLM_API_MODEL")
    llm_api_key: str = Field(..., alias="LLM_API_KEY")
    llm_api_base_url: str = Field(..., alias="LLM_API_BASE_URL")

    nanobot_gateway_container_address: str = Field(..., alias="NANOBOT_GATEWAY_CONTAINER_ADDRESS")
    nanobot_gateway_container_port: int = Field(..., alias="NANOBOT_GATEWAY_CONTAINER_PORT")

    # Task 2B — uncomment after you add the webchat channel.
    # nanobot_webchat_container_address: str = Field(..., alias="NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    # nanobot_webchat_container_port: int = Field(..., alias="NANOBOT_WEBCHAT_CONTAINER_PORT")

    nanobot_lms_backend_url: str = Field(..., alias="NANOBOT_LMS_BACKEND_URL")
    nanobot_lms_api_key: str = Field(..., alias="NANOBOT_LMS_API_KEY")

    # Task 3 — uncomment after you add mcp-obs.
    # nanobot_victorialogs_url: str = Field(..., alias="NANOBOT_VICTORIALOGS_URL")
    # nanobot_victoriatraces_url: str = Field(..., alias="NANOBOT_VICTORIATRACES_URL")

    # Task 2B — uncomment after you add the webchat channel.
    # nanobot_access_key: str = Field(..., alias="NANOBOT_ACCESS_KEY")
    # nanobot_ui_relay_url: str = Field(default="http://127.0.0.1:8766", alias="NANOBOT_UI_RELAY_URL")
    # nanobot_ui_relay_token: str | None = Field(default=None, alias="NANOBOT_UI_RELAY_TOKEN")

    otel_traces_exporter: str = Field(..., alias="OTEL_TRACES_EXPORTER")
    otel_metrics_exporter: str = Field(..., alias="OTEL_METRICS_EXPORTER")
    otel_logs_exporter: str = Field(..., alias="OTEL_LOGS_EXPORTER")
    otel_exporter_otlp_endpoint: str = Field(..., alias="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_exporter_otlp_protocol: str = Field(..., alias="OTEL_EXPORTER_OTLP_PROTOCOL")
    otel_python_log_correlation: str = Field(..., alias="OTEL_PYTHON_LOG_CORRELATION")


def _otel_env(env: Settings, service_name: str) -> dict[str, str]:
    return {
        "OTEL_SERVICE_NAME": service_name,
        "OTEL_TRACES_EXPORTER": env.otel_traces_exporter,
        "OTEL_METRICS_EXPORTER": env.otel_metrics_exporter,
        "OTEL_LOGS_EXPORTER": env.otel_logs_exporter,
        "OTEL_EXPORTER_OTLP_ENDPOINT": env.otel_exporter_otlp_endpoint,
        "OTEL_EXPORTER_OTLP_PROTOCOL": env.otel_exporter_otlp_protocol,
        "OTEL_PYTHON_LOG_CORRELATION": env.otel_python_log_correlation,
    }


def _resolve_config() -> Config:
    env = Settings.model_validate({})
    config = load_config(CONFIG_PATH)

    config.agents.defaults.model = env.llm_api_model
    config.providers.custom.api_key = env.llm_api_key
    config.providers.custom.api_base = env.llm_api_base_url

    config.gateway.host = env.nanobot_gateway_container_address
    config.gateway.port = env.nanobot_gateway_container_port

    # Task 2B — uncomment after you add the webchat channel.
    # config.channels.webchat = {  # pyright: ignore[reportAttributeAccessIssue]
    #     "enabled": True,
    #     "host": env.nanobot_webchat_container_address,
    #     "port": env.nanobot_webchat_container_port,
    #     "allowFrom": ["*"],
    # }

    # MCP servers
    config.tools.mcp_servers["lms"] = MCPServerConfig(
        command="opentelemetry-instrument",
        args=["python", "-m", "mcp_lms"],
        env={
            "NANOBOT_LMS_BACKEND_URL": env.nanobot_lms_backend_url,
            "NANOBOT_LMS_API_KEY": env.nanobot_lms_api_key,
            **_otel_env(env, "mcp-lms"),
        },
    )
    # Task 3 — uncomment after you add mcp-obs.
    # config.tools.mcp_servers["obs"] = MCPServerConfig(
    #     command="opentelemetry-instrument",
    #     args=["python", "-m", "mcp_obs"],
    #     env={
    #         "NANOBOT_VICTORIALOGS_URL": env.nanobot_victorialogs_url,
    #         "NANOBOT_VICTORIATRACES_URL": env.nanobot_victoriatraces_url,
    #         **_otel_env(env, "mcp-obs"),
    #     },
    # )
    # Task 2B — uncomment after you add the webchat channel.
    # config.tools.mcp_servers["webchat"] = MCPServerConfig(
    #     command="opentelemetry-instrument",
    #     args=["python", "-m", "mcp_webchat"],
    #     env={
    #         "NANOBOT_UI_RELAY_URL": env.nanobot_ui_relay_url,
    #         "NANOBOT_UI_RELAY_TOKEN": env.nanobot_ui_relay_token or env.nanobot_access_key,
    #         **_otel_env(env, "mcp-webchat"),
    #     },
    # )

    return config


def main() -> None:
    config = _resolve_config()
    RESOLVED_CONFIG_PATH.write_text(
        json.dumps(
            config.model_dump(mode="json", by_alias=True), indent=2
        )
        + "\n",
        encoding="utf-8",
    )
    os.execvp(
        "opentelemetry-instrument",
        [
            "opentelemetry-instrument",
            "nanobot",
            "gateway",
            "--config",
            str(RESOLVED_CONFIG_PATH),
            "--workspace",
            str(APP_DIR / "workspace"),
        ],
    )


if __name__ == "__main__":
    main()
