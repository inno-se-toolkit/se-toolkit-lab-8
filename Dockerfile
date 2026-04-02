# Multi-stage build for nanobot agent
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY --from=workspace pyproject.toml uv.lock /app/
COPY pyproject.toml /app/nanobot/pyproject.toml
COPY --from=workspace mcp/ /app/mcp/
COPY --from=workspace nanobot-websocket-channel/ /app/nanobot-websocket-channel/
COPY . /app/nanobot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

# Install mcp-obs separately
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -e /app/mcp/mcp-obs

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ARG APP_UID=999
ARG APP_GID=999

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid ${APP_GID} nonroot \
    && useradd --system --gid ${APP_GID} --uid ${APP_UID} --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot
WORKDIR /app

CMD ["python", "/app/nanobot/entrypoint.py"]
