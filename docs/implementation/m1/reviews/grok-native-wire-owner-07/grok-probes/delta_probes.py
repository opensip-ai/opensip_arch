"""Independent Grok delta probes for native07 wording correction. Writes only under review/results."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-native-review-07/review")
COPY = REVIEW / "copy"
PARENT = Path("/tmp/opensip-implementation/m1-native-wire-owner-subject-06")
RESULTS = REVIEW / "results"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
ARCH = "/Users/sb/code/opensip-ai/opensip_arch"
RESULTS.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(COPY / "tools"))
import filelist as FL  # noqa: E402


class Cases:
    def __init__(self):
        self.rows = []

    def rec(self, name, passed, **detail):
        self.rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name)
        return passed


def copy_inputs(dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    for rel in FL.INPUTS:
        dst = dest / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((COPY / rel).read_bytes())
    (dest / "tmp").mkdir(parents=True, exist_ok=True)


def run_check(root: Path, out_name: str):
    out = root / "tmp" / out_name
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": "/tmp",
        "OPENSIP_ARCH": ARCH,
        "TMPDIR": str(root / "tmp"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPYCACHEPREFIX": str(root / "tmp" / "pycache"),
    }
    proc = subprocess.run(
        [PY, "-I", "-B", "check.py", "--out", str(out)],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=2400,
    )
    doc = json.loads(out.read_text()) if out.exists() else {"results": [], "failed": -1, "returncode": proc.returncode}
    wording = next((r for r in doc.get("results", []) if r["id"] == "unpromoted-successor-authority-wording"), None)
    return proc.returncode, doc, wording, proc.stderr[-400:]


def main():
    C = Cases()
    wire = json.loads((COPY / "wire-carriers.v1.json").read_text())
    standing = wire["privateRepresentation"]["patternDialect"]["standing"]
    claim = re.compile(
        r"(?i)selected[ _-]*final[ _-]*owner|final[ _-]+owner|selectedOwner|approved[ _-]+(owner|successor)|authoritative[ _-]+owner"
    )
    promo = "effective as selected semantics only after root acceptance and source-bridge promotion"
    C.rec(
        "dialect-standing-has-promotion-condition",
        promo in standing and "proposed reference correction" in standing,
        standing=standing,
    )
    C.rec(
        "dialect-standing-no-selected-final-owner",
        not claim.search(standing),
        standing=standing,
        hits=[m.group(0) for m in claim.finditer(standing)],
    )
    C.rec(
        "full-carrier-no-premature-authority-claim",
        not claim.search(json.dumps(wire)),
        hits=sorted({m.group(0) for m in claim.finditer(json.dumps(wire))}),
    )
    parent_standing = json.loads((PARENT / "wire-carriers.v1.json").read_text())["privateRepresentation"]["patternDialect"]["standing"]
    C.rec(
        "parent06-standing-still-has-the-defect",
        "selected final owner" in parent_standing.lower(),
        parentStanding=parent_standing,
    )

    # Unchanged algorithm bytes vs native06.
    unchanged = [
        "tools/sender_ref.py",
        "tools/wirecodec.py",
        "tools/representability.py",
        "tools/admission_ref.py",
        "tools/owner_successor.py",
        "tools/check_reference.py",
        "check.py",
    ]
    algo = []
    for rel in unchanged:
        a = hashlib.sha256((PARENT / rel).read_bytes()).hexdigest()
        b = hashlib.sha256((COPY / rel).read_bytes()).hexdigest()
        algo.append({"path": rel, "match": a == b})
    C.rec("runtime-algorithms-unchanged-vs-native06", all(x["match"] for x in algo), files=algo)

    # Mutation 1: restore the previously missed phrase in patternDialect.standing.
    d1 = RESULTS / "mut-dialect-claim"
    copy_inputs(d1)
    w = json.loads((d1 / "wire-carriers.v1.json").read_text())
    w["privateRepresentation"]["patternDialect"]["standing"] += " The selected final owner."
    (d1 / "wire-carriers.v1.json").write_text(json.dumps(w, indent=1, ensure_ascii=False) + "\n")
    rc, doc, wording, err = run_check(d1, "mut1.json")
    C.rec(
        "mutation-dialect-selected-final-owner-fails-wording-check",
        wording is not None and wording["ok"] is False,
        returncode=rc,
        wording=wording,
        stderrTail=err,
    )

    # Mutation 2: drop the promotion condition from patternDialect.standing.
    d2 = RESULTS / "mut-dialect-promo"
    copy_inputs(d2)
    w = json.loads((d2 / "wire-carriers.v1.json").read_text())
    w["privateRepresentation"]["patternDialect"]["standing"] = w["privateRepresentation"]["patternDialect"]["standing"].replace(promo, "in force")
    (d2 / "wire-carriers.v1.json").write_text(json.dumps(w, indent=1, ensure_ascii=False) + "\n")
    rc, doc, wording, err = run_check(d2, "mut2.json")
    C.rec(
        "mutation-dialect-promotion-condition-removed-fails-wording-check",
        wording is not None and wording["ok"] is False,
        returncode=rc,
        wording=wording,
        stderrTail=err,
    )

    # Mutation 3: expanded scan — phrase in a non-admission carrier field.
    d3 = RESULTS / "mut-profile-claim"
    copy_inputs(d3)
    w = json.loads((d3 / "wire-carriers.v1.json").read_text())
    w["profiles"]["ts2-cbor"]["decodeRule"] += " selected final owner"
    (d3 / "wire-carriers.v1.json").write_text(json.dumps(w, indent=1, ensure_ascii=False) + "\n")
    rc, doc, wording, err = run_check(d3, "mut3.json")
    C.rec(
        "mutation-non-admission-field-fails-expanded-scan",
        wording is not None and wording["ok"] is False and "wire-carriers.v1.json" in json.dumps(wording.get("detail") or ""),
        returncode=rc,
        wording=wording,
        stderrTail=err,
        note="Native06 scanned only admission[].rule; this field would have been missed.",
    )

    failed = [r for r in C.rows if not r["passed"]]
    out = {
        "standing": "Independent Grok delta probes of native07 wording correction; not product acceptance",
        "passed": not failed,
        "caseCount": len(C.rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": C.rows,
    }
    (RESULTS / "delta-probes.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        (RESULTS / "delta-probes.exc").write_text(traceback.format_exc())
        raise
