from datetime import datetime

import pandas as pd

from config import (
    PROJECT_ROOT,
    FEATURE_THRESHOLDS,
    MIN_HITS,
    PADDING_SEC,
    INTERESTING_MINUTES_CSV,
    INTERESTING_SEGMENTS_CSV,
)

REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "report.md"

def hhmmss(total_sec: int) -> str:
    total_sec = int(total_sec)

    h = total_sec // 3600
    m = (total_sec % 3600) // 60
    s = total_sec % 60

    return f"{h:02d}:{m:02d}:{s:02d}"

lines = []
lines.append(f"# ErgoVision AI report")
lines.append("")
lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
lines.append("")
lines.append("## Config")
lines.append(f"- MIN_HITS: {MIN_HITS}")
lines.append(f"- PADDING_SEC: {PADDING_SEC}")
lines.append("- FEATURE_THRESHOLDS:")
for k, v in FEATURE_THRESHOLDS.items():
    lines.append(f"  - {k}: {v}")
lines.append("")

# counts
mins = pd.read_csv(INTERESTING_MINUTES_CSV)
segs = pd.read_csv(INTERESTING_SEGMENTS_CSV)

lines.append("## Summary")
lines.append(f"- Interesting minutes: {len(mins)}")
lines.append(f"- Interesting segments: {len(segs)}")
lines.append("")

lines.append("## Timeline plot")
lines.append("")

lines.append("## Top segments")
top = segs.sort_values("segment_score", ascending=False).head(10)

for _, r in top.iterrows():
    s = int(r["start_minute"]) * 60
    e = (int(r["end_minute"]) + 1) * 60
    score = float(r["segment_score"])
    feats = str(r["features"])
    lines.append(f"- {hhmmss(s)}–{hhmmss(e)} | score={score:.3f} | {feats}")

REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
print("Saved:", REPORT_PATH)