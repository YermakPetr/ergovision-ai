from pathlib import Path
import cv2
import mediapipe as mp

project_root = Path(__file__).resolve().parents[1]

video_path = project_root / "data" / "raw" / "lecture.mp4"
out_dir = project_root / "data" / "processed"
out_dir.mkdir(parents=True, exist_ok=True)
print("Project root:", project_root)
print("Video path:", video_path)

cap = cv2.VideoCapture(str(video_path))
if not cap.isOpened():
    raise RuntimeError("Cannot open video: " + str(video_path))

ret, frame_bgr = cap.read()
cap.release()

if not ret:
    raise RuntimeError("Cannot read first frame")

print("Frame shape:", frame_bgr.shape)

frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
print("Converted BGR -> RGB")

mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

with mp_pose.Pose(
    static_image_mode=True,
) as pose, mp_face.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
) as face:
    pose_res = pose.process(frame_rgb)
    face_res = face.process(frame_rgb)

print("Pose landmarks detected:", pose_res.pose_landmarks is not None)
print("Face landmarks detected:", bool(face_res.multi_face_landmarks))

annotated = frame_bgr.copy()

if pose_res.pose_landmarks:
    mp_draw.draw_landmarks(
        annotated,
        pose_res.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style(),
    )

if face_res.multi_face_landmarks:
    mp_draw.draw_landmarks(
        annotated,
        face_res.multi_face_landmarks[0],
        mp_face.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style(),
    )

out_path = out_dir / "annotated_frame.jpg"
cv2.imwrite(str(out_path), annotated)
print("Saved:", out_path)
print("Step 2 works")