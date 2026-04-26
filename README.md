# AI Workspace · AI 工作区

[English](#english) | [中文](#中文)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

---

## English

> *One shared folder. Every AI you use, finally on the same page.*

You use Claude Code in VS Code. Kimi in the browser. Cursor for a quick edit. Maybe an OpenHarness agent for automation.

**They all forget everything the moment you switch.**

This workspace template gives every AI you use a shared memory, shared rules, and a shared log — so they can pick up where each other left off.

### How it works

```
Open this folder in VS Code / Cursor / any IDE
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

### Quick Start

```bash
git clone https://github.com/ZhiFengHua2/ai-commons.git
cd ai-commons
pip install watchdog plyer
python init.py
```

Then tell your AI: `"Read ONBOARDING.md and start working."`

### What's included

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

### Compatible agents

| Agent | How it initializes |
|-------|--------------------|
| Claude Code | Bootstrap file auto-loads `memory/MEMORY.md` each session |
| Cursor / VS Code Copilot | Paste ONBOARDING.md content as system context |
| Kimi / ChatGPT (web) | Upload or paste ONBOARDING.md at session start |
| OpenHarness agents | `system_prompt = open("ONBOARDING.md").read() + your_task` |
| Any other agent | Same pattern — read ONBOARDING.md first |

### What it solves

**The problem**: Every AI tool stores context in its own silo. When you switch tools — or start a new session — everything resets. You repeat yourself constantly.

**What this doesn't solve**: Real-time synchronization between agents running simultaneously. This is a workspace for human-orchestrated multi-AI workflows, not programmatic agent pipelines.

### Memory format

```markdown
---
name: user profile
description: user's background, goals, collaboration style
type: user
---

Content here...
```

Human-readable. Git-diffable. No database required. See `memory/_example/` for templates.

---

## 中文

> *一个共享文件夹，让你用的每一个 AI，终于站在同一起跑线上。*

你在 VS Code 里用 Claude Code，在浏览器里用 Kimi，偶尔切到 Cursor 改代码，有时候跑个 OpenHarness 自动化任务。

**但每次切换，上下文就断了。**

这个工作区模板给你用的所有 AI 一个共享记忆、共同规则和共用日志——让它们能接着彼此的进度继续干活。

### 工作原理

```
用 VS Code / Cursor / 任意 IDE 打开这个文件夹
                ↓
python init.py          ← 只跑一次，完成所有初始化
                ↓
告诉你的 AI："读 ONBOARDING.md"
                ↓
AI 自我初始化：注册品牌词、建立 bootstrap、写入接入日志
                ↓
你的所有 AI 现在共享 memory/、遵守同一套规则、写同一份日志
```

**不是服务器，不是云服务，就是一个文件夹。**

### 快速开始

```bash
git clone https://github.com/ZhiFengHua2/ai-commons.git
cd ai-commons
pip install watchdog plyer
python init.py
```

然后告诉你的 AI：`"读 ONBOARDING.md，开始工作。"`

### 包含哪些文件

| 文件 | 用途 |
|------|------|
| `ONBOARDING.md` | 每个 AI 读这个完成自我初始化 |
| `init.py` | 首次使用配置向导 |
| `naming-guard.py` | 扫描品牌名违规 |
| `workspace-watcher.py` | 实时守护进程，违规立即 OS 通知 |
| `workspace_lock.py` | 写入锁模块，防止多 AI 并发覆写 |
| `memory_sync.py` | 记忆备份（优先 git，无 git 时滚动快照） |
| `rules/` | 命名规范、工作区边界、多 Agent 协作协议 |
| `memory/` | 共享记忆库，所有 AI 共读共写 |

### 兼容哪些 Agent

| Agent | 初始化方式 |
|-------|----------|
| Claude Code | Bootstrap 文件每次会话自动加载 `memory/MEMORY.md` |
| Cursor / VS Code Copilot | 把 ONBOARDING.md 内容粘贴为系统上下文 |
| Kimi / ChatGPT（网页版） | 会话开始时上传或粘贴 ONBOARDING.md |
| OpenHarness agents | `system_prompt = open("ONBOARDING.md").read() + 任务描述` |
| 其他任意 Agent | 同样的模式——先读 ONBOARDING.md |

### 解决什么问题

**问题**：每个 AI 工具把上下文锁在自己的孤岛里。切换工具或开新会话，一切归零，你不得不反复解释背景。

**这个方案做不到的**：多个 AI 同时运行时的实时同步（文件系统协调有固有延迟）。这是面向**人类主导**的多 AI 工作流，不是全自动化 Agent 流水线。

### 记忆格式

```markdown
---
name: 用户画像
description: 用户背景、目标和协作偏好
type: user
---

内容写这里...
```

人类可读，git 可 diff，不需要数据库。模板见 `memory/_example/`。

---

MIT License
