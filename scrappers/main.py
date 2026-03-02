"""
Main entry point for running scrapers
"""
import argparse
import logging
from core.browser_manager import BrowserManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_scraper(scraper_name, headless=False, query=None, database=None, **kwargs):
    """
    Run a specific scraper

    Args:
        scraper_name: Name of the scraper to run
        headless: Run browser in headless mode
        query: Natural language query for data extraction
        database: Database name to select
        **kwargs: Additional arguments for the scraper
    """
    browser = BrowserManager(headless=headless)

    try:
        driver = browser.start_browser()

        # Import and run the appropriate scraper
        if scraper_name == 'db_portal' or scraper_name == 'copart':
            from scrapers.db_portal_scraper import DBPortalScraper
            scraper = DBPortalScraper(driver)
            result = scraper.run(
                natural_language_query=query,
                database_name=database
            )
            logger.info(f"Scraper result: {result}")

            # Pretty print results
            if result.get('status') == 'success' and result.get('data'):
                print("\n" + "="*60)
                print("📊 QUERY RESULTS")
                print("="*60)
                print(f"Query: {result.get('query', 'N/A')}")
                print(f"SQL: {result.get('sql', 'N/A')}")
                print("\nData:")

                data = result['data']
                if isinstance(data, list) and len(data) > 0:
                    import pandas as pd
                    df = pd.DataFrame(data)
                    print(df.to_string())
                    print(f"\n✅ Total rows: {len(data)}")
                else:
                    print(data)
                print("="*60 + "\n")

        # Add more scrapers here as you create them
        # elif scraper_name == 'site2':
        #     from scrapers.site2_scraper import Site2Scraper
        #     scraper = Site2Scraper(driver)
        #     result = scraper.run()

        else:
            logger.error(f"Unknown scraper: {scraper_name}")
            logger.info("Available scrapers: db_portal (copart)")
            return None

        return result

    except Exception as e:
        logger.error(f"Error running scraper: {e}", exc_info=True)
        return None

    finally:
        # Keep browser open if not headless (for debugging)
        if headless:
            browser.close_browser()
        else:
            logger.info("Browser left open for inspection. Close manually when done.")


def main():
    parser = argparse.ArgumentParser(description='Run web scrapers')
    parser.add_argument('scraper', help='Name of the scraper to run (e.g., db_portal, copart)')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    parser.add_argument('--query', '-q', help='Natural language query (e.g., "show all Toyotas sold last month")')
    parser.add_argument('--database', '-db', help='Database name to select')
    parser.add_argument('--schedule', help='Schedule to run (e.g., "10:30" for daily at 10:30 AM)')

    args = parser.parse_args()

    if args.schedule:
        import schedule
        import time

        logger.info(f"Scheduling {args.scraper} to run daily at {args.schedule}")
        schedule.every().day.at(args.schedule).do(
            run_scraper, args.scraper, args.headless, args.query, args.database
        )

        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        # Run immediately
        run_scraper(args.scraper, args.headless, args.query, args.database)


if __name__ == '__main__':
    main()
