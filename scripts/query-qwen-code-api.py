"""Query the Qwen Code API (OpenAI-compatible endpoint).

Usage:
    python scripts/query-qwen-code-api.py [OPTIONS] PROMPT

Options:
    --env-file FILE  Load variables from a .env file (default: .env.docker.secret)
    --base-url URL   API base URL   (default: $LLM_API_HOST_BASE_URL)
    --port PORT      Shorthand for http://localhost:<PORT>/v1 (overrides --base-url)
    --api-key KEY    API key        (default: $LLM_API_KEY)
    --model MODEL    Model name     (default: $LLM_API_MODEL)

Environment variables:
    LLM_API_HOST_BASE_URL   Default base URL (host-side)
    LLM_API_KEY             Default API key
    LLM_API_MODEL           Default model name
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_ENV_FILE = _REPO_ROOT / ".env.docker.secret"


def _resolve_env_file() -> Path | None:
    """Pre-parse --env-file from argv before argparse/pydantic run."""
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--env-file", type=Path)
    env_args, _ = pre.parse_known_args()
    if env_args.env_file:
        return env_args.env_file
    if _DEFAULT_ENV_FILE.is_file():
        return _DEFAULT_ENV_FILE
    return None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_resolve_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str = Field(..., alias="LLM_API_HOST_BASE_URL")
    api_key: str = Field(..., alias="LLM_API_KEY")
    model: str = Field(..., alias="LLM_API_MODEL")


def main() -> None:
    settings = Settings.model_validate({})

    parser = argparse.ArgumentParser(description="Query the Qwen Code API")
    parser.add_argument(
        "--env-file",
        default=None,
        help="Load variables from a .env file (default: .env.docker.secret)",
    )
    parser.add_argument(
        "--base-url",
        default=settings.base_url,
        help="API base URL (default: $LLM_API_BASE_URL)",
    )
    parser.add_argument(
        "--port",
        type=int,
        help="Shorthand for http://localhost:<PORT>/v1 (overrides --base-url)",
    )
    parser.add_argument(
        "--api-key",
        default=settings.api_key,
        help="API key (default: $LLM_API_KEY)",
    )
    parser.add_argument(
        "--model",
        default=settings.model,
        help="Model name (default: $LLM_API_MODEL or coder-model)",
    )
    parser.add_argument("prompt", nargs="+", help="The prompt to send")
    args = parser.parse_args()

    base_url: str = args.base_url
    if args.port is not None:
        base_url = f"http://localhost:{args.port}/v1"
    if not base_url.startswith(("http://", "https://")):
        base_url = f"http://{base_url}"
    if not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"

    api_key: str = args.api_key
    if not api_key:
        print("Error: API key is required (--api-key or LLM_API_KEY)", file=sys.stderr)
        sys.exit(1)

    prompt = " ".join(args.prompt)
    url = f"{base_url.rstrip('/')}/chat/completions"

    payload = json.dumps(
        {
            "model": args.model,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            print(json.dumps(data, indent=2))
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
