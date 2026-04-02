"""Runtime settings for the LMS MCP server."""

from __future__ import annotations

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str = Field(
        validation_alias=AliasChoices("NANOBOT_LMS_BACKEND_URL"),
    )
    api_key: str = Field(
        validation_alias=AliasChoices("NANOBOT_LMS_API_KEY", "LMS_API_KEY"),
    )


def resolve_settings(base_url: str | None = None) -> Settings:
    overrides: dict[str, str] = {}
    if base_url:
        overrides["base_url"] = base_url
    return Settings.model_validate(overrides)
