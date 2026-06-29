# CARD-006: Godot Plugin Enablement Notes

**Status**: DECIDED  
**Created**: 2026-06-28  
**References**: CARD-001 (MCP tools), CARD-004 (agent setup)

## What Happens When You Enable a Plugin in a Fresh Project

If `project.godot` already has the plugin listed under `[editor_plugins]`, Godot will:
- Load and activate it immediately on project open
- Show the **Godot AI dock** panel on the right side of the editor
- Start the MCP Python server automatically (port 8000)

If `project.godot` does NOT have the plugin yet, clicking Enable in Project Settings → Plugins will:
1. Add `[editor_plugins] enabled=PackedStringArray("res://addons/<plugin>/plugin.cfg")` to project.godot
2. Create `.godit/` directory with editor state files (uid_cache.bin, global_script_class_cache.cfg)
3. Start the plugin's autoload scripts

## Important: Pre-populated Config = No New Files

When `project.godot` is pre-populated with `[editor_plugins]`, opening the project in Godot and clicking Enable does **nothing new** — it was already enabled. The editor simply activates it without rewriting anything. This means:
- `.godit/` may or may not appear depending on whether the project was opened before plugin config was added
- `project.godot` won't change because it's already correct

## Plugin Activation Checklist

After opening `my-game/` in Godot 4.x:
- [ ] **Godot AI dock** visible on right side of editor
- [ ] Status dots show green/yellow/red for each configured MCP client (Claude Code, OpenCode, etc.)
- [ ] Click **Configure** next to your MCP client if not auto-configured
- [ ] Server URL should be `http://127.0.0.1:8000/mcp`
- [ ] Click **Tools** in the dock — see 120+ available tools listed

## Important Notes for Future Projects

When cloning or copying this repo to a new project:
1. The plugin is already configured in `project.godot` (editor_plugins + autoload sections)
2. You may need to re-enable it after opening in Godot if the editor doesn't auto-load it
3. `.godit/` and any import files should be gitignored (they're editor-generated cache)
