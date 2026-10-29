"""Turn a sequence of 1080x1920 frames into a cross-faded reel over an original synthesized track.

CLI: python tools/make_reel.py OUT.mp4 SECONDS_PER_FRAME frame1.png frame2.png ...
"""
import os
import subprocess
import sys
import tempfile

import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_music  # noqa: E402

FADE = 0.5


def build_reel(frames, durs, out_path):
    length = sum(durs) - FADE * (len(durs) - 1)
    offsets, offset = [], 0.0
    for i in range(1, len(durs)):
        offset += durs[i - 1] - FADE
        offsets.append(offset)

    with tempfile.TemporaryDirectory() as tmp:
        music = os.path.join(tmp, "music.wav")
        make_music.main(music, length, [o + FADE / 2 for o in offsets])

        cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error"]
        for frame, dur in zip(frames, durs):
            cmd += ["-loop", "1", "-t", str(dur), "-i", frame]
        cmd += ["-i", music]
        parts, prev = [], "[0:v]"
        for i, offset in enumerate(offsets, start=1):
            label = f"[v{i}]"
            parts.append(f"{prev}[{i}:v]xfade=transition=fade:duration={FADE}:offset={offset:.2f}{label}")
            prev = label
        parts.append(f"{prev}scale=1080:1920,format=yuv420p,fps=30[vout]")
        cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{len(durs)}:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "128k", "-ac", "2",
                "-shortest", "-movflags", "+faststart", out_path]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    out, secs, frames = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
    build_reel(frames, [secs] * len(frames), out)
    print("done", out)
