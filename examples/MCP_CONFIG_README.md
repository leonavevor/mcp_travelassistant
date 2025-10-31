# MCP Server Configuration Examples

This directory contains configuration examples for running the MCP Travel Planner server with Claude Desktop or other MCP clients.

## Configuration Files

### 1. `claude_desktop_config_template.json`
Standard configuration for running the MCP server with a local Python installation.

**Use case**: When you have the package installed locally via pip, poetry, or uv.

### 2. `claude_desktop_config_uv_testpypi.json`
Configuration for running the MCP server directly from Test PyPI using `uv run`.

**Use case**: Testing pre-release versions from Test PyPI without installing them.

### 3. `claude_desktop_config_uv_pypi.json`
Configuration for running the MCP server directly from PyPI using `uv run`.

**Use case**: Running the latest stable version without installation.

---

## Installation Methods

### Method 1: Standard Installation (Recommended for Production)

**Install the package:**

```bash
# From PyPI (when published)
pip install py_mcp_travelplanner

# Or with uv
uv pip install py_mcp_travelplanner

# Or from Test PyPI
pip install --index-url https://test.pypi.org/simple/ py_mcp_travelplanner
```

**Claude Desktop Config Location:**

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**

Use the content from `claude_desktop_config_template.json`:

```json
{
  "mcpServers": {
    "py_mcp_travelplanner": {
      "command": "python",
      "args": ["-m", "py_mcp_travelplanner.mcp_server"],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

---

### Method 2: UV Run with Test PyPI (For Testing)

**No installation required!** UV will download and run the package on-demand.

**Configuration:**

Use the content from `claude_desktop_config_uv_testpypi.json`:

```json
{
  "mcpServers": {
    "py_mcp_travelplanner_uv_testpypi": {
      "command": "uv",
      "args": [
        "run",
        "--index",
        "https://test.pypi.org/simple",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

**Command Breakdown:**
- `uv run` - Run a command with UV
- `--index https://test.pypi.org/simple` - Use Test PyPI as package source
- `--with py_mcp_travelplanner` - Download and include this package
- `--no-project` - Don't require a pyproject.toml in current directory
- `--` - Separator between UV args and command args
- `py_mcp_travelplanner_cli` - The command to run (entry point)

**Prerequisites:**
- Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh` (Unix/macOS)
- Or: `pip install uv`

---

### Method 3: UV Run with PyPI (For Latest Stable)

**Configuration:**

Use the content from `claude_desktop_config_uv_pypi.json`:

```json
{
  "mcpServers": {
    "py_mcp_travelplanner_uv": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

---

## Environment Variables Reference

All configuration methods support the following environment variables:

### Required
- `SERPAPI_KEY` - Your SerpAPI key for search functionality (**required**)

### Server Configuration
- `CONTROL_SERVER_HOST` - Server host (default: `127.0.0.1`)
- `CONTROL_SERVER_PORT` - Server port (default: `8787`)
- `MCP_SERVER_NAME` - Server identifier (default: `py_mcp_travelplanner_unified`)

### Logging
- `LOG_LEVEL` - Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`)
- `LOG_FORMAT` - Log message format

### Features
- `ENABLE_AUTO_DISCOVERY` - Auto-discover servers: `true`/`false` (default: `true`)
- `DEBUG_MODE` - Enable debug mode: `true`/`false` (default: `false`)
- `DRY_RUN` - Dry run mode (no actual operations): `true`/`false` (default: `false`)
- `ENABLE_PID_TRACKING` - Track server PIDs: `true`/`false` (default: `true`)

### Server Process Management
- `SERVER_START_TIMEOUT` - Server start timeout in seconds (default: `30.0`)
- `SERVER_STOP_TIMEOUT` - Server stop timeout in seconds (default: `5.0`)
- `HEALTH_CHECK_INTERVAL` - Health check interval in seconds (default: `10.0`)

### Configuration Files
- `MCP_CONFIG_PATH` - Path to runtime_config.yaml (default: `./runtime_config.yaml`)
- `MCP_ENV_FILE` - Path to .env file (default: `./.env`)

---

## Complete Configuration Examples

### Minimal Configuration

```json
{
  "mcpServers": {
    "py_mcp_travelplanner": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

### Full Configuration with All Options

```json
{
  "mcpServers": {
    "py_mcp_travelplanner": {
      "command": "uv",
      "args": [
        "run",
        "--index",
        "https://test.pypi.org/simple",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here",
        "LOG_LEVEL": "DEBUG",
        "CONTROL_SERVER_HOST": "127.0.0.1",
        "CONTROL_SERVER_PORT": "8787",
        "MCP_SERVER_NAME": "py_mcp_travelplanner_unified",
        "ENABLE_AUTO_DISCOVERY": "true",
        "DEBUG_MODE": "true",
        "DRY_RUN": "false",
        "SERVER_START_TIMEOUT": "60.0",
        "SERVER_STOP_TIMEOUT": "10.0",
        "HEALTH_CHECK_INTERVAL": "15.0",
        "ENABLE_PID_TRACKING": "true",
        "MCP_CONFIG_PATH": "/path/to/custom_config.yaml",
        "MCP_ENV_FILE": "/path/to/custom.env"
      }
    }
  }
}
```

### Multiple Server Instances

You can run multiple instances with different configurations:

```json
{
  "mcpServers": {
    "py_mcp_travelplanner_production": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "production_key",
        "LOG_LEVEL": "WARNING",
        "CONTROL_SERVER_PORT": "8787"
      }
    },
    "py_mcp_travelplanner_dev": {
      "command": "uv",
      "args": [
        "run",
        "--index",
        "https://test.pypi.org/simple",
        "--with",
        "py_mcp_travelplanner",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "dev_key",
        "LOG_LEVEL": "DEBUG",
        "CONTROL_SERVER_PORT": "8788",
        "DEBUG_MODE": "true"
      }
    }
  }
}
```

---

## Getting Your SERPAPI Key

1. Visit [https://serpapi.com/](https://serpapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Replace `your_serpapi_key_here` in the config with your actual key

**Free Tier**: 100 searches/month

---

## Testing the Configuration

### Option 1: Test with UV directly

```bash
# Test PyPI
uv run \
  --index https://test.pypi.org/simple \
  --with py_mcp_travelplanner \
  --no-project \
  -- py_mcp_travelplanner_cli list

# Regular PyPI
uv run \
  --with py_mcp_travelplanner \
  --no-project \
  -- py_mcp_travelplanner_cli list
```

### Option 2: Test with Python module

```bash
# After installation
python -m py_mcp_travelplanner.cli list
```

### Option 3: Test with console script

```bash
# After installation
py_mcp_travelplanner_cli list
```

---

## Troubleshooting

### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv
```

### Package Not Found on Test PyPI
- Verify the package name is correct: `py_mcp_travelplanner`
- Check if the version exists on Test PyPI
- Try without `--index` flag to use regular PyPI

### SERPAPI Key Issues
- Ensure the key is correctly set in the `env` section
- Test the key at [https://serpapi.com/manage-api-key](https://serpapi.com/manage-api-key)
- Check you haven't exceeded the free tier limit

### Claude Desktop Not Connecting
1. Check the config file location is correct for your OS
2. Restart Claude Desktop after config changes
3. Check the logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`
   - Linux: `~/.config/Claude/logs/`

### Server Won't Start
- Check all required environment variables are set
- Verify Python is in your PATH
- Check the command and args are correct
- Look for error messages in Claude Desktop logs

---

## Configuration Priority

The system loads configuration in this order (highest to lowest priority):

1. **Environment variables** (set in MCP config `env` section)
2. **.env file** (if MCP_ENV_FILE is set or .env exists)
3. **runtime_config.yaml** (if MCP_CONFIG_PATH is set or runtime_config.yaml exists)
4. **Default values** (built into the application)

---

## Best Practices

### Security
- ✅ Never commit API keys to version control
- ✅ Use environment variables for sensitive data
- ✅ Keep your Claude Desktop config file private

### Performance
- ✅ Use `--no-project` with UV to avoid project detection overhead
- ✅ Set `LOG_LEVEL` to `WARNING` or `ERROR` in production
- ✅ Disable `DEBUG_MODE` in production

### Reliability
- ✅ Pin package versions in production: `--with py_mcp_travelplanner==0.1.5`
- ✅ Use regular PyPI for production, Test PyPI only for testing
- ✅ Set reasonable timeouts for your use case

### Development
- ✅ Use `DEBUG_MODE: true` during development
- ✅ Use `DRY_RUN: true` to test without side effects
- ✅ Use separate server instances for dev/staging/production

---

## Version-Specific Configuration

### Pinning to a Specific Version

```json
{
  "mcpServers": {
    "py_mcp_travelplanner": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "py_mcp_travelplanner==0.1.5",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

### Using Latest Pre-release

```json
{
  "mcpServers": {
    "py_mcp_travelplanner_beta": {
      "command": "uv",
      "args": [
        "run",
        "--index",
        "https://test.pypi.org/simple",
        "--with",
        "py_mcp_travelplanner",
        "--prerelease=allow",
        "--no-project",
        "--",
        "py_mcp_travelplanner_cli"
      ],
      "env": {
        "SERPAPI_KEY": "your_serpapi_key_here"
      }
    }
  }
}
```

---

## Additional Resources

- **UV Documentation**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **MCP Protocol**: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- **Claude Desktop**: [https://claude.ai/download](https://claude.ai/download)
- **SerpAPI**: [https://serpapi.com/](https://serpapi.com/)

---

## Quick Start Commands

### 1. Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Copy config template
```bash
# macOS
cp examples/claude_desktop_config_uv_testpypi.json \
   ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cp examples/claude_desktop_config_uv_testpypi.json \
   ~/.config/Claude/claude_desktop_config.json

# Windows (PowerShell)
Copy-Item examples/claude_desktop_config_uv_testpypi.json `
   $env:APPDATA\Claude\claude_desktop_config.json
```

### 3. Edit config and add your SERPAPI key
```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
nano ~/.config/Claude/claude_desktop_config.json

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### 4. Restart Claude Desktop

You're ready to go! 🚀

---

## License

MIT License - See LICENSE file for details.

