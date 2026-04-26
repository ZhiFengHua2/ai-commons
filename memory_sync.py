#!/usr/bin/env python3
"""
memory_sync.py — Memory backup and sync tool

Features:
  1. Backup before sync: git auto-commit (default) or rolling snapshots (fallback)
  2. Optional: sync to MemPalace if installed and configured

Backup strategy (auto-detected):
  git available → git init memory/ + auto-commit on each sync
  git not found → rolling snapshots: memory/.snapshots/YYYY-MM-DD_filename, keep 7 days

Usage: python memory_sync.py
"""
from __future__ import annotations
import os
import sys
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE     = Path(__file__).parent.resolve()
MEMORY_DIR    = WORKSPACE / "memory"
SNAPSHOT_DIR  = MEMORY_DIR / ".snapshots"
SNAPSHOT_KEEP = 7

GIT_ENV = {"GIT_TERMINAL_PROMPT": "0", "LANG": "C"}


# ── Backup ───────────────────────────────────────────────────────────────────

def _git_available() -> bool:
    return shutil.which("git") is not None


def _git_inited() -> bool:
    return (MEMORY_DIR / ".git").exists()


def _git_init():
    subprocess.run(["git", "init"], cwd=str(MEMORY_DIR),
                   capture_output=True, env={**os.environ, **GIT_ENV})
    gitignore = MEMORY_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(".snapshots/\n_prebaked/\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore"], cwd=str(MEMORY_DIR),
                   capture_output=True, env={**os.environ, **GIT_ENV})
    subprocess.run(["git", "commit", "-m", "init: memory git tracking"],
                   cwd=str(MEMORY_DIR), capture_output=True,
                   env={**os.environ, **GIT_ENV})
    print("  [git] memory/ initialized with version tracking")


def git_commit(msg: str = "auto: memory sync"):
    if not _git_inited():
        _git_init()
    subprocess.run(["git", "add", "-A"], cwd=str(MEMORY_DIR),
                   capture_output=True, env={**os.environ, **GIT_ENV})
    result = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=str(MEMORY_DIR), capture_output=True,
        text=True, encoding="utf-8", errors="replace",
        env={**os.environ, **GIT_ENV}
    )
    combined = (result.stdout or "") + (result.stderr or "")
    if "nothing to commit" in combined:
        print("  [git] no changes, skipping commit")
    else:
        print(f"  [git] committed: {msg}")


def snapshot_backup():
    SNAPSHOT_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    for src in MEMORY_DIR.glob("*.md"):
        dst = SNAPSHOT_DIR / f"{today}_{src.name}"
        if not dst.exists():
            shutil.copy2(src, dst)
    cutoff = datetime.now() - timedelta(days=SNAPSHOT_KEEP)
    removed = 0
    for old in SNAPSHOT_DIR.iterdir():
        try:
            date_str = old.name.split("_")[0]
            if datetime.strptime(date_str, "%Y-%m-%d") < cutoff:
                old.unlink()
                removed += 1
        except (ValueError, IndexError):
            pass
    if removed:
        print(f"  [snapshot] removed {removed} expired snapshots")


def backup():
    if _git_available():
        git_commit()
    else:
        snapshot_backup()
        print("  [snapshot] memory files backed up (install git for full history)")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Memory Sync")
    print("=" * 50)
    print("\n[1/2] Backing up memory...")
    backup()
    print("\n[2/2] Done.")
    print("\nTo restore a file:")
    if _git_available():
        print("  git -C memory/ log --oneline        # view history")
        print("  git -C memory/ checkout HEAD~1 -- filename.md  # restore")
    else:
        print("  Copy from memory/.snapshots/YYYY-MM-DD_filename.md")


if __name__ == "__main__":
    main()
