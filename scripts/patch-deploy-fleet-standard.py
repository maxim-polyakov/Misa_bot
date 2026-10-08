#!/usr/bin/env python3
"""Normalize compose-k3s-sync deploy step across fleet workflows."""
from __future__ import annotations

import base64
import json
import re
import subprocess

# repo, workflow filename
FLEET = [
    ("maxim-polyakov/Misa_bot", "deploy.yml"),
    ("maxim-polyakov/businessCard", "deploy.yml"),
    ("maxim-polyakov/canban_desktop", "deploy.yml"),
    ("maxim-polyakov/e-commerce-java-two", "deploy.yml"),
    ("maxim-polyakov/lotus_game", "deploy.yml"),
    ("maxim-polyakov/misadrawing", "deploy.yml"),
    ("maxim-polyakov/AirflowMlflow", "deploy.yml"),
    ("maxim-polyakov/ForLogs", "deploy.yml"),
    ("maxim-polyakov/Tests", "deploy.yml"),
    ("baxic-top-projects/hackaton", "deploy.yml"),
    ("baxic-top-projects/avicena-project", "deploy.yml"),
    ("baxic-top-projects/fizuli-order", "deploy.yml"),
    ("baxic-top-projects/Galaxy-map", "client.yml"),
]

MSG = "chore: standard compose-k3s-sync deploy (lock, stdbuf, no --no-cache)"


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def normalize(body: str) -> str | None:
    if "compose-k3s-sync" not in body:
        return None
    orig = body
    body = re.sub(r"\n\s+--no-cache\s*\n", "\n", body)
    body = re.sub(
        r"export COMPOSE_K3S_LOCK_WAIT=1800",
        'export COMPOSE_K3S_LOCK_WAIT="${COMPOSE_K3S_LOCK_WAIT:-300}"',
        body,
    )
    if "COMPOSE_K3S_LOCK_WAIT" not in body:
        body = body.replace(
            "export TMPDIR=/tmp\n",
            "export TMPDIR=/tmp\n"
            '            export COMPOSE_K3S_LOCK_WAIT="${COMPOSE_K3S_LOCK_WAIT:-300}"\n'
            "            export COMPOSE_K3S_CLEAR_ORPHAN_LOCK=1\n"
            '            echo "[deploy] starting compose-k3s-sync (lock wait ${COMPOSE_K3S_LOCK_WAIT}s max)"\n',
        )
    elif "COMPOSE_K3S_CLEAR_ORPHAN_LOCK" not in body:
        body = body.replace(
            "export COMPOSE_K3S_LOCK_WAIT=",
            "export COMPOSE_K3S_CLEAR_ORPHAN_LOCK=1\n            export COMPOSE_K3S_LOCK_WAIT=",
            1,
        )
    body = re.sub(
        r'(?<!stdbuf -oL -eL )bash "\$DEPLOY_PATH/scripts/compose-k3s-sync\.sh"',
        'stdbuf -oL -eL bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh"',
        body,
    )
    body = re.sub(
        r"docker compose pull && \\\n\s+bash ",
        "docker compose pull && \\\n             stdbuf -oL -eL bash ",
        body,
    )
    if "echo \"[deploy]" not in body and "appleboy/ssh-action" in body:
        body = re.sub(
            r"(script: \|\n)(            cd \"\$DEPLOY_PATH\")",
            r'\1            set -euo pipefail\n            echo "[deploy] $(date -Is) connected on $(hostname)"\n\2',
            body,
            count=1,
        )
    return body if body != orig else None


def main() -> None:
    for repo, fn in FLEET:
        path = f".github/workflows/{fn}"
        try:
            j = json.loads(gh("api", f"repos/{repo}/contents/{path}"))
        except subprocess.CalledProcessError:
            print("skip missing", repo, fn)
            continue
        body = base64.b64decode(j["content"]).decode()
        new = normalize(body)
        if new is None:
            print("skip ok", repo)
            continue
        payload = {
            "message": MSG,
            "content": base64.b64encode(new.encode()).decode(),
            "branch": "main",
            "sha": j["sha"],
        }
        subprocess.run(
            ["gh", "api", "-X", "PUT", f"repos/{repo}/contents/{path}", "--input", "-"],
            input=json.dumps(payload).encode(),
            check=True,
        )
        print("patched", repo, fn)


if __name__ == "__main__":
    main()
