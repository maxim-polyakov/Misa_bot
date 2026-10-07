#!/usr/bin/env python3
import base64
import json
import re
import subprocess

REPOS = [
    "maxim-polyakov/Misa_bot",
    "maxim-polyakov/businessCard",
    "maxim-polyakov/canban_desktop",
    "maxim-polyakov/e-commerce-java-two",
    "maxim-polyakov/lotus_game",
    "maxim-polyakov/misadrawing",
    "maxim-polyakov/AirflowMlflow",
    "maxim-polyakov/ForLogs",
    "maxim-polyakov/Tests",
    "baxic-top-projects/hackaton",
    "baxic-top-projects/avicena-project",
    "baxic-top-projects/fizuli-order",
    "baxic-top-projects/Galaxy-map",
]


def fetch(repo: str, path: str) -> str | None:
    try:
        raw = subprocess.check_output(
            ["gh", "api", f"repos/{repo}/contents/{path}"], text=True
        )
    except subprocess.CalledProcessError:
        return None
    j = json.loads(raw)
    return base64.b64decode(j["content"]).decode()


def main() -> None:
    for repo in REPOS:
        wf = (
            ".github/workflows/client.yml"
            if repo.endswith("Galaxy-map")
            else ".github/workflows/deploy.yml"
        )
        body = fetch(repo, wf)
        if body is None:
            print(f"{repo}: NO {wf}")
            continue
        src = re.search(r'source:\s*"([^"]*)"', body)
        print(
            f"{repo}: helper={'compose-k3s-sync' in body} "
            f"sudo={'sudo' in body} "
            f"compose_up={'compose up' in body} "
            f"scripts={'scripts' in (src.group(1) if src else '')} "
            f"source={src.group(1) if src else '?'}"
        )


if __name__ == "__main__":
    main()
