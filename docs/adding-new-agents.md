# Adding New Agents to the System

Step-by-step guide to onboard new LLM models.

## Prerequisites

1. Model must be available in Ollama
   ```bash
   ollama pull model-name
   ollama list  # Verify it shows up
   ```

2. You know the model's characteristics:
   - Context window size
   - Typical use cases
   - Strengths and weaknesses
   - Recommended temperature/sampling

## Step 1: Create Agent Card

Create `orchestration/agent-cards/YOUR-AGENT.yaml`:

```yaml
name: "Model Name:XB"  # Human-readable name
model: "ollama/model-name"  # Exact Ollama model ID
role: "One-line description of primary role"
context_window: 262144  # Tokens
parameters:
  temperature: 0.7  # Typical temperature
  top_p: 0.9
  repeat_penalty: 1.1

strengths:
  - "What it's exceptionally good at"
  - "Another strength"
  - "And another"

capabilities:
  can_generate_code: true  # true/false
  can_reason: true
  can_follow_instructions: true
  can_verify: false
  can_optimize: false

weaknesses:
  - "Known limitation 1"
  - "Known limitation 2"

best_for:
  - "Primary use case 1"
  - "Primary use case 2"
  - "Secondary use case"

worst_for:
  - "Avoid using for this"
  - "And this"

dispatch_criteria:
  - "When to route this agent"
  - "Another routing condition"

fallback_chain:
  - "fallback-agent-1"  # If this agent unavailable
  - "fallback-agent-2"
  - null  # Hard failure if all unavailable
```

## Step 2: Add Dispatch Rules

Edit `orchestration/dispatch-rules.yaml`:

### Option A: Keyword-Based Routing

```yaml
keyword_routing:
  - keywords: ["your", "keywords"]
    primary: "your-agent-id"
```

### Option B: Complex Rule

```yaml
dispatch_rules:
  - id: "your_rule_id"
    condition: "task_type == 'your_type' AND some_condition == true"
    primary: "your-agent-id"
    fallback: "fallback-agent"
    reason: "Why this agent is chosen for this condition"
```

### Option C: Update Fallback Chain

```yaml
fallback_chain:
  - "new-agent"
  - "existing-agent"
  - "another-agent"
```

## Step 3: Test

### Manual Test

```bash
# List agents to verify it loaded
python3 orchestration/orchestrator.py --list-agents | grep your-agent

# Test explicit agent selection
python3 orchestration/orchestrator.py --task "test task" --agent your-agent

# Test keyword routing
python3 orchestration/orchestrator.py --task "your keyword here: test" --verbose
```

### Verification

1. Agent appears in `--list-agents` output
2. Can be explicitly selected with `--agent your-agent`
3. Appropriate keywords trigger auto-selection
4. Fallback chain works if agent unavailable

## Step 4: Document

Add entry to relevant documentation:

1. **README.md** - Add to models list
2. **agent-system-architecture.md** - Update agent comparison table
3. **dispatch-strategy.md** - Add dispatch examples if unique

## Examples

### Example 1: Adding a Lightweight Specialist

Suppose you add a model optimized for mobile deployment:

```yaml
# orchestration/agent-cards/mobile-lite.yaml
name: "MobileLite:8B"
model: "ollama/mobilelite:8b"
role: "Ultra-lightweight inference"
context_window: 8192

strengths:
  - "Extremely fast (8B)"
  - "Minimal memory footprint"
  - "Good for edge deployment"

capabilities:
  can_generate_code: true
  can_reason: false
  can_follow_instructions: true

weaknesses:
  - "Very limited context (8K)"
  - "Can't handle complex reasoning"

best_for:
  - "Mobile/edge deployment"
  - "Ultra-fast responses to simple queries"

worst_for:
  - "Complex reasoning"
  - "Long contexts"
  - "Code review"

dispatch_criteria:
  - "Task marked 'mobile-optimized'"
  - "Context size < 8K"

fallback_chain:
  - "mistral-small3"
  - "nemotron3"
```

```yaml
# In dispatch-rules.yaml
keyword_routing:
  - keywords: ["mobile", "edge", "lightweight"]
    primary: "mobile-lite"
```

### Example 2: Adding a Specialized Domain Expert

Suppose you add a model trained for Godot scripting:

```yaml
# orchestration/agent-cards/godot-specialist.yaml
name: "GodotMaster:32B"
model: "ollama/godot-specialist:32b"
role: "Godot 4 scripting specialist"
context_window: 262144

strengths:
  - "Godot 4 API mastery"
  - "GDScript + C# proficiency"
  - "Game architecture patterns"
  - "Best practices for Godot"

capabilities:
  can_generate_code: true
  can_reason: true
  can_follow_instructions: true
  can_review: true
  can_optimize: true

best_for:
  - "GDScript implementation"
  - "C# for Godot projects"
  - "Godot-specific architecture"
  - "Godot API questions"

worst_for:
  - "Non-Godot tasks"
  - "General game design"

dispatch_criteria:
  - "Task mentions 'Godot'"
  - "Task mentions 'GDScript' or 'gdscript'"
  - "Task mentions 'C# for Godot'"

fallback_chain:
  - "qwen3-coder"
  - "qwen3.6"
```

```yaml
# In dispatch-rules.yaml
keyword_routing:
  - keywords: ["godot", "gdscript", "gd-script"]
    primary: "godot-specialist"
```

## Troubleshooting

### Agent doesn't appear in list
- Check YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('file.yaml'))"`
- Ensure file is in `orchestration/agent-cards/`
- Verify no filename starts with `.`

### Dispatch doesn't select new agent
- Check keyword routing: keywords must match task (case-insensitive)
- Verify dispatch rules loaded: check logs with `--verbose`
- Force agent selection to verify it works: `--agent agent-id`

### Model not found in Ollama
- Verify model is loaded: `ollama list`
- Pull if needed: `ollama pull model-name`
- Restart Ollama if recently pulled

### Fallback chain not working
- Verify fallback agent IDs exist
- Check YAML syntax
- Review logs for error messages

## Performance Tuning

After adding an agent, monitor its performance:

1. **Accuracy**: Does it produce correct results for its intended use case?
2. **Speed**: Is it faster/slower than expected?
3. **Reliability**: Does it fail gracefully when confused?
4. **Context efficiency**: Does it stay within its context window?

Adjust dispatch rules if needed to optimize task distribution.
