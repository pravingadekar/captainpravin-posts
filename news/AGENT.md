# Forex news posts — daily + weekly (for the cloud agent)

Brand: **Trade With Captain Pravin** (@tradewithcaptainpravin). Audience: Indian forex beginners. Hinglish.
Purpose: tell people WHEN the big economic news is (in IST) and how to stay safe around it. Information only.

Run date: `D=$(TZ=Asia/Kolkata date +%F)`, weekday `W=$(TZ=Asia/Kolkata date +%a)`.

- `W` = Sat → nothing to do, stop.
- `W` = Sun → **weekly** post: `MODE=weekly`, `DIR=news/week-$D`.
- Mon-Fri → **daily** post: `MODE=daily`, `DIR=news/$D`.

If `$DIR/reel.mp4` already exists, skip to step 6.

## Steps

1. Build the draft from the calendar feed (event times are converted to IST by the script — never type or change
   an event line or time yourself):
   ```
   python3 -m pip install -q -r requirements.txt   # if PIL fails with "_imaging": add --force-reinstall
   python3 tools/make_news.py $MODE $D $DIR
   ```
   Exit code 3 means no medium/high-impact news → no post today; stop and say so.
2. Fill every `TODO` in `$DIR/content.json`:
   - The **SAMJHO** slide: explain the single most important event (weekly: the one or two biggest) in simple
     Hinglish: what it measures, which currency / pairs / gold usually react, why the move can be big.
     `title` under ~45 chars (e.g. "NFP Kya Hai?"), one short `text`, `list` of 2-4 items under ~40 chars.
     Plain ASCII plus ÷ × % $ ₹ only; no emoji, no arrows.
   - `narration`: one voiceover line per slide (same count as slides), Devanagari, English words transliterated,
     numbers and times spelled out (शाम छह बजे, यूएसडी, जीडीपी). Calendar slides: read the 2-3 most important
     events with their times, not every line. Last line asks the slide's question, then ends exactly with:
     "फ़ॉलो और सब्सक्राइब करो, ट्रेड विद कैप्टन प्रवीण। हम रोज़ रात नौ बजे यूट्यूब पर लाइव आते हैं, लाइव में हमारे साथ ज़रूर जुड़िए।"
   - Never say which way price will go, never "buy/sell", never "forecast se zyada aaya to X karo". Allowed:
     "result forecast se bahut alag aaya to kisi bhi taraf bada move ho sakta hai".
3. Write `$DIR/captions.md` with four captions (Instagram carousel, Instagram Reel, Facebook, YouTube Short).
   Each: hook, the key events with IST times copied exactly from `$DIR/events.json`, one safety line,
   "Follow + Subscribe karo @tradewithcaptainpravin", "🔴 Hum roz raat 9 baje YouTube par LIVE aate hain, live mein
   hamare saath judo!", "Disclaimer: Sirf educational content. Financial advice nahi. Forex trading mein high risk
   hai.", hashtags (#forexnews #economiccalendar #forextrading #forexindia #tradingnews #forex plus 4-8 for the
   day's events). YouTube title under 100 chars ending in `#shorts`, e.g.
   "Aaj Ke Bade Forex News (30 Oct) | Time IST #shorts" / "Is Hafte Ke Forex News | Weekly Calendar #shorts".
4. Render: `python3 tools/make_post.py $DIR`. It must print "with voice" (needs `ELEVENLABS_API_KEY`; never print
   it). If the voice fails twice, render with `--no-voice` and say so. Open every `slideN.png`: nothing may overflow,
   overlap the footer or show empty boxes. Fix only the text you wrote, re-render until clean.
4b. **Animated reel (daily AND weekly)** — replaces the slideshow `reel.mp4`; the carousel slides stay. Do this
   after the last `make_post.py` run, because make_post.py overwrites `reel.mp4`.
   Write `$DIR/anim.json`:
   ```
   {"mode": "<daily|weekly>",
    "hook": ["IS HAFTE", "3 BADE NEWS", "GOLD aur USD hil sakte hain!"],
    "events": [{"ist": "...", "what": "US Retail Sales", "sub": "Log kitna kharch kar rahe hain?",
                "pairs": "USD  |  GOLD  |  EURUSD", "star": false}, ...],
    "safety": ["News se 15 min pehle naya trade nahi", "Spread aur slippage badh sakta hai",
               "Stop loss hamesha lagao", "Lot size chhota rakho"],
    "narration": ["...", "...", ...]}
   ```
   - `events`: weekly = the 3 biggest events of the week (2 if only 2; max 4); daily = today's events, 1-3 cards
     (the most important ones). Time order. `ist` copied exactly from `events.json` (events with the same `ist` are
     one card; the script computes day, time, flag, "DER RAAT" for times before 4 AM, and the "Forecast vs Pichhla"
     bars from events.json; it refuses an `ist` that is not in events.json). `what`: short English name under
     ~22 chars. `sub`: simple Hinglish question under ~32 chars (what it measures, no direction). `pairs`: 2-3
     instruments that usually react, joined with "  |  ". `"star": true` on the single biggest only (ignored when
     there is just one card).
   - `hook` (3 short lines, each under ~30 chars, never a price direction):
     weekly: "IS HAFTE" / "<cards> BADE NEWS" / which market can move.
     daily: when the first big news is + its currency, e.g. "AAJ SHAAM 7 BAJE" / "USD ka BADA NEWS!" /
     "GOLD aur EURUSD hil sakte hain!" (if several, "AAJ <cards> BADE NEWS" as line 2).
   - `safety`: daily only (omit for weekly): exactly the 4 items above (you may shorten, each under ~38 chars).
   - `narration`: Devanagari, one line per scene = 1 (hook) + cards + 1 if safety + 1 (closing). Hook line starts
     "रुको!". One line per card: ordinal if more than one card (पहला, दूसरा, और तीसरा), day (daily: "आज"), time
     spelled out the way the card shows it (late night: "बुधवार देर रात साढ़े बारह बजे"), the name, and one short
     meaning; daily cards may read the forecast and previous numbers from events.json. Safety line: the 4 tips in
     one or two sentences. Last line exactly:
     "टाइम नोट कर लो, और ये रील सेव करो। फ़ॉलो करो ट्रेड विद कैप्टन प्रवीण, हम रोज़ रात नौ बजे यूट्यूब पर लाइव आते हैं।"
   Run `python3 tools/make_anim_reel.py $DIR`. It must print "with voice". Open every `$DIR/check/anim*.jpg`:
   text must fit inside its card, day/time must match events.json. If it fails twice, keep the slideshow reel
   (re-run `python3 tools/make_post.py $DIR` if `reel.mp4` is missing) and say so in the final message.
5. Commit (`News $MODE $D`), `git pull --rebase origin main`, push to `main` (other routines push too; on a rejected
   push, pull --rebase and retry up to 3 times). Confirm the raw URLs of `slide1.png` and `reel.mp4` under
   `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/$DIR/` return HTTP 200 (retry 2 min).
6. Metricool (blogId `7732528`, timezone `Asia/Calcutta`, autoPublish true). First getScheduledPosts for $D and
   skip anything already scheduled. Carousel = all `slideN.png` URLs in order; reel = `reel.mp4`.

   | Mode | Time | Post |
   |---|---|---|
   | daily | 07:30 | Instagram `POST` carousel + Facebook `POST` carousel |
   | daily | 12:30 | Instagram `REEL` (`showReelOnFeed: true`) + YouTube `short` |
   | daily | 13:00 | Facebook `REEL` |
   | weekly | 10:00 | Instagram `POST` carousel + Facebook `POST` carousel |
   | weekly | 12:00 | Instagram `REEL` + YouTube `short` |
   | weekly | 12:30 | Facebook `REEL` |

   YouTube: `madeForKids: false`, `category: EDUCATION`, `privacy: public`. If a slot has passed, use 10 minutes
   from now.
   Daily: if every event in `events.json` is before 12:30 IST, post the reels at 07:45 (Instagram + YouTube) and
   07:50 (Facebook) instead, so they go out before the news. A reel or carousel already scheduled for $D on a
   network (at any time) counts as done — never schedule a second one.
   If createScheduledPost fails with "Failed to normalize media", the file was pushed too recently for
   Metricool to fetch: wait 90 seconds (`sleep 90`) and retry, up to 5 times, before reporting failure.

## Final message
Mode, date, number of events, what was scheduled when (or what failed).
