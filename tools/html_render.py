"""Screenshot an HTML file to PNG with headless Chrome/Chromium.

A browser is used instead of Pillow because Pillow (without libraqm) cannot shape Devanagari: matras
and conjuncts come out broken. Chrome shapes Hindi correctly on every OS.

Browser lookup: $CHROME, then common install paths, then PATH, then Playwright's Chromium
(installed on first use if needed).
"""
import os
import shutil
import subprocess
import sys
import tempfile

_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
_browser = None


def _playwright_chromium():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "playwright"], check=True)
        from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        exe = p.chromium.executable_path
    if not os.path.exists(exe):
        subprocess.run([sys.executable, "-m", "playwright", "install", "--with-deps", "chromium"], check=True)
    return exe


def browser():
    global _browser
    if _browser:
        return _browser
    env = os.environ.get("CHROME")
    found = [env] if env else []
    found += [c for c in _CANDIDATES if os.path.exists(c)]
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if shutil.which(name):
            found.append(shutil.which(name))
    _browser = found[0] if found else _playwright_chromium()
    return _browser


def screenshot(html_path, png_path, w, h):
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/").lstrip("/")
    with tempfile.TemporaryDirectory() as profile:
        cmd = [browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
               "--allow-file-access-from-files", f"--user-data-dir={profile}",
               f"--window-size={w},{h}", "--virtual-time-budget=4000",
               f"--screenshot={os.path.abspath(png_path)}", url]
        if sys.platform.startswith("linux"):
            cmd.insert(1, "--no-sandbox")
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    if not os.path.exists(png_path):
        sys.exit(f"browser did not write {png_path}")
