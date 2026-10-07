#!/usr/bin/env python3
"""Ensure Deploy SSH scripts export compose build env before compose-k3s-sync."""
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

BUILD_ENV = """            export COMPOSE_BAKE=0
            export BUILDX_NO_DEFAULT_ATTESTATIONS=1
            export TMPDIR=/tmp
"""

MSG = "fix: export compose build env in Deploy (metadata-file flake)"


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def patch(body: str) -> str | None:
    if "BUILDX_NO_DEFAULT_ATTESTATIONS" in body:
        return None
    if "compose-k3s-sync.sh" not in body:
        return None
    m = re.search(
        r'\n            bash "\$DEPLOY_PATH/scripts/compose-k3s-sync\.sh"',
        body,
    )
    if not m:
        return None
    return body[: m.start()] + "\n" + BUILD_ENV.rstrip() + body[m.start() :]


def main() -> None:
    for repo, fn in REPOS:
        path = f".github/workflows/{fn}"
        try:
            j = json.loads(gh("api", f"repos/{repo}/contents/{path}"))
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
