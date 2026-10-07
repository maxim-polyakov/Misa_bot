#!/usr/bin/env python3
"""Add scripts/compose-k3s-sync.sh and install step to k3s deploy workflows."""
from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
from pathlib import Path

HELPER = Path(__file__).resolve().parent / "compose-k3s-sync.sh"
RUN_HELPER = 'bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh" \\\n'

# repo -> workflow paths (under .github/workflows/)
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


def patch_workflow(text: str, repo: str = "") -> str:
    if RUN_HELPER.strip() in text and "sudo -n /usr/local/sbin/compose-k3s-sync" not in text:
        if "scripts" in text or repo in (
            "maxim-polyakov/ForLogs",
            "maxim-polyakov/Tests",
            "maxim-polyakov/AirflowMlflow",
        ):
            return text
    if re.search(r'source:\s*"[^"]*"', text):
        def add_scripts(m: re.Match[str]) -> str:
            inner = m.group(1)
            if "scripts" in inner.split(","):
                return m.group(0)
            parts = [p.strip() for p in inner.split(",") if p.strip()]
            if "docker-compose.yml" in parts:
                idx = parts.index("docker-compose.yml")
                parts.insert(idx, "scripts")
            else:
                parts.append("scripts")
            return f'source: "{",".join(parts)}"'

        text = re.sub(r'source:\s*"([^"]*)"', add_scripts, text, count=1)
    for old in (
        "            sudo -n /usr/local/sbin/compose-k3s-sync \\",
        'bash "$DEPLOY_PATH/scripts/compose-k3s-sync.sh" \\',
    ):
        if old in text and RUN_HELPER.strip() not in text:
            text = text.replace(old, RUN_HELPER, 1)
            break
    else:
        if "compose-k3s-sync" not in text:
            pass
        elif RUN_HELPER.strip() not in text:
            text = text.replace(
                "            sudo -n /usr/local/sbin/compose-k3s-sync \\",
                RUN_HELPER,
                1,
            )
    text = re.sub(
        r'^\s*sudo install -m 755 "\$DEPLOY_PATH/scripts/compose-k3s-sync\.sh" '
        r"/usr/local/sbin/compose-k3s-sync\s*\n",
        "",
        text,
        flags=re.M,
    )
    text = text.replace(
        "sudo -n /usr/local/sbin/compose-k3s-sync \\",
        RUN_HELPER,
    )
    if repo == "maxim-polyakov/Tests" and "--compose-file compose.yaml" not in text:
        text = re.sub(
            r'(bash "\$DEPLOY_PATH/scripts/compose-k3s-sync\.sh" \\)\n',
            r'\1\n              --compose-file compose.yaml \\\n',
            text,
            count=1,
        )
    return text


def main() -> None:
    helper = HELPER.read_bytes()
    for repo, workflows in TARGETS.items():
        for wf in workflows:
            api = f"repos/{repo}/contents/{wf}"
            try:
                raw = json.loads(gh("api", api))
            except subprocess.CalledProcessError as err:
                print("skip", repo, wf, err, file=sys.stderr)
                continue
            body = base64.b64decode(raw["content"]).decode()
            patched = patch_workflow(body, repo)
            if patched != body:
                put_file(
                    repo,
                    wf,
                    patched.encode(),
                    "deploy: ship compose-k3s-sync with hostAliases on each deploy",
                )
                print("updated", repo, wf)
            else:
                print("ok", repo, wf)
        put_file(
            repo,
            "scripts/compose-k3s-sync.sh",
            helper,
            "add: compose-k3s-sync helper (compose service names on k3s)",
        )
        print("helper", repo)


if __name__ == "__main__":
    main()
