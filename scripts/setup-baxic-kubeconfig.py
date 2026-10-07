#!/usr/bin/env python3
"""Install readable kubeconfig for baxic on k3s deploy nodes."""
from __future__ import annotations

import os
import shlex
import sys
import time

import paramiko

HOSTS = (
    "89.124.86.173",
    "146.103.110.27",
    "192.144.57.185",
    "45.150.37.39",
)


def run(client: paramiko.SSHClient, password: str, cmd: str, timeout: float = 60) -> tuple[int, str, str]:
    wrapped = f"echo {shlex.quote(password)} | sudo -S -p '' bash -c {shlex.quote(cmd)}"
    _, stdout, stderr = client.exec_command(wrapped, timeout=timeout)
    deadline = time.time() + timeout
    while not stdout.channel.exit_status_ready():
        if time.time() > deadline:
            stdout.channel.close()
            return 124, "", "timeout"
        time.sleep(0.2)
    code = stdout.channel.recv_exit_status()
    return code, stdout.read().decode(errors="replace"), stderr.read().decode(errors="replace")


def main() -> None:
    password = os.environ.get("SSHPASS")
    if not password:
        print("SSHPASS env required", file=sys.stderr)
        sys.exit(1)
    hosts = sys.argv[1:] or HOSTS
    failed = False
    install_cmd = (
        "set -eu; "
        "install -d -o baxic -g baxic -m 700 /home/baxic/.kube; "
        "if [ -f /etc/rancher/k3s/compose-sync.yaml ]; then "
        "src=/etc/rancher/k3s/compose-sync.yaml; "
        "elif [ -f /etc/rancher/k3s/k3s.yaml ]; then "
        "src=/etc/rancher/k3s/k3s.yaml; "
        "else echo missing kubeconfig >&2; exit 1; fi; "
        "install -o baxic -g baxic -m 600 \"$src\" /home/baxic/.kube/config"
    )
    for host in hosts:
        print(f"=== {host} ===", flush=True)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                host,
                username="baxic",
                password=password,
                timeout=20,
                allow_agent=False,
                look_for_keys=False,
            )
        except Exception as exc:
            print(f"connect failed: {exc}", file=sys.stderr)
            failed = True
            continue
        code, out, err = run(client, password, install_cmd)
        if out:
            print(out, end="")
        if err:
            print(err, end="", file=sys.stderr)
        if code != 0:
            print(f"install exit {code}", file=sys.stderr)
            failed = True
            client.close()
            continue
        _, stdout, stderr = client.exec_command(
            "test -r /home/baxic/.kube/config && wc -c /home/baxic/.kube/config",
            timeout=15,
        )
        print(stdout.read().decode(errors="replace"), end="")
        err = stderr.read().decode(errors="replace")
        if err:
            print(err, end="", file=sys.stderr)
        if stdout.channel.recv_exit_status() != 0:
            failed = True
        else:
            print("OK", flush=True)
        client.close()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
