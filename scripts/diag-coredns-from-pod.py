#!/usr/bin/env python3
import base64
import os
import textwrap

import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"

PY = textwrap.dedent(
    """
    import socket

    def query_udp(server, qname="google.com."):
        name = qname.rstrip(".") + "."
        tid = b"\\x12\\x34"
        hdr = tid + b"\\x01\\x00" + b"\\x00\\x01\\x00\\x00\\x00\\x00\\x00\\x00"
        q = b"".join(bytes([len(p)]) + p.encode() for p in name.split(".")) + b"\\x00\\x00\\x01\\x00\\x01"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.sendto(hdr + q, (server, 53))
        data, _ = s.recvfrom(512)
        print(f"udp53 {server} ok len={len(data)}")

    for host in ("misa-redis", "misa-redis.misa-bot.svc.cluster.local"):
        try:
            ip = socket.getaddrinfo(host, 6379, type=socket.SOCK_STREAM)[0][4][0]
            print(f"getaddrinfo {host} -> {ip}")
        except OSError as e:
            print(f"getaddrinfo {host} FAIL {e}")

    for srv in ("10.43.0.10", "8.8.8.8"):
        try:
            query_udp(srv)
        except OSError as e:
            print(f"udp53 {srv} FAIL {e}")
    """
).strip()

b64 = base64.b64encode(PY.encode()).decode()
cmd = (
    f"{K} exec -n misa-bot deploy/misa-bot-server -- "
    f"python3 -c \"import base64; exec(base64.b64decode('{b64}'))\""
)

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
print("$ dns test from misa-bot-server on worker-146")
_, o, e = c.exec_command(cmd, timeout=45)
print(o.read().decode())
print(e.read().decode())
c.close()
