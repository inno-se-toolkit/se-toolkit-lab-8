# Multi-stage build for the nanobot service.
# Build context: ./nanobot  additional_contexts: workspace: .

ARG REGISTRY_PREFIX_DOCKER_HUB
ARG APP_UID=1000
ARG APP_GID=1000

# ---
# Stage 1: build the venv in /app
# ---
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy root workspace manifest and lockfile
COPY --from=workspace pyproject.toml uv.lock /app/
# Copy nanobot project manifest (context root = ./nanobot)
COPY pyproject.toml /app/nanobot/pyproject.toml
# Copy dependent package manifests for uv dep resolution
COPY --from=workspace mcp/mcp-lms/pyproject.toml /app/mcp/mcp-lms/pyproject.toml
COPY --from=workspace mcp/mcp-obs/pyproject.toml /app/mcp/mcp-obs/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml \
    /app/nanobot-websocket-channel/nanobot-channel-protocol/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat/pyproject.toml \
    /app/nanobot-websocket-channel/nanobot-webchat/pyproject.toml
COPY --from=workspace nanobot-websocket-channel/mcp-webchat/pyproject.toml \
    /app/nanobot-websocket-channel/mcp-webchat/pyproject.toml

# Install non-workspace deps first (caches heavy packages like nanobot-ai)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

# Copy all source needed for editable installs
COPY --from=workspace mcp/mcp-lms/src /app/mcp/mcp-lms/src
COPY --from=workspace mcp/mcp-obs /app/mcp/mcp-obs
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol/src \
    /app/nanobot-websocket-channel/nanobot-channel-protocol/src
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat/src \
    /app/nanobot-websocket-channel/nanobot-webchat/src
COPY --from=workspace nanobot-websocket-channel/mcp-webchat/src \
    /app/nanobot-websocket-channel/mcp-webchat/src
# Copy the nanobot project itself
COPY . /app/nanobot

# Register editable installs (workspace packages)
# First install mcp-obs explicitly since nanobot depends on it
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --editable /app/mcp/mcp-obs && \
    uv sync --package nanobot

# ---
# Stage 2: runtime image without uv
# ---
ARG REGISTRY_PREFIX_DOCKER_HUB

FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Redeclare ARGs after FROM so they are available in this stage
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LANG=C.UTF-8

RUN groupadd --system --gid ${APP_GID} appuser \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

COPY --from=builder --chown=appuser:appuser /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER appuser
WORKDIR /app

CMD ["python", "/app/nanobot/entrypoint.py"]
