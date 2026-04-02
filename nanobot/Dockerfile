FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14.0-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /usr/local/bin/uv

# Copy from workspace context
COPY --from=workspace . /app/

# Install nanobot dependencies and MCP servers
WORKDIR /app/nanobot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev && \
    uv pip install -e /app/mcp/mcp-lms -e /app/mcp/mcp-obs -e /app/nanobot-websocket-channel/nanobot-webchat -e /app/nanobot-websocket-channel/mcp-webchat -e /app/nanobot-websocket-channel/nanobot-channel-protocol

# Create app user
ARG APP_UID=1000
ARG APP_GID=1000
RUN groupadd -g "${APP_GID}" app && useradd -u "${APP_UID}" -g "${APP_GID}" -m app
RUN chown -R app:app /app
USER app

ENTRYPOINT ["/usr/local/bin/uv", "run", "--directory", "/app/nanobot", "python", "/app/nanobot/entrypoint.py"]
