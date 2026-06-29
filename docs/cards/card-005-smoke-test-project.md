# CARD-005: Smoke Test Project — Splash Screen + System Info Collector

**Status**: DRAFTING  
**Created**: 2026-06-28  
**References**: CARD-001 (MCP tools), CARD-004 (agent setup)

## Purpose

A minimal Godot project that serves two purposes:
1. **Smoke test** — proves Godot, the godot_ai plugin, and OpenCode MCP integration all work end-to-end
2. **Baseline analysis** — generates a JSON file with Godot environment facts for AI agents to reference across sessions (no hallucinated env data)

## Requirements

### REQ-001: Splash Screen Scene (`res://scenes/splash.tscn`)

A minimal splash screen that loads instantly and auto-transitions after 2 seconds.

- **Scene structure:**
  - `Node` root (named "Splash")
    - `ColorRect` full viewport, solid color (#1a1a2e — dark blue-black)
      - `Label` centered text: "System Info Collector" in white, large font
      - `Label` below it showing Godot version string (populated at runtime)

- **Script:** `res://scripts/splash.gd` attached to root node
  - On `_ready()`: reads and displays Godot engine version via `DisplayServer.get_rendering_device().get_video_card_vendor()` or equivalent
  - After 2 seconds, auto-transitions to the system info scene via `get_tree().change_scene_to_file("res://scenes/system_info.tscn")`

### REQ-002: System Info Scene (`res://scenes/system_info.tscn`)

A single-screen scene that collects and displays Godot environment data.

- **Scene structure:**
  - `Node` root (named "SystemInfo")
    - `Control` root panel (full viewport)
      - `TextEdit` read-only, full size — displays the collected JSON output in real-time as it's generated
      - `Button` at bottom: "Regenerate" to re-collect data

- **Script:** `res://scripts/system_info_collector.gd` attached to root node
  - On `_ready()`: calls `collect_system_data()` which queries Godot APIs and writes JSON

### REQ-003: System Info Collector (`res://scripts/system_info_collector.gd`)

The core logic — collects Godot environment data into a structured JSON object.

**Data to collect:**

| Field | Source API | Purpose for AI Agents |
|-------|-----------|----------------------|
| `godot_version` | `Engine.get_version_info()` | Engine version agents target |
| `renderer_vendor` | `DisplayServer.get_rendering_device().get_video_card_vendor()` (if available) or fallback to `OS.get_video_adapter_vendor()` | GPU info for performance guidance |
| `renderer_name` | `OS.get_video_adapter_renderer()` | Specific renderer used |
| `os_name` | `OS.get_name()` | Target OS detection |
| `os_version` | `OS.get_unix_version()` or `OS.has_feature("windows")/("macos")` | OS version details |
| `screen_size` | `DisplayServer.screen_get_size()` | Default viewport dimensions |
| `available_display_modes` | `DisplayServer.get_screen_list()` + `DisplayServer.screen_get_usable_rect()` | Display capabilities |
| `cpu_cores` | `OS.get_processor_count()` | Performance baseline |
| `memory_total_mb` | `OS.get_static_memory_usage_mb()` or equivalent | Memory available for asset budgets |
| `project_path` | `"res://"` | Absolute project root path |
| `godot_ai_plugin_version` | Plugin's tool catalog (via `ToolCatalog.get_tool_list()` if plugin is loaded) | MCP capability baseline |

**Output:** JSON written to `my-game/.opencode/system-info.json` inside the Godot project.

### REQ-004: System Info JSON Output (`my-game/.opencode/system-info.json`)

The collector writes a well-formatted JSON file that AI agents can read on session start.

- File path: `res://.opencode/system-info.json` (inside the Godot project)
- Format: Pretty-printed JSON with sorted keys for deterministic diffs
- Content includes all fields from REQ-003 plus a `"collected_at"` ISO timestamp and `"godot_ai_plugin_version"` if available
- The file is gitignored via `.gitignore` addition (it's generated, not committed)

### REQ-005: Agent Reference Instructions

The root AGENTS.md must instruct agents to read `my-game/.opencode/system-info.json` on session start for environment context.

## Implementation Order

1. Create `res://scenes/splash.tscn` + `res://scripts/splash.gd`
2. Create `res://scenes/system_info.tscn` + `res://scripts/system_info_collector.gd`
3. Update `project.godot` to set splash as main scene
4. Write `.gitignore` additions for Godot-specific files (`.import/`, `*.remap`, etc.)

## Test Plan

- Open the project in Godot 4.x → splash screen appears within 1 second
- After 2 seconds, transitions to system info scene with JSON output visible
- Verify all fields from REQ-003 are populated correctly
- Close Godot → verify `system-info.json` exists and is valid JSON

## Status

DRAFTING (awaiting implementation)
