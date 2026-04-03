"""Settings for the observability MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class ObsSettings:
    """Configuration for VictoriaLogs and VictoriaTraces endpoints."""

    victorialogs_url: str = "http://victorialogs:9428"
    victoriatraces_url: str = "http://victoriatraces:10428"


def resolve_settings() -> ObsSettings:
    """Resolve settings from environment variables with defaults."""
    return ObsSettings(
        victorialogs_url=os.environ.get(
            "NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"
        ),
        victoriatraces_url=os.environ.get(
            "NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428"
        ),
    )
