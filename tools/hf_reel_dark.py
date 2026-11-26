"""Dark 9:16 explainer reel (neon candles, chapter progress, stamp, step chips, comment CTA) as one HyperFrames project.

  python tools/hf_reel_dark.py reels/<folder>
  cd reels/<folder>/hf && npx --yes hyperframes@0.9.52 render --quality delivery -o out.mp4

Needs <folder>/script.json {chapters:[{id, tag, title, text}] x5} and voice/<id>.wav (Sarvam ratan).
First reel: "Stop loss हर बार क्यों हिट होता है?" (c1 trap, c2 stop cluster sweep, c3 3-step smart SL, c4 risk rule, c5 CTA).
"""
import json, math, os, random, shutil, subprocess, sys, wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hf_lesson import load_wav, trim, pop, whoosh, ding, riser, boom, word_times, esc, T, SR  # noqa: E402

W, H = 1080, 1920
G, R, Y, MUT = "#22e58b", "#ff3b5c", "#fbbf24", "#64748b"
KEYS = ["स्टॉप", "लॉस", "ट्रैप", "विक", "बफ़र", "क्लोज़", "लॉट", "रिस्क", "एस", "एल।", "कमेंट", "फ़ॉलो", "किस्मत", "ऑर्डर"]
GAP = 0.35

# ---------------------------------------------------------------- candle series (price units)
# up leg -> pullback to swing low (55) -> bounce (entry) -> sweep wick to 48 -> rally
OPENS = [30, 33, 32, 36, 39, 38, 43, 46, 45, 50, 54, 53, 58, 62, 66, 64, 61, 58, 56, 57, 60, 63, 62, 59, 58, 64, 70, 76, 82, 88]
CLOSES = OPENS[1:] + [93]
SWING, SWEEP_I, ENTRY_I = 17, 23, 21
LOWS = [min(o, c) - 1.2 for o, c in zip(OPENS, CLOSES)]
HIGHS = [max(o, c) + 1.2 for o, c in zip(OPENS, CLOSES)]
LOWS[SWING] = 55.0
LOWS[SWEEP_I] = 47.5           # the stop-hunt wick
CX0, CSTEP, CW = 60, 32, 24
PY0, PY1, YT, YB = 27, 96, 440, 1380
SL_NAIVE, SL_SMART = 53.0, 44.0


def px(i):
    return CX0 + i * CSTEP


def py(p):
    return YB - (p - PY0) / (PY1 - PY0) * (YB - YT)


def candle(gid, i):
    o, c, lo, hi = OPENS[i], CLOSES[i], LOWS[i], HIGHS[i]
    col = G if c >= o else R
    x = px(i)
    top, bot = py(max(o, c)), py(min(o, c))
    return (f'<g id="{gid}" style="filter:drop-shadow(0 0 6px {col}88)">'
            f'<line x1="{x + CW / 2}" y1="{py(hi):.0f}" x2="{x + CW / 2}" y2="{py(lo):.0f}" stroke="{col}" stroke-width="3"/>'
            f'<rect x="{x}" y="{top:.0f}" width="{CW}" height="{max(bot - top, 4):.0f}" rx="3" fill="{col}"/></g>')


class Reel:
    def __init__(self, folder, s):
        self.folder, self.s = folder, s
        self.voices = [trim(load_wav(os.path.join(folder, "voice", f"{c['id']}.wav"))) for c in s["chapters"]]
        self.seg, t = [], 0.45
        for v in self.voices:
            self.seg.append((t, t + v.size / SR))
            t += v.size / SR + GAP
        self.total = round(t + 0.9, 2)
        self.el, self.js, self.sfx = [], [], []

    # ---------------------------------------------------------- chrome
    def chrome(self):
        n = len(self.seg)
        segw = (W - 120 - 12 * (n - 1)) / n
        for k in range(n):
            self.el.append(f'<div class="pg" style="left:{60 + k * (segw + 12):.0f}px;width:{segw:.0f}px">'
                           f'<div id="pf{k}" class="pf"></div></div>')
            a = self.seg[k][0] - 0.2
            b = self.seg[k + 1][0] - 0.2 if k + 1 < n else self.total
            self.js.append(f'tl.fromTo("#pf{k}",{{scaleX:0}},{{scaleX:1,duration:{b - a:.2f},ease:"none"}},{T(a)});')
        self.el.append('<div id="brand">TRADE WITH CAPTAIN PRAVIN</div>')
        self.el.append('<div id="disc">Educational only • Illustrative chart • Not financial advice • AI voice</div>')
        for k, c in enumerate(self.s["chapters"]):
            a = self.seg[k][0] - 0.3
            b = self.seg[k + 1][0] - 0.3 if k + 1 < n else self.total + 1
            words = c["title"].split()
            tw = " ".join(f'<span class="{"tk" if "*" in w else ""}">{esc(w.replace("*", ""))}</span>' for w in words)
            live = '<div class="live"><i></i>LIVE · 15m · EXAMPLE CHART</div>' if k < 3 else ""
            self.el.append(f'<div id="hd{k}" class="hd"><div class="tg">{esc(c["tag"])}</div>'
                           f'<div class="tt">{tw}</div>{live}</div>')
            self.js.append(f'tl.fromTo("#hd{k}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.35,ease:"expo.out",'
                           f'immediateRender:false}},{T(max(a, 0.05))});')
            self.js.append(f'tl.fromTo("#hd{k} .tt span",{{opacity:0,y:24,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",'
                           f'duration:0.3,stagger:0.07,ease:"expo.out",immediateRender:false}},{T(max(a, 0.05) + 0.1)});')
            if k + 1 < n:
                self.js.append(f'tl.to("#hd{k}",{{opacity:0,y:-20,duration:0.2}},{T(b - 0.2)});')
                self.js.append(f'tl.set("#hd{k}",{{visibility:"hidden"}},{T(b)});')
            if k:
                self.sfx.append((whoosh(0.4), a, 0.55))

    def captions(self, top=1470):
        for i, c in enumerate(self.s["chapters"]):
            wt = word_times(c["text"], *self.seg[i])
            groups, cur = [], []
            for wd in wt:
                cur.append(wd)
                if len(cur) >= 3 or wd[0].endswith((",", "।", "?", "!")):
                    groups.append(cur)
                    cur = []
            if cur:
                groups.append(cur)
            for g, grp in enumerate(groups):
                gid = f"cp{i}_{g}"
                self.el.append(f'<div id="{gid}" class="cap" style="top:{top}px">' + " ".join(
                    f'<span id="{gid}_{k}">{esc(w)}</span>' for k, (w, a, b) in enumerate(grp)) + "</div>")
                g0 = grp[0][1] - 0.04
                nxt = groups[g + 1][0][1] - 0.04 if g + 1 < len(groups) else grp[-1][2] + 0.25
                self.js.append(f'tl.fromTo("#{gid}",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.12,ease:"back.out(2)",'
                               f'immediateRender:false}},{T(g0)});')
                for k, (w, a, b) in enumerate(grp):
                    col = Y if any(x in w for x in KEYS) else "#ffffff"
                    self.js.append(f'tl.to("#{gid}_{k}",{{color:"{col}",duration:0.05}},{T(a)});')
                self.js.append(f'tl.to("#{gid}",{{opacity:0,duration:0.06}},{T(nxt - 0.06)});')
                self.js.append(f'tl.set("#{gid}",{{visibility:"hidden"}},{T(nxt)});')

    def particles(self, at, cx, cy, n=26, cols=(R, Y, "#ff8a3d")):
        rng = random.Random(int(at * 1000))
        for k in range(n):
            pid = f"pt{int(at * 100)}_{k}"
            ang, dist = rng.uniform(0, 2 * math.pi), rng.uniform(120, 420)
            self.el.append(f'<div id="{pid}" class="pt" style="left:{cx}px;top:{cy}px;background:{rng.choice(cols)}"></div>')
            self.js.append(f'tl.fromTo("#{pid}",{{x:0,y:0,opacity:1,scale:1}},{{x:{dist * math.cos(ang):.0f},'
                           f'y:{dist * math.sin(ang):.0f},opacity:0,scale:0.3,duration:0.9,ease:"power3.out",immediateRender:false}},{T(at)});')

    def stamp(self, sid, text, at, until, col=R, top=760):
        zig = " ".join(f"{x},{0 if (x // 40) % 2 == 0 else 46}" for x in range(0, W + 41, 40))
        self.el.append(f'<div id="{sid}" class="stamp" style="top:{top}px">'
                       f'<svg class="teeth" width="{W}" height="46" viewBox="0 0 {W} 46"><polyline points="{zig}" fill="none" '
                       f'stroke="{col}" stroke-width="6"/></svg>'
                       f'<div class="sw" style="color:{col};text-shadow:0 0 30px {col}">{esc(text)}</div>'
                       f'<svg class="teeth" width="{W}" height="46" viewBox="0 0 {W} 46"><polyline points="{zig}" fill="none" '
                       f'stroke="{col}" stroke-width="6"/></svg></div>')
        self.js.append(f'tl.fromTo("#{sid}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.22,ease:"power4.out",'
                       f'immediateRender:false}},{T(at)});')
        self.js.append(f'tl.fromTo("#{sid} .sw",{{x:-10}},{{x:10,duration:0.04,yoyo:true,repeat:9,ease:"none",'
                       f'immediateRender:false}},{T(at + 0.2)});')
        self.js.append(f'tl.fromTo("#stage",{{x:0,y:0}},{{x:16,y:-10,duration:0.04,yoyo:true,repeat:7,ease:"none",'
                       f'immediateRender:false}},{T(at)});')
        self.js.append(f'tl.to("#{sid}",{{opacity:0,scale:0.9,duration:0.25}},{T(until)});')
        self.sfx.append((boom(), at, 0.9))
        self.particles(at + 0.05, W // 2, top + 110)

    def tagbox(self, tid, text, x, y, col, at, until=None):
        self.el.append(f'<div id="{tid}" class="tagb" style="left:{x:.0f}px;top:{y:.0f}px;color:{col};border-color:{col};'
                       f'box-shadow:0 0 18px {col}66">{esc(text)}</div>')
        self.js.append(f'tl.fromTo("#{tid}",{{opacity:0,y:16,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(2.5)",'
                       f'immediateRender:false}},{T(at)});')
        self.sfx.append((pop(0.06, 1300), at, 0.4))
        if until:
            self.js.append(f'tl.to("#{tid}",{{opacity:0,duration:0.2}},{T(until)});')

    # ---------------------------------------------------------- chapters
    def chart_group(self, k, upto, show_at, hide_at, build=True, build_dur=1.6):
        """Candles 0..upto-1 in group k. build=True pops them in one by one."""
        cs = "".join(candle(f"c{k}_{i}", i) for i in range(len(OPENS)))
        grid = "".join(f'<line x1="40" y1="{y}" x2="{W - 40}" y2="{y}" stroke="#ffffff10" stroke-width="2"/>'
                       for y in range(YT, YB + 1, 110))
        self.el.append(f'<svg id="ch{k}" class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{grid}'
                       f'<g id="ex{k}"></g>{cs}<g id="ov{k}"></g></svg>')
        self.js.append(f'tl.set("#ch{k}",{{opacity:0}},0);')
        self.js.append(f'tl.to("#ch{k}",{{opacity:1,duration:0.25}},{T(show_at)});')
        for i in range(len(OPENS)):
            if i >= upto:
                self.js.append(f'tl.set("#c{k}_{i}",{{opacity:0}},0);')
            elif build:
                at = show_at + build_dur * i / upto
                self.js.append(f'tl.fromTo("#c{k}_{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,'
                               f'duration:0.18,ease:"back.out(2)",immediateRender:false}},{T(at)});')
        self.js.append(f'tl.to("#ch{k}",{{opacity:0,duration:0.25}},{T(hide_at)});')
        self.js.append(f'tl.set("#ch{k}",{{visibility:"hidden"}},{T(hide_at + 0.26)});')

    def reveal(self, k, i0, i1, at, dur):
        for i in range(i0, i1):
            t = at + dur * (i - i0) / max(1, i1 - i0)
            self.js.append(f'tl.fromTo("#c{k}_{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,'
                           f'duration:0.16,ease:"back.out(2)",immediateRender:false}},{T(t)});')

    def hline(self, hid, k, price, col, label, at, dash="14 10", x1=40, x2=W - 40, w=4):
        y = py(price)
        self.el.append(f'<svg id="{hid}" class="chart" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                       f'<line x1="{x1}" y1="{y:.0f}" x2="{x2}" y2="{y:.0f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
                       f'<text x="{x1 + 6}" y="{y - 12:.0f}" class="ll" fill="{col}">{esc(label)}</text></svg>')
        self.js.append(f'tl.set("#{hid}",{{opacity:0}},0);')
        self.js.append(f'tl.fromTo("#{hid}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"expo.out",immediateRender:false}},'
                       f'{T(at)});')

    def hide(self, sel, at):
        self.js.append(f'tl.to("{sel}",{{opacity:0,duration:0.2}},{T(at)});')

    def c1(self):
        a, e = self.seg[0]
        d = e - a
        self.chart_group(1, ENTRY_I + 1, 0.15, e + GAP - 0.1, build_dur=1.4)
        self.hline("sl1", 1, SL_NAIVE, R, "YOUR SL", 1.0)
        self.tagbox("buy1", "↑ BUY", px(ENTRY_I) - 30, py(HIGHS[ENTRY_I]) - 70, G, 1.4)
        hit = a + d * 0.42
        self.reveal(1, ENTRY_I + 1, SWEEP_I + 1, hit - 0.5, 0.45)
        self.stamp("st1", "SL HIT", hit, hit + 1.3)
        self.reveal(1, SWEEP_I + 1, len(OPENS), hit + 1.3, 1.4)
        self.tagbox("ny1", "+ बिना आपके 😩", px(26) - 120, py(95) - 10, Y, hit + 2.0)
        self.hide("#sl1,#buy1,#ny1", e + GAP - 0.15)

    def c2(self):
        a, e = self.seg[1]
        d = e - a
        self.chart_group(2, SWING + 4, a - 0.15, e + GAP - 0.1, build=False)
        # stop cluster: many little SL chips under the swing low
        rng = random.Random(7)
        za = a + d * 0.2
        zone_y = py(SL_NAIVE + 1.5)
        self.el.append(f'<div id="zone2" class="zone" style="top:{zone_y:.0f}px;height:{py(48.5) - zone_y:.0f}px"></div>')
        self.js.append(f'tl.fromTo("#zone2",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:0.4,ease:"expo.out",'
                       f'immediateRender:false}},{T(za)});')
        for j in range(14):
            x = px(SWING) - 300 + (j % 7) * 96 + rng.uniform(-8, 8)
            yy = py(SL_NAIVE + 0.6) + (j // 7) * 56 + rng.uniform(-6, 6)
            cid = f"sl2_{j}"
            self.el.append(f'<div id="{cid}" class="slc" style="left:{x:.0f}px;top:{yy:.0f}px">SL</div>')
            at = za + 0.25 + 0.09 * j
            self.js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.2,ease:"back.out(3)",'
                           f'immediateRender:false}},{T(at)});')
            self.sfx.append((pop(0.04, 900 + 50 * j), at, 0.25))
        self.tagbox("lb2", "STOP CLUSTER", px(SWING) - 210, py(46) + 20, R, za + 1.4)
        sweep = a + d * 0.66
        self.reveal(2, SWING + 4, SWEEP_I + 1, sweep - 0.6, 0.55)
        self.js.append(f'tl.to(".slc",{{opacity:0,scale:1.8,duration:0.25,stagger:0.02}},{T(sweep)});')
        self.particles(sweep, int(px(SWEEP_I)), int(py(50)), 20)
        self.sfx.append((boom(), sweep, 0.6))
        self.tagbox("of2", "ORDERS FILLED ✓", px(SWEEP_I) - 120, py(PY1) + 20, Y, sweep + 0.15)
        self.reveal(2, SWEEP_I + 1, len(OPENS), sweep + 0.7, 1.4)
        self.tagbox("up2", "↑ वापस ऊपर", px(27) - 160, py(80), G, sweep + 1.6)
        self.hide("#zone2,#lb2,#of2,#up2", e + GAP - 0.15)

    def c3(self):
        a, e = self.seg[2]
        d = e - a
        steps = [("BUFFER", 0.12), ("CLOSE", 0.42), ("LOT SIZE", 0.70)]
        self.el.append('<div id="steps">' + "".join(
            f'<div id="sp{j}" class="sp"><b id="sk{j}">{j + 1}</b>{s}</div>' for j, (s, _) in enumerate(steps)) + "</div>")
        self.js.append(f'tl.fromTo("#steps",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{T(a - 0.1)});')
        self.chart_group(3, ENTRY_I + 1, a - 0.1, e + GAP - 0.1, build=False)
        self.hline("sl3n", 3, SL_NAIVE, "#ff3b5c66", "पुराना SL", a + 0.2)
        for j, (s, f) in enumerate(steps):
            at = a + d * f
            self.js.append(f'tl.to("#sp{j}",{{background:"#22e58b22",borderColor:"{G}",color:"#ffffff",duration:0.2}},{T(at)});')
            self.js.append(f'tl.set("#sk{j}",{{innerHTML:"✓"}},{T(at)});')
            self.js.append(f'tl.fromTo("#sk{j}",{{scale:0.3}},{{scale:1,duration:0.3,ease:"back.out(3)",immediateRender:false}},{T(at)});')
            self.sfx.append((ding(), at, 0.35))
        # step 1: smart SL below the structure with a buffer zone
        t1 = a + d * 0.12 + 0.3
        self.hline("sl3", 3, SL_SMART, G, "SMART SL (बफ़र)", t1)
        bz = py(LOWS[SWING])
        self.el.append(f'<div id="buf3" class="buf" style="top:{bz:.0f}px;height:{py(SL_SMART) - bz:.0f}px"></div>')
        self.js.append(f'tl.fromTo("#buf3",{{opacity:0}},{{opacity:1,duration:0.4,immediateRender:false}},{T(t1 + 0.2)});')
        # step 2: entry only after a close
        t2 = a + d * 0.42 + 0.3
        self.tagbox("cl3", "✓ CLOSE के बाद ENTRY", px(ENTRY_I) - 180, py(HIGHS[ENTRY_I]) - 80, G, t2)
        self.reveal(3, ENTRY_I + 1, SWEEP_I + 1, t2 + 0.6, 0.5)
        self.tagbox("sf3", "SL SAFE ✓", px(SWEEP_I) + 40, py(LOWS[SWEEP_I]) - 10, G, t2 + 1.25)
        self.reveal(3, SWEEP_I + 1, len(OPENS), t2 + 1.5, 1.2)
        # step 3: lot size card
        t3 = a + d * 0.70 + 0.3
        self.el.append(f'<div id="lot3" class="lot"><div>SL बड़ा ➜ <span style="color:{Y}">LOT छोटा</span></div>'
                       f'<div class="rk">RISK <b>1–2%</b></div></div>')
        self.js.append(f'tl.fromTo("#lot3",{{opacity:0,scale:0.6,y:40}},{{opacity:1,scale:1,y:0,duration:0.5,ease:"elastic.out(1,0.6)",'
                       f'immediateRender:false}},{T(t3)});')
        self.hide("#steps,#sl3,#sl3n,#buf3,#cl3,#sf3,#lot3", e + GAP - 0.15)

    def c4(self):
        a, e = self.seg[3]
        d = e - a
        self.el.append(f'<div id="rule4"><div class="r4a">❌ SL हटाया</div><div class="r4b">= बड़ा नुकसान</div>'
                       f'<div class="r4sep"></div><div class="r4a" style="color:{G}">✅ सही SL + छोटा रिस्क</div>'
                       f'<div class="r4b">= मार्केट में टिके रहो</div></div>')
        self.js.append(f'tl.fromTo("#rule4",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},'
                       f'{T(a - 0.1)});')
        self.js.append(f'tl.fromTo("#rule4 .r4a:first-child,#rule4 .r4b:nth-child(2)",{{opacity:0,x:-40}},{{opacity:1,x:0,'
                       f'duration:0.3,stagger:0.15,immediateRender:false}},{T(a + 0.1)});')
        self.js.append(f'tl.fromTo("#rule4 .r4a:nth-child(4),#rule4 .r4b:nth-child(5)",{{opacity:0,x:-40}},{{opacity:1,x:0,'
                       f'duration:0.3,stagger:0.15,immediateRender:false}},{T(a + d * 0.45)});')
        self.sfx.append((pop(0.08, 500), a + 0.1, 0.5))
        self.sfx.append((ding(), a + d * 0.45, 0.5))
        self.hide("#rule4", e + GAP - 0.15)

    def c5(self):
        a, e = self.seg[4]
        d = e - a
        self.el.append('<div id="end5"><div class="logo">CP</div><div class="bn">TRADE WITH<br>CAPTAIN PRAVIN</div>'
                       '<div class="ck">COMMENT KARO</div><div class="cbox"><i></i><span id="typ"></span><u id="cur">|</u></div>'
                       '<div id="fol">+ FOLLOW</div></div>')
        self.js.append(f'tl.fromTo("#end5",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(a - 0.1)});')
        ta = a + d * 0.3
        for j, ch in enumerate(["S", "SL"]):
            self.js.append(f'tl.set("#typ",{{innerHTML:"{ch}"}},{T(ta + 0.25 * j)});')
            self.sfx.append((pop(0.03, 2200), ta + 0.25 * j, 0.35))
        self.js.append(f'tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:0.3,yoyo:true,repeat:{int(d / 0.6) + 2},ease:"none",'
                       f'immediateRender:false}},{T(a)});')
        fa = a + d * 0.55
        self.js.append(f'tl.fromTo("#fol",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(fa)});')
        self.js.append(f'tl.to("#fol",{{scale:1.08,duration:0.35,yoyo:true,repeat:{int((e - fa) / 0.7) + 1},ease:"sine.inOut"}},'
                       f'{T(fa + 0.45)});')
        self.sfx.append((ding(), fa, 0.6))

    # ---------------------------------------------------------- output
    def write(self, music):
        proj = os.path.join(self.folder, "hf")
        os.makedirs(os.path.join(proj, "assets", "fonts"), exist_ok=True)
        for f in ("Poppins-SemiBold.ttf", "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"):
            shutil.copy(os.path.join(HERE, "fonts", f), os.path.join(proj, "assets", "fonts", f))
        n = int(self.total * SR)
        vo, fx = np.zeros(n, np.float32), np.zeros(n, np.float32)
        for (a, _), v in zip(self.seg, self.voices):
            i = int(a * SR)
            vo[i:i + v.size] += v[: max(0, n - i)]
        for snd, at, g in self.sfx:
            i = max(int(at * SR), 0)
            j = min(i + snd.size, n)
            if j > i:
                fx[i:j] += snd[: j - i] * g
        m = np.tile(music, n // music.size + 1)[:n]
        m = m * (0.15 / max(np.abs(m).max(), 1e-6))
        k = int(0.25 * SR)
        cs = np.concatenate([[0.0], np.cumsum((np.abs(vo) > 0.02).astype(np.float64))])
        idx = np.arange(n)
        env = ((cs[np.clip(idx + k // 2, 0, n)] - cs[np.clip(idx - k // 2, 0, n)]) / k).astype(np.float32)
        mix = vo + fx * 0.5 + m * (1 - 0.6 * np.clip(env * 3, 0, 1))
        fade = int(0.6 * SR)
        mix[-fade:] *= np.linspace(1, 0, fade)
        mix /= max(1.0, np.abs(mix).max() / 0.97)
        with wave.open(os.path.join(proj, "assets", "mix.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((mix * 32767).astype(np.int16).tobytes())
        doc = f"""<!doctype html>
<html lang="hi"><head><meta charset="UTF-8" /><meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{self.total}" data-width="{W}" data-height="{H}">
<div id="stage" class="clip" data-start="0" data-duration="{self.total}" data-track-index="0" style="position:absolute;inset:0">
<div id="bg"></div><div id="grid"></div>
{chr(10).join(self.el)}
</div>
<audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{self.total}" data-track-index="1" data-volume="1"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(self.js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body></html>
"""
        with open(os.path.join(proj, "index.html"), "w", encoding="utf-8") as f:
            f.write(doc)
        print(f"wrote {proj} ({self.total}s, {len(self.js)} tweens)")


CSS = f"""
@font-face{{font-family:'Poppins';src:url('assets/fonts/Poppins-SemiBold.ttf');font-weight:500 600}}
@font-face{{font-family:'Poppins';src:url('assets/fonts/Poppins-Bold.ttf');font-weight:700}}
@font-face{{font-family:'Poppins';src:url('assets/fonts/Poppins-ExtraBold.ttf');font-weight:800 900}}
@font-face{{font-family:'HindiUI';src:local('Nirmala UI Bold'),local('NirmalaUI-Bold'),local('Nirmala UI');font-weight:700 900}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#050b09}}
#root{{position:relative;width:100%;height:100%;overflow:hidden;font-family:'Poppins','HindiUI',sans-serif}}
#bg{{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#0d2a1f 0%,#07130e 45%,#040807 100%)}}
#grid{{position:absolute;inset:0;background-image:linear-gradient(#22e58b0d 2px,transparent 2px),
 linear-gradient(90deg,#22e58b0d 2px,transparent 2px);background-size:72px 72px}}
.pg{{position:absolute;top:70px;height:8px;border-radius:8px;background:#ffffff1f;overflow:hidden}}
.pf{{width:100%;height:100%;background:{G};transform-origin:0 50%;transform:scaleX(0);box-shadow:0 0 12px {G}}}
#brand{{position:absolute;left:0;right:0;top:1770px;text-align:center;font:800 28px 'Poppins';letter-spacing:.2em;color:#ffffff88}}
#disc{{position:absolute;left:0;right:0;top:1830px;text-align:center;font:600 24px 'Poppins';color:#ffffff66}}
.hd{{position:absolute;left:60px;right:60px;top:120px;opacity:0}}
.tg{{font:700 30px 'Poppins';letter-spacing:.18em;color:{G}}}
.tt{{font-family:'Poppins','HindiUI';font-weight:900;font-size:92px;line-height:1.12;color:#fff;margin-top:14px}}
.tt span{{display:inline-block;margin-right:22px}}
.tt .tk{{color:{R};text-shadow:0 0 26px {R}88}}
.live{{margin-top:18px;font:700 26px 'Poppins';letter-spacing:.14em;color:#ffffffaa}}
.live i{{display:inline-block;width:16px;height:16px;border-radius:50%;background:{R};margin-right:12px;box-shadow:0 0 12px {R}}}
.chart{{position:absolute;left:0;top:0}}
.ll{{font:800 30px 'Poppins','HindiUI';letter-spacing:.08em}}
.cap{{position:absolute;left:40px;right:40px;text-align:center;font-family:'HindiUI';font-weight:900;font-size:96px;
 line-height:1.2;color:{MUT};opacity:0;text-shadow:0 6px 24px #000}}
.cap span{{display:inline-block;margin:0 10px}}
.stamp{{position:absolute;left:0;width:{W}px;text-align:center;opacity:0}}
.teeth{{display:block}}
.sw{{font:900 220px/1.05 'Poppins';letter-spacing:.02em}}
.pt{{position:absolute;width:16px;height:16px;border-radius:3px;opacity:0}}
.tagb{{position:absolute;padding:8px 20px;border-radius:12px;border:3px solid;background:#050b09dd;
 font:800 32px 'Poppins','HindiUI';letter-spacing:.04em;opacity:0;white-space:nowrap}}
.zone{{position:absolute;left:60px;right:60px;background:linear-gradient(90deg,#ff3b5c00,#ff3b5c33,#ff3b5c00);
 border-top:3px dashed {R};transform-origin:0 50%;opacity:0}}
.slc{{position:absolute;padding:4px 12px;border-radius:8px;background:{R};color:#fff;font:900 26px 'Poppins';opacity:0;
 box-shadow:0 0 14px {R}}}
#steps{{position:absolute;left:60px;right:60px;top:400px;display:flex;gap:18px;opacity:0}}
.sp{{flex:1;padding:14px 0;text-align:center;border:3px solid #ffffff33;border-radius:40px;color:#ffffff99;
 font:800 32px 'Poppins'}}
.sp b{{display:inline-block;width:42px;height:42px;line-height:42px;border-radius:50%;background:{G};color:#04120b;
 margin-right:12px;font-size:26px}}
.buf{{position:absolute;left:60px;right:60px;background:#22e58b1f;border-bottom:3px solid {G};opacity:0}}
.lot{{position:absolute;left:90px;right:90px;top:1190px;padding:26px 30px;border-radius:30px;background:#0b1f17;
 border:4px solid {G};text-align:center;font:900 58px 'HindiUI','Poppins';color:#fff;box-shadow:0 0 40px {G}55;opacity:0}}
.lot .rk{{font:800 40px 'Poppins';color:#ffffffaa;margin-top:8px}}
.lot .rk b{{color:{G}}}
#rule4{{position:absolute;left:70px;right:70px;top:520px;padding:50px 40px;border-radius:40px;background:#0b1712;
 border:4px solid #ffffff22;text-align:center;opacity:0}}
.r4a{{font:900 76px 'HindiUI','Poppins';color:{R}}}
.r4b{{font:800 60px 'HindiUI';color:#fff;margin:6px 0 10px}}
.r4sep{{height:4px;background:#ffffff22;margin:34px 40px}}
#end5{{position:absolute;left:0;right:0;top:330px;text-align:center;opacity:0}}
.logo{{width:220px;height:220px;margin:0 auto;border-radius:50%;background:#0b1f17;border:6px solid {G};
 font:900 100px/206px 'Poppins';color:{G};box-shadow:0 0 60px {G}66}}
.bn{{font:900 60px/1.15 'Poppins';color:#fff;margin:30px 0 70px;letter-spacing:.04em}}
.ck{{font:800 34px 'Poppins';letter-spacing:.3em;color:#ffffff88;margin-bottom:20px}}
.cbox{{width:760px;margin:0 auto;padding:30px 40px;border-radius:60px;border:4px solid {G};background:#0b1f17;text-align:left;
 font:900 70px 'Poppins';color:#fff;box-shadow:0 0 40px {G}44}}
.cbox i{{display:inline-block;width:44px;height:44px;border-radius:50%;background:{G};margin-right:26px;vertical-align:middle}}
.cbox u{{text-decoration:none;color:{G}}}
#fol{{display:inline-block;margin-top:70px;padding:20px 70px;border-radius:24px;background:{R};color:#fff;font:900 60px 'Poppins';
 opacity:0;box-shadow:0 0 40px {R}88}}
"""


def music(folder):
    mp = os.path.join(folder, "hf", "music.wav")
    if not os.path.exists(mp):
        os.makedirs(os.path.dirname(mp), exist_ok=True)
        soft = os.path.join(os.path.dirname(os.path.dirname(HERE)), "motivation-posts", "tools", "soft_music.py")
        subprocess.run([sys.executable, soft, mp, "60"], check=True)
    return load_wav(mp)


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    r = Reel(folder, s)
    r.chrome()
    r.c1(); r.c2(); r.c3(); r.c4(); r.c5()
    r.captions()
    r.write(music(folder))


if __name__ == "__main__":
    main()
