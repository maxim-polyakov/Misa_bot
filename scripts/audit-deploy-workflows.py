#!/usr/bin/env python3
"""Report broken/truncated deploy workflows on GitHub."""
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


def fetch(repo: str, fn: str) -> tuple[str, int, str]:
    path = f".github/workflows/{fn}"
    j = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/contents/{path}"], text=True))
    body = base64.b64decode(j["content"]).decode()
    return body, int(j["size"]), j["sha"]


def issues(body: str) -> list[str]:
    out: list[str] = []
    if "workflow_dispatch:" not in body:
        out.append("no_workflow_dispatch")
    if "compose-k3s-sync" not in body:
        out.append("no_helper")
    if re.search(r"script:\s*\|\n[^\s]", body):
        out.append("bad_script_indent")
    lines = body.splitlines()
    if len(lines) < 85 and "  deploy:" in body:
        out.append(f"short_{len(lines)}_lines")
    tail = body.rstrip()
    if tail.endswith("\\") or tail.endswith('bash "$DEPLOY_PATH'):
        out.append("truncated_tail")
    if "script: |" in body and "compose-k3s-sync.sh" in body:
        m = re.search(r"script:\s*\|\n(.*)", body, re.S)
        if m and not m.group(1).lstrip().startswith(("cd ", "if ", "bash ", "#")):
            if m.group(1).split("\n")[0].startswith("bash"):
                out.append("bad_script_indent")
    return out


def main() -> None:
    for repo, fn in REPOS:
        try:
            body, size, sha = fetch(repo, fn)
        except subprocess.CalledProcessError:
            print(f"{repo}: MISSING {fn}")
            continue
        prob = issues(body)
        status = "OK" if not prob else ",".join(prob)
        print(f"{repo:45} {size:5}B {status}")
        if prob:
            print("  last lines:", body.splitlines()[-3:])


if __name__ == "__main__":
    main()
