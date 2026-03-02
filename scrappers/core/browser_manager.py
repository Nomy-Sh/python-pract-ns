"""
Browser Manager - Handles browser initialization and management
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser instances and provides utilities for browser operations"""

    def __init__(self, headless=False, existing_session=False):
        """
        Initialize browser manager

        Args:
            headless: Run browser in headless mode
            existing_session: Connect to existing browser session
        """
        self.headless = headless
        self.existing_session = existing_session
        self.driver = None

    def start_browser(self, user_data_dir=None, profile_directory=None):
        """
        Start a new browser instance or connect to existing one

        Args:
            user_data_dir: Path to Chrome user data directory (for persistent sessions)
            profile_directory: Specific profile to use (e.g., 'Default', 'Profile 1')
        """
        try:
            options = Options()

            if self.headless:
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')

            # Useful options for scraping
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # Connect to existing profile if specified
            if user_data_dir:
                options.add_argument(f'--user-data-dir={user_data_dir}')
            if profile_directory:
                options.add_argument(f'--profile-directory={profile_directory}')

            # Start browser
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

            # Remove webdriver flag
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            logger.info("Browser started successfully")
            return self.driver

        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise

    def connect_to_existing_tab(self, url_pattern=None):
        """
        Connect to an already open tab by URL pattern

        Args:
            url_pattern: Part of URL to match (e.g., 'example.com')
        """
        if not self.driver:
            raise Exception("Browser not started. Call start_browser() first")

        original_window = self.driver.current_window_handle

        for window_handle in self.driver.window_handles:
            self.driver.switch_to.window(window_handle)
            current_url = self.driver.current_url

            if url_pattern and url_pattern in current_url:
                logger.info(f"Connected to existing tab: {current_url}")
                return True

        # If not found, switch back to original
        self.driver.switch_to.window(original_window)
        logger.warning(f"No tab found matching pattern: {url_pattern}")
        return False

    def open_new_tab(self, url):
        """Open a new tab with the specified URL"""
        if not self.driver:
            raise Exception("Browser not started. Call start_browser() first")

        self.driver.execute_script(f"window.open('{url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        logger.info(f"Opened new tab: {url}")

    def close_browser(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
