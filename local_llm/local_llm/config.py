"""Configuration for local LLM service."""
import os

# Ollama server configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_API_BASE = f"{OLLAMA_BASE_URL}/v1"  # OpenAI-compatible endpoint

# Default models for different tasks
DEFAULT_GENERAL_MODEL = os.getenv("OLLAMA_GENERAL_MODEL", "llama3.1:8b")
DEFAULT_SQL_MODEL = os.getenv("OLLAMA_SQL_MODEL", "llama3.1:8b")  # llama3.1:8b works better than sqlcoder:7b
DEFAULT_FAST_MODEL = os.getenv("OLLAMA_FAST_MODEL", "phi3:mini")

# Timeouts
DEFAULT_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))  # seconds
HEALTH_CHECK_TIMEOUT = 5  # seconds

# Temperature settings
DEFAULT_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.1"))

# Agent settings
AGENT_MAX_ITERATIONS = int(os.getenv("AGENT_MAX_ITERATIONS", "10"))
DEFAULT_AGENT_MODEL = os.getenv("OLLAMA_AGENT_MODEL", "llama3.1:8b")
AGENT_MAX_RESULT_LENGTH = int(os.getenv("AGENT_MAX_RESULT_LENGTH", "4000"))
