"""Sanity checks for the generated Settings\\Settings.ini (run after gen_settings.py, and before every release).

    python tools/check_settings.py

Checks:
  * every tab button [TabN] calls Tab(N)
  * every function called from a button exists in Settings.lua
  * every file is UTF-16 LE with BOM (the encoding Rainmeter needs for non-ASCII text)
Exit code 1 if anything is wrong.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_sub = os.path.join(HERE, "..", "SpotifyNeonLyrics")
SKIN = _sub if os.path.isdir(_sub) else os.path.join(HERE, "..")
problems = []


def read16(path):
    with open(path, "rb") as f:
        raw = f.read()
    if raw[:2] != b"\xff\xfe":
        problems.append(f"not UTF-16 LE with BOM: {os.path.relpath(path, SKIN)}")
    return raw.decode("utf-16")


ini = read16(os.path.join(SKIN, "Settings", "Settings.ini"))
lua = read16(os.path.join(SKIN, "@Resources", "Scripts", "Settings.lua"))

# 1) tab buttons
for m in re.finditer(r"^\[Tab(\d)\]\r?\n(?:.*\r?\n)*?LeftMouseUpAction=(.*)$", ini, re.M):
    n, action = m.group(1), m.group(2)
    if f"Tab({n})" not in action:
        problems.append(f"[Tab{n}] button calls the wrong tab: {action}")

# 2) every called function exists
defined = set(re.findall(r"^function (\w+)\(", lua, re.M))
called = set(re.findall(r'CommandMeasure S "(\w+)\(', ini))
for fn in sorted(called - defined):
    problems.append(f"Settings.ini calls {fn}() but Settings.lua does not define it")

# 3) other skin files encoding
for rel in ("Main.ini", "Hub.ini", os.path.join("Launcher", "Launcher.ini"),
            os.path.join("@Resources", "Scripts", "LyricsParser.lua")):
    p = os.path.join(SKIN, rel)
    if os.path.exists(p):
        read16(p)

if problems:
    print("PROBLEMS:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print(f"settings OK: {len(called)} handler functions, tab buttons correct, encodings OK")
