"""Health check utilities for Ollama service."""
import sys
from typing import Dict, List
import httpx
import ollama

from .config import OLLAMA_BASE_URL, HEALTH_CHECK_TIMEOUT
from .exceptions import OllamaNotRunningError


def check_ollama_running() -> bool:
    """Check if Ollama server is running."""
    try:
        response = httpx.get(
            f"{OLLAMA_BASE_URL}/api/tags",
            timeout=HEALTH_CHECK_TIMEOUT
        )
        return response.status_code == 200
    except (httpx.ConnectError, httpx.TimeoutException):
        return False


def get_available_models() -> List[str]:
    """Get list of available models from Ollama."""
    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)
        models_response = client.list()
        return [model.model for model in models_response.models]
    except Exception as e:
        raise OllamaNotRunningError(f"Failed to fetch models: {str(e)}")


def get_health_status() -> Dict:
    """Get comprehensive health status."""
    status = {
        "ollama_running": False,
        "base_url": OLLAMA_BASE_URL,
        "models_available": [],
        "error": None
    }

    try:
        status["ollama_running"] = check_ollama_running()

        if status["ollama_running"]:
            status["models_available"] = get_available_models()
        else:
            status["error"] = "Ollama server is not running or unreachable"
    except Exception as e:
        status["error"] = str(e)

    return status


def print_health_status():
    """Print formatted health status."""
    status = get_health_status()

    print(f"\n{'='*60}")
    print("Local LLM Health Check")
    print(f"{'='*60}")
    print(f"Ollama URL:     {status['base_url']}")
    print(f"Status:         {'✓ Running' if status['ollama_running'] else '✗ Not Running'}")

    if status['error']:
        print(f"Error:          {status['error']}")

    if status['models_available']:
        print(f"\nAvailable Models ({len(status['models_available'])}):")
        for model in sorted(status['models_available']):
            print(f"  • {model}")
    else:
        print("\nNo models available. Run 'local-llm-setup' to pull models.")

    print(f"{'='*60}\n")

    return status


def main():
    """CLI entry point for health check."""
    status = print_health_status()

    # Exit with error code if not healthy
    if not status['ollama_running'] or not status['models_available']:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
