# Daily post routine (for the cloud agent)

Brand: **Trade With Captain Pravin** (@tradewithcaptainpravin). Audience: Indian beginners learning forex.
Language: Hinglish (Roman script). Educational only.

## Steps (run once per day, ~8:00 AM IST, before the first slot at 10:00 AM)

1. `D=$(TZ=Asia/Kolkata date +%F)`. If `posts/$D/` already exists with `reel.mp4`, skip to step 6.
2. Pick the first unchecked topic in `topics.md`; tick it as `- [x] <topic> ($D)`.
3. Write `posts/$D/content.json` with exactly 6 slides, same shape as `posts/2026-10-29/content.json`:
   - Slide 1: hook (`tag`, `title` as a question/bold claim, short `text`, `box` "Aaj seekho: ...").
   - Slides 2-5: one idea each, with a concrete number/example. Use `list`, `box`, `compare` (colors `green`/`red`).
   - Slide 6: `tag` "AAPKI BAARI", engagement question as `title`, `text`,
     `cta` exactly "Follow + Subscribe karo. Roz YouTube LIVE par saath judo!",
     `disclaimer` exactly: "Disclaimer: Sirf educational content. Financial advice nahi. Forex/CFD trading mein high risk hai, aapka paisa doob sakta hai."
   - Keep titles under ~45 chars and list items under ~40 chars. Use only plain ASCII plus ÷ × % $ ₹ in slide text:
     NO emoji and NO arrows (→) — Poppins has no glyph for them.
   - Double-check every number and formula.
   - Add `"narration"`: a list of exactly 6 voiceover lines, one per slide, spoken by a Hindi female voice
     (ElevenLabs). Write them in Devanagari, with English trading words transliterated (ट्रेड, रिस्क, स्टॉप लॉस,
     लॉट साइज़) and numbers spelled as words (एक परसेंट, दस डॉलर) so the voice pronounces them correctly.
     Conversational Hinglish, 1-2 short sentences per slide (~12-25 words). Line 1 is the hook. Line 6 asks the
     comment question, then ends exactly with: "फ़ॉलो और सब्सक्राइब करो, ट्रेड विद कैप्टन प्रवीण। हम रोज़ यूट्यूब
     पर लाइव आते हैं, लाइव में हमारे साथ ज़रूर जुड़िए।" Same facts as the slides, nothing extra.
4. Write `posts/$D/captions.md` (Instagram carousel, Instagram Reel, Facebook, YouTube Short) in the format of
   `posts/2026-10-29/captions.md`. Each caption: hook, key points, engagement question, CTA, disclaimer, hashtags.
   The CTA in every caption: "Follow + Subscribe karo @tradewithcaptainpravin" and
   "🔴 Hum roz YouTube par LIVE aate hain, live mein hamare saath judo!" (YouTube: "Subscribe karo" + the same
   live line). YouTube title under 100 chars, ending in `#shorts`.
5. Render and check:
   ```
   python3 -m pip install -q -r requirements.txt   # if PIL fails with "_imaging": add --force-reinstall
   python3 tools/make_post.py posts/$D
   ```
   It must print "with voice" (needs `ELEVENLABS_API_KEY`, set in the environment; never print it). If the voice
   step fails, retry once; if it still fails, render with `--no-voice` so the post still goes out, and say so in
   your final message. Open every `slideN.png` and look at it. Text must not overflow the frame, overlap the footer, or show empty boxes.
   Fix content.json and re-render until clean. Then commit (`Post $D: <topic>`), `git pull --rebase origin main`, and push
   to `main` (another routine pushes to this repo too; on a rejected push, pull --rebase and retry up to 3 times).
6. Confirm `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/posts/$D/slide1.png` and
   `.../reel.mp4` return HTTP 200 (retry for up to 2 minutes after push).
7. Metricool (blogId `7732528`, timezone `Asia/Calcutta`). First call getScheduledPosts for $D; do not create a post
   that already exists. Then create, timezone Asia/Calcutta, autoPublish true, at these times on `$D`
   (from Metricool best-time data, Oct 2026; the reel gets each network's peak slot because reels reach non-followers):
   | Time  | Post |
   |-------|------|
   | 10:00 | Facebook `REEL` with reel.mp4, Reel caption (Facebook variant) |
   | 12:00 | Facebook `POST` with slide1..slide6 URLs, Facebook caption |
   | 16:00 | YouTube `short` with reel.mp4: title, `madeForKids: false`, `category: EDUCATION`, `privacy: public` |
   | 18:00 | Instagram `REEL` with reel.mp4, `showReelOnFeed: true`, Reel caption |
   | 20:00 | Instagram `POST` with slide1..slide6 URLs (carousel), Instagram carousel caption |
   If the run is late and a slot has already passed, schedule that post 10 minutes from now instead.
   Media URLs: `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/posts/$D/<file>`.

## Content rules (never break)
- Education only. No buy/sell signals, no "ye pair kharido", no price predictions, no profit/income guarantees.
- No fake testimonials or screenshots of profits.
- Every post: hook, engagement question, Follow/Subscribe CTA, disclaimer, hashtags.
