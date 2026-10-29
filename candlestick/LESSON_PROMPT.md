# Candlestick lesson prompt (content + design — do not change)

You are producing today's Instagram Reels lesson for the brand "TRADE WITH CAPTAIN PRAVIN". Work fully autonomously — the user (Pravin) will NOT reply. Never use AskUserQuestion. Just build and deliver.

DELIVERABLE: (A) exactly 5 SEPARATE PNG images, each 1080x1920 (9:16) — no collage, one notebook page per image — saved for auto-publishing; and (B) a ready-to-paste Instagram CAPTION + 30 VIRAL HASHTAGS in your reply.

===========================================================
STEP 1 — DAY NUMBER AND PATTERN
===========================================================
The DAY number is given to you by candlestick/AGENT.md (it is NOT computed from the date). Use the pattern for that DAY from the list below; for DAY 41+ use the topic AGENT.md gives you.

Pattern by DAY (Morning Star, Shooting Star and Hammer are ALREADY covered — never repeat them):
5 Hanging Man | 6 Inverted Hammer | 7 Bullish Engulfing | 8 Bearish Engulfing | 9 Doji | 10 Dragonfly Doji | 11 Gravestone Doji | 12 Spinning Top | 13 Marubozu | 14 Piercing Line | 15 Dark Cloud Cover | 16 Evening Star | 17 Three White Soldiers | 18 Three Black Crows | 19 Bullish Harami | 20 Bearish Harami | 21 Harami Cross | 22 Tweezer Top | 23 Tweezer Bottom | 24 Rising Three Methods | 25 Falling Three Methods | 26 Three Inside Up | 27 Three Inside Down | 28 Three Outside Up | 29 Three Outside Down | 30 Bullish Kicker | 31 Bearish Kicker | 32 Bullish Belt Hold | 33 Bearish Belt Hold | 34 On-Neck Line | 35 Separating Lines | 36 Upside Tasuki Gap | 37 Downside Tasuki Gap | 38 Bullish Abandoned Baby | 39 Bearish Abandoned Baby | 40 Hikkake Pattern
DAY 41+: teach combination/advanced lessons (pattern + Support-Resistance, pattern + Volume, pattern + Trendline, pattern + RSI, Multi-timeframe confirmation, Risk Management, Position Sizing, Trading Psychology, Common Mistakes, Backtesting) — one new topic per day, never repeat.

Only ONE pattern per day. Same DAY number on all 5 pages.

===========================================================
STEP 2 — SET UP THE RENDER PIPELINE (cloud container)
===========================================================
cd /home/claude
npm install playwright @fontsource/kalam @fontsource/caveat

Create /home/claude/reels/shared.js EXACTLY as below (this is the fixed brand template — never change colours, fonts, spiral or brand strip):

--- shared.js ---
const FONT_DIR = '/home/claude/node_modules/@fontsource';

const CSS = `
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-devanagari-400-normal.woff2') format('woff2');font-weight:400;unicode-range:U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FF;}
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-devanagari-700-normal.woff2') format('woff2');font-weight:700;unicode-range:U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FF;}
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-devanagari-300-normal.woff2') format('woff2');font-weight:300;unicode-range:U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+25CC,U+A830-A839,U+A8E0-A8FF;}
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-latin-400-normal.woff2') format('woff2');font-weight:400;}
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-latin-700-normal.woff2') format('woff2');font-weight:700;}
@font-face{font-family:'Kalam';src:url('file://${FONT_DIR}/kalam/files/kalam-latin-300-normal.woff2') format('woff2');font-weight:300;}
@font-face{font-family:'Caveat';src:url('file://${FONT_DIR}/caveat/files/caveat-latin-700-normal.woff2') format('woff2');font-weight:700;}

*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1920px;overflow:hidden;}
body{font-family:'Kalam','Noto Color Emoji',sans-serif;background:#fff;}

.page{position:relative;width:1080px;height:1920px;overflow:hidden;
  background:radial-gradient(ellipse at 20% 10%, rgba(255,252,236,1) 0%, rgba(253,248,232,1) 45%, rgba(248,241,220,1) 100%);}
.rules{position:absolute;left:0;top:0;width:1080px;height:1920px;
  background:repeating-linear-gradient(to bottom, transparent 0px, transparent 51px, rgba(120,165,200,.42) 51px, rgba(120,165,200,.42) 53px);
  background-position:0 96px;
  -webkit-mask-image:linear-gradient(to right, transparent 0px, transparent 118px, #000 132px, #000 100%);}
.grain{position:absolute;inset:0;opacity:.5;mix-blend-mode:multiply;}
.shade{position:absolute;inset:0;background:
   linear-gradient(to right, rgba(140,115,70,.20) 0px, rgba(140,115,70,.06) 60px, rgba(0,0,0,0) 200px),
   linear-gradient(to bottom, rgba(120,100,60,.10), rgba(0,0,0,0) 240px, rgba(0,0,0,0) 1650px, rgba(120,100,60,.12));
  pointer-events:none;}
.margin-line{position:absolute;left:196px;top:0;width:3px;height:1920px;background:rgba(214,86,86,.62);}
.margin-line2{position:absolute;left:203px;top:0;width:2px;height:1920px;background:rgba(214,86,86,.28);}
.spiral{position:absolute;left:0;top:0;width:170px;height:1920px;}
.brand{position:absolute;left:112px;top:0;width:74px;height:1920px;
  background:linear-gradient(to bottom,#12365e,#1c4b7d 40%,#12365e);
  box-shadow:2px 0 10px rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;}
.brand span{display:block;transform:rotate(-90deg);white-space:nowrap;color:#fdf6df;
  font-family:'Kalam';font-weight:700;font-size:40px;letter-spacing:5px;text-shadow:0 2px 3px rgba(0,0,0,.4);}
.content{position:absolute;left:236px;top:0;width:800px;height:1920px;}
.hdr{position:absolute;top:64px;left:0;width:800px;display:flex;align-items:center;justify-content:space-between;}
.day{font-family:'Kalam';font-weight:700;font-size:44px;color:#b3261e;border:4px solid #b3261e;
  border-radius:14px;padding:2px 22px 8px;transform:rotate(-1.4deg);background:rgba(255,255,255,.35);}
.pgno{font-family:'Kalam';font-weight:700;font-size:40px;color:#1b3f7a;width:104px;height:104px;
  border:4px solid #1b3f7a;border-radius:50%;display:flex;align-items:center;justify-content:center;
  transform:rotate(3deg);background:rgba(255,255,255,.4);}
h1.title{font-family:'Kalam';font-weight:700;font-size:76px;color:#10306b;line-height:1.12;transform:rotate(-.8deg);}
h1.title .en{display:block;font-size:44px;color:#b3261e;font-weight:700;letter-spacing:2px;margin-top:2px;}
.hl{background:linear-gradient(to bottom, rgba(255,232,84,0) 12%, rgba(255,226,64,.85) 14%, rgba(255,226,64,.85) 92%, rgba(255,226,64,0) 94%);padding:0 10px;border-radius:6px;box-decoration-break:clone;-webkit-box-decoration-break:clone;}
.hl-g{background:linear-gradient(to bottom, rgba(150,240,180,0) 12%, rgba(140,235,175,.8) 14%, rgba(140,235,175,.8) 92%, rgba(150,240,180,0) 94%);padding:0 10px;border-radius:6px;box-decoration-break:clone;-webkit-box-decoration-break:clone;}
.hl-p{background:linear-gradient(to bottom, rgba(255,170,200,0) 12%, rgba(255,168,198,.75) 14%, rgba(255,168,198,.75) 92%, rgba(255,170,200,0) 94%);padding:0 10px;border-radius:6px;box-decoration-break:clone;-webkit-box-decoration-break:clone;}
h2{font-family:'Kalam';font-weight:700;font-size:50px;color:#0e2f66;}
h2.red{color:#b3261e;}
p,li,div.t{font-family:'Kalam';font-weight:400;font-size:37px;color:#152a4a;line-height:1.45;}
.blue{color:#14357c;} .red{color:#b3261e;} .green{color:#12703c;} .blk{color:#24242a;}
b{font-weight:700;}
ul{list-style:none;}
li{position:relative;padding-left:44px;margin-bottom:12px;}
li:before{content:'';position:absolute;left:6px;top:22px;width:14px;height:14px;border-radius:50%;background:#b3261e;}
ol{list-style:none;counter-reset:c;}
ol li{counter-increment:c;padding-left:56px;}
ol li:before{content:counter(c) ')';background:none;left:0;top:0;width:auto;height:auto;font-family:'Kalam';font-weight:700;font-size:37px;color:#b3261e;}
.box{border:4px solid #14357c;border-radius:18px;padding:18px 24px 22px;background:rgba(255,255,255,.42);}
.box.red{border-color:#b3261e;}
.box.green{border-color:#12703c;}
.box.dash{border-style:dashed;}
.uline{border-bottom:5px solid #d8b400;padding-bottom:4px;display:inline-block;}
.uline-r{border-bottom:5px solid #b3261e;padding-bottom:4px;display:inline-block;}
svg text{font-family:'Kalam';font-weight:700;}
.rough{filter:url(#rough);}
`;

function spiralSVG(){
  let rings = '';
  const n = 21;
  for(let i=0;i<n;i++){
    const y = 74 + i*(1920-148)/(n-1);
    const j = (i%3)-1;
    rings += `
    <g transform="translate(0,${y.toFixed(1)}) rotate(${(j*0.8).toFixed(2)} 90 0)">
      <ellipse cx="88" cy="0" rx="15" ry="17" fill="#3a3226" opacity=".55"/>
      <ellipse cx="88" cy="-2" rx="13" ry="15" fill="#efe6cd"/>
      <ellipse cx="88" cy="1" rx="13" ry="15" fill="#2b2a26" opacity=".78"/>
      <path d="M 132 -26 C 150 -6, 128 24, 96 26 C 60 28, 26 16, 12 -8 C 2 -26, 16 -40, 40 -36" fill="none" stroke="#8d8f95" stroke-width="13" stroke-linecap="round"/>
      <path d="M 132 -26 C 150 -6, 128 24, 96 26 C 60 28, 26 16, 12 -8 C 2 -26, 16 -40, 40 -36" fill="none" stroke="#e2e5ea" stroke-width="5" stroke-linecap="round" opacity=".85"/>
      <path d="M 96 26 C 60 28, 26 16, 12 -8" fill="none" stroke="#5d6067" stroke-width="4" stroke-linecap="round" opacity=".5"/>
    </g>`;
  }
  return `<svg class="spiral" viewBox="0 0 170 1920" width="170" height="1920">${rings}</svg>`;
}

const DEFS = `
<svg width="0" height="0" style="position:absolute">
  <defs>
    <filter id="rough">
      <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="3" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="3.4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>
<svg class="grain" width="1080" height="1920">
  <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="4" stitchTiles="stitch"/>
  <feColorMatrix type="saturate" values="0"/></filter>
  <rect width="1080" height="1920" filter="url(#grain)" opacity="0.10"/>
</svg>`;

function page(pageNo, dayNo, bodyHTML){
  return `<!DOCTYPE html><html lang="hi"><head><meta charset="utf-8"><style>${CSS}</style></head>
<body><div class="page">
  <div class="rules"></div>
  ${DEFS}
  <div class="shade"></div>
  <div class="margin-line"></div><div class="margin-line2"></div>
  ${spiralSVG()}
  <div class="brand"><span>TRADE WITH CAPTAIN PRAVIN</span></div>
  <div class="content">
    <div class="hdr"><div class="day">DAY ${dayNo}</div><div class="pgno">${pageNo}/5</div></div>
    ${bodyHTML}
  </div>
</div></body></html>`;
}

module.exports = { page };
--- end shared.js ---

Create /home/claude/reels/build.js EXACTLY as below, setting DAY and SLUG for today:

--- build.js ---
const fs = require('fs');
const path = require('path');
const { page } = require('./shared');
const { chromium } = require('playwright');

const DAY = 5;                    // <-- set today's DAY number
const SLUG = 'HangingMan';        // <-- set today's pattern slug (no spaces)
const OUT = '/home/claude/reels/out';
fs.mkdirSync(OUT, { recursive: true });
const only = process.argv[2] ? process.argv[2].split(',').map(Number) : [1,2,3,4,5];

(async () => {
  const dirs = fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d));
  const base = '/opt/pw-browsers/' + dirs[dirs.length - 1];
  const exe = ['chrome-linux/chrome', 'chrome-linux64/chrome'].map(p => base + '/' + p).find(p => fs.existsSync(p)) || '';
  const browser = await chromium.launch(fs.existsSync(exe) ? { executablePath: exe } : {});
  const ctx = await browser.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const pg = await ctx.newPage();
  for (const n of only) {
    const file = path.join(__dirname, `p${n}.js`);
    if (!fs.existsSync(file)) continue;
    delete require.cache[require.resolve(file)];
    const body = require(file);
    const htmlPath = path.join(OUT, `page${n}.html`);
    fs.writeFileSync(htmlPath, page(n, DAY, body));
    await pg.goto('file://' + htmlPath);
    await pg.waitForTimeout(400);
    await pg.screenshot({ path: path.join(OUT, `DAY${DAY}_${SLUG}_Page${n}.png`), clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    console.log('rendered page', n);
  }
  await browser.close();
})();
--- end build.js ---

Then write /home/claude/reels/p1.js … p5.js. Each file is `module.exports = ` + a JS template literal of the page body HTML. Use absolute positioning inside the 800px-wide content column. Reference example of the exact style/quality expected (this was DAY 4, Hammer — copy the STYLE, write NEW content for today's pattern):

module.exports = `
<div style="position:absolute;top:196px;left:0;width:800px;">
  <h1 class="title"><span class="hl">हैमर कैंडल</span><span class="en">( HAMMER CANDLESTICK )</span></h1>
</div>
<div style="position:absolute;top:392px;left:0;width:800px;">
  <h2 class="red" style="transform:rotate(-.6deg);"><span class="uline">यह क्या है ?</span></h2>
  <div class="t" style="margin-top:18px;line-height:1.5;">यह <b class="red">एक ही candle</b> का pattern है &mdash; जिसकी<br>body <b>छोटी</b> और ऊपर की तरफ होती है, तथा<br>नीचे की <b class="blue">wick (छाया) बहुत लंबी</b> होती है।</div>
</div>
<div style="position:absolute;top:862px;left:0;width:414px;">
  <div class="box green" style="transform:rotate(-1deg);padding:14px 18px 18px;">
    <div class="t" style="font-size:31px;">यह कैसा signal है ?</div>
    <div style="font-family:'Kalam';font-weight:700;font-size:41px;color:#12703c;margin-top:6px;"><span class="hl-g">BULLISH</span></div>
    <div class="t" style="font-size:31px;margin-top:4px;">(तेजी का reversal संकेत)</div>
  </div>
</div>
<svg style="position:absolute;top:800px;left:430px;" width="370" height="644" viewBox="0 0 370 644">
  <g class="rough">
    <line x1="205" y1="164" x2="205" y2="200" stroke="#12703c" stroke-width="9" stroke-linecap="round"/>
    <rect x="150" y="200" width="110" height="96" fill="#2e9e5b" stroke="#0e5a32" stroke-width="8" rx="4"/>
    <line x1="205" y1="296" x2="205" y2="482" stroke="#12703c" stroke-width="9" stroke-linecap="round"/>
    <ellipse cx="205" cy="322" rx="132" ry="202" fill="none" stroke="#c8481f" stroke-width="7" opacity=".9"/>
  </g>
  <text x="205" y="566" font-size="36" fill="#0e2f66" text-anchor="middle" font-weight="700">HAMMER</text>
</svg>
<div style="position:absolute;top:1744px;left:0;width:800px;text-align:center;">
  <span style="font-family:'Kalam';font-weight:700;font-size:30px;color:#6b6250;letter-spacing:2px;">TRADE WITH CAPTAIN PRAVIN &nbsp;•&nbsp; DAY 4</span>
</div>
`;

Candle colours: bullish body fill #2e9e5b stroke #0e5a32; bearish body fill #e05a4a stroke #8e2a1e; wicks #1e8b4f / #c0392b. Circle/marker #c8481f. Dashed support/resistance #14357c. All hand-drawn shapes go inside `<g class="rough">` (never apply the filter to <text>).

===========================================================
STEP 3 — PAGE CONTENT (Hindi/Devanagari, simple; English trading terms in brackets. NO Marathi, NO Gujarati.)
===========================================================
Every page: DAY number badge top-left, page number circle top-right (1/5 … 5/5), spiral binding, left brand strip, small footer "TRADE WITH CAPTAIN PRAVIN • DAY N". Keep all content between y=190 and y=1790 so Instagram UI does not cover it.

PAGE 1 — INTRODUCTION: pattern name as big Hindi heading + English name in brackets; "यह क्या है?" with 2 short Hindi paragraphs; Bullish/Bearish/Neutral classification box; "कहाँ बनता है?" (Uptrend/Downtrend + Support/Resistance context); one LARGE technically-correct candle diagram circled in red with a label; a "सीधा मतलब" box. Keep breathing space. (For multi-candle patterns, put the diagram full-width below the text instead of beside it.)

PAGE 2 — "कैंडल की संरचना (Structure)": one LARGE labelled diagram with Open, High, Low, Close, Real Body, Upper Wick, Lower Wick (dashed leader lines to the right for OHLC, red brackets on the left for body/wick sizes). Then "पहचानने के नियम (Rules)" — 4 to 6 numbered rules covering body size, wick size, candle colour, market context, position in trend, and the confirmation requirement. End with a dashed "याद रखें" box holding the single most important identification point. Diagram must match the rules exactly.

PAGE 3 — "चार्ट में उदाहरण (Chart Example)": hand-drawn simplified chart with a price axis, previous trend candles, the pattern itself circled, a dashed Support/Resistance line, the confirmation candle, and a curved arrow for the likely move after confirmation. Right-side labels must be text-anchor="end" at x=790 so nothing clips. Below: "क्या हुआ यहाँ?" — 5 numbered steps in Hindi using hypothetical prices. Add a dashed note: figures are only for explanation, price need not always move that way. Never claim a guaranteed reversal or profit.

PAGE 4 — "ट्रेडिंग सेटअप (Trading Setup)": 1) ENTRY (only after confirmation), 2) STOP LOSS (based on the pattern's relevant High/Low), 3) TARGET (nearest Support/Resistance, R:R 1:2 or 1:3), 4) CONFIRMATION (next candle, Volume, Support/Resistance, market structure). Then a boxed hypothetical example with Entry / Stop Loss / Target 1 / Target 2 whose numbers are arithmetically consistent with the Page 3 chart, plus a small dashed Target/Entry/SL ladder sketch. Must include: "यह केवल educational example है, financial advice नहीं।"

PAGE 5 — "QUICK REVISION": (1) मुख्य बातें — name, Bullish/Bearish/Neutral, कहाँ बनता है, structure, signal meaning, with a small candle sketch; (2) Trading Checklist in two columns with ☐ boxes — Trend check, Pattern check, Support/Resistance, Confirmation, Entry, Stop Loss, Target + R:R, Risk management; (3) a red "⚠ सावधानी" box — केवल pattern देखकर trade न लें / Confirmation ज़रूर लें / Risk Management follow करें / कोई भी pattern 100% guarantee नहीं देता। Then a large bordered CTA box, exactly this text:
📚 Trading की जानकारी के लिए हमें FOLLOW करें ❤️
🔴 Live Trading देखने के लिए हमारे YouTube Channel को SUBSCRIBE करें 🔔
and below it, large and highlighted: TRADE WITH CAPTAIN PRAVIN

===========================================================
STEP 4 — MANDATORY VISUAL QA LOOP
===========================================================
After `node reels/build.js`, downscale each PNG to 594x1056 with PIL and READ each preview image yourself. Check for: overlapping text, text clipped at the right edge of the 800px column or the SVG viewBox, content colliding with the next block, content above y=190 or below y=1790, wrong DAY number, misspelled "TRADE WITH CAPTAIN PRAVIN", any Marathi/Gujarati text. Fix the offending p*.js, re-render, and look again. Repeat until all 5 pages are clean. Do not deliver un-inspected pages.

Also verify with python3 that every PNG is exactly 1080x1920.

===========================================================
STEP 5 — WRITE THE INSTAGRAM CAPTION + VIRAL HASHTAGS
===========================================================
Write a fresh caption for today's pattern in Hinglish (Hindi in Devanagari + normal English trading words), inside one plain ``` code block so Pravin can copy it in one tap. Follow this exact skeleton, but write NEW words every day — never copy yesterday's lines:

1. HOOK — first line must stop the scroll: a warning, a question or a bold claim about where this pattern appears (e.g. "🔴 Uptrend के TOP पर ये candle दिखे तो सावधान हो जाओ!"). Use 1–2 emojis max in the hook.
2. Pattern का नाम (Hindi) + English name + "— DAY N 📓"
3. 2 short lines describing the candle in simple Hindi.
4. 5 ✅ bullet lines: कहाँ बनता है / Signal (Bullish-Bearish-Neutral) / main structure Rule / Confirmation / Stop Loss.
5. ⚠️ one caution line: सिर्फ़ pattern देखकर trade मत करो — Confirmation + Risk Management ज़रूरी। कोई भी pattern 100% guarantee नहीं देता।
6. CTA lines: "📚 पूरी 5 pages की notebook swipe करके पढ़ो →", "❤️ Trading सीखने के लिए FOLLOW करो — @tradewithcaptainpravin", "🔔 Live Trading देखने के लिए YouTube Channel SUBSCRIBE करो"
7. Tomorrow teaser: "Kal DAY N+1 — <tomorrow's pattern> ... Miss मत करना!" (look it up in the STEP 1 list)
8. Engagement line: "📌 Save करो | 📤 Share करो | 💬 Comment में बताओ ..."
9. "(Educational purpose only, not financial advice)"

Then, in a SECOND separate ``` code block, give exactly 30 hashtags on one line, space-separated, lowercase. Build them as: ~8 pattern/topic-specific tags for TODAY'S pattern (e.g. #hangingman #bearishreversal), ~14 evergreen trading tags, ~5 Hindi/India tags, and ~3 reach tags. Keep these fixed in every list: #candlestickpatterns #priceaction #stockmarketindia #sharemarkethindi #tradingforbeginners #technicalanalysis #intradaytrading #nifty50 #banknifty #optionstrading #tradewithcaptainpravin #reelsindia #viralreels #trendingreels. Rotate the rest so the tag set is not identical every day. No banned/spammy tags, no "#followforfollow" type tags.

Finally add one short line of posting advice for today: which words to put as on-screen text in the first 2 seconds, and best posting time (सुबह 8–10 या शाम 7–10 IST).

===========================================================
STEP 6 — DELIVER
===========================================================
Delete the preview and .html files. Keep the 5 PNGs, the caption and the hashtags: candlestick/AGENT.md says where to save them and how to publish.

ACCURACY RULES: the candle diagram, the chart example and the written rules must all describe the SAME pattern correctly. Never invent an incorrect candle structure. Never promise profits or say "100% accurate". Always include confirmation and risk management.