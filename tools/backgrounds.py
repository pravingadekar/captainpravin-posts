"""Fetch a topic-matched background photo for a slide from a free text-to-image service.

The image is generated from an English prompt (content.json "bg"), the service's watermark strip at the
bottom is cropped off, and the result is cached next to the post so re-renders are stable.
"""
import io
import os
import time
import urllib.parse
import urllib.request

from PIL import Image

STYLE = ", cinematic photo, dark moody navy blue and gold lighting, shallow depth of field, no text, no letters, no logos"
URL = "https://image.pollinations.ai/prompt/{p}?width={w}&height={h}&nologo=true&seed={s}"


GAP = 47  # the free tier allows 1 image every 45 seconds per IP
_last = [0.0]


def fetch(prompt, path, w=1080, h=1350, seed=1, tries=5):
    """Download one background to `path` (jpg). Returns the path, or None if the service failed."""
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        return path
    url = URL.format(p=urllib.parse.quote(prompt + STYLE), w=w, h=h, s=seed)
    for attempt in range(tries):
        wait = _last[0] + GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "post-renderer/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r:
                data = r.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            # drop the bottom strip that can carry the service's watermark
            img = img.crop((0, 0, img.width, int(img.height * 0.92)))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            img.save(path, quality=88)
            return path
        except Exception as e:  # network or decode error: retry, then give up
            print(f"  background attempt {attempt + 1} failed: {e}")
    return None
