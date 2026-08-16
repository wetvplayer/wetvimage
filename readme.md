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

## Web Player & Stream Dashboard

To visually preview your channel logos, filter by category, and play/test streams directly in your browser:

```powershell
py web_player_preview.py
# Or preview a specific playlist:
py web_player_preview.py sports_github.m3u
```

---

## Free Movie & VOD Uploaders

### Option A: Pixeldrain (Up to 10 GB per Movie)
Fastest direct MP4 streaming links with high bandwidth:

```powershell
# Upload a single movie
py upload_pixeldrain.py "C:\Movies\Inception.mp4" "Inception (2010)" "Sci-Fi"

# Upload an entire folder of movies at once:
py upload_pixeldrain.py --folder "C:\Movies" "Action Movies"
```

*(First time you run it, you can enter your free API key from [pixeldrain.com/user/api_keys](https://pixeldrain.com/user/api_keys))*

---

### Option B: Archive.org (Unlimited Permanent Storage)
Permanent S3-backed movie storage:

```powershell
py upload_movies.py "C:\path\to\movie.mp4" "Spider-Man 2002" "Action Movies"
```

---

## Features

1. **Auto-Discovery for Missing Logos**: Automatically searches channels with empty `tvg-logo=""` against 48,000+ indexed channels (from iptv-org) and fills them in.
2. **Global jsDelivr CDN Hosting**: All logos are served with 100% uptime and speed:
   `https://cdn.jsdelivr.net/gh/wetvplayer/wetvimage@main/logos/<filename>.png`
3. **One-Click Auto Git Push**: Automatically stages, commits, and pushes only the new image files to `wetvplayer/wetvimage` on GitHub.
4. **Clean Git Tracking**: `.m3u` playlist files and temporary scripts are excluded via `.gitignore` so your public repository contains only the clean image assets.
