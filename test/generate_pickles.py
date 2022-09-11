import os
import subprocess
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from finance import Utils

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")
