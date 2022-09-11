import os
import shutil
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).parent
sys.path.append(str(DIR.parent))
from finance import Utils

for path in DIR.glob("Test*"):
    if path.is_dir():
        shutil.rmtree(path)

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")
