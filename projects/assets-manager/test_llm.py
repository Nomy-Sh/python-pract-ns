#!/usr/bin/env python3
"""Test local_llm in assets-manager project."""

from local_llm import OllamaClient

def main():
    # Create client
    client = OllamaClient()

    # Test chat
    print("Testing local_llm integration...")
    response = client.chat("Say hello in 5 words")
    print(f"Response: {response}")

    # Test code generation
    code = client.generate_code(
        task="Create a Flask route for homepage",
        language="python"
    )
    print("\nGenerated Flask route:")
    print(code)

if __name__ == "__main__":
    main()
