# CARD-001: Godot AI MCP Plugin (dlight) — Primary MCP Server

**Status**: RESEARCHING → DECIDED as primary candidate  
**Created**: 2026-06-28  
**References**: CARD-003 (AGENTS.md architecture), CARD-002 (spec process)

## Overview

The Godot AI plugin by dlight (hi-godot/godot-ai) is the leading MCP server for Godot 4. It connects MCP-compatible AI assistants to a live Godot editor, providing 120+ tools spanning scenes, nodes, scripts, animations, UI, themes, materials, particles, input mapping, and project settings.

## Key Details

- **Source**: https://github.com/hi-godot/godot-ai
- **Asset Store**: https://store.godotengine.org/asset/dlight/godot-ai/
- **License**: MIT
- **Min Godot Version**: 4.3 (4.4+ recommended)
- **Latest**: v2.7.4

## Capabilities

1. **Scene Inspection & Construction** — Build entire UI hierarchies from prompts, inspect node trees
2. **Script Editing** — Attach GDScript/C# scripts, inline parse diagnostics on every write
3. **AnimationAuthoring** — AnimationPlayer with fade/slide/shake/pulse presets
4. **Materials** — StandardMaterial3D, ORMMaterial3D, ShaderMaterial creation/editing
5. **Particles** — GPU + CPU, 2D/3D, seven built-in presets (fire, smoke, spark_burst, magic, rain, explosion, lightning)
6. **Smart Screenshots** — AI agents can see the live scene via screenshot tools
7. **Camera Control** — Camera2D/3D configuration, follow, damping, limits
8. **Audio** — AudioStreamPlayer 2D/3D setup
9. **Resources** — Inline or .tres files for meshes, shapes, curves, gradients, styleboxes
10. **Multi-Instance Support** — Works across multiple Godot editor instances

## MCP Client Compatibility (18 clients)

Claude Code, Codex, Antigravity, Cursor, Windsurf, VS Code, Zed, Gemini CLI, Cline, Kilo Code, Roo Code, Kiro, Trae, Cherry Studio, **OpenCode**, Qwen Code, and more.

## Installation

```
1. Install uv (if not present)
2. Download addon from Asset Library or drop into addons/godot_ai/
3. In Godot: Project → Project Settings → Plugins — enable "Godot AI"
4. Open Godot AI dock, click your MCP client to configure in one click
5. Open your MCP client and start prompting
```

## Why This Over Alternatives

| Factor | dlight/godot-ai | Fennara AI | Ziva | Hera Agent | Funplay MCP |
|--------|-----------------|------------|------|------------|-------------|
| Tools count | 120+ | unknown | unknown | "MCP-grade" | editor-only |
| OpenCode native | Yes (listed) | unknown | Proprietary | MIT CLI | Cursor/VS Code focused |
| Source available | GitHub (MIT) | MIT | Proprietary | MIT | MIT |
| Stars/maturity | 9500+ lineage from MCP for Unity | Newer | 5 reviews | 0 reviews | 2 reviews |
| Live editor bridge | Full | partial | full | CLI-based | editor-only |

**Verdict**: dlight/godot-ai is the strongest candidate — most mature, widest tool coverage, native OpenCode support via its 18-client list, MIT licensed, and from the proven MCP for Unity team.

## Implementation Notes for This Repo

When setting up this repo:
1. Install Godot AI as `addons/godot_ai/` in the Godot project
2. Configure it to connect to OpenCode's MCP stream (stdio or SSE)
3. Use smart screenshots during dev cycle: agent modifies scene → takes screenshot → verifies visually
4. Inline GDScript diagnostics give immediate feedback on syntax errors before running
5. The 120+ tools cover the full spec-to-implementation loop we need

## Related Cards

- CARD-002: Spec-driven interview process (how MCP tools feed into spec verification)
- CARD-003: AGENTS.md architecture (where OpenCode + MCP integrate with agent workflow)
