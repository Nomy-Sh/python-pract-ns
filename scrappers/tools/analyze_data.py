"""Data analysis tool using the local LLM."""
from local_llm import OllamaClient
import logging

logger = logging.getLogger(__name__)


def analyze_data(data: str, question: str) -> str:
    """
    Analyze data and answer questions about it using the local LLM.

    Args:
        data: Data to analyze (JSON string, CSV text, or any text format)
        question: Question to answer about the data

    Returns:
        Analysis result as string
    """
    try:
        client = OllamaClient()
        analysis = client.analyze_query_results(
            data=data,
            question=question,
        )
        return analysis

    except Exception as e:
        logger.error(f"Data analysis failed: {e}")
        return f"Error analyzing data: {str(e)}"
