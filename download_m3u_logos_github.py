import os
import sys
import re
import json
import time
import hashlib
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

def sanitize_filename(name):
    # Keep alphanumeric, dashes, dots, underscores
    clean = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)
    return clean

def get_filename_for_url(url, channel_name=None):
    parsed = urllib.parse.urlparse(url)
    basename = os.path.basename(parsed.path)
    ext = os.path.splitext(basename)[1].lower()
    
    if not ext or ext not in ['.png', '.jpg', '.jpeg', '.webp', '.svg']:
        ext = '.png'
        
    if channel_name:
        sanitized_name = sanitize_filename(channel_name).strip('_')
        if sanitized_name:
            # Add short hash to avoid collision
            h = hashlib.md5(url.encode('utf-8')).hexdigest()[:6]
            return f"{sanitized_name}_{h}{ext}"
            
    if basename and '.' in basename:
        return sanitize_filename(basename)
        
    h = hashlib.md5(url.encode('utf-8')).hexdigest()[:10]
    return f"logo_{h}{ext}"

def download_image(url, save_path, max_retries=3):
    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        return True
        
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': USER_AGENT,
                'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    data = resp.read()
                    if len(data) > 0:
                        with open(save_path, 'wb') as f:
                            f.write(data)
                        return True
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"[-] Failed downloading {url}: {e}")
            time.sleep(1)
    return False

def process_playlist(input_file, output_file, logos_dir, github_user, github_repo, branch='main', use_jsdelivr=True, max_workers=8):
    if not os.path.exists(input_file):
        print(f"[!] Input file '{input_file}' not found.")
        return False

    os.makedirs(logos_dir, exist_ok=True)
    
    print(f"[*] Reading '{input_file}'...")
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    url_to_channel = {}
    for line in lines:
        if line.startswith('#EXTINF:'):
            logo_match = re.search(r'tvg-logo="([^"]+)"', line)
            channel_match = re.search(r',([^,]+)$', line)
            if logo_match:
                url = logo_match.group(1).strip()
                if url.startswith('http'):
                    name = channel_match.group(1).strip() if channel_match else None
                    if url not in url_to_channel:
                        url_to_channel[url] = name

    unique_urls = list(url_to_channel.keys())
    print(f"[*] Found {len(unique_urls)} unique logo URLs.")

    url_to_filename = {}
    url_to_cdn = {}
    download_tasks = []

    for url in unique_urls:
        ch_name = url_to_channel.get(url)
        fname = get_filename_for_url(url, ch_name)
        save_path = os.path.join(logos_dir, fname)
        url_to_filename[url] = fname
        
        if use_jsdelivr:
            # jsDelivr CDN URL: Fast, global CDN caching
            cdn_url = f"https://cdn.jsdelivr.net/gh/{github_user}/{github_repo}@{branch}/logos/{fname}"
        else:
            # GitHub Raw URL
            cdn_url = f"https://raw.githubusercontent.com/{github_user}/{github_repo}/{branch}/logos/{fname}"
            
        url_to_cdn[url] = cdn_url
        download_tasks.append((url, save_path))

    print(f"[*] Downloading images to '{logos_dir}' folder using {max_workers} threads...")
    completed = 0
    success = 0
    total = len(download_tasks)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_image, url, path): (url, path) for url, path in download_tasks}
        for f in as_completed(futures):
            url, path = futures[f]
            completed += 1
            is_ok = f.result()
            if is_ok:
                success += 1
                print(f"[{completed}/{total}] OK: {os.path.basename(path)}")
            else:
                print(f"[{completed}/{total}] FAILED: {url}")

    print(f"\n[*] Download complete: {success}/{total} logos saved to '{logos_dir}/'.")

    # Generate new M3U content
    new_lines = []
    for line in lines:
        if line.startswith('#EXTINF:'):
            def repl(m):
                old = m.group(1)
                new_url = url_to_cdn.get(old, old)
                return f'tvg-logo="{new_url}"'
            new_line = re.sub(r'tvg-logo="([^"]+)"', repl, line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"[+] Created updated playlist: '{output_file}'")
    print(f"\n[+] CDN URL Preview:")
    for sample_url in list(url_to_cdn.values())[:3]:
        print(f"    - {sample_url}")

    return True

def main():
    # Configuration
    GITHUB_USER = 'wetvplayer'     # Your GitHub username / organization
    GITHUB_REPO = 'wetvimage'      # Your GitHub repo name
    BRANCH = 'main'
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'sports.m3u'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'sports_github.m3u'
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, input_file) if not os.path.isabs(input_file) else input_file
    output_path = os.path.join(base_dir, output_file) if not os.path.isabs(output_file) else output_file
    logos_dir = os.path.join(base_dir, 'logos')

    process_playlist(
        input_file=input_path,
        output_file=output_path,
        logos_dir=logos_dir,
        github_user=GITHUB_USER,
        github_repo=GITHUB_REPO,
        branch=BRANCH,
        use_jsdelivr=True,  # True = fast jsDelivr CDN, False = raw.githubusercontent.com
        max_workers=8
    )

if __name__ == '__main__':
    main()
