# Stage 1: Build
FROM astral/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy entire workspace
COPY . /app/workspace

WORKDIR /app/workspace

# Sync workspace to install all dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Stage 2: Runtime
FROM python:3.14.2-slim-bookworm AS runtime

# Create nonroot user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy venv from builder
COPY --from=builder --chown=nonroot:nonroot /app/workspace/.venv /app/.venv

# Copy nanobot directory
COPY --from=builder --chown=nonroot:nonroot /app/workspace/nanobot /app/nanobot

# Copy mcp directory (for editable imports)
COPY --from=builder --chown=nonroot:nonroot /app/workspace/mcp /app/workspace/mcp

# Copy nanobot-websocket-channel directory (for editable imports)
COPY --from=builder --chown=nonroot:nonroot /app/workspace/nanobot-websocket-channel /app/workspace/nanobot-websocket-channel

WORKDIR /app/nanobot

# Set PATH to include venv
ENV PATH="/app/.venv/bin:$PATH"

# Run entrypoint
CMD ["python", "/app/nanobot/entrypoint.py"]
