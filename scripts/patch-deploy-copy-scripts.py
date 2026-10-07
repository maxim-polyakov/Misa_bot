#!/usr/bin/env python3
"""Add scripts/ to appleboy scp source when compose-k3s-sync is used."""
from __future__ import annotations

import base64
import json
import re
import subprocess

REPOS = [
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

MSG = "fix: scp scripts/ on deploy so compose-k3s-sync helper is updated"


def patch(body: str) -> str | None:
    if "compose-k3s-sync.sh" not in body:
        return None

    def repl(m: re.Match[str]) -> str:
        src = m.group(1)
        parts = [p.strip() for p in src.split(",")]
        if "scripts" in parts:
            return m.group(0)
        # insert scripts before docker-compose.yml when present
        if "docker-compose.yml" in parts:
            idx = parts.index("docker-compose.yml")
            parts.insert(idx, "scripts")
        else:
            parts.append("scripts")
        new_src = ",".join(parts)
        return f'source: "{new_src}"'

    new_body, n = re.subn(r'source:\s*"([^"]+)"', repl, body, count=0)
    if n == 0:
        return None
    if new_body == body:
        return None
    return new_body


def main() -> None:
    for repo, fn in REPOS:
        path = f".github/workflows/{fn}"
        try:
            j = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/contents/{path}"], text=True))
        except subprocess.CalledProcessError:
            print("skip missing", repo, fn)
            continue
        body = base64.b64decode(j["content"]).decode()
        new = patch(body)
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
