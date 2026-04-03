"""Allow running as `python -m mcp_lms [base_url]`."""

import asyncio
import sys

from mcp_lms.server import main

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(main(base_url))
