# CARD-004: OpenCode Native Agent Setup

**Status**: ACTIVE  
**Created**: 2026-06-28  
**References**: CARD-001 (MCP tools), CARD-003 (AGENTS.md)

## Purpose

This card documents the native OpenCode configuration that replaces all bespoke orchestration code. Agent routing, model selection, and MCP integration are handled entirely through `.opencode/agents/*.md` files and `opencode.json`.

## What Was Removed

| File | Reason |
|------|--------|
| `orchestration/orchestrator.py` | Custom Python dispatch — replaced by OpenCode native agents |
| `orchestration/dispatch-rules.yaml` | Routing rules — replaced by per-agent model config |
| `orchestration/agent-cards/*.yaml` | Agent capability profiles — replaced by `.opencode/agents/*.md` |

## What Remains / Was Created

### Agent Cards (`.opencode/agents/*.md`)

Each agent is a single Markdown file with frontmatter specifying its model, mode, and permissions:

| File | Model | Mode | Purpose |
|------|-------|------|---------|
| `build.md` | ollama/qwen3.6:35b-256k | primary | Full dev agent — reads AGENTS.md prompt, writes code/tests/docs |
| `godot-dev.md` | ollama/qwen3-coder:30b-256k | subagent | Game code generation — GDScript/C#, scenes, node wiring |
| `spec-reviewer.md` | ollama/nemotron3:33b-256k | subagent | Spec compliance verification — read-only review of implementation vs specs |

Built-in agents also available:
- **plan** (primary) — restricted to analysis, no file edits
- **general**, **explore**, **scout** (subagents) — for research and codebase exploration

### Skills (`.opencode/skills/*/SKILL.md`)

Skills are loaded on-demand when their description matches a user request:

| Skill | Path | Purpose |
|-------|------|---------|
| `spec-review` | `.opencode/skills/spec-review/SKILL.md` | Review implementation against spec docs and research cards |
| `card-mgmt` | `.opencode/skills/card-mgmt/SKILL.md` | Manage research card system (catalogue updates, status changes) |

### opencode.json (project root)

Contains:
- `model`: ollama/qwen3.6:35b as default
- `mcp.godot-ai`: HTTP connection to Godot AI plugin at `http://127.0.0.1:8000/mcp`
- `instructions`: loads AGENTS.md + docs/cards/catalogue.md automatically

### Project Structure

```
godot-4-opencode-dev-test/          ← repo root = infrastructure/tooling
├── opencode.json                  ← MCP config (HTTP, port 8000)
├── .opencode/
│   ├── agents/*.md                ← agent model assignments (native OpenCode)
│   └── skills/*/SKILL.md          ← on-demand skill definitions
├── my-game/                       ← Godot 4.x project root (GDScript only)
│   ├── project.godot              ← created manually or via editor
│   ├── scenes/                    ← .tscn scene files
│   ├── scripts/                   ← .gd GDScript files
│   └── assets/                    ← textures, audio, fonts
├── docs/cards/                    ← research card system
└── ollama/model-files/            ← Ollama Modelfile configs
```

### Godot AI MCP Connection

The plugin runs inside the open Godot editor:
1. Open `my-game/` in Godot 4.x
2. Enable "Godot AI" plugin → Python server starts on port 8000
3. HTTP endpoint is always `http://127.0.0.1:8000/mcp`
4. OpenCode connects via MCP config (`type: "http"` in opencode.json)

### Agent Selection Flow

```
User request → OpenCode primary agent (build/plan via Tab or @mention)
  ↓
If task is game implementation → build invokes @godot-dev subagent with ollama/qwen3-coder:30b-256k
If task is spec verification → build invokes @spec-reviewer subagent with ollama/nemotron3:33b-256k
If skill needed (e.g. "update the card system") → loaded via skill tool automatically
```

## Key Design Decisions

1. **No custom dispatch code** — OpenCode's native agent + model assignment handles all routing
2. **One model per agent** — each `.md` file explicitly declares its Ollama model; no YAML routing rules needed
3. **Skills over commands for reusable workflows** — skills are discovered by the agent, commands require user typing
4. **AGENTS.md as instructions source** — loaded automatically via `prompt: "{file:./AGENTS.md}"` on every build session
5. **Godot project in subfolder** (`my-game/`) to prevent config conflicts between OpenCode and Godot tooling

## Related Cards

CARD-001: Godot AI MCP Plugin — provides the 120+ tools agents use for game development  
CARD-003: AGENTS.md Architecture — defines the instruction file hierarchy
