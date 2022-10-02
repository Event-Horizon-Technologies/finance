#need to do this first
from pathlib import Path
import sys
DIR = Path(__file__).parent
sys.path.append(str(DIR.parent))

#our package imports first
from finance import Utils

#then other imports
import os
import shutil
import subprocess

SUCCESS_STR = Utils.Format.GREEN + \
              "##########################################################################\n" + \
              "#                         GENERATED ALL PICKLES!                         #\n" + \
              "##########################################################################"   + \
              Utils.Format.NONE

for path in DIR.glob("Test*"):
    if path.is_dir():
        shutil.rmtree(path)

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")

try:
    subprocess.check_output("pytest", stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    print(SUCCESS_STR)
except subprocess.CalledProcessError as exc:
    print(f"{Utils.Format.RED}{exc.output}{Utils.Format.NONE}")