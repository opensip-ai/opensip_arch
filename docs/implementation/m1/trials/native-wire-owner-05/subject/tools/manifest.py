#!/usr/bin/env python3
"""Write subject-files.json: the explicit complete subject file list (candidate 05).

Groups (tools/filelist.py is the source of truth; subject-files.json is an OUTPUT and is read by nothing in check or
selftest):
  inputs   - the execution closure of build, check, selftest and isolation; isolation.py copies exactly these.
  outputs  - generated run results (check-result.json, selftest-result.json, isolation-result.json, outcome.json).
  evidence - preserved prior subject and review evidence under prior/ that is not an input (read by nothing).
subject-files.json does not list itself. The harness files belong to the session, not the subject.

    PYTHONDONTWRITEBYTECODE=1 python3 -B tools/manifest.py [--inputs-only]
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import filelist as FL  # noqa: E402

SELF = "subject-files.json"


def row(p):
    b = (ROOT / p).read_bytes()
    return {"path": p, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def main(with_outputs=True):
    evidence = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "prior").rglob("*") if p.is_file() and str(p.relative_to(ROOT)) not in FL.INPUTS)
    outputs = [p for p in FL.OUTPUTS if p != SELF]
    listed = set(FL.INPUTS) | set(outputs) | set(evidence) | {SELF}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and "tmp" not in p.relative_to(ROOT).parts}
    unlisted = sorted(actual - listed - FL.HARNESS)
    missing = sorted(p for p in FL.INPUTS if not (ROOT / p).is_file())
    if unlisted or missing:
        raise SystemExit("unlisted subject files: " + ", ".join(unlisted) + " | missing inputs: " + ", ".join(missing))
    doc = {"standing": "AUTHOR candidate 05 explicit complete subject file list; not approval. tmp/ is scratch and excluded. The execution closure is exactly `inputs` (tools/filelist.py); this file itself is an output.",
           "inputs": [row(p) for p in FL.INPUTS],
           "outputs": [row(p) for p in outputs if with_outputs and (ROOT / p).exists()],
           "evidence": [row(p) for p in evidence],
           "excludedHarness": sorted(FL.HARNESS)}
    (ROOT / SELF).write_text(json.dumps(doc, indent=1) + "\n")
    print({"inputs": len(doc["inputs"]), "outputs": len(doc["outputs"]), "evidence": len(doc["evidence"])})


if __name__ == "__main__":
    main(with_outputs="--inputs-only" not in sys.argv)
