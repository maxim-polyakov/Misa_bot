#!/usr/bin/env python3
"""Copy canonical compose-k3s-sync.sh into fleet-export/<folder>/scripts/."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = Path(__file__).resolve().parent / "compose-k3s-sync.sh"
OUT = ROOT / "fleet-export"

FOLDERS = [
    "Misa_bot",
    "businessCard",
    "canban_desktop",
    "e-commerce-java-two",
    "lotus_game",
    "misadrawing",
    "AirflowMlflow",
    "ForLogs",
    "Tests",
    "hackaton",
    "avicena-project",
    "fizuli-order",
    "Galaxy-map",
]


def main() -> None:
    data = HELPER.read_bytes().replace(b"\r\n", b"\n")
    for name in FOLDERS:
        dest_dir = OUT / name / "scripts"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "compose-k3s-sync.sh"
        dest.write_bytes(data)
        print(dest, len(data))


if __name__ == "__main__":
    main()
