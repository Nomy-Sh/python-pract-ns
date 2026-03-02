"""
Agent tools for web search, scraping, browsing, and data analysis.

Usage:
    from tools import get_default_tools

    tools = get_default_tools()
    agent = Agent(tools=tools)
"""
from local_llm.agent import Tool
from typing import List
import logging

logger = logging.getLogger(__name__)


def _make_tool(name: str, description: str, parameters: dict, function, requires_browser: bool = False) -> Tool:
    """Create a Tool from parameters."""
    return Tool(
        name=name,
        description=description,
        parameters=parameters,
        function=function,
        requires_browser=requires_browser,
    )


def get_default_tools(
    include_browser_tools: bool = True,
    include_copart: bool = False,
) -> List[Tool]:
    """
    Get the default set of agent tools.

    Args:
        include_browser_tools: Include Selenium-based tools (browse_page)
        include_copart: Include the Copart query tool (requires manual login)

    Returns:
        List of Tool objects ready for the Agent
    """
    tools = []

    # Always include lightweight tools
    from .web_search import web_search
    from .fetch_page import fetch_page
    from .extract_links import extract_links
    from .analyze_data import analyze_data

    tools.append(_make_tool(
        name="web_search",
        description="Search the web using DuckDuckGo when the user explicitly asks to search OR when you need very recent/current information you don't have. Returns titles, URLs, and snippets.",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum results to return (default 5, max 10)",
                    "default": 5
                }
            },
            "required": ["query"]
        },
        function=web_search,
    ))

    tools.append(_make_tool(
        name="fetch_page",
        description="Fetch a web page and extract its text content. Best for articles, documentation, and static pages. Use browse_page instead for JavaScript-heavy sites.",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch"
                },
                "extract_mode": {
                    "type": "string",
                    "description": "How to extract: 'text' (default), 'html', or 'summary'",
                    "default": "text"
                }
            },
            "required": ["url"]
        },
        function=fetch_page,
    ))

    tools.append(_make_tool(
        name="extract_links",
        description="Extract all links from a web page. Useful for finding specific pages, navigation, or discovering content on a site.",
        parameters={
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to extract links from"
                },
                "filter_pattern": {
                    "type": "string",
                    "description": "Optional keyword to filter links",
                    "default": ""
                }
            },
            "required": ["url"]
        },
        function=extract_links,
    ))

    tools.append(_make_tool(
        name="analyze_data",
        description="Analyze data (JSON, CSV, or text) and answer questions about it. Good for summarizing, finding patterns, or comparing values.",
        parameters={
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "The data to analyze"
                },
                "question": {
                    "type": "string",
                    "description": "Question to answer about the data"
                }
            },
            "required": ["data", "question"]
        },
        function=analyze_data,
    ))

    if include_browser_tools:
        from .browse_page import browse_page
        tools.append(_make_tool(
            name="browse_page",
            description="Open a URL in a headless browser with JavaScript support. Use for JS-heavy sites, SPAs, or dynamically loaded content. Slower than fetch_page.",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to browse"
                    },
                    "wait_seconds": {
                        "type": "integer",
                        "description": "Seconds to wait for JS rendering (default 3)",
                        "default": 3
                    }
                },
                "required": ["url"]
            },
            function=browse_page,
            requires_browser=True,
        ))

    if include_copart:
        from .query_copart import query_copart
        tools.append(_make_tool(
            name="query_copart",
            description="Query the Copart data portal using natural language. Converts to SQL and executes. Requires manual login.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query about Copart data"
                    },
                    "database_name": {
                        "type": "string",
                        "description": "Specific database to select (optional)"
                    }
                },
                "required": ["query"]
            },
            function=query_copart,
            requires_browser=True,
        ))

    logger.info(f"Loaded {len(tools)} tools: {[t.name for t in tools]}")
    return tools
