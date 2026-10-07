#!/usr/bin/env python3
"""On each server project dir: refresh that repo's compose-k3s-sync.sh, then run it."""
from __future__ import annotations

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
    github_repo: str  # for non-git deploy dirs: raw fetch
    env_args: str = ""
    jump_via: str | None = None


PROJECTS = [
    Project("146.103.110.27", "worker-146", "Misa_bot", "maxim-polyakov/Misa_bot", "--env-file client/.env"),
    Project("146.103.110.27", "worker-146", "businessCard", "maxim-polyakov/businessCard"),
    Project("146.103.110.27", "worker-146", "canban_desktop", "maxim-polyakov/canban_desktop"),
    Project("146.103.110.27", "worker-146", "e-commerce-java-two", "maxim-polyakov/e-commerce-java-two"),
    Project("146.103.110.27", "worker-146", "Galaxy-map", "baxic-top-projects/Galaxy-map"),
    Project("146.103.110.27", "worker-146", "lotus_game", "maxim-polyakov/lotus_game"),
    Project("146.103.110.27", "worker-146", "misadrawing", "maxim-polyakov/misadrawing"),
    Project("146.103.110.27", "worker-146", "hackaton", "baxic-top-projects/hackaton"),
    Project("146.103.110.27", "worker-146", "ForLogs", "maxim-polyakov/ForLogs"),
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
        c.connect(host, username="baxic", password=PWD, timeout=25, allow_agent=False, look_for_keys=False)
        return c
    j = paramiko.SSHClient()
    j.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    j.connect(jump, username="baxic", password=PWD, timeout=25, allow_agent=False, look_for_keys=False)
    ch = j.get_transport().open_channel("direct-tcpip", (host, 22), ("127.0.0.1", 0), timeout=25)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(host, username="baxic", password=PWD, sock=ch, timeout=25, allow_agent=False, look_for_keys=False)
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
repo="{repo}"
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
    failures: list[str] = []
    for proj in PROJECTS:
        deploy = f"{BASE}/{proj.folder}"
        print(f"\n--- {proj.node_label} / {proj.folder} ---", flush=True)
        try:
            c = connect(proj.host, proj.jump_via)
        except Exception as exc:
            print(f"  connect FAIL: {exc}")
            failures.append(f"{proj.folder}: connect")
            continue
        _, chk, _ = run(
            c,
            f'test -f "{deploy}/docker-compose.yml" && echo ok || echo no-compose',
            timeout=30,
        )
        if "no-compose" in chk:
            print("  skip: no docker-compose.yml")
            c.close()
            continue
        code, out, err = run(c, refresh_helper_shell(deploy, proj.github_repo), timeout=120)
        print(out)
        if err.strip():
            print(err, file=sys.stderr)
        if code != 0:
            failures.append(f"{proj.folder}: refresh({code})")
            c.close()
            continue
        extra = f" {proj.env_args}" if proj.env_args else ""
        sync = (
            f'bash "{deploy}/{HELPER}" --project-dir "{deploy}"{extra} '
            f"--skip-build --timeout 15m"
        )
        code, out, err = run(c, sync, timeout=960)
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
    print("done — each project used its own scripts/compose-k3s-sync.sh")


if __name__ == "__main__":
    main()
