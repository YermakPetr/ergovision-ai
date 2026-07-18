from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
path = PROJECT_ROOT / "data" / "processed" / "landmarks.jsonl"

if not path.exists():
    raise FileNotFoundError(f"Landmarks file not found: {path}")

with open(path, "r", encoding="utf-8") as file:
    first_line = file.readline().strip()

if not first_line:
    raise ValueError(f"Landmarks file is empty: {path}")

first_record = json.loads(first_line)

print("Keys:", list(first_record.keys()))
print("Frame index:", first_record["frame_index"])
print("Time (sec):", first_record["time_sec"])
print("Pose points:", len(first_record["pose"]))
print("Face points:", len(first_record["face"]))