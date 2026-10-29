"""Build the draft content.json for a forex news post from the ForexFactory weekly calendar feed.

Event times come straight from the feed, converted to IST, so the agent never types a time by hand.
The agent then fills the "SAMJHO" slide (marked TODO) and the narration, and renders with make_post.py.

    python tools/make_news.py daily  2026-10-30 news/2026-10-30
    python tools/make_news.py weekly 2026-11-01 news/week-2026-11-01

Exit code 3 = no news worth a post (weekend, or no medium/high events) -> skip posting.
"""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

FEED = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
IST = timezone(timedelta(hours=5, minutes=30))
PER_SLIDE = 7
DAY_STARTS = 7  # a daily post covers 07:00 IST to 07:00 IST next day
TODO = "TODO"

DISCLAIMER = ("Disclaimer: Sirf educational content. Financial advice nahi. "
              "Forex/CFD trading mein high risk hai, aapka paisa doob sakta hai.")
SAFETY = [
    ["tag", "SAFETY FIRST"],
    ["title", "News Time Par Kya Karein?"],
    ["list", [
        "News se 15 min pehle naya trade nahi",
        "Spread aur slippage badh sakta hai",
        "Stop loss hamesha lagao",
        "Lot size chhota rakho",
    ]],
    ["text", "Bada move dono taraf ho sakta hai. Pehle bachao, phir kamao."],
]


def load_feed(path=None):
    if path:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    req = urllib.request.Request(FEED, headers={"User-Agent": "captainpravin-posts"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def to_ist(raw):
    events = []
    for e in raw:
        if e.get("impact") not in ("High", "Medium") or not e.get("date"):
            continue
        t = datetime.fromisoformat(e["date"]).astimezone(IST)
        events.append({"ist": t, "currency": e["country"], "title": e["title"], "impact": e["impact"],
                       "forecast": e.get("forecast", ""), "previous": e.get("previous", "")})
    return sorted(events, key=lambda e: e["ist"])


def pick(events):
    """High-impact events; fall back to medium ones on a quiet day."""
    high = [e for e in events if e["impact"] == "High"]
    return high or events


def fmt_time(t, day=None):
    s = t.strftime("%I:%M %p").lstrip("0")
    return s if day is None or t.date() == day else f"{s} {t.strftime('%a')}"


def lines(events, day=None):
    """One line per (time, currency), joining events released together. With `day`, times on
    another date get the weekday appended (e.g. "1:30 AM Fri")."""
    grouped = {}
    for e in events:
        grouped.setdefault((e["ist"], e["currency"]), []).append(e["title"])
    return [f"{fmt_time(t, day)} | {cur} | {' + '.join(titles)}" for (t, cur), titles in grouped.items()]


def chunks(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def closing(question):
    return [
        ["tag", "AAPKI BAARI"],
        ["title", question],
        ["text", "Comment mein batao!"],
        ["cta", "Follow + Subscribe karo. Roz raat 9 baje YouTube LIVE!"],
        ["disclaimer", DISCLAIMER],
    ]


def explain_slide():
    return [["tag", "SAMJHO"], ["title", TODO], ["text", TODO], ["list", [TODO]]]


def daily(events, day):
    start = datetime(day.year, day.month, day.day, DAY_STARTS, tzinfo=IST)
    todays = pick([e for e in events if start <= e["ist"] < start + timedelta(days=1)])
    if not todays:
        return None, []
    ls = lines(todays, day)
    label = "HIGH impact" if todays[0]["impact"] == "High" else "MEDIUM impact"
    slides = [[
        ["tag", "FOREX NEWS"],
        ["title", "Aaj Ke Bade Forex News"],
        ["text", f"{day.strftime('%A')}, {day.day} {day.strftime('%b')} | Sab time IST mein"],
        ["box", f"Aaj {len(ls)} {label} news"],
    ]]
    for i, part in enumerate(chunks(ls, PER_SLIDE)):
        tag = "AAJ KA CALENDAR" + (f" ({i + 1})" if len(ls) > PER_SLIDE else "")
        slides.append([["tag", tag], ["title", "Time Note Kar Lo"], ["list", part]])
    slides += [explain_slide(), SAFETY, closing("Aaj Kaunsi News Par Nazar Rakhoge?")]
    return slides, todays


def weekly(events, week_start):
    days = [week_start + timedelta(d) for d in range(7)]
    week = pick([e for e in events if e["ist"].date() in days])
    if not week:
        return None, []
    trading = [d for d in days if any(e["ist"].date() == d for e in week)]
    first, last = trading[0], trading[-1]
    total = len(lines(week))
    slides = [[
        ["tag", "WEEKLY CALENDAR"],
        ["title", "Is Hafte Ke Bade Forex News"],
        ["text", f"{first.day} {first.strftime('%b')} - {last.day} {last.strftime('%b')} | Sab time IST mein"],
        ["box", f"Is hafte {total} bade news events"],
    ]]
    for d in trading:
        ls = lines([e for e in week if e["ist"].date() == d])
        for i, part in enumerate(chunks(ls, PER_SLIDE)):
            tag = f"{d.strftime('%A').upper()}, {d.day} {d.strftime('%b').upper()}"
            if len(ls) > PER_SLIDE:
                tag += f" ({i + 1})"
            slides.append([["tag", tag], ["list", part]])
    slides += [explain_slide(), SAFETY, closing("Is Hafte Kaunsi News Sabse Badi Lagti Hai?")]
    return slides, week


def main():
    mode, day, out = sys.argv[1], date.fromisoformat(sys.argv[2]), sys.argv[3]
    feed = sys.argv[4] if len(sys.argv) > 4 else None
    events = to_ist(load_feed(feed))
    slides, used = (daily if mode == "daily" else weekly)(events, day)
    if not slides:
        print("no news events for", mode, day)
        sys.exit(3)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "events.json"), "w", encoding="utf-8") as f:
        json.dump([{**e, "ist": e["ist"].isoformat()} for e in used], f, ensure_ascii=False, indent=2)
    content = {"topic": f"Forex news {mode} {day}", "slides": slides, "narration": [TODO] * len(slides)}
    with open(os.path.join(out, "content.json"), "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    print(f"{len(slides)} slides, {len(used)} events ->", out)


if __name__ == "__main__":
    main()
