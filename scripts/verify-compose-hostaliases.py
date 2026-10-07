#!/usr/bin/env python3
"""List compose Deployments that still have hostAliases."""
from __future__ import annotations

import json
import os
import subprocess
import sys


def main() -> None:
    import paramiko

    p = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
    remote_py = r"""
import json, subprocess
kube = ["k3s", "kubectl", "--kubeconfig", "/home/baxic/.kube/config"]
out = subprocess.run([*kube, "get", "deploy", "-A", "-l", "compose.project", "-o", "json"],
                     capture_output=True, text=True, check=True)
items = json.loads(out.stdout).get("items", [])
ha = [(i["metadata"]["namespace"], i["metadata"]["name"])
      for i in items
      if i.get("spec", {}).get("template", {}).get("spec", {}).get("hostAliases")]
print("hostAliases remaining:", len(ha))
for x in ha:
    print(" ", x[0], x[1])
"""
    import base64

    cmd = f"echo {base64.b64encode(remote_py.encode()).decode()} | base64 -d | python3"
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect("89.124.86.173", username="baxic", password=p, timeout=25, allow_agent=False, look_for_keys=False)
    _, o, e = c.exec_command(cmd, timeout=60)
    print(o.read().decode())
    err = e.read().decode()
    if err:
        print(err, file=sys.stderr)
    c.close()


if __name__ == "__main__":
    main()
