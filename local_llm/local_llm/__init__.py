"""Local LLM service using Ollama with OpenAI-compatible API."""

from .client import OllamaClient
from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_API_BASE,
    DEFAULT_GENERAL_MODEL,
    DEFAULT_SQL_MODEL,
    DEFAULT_FAST_MODEL,
)
from .exceptions import (
    LocalLLMError,
    OllamaNotRunningError,
    ModelNotFoundError,
    CompletionError,
    AgentError,
    ToolExecutionError,
    MaxIterationsError,
)
from .health import check_ollama_running, get_available_models, get_health_status
from .agent import Agent, Tool, ToolRegistry, ConversationHistory

__version__ = "0.1.0"

__all__ = [
    "OllamaClient",
    "OLLAMA_BASE_URL",
    "OLLAMA_API_BASE",
    "DEFAULT_GENERAL_MODEL",
    "DEFAULT_SQL_MODEL",
    "DEFAULT_FAST_MODEL",
    "LocalLLMError",
    "OllamaNotRunningError",
    "ModelNotFoundError",
    "CompletionError",
    "AgentError",
    "ToolExecutionError",
    "MaxIterationsError",
    "check_ollama_running",
    "get_available_models",
    "get_health_status",
    "Agent",
    "Tool",
    "ToolRegistry",
    "ConversationHistory",
]
