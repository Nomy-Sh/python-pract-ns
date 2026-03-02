"""Conversation history management for multi-turn agent chat."""
from typing import List, Dict, Any, Optional
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)


class ConversationHistory:
    """
    Manages the ordered list of messages for multi-turn conversation.

    Message format follows the OpenAI chat completions spec:
    - {"role": "system", "content": "..."}
    - {"role": "user", "content": "..."}
    - {"role": "assistant", "content": "..."} or with tool_calls
    - {"role": "tool", "tool_call_id": "...", "name": "...", "content": "..."}
    """

    def __init__(self, system_prompt: Optional[str] = None, max_messages: int = 100):
        self._messages: List[Dict[str, Any]] = []
        self._max_messages = max_messages
        if system_prompt:
            self._messages.append({"role": "system", "content": system_prompt})

    @property
    def messages(self) -> List[Dict[str, Any]]:
        """Return a copy of the message list."""
        return deepcopy(self._messages)

    def add_user_message(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})
        self._trim_if_needed()

    def add_assistant_message(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})
        self._trim_if_needed()

    def add_assistant_tool_calls(self, message: Dict[str, Any]) -> None:
        """Add an assistant message that contains tool_calls (the raw response message)."""
        self._messages.append(message)
        self._trim_if_needed()

    def add_tool_result(self, tool_call_id: str, name: str, content: str) -> None:
        """Add a tool result message."""
        self._messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "name": name,
            "content": content,
        })
        self._trim_if_needed()

    def clear(self) -> None:
        """Clear all messages except the system prompt."""
        system = [m for m in self._messages if m["role"] == "system"]
        self._messages = system

    def get_last_assistant_content(self) -> Optional[str]:
        """Get the content of the most recent assistant message."""
        for msg in reversed(self._messages):
            if msg["role"] == "assistant" and msg.get("content"):
                return msg["content"]
        return None

    def _trim_if_needed(self) -> None:
        """Trim old messages if over max, keeping system prompt."""
        if len(self._messages) <= self._max_messages:
            return
        system = [m for m in self._messages if m["role"] == "system"]
        non_system = [m for m in self._messages if m["role"] != "system"]
        # Keep the most recent messages
        keep = self._max_messages - len(system)
        self._messages = system + non_system[-keep:]
        logger.debug(f"Trimmed conversation to {len(self._messages)} messages")

    def __len__(self) -> int:
        return len(self._messages)
