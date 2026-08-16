import os
import sys
import re
import json
import time
import uuid
import random
import mimetypes
import urllib.request
import urllib.error
import http.cookiejar
from concurrent.futures import ThreadPoolExecutor, as_completed

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

class PostImgUploader:
    def __init__(self, cache_file='logo_cache.json'):
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Warning: Could not save cache: {e}")

    def download_image(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': USER_AGENT,
                    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
                })
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        content_type = resp.headers.get_content_type() or 'image/png'
                        data = resp.read()
                        return data, content_type
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[-] Failed downloading {url}: {e}")
                time.sleep(1)
        return None, None

    def upload_image(self, img_data, filename='image.png', content_type='image/png', max_retries=3):
        boundary = '----WebKitFormBoundary' + uuid.uuid4().hex
        upload_session = f'{int(time.time()*1000)}{random.random():.16f}'[0:24]
        
        body = bytearray()
        def add_field(name, val):
            body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{val}\r\n'.encode('utf-8'))
            
        add_field('token', '')
        add_field('upload_session', upload_session)
        add_field('numfiles', '1')
        add_field('gallery', '')
        add_field('ui', '[true,true,0,"desktop"]')
        add_field('optsize', '0')
        add_field('expire', '0')
        add_field('session_upload', str(int(time.time()*1000)))
        
        body.extend(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: {content_type}\r\n\r\n'.encode('utf-8'))
        body.extend(img_data)
        body.extend(f'\r\n--{boundary}--\r\n'.encode('utf-8'))
        
        for attempt in range(max_retries):
            try:
                req = urllib.request.Request('https://postimages.org/json/rr', data=bytes(body), headers={
                    'User-Agent': USER_AGENT,
                    'Content-Type': f'multipart/form-data; boundary={boundary}',
                    'Origin': 'https://postimages.org',
                    'Referer': 'https://postimages.org/',
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                })
                
                resp = self.opener.open(req, timeout=30)
                res_text = resp.read().decode('utf-8')
                res_json = json.loads(res_text)
                
                page_url = res_json.get('url') or res_json.get('image')
                if page_url:
                    direct_url = self.resolve_direct_url(page_url)
                    return direct_url
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[-] Upload failed for {filename}: {e}")
                time.sleep(1.5)
        return None

    def resolve_direct_url(self, page_url):
        try:
            req = urllib.request.Request(page_url, headers={'User-Agent': USER_AGENT})
            resp = self.opener.open(req, timeout=15)
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Check og:image
            og_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html, re.I)
            if og_match:
                return og_match.group(1)
                
            # Check direct download link
            dl_match = re.search(r'href=["\'](https?://i\.postimg\.cc/[^"\']+)["\']', html, re.I)
            if dl_match:
                return dl_match.group(1)
                
            # Check any i.postimg.cc link
            all_links = re.findall(r'https?://i\.postimg\.cc/[^\s"\'<>]+', html)
            if all_links:
                return all_links[0]
                
            return page_url
        except Exception:
            return page_url

    def process_single_url(self, original_url):
        if original_url in self.cache:
            return original_url, self.cache[original_url]
            
        # Extract filename from URL
        clean_url = original_url.split('?')[0]
        basename = os.path.basename(clean_url)
        if not basename or '.' not in basename:
            basename = f"logo_{uuid.uuid4().hex[:8]}.png"
            
        data, content_type = self.download_image(original_url)
        if not data:
            return original_url, None
            
        uploaded_url = self.upload_image(data, filename=basename, content_type=content_type)
        if uploaded_url:
            self.cache[original_url] = uploaded_url
            self._save_cache()
            return original_url, uploaded_url
            
        return original_url, None

    def process_m3u(self, input_file, output_file, max_workers=5):
        if not os.path.exists(input_file):
            print(f"[!] Input file '{input_file}' not found.")
            return False

        print(f"[*] Reading '{input_file}'...")
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find all logo URLs
        logo_urls = re.findall(r'tvg-logo="([^"]+)"', content)
        unique_urls = [u.strip() for u in set(logo_urls) if u.strip().startswith('http')]
        
        print(f"[*] Found {len(logo_urls)} total logo entries ({len(unique_urls)} unique URLs).")
        
        url_map = {}
        completed = 0
        total = len(unique_urls)
        
        print(f"[*] Starting uploads to Postimg.cc using {max_workers} worker threads...\n")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.process_single_url, url): url for url in unique_urls}
            
            for future in as_completed(future_to_url):
                orig_url, new_url = future.result()
                completed += 1
                if new_url:
                    url_map[orig_url] = new_url
                    print(f"[{completed}/{total}] SUCCESS: {orig_url} -> {new_url}")
                else:
                    print(f"[{completed}/{total}] FAILED:  {orig_url}")

        print(f"\n[*] Upload phase finished. Successfully uploaded: {len(url_map)}/{total}")
        
        # Replace URLs in the M3U content
        def replace_logo(match):
            old_url = match.group(1)
            new_url = url_map.get(old_url, old_url)
            return f'tvg-logo="{new_url}"'

        new_content = re.sub(r'tvg-logo="([^"]+)"', replace_logo, content)
        
        print(f"[*] Writing updated playlist to '{output_file}'...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"[+] Done! New playlist saved at: {output_file}")
        return True


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'sports.m3u'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'sports_postimg.m3u'
    
    # Resolve absolute paths if needed
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(input_file):
        input_file = os.path.join(base_dir, input_file)
    if not os.path.isabs(output_file):
        output_file = os.path.join(base_dir, output_file)
        
    cache_file = os.path.join(base_dir, 'logo_cache.json')
    
    uploader = PostImgUploader(cache_file=cache_file)
    uploader.process_m3u(input_file, output_file, max_workers=6)

if __name__ == '__main__':
    main()
