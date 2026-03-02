"""Custom exceptions for local LLM service."""


class LocalLLMError(Exception):
    """Base exception for local LLM errors."""
    pass


class OllamaNotRunningError(LocalLLMError):
    """Raised when Ollama server is not running or unreachable."""
    pass


class ModelNotFoundError(LocalLLMError):
    """Raised when a requested model is not available."""
    pass


class CompletionError(LocalLLMError):
    """Raised when LLM completion fails."""
    pass


class AgentError(LocalLLMError):
    """Raised when the agent loop encounters a fatal error."""
    pass


class ToolExecutionError(LocalLLMError):
    """Raised when a tool execution fails."""
    pass


class MaxIterationsError(AgentError):
    """Raised when the agent exceeds maximum iterations."""
    pass
