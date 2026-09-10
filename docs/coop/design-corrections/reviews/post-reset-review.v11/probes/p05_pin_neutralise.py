#!/usr/bin/env python3
"""p05: isolate the stale-pin defect.

Builds a SECOND disposable copy in which the ONLY change is the two stale
`correction-crosswalk.proposed.json` pins updated to the actual frozen v11 digest, then re-runs
all six reference commands. If all six then pass with the declared counts, the defect is
localised to pin bookkeeping and the underlying evidence is otherwise sound. Nothing here is
proposed as a fix to the frozen subject; it is a severity probe only.
"""
import hashlib
import json
import os
import shutil
import subprocess

PY = "/tmp/opensip-architecture-review-env/bin/python"
SRC = "/tmp/opensip-design-corrections/candidate-subject.v11"
DST = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/subject-v11-pinfix"
DC = "docs/coop/design-corrections"
TARGET = f"{DC}/correction-crosswalk.proposed.json"
LEDGERS = [f"{DC}/security/source-pins.v1.json", f"{DC}/workflows/source-pins.v1.json"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


if os.path.exists(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)

actual = sha(os.path.join(DST, TARGET))
stale = "9560a51eed387b5f4879e9a05e039fffcdacaba5c390135ba13ed7fa5936fc4e"

edits = []
for ledger in LEDGERS:
    p = os.path.join(DST, ledger)
    text = open(p, "r").read()
    n = text.count(stale)
    text = text.replace(stale, actual)
    open(p, "w").write(text)
    edits.append({"ledger": ledger, "replacements": n})

spec = json.load(open(os.path.join(
    DST, f"{DC}/reviews/codex-post-reset.v1/final-reference.v11/reference-checks.json")))
ORIG = "/Users/sb/code/opensip-ai/opensip_arch/"

results = []
for entry in spec["commands"]:
    cmd = [os.path.join(DST, t[len(ORIG):]) if t.startswith(ORIG) else t
           for t in entry["command"]]
    proc = subprocess.run(cmd, cwd=DST, capture_output=True, text=True)
    results.append({
        "name": entry["name"],
        "declaredExitCode": entry["exitCode"],
        "observedExitCode": proc.returncode,
        "matches": proc.returncode == entry["exitCode"],
        "stdoutTail": proc.stdout[-600:].strip(),
    })

print(json.dumps({
    "onlyChange": "two stale crosswalk pins -> actual v11 digest",
    "actualCrosswalkDigest": actual,
    "edits": edits,
    "allSixPass": all(r["matches"] for r in results),
    "results": results,
}, indent=2))
