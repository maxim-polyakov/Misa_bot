#!/usr/bin/env python3
"""Install baxic kubeconfig using SSH private key (e.g. ~/.ssh/galaxy_deploy)."""
from __future__ import annotations

import os
import shlex
import sys
import time
from pathlib import Path

import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "146.103.110.27"
KEY = Path(
    sys.argv[2]
    if len(sys.argv) > 2
    else Path.home() / ".ssh" / "galaxy_deploy"
)
SUDO_PASS = os.environ.get("SSHPASS", "")

INSTALL = (
    "set -eu; "
    "install -d -o baxic -g baxic -m 700 /home/baxic/.kube; "
    "if [ -f /etc/rancher/k3s/compose-sync.yaml ]; then "
    "src=/etc/rancher/k3s/compose-sync.yaml; "
    "elif [ -f /etc/rancher/k3s/k3s.yaml ]; then "
    "src=/etc/rancher/k3s/k3s.yaml; "
    "else echo missing kubeconfig >&2; exit 1; fi; "
    "install -o baxic -g baxic -m 600 \"$src\" /home/baxic/.kube/config; "
    "wc -c /home/baxic/.kube/config"
)


def main() -> None:
    if not KEY.is_file():
        print(f"missing key: {KEY}", file=sys.stderr)
        sys.exit(1)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username="baxic",
        key_filename=str(KEY),
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    sudo_cmd = (
        f"echo {shlex.quote(SUDO_PASS)} | sudo -S -p '' bash -c {shlex.quote(INSTALL)}"
        if SUDO_PASS
        else f"sudo -n bash -c {shlex.quote(INSTALL)}"
    )
    _, stdout, stderr = client.exec_command(sudo_cmd, timeout=90)
    deadline = time.time() + 90
    while not stdout.channel.exit_status_ready():
        if time.time() > deadline:
            sys.exit(124)
        time.sleep(0.2)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    print(out, end="")
    if err:
        print(err, end="", file=sys.stderr)
    if code == 0:
        _, stdout, _ = client.exec_command(
            "k3s kubectl --kubeconfig /home/baxic/.kube/config get nodes -o name --request-timeout=15s",
            timeout=30,
        )
        print(stdout.read().decode(), end="")
        code = stdout.channel.recv_exit_status()
    client.close()
    if code == 0:
        print(f"OK {HOST}")
    sys.exit(code)


if __name__ == "__main__":
    main()
