"""Animated weekly-news reel (hook + one sliding card per big event + recap), 1080x1920, voiced.

Usage: python3 tools/make_anim_reel.py <DIR> [--no-voice] [--voice-dir DIR_WITH_0..N_audio]

Reads <DIR>/anim.json and <DIR>/events.json, writes <DIR>/reel.mp4 (only after a successful render).
anim.json:
{
  "hook": ["IS HAFTE", "3 BADE NEWS", "GOLD aur USD hil sakte hain!"],
  "events": [  2-4 items, in time order
    {"ist": "<copied exactly from events.json>", "what": "US Retail Sales",
     "sub": "Log kitna kharch kar rahe hain?", "pairs": "USD | GOLD | EURUSD", "star": false}
  ],
  "narration": [hook line, one line per event, closing line]   (Devanagari, for the voice)
}
Day/time labels and flags are computed from "ist" + events.json; an "ist" not in events.json is an error.
"""
import json, math, os, random, shutil, subprocess, sys, tempfile
from datetime import datetime, timedelta

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import imageio_ffmpeg  # noqa: E402
import make_music  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30
FD = os.path.join(HERE, "fonts")
EMOJI_DIR = os.path.join(HERE, "emoji")
NAVY, NAVY2 = (8, 16, 38), (14, 28, 62)
YEL, WHITE, RED, GREEN, GREY = (255, 200, 0), (255, 255, 255), (235, 50, 60), (30, 200, 110), (150, 165, 195)
DAYS = ["SOMVAR", "MANGAL", "BUDH", "GURU", "SHUKRA", "SHANI", "RAVI"]
BANK_WORDS = ("FOMC", "Rate", "Monetary", "Minutes", "Fed ", "Speaks", "ECB", "BOE", "BOJ", "RBA", "Policy")
LEAD, TAIL = 0.25, 0.45
MINS = {"hook": 3.2, "event": 5.6, "end": 5.0}

_fonts = {}
def font(w, s):
    k = (w, s)
    if k not in _fonts: _fonts[k] = ImageFont.truetype(os.path.join(FD, f"Poppins-{w}.ttf"), s)
    return _fonts[k]

_emo = {}
def emo(name, size):
    k = (name, size)
    if k not in _emo:
        im = Image.open(os.path.join(EMOJI_DIR, f"{name}.png")).convert("RGBA")
        r = size / max(im.size)
        _emo[k] = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    return _emo[k]

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def back_out(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def text_layer(s, f, fill, stroke=8, pad=30):
    bb = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), s, font=f, stroke_width=stroke)
    L = Image.new("RGBA", (bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(L).text((pad - bb[0], pad - bb[1]), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    return L

def fit(s, weight, size, maxw):
    while size > 30 and ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=font(weight, size)) > maxw:
        size -= 2
    return font(weight, size)

def text_c(d, xy, s, f, fill, anchor="mm"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def pill(d, cx, cy, s, f, bg, fg, padx=34, pady=18):
    w = d.textlength(s, font=f); hh = f.size
    d.rounded_rectangle([cx - w / 2 - padx, cy - hh / 2 - pady, cx + w / 2 + padx, cy + hh / 2 + pady + 6], radius=22, fill=bg)
    text_c(d, (cx, cy + 4), s, f, fg)

def scaled_paste(img, layer, s, cx, cy):
    if s <= 0.01: return
    L = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.BICUBIC)
    img.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))

def label_for(ist):
    """Day label + time. Before 4 AM IST counts as the previous day's late night."""
    t = datetime.fromisoformat(ist)
    tm = t.strftime("%I:%M %p").lstrip("0")
    if t.hour < 4:
        p = t - timedelta(days=1)
        return f"{DAYS[p.weekday()]} DER RAAT  |  {t.day} {t.strftime('%b').upper()}", tm, f"{t.day} {t.strftime('%b').upper()}"
    return f"{DAYS[t.weekday()]}, {t.day} {t.strftime('%b').upper()}", tm, f"{t.day} {t.strftime('%b').upper()}"


class Reel:
    def __init__(self, anim, events):
        self.cards = []
        by_ist = {}
        for e in events:
            by_ist.setdefault(e["ist"], []).append(e)
        for i, c in enumerate(anim["events"]):
            if c["ist"] not in by_ist:
                sys.exit(f"anim.json event {i + 1}: ist {c['ist']} is not in events.json")
            evs = by_ist[c["ist"]]
            cur = evs[0]["currency"]
            flags = [cur if os.path.exists(os.path.join(EMOJI_DIR, f"{cur}.png")) else "bank"]
            if any(w in e["title"] for e in evs for w in BANK_WORDS) and "bank" not in flags:
                flags.append("bank")
            day, tm, short = label_for(c["ist"])
            self.cards.append(dict(c, n=str(i + 1), flags=flags, day=day, time=tm, short=short))
        self.hook = anim["hook"]
        seen = []
        for c in self.cards:
            for f in c["flags"]:
                if f not in seen: seen.append(f)
        self.hook_flags = seen[:4]
        random.seed(7); p = 100.0; self.candles = []
        for _ in range(70):
            o = p; p += random.gauss(0.25, 2.2)
            self.candles.append((o, p, max(o, p) + abs(random.gauss(0, 1.2)), min(o, p) - abs(random.gauss(0, 1.2))))
        self.lo = min(c[3] for c in self.candles); self.hi = max(c[2] for c in self.candles)
        bg = Image.new("RGB", (W, H), NAVY); d = ImageDraw.Draw(bg)
        for y in range(H):
            k = y / H
            d.line([(0, y), (W, y)], fill=tuple(int(NAVY2[i] * (1 - k) + NAVY[i] * k) for i in range(3)))
        for y in range(0, H, 120): d.line([(0, y), (W, y)], fill=(22, 38, 75))
        for x in range(0, W, 120): d.line([(x, 0), (x, H)], fill=(22, 38, 75))
        self.bg = bg.convert("RGBA")
        self.h1 = text_layer(self.hook[0], fit(self.hook[0], "ExtraBold", 110, 980), YEL)
        self.h2 = text_layer(self.hook[1], fit(self.hook[1], "ExtraBold", 150, 1000), WHITE)
        self.h3 = text_layer(self.hook[2], fit(self.hook[2], "Bold", 58, 940), WHITE, stroke=0) if len(self.hook) > 2 else None

    def set_timing(self, durs):
        names = ["hook"] + [f"e{i}" for i in range(len(self.cards))] + ["end"]
        self.scenes, acc = [], 0.0
        for nm, dd in zip(names, durs):
            self.scenes.append((nm, acc, dd)); acc += dd
        self.dur = acc

    def candles_layer(self, img, t):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        shown = min(len(self.candles), int(8 + t * 14)); cw, gap = 26, 14
        x0 = W - shown * (cw + gap) - (t * 20) % (cw + gap); top, bot = 1150, 1650
        def Y(v): return bot - (v - self.lo) / (self.hi - self.lo) * (bot - top)
        for i, (o, c, h, l) in enumerate(self.candles[:shown]):
            x = x0 + i * (cw + gap)
            if x < -40: continue
            col = (GREEN if c >= o else RED) + (56,)
            ld.line([(x + cw / 2, Y(h)), (x + cw / 2, Y(l))], fill=col, width=3)
            ld.rectangle([x, min(Y(o), Y(c)), x + cw, max(Y(o), Y(c)) + 2], fill=col)
        img.alpha_composite(layer)

    def hook_scene(self, img, t):
        d = ImageDraw.Draw(img)
        if int(t * 6) % 2 == 0 and t < 1.0:
            d.rectangle([0, 0, W, 18], fill=RED); d.rectangle([0, H - 18, W, H], fill=RED)
        scaled_paste(img, self.h1, back_out(t / 0.35), W / 2, 560)
        pulse = 1 + 0.04 * math.sin(t * 9) if t > 0.6 else back_out((t - 0.2) / 0.4)
        scaled_paste(img, self.h2, pulse, W / 2, 730)
        if self.h3 is not None and t > 0.7:
            a = ease_out((t - 0.7) / 0.3); bw = self.h3.width + 20
            box = Image.new("RGBA", (bw, self.h3.height), RED + (255,)); box.alpha_composite(self.h3, (10, 0))
            box = box.crop((0, 0, max(1, int(bw * a)), box.height))
            img.alpha_composite(box, (int(W / 2 - bw / 2), 870))
        n = len(self.hook_flags)
        for i, f in enumerate(self.hook_flags):
            s = back_out((t - 1.1 - i * 0.15) / 0.3)
            if s > 0:
                scaled_paste(img, emo(f, 150), s, W / 2 + (i - (n - 1) / 2) * 220, 1110 + 10 * math.sin(t * 5 + i))

    def card_scene(self, img, t, ev):
        d = ImageDraw.Draw(img); ox = int((1 - ease_out(t / 0.45)) * W)
        img.alpha_composite(text_layer(ev["n"], font("ExtraBold", 330), YEL + (60,), stroke=0), (int(80 + ox * 0.6), 150))
        pill(d, W / 2 + ox, 330, f"NEWS #{ev['n']}", font("ExtraBold", 44), RED, WHITE)
        cx0, cy0, cx1, cy1 = 70 + ox, 430, W - 70 + ox, 1250
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([cx0 + 10, cy0 + 16, cx1 + 10, cy1 + 16], radius=46, fill=(0, 0, 0, 120))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
        d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=46, fill=(20, 36, 78), outline=YEL, width=5)
        n = len(ev["flags"])
        for i, f in enumerate(ev["flags"]):
            s = back_out((t - 0.35 - 0.12 * i) / 0.3) * (1 + 0.06 * math.sin(t * 6 + i))
            scaled_paste(img, emo(f, 150), s, W / 2 + ox + (i - (n - 1) / 2) * 190, cy0 + 130)
        text_c(d, (W / 2 + ox, cy0 + 285), ev["day"], fit(ev["day"], "Bold", 52, 860), GREY)
        tt = ease_out((t - 0.5) / 0.35)
        tl = text_layer(ev["time"] + " IST", fit(ev["time"] + " IST", "ExtraBold", 96, 860), YEL, stroke=0)
        scaled_paste(img, tl, 0.6 + 0.4 * tt if tt > 0 else 0, W / 2 + ox, cy0 + 385)
        text_c(d, (W / 2 + ox, cy0 + 515), ev["what"], fit(ev["what"], "ExtraBold", 74, 860), WHITE)
        if t > 0.9:
            text_c(d, (W / 2 + ox, cy0 + 605), ev["sub"], fit(ev["sub"], "Medium", 46, 860), (210, 220, 240))
        text_c(d, (cx0 + 70, cy0 + 715), "IMPACT", font("Bold", 40), GREY, anchor="lm")
        for b in range(5):
            ft = clamp((t - 1.1 - b * 0.12) / 0.15); x = cx0 + 250 + b * 84; hb = 30 + b * 14
            d.rounded_rectangle([x, cy0 + 740 - hb, x + 62, cy0 + 740], radius=10, fill=(40, 58, 100))
            if ft > 0: d.rounded_rectangle([x, cy0 + 740 - hb * ft, x + 62, cy0 + 740], radius=10, fill=RED)
        if t > 1.8: pill(d, cx1 - 120, cy0 + 715, "HIGH", font("ExtraBold", 38), RED, WHITE, padx=22, pady=10)
        off = 40 if ev.get("star") else 0
        if t > 1.4:
            a = ease_out((t - 1.4) / 0.3)
            text_c(d, (W / 2 + ox, cy1 + 95 + off - 30 * (1 - a)), "Kis par asar:", font("Medium", 42), GREY)
            text_c(d, (W / 2 + ox, cy1 + 160 + off - 30 * (1 - a)), ev["pairs"], fit(ev["pairs"], "ExtraBold", 54, 940), GREEN)
        if ev.get("star") and t > 2.2:
            s = back_out((t - 2.2) / 0.3) * (1 + 0.05 * math.sin(t * 8))
            tag = text_layer("HAFTE KA SABSE BADA!", font("ExtraBold", 48), WHITE, stroke=0, pad=22)
            bx = Image.new("RGBA", tag.size, RED + (255,)); bx.alpha_composite(tag)
            scaled_paste(img, bx.rotate(-6, expand=True, resample=Image.BICUBIC), s, W / 2 + 190 + ox, cy1 + 5)

    def end_scene(self, img, t):
        d = ImageDraw.Draw(img)
        text_c(d, (W / 2, 360), "Time note kar lo!", font("ExtraBold", 84), YEL)
        for i, c in enumerate(self.cards):
            a = ease_out((t - 0.2 - 0.2 * i) / 0.35)
            if a <= 0: continue
            y = 520 + i * 150; x = int((1 - a) * -W)
            d.rounded_rectangle([70 + x, y - 58, W - 70 + x, y + 58], radius=30, fill=(20, 36, 78), outline=(60, 80, 130), width=3)
            text_c(d, (110 + x, y - 16), c["short"], font("Bold", 34), GREY, anchor="lm")
            text_c(d, (110 + x, y + 24), c["time"], font("ExtraBold", 40), YEL, anchor="lm")
            text_c(d, (W - 110 + x, y), c["what"], fit(c["what"], "ExtraBold", 48, 600), WHITE, anchor="rm")
        yb = 520 + len(self.cards) * 150 + 20
        if t > 1.0:
            scaled_paste(img, emo("pin", 100), back_out((t - 1.0) / 0.3), 230, yb)
            text_c(d, (310, yb + 5), "SAVE karo, bhoolna mat", font("ExtraBold", 54), WHITE, anchor="lm")
        if t > 1.5:
            s = back_out((t - 1.5) / 0.3) * (1 + 0.04 * math.sin(t * 7))
            cta = text_layer("FOLLOW @tradewithcaptainpravin", font("ExtraBold", 50), (10, 10, 10), stroke=0, pad=28)
            bx = Image.new("RGBA", cta.size, YEL + (255,)); bx.alpha_composite(cta)
            m = Image.new("L", bx.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bx.width, bx.height], radius=30, fill=255)
            bx.putalpha(m); scaled_paste(img, bx, s, W / 2, yb + 165)
        if t > 1.9:
            scaled_paste(img, emo("live", 56), 1, 205, yb + 310)
            text_c(d, (250, yb + 313), "Roz raat 9 baje YouTube LIVE", font("Bold", 50), WHITE, anchor="lm")
        text_c(d, (W / 2, yb + 440), "Sirf educational. Financial advice nahi. Forex trading mein high risk hai.", font("Regular", 28), GREY)

    def frame(self, t):
        img = self.bg.copy(); self.candles_layer(img, t)
        sc = next((s for s in self.scenes if s[1] <= t < s[1] + s[2]), self.scenes[-1])
        lt = t - sc[1]
        if sc[0] == "hook": self.hook_scene(img, lt)
        elif sc[0] == "end": self.end_scene(img, lt)
        else: self.card_scene(img, lt, self.cards[int(sc[0][1:])])
        d = ImageDraw.Draw(img)
        text_c(d, (60, 110), "TRADE WITH CAPTAIN PRAVIN", font("Bold", 34), YEL, anchor="lm")
        text_c(d, (W - 60, 110), "FOREX NEWS", font("Bold", 34), GREY, anchor="rm")
        d.rectangle([0, H - 16, int(W * t / self.dur), H], fill=YEL)
        for _, st, _ in self.scenes[1:]:
            if 0 <= t - st < 0.12:
                img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - (t - st) / 0.12)))))
        z = 1 + sum(0.06 * math.exp(-(t - st) * 6) for _, st, _ in self.scenes if t >= st)
        if z > 1.002:
            big = img.resize((int(W * z), int(H * z)), Image.BILINEAR)
            l, u = (big.width - W) // 2, (big.height - H) // 2
            img = big.crop((l, u, l + W, u + H))
        return img.convert("RGB")


def audio_seconds(path):
    out = subprocess.run([FFMPEG, "-i", path, "-f", "null", "-"], capture_output=True, text=True).stderr
    t = [l for l in out.split("\n") if "time=" in l][-1].split("time=")[1].split()[0]
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    args = sys.argv[1:]
    out_dir = args[0]; no_voice = "--no-voice" in args
    vdir = args[args.index("--voice-dir") + 1] if "--voice-dir" in args else None
    anim = json.load(open(os.path.join(out_dir, "anim.json"), encoding="utf-8"))
    events = json.load(open(os.path.join(out_dir, "events.json"), encoding="utf-8"))
    if not 2 <= len(anim["events"]) <= 4: sys.exit("anim.json needs 2-4 events")
    reel = Reel(anim, events)
    n_scenes = len(anim["events"]) + 2
    if len(anim.get("narration", [])) != n_scenes: sys.exit(f"narration needs {n_scenes} lines")

    with tempfile.TemporaryDirectory() as tmp:
        voices = None
        if vdir:
            voices = [os.path.join(vdir, sorted(f for f in os.listdir(vdir) if f.startswith(f"{i}."))[0]) for i in range(n_scenes)]
        elif not no_voice:
            import tts
            if not tts.available(): sys.exit("ELEVENLABS_API_KEY missing (use --no-voice to render without)")
            voices = [os.path.join(tmp, f"{i}.mp3") for i in range(n_scenes)]
            for line, p in zip(anim["narration"], voices): tts.speak(line, p)
        mins = [MINS["hook"]] + [MINS["event"]] * len(anim["events"]) + [MINS["end"]]
        durs = [max(m, LEAD + audio_seconds(v) + TAIL) for m, v in zip(mins, voices)] if voices else mins
        reel.set_timing(durs)

        music = os.path.join(tmp, "music.wav")
        make_music.main(music, reel.dur + 0.5, [s[1] for s in reel.scenes[1:]])
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", str(FPS), "-i", "-", "-i", music]
        if voices:
            for v in voices: cmd += ["-i", v]
            fc = f"[1:a]volume=0.22,afade=t=out:st={reel.dur - 1.2:.2f}:d=1.2[m];"
            for i in range(n_scenes):
                ms = int((reel.scenes[i][1] + LEAD) * 1000)
                fc += f"[{i + 2}:a]aresample=44100,adelay={ms}|{ms},volume=1.6[v{i}];"
            fc += "[m]" + "".join(f"[v{i}]" for i in range(n_scenes)) + f"amix=inputs={n_scenes + 1}:duration=first:normalize=0,alimiter=limit=0.95[a]"
        else:
            fc = f"[1:a]volume=0.9,afade=t=out:st={reel.dur - 1.2:.2f}:d=1.2[a]"
        tmp_out = os.path.join(tmp, "reel.mp4")
        cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", tmp_out]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for i in range(int(reel.dur * FPS)):
            ff.stdin.write(reel.frame(i / FPS).tobytes())
        ff.stdin.close()
        if ff.wait() != 0: sys.exit("ffmpeg failed")
        os.makedirs(os.path.join(out_dir, "check"), exist_ok=True)
        for k, (nm, st, dd) in enumerate(reel.scenes):  # one still per scene for visual QA
            reel.frame(st + min(dd - 0.2, 2.6)).save(os.path.join(out_dir, "check", f"anim{k}.jpg"), quality=80)
        shutil.move(tmp_out, os.path.join(out_dir, "reel.mp4"))
    print(f"animated reel {reel.dur:.1f}s", "with voice" if voices else "WITHOUT voice", "->", os.path.join(out_dir, "reel.mp4"))


if __name__ == "__main__":
    main()
