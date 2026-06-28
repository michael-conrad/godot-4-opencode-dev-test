# Dispatch Task to Multi-Agent System

Route a task to the appropriate specialized agent.

## Usage

```bash
opencode --command "dispatch-task" --args "Your task description"
```

## Examples

### Code Generation
```
Write a GDScript script for player movement with WASD controls and diagonal movement support
```

### Game Design
```
Design the combat system for a top-down Godot game with classes: Warrior, Ranger, Mage
```

### Code Review
```
Review this GDScript code for performance issues and suggest optimizations: [code snippet]
```

### Quick Prototype
```
Quickly prototype a pause menu UI for Godot 4
```

## Agent Selection

The system automatically selects the best agent based on your task keywords:

- **"write", "implement", "code", "script"** → Qwen 3-Coder (specialized code generation)
- **"design", "spec", "architecture"** → Qwen 3.6 Orchestrator (planning/design)
- **"review", "verify", "check", "validate"** → Nemotron 3 (verification)
- **"quick", "fast", "rapid", "prototype"** → Devstral Small (speed)
- **"plan", "decompose", "organize"** → Qwen 3.6 Orchestrator (coordination)
- **"debug", "fix", "bug", "error"** → Qwen 3-Coder (debugging)

## Force Specific Agent

```bash
python3 orchestration/orchestrator.py --task "your task" --agent qwen3-coder
```

Available agents:
- `qwen3.6-orchestrator` - Main orchestrator
- `qwen3-coder` - Code specialist
- `devstral-small` - Fast prototyping
- `nemotron3` - Balanced verification
- `laguna-xs` - Lightweight
- `gpt-oss` - General purpose
- `gemma4` - Instruction follower
- `mistral-small3` - Ultra-fast
- `granite4.1` - Code-focused
- `qwen3.5` - General purpose
- `nemotron-cascade` - Multi-step reasoning
