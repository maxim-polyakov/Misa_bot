#!/usr/bin/env python3
"""Hit Canban/Lotus public APIs and in-cluster health from cp."""
from __future__ import annotations

import json
import os

import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


def run(c: paramiko.SSHClient, cmd: str, timeout: int = 60) -> str:
    print(f"$ {cmd[:130]}")
    _, o, e = c.exec_command(cmd, timeout=timeout)
    out = (o.read() + e.read()).decode()
    print(out[:2500])
    return out


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

    print("=== hostPort / services ===")
    run(
        c,
        f"{K} get svc -n canban-desktop -o wide; {K} get svc -n lotus-game -o wide",
    )

    # Discover listening ports on worker-146 for canban/lotus (hostPort)
    run(
        c,
        "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=8 baxic@146.103.110.27 "
        "'ss -ltn | grep -E \":5000|:8080|:80\" | head -15' 2>&1 || true",
        timeout=25,
    )

    urls = [
        ("canban web", "curl -sS -m 15 -o /dev/null -w 'code:%{http_code} time:%{time_total}\\n' https://canban.baxic.ru/"),
        ("canban api swagger", "curl -sS -m 15 -o /dev/null -w 'code:%{http_code}\\n' https://canbanapi.baxic.ru/swagger/index.html"),
        ("canban api health", "curl -sS -m 15 -w '\\ncode:%{http_code}\\n' https://canbanapi.baxic.ru/health 2>/dev/null || curl -sS -m 15 -w '\\ncode:%{http_code}\\n' https://canbanapi.baxic.ru/api/health"),
        ("lotus web", "curl -sS -m 15 -o /dev/null -w 'code:%{http_code} time:%{time_total}\\n' https://lotus.baxic.ru/"),
        ("lotus api actuator", "curl -sS -m 15 -w '\\ncode:%{http_code}\\n' https://lotusapi.baxic.ru/actuator/health"),
    ]
    print("\n=== public HTTPS ===")
    for label, cmd in urls:
        print(f"\n--- {label} ---")
        run(c, cmd)

    print("\n=== in-cluster (port-forward style via pod IP) ===")
    for ns, dep, path in [
        ("canban-desktop", "canban-desktop-api", "/"),
        ("lotus-game", "lotus-game-server", "/actuator/health"),
    ]:
        cmd = (
            f"IP=$({K} get pod -n {ns} -l compose.service -o jsonpath="
            f"'{{range .items}}{{if eq .metadata.labels.compose.service \"{'api' if 'canban' in ns else 'server'}\"}}{{.status.podIP}}{{end}}{{end}}' 2>/dev/null); "
            f"echo pod_ip=$IP; "
            f"curl -sS -m 10 -w '\\ncode:%{{http_code}}\\n' http://$IP:{'5000' if 'canban' in ns else '8080'}{path} 2>&1"
        )
        # simpler: get pod by deployment
        port = 5000 if "canban" in ns else 8080
        svc = "api" if "canban" in ns else "server"
        cmd = (
            f"POD=$({K} get pods -n {ns} -l compose.service={svc} "
            f"-o jsonpath='{{.items[0].status.podIP}}'); "
            f"echo {ns} pod=$POD; "
            f"curl -sS -m 12 -w '\\ncode:%{{http_code}}\\n' http://$POD:{port}{path}"
        )
        run(c, cmd)

    print("\n=== recent app logs (errors) ===")
    run(
        c,
        f"{K} logs -n canban-desktop deploy/canban-desktop-api --tail=30 | grep -iE 'redis|error|exception|fail' || echo '(no redis errors in tail)'",
    )
    run(
        c,
        f"{K} logs -n lotus-game deploy/lotus-game-server --tail=40 | grep -iE 'redis|kafka|error|exception|fail' || echo '(no redis/kafka errors in tail)'",
    )

    c.close()


if __name__ == "__main__":
    main()
