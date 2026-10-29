# captainpravin-posts

Public media for **Trade With Captain Pravin** daily posts (Facebook, Instagram, YouTube via Metricool).

## Structure

```
posts/YYYY-MM-DD/slide1.png ... slide6.png   # carousel, 1080x1350
posts/YYYY-MM-DD/reel.mp4                    # reel / Short, 1080x1920
```

## Public URL format

```
https://raw.githubusercontent.com/pravingadekar/captainpravin-posts/main/posts/<date>/<file>
```

Educational content only. No buy/sell signals or profit guarantees.

## Making a post

```
pip install pillow imageio-ffmpeg
python tools/make_post.py posts/YYYY-MM-DD
```

Edit `SLIDES` in `tools/make_post.py` for the day's topic. Fonts: Poppins (OFL).

## Daily routines

- `AGENT.md` — forex carousel + reel, routine at 8:00 AM IST.
- `candlestick/AGENT.md` — Hindi candlestick notebook reels (content spec in `candlestick/LESSON_PROMPT.md`), routine at 7:00 AM IST.
- `tools/make_reel.py` — any sequence of 1080x1920 frames → reel with original background music.
