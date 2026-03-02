# Web Scraper & Automation Framework

A flexible Python framework for building web scrapers and automation bots using Selenium.

## Features

- ✅ Open browsers or connect to existing tabs
- ✅ Click buttons and interact with elements
- ✅ Extract data intelligently
- ✅ Make decisions based on page content
- ✅ Support for multiple websites with different structures
- ✅ Run manually or on a schedule
- ✅ Extensible architecture

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run a scraper manually:
```bash
python main.py db_portal
```

3. Run in headless mode:
```bash
python main.py db_portal --headless
```

4. Schedule a scraper:
```bash
python main.py db_portal --schedule "14:30"
```

## Project Structure

```
scrappers/
├── core/                      # Core framework
│   ├── browser_manager.py     # Browser setup & management
│   └── base_scraper.py        # Base class with common utilities
├── scrapers/                  # Site-specific scrapers
│   └── db_portal_scraper.py   # DB Portal scraper
├── main.py                    # Entry point
└── requirements.txt           # Dependencies
```

## Creating a New Scraper

1. Create a new file in `scrapers/` directory
2. Inherit from `BaseScraper`
3. Implement the `run()` method
4. Add it to `main.py`

Example:
```python
from core.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class MyScraper(BaseScraper):
    def run(self):
        self.navigate_to("https://example.com")

        if self.check_if_button_exists(By.ID, "submit-btn"):
            self.click_button(By.ID, "submit-btn")

        data = self.extract_text(By.CLASS_NAME, "result")
        return {"data": data}
```

## Available Methods

### Browser Operations
- `navigate_to(url)` - Navigate to a URL
- `wait_for_element(by, value, timeout)` - Wait for element to appear
- `wait_for_clickable(by, value, timeout)` - Wait for element to be clickable

### Interactions
- `click_button(by, value)` - Click an element with fallback methods
- `fill_input(by, value, text)` - Fill an input field
- `check_if_button_exists(by, value)` - Check if element exists

### Data Extraction
- `extract_text(by, value)` - Extract text from single element
- `extract_multiple_texts(by, value)` - Extract from multiple elements
- `get_page_content()` - Get full page text

### Decision Making
- `make_decision(content, rules)` - Make decisions based on content

### Utilities
- `take_screenshot(filename)` - Save screenshot
- `execute_custom_js(script)` - Run custom JavaScript

## Next Steps

Customize `scrapers/db_portal_scraper.py` with your specific DB portal logic.
