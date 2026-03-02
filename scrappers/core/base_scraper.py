"""
Base Scraper - Parent class for all site-specific scrapers
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

logger = logging.getLogger(__name__)


class BaseScraper:
    """Base class with common scraping utilities"""

    def __init__(self, driver, config=None):
        """
        Initialize base scraper

        Args:
            driver: Selenium WebDriver instance
            config: Site-specific configuration dict
        """
        self.driver = driver
        self.config = config or {}
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, url):
        """Navigate to a URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        time.sleep(1)  # Brief pause for page to start loading

    def wait_for_element(self, by, value, timeout=10):
        """
        Wait for an element to be present

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found, None if not found
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Element not found: {by}={value}")
            return None

    def wait_for_clickable(self, by, value, timeout=10):
        """
        Wait for an element to be clickable

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found and clickable, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.warning(f"Element not clickable: {by}={value}")
            return None

    def check_if_button_exists(self, by, value, timeout=5):
        """
        Check if a button/element exists without throwing error

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Time to wait

        Returns:
            True if exists, False otherwise
        """
        element = self.wait_for_element(by, value, timeout)
        return element is not None

    def click_button(self, by, value, timeout=10):
        """
        Click a button with multiple fallback methods

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time

        Returns:
            True if clicked, False otherwise
        """
        try:
            element = self.wait_for_clickable(by, value, timeout)
            if element:
                try:
                    element.click()
                    logger.info(f"Clicked element: {value}")
                    return True
                except:
                    # Fallback to JavaScript click
                    self.driver.execute_script("arguments[0].click();", element)
                    logger.info(f"Clicked element via JS: {value}")
                    return True
        except Exception as e:
            logger.error(f"Failed to click element {value}: {e}")
        return False

    def extract_text(self, by, value, timeout=5):
        """
        Extract text from an element

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time

        Returns:
            Text content or None
        """
        element = self.wait_for_element(by, value, timeout)
        if element:
            return element.text.strip()
        return None

    def extract_multiple_texts(self, by, value, timeout=5):
        """
        Extract text from multiple matching elements

        Args:
            by: Selenium By locator type
            value: Locator value
            timeout: Maximum wait time

        Returns:
            List of text contents
        """
        try:
            elements = self.driver.find_elements(by, value)
            return [el.text.strip() for el in elements if el.text.strip()]
        except Exception as e:
            logger.error(f"Failed to extract multiple texts: {e}")
            return []

    def fill_input(self, by, value, text, clear_first=True):
        """
        Fill an input field

        Args:
            by: Selenium By locator type
            value: Locator value
            text: Text to input
            clear_first: Clear field before typing

        Returns:
            True if successful, False otherwise
        """
        try:
            element = self.wait_for_element(by, value)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logger.info(f"Filled input: {value}")
                return True
        except Exception as e:
            logger.error(f"Failed to fill input {value}: {e}")
        return False

    def get_page_content(self):
        """Get the full page content as text"""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def take_screenshot(self, filename):
        """Take a screenshot of current page"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return False

    def execute_custom_js(self, script):
        """Execute custom JavaScript"""
        return self.driver.execute_script(script)

    def make_decision(self, page_content, rules):
        """
        Make a decision based on page content

        Args:
            page_content: Text content to analyze
            rules: Dict of condition->action mappings

        Returns:
            Action to take based on rules
        """
        for condition, action in rules.items():
            if condition.lower() in page_content.lower():
                logger.info(f"Condition met: {condition} -> {action}")
                return action
        return None

    def run(self):
        """Override this method in child classes with site-specific logic"""
        raise NotImplementedError("Subclasses must implement run() method")
