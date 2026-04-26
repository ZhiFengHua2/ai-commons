---
version: 1.0
---

# Naming Conventions

## Quick Card

**Core principle: name by function, not by tool.**

Brand keywords forbidden in any filename or directory name — see full list in `rules/brand-names.txt`.

**Three questions before creating a file:**
1. Does the name contain an AI brand or company name?
2. Is this runtime data or a config file?
3. If a new AI joins tomorrow, will this name still make sense to it?

→ If 1 or 2 is "yes", or 3 is "no" → use a generic functional name instead.

---

## Required Name Substitutions

| Purpose | ❌ Forbidden | ✅ Use instead |
|---------|-------------|---------------|
| AI behavior guide | `CLAUDE.md`, `KIMI.md` | `AGENTS.md`, `RULES.md` |
| Prompt templates | `claude-prompt.md`, `kimi-prompt.txt` | `PROMPT.md`, `PROMPT-[purpose].md` |
| Plugins / skills | `.claude-plugin/`, `.kimi-skills/` | `skills/`, `plugin-manifest/` |
| Memory files | `claude-memory.md`, `kimi-memory.json` | `MEMORY.md`, `memory-[topic].md` |
| Shared logs | `kimi-log.md`, `claude-log.txt` | `shared_log.md` |
| Task output | `gpt-output.md`, `claude-notes.md` | Functional: `research-notes.md`, `api-design.md` |

---

## Forbidden Directory Names

`sessions/` `session-env/` `file-history/` `telemetry/` `shell-snapshots/`
`downloads/` `cache/` `backups/` `plugins/` `ide/`

---

## Forbidden File Names

- AI auto-generated docs: `CHANGELOG.md`, `STARTUP.md`, `history.jsonl`
- Config / credential files: `settings.json`, `.credentials.json`, `.mcp.json`, `config.toml`
- Lock files: `*.lock` (unless project dependency lock files, e.g. `package-lock.json`)

---

## Violation Handling

1. Stop current operation
2. Rename the file/directory to a generic functional name
3. If runtime data, migrate to the AI's own config directory
4. Run `naming-guard.py` to verify clean state

**This convention also applies to directory references inside documents — do not suggest other AIs create brand-named directories.**
