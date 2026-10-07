#!/usr/bin/env python3
import os
import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"

cmds = [
    f"{K} exec -n canban-desktop deploy/canban-desktop-redis -- redis-cli ping",
    f"{K} logs -n canban-desktop deploy/canban-desktop-api --tail=20",
    f"{K} exec -n lotus-game deploy/lotus-game-lotus-redis -- redis-cli ping",
    f"{K} logs -n lotus-game deploy/lotus-game-server --tail=20",
    f"{K} get deploy canban-desktop-api -n canban-desktop -o jsonpath='{{range .spec.template.spec.containers[0].env}}{{println .name .value}}{{end}}' | grep -i redis",
]

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect("89.124.86.173", username="baxic", password=P, timeout=25, allow_agent=False, look_for_keys=False)
for cmd in cmds:
    print("$", cmd[:100])
    _, o, e = c.exec_command(cmd, timeout=45)
    print((o.read() + e.read()).decode()[:2000])
    print()
c.close()
