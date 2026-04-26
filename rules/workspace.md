---
version: 1.0
---

# Workspace Rules

## Quick Card (read on every join, ~1 minute)

1. **This is the user's personal asset area, not any AI's config directory.**
2. Your runtime data (logs, sessions, cache, credentials) must go in your own directory.
3. No AI brand names in filenames or directory names. → See `rules/naming.md`
4. No runtime directories (full list in `rules/naming.md`).
5. `shared_log.md` append-only. `memory/` grows, never shrinks (ask user before modifying core structure).

**Before creating any file: brand name? runtime data? → If yes to either, stop.**

---

## What the Workspace Contains

```
ai-workspace/
├── rules/           ← rule documents (this directory)
├── memory/          ← shared memory (multi-AI co-created)
├── projects/        ← active project code (git repos)
├── notes/           ← user knowledge base
├── archive/         ← completed project cold storage (AI does not auto-read)
├── .ai-index/       ← multi-role collaboration artifacts
├── ONBOARDING.md    ← new agent entry point
├── AGENTS.md        ← global behavior principles
└── shared_log.md    ← multi-AI shared log (append-only)
```

**Does not belong here:** AI config directories, lock files, IDE extensions, settings.json, credentials.

---

## Read/Write Permissions

| Path | Read | Write | Constraint |
|------|------|-------|-----------|
| `projects/` | ✅ | ✅ | Prompt user to git commit after changes |
| `memory/` | ✅ | ✅ append | Ask user before modifying `MEMORY.md` core structure |
| `notes/` | ✅ | ✅ | Move new files here after task, don't pile in root |
| `shared_log.md` | ✅ | ✅ append | Append only. Format: `[YYYY-MM-DD HH:MM] [agent] description` |
| `archive/` | ✅ | archive only | Do not modify after archiving |
| Root rule docs | ✅ | ❌ | Modifying rule docs requires user confirmation |

---

## Concurrent Conflict Handling

- `projects/`: git repos, use commits as coordination unit for multi-AI edits.
- `memory/*.md`: use `workspace_lock.py` before writing. LOW risk = auto-retry after TTL. MED risk = pause + notify user.
- `shared_log.md`: append-only, no conflict risk.

---

## Three-Layer Naming Protection

**Layer 1 (Awareness)**: This file and `rules/naming.md` state explicit prohibitions.
**Layer 2 (Auto-detection)**: `naming-guard.py` scans for violations. Run periodically or when violations are suspected.
**Layer 3 (Continuous)**: `workspace-watcher.py` daemon detects violations in real time and notifies the OS.

---

## Document Growth Protocol

| Situation | Required action |
|-----------|----------------|
| Any `rules/` file > 200 lines | Split: keep `<name>.md` as quick card (≤80 lines), move details to `<name>-ref.md` |
| `ONBOARDING.md` > 80 lines | Compress, push details down to `rules/` files |
| `memory/MEMORY.md` > 200 lines | Merge related entries, keep index lean |
| `notes/` > 20 files | Create topic subdirectories |

**Archive trigger**: When a project completes and user confirms → move `projects/<name>/` + `.ai-index/` artifacts → `archive/YYYY-MM/<name>/`.
