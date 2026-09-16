"""Run one command and keep its full stdout/stderr/exit as a numbered receipt (failures are kept).

usage: run_logged.py <receipt-name> <cwd> <arg> [<arg> ...]
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

RECEIPTS = Path(__file__).resolve().parents[1] / "receipts"
name, cwd, argv = sys.argv[1], sys.argv[2], sys.argv[3:]
RECEIPTS.mkdir(exist_ok=True)
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
receipt = {"name": name, "cwd": cwd, "argv": argv, "startedUtc": started, "exitCode": proc.returncode,
           "stdout": proc.stdout, "stderr": proc.stderr}
path = RECEIPTS / (name + ".json")
if path.exists():
    raise SystemExit("receipt exists, refusing to overwrite: " + str(path))
path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
sys.stdout.write(proc.stdout[-6000:])
sys.stderr.write(proc.stderr[-6000:])
print(f"\n[receipt {path.name} exit={proc.returncode}]")
sys.exit(0)
