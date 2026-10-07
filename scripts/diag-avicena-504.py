#!/usr/bin/env python3
import os
import paramiko
import shlex
from pathlib import Path

p = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
k = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


def cp(cmd: str) -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("89.124.86.173", username="baxic", password=p, timeout=25, allow_agent=False, look_for_keys=False)
    print(f"$ {cmd[:110]}")
    _, o, e = c.exec_command(cmd, timeout=90)
    print(o.read().decode()[:8000])
    err = e.read().decode()
    if err:
        print("stderr:", err[:800])
    c.close()


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
    print(f"$ {cmd[:110]}")
    _, o, e = c.exec_command(cmd, timeout=90)
    print(o.read().decode()[:8000])
    err = e.read().decode()
    if err:
        print("stderr:", err[:800])
    c.close()


cp(f"{k} get deploy -n avicena-project -o yaml | grep -E 'hostPort|containerPort|hostAliases' -A1")
cp(
    f"{k} exec -n avicena-project deploy/server -- "
    "python -c \"import socket; s=socket.create_connection(('smtp-service-avicena',1025),5); print('smtp_ok'); s.close()\""
)
cp(
    f"{k} exec -n avicena-project deploy/server -- "
    "curl -sS -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/docs || true"
)

w192("curl -sS -m 5 -o /dev/null -w 'host3000:%{http_code}\\n' http://127.0.0.1:3000/ || echo fail3000")
w192("curl -sS -m 5 -o /dev/null -w 'host8080:%{http_code}\\n' http://127.0.0.1:8080/docs || echo fail8080")
w192("ss -ltn | grep -E '3000|8080|8185|1025' || true")
w192(f"echo {shlex.quote(p)} | sudo -S -p '' grep -R 'proxy_pass\\|avice\\|8080\\|3000' /etc/nginx/sites-enabled/ 2>/dev/null | head -30")
