"""MCP server for managing nanobot cron jobs."""

import json
import os
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

server = Server("cron")


class _NoArgs(BaseModel):
    pass


class _CreateJob(BaseModel):
    name: str = Field(description="Job name")
    schedule: str = Field(description="Cron expression")
    prompt: str = Field(description="Prompt to execute")
    chat_id: str = Field(default="default")


class _RemoveJob(BaseModel):
    name: str = Field(description="Job name")


def get_cron_dir():
    return os.environ.get("NANOBOT_CRON_DIR", "/app/nanobot/cron")


def load_jobs():
    jobs_path = Path(get_cron_dir()) / "jobs.json"
    if not jobs_path.exists():
        return {"version": 1, "jobs": []}
    with open(jobs_path) as f:
        return json.load(f)


def save_jobs(data):
    jobs_path = Path(get_cron_dir()) / "jobs.json"
    jobs_path.parent.mkdir(parents=True, exist_ok=True)
    with open(jobs_path, "w") as f:
        json.dump(data, f, indent=2)


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="cron_list",
            description="List all scheduled cron jobs",
            inputSchema=_NoArgs.model_json_schema()
        ),
        Tool(
            name="cron_create",
            description="Create a new cron job",
            inputSchema=_CreateJob.model_json_schema()
        ),
        Tool(
            name="cron_remove",
            description="Remove a cron job",
            inputSchema=_RemoveJob.model_json_schema()
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None = None):
    args = arguments or {}
    
    if name == "cron_list":
        data = load_jobs()
        return [TextContent(type="text", text=json.dumps(data, indent=2))]
    
    elif name == "cron_create":
        job_name = args.get("name", "")
        schedule = args.get("schedule", "")
        prompt = args.get("prompt", "")
        chat_id = args.get("chat_id", "default")
        
        data = load_jobs()
        for job in data["jobs"]:
            if job.get("name") == job_name:
                return [TextContent(type="text", text=json.dumps({"error": f"Job '{job_name}' exists"}))]
        
        new_job = {"name": job_name, "schedule": schedule, "prompt": prompt, "chat_id": chat_id, "enabled": True}
        data["jobs"].append(new_job)
        save_jobs(data)
        return [TextContent(type="text", text=json.dumps({"status": "created", "job": new_job}))]
    
    elif name == "cron_remove":
        job_name = args.get("name", "")
        data = load_jobs()
        original = len(data["jobs"])
        data["jobs"] = [j for j in data["jobs"] if j.get("name") != job_name]
        if len(data["jobs"]) == original:
            return [TextContent(type="text", text=json.dumps({"error": f"Job '{job_name}' not found"}))]
        save_jobs(data)
        return [TextContent(type="text", text=json.dumps({"status": "removed"}))]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
