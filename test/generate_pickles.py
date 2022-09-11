from finance import Utils

import os
import subprocess

os.environ["MODE"] = Utils.PICKLE_GENERATION_MODE
subprocess.getoutput("pytest")
