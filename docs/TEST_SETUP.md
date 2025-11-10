# Test Setup Instructions

## Prerequisites

### 1. Set up SERPAPI_KEY

The test suite requires a valid SERPAPI_KEY to run integration tests. 

#### Option 1: Create .env file (Recommended)
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your SERPAPI_KEY
# .env
SERPAPI_KEY="your_actual_serpapi_key_here"
```

#### Option 2: Set environment variable
```bash
export SERPAPI_KEY="your_actual_serpapi_key_here"
```

#### Get a SERPAPI_KEY
1. Visit https://serpapi.com/
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Add it to your .env file

### 2. Install Dependencies
```bash
# Install all dependencies
pip install -r requirements.txt

# Or use the virtual environment
source .venv/bin/activate
pip install -e .
```

## Running Tests

### All Tests
```bash
# Run all tests
python -m pytest tests/ -v

# Or use the test runner
python run_all_tests.py
```

### Specific Test Files
```bash
# Tool delegation tests (requires SERPAPI_KEY)
python -m pytest tests/test_tool_fix.py -v
python -m pytest tests/test_all_tools.py -v
python -m pytest tests/verify_fix.py -v

# Unit tests (no API key needed)
python -m pytest tests/test_cli_handlers.py -v
python -m pytest tests/test_config.py -v
python -m pytest tests/test_pid_lifecycle.py -v
```

### Skipping API Tests
If you don't have a SERPAPI_KEY, the integration tests will be automatically skipped:
```bash
# Tests will skip with message:
# "SERPAPI_KEY not found in environment. Please set it in .env file."
```

## Security Notes

- ⚠️ **Never commit your .env file** to version control
- ✅ The .env file is already in .gitignore
- ✅ Use .env.example as a template (safe to commit)
- ✅ All test files now use environment variables instead of hardcoded keys

## Troubleshooting

### Test Fails with "SERPAPI_KEY not found"
```bash
# Make sure .env file exists and contains the key
cat .env

# Or set it directly
export SERPAPI_KEY="your_key_here"
python -m pytest tests/test_tool_fix.py -v
```

### Tests are Skipped
This is normal behavior when SERPAPI_KEY is not available. Unit tests will still run.

### API Rate Limits
If you hit rate limits:
- Free tier has limited requests per month
- Tests may fail with rate limit errors
- Wait or upgrade your SERPAPI account

