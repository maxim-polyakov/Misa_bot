#!/usr/bin/env python3
"""Synchronize Compose projects with k3s after Docker containers are recreated."""

from __future__ import annotations

import json
import os
import select
import subprocess
import sys
import time
from dataclasses import dataclass


DEBOUNCE_SECONDS = int(os.environ.get("COMPOSE_K3S_DEBOUNCE", "20"))
HELPER = os.environ.get(
    "COMPOSE_K3S_HELPER", "/usr/local/sbin/compose-k3s-sync"
)


@dataclass
class PendingProject:
    project: str
    working_dir: str
    config_file: str | None
    env_file: str | None
    deadline: float


def log(message: str) -> None:
    print(f"[compose-k3s-watch] {message}", flush=True)


def relative_file(working_dir: str, value: str | None) -> str | None:
    if not value:
        return None
    first = value.split(",", 1)[0]
    if os.path.isabs(first):
        try:
            return os.path.relpath(first, working_dir)
        except ValueError:
            return first
    return first


def event_stream() -> subprocess.Popen[str]:
    return subprocess.Popen(
        [
            "docker",
            "events",
            "--format",
            "{{json .}}",
            "--filter",
            "type=container",
            "--filter",
            "event=start",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )


def queue_event(line: str, pending: dict[str, PendingProject]) -> None:
    try:
        event = json.loads(line)
    except json.JSONDecodeError:
        log(f"ignored malformed Docker event: {line.rstrip()}")
        return

    attributes = event.get("Actor", {}).get("Attributes", {})
    project = attributes.get("com.docker.compose.project")
    working_dir = attributes.get("com.docker.compose.project.working_dir")
    if not project or not working_dir:
        return

    pending[project] = PendingProject(
        project=project,
        working_dir=working_dir,
        config_file=relative_file(
            working_dir, attributes.get("com.docker.compose.project.config_files")
        ),
        env_file=relative_file(
            working_dir,
            attributes.get("com.docker.compose.project.environment_file"),
        ),
        deadline=time.monotonic() + DEBOUNCE_SECONDS,
    )
    log(f"queued {project}; waiting {DEBOUNCE_SECONDS}s for Compose to settle")


def sync_project(item: PendingProject) -> None:
    if not os.path.isdir(item.working_dir):
        log(f"skipped {item.project}: directory not found: {item.working_dir}")
        return

    command = [
        HELPER,
        "--project-dir",
        item.working_dir,
        "--skip-build",
    ]
    if item.config_file:
        command.extend(["--compose-file", item.config_file])
    if item.env_file and os.path.isfile(
        os.path.join(item.working_dir, item.env_file)
    ):
        command.extend(["--env-file", item.env_file])

    log(f"syncing {item.project}")
    result = subprocess.run(command, check=False)
    if result.returncode:
        log(f"sync failed for {item.project} with exit code {result.returncode}")
    else:
        log(f"sync completed for {item.project}")


def main() -> int:
    pending: dict[str, PendingProject] = {}

    while True:
        stream = event_stream()
        assert stream.stdout is not None
        log("watching Docker Compose start events")

        while stream.poll() is None:
            readable, _, _ = select.select([stream.stdout], [], [], 1)
            if readable:
                line = stream.stdout.readline()
                if line:
                    queue_event(line, pending)

            now = time.monotonic()
            due = [
                project
                for project, item in pending.items()
                if item.deadline <= now
            ]
            for project in due:
                sync_project(pending.pop(project))

        error = stream.stderr.read().strip() if stream.stderr else ""
        log(f"Docker event stream exited ({stream.returncode}): {error}")
        time.sleep(5)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        sys.exit(0)
