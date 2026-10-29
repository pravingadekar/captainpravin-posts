"""ElevenLabs text-to-speech: one MP3 per line of narration.

Needs ELEVENLABS_API_KEY in the environment (never hard-code it). ELEVENLABS_VOICE_ID overrides the default voice.
"""
import json
import os
import urllib.request

# "Heena M – Influencer UGC Voice": Hindi (hi-IN), female, upbeat
DEFAULT_VOICE = "7PoJrtDD6yvTa56HTDt1"
MODEL = "eleven_multilingual_v2"


def available():
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def speak(text, out_path):
    voice = os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE)
    body = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.3},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp, open(out_path, "wb") as f:
        f.write(resp.read())


def speak_all(lines, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, line in enumerate(lines, start=1):
        path = os.path.join(out_dir, f"voice{i}.mp3")
        speak(line, path)
        paths.append(path)
    return paths
