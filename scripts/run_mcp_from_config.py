"""
Unified MCP Travel Planner Launcher Script

This script reads a YAML or JSON config file and launches all MCP servers (event, weather, hotel, flight, finance, geocoder)
with the specified transport (stdio or http), host, port, and environment variables (e.g., SERPAPI_KEY).

Usage:
  python scripts/run_mcp_from_config.py --config runtime_config.yaml

Example config (YAML or JSON):

servers:
  weather:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8791
  event:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8796
  hotel:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8795
  flight:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8793
  finance:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8792
  geocoder:
    enabled: true
    transport: http
    host: 127.0.0.1
    port: 8794

SERPAPI_KEY: "your_serpapi_key_here"

"""
import os
import sys
import subprocess
import argparse
import yaml
import json
from pathlib import Path

def load_config(path):
    with open(path, 'r') as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)

def launch_server(name, opts, env):
    if not opts.get('enabled', True):
        print(f"Skipping {name}-server (disabled)")
        return None
    base_dir = Path(__file__).parent.parent / 'py_mcp_travelplanner' / f"{name}_server"
    main_py = base_dir / 'main.py'
    if not main_py.exists():
        print(f"Warning: {main_py} not found!")
        return None
    cmd = [sys.executable, str(main_py),
           '--transport', opts.get('transport', 'stdio')]
    if opts.get('transport', 'stdio') == 'http':
        cmd += ['--host', opts.get('host', '127.0.0.1'),
                '--port', str(opts.get('port', 8700))]
    print(f"Launching {name}-server: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, env=env)
    return proc

def main():
    parser = argparse.ArgumentParser(description="Unified MCP Travel Planner Launcher")
    parser.add_argument('--config', required=True, help='Path to YAML or JSON config file')
    args = parser.parse_args()
    config = load_config(args.config)
    env = os.environ.copy()
    if 'SERPAPI_KEY' in config:
        env['SERPAPI_KEY'] = config['SERPAPI_KEY']
    procs = []
    for name, opts in config.get('servers', {}).items():
        proc = launch_server(name, opts, env)
        if proc:
            procs.append(proc)
    print(f"Launched {len(procs)} MCP servers. Press Ctrl+C to stop.")
    try:
        for proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        print("\nShutting down all servers...")
        for proc in procs:
            proc.terminate()
        for proc in procs:
            proc.wait()
    print("All servers stopped.")

if __name__ == '__main__':
    main()

