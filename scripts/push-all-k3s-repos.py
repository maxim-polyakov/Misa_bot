#!/usr/bin/env python3
"""Push local k3s deploy artifacts to all GitHub repos via Contents API."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

REPOS: dict[str, list[tuple[Path, str]]] = {
    "maxim-polyakov/Misa_bot": [
        (SCRIPTS / "compose-k3s-sync.sh", "scripts/compose-k3s-sync.sh"),
        (ROOT / ".github/workflows/deploy.yml", ".github/workflows/deploy.yml"),
        (SCRIPTS / "rollout-compose-k3s-helper.py", "scripts/rollout-compose-k3s-helper.py"),
        (SCRIPTS / "rollout-no-sudo-deploy.py", "scripts/rollout-no-sudo-deploy.py"),
        (SCRIPTS / "inspect-deploy-workflows.py", "scripts/inspect-deploy-workflows.py"),
        (SCRIPTS / "push-helper-one.py", "scripts/push-helper-one.py"),
        (SCRIPTS / "push-all-k3s-repos.py", "scripts/push-all-k3s-repos.py"),
    ],
}

HELPER_ONLY = [
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

for repo in HELPER_ONLY:
    REPOS[repo] = [
        (SCRIPTS / "compose-k3s-sync.sh", "scripts/compose-k3s-sync.sh"),
    ]

COMMIT_MSG = (
    "chore: compose-k3s-sync SMTP public DNS only; drop compose hostAliases"
)


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def put_file(repo: str, repo_path: str, content: bytes, message: str) -> None:
    api = f"repos/{repo}/contents/{repo_path}"
    try:
        sha = gh("api", api, "--jq", ".sha").strip()
    except subprocess.CalledProcessError:
        sha = None
    payload: dict = {
        "message": message,
        "content": base64.b64encode(content).decode(),
        "branch": "main",
    }
    if sha:
        payload["sha"] = sha
    subprocess.run(
        ["gh", "api", "-X", "PUT", api, "--input", "-"],
        input=json.dumps(payload).encode(),
        check=True,
    )


def normalize_sh(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def main() -> None:
    only = sys.argv[1:]
    items = REPOS.items()
    if only:
        items = [(r, REPOS[r]) for r in only if r in REPOS]
    for repo, files in items:
        print(f"=== {repo} ===", flush=True)
        for local, remote in files:
            if not local.is_file():
                print("skip missing", local, file=sys.stderr)
                continue
            data = local.read_bytes()
            if local.suffix == ".sh":
                data = normalize_sh(data)
            put_file(repo, remote, data, COMMIT_MSG)
            print("  ok", remote, flush=True)


if __name__ == "__main__":
    main()
