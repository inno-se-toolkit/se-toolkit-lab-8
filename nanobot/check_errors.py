#!/usr/bin/env python3
"""Simple observability tool for nanobot."""
import json
import sys
import httpx

def check_errors():
    try:
        resp = httpx.get(
            "http://victorialogs:9428/select/logsql/query",
            params={"query": "severity:ERROR", "limit": 5},
            timeout=10
        )
        lines = [l for l in resp.text.strip().split("\\n") if l.strip()]
        if lines:
            print(f"Found {len(lines)} error(s):")
            for line in lines[:3]:
                try:
                    data = json.loads(line)
                    print(f"  - {data.get(\"_msg\", \"unknown\")}: {data.get(\"error\", \"\")[:100]}")
                except:
                    print(f"  - {line[:100]}")
        else:
            print("No recent errors found")
    except Exception as e:
        print(f"Error checking logs: {e}")

if __name__ == "__main__":
    check_errors()
