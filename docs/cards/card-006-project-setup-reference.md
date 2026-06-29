# CARD-006: Project Setup Reference Card

**Status**: ACTIVE  
**Created**: 2026-06-28  
**References**: CARD-001 (MCP tools), CARD-004 (agent setup)

## Purpose

Quick reference for setting up a new Godot project with this tooling stack. Copy-paste these steps when cloning or creating a fresh project.

## Setup Steps

### 1. Clone the repo
```bash
git clone <repo-url> && cd my-game
```

### 2. Install godot_ai addon (if not already present)
```bash
# From GitHub:
mkdir -p addons && git clone --depth 1 https://github.com/hi-godot/godot-ai.git _tmp
cp -r _tmp/plugin/addons/godot_ai ./addons/ && rm -rf _tmp

# Or from Godot Asset Store (AssetLib tab → search "Godot AI" → Download)
```

### 3. Enable the plugin in Godot Editor
1. Open `my-game/` in Godot 4.x
2. **Project → Project Settings → Plugins**
3. Find **"Godot AI"** and click **Enable**
4. The MCP dock appears on the right — shows status dots for each configured client
5. Close the editor (plugin state persists)

### 4. Verify plugin is active
After closing the editor, check:
- `project.godot` has `[editor_plugins] enabled=PackedStringArray("res://addons/godot_ai/plugin.cfg")`
- `.godit/` directory exists with `global_script_class_cache.cfg` and `uid_cache.bin`

### 5. Configure MCP client (one-time per client)
In the Godot AI dock, click **Configure** next to your client:
- **OpenCode**: Auto-configures if found in PATH
- **Claude Code**: Writes Claude Desktop config automatically  
- Manual: Server URL is always `http://127.0.0.1:8000/mcp`

### 6. Verify MCP connection
In the dock, click **Tools** — you should see all 120+ available tools with green status dots.

## Files Created by Godot (do NOT commit to git)

| Path | Purpose | Ignore? |
|------|---------|---------|
| `.godit/` | Editor layout, cache files | Yes — add to .gitignore |
| `*.remap` | Imported resource remaps | Yes |
| `*.import/` | Import pipeline temp files | Yes |

## Common Issues

- **Plugin won't enable**: Disable → Apply → Enable again in Project Settings
- **MCP dock not visible**: Ensure plugin is enabled AND project has been opened at least once after enabling
- **Port conflict**: Godot AI uses port 8000 by default. Change in dock if occupied
