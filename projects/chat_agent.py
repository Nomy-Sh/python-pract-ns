#!/usr/bin/env python3
"""Intelligent multi-agent system with command execution capabilities."""

from local_llm import OllamaClient
import sys
import re
import subprocess
import shlex
import json
import os
from datetime import datetime


class CommandExecutionAgent:
    """Specialist agent for executing terminal commands safely."""

    def __init__(self, client):
        self.client = client

    def parse_command(self, user_input: str) -> dict:
        """Extract and analyze the command from user input."""

        prompt = f"""Extract the Linux/terminal command from this request:

User request: "{user_input}"

If this is a command execution request, provide:
1. The exact command to run
2. A brief 1-2 line description of what it does
3. Any safety warnings if applicable

Format your response as:
COMMAND: [the command]
DESCRIPTION: [1-2 line description]
WARNINGS: [any safety concerns or "None"]

If this is NOT a command request, respond with: "NOT_A_COMMAND"
"""

        response = self.client.chat(prompt, temperature=0.1)

        if "NOT_A_COMMAND" in response:
            return None

        # Parse response
        command_match = re.search(r'COMMAND:\s*(.+)', response)
        desc_match = re.search(r'DESCRIPTION:\s*(.+)', response, re.DOTALL)
        warn_match = re.search(r'WARNINGS:\s*(.+)', response)

        if command_match:
            command = command_match.group(1).strip()
            # Remove backticks if present
            command = command.strip('`').strip()
            description = desc_match.group(1).strip() if desc_match else "Execute command"
            warnings = warn_match.group(1).strip() if warn_match else "None"

            return {
                "command": command,
                "description": description,
                "warnings": warnings
            }

        return None

    def execute(self, user_input: str) -> str:
        """Execute terminal command with user permission."""

        # Parse the command
        cmd_info = self.parse_command(user_input)

        if not cmd_info:
            return "❌ Could not parse a valid command from your request."

        command = cmd_info["command"]
        description = cmd_info["description"]
        warnings = cmd_info["warnings"]

        # Display command info
        print(f"\n📋 Command to execute:")
        print(f"   $ {command}")
        print(f"\n📝 Description:")
        print(f"   {description}")

        if warnings and warnings.lower() != "none":
            print(f"\n⚠️  Warnings:")
            print(f"   {warnings}")

        # Ask for permission
        print("\n" + "="*70)
        response = input("❓ Execute this command? (yes/no): ").strip().lower()

        if response not in ['yes', 'y']:
            return "❌ Command execution cancelled by user."

        # Execute command
        try:
            print("\n🔄 Executing...\n")
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=30
            )

            output = f"✅ Command executed successfully!\n\n"

            if result.stdout:
                output += f"Output:\n{result.stdout}\n"

            if result.stderr:
                output += f"Errors:\n{result.stderr}\n"

            output += f"\nReturn code: {result.returncode}"

            return output

        except subprocess.TimeoutExpired:
            return "❌ Command timed out after 30 seconds"
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"


class MultiAgentOrchestrator:
    """Orchestrates multiple agents for complex tasks."""

    def __init__(self, client):
        self.client = client

    def analyze_workflow(self, user_input: str) -> dict:
        """Determine if request needs multiple agents and create workflow."""

        prompt = f"""Analyze if this request requires multiple specialized agents:

User request: "{user_input}"

Available agents:
1. CODE_GENERATE - Generate code
2. CODE_REVIEW - Review code
3. CODE_EXPLAIN - Explain code
4. SQL_GENERATE - Generate SQL
5. COMMAND_EXECUTE - Run terminal commands
6. CHAT - General conversation

Determine:
1. Does this need multiple agents? (YES/NO)
2. If YES, list the agents needed in order
3. Describe the workflow

Format:
MULTI_AGENT: YES or NO
AGENTS: [agent1, agent2, ...]
WORKFLOW: [brief description]

Example:
MULTI_AGENT: YES
AGENTS: CODE_GENERATE, COMMAND_EXECUTE
WORKFLOW: First generate a Python script, then execute it"""

        response = self.client.chat(prompt, temperature=0.1)

        multi_match = re.search(r'MULTI_AGENT:\s*(YES|NO)', response, re.IGNORECASE)
        agents_match = re.search(r'AGENTS:\s*\[(.+?)\]', response)
        workflow_match = re.search(r'WORKFLOW:\s*(.+)', response, re.DOTALL)

        if multi_match and multi_match.group(1).upper() == 'YES':
            agents_str = agents_match.group(1) if agents_match else ""
            agents = [a.strip() for a in agents_str.split(',')]
            workflow = workflow_match.group(1).strip() if workflow_match else ""

            return {
                "multi_agent": True,
                "agents": agents,
                "workflow": workflow
            }

        return {"multi_agent": False}


class RouterAgent:
    """Main agent that analyzes requests and routes to specialists."""

    def __init__(self, history_file="chat_agent_history.json"):
        self.client = OllamaClient()
        self.conversation_history = []
        self.command_agent = CommandExecutionAgent(self.client)
        self.orchestrator = MultiAgentOrchestrator(self.client)
        self.history_file = history_file
        self.session_start = datetime.now().isoformat()

        # Load existing history
        self._load_history()

    def _load_history(self):
        """Load conversation history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('history', [])
                    print(f"✅ Loaded {len(self.conversation_history)} previous conversations")
            except Exception as e:
                print(f"⚠️  Could not load history: {e}")
                self.conversation_history = []

    def _save_history(self):
        """Save conversation history to file."""
        try:
            data = {
                'session_start': self.session_start,
                'last_updated': datetime.now().isoformat(),
                'history': self.conversation_history
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save history: {e}")

    def _add_to_history(self, user_input: str, specialist_type: str, specialist_response: str, final_response: str):
        """Add an exchange to conversation history."""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'specialist_type': specialist_type,
            'specialist_response': specialist_response,
            'final_response': final_response
        })
        # Keep only last 50 exchanges to prevent file from growing too large
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
        self._save_history()

    def _get_recent_context(self, limit=5):
        """Get recent conversation context for continuity."""
        if not self.conversation_history:
            return ""

        recent = self.conversation_history[-limit:]
        context = "Recent conversation context:\n"
        for exchange in recent:
            context += f"User: {exchange['user_input'][:100]}\n"
            context += f"Response: {exchange['final_response'][:100]}\n\n"
        return context

    def synthesize_final_response(self, user_input: str, specialist_type: str, specialist_response: str) -> str:
        """
        Synthesize a final response from Router Agent perspective.
        Incorporates context and provides a cohesive response as the main entity.
        """
        # For command execution, keep it simple and direct
        if specialist_type == "COMMAND_EXECUTE":
            if "successfully" in specialist_response.lower():
                return f"✅ Command executed successfully. Here's what I found:\n\n{specialist_response}"
            else:
                return specialist_response

        # For chat, return as-is (already conversational)
        if specialist_type == "CHAT":
            return specialist_response

        # For technical responses, add Router Agent's context
        context = self._get_recent_context(limit=3)

        # Build a prompt for the Router Agent to provide final response
        prompt = f"""You are the Router Agent, the main coordinator of a multi-agent system.

{context if context else 'This is a new conversation.'}

User's current request: "{user_input}"

The {specialist_type} specialist has processed this request and provided the following result:

{specialist_response[:1000]}{'...' if len(specialist_response) > 1000 else ''}

As the Router Agent, provide a brief, natural final response to the user that:
1. Acknowledges what was done
2. Highlights key points from the specialist's work
3. Maintains conversational continuity
4. Keeps it concise (2-4 sentences for code/technical tasks)

Respond naturally as the Router Agent coordinating this multi-agent system."""

        try:
            final_response = self.client.chat(prompt, temperature=0.3)
            return final_response
        except Exception:
            # Fallback: return specialist response with minimal wrapper
            return f"[{specialist_type} completed]\n\n{specialist_response}"

    def analyze_intent(self, user_input: str) -> dict:
        """Analyze user intent to determine which specialist to use."""

        analysis_prompt = f"""Analyze this user request and determine the intent:

User request: "{user_input}"

Classify the intent into ONE of these categories:
1. CODE_GENERATE - User wants to generate/create new code
2. CODE_REVIEW - User wants feedback/review on existing code
3. CODE_EXPLAIN - User wants to understand what code does
4. SQL_GENERATE - User wants to create SQL queries
5. COMMAND_EXECUTE - User wants to run a terminal/Linux command
6. CHAT - General conversation, questions, or anything else

Indicators:
- CODE_GENERATE: "create", "generate", "write", "build", "make a function"
- CODE_REVIEW: "review", "check", "improve", "what's wrong", contains code snippets
- CODE_EXPLAIN: "explain", "what does", "how does", "understand this code"
- SQL_GENERATE: mentions "database", "query", "SQL", "select", "table"
- COMMAND_EXECUTE: "run", "execute", "command", "list files", "check", mentions commands like ls, grep, ps
- CHAT: everything else

Respond with ONLY the category name (e.g., "CODE_GENERATE" or "CHAT"), nothing else."""

        try:
            intent = self.client.chat(analysis_prompt, temperature=0.1).strip().upper()

            # Clean up response and map to intent
            if "CODE_GENERATE" in intent:
                return {"type": "CODE_GENERATE", "icon": "💻"}
            elif "CODE_REVIEW" in intent:
                return {"type": "CODE_REVIEW", "icon": "🔍"}
            elif "CODE_EXPLAIN" in intent:
                return {"type": "CODE_EXPLAIN", "icon": "📚"}
            elif "SQL_GENERATE" in intent:
                return {"type": "SQL_GENERATE", "icon": "🗃️"}
            elif "COMMAND_EXECUTE" in intent:
                return {"type": "COMMAND_EXECUTE", "icon": "⚡"}
            else:
                return {"type": "CHAT", "icon": "💬"}
        except Exception:
            return {"type": "CHAT", "icon": "💬"}

    def route_to_specialist(self, user_input: str, intent: dict) -> str:
        """Route request to appropriate specialist agent."""

        intent_type = intent["type"]
        icon = intent["icon"]

        print(f"\n{icon} [Routing to {intent_type} specialist...]")

        try:
            if intent_type == "CODE_GENERATE":
                return self.code_generation_agent(user_input)

            elif intent_type == "CODE_REVIEW":
                return self.code_review_agent(user_input)

            elif intent_type == "CODE_EXPLAIN":
                return self.code_explanation_agent(user_input)

            elif intent_type == "SQL_GENERATE":
                return self.sql_generation_agent(user_input)

            elif intent_type == "COMMAND_EXECUTE":
                return self.command_agent.execute(user_input)

            else:  # CHAT
                return self.general_chat_agent(user_input)

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def handle_multi_agent_workflow(self, user_input: str, workflow: dict) -> str:
        """Handle requests that need multiple agents."""

        print(f"\n🔗 [Multi-agent workflow detected]")
        print(f"📋 Workflow: {workflow['workflow']}")
        print(f"🤖 Agents needed: {', '.join(workflow['agents'])}\n")

        results = []
        workflow_log = []

        for agent_type in workflow['agents']:
            print(f"\n{'='*70}")
            print(f"➡️  Executing: {agent_type}")
            print(f"{'='*70}")

            # Create a focused sub-task for this agent
            intent = {"type": agent_type, "icon": "🔗"}
            result = self.route_to_specialist(user_input, intent)

            # Store structured result
            workflow_log.append({
                'agent': agent_type,
                'result': result
            })
            results.append(f"\n[{agent_type} Result]:\n{result}")

            # Ask if user wants to continue to next agent
            if len(workflow['agents']) > 1 and agent_type != workflow['agents'][-1]:
                response = input("\n➡️  Continue to next agent? (yes/no): ").strip().lower()
                if response not in ['yes', 'y']:
                    results.append("\n⚠️  Workflow stopped by user")
                    break

        # Return combined workflow results
        return "\n\n".join(results)

    def code_generation_agent(self, user_input: str) -> str:
        """Specialist for generating code."""
        language = "python"
        if "javascript" in user_input.lower() or "js" in user_input.lower():
            language = "javascript"
        elif "java" in user_input.lower() and "javascript" not in user_input.lower():
            language = "java"
        elif "go" in user_input.lower():
            language = "go"

        return self.client.generate_code(user_input, language)

    def code_review_agent(self, user_input: str) -> str:
        """Specialist for reviewing code."""
        code_match = re.search(r'```[\s\S]*?```|`[^`]+`', user_input)

        if code_match:
            code = code_match.group(0).strip('`').strip()
        else:
            code = user_input

        focus = "general"
        if "security" in user_input.lower():
            focus = "security"
        elif "performance" in user_input.lower() or "speed" in user_input.lower():
            focus = "performance"
        elif "style" in user_input.lower() or "format" in user_input.lower():
            focus = "style"

        return self.client.review_code(code, focus)

    def code_explanation_agent(self, user_input: str) -> str:
        """Specialist for explaining code."""
        code_match = re.search(r'```[\s\S]*?```|`[^`]+`', user_input)

        if code_match:
            code = code_match.group(0).strip('`').strip()
        else:
            code = user_input

        detail_level = "concise"
        if "beginner" in user_input.lower() or "simple" in user_input.lower():
            detail_level = "beginner"
        elif "detailed" in user_input.lower() or "depth" in user_input.lower():
            detail_level = "detailed"

        return self.client.explain_code(code, detail_level)

    def sql_generation_agent(self, user_input: str) -> str:
        """Specialist for generating SQL queries."""
        schema_match = re.search(r'schema:?\s*(.+)', user_input, re.IGNORECASE | re.DOTALL)

        if schema_match:
            schema_info = schema_match.group(1).strip()
            query_text = re.sub(r'schema:?\s*.+', '', user_input, flags=re.IGNORECASE | re.DOTALL).strip()
        else:
            return "🗃️ To generate SQL, I need schema information. Please provide:\n\nExample: 'Create a query to find all users. Schema: users table has id, name, email, created_at columns'"

        return self.client.natural_language_to_sql(query_text, schema_info)

    def general_chat_agent(self, user_input: str) -> str:
        """Specialist for general conversation."""
        return self.client.chat(user_input)

    def run(self):
        """Main interactive loop."""
        print("\n" + "=" * 70)
        print("  🤖 Router Agent - Intelligent Multi-Agent System")
        print("  Coordinating specialized agents for your tasks")
        print("=" * 70)
        print("\n✅ Connected to Ollama")
        if self.conversation_history:
            print(f"📚 Loaded conversation history ({len(self.conversation_history)} previous exchanges)")
        print("\n💡 Available Specialists:")
        print("   • Code Generation (Python, JS, Go, Java)")
        print("   • Code Review & Explanation")
        print("   • SQL Query Generation")
        print("   • Command Execution (Linux/bash)")
        print("   • General Chat")
        print("   • Multi-agent orchestration for complex tasks")
        print(f"\n💾 Session history: {self.history_file}")
        print("\n   Type 'exit' or 'quit' to end the session.\n")
        print("-" * 70)

        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\n👋 Goodbye! Session saved to {self.history_file}")
                    print(f"📊 Total exchanges this session: {len([h for h in self.conversation_history if h.get('timestamp', '').startswith(self.session_start.split('T')[0])])}")
                    break

                if not user_input:
                    continue

                # Check if multi-agent workflow is needed
                print("🔄 [Analyzing request...]", end="\r")
                workflow = self.orchestrator.analyze_workflow(user_input)

                if workflow.get("multi_agent"):
                    # Handle multi-agent workflow
                    specialist_response = self.handle_multi_agent_workflow(user_input, workflow)
                    specialist_type = "MULTI_AGENT"
                else:
                    # Single agent routing
                    intent = self.analyze_intent(user_input)
                    specialist_type = intent["type"]
                    specialist_response = self.route_to_specialist(user_input, intent)

                # Synthesize final response from Router Agent
                print(f"\n🤖 Router Agent [Synthesizing final response...]\n")
                final_response = self.synthesize_final_response(user_input, specialist_type, specialist_response)

                print(f"🤖 Router Agent:\n{final_response}\n")
                print("-" * 70)

                # Save to history
                self._add_to_history(user_input, specialist_type, specialist_response, final_response)

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    """Entry point."""
    try:
        agent = RouterAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        print("Make sure Ollama is running!")
        sys.exit(1)


if __name__ == "__main__":
    main()
