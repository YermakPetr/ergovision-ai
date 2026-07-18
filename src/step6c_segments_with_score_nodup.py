from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MINUTES_PATH = PROJECT_ROOT / "data" / "processed" / "interesting_minutes.csv"
OUT_PATH = PROJECT_ROOT / "data" / "processed" / "interesting_segments.csv"

df = pd.read_csv(MINUTES_PATH)

g = df.sort_values("minute").copy()

segments = []
current_start = None
current_end = None
current_features = set()
current_score = 0.0

for _, row in g.iterrows():
    minute = int(row["minute"])
    hits = str(row["hits"])

    feats = {
        item.split(":")[0]
        for item in hits.split(";")
        if ":" in item
    }

    score = float(row["minute_score"])

    if current_start is None:
        current_start = minute
        current_end = minute
        current_features = set(feats)
        current_score = score
        continue

    if minute == current_end + 1:
        current_end = minute
        current_features |= feats
        current_score = max(current_score, score)
    else:
        segments.append({
            "start_minute": current_start,
            "end_minute": current_end,
            "features": ";".join(sorted(current_features)),
            "segment_score": round(current_score, 3)
        })
        current_start = minute
        current_end = minute
        current_features = set(feats)
        current_score = score

if current_start is not None:
    segments.append({
        "start_minute": current_start,
        "end_minute": current_end,
        "features": ";".join(sorted(current_features)),
        "segment_score": round(current_score, 3)
    })

out_df = pd.DataFrame(
    segments,
    columns=[
        "start_minute",
        "end_minute",
        "features",
        "segment_score",
    ],
)

if not out_df.empty:
    out_df = out_df.sort_values(
        "segment_score",
        ascending=False,
    )
out_df.to_csv(OUT_PATH, index=False)

print("Saved:", OUT_PATH)
print("Segments:", len(out_df))
print(out_df.head(10))