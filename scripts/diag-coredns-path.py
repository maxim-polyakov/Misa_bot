#!/usr/bin/env python3
"""Why pod DNS fails while nodes/agents are Ready."""
from __future__ import annotations

import os

import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


def run(c: paramiko.SSHClient, cmd: str, timeout: int = 60) -> None:
    print(f"\n$ {cmd[:140]}")
    _, o, e = c.exec_command(cmd, timeout=timeout)
    out = o.read().decode()
    err = e.read().decode()
    if out:
        print(out[:4000])
    if err:
        print("stderr:", err[:1500])


def main() -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "89.124.86.173",
        username="baxic",
        password=P,
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )

    run(c, f"{K} get nodes -o wide")
    run(c, f"{K} get pods -n kube-system -o wide | grep -E 'coredns|NAME'")
    run(c, f"{K} get svc -n kube-system kube-dns -o wide 2>/dev/null; {K} get svc -n kube-system -l k8s-app=kube-dns -o wide")

    # Worker pod (146)
    run(
        c,
        f"{K} exec -n misa-bot deploy/misa-bot-server -- cat /etc/resolv.conf",
    )
    run(
        c,
        f"{K} exec -n misa-bot deploy/misa-bot-server -- sh -c "
        "'nslookup kubernetes.default.svc.cluster.local 10.43.0.10 2>&1; echo ---; "
        "nslookup misa-redis.misa-bot.svc.cluster.local 10.43.0.10 2>&1; echo ---; "
        "timeout 3 nc -zv 10.43.0.10 53 2>&1 || true'",
    )
    run(
        c,
        f"{K} get pod -n misa-bot -l compose.service=server -o jsonpath='node={{.items[0].spec.nodeName}} podIP={{.items[0].status.podIP}}\\n'",
    )

    # CoreDNS logs snippet
    run(
        c,
        f"{K} logs -n kube-system -l k8s-app=kube-dns --tail=15 2>&1 | tail -15",
    )

    # flannel on cp
    run(
        c,
        f"{K} get pods -n kube-system -l app=flannel -o wide 2>/dev/null; "
        f"{K} get pods -n kube-system | grep -i flannel",
    )

    c.close()


if __name__ == "__main__":
    main()
