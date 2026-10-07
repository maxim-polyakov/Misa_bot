#!/usr/bin/env python3
"""Grant baxic k3s containerd access (k3s group + passwordless k3s ctr sudo)."""
from __future__ import annotations

import os
import shlex
import sys
import time
from pathlib import Path

import paramiko

# host -> optional private key path (password from SSHPASS if no key)
NODES: list[tuple[str, str | None]] = [
    ("146.103.110.27", str(Path.home() / ".ssh" / "galaxy_deploy")),
    ("192.144.57.185", str(Path.home() / ".ssh" / "avicena_deploy")),
    ("89.124.86.173", None),
    ("45.150.37.39", None),
]

REMOTE = r"""set -eu
K3S=$(command -v k3s)
if getent group k3s >/dev/null; then
  usermod -aG k3s baxic || true
fi
printf 'baxic ALL=(root) NOPASSWD: %s ctr *\n' "$K3S" > /tmp/baxic-k3s-ctr.sudoers
visudo -cf /tmp/baxic-k3s-ctr.sudoers
install -o root -g root -m 0440 /tmp/baxic-k3s-ctr.sudoers /etc/sudoers.d/baxic-k3s-ctr
rm -f /tmp/baxic-k3s-ctr.sudoers
echo "sudoers:" /etc/sudoers.d/baxic-k3s-ctr
cat /etc/sudoers.d/baxic-k3s-ctr
"""


def connect(host: str, key_path: str | None, password: str) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    kwargs: dict = dict(
        hostname=host,
        username="baxic",
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )
    if key_path and Path(key_path).is_file():
        kwargs["key_filename"] = key_path
    else:
        kwargs["password"] = password
    client.connect(**kwargs)
    return client


def run_sudo(client: paramiko.SSHClient, password: str) -> tuple[int, str, str]:
    inner = shlex.quote(REMOTE)
    cmd = f"echo {shlex.quote(password)} | sudo -S -p '' bash -c {inner}"
    _, stdout, stderr = client.exec_command(cmd, timeout=90)
    deadline = time.time() + 90
    while not stdout.channel.exit_status_ready():
        if time.time() > deadline:
            return 124, "", "timeout"
        time.sleep(0.2)
    code = stdout.channel.recv_exit_status()
    return code, stdout.read().decode(errors="replace"), stderr.read().decode(errors="replace")


def main() -> None:
    password = os.environ.get("SSHPASS", "")
    if not password:
        print("SSHPASS env required for sudo on nodes", file=sys.stderr)
        sys.exit(1)
    only = set(sys.argv[1:])
    nodes = [(h, k) for h, k in NODES if not only or h in only]
    failed = False
    for host, key in nodes:
        print(f"=== {host} ===", flush=True)
        try:
            client = connect(host, key, password)
        except Exception as exc:
            print(f"connect failed: {exc}", file=sys.stderr)
            failed = True
            continue
        code, out, err = run_sudo(client, password)
        if out:
            print(out, end="")
        if err:
            print(err, end="", file=sys.stderr)
        if code != 0:
            print(f"setup exit {code}", file=sys.stderr)
            failed = True
            client.close()
            continue
        _, stdout, stderr = client.exec_command(
            "timeout 15 sudo -n k3s ctr -n k8s.io version >/dev/null",
            timeout=25,
        )
        out = stdout.read().decode(errors="replace")
        err = stderr.read().decode(errors="replace")
        code = stdout.channel.recv_exit_status()
        if out:
            print(out, end="")
        if err:
            print(err, end="", file=sys.stderr)
        if code != 0:
            print(f"verify failed exit {code}", file=sys.stderr)
            failed = True
        else:
            print("OK", flush=True)
        client.close()
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
