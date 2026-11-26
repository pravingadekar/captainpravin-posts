"""Fast, notification-style 9:16 promo for Adhishree Algo Trading (v2, "more engaging"): hook text on frame 1,
phone lock screen buzzing with trade notifications, kinetic slam words, dashboard inside the phone, big offer.
No P&L / returns anywhere.

  python tools/hf_reel_ad2.py reels/<folder>
  cd reels/<folder>/hf && npx --yes hyperframes@0.9.52 render --quality delivery -o out.mp4
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hf_reel_dark as D  # noqa: E402
from hf_reel_dark import Reel, G, R, Y, W, T, esc, pop, ding, boom, whoosh, riser  # noqa: E402

O = "#ff7a1a"


class Ad2(Reel):
    def slam(self, wid, html, at, until, color="#fff", size=96, top=150, sfx=True):
        self.el.append(f'<div id="{wid}" class="kw" style="top:{top}px;font-size:{size}px;color:{color}">{html}</div>')
        self.js.append(f'tl.fromTo("#{wid}",{{opacity:0,scale:2.4,rotation:-4}},{{opacity:1,scale:1,rotation:0,duration:0.28,'
                       f'ease:"back.out(2.2)",immediateRender:false}},{T(at)});')
        if until is not None:
            self.js.append(f'tl.to("#{wid}",{{opacity:0,scale:0.8,y:-30,duration:0.18}},{T(until)});')
            self.js.append(f'tl.set("#{wid}",{{visibility:"hidden"}},{T(until + 0.2)});')
        if sfx:
            self.sfx.append((boom(), at, 0.45))
            self.sfx.append((whoosh(0.3), at - 0.12, 0.4))

    def shake(self, at, sel="#phone", n=9, amp=10):
        self.js.append(f'tl.fromTo("{sel}",{{x:0}},{{x:{amp},duration:0.04,yoyo:true,repeat:{n},ease:"none",immediateRender:false}},{T(at)});')

    def notif(self, nid, icon, title, body, slot, at, until=None):
        self.el.append(f'<div id="{nid}" class="nt" style="top:{700 + slot * 175}px"><span class="ni">{icon}</span>'
                       f'<div><div class="nh">Adhishree Algo <i>• अभी</i></div><div class="nb">{esc(title)}</div>'
                       f'<div class="ns">{esc(body)}</div></div></div>')
        self.js.append(f'tl.fromTo("#{nid}",{{opacity:0,y:-90,scale:0.9}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.8)",'
                       f'immediateRender:false}},{T(at)});')
        self.sfx.append((ding(), at, 0.45))
        self.sfx.append((pop(0.05, 180), at, 0.6))
        if until is not None:
            self.js.append(f'tl.to("#{nid}",{{opacity:0,duration:0.2}},{T(until)});')

    def screen(self, sid, img, at, until):
        self.el_phone.append(f'<img id="{sid}" class="scr" src="assets/{img}"/>')
        self.js.append(f'tl.set("#{sid}",{{opacity:0}},0);')
        self.js.append(f'tl.fromTo("#{sid}",{{opacity:0,y:80,scale:1.08}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"expo.out",'
                       f'immediateRender:false}},{T(at)});')
        if until is not None:
            self.js.append(f'tl.to("#{sid}",{{opacity:0,duration:0.15}},{T(until)});')
        self.sfx.append((whoosh(0.3), at - 0.05, 0.45))

    def build(self):
        self.el_phone = []
        s = self.seg
        # ---------- c1: hook on frame 0
        a, e = s[0]
        d = e - a
        self.el.append(f'<div id="hook" class="kw" style="top:120px;font-size:100px">मीटिंग में थे…<br>'
                       f'<span style="color:{O}">ट्रेड हो गया? 🤯</span></div>')
        self.js.append('tl.fromTo("#hook",{scale:1.18},{scale:1,duration:0.35,ease:"back.out(2)"},0.02);')
        self.shake(0.05, "#hook", 5, 8)
        self.sfx.append((boom(), 0.05, 0.8))
        self.js.append(f'tl.to("#hook",{{opacity:0,y:-30,duration:0.2}},{T(e + 0.1)});')
        self.js.append('tl.fromTo("#phone",{y:900,rotation:8},{y:0,rotation:0,duration:0.6,ease:"expo.out"},0.25);')
        self.el.append(f'<div id="mtg" class="pill" style="left:40px;top:470px;background:{R}">💼 मीटिंग LIVE</div>')
        self.js.append(f'tl.fromTo("#mtg",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.3,ease:"back.out(2)"}},0.7);')
        self.js.append(f'tl.to("#mtg",{{opacity:0,duration:0.2}},{T(s[1][1])});')
        bz = a + d * 0.5
        self.shake(bz, "#phone", 13, 12)
        for k in range(4):
            self.sfx.append((pop(0.09, 120), bz + 0.1 * k, 0.9))
        self.notif("n1", "📈", "NIFTY: एंट्री रूल पूरा हुआ ✅", "ऑर्डर आपके ब्रोकर पर लगा", 0, bz + 0.3)
        # ---------- c2: kinetic no-chart / no-rush + more notifs
        a, e = s[1]
        d = e - a
        self.slam("k1", "ना चार्ट 👀 ❌", a + 0.02, a + d * 0.22)
        self.slam("k2", "ना जल्दबाज़ी ❌", a + d * 0.24, a + d * 0.5)
        self.notif("n2", "🛡️", "स्टॉप लॉस लग गया", "आपके रूल के हिसाब से", 1, a + d * 0.55)
        self.notif("n3", "🎯", "एग्ज़िट भी ऑटोमैटिक", "टारगेट या SL, जो पहले आए", 2, a + d * 0.7)
        self.slam("k3", f'<span style="color:{O}">सब ऑटोमैटिक ⚙️</span>', a + d * 0.82, e + 0.15)
        self.js.append(f'tl.to(["#n1","#n2","#n3","#lock"],{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        # ---------- c3: brand + 3 steps on the phone screen
        a, e = s[2]
        d = e - a
        self.slam("k4", f'<span class="brand">ADHISHREE <b>ALGO</b></span>', a + 0.02, a + d * 0.32, size=92)
        self.screen("sc0", "market.png", a + 0.05, a + d * 0.33)
        self.particles(a + 0.1, 540, 220, 22, (O, Y, "#ffd2a8"))
        for j, (txt, img, f) in enumerate([("1 🔗 ब्रोकर", "broker.png", 0.33), ("2 📊 स्ट्रैटेजी", "algos.png", 0.52),
                                           ("3 🛡️ रिस्क", "risk.png", 0.72)]):
            at = a + d * f
            nxt = a + d * [0.52, 0.72, 0.9][j]
            self.slam(f"st{j}", f'<span class="num">{txt[0]}</span>{esc(txt[1:])}', at, nxt, color="#fff", size=92)
            self.screen(f"sc{j + 1}", img, at + 0.02, nxt if j < 2 else e + 0.15)
        self.slam("k5", f'<span style="color:{G}">बस! ✅</span>', a + d * 0.9, e + 0.15)
        # ---------- c4: paper first
        a, e = s[3]
        d = e - a
        self.slam("k6", f'पहले <span style="color:{G}">PAPER</span> 📝', a + 0.02, e + 0.15)
        self.screen("sc4", "paper.png", a + 0.05, e + 0.15)
        self.el.append(f'<div id="sw" class="sw"><span id="swk"></span><b>PAPER</b><em>LIVE</em></div>')
        self.js.append(f'tl.fromTo("#sw",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(a + d * 0.3)});')
        self.js.append(f'tl.to("#sw",{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        self.el.append(f'<div id="fp" class="sticker">FREE प्रैक्टिस ✓</div>')
        self.js.append(f'tl.fromTo("#fp",{{opacity:0,scale:0.3,rotation:-20}},{{opacity:1,scale:1,rotation:-8,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(a + d * 0.55)});')
        self.js.append(f'tl.to("#fp",{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        self.sfx.append((ding(), a + d * 0.55, 0.5))
        # ---------- c5: offer
        a, e = s[4]
        d = e - a
        self.js.append(f'tl.to("#phone",{{y:1800,rotation:-10,duration:0.5,ease:"power3.in"}},{T(a - 0.2)});')
        self.el.append(f'<div id="off" class="off"><div class="gb">🎁</div><div class="gn">पहले <b id="gc">0</b></div>'
                       f'<div class="gt">कम्युनिटी मेंबर्स</div><div class="tk">FREE EARLY ACCESS</div></div>')
        self.js.append(f'tl.fromTo("#off",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.45,ease:"back.out(2.4)",immediateRender:false}},{T(a + 0.05)});')
        for j in range(1, 21):
            self.js.append(f'tl.set("#gc",{{innerHTML:"{j * 50}"}},{T(a + 0.2 + 0.05 * j)});')
        self.js.append(f'tl.to("#off .gb",{{rotation:12,scale:1.2,duration:0.12,yoyo:true,repeat:9}},{T(a + 0.2)});')
        self.sfx.append((riser(1.0), a + 0.2, 0.45))
        self.sfx.append((boom(), a + 1.2, 0.6))
        self.particles(a + 1.2, 540, 600, 34, (O, Y, G, "#ff7aa2"))
        self.js.append(f'tl.to("#off",{{y:-250,scale:0.8,duration:0.4,ease:"power2.inOut"}},{T(a + d * 0.48)});')
        acts = [("▶", "SUBSCRIBE", "#ff2d2d", 0.5), ("📷", "FOLLOW", "#d946ef", 0.66), ("📩", "SCREENSHOT DM", O, 0.82)]
        self.el.append('<div id="acts">' + "".join(f'<div class="ac" id="ac{j}"><span style="background:{c}">{i}</span>{t}</div>'
                                                    for j, (i, t, c, _) in enumerate(acts)) + "</div>")
        for j, (_, _, _, f) in enumerate(acts):
            at = a + d * f
            self.js.append(f'tl.fromTo("#ac{j}",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(at)});')
            self.sfx.append((pop(0.06, 900 + 250 * j), at, 0.5))
        self.js.append(f'tl.to(["#off","#acts"],{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        # ---------- c6: disclaimer end card
        a, e = s[5]
        self.el.append(f'<div id="end" class="endc"><div class="lg">A</div><div class="ln">ADHISHREE <b>ALGO</b></div>'
                       f'<div class="dc">⚠️ सिर्फ़ एजुकेशनल कंटेंट • ट्रेडिंग में रिस्क है<br>प्रॉफ़िट की कोई गारंटी नहीं</div>'
                       f'<div class="cp">TRADE WITH CAPTAIN PRAVIN</div></div>')
        self.js.append(f'tl.fromTo("#end",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.4,ease:"expo.out",immediateRender:false}},{T(a - 0.1)});')
        # ---------- phone shell (lock screen)
        self.el.append(f'<div id="phone"><div class="notch"></div><div id="pscr"><div id="lock"><div class="lt">9:31</div>'
                       f'<div class="ld">मंगलवार, 2 दिसंबर</div></div>{"".join(self.el_phone)}</div></div>')


EXTRA = f"""
#bg{{background:radial-gradient(circle at 50% 45%,#2a1406 0%,#0d0703 55%,#000 100%) !important}}
.pf{{background:{O} !important;box-shadow:0 0 12px {O} !important}}
.hd,.live,#brand{{display:none !important}}
.kw{{position:absolute;left:30px;right:30px;text-align:center;font-family:'HindiUI','Poppins';font-weight:900;line-height:1.15;
 color:#fff;text-shadow:0 8px 0 #0008,0 0 40px #000;z-index:5;opacity:0}}
#hook{{opacity:1}}
.kw .num{{display:inline-block;width:110px;height:110px;line-height:110px;border-radius:30px;background:{O};color:#1a0d02;
 margin-right:24px;font-family:'Poppins'}}
.kw .brand{{font-family:'Poppins';letter-spacing:.03em}} .kw .brand b{{color:{O}}}
#phone{{position:absolute;left:250px;top:340px;width:580px;height:1060px;border-radius:78px;background:#111;border:14px solid #2a2a2a;
 box-shadow:0 40px 120px #000,0 0 0 3px #555,0 0 80px {O}33;overflow:hidden;z-index:2}}
.notch{{position:absolute;left:50%;top:14px;width:170px;height:40px;margin-left:-85px;border-radius:24px;background:#000;z-index:4}}
#pscr{{position:absolute;inset:0;background:linear-gradient(160deg,#1b2a4a,#3a1c4d 55%,#5a2a14);overflow:hidden}}
#lock{{position:absolute;left:0;right:0;top:90px;text-align:center;color:#fff}}
#lock .lt{{font:300 150px/1 'Poppins'}} #lock .ld{{font:800 34px 'HindiUI';opacity:.85;margin-top:10px}}
.scr{{position:absolute;left:0;top:70px;width:100%;opacity:0}}
.nt{{position:absolute;left:270px;width:540px;display:flex;gap:18px;align-items:flex-start;padding:22px 24px;border-radius:30px;
 background:#ffffffe8;color:#111;box-shadow:0 14px 40px #000a;opacity:0;z-index:3}}
.ni{{flex:none;width:72px;height:72px;border-radius:18px;background:{O};font-size:42px;line-height:72px;text-align:center}}
.nh{{font:800 22px 'Poppins';color:#666}} .nh i{{font-style:normal;font-weight:600}}
.nb{{font:900 34px/1.2 'HindiUI';color:#111;margin-top:4px}} .ns{{font:700 26px 'HindiUI';color:#555}}
.pill{{position:absolute;padding:12px 28px;border-radius:30px;font:900 40px 'HindiUI';color:#fff;opacity:0;z-index:4}}
.sw{{position:absolute;left:0;right:0;top:1290px;margin:auto;width:max-content;padding:10px;border-radius:60px;background:#000c;
 border:3px solid #ffffff33;font:900 46px 'Poppins';opacity:0;z-index:4}}
.sw b{{display:inline-block;padding:8px 40px;border-radius:50px;background:{G};color:#04120b;box-shadow:0 0 30px {G}}}
.sw em{{display:inline-block;padding:8px 40px;font-style:normal;color:#ffffff66}}
.sticker{{position:absolute;right:40px;top:640px;padding:18px 34px;border-radius:24px;background:{Y};color:#1a1202;
 font:900 58px 'HindiUI';opacity:0;box-shadow:0 12px 40px #000a;z-index:4}}
.off{{position:absolute;left:0;right:0;top:420px;text-align:center;opacity:0;z-index:3}}
.gb{{font-size:220px;line-height:1;display:inline-block}}
.gn{{font:900 120px/1.1 'HindiUI';color:#fff}} .gn b{{font-family:'Poppins';color:{O};text-shadow:0 0 40px {O}}}
.gt{{font:900 64px 'HindiUI';color:#fff}}
.tk{{display:inline-block;margin-top:24px;padding:18px 50px;border:5px dashed #04120b;outline:6px solid {G};border-radius:18px;
 background:{G};color:#04120b;font:900 70px 'Poppins'}}
#acts{{position:absolute;left:90px;right:90px;top:900px;z-index:3}}
.ac{{display:flex;align-items:center;gap:30px;padding:22px 34px;margin-bottom:26px;border-radius:30px;background:#16100b;
 border:3px solid #ffffff22;font:900 62px 'Poppins';color:#fff;opacity:0}}
.ac span{{width:100px;height:100px;border-radius:26px;display:inline-flex;align-items:center;justify-content:center;font-size:56px;color:#fff}}
.endc{{position:absolute;left:0;right:0;top:420px;text-align:center;opacity:0;z-index:3}}
.endc .lg{{width:220px;height:220px;margin:0 auto;border-radius:54px;background:linear-gradient(135deg,{O},#ffb347);
 font:900 160px/220px 'Poppins';color:#1a0d02;box-shadow:0 0 80px {O}aa}}
.endc .ln{{font:900 92px 'Poppins';color:#fff;margin-top:30px}} .endc .ln b{{color:{O}}}
.endc .dc{{margin:50px auto 0;width:980px;padding:28px 20px;border-radius:30px;border:3px solid {Y}88;background:#1a1405;
 font:900 48px/1.45 'HindiUI';color:{Y}}}
.endc .cp{{margin-top:36px;font:800 32px 'Poppins';letter-spacing:.2em;color:#ffffff88}}
.cap{{z-index:6}}
"""


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    D.CSS += EXTRA
    D.GAP = 0.25
    r = Ad2(folder, s)
    r.seg = []
    t = 0.3
    for v in r.voices:
        r.seg.append((t, t + v.size / D.SR))
        t += v.size / D.SR + 0.25
    r.total = round(t + 0.8, 2)
    r.chrome()
    r.build()
    r.captions()
    r.write(D.music(folder))
    for f in os.listdir(os.path.join(folder, "shots")):
        shutil.copy(os.path.join(folder, "shots", f), os.path.join(folder, "hf", "assets", f))


if __name__ == "__main__":
    main()
