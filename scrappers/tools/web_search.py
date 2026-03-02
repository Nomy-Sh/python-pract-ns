"""Web search tool using DuckDuckGo."""
import logging
import json
import ssl
import urllib3

logger = logging.getLogger(__name__)

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        JSON string of search results with title, url, snippet
    """
    try:
        # Ensure max_results is an integer (sometimes comes as string from tool call)
        max_results = int(max_results) if max_results else 5
        max_results = min(max_results, 10)  # Cap at 10
        # Try newer ddgs package first, fallback to old duckduckgo_search
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS

        # Configure SSL context to handle certificate issues
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

        results = []
        # Use DDGS with default settings for better compatibility
        with DDGS() as ddgs:
            # ddgs.text() handles timeout internally
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })

        if not results:
            return json.dumps({"message": f"No results found for: {query}"})

        return json.dumps(results, indent=2)

    except ImportError as e:
        error_msg = "DuckDuckGo search library not available. Install with: pip install ddgs"
        logger.error(error_msg)
        return json.dumps({"error": error_msg})
    except TimeoutError as e:
        error_msg = f"Search timed out for query: {query}. Please try again."
        logger.error(f"Timeout: {e}")
        return json.dumps({"error": error_msg})
    except Exception as e:
        error_msg = f"Search failed: {str(e)}. This may be due to network connectivity issues."
        logger.error(f"Web search failed: {e}", exc_info=True)
        return json.dumps({"error": error_msg, "query": query})
