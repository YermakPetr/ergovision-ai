from pathlib import Path
import json
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
in_path = PROJECT_ROOT / "data" / "processed" / "features.jsonl"
out_path = PROJECT_ROOT / "data" / "processed" / "features_1min.csv"

rows = []
with open(in_path, "r", encoding="utf-8") as f:
    for line in f:
        rec = json.loads(line)
        t = float(rec["time_sec"])
        minute = int(t // 60)

        rows.append({
            "minute": minute,
            "shoulder_height_diff": rec.get("shoulder_height_diff"),
            "head_roll_deg": rec.get("head_roll_deg"),
            "mouth_open_ratio": rec.get("mouth_open_ratio"),
        })

df = pd.DataFrame(rows)

agg = df.groupby("minute").agg(
    samples_shoulder=("shoulder_height_diff", "count"),
    shoulder_mean=("shoulder_height_diff", "mean"),
    shoulder_min=("shoulder_height_diff", "min"),
    shoulder_max=("shoulder_height_diff", "max"),

    samples_headroll=("head_roll_deg", "count"),
    headroll_mean=("head_roll_deg", "mean"),
    headroll_min=("head_roll_deg", "min"),
    headroll_max=("head_roll_deg", "max"),

    samples_mouth=("mouth_open_ratio", "count"),
    mouth_mean=("mouth_open_ratio", "mean"),
    mouth_min=("mouth_open_ratio", "min"),
    mouth_max=("mouth_open_ratio", "max"),
).reset_index()

out_path.parent.mkdir(parents=True, exist_ok=True)
agg.to_csv(out_path, index=False, encoding="utf-8")

print("IN :", in_path)
print("OUT:", out_path)
print("Minutes:", len(agg))
print(agg.head(5))