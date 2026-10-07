#!/usr/bin/env python3
"""TCP checks from app pods to compose Redis/Kafka service names."""
from __future__ import annotations

import json
import os
import textwrap

import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"

# (namespace, deploy to exec, host, port, label)
CHECKS = [
    ("misa-bot", "misa-bot-server", "misa-redis", 6379, "misa redis"),
    ("misa-bot", "misa-bot-server", "smtp-service-misa", 1025, "misa smtp"),
    ("galaxy-map", "galaxy-map-api-gateway", "redis", 6379, "galaxy redis"),
    ("galaxy-map", "galaxy-map-api-gateway", "kafka", 9092, "galaxy kafka:9092"),
    ("galaxy-map", "galaxy-map-catalog-service", "kafka", 9092, "catalog->kafka"),
    ("canban-desktop", "canban-desktop-api", "redis", 6379, "canban redis"),
    ("lotus-game", "lotus-game-server", "lotus-redis", 6379, "lotus redis"),
    ("wrighttest", "backend", "redis", 6379, "wrighttest redis"),
    ("e-commerce-java-two", "e-commerce-java-two-app", "smtp-service", 1025, "ecom smtp"),
]

PY = textwrap.dedent(
    """
    import socket, sys
    host, port = sys.argv[1], int(sys.argv[2])
    try:
        socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        s = socket.create_connection((host, port), 5)
        s.close()
        print("ok")
    except Exception as e:
        print("fail:", e)
        sys.exit(1)
    """
).strip()


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

    print("=== service ClusterIPs (compose.project) ===")
    _, o, _ = c.exec_command(
        f"{K} get svc -A -l compose.project -o json", timeout=60
    )
    svcs = json.loads(o.read().decode()).get("items", [])
    for name in ("redis", "kafka", "misa-redis", "galaxy-map-redis", "galaxy-map-kafka"):
        for s in svcs:
            n = s["metadata"]["name"]
            if name in n or n == name:
                ns = s["metadata"]["namespace"]
                ip = s["spec"].get("clusterIP")
                ports = [p.get("port") for p in s["spec"].get("ports", [])]
                print(f"  {ns}/{n} {ip} ports={ports}")

    print("\n=== TCP from app pods ===")

    def tcp_check(ns: str, deploy: str, host: str, port: int) -> str:
        py_cmd = (
            f"{K} exec -n {ns} deploy/{deploy} -- "
            f"python3 -c \"import socket;s=socket.create_connection(('{host}',{port}),5);"
            f"s.close();print('ok')\" 2>&1"
        )
        _, out, err = c.exec_command(py_cmd, timeout=45)
        text = (out.read() + err.read()).decode()
        if "ok" in text and "error" not in text.lower()[:20]:
            return "ok"
        sh_cmd = (
            f"{K} exec -n {ns} deploy/{deploy} -- "
            f"sh -c \"(echo >/dev/tcp/{host}/{port}) 2>/dev/null && echo ok || echo fail\" 2>&1"
        )
        _, out2, err2 = c.exec_command(sh_cmd, timeout=45)
        return (out2.read() + err2.read()).decode().strip().split()[-1][:80]

    for ns, deploy, host, port, label in CHECKS:
        text = tcp_check(ns, deploy, host, port)
        status = "OK" if text == "ok" else "FAIL"
        print(f"  [{status}] {label:22} {ns}/{deploy} -> {host}:{port}  ({text})")

    c.close()


if __name__ == "__main__":
    main()
