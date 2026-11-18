# Contributing

Thanks for helping! This is a Rainmeter skin, so a few things work differently from a normal codebase.

## Quick start

1. Clone the repo and copy (or symlink) `SpotifyNeonLyrics/` into `Documents\Rainmeter\Skins\`.
2. In Rainmeter: *Manage* → *Refresh all*, then load `SpotifyNeonLyrics\Main.ini`.
3. Edit → save → right-click the skin → *Refresh skin*. (Lua changes also need a refresh.)

## Rules that will bite you

| Rule | Why |
|---|---|
| Save `.ini` / `.lua` as **UTF-16 LE with BOM** | Rainmeter decodes non-ASCII only in that encoding. UTF-8 → garbled Tamil/Hindi/CJK lyrics; UTF-8 **with** BOM → the Lua script won't load. `.gitattributes` keeps these files byte-for-byte, so diffs show as binary — describe changes in the PR. |
| Don't edit `Settings/Settings.ini` by hand (not even temporarily) | It's generated: change `tools/gen_settings.py`, run `python tools/gen_settings.py`, then `python tools/check_settings.py`. To try a tab without clicking, call `Tab(n)` through `!CommandMeasure S ...`. |
| Fetch lyrics **once per track change** | LRCLIB is a free community API. No timers that call it. |
| Meters read variables, Lua does the maths | All layout numbers come from `Layout()` in `LyricsParser.lua`. Meters in `Main.ini` should only use `#Variables#`. |
| `Main`, `Settings`, `Launcher` are separate configs | Two `.ini` files in the same Rainmeter folder can't be loaded together. That's why Settings lives in `Settings/` and the gear in `Launcher/`. |
| Per-user files are git-ignored | `User.inc`, `offsets.txt`, saved layouts, cache and logs. Defaults ship in `User.default.inc`. |

## Debugging

- Turn on **Settings → More → Debug log**, reproduce the problem, then *Open log file*
  (`SpotifyNeonLyrics/@Resources/Logs/debug.log`). Errors include a stack trace and the current track/fetch state.
- Rainmeter's own log: *Rainmeter → Manage → Log* (errors/warnings from the skin appear with the `[Lyrics]` / `[Settings]` prefix).
- Lyrics cache: `@Resources/Cache/lrclib.json` is the raw LRCLIB response for the current track.

## Making a release

1. Update `CHANGELOG.md` (every change goes in) and bump `SpotifyNeonLyrics/@Resources/VERSION.txt`.
2. `python tools/build_rmskin.py` → `releases/SpotifyNeonLyrics_<version>.rmskin`.
3. Test the `.rmskin` on a clean Rainmeter profile: double-click, play a song, open Settings, change a few things.

## Pull request checklist

- [ ] Tested in Rainmeter with a song playing **and** with Spotify closed
- [ ] Tested a non-Latin song (e.g. Tamil/Japanese) if you touched text/wrapping code
- [ ] `CHANGELOG.md` updated
- [ ] Regenerated `Settings.ini` if you touched `tools/gen_settings.py`, then ran `python tools/check_settings.py`
- [ ] Lua/INI files still UTF-16 LE
- [ ] No per-user files (`User.inc`, `offsets.txt`, logs, cache) committed
