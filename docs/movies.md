# 🎬 Movies & VOD Documentation

Complete guide for uploading, extracting, transcoding, and managing Video On Demand (VOD) and Movie streams for your IPTV service.

---

## 📌 Table of Contents
1. [Overview](#overview)
2. [Uploaders & Storage Providers](#uploaders--storage-providers)
   - [Option A: Pixeldrain (High Bandwidth MP4)](#option-a-pixeldrain-high-bandwidth-mp4)
   - [Option B: DoodStream (Transcoding & Embeds)](#option-b-doodstream-transcoding--embeds)
   - [Option C: Streamtape (Direct & Remote Upload)](#option-c-streamtape-direct--remote-upload)
   - [Option D: Universal Stream Extractor (yt-dlp)](#option-d-universal-stream-extractor-yt-dlp)
3. [Playlist Generation (`playlists/movies.m3u`)](#playlist-generation-playlistsmoviesm3u)
4. [Supported Formats & Best Practices](#supported-formats--best-practices)

---

## 1. Overview
The movie toolchain allows you to take local video files or web stream URLs, upload them to high-speed cloud hosts, extract thumbnails, and automatically append them to your IPTV movie playlist (`playlists/movies.m3u`).

---

## 2. Uploaders & Storage Providers

### Option A: Pixeldrain (High Bandwidth MP4)
- **File Limit**: Up to 10 GB per video.
- **Features**: Direct MP4 stream links, fast streaming speeds.
- **Script**: `scripts/upload_pixeldrain.py`
- **Config**: `configs/pixeldrain_config.json`

#### Usage:
```powershell
# 1. Upload a single local movie file:
py scripts/upload_pixeldrain.py "C:\Movies\Inception.2010.mp4" "Inception (2010)" "Sci-Fi"

# 2. Upload an entire directory of movies in batch:
py scripts/upload_pixeldrain.py --folder "C:\Movies" "Action Movies"
```

---

### Option B: DoodStream (Transcoding & Embeds)
- **Storage**: Unlimited video storage.
- **Features**: Auto multi-quality transcoding (1080p/720p/480p), responsive iframe embed links.
- **Script**: `scripts/upload_doodstream.py`
- **Config**: `configs/doodstream_config.json`

#### Usage:
```powershell
# 1. Upload local movie file:
py scripts/upload_doodstream.py "C:\Movies\Gladiator.mp4" "Gladiator (2000)" "Action"

# 2. Remote URL upload (Transfers web video with zero PC bandwidth usage):
py scripts/upload_doodstream.py --remote "https://example.com/video.mp4" "Movie Title" "Movies"
```

---

### Option C: Streamtape (Direct & Remote Upload)
- **Storage**: Unlimited storage.
- **Features**: Fast direct streaming, remote URL mirroring.
- **Script**: `scripts/upload_streamtape.py`
- **Config**: `configs/streamtape_config.json`

#### Usage:
```powershell
# Upload local video file:
py scripts/upload_streamtape.py "C:\Movies\Interstellar.mp4" "Interstellar (2014)" "Sci-Fi"
```

---

### Option D: Universal Stream Extractor (yt-dlp)
- **Engine**: Powered by `yt-dlp`.
- **Supported Platforms**: YouTube, Twitch, Facebook, VK, Dailymotion, and 1,000+ web streaming sites.
- **Script**: `scripts/universal_stream_extractor.py`

#### Usage:
```powershell
# 1. Extract direct stream link & thumbnail into playlists/movies.m3u:
py scripts/universal_stream_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# 2. Download web stream and push permanently to Pixeldrain:
py scripts/universal_stream_extractor.py --upload-pixeldrain "https://www.youtube.com/watch?v=VIDEO_ID" "Action"
```

---

## 3. Playlist Generation (`playlists/movies.m3u`)

Every movie uploader automatically creates and appends entries to `playlists/movies.m3u` using standard `#EXTINF` formatting:

```m3u
#EXTM3U
#EXTINF:-1 tvg-id="0" tvg-name="Inception (2010)" tvg-logo="https://cdn.jsdelivr.net/gh/wetvplayer/wetvimage@main/logos/inception.png" group-title="Sci-Fi",Inception (2010)
https://pixeldrain.com/api/file/FILE_ID?download
```

---

## 4. Supported Video Formats & Subtitles

- **Video Containers**: `.mp4`, `.mkv`, `.ts`, `.avi`, `.mov`, `.webm`, `.m4v`, `.flv`
- **Subtitles**: `.srt`, `.vtt`, `.sub`, `.ass`
- **Git Protection**: All video formats are automatically ignored in `.gitignore` so large video binaries are never committed to your Git repository.
