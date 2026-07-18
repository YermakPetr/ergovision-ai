from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable  

SCRIPTS = [
    "src/step6d_find_interesting_minutes_from_config.py",
    "src/step6c_segments_with_score_nodup.py",
    "src/step7_export_clips_ffmpeg.py",
    "src/step8b_plot_interesting_timeline.py",
    "src/step8_make_report.py",
]
for rel in SCRIPTS:
    script_path = PROJECT_ROOT / rel
    print("\n" + "=" * 60)
    print("RUN:", script_path)
    print("=" * 60)

    subprocess.run([PY, str(script_path)], check=True)

print("\n✅ Pipeline done.")