#!/usr/bin/env python3
import json
import os
import paramiko
import shlex
from pathlib import Path

p = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
k = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


def w192(cmd: str) -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "192.144.57.185",
        username="baxic",
        key_filename=str(Path.home() / ".ssh" / "avicena_deploy"),
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    print(f"$ {cmd[:120]}")
    _, o, e = c.exec_command(cmd, timeout=120)
    print(o.read().decode()[:6000])
    err = e.read().decode()
    if err:
        print("stderr:", err[:1000])
    c.close()


def cp(cmd: str) -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("89.124.86.173", username="baxic", password=p, timeout=25, allow_agent=False, look_for_keys=False)
    print(f"$ {cmd[:120]}")
    _, o, e = c.exec_command(cmd, timeout=120)
    print(o.read().decode()[:6000])
    err = e.read().decode()
    if err:
        print("stderr:", err[:1000])
    c.close()


body = json.dumps(
    {
        "company": "test",
        "name": "test",
        "phone": "+70000000000",
        "message": "diag",
        "source": "main",
    }
)
body_q = shlex.quote(body)

w192(
    f"curl -sS -m 60 -w '\\nhttp:%{{http_code}} time:%{{time_total}}\\n' "
    f"-H 'Content-Type: application/json' -d {body_q} "
    f"http://127.0.0.1:8080/api/inquiries || true"
)
w192(
    "curl -sS -m 10 -w '\\nhttps:%{http_code} time:%{time_total}\\n' "
    "-H 'Content-Type: application/json' -d '{\"company\":\"t\",\"name\":\"t\",\"phone\":\"1\",\"message\":\"m\",\"source\":\"main\"}' "
    "https://api.avice.su/api/inquiries || true"
)
w192(f"echo {shlex.quote(p)} | sudo -S -p '' ss -ltnp | grep -E ':3000|:8080|:8185' || true")
cp(f"{k} logs -n avicena-project deploy/server --tail=40")
cp(f"{k} logs -n avicena-project deploy/smtp-service-avicena --tail=30")
