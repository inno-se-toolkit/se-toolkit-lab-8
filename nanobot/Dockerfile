ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_PROJECT_ENVIRONMENT=/opt/nanobot-venv

WORKDIR /app

COPY --from=workspace pyproject.toml uv.lock /app/
COPY pyproject.toml README.md /app/nanobot/
COPY --from=workspace mcp /app/mcp
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --gid "${APP_GID}" nonroot \
    && useradd --uid "${APP_UID}" --gid "${APP_GID}" --create-home nonroot

COPY --from=builder --chown=${APP_UID}:${APP_GID} /opt/nanobot-venv /opt/nanobot-venv
COPY --from=builder --chown=${APP_UID}:${APP_GID} /app /app

ENV PATH="/opt/nanobot-venv/bin:$PATH"

USER nonroot
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
