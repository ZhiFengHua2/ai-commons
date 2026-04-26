# Global Agent Behavior

This file applies to all agents across all projects as soft guidance (not hard constraints).

## Code Production Principles

- Search for existing implementations before writing new code — prefer reuse
- Explain reasons before introducing new dependencies, wait for confirmation
- Test files go in `tests/`, named to match source files
- Python: use `typing` annotations. Rust: explicit trait bounds. No ambiguous types.

## Knowledge Internalization Reminder

When a single response contains large amounts of new information (more than 3 major concepts, or systematic knowledge output), proactively ask the user at the end whether they have internalized the key points, and suggest triggering a knowledge internalization check.

---

## Cache & Collaboration Rules (Three-Layer Architecture)

### 1. Global Layer — `memory/`
- **Content**: User profile, career path, collaboration preferences — finalized memories.
- **Usage (by agent type)**:
  - Agents with bootstrap support: read `memory/MEMORY.md` index, load specific `memory/*.md` files as needed.
  - Agents without bootstrap: read `memory/_prebaked/injection.md` for full-context injection.
- **Update frequency**: `injection.md` should be regenerated after substantive changes to `memory/`.

### 2. Project Layer — `projects/current/`
- **Content**: Source code, raw papers, dataset descriptions, original documents.
- **Usage**: Agents read original files directly. Do not read another agent's secondary summaries.
- **Rule**: Original files are retained when projects are archived — never deleted by cache cleanup.

### 3. Session Layer — `.ai-cache/sessions/slot-[a|b|c]/`
- **Content**: Per-session agent notes, temporary downloads, intermediate outputs.
- **Usage**: Each slot serves one session flow at a time. Agents exclusively read/write their own slot.
- **Cleanup**: Clear only the relevant slot when archiving a project.

### Slot Usage

| Slot | Purpose | Concurrency |
|------|---------|-------------|
| `slot-a` | Current `projects/current/` code execution | Can open slot-b for planning |
| `slot-b` | Planning/discussing next project | Can open slot-c for emergencies |
| `slot-c` | Emergency exploration or temp research | Keep empty when possible |

### Required Header for Session Notes

Any `.md` file written to a session slot must include:

```yaml
---
source: "original file path"
accessed: "YYYY-MM-DD"
type: "digest"
disclaimer: "This is a summary. Verify against original: [path]"
---
```

### Prohibited
- Agents must not read files in another agent's session slot.
- Session-layer summaries must not replace reading original project-layer files.
- Session-specific content must not be written into the global prebaked package.
