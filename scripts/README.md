# Scripts

## qwen-auth.py

Authenticate with Qwen OAuth and save credentials to `~/.qwen/oauth_creds.json`.

### When to use

When the Qwen Code API proxy shows `"status": "expired"` or your agent returns `Error: Internal Server Error`, the OAuth token needs refreshing.

### Usage

On your VM:

```terminal
cd ~/se-toolkit-lab-8
python3 scripts/qwen-auth.py
```

The script will:

1. Request a device code from Qwen.
2. Print a URL — open it in your browser and authorize.
3. Press Enter in the terminal.
4. Exchange the code for an access token and save it to `~/.qwen/oauth_creds.json`.

After that, restart the Qwen proxy:

```terminal
docker compose --env-file .env.docker.secret restart qwen-code-api
```

### WAF troubleshooting

If the token exchange fails (Alibaba WAF blocks some datacenter IPs), the script prints a `curl` command. Run it from your laptop and save the output to `~/.qwen/oauth_creds.json` on the VM:

```terminal
# On your laptop — run the curl command the script printed
curl -s -X POST "https://chat.qwen.ai/api/v1/oauth2/token" ... > /tmp/qwen_token.json

# Copy to VM
scp /tmp/qwen_token.json YOUR_VM:~/.qwen/oauth_creds.json
```

### Checking token status

```terminal
curl -s -H "X-API-Key: YOUR_QWEN_CODE_API_KEY" http://localhost:42005/health
```

Look at `default_account.status` — should be `"healthy"`. If `"expired"`, re-run `qwen-auth.py`.
