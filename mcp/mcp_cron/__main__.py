"""Entry point for the cron MCP server."""

import asyncio
import os

from mcp_cron.server import main

if __name__ == "__main__":
    os.environ.setdefault("NANOBOT_CRON_DIR", "/app/nanobot/cron")
    asyncio.run(main())
