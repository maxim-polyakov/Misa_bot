#!/usr/bin/env python3
"""Install baxic kubeconfig on a host via SSH jump (cp -> target)."""
from __future__ import annotations

import os
import shlex
import sys
import time

import paramiko

JUMP = "89.124.86.173"
TARGET = sys.argv[1] if len(sys.argv) > 1 else "146.103.110.27"

INSTALL = (
    "set -eu; "
    "install -d -o baxic -g baxic -m 700 /home/baxic/.kube; "
    "if [ -f /etc/rancher/k3s/compose-sync.yaml ]; then "
    "src=/etc/rancher/k3s/compose-sync.yaml; "
    "elif [ -f /etc/rancher/k3s/k3s.yaml ]; then "
    "src=/etc/rancher/k3s/k3s.yaml; "
    "else echo missing kubeconfig >&2; exit 1; fi; "
    "install -o baxic -g baxic -m 600 \"$src\" /home/baxic/.kube/config; "
    "test -r /home/baxic/.kube/config && wc -c /home/baxic/.kube/config"
)


def main() -> None:
    password = os.environ.get("SSHPASS")
    if not password:
        print("SSHPASS env required", file=sys.stderr)
        sys.exit(1)

    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump.connect(
        JUMP,
        username="baxic",
        password=password,
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )

    remote = (
        f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=20 baxic@{TARGET} "
        f"{shlex.quote('echo ' + shlex.quote(password) + ' | sudo -S -p \"\" bash -c ' + shlex.quote(INSTALL))}"
    )
    _, stdout, stderr = jump.exec_command(remote, timeout=120)
    deadline = time.time() + 120
    while not stdout.channel.exit_status_ready():
        if time.time() > deadline:
            print("timeout", file=sys.stderr)
            sys.exit(1)
        time.sleep(0.2)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    if out:
        print(out, end="")
    if err:
        print(err, end="", file=sys.stderr)
    jump.close()
    if code == 0:
        print(f"OK {TARGET} via {JUMP}")
    sys.exit(code)


if __name__ == "__main__":
    main()
