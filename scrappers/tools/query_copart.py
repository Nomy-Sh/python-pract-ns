"""Copart database query tool wrapping the existing DBPortalScraper."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.browser_manager import BrowserManager
from scrapers.db_portal_scraper import DBPortalScraper
import logging
import json

logger = logging.getLogger(__name__)


def query_copart(query: str, database_name: str = None) -> str:
    """
    Execute a natural language query against the Copart data portal.

    Note: This requires a browser session. The user will need to manually
    login to the Copart portal when prompted.

    Args:
        query: Natural language query (e.g., "show all Toyota vehicles from 2023")
        database_name: Specific database to select (optional)

    Returns:
        JSON string with query results or status
    """
    browser = None
    try:
        browser = BrowserManager(headless=False)  # Must be visible for login
        driver = browser.start_browser()

        scraper = DBPortalScraper(driver, use_llm=True)
        result = scraper.run(
            natural_language_query=query,
            database_name=database_name,
        )

        return json.dumps(result, default=str, indent=2)

    except Exception as e:
        logger.error(f"Copart query failed: {e}")
        return json.dumps({"status": "error", "message": str(e)})

    finally:
        if browser:
            browser.close_browser()
