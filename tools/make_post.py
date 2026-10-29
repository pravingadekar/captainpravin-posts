"""Render a 6-slide carousel (1080x1350) and a reel (1080x1920) for one post."""
import os
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = sys.argv[1]

NAVY_TOP = (12, 27, 54)
NAVY_BOT = (5, 13, 30)
GOLD = (245, 184, 46)
WHITE = (255, 255, 255)
MUTED = (170, 184, 208)
CARD = (20, 40, 75)
RED = (232, 93, 93)
GREEN = (88, 201, 128)
HANDLE = "@tradewithcaptainpravin"


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{weight}.ttf"), size)


# Each slide: list of blocks. Block kinds: tag, title, text, box, compare, cta, disclaimer
SLIDES = [
    [
        ("tag", "FOREX BASICS"),
        ("title", "90% Traders Account Kyun Uda Dete Hain?"),
        ("text", "Strategy nahi... RISK galat hota hai."),
        ("box", "Aaj seekho: 1% Risk Rule"),
    ],
    [
        ("tag", "PROBLEM"),
        ("title", "Account Udne Ke 3 Reason"),
        ("list", [
            "Bada lot size, chhota account",
            "Stop loss lagaya hi nahi",
            "Loss ke baad revenge trade",
        ]),
        ("text", "Ek bura din poora mahina kha jaata hai."),
    ],
    [
        ("tag", "THE RULE"),
        ("title", "1% Risk Rule Kya Hai?"),
        ("text", "Ek trade mein account ka maximum 1% hi risk karo."),
        ("box", "$1,000 account  =  max $10 risk / trade"),
        ("text", "Stop loss hit hua? Sirf 1% gaya. Account zinda hai."),
    ],
    [
        ("tag", "MATHS DEKHO"),
        ("title", "Lagatar 10 Loss Ke Baad"),
        ("compare", [
            ("1% risk / trade", "~90% account bacha", GREEN),
            ("10% risk / trade", "~35% account bacha", RED),
        ]),
        ("text", "Same 10 loss. Farak sirf risk size ka."),
    ],
    [
        ("tag", "LOT SIZE"),
        ("title", "Lot Size Kaise Nikaalein?"),
        ("box", "Lot = Risk $ ÷ (SL pips × pip value)"),
        ("list", [
            "Account $1,000, risk 1% = $10",
            "Stop loss 20 pips (EURUSD)",
            "0.01 lot = $0.10 / pip",
            "$10 ÷ (20 × $0.10) = 5 micro = 0.05 lot",
        ]),
    ],
    [
        ("tag", "AAPKI BAARI"),
        ("title", "Aap Ek Trade Mein Kitna % Risk Lete Ho?"),
        ("text", "Comment mein batao. Honest answer chahiye!"),
        ("cta", "Follow karo aur daily forex seekho"),
        ("disclaimer", "Disclaimer: Sirf educational content. Financial advice nahi. "
                       "Forex/CFD trading mein high risk hai, aapka paisa doob sakta hai."),
    ],
]


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def background(w, h):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        d.line([(0, y), (w, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(NAVY_TOP, NAVY_BOT)))
    # subtle gold accents
    d.rectangle([0, 0, w, 10], fill=GOLD)
    for i in range(6):
        x = w - 220 + i * 34
        d.rectangle([x, 60 + i * 6, x + 14, 130 - i * 4], fill=(30, 52, 90))
    return img


def render(idx, w, h, swipe=True):
    img = background(w, h)
    d = ImageDraw.Draw(img)
    pad = 90
    inner = w - 2 * pad

    d.text((pad, 60), "TRADE WITH CAPTAIN PRAVIN", font=font("SemiBold", 28), fill=GOLD)
    d.text((pad, 98), f"{idx + 1} / {len(SLIDES)}", font=font("Medium", 26), fill=MUTED)

    # measure content, then centre it vertically
    blocks = SLIDES[idx]
    ops, y = [], 0
    for kind, val in blocks:
        if kind == "tag":
            f = font("Bold", 30)
            tw = d.textlength(val, font=f)
            ops.append(("pill", y, val, f, tw))
            y += 90
        elif kind == "title":
            f = font("ExtraBold", 74)
            for ln in wrap(d, val, f, inner):
                ops.append(("line", y, ln, f, WHITE))
                y += 92
            ops.append(("rule", y + 10))
            y += 60
        elif kind == "text":
            f = font("Regular", 40)
            for ln in wrap(d, val, f, inner):
                ops.append(("line", y, ln, f, MUTED))
                y += 58
            y += 30
        elif kind == "list":
            f = font("Medium", 40)
            for item in val:
                lines = wrap(d, item, f, inner - 70)
                ops.append(("dot", y))
                for ln in lines:
                    ops.append(("line_x", y, ln, f, WHITE, pad + 60))
                    y += 58
                y += 22
            y += 20
        elif kind in ("box", "cta"):
            f = font("Bold", 42)
            lines = wrap(d, val, f, inner - 80)
            bh = len(lines) * 60 + 60
            ops.append(("box", y, lines, f, bh, kind))
            y += bh + 40
        elif kind == "compare":
            for label, result, col in val:
                ops.append(("cmp", y, label, result, col))
                y += 190
            y += 20
        elif kind == "disclaimer":
            f = font("Regular", 26)
            for ln in wrap(d, val, f, inner):
                ops.append(("line", y, ln, f, MUTED))
                y += 38
    top = max(170, (h - y) // 2 + 20)

    for op in ops:
        kind, oy = op[0], op[1] + top
        if kind == "pill":
            _, _, txt, f, tw = op
            d.rounded_rectangle([pad, oy, pad + tw + 48, oy + 56], radius=28, fill=GOLD)
            d.text((pad + 24, oy + 8), txt, font=f, fill=NAVY_BOT)
        elif kind == "line":
            _, _, txt, f, col = op
            d.text((pad, oy), txt, font=f, fill=col)
        elif kind == "line_x":
            _, _, txt, f, col, x = op
            d.text((x, oy), txt, font=f, fill=col)
        elif kind == "dot":
            d.ellipse([pad + 8, oy + 20, pad + 30, oy + 42], fill=GOLD)
        elif kind == "rule":
            d.rectangle([pad, oy, pad + 140, oy + 8], fill=GOLD)
        elif kind == "box":
            _, _, lines, f, bh, bk = op
            if bk == "cta":
                d.rounded_rectangle([pad, oy, w - pad, oy + bh], radius=24, fill=GOLD)
                col = NAVY_BOT
            else:
                d.rounded_rectangle([pad, oy, w - pad, oy + bh], radius=24, fill=CARD, outline=GOLD, width=4)
                col = GOLD
            for i, ln in enumerate(lines):
                d.text((pad + 40, oy + 30 + i * 60), ln, font=f, fill=col)
        elif kind == "cmp":
            _, _, label, result, col = op
            d.rounded_rectangle([pad, oy, w - pad, oy + 160], radius=24, fill=CARD)
            d.rectangle([pad, oy + 20, pad + 10, oy + 140], fill=col)
            d.text((pad + 50, oy + 24), label, font=font("Medium", 36), fill=MUTED)
            d.text((pad + 50, oy + 72), result, font=font("ExtraBold", 54), fill=col)

    # footer
    d.line([(pad, h - 130), (w - pad, h - 130)], fill=(40, 62, 100), width=2)
    d.text((pad, h - 105), HANDLE, font=font("SemiBold", 34), fill=GOLD)
    if swipe and idx < len(SLIDES) - 1:
        f = font("Medium", 30)
        s = "Swipe  >"
        d.text((w - pad - d.textlength(s, font=f), h - 100), s, font=f, fill=MUTED)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    reel_dir = os.path.join(HERE, "reel_frames")
    os.makedirs(reel_dir, exist_ok=True)
    for i in range(len(SLIDES)):
        render(i, 1080, 1350).save(os.path.join(OUT, f"slide{i + 1}.png"), optimize=True)
        render(i, 1080, 1920, swipe=False).save(os.path.join(reel_dir, f"r{i + 1}.png"))

    # reel: each slide held, cross-faded, with a silent audio track
    durs = [3.5, 4, 4.5, 4.5, 5.5, 5.5]
    fade = 0.5
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff, "-y", "-loglevel", "error"]
    for i, dur in enumerate(durs):
        cmd += ["-loop", "1", "-t", str(dur), "-i", os.path.join(reel_dir, f"r{i + 1}.png")]
    cmd += ["-f", "lavfi", "-t", str(sum(durs) - fade * (len(durs) - 1)),
            "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    parts, prev, offset = [], "[0:v]", 0.0
    for i in range(1, len(durs)):
        offset += durs[i - 1] - fade
        label = f"[v{i}]"
        parts.append(f"{prev}[{i}:v]xfade=transition=fade:duration={fade}:offset={offset:.2f}{label}")
        prev = label
    parts.append(f"{prev}format=yuv420p,fps=30[vout]")
    cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{len(durs)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-movflags", "+faststart", os.path.join(OUT, "reel.mp4")]
    subprocess.run(cmd, check=True)
    print("done", OUT)


if __name__ == "__main__":
    main()
