# 🚀 Quick Start Guide - Agentic AI System

## ⚡ TL;DR

```bash
# Start chatting with your AI agent
agent-chat
```

That's it! Your local AI agent with web search, scraping, and data analysis is ready.

---

## 📋 What You Have

### Agent Chat (CLI)
```bash
agent-chat                      # Start interactive chat
agent-chat --verbose            # Debug mode
agent-chat --no-browser         # Disable Selenium tools
agent-chat --max-iterations 5   # Limit tool calls
```

### Python API
```python
from local_llm.agent import Agent
from tools import get_default_tools

agent = Agent(tools=get_default_tools())
response = agent.chat("Search for Python tutorials")
print(response)
```

---

## 🔧 Available Tools

| Tool | What It Does | Speed |
|------|--------------|-------|
| `web_search` | Search the web with DuckDuckGo | Fast |
| `fetch_page` | Get content from static pages | Fast |
| `browse_page` | Render JS-heavy sites (Selenium) | Slow |
| `extract_links` | Get all links from a page | Fast |
| `analyze_data` | LLM data analysis | Medium |
| `query_copart` | Copart database queries | Slow |

---

## 💬 Example Conversations

### Simple Questions (No Tools)
```
You: Hello!
Agent: [Greets you directly]

You: What is 2 + 2?
Agent: [Answers directly]
```

### With Tool Usage
```
You: Search for Python web scraping tutorials
Agent: [Uses web_search]
Agent: Here are some great tutorials...

You: Fetch the first one and summarize it
Agent: [Uses fetch_page]
Agent: The tutorial covers...

You: What links are on python.org?
Agent: [Uses extract_links]
Agent: Here are the main links...
```

---

## 🎮 CLI Commands

Inside `agent-chat`:

```bash
/help       # Show help
/tools      # List available tools
/history    # Show conversation
/clear      # Reset conversation
/quit       # Exit
```

---

## 🛠️ Customization

### Add Your Own Tool

```python
from local_llm.agent import Agent, Tool

def my_function(param: str) -> str:
    return f"Result: {param}"

tool = Tool(
    name="my_tool",
    description="What this tool does",
    parameters={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    },
    function=my_function
)

agent = Agent(tools=[tool])
response = agent.chat("Use my tool with test")
```

### Configure Models

Create `.env`:
```bash
OLLAMA_GENERAL_MODEL=llama3.1:8b
OLLAMA_FAST_MODEL=phi3:mini
AGENT_MAX_ITERATIONS=10
```

### Add Site Strategies

Edit `configs/sites.yaml`:
```yaml
sites:
  - pattern: "*.yoursite.com/*"
    strategy: fetch
    notes: "Your custom site"
```

---

## 🔍 Troubleshooting

### Agent Not Calling Tools?

Check logs:
```bash
agent-chat --verbose
```

### SSL Errors?

```bash
pip install --upgrade certifi
```

### Want More Tools?

Edit `tools/__init__.py` and add your tool to `get_default_tools()`

---

## 📚 Documentation Files

- `AGENT_SYSTEM_COMPLETE.md` - Full implementation details
- `TESTING_COMPLETE.md` - Test results and verification
- `QUICK_START.md` - This file
- `MIGRATION_COMPLETE.md` - Original LLM migration
- `SYSTEM_READY.md` - System status

---

## 🎯 Common Use Cases

### Research
```
You: Search for information about [topic]
Agent: [Searches web, summarizes findings]
```

### Web Scraping
```
You: Get the content from [URL]
Agent: [Fetches page, extracts content]

You: Extract all links from [URL]
Agent: [Gets links, formats them]
```

### Data Analysis
```
You: Analyze this data: [paste data]
     What's the average?
Agent: [Uses analyze_data tool, provides insights]
```

### Copart Queries
```bash
agent-chat --copart  # Enable Copart tool

You: Query Copart for Toyota vehicles under $20k
Agent: [Opens browser, runs query, returns results]
```

---

## ⚡ Pro Tips

1. **Be Specific**: "Search for Python 3.12 features" works better than "Python info"

2. **Chain Questions**: The agent remembers context
   ```
   You: Search for Python tutorials
   You: Which one is best for beginners?  # Remembers previous search
   ```

3. **Use /clear**: Reset when changing topics
   ```
   You: /clear
   You: [New topic]
   ```

4. **Check Tools**: Use `/tools` to see what's available

5. **Adjust Iterations**: Use `--max-iterations` for complex multi-step tasks

---

## 🚀 Advanced Usage

### Background Mode
```python
from local_llm.agent import Agent
from tools import get_default_tools

agent = Agent(tools=get_default_tools())

# Run multiple queries
questions = [
    "Search for Python tutorials",
    "What is machine learning?",
    "Get links from python.org"
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {agent.chat(q)}\n")
    print("-" * 60)
```

### Custom Callbacks
```python
def on_tool(name, args):
    print(f"🔧 Using: {name}")
    # Log to file, send notification, etc.

def on_result(name, result):
    print(f"✅ {name}: {len(result)} chars")
    # Store results, update UI, etc.

agent = Agent(
    tools=get_default_tools(),
    on_tool_start=on_tool,
    on_tool_end=on_result
)
```

### Multi-Agent System
```python
# Research agent
researcher = Agent(
    tools=[web_search, fetch_page],
    system_prompt="You are a research assistant..."
)

# Data analyst agent
analyst = Agent(
    tools=[analyze_data],
    system_prompt="You are a data analyst..."
)

# Use different agents for different tasks
research = researcher.chat("Find Python tutorials")
analysis = analyst.chat(f"Analyze this: {research}")
```

---

## 🎉 You're Ready!

Start with:
```bash
agent-chat
```

Ask anything, and the agent will use tools as needed!

---

**Happy Chatting! 🤖**
