"""Extract links from a web page."""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import json

logger = logging.getLogger(__name__)


def extract_links(url: str, filter_pattern: str = "") -> str:
    """
    Extract all links from a web page.

    Args:
        url: The URL to extract links from
        filter_pattern: Optional substring to filter links

    Returns:
        JSON list of {text, url} objects
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        links = []

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)

            # Resolve relative URLs
            full_url = urljoin(url, href)

            # Skip anchors, javascript, mailto
            if full_url.startswith(("javascript:", "mailto:", "#")):
                continue

            # Apply filter
            if filter_pattern:
                if filter_pattern.lower() not in text.lower() and filter_pattern.lower() not in full_url.lower():
                    continue

            links.append({"text": text or "(no text)", "url": full_url})

        # Deduplicate by URL
        seen = set()
        unique_links = []
        for link in links:
            if link["url"] not in seen:
                seen.add(link["url"])
                unique_links.append(link)

        return json.dumps(unique_links[:50], indent=2)  # Limit to 50 links

    except Exception as e:
        logger.error(f"Failed to extract links from {url}: {e}")
        return json.dumps({"error": f"Failed to extract links: {str(e)}"})
