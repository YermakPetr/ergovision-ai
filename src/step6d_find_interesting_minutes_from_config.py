import pandas as pd
from config import FEATURES_1MIN_CSV, INTERESTING_MINUTES_CSV, FEATURE_THRESHOLDS, MIN_HITS

df = pd.read_csv(FEATURES_1MIN_CSV)

stats = {}
for feat in FEATURE_THRESHOLDS.keys():
    stats[feat] = (df[feat].mean(), df[feat].std())

rows = []
for _, r in df.iterrows():
    minute = int(r["minute"])
    hits = []

    for feat, thr in FEATURE_THRESHOLDS.items():
        mean, std = stats[feat]
        if std == 0 or pd.isna(std):
            continue
        z = (r[feat] - mean) / std
        if abs(z) >= thr:
            hits.append((feat, float(z)))

    if len(hits) >= MIN_HITS:
        minute_score = max(abs(z) for _, z in hits)
        rows.append({
            "minute": minute,
            "hits": ";".join(f"{feat}:{z:.3f}" for feat, z in hits),
            "minute_score": round(minute_score, 3),
        })

out_df = pd.DataFrame(
    rows,
    columns=["minute", "hits", "minute_score"]
)

if not out_df.empty:
    out_df = out_df.sort_values(
        ["minute_score", "minute"],
        ascending=[False, True]
    )

out_df.to_csv(INTERESTING_MINUTES_CSV, index=False)

print("Saved:", INTERESTING_MINUTES_CSV)
print("Minutes found:", len(out_df))
print(out_df.head(15))