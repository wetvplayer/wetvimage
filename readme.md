# IPTV Auto-Sync & Logo Matcher

Automated tool to download existing channel logos, auto-discover missing logos from the global IPTV database, host them on GitHub via jsDelivr CDN, and output a clean updated `.m3u` playlist.

---

## Quick Start (All-in-One Command)

To process your default playlist (`sports.m3u`), auto-fill missing logos, update the playlist, and automatically push new images to GitHub:

```powershell
py sync_logos.py
```

### For Any Other M3U File:
```powershell
py sync_logos.py my_playlist.m3u
# Or specify custom output name:
py sync_logos.py my_playlist.m3u output_playlist.m3u
```

---

## Features

1. **Auto-Discovery for Missing Logos**: Automatically searches channels with empty `tvg-logo=""` against 48,000+ indexed channels (from iptv-org) and fills them in.
2. **Global jsDelivr CDN Hosting**: All logos are served with 100% uptime and speed:
   `https://cdn.jsdelivr.net/gh/wetvplayer/wetvimage@main/logos/<filename>.png`
3. **One-Click Auto Git Push**: Automatically stages, commits, and pushes only the new image files to `wetvplayer/wetvimage` on GitHub.
4. **Clean Git Tracking**: `.m3u` playlist files and temporary scripts are excluded via `.gitignore` so your public repository contains only the clean image assets.
