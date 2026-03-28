# Stage 1: builder
FROM harbor.pg.innopolis.university/docker-hub-cache/astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0
WORKDIR /app

# Copy root dependency files
COPY uv.lock pyproject.toml /app/

# Copy local packages that are referenced in pyproject.toml
COPY mcp/ /app/mcp/
COPY nanobot-websocket-channel/ /app/nanobot-websocket-channel/
COPY nanobot/ /app/nanobot/

# Install dependencies (including nanobot and its extras)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --package nanobot

# Stage 2: final image
FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14.2-slim-bookworm
RUN groupadd --system --gid 999 nonroot && useradd --system --gid 999 --uid 999 --create-home nonroot
COPY --from=builder --chown=nonroot:nonroot /app /app
WORKDIR /app/nanobot
ENV PATH="/app/.venv/bin:$PATH"
USER nonroot
CMD ["python", "entrypoint.py"]
