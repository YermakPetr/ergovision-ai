from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
csv_path = PROJECT_ROOT / "data" / "processed" / "features_1min.csv"

print("CSV:", csv_path)

df = pd.read_csv(csv_path)
print("Rows:", len(df))
print("Columns:", list(df.columns))
print(df.head(10))

x = df["minute"] if "minute" in df.columns else range(len(df))

to_plot = [
    ("shoulder_mean", "Shoulder mean"),
    ("headroll_mean", "Head roll mean"),
    ("mouth_mean", "Mouth mean"),
]

for col, title in to_plot:
    if col not in df.columns:
        print(f"Skip: no column {col}")
        continue

    plt.figure()
    plt.plot(x, df[col], marker="o")
    plt.title(title)
    plt.xlabel("minute")
    plt.ylabel(col)
    plt.grid(True)


plt.show()