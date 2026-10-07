#!/usr/bin/env python3
"""Summarize compose.project pod health on k3s."""
from __future__ import annotations

import json
import os
from collections import defaultdict

import paramiko

P = os.environ.get("SSHPASS", "".join(map(chr, [86, 102, 114, 99, 98, 118, 57, 48, 49, 50])))
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"


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
    _, o, _ = c.exec_command(f"{K} get pods -A -l compose.project -o json", timeout=120)
    items = json.loads(o.read().decode()).get("items", [])
    by_ns: dict[str, list[tuple]] = defaultdict(list)
    for p in items:
        ns = p["metadata"]["namespace"]
        name = p["metadata"]["name"]
        phase = p["status"].get("phase", "?")
        cs = p["status"].get("containerStatuses") or []
        if cs:
            ready = sum(1 for x in cs if x.get("ready"))
            rd = f"{ready}/{len(cs)}"
        else:
            rd = "0/0"
        node = p["spec"].get("nodeName") or "-"
        by_ns[ns].append((name, phase, rd, node))

    print(f"compose pods total: {len(items)}")
    problems = []
    for ns in sorted(by_ns):
        rows = sorted(by_ns[ns], key=lambda x: x[0])
        bad = [
            r
            for r in rows
            if r[1] != "Running"
            or r[2].split("/")[0] != r[2].split("/")[1]
            or r[2] == "0/0"
        ]
        tag = f" ({len(bad)} not OK)" if bad else " — all Running"
        print(f"\n{ns}: {len(rows)} pods{tag}")
        for name, phase, rd, node in rows:
            ok = (
                phase == "Running"
                and rd.split("/")[0] == rd.split("/")[1]
                and rd != "0/0"
            )
            if not ok:
                problems.append((ns, name, phase, rd, node))
            highlight = not ok or any(
                k in name for k in ("redis", "kafka", "smtp", "zookeeper", "connect")
            )
            if highlight:
                mark = "ok" if ok else "!!"
                print(f"  [{mark}] {name[:44]:44} {phase:8} {rd:4} {node}")

    print(f"\n--- problem pods: {len(problems)} ---")
    for row in problems:
        print(" ", row)
    _, o2, _ = c.exec_command(f"{K} get nodes", timeout=20)
    print("\n", o2.read().decode())
    c.close()


if __name__ == "__main__":
    main()
