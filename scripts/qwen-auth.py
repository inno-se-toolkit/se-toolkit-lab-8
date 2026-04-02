#!/usr/bin/env python3
"""Authenticate with Qwen OAuth and save credentials to ~/.qwen/oauth_creds.json.

Usage (on your VM):
    python3 scripts/qwen-auth.py

The script will print a URL. Open it in your browser and authorize.
Then press Enter and the script will exchange the code for a token.

If the token exchange fails from the VM (Alibaba WAF blocks some IPs),
the script prints a curl command you can run from your laptop instead.
"""

import base64
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CLIENT_ID = "f0304373b74a44d2b584a3fb70ca9e56"
SCOPE = "openid profile email model.completion"
AUTH_URL = "https://chat.qwen.ai/api/v1/oauth2"
UA = "qwen-code/0.12.2"
CREDS_PATH = os.path.expanduser("~/.qwen/oauth_creds.json")


def _request(url, data_dict):
    data = urllib.parse.urlencode(data_dict).encode()
    req = urllib.request.Request(url, data, {
        "User-Agent": UA,
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    body = urllib.request.urlopen(req, timeout=15).read()
    if b"<!doctype" in body.lower() or b"aliyun_waf" in body.lower():
        raise RuntimeError("WAF_BLOCK")
    return json.loads(body)


def main():
    # Step 1: PKCE
    verifier = secrets.token_urlsafe(32)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    # Step 2: Device code
    print("Requesting device code...")
    try:
        resp = _request(f"{AUTH_URL}/device/code", {
            "client_id": CLIENT_ID,
            "scope": SCOPE,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        })
    except RuntimeError:
        print("ERROR: WAF blocked the device code request.")
        print("Try again in a minute, or run this script from a different machine.")
        sys.exit(1)

    device_code = resp["device_code"]
    verify_url = resp.get("verification_uri_complete", "")

    print()
    print(f"  Open this URL in your browser:\n")
    print(f"  {verify_url}\n")
    input("  Press Enter after you authorized in the browser...")

    # Step 3: Exchange for token
    print("Exchanging code for token...")
    token_params = {
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        "client_id": CLIENT_ID,
        "device_code": device_code,
        "code_verifier": verifier,
    }

    token = None
    for attempt in range(5):
        try:
            token = _request(f"{AUTH_URL}/token", token_params)
            break
        except RuntimeError:
            if attempt < 4:
                print(f"  WAF blocked attempt {attempt + 1}, retrying in 3s...")
                time.sleep(3)
            continue
        except urllib.error.HTTPError as e:
            body = e.read()
            if b"aliyun_waf" in body.lower() or b"<!doctype" in body.lower():
                if attempt < 4:
                    print(f"  WAF blocked attempt {attempt + 1}, retrying in 3s...")
                    time.sleep(3)
                continue
            print(f"ERROR: HTTP {e.code}: {body.decode()[:200]}")
            sys.exit(1)

    if token is None:
        print()
        print("The token exchange is blocked by Alibaba WAF from this IP.")
        print("Run this curl command from your laptop or phone hotspot instead:\n")
        curl_data = urllib.parse.urlencode(token_params)
        print(f'  curl -s -X POST "{AUTH_URL}/token" \\')
        print(f'    -H "User-Agent: {UA}" \\')
        print(f'    -H "Content-Type: application/x-www-form-urlencoded" \\')
        print(f'    -d "{curl_data}"')
        print()
        print(f"Then save the JSON output to {CREDS_PATH} on the VM.")
        print("You'll need to add expiry_date (ms timestamp) and resource_url fields.")
        sys.exit(1)

    if "access_token" not in token:
        print(f"ERROR: unexpected response: {json.dumps(token)[:300]}")
        sys.exit(1)

    # Step 4: Save credentials
    creds = {
        "access_token": token["access_token"],
        "token_type": token.get("token_type", "Bearer"),
        "refresh_token": token.get("refresh_token", ""),
        "resource_url": token.get("resource_url", "portal.qwen.ai"),
        "expiry_date": int(time.time() * 1000) + token.get("expires_in", 3600) * 1000,
    }
    os.makedirs(os.path.dirname(CREDS_PATH), exist_ok=True)
    with open(CREDS_PATH, "w") as f:
        json.dump(creds, f, indent=2)
    os.chmod(CREDS_PATH, 0o600)

    expires_min = token.get("expires_in", 0) // 60
    print(f"\nSuccess! Token saved to {CREDS_PATH} (expires in {expires_min} min)")
    print("Restart the Qwen proxy to pick it up:")
    print("  docker compose --env-file .env.docker.secret restart qwen-code-api")


if __name__ == "__main__":
    main()
