# Local LLM Service

A reusable Python package for running local LLM tasks using Ollama with an OpenAI-compatible API.

## Features

- **OpenAI-compatible API** for easy portability
- **Task-specific methods** for common LLM operations
- **Model management** with recommended models for M3 Mac
- **Health checks** and setup utilities
- **No API keys required** - runs completely locally

## Installation

### Prerequisites

1. Install Ollama: https://ollama.ai/download
2. Make sure Ollama is running (open the app or run `ollama serve`)

### Install Package

```bash
cd local_llm
pip install -e .
```

Or use the one-command setup:

```bash
bash scripts/setup.sh
```

## Quick Start

### 1. Pull Models

```bash
local-llm-setup
```

This pulls the recommended models:
- `llama3.1:8b` - General purpose (~5GB RAM)
- `sqlcoder:7b` - SQL generation (~4.5GB RAM)
- `phi3:mini` - Fast responses (~2.3GB RAM)

### 2. Check Health

```bash
local-llm-health
```

### 3. Use in Your Code

```python
from local_llm import OllamaClient

client = OllamaClient()

# General chat
response = client.chat("Explain quantum computing in simple terms")

# Natural language to SQL
sql = client.natural_language_to_sql(
    user_query="Show all users who signed up this month",
    schema_info="Table: users (id, name, email, created_at)",
)

# Analyze data
analysis = client.analyze_query_results(
    data=[{"name": "Alice", "sales": 1000}, {"name": "Bob", "sales": 1500}],
    question="Who has the highest sales?",
)

# Understand web pages
context = client.understand_page_context(
    page_content="<html>...</html>",
    question="What is this page about?",
)
```

## Configuration

Environment variables (all optional):

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GENERAL_MODEL=llama3.1:8b
OLLAMA_SQL_MODEL=sqlcoder:7b
OLLAMA_FAST_MODEL=phi3:mini
OLLAMA_TIMEOUT=120
OLLAMA_TEMPERATURE=0.1
```

## API Reference

### OllamaClient

#### `chat(message, system=None, model=None, temperature=None, max_tokens=None)`
General chat completion.

#### `natural_language_to_sql(user_query, schema_info, database_type="MySQL", model=None)`
Convert natural language to SQL.

#### `analyze_query_results(data, question, model=None)`
Analyze query results and answer questions.

#### `understand_page_context(page_content, question, model=None)`
Understand webpage context.

## Using in Other Projects

From any Python project:

```bash
pip install -e /path/to/local_llm
```

Then:

```python
from local_llm import OllamaClient

client = OllamaClient()
# Use as shown above
```

## Recommended Models

| Task | Model | RAM | Use Cases |
|------|-------|-----|-----------|
| General | `llama3.1:8b` | ~5GB | Chat, analysis, general tasks |
| SQL | `sqlcoder:7b` | ~4.5GB | Text-to-SQL, query generation |
| Fast | `phi3:mini` | ~2.3GB | Quick tasks, low latency |

## CLI Commands

- `local-llm-setup` - Pull recommended models
- `local-llm-health` - Check Ollama status and available models

## Testing

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
