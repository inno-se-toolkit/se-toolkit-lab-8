# MCP Observability Server

MCP server providing tools for querying VictoriaLogs and VictoriaTraces.

## Tools

- `logs_search` - Search logs using LogsQL query
- `logs_error_count` - Count errors per service over time window
- `traces_list` - List recent traces for a service
- `traces_get` - Fetch specific trace by ID

## Usage

```bash
uv add mcp-observability --editable ../mcp
```

Then configure in nanobot config.json:

```json
{
  "tools": {
    "mcpServers": {
      "observability": {
        "command": "python",
        "args": ["-m", "mcp_observability"],
        "env": {
          "VICTORIALOGS_URL": "http://localhost:9428",
          "VICTORIATRACES_URL": "http://localhost:10428"
        }
      }
    }
  }
}
```
