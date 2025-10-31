#!/usr/bin/env python3
"""Example script demonstrating runtime configuration usage.

This script shows how to use the RuntimeConfig class to load configuration
from multiple sources with proper precedence.
"""
from py_mcp_travelplanner.config import get_config, get_api_key

def main():
    """Demonstrate configuration loading and access."""
    print("=" * 70)
    print("MCP Travel Planner - Runtime Configuration Example")
    print("=" * 70)
    print()
    
    # Get the global config instance
    config = get_config()
    
    print("Configuration loaded from:")
    print("  1. Environment variables (highest priority)")
    print("  2. .env file")
    print("  3. runtime_config.yaml")
    print("  4. Default values (lowest priority)")
    print()
    
    # Display key configuration values
    print("Server Configuration:")
    print("-" * 70)
    print(f"  Host:             {config.get('CONTROL_SERVER_HOST')}")
    print(f"  Port:             {config.get('CONTROL_SERVER_PORT')}")
    print(f"  Server Name:      {config.get('MCP_SERVER_NAME')}")
    print()
    
    print("Logging Configuration:")
    print("-" * 70)
    print(f"  Log Level:        {config.get('LOG_LEVEL')}")
    print(f"  Log Format:       {config.get('LOG_FORMAT')}")
    print()
    
    print("Server Process Management:")
    print("-" * 70)
    print(f"  Start Timeout:    {config.get('SERVER_START_TIMEOUT')} seconds")
    print(f"  Stop Timeout:     {config.get('SERVER_STOP_TIMEOUT')} seconds")
    print(f"  Health Check:     {config.get('HEALTH_CHECK_INTERVAL')} seconds")
    print()
    
    print("Feature Flags:")
    print("-" * 70)
    print(f"  Auto Discovery:   {config.get('ENABLE_AUTO_DISCOVERY')}")
    print(f"  PID Tracking:     {config.get('ENABLE_PID_TRACKING')}")
    print(f"  Dry Run:          {config.get('DRY_RUN')}")
    print(f"  Debug Mode:       {config.get('DEBUG_MODE')}")
    print()
    
    # Check API key status
    print("API Configuration:")
    print("-" * 70)
    serpapi_key = get_api_key('SERPAPI_KEY')
    if serpapi_key:
        # Mask the key for security
        masked_key = serpapi_key[:8] + '...' + serpapi_key[-8:] if len(serpapi_key) > 16 else '***'
        print(f"  SERPAPI_KEY:      {masked_key} (configured)")
    else:
        print(f"  SERPAPI_KEY:      Not configured")
    print()
    
    # Show how to get a safe dict for logging
    print("Configuration Export (safe for logging):")
    print("-" * 70)
    safe_config = config.to_dict(include_sensitive=False)
    print(f"  Total config keys: {len(safe_config)}")
    print(f"  Sensitive values:  Redacted")
    print()
    
    # Example: checking if a key exists
    print("Configuration Checks:")
    print("-" * 70)
    print(f"  Has CONTROL_SERVER_PORT: {config.has('CONTROL_SERVER_PORT')}")
    print(f"  Has NONEXISTENT_KEY:     {config.has('NONEXISTENT_KEY')}")
    print()
    
    print("=" * 70)
    print("Example complete!")
    print("=" * 70)
    print()
    print("To customize configuration:")
    print("  1. Set environment variables (e.g., export CONTROL_SERVER_PORT=9000)")
    print("  2. Create a .env file in the project root")
    print("  3. Edit runtime_config.yaml")
    print()

if __name__ == '__main__':
    main()

