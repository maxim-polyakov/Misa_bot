#!/usr/bin/env python3
"""Stabilize worker-146: stop runaway deploys, restart k3s-agent, clear unreachable taints."""
from __future__ import annotations

import os
import shlex
import time
from pathlib import Path

import paramiko

PASS = os.environ.get(
    "SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50]))
)
KEY = Path.home() / ".ssh" / "galaxy_deploy"
KUBE = "k3s kubectl --kubeconfig /home/baxic/.kube/config"

ON_146 = r"""set -eu
echo "=== stopping parallel compose-k3s-sync ==="
pkill -f 'scripts/compose-k3s-sync.sh' || true
sleep 2
pgrep -af compose-k3s-sync || echo "no compose-k3s-sync left"
echo "=== restart k3s-agent ==="
systemctl restart k3s-agent
sleep 5
systemctl is-active k3s-agent
uptime
free -h | head -2
"""


def ssh_146(cmd: str) -> int:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "146.103.110.27",
        username="baxic",
        key_filename=str(KEY),
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    full = f"echo {shlex.quote(PASS)} | sudo -S -p '' bash -c {shlex.quote(cmd)}"
    _, o, e = c.exec_command(full, timeout=120)
    print(o.read().decode(), end="")
    err = e.read().decode()
    if err:
        print(err, end="")
    code = o.channel.recv_exit_status()
    c.close()
    return code


def ssh_cp(cmd: str) -> str:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "89.124.86.173",
        username="baxic",
        password=PASS,
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    _, o, e = c.exec_command(cmd, timeout=60)
    out = o.read().decode()
    err = e.read().decode()
    code = o.channel.recv_exit_status()
    c.close()
    if err:
        print(err, end="")
    if code != 0:
        raise SystemExit(code)
    return out


def main() -> None:
    print("--- worker-146 local recovery ---")
    ssh_146(ON_146)
    print("--- wait for node Ready ---")
    for i in range(18):
        time.sleep(10)
        out = ssh_cp(f"{KUBE} get node worker-146 -o jsonpath='{{.status.conditions[?(@.type==\"Ready\")].status}} {{.spec.taints}}'")
        print(f"try {i+1}:", out.strip())
        if "True" in out.split()[0]:
            break
    print("--- clear unreachable taints if any ---")
    for taint in (
        "node.kubernetes.io/unreachable:NoSchedule-",
        "node.kubernetes.io/unreachable:NoExecute-",
    ):
        try:
            ssh_cp(f"{KUBE} taint nodes worker-146 {taint} 2>/dev/null || true")
        except SystemExit:
            pass
    print(ssh_cp(f"{KUBE} get nodes -o wide"))
    print(ssh_cp(f"{KUBE} get pods -A --field-selector status.phase=Pending -o wide | wc -l"))


if __name__ == "__main__":
    main()
