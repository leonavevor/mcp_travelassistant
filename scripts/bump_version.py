#!/usr/bin/env python3
"""Bump the version in pyproject.toml.
Usage: bump_version.py [major|minor|patch]
"""
import re
import sys
from pathlib import Path

level = sys.argv[1] if len(sys.argv) > 1 else "patch"

# Find pyproject.toml by searching upward from the script's directory so the
# script works when run when invoked from scripts/ (Makefile) or from the repo root.
here = Path(__file__).resolve().parent
p = None
for parent in (here, *here.parents):
    candidate = parent / "pyproject.toml"
    if candidate.exists():
        p = candidate
        break
if p is None:
    print(
        "Error: pyproject.toml not found (searched from script up to filesystem root)",
        file=sys.stderr,
    )
    sys.exit(1)

s = p.read_text()

# match semantic version numbers like 1.2.3
m = re.search(r'^version\s*=\s*"(\d+)\.(\d+)\.(\d+)"', s, flags=re.M)
if not m:
    print("Error: version not found in pyproject.toml", file=sys.stderr)
    sys.exit(1)
maj, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
if level == "major":
    maj += 1
    minor = 0
    patch = 0
elif level == "minor":
    minor += 1
    patch = 0
else:
    patch += 1

new = f'version = "{maj}.{minor}.{patch}"'
s2 = re.sub(r"^version\s*=.*$", new, s, flags=re.M)
p.write_text(s2)
print(f"Bumped version to {maj}.{minor}.{patch}")
