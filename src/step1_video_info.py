from pathlib import Path
import cv2

current_file = Path(__file__)
current_file = current_file.resolve()
project_root = current_file.parents[1]
print("Project root:", project_root)

video_path = project_root / "data" / "raw" / "lecture.mp4"
print("Video path:", video_path)

if not video_path.exists():
    print("ERROR: video file not found!")
    exit()

print("Video file found!")
cap = cv2.VideoCapture(str(video_path))

if not cap.isOpened():
    print("ERROR: OpenCV cannot open video")
    exit()

print("Video successfully opened")
fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if fps <= 0:
    print("ERROR: invalid video FPS")
    cap.release()
    raise SystemExit(1)

duration_sec = frame_count / fps
duration_min = duration_sec / 60

print("FPS:", fps)
print("Total frames:", frame_count)
print("Duration (min):", round(duration_min, 2))
ret, frame = cap.read()

if not ret:
    print("ERROR: cannot read first frame")
    exit()

print("First frame read successfully")
print("Frame shape:", frame.shape)

out_dir = project_root / "data" / "processed"
out_dir.mkdir(parents=True, exist_ok=True)

out_image_path = out_dir / "first_frame.jpg"
cv2.imwrite(str(out_image_path), frame)

cap.release()

print("Saved first frame to:", out_image_path)
print("Step 1 works")