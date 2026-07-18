from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "lecture.mp4"
FEATURES_1MIN_CSV = PROJECT_ROOT / "data" / "processed" / "features_1min.csv"
INTERESTING_MINUTES_CSV = PROJECT_ROOT / "data" / "processed" / "interesting_minutes.csv"
INTERESTING_SEGMENTS_CSV = PROJECT_ROOT / "data" / "processed" / "interesting_segments.csv"

FEATURE_THRESHOLDS = {
    "shoulder_mean": 2.0,
    "headroll_mean": 2.0,
    "mouth_mean": 2.0,
}

MIN_HITS = 1  

FFMPEG_PATH = r"C:\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
PADDING_SEC = 10
DRAW_TEXT = True
OUT_CLIPS_DIRNAME = "clips_scored" 