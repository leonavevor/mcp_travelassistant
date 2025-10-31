# MCP Config Quick Reference

## Quick Copy-Paste Configurations

### 🧪 Test PyPI (For Testing Pre-releases)

```json
{
  "mcpServers": {
    "py_mcp_travelplanner_testpypi": {
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

---

### 📦 PyPI (Stable Release)

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

---

### 🐍 Local Installation

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

### 📌 Pinned Version

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

---

## UV Command Examples

### Test from Test PyPI
```bash
uv run \
  --index https://test.pypi.org/simple \
  --with py_mcp_travelplanner \
  --no-project \
  -- py_mcp_travelplanner_cli list
```

### Test from PyPI
```bash
uv run \
  --with py_mcp_travelplanner \
  --no-project \
  -- py_mcp_travelplanner_cli list
```

### Test specific version
```bash
uv run \
  --with py_mcp_travelplanner==0.1.5 \
  --no-project \
  -- py_mcp_travelplanner_cli list
```

---

## Config File Locations

| OS | Path |
|---|---|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

---

## Environment Variables Cheat Sheet

| Variable | Default | Description |
|---|---|---|
| `SERPAPI_KEY` | None | **Required** - Your SerpAPI key |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `CONTROL_SERVER_PORT` | `8787` | Server port |
| `DEBUG_MODE` | `false` | Enable debug mode |
| `DRY_RUN` | `false` | Test without side effects |

---

## Quick Commands

### Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
pip install uv
```

### Edit Claude Config
```bash
# macOS
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
nano ~/.config/Claude/claude_desktop_config.json

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### Check Claude Logs
```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp*.log

# Linux
tail -f ~/.config/Claude/logs/mcp*.log

# Windows
Get-Content $env:APPDATA\Claude\logs\mcp*.log -Wait
```

---

## Troubleshooting One-Liners

```bash
# Test UV installation
uv --version

# Test package availability
uv run --with py_mcp_travelplanner --no-project -- python -c "import py_mcp_travelplanner; print('OK')"

# Test from Test PyPI
uv run --index https://test.pypi.org/simple --with py_mcp_travelplanner --no-project -- python -c "import py_mcp_travelplanner; print('OK')"

# Verify SERPAPI key
curl "https://serpapi.com/search.json?q=test&api_key=YOUR_KEY_HERE"
```

---

## Remember

1. Replace `your_serpapi_key_here` with your actual key
2. Restart Claude Desktop after config changes
3. Check logs if it doesn't work
4. Use Test PyPI only for testing, PyPI for production

---

**Need help?** Check `MCP_CONFIG_README.md` for detailed documentation.

