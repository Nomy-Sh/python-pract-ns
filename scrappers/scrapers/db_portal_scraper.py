"""
Copart Data Portal Scraper - Automated SQL query execution with LLM support
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from core.base_scraper import BaseScraper
from core.llm_helper import LLMHelper
import logging
import time
import os
import pandas as pd

logger = logging.getLogger(__name__)


class DBPortalScraper(BaseScraper):
    """Scraper for Copart Data Portal (https://data.copart.com/)"""

    def __init__(self, driver, use_llm=True):
        super().__init__(driver)
        self.portal_url = "https://data.copart.com/"
        self.llm_helper = LLMHelper() if use_llm else None
        self.schema_info = self._load_schema_info()

    def _load_schema_info(self):
        """Load database schema information for SQL generation"""
        schema_path = os.path.join(
            os.path.dirname(__file__),
            '..', 'configs', 'copart_schema.txt'
        )
        try:
            with open(schema_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Schema file not found, SQL generation may be less accurate")
            return None

    def run(self, natural_language_query=None, database_name=None):
        """
        Main execution flow for Copart data portal

        Args:
            natural_language_query: Human-readable query (e.g., "show all Toyotas sold last month")
            database_name: Specific database to select (optional)

        Returns:
            Dict with scraped data or status
        """
        try:
            logger.info("Starting Copart Data Portal scraper")

            # Navigate to portal
            self.navigate_to(self.portal_url)
            time.sleep(2)

            # Wait for login
            logger.info("⏳ Waiting for you to login...")
            if not self.wait_for_user_login():
                return {"status": "error", "message": "Login timeout or failed"}

            logger.info("✅ Login detected, proceeding...")

            # Select database
            if not self.select_database(database_name):
                return {"status": "error", "message": "Failed to select database"}

            # Generate and execute query
            if natural_language_query:
                if not self.llm_helper:
                    return {
                        "status": "error",
                        "message": "LLM helper not initialized. Ensure Ollama is running and models are installed."
                    }

                sql_query = self.llm_helper.natural_language_to_sql(
                    natural_language_query,
                    self.schema_info
                )
                logger.info(f"📝 Generated SQL: {sql_query}")

                data = self.execute_query(sql_query)

                return {
                    "status": "success",
                    "query": natural_language_query,
                    "sql": sql_query,
                    "data": data
                }
            else:
                return {
                    "status": "success",
                    "message": "Ready for queries. Pass natural_language_query parameter."
                }

        except Exception as e:
            logger.error(f"Error in Copart scraper: {e}", exc_info=True)
            return {"status": "error", "message": str(e)}

    def wait_for_user_login(self, timeout=300):
        """
        Wait for user to manually login
        Detects login by checking if we're past the login page

        Args:
            timeout: Maximum seconds to wait (default 5 minutes)

        Returns:
            True if login detected, False if timeout
        """
        print("\n" + "="*60)
        print("🔐 PLEASE LOGIN TO COPART DATA PORTAL")
        print("="*60)
        print("The browser is open. Please complete the login process.")
        print("The script will automatically continue once logged in.")
        print("="*60 + "\n")

        start_time = time.time()

        while time.time() - start_time < timeout:
            current_url = self.driver.current_url

            # Check if we're past login (adjust these checks based on actual URLs)
            if "login" not in current_url.lower() and "signin" not in current_url.lower():
                # Additional check: look for elements that appear after login
                # Adjust these selectors based on actual portal structure
                if self.check_if_button_exists(By.XPATH, "//*[contains(text(), 'Database') or contains(text(), 'Query') or contains(text(), 'SQL')]", timeout=2):
                    return True

            time.sleep(2)

        logger.error("Login timeout - user did not complete login in time")
        return False

    def select_database(self, database_name=None):
        """
        Select database from the list

        Args:
            database_name: Specific database to select. If None, will try to auto-select or use LLM

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Looking for database selector...")

            # Common selectors for database dropdowns (adjust based on actual portal)
            possible_selectors = [
                (By.ID, "database-select"),
                (By.NAME, "database"),
                (By.XPATH, "//select[contains(@class, 'database')]"),
                (By.XPATH, "//select[contains(@id, 'db')]"),
                (By.XPATH, "//button[contains(text(), 'Select Database')]"),
            ]

            database_element = None
            for by, value in possible_selectors:
                element = self.wait_for_element(by, value, timeout=3)
                if element:
                    database_element = element
                    logger.info(f"Found database selector: {value}")
                    break

            if not database_element:
                # Try to understand the page with LLM
                if self.llm_helper:
                    page_content = self.get_page_content()
                    guidance = self.llm_helper.understand_page_context(
                        page_content,
                        "Where is the database selection dropdown or button? Describe how to select a database."
                    )
                    logger.info(f"LLM guidance: {guidance}")

                logger.warning("Could not find database selector automatically")
                print("\n⚠️  Could not find database selector automatically.")
                print("Please manually select the database in the browser.")
                input("Press Enter once you've selected the database...")
                return True

            # If specific database name provided, select it
            if database_name:
                # Handle dropdown
                if database_element.tag_name == 'select':
                    from selenium.webdriver.support.ui import Select
                    select = Select(database_element)
                    select.select_by_visible_text(database_name)
                    logger.info(f"Selected database: {database_name}")
                else:
                    # Handle button/other element
                    database_element.click()
                    time.sleep(1)
                    # Try to find and click the specific database in a list
                    db_option = self.wait_for_element(
                        By.XPATH,
                        f"//*[contains(text(), '{database_name}')]",
                        timeout=3
                    )
                    if db_option:
                        db_option.click()
                        logger.info(f"Selected database: {database_name}")
            else:
                # Auto-select first available or prompt user
                print("\n💡 Please manually select your desired database.")
                input("Press Enter once selected...")

            return True

        except Exception as e:
            logger.error(f"Error selecting database: {e}")
            return False

    def execute_query(self, sql_query):
        """
        Execute SQL query in the portal

        Args:
            sql_query: SQL query string

        Returns:
            Query results as list of dicts or pandas DataFrame
        """
        try:
            logger.info(f"Executing query: {sql_query}")

            # Find query input box (adjust selectors based on actual portal)
            query_selectors = [
                (By.ID, "query"),
                (By.NAME, "sql"),
                (By.XPATH, "//textarea[contains(@class, 'query')]"),
                (By.XPATH, "//textarea[contains(@placeholder, 'SQL')]"),
                (By.CSS_SELECTOR, "textarea.sql-editor"),
            ]

            query_box = None
            for by, value in query_selectors:
                element = self.wait_for_element(by, value, timeout=3)
                if element:
                    query_box = element
                    logger.info(f"Found query box: {value}")
                    break

            if not query_box:
                logger.error("Could not find query input box")
                print("\n⚠️  Could not find query input box.")
                print("Please manually paste and execute this query:")
                print(f"\n{sql_query}\n")
                input("Press Enter once query is executed...")
                return self.extract_query_results()

            # Enter query
            query_box.clear()
            query_box.send_keys(sql_query)
            time.sleep(0.5)

            # Find and click execute button
            execute_selectors = [
                (By.XPATH, "//button[contains(text(), 'Execute') or contains(text(), 'Run')]"),
                (By.ID, "execute"),
                (By.ID, "run-query"),
                (By.CSS_SELECTOR, "button.execute"),
            ]

            for by, value in execute_selectors:
                if self.click_button(by, value, timeout=2):
                    logger.info("Query executed")
                    break
            else:
                # Fallback: try pressing Ctrl+Enter or Cmd+Enter
                query_box.send_keys(Keys.COMMAND + Keys.RETURN)
                logger.info("Attempted query execution with keyboard shortcut")

            # Wait for results
            time.sleep(3)
            return self.extract_query_results()

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def extract_query_results(self):
        """
        Extract query results from the page

        Returns:
            Results as list of dicts or pandas DataFrame
        """
        try:
            logger.info("Extracting query results...")

            # Try to find results table (adjust selectors based on actual portal)
            table_selectors = [
                (By.XPATH, "//table[contains(@class, 'results')]"),
                (By.CSS_SELECTOR, "table.data-table"),
                (By.XPATH, "//div[contains(@class, 'results')]//table"),
            ]

            table = None
            for by, value in table_selectors:
                element = self.wait_for_element(by, value, timeout=5)
                if element:
                    table = element
                    logger.info("Found results table")
                    break

            if table:
                # Extract using pandas (most robust)
                try:
                    tables = pd.read_html(self.driver.page_source)
                    if tables:
                        df = tables[-1]  # Usually the last table is results
                        logger.info(f"Extracted {len(df)} rows")
                        return df.to_dict('records')
                except:
                    pass

                # Fallback: manual extraction
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) > 1:
                    headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "th")]
                    data = []
                    for row in rows[1:]:
                        cells = [td.text for td in row.find_elements(By.TAG_NAME, "td")]
                        data.append(dict(zip(headers, cells)))
                    logger.info(f"Extracted {len(data)} rows")
                    return data

            logger.warning("Could not extract results automatically")
            return None

        except Exception as e:
            logger.error(f"Error extracting results: {e}")
            return None
