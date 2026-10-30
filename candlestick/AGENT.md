# Candlestick reels — daily routine (for the cloud agent)

Series: "TRADE WITH CAPTAIN PRAVIN" Hindi candlestick notebook lessons (5 pages, 1080x1920) for Indian stock-market
beginners. The lesson content and design are defined in `candlestick/LESSON_PROMPT.md` — follow it exactly, do not
change colours, fonts, layout, language rules or accuracy rules. This file only says WHICH day to make and how to publish.

Run date: `D=$(TZ=Asia/Kolkata date +%F)`. Repo root = the checked-out `captainpravin-posts`.

## What each run posts

Read `candlestick/state.json`. YouTube must stay in strict DAY order (25, 26, 27, ...), never jumping ahead.

**A. Instagram + Facebook lesson**: `N = ig_next_day`. Make it (if `days/DAY<N>/reel.mp4` doesn't exist yet) and post
it to Instagram and Facebook. Then `ig_next_day += 1`.

**B. YouTube, in order**: up to TWO days per run, taken from `yt_next_day` upwards:
- Skip any DAY listed in `yt_already_posted` (it is on YouTube already; drop it from that list and move on).
- Never go past N (today's Instagram day). Once YouTube has caught up, it posts just that one day, same as Instagram.
- For each YouTube DAY `M`: if `days/DAY<MMM>/reel.mp4` already exists (made earlier for Instagram), reuse it as is.
  Otherwise make the lesson (rules below; it goes to YouTube only).
- After each YouTube DAY is scheduled: `yt_next_day = M + 1`.

Do A completely first, then B.

## Making one lesson (DAY = N or M)

1. Topic:
   - DAY <= 40: the pattern for that DAY in LESSON_PROMPT.md STEP 1.
   - DAY 64, 65, 66: the topic listed for that DAY in `candlestick/topics_log.md`.
   - Any other DAY >= 41: a NEW advanced candlestick/price-action lesson not yet used on the same platform(s) per
     `topics_log.md`. Instagram lessons must also avoid every topic in the "Known history" list. For YouTube-only
     DAY 41-63, the ten topics in "Known history" are allowed (YouTube never got them) — use them first, in order.
2. Follow LESSON_PROMPT.md STEP 2-5 with that DAY and topic. Work in `/home/claude` as written; if it is not writable,
   use `/tmp/claude` and change every `/home/claude` path to match. Do the full visual QA loop.
3. The STEP 5 tomorrow teaser: Instagram lesson → DAY N+1; YouTube-only lesson → DAY M+1 (its topic per the rules above; if unknown
   yet, write a short generic teaser "Kal DAY M+1 ... Miss मत करना!").
4. Save to `candlestick/days/DAY<NNN>/` (zero-padded, e.g. `DAY064`):
   `page1.png` … `page5.png`, `caption.txt` (the caption block text), `hashtags.txt` (the 30 hashtags line).
5. Build the reel (7 seconds per page, original synthesized background music — no other audio):
   ```
   python3 -m pip install -q -r requirements.txt   # if PIL fails with "_imaging": add --force-reinstall
   python3 tools/make_reel.py candlestick/days/DAY<NNN>/reel.mp4 7 candlestick/days/DAY<NNN>/page{1,2,3,4,5}.png
   ```
6. Append to `topics_log.md` under "Automated log": `- DAY N | <platforms> | <Hindi name> (<English name>) | $D`
   (also add a line when YouTube reuses an Instagram reel). Update `state.json` as described above.
7. Commit (`Candlestick DAY N: <English name>`), then `git pull --rebase origin main` and push to `main` (another routine
   pushes to this repo too; on a rejected push, pull --rebase and retry up to 3 times). Confirm
   `https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/candlestick/days/DAY<NNN>/reel.mp4`
   returns HTTP 200 (retry up to 2 minutes).

If rendering, QA, the reel build, the push or the URL check fails: do not schedule that lesson, do not advance its
counter (revert the state.json change), and report the failure in your final message.

## Publishing (Metricool, blogId `7732528`, timezone `Asia/Calcutta`, autoPublish true)

First call getScheduledPosts for $D and skip anything already scheduled (same DAY in the text/title).
Media: the reel.mp4 raw URL above. Text = caption.txt + blank line + hashtags.txt.

| Lesson | Time on $D | Network | Settings |
|---|---|---|---|
| A | 14:00 | Instagram | `instagramData.type: REEL`, `showReelOnFeed: true` |
| A | 17:00 | Facebook | `facebookData.type: REEL` |
| B, first YouTube DAY | 10:00 | YouTube | `type: short`, see YouTube below |
| B, second YouTube DAY | 14:00 | YouTube | `type: short`, see YouTube below |

YouTube: `title` = `DAY <M> | <Hindi name> (<English name>) | Candlestick Hindi #shorts` (must be under 100 chars;
shorten the Hindi name if needed), `madeForKids: false`, `category: EDUCATION`, `privacy: public`,
`tags`: 6-10 relevant tags from the hashtags (without #).

If the run is late and a slot has already passed, schedule that post 10 minutes from now instead.
If createScheduledPost fails with "Failed to normalize media", the file was pushed too recently for
Metricool to fetch: wait 90 seconds (`sleep 90`) and retry, up to 5 times, before reporting failure.

## Final message
One line per lesson: DAY, topic, which posts were scheduled at what time (or what failed).
