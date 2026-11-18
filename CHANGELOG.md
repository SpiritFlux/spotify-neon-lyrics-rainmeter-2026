# Changelog

## 4.9.0
- **Click-through button:** a third button between the settings gear and the power button turns click-through on/off (lit purple = on). It appears with the others after the 2-second hover,
  and stays visible while click-through is on (a click-through skin can't see the pointer). The state is saved, kept in sync with *Settings -> More -> Lyrics click-through*,
  and read from Rainmeter's own setting at load, so it never starts out of sync. The Settings panel itself is never click-through.
- Launcher window is now 98 x 30 (gear, click-through, power). Debug log records click-through changes.
- README: contact line.

## 4.8.0
- **Settings + power buttons moved into the corner:** they now sit at the top-right of the lyrics (where the old *Customize* button was) as a small horizontal pair.
  The hover *Customize* button is removed. Settings can still be opened by double-click or right-click -> *Customize layout...*.
- **Hover to reveal (default):** the buttons appear after the pointer rests on the lyrics for 2 seconds (*Settings -> More -> Buttons appear after hovering*)
  and hide again about 3 seconds after you leave. With *click-through* on, hovering can't be detected, so they stay visible then.
- The Settings panel opens right next to the lyrics again (no extra gap). Debug log now records when the buttons are shown/hidden.

## 4.7.0
- **Auto font for the song's language:** the skin detects the script of the lyrics and switches the lyric font when your font can't draw it
  (Indic -> Nirmala UI, Thai -> Leelawadee UI, Japanese -> Yu Gothic UI, Korean -> Malgun Gothic, Chinese -> Microsoft YaHei UI, Arabic/Hebrew/Georgian/Armenian -> Segoe UI).
  Toggle: *Settings -> Text -> Auto-pick font*. Latin/Cyrillic/Greek keep your font. New fonts in the font list: Malgun Gothic, Microsoft YaHei UI, Leelawadee UI.
- **Wrapping for languages without spaces** (Japanese, Chinese, Thai): over-long runs are now broken between characters instead of running off the edge.
- Docs: README *Languages* section (what is supported and how it was verified). No AI-attribution text remains in files or commit messages.

## 4.6.1
- **Bug fix - Look tab button:** the *Look* tab button opened the Layout tab (`Tab(1)` instead of `Tab(2)`), and the *About* / *More* tab buttons were affected the same way
  in one build. Cause: a build-time test edit of the generated `Settings.ini`. `Settings.ini` is regenerated, and there is now `tools/check_settings.py`,
  which verifies every tab button, every handler function and the file encodings. `build_rmskin.py` refuses to package if the check fails.

## 4.6.0
- **Box themes from the original skin:** *Look -> Box style* = **Neon**, **Glass**, **AMOLED** (colors, box opacity, border strength and glow strengths exactly as in the 3.x skin).
  Picking one switches Lyrics-only to Card so the box is visible. Also *Corners* (Square / Rounded / Pill) and *Size* presets (Small / Medium / Large = 75 / 100 / 125 %).
- **Bug fix - theme swatches:** the color circles were drawn around the meter origin, so only one quarter of each was clickable. They now react everywhere.
- **Bug fix - Open log file:** the log file is now created when Settings opens, so the button always has something to open.
- **Bug fix - preview while Settings is open:** Settings re-asserts it every second, so sample lyrics survive a refresh of the lyrics skin.
- **Quick save** now names layouts after their contents (e.g. `Card - Neon - 3 lines`).
- Glow-text and shadow strengths are real settings (`GlowTextA`, `ShadowA`) instead of constants; box styles use them. New saved-layout keys: `BoxStyle`, `BorderA`, `GlowA`, `GlowTextA`.
- Settings panel is 670 px tall.

## 4.5.0
- **About tab** in Settings: version, quick setup video, Rainmeter forum thread, GitHub repository, releases and issue tracker links.
- **Gear + power buttons are visible by default** (faint, bright on hover). They were hover-only and easy to miss. *Settings -> More -> Only show them on hover*
  restores the old behaviour (delay setting still applies). Setting is called `GearHoverOnly` (default 0).
- Settings panel now has 7 tabs and is 650 px tall.

## 4.4.0
- **Idle state is calm:** when Spotify isn't open / nothing is playing, a small faded message is shown instead of animated sample lyrics.
  Sample lyrics now only show while the Settings panel is open or if *Always preview lyrics when idle* is on (default off).
- **Debug log:** errors/warnings always go to the Rainmeter log and `@Resources\Logs\debug.log` (with stack traces and context: track, fetch state).
  Turn on *Settings -> More -> Debug log* for INFO/DEBUG detail; *Open log file* opens it. Log rotates at 256 KB. All public Lua functions are guarded.
- **Close the skin from the skin:** hover the lyrics, then use the power button under the gear (⚙). Two clicks (first arms, second closes).
- **Disabled the broken `Main_SYNCFIX.ini`** (it shared Main's Rainmeter config, so loading it replaced the real skin) and the old `_Presets`/`_System` skins;
  they were moved to `_Legacy` and renamed `*.disabled`.
- Fixes: `_prevIndex` was reset on a different variable than the one the scroll logic reads; hint default no longer self-references.
- Cleanup: removed dead helpers (`GetLine`, `GetSizeForLine`, `Invalidate`), documented the Lua/INI files, added `CONTRIBUTING.md`.
- Settings panel is taller (610 px) to fit the new options.

## Repository organisation (4.3.0 PR)
- Skin lives in `SpotifyNeonLyrics/`; installers in `releases/` (old v1/v2 `.rmskin` moved there); tools in `tools/`.
- Old v1/v2 skin files (`AMOLEDBig`, `Base`, `GlassMedium`, `NeonSmall`, `SpotifyLyricsWebClean` x2) moved to `SpotifyNeonLyrics/_Legacy/`.
- Removed duplicate `README.txt` files (superseded by `README.md`); skin metadata license set to MIT to match `LICENSE`.
- Added `.gitignore` (per-user files) and `.gitattributes` (UTF-16 skin files kept byte-for-byte).

## 4.3.0
- **Custom number of lines:** *Lyric lines shown* is now a 1-11 stepper (current line + up to 5 before and 5 after) instead of 1/3/5.
  Meters, spacing, fading and window height all follow the count. Existing saved layouts with 1/3/5 keep working.
- **Gear delay setting:** Settings -> More -> *Gear appears after hover* (0.5-10 s, default 2 s).
- **Cut-off lyrics, root cause:** the width estimate was within ~6 % of reality but lines wrapped at 95 % of the area, leaving no margin
  for glow/shadow. Widths were re-calibrated against real GDI+ measurements of Nirmala UI / Yu Gothic UI (+8 %) and lines now wrap at 88 %.
- Internal: side lines are `LyricPrev1..5` / `LyricNext1..5` (meters `MeterLyricPrev1..5` / `MeterLyricNext1..5`); layout flags `ShowP1..5` / `ShowN1..5`.

## 4.2.1
- **Gear button appears on hover:** hidden by default; shows after the pointer rests on the lyrics for ~2 s and stays ~3 s after
  you leave (or while you hover it). A click-through skin can't see the pointer, so then the button stays visible.
- **No more overlap with *Customize*:** the button is placed right of the lyrics, else left, else above, else the bottom-right
  corner - never inside the top-right corner. Settings now open with extra gap so they don't cover it.

## 4.2.0
- **Always-reachable settings:** new ⚙ button skin (`Launcher\Launcher.ini`) placed automatically next to the lyrics. Works
  even when the lyrics are click-through (double-click / right-click can't reach them then). Toggle: Settings → More →
  *Gear button*; right-click the button to hide it. Closes with the lyrics.
- **Settings are never click-through:** opening Settings (and the Launcher) forces `ClickThrough 0` on their own windows;
  the *Lyrics click-through* toggle only affects the lyrics skin.
- **Wrapping fix:** the line-width estimate was too small (Rainmeter font sizes are points, Indic/CJK glyphs are wider), so
  long previous/next lines ran past the edge. Estimates are now conservative and lines wrap at 95 % of the lyrics width.
- Everything is recorded in this file; see *Files* below for the full list of what changed since 3.0.
## 4.1.0
- **Lyrics fetch:** now requested once per track change (was a `curl` call every second, even when idle). Retries up to
  3 times, 12 s timeout, identifying `User-Agent`. Stale cache is deleted on track change so old lyrics never flash.
- **Status messages:** "Searching lyrics…", "No lyrics found for this song", "Instrumental", "Can't reach the lyrics service"
  (toggle: Motion → Show lyric status messages).
- **Fade between songs** (toggle: Motion → Fade between songs).
- **Saved layouts:** save/load/delete up to 6 named layouts (Settings → Saved), stored in `@Resources\Layouts`.
- **Per-song timing offsets** on top of the global offset (Settings → More); stored in `@Resources\Settings\offsets.txt`.
- **One-click package:** `python tools/build_rmskin.py` → `dist/SpotifyNeonLyrics_<version>.rmskin`.
- Settings: new *Motion*, *Saved* and *More* tabs. `Settings.ini` is now generated by `tools/gen_settings.py`.
- `User.inc` is created from `User.default.inc` on first run and is no longer tracked in git.
- Removed unused FileView measure, empty `Layout_*.inc` files and the hard-coded debug meters.

## 4.0.0
- New `Main.ini`: Lyrics Only mode (no box), Card and Now Playing layouts; 1/3/5 lines; alignment; fonts; 8 themes.
- Live Settings panel in its own Rainmeter config (runs beside the lyrics, no Apply button).
- Preview lyrics when idle; smooth scrolling and word-by-word glow; opens settings beside the lyrics.
- Lyrics: picks the best LRCLIB result (prefers synced), splits unsynced lyrics across the track, wraps long lines,
  full Unicode support (script saved as UTF-16 LE), sub-second timing interpolation.

## Files (since the 3.0 build)
**Added:** `Launcher\Launcher.ini`, `Settings\Settings.ini` (generated), `@Resources\Scripts\Settings.lua`,
`@Resources\Settings\User.default.inc`, `@Resources\Layouts\.gitkeep`, `@Resources\Cache\.gitkeep`,
`tools\gen_settings.py`, `tools\build_rmskin.py`, `README.md`, `CHANGELOG.md`, `.gitignore`, `.gitattributes`.
**Rewritten:** `Main.ini` (new layout engine, box-free Lyrics Only), `@Resources\Scripts\LyricsParser.lua` (fetch-once,
status, fade, best-result pick, wrap, animation, per-song offsets, launcher), `Hub.ini` (now a launcher for Main + Settings),
`@Resources\Settings\User.inc` (per-user, git-ignored).
**Removed:** `README.txt` (→ README.md), empty `@Resources\Layouts\Layout_*.inc`.
**Untouched legacy (not packaged):** `_Presets`, `_System`, `Main_SYNCFIX.ini`, `*_GOLDEN.lua`, `*_SYNCFIX.lua`,
`@Resources\Styles`, `@Resources\Modules`.
A pre-redesign backup zip is kept locally (git-ignored): `_Backup_v3.0_before_redesign.zip`.