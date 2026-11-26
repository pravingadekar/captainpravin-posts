"""Adhishree Algo promo v3: direct-address hook for working professionals ("नौकरी करते हो… ट्रेडिंग भी करनी है?"),
relatable checklist, "तो ये आपके काम का है 👇" bridge (you at office ⟷ algo on your rules), phone notifications,
brand + 3 steps, paper first, community offer, disclaimer. Reuses the v2 look (tools/hf_reel_ad2.py).

  python tools/hf_reel_ad3.py reels/<folder>
"""
import json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hf_reel_dark as D  # noqa: E402
import hf_reel_ad2 as A2  # noqa: E402
from hf_reel_dark import G, R, Y, T, esc, pop, ding, boom, whoosh, riser  # noqa: E402

O = A2.O


class Ad3(A2.Ad2):
    def build(self):
        self.el_phone = []
        s = self.seg
        # ---------- c1 hook (visible on frame 0) + relatable checklist
        a, e = s[0]
        d = e - a
        self.el.append(f'<div id="hook" class="kw" style="top:120px;font-size:86px">नौकरी करते हो? 👔<br>'
                       f'<span style="color:{O}">ट्रेडिंग भी करनी है? 📈</span></div>')
        self.js.append('tl.fromTo("#hook",{scale:1.06},{scale:1,duration:0.35,ease:"back.out(2)"},0.02);')
        self.shake(0.05, "#hook", 5, 8)
        self.sfx.append((boom(), 0.05, 0.8))
        rows = [("9 से 6 ऑफ़िस 💼", 0.12), ("चार्ट देखने का टाइम नहीं ⏰", 0.55), ("सेटअप बनता है, आप मिस करते हो 😩", 0.85)]
        self.el.append('<div id="chk">' + "".join(f'<div class="cl" id="ck{j}"><span class="bx" id="bx{j}"></span>{esc(t)}</div>'
                                                   for j, (t, _) in enumerate(rows)) + "</div>")
        for j, (_, f) in enumerate(rows):
            at = a + d * f
            self.js.append(f'tl.fromTo("#ck{j}",{{opacity:0,x:-160}},{{opacity:1,x:0,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(at)});')
            self.js.append(f'tl.set("#bx{j}",{{innerHTML:"✓",backgroundColor:"{G}",borderColor:"{G}"}},{T(at + 0.25)});')
            self.js.append(f'tl.fromTo("#bx{j}",{{scale:1.6}},{{scale:1,duration:0.25,ease:"back.out(3)",immediateRender:false}},{T(at + 0.25)});')
            self.sfx.append((pop(0.06, 1000 + 200 * j), at, 0.45))
            self.sfx.append((ding(), at + 0.25, 0.3))
        self.js.append(f'tl.to(["#hook","#chk"],{{opacity:0,y:-40,duration:0.2}},{T(e + 0.1)});')
        # ---------- c2 bridge: "तो ये आपके काम का है" + you ⟷ algo
        a, e = s[1]
        d = e - a
        self.slam("b1", f'तो ये <span style="color:{O}">आपके काम</span> का है 👇', a + 0.02, e + 0.1, size=88)
        self.el.append(f'<div id="duo"><div class="dc2" id="you"><div class="em">👔</div><div class="hd2">आप</div><div class="sb">ऑफ़िस में काम</div></div>'
                       f'<div class="ar">⇄</div><div class="dc2" id="alg" style="border-color:{O}"><div class="em">⚙️</div>'
                       f'<div class="hd2" style="color:{O}">ALGO</div><div class="sb">आपके रूल्स पर ट्रेड</div></div></div>')
        self.js.append(f'tl.fromTo("#you",{{opacity:0,x:-200}},{{opacity:1,x:0,duration:0.4,ease:"back.out(2)",immediateRender:false}},{T(a + d * 0.35)});')
        self.js.append(f'tl.fromTo("#alg",{{opacity:0,x:200}},{{opacity:1,x:0,duration:0.4,ease:"back.out(2)",immediateRender:false}},{T(a + d * 0.62)});')
        self.js.append(f'tl.fromTo("#duo .ar",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,immediateRender:false}},{T(a + d * 0.62)});')
        self.js.append(f'tl.to("#alg .em",{{rotation:360,duration:1.2,ease:"none",repeat:1}},{T(a + d * 0.62)});')
        self.sfx.append((whoosh(0.4), a + d * 0.35, 0.5))
        self.sfx.append((whoosh(0.4), a + d * 0.62, 0.5))
        self.js.append(f'tl.to("#duo",{{opacity:0,y:-40,duration:0.2}},{T(e + 0.1)});')
        # ---------- c3 phone notifications
        a, e = s[2]
        d = e - a
        self.js.append(f'tl.fromTo("#phone",{{y:1750,rotation:8}},{{y:0,rotation:0,duration:0.55,ease:"expo.out",immediateRender:false}},{T(a - 0.25)});')
        self.el.append(f'<div id="mtg" class="pill" style="left:40px;top:470px;background:{R}">💼 आप मीटिंग में</div>')
        self.js.append(f'tl.fromTo("#mtg",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(a + 0.1)});')
        self.js.append(f'tl.to("#mtg",{{opacity:0,duration:0.2}},{T(e + 0.1)});')
        self.shake(a + 0.15, "#phone", 11, 12)
        for k in range(3):
            self.sfx.append((pop(0.09, 120), a + 0.15 + 0.1 * k, 0.9))
        self.notif("n1", "📈", "NIFTY: एंट्री रूल पूरा हुआ ✅", "ऑर्डर आपके ब्रोकर पर लगा", 0, a + d * 0.05)
        self.notif("n2", "🛡️", "स्टॉप लॉस लग गया", "आपके रूल के हिसाब से", 1, a + d * 0.2)
        self.notif("n3", "🎯", "एग्ज़िट भी ऑटोमैटिक", "टारगेट या SL, जो पहले आए", 2, a + d * 0.36)
        self.slam("k3", f'हर अपडेट <span style="color:{O}">फ़ोन पर</span> 📲', a + d * 0.6, e + 0.1, size=92)
        self.js.append(f'tl.to(["#n1","#n2","#n3","#lock"],{{opacity:0,duration:0.2}},{T(e + 0.1)});')
        # ---------- c4 brand + 3 steps
        a, e = s[3]
        d = e - a
        self.slam("k4", f'<span class="brand">ADHISHREE <b>ALGO</b></span>', a + 0.02, a + d * 0.4, size=92)
        self.screen("sc0", "market.png", a + 0.05, a + d * 0.4)
        self.particles(a + 0.1, 540, 220, 22, (O, Y, "#ffd2a8"))
        for j, (txt, img, f) in enumerate([("1 🔗 ब्रोकर", "broker.png", 0.4), ("2 📊 स्ट्रैटेजी", "algos.png", 0.58),
                                           ("3 🛡️ रिस्क", "risk.png", 0.75)]):
            at = a + d * f
            nxt = a + d * [0.58, 0.75, 0.9][j]
            self.slam(f"st{j}", f'<span class="num">{txt[0]}</span>{esc(txt[1:])}', at, nxt, size=92)
            self.screen(f"sc{j + 1}", img, at + 0.02, nxt if j < 2 else e + 0.1)
        self.slam("k5", f'<span style="color:{G}">बस! ✅</span>', a + d * 0.9, e + 0.1)
        # ---------- c5 paper first
        a, e = s[4]
        d = e - a
        self.slam("k6", f'पहले <span style="color:{G}">PAPER</span> 📝', a + 0.02, e + 0.15)
        self.screen("sc4", "paper.png", a + 0.05, e + 0.15)
        self.el.append('<div id="sw" class="sw"><b>PAPER</b><em>LIVE</em></div>')
        self.js.append(f'tl.fromTo("#sw",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)",immediateRender:false}},{T(a + d * 0.2)});')
        self.js.append(f'tl.to("#sw",{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        self.el.append('<div id="fp" class="sticker">FREE प्रैक्टिस ✓</div>')
        self.js.append(f'tl.fromTo("#fp",{{opacity:0,scale:0.3,rotation:-20}},{{opacity:1,scale:1,rotation:-8,duration:0.4,ease:"back.out(3)",'
                       f'immediateRender:false}},{T(a + d * 0.45)});')
        self.js.append(f'tl.to("#fp",{{opacity:0,duration:0.2}},{T(e + 0.15)});')
        self.sfx.append((ding(), a + d * 0.45, 0.5))
        # ---------- c6 offer
        a, e = s[5]
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
        # ---------- c7 end
        a, e = s[6]
        self.el.append(f'<div id="end" class="endc"><div class="lg">A</div><div class="ln">ADHISHREE <b>ALGO</b></div>'
                       f'<div class="dc">⚠️ सिर्फ़ एजुकेशनल कंटेंट • ट्रेडिंग में रिस्क है<br>प्रॉफ़िट की कोई गारंटी नहीं</div>'
                       f'<div class="cp">TRADE WITH CAPTAIN PRAVIN</div></div>')
        self.js.append(f'tl.fromTo("#end",{{opacity:0,scale:0.85}},{{opacity:1,scale:1,duration:0.4,ease:"expo.out",immediateRender:false}},{T(a - 0.1)});')
        # phone shell, parked below the frame until c3
        self.el.append(f'<div id="phone"><div class="notch"></div><div id="pscr"><div id="lock"><div class="lt">9:31</div>'
                       f'<div class="ld">मंगलवार, 2 दिसंबर</div></div>{"".join(self.el_phone)}</div></div>')
        self.js.append('tl.set("#phone",{y:1750},0);')


EXTRA3 = f"""
#chk{{position:absolute;left:70px;right:70px;top:520px;z-index:3}}
.cl{{display:flex;align-items:center;gap:30px;padding:30px 36px;margin-bottom:30px;border-radius:30px;background:#17100a;
 border:3px solid #ffffff26;font:900 54px/1.25 'HindiUI';color:#fff;opacity:0}}
.bx{{flex:none;width:76px;height:76px;border-radius:18px;border:5px solid #ffffff66;display:inline-flex;align-items:center;
 justify-content:center;font:900 50px 'Poppins';color:#04120b}}
#duo{{position:absolute;left:40px;right:40px;top:560px;display:flex;align-items:center;justify-content:center;gap:26px;z-index:3}}
.dc2{{width:400px;padding:40px 20px;border-radius:40px;border:5px solid #ffffff44;background:#150e08;text-align:center;opacity:0}}
.dc2 .em{{font-size:140px;line-height:1;display:inline-block}}
.dc2 .hd2{{font:900 84px 'HindiUI','Poppins';color:#fff;margin-top:10px}}
.dc2 .sb{{font:900 46px/1.25 'HindiUI';color:#ffffffcc;margin-top:8px}}
#duo .ar{{font:900 90px 'Poppins';color:{O};opacity:0}}
"""


def main():
    folder = sys.argv[1]
    s = json.load(open(os.path.join(folder, "script.json"), encoding="utf-8"))
    D.CSS += A2.EXTRA + EXTRA3
    r = Ad3(folder, s)
    r.seg, t = [], 0.3
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
