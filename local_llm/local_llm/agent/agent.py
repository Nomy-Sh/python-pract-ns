"""Core Agent class implementing the tool-calling loop."""
from typing import List, Optional, Callable, Any, Dict
import json
import logging

from openai import OpenAI
from ..config import (
    OLLAMA_API_BASE,
    DEFAULT_GENERAL_MODEL,
    DEFAULT_TIMEOUT,
    DEFAULT_TEMPERATURE,
    AGENT_MAX_RESULT_LENGTH,
)
from ..exceptions import CompletionError, AgentError, MaxIterationsError
from .tool import Tool, ToolRegistry
from .conversation import ConversationHistory

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant with access to tools.

IMPORTANT: Only use tools when absolutely necessary. Try to answer from your knowledge first.

Use tools ONLY when:
- The user explicitly asks you to search, browse, or fetch something
- You need current/recent information (news, events after your knowledge cutoff)
- You need to access specific web pages or URLs
- You need to analyze user-provided data

DO NOT use tools for:
- General knowledge questions you can answer directly
- Greetings, casual conversation, or clarifications
- Definitions, explanations, or historical facts you already know
- Math, logic, or reasoning you can do yourself

Guidelines:
- Answer directly when you have the knowledge
- Use tools sparingly and only when needed
- After using tools, synthesize the results into a clear response
- If a tool fails, try an alternative approach or explain what went wrong"""


class Agent:
    """
    Agentic AI system that uses LLM tool calling to autonomously solve tasks.

    The agent loop:
    1. Send conversation history + tool definitions to LLM
    2. If LLM responds with tool_calls: execute each tool, add results to history, goto 1
    3. If LLM responds with content (no tool_calls): return the content as final answer
    4. If max_iterations reached: return whatever content is available + warning
    """

    def __init__(
        self,
        tools: Optional[List[Tool]] = None,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        model: str = DEFAULT_GENERAL_MODEL,
        base_url: str = OLLAMA_API_BASE,
        timeout: int = DEFAULT_TIMEOUT,
        temperature: float = DEFAULT_TEMPERATURE,
        max_iterations: int = 10,
        max_history: int = 100,
        on_tool_start: Optional[Callable[[str, Dict], None]] = None,
        on_tool_end: Optional[Callable[[str, str], None]] = None,
        on_thinking: Optional[Callable[[str], None]] = None,
    ):
        """
        Args:
            tools: List of Tool objects the agent can use
            system_prompt: System prompt setting agent behavior
            model: Ollama model to use (must support tool calling, e.g. llama3.1:8b)
            base_url: Ollama API base URL
            timeout: Request timeout in seconds
            temperature: Sampling temperature
            max_iterations: Max tool-call loops before forcing a response
            max_history: Max messages to keep in conversation
            on_tool_start: Callback(tool_name, args) fired before tool execution
            on_tool_end: Callback(tool_name, result) fired after tool execution
            on_thinking: Callback(text) fired when agent produces intermediate text
        """
        self.model = model
        self.temperature = temperature
        self.max_iterations = max_iterations

        # Callbacks for UI
        self.on_tool_start = on_tool_start
        self.on_tool_end = on_tool_end
        self.on_thinking = on_thinking

        # OpenAI client pointed at Ollama
        self.client = OpenAI(
            base_url=base_url,
            api_key="ollama",
            timeout=timeout,
        )

        # Tool registry
        self.registry = ToolRegistry()
        if tools:
            for tool in tools:
                self.registry.register(tool)

        # Conversation history
        self.conversation = ConversationHistory(
            system_prompt=system_prompt,
            max_messages=max_history,
        )

    def add_tool(self, tool: Tool) -> None:
        """Register an additional tool."""
        self.registry.register(tool)

    def chat(self, message: str) -> str:
        """
        Send a message and get a response, potentially using tools.

        This is the main entry point. It adds the user message to history,
        runs the agent loop, and returns the final text response.

        Args:
            message: User's input message

        Returns:
            Agent's final text response

        Raises:
            AgentError: If the agent loop fails
            MaxIterationsError: If max iterations exceeded (still returns partial)
        """
        self.conversation.add_user_message(message)

        try:
            return self._run_loop()
        except MaxIterationsError:
            # Return whatever we have
            last = self.conversation.get_last_assistant_content()
            if last:
                return last + "\n\n[Stopped: reached maximum tool iterations]"
            return "[Agent reached maximum iterations without producing a final answer. Please try rephrasing your question.]"
        except Exception as e:
            logger.error(f"Agent loop failed: {e}", exc_info=True)
            raise AgentError(f"Agent failed: {str(e)}")

    def _run_loop(self) -> str:
        """
        The core agent loop.

        Calls the LLM, checks for tool_calls, executes them,
        feeds results back, repeats until LLM gives a text response.
        """
        openai_tools = self.registry.to_openai_tools() if len(self.registry) > 0 else None

        for iteration in range(self.max_iterations):
            logger.info(f"Agent loop iteration {iteration + 1}/{self.max_iterations}")

            # Build the API call kwargs
            kwargs = {
                "model": self.model,
                "messages": self.conversation.messages,
                "temperature": self.temperature,
            }
            if openai_tools:
                kwargs["tools"] = openai_tools

            # Call the LLM
            try:
                response = self.client.chat.completions.create(**kwargs)
            except Exception as e:
                raise CompletionError(f"LLM call failed: {str(e)}")

            choice = response.choices[0]
            message = choice.message

            # Parse tool calls - handle both native OpenAI format and JSON text fallback
            tool_calls = self._parse_tool_calls(message)

            # Case 1: LLM wants to call tools
            if tool_calls:
                # Add the assistant message (with tool_calls) to history
                # Build proper message format
                assistant_msg = {
                    "role": "assistant",
                    "content": None,  # Clear content when using tools
                    "tool_calls": tool_calls
                }
                self.conversation.add_assistant_tool_calls(assistant_msg)

                # Execute each tool call
                for tc in tool_calls:
                    tool_name = tc["function"]["name"]

                    # Parse arguments (already a dict from _parse_tool_calls)
                    args = tc["function"].get("arguments", {})
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                            logger.warning(f"Failed to parse args for {tool_name}: {args}")

                    # Fire callback
                    if self.on_tool_start:
                        self.on_tool_start(tool_name, args)

                    # Look up and execute the tool
                    tool = self.registry.get(tool_name)
                    if tool:
                        result = tool.execute(**args)
                    else:
                        result = f"Error: Unknown tool '{tool_name}'. Available tools: {[t.name for t in self.registry.list_tools()]}"
                        logger.warning(f"LLM requested unknown tool: {tool_name}")

                    # Truncate very long results to avoid blowing context window
                    if len(result) > AGENT_MAX_RESULT_LENGTH:
                        result = result[:AGENT_MAX_RESULT_LENGTH] + f"\n... [truncated, {len(result)} chars total]"

                    # Fire callback
                    if self.on_tool_end:
                        self.on_tool_end(tool_name, result)

                    # Add tool result to conversation
                    self.conversation.add_tool_result(
                        tool_call_id=tc["id"],
                        name=tool_name,
                        content=result,
                    )

                # Continue the loop -- send tool results back to LLM
                continue

            # Case 2: LLM responded with text (no tool calls) -- this is the final answer
            final_content = message.content or ""
            if final_content:
                self.conversation.add_assistant_message(final_content)
            return final_content.strip()

        # If we exhaust iterations
        raise MaxIterationsError(f"Agent exceeded {self.max_iterations} iterations")

    def _parse_tool_calls(self, message) -> Optional[List[Dict[str, Any]]]:
        """
        Parse tool calls from LLM response, handling both native OpenAI format
        and JSON text fallback for models like llama3.1:8b.

        Returns list of tool call dicts in OpenAI format, or None if no tool calls.
        """
        # Case 1: Native OpenAI format (message.tool_calls is populated)
        if message.tool_calls:
            return [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    }
                }
                for tc in message.tool_calls
            ]

        # Case 2: JSON text fallback for llama3.1:8b
        # Model returns text like: {"name": "tool_name", "parameters": {...}}
        if message.content and isinstance(message.content, str):
            content = message.content.strip()

            # Try to find JSON in the content (might be surrounded by text)
            json_start = content.find('{')
            json_end = content.rfind('}')

            if json_start != -1 and json_end != -1 and json_end > json_start:
                json_str = content[json_start:json_end + 1]
                try:
                    parsed = json.loads(json_str)

                    # Check if it's a tool call format
                    if "name" in parsed and ("parameters" in parsed or "arguments" in parsed):
                        tool_name = parsed["name"]
                        # Handle both "parameters" and "arguments" keys
                        tool_args = parsed.get("parameters", parsed.get("arguments", {}))

                        logger.info(f"Parsed JSON text tool call: {tool_name} with args {tool_args}")

                        # Ollama expects arguments as a JSON string, not a dict
                        args_str = json.dumps(tool_args) if isinstance(tool_args, dict) else tool_args

                        return [{
                            "id": f"call_{abs(hash(json_str)) % 100000}",  # Generate stable ID
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": args_str,
                            }
                        }]
                except (json.JSONDecodeError, ValueError) as e:
                    logger.debug(f"Failed to parse JSON from content: {e}")

        return None

    def reset(self) -> None:
        """Clear conversation history (keeps system prompt and tools)."""
        self.conversation.clear()

    def get_history(self) -> List[Dict[str, Any]]:
        """Get the full conversation history."""
        return self.conversation.messages
