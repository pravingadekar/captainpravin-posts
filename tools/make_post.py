"""Render a 6-slide carousel (1080x1350) and a reel (1080x1920) for one post.

Slides are laid out in HTML and screenshotted with headless Chrome (tools/html_render.py), so Hindi
(Devanagari) text is shaped correctly. Each slide sits on a topic-matched background photo
(tools/backgrounds.py) under a dark navy overlay so the text stays readable.

Usage: python tools/make_post.py posts/<date> [--no-voice] [--no-bg]
"""
import html
import json
import os
import re
import sys
import tempfile

import backgrounds
import html_render
import tts
from make_reel import build_reel, voice_durations

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = sys.argv[1]
HANDLE = "@tradewithcaptainpravin"

# Content comes from <OUT>/content.json:
#   {"topic": str, "slides": [[[kind, value], ...], ...], "bg": [prompt per slide], "narration": [...]}
# Block kinds: tag, title, text, list (list of str), box, compare ([[label, result, "green"|"red"], ...]),
# cta, disclaimer. The last slide should hold the question, cta and disclaimer.
# "bg" (optional): one short English image prompt per slide describing a scene that matches that slide.
# "narration" (optional): one voiceover line per slide (Devanagari reads best) for the reel.
with open(os.path.join(OUT, "content.json"), encoding="utf-8") as _f:
    _content = json.load(_f)
SLIDES = _content["slides"]
NARRATION = _content.get("narration")
BG = _content.get("bg")
if "TODO" in json.dumps(_content):
    sys.exit("content.json still has TODO placeholders")
if NARRATION and len(NARRATION) != len(SLIDES):
    sys.exit(f"narration has {len(NARRATION)} lines for {len(SLIDES)} slides")
if BG and len(BG) != len(SLIDES):
    sys.exit(f"bg has {len(BG)} prompts for {len(SLIDES)} slides")


def _url(path):
    return "file:///" + os.path.abspath(path).replace("\\", "/").lstrip("/")


FONT_CSS = "\n".join(
    f'@font-face{{font-family:P;src:url("{_url(os.path.join(FONTS, f"Poppins-{name}.ttf"))}");font-weight:{wt}}}'
    for name, wt in (("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800))
)

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{font-family:P,'Noto Sans Devanagari',sans-serif;color:#fff;background:#050d1e %(bg)s center/cover no-repeat;position:relative}
.ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,20,44,.25) 0%%,rgba(6,15,34,.55) 35%%,rgba(4,10,24,.78) 65%%,rgba(4,10,24,.93) 100%%)}
.bar{position:absolute;left:0;right:0;top:0;height:10px;background:#f5b82e}
.head{position:absolute;left:90px;top:60px}
.brand{font-weight:600;font-size:28px;color:#f5b82e;letter-spacing:.5px}
.num{font-weight:500;font-size:26px;color:#c3cfe2;margin-top:4px}
.main{position:absolute;left:90px;right:90px;top:180px;bottom:150px;display:flex;flex-direction:column;justify-content:center}
#c{--s:1}
.tag{display:inline-block;background:#f5b82e;color:#050d1e;font-weight:700;font-size:30u;padding:.25em .8em;border-radius:40px;margin-bottom:34u;line-height:1.3}
.title{font-weight:800;font-size:70u;line-height:1.32;text-shadow:0 3px 20px rgba(0,0,0,.95)}
.rule{width:140u;height:8u;background:#f5b82e;margin:22u 0 40u}
.text{font-size:40u;line-height:1.5;color:#dbe4f2;margin-bottom:30u;text-shadow:0 2px 12px rgba(0,0,0,.95)}
ul{list-style:none;margin-bottom:28u}
li{position:relative;padding-left:60u;font-weight:500;font-size:40u;line-height:1.45;margin-bottom:20u;text-shadow:0 2px 12px rgba(0,0,0,.95)}
li:before{content:"";position:absolute;left:8px;top:.45em;width:22px;height:22px;border-radius:50%%;background:#f5b82e}
.box{background:rgba(16,34,66,.82);border:4u solid #f5b82e;border-radius:24u;padding:28u 40u;color:#f5b82e;font-weight:700;font-size:42u;line-height:1.45;margin-bottom:36u}
.cta{background:#f5b82e;color:#050d1e;border-radius:24u;padding:28u 40u;font-weight:700;font-size:42u;line-height:1.45;margin-bottom:36u}
.cmp{background:rgba(16,34,66,.85);border-radius:24u;padding:24u 50u;margin-bottom:28u;border-left:10u solid}
.cmp .l{font-weight:500;font-size:36u;color:#c3cfe2}.cmp .r{font-weight:800;font-size:54u}
.disc{font-size:26u;line-height:1.5;color:#b7c4d9}
.foot{position:absolute;left:90px;right:90px;bottom:0;height:130px;border-top:2px solid rgba(120,150,200,.35);display:flex;justify-content:space-between;align-items:center}
.handle{font-weight:600;font-size:34px;color:#f5b82e}.swipe{font-weight:500;font-size:30px;color:#c3cfe2}
"""
# "Nu" = N px times the fit scale --s (set by FIT_JS)
CSS = re.sub("(?<![a-z.])([0-9]+)u(?![a-z])", lambda m: f"calc({m.group(1)}px*var(--s))", CSS)
COLORS = {"green": "#58c980", "red": "#e85d5d", "gold": "#f5b82e"}

# shrink the content (font scale --s) until it fits between header and footer
FIT_JS = """<script>
var m=document.querySelector('.main'),c=document.getElementById('c'),s=1;
while(c.scrollHeight>m.clientHeight&&s>0.6){s-=0.04;c.style.setProperty('--s',s);}
</script>"""


def block_html(kind, val):
    e = html.escape
    if kind == "tag":
        return f'<div><span class="tag">{e(val)}</span></div>'
    if kind == "title":
        return f'<div class="title">{e(val)}</div><div class="rule"></div>'
    if kind == "text":
        return f'<div class="text">{e(val)}</div>'
    if kind == "list":
        return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in val) + "</ul>"
    if kind in ("box", "cta"):
        return f'<div class="{kind}">{e(val)}</div>'
    if kind == "compare":
        return "".join(
            f'<div class="cmp" style="border-color:{COLORS[c]}"><div class="l">{e(l)}</div>'
            f'<div class="r" style="color:{COLORS[c]}">{e(r)}</div></div>' for l, r, c in val)
    if kind == "disclaimer":
        return f'<div class="disc">{e(val)}</div>'
    sys.exit(f"unknown block kind {kind!r}")


def slide_html(idx, w, h, bg_path, swipe):
    bg = f'url("{_url(bg_path)}")' if bg_path else "linear-gradient(#0c1b36,#050d1e)"
    body = "".join(block_html(k, v) for k, v in SLIDES[idx])
    sw = '<div class="swipe">Swipe &rsaquo;</div>' if swipe and idx < len(SLIDES) - 1 else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{FONT_CSS}{CSS % {"w": w, "h": h, "bg": bg}}'
            f'</style></head><body><div class="ov"></div><div class="bar"></div>'
            f'<div class="head"><div class="brand">TRADE WITH CAPTAIN PRAVIN</div>'
            f'<div class="num">{idx + 1} / {len(SLIDES)}</div></div>'
            f'<div class="main"><div id="c">{body}</div></div>'
            f'<div class="foot"><div class="handle">{HANDLE}</div>{sw}</div>{FIT_JS}</body></html>')


def render(idx, w, h, png, bg_path, swipe=True):
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "s.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(slide_html(idx, w, h, bg_path, swipe))
        html_render.screenshot(page, png, w, h)


def main():
    os.makedirs(OUT, exist_ok=True)
    reel_dir = os.path.join(HERE, "reel_frames")
    os.makedirs(reel_dir, exist_ok=True)

    bgs = [None] * len(SLIDES)
    if BG and "--no-bg" not in sys.argv:
        for i, prompt in enumerate(BG):
            bgs[i] = backgrounds.fetch(prompt, os.path.join(OUT, "bg", f"bg{i + 1}.jpg"), 1080, 1920, seed=i + 1)
        missing = [i + 1 for i, b in enumerate(bgs) if not b]
        if missing:
            print(f"WARNING: no background photo for slides {missing}; plain navy used")

    for i in range(len(SLIDES)):
        render(i, 1080, 1350, os.path.join(OUT, f"slide{i + 1}.png"), bgs[i])
        render(i, 1080, 1920, os.path.join(reel_dir, f"r{i + 1}.png"), bgs[i], swipe=False)

    # reel: each slide held, cross-faded, over an original synthesized track,
    # with a voiceover when content.json has narration and a TTS key is set
    frames = [os.path.join(reel_dir, f"r{i + 1}.png") for i in range(len(SLIDES))]
    voices = None
    if NARRATION and "--no-voice" not in sys.argv:
        if not tts.available():
            sys.exit("content.json has narration but ELEVENLABS_API_KEY is not set (use --no-voice to skip)")
        voices = tts.speak_all(NARRATION, os.path.join(reel_dir, "voice"))
    if voices:
        durs = voice_durations(voices)
    elif len(SLIDES) == 6:
        durs = [3.5, 4, 4.5, 4.5, 5.5, 5.5]
    else:
        durs = [3.5] + [5.0] * (len(SLIDES) - 2) + [5.5]
    build_reel(frames, durs, os.path.join(OUT, "reel.mp4"), voices)
    print("done", OUT, "with voice" if voices else "music only")


if __name__ == "__main__":
    main()
