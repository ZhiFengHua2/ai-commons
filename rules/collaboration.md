---
version: 2.0
---

# Multi-Agent Collaboration Rules

---

## 1. Roles & Responsibilities

| Role | Responsibility | Output |
|------|---------------|--------|
| **PLAN** | Structure requirements, identify risks, define decision points | Plan doc → `.ai-index/plans/` |
| **AUDIT** | Review plan feasibility, break into executable steps | Execution manual → `.ai-index/manuals/` |
| **EXEC** | Execute manual steps, output decision cards | Execution summary → `.ai-index/executions/` |
| **REVIEW** | Audit execution against manual, fix or escalate | Audit report → `.ai-index/audits/` |

**Core principle**: The human is the only decision-maker. AI provides input, executes instructions, returns results.

---

## 2. Normal Flow

```
PLAN → human confirms → AUDIT → human confirms → EXEC → REVIEW → human confirms → done/next
```

**Exception escalation**: EXEC encounters uncovered edge case → stop, output decision card → human decides whether to escalate back to PLAN.
REVIEW finds plan/rule conflict → output divergence report → force escalation to PLAN.

---

## 3. Output Formats

### Plan Doc (PLAN output)
```
# Plan vX.Y - [goal]
## Background & Constraints / ## Core Assumptions / ## Scope (in/out)
## Risk Level (low/med/high) / ## Decision Points (table) / ## Deliverables
```

### Execution Manual (AUDIT output)
```
# Execution Manual vX.Y — Source: Plan vX.Y
## Pre-checks (verifiable conditions)
## Step N: description | command | expected result | rollback | human checkpoint
## Uncertainty statement / ## Completion criteria
```

### Execution Summary (EXEC output)
```
========== Decision Point: EXEC Complete ==========
[One-line summary] [Change log (table)] [Risk level] [Exceptions]
[Your options] 1.Let REVIEW audit 2.Escalate to PLAN 3.Continue 4.Rollback
===================================================
```

### Audit Report (REVIEW output)
```
# Fixed: issue found + fix + verification → status: can continue
# Divergence Report: core conflict + evidence + impact + options → force escalate to PLAN
```

---

## 4. Two-Window Mode (AUDIT + REVIEW sharing one AI account)

**Two independent windows, strict role separation — never mix roles in one window.**

### Startup
- Window B: read `.ai-index/role-audit.md`, paste as first message
- Window D: read `.ai-index/role-review.md`, paste as first message

### Shared Cache (both read, write by field only)
```
.ai-index/shared-cache/
├── manifest.json               ← AUDIT writes only audit field, REVIEW writes only review field
├── workspace-structure.json
└── current-project-context.md
```

### manifest.json Write Protocol
1. Read current file
2. Modify only your own field (`audit` or `review`)
3. Preserve the other agent's field unchanged
4. If the other field was modified during your write → stop, notify human

---

## 5. Exception Log

File: `.ai-index/exception-log.jsonl` (one entry per line, append-only)

```jsonl
{"time":"ISO8601","project":"xxx","version":"v1.0","stage":"EXEC","exception":"description","human_action":"rollback/reflow_to_plan/continue/skip","root_cause":"","pattern_tag":""}
```

**Log when**: human chooses "rollback" or "escalate to PLAN".

---

## 6. Human Quick Reference

| Situation | Reply |
|-----------|-------|
| Agree, continue with default | `1` or `continue` |
| Escalate for discussion | `2` or `escalate` |
| Know exactly what you're doing | `3` |
| Error, rollback | `4` or `rollback` |
