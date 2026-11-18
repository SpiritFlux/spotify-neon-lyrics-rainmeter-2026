# Spotify Neon Lyrics for Rainmeter

A real-time synced lyrics panel for Spotify Desktop using WebNowPlaying and LRCLIB.

- Modern neon aesthetic
- Real-time synced LRC lyric parsing
- Lightweight (no Spotify API tokens required)
- Designed for 2026 desktop setups

Official Website: https://spotifyneonlyrics.wixsite.com/neonlyrics

Premium $2.50: https://neonlyrics.gumroad.com/l/neonlyricspremium

## What's new in 4.x

- **Lyrics Only mode** — just the text: no box, no border, no branding
- **Live settings panel** — every change applies instantly (no Apply button), opens beside the lyrics
- **Box themes** — Neon, Glass and AMOLED (from the original skin), corner styles and size presets
- **Customizable** — layout mode (Lyrics only / Card / Now playing), **1-11 lyric lines**, alignment, size, width, spacing,
  fonts, 8 themes, glow, shadow, box opacity and corner radius
- **Smooth scrolling** and **word-by-word glow** (both optional), **fade between songs**
- **Status messages** — Searching / No lyrics found / Instrumental / Can't reach the lyrics service
- **Saved layouts** (name them, up to 6) and **per-song timing offsets**
- **Always reachable settings** — ⚙ (settings), click-through and power (close) buttons appear in the top-right corner after hovering for 2 seconds (always visible when click-through is on)
- **20 scripts supported** with an automatic font for the song's language (Tamil, Hindi, Japanese, Korean, Chinese, Thai, Arabic, Cyrillic…) — see [Languages](#languages)
- Preview lyrics when nothing is playing, so you can style it without Spotify running
- Lyrics are fetched **once per track change** (retried up to 3×) instead of polling LRCLIB
- **Calm idle state** — when Spotify isn't open you get a small faded message, not flashing sample lyrics
- **Close from the skin** — hover the lyrics → x (or the power button under ⚙); two clicks to confirm
- **Debug log** — one toggle gives you a log file to attach to bug reports

See [CHANGELOG.md](CHANGELOG.md) for the full list.

## Links

- Quick setup guide (video): https://www.youtube.com/watch?v=TNNlO35z9I8
- Rainmeter forum thread: https://forum.rainmeter.net/viewtopic.php?t=45826
- GitHub (original project): https://github.com/SpiritFlux/spotify-neon-lyrics-rainmeter-2026
- Releases: https://github.com/SpiritFlux/spotify-neon-lyrics-rainmeter-2026/releases/tag/SpotifyNeonLyricsv3

The same links are in the skin: **Settings → About**.

## Languages

- **Interface (Settings panel, messages):** English only for now.
- **Lyrics:** any language LRCLIB has lyrics for and Windows can draw — **20 scripts** (hundreds of languages):
  Latin (incl. accents / Vietnamese), Cyrillic, Greek, Armenian, Georgian, Hebrew, Arabic, Devanagari (Hindi, Marathi, Nepali),
  Bengali, Gurmukhi (Punjabi), Gujarati, Tamil, Telugu, Kannada, Malayalam, Sinhala, Thai, Japanese, Korean and Chinese.
- **Automatic font:** the skin detects the lyrics' script and switches to a Windows font that has those glyphs
  (*Settings → Text → Auto-pick font*; on by default). Latin/Cyrillic/Greek keep your chosen font.
- **How this was checked:** glyph coverage of the Windows fonts was measured for all of the scripts above; the script detection and
  font choice were tested on 10 scripts; real songs were verified in Latin (Portuguese) and Tamil. Other scripts are not yet verified
  on real songs — please report problems with the debug log attached.
- **Known limits:** Arabic and Hebrew are right-to-left, so line breaks and ordering may not be perfect. Languages without spaces
  (Japanese, Chinese, Thai) are wrapped between characters. Needs the matching Windows fonts (present on a normal Windows 10/11 install).
## Requirements

- Rainmeter 4.5+
- WebNowPlaying plugin
- WebNowPlaying browser extension
- Spicetify with WebNowPlaying enabled
- Spotify Desktop

## Install

1. Download `SpotifyNeonLyrics_<version>.rmskin` from [`releases/`](releases/) and double-click it
   (or copy the `SpotifyNeonLyrics` folder to `Documents\Rainmeter\Skins\` and load `Main.ini`).
2. Play a song. **Double-click the lyrics**, right-click → *Customize layout…*, or hover the lyrics for 2 seconds and click the ⚙ button that appears in the top-right corner (next to it: click-through on/off and power).
3. Tabs: **Layout** · **Look** · **Text** · **Motion** · **Saved** · **More**. Choose *Lyrics only* for no box.

### Troubleshooting

| Problem | Fix |
|---|---|
| Nothing shows | Play a song with the WebNowPlaying extension connected (idle shows preview lyrics). |
| "No lyrics found" | LRCLIB doesn't have that track. |
| "Can't reach the lyrics service" | Check your connection / that `curl.exe` works (it retries 3 times). |
| Boxes / missing characters | Text tab → pick a font with your script (Nirmala UI for Indic, Yu Gothic UI for CJK). |
| Unsynced lyrics drift | Plain-text lyrics are spread evenly over the song; use *More → This song's timing*. |
| Something is broken | Settings → More → **Debug log** on, reproduce it, then *Open log file* (or see @Resources/Logs/debug.log). Errors also appear in Rainmeter's log. Attach it to your issue. |
| Lyrics early/late | *More → Lyric timing* (all songs) or *This song's timing*. |

## Repository layout

```
SpotifyNeonLyrics/            the Rainmeter skin (this is what gets installed)
  Main.ini                    the lyrics skin
  Hub.ini                     launcher (opens Main + Settings)
  Launcher/Launcher.ini       the ⚙ / click-through / power buttons (placed by Main)
  Settings/Settings.ini       GENERATED live settings panel (see tools/)
  @Resources/Scripts/         LyricsParser.lua (engine), Settings.lua (panel logic)
  @Resources/Settings/        User.default.inc (shipped defaults; User.inc is per-user, git-ignored)
  @Resources/Logs/            debug.log (git-ignored)
  _Legacy/                    old v1/v2 skins, kept for history (not packaged)
releases/                     packaged .rmskin installers
tools/                        gen_settings.py, build_rmskin.py
CHANGELOG.md
```

## Contributing / development

- **Lua and INI files must be saved as UTF-16 LE** (with BOM). UTF-8 shows mojibake for non-Latin lyrics, and UTF-8
  *with* BOM stops the script from loading. `.gitattributes` keeps them byte-for-byte.
- `SpotifyNeonLyrics/Settings/Settings.ini` is generated — edit `tools/gen_settings.py`, then `python tools/gen_settings.py`.
- Build an installer: bump `SpotifyNeonLyrics/@Resources/VERSION.txt`, run `python tools/build_rmskin.py` → `releases/`.
- Please keep fetching to **once per track change**; LRCLIB is a free community service.
- Log every change in `CHANGELOG.md`.

## Credits & contact

Original skin by SpiritFlux (NeonLyrics Project). 4.x live settings, box themes and multi-language support by notgiridharan.

Discord: `nfoj`

## Support

If you enjoy this project and would like to support continued development and polish, you can do so here:

https://buymeacoffee.com/spiritflux

Support is completely optional, but always appreciated ❤️

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by Spotify.

Lyrics are fetched dynamically from LRCLIB. This project does not host, store, or redistribute lyrics.

All trademarks and copyrights belong to their respective owners.

## License

MIT License — see [LICENSE](LICENSE).
