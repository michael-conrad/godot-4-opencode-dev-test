# Orchestration System

Multi-agent dispatch engine for Godot game development tasks.

## Quick Start

```bash
# List all agents
uv run orchestration/orchestrator.py --list-agents

# Dispatch a task
uv run orchestration/orchestrator.py --task "your task here"

# Interactive mode
uv run orchestration/orchestrator.py --interactive

# Verbose logging
uv run orchestration/orchestrator.py --task "..." --verbose
```

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

### Ollama Client (`ollama_client.py`)

HTTP client wrapper for Ollama REST API:
- Chat completion calls
- Embedding generation (utility)
- Model listing
- Error handling + retries
- Ollama is a system service on `http://localhost:11434`

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

## Agent Selection Examples

| Task | Primary | Fallback |
|------|---------|----------|
| "Write GDScript for player movement" | qwen3-coder | devstral-small |
| "Design the combat system" | qwen3.6-orchestrator | nemotron3 |
| "Verify code quality" | nemotron3 | qwen3.6-orchestrator |
| "Quick prototype UI screen" | devstral-small | qwen3-coder |
| "Uncertain task" | nemotron3 | qwen3.6-orchestrator |

## Running with uv

All scripts use PEP 723 headers and are run via `uv`:

```bash
# Direct invocation (uv finds the PEP 723 script header)
uv run orchestration/orchestrator.py [args]

# Or explicitly with Python
uv run python orchestration/orchestrator.py [args]
```

## Environment

Python 3.10+

Dependencies defined in `pyproject.toml`:
- `requests>=2.31.0` - HTTP client
- `pyyaml>=6.0` - YAML parsing

Development dependencies:
- `pytest>=7.4.0` - Testing
- `black>=23.7.0` - Code formatting
- `ruff>=0.0.287` - Linting
- `mypy>=1.4.1` - Type checking

## See Also

- [Agent System Architecture](../docs/agent-system-architecture.md) - Detailed design
- [Dispatch Strategy](../docs/dispatch-strategy.md) - Routing logic with examples
- [Adding New Agents](../docs/adding-new-agents.md) - Onboarding guide
