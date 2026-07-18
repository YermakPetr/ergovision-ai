from pathlib import Path
import json
import time

import cv2
import mediapipe as mp


SAMPLING_FPS = 5          
MAX_PROCESSED_FRAMES = None 


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "lecture.mp4"
OUT_DIR = PROJECT_ROOT / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "landmarks.jsonl"

print("Video:", VIDEO_PATH)
print("Output file:", OUT_FILE)


cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    raise RuntimeError("Cannot open video")

video_fps = cap.get(cv2.CAP_PROP_FPS)

if video_fps <= 0:
    cap.release()
    raise RuntimeError("Cannot determine video FPS")

step = max(int(round(video_fps / SAMPLING_FPS)), 1)

print("Video FPS:", video_fps)
print("Sampling FPS:", SAMPLING_FPS)
print("Frame step:", step)


mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh

pose = mp_pose.Pose()  
face = mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)

print("MediaPipe models created")


processed = 0
frame_index = 0
start_time = time.time()

with open(OUT_FILE, "w", encoding="utf-8") as f:
    while True:
        ret, frame_bgr = cap.read()
        if not ret:
            break

        if frame_index % step != 0:
            frame_index += 1
            continue

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        pose_res = pose.process(frame_rgb)
        face_res = face.process(frame_rgb)

        pose_landmarks = []
        if pose_res.pose_landmarks:
            for lm in pose_res.pose_landmarks.landmark:
                pose_landmarks.append([lm.x, lm.y, lm.z, lm.visibility])

        face_landmarks = []
        if face_res.multi_face_landmarks:
            for lm in face_res.multi_face_landmarks[0].landmark:
                face_landmarks.append([lm.x, lm.y, lm.z])

        record = {
            "frame_index": frame_index,
            "time_sec": frame_index / video_fps,
            "pose": pose_landmarks,
            "face": face_landmarks,
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

        processed += 1

        if processed % 50 == 0:
            elapsed = time.time() - start_time
            speed = processed / elapsed if elapsed > 0 else 0
            print(f"Processed: {processed} | Speed: {speed:.1f} frames/s")

        if MAX_PROCESSED_FRAMES is not None and processed >= MAX_PROCESSED_FRAMES:
            print("Stopped early for dev test")
            break

        frame_index += 1


cap.release()
pose.close()
face.close()

print("Done. Saved frames:", processed)
print("File:", OUT_FILE)