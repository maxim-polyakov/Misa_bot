#!/usr/bin/env python3
"""Remove sudo from k3s deploy workflows; run project-local helper via bash."""
from __future__ import annotations

import base64
import json
import re
import subprocess
import sys

TARGETS: dict[str, list[str]] = {
    "maxim-polyakov/Misa_bot": [".github/workflows/deploy.yml"],
    "maxim-polyakov/businessCard": [".github/workflows/deploy.yml"],
    "maxim-polyakov/canban_desktop": [".github/workflows/deploy.yml"],
    "maxim-polyakov/e-commerce-java-two": [".github/workflows/deploy.yml"],
    "maxim-polyakov/lotus_game": [".github/workflows/deploy.yml"],
    "maxim-polyakov/misadrawing": [".github/workflows/deploy.yml"],
    "maxim-polyakov/AirflowMlflow": [".github/workflows/deploy.yml"],
    "maxim-polyakov/ForLogs": [".github/workflows/deploy.yml"],
    "maxim-polyakov/Tests": [".github/workflows/deploy.yml"],
    "baxic-top-projects/avicena-project": [".github/workflows/deploy.yml"],
    "baxic-top-projects/hackaton": [".github/workflows/deploy.yml"],
    "baxic-top-projects/fizuli-order": [".github/workflows/deploy.yml"],
    "baxic-top-projects/Galaxy-map": [".github/workflows/client.yml"],
}


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def put_file(repo: str, path: str, content: bytes, message: str) -> None:
    api = f"repos/{repo}/contents/{path}"
    sha = gh("api", api, "--jq", ".sha").strip()
    payload = {
        "message": message,
        "content": base64.b64encode(content).decode(),
        "branch": "main",
        "sha": sha,
    }
    subprocess.run(
        ["gh", "api", "-X", "PUT", api, "--input", "-"],
        input=json.dumps(payload).encode(),
        check=True,
    )


def patch(text: str) -> str:
    text = re.sub(
        r'^\s*sudo install -m 755 "\$DEPLOY_PATH/scripts/compose-k3s-sync\.sh" '
        r"/usr/local/sbin/compose-k3s-sync\s*\n",
        "",
        text,
        flags=re.M,
    )
    text = text.replace(
        "sudo -n /usr/local/sbin/compose-k3s-sync \\",
        'bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh" \\',
    )
    text = text.replace(
        "sudo -n /usr/local/sbin/compose-k3s-sync",
        'bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh"',
    )
    return text


def main() -> None:
    for repo, workflows in TARGETS.items():
        for wf in workflows:
            raw = json.loads(gh("api", f"repos/{repo}/contents/{wf}"))
            body = base64.b64decode(raw["content"]).decode()
            patched = patch(body)
            if patched == body:
                print("unchanged", repo, wf)
                continue
            put_file(
                repo,
                wf,
                patched.encode(),
                "deploy: run compose-k3s-sync from project scripts without sudo",
            )
            print("updated", repo, wf)


if __name__ == "__main__":
    main()
