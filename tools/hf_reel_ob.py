"""Dark 9:16 order-block explainer reel + "free tool" teaser (site name hidden) + like-goal / comment-keyword CTA.

  python tools/hf_reel_ob.py reels/<folder>
  cd reels/<folder>/hf && npx --yes hyperframes@0.9.52 render --quality delivery -o out.mp4

Needs script.json chapters c1..c5, voice/<id>.wav, and shots/ (ob.png, flow_anim.mp4, bubbles_anim.mp4) cropped so the
site's name/logo never shows.
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hf_reel_dark as D  # noqa: E402
from hf_reel_dark import Reel, G, R, Y, W, T, esc, pop, ding, boom, whoosh, riser  # noqa: E402

GOLD = "#f5c542"
PY0, PY1, YT, YB = 48, 96, 470, 1300
CX0, CSTEP, CW = 46, 38, 26

# (open, close) — downtrend, OB candle (10), displacement, return into zone, confirmation (20), rally
OC = [(82, 80), (80, 77.5), (77.5, 78.5), (78.5, 75), (75, 72), (72, 73), (73, 69), (69, 66), (66, 67), (67, 62),
      (62, 58),                                           # 10 = order block (last red before the move)
      (58, 66), (66, 74), (74, 81), (81, 86),             # 11-14 displacement
      (86, 83.5), (83.5, 80), (80, 74.5), (74.5, 68.5), (68.5, 61.5),   # 15-19 back into the zone
      (61.5, 67),                                         # 20 confirmation
      (67, 71.5), (71.5, 76), (76, 81.5), (81.5, 87), (87, 92.5)]       # 21-25 rally
OB = 10
CONF = 20
OB_HI, OB_LO = 62.8, 57.2
LOW_OVR = {19: 59.0}


def px(i):
    return CX0 + i * CSTEP


def py(p):
    return YB - (p - PY0) / (PY1 - PY0) * (YB - YT)


def candle(i):
    o, c = OC[i]
    hi = max(o, c) + 0.8
    lo = LOW_OVR.get(i, min(o, c) - 0.8)
    if i == OB:
        hi, lo = OB_HI, OB_LO
    col = G if c >= o else R
    x = px(i)
    top, bot = py(max(o, c)), py(min(o, c))
    return (f'<g id="k{i}" style="filter:drop-shadow(0 0 8px {col}88)">'
            f'<line x1="{x + CW / 2}" y1="{py(hi):.0f}" x2="{x + CW / 2}" y2="{py(lo):.0f}" stroke="{col}" stroke-width="4"/>'
            f'<rect x="{x}" y="{top:.0f}" width="{CW}" height="{max(bot - top, 5):.0f}" rx="4" fill="{col}"/></g>')


class OBReel(Reel):
    def reveal(self, i0, i1, at, dur, big=False):
        for i in range(i0, i1):
            t = at + dur * (i - i0) / max(1, i1 - i0)
            self.js.append(f'tl.fromTo("#k{i}",{{opacity:0,scaleY:0.1,transformOrigin:"50% 100%"}},{{opacity:1,scaleY:1,'
                           f'duration:{0.3 if big else 0.16},ease:"back.out(2)",immediateRender:false}},{T(t)});')
            if big:
                self.sfx.append((pop(0.06, 700), t, 0.4))

    def card(self, cid, html, x, y, col, at, until):
        self.el.append(f'<div id="{cid}" class="pc" style="left:{x:.0f}px;top:{y:.0f}px;border-color:{col};'
                       f'box-shadow:0 0 30px {col}55">{html}</div>')
        self.js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:0.5,y:30}},{{opacity:1,scale:1,y:0,duration:0.4,ease:"back.out(2.5)",'
                       f'immediateRender:false}},{T(at)});')
        self.js.append(f'tl.to("#{cid}",{{opacity:0,duration:0.2}},{T(until)});')
        self.sfx.append((pop(0.07, 900), at, 0.45))

    def chart(self):
        grid = "".join(f'<line x1="40" y1="{py(p):.0f}" x2="{W - 40}" y2="{py(p):.0f}" stroke="#ffffff0d" stroke-width="2"/>'
                       for p in range(50, 97, 6))
        zone = (f'<rect id="obz" x="{px(OB) - 6}" y="{py(OB_HI):.0f}" width="{W - 40 - px(OB) + 6}" height="{py(OB_LO) - py(OB_HI):.0f}" '
                f'fill="{GOLD}22" stroke="{GOLD}" stroke-width="3" stroke-dasharray="12 8"/>'
                f'<text id="obt" x="{W - 50}" y="{py(OB_LO) + 40:.0f}" text-anchor="end" class="ll" fill="{GOLD}">BULLISH ORDER BLOCK</text>')
        ring = (f'<circle id="obr" cx="{px(OB) + CW / 2}" cy="{py(60):.0f}" r="44" fill="none" stroke="{GOLD}" stroke-width="7" '
                f'style="filter:drop-shadow(0 0 12px {GOLD})"/>')
        cr = (f'<circle id="cfr" cx="{px(CONF) + CW / 2}" cy="{py(64):.0f}" r="48" fill="none" stroke="{G}" stroke-width="7" '
              f'style="filter:drop-shadow(0 0 12px {G})"/>')
        sl = (f'<g id="slg"><line x1="{px(OB) - 6}" y1="{py(OB_LO - 1.6):.0f}" x2="{W - 40}" y2="{py(OB_LO - 1.6):.0f}" stroke="{R}" '
              f'stroke-width="4" stroke-dasharray="14 10"/><text x="{px(OB) - 6}" y="{py(OB_LO - 1.6) + 38:.0f}" text-anchor="start" '
              f'class="ll" fill="{R}">STOP LOSS</text></g>')
        disp = (f'<g id="dsp"><path d="M{px(11) - 10} {py(60):.0f} Q {px(13)} {py(70):.0f} {px(14) + 20} {py(90):.0f}" fill="none" '
                f'stroke="{G}" stroke-width="6" stroke-dasharray="14 10" marker-end="url(#ah)"/></g>')
        defs = f'<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="{G}"/></marker></defs>'
        cs = "".join(candle(i) for i in range(len(OC)))
        self.el.append(f'<svg id="cv" class="chart" width="{W}" height="1920" viewBox="0 0 {W} 1920">{defs}{grid}{zone}{sl}{cs}'
                       f'{ring}{cr}{disp}</svg>')
        for sel in ["#obz", "#obt", "#obr", "#cfr", "#slg", "#dsp"] + [f"#k{i}" for i in range(len(OC))]:
            self.js.append(f'tl.set("{sel}",{{opacity:0}},0);')

    def c1(self):
        a, e = self.seg[0]
        d = e - a
        self.reveal(0, OB + 1, 0.15, 1.3)
        self.reveal(OB + 1, 15, a + d * 0.3, 0.8, big=True)
        self.js.append(f'tl.fromTo("#dsp",{{opacity:0}},{{opacity:1,duration:0.4,immediateRender:false}},{T(a + d * 0.45)});')
        self.sfx.append((riser(1.0), a + d * 0.2, 0.4))
        self.card("sm1", f'🏦 SMART MONEY<br><b style="color:{G}">BUY 10,00,000</b>', 520, py(60) + 70, G, a + d * 0.55, e + 0.2)
        self.js.append(f'tl.to("#dsp",{{opacity:0,duration:0.2}},{T(e + 0.2)});')

    def c2(self):
        a, e = self.seg[1]
        d = e - a
        r = a + d * 0.12
        self.js.append(f'tl.fromTo("#obr",{{opacity:0,scale:2.2,svgOrigin:"{px(OB) + CW / 2} {py(60):.0f}"}},{{opacity:1,scale:1,'
                       f'duration:0.4,ease:"back.out(2)",immediateRender:false}},{T(r)});')
        self.js.append(f'tl.to("#k{OB}",{{scale:1.25,svgOrigin:"{px(OB) + CW / 2} {py(60):.0f}",duration:0.25,yoyo:true,repeat:3}},{T(r)});')
        self.sfx.append((ding(), r, 0.5))
        self.tagbox("lc2", "आख़िरी लाल कैंडल", px(OB) - 120, py(OB_LO) + 70, GOLD, r + 0.3, e)
        zt = a + d * 0.66
        self.js.append(f'tl.fromTo("#obz",{{opacity:0,scaleX:0,svgOrigin:"{px(OB)} {py(60):.0f}"}},{{opacity:1,scaleX:1,duration:0.7,'
                       f'ease:"expo.out",immediateRender:false}},{T(zt)});')
        self.js.append(f'tl.fromTo("#obt",{{opacity:0}},{{opacity:1,duration:0.3,immediateRender:false}},{T(zt + 0.5)});')
        self.sfx.append((whoosh(0.5), zt, 0.6))
        self.js.append(f'tl.to("#obr",{{opacity:0,duration:0.3}},{T(e)});')

    def c3(self):
        a, e = self.seg[2]
        d = e - a
        self.reveal(15, 20, a + 0.1, d * 0.4)
        self.card("rt3", f'👤 RETAIL<br><b style="color:{R}">डरकर SELL</b>', 80, py(OB_LO) + 90, R, a + d * 0.55, e + 0.1)
        self.card("sm3", f'🏦 SMART MONEY<br><b style="color:{G}">यहीं BUY</b>', 600, py(OB_LO) + 90, G, a + d * 0.72, e + 0.1)
        self.js.append(f'tl.to("#obz",{{fill:"{GOLD}55",duration:0.3,yoyo:true,repeat:3}},{T(a + d * 0.45)});')
        self.sfx.append((boom(), a + d * 0.45, 0.5))

    def c4(self):
        a, e = self.seg[3]
        d = e - a
        steps = [("CONFIRMATION", 0.30), ("SL नीचे", 0.55), ("RISK 1-2%", 0.78)]
        self.el.append('<div id="steps">' + "".join(
            f'<div id="sp{j}" class="sp"><b id="sk{j}">{j + 1}</b>{esc(s)}</div>' for j, (s, _) in enumerate(steps)) + "</div>")
        self.js.append(f'tl.fromTo("#steps",{{opacity:0,y:-20}},{{opacity:1,y:0,duration:0.3,immediateRender:false}},{T(a - 0.1)});')
        self.tagbox("nw4", "✕ हर OB काम नहीं करता", 90, py(52) + 60, R, a + 0.3, a + d * 0.3)
        for j, (s, f) in enumerate(steps):
            at = a + d * f
            self.js.append(f'tl.to("#sp{j}",{{background:"#22e58b22",borderColor:"{G}",color:"#ffffff",duration:0.2}},{T(at)});')
            self.js.append(f'tl.set("#sk{j}",{{innerHTML:"✓"}},{T(at)});')
            self.sfx.append((ding(), at, 0.35))
        c1 = a + d * 0.30
        self.reveal(CONF, CONF + 1, c1, 0.1, big=True)
        self.js.append(f'tl.fromTo("#cfr",{{opacity:0,scale:2,svgOrigin:"{px(CONF) + CW / 2} {py(64):.0f}"}},{{opacity:1,scale:1,'
                       f'duration:0.35,ease:"back.out(2)",immediateRender:false}},{T(c1 + 0.1)});')
        self.js.append(f'tl.fromTo("#slg",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.35,immediateRender:false}},{T(a + d * 0.55)});')
        self.reveal(CONF + 1, len(OC), a + d * 0.78, 1.2)
        self.hide("#steps,#cfr,#slg,#obz,#obt", e + 0.15)

    def teaser(self):
        a, e = self.seg[4]
        d = e - a
        self.js.append(f'tl.to("#cv",{{opacity:0.12,filter:"blur(6px)",duration:0.5}},{T(a - 0.2)});')
        # browser-like card with the live money-flow animation (site name hidden)
        vd = round(self.total - (a - 0.1), 2)
        self.el.append(f'<div id="bw" class="bw"><div class="bar"><i></i><i></i><i></i><span>🔒 ●●●●●●.com</span></div>'
                       f'<video id="fa" class="clip" src="assets/flow_anim.mp4" muted playsinline data-start="{a - 0.1:.2f}" '
                       f'data-duration="{min(vd, 8):.2f}" data-track-index="2"></video></div>')
        self.js.append(f'tl.fromTo("#bw",{{opacity:0,y:140,rotationX:35,scale:0.7}},{{opacity:1,y:0,rotationX:0,scale:1,duration:0.8,'
                       f'ease:"expo.out",immediateRender:false}},{T(a)});')
        self.sfx.append((whoosh(0.5), a, 0.7))
        s2 = a + d * 0.2
        self.el.append(f'<div id="sc2" class="shot" style="left:40px;top:890px;width:600px">'
                       f'<img src="assets/ob.png" style="width:100%"/></div>'
                       f'<div id="sc3" class="shot" style="left:690px;top:870px;width:330px">'
                       f'<video id="ba" class="clip" src="assets/bubbles_anim.mp4" muted playsinline data-start="{s2:.2f}" '
                       f'data-duration="{min(self.total - s2, 8):.2f}" data-track-index="3" style="width:100%"></video></div>')
        self.js.append(f'tl.fromTo("#sc2",{{opacity:0,x:-200,rotation:-8}},{{opacity:1,x:0,rotation:-3,duration:0.6,ease:"expo.out",'
                       f'immediateRender:false}},{T(s2)});')
        self.js.append(f'tl.fromTo("#sc3",{{opacity:0,x:200,rotation:8}},{{opacity:1,x:0,rotation:3,duration:0.6,ease:"expo.out",'
                       f'immediateRender:false}},{T(s2 + 0.25)});')
        self.sfx.append((pop(0.07, 800), s2, 0.5))
        self.sfx.append((pop(0.07, 1100), s2 + 0.25, 0.5))
        # like goal
        lk = a + d * 0.48
        self.js.append(f'tl.to(["#sc2","#sc3"],{{opacity:0,y:40,duration:0.3}},{T(lk - 0.2)});')
        self.el.append(f'<div id="lg"><div class="lh">❤️</div><div class="lt"><b id="lgn">0</b> / 1K</div>'
                       f'<div class="lbar"><div id="lbf"></div></div><div class="lx">= साइट का नाम 🔓</div></div>')
        self.js.append(f'tl.fromTo("#lg",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2.5)",'
                       f'immediateRender:false}},{T(lk)});')
        for j in range(1, 21):
            self.js.append(f'tl.set("#lgn",{{innerHTML:"{j * 50 if j < 20 else "1K"}"}},{T(lk + 0.3 + 0.07 * j)});')
        self.js.append(f'tl.fromTo("#lbf",{{scaleX:0}},{{scaleX:1,duration:1.4,ease:"power2.in",immediateRender:false}},{T(lk + 0.3)});')
        self.js.append(f'tl.to("#lg .lh",{{scale:1.35,duration:0.18,yoyo:true,repeat:7}},{T(lk + 0.3)});')
        self.sfx.append((riser(1.4), lk + 0.3, 0.45))
        self.sfx.append((ding(), lk + 1.75, 0.7))
        self.particles(lk + 1.75, 540, 1180, 26, (R, "#ff7aa2", Y))
        # comment OB + follow
        ct = a + d * 0.72
        self.js.append(f'tl.to(["#lg","#bw"],{{opacity:0,scale:0.8,duration:0.25}},{T(ct - 0.25)});')
        self.el.append(f'<div id="cta5"><div class="ck">कमेंट करो 👇</div><div class="cbox"><i></i><span id="typ"></span><u id="cur">|</u></div>'
                       f'<div id="fol">+ FOLLOW</div></div>')
        self.js.append(f'tl.fromTo("#cta5",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"expo.out",immediateRender:false}},{T(ct)});')
        for j, ch in enumerate(["O", "OB"]):
            self.js.append(f'tl.set("#typ",{{innerHTML:"{ch}"}},{T(ct + 0.35 + 0.25 * j)});')
            self.sfx.append((pop(0.03, 2200), ct + 0.35 + 0.25 * j, 0.35))
        self.js.append(f'tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:0.3,yoyo:true,repeat:{int((e - ct) / 0.6) + 2},ease:"none",'
                       f'immediateRender:false}},{T(ct)});')
        fa = ct + 1.0
        self.js.append(f'tl.fromTo("#fol",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(fa)});')
        self.js.append(f'tl.to("#fol",{{scale:1.08,duration:0.35,yoyo:true,repeat:{int((self.total - fa) / 0.7) + 1},ease:"sine.inOut"}},'
                       f'{T(fa + 0.45)});')
        self.sfx.append((ding(), fa, 0.5))


EXTRA = f"""
#bg{{background:radial-gradient(circle at 50% 45%,#141006 0%,#070604 55%,#000 100%) !important}}
.tt .tk{{color:{GOLD} !important;text-shadow:0 0 26px {GOLD}88 !important}}
.pc{{position:absolute;padding:14px 26px;border-radius:18px;border:4px solid;background:#0b0b0bee;text-align:center;
 font:900 34px/1.25 'Poppins','HindiUI';color:#fff;opacity:0;white-space:nowrap}}
.pc b{{font-size:40px}}
#steps{{position:absolute;left:40px;right:40px;top:400px;display:flex;gap:14px;opacity:0}}
.sp{{flex:1;padding:12px 0;text-align:center;border:3px solid #ffffff33;border-radius:40px;color:#ffffff99;
 font:800 28px 'Poppins','HindiUI';white-space:nowrap}}
.sp b{{display:inline-block;width:38px;height:38px;line-height:38px;border-radius:50%;background:{G};color:#04120b;
 margin-right:10px;font-size:24px}}
.bw{{position:absolute;left:40px;right:40px;top:380px;border-radius:26px;overflow:hidden;background:#fff;
 box-shadow:0 30px 80px #000c,0 0 0 4px {GOLD}88;opacity:0;transform-origin:50% 0}}
.bw .bar{{height:54px;background:#e5e7eb;display:flex;align-items:center;gap:10px;padding:0 20px}}
.bw .bar i{{width:16px;height:16px;border-radius:50%;background:#f87171;display:inline-block}}
.bw .bar i:nth-child(2){{background:#fbbf24}} .bw .bar i:nth-child(3){{background:#34d399}}
.bw .bar span{{margin-left:20px;padding:6px 24px;border-radius:20px;background:#fff;font:700 26px 'Poppins';color:#64748b;
 filter:blur(1.5px)}}
.bw video{{display:block;width:100%}}
.shot{{position:absolute;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 20px 60px #000c,0 0 0 4px {GOLD}66;opacity:0}}
.shot video{{display:block}}
#lg{{position:absolute;left:90px;right:90px;top:960px;padding:30px;border-radius:34px;background:#170a0e;border:4px solid {R};
 text-align:center;box-shadow:0 0 50px {R}66;opacity:0}}
.lh{{font-size:110px;line-height:1;display:inline-block}}
.lt{{font:900 84px 'Poppins';color:#fff}} .lt b{{color:{R}}}
.lbar{{height:22px;border-radius:12px;background:#ffffff22;margin:14px 20px;overflow:hidden}}
#lbf{{height:100%;background:linear-gradient(90deg,{R},#ff7aa2);transform-origin:0 50%;transform:scaleX(0)}}
.lx{{font:900 56px 'HindiUI';color:{Y}}}
#cta5{{position:absolute;left:0;right:0;top:960px;text-align:center;opacity:0}}
#cta5 .ck{{letter-spacing:0;font:900 50px 'HindiUI';color:#ffffffcc;margin-bottom:20px}}
#cta5 .cbox{{width:640px;margin:0 auto;padding:26px 40px;border-radius:60px;border:4px solid {GOLD};background:#14110a;text-align:left;
 font:900 80px 'Poppins';color:#fff;box-shadow:0 0 40px {GOLD}55}}
#cta5 .cbox i{{display:inline-block;width:44px;height:44px;border-radius:50%;background:{GOLD};margin-right:26px;vertical-align:middle}}
#cta5 .cbox u{{text-decoration:none;color:{GOLD}}}
#cta5 #fol{{margin-top:40px}}
"""


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    D.CSS += EXTRA
    r = OBReel(folder, s)
    r.chrome()
    r.chart()
    r.c1(); r.c2(); r.c3(); r.c4(); r.teaser()
    r.captions()
    r.write(D.music(folder))
    for f in ("flow_anim.mp4", "bubbles_anim.mp4", "ob.png"):
        shutil.copy(os.path.join(folder, "shots", f), os.path.join(folder, "hf", "assets", f))


if __name__ == "__main__":
    main()
