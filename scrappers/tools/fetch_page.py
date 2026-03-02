"""Lightweight page fetching with requests + BeautifulSoup."""
import requests
from bs4 import BeautifulSoup
import logging
import json
import re

logger = logging.getLogger(__name__)


def _clean_text(soup: BeautifulSoup) -> str:
    """Extract clean text from parsed HTML."""
    # Remove script, style, nav, footer, header elements
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    # Collapse multiple whitespace/newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def fetch_page(url: str, extract_mode: str = "text") -> str:
    """
    Fetch a web page using requests and extract content with BeautifulSoup.

    Best for static pages, articles, documentation. Falls back gracefully
    if the page requires JavaScript.

    Args:
        url: The URL to fetch
        extract_mode: "text" for clean text, "html" for raw HTML, "summary" for title+meta+preview

    Returns:
        Extracted page content as string
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        if extract_mode == "html":
            return response.text[:8000]

        if extract_mode == "summary":
            title = soup.title.string if soup.title else "No title"
            meta_desc = ""
            meta_tag = soup.find("meta", attrs={"name": "description"})
            if meta_tag:
                meta_desc = meta_tag.get("content", "")
            paragraphs = [p.get_text().strip() for p in soup.find_all("p")[:5]]
            return json.dumps({
                "title": title,
                "description": meta_desc,
                "url": url,
                "content_preview": "\n".join(paragraphs)
            }, indent=2)

        # Default: clean text extraction
        text = _clean_text(soup)

        # Truncate for LLM context
        if len(text) > 6000:
            text = text[:6000] + "\n... [content truncated]"

        return text

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return json.dumps({"error": f"Failed to fetch page: {str(e)}", "url": url})
