"""Entry point for the observability MCP server."""

import asyncio
import os
import sys

from mcp_observability.server import main

if __name__ == "__main__":
    logs_url = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
    traces_url = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")
    asyncio.run(main(logs_url, traces_url))
