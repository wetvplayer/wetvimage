# 📺 Live TV & Channel Logo CDN Documentation

Complete guide for managing Live IPTV playlists, auto-discovering missing channel logos, hosting images on GitHub via jsDelivr CDN, and previewing streams.

---

## 📌 Table of Contents
1. [Overview](#overview)
2. [Live Logo Sync Tool (`scripts/sync_logos.py`)](#live-logo-sync-tool-scriptssync_logospy)
   - [Command Usage](#command-usage)
   - [How Logo Discovery Works](#how-logo-discovery-works)
   - [jsDelivr CDN Structure](#jsdelivr-cdn-structure)
   - [Automatic Git Push](#automatic-git-push)
3. [Web Player & Stream Dashboard (`scripts/web_player_preview.py`)](#web-player--stream-dashboard-scriptsweb_player_previewpy)
4. [Playlist Management (`playlists/`)](#playlist-management-playlists)

---

## 1. Overview
The Live TV system ensures your channel playlists always have high-resolution, fast-loading channel logos served through a global CDN (jsDelivr), with automatic Git commits to the `wetvplayer/wetvimage` repository.

---

## 2. Live Logo Sync Tool (`scripts/sync_logos.py`)

### Command Usage:
```powershell
# 1. Default: processes playlists/sports.m3u and outputs playlists/sports_github.m3u
py scripts/sync_logos.py

# 2. Process any custom playlist:
py scripts/sync_logos.py playlists/kurdish_channels.m3u

# 3. Specify custom input and output files:
py scripts/sync_logos.py playlists/input.m3u playlists/output_cdn.m3u
```

### How Logo Discovery Works:
1. **Parser**: Reads every `#EXTINF:` entry in the `.m3u` file.
2. **Missing Logo Detection**: For any channel where `tvg-logo=""` is empty, it cleans channel tokens (e.g. `[HD]`, `4K`, `FHD`, `HEVC`, `(1080p)`, language tags) and queries the **48,000+ indexed channel database** from `iptv-org`.
3. **Download & Deduplication**: Downloads unique image files into `logos/` with an MD5 hash suffix to avoid name collisions (e.g., `beIN_SPORTS_1_HD_c460c9.png`).
4. **CDN URL Rewriting**: Rewrites all `tvg-logo` attributes in the output playlist to jsDelivr CDN URLs.
5. **Git Sync**: Stages `logos/`, creates a commit `Auto-sync: update channel logos`, and pushes directly to `origin main`.

### jsDelivr CDN Format:
All hosted channel logos are immediately accessible worldwide with 100% uptime:
```
https://cdn.jsdelivr.net/gh/wetvplayer/wetvimage@main/logos/<channel_name>_<hash>.png
```

---

## 3. Web Player & Stream Dashboard (`scripts/web_player_preview.py`)

Preview your channels, check stream latency, test video playback, and inspect logo rendering directly in your browser without needing external player apps:

```powershell
# Launch preview with default playlist:
py scripts/web_player_preview.py

# Or launch with a specific M3U playlist:
py scripts/web_player_preview.py playlists/sports_github.m3u
```

### Player Features:
- **Built-in HLS / VideoJS Player**: Native playback of `.m3u8` and `.ts` streams.
- **Category Filter Tabs**: Filter channels by category instantly.
- **Logo Visualizer**: Shows live CDN images with broken link fallback indicators.
- **Search Bar**: Instant channel search by name or stream URL.

---

## 4. Directory Conventions for Live TV

- **`logos/`**: Only repository image assets (`.png`, `.webp`) are stored here and tracked in Git.
- **`playlists/`**: Contains raw (`sports.m3u`) and CDN-updated (`sports_github.m3u`) playlist files.
- **`cache/`**: Contains `iptv_db_cache.json` (auto-refreshed every 7 days).
