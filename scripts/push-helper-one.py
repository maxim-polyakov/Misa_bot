#!/usr/bin/env python3
"""Upload scripts/compose-k3s-sync.sh to one or more GitHub repos."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

HELPER = Path(__file__).resolve().parent / "compose-k3s-sync.sh"
DEFAULT_REPOS = [
    "maxim-polyakov/Misa_bot",
    "maxim-polyakov/businessCard",
    "maxim-polyakov/canban_desktop",
    "maxim-polyakov/e-commerce-java-two",
    "maxim-polyakov/lotus_game",
    "maxim-polyakov/misadrawing",
    "maxim-polyakov/AirflowMlflow",
    "maxim-polyakov/ForLogs",
    "maxim-polyakov/Tests",
    "baxic-top-projects/avicena-project",
    "baxic-top-projects/hackaton",
    "baxic-top-projects/fizuli-order",
    "baxic-top-projects/Galaxy-map",
]
REPOS = sys.argv[1:] or DEFAULT_REPOS


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def main() -> None:
    data = HELPER.read_bytes()
    for repo in REPOS:
        path = "scripts/compose-k3s-sync.sh"
        api = f"repos/{repo}/contents/{path}"
        try:
            sha = gh("api", api, "--jq", ".sha").strip()
        except subprocess.CalledProcessError:
            sha = None
        payload: dict = {
            "message": "fix: compose-k3s-sync lock file in /tmp (no /var/lock sudo)",
            "content": base64.b64encode(data).decode(),
            "branch": "main",
        }
        if sha:
            payload["sha"] = sha
        subprocess.run(
            ["gh", "api", "-X", "PUT", api, "--input", "-"],
            input=json.dumps(payload).encode(),
            check=True,
        )
        print("pushed", repo)


if __name__ == "__main__":
    main()
