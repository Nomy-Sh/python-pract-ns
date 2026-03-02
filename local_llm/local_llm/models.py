"""Model registry and recommendations."""

# Recommended models for 16GB M3 Mac
RECOMMENDED_MODELS = {
    "general": {
        "name": "llama3.1:8b",
        "description": "General-purpose conversational model",
        "ram_required": "~5GB",
        "use_cases": ["chat", "general tasks", "analysis"]
    },
    "sql": {
        "name": "sqlcoder:7b",
        "description": "Specialized for SQL generation and database queries",
        "ram_required": "~4.5GB",
        "use_cases": ["text-to-sql", "query generation", "database operations"]
    },
    "fast": {
        "name": "phi3:mini",
        "description": "Lightweight, fast responses",
        "ram_required": "~2.3GB",
        "use_cases": ["quick tasks", "simple analysis", "low-latency needs"]
    }
}


def get_recommended_model_names():
    """Get list of recommended model names to pull."""
    return [model["name"] for model in RECOMMENDED_MODELS.values()]


def get_model_info(model_name):
    """Get information about a recommended model."""
    for category, info in RECOMMENDED_MODELS.items():
        if info["name"] == model_name:
            return {**info, "category": category}
    return None


def print_model_recommendations():
    """Print formatted table of model recommendations."""
    print("\nRecommended Models for 16GB M3 Mac:")
    print("-" * 70)
    print(f"{'Task':<12} {'Model':<20} {'RAM':<10} {'Use Cases'}")
    print("-" * 70)

    for category, info in RECOMMENDED_MODELS.items():
        use_cases = ", ".join(info["use_cases"][:2])  # Show first 2 use cases
        print(f"{category.capitalize():<12} {info['name']:<20} {info['ram_required']:<10} {use_cases}")
    print("-" * 70)
