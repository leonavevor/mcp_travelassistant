# Runtime Configuration Module

The `config.py` module provides centralized configuration management for the MCP Travel Planner application with multi-source support and proper precedence handling.

## Features

- **Multi-source configuration loading** with clear precedence
- **Type conversion** for common types (bool, int, float)
- **Lazy loading** - configuration is loaded on first access
- **Reloadable** - can reload configuration at runtime
- **Safe export** - can export configuration with sensitive values masked
- **Global singleton** - single configuration instance across the application
- **Optional dependencies** - gracefully handles missing PyYAML or python-dotenv

## Configuration Precedence

Configuration is loaded from multiple sources in the following order (highest to lowest priority):

1. **Environment variables** (highest priority)
2. **.env file**
3. **runtime_config.yaml file**
4. **Default values** (lowest priority)

This means an environment variable will always override a value from a .env file, which will override a value from runtime_config.yaml, which will override the default value.

## Quick Start

### Basic Usage

```python
from py_mcp_travelplanner.config import get_config

# Get the global config instance
config = get_config()

# Get configuration values
host = config.get('CONTROL_SERVER_HOST')  # Returns: '127.0.0.1'
port = config.get('CONTROL_SERVER_PORT')  # Returns: 8787

# Get with custom default
timeout = config.get('CUSTOM_TIMEOUT', default=60)

# Check if a key exists
if config.has('SERPAPI_KEY'):
    print("API key is configured")
```

### Getting API Keys

```python
from py_mcp_travelplanner.config import get_api_key

# Convenient method for getting API keys
api_key = get_api_key('SERPAPI_KEY')
if api_key:
    print(f"API key configured: {api_key[:8]}...")
else:
    print("API key not configured")
```

### Setting Values at Runtime

```python
from py_mcp_travelplanner.config import get_config

config = get_config()

# Set a value (only affects in-memory config, not files)
config.set('DEBUG_MODE', True)

# Reload from sources
config.reload()
```

## Configuration Files

### runtime_config.yaml

Create a `runtime_config.yaml` file in your project root:

```yaml
# Server Configuration
CONTROL_SERVER_HOST: "0.0.0.0"
CONTROL_SERVER_PORT: 9000
MCP_SERVER_NAME: "my_custom_server"

# Logging
LOG_LEVEL: "DEBUG"

# API Keys
SERPAPI_KEY: "your_api_key_here"

# Feature Flags
ENABLE_AUTO_DISCOVERY: true
DEBUG_MODE: false

# Nested configuration for specific servers
FLIGHT_SERVER:
  MAX_RESULTS: 20
  CACHE_TTL: 3600
```

### .env File

Create a `.env` file in your project root:

```bash
# Server Configuration
CONTROL_SERVER_HOST=localhost
CONTROL_SERVER_PORT=8787

# API Keys
SERPAPI_KEY=your_serpapi_key_here

# Logging
LOG_LEVEL=INFO
```

### Environment Variables

Set environment variables to override all other sources:

```bash
export CONTROL_SERVER_PORT=9999
export LOG_LEVEL=DEBUG
export SERPAPI_KEY=your_key_here
```

## Default Configuration Values

The following default values are built into the config module:

```python
{
    # Server Configuration
    'CONTROL_SERVER_HOST': '127.0.0.1',
    'CONTROL_SERVER_PORT': 8787,
    'MCP_SERVER_NAME': 'py_mcp_travelplanner_unified',
    
    # Logging Configuration
    'LOG_LEVEL': 'INFO',
    'LOG_FORMAT': '%(levelname)s:%(name)s: %(message)s',
    
    # Server Process Management
    'SERVER_START_TIMEOUT': 30.0,
    'SERVER_STOP_TIMEOUT': 5.0,
    'HEALTH_CHECK_INTERVAL': 10.0,
    
    # API Keys
    'SERPAPI_KEY': None,
    
    # Server Discovery
    'SERVERS_DIR': None,  # Auto-detected if None
    'ENABLE_AUTO_DISCOVERY': True,
    
    # Development/Debug
    'DRY_RUN': False,
    'VERBOSE': False,
    'DEBUG_MODE': False,
    
    # PID File Management
    'PID_FILE_DIR': '.mcp_pids',
    'ENABLE_PID_TRACKING': True,
}
```

## Advanced Usage

### Custom Configuration Paths

```python
from py_mcp_travelplanner.config import RuntimeConfig

# Use custom paths
config = RuntimeConfig(
    config_path='/path/to/custom_config.yaml',
    env_file='/path/to/custom.env',
    auto_load=True
)
```

### Exporting Configuration

```python
from py_mcp_travelplanner.config import get_config

config = get_config()

# Export all configuration (masks sensitive values)
safe_config = config.to_dict(include_sensitive=False)
print(safe_config)
# Output: {'SERPAPI_KEY': '***REDACTED***', ...}

# Export with sensitive values
full_config = config.to_dict(include_sensitive=True)
print(full_config)
# Output: {'SERPAPI_KEY': 'actual_key_value', ...}
```

### Type Conversion

The config module automatically converts string values to appropriate types based on default values:

```python
# Boolean conversion
config.get('ENABLE_AUTO_DISCOVERY')  # Returns True (bool)
# Accepts: 'true', '1', 'yes', 'on' -> True
# Accepts: 'false', '0', 'no', 'off' -> False

# Integer conversion
config.get('CONTROL_SERVER_PORT')  # Returns 8787 (int)

# Float conversion
config.get('SERVER_START_TIMEOUT')  # Returns 30.0 (float)
```

### Testing with Config

```python
import pytest
from py_mcp_travelplanner.config import get_config, reset_config

@pytest.fixture
def clean_config():
    """Reset config before and after test."""
    reset_config()
    yield
    reset_config()

def test_my_feature(clean_config):
    config = get_config()
    config.set('DEBUG_MODE', True)
    # ... test code ...
```

## Environment Variables

The following environment variables control config file locations:

- `MCP_CONFIG_PATH`: Path to runtime_config.yaml (default: `./runtime_config.yaml`)
- `MCP_ENV_FILE`: Path to .env file (default: `./.env`)

Example:

```bash
export MCP_CONFIG_PATH=/etc/mcp/config.yaml
export MCP_ENV_FILE=/etc/mcp/.env
```

## API Reference

### `get_config(reload: bool = False) -> RuntimeConfig`

Get the global configuration instance.

**Parameters:**
- `reload` (bool): If True, reload configuration from all sources

**Returns:**
- RuntimeConfig: The global configuration instance

### `reset_config() -> None`

Reset the global configuration instance. Primarily useful for testing.

### `get_api_key(key_name: str) -> Optional[str]`

Get an API key from configuration.

**Parameters:**
- `key_name` (str): Name of the API key (e.g., 'SERPAPI_KEY')

**Returns:**
- str | None: API key value or None if not set

### `RuntimeConfig` Class

#### Methods

- `get(key: str, default: Any = None) -> Any`: Get a configuration value
- `set(key: str, value: Any) -> None`: Set a configuration value at runtime
- `has(key: str) -> bool`: Check if a configuration key exists
- `get_all() -> Dict[str, Any]`: Get all configuration values as a dictionary
- `reload() -> None`: Reload configuration from all sources
- `to_dict(include_sensitive: bool = False) -> Dict[str, Any]`: Export configuration as dictionary

## Examples

See `examples/config_example.py` for a complete working example.

Run it with:

```bash
cd /path/to/mcp_travelplanner
PYTHONPATH=. python examples/config_example.py
```

## Testing

The config module includes comprehensive tests covering:

- Default values
- YAML file loading
- .env file loading
- Environment variable precedence
- Type conversion
- Configuration methods
- Edge cases and error handling
- Integration scenarios

Run the tests:

```bash
pytest tests/test_config.py -v
```

## Dependencies

- **Required**: None (uses standard library only for basic functionality)
- **Optional**:
  - `pyyaml>=6.0.1` - For YAML config file support
  - `python-dotenv>=1.1.0` - For enhanced .env file parsing

If optional dependencies are not installed, the config module will:
- Skip YAML file loading (if PyYAML not installed)
- Fall back to simple .env parsing (if python-dotenv not installed)

## Best Practices

1. **Use environment variables for secrets** - Don't commit API keys to version control
2. **Use runtime_config.yaml for defaults** - Good for team-wide defaults
3. **Use .env for local overrides** - Good for developer-specific settings
4. **Check config exists before use** - Use `config.has()` to check if a key is set
5. **Use get_api_key() for API keys** - Convenient and consistent
6. **Reset config in tests** - Always use `reset_config()` in test fixtures

## Troubleshooting

### Configuration not loading

Check the logs - the config module logs when it loads configuration:

```
INFO:py_mcp_travelplanner.config: Loaded configuration from /path/to/runtime_config.yaml
INFO:py_mcp_travelplanner.config: Loaded configuration from /path/to/.env
INFO:py_mcp_travelplanner.config: Logging configured: level=INFO
INFO:py_mcp_travelplanner.config: Runtime configuration loaded successfully
```

### Wrong value returned

Remember the precedence order:
1. Environment variables (highest)
2. .env file
3. YAML file
4. Defaults (lowest)

Check if a higher-priority source is setting the value.

### Type conversion issues

If a value isn't being converted to the expected type, ensure:
1. The key exists in the defaults dictionary (in `config.py`)
2. The default value has the correct type
3. The string value can be converted to that type

## License

MIT License - See LICENSE file for details.

