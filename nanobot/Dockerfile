# Nanobot gateway Dockerfile
# Adapted from backend/Dockerfile and qwen-code-api/Dockerfile

# ---
# Stage 1: build the application in the `/app` directory.
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads - use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Copy workspace root pyproject.toml and uv.lock for dependency resolution
COPY --from=workspace pyproject.toml uv.lock /app/

# Copy nanobot project pyproject.toml
COPY pyproject.toml /app/nanobot/pyproject.toml

# Copy MCP and websocket channel projects for workspace resolution (from /workspace context)
COPY --from=workspace mcp/mcp-lms /app/mcp/mcp-lms
COPY --from=workspace nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol
COPY --from=workspace nanobot-websocket-channel/mcp-webchat /app/nanobot-websocket-channel/mcp-webchat
COPY --from=workspace nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat

# Sync dependencies (nanobot-lab package with all dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot-lab

# Copy the nanobot project source
COPY . /app/nanobot

# ---
# Stage 2: use a final image without uv
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

# Set environment variables for Python and application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Make sure we use UTF-8 encoding
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Setup a non-root user - UID/GID will be set via build args to match host user
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd --system --gid ${APP_GID} appgroup \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home appuser

# Copy the application from the builder
COPY --from=builder --chown=appuser:appgroup /app /app

# Create writable directory for nanobot workspace and credentials
# Also ensure the nanobot directory is writable for config.resolved.json
RUN mkdir -p /app/nanobot/workspace/memory \
    && mkdir -p /app/nanobot/workspace/sessions \
    && chown -R appuser:appgroup /app/nanobot

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Use the app user to run our application
USER appuser

# Use `/app/nanobot` as the working directory
WORKDIR /app/nanobot

# Run the nanobot gateway via entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
