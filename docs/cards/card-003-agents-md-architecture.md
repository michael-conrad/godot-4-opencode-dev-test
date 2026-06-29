# CARD-003: AGENTS.md Architecture — Agent Context Files

**Status**: ACTIVE  
**Created**: 2026-06-28  
**References**: CARD-001 (MCP tools), CARD-002 (spec process)

## Purpose

Agent context files (`AGENTS.md`) provide per-directory instructions that OpenCode automatically loads when working in those directories. This creates a hierarchy of agent knowledge without relying on fragile session memory.

### File Layout

```
godot-4-opencode-dev-test/
├── AGENTS.md                    ← Root: primary workflow, card catalogue entry point
├── docs/
│   ├── AGENTS.md                ← Docs layer: spec conventions, card writing rules
│   └── cards/
│       ├── catalogue.md         ← Card index (read first on every session)
│       ├── card-001-*.md        ← Research findings with cross-references
│       └── ...
├── orchestration/
│   ├── AGENTS.md                ← Orchestration layer: agent routing rules
│   └── ...                      ← Agent cards, dispatch rules, orchestrator code
└── .opencode/
    ├── package.json             ← OpenCode SDK bindings (no AGENTS.md needed)
    └── commands/                ← Custom opencode command definitions
```

### Each File's Responsibility

| Location | Responsibility | Loaded When Agent Works In... |
|----------|---------------|-------------------------------|
| Root `AGENTS.md` | Primary workflow entry, card catalogue index, MCP overview, dev rules | Any directory in this repo |
| `docs/AGENTS.md` | Spec conventions, card writing standards, when to create new cards | docs/specs/, docs/cards/, docs/systems/ |
| `orchestration/AGENTS.md` | Agent routing guidance, what each model does, scope boundaries | orchestration/* |

### Cross-Reference Pattern

Each AGENTS.md file must include a "Related" section pointing to other context files:

```markdown
## Related Context
- docs/cards/catalogue.md — active research cards index
- CARD-001 → docs/cards/card-001-godot-ai-mcp-plugin.md (MCP tooling)
- CARD-002 → docs/cards/card-002-spec-driven-interview-process.md (spec process)
```

### When to Update AGENTS.md Files

**Root `AGENTS.md`**: Only when the primary workflow changes or new card catalogue entries are added. This is the most important file — agents read it every session start.

**`docs/AGENTS.md`**: When spec conventions change, new documentation types are introduced, or card writing rules evolve.

**`orchestration/AGENTS.md`**: When agent routing rules change (new models, new dispatch targets).

### What NOT to Put in AGENTS.md

- Implementation details that change frequently
 - Code examples longer than a few lines
- Full MCP tool lists (reference CARD-001 instead)
- Project history or changelog entries

AGENTS.md files are **instructions**, not documentation. They tell the agent HOW to work, not WHAT exists.

## Related Cards

CARD-001: Godot AI MCP Plugin — provides the tooling that agents interact with via MCP  
CARD-002: Spec-driven interview process — defines what specs look like and how they're created
