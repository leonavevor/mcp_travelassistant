#!/usr/bin/env python3
"""Runner to start/stop MCP servers from a single JSON config file.

This script centralizes configuration for all services in `mcp_config.json` and
can either call the local HTTP control server (convenience wrapper) or fall
back to spawning per-server subprocesses (with env injection) or invoking
local handlers when appropriate.

Usage:
  python scripts/run_mcp_from_config.py [--config mcp_config.json] [--dry-run]

Behavior:
- By default it will try to call the HTTP control server at 127.0.0.1:8787.
- If the HTTP endpoint is unreachable or `requests` is not available, it will
  attempt to spawn each server's `main.py` under `py_mcp_travelplanner/<server>/main.py`,
  injecting any `env` overrides from the config into the child process.

The expected config file layout is the repository-root `mcp_config.json`:
{
  "name": "travel-planner",
  "servers": [
    {"name": "flight_server"},
    {"name": "weather_server"}
  ],
  "start_all": {"dry_run": true}
}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
import subprocess

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "mcp_config.json"
DEFAULT_HTTP = ("127.0.0.1", 8787)


def load_config(path: Path) -> Dict[str, Any]:
    with path.open() as fh:
        return json.load(fh)


def try_http_control(host: str, port: int) -> bool:
    try:
        import requests
    except Exception:
        return False
    try:
        r = requests.get(f"http://{host}:{port}/status", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def http_post(host: str, port: int, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
    import requests

    url = f"http://{host}:{port}{path}"
    try:
        if params:
            r = requests.post(url, params=params, timeout=10)
        else:
            r = requests.post(url, timeout=10)
        try:
            return r.json()
        except Exception:
            return r.text
    except Exception as e:
        return {"error": str(e)}


def run_via_http(cfg: Dict[str, Any], host: str, port: int, dry_run_override: Optional[bool]):
    print(f"Using HTTP control server at {host}:{port}")
    servers = cfg.get("servers", [])

    for s in servers:
        name = s.get("name")
        if not name:
            continue
        dry = s.get("dry_run")
        if dry is None:
            if dry_run_override is not None:
                dry = dry_run_override
            else:
                dry = bool(cfg.get("start_all", {}).get("dry_run", True))
        params = {"server": name, "dry": "true" if dry else "false"}
        print(f"POST /start server={name} dry={dry}")
        res = http_post(host, port, "/start", params=params)
        print(res)

    start_all = cfg.get("start_all")
    if start_all is not None:
        dry = start_all.get("dry_run", False) if dry_run_override is None else bool(dry_run_override)
        print(f"POST /start_all dry={dry}")
        res = http_post(host, port, "/start_all", params={"dry": "true" if dry else "false"})
        print(res)


def spawn_server_process(base_dir: Path, server_name: str, env_overrides: Optional[Dict[str, Any]] = None, dry_run: bool = False) -> Dict[str, Any]:
    """Spawn the server's main.py as a subprocess with merged environment.

    Returns a dict with keys: ok (bool), pid (int|None), log (str), error (str|None)
    """
    result: Dict[str, Any] = {"ok": False, "pid": None, "log": None, "error": None}

    server_script = base_dir / "py_mcp_travelplanner" / server_name / "main.py"
    if not server_script.exists():
        result["error"] = f"main.py not found for server '{server_name}' at {server_script}"
        return result

    if dry_run:
        result["ok"] = True
        result["log"] = f"dry-run: would spawn {server_script}"
        return result

    # Prepare environment
    env = os.environ.copy()
    if env_overrides:
        # ensure values are strings
        for k, v in env_overrides.items():
            env[k] = str(v)

    # Prepare logs directory
    logs_dir = base_dir / "logs"
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    log_path = logs_dir / f"{server_name}.log"

    # Build command
    cmd = [sys.executable, str(server_script)]

    try:
        log_f = open(log_path, "a")
        proc = subprocess.Popen(cmd, env=env, stdout=log_f, stderr=subprocess.STDOUT, close_fds=True)
        # small sleep to let process start and produce PID
        time.sleep(0.05)
        result["ok"] = True
        result["pid"] = proc.pid
        result["log"] = str(log_path)
    except Exception as e:
        result["error"] = str(e)
    finally:
        try:
            log_f.close()
        except Exception:
            pass

    return result


def run_via_local_handlers(cfg: Dict[str, Any], dry_run_override: Optional[bool]):
    """Spawn local server subprocesses and inject env overrides. Falls back to cli_handlers if spawn not possible."""
    print("Using local subprocess spawn fallback")
    base_dir = Path(__file__).resolve().parents[1]

    sys.path.insert(0, str(base_dir))
    try:
        from py_mcp_travelplanner import cli_handlers  # type: ignore
    except Exception:
        cli_handlers = None

    servers = cfg.get("servers", [])
    for s in servers:
        name = s.get("name")
        if not name:
            continue
        env_overrides = s.get("env")
        dry = s.get("dry_run")
        if dry is None:
            if dry_run_override is not None:
                dry = bool(dry_run_override)
            else:
                dry = bool(cfg.get("start_all", {}).get("dry_run", True))

        spawn_res = spawn_server_process(base_dir, name, env_overrides=env_overrides, dry_run=bool(dry))
        if spawn_res.get("ok"):
            print({"server": name, "started": True, "pid": spawn_res.get("pid"), "log": spawn_res.get("log")})
            continue

        # Fallback to cli_handlers.start_server if spawning failed
        if cli_handlers is not None:
            try:
                ok = cli_handlers.start_server(name, dry_run=bool(dry), env_overrides=env_overrides)
                print({"server": name, "started": bool(ok)})
                continue
            except Exception as e:
                print({"server": name, "error": str(e)})
                continue

        print({"server": name, "spawn_error": spawn_res.get("error")})

    # Optionally call start_all via handlers if available to run any post-start logic
    start_all = cfg.get("start_all")
    if start_all:
        dry = start_all.get("dry_run", True) if dry_run_override is None else bool(dry_run_override)
        print(f"start_all behavior: dry_run={dry}")
        if cli_handlers is not None:
            try:
                res = cli_handlers.start_all_servers(dry_run=bool(dry))
                print(res)
            except Exception as e:
                print({"start_all_error": str(e)})
        else:
            print("start_all: completed (spawned per-server processes)")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run MCP servers from a single JSON config")
    parser.add_argument("--config", "-c", type=Path, default=DEFAULT_CONFIG, help="Path to mcp_config.json")
    parser.add_argument("--http-host", default=DEFAULT_HTTP[0], help="HTTP control server host")
    parser.add_argument("--http-port", type=int, default=DEFAULT_HTTP[1], help="HTTP control server port")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Force dry run")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Force actual start")
    parser.set_defaults(dry_run=None)

    args = parser.parse_args(argv)

    if not args.config.exists():
        print(f"Config file not found: {args.config}")
        return 2

    cfg = load_config(args.config)

    # Decide whether to use HTTP control or local handlers
    use_http = try_http_control(args.http_host, args.http_port)
    if use_http:
        try:
            run_via_http(cfg, args.http_host, args.http_port, args.dry_run)
            return 0
        except Exception as e:
            print("HTTP control error:", e)
            print("Falling back to local handlers")

    # fallback
    try:
        run_via_local_handlers(cfg, args.dry_run)
        return 0
    except Exception as e:
        print("Local handlers error:", e)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
