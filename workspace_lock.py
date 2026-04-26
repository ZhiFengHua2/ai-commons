#!/usr/bin/env python3
"""
workspace_lock.py — Tiered write-conflict management

Usage (call before writing any shared file):
    from workspace_lock import acquire, release, LockConflict

    try:
        acquire("memory/user_profile.md", agent="my-agent")
        # ... write file ...
    except LockConflict as e:
        print(e)
    finally:
        release("memory/user_profile.md", agent="my-agent")

Risk levels (auto-detected by path):
    LOW  — memory/*.md   → wait for TTL, auto-retry once, silent log
    MED  — projects/**   → pause, write conflict-pending.json, notify user
"""
from __future__ import annotations
import json
import time
from datetime import datetime
from pathlib import Path

WORKSPACE  = Path(__file__).parent.resolve()
LOCKS_DIR  = WORKSPACE / ".locks"
CONFLICT_F = WORKSPACE / ".locks" / "conflict-pending.json"
LOG_FILE   = WORKSPACE / "shared_log.md"
LOCK_TTL   = 60


class LockConflict(Exception):
    pass


def _risk_level(filepath: str) -> str:
    try:
        rel = Path(filepath).relative_to(WORKSPACE)
    except ValueError:
        rel = Path(filepath)
    return "LOW" if rel.parts and rel.parts[0] == "memory" else "MED"


def _lock_path(filepath: str) -> Path:
    LOCKS_DIR.mkdir(exist_ok=True)
    return LOCKS_DIR / (Path(filepath).name + ".lock")


def _log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [workspace-lock] {msg}\n")


def _read_lock(lock_file: Path) -> dict | None:
    try:
        return json.loads(lock_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def _is_stale(data: dict) -> bool:
    try:
        ts = datetime.fromisoformat(data["ts"])
        return (datetime.now() - ts).total_seconds() > LOCK_TTL
    except Exception:
        return True


def acquire(filepath: str, agent: str, retry: bool = True) -> None:
    lock_file = _lock_path(filepath)
    level = _risk_level(filepath)
    existing = _read_lock(lock_file)

    if existing and not _is_stale(existing):
        owner = existing.get("agent", "unknown")
        if owner == agent:
            return  # reentrant, allow
        if level == "LOW" and retry:
            elapsed = (datetime.now() - datetime.fromisoformat(existing["ts"])).total_seconds()
            wait = max(1, LOCK_TTL - int(elapsed))
            _log(f"LOW conflict {filepath} — waiting {wait}s (held by {owner})")
            time.sleep(wait + 1)
            existing = _read_lock(lock_file)
            if existing and not _is_stale(existing):
                raise LockConflict(f"Still locked by {owner} after retry: {filepath}")
        else:
            _write_conflict_pending(filepath, agent, owner)
            raise LockConflict(
                f"Write conflict: {filepath} is being written by {owner}. "
                f"See .locks/conflict-pending.json for options."
            )

    if lock_file.exists():
        lock_file.unlink(missing_ok=True)

    lock_file.write_text(json.dumps({
        "agent": agent, "file": filepath, "ts": datetime.now().isoformat()
    }, ensure_ascii=False), encoding="utf-8")


def release(filepath: str, agent: str) -> None:
    lock_file = _lock_path(filepath)
    data = _read_lock(lock_file)
    if data and data.get("agent") == agent:
        lock_file.unlink(missing_ok=True)


def _write_conflict_pending(filepath: str, blocked: str, owner: str):
    LOCKS_DIR.mkdir(exist_ok=True)
    CONFLICT_F.write_text(json.dumps({
        "file": filepath,
        "blocked_agent": blocked,
        "lock_owner": owner,
        "ts": datetime.now().isoformat(),
        "user_options": ["override", "retry_in_30s", "manual_edit"],
        "resolved": False,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"[MED conflict] {filepath} — {blocked} blocked by {owner}, waiting for user")
