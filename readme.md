# IPTV Auto-Sync, CDN Logo Hosting & MCP Manager

Automated toolkit to discover missing channel logos, download & host them on GitHub via jsDelivr CDN, preview streams with a built-in web player, and synchronize playlists directly with MyTVPro MCP.

---

## 🚀 Quick Start: Logo Sync & GitHub CDN Upload

To automatically scan your playlist, auto-find missing channel logos from the global IPTV database, download them, and push them to GitHub CDN:

```powershell
# Default: Processes playlists/sports.m3u -> generates playlists/sports_github.m3u
py scripts/sync_logos.py
```

### For Any Other Custom M3U Playlist:
```powershell
# Specify input playlist:
py scripts/sync_logos.py playlists/my_playlist.m3u

# Specify input and custom output name:
py scripts/sync_logos.py playlists/my_playlist.m3u playlists/my_output.m3u
```

### How the Logo Sync Works:
1. **Auto-Discovery**: Scans all `#EXTINF:` entries for missing logos (`tvg-logo=""`) and matches them against **48,000+ indexed channels** from `iptv-org`.
2. **Local Download**: Downloads high-resolution icons to the local `logos/` folder with unique hashes to prevent collisions.
3. **jsDelivr CDN Hosting**: Rewrites all logo URLs to high-speed, 100% uptime CDN links:
   ```
   https://cdn.jsdelivr.net/gh/wetvplayer/wetvimage@main/logos/<channel_name>_<hash>.png
   ```
4. **Auto Git Push**: Automatically stages, commits, and pushes new images to the `wetvplayer/wetvimage` repository on GitHub.

---

## 🌐 Web Player & Stream Preview Dashboard

Test streams, inspect logos, and preview channels directly in your browser:

```powershell
# Preview default sports playlist
py scripts/web_player_preview.py

# Or preview any specific M3U playlist:
py scripts/web_player_preview.py playlists/sports_github.m3u
```

---

## ⚡ MyTVPro MCP Automation

Tools to synchronize categories, bouquets, and channels directly with your IPTV CMS:

### 1. Upload Playlist & Create Bouquets
```powershell
py mcp/upload_sports_mcp.py
```
- Imports live channels into MyTVPro.
- Creates `All Sports` category and bouquet.
- Automatically assigns channels and links bouquets to all VIP packages and user lines.

### 2. Merge All Categories into Single "All Sports"
```powershell
py mcp/merge_all_sports.py
```

### 3. List All Categories & Channel Counts
```powershell
py mcp/list_categories.py
```

---

## 🎬 Free Movie & Video Uploaders

### Option A: Pixeldrain (Up to 10 GB per Video)
Fast direct MP4 streaming links:
```powershell
# Single movie
py scripts/upload_pixeldrain.py "C:\Movies\Movie.mp4" "Movie Title (2024)" "Action"

# Entire folder
py scripts/upload_pixeldrain.py --folder "C:\Movies" "Movies"
```

### Option B: DoodStream (Unlimited Storage & Embeds)
```powershell
# Local movie upload
py scripts/upload_doodstream.py "C:\Movies\Movie.mp4" "Movie Title" "Movies"

# Remote URL upload (zero local bandwidth)
py scripts/upload_doodstream.py --remote "https://example.com/video.mp4" "Movie Title" "Movies"
```

### Option C: Streamtape (Direct & Remote Upload)
```powershell
py scripts/upload_streamtape.py "C:\Movies\Movie.mp4" "Movie Title" "Movies"
```

### Option D: Universal Stream Extractor (yt-dlp powered)
Extract direct stream URLs and thumbnails from YouTube, Twitch, Facebook, VK, and web video pages:
```powershell
# Extract stream and thumbnail directly into playlists/movies.m3u:
py scripts/universal_stream_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Extract and push video to Pixeldrain:
py scripts/universal_stream_extractor.py --upload-pixeldrain "https://www.youtube.com/watch?v=VIDEO_ID" "Action"
```

---

## 📁 Directory Structure

```
halabja88/
├── cache/                  # Database & logo cache files
│   ├── iptv_db_cache.json
│   └── logo_cache.json
├── configs/                # API credentials & service configurations
│   ├── doodstream_config.json
│   ├── pixeldrain_config.json
│   └── streamtape_config.json
├── logos/                  # CDN channel logo assets (tracked in Git)
│   └── *.png
├── mcp/                    # MCP synchronization scripts & bouquet tools
│   ├── upload_sports_mcp.py
│   ├── merge_all_sports.py
│   └── list_categories.py
├── playlists/              # Local M3U playlists
│   ├── sports.m3u          # Source playlist
│   ├── sports_github.m3u   # CDN-linked playlist
│   └── movies.m3u
├── scripts/                # Automation utilities & uploaders
│   ├── sync_logos.py       # Core logo sync & GitHub CDN pusher
│   ├── web_player_preview.py
│   └── upload_*.py
├── templates/              # Web player templates & embed code
├── .gitignore              # Clean Git ignore rules (only logos are tracked)
└── readme.md               # User guide & documentation
```
