# AI 工作区

> *一个共享文件夹，让你用的每一个 AI，终于站在同一起跑线上。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

[English](README.md)

<br>

你在 VS Code 里用 Claude Code，在浏览器里用 Kimi，偶尔切到 Cursor 改代码，有时候跑个 OpenHarness 自动化任务。

**但每次切换，上下文就断了。**

这个工作区模板给你用的所有 AI 一个共享记忆、共同规则和共用日志——让它们能接着彼此的进度继续干活。

---

## 工作原理

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

---

## 快速开始

```bash
git clone https://github.com/ZhiFengHua2/ai-commons.git
cd ai-commons
pip install watchdog plyer
python init.py
```

然后告诉你的 AI：`"读 ONBOARDING.md，开始工作。"`

---

## 包含哪些文件

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

---

## 兼容哪些 Agent

只要能读 markdown 文件的 AI，都能接入：

| Agent | 初始化方式 |
|-------|----------|
| Claude Code | Bootstrap 文件每次会话自动加载 `memory/MEMORY.md` |
| Cursor / VS Code Copilot | 把 ONBOARDING.md 内容粘贴为系统上下文 |
| Kimi / ChatGPT（网页版） | 会话开始时上传或粘贴 ONBOARDING.md |
| OpenHarness agents | `system_prompt = open("ONBOARDING.md").read() + 任务描述` |
| 其他任意 Agent | 同样的模式——先读 ONBOARDING.md |

---

## 解决什么问题

**问题**：每个 AI 工具把上下文锁在自己的孤岛里。切换工具或开新会话，一切归零，你不得不反复解释背景。

**这个方案做不到的**：多个 AI 同时运行时的实时同步（文件系统协调有固有延迟）。这是面向**人类主导**的多 AI 工作流，不是全自动化 Agent 流水线。

---

## 记忆格式

记忆文件是带 YAML frontmatter 的纯 markdown：

```markdown
---
name: 用户画像
description: 用户背景、目标和协作偏好
type: user
---

内容写这里...
```

人类可读，git 可 diff，不需要数据库。

模板见 `memory/_example/`。

---

## 工作区结构

```
ai-workspace/
├── memory/          ← 共享记忆（所有 AI 共读共写）
├── projects/        ← 活跃项目代码
├── notes/           ← 知识库、调研产物
├── rules/           ← 命名规范、协作协议
├── archive/         ← 已完成项目冷归档
└── .ai-index/       ← 多角色协作工件
```

---

## 参与贡献

想添加新 Agent 类型的支持，在 `docs/agent-adapters/` 里加一个示例，展示该 Agent 怎么加载 ONBOARDING.md 即可。

MIT License
