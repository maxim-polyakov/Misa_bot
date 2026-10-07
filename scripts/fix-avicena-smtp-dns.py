#!/usr/bin/env python3
"""Patch Avicena Maildev deployment DNS and verify inquiry API."""
import json
import os
from pathlib import Path

import paramiko

HOST = "192.144.57.185"
USER = "baxic"
K = "k3s kubectl --kubeconfig /home/baxic/.kube/config"
NS = "avicena-project"
DEPLOY = "smtp-service-avicena"

DNS_PATCH = {
    "spec": {
        "template": {
            "spec": {
                "dnsConfig": {
                    "nameservers": ["8.8.8.8", "1.1.1.1"],
                    "searches": [
                        "avicena-project.svc.cluster.local",
                        "svc.cluster.local",
                        "cluster.local",
                    ],
                    "options": [{"name": "ndots", "value": "5"}],
                }
            }
        }
    }
}


def run(client: paramiko.SSHClient, cmd: str, timeout: int = 120) -> str:
    print(f"$ {cmd}")
    _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out:
        print(out.rstrip())
    if err:
        print(err.rstrip())
    return out + err


def main() -> None:
    password = os.environ.get("SSHPASS", "")
    key = str(Path.home() / ".ssh" / "avicena_deploy")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, password=password or None, key_filename=key)

    run(client, f"{K} exec -n {NS} deploy/{DEPLOY} -- cat /etc/resolv.conf")
    run(
        client,
        f"{K} exec -n {NS} deploy/{DEPLOY} -- sh -c "
        "'nslookup smtp.gmail.com 2>&1 || getent hosts smtp.gmail.com'",
    )

    patch_json = json.dumps(DNS_PATCH)
    run(
        client,
        f"{K} patch deployment {DEPLOY} -n {NS} --type merge -p '{patch_json}'",
    )
    run(
        client,
        f"{K} rollout status deployment/{DEPLOY} -n {NS} --timeout=120s",
    )
    run(
        client,
        f"{K} exec -n {NS} deploy/{DEPLOY} -- sh -c "
        "'nslookup smtp.gmail.com 2>&1 || getent hosts smtp.gmail.com'",
    )

    payload = (
        '{"company":"Test Co","name":"Test","phone":"+79991234567",'
        '"message":"dns-fix-test","source":"buyers","consent":true}'
    )
    run(
        client,
        "curl -sS -m 120 -w '\\nhttp:%{http_code} time:%{time_total}\\n' "
        f"-H 'Content-Type: application/json' -d '{payload}' "
        "http://127.0.0.1:8080/api/inquiries",
        timeout=130,
    )
    run(client, f"{K} logs -n {NS} deploy/smtp-service-avicena --tail=15")
    client.close()


if __name__ == "__main__":
    main()
