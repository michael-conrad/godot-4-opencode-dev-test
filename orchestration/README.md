# Orchestration System

Multi-agent dispatch engine for Godot game development tasks.

## Components

### Agent Cards (`agent-cards/`)

Each agent has a capability profile (YAML) describing:
- **Strengths**: What it excels at
- **Weaknesses**: Limitations and performance characteristics
- **Best for**: Primary use cases
- **Worst for**: Avoid these tasks
- **Dispatch criteria**: When the orchestrator should select this agent

### Dispatch Rules (`dispatch-rules.yaml`)

Decision tree for routing tasks to agents:
- Deterministic routing (task keywords/type)
- Fallback chains (if primary agent unavailable)
- Uncertainty handling (fallback to balanced agent)

### Orchestrator (`orchestrator.py`)

Main dispatch engine:
1. Loads agent cards
2. Parses incoming task
3. Matches against dispatch rules
4. Sends to selected agent(s) via Ollama
5. Validates + returns results

### Ollama Client (`ollama-client.py`)

HTTP client wrapper for Ollama REST API:
- Chat completion calls
- Embedding generation (utility)
- Model listing
- Error handling + retries

## Workflow

```
User Input (OpenCode)
  ↓
Orchestrator reads task
  ↓
Match dispatch rules
  ↓
Select agent(s)
  ↓
Ollama API call
  ↓
Agent processes
  ↓
(optionally: call embedding service for semantic ops)
  ↓
Return result
```

## Running

```bash
# Single task
python3 orchestration/orchestrator.py --task "write a GDScript player movement script"

# Interactive mode
python3 orchestration/orchestrator.py --interactive

# Specify agent explicitly
python3 orchestration/orchestrator.py --task "..." --agent qwen3-coder

# Verbose logging
python3 orchestration/orchestrator.py --task "..." --verbose
```

## Agent Selection Examples

| Task | Primary | Fallback |
|------|---------|----------|
| "Write GDScript for player movement" | qwen3-coder | devstral-small |
| "Design the combat system" | qwen3.6-orchestrator | nemotron3 |
| "Verify code quality" | nemotron3 | qwen3.6-orchestrator |
| "Quick prototype UI screen" | devstral-small | qwen3-coder |
| "Uncertain task" | nemotron3 | qwen3.6-orchestrator |
