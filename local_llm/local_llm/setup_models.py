"""Setup script to pull recommended models."""
import sys
import ollama

from .config import OLLAMA_BASE_URL
from .models import get_recommended_model_names, print_model_recommendations
from .health import check_ollama_running


def pull_model(model_name: str) -> bool:
    """Pull a model from Ollama registry."""
    print(f"\nPulling model: {model_name}")
    print("This may take several minutes depending on model size...")

    try:
        client = ollama.Client(host=OLLAMA_BASE_URL)

        # Pull with progress indication
        current_status = None
        for progress in client.pull(model_name, stream=True):
            status = progress.get('status', '')

            # Only print status changes to avoid spam
            if status != current_status:
                print(f"  {status}")
                current_status = status

        print(f"✓ Successfully pulled {model_name}")
        return True

    except Exception as e:
        print(f"✗ Failed to pull {model_name}: {str(e)}")
        return False


def setup_models():
    """Pull all recommended models."""
    print("\n" + "="*60)
    print("Local LLM Setup - Pulling Recommended Models")
    print("="*60)

    # Check if Ollama is running
    if not check_ollama_running():
        print("\n✗ Error: Ollama server is not running!")
        print("\nPlease start Ollama:")
        print("  macOS: Open Ollama app or run 'ollama serve'")
        print("  Linux: Run 'ollama serve' in a terminal")
        print(f"\nExpected URL: {OLLAMA_BASE_URL}")
        return False

    print(f"✓ Ollama server is running at {OLLAMA_BASE_URL}")

    # Show what will be installed
    print_model_recommendations()

    # Pull each model
    model_names = get_recommended_model_names()
    print(f"\nPulling {len(model_names)} models...")

    results = {}
    for model_name in model_names:
        results[model_name] = pull_model(model_name)

    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)

    success_count = sum(results.values())
    total_count = len(results)

    for model_name, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {model_name}")

    print(f"\nSuccessfully pulled {success_count}/{total_count} models")
    print("="*60 + "\n")

    return success_count == total_count


def main():
    """CLI entry point for model setup."""
    try:
        success = setup_models()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Setup failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
