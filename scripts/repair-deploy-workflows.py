#!/usr/bin/env python3
"""Fix truncated/broken deploy.yml workflow_dispatch SSH script blocks."""
from __future__ import annotations

import base64
import json
import re
import subprocess

# repo -> (workflow file, env-file arg for compose-k3s-sync, use --no-cache)
REPAIRS: dict[str, tuple[str, str | None, bool]] = {
    "maxim-polyakov/canban_desktop": ("deploy.yml", "client/.env", False),
    "maxim-polyakov/e-commerce-java-two": ("deploy.yml", "client/.env", False),
    "maxim-polyakov/lotus_game": ("deploy.yml", ".env", False),
    "maxim-polyakov/misadrawing": ("deploy.yml", "client/.env", False),
    "baxic-top-projects/hackaton": ("deploy.yml", ".env", False),
    "baxic-top-projects/fizuli-order": ("deploy.yml", "client/.env", False),
}

RESTORE_SHA: dict[str, str] = {
    "maxim-polyakov/canban_desktop": "43152e6e",
    "maxim-polyakov/e-commerce-java-two": "9dd7ce3d",
    "maxim-polyakov/lotus_game": "4984c47b",
    "maxim-polyakov/misadrawing": "93514692",
    "baxic-top-projects/hackaton": "fef0e07f",
    "baxic-top-projects/fizuli-order": "c2b88901",
}


def gh(*args: str) -> str:
    return subprocess.check_output(["gh", *args], text=True)


def fetch_at(repo: str, path: str, ref: str) -> str:
    j = json.loads(gh("api", f"repos/{repo}/contents/{path}?ref={ref}"))
    return base64.b64decode(j["content"]).decode()


def fetch_head(repo: str, path: str) -> tuple[str, str]:
    j = json.loads(gh("api", f"repos/{repo}/contents/{path}"))
    return base64.b64decode(j["content"]).decode(), j["sha"]


def put_file(repo: str, path: str, content: str, sha: str, message: str) -> None:
    api = f"repos/{repo}/contents/{path}"
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": "main",
        "sha": sha,
    }
    subprocess.run(
        ["gh", "api", "-X", "PUT", api, "--input", "-"],
        input=json.dumps(payload).encode(),
        check=True,
    )


def build_sync_script(env_file: str | None, no_cache: bool) -> str:
    lines = [
        '            cd "$DEPLOY_PATH"',
        "            export COMPOSE_BAKE=0",
        "            export BUILDX_NO_DEFAULT_ATTESTATIONS=1",
        "            export TMPDIR=/tmp",
        '            bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh" \\',
        '              --project-dir "$DEPLOY_PATH" \\',
    ]
    if env_file:
        lines.append(f"              --env-file {env_file} \\")
    if no_cache:
        lines.append("              --no-cache")
    else:
        lines[-1] = lines[-1].rstrip(" \\")
    return "          script: |\n" + "\n".join(lines) + "\n"


def replace_script_block(body: str, env_file: str | None, no_cache: bool) -> str:
    m = re.search(r"\n          script: \|\n", body)
    if not m:
        raise ValueError("script block not found")
    return body[: m.start() + 1] + build_sync_script(env_file, no_cache)


def needs_repair(body: str) -> bool:
    if re.search(r"script:\s*\|\n[^\s]", body):
        return True
    if body.rstrip().endswith("\\"):
        return True
    lines = body.splitlines()
    return len(lines) < 80 and "  deploy:" in body


def main() -> None:
    for repo, (fn, env_file, no_cache) in REPAIRS.items():
        path = f".github/workflows/{fn}"
        head, sha = fetch_head(repo, path)
        if not needs_repair(head):
            print("skip ok", repo)
            continue
        ref = RESTORE_SHA.get(repo, "main")
        try:
            body = fetch_at(repo, path, ref)
        except subprocess.CalledProcessError:
            body = head
        body = re.sub(
            r"sudo -n /usr/local/sbin/compose-k3s-sync",
            'bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh"',
            body,
        )
        body = replace_script_block(body, env_file, no_cache)
        put_file(
            repo,
            path,
            body,
            sha,
            "fix: restore complete deploy.yml workflow and compose-k3s-sync step",
        )
        print("fixed", repo, f"({len(body.splitlines())} lines)")


if __name__ == "__main__":
    main()
