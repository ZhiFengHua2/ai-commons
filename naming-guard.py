#!/usr/bin/env python3
"""
naming-guard.py — Workspace naming convention scanner

Scans the workspace for files/directories that violate naming rules:
  - AI brand/company names in filenames
  - Runtime data directories in the shared workspace

Usage:
    python naming-guard.py [target_directory]

Exit codes:
    0 — check passed
    1 — violations found
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

WORKSPACE = Path(__file__).parent.resolve()


def _load_brand_names() -> set[str]:
    cfg = WORKSPACE / "rules" / "brand-names.txt"
    if not cfg.exists():
        return set()
    lines = cfg.read_text(encoding="utf-8").splitlines()
    return {l.strip().lower() for l in lines if l.strip() and not l.startswith("#")}


BRAND_NAMES = _load_brand_names()

RUNTIME_DIRS = {
    "sessions", "session-env", "file-history", "telemetry",
    "shell-snapshots", "downloads", "cache", "backups",
    "plugins", "ide",
}

RUNTIME_FILES = {
    "settings.json", ".credentials.json", ".mcp.json",
    "config.toml", "changelog.md", "startup.md",
    ".caveman-active", "history.jsonl",
}

EXEMPTIONS = {
    "agents.md", "agents", "prompt", "shared_log.md", "shared_log",
    "memory_sync.py", "naming-guard.py", "workspace-watcher.py",
    "workspace_lock.py", "init.py",
}

EXEMPTED_PARENT_DIRS = {".ai-cache"}

SKIP_BRAND_CHECK_FOR_HIDDEN = True


def check_name(name: str) -> list[str]:
    lower = name.lower()
    issues = []
    if lower in EXEMPTIONS:
        return issues
    for brand in sorted(BRAND_NAMES, key=len, reverse=True):
        if brand in lower:
            issues.append(f"contains AI brand name '{brand}'")
            break
    if lower in RUNTIME_DIRS:
        issues.append("runtime directory not allowed in shared workspace")
    if lower in RUNTIME_FILES:
        issues.append("runtime file not allowed in shared workspace")
    return issues


def scan(target: Path) -> list[tuple[Path, str, list[str]]]:
    violations = []
    target_resolved = target.resolve()
    for root, dirs, files in os.walk(target):
        root_path = Path(root).resolve()
        try:
            rel = root_path.relative_to(target_resolved)
        except ValueError:
            rel = root_path
        rel_parts = set(rel.parts)
        in_exempted_parent = bool(rel_parts & EXEMPTED_PARENT_DIRS)
        for d in dirs:
            if SKIP_BRAND_CHECK_FOR_HIDDEN and d.startswith("."):
                continue
            issues = check_name(d)
            if in_exempted_parent:
                issues = [i for i in issues if "runtime directory" not in i]
            if issues:
                violations.append((rel / d, "DIR", issues))
        for f in files:
            issues = check_name(f)
            if issues:
                violations.append((rel / f, "FILE", issues))
    return violations


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else WORKSPACE
    if not target.exists():
        print(f"[!] Directory not found: {target}")
        return 2
    print(f"Scanning: {target.resolve()}\n")
    violations = scan(target)
    if not violations:
        print("✓ Naming check passed. No violations found.")
        return 0
    print(f"⚠ {len(violations)} naming violation(s) found:\n")
    for path, ftype, issues in violations:
        icon = "DIR" if ftype == "DIR" else "FILE"
        print(f"  [{icon}] {path}")
        for issue in issues:
            print(f"         → {issue}")
        print()
    print("See rules/naming.md for correct naming conventions.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
