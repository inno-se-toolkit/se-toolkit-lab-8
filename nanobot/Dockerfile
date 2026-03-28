ARG REGISTRY_PREFIX_DOCKER_HUB

FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY --from=workspace pyproject.toml uv.lock /app/
COPY pyproject.toml /app/nanobot/pyproject.toml

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-workspace --package nanobot

COPY . /app/nanobot
COPY --from=workspace mcp /app/mcp
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --package nanobot

FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV PATH="/app/.venv/bin:$PATH"

RUN set -eux; \
    if [ "$APP_UID" != "0" ] || [ "$APP_GID" != "0" ]; then \
        groupadd --gid "$APP_GID" appgroup; \
        useradd --uid "$APP_UID" --gid "$APP_GID" --create-home appuser; \
    fi

COPY --from=builder /app /app

RUN set -eux; \
    if [ "$APP_UID" != "0" ] || [ "$APP_GID" != "0" ]; then \
        chown -R "$APP_UID:$APP_GID" /app; \
    fi

USER ${APP_UID}:${APP_GID}
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
