"""Run the statistical example and each executable animation demonstration."""
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parent
subprocess.run([sys.executable, 'worked_example.py'], cwd=root, check=True)
if shutil.which('ffmpeg') is None:
    raise SystemExit('Static results are ready. Install FFmpeg on PATH to render animations.')
for name in ['05_paired_scores.py', '06_case_metric.py', '07_paired_bootstrap.py',
             '08_resampling_and_clt.py', '09_exact_sign_flips.py',
             '10_interval_and_test.py', '11_dependent_frames.py']:
    print(f'Running {name}', flush=True)
    subprocess.run([sys.executable, name], cwd=root, check=True)
