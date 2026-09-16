#!/usr/bin/env python3
"""Write subject-files.json: the explicit complete subject file list.

Groups:
  inputs   - every file needed to rebuild, check and selftest (sufficient on its own plus the pinned architecture
             snapshot and the declared reference environment); isolation.py copies exactly these.
  outputs  - generated run results (check-result.json, selftest-result.json, isolation-result.json, outcome.json).
  evidence - preserved prior subject-01 and review-01 evidence (read by nothing).
subject-files.json does not list itself (no self-pin). The harness files launch-public.py, process.json, prompt.md and
public-events.jsonl belong to the session, not the subject.

    PYTHONDONTWRITEBYTECODE=1 python3 -B tools/manifest.py
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ["contract.md", "successor.json", "wire-carriers.v1.json", "wire-carriers.meta.schema.json", "field-coverage.json",
          "admission-vectors.json", "p3-guard-successor.v1.json", "reference-environment.json", "check.py", "selftest.py",
          "tools/common.py", "tools/records_ts2.py", "tools/records_rust3.py", "tools/rules.py", "tools/succ.py", "tools/build.py",
          "tools/vectors.py", "tools/wirecodec.py", "tools/admission_ref.py", "tools/check_static.py", "tools/check_reference.py",
          "tools/manifest.py", "tools/isolation.py", "tools/outcome.py",
          "inputs/ts2-fields.json", "inputs/rust3-fields.json", "inputs/generator-candidate03-options.json"]
OUTPUTS = ["check-result.json", "selftest-result.json", "isolation-result.json", "outcome.json"]
HARNESS = {"launch-public.py", "process.json", "prompt.md", "public-events.jsonl", "subject-files.json"}


def row(p):
    b = (ROOT / p).read_bytes()
    return {"path": p, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def main(with_outputs=True):
    evidence = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "prior").rglob("*") if p.is_file())
    listed = set(INPUTS) | set(OUTPUTS) | set(evidence)
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and "tmp" not in p.relative_to(ROOT).parts}
    unlisted = sorted(actual - listed - HARNESS)
    if unlisted:
        raise SystemExit("unlisted subject files: " + ", ".join(unlisted))
    doc = {"standing": "AUTHOR candidate 02 explicit complete subject file list; not approval. tmp/ is scratch and excluded.",
           "inputs": [row(p) for p in INPUTS],
           "outputs": [row(p) for p in OUTPUTS if with_outputs and (ROOT / p).exists()],
           "evidence": [row(p) for p in evidence],
           "excludedHarness": sorted(HARNESS - {"subject-files.json"})}
    (ROOT / "subject-files.json").write_text(json.dumps(doc, indent=1) + "\n")
    print({"inputs": len(doc["inputs"]), "outputs": len(doc["outputs"]), "evidence": len(doc["evidence"])})


if __name__ == "__main__":
    import sys
    main(with_outputs="--inputs-only" not in sys.argv)
