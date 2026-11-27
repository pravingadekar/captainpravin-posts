"""Dark 9:16 "Gold 3 levels" reel drawn from REAL daily gold candles (gold_daily.json), not an example chart.

  python tools/hf_reel_gold.py reels/<folder>
  cd reels/<folder>/hf && npx --yes hyperframes@0.9.52 render --quality delivery -o out.mp4

Needs <folder>/script.json (chapters c1..c5), voice/<id>.wav (Sarvam ratan) and gold_daily.json
{rows: [[date, open, high, low, close], ...]} (45 daily candles). Levels are set in LEVELS below and must be
re-read from the chart every time this is reused. Education only: levels to watch, never a buy/sell call.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hf_reel_dark as D  # noqa: E402
from hf_reel_dark import Reel, G, R, Y, W, T, esc, pop, ding, whoosh, riser  # noqa: E402

GOLD, ORG = "#f5c542", "#ff8a3d"
PY0, PY1, YT, YB = 3380, 4400, 470, 1390
CX0, CSTEP, CW = 50, 21.5, 14

# levels read from the 27 Nov 2026 chart
SUP_LO, SUP_HI = 3425, 3500     # Nov 20 low 3503, Nov 25 low 3425: two bounces
RES1 = 3690                     # Nov 23 high 3691, Nov 27 high 3694
RES2 = 3860                     # Nov 13-17 lows (old support), broke Nov 18
ROWS = []


def px(i):
    return CX0 + i * CSTEP


def py(p):
    return YB - (p - PY0) / (PY1 - PY0) * (YB - YT)


def idx(date):
    return next(i for i, r in enumerate(ROWS) if r[0] == date)


def candle(i):
    _, o, hi, lo, c = ROWS[i]
    col = G if c >= o else R
    x = px(i)
    top, bot = py(max(o, c)), py(min(o, c))
    return (f'<g id="k{i}" style="filter:drop-shadow(0 0 6px {col}88)">'
            f'<line x1="{x + CW / 2}" y1="{py(hi):.0f}" x2="{x + CW / 2}" y2="{py(lo):.0f}" stroke="{col}" stroke-width="3"/>'
            f'<rect x="{x}" y="{top:.0f}" width="{CW}" height="{max(bot - top, 4):.0f}" rx="2" fill="{col}"/></g>')


class GoldReel(Reel):
    def fix_chrome(self):
        self.el = [e.replace("LIVE · 15m · EXAMPLE CHART", "GOLD FUTURES · DAILY · 27 NOV")
                    .replace("Educational only • Illustrative chart • Not financial advice • AI voice",
                             "Educational only • Not financial advice • Real daily data • AI voice") for e in self.el]

    def reveal(self, i0, i1, at, dur):
        for i in range(i0, i1):
            t = at + dur * (i - i0) / max(1, i1 - i0)
            self.js.append(f'tl.fromTo("#k{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,'
                           f'duration:0.16,ease:"back.out(2)",immediateRender:false}},{T(t)});')

    def line(self, lid, price, col, label, at, anchor="start", dash="14 10", w=4):
        y = py(price)
        x = 50 if anchor == "start" else W - 50
        self.el.append(f'<svg id="{lid}" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">'
                       f'<line x1="40" y1="{y:.0f}" x2="{W - 40}" y2="{y:.0f}" stroke="{col}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
                       f'<text x="{x}" y="{y - 14:.0f}" text-anchor="{anchor}" class="ll" fill="{col}" '
                       f'style="paint-order:stroke;stroke:#000;stroke-width:8px">{esc(label)}</text></svg>')
        self.js.append(f'tl.set("#{lid}",{{opacity:0}},0);')
        self.js.append(f'tl.fromTo("#{lid}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,ease:"expo.out",immediateRender:false}},'
                       f'{T(at)});')
        self.sfx.append((whoosh(0.35), at, 0.4))

    def chart(self):
        grid = "".join(f'<line x1="40" y1="{py(p):.0f}" x2="{W - 40}" y2="{py(p):.0f}" stroke="#ffffff0d" stroke-width="2"/>'
                       f'<text x="{W - 44}" y="{py(p) - 8:.0f}" text-anchor="end" class="ax">{p}</text>'
                       for p in range(3400, 4401, 200))
        cs = "".join(candle(i) for i in range(len(ROWS)))
        self.el.append(f'<svg id="cv" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">{grid}{cs}</svg>')
        for i in range(len(ROWS)):
            self.js.append(f'tl.set("#k{i}",{{opacity:0}},0);')

    def c1(self):
        a, e = self.seg[0]
        d = e - a
        self.reveal(0, len(ROWS), 0.15, 2.0)
        hi_i, lo_i = 0, idx("2026-11-25")
        x0, y0, x1, y1 = px(hi_i) + CW / 2, py(ROWS[hi_i][2]), px(lo_i) + CW / 2, py(ROWS[lo_i][3])
        at = a + d * 0.28
        self.el.append(f'<svg id="dr1" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">'
                       f'<defs><marker id="ah1" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto">'
                       f'<path d="M0 0L8 4L0 8z" fill="{R}"/></marker></defs>'
                       f'<line id="drl" x1="{x0}" y1="{y0 - 20:.0f}" x2="{x1}" y2="{y1 + 20:.0f}" stroke="{R}" stroke-width="7" '
                       f'stroke-dasharray="1400" stroke-dashoffset="1400" marker-end="url(#ah1)" style="filter:drop-shadow(0 0 10px {R})"/></svg>')
        self.js.append(f'tl.set("#dr1",{{opacity:0}},0);')
        self.js.append(f'tl.set("#dr1",{{opacity:1}},{T(at)});')
        self.js.append(f'tl.to("#drl",{{strokeDashoffset:0,duration:0.8,ease:"power2.in"}},{T(at)});')
        self.sfx.append((riser(0.8), at, 0.45))
        self.tagbox("dt1", "−$926  (−21%)", 330, py(4000), R, at + 0.8)
        self.tagbox("tm1", "⏱ 50 SEC", 760, py(4330), GOLD, a + d * 0.78)
        self.hide("#dr1,#dt1,#tm1", e + 0.1)

    def c2(self):
        a, e = self.seg[1]
        d = e - a
        b = idx("2026-11-18")
        lo = idx("2026-11-20")
        for i in range(b + 1, len(ROWS)):
            self.js.append(f'tl.to("#k{i}",{{opacity:0,duration:0.2}},{T(a - 0.1)});')
        entry = ROWS[b][4]
        t0 = a + d * 0.42
        self.line("en2", entry, "#cbd5e1", f"इतना गिरा, BUY!  {entry:.0f}", t0, anchor="end")
        self.tagbox("by2", "↑ BUY", px(b) - 60, py(ROWS[b][2]) - 70, G, t0 + 0.2)
        t1 = t0 + 1.2
        self.reveal(b + 1, lo + 1, t1, 0.6)
        self.stamp("st2", f"−${entry - ROWS[lo][3]:.0f}", t1 + 0.7, t1 + 2.0)
        self.tagbox("ns2", "✕ NO STOP LOSS", 80, py(3450) + 40, R, a + d * 0.78)
        self.hide("#en2,#by2,#ns2", e + 0.15)
        self.reveal(lo + 1, len(ROWS), e + 0.05, 0.4)

    def c3(self):
        a, e = self.seg[2]
        d = e - a
        za = a + d * 0.04
        y0, y1 = py(SUP_HI), py(SUP_LO)
        self.el.append(f'<div id="sz3" class="sz" style="top:{y0:.0f}px;height:{y1 - y0:.0f}px"></div>'
                       f'<div id="szt" class="szl" style="top:{y1 + 10:.0f}px">1 · SUPPORT 3425–3500</div>')
        self.js.append(f'tl.fromTo("#sz3",{{opacity:0,scaleX:0}},{{opacity:1,scaleX:1,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(za)});')
        self.js.append(f'tl.fromTo("#szt",{{opacity:0}},{{opacity:1,duration:0.3,immediateRender:false}},{T(za + 0.3)});')
        self.sfx.append((ding(), za, 0.4))
        for j, dt in enumerate(("2026-11-20", "2026-11-25")):
            i = idx(dt)
            self.tagbox(f"bn3_{j}", "↑", px(i) - 12, py(ROWS[i][3]) + 4, G, za + 0.9 + 0.4 * j)
        self.line("r13", RES1, GOLD, "2 · 3690 RESISTANCE", a + d * 0.42)
        self.line("r23", RES2, ORG, "3 · 3860 पुराना SUPPORT", a + d * 0.72)

    def c4(self):
        a, e = self.seg[3]
        d = e - a
        self.js.append(f'tl.to(["#cv","#sz3","#szt","#r13","#r23","#bn3_0","#bn3_1"],{{opacity:0.15,duration:0.3}},{T(a - 0.2)});')
        self.el.append(f'<div id="rule4"><div class="r4a">⬇ 3425 के नीचे CLOSE</div><div class="r4b">= गिरावट बाकी हो सकती है</div>'
                       f'<div class="r4sep"></div><div class="r4a" style="color:{G}">⬆ 3690 के ऊपर CLOSE</div>'
                       f'<div class="r4b">= बदलाव का संकेत</div><div class="r4sep"></div>'
                       f'<div class="r4c">तब तक: SL ज़रूर · RISK <b>1–2%</b></div></div>')
        self.js.append(f'tl.fromTo("#rule4",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.5,ease:"expo.out",immediateRender:false}},'
                       f'{T(a - 0.1)});')
        parts = [("#rule4 .r4a:nth-child(1),#rule4 .r4b:nth-child(2)", 0.12),
                 ("#rule4 .r4a:nth-child(4),#rule4 .r4b:nth-child(5)", 0.45), ("#rule4 .r4c", 0.72)]
        for k, (sel, f) in enumerate(parts):
            self.js.append(f'tl.fromTo("{sel}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.3,stagger:0.12,'
                           f'immediateRender:false}},{T(a + d * f)});')
            self.sfx.append((ding() if k else pop(0.08, 500), a + d * f, 0.45))
        self.hide("#rule4", e + 0.15)

    def c5(self):
        a, e = self.seg[4]
        d = e - a
        self.js.append(f'tl.to(["#cv","#sz3","#szt","#r13","#r23","#bn3_0","#bn3_1"],{{opacity:0,duration:0.3}},{T(a - 0.2)});')
        self.el.append('<div id="end5"><div class="logo">CP</div><div class="bn">TRADE WITH<br>CAPTAIN PRAVIN</div>'
                       '<div class="ck">पहले कौन सा LEVEL? 👇</div><div class="cbox"><i></i><span id="typ"></span><u id="cur">|</u></div>'
                       '<div id="fol">+ FOLLOW</div></div>')
        self.js.append(f'tl.fromTo("#end5",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(a - 0.1)});')
        ta = a + d * 0.15
        txt = "3425 या 3690?"
        for j in range(1, len(txt) + 1):
            self.js.append(f'tl.set("#typ",{{innerHTML:"{txt[:j]}"}},{T(ta + 0.07 * j)});')
            if j % 3 == 0:
                self.sfx.append((pop(0.03, 2200), ta + 0.07 * j, 0.3))
        self.js.append(f'tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:0.3,yoyo:true,repeat:{int(d / 0.6) + 2},ease:"none",'
                       f'immediateRender:false}},{T(a)});')
        fa = a + d * 0.45
        self.js.append(f'tl.fromTo("#fol",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(fa)});')
        self.js.append(f'tl.to("#fol",{{scale:1.08,duration:0.35,yoyo:true,repeat:{int((self.total - fa) / 0.7) + 1},ease:"sine.inOut"}},'
                       f'{T(fa + 0.45)});')
        self.sfx.append((ding(), fa, 0.6))


EXTRA = f"""
#bg{{background:radial-gradient(circle at 50% 45%,#161106 0%,#080705 55%,#000 100%) !important}}
#grid{{background-image:linear-gradient(#f5c5420a 2px,transparent 2px),linear-gradient(90deg,#f5c5420a 2px,transparent 2px) !important}}
.tg{{color:{GOLD} !important}}
.tt .tk{{color:{GOLD} !important;text-shadow:0 0 26px {GOLD}88 !important}}
.ax{{font:700 24px 'Poppins';fill:#ffffff44}}
.sz{{position:absolute;left:40px;right:40px;background:linear-gradient(90deg,#22e58b10,#22e58b40,#22e58b10);
 border-top:3px solid {G};border-bottom:3px solid {G};transform-origin:0 50%;opacity:0}}
.szl{{position:absolute;left:50px;font:800 30px 'Poppins';letter-spacing:.06em;color:{G};opacity:0;
 text-shadow:0 0 8px #000,0 0 8px #000}}
#rule4{{top:470px !important;padding:44px 30px !important}}
.r4a{{font-size:64px !important}}
.r4b{{font-size:52px !important}}
.r4sep{{margin:26px 40px !important}}
.r4c{{font:900 50px 'HindiUI','Poppins';color:#fff}} .r4c b{{color:{GOLD}}}
.cbox{{font-family:'Poppins','HindiUI' !important;font-size:64px !important;border-color:{GOLD} !important}}
.cbox i{{background:{GOLD} !important}} .cbox u{{color:{GOLD} !important}}
.ck{{letter-spacing:0 !important;font:900 50px 'HindiUI','Poppins' !important;color:#ffffffcc !important}}
"""


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    ROWS.extend(json.load(open(os.path.join(folder, "gold_daily.json")))["rows"])
    D.CSS += EXTRA
    D.KEYS = ["सोना", "डॉलर", "गलती", "स्टॉप", "लॉस", "सपोर्ट", "रेज़िस्टेंस", "लेवल", "क्लोज़", "रिस्क", "कमेंट",
              "फ़ॉलो", "कन्फ़र्मेशन", "बाउंस", "जल्दबाज़ी"]
    r = GoldReel(folder, s)
    r.chrome()
    r.fix_chrome()
    r.chart()
    r.c1(); r.c2(); r.c3(); r.c4(); r.c5()
    r.captions()
    r.write(D.music(folder))


if __name__ == "__main__":
    main()
