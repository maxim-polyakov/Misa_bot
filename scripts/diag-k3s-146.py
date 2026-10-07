#!/usr/bin/env python3
import os
import paramiko
from pathlib import Path

p = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
kube = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


def ssh_cp(*cmds: str) -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "89.124.86.173",
        username="baxic",
        password=p,
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    for cmd in cmds:
        print(f"$ {cmd[:100]}")
        _, o, e = c.exec_command(cmd, timeout=90)
        out = o.read().decode(errors="replace")
        err = e.read().decode(errors="replace")
        if out:
            print(out)
        if err:
            print("stderr:", err[:1500])
        print("exit", o.channel.recv_exit_status(), "\n")
    c.close()


def ssh_146(cmd: str) -> None:
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(
        "146.103.110.27",
        username="baxic",
        key_filename=str(Path.home() / ".ssh" / "galaxy_deploy"),
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    print(f"$ {cmd[:100]}")
    _, o, e = c.exec_command(cmd, timeout=90)
    out = o.read().decode(errors="replace")
    err = e.read().decode(errors="replace")
    if out:
        print(out)
    if err:
        print("stderr:", err[:1500])
    print("exit", o.channel.recv_exit_status(), "\n")
    c.close()


ssh_cp(
    f"{kube} get nodes -o wide",
    f"{kube} describe node worker-146",
    f"{kube} get pods -A --field-selector status.phase=Pending -o wide",
    f"{kube} get events -A --field-selector involvedObject.kind=Pod --sort-by=.lastTimestamp | tail -25",
)
ssh_146(
    "uptime; free -h; df -h / /mnt/data 2>/dev/null; "
    "echo PASS | sudo -S df -h 2>/dev/null | head -5; "
    "ps aux --sort=-%%cpu | head -12"
)
