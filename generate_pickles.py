#!/usr/bin/env python3
import os
import shutil
import subprocess
from pathlib import Path

from finance import Utils

DIR = Path(__file__).parent
SUCCESS_STR = Utils.Format.green(
    "##########################################################################\n"
    "#                         GENERATED ALL PICKLES!                         #\n"
    "##########################################################################"
)
for path in DIR.glob("Test*"):
    if path.is_dir():
        shutil.rmtree(path)

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")

try:
    subprocess.check_output(
        "pytest", stderr=subprocess.STDOUT, shell=True, universal_newlines=True
    )
    print(SUCCESS_STR)
except subprocess.CalledProcessError as exc:
    print(Utils.Format.red(exc.output))
