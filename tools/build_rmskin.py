"""Builds a one-click installer:  releases/SpotifyNeonLyrics_<version>.rmskin (or dist/ in a flat skin folder)

Usage (from the skin root):  python tools/build_rmskin.py

An .rmskin is just a zip with an RMSKIN.ini and a Skins/ folder. Double-click it
and Rainmeter installs + loads the skin. Per-user files (User.inc, saved layouts,
per-song offsets, the lyrics cache) are NOT packaged; User.inc is shipped from
User.default.inc so every install starts from clean defaults.
"""
import os
import re
import sys
import zipfile
import fnmatch

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
_sub = os.path.join(REPO, "SpotifyNeonLyrics")
ROOT = _sub if os.path.isdir(_sub) else REPO        # skin folder (repo layout or flat)
OUT_DIR = os.path.join(REPO, "releases") if ROOT != REPO else os.path.join(REPO, "dist")
SKIN = "SpotifyNeonLyrics"

EXCLUDE = [
    "tools/*", "dist/*", ".git/*", ".git*", "docs/*", "_Backup*", "*.rmskin", "*.zip",
    "_Presets/*", "_System/*", "_Legacy/*", "Main_SYNCFIX.ini",          # legacy experiments
    "@Resources/Scripts/*_GOLDEN.lua", "@Resources/Scripts/*_SYNCFIX.lua",
    "@Resources/Styles/*", "@Resources/Modules/*",           # only used by the legacy files
    "@Resources/Settings/User.inc", "@Resources/Settings/offsets.txt",
    "@Resources/Layouts/*.txt", "@Resources/Cache/*.json", "@Resources/Cache/song_state.txt", "@Resources/Logs/*.log", "@Resources/Logs/*.old",
    "CHANGELOG.md", "README.md", ".gitignore", ".gitattributes",
]
KEEP = ["@Resources/Layouts/.gitkeep", "@Resources/Cache/.gitkeep", "@Resources/Logs/.gitkeep"]


def excluded(rel):
    if rel in KEEP:
        return False
    return any(fnmatch.fnmatch(rel, pat) for pat in EXCLUDE)


def version():
    with open(os.path.join(ROOT, "@Resources", "VERSION.txt"), encoding="utf-8") as f:
        m = re.search(r"^VERSION=(\S+)", f.read(), re.M)
    return m.group(1) if m else "0.0.0"


def main():
    # refuse to package a broken settings panel
    import subprocess
    chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_settings.py")
    if subprocess.call([sys.executable, chk]) != 0:
        print("check_settings.py failed - fix the problems above before building")
        return 1
    ver = version()
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, f"{SKIN}_{ver}.rmskin")
    rmskin_ini = (
        "[rmskin]\r\n"
        f"Name={SKIN}\r\n"
        "Author=NeonLyrics Project\r\n"
        f"Version={ver}\r\n"
        "LoadType=Skin\r\n"
        f"Load={SKIN}\\Main.ini\r\n"
        f"VariableFiles={SKIN}\\@Resources\\Settings\\User.inc\r\n"
        "MinimumRainmeter=4005000\r\n"
        "MinimumWindows=6001\r\n"
    )
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("RMSKIN.ini", rmskin_ini.encode("utf-16"))
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "dist", "tools", "docs", "__pycache__")]
            for name in files:
                full = os.path.join(base, name)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                if excluded(rel):
                    continue
                z.write(full, f"Skins/{SKIN}/{rel}")
                count += 1
        # clean per-user defaults
        z.write(os.path.join(ROOT, "@Resources", "Settings", "User.default.inc"),
                f"Skins/{SKIN}/@Resources/Settings/User.inc")
        count += 1
    print(f"built {out} ({count} files, {os.path.getsize(out) // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
