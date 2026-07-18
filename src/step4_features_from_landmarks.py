from pathlib import Path
import json
import math


POSE_LEFT_SHOULDER = 11
POSE_RIGHT_SHOULDER = 12

FACE_RIGHT_EYE_OUTER = 33
FACE_LEFT_EYE_OUTER = 263

FACE_UPPER_LIP = 13
FACE_LOWER_LIP = 14


def safe_get(points, idx):
    """Return the point at the given index, or None if it does not exist."""
    if points is None:
        return None
    if idx < 0 or idx >= len(points):
        return None
    return points[idx]


def dist2d(a, b):
    """Calculate the distance between two 2D points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def angle_deg(a, b):
    """Calculate the angle from point a to point b in degrees."""
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.degrees(math.atan2(dy, dx))


PROJECT_ROOT = Path(__file__).resolve().parents[1]
IN_FILE = PROJECT_ROOT / "data" / "processed" / "landmarks.jsonl"
OUT_FILE = PROJECT_ROOT / "data" / "processed" / "features.jsonl"

print("IN :", IN_FILE)
print("OUT:", OUT_FILE)

with open(IN_FILE, "r", encoding="utf-8") as fin, open(
    OUT_FILE, "w", encoding="utf-8"
) as fout:
    for line in fin:
        record = json.loads(line)

        frame_index = record["frame_index"]
        time_sec = record["time_sec"]
        pose_points = record["pose"]
        face_points = record["face"]

        left_shoulder = safe_get(pose_points, POSE_LEFT_SHOULDER)
        right_shoulder = safe_get(pose_points, POSE_RIGHT_SHOULDER)

        if left_shoulder is not None and right_shoulder is not None:
            shoulder_height_diff = right_shoulder[1] - left_shoulder[1]
        else:
            shoulder_height_diff = None

        right_eye = safe_get(face_points, FACE_RIGHT_EYE_OUTER)
        left_eye = safe_get(face_points, FACE_LEFT_EYE_OUTER)

        if right_eye is not None and left_eye is not None:
            head_roll_deg = angle_deg(right_eye, left_eye)
        else:
            head_roll_deg = None

        upper_lip = safe_get(face_points, FACE_UPPER_LIP)
        lower_lip = safe_get(face_points, FACE_LOWER_LIP)

        if (
            upper_lip is not None
            and lower_lip is not None
            and right_eye is not None
            and left_eye is not None
        ):
            mouth_open = dist2d(upper_lip, lower_lip)
            eye_width = dist2d(right_eye, left_eye)
            mouth_open_ratio = mouth_open / eye_width if eye_width > 0 else None
        else:
            mouth_open_ratio = None

        output_record = {
            "frame_index": frame_index,
            "time_sec": time_sec,
            "shoulder_height_diff": shoulder_height_diff,
            "head_roll_deg": head_roll_deg,
            "mouth_open_ratio": mouth_open_ratio,
        }

        fout.write(json.dumps(output_record, ensure_ascii=False) + "\n")

print("Done.")