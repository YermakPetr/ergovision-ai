from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
path = PROJECT_ROOT / "data" / "processed" / "features.jsonl"

if not path.exists():
    raise FileNotFoundError(f"Features file not found: {path}")

with open(path, "r", encoding="utf-8") as file:
    for index in range(3):
        line = file.readline().strip()

        if not line:
            break

        record = json.loads(line)
        print(record)