# Copart Data Portal Scraper Usage Guide

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API key:**
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

Get your API key from: https://console.anthropic.com/

3. **Update schema (optional but recommended):**
Edit `configs/copart_schema.txt` with actual table/column names from Copart portal for better SQL generation.

## Usage Examples

### Basic Usage (Manual Login)
```bash
python main.py copart --query "show me all vehicles"
```

**What happens:**
1. Opens browser to https://data.copart.com/
2. Waits for you to manually login
3. Automatically detects when login is complete
4. Proceeds with your query

### With Database Selection
```bash
python main.py copart --database "production" --query "find all Toyotas from last month"
```

### Advanced Queries
```bash
# Find specific data
python main.py copart -q "show all vehicles sold for more than $10000"

# Date-based queries
python main.py copart -q "get sales data from January 2024"

# Complex queries
python main.py copart -q "find all damaged Honda Accords in California yards"
```

### Scheduled Execution
```bash
# Run daily at 9:30 AM
python main.py copart --query "daily sales report" --schedule "09:30"
```

## How It Works

### 1. Login Handling
- Script opens browser and navigates to Copart portal
- **You manually login** (the script waits and watches)
- Once login detected, automation continues
- Timeout: 5 minutes (configurable in code)

### 2. Natural Language to SQL
Uses Claude AI to convert your query:
- **Input:** "show me all Toyotas sold last month"
- **Output:** `SELECT * FROM vehicles WHERE make = 'Toyota' AND sale_date >= DATE_SUB(NOW(), INTERVAL 1 MONTH)`

### 3. Database Selection
- Auto-detects database dropdown
- Selects specified database or prompts you to select manually
- Falls back to manual selection if needed

### 4. Query Execution
- Finds SQL query input box
- Pastes generated SQL
- Clicks execute button (or uses keyboard shortcut)
- Waits for results

### 5. Data Extraction
- Extracts results table
- Converts to pandas DataFrame
- Returns structured data
- Pretty prints in terminal

## Customization

### Update Schema Info
Edit `configs/copart_schema.txt` with actual database structure:
```
Tables:
- vehicles: vin, make, model, year, location_id, sale_date, sale_price
- locations: id, yard_name, city, state
```

Better schema = better SQL generation!

### Adjust Selectors
If portal UI changes, update selectors in `scrapers/db_portal_scraper.py`:
```python
query_selectors = [
    (By.ID, "your-actual-id"),
    (By.XPATH, "//your-xpath"),
]
```

### Change Login Timeout
In `db_portal_scraper.py`:
```python
def wait_for_user_login(self, timeout=300):  # 300 seconds = 5 minutes
```

## Troubleshooting

### "Could not find query input box"
- Script will prompt you to manually paste query
- Update `query_selectors` in code with correct selectors

### "Could not find database selector"
- Script prompts for manual selection
- Update `database_selectors` in code

### "Login timeout"
- Login faster (default 5 min timeout)
- Or increase timeout in code

### SQL Generation Issues
- Update `configs/copart_schema.txt` with better schema info
- LLM needs table/column names to generate accurate queries

### API Key Error
- Make sure `ANTHROPIC_API_KEY` is set in `.env` file
- Or export it: `export ANTHROPIC_API_KEY=your_key`

## Example Workflow

```bash
# 1. First time - explore database
python main.py copart

# When portal opens:
# - Login manually
# - Explore available databases and tables
# - Update configs/copart_schema.txt

# 2. Run queries
python main.py copart -q "show me table structure" -db "production"
python main.py copart -q "get last 100 sales"

# 3. Schedule daily reports
python main.py copart -q "daily inventory report" --schedule "08:00"
```

## Output

Results are displayed in terminal and returned as:
```python
{
    "status": "success",
    "query": "show all Toyotas",
    "sql": "SELECT * FROM vehicles WHERE make = 'Toyota'",
    "data": [
        {"vin": "123", "make": "Toyota", "model": "Camry", ...},
        ...
    ]
}
```

## Next Steps

1. Explore Copart portal structure
2. Update schema file for better queries
3. Test with simple queries first
4. Build up to complex scheduled automation
