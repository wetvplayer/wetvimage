# IPTV Logo Uploader & CDN Generator

This repository contains tools to extract channel logos from `.m3u` playlists, save/upload them to permanent hosting services, and generate updated playlist files with direct CDN URLs.

---

## Option 1: GitHub + jsDelivr CDN (Permanent & Fastest)

Downloads all channel logos locally into the `logos/` folder and generates a playlist pointing to jsDelivr global CDN:
`https://cdn.jsdelivr.net/gh/<username>/<repo>@main/logos/<filename>.png`

### Run Script:
```powershell
py download_m3u_logos_github.py
```

### Push to GitHub:
```powershell
git init
git add .
git commit -m "Add channel logos and updated playlist"
git branch -M main
git remote add origin https://github.com/wetvplayer/wetvimage.git
git push -u origin main
```

---

## Option 2: Postimages (postimg.cc) Direct Uploader

Directly uploads logos to Postimages with no expiration (`expire: 0`) and resolves direct `https://i.postimg.cc/...` URLs.

### Run Script:
```powershell
# Default (sports.m3u -> sports_postimg.m3u)
py upload_m3u_logos.py

# Custom files
py upload_m3u_logos.py input_file.m3u output_file.m3u
```
