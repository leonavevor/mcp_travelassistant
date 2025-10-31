# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.12] - 2025-11-01

### Fixed
- **Critical:** Fixed `ModuleNotFoundError: No module named 'mcp'` when installing package without extras
  - Moved `mcp>=1.9.1` and `fastmcp>=2.5.1` from optional `[servers]` extra to core dependencies
  - Package now works immediately after `pip install py_mcp_travelplanner` or `uv run --with py_mcp_travelplanner`
  - No need to install extras for basic MCP server functionality

### Changed
- Improved CLI error handling with helper functions `_run_mcp_server()` and `_run_control_server()`
- Better error messages when dependencies are missing, with clear installation instructions
- Replaced `__import__()` calls with proper import error handling

### Documentation
- Updated README.md to remove outdated JSON runtime config references
- Added `docs.not-needed/MCP_DEPENDENCY_FIX.md` with detailed fix explanation
- Added `docs.not-needed/FIX_SUMMARY.md` with comprehensive summary
- Modernized configuration documentation with references to `examples/` directory

## [0.1.11] - 2025-10-31

### Added
- Multi-source runtime configuration system (env vars > .env > YAML > defaults)
- Comprehensive configuration documentation in `docs.not-needed/CONFIG_README.md`
- 28 comprehensive tests for runtime configuration (all passing)
- Configuration example script in `examples/config_example.py`

### Changed
- PyYAML and python-dotenv added to core dependencies for config support
- Fixed recursion bug in `config.py` `_configure_logging()` method
- Updated CLI handlers to use new config module

## [0.1.10] - 2025-10-31

### Added
- MCP configuration examples for Claude Desktop
- `examples/claude_desktop_config_uv_testpypi.json` - UV with Test PyPI
- `examples/claude_desktop_config_uv_pypi.json` - UV with PyPI
- `examples/claude_desktop_config_template.json` - Local installation
- Comprehensive MCP configuration documentation in `examples/MCP_CONFIG_README.md`
- Quick reference guide in `examples/QUICK_REFERENCE.md`
- Automated test script `examples/test_uv_config.sh`

### Documentation
- Added visual guide `examples/VISUAL_GUIDE.txt`
- Added implementation summary `examples/MCP_CONFIG_IMPLEMENTATION.md`

## [0.1.5] - 2025-10-30

### Added
- Initial unified MCP server implementation
- CLI with commands: list, start, health, start-all, serve, mcp
- HTTP control server for service orchestration
- 25 comprehensive tests for MCP server (all passing)
- PID tracking for running services
- Service discovery and health checks

### Features
- Single MCP server entry point for all travel services
- Tools: list_servers, start_server, stop_server, health_check, get_status
- Backend services: event, finance, flight, geocoder, hotel, weather
- SERPAPI key verification

## [0.1.0] - 2025-10-29

### Added
- Initial project structure
- Basic package configuration
- Server-specific modules (event, finance, flight, geocoder, hotel, weather)
- Test infrastructure

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

Given a version number MAJOR.MINOR.PATCH (e.g., 0.1.12):
- The **0** indicates the project is in initial development
- The **1** is the minor version (new features)
- The **12** is the patch version (bug fixes)

