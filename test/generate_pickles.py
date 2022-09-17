import os
import shutil
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).parent
sys.path.append(str(DIR.parent))
from finance import Utils, Format

SUCCESS_STR = Format.GREEN + \
              "##########################################################################\n" + \
              "#                         GENERATED ALL PICKLES!                         #\n" + \
              "##########################################################################"   + \
              Format.NONE

for path in DIR.glob("Test*"):
    if path.is_dir():
        shutil.rmtree(path)

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")

try:
    subprocess.check_output("pytest", stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    print(SUCCESS_STR)
except subprocess.CalledProcessError as exc:
    print(f"{Format.RED}{exc.output}{Format.NONE}")