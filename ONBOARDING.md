---
version: 2.0
---

# New Agent Onboarding

## 7 Rules (read this, nothing else required)

1. **This is the user's personal asset area, not an AI config directory.** Write your runtime data to your own directory (e.g. `~/.claude/`, `~/.kimi/`).
2. **No brand-name files.** Full list in `rules/brand-names.txt` — forbidden in any filename or directory name.
3. **On first join: append your brand keywords to `rules/brand-names.txt`.** One keyword per line, comments with `#`.
4. **No runtime directories.** `sessions/`, `cache/`, `backups/`, `telemetry/` etc. are forbidden.
5. **`shared_log.md` append-only. `memory/` grows, never shrinks.**
6. **Before creating any file: does it contain a brand name? Is it runtime data? → If yes to either, stop.**
7. **Before writing to `memory/`, call `workspace_lock.acquire(filepath, agent=your_agent_name)`. Release after writing.** Same for `projects/`. On conflict, check `.locks/conflict-pending.json`.

> Edge cases → `rules/workspace.md`
> Naming uncertain → `rules/naming.md`
> Multi-agent coordination → `rules/collaboration.md`

---

## Onboarding Steps

**Step 1: Read shared memory**

Open `memory/MEMORY.md` (index), load specific memory files as needed.

**Step 2: Create bootstrap index in your own config directory**

In your own config dir (not this workspace), create a bootstrap file containing:
- Startup instruction: read `memory/MEMORY.md` at the start of each new session
- Hard rules summary: the 7 rules above

**Step 3: Write onboarding log**

Append to `shared_log.md`:
```
[YYYY-MM-DD HH:MM] [your-agent-name] onboarding complete
```

---

## Workspace Structure

```
ai-workspace/
├── ONBOARDING.md           ← this file (entry point)
├── AGENTS.md               ← global behavior principles
├── shared_log.md           ← multi-AI shared log (append-only)
├── init.py                 ← first-time setup wizard
├── naming-guard.py         ← naming violation scanner
├── workspace-watcher.py    ← OS-level daemon, real-time violation detection
├── workspace_lock.py       ← write-lock module for concurrent access
├── memory_sync.py          ← memory sync + git auto-backup
├── rules/
│   ├── workspace.md        ← workspace boundary rules
│   ├── naming.md           ← naming conventions reference
│   ├── collaboration.md    ← multi-agent coordination protocol
│   └── brand-names.txt     ← brand keyword blocklist (agents append here)
├── memory/
│   ├── MEMORY.md           ← shared memory index
│   └── _example/           ← example memory file format
├── projects/               ← active project code
├── notes/                  ← user knowledge base
└── archive/                ← cold archive (AI does not auto-read)
```

---

## Common Mistakes

| Wrong | Right |
|-------|-------|
| Creating `CLAUDE.md`, `kimi-notes.md` | Use functional names: `AGENTS.md`, `research-notes.md` |
| Writing runtime logs here | Write to your own config directory |
| Writing memory content to your own dir | Write to `memory/` (shared) |
| Leaving files in root after task completion | Move to `notes/` or archive with project |
