# AI Workspace

> *One shared folder. Every AI you use, finally on the same page.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

[中文文档](README_CN.md)

<br>

You use Claude Code in VS Code. Kimi in the browser. Cursor for a quick edit. Maybe an OpenHarness agent for automation.

**They all forget everything the moment you switch.**

This workspace template gives every AI you use a shared memory, shared rules, and a shared log — so they can pick up where each other left off.

---

## How it works

```
You open this folder in VS Code / Cursor / any IDE
         ↓
python init.py          ← runs once, sets everything up
         ↓
Tell your AI: "Read ONBOARDING.md"
         ↓
AI initializes itself: registers its brand, sets up its bootstrap
         ↓
All your AIs now share memory/, follow the same rules, write to the same log
```

**It's not a server. It's not a cloud service. It's a folder.**

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ai-workspace
cd ai-workspace
pip install watchdog plyer
python init.py
```

Then tell your AI: `"Read ONBOARDING.md and start working."`

---

## What's included

| File | Purpose |
|------|---------|
| `ONBOARDING.md` | Protocol every AI reads to initialize itself |
| `init.py` | First-time setup wizard |
| `naming-guard.py` | Scans for brand-name violations |
| `workspace-watcher.py` | Real-time daemon, OS notification on violations |
| `workspace_lock.py` | Write-lock module, prevents concurrent overwrites |
| `memory_sync.py` | Memory backup (git default, snapshots fallback) |
| `rules/` | Naming conventions, workspace boundaries, multi-agent protocol |
| `memory/` | Shared memory — all AIs read and write here |

---

## Compatible agents

Works with any AI that can read a markdown file:

| Agent | How it initializes |
|-------|--------------------|
| Claude Code | Bootstrap file auto-loads `memory/MEMORY.md` each session |
| Cursor / VS Code Copilot | Paste ONBOARDING.md content as system context |
| Kimi / ChatGPT (web) | Upload or paste ONBOARDING.md at session start |
| OpenHarness agents | `system_prompt = open("ONBOARDING.md").read() + your_task` |
| Any other agent | Same pattern — read ONBOARDING.md first |

---

## What it solves

**The problem**: Every AI tool stores context in its own silo. When you switch tools — or start a new session — everything resets. You repeat yourself constantly.

**What this doesn't solve**: Real-time synchronization between agents running simultaneously (file-based coordination has inherent latency). This is a workspace for human-orchestrated multi-AI workflows, not programmatic agent pipelines.

---

## Memory format

Memories are plain markdown files with YAML frontmatter:

```markdown
---
name: user profile
description: user's background, goals, collaboration style
type: user
---

Content here...
```

Human-readable. Git-diffable. No database required.

See `memory/_example/` for templates.

---

## Workspace structure

```
ai-workspace/
├── memory/          ← shared memory (all AIs read/write)
├── projects/        ← your active project code
├── notes/           ← knowledge base, research output
├── rules/           ← naming conventions, collaboration protocol
├── archive/         ← completed projects, cold storage
└── .ai-index/       ← multi-role collaboration artifacts
```

---

## Contributing

To add support for a new agent type, add an example to `docs/agent-adapters/` showing how that agent loads ONBOARDING.md.

MIT License
