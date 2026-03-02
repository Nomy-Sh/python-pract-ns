"""Browser-based page fetching using Selenium for JS-heavy sites."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser_manager import BrowserManager
from bs4 import BeautifulSoup
import logging
import json
import time
import re

logger = logging.getLogger(__name__)

# Shared browser instance (lazy-initialized)
_browser_manager = None
_driver = None


def _get_driver():
    """Get or create the shared browser instance."""
    global _browser_manager, _driver
    if _driver is None:
        _browser_manager = BrowserManager(headless=True)
        _driver = _browser_manager.start_browser()
    return _driver


def _clean_text(html: str) -> str:
    """Extract clean text from HTML."""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def browse_page(url: str, wait_seconds: int = 3) -> str:
    """
    Open a URL in a headless browser and extract content after JavaScript renders.

    Use this for JavaScript-heavy sites, SPAs, or pages that require dynamic loading.
    This is slower than fetch_page but handles JS rendering.

    Args:
        url: The URL to browse
        wait_seconds: Seconds to wait for JS to render (default 3)

    Returns:
        Extracted page content as string
    """
    try:
        driver = _get_driver()
        driver.get(url)
        time.sleep(wait_seconds)

        page_source = driver.page_source
        text = _clean_text(page_source)

        if len(text) > 6000:
            text = text[:6000] + "\n... [content truncated]"

        return text

    except Exception as e:
        logger.error(f"Failed to browse {url}: {e}")
        return json.dumps({"error": f"Failed to browse page: {str(e)}", "url": url})


def shutdown_browser():
    """Clean up the shared browser instance."""
    global _browser_manager, _driver
    if _browser_manager:
        _browser_manager.close_browser()
        _browser_manager = None
        _driver = None
