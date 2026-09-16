"""Create scratch copies inside this runtime (never elsewhere).

usage: make_scratch.py <name> <source-root>   -> <runtime>/scratch-<name>/candidate
"""
import os
import shutil
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
name, source = sys.argv[1], Path(sys.argv[2])
dest = RUNTIME / ("scratch-" + name) / "candidate"
if dest.exists():
    raise SystemExit("exists: " + str(dest))
shutil.copytree(source, dest, symlinks=True)
print(dest, sum(len(files) for _, _, files in os.walk(dest)))
