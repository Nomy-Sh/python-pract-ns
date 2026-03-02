#!/bin/bash
# One-command setup for local_llm

set -e  # Exit on error

echo "=========================================="
echo "Local LLM Setup Script"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: Must be run from local_llm project root"
    exit 1
fi

# Install package in editable mode
echo ""
echo "Installing local_llm package..."
pip install -e ".[dev]"

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running (open Ollama app or run 'ollama serve')"
echo "2. Run: local-llm-setup      (to pull recommended models)"
echo "3. Run: local-llm-health     (to verify setup)"
echo ""
echo "=========================================="
