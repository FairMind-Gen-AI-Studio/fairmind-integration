# LLM Optimization Reference

## Model Selection

### Model Tiers

```
┌─────────────────────────────────────────────────────────┐
│                    Model Selection Guide                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Complexity ▲                                           │
│             │  ┌─────────────────────────────────┐      │
│    High     │  │  Claude Opus / GPT-4           │      │
│             │  │  Complex reasoning, analysis    │      │
│             │  └─────────────────────────────────┘      │
│             │  ┌─────────────────────────────────┐      │
│    Medium   │  │  Claude Sonnet / GPT-4-mini    │      │
│             │  │  Code, structured output        │      │
│             │  └─────────────────────────────────┘      │
│             │  ┌─────────────────────────────────┐      │
│    Low      │  │  Claude Haiku / GPT-3.5        │      │
│             │  │  Classification, extraction     │      │
│             │  └─────────────────────────────────┘      │
│             └────────────────────────────────────► Cost │
└─────────────────────────────────────────────────────────┘
```

### Task-Based Selection

```python
MODEL_ROUTING = {
    # High complexity - use best model
    "complex_reasoning": "claude-opus-4-20250514",
    "code_review": "claude-sonnet-4-20250514",
    "architecture_design": "claude-opus-4-20250514",

    # Medium complexity - balanced model
    "code_generation": "claude-sonnet-4-20250514",
    "summarization": "claude-sonnet-4-20250514",
    "translation": "claude-sonnet-4-20250514",

    # Low complexity - cost-effective model
    "classification": "claude-3-5-haiku-20241022",
    "extraction": "claude-3-5-haiku-20241022",
    "formatting": "claude-3-5-haiku-20241022",
}

def select_model(task_type: str, context: dict) -> str:
    base_model = MODEL_ROUTING.get(task_type, "claude-sonnet-4-20250514")

    # Upgrade for critical paths
    if context.get("is_critical"):
        return upgrade_model(base_model)

    return base_model
```

## Prompt Optimization

### Structured Prompts

```python
OPTIMIZED_PROMPT = """
<context>
{system_context}
</context>

<task>
{task_description}
</task>

<constraints>
- Output format: {output_format}
- Max length: {max_length}
- Required fields: {required_fields}
</constraints>

<examples>
{few_shot_examples}
</examples>

<input>
{user_input}
</input>
"""
```

### Few-Shot Learning

```python
def create_few_shot_prompt(
    task: str,
    examples: list[dict],
    input_data: str
) -> str:
    """Create optimized few-shot prompt."""

    example_text = "\n\n".join([
        f"Input: {ex['input']}\nOutput: {ex['output']}"
        for ex in examples[:3]  # Limit to 3 examples
    ])

    return f"""Task: {task}

Examples:
{example_text}

Now process this input:
Input: {input_data}
Output:"""
```

### Chain of Thought

```python
COT_PROMPT = """
Solve this problem step by step.

Problem: {problem}

Think through this carefully:
1. First, identify the key elements
2. Then, analyze the relationships
3. Finally, derive the solution

Let's work through it:
"""

# For complex reasoning tasks
STRUCTURED_COT = """
<problem>
{problem}
</problem>

<analysis>
Step 1 - Understanding:
[Analyze the problem]

Step 2 - Approach:
[Determine solution strategy]

Step 3 - Execution:
[Apply the approach]

Step 4 - Verification:
[Check the solution]
</analysis>

<answer>
[Final answer]
</answer>
"""
```

## Output Optimization

### Structured Output

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float
    recommendations: list[str]

# Force structured output
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": prompt}],
    tools=[{
        "name": "submit_analysis",
        "description": "Submit structured analysis",
        "input_schema": AnalysisResult.model_json_schema()
    }],
    tool_choice={"type": "tool", "name": "submit_analysis"}
)
```

### Output Parsing

```python
import json
from typing import TypeVar, Type

T = TypeVar('T', bound=BaseModel)

def parse_llm_output(
    response: str,
    model_class: Type[T],
    fallback: T | None = None
) -> T:
    """Parse LLM output with fallback."""
    try:
        # Try JSON parsing first
        data = json.loads(response)
        return model_class.model_validate(data)
    except json.JSONDecodeError:
        # Try extracting JSON from markdown
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0]
            data = json.loads(json_str)
            return model_class.model_validate(data)
    except Exception as e:
        if fallback:
            return fallback
        raise ValueError(f"Failed to parse LLM output: {e}")
```

## Temperature and Sampling

### Temperature Guidelines

```python
TEMPERATURE_SETTINGS = {
    # Deterministic tasks - low temperature
    "classification": 0.0,
    "extraction": 0.0,
    "code_generation": 0.2,
    "translation": 0.3,

    # Creative tasks - higher temperature
    "brainstorming": 0.8,
    "creative_writing": 0.9,
    "exploration": 0.7,

    # Default for general tasks
    "default": 0.5,
}

def get_temperature(task_type: str) -> float:
    return TEMPERATURE_SETTINGS.get(task_type, 0.5)
```

### Sampling Strategies

```python
# For diverse outputs
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8,
    top_p=0.95,  # Nucleus sampling
)

# For consistent outputs
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.0,  # Greedy decoding
)
```

## Context Window Optimization

### Token Estimation

```python
def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars per token)."""
    return len(text) // 4

def fits_context(
    messages: list[dict],
    max_tokens: int = 100000
) -> bool:
    """Check if messages fit in context window."""
    total = sum(estimate_tokens(m["content"]) for m in messages)
    return total < max_tokens * 0.8  # Leave 20% buffer
```

### Context Compression

```python
def compress_context(
    messages: list[dict],
    max_tokens: int
) -> list[dict]:
    """Compress context to fit token limit."""

    # Always keep system message and recent messages
    system = [m for m in messages if m["role"] == "system"]
    recent = messages[-5:]  # Last 5 messages

    current_tokens = sum(
        estimate_tokens(m["content"])
        for m in system + recent
    )

    # Add older messages if space allows
    result = system.copy()
    for msg in messages[len(system):-5]:
        msg_tokens = estimate_tokens(msg["content"])
        if current_tokens + msg_tokens < max_tokens:
            result.append(msg)
            current_tokens += msg_tokens

    result.extend(recent)
    return result
```

## Fine-Tuning Considerations

### When to Fine-Tune

```
Fine-tune when:
├── Consistent specialized format needed
├── Domain-specific terminology important
├── Prompt engineering insufficient
└── Cost savings at scale justify training cost

Don't fine-tune when:
├── Few-shot prompting works well
├── Task requirements change frequently
├── Limited training data available
└── General reasoning needed
```

### Fine-Tuning Data Format

```python
# Training data format for Claude
training_examples = [
    {
        "messages": [
            {"role": "user", "content": "Input text here"},
            {"role": "assistant", "content": "Expected output"}
        ]
    },
    # More examples...
]

# Minimum: 100-1000 high-quality examples
# Quality > Quantity
```

## Performance Monitoring

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LLMMetrics:
    model: str
    task_type: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    success: bool
    timestamp: datetime

class LLMMonitor:
    def __init__(self):
        self.metrics: list[LLMMetrics] = []

    def record(self, metrics: LLMMetrics):
        self.metrics.append(metrics)

        # Alert on high latency
        if metrics.latency_ms > 5000:
            self.alert(f"High latency: {metrics.latency_ms}ms")

        # Alert on failures
        if not metrics.success:
            self.alert(f"LLM call failed: {metrics.model}")

    def get_stats(self, model: str) -> dict:
        model_metrics = [m for m in self.metrics if m.model == model]
        return {
            "avg_latency": sum(m.latency_ms for m in model_metrics) / len(model_metrics),
            "success_rate": sum(1 for m in model_metrics if m.success) / len(model_metrics),
            "total_tokens": sum(m.input_tokens + m.output_tokens for m in model_metrics),
        }
```
