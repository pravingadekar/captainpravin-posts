# Daily post routine (for the cloud agent)

Brand: **Trade With Captain Pravin** (@tradewithcaptainpravin). Audience: Indian beginners learning forex.
Language: Hinglish (Roman script). Educational only.

## Steps (run once per day, ~5:30 PM IST)

1. `D=$(TZ=Asia/Kolkata date +%F)`. If `posts/$D/` already exists with `reel.mp4`, skip to step 6.
2. Pick the first unchecked topic in `topics.md`; tick it as `- [x] <topic> ($D)`.
3. Write `posts/$D/content.json` with exactly 6 slides, same shape as `posts/2026-10-30/content.json`:
   - Slide 1: hook (`tag`, `title` as a question/bold claim, short `text`, `box` "Aaj seekho: ...").
   - Slides 2-5: one idea each, with a concrete number/example. Use `list`, `box`, `compare` (colors `green`/`red`).
   - Slide 6: `tag` "AAPKI BAARI", engagement question as `title`, `text`, `cta` "Follow karo aur daily forex seekho",
     `disclaimer` exactly: "Disclaimer: Sirf educational content. Financial advice nahi. Forex/CFD trading mein high risk hai, aapka paisa doob sakta hai."
   - Keep titles under ~45 chars and list items under ~40 chars. Use only plain ASCII plus ÷ × % $ ₹ in slide text:
     NO emoji and NO arrows (→) — Poppins has no glyph for them.
   - Double-check every number and formula.
4. Write `posts/$D/captions.md` (Instagram carousel, Instagram Reel, Facebook, YouTube Short) in the format of
   `posts/2026-10-30/captions.md`. Each caption: hook, key points, engagement question, Follow/Subscribe CTA,
   disclaimer, hashtags. YouTube title under 100 chars, ending in `#shorts`.
5. Render and check:
   ```
   pip install -q -r requirements.txt
   python tools/make_post.py posts/$D
   ```
   Open every `slideN.png` and look at it. Text must not overflow the frame, overlap the footer, or show empty boxes.
   Fix content.json and re-render until clean. Then commit (`Post $D: <topic>`) and push to `main`.
6. Confirm `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/posts/$D/slide1.png` and
   `.../reel.mp4` return HTTP 200 (retry for up to 2 minutes after push).
7. Metricool (blogId `7732528`, timezone `Asia/Calcutta`). First call getScheduledPosts for $D; do not create a post
   that already exists. Then create, all at `$D` 19:00:00 Asia/Calcutta, autoPublish true:
   - Instagram `POST` with slide1..slide6 URLs (carousel), Instagram carousel caption.
   - Instagram `REEL` with reel.mp4, `showReelOnFeed: true`, Reel caption. Schedule at 19:05.
   - Facebook `POST` with slide1..slide6 URLs, Facebook caption.
   - Facebook `REEL` with reel.mp4, Reel caption (Facebook variant). Schedule at 19:05.
   - YouTube `short` with reel.mp4: title, `madeForKids: false`, `category: EDUCATION`, `privacy: public`.
   Media URLs: `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/posts/$D/<file>`.

## Content rules (never break)
- Education only. No buy/sell signals, no "ye pair kharido", no price predictions, no profit/income guarantees.
- No fake testimonials or screenshots of profits.
- Every post: hook, engagement question, Follow/Subscribe CTA, disclaimer, hashtags.
