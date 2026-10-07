#!/usr/bin/env python3
import base64
import hashlib
import json
import subprocess
from pathlib import Path

LOCAL = Path(__file__).resolve().parent / "compose-k3s-sync.sh"
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


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    local = LOCAL.read_bytes()
    lh = content_hash(local)
    print(f"canonical (Misa_bot local): {len(local)} bytes, sha256={lh[:16]}...\n")
    groups: dict[str, list[str]] = {}
    for repo in REPOS:
        meta = json.loads(
            subprocess.check_output(
                ["gh", "api", f"repos/{repo}/contents/scripts/compose-k3s-sync.sh"],
                text=True,
            )
        )
        blob_sha = meta["sha"]
        b64 = subprocess.check_output(
            ["gh", "api", f"repos/{repo}/git/blobs/{blob_sha}", "--jq", ".content"],
            text=True,
        ).strip().strip('"')
        data = base64.b64decode(b64)
        h = content_hash(data)
        groups.setdefault(h, []).append(repo)
        tag = "match local" if h == lh else "different"
        print(f"  {repo}: git-blob {blob_sha[:12]}… size {meta['size']} — {tag}")

    print("\n--- unique contents ---")
    for h, repos in sorted(groups.items(), key=lambda x: -len(x[1])):
        label = " (= local Misa_bot)" if h == lh else ""
        print(f"  {len(repos)} repo(s) sha256={h[:16]}…{label}")
        for r in repos:
            print(f"    - {r}")


if __name__ == "__main__":
    main()
