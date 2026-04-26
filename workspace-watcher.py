#!/usr/bin/env python3
"""
workspace-watcher.py — Real-time workspace guard daemon

Monitors the workspace for file changes:
  - New files / renames trigger naming convention check
  - Violations are written to shared_log.md + OS native notification

Dependencies: pip install watchdog plyer
Usage:
    python workspace-watcher.py          (foreground, Ctrl+C to stop)
    python workspace-watcher.py --daemon (background mode)
"""
from __future__ import annotations
import sys
import time
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.resolve()
LOG_FILE  = WORKSPACE / "shared_log.md"
GUARD     = WORKSPACE / "naming-guard.py"

IGNORE_DIRS = {".git", ".ai-cache", ".locks", ".snapshots", "__pycache__"}


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [workspace-watcher] {msg}\n")


def notify(title: str, message: str):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, timeout=8)
    except Exception:
        print(f"[notify] {title}: {message}")


def check_path(path: str) -> list[str]:
    result = subprocess.run(
        [sys.executable, str(GUARD), str(WORKSPACE)],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    violations = []
    name = Path(path).name
    for line in result.stdout.splitlines():
        if name in line and ("→" in line or "violation" in line.lower()):
            violations.append(line.strip())
    return violations


def should_ignore(path: str) -> bool:
    return any(part in IGNORE_DIRS for part in Path(path).parts)


try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    class WorkspaceHandler(FileSystemEventHandler):
        def _handle(self, event, action: str):
            if event.is_directory:
                return
            src = event.src_path
            if should_ignore(src):
                return
            violations = check_path(src)
            if violations:
                desc = "; ".join(violations)
                log(f"[naming-violation] {action}: {src} — {desc}")
                notify("Workspace naming violation", f"{Path(src).name}\n{desc}")

        def on_created(self, event):
            self._handle(event, "created")

        def on_moved(self, event):
            event.src_path = event.dest_path
            self._handle(event, "renamed")

    WATCHDOG_OK = True

except ImportError:
    WATCHDOG_OK = False


def run():
    if not WATCHDOG_OK:
        print("[error] Missing dependency. Run: pip install watchdog plyer")
        sys.exit(1)
    observer = Observer()
    observer.schedule(WorkspaceHandler(), str(WORKSPACE), recursive=True)
    observer.start()
    log("workspace-watcher started")
    print(f"[workspace-watcher] Watching {WORKSPACE} — Ctrl+C to stop")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        log("workspace-watcher stopped")
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action="store_true")
    parser.parse_args()
    run()
