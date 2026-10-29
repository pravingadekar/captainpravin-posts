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

## Final message
Mode, date, number of events, what was scheduled when (or what failed).
