# Host reel (split-screen), every other day

Format approved by Pravin on 14 Nov 2026 (test: `reels/test-2026-11-14-split/`).
Top half: a fictional AI host talks (3 Google Flow clips) and animated trading cards cut in.
Bottom half: a navy+gold "poster" whose steps light up as the host talks about them.
Builder: `C:\Users\pravi\Documents\motivation-posts\tools\split_reel.py` (theme `captain`).

## Host
- Start frame: `character/host_trader_v2.png`. He is a fictional young Indian man: neat hair, trimmed beard,
  navy blazer, white tee, home trading desk. Never use Pravin's own photos (`character/pravin_ref/`,
  `host_pravin_v*.png`); Pravin said no on 14 Nov.
- Prompt template: `reels/host_prompt.txt` (`{line}` = the Devanagari line). Keep its wording.

## reels/D/script.json
Copy the shape of `reels/test-2026-11-14-split/script.json`:
- `theme`: "captain". `host_crop_y`: 150. `face`: [540, 470].
- `footer`: "Sirf educational. Financial advice nahi. Forex me high risk hai.|n|AI generated video | Trade With Captain Pravin"
- `hook`: Hinglish question/claim, at most 7 words.
- `poster`: `title_small` (2-3 words), `title_big` (at most 12 characters, caps, e.g. "3 SIGNS", "3 RULES"),
  exactly 3 `steps`, each with `label` ("Sign 01"), `title` (max ~18 chars), `sub` (max ~32 chars), and
  `on` ([shot, fraction]: when that step lights up). Usually: step 1 [2, 0.0], step 2 [2, 0.5], step 3 [3, 0.0].
- `cta`: {"text": "Follow @tradewithcaptainpravin", "on": [3, 0.62]}
- `shots`: exactly 3. Each has:
  - `dialogue`: Hinglish in Roman script, 12-15 words, with 1-2 `*key*` words. These are the captions.
  - `dialogue_hi`: the same line in Devanagari, which is what the host speaks. Write English trading words
    in Devanagari (ट्रेड, लॉस, लॉट साइज़) and numbers as words.
  - Shot 1 is the hook and names the viewer's problem. Shot 2 covers points 1 and 2. Shot 3 covers point 3,
    then a 3-4 word takeaway, then "फ़ॉलो करो".
  - `broll`: 1-2 cards per shot, `{"at": f, "to": f, "card": {...}}` (fractions of that shot's speech; leave
    some host time in every shot). Card types:
    - `chart` {label, title, bubble}: candles plus a pop-up bubble
    - `trades` {label, title, rows: [[time, pair, "-$20", "red"|"green"]], note}
    - `counter` {label, to, warn, caption, note}
    - `lots` {label, title, bars: [[label, value, height 0..1]], note}
    - `checklist` {label, title, items}
    - `note` {label, title, lines}
    - `chat` {label, title, messages: [{from: me|her, text}]}
    - `quote` {label, text with *key*}
    - `clock` {label, time, thoughts}
    Labels are short ("Sign 01 · Revenge trade"). All numbers must be correct and only illustrative.

## Content rules (same as AGENT.md)
Education only. No buy/sell signals, no "ye pair kharido", no price predictions, no profit promises, no fake
profit screenshots. The AI-generated label and the disclaimer footer always stay on screen.
