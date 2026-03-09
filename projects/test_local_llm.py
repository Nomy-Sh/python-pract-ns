#!/usr/bin/env python3
"""Interactive chat interface for local_llm package."""

from local_llm import OllamaClient
import sys


def print_header():
    """Print welcome header."""
    print("\n" + "=" * 70)
    print("  🤖 Local LLM Interactive Chat")
    print("  Model: qwen2.5-coder:7b")
    print("=" * 70)


def print_menu():
    """Print available modes."""
    print("\n📋 Available Modes:")
    print("  1. chat       - General conversation")
    print("  2. code       - Generate code")
    print("  3. review     - Review code")
    print("  4. explain    - Explain code")
    print("  5. sql        - Natural language to SQL")
    print("  6. help       - Show this menu")
    print("  7. exit/quit  - Exit the program")
    print("-" * 70)


def chat_mode(client):
    """General chat mode."""
    print("\n💬 Chat Mode (type 'back' to return to menu)")
    print("-" * 70)

    while True:
        user_input = input("\n👤 You: ").strip()

        if user_input.lower() in ['back', 'menu']:
            break
        if not user_input:
            continue

        print("\n🤖 Agent: ", end="", flush=True)
        try:
            response = client.chat(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {e}")


def code_mode(client):
    """Code generation mode."""
    print("\n💻 Code Generation Mode (type 'back' to return to menu)")
    print("-" * 70)

    while True:
        print("\n📝 Describe what code you want to generate:")
        task = input("👤 Task: ").strip()

        if task.lower() in ['back', 'menu']:
            break
        if not task:
            continue

        language = input("🔤 Language (default: python): ").strip() or "python"

        print("\n🤖 Generating code...\n")
        try:
            code = client.generate_code(task, language)
            print(code)
        except Exception as e:
            print(f"Error: {e}")


def review_mode(client):
    """Code review mode."""
    print("\n🔍 Code Review Mode (type 'back' to return to menu)")
    print("-" * 70)

    while True:
        print("\n📝 Paste your code (type 'END' on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            if line.strip().upper() in ['BACK', 'MENU']:
                return
            lines.append(line)

        if not lines:
            continue

        code = '\n'.join(lines)
        focus = input("🎯 Focus (general/security/performance/style, default: general): ").strip() or "general"

        print("\n🤖 Reviewing code...\n")
        try:
            review = client.review_code(code, focus)
            print(review)
        except Exception as e:
            print(f"Error: {e}")


def explain_mode(client):
    """Code explanation mode."""
    print("\n📚 Code Explanation Mode (type 'back' to return to menu)")
    print("-" * 70)

    while True:
        print("\n📝 Paste your code (type 'END' on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            if line.strip().upper() in ['BACK', 'MENU']:
                return
            lines.append(line)

        if not lines:
            continue

        code = '\n'.join(lines)
        level = input("📊 Detail level (concise/detailed/beginner, default: concise): ").strip() or "concise"

        print("\n🤖 Explaining code...\n")
        try:
            explanation = client.explain_code(code, level)
            print(explanation)
        except Exception as e:
            print(f"Error: {e}")


def sql_mode(client):
    """SQL generation mode."""
    print("\n🗃️  SQL Generation Mode (type 'back' to return to menu)")
    print("-" * 70)

    while True:
        print("\n📝 Enter your database schema:")
        schema = input("👤 Schema: ").strip()

        if schema.lower() in ['back', 'menu']:
            break
        if not schema:
            continue

        print("\n📝 What query do you want?")
        query = input("👤 Query: ").strip()

        if query.lower() in ['back', 'menu']:
            break
        if not query:
            continue

        print("\n🤖 Generating SQL...\n")
        try:
            sql = client.natural_language_to_sql(query, schema)
            print(sql)
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main interactive loop."""
    print_header()

    # Initialize client
    try:
        client = OllamaClient()
        print("\n✅ Connected to Ollama")
    except Exception as e:
        print(f"\n❌ Error connecting to Ollama: {e}")
        print("Make sure Ollama is running!")
        sys.exit(1)

    print_menu()

    modes = {
        '1': ('chat', chat_mode),
        '2': ('code', code_mode),
        '3': ('review', review_mode),
        '4': ('explain', explain_mode),
        '5': ('sql', sql_mode),
        'chat': ('chat', chat_mode),
        'code': ('code', code_mode),
        'review': ('review', review_mode),
        'explain': ('explain', explain_mode),
        'sql': ('sql', sql_mode),
    }

    while True:
        try:
            choice = input("\n🎯 Select mode (1-5 or name): ").strip().lower()

            if choice in ['exit', 'quit', '7']:
                print("\n👋 Goodbye!")
                break

            if choice in ['help', '6', 'menu']:
                print_menu()
                continue

            if choice in modes:
                mode_name, mode_func = modes[choice]
                mode_func(client)
            else:
                print("❌ Invalid choice. Type 'help' to see options.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
