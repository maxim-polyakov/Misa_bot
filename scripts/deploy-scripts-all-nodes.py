#!/usr/bin/env python3
"""Refresh each project's compose-k3s-sync.sh and run fleet sync (patch or rollout)."""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass

import paramiko

PWD = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
BASE = "/home/baxic/Documents/GitHub"
HELPER = "scripts/compose-k3s-sync.sh"


@dataclass
class Project:
    host: str
    node_label: str
    folder: str
    github_repo: str
    env_args: str = ""
    jump_via: str | None = None
    skip_sync: bool = False
    skip_reason: str = ""


PROJECTS = [
    Project("146.103.110.27", "worker-146", "Misa_bot", "maxim-polyakov/Misa_bot", "--env-file client/.env"),
    Project("146.103.110.27", "worker-146", "businessCard", "maxim-polyakov/businessCard"),
    Project("146.103.110.27", "worker-146", "canban_desktop", "maxim-polyakov/canban_desktop"),
    Project("146.103.110.27", "worker-146", "e-commerce-java-two", "maxim-polyakov/e-commerce-java-two"),
    Project("146.103.110.27", "worker-146", "Galaxy-map", "baxic-top-projects/Galaxy-map"),
    Project("146.103.110.27", "worker-146", "lotus_game", "maxim-polyakov/lotus_game"),
    Project("146.103.110.27", "worker-146", "misadrawing", "maxim-polyakov/misadrawing"),
    Project(
        "146.103.110.27",
        "worker-146",
        "hackaton",
        "baxic-top-projects/hackaton",
        skip_sync=True,
        skip_reason="github/* Deployments lack compose.project labels",
    ),
    Project("146.103.110.27", "worker-146", "ai_stream_project", "maxim-polyakov/ForLogs"),
    Project(
        "192.144.57.185",
        "worker-192",
        "avicena-project",
        "baxic-top-projects/avicena-project",
        "--env-file .env",
        jump_via="146.103.110.27",
    ),
    Project("89.124.86.173", "cp-baxic", "AirflowMlflow", "maxim-polyakov/AirflowMlflow"),
    Project("89.124.86.173", "cp-baxic", "Writetest", "maxim-polyakov/Tests"),
    Project("45.150.37.39", "worker-45", "fizuli-order", "baxic-top-projects/fizuli-order"),
]


def connect(host: str, jump: str | None) -> paramiko.SSHClient:
    if not jump:
        c = paramiko.SSHClient()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host, username="baxic", password=PWD, timeout=30, allow_agent=False, look_for_keys=False)
        c.get_transport().set_keepalive(30)
        return c
    j = paramiko.SSHClient()
    j.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    j.connect(jump, username="baxic", password=PWD, timeout=30, allow_agent=False, look_for_keys=False)
    j.get_transport().set_keepalive(30)
    ch = j.get_transport().open_channel("direct-tcpip", (host, 22), ("127.0.0.1", 0), timeout=60)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="baxic", password=PWD, sock=ch, timeout=60, allow_agent=False, look_for_keys=False)
    c.get_transport().set_keepalive(30)
    return c


def run(c: paramiko.SSHClient, cmd: str, timeout: int = 900) -> tuple[int, str, str]:
    _, o, e = c.exec_command(cmd, timeout=timeout, get_pty=True)
    out = o.read().decode(errors="replace")
    err = e.read().decode(errors="replace")
    return o.channel.recv_exit_status(), out, err


def refresh_helper_shell(deploy: str, repo: str) -> str:
    raw = f"https://raw.githubusercontent.com/{repo}/main/{HELPER}"
    return f"""
set -e
deploy="{deploy}"
raw="{raw}"
mkdir -p "$deploy/scripts"
if [ -d "$deploy/.git" ]; then
  cd "$deploy"
  git fetch origin main 2>/dev/null || git fetch origin master
  br=main
  git show-ref --verify --quiet refs/remotes/origin/main || br=master
  git checkout "origin/$br" -- {HELPER}
else
  curl -fsSL "$raw" -o "$deploy/{HELPER}"
fi
chmod +x "$deploy/{HELPER}"
test -s "$deploy/{HELPER}"
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("patch-only", "skip-build", "build"),
        default="skip-build",
        help="patch-only: schema only; skip-build: rollout if images exist else patch; build: compose build + rollout",
    )
    parser.add_argument("--scripts-only", action="store_true", help="only refresh helper script on disk")
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="FOLDER",
        help="limit to project folder names (e.g. Misa_bot Galaxy-map)",
    )
    args = parser.parse_args()

    sync_flags = {
        "patch-only": "--patch-only",
        "skip-build": "--skip-build",
        "build": "",
    }[args.mode]

    only = set(args.only) if args.only else None
    failures: list[str] = []
    for proj in PROJECTS:
        if only and proj.folder not in only:
            continue
        deploy = f"{BASE}/{proj.folder}"
        print(f"\n--- {proj.node_label} / {proj.folder} ---", flush=True)
        try:
            c = connect(proj.host, proj.jump_via)
        except Exception as exc:
            print(f"  connect FAIL: {exc}")
            failures.append(f"{proj.folder}: connect")
            continue
        refresh_timeout = 300 if proj.jump_via else 120
        _, chk, _ = run(
            c,
            f'test -f "{deploy}/docker-compose.yml" && echo ok || echo no-compose',
            timeout=30,
        )
        if "no-compose" in chk:
            print("  skip: no docker-compose.yml")
            c.close()
            continue
        code, out, err = run(c, refresh_helper_shell(deploy, proj.github_repo), timeout=refresh_timeout)
        print(out)
        if err.strip():
            print(err, file=sys.stderr)
        if code != 0:
            failures.append(f"{proj.folder}: refresh({code})")
            c.close()
            continue
        if args.scripts_only:
            print("  OK (helper only)")
            c.close()
            continue
        if proj.skip_sync:
            print(f"  OK (helper only; sync skipped: {proj.skip_reason})")
            c.close()
            continue
        extra = f" {proj.env_args}" if proj.env_args else ""
        sync = f'bash "{deploy}/{HELPER}" --project-dir "{deploy}"{extra} {sync_flags} --timeout 20m'
        sync = sync.strip()
        code, out, err = run(c, sync, timeout=1500)
        print(out)
        if err.strip():
            print(err, file=sys.stderr)
        c.close()
        if code != 0:
            failures.append(f"{proj.folder}: sync({code})")
            print(f"  sync exit {code}")
        else:
            print("  OK")

    print("\n======== summary ========")
    if failures:
        print("FAILED:", ", ".join(failures))
        sys.exit(1)
    print("done")


if __name__ == "__main__":
    main()
