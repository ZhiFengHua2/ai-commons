#!/usr/bin/env python3
"""
init.py — AI Workspace first-time setup wizard

Run once when you (or your AI) first opens this workspace:
    python init.py

What it does:
  1. Registers your agent's brand keywords in rules/brand-names.txt
  2. Initializes git version tracking for memory/ (or falls back to snapshots)
  3. Creates a bootstrap index for Claude Code (if applicable)
  4. Writes an onboarding entry to shared_log.md
"""
from __future__ import annotations
import os
import sys
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).parent.resolve()

GIT_ENV = {"GIT_TERMINAL_PROMPT": "0", "LANG": "C"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _ask(prompt: str, default: str = "") -> str:
    if default:
        val = input(f"{prompt} [{default}]: ").strip()
        return val if val else default
    return input(f"{prompt}: ").strip()


def _yn(prompt: str, default: bool = True) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    val = input(f"{prompt} {hint}: ").strip().lower()
    if not val:
        return default
    return val in ("y", "yes")


def _log(msg: str):
    log_file = WORKSPACE / "shared_log.md"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [init] {msg}\n")


# ── Steps ─────────────────────────────────────────────────────────────────────

def step_register_agent(agent_name: str, brand_keywords: list[str]):
    brand_file = WORKSPACE / "rules" / "brand-names.txt"
    existing = brand_file.read_text(encoding="utf-8").lower()
    added = []
    for kw in brand_keywords:
        kw = kw.strip().lower()
        if kw and kw not in existing:
            with open(brand_file, "a", encoding="utf-8") as f:
                f.write(f"{kw}\n")
            added.append(kw)
    if added:
        print(f"  ✓ brand-names.txt updated: {', '.join(added)}")
    else:
        print(f"  ✓ brand-names.txt already up to date")


def step_init_git():
    memory_dir = WORKSPACE / "memory"
    git_dir = memory_dir / ".git"
    if git_dir.exists():
        print("  ✓ memory/ git already initialized")
        return
    subprocess.run(["git", "init"], cwd=str(memory_dir),
                   capture_output=True, env={**os.environ, **GIT_ENV})
    gitignore = memory_dir / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(".snapshots/\n_prebaked/\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=str(memory_dir),
                   capture_output=True, env={**os.environ, **GIT_ENV})
    subprocess.run(["git", "commit", "-m", "init: memory tracking"],
                   cwd=str(memory_dir), capture_output=True,
                   env={**os.environ, **GIT_ENV})
    print("  ✓ memory/ git initialized")


def step_init_snapshots():
    snapshot_dir = WORKSPACE / "memory" / ".snapshots"
    snapshot_dir.mkdir(exist_ok=True)
    print("  ✓ memory/.snapshots/ created (rolling backup mode)")
    print("    Install git for full version history.")


def step_claude_bootstrap():
    """Create bootstrap index for Claude Code."""
    workspace_key = str(WORKSPACE).replace("\\", "/").replace(":", "").replace("/", "-").lstrip("-")
    bootstrap_dir = Path.home() / ".claude" / "projects" / workspace_key / "memory"
    bootstrap_dir.mkdir(parents=True, exist_ok=True)
    bootstrap_file = bootstrap_dir / "MEMORY.md"
    content = f"""# Bootstrap — AI Workspace

## Step 1: Read shared memory

At the start of every new session, read:
`{WORKSPACE / "memory" / "MEMORY.md"}`

Then load specific memory files from the index as needed.

## Step 2: Read workspace rules

Read `{WORKSPACE / "ONBOARDING.md"}` once if you haven't this session.

## Hard rules (summary)
1. No brand-name files in the workspace
2. No runtime directories
3. shared_log.md append-only, memory/ grows never shrinks
4. Use workspace_lock.py before writing to memory/ or projects/
5. Append your brand keywords to rules/brand-names.txt on first join
"""
    bootstrap_file.write_text(content, encoding="utf-8")
    print(f"  ✓ Claude Code bootstrap created: {bootstrap_file}")


def step_write_log(agent_name: str):
    _log(f"agent '{agent_name}' onboarding complete")
    print(f"  ✓ shared_log.md updated")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print()
    print("╔══════════════════════════════════════╗")
    print("║   AI Workspace — First-time Setup    ║")
    print("╚══════════════════════════════════════╝")
    print()

    # Step 1: Agent identity
    print("── Step 1: Agent identity ──────────────")
    agent_name = _ask("Your agent name (e.g. claude-code, kimi, cursor-agent)")
    if not agent_name:
        print("[error] Agent name is required.")
        sys.exit(1)

    brand_input = _ask(
        f"Brand keywords to block (comma-separated, e.g. '{agent_name}')",
        default=agent_name
    )
    brand_keywords = [k.strip() for k in brand_input.split(",") if k.strip()]

    print()
    step_register_agent(agent_name, brand_keywords)

    # Step 2: Memory backup strategy
    print()
    print("── Step 2: Memory backup ───────────────")
    git_ok = shutil.which("git") is not None
    use_git = False
    if git_ok:
        use_git = _yn("git detected. Enable full version history for memory/?", default=True)
    else:
        print("  git not found — will use rolling snapshots (7-day retention).")

    if use_git:
        step_init_git()
    else:
        step_init_snapshots()

    # Step 3: Claude Code bootstrap (optional)
    print()
    print("── Step 3: Claude Code bootstrap ───────")
    if _yn("Create Claude Code bootstrap file? (skip if not using Claude Code)", default=False):
        step_claude_bootstrap()
    else:
        print("  skipped")

    # Step 4: Log
    print()
    step_write_log(agent_name)

    # Done
    print()
    print("╔══════════════════════════════════════╗")
    print("║   Setup complete!                    ║")
    print("╚══════════════════════════════════════╝")
    print()
    print("Next: tell your AI —")
    print('  "Read ONBOARDING.md and start working."')
    print()
    print("To start the real-time naming guard daemon:")
    print("  python workspace-watcher.py")
    print()


if __name__ == "__main__":
    main()
