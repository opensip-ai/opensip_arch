#!/usr/bin/env python3
"""p06: are the NEW v11 annotation checks actually discriminating?

Counts and source greps prove nothing. This runs the SAME v11 checker against the PRE-FIX v10
identity-model.py, in a disposable foundation directory. A check that is discriminating must
FAIL there and PASS against the v11 model. A check that passes in both arms is not evidence
that the defect was closed.

Arms:
  A  v11 checker + v11 model  (expect: all pass)
  B  v11 checker + v10 model  (expect: exactly the new annotation checks fail)
  C  v10 checker + v10 model  (expect: all pass -- v10's own suite could not see the defect)
"""
import json
import os
import shutil
import subprocess

PY = "/tmp/opensip-architecture-review-env/bin/python"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
WORK = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/discriminate"
DC = "docs/coop/design-corrections"


def build(tag, checker_root, model_root):
    """Full disposable subject tree; only the two files under test are chosen per arm."""
    dst = os.path.join(WORK, tag)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(V11, dst)
    shutil.copyfile(os.path.join(checker_root, DC, "foundation/check-identity.py"),
                    os.path.join(dst, DC, "foundation/check-identity.py"))
    shutil.copyfile(os.path.join(model_root, DC, "foundation/identity-model.py"),
                    os.path.join(dst, DC, "foundation/identity-model.py"))
    return dst


def run(dst):
    rep = os.path.join(dst, "out.json")
    proc = subprocess.run(
        [PY, "-I", "-B", os.path.join(dst, DC, "foundation/check-identity.py"),
         "--report", rep],
        cwd=dst, capture_output=True, text=True)
    checks = {}
    if os.path.isfile(rep):
        checks = {c["id"]: c["passed"] for c in json.load(open(rep))["checks"]}
    return proc.returncode, proc.stdout[-400:], proc.stderr[-800:], checks


os.makedirs(WORK, exist_ok=True)
arms = {}
for tag, ck, md in (("A_v11check_v11model", V11, V11),
                    ("B_v11check_v10model", V11, V10),
                    ("C_v10check_v10model", V10, V10)):
    rc, out, err, checks = run(build(tag, ck, md))
    arms[tag] = {
        "exit": rc,
        "stdout": out.strip(),
        "stderrTail": err.strip()[-400:],
        "total": len(checks),
        "failed": sorted(k for k, v in checks.items() if not v),
        "_checks": checks,
    }

A, B, C = arms["A_v11check_v11model"], arms["B_v11check_v10model"], arms["C_v10check_v10model"]
new_ids = sorted(set(A["_checks"]) - set(C["_checks"]))
discriminating = sorted(i for i in new_ids if A["_checks"].get(i) and not B["_checks"].get(i, False))
non_discriminating = sorted(i for i in new_ids if A["_checks"].get(i) and B["_checks"].get(i, False))

out = {
    "armA_v11_v11": {k: v for k, v in A.items() if k != "_checks"},
    "armB_v11_v10": {k: v for k, v in B.items() if k != "_checks"},
    "armC_v10_v10": {k: v for k, v in C.items() if k != "_checks"},
    "newCheckIdsAddedInV11": new_ids,
    "newCheckCount": len(new_ids),
    "discriminatingNewChecks": discriminating,
    "nonDiscriminatingNewChecks": non_discriminating,
    "preexistingChecksFailingUnderPreFixModel": sorted(
        i for i in B["failed"] if i not in new_ids),
}
for tag in arms:
    arms[tag].pop("_checks")
print(json.dumps(out, indent=2))
