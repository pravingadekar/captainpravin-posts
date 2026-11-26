"""Dark 9:16 "X vs Y" reel with a countdown-timer hook (reference-library patterns 1, 2, 4: black bg, big candles,
pill tags, 50-SEC timer, trapped-trader icons, TRAPPED stamp, side-by-side compare cards, comment CTA).

  python tools/hf_reel_vs.py reels/<folder>
  cd reels/<folder>/hf && npx --yes hyperframes@0.9.52 render --quality delivery -o out.mp4

script.json: chapters c1 (hook), c2 (fake), c3 (real), c4 (compare), c5 (CTA); voice/<id>.wav. First use: fake vs real breakout.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hf_reel_dark as D  # noqa: E402
from hf_reel_dark import Reel, G, R, Y, W, T, esc, pop, ding, boom, whoosh, riser  # noqa: E402

O = "#ff8a3d"
RES, SUP = 60.0, 50.0
PY0, PY1, YT, YB = 40, 84, 470, 1290
VY = 1365                     # volume baseline
CX0, CSTEP, CW = 50, 47, 34

BASE = [(55, 58), (58, 54), (54, 57), (57, 59.5), (59.5, 56), (56, 52), (52, 55), (55, 51), (51, 54), (54, 57),
        (57, 55), (55, 57.5)]                                     # range under resistance (12 candles)
FAKE = [(57.5, 62.5, 64.5), (62.5, 56, None), (56, 53, None), (53, 49, None), (49, 50.5, None), (50.5, 46, None),
        (46, 44, None), (44, 42.5, None), (42.5, 43.5, None)]     # (open, close, high override)
REAL = [(57.5, 66, None), (66, 68.5, None), (68.5, 65, None), (65, 61.5, None), (61.5, 66.5, None), (66.5, 70, None),
        (70, 74, None), (74, 77, None), (77, 81, None)]
FAKE_VOL = [40, 35, 45, 38, 42, 36, 40, 44, 38, 41, 37, 40] + [48, 70, 55, 50, 40, 45, 38, 35, 36]
REAL_VOL = [40, 35, 45, 38, 42, 36, 40, 44, 38, 41, 37, 40] + [130, 90, 55, 50, 75, 80, 70, 72, 68]
BO = 12                                                           # breakout candle index


def px(i):
    return CX0 + i * CSTEP


def py(p):
    return YB - (p - PY0) / (PY1 - PY0) * (YB - YT)


def series(tail):
    out = []
    for k, (o, c) in enumerate(BASE):
        out.append((o, c, max(o, c) + 0.9, min(o, c) - 0.9))
    for o, c, hi in tail:
        out.append((o, c, hi if hi else max(o, c) + 0.9, min(o, c) - 0.9))
    return out


def candle_svg(gid, i, o, c, hi, lo):
    col = G if c >= o else R
    x = px(i)
    top, bot = py(max(o, c)), py(min(o, c))
    return (f'<g id="{gid}" style="filter:drop-shadow(0 0 8px {col}88)">'
            f'<line x1="{x + CW / 2}" y1="{py(hi):.0f}" x2="{x + CW / 2}" y2="{py(lo):.0f}" stroke="{col}" stroke-width="4"/>'
            f'<rect x="{x}" y="{top:.0f}" width="{CW}" height="{max(bot - top, 5):.0f}" rx="4" fill="{col}"/></g>')


def person(x, y, pid):
    return (f'<g transform="translate({x},{y})"><g id="{pid}"><circle cx="0" cy="-22" r="11" fill="#fff"/>'
            f'<path d="M-17 12 Q-17 -8 0 -8 Q17 -8 17 12 Z" fill="#fff"/></g></g>')


class VS(Reel):
    def chart(self, k, data, vols, show_at, hide_at, n_build, build_dur):
        grid = "".join(f'<line x1="40" y1="{y:.0f}" x2="{W - 40}" y2="{y:.0f}" stroke="#ffffff0d" stroke-width="2"/>'
                       for y in [py(p) for p in range(40, 86, 6)])
        cs = "".join(candle_svg(f"k{k}_{i}", i, *d) for i, d in enumerate(data))
        vb = "".join(f'<rect id="v{k}_{i}" x="{px(i) + 4}" y="{VY - v * 0.75:.0f}" width="{CW - 8}" height="{v * 0.75:.0f}" '
                     f'rx="3" fill="{G if data[i][1] >= data[i][0] else R}" opacity="0.45"/>' for i, v in enumerate(vols))
        res = (f'<rect x="40" y="{py(RES) - 10:.0f}" width="{W - 80}" height="20" fill="#ffffff10"/>'
               f'<line x1="40" y1="{py(RES):.0f}" x2="{W - 40}" y2="{py(RES):.0f}" stroke="#e2e8f0" stroke-width="4" '
               f'stroke-dasharray="16 12"/><text x="46" y="{py(RES) - 22:.0f}" class="ll" fill="#e2e8f0">RESISTANCE</text>'
               f'<text x="46" y="{VY + 34}" class="ll" fill="#ffffff55" style="font-size:24px">VOLUME</text>')
        self.el.append(f'<svg id="cv{k}" class="chart" width="{W}" height="{1920}" viewBox="0 0 {W} 1920">{grid}{res}{vb}{cs}</svg>')
        self.js.append(f'tl.set("#cv{k}",{{opacity:0}},0);')
        self.js.append(f'tl.to("#cv{k}",{{opacity:1,duration:0.25}},{T(show_at)});')
        for i in range(len(data)):
            if i >= n_build:
                self.js.append(f'tl.set(["#k{k}_{i}","#v{k}_{i}"],{{opacity:0}},0);')
            else:
                at = show_at + build_dur * i / n_build
                self.js.append(f'tl.fromTo(["#k{k}_{i}","#v{k}_{i}"],{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},'
                               f'{{opacity:1,scaleY:1,duration:0.16,ease:"back.out(2)",immediateRender:false}},{T(at)});')
        self.js.append(f'tl.to("#cv{k}",{{opacity:0,duration:0.25}},{T(hide_at)});')
        self.js.append(f'tl.set("#cv{k}",{{visibility:"hidden"}},{T(hide_at + 0.26)});')

    def show(self, k, i, at, op=0.45, big=False):
        self.js.append(f'tl.fromTo("#k{k}_{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,'
                       f'duration:{0.35 if big else 0.16},ease:"back.out(2)",immediateRender:false}},{T(at)});')
        self.js.append(f'tl.fromTo("#v{k}_{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:{op},scaleY:1,'
                       f'duration:0.25,immediateRender:false}},{T(at)});')
        self.sfx.append((pop(0.05, 700 if big else 1100), at, 0.5 if big else 0.25))

    # ---------------------------------------------------------------- hook: 50 SEC timer
    def timer(self):
        a, e = self.seg[0]
        n = 50
        self.el.append(f'<div id="tm"><svg width="170" height="170" viewBox="0 0 170 170">'
                       f'<circle cx="85" cy="85" r="74" fill="#0b0b0b" stroke="#ffffff22" stroke-width="10"/>'
                       f'<circle id="tmr" cx="85" cy="85" r="74" fill="none" stroke="{Y}" stroke-width="10" stroke-linecap="round" '
                       f'transform="rotate(-90 85 85)" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0"/></svg>'
                       f'<div id="tmn">{n}</div><div id="tms">SEC</div><div id="tmk"></div></div>')
        # big in the centre for the hook, then flies to the corner and keeps ticking
        self.js.append('tl.fromTo("#tm",{x:-420,y:520,scale:0},{x:-420,y:520,scale:2.6,duration:0.45,ease:"back.out(2)"},0.1);')
        self.sfx.append((boom(), 0.15, 0.7))
        fly = e - 0.6
        self.js.append(f'tl.to("#tm",{{x:0,y:0,scale:1,duration:0.6,ease:"power3.inOut"}},{T(fly)});')
        self.sfx.append((whoosh(0.5), fly, 0.6))
        tick = (self.total - 1.0 - 0.5) / n
        for j in range(1, n + 1):
            self.js.append(f'tl.set("#tmn",{{innerHTML:"{n - j}"}},{T(0.5 + tick * j)});')
        self.js.append(f'tl.to("#tmr",{{strokeDashoffset:100,duration:{tick * n:.2f},ease:"none"}},0.5);')
        # hook text: FAKE vs REAL badges under the big timer
        self.el.append(f'<div id="vsb"><span style="background:{R}">FAKE</span><b>vs</b><span style="background:{G};color:#04120b">'
                       f'REAL</span></div>')
        self.js.append(f'tl.fromTo("#vsb span,#vsb b",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,stagger:0.18,'
                       f'ease:"back.out(3)",immediateRender:false}},{T(a + 1.2)});')
        self.js.append(f'tl.to("#vsb",{{opacity:0,y:-30,duration:0.3}},{T(fly)});')
        self.sfx.append((pop(0.08, 600), a + 1.2, 0.6))
        self.sfx.append((pop(0.08, 1400), a + 1.56, 0.6))

    def fake(self):
        a, e = self.seg[1]
        d = e - a
        data = series(FAKE)
        self.chart(2, data, FAKE_VOL, a - 0.3, e + 0.1, BO, 1.0)
        bo = a + d * 0.18
        self.show(2, BO, bo, 0.45, big=True)
        self.tagbox("bm2", "✕ BIGGEST MISTAKE: तुरंत BUY", px(BO) - 330, py(66) - 30, R, bo + 0.5, e)
        # trapped buyers above the breakout
        ppl = "".join(person(px(BO) - 150 + 62 * j, py(70), f"pp{j}") for j in range(6))
        self.el.append(f'<svg id="ppl" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">{ppl}</svg>')
        self.js.append('tl.set("#ppl",{opacity:1},0);')
        for j in range(6):
            at = bo + 0.6 + 0.1 * j
            self.js.append(f'tl.set("#pp{j}",{{opacity:0}},0);')
            self.js.append(f'tl.fromTo("#pp{j}",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.25,ease:"back.out(3)",'
                           f'immediateRender:false}},{T(at)});')
            self.sfx.append((pop(0.04, 1500 + 60 * j), at, 0.25))
        self.tagbox("lv2", "VOLUME कम ⚠", px(BO) - 60, VY - 120, O, a + d * 0.45, e)
        back = a + d * 0.62
        self.show(2, BO + 1, back, 0.45, big=True)
        self.js.append(f'tl.to("#ppl path,#ppl circle",{{fill:"{R}",duration:0.15}},{T(back + 0.2)});')
        self.stamp("st2", "TRAPPED", back + 0.25, back + 1.6, col=O, top=640)
        for j, i in enumerate(range(BO + 2, len(data))):
            self.show(2, i, back + 1.0 + 0.22 * j)
        self.hide("#ppl", e)

    def real(self):
        a, e = self.seg[2]
        d = e - a
        data = series(REAL)
        self.chart(3, data, REAL_VOL, a - 0.3, e + 0.1, BO, 0.8)
        bo = a + d * 0.2
        self.show(3, BO, bo, 0.9, big=True)
        self.tagbox("cl3", "✓ CLOSE ऊपर", px(BO) - 120, py(70) - 20, G, bo + 0.4, e)
        self.tagbox("vl3", "✓ VOLUME ↑", px(BO) + 60, VY - 160, G, a + d * 0.38, e)
        self.sfx.append((ding(), a + d * 0.38, 0.4))
        for j, i in enumerate(range(BO + 1, BO + 4)):
            self.show(3, i, a + d * 0.5 + 0.35 * j)
        rt = a + d * 0.5 + 1.1
        self.el.append(f'<svg id="rr3" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">'
                       f'<circle cx="{px(BO + 3) + CW / 2}" cy="{py(60.6):.0f}" r="52" fill="none" stroke="{G}" stroke-width="7" '
                       f'style="filter:drop-shadow(0 0 12px {G})"/></svg>')
        self.js.append('tl.set("#rr3",{opacity:0},0);')
        self.js.append(f'tl.fromTo("#rr3",{{opacity:0,scale:2,svgOrigin:"{px(BO + 3) + CW / 2} {py(60.6):.0f}"}},{{opacity:1,scale:1,'
                       f'duration:0.35,ease:"back.out(2)",immediateRender:false}},{T(rt)});')
        self.tagbox("rt3", "✓ RETEST HOLD", px(BO + 3) - 110, py(55.5), G, rt + 0.15, e)
        self.sfx.append((ding(), rt, 0.5))
        for j, i in enumerate(range(BO + 4, len(data))):
            self.show(3, i, rt + 0.6 + 0.25 * j)
        self.sfx.append((riser(1.2), rt + 0.4, 0.35))
        self.hide("#rr3", e)

    def compare(self):
        a, e = self.seg[3]
        d = e - a
        rows = [("विक ऊपर, क्लोज़ अंदर", "क्लोज़ ऊपर"), ("वॉल्यूम कम", "वॉल्यूम ज़्यादा"), ("तुरंत वापस अंदर", "रीटेस्ट होल्ड")]
        fk = "".join(f'<div class="cr" id="fr{j}">✕ {esc(f)}</div>' for j, (f, _) in enumerate(rows))
        rl = "".join(f'<div class="cr" id="rl{j}">✓ {esc(r)}</div>' for j, (_, r) in enumerate(rows))
        self.el.append(f'<div id="cmp"><div class="cc" id="ccf" style="border-color:{R}"><div class="ch" style="background:{R}">FAKE</div>'
                       f'<svg width="200" height="190" viewBox="0 0 200 190"><line x1="0" y1="80" x2="200" y2="80" stroke="#fff" '
                       f'stroke-width="3" stroke-dasharray="10 8"/><line x1="70" y1="20" x2="70" y2="150" stroke="{G}" stroke-width="4"/>'
                       f'<rect x="56" y="70" width="28" height="60" fill="{G}" rx="3"/><rect x="120" y="85" width="28" height="80" '
                       f'fill="{R}" rx="3"/></svg>{fk}</div>'
                       f'<div class="cc" id="ccr" style="border-color:{G}"><div class="ch" style="background:{G};color:#04120b">REAL</div>'
                       f'<svg width="200" height="190" viewBox="0 0 200 190"><line x1="0" y1="110" x2="200" y2="110" stroke="#fff" '
                       f'stroke-width="3" stroke-dasharray="10 8"/><rect x="30" y="40" width="28" height="90" fill="{G}" rx="3"/>'
                       f'<rect x="90" y="70" width="28" height="40" fill="{R}" rx="3"/><rect x="150" y="10" width="28" height="100" '
                       f'fill="{G}" rx="3"/></svg>{rl}</div></div>')
        self.js.append(f'tl.fromTo("#ccf",{{opacity:0,x:-200,rotation:-6}},{{opacity:1,x:0,rotation:0,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(a - 0.1)});')
        self.js.append(f'tl.fromTo("#ccr",{{opacity:0,x:200,rotation:6}},{{opacity:1,x:0,rotation:0,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(a + 0.15)});')
        self.sfx.append((whoosh(0.4), a - 0.1, 0.5))
        for j in range(3):
            at = a + d * (0.2 + 0.17 * j)
            self.js.append(f'tl.fromTo(["#fr{j}","#rl{j}"],{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,stagger:0.12,'
                           f'ease:"back.out(2)",immediateRender:false}},{T(at)});')
            self.sfx.append((pop(0.06, 1000 + 150 * j), at, 0.4))
        self.el.append(f'<div id="slw">+ स्टॉप लॉस हमेशा 🛡️</div>')
        self.js.append(f'tl.fromTo("#slw",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(a + d * 0.75)});')
        self.sfx.append((ding(), a + d * 0.75, 0.5))
        self.hide("#cmp,#slw", e + 0.1)

    def cta(self):
        a, e = self.seg[4]
        d = e - a
        self.el.append(f'<div id="end5"><div class="logo">CP</div><div class="bn">TRADE WITH<br>CAPTAIN PRAVIN</div>'
                       f'<div class="ck" style="letter-spacing:0;font:900 44px HindiUI">कमेंट करो 👇</div><div class="cbox" style="text-align:center;font-family:HindiUI">'
                       f'फँसे हो? <span style="color:{G}">हाँ</span> / <span style="color:{R}">ना</span></div>'
                       f'<div class="row5"><div id="sv5">📌 SAVE</div><div id="fol">+ FOLLOW</div></div></div>')
        self.js.append(f'tl.fromTo("#end5",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.5,ease:"expo.out",'
                       f'immediateRender:false}},{T(a - 0.1)});')
        sa = a + d * 0.42
        self.js.append(f'tl.fromTo("#sv5",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(sa)});')
        self.js.append(f'tl.fromTo("#fol",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(sa + 0.5)});')
        self.js.append(f'tl.to("#fol",{{scale:1.08,duration:0.35,yoyo:true,repeat:{int((e - sa) / 0.7) + 1},ease:"sine.inOut"}},'
                       f'{T(sa + 0.9)});')
        self.sfx.append((ding(), sa, 0.5))
        self.sfx.append((pop(0.06, 1500), sa + 0.5, 0.5))


EXTRA = f"""
.hd{{right:250px}}
.tt .tk.g{{color:{G};text-shadow:0 0 26px {G}88}}
#tm{{position:absolute;left:870px;top:110px;width:170px;height:170px;transform-origin:50% 50%}}
#tm svg{{position:absolute;left:0;top:0}}
#tmn{{position:absolute;left:0;right:0;top:30px;text-align:center;font:900 72px/1 'Poppins';color:#fff}}
#tms{{position:absolute;left:0;right:0;top:104px;text-align:center;font:800 24px 'Poppins';letter-spacing:.2em;color:{Y}}}
#vsb{{position:absolute;left:0;right:0;top:1180px;text-align:center;font:900 96px 'Poppins'}}
#vsb span{{display:inline-block;padding:6px 34px 12px;border-radius:24px;color:#fff;margin:0 14px}}
#vsb b{{display:inline-block;color:#ffffffaa;font-size:64px}}
#cmp{{position:absolute;left:40px;right:40px;top:420px;display:flex;gap:28px}}
.cc{{flex:1;border:5px solid;border-radius:34px;background:#0b0f0d;padding:0 0 26px;text-align:center;overflow:hidden;opacity:0}}
.ch{{font:900 64px 'Poppins';color:#fff;padding:10px 0 14px;margin-bottom:18px}}
.cc svg{{display:block;margin:0 auto 10px}}
.cr{{font:900 40px/1.25 'HindiUI';color:#fff;padding:14px 18px;border-top:2px solid #ffffff1a;opacity:0}}
#slw{{position:absolute;left:0;right:0;top:1250px;margin:auto;width:max-content;padding:12px 40px;border-radius:24px;
 background:{Y};color:#0b0b0b;font:900 56px 'HindiUI';opacity:0}}
.row5{{display:flex;gap:30px;justify-content:center;margin-top:60px}}
#sv5{{padding:20px 50px;border-radius:24px;background:#ffffff;color:#0b0b0b;font:900 56px 'Poppins';opacity:0}}
.row5 #fol{{margin-top:0}}
#bg{{background:radial-gradient(circle at 50% 45%,#111 0%,#060606 55%,#000 100%) !important}}
#grid{{opacity:.5}}
"""


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    D.CSS += EXTRA
    r = VS(folder, s)
    r.chrome()
    # green "Real" keyword in titles
    r.el = [x.replace('<span class="tk">Real?</span>', '<span class="tk g">Real?</span>')
             .replace('<span class="tk">Real</span>', '<span class="tk g">Real</span>') for x in r.el]
    r.timer(); r.fake(); r.real(); r.compare(); r.cta()
    r.captions()
    r.write(D.music(folder))


if __name__ == "__main__":
    main()
