---
name: nmem-cli
description: The user's central memory system that persists across all agents and sessions. Use at session start to check working memory for context. Use when recalling past decisions, searching conversation history, saving insights worth remembering, or preserving this session. Also use when the user mentions memories, knowledge base, working memory, or past sessions.
---

# nmem — Persistent Memory CLI

You have `nmem` on your PATH. It is the user's central memory system — shared across all agents, editors, and sessions.

**Start every session** with `nmem wm` to read today's Working Memory (focus areas, flags, briefing).

Three areas — explore each with `--help`:

- `nmem m` — memories (search, add, show). Try: `nmem m search "your topic"`
- `nmem t` — threads (search past sessions, save this one). Try: `nmem t save --from Codex`
- `nmem wm` — working memory (daily focus surface — read, edit, history)

Add `--json` before any subcommand for machine-readable output.
