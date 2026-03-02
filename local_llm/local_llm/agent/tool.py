"""Tool definition and registry for the agent system."""
from dataclasses import dataclass
from typing import Callable, Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class Tool:
    """
    A tool that the agent can invoke.

    Attributes:
        name: Unique identifier (e.g., "web_search")
        description: Human-readable description the LLM sees to decide when to use it
        parameters: JSON Schema dict describing the function's parameters
        function: The actual Python callable to execute
        requires_browser: Whether this tool needs a Selenium browser instance
    """
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable
    requires_browser: bool = False

    def to_openai_tool(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            }
        }

    def execute(self, **kwargs) -> str:
        """Execute the tool and return string result."""
        try:
            result = self.function(**kwargs)
            if isinstance(result, str):
                return result
            return json.dumps(result, default=str, indent=2)
        except Exception as e:
            logger.error(f"Tool '{self.name}' failed: {e}")
            return f"Error executing {self.name}: {str(e)}"


class ToolRegistry:
    """Registry that holds tools and provides lookup."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool. Overwrites if name already exists."""
        self._tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_tools(self) -> List[Tool]:
        """Return all registered tools."""
        return list(self._tools.values())

    def to_openai_tools(self) -> List[Dict[str, Any]]:
        """Convert all tools to OpenAI format for the API call."""
        return [tool.to_openai_tool() for tool in self._tools.values()]

    def __len__(self) -> int:
        return len(self._tools)

    def __contains__(self, name: str) -> bool:
        return name in self._tools
