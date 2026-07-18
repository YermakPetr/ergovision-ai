from pathlib import Path
import subprocess

import pandas as pd

from config import (
    VIDEO_PATH,
    INTERESTING_SEGMENTS_CSV,
    FFMPEG_PATH,
    PADDING_SEC,
    DRAW_TEXT,
    OUT_CLIPS_DIRNAME,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SEG_PATH = INTERESTING_SEGMENTS_CSV
OUT_DIR = PROJECT_ROOT / "data" / "processed" / OUT_CLIPS_DIRNAME
OUT_DIR.mkdir(parents=True, exist_ok=True)


def hhmmss(total_sec: int) -> str:
    total_sec = int(total_sec)
    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


df = pd.read_csv(SEG_PATH)

if "segment_score" in df.columns:
    df = df.sort_values("segment_score", ascending=False).reset_index(drop=True)

for rank, row in df.iterrows():
    start_min = int(row["start_minute"])
    end_min = int(row["end_minute"])
    feats_raw = str(row["features"])
    score = float(row["segment_score"]) if "segment_score" in df.columns else 0.0

    feats_safe = feats_raw.replace(";", "_")
    score_tag = f"score{score:.2f}"

    start_sec = start_min * 60 - PADDING_SEC
    if start_sec < 0:
        start_sec = 0

    end_sec = (end_min + 1) * 60 + PADDING_SEC
    duration_sec = end_sec - start_sec

    out_name = f"rank_{rank:02d}_{start_min:03d}-{end_min:03d}_{score_tag}_{feats_safe}.mp4"
    out_path = OUT_DIR / out_name

    if DRAW_TEXT:
        orig_start_str = hhmmss(start_sec).replace(":", r"\:")
        features_str = feats_raw.replace(":", r"\:")
        score_str = f"{score:.3f}"

        vf = (
            "drawtext="
            "font=Arial:fontcolor=white:fontsize=24:"
            "box=1:boxcolor=black@0.5:boxborderw=8:"
            "x=20:y=20:"
            f"text='ORIG_START {orig_start_str} | CLIP %{{pts\\:hms}}',"
            "drawtext="
            "font=Arial:fontcolor=white:fontsize=22:"
            "box=1:boxcolor=black@0.5:boxborderw=8:"
            "x=20:y=60:"
            f"text='FEATURES {features_str}',"
            "drawtext="
            "font=Arial:fontcolor=white:fontsize=22:"
            "box=1:boxcolor=black@0.5:boxborderw=8:"
            "x=20:y=100:"
            f"text='SCORE {score_str}'"
        )

        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", str(start_sec),
            "-i", str(VIDEO_PATH),
            "-t", str(duration_sec),
            "-vf", vf,
            "-c:v", "libx264", "-crf", "18",
            "-c:a", "aac",
            str(out_path)
        ]
    else:
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", str(start_sec),
            "-i", str(VIDEO_PATH),
            "-t", str(duration_sec),
            "-c", "copy",
            str(out_path)
        ]

    print("RUN:", " ".join(cmd))
    subprocess.run(cmd, check=True)

print("Done. Clips in:", OUT_DIR)