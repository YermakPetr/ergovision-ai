import pandas as pd
import matplotlib.pyplot as plt

from config import PROJECT_ROOT, INTERESTING_MINUTES_CSV

OUT_PNG = PROJECT_ROOT / "data" / "processed" / "timeline_interesting.png"

df = pd.read_csv(INTERESTING_MINUTES_CSV)

x = df["minute"].astype(int).tolist()
y = df["minute_score"].astype(float).tolist()

plt.figure()
plt.scatter(x, y)


def short_feature_name(name: str) -> str:
    return name.replace("_mean", "").replace("_", "")

for _, r in df.iterrows():
    minute = int(r["minute"])
    score = float(r["minute_score"])

    hits = str(r["hits"])  
    feat_names = []
    for part in hits.split(";"):
        if ":" in part:
            feat = part.split(":", 1)[0].strip()
            feat_names.append(short_feature_name(feat))

    feat_names = sorted(set(feat_names))
    label = "+".join(feat_names)

    plt.text(minute + 0.2, score, label, fontsize=9)

plt.title("Interesting minutes (score)")
plt.xlabel("minute")
plt.ylabel("minute_score")
plt.grid(True)

OUT_PNG.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(
    OUT_PNG,
    dpi=150,
    bbox_inches="tight",
)

plt.close()

print("Saved:", OUT_PNG)