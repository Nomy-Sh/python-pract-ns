"""Rich CLI chat interface for the agent."""
import sys
import signal
import logging
from typing import Dict
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import box

from local_llm.agent import Agent
from local_llm.health import check_ollama_running, get_available_models
from local_llm.config import DEFAULT_GENERAL_MODEL, AGENT_MAX_ITERATIONS

logger = logging.getLogger(__name__)

console = Console()


def display_welcome():
    """Show welcome banner."""
    welcome = Table(show_header=False, box=box.DOUBLE_EDGE, expand=True)
    welcome.add_row(
        "[bold cyan]Agent Chat[/bold cyan]\n"
        "[dim]Local AI agent with web search, scraping, and data analysis[/dim]\n"
        "\n"
        "[dim]Commands: /help, /clear, /tools, /history, /quit[/dim]"
    )
    console.print(welcome)
    console.print()


def display_tool_execution(tool_name: str, args: Dict):
    """Called when a tool starts executing."""
    args_summary = ", ".join(f"{k}={repr(v)[:50]}" for k, v in args.items())
    console.print(
        f"  [yellow]> [bold]{tool_name}[/bold]({args_summary})[/yellow]"
    )


def display_tool_result(tool_name: str, result: str):
    """Called when a tool finishes."""
    # Show a truncated preview of the result
    preview = result[:200].replace("\n", " ")
    if len(result) > 200:
        preview += "..."
    console.print(f"  [green]< {tool_name}[/green] [dim]({len(result)} chars)[/dim]")


def display_thinking(text: str):
    """Called when agent produces intermediate thinking."""
    console.print(f"  [dim italic]{text}[/dim italic]")


def handle_slash_command(command: str, agent: Agent) -> bool:
    """
    Handle slash commands. Returns True if should exit.
    """
    cmd = command.strip().lower()

    if cmd in ("/quit", "/exit", "/q"):
        console.print("[dim]Goodbye![/dim]")
        return True

    if cmd == "/clear":
        agent.reset()
        console.clear()
        display_welcome()
        console.print("[dim]Conversation cleared.[/dim]")
        return False

    if cmd == "/tools":
        table = Table(title="Available Tools", box=box.SIMPLE)
        table.add_column("Tool", style="cyan")
        table.add_column("Description")
        table.add_column("Browser?", justify="center")
        for tool in agent.registry.list_tools():
            browser = "[yellow]Yes[/yellow]" if tool.requires_browser else "No"
            table.add_row(tool.name, tool.description[:80], browser)
        console.print(table)
        return False

    if cmd == "/history":
        for msg in agent.get_history():
            role = msg["role"]
            content = msg.get("content", "")
            if role == "system":
                console.print(f"[dim][system] {content[:100]}...[/dim]")
            elif role == "user":
                console.print(f"[cyan][user][/cyan] {content}")
            elif role == "assistant":
                if content:
                    console.print(f"[green][assistant][/green] {content[:200]}")
                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        console.print(f"  [yellow]-> {tc['function']['name']}()[/yellow]")
            elif role == "tool":
                console.print(f"  [dim][tool:{msg.get('name', '?')}] {content[:100]}...[/dim]")
        return False

    if cmd == "/help":
        help_text = """
**Commands:**
- `/help` - Show this help
- `/tools` - List available tools
- `/history` - Show conversation history
- `/clear` - Clear conversation and screen
- `/quit` - Exit the chat

**Tips:**
- Ask questions naturally - the agent will use tools automatically
- "Search for Python tutorials" -> agent uses web_search
- "What does example.com say?" -> agent uses fetch_page
- "Summarize this data: [paste data]" -> agent uses analyze_data
"""
        console.print(Markdown(help_text))
        return False

    console.print(f"[red]Unknown command: {command}[/red]")
    return False


def main():
    """Main CLI entry point."""
    # Check Ollama health first
    if not check_ollama_running():
        console.print("[red bold]Error: Ollama is not running![/red bold]")
        console.print("Start Ollama first: open the Ollama app or run 'ollama serve'")
        sys.exit(1)

    # Parse CLI arguments
    import argparse
    parser = argparse.ArgumentParser(description="Agent Chat - AI assistant with tools")
    parser.add_argument("--model", default=DEFAULT_GENERAL_MODEL, help="LLM model to use")
    parser.add_argument("--max-iterations", type=int, default=AGENT_MAX_ITERATIONS, help="Max tool iterations")
    parser.add_argument("--no-browser", action="store_true", help="Disable browser-based tools")
    parser.add_argument("--copart", action="store_true", help="Enable Copart query tool")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Load tools
    from tools import get_default_tools
    tools = get_default_tools(
        include_browser_tools=not args.no_browser,
        include_copart=args.copart,
    )

    # Create agent
    agent = Agent(
        tools=tools,
        model=args.model,
        max_iterations=args.max_iterations,
        on_tool_start=display_tool_execution,
        on_tool_end=display_tool_result,
        on_thinking=display_thinking,
    )

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        console.print("\n[dim]Interrupted. Type /quit to exit.[/dim]")
    signal.signal(signal.SIGINT, signal_handler)

    # Display welcome
    display_welcome()

    # Main chat loop
    while True:
        try:
            user_input = console.input("[bold cyan]You:[/bold cyan] ").strip()

            if not user_input:
                continue

            # Handle slash commands
            if user_input.startswith("/"):
                should_exit = handle_slash_command(user_input, agent)
                if should_exit:
                    break
                continue

            # Send to agent
            console.print()  # Spacing
            with console.status("[bold green]Thinking...", spinner="dots"):
                response = agent.chat(user_input)

            # Display response as markdown
            console.print()
            console.print(Panel(
                Markdown(response),
                title="[bold green]Agent[/bold green]",
                border_style="green",
                expand=True,
            ))
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Type /quit to exit.[/dim]")
            continue
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]\n")
            logger.error(f"Chat error: {e}", exc_info=True)

    # Cleanup
    try:
        from tools.browse_page import shutdown_browser
        shutdown_browser()
    except Exception:
        pass


if __name__ == "__main__":
    main()
