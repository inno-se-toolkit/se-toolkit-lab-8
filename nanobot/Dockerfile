ARG REGISTRY_PREFIX_DOCKER_HUB

FROM astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

RUN apt-get update && apt-get install -y --no-install-recommends make gcc python3-dev

WORKDIR /app

COPY --from=workspace pyproject.toml uv.lock /app/
COPY --from=workspace nanobot-websocket-channel /app/nanobot-websocket-channel
COPY --from=workspace mcp /app/mcp
COPY pyproject.toml /app/nanobot/pyproject.toml
COPY entrypoint.py /app/nanobot/entrypoint.py
COPY config.json /app/nanobot/config.json
COPY --from=workspace nanobot/workspace /app/nanobot/workspace
COPY mcp_lms /app/nanobot/mcp_lms
COPY mcp_observability /app/nanobot/mcp_observability

RUN --mount=type=cache,target=/root/.cache/uv cd /app/nanobot && uv sync --frozen

FROM python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN groupadd --system --gid 999 nonroot && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/nanobot/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/usr/lib/wsl/lib:/mnt/c/Users/Davlat/AppData/Local/Programs/Microsoft VS Code:/mnt/c/WINDOWS/system32:/mnt/c/WINDOWS:/mnt/c/WINDOWS/System32/Wbem:/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/:/mnt/c/WINDOWS/System32/OpenSSH/:/mnt/c/Program Files/Microsoft SQL Server/150/Tools/Binn/:/mnt/d/CMake/bin:/mnt/d/Git/cmd:/mnt/c/ProgramData/chocolatey/bin:/mnt/c/mingw-w64-v12.0.0 (2)/mingw-w64-v12.0.0:/mnt/c/Program Files/dotnet/:/mnt/c/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit/:/Docker/host/bin:/mnt/c/Program Files/nodejs/:/mnt/c/Users/Davlat/.local/bin:/mnt/c/Users/Davlat/AppData/Local/Programs/Python/Launcher/:/mnt/c/Program Files/JetBrains/CLion 2023.2.1/CLion 2023.2.1:/mnt/c/Users/Davlat/AppData/Local/GitHubDesktop/bin:/mnt/d/IntelliJ IDEA 2023.2.2/bin:/mnt/c/Users/Davlat/AppData/Local/JetBrains/Toolbox/scripts:/mnt/d/PyCharm Community Edition 2023.3.2/bin:/mnt/d/CLion 2023.3.2/bin:/mnt/d/WebStorm 2024.1.3/bin:/mnt/c/Users/Davlat/AppData/Local/Programs/Ollama:/mnt/c/Users/Davlat/AppData/Local/Microsoft/WindowsApps:/mnt/d/JetBrains Rider 2024.3.8/bin:/mnt/c/Users/Davlat/.dotnet/tools:/mnt/c/Users/Davlat/AppData/Local/Programs/Microsoft VS Code/bin:/mnt/c/Users/Davlat/AppData/Roaming/npm"
ENV PYTHONPATH="/app/nanobot:/app/mcp"

USER nonroot
WORKDIR /app/nanobot

CMD ["python", "/app/nanobot/entrypoint.py"]
