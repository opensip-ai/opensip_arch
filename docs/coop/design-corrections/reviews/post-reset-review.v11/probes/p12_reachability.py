#!/usr/bin/env python3
"""p12: line-level reachability of the record() merge branch, closing v10-A3 on its own terms.

v10-A3 measured that the merge branch in relation_digest_annotation_coverage.record was executed
ZERO times across the whole 661-check v10 suite, so the enforcement code the suite claimed to
cover was never actually reached. This re-measures with sys.settrace over the FULL suite, for the
v10 suite/model and the v11 suite/model, without editing any frozen source.

Counted lines are located by source text, not by fixed line number, so the two versions are
compared on the same semantic statements.
"""
import json
import os
import runpy
import subprocess
import sys

DRIVER = r'''
import json,sys,runpy
target=sys.argv[1]; model=sys.argv[2]; out=sys.argv[3]
# locate the statements of interest by TEXT in identity-model.py
src=open(model).read().splitlines()
want={}
for i,line in enumerate(src,1):
    s=line.strip()
    if s.startswith("previous=seen.get(path)"):want[i]="record.lookupPrevious"
    if s.startswith("missing=previous['missing'] or missing"):want[i]="record.mergeBranch.missingMonotonic"
    if s.startswith("annotations=previous['annotations']+[a for a in annotations"):want[i]="record.mergeBranch.v10merge"
    if s.startswith("if not previous['annotations'] or not annotations:annotations=[]"):want[i]="record.mergeBranch.v10poisonTest"
    if s.startswith("merged=list(previous['annotations'])"):want[i]="record.mergeBranch.v11merge"
    if s.startswith("missing=not annotations"):want[i]="record.missingFromIncoming"
    if s.startswith("if uncovered:raise"):want[i]="law.uncoveredRaise"
    if s.startswith("raise C.AdmissionError('RELATION_DIGEST_ANNOTATION_CONFLICT"):want[i]="law.conflictRaise"
    if s.startswith("if sighting.get('missing'):continue"):want[i]="law.skipMissingSighting"
counts={v:0 for v in want.values()}
mabs=__import__("os").path.abspath(model)
def tracer(frame,event,arg):
    if event=="call":
        return tracer if __import__("os").path.abspath(frame.f_code.co_filename)==mabs else None
    if event=="line":
        n=want.get(frame.f_lineno)
        if n:counts[n]+=1
    return tracer
sys.argv=[target]
sys.settrace(tracer)
try:
    runpy.run_path(target,run_name="__main__")
except SystemExit:
    pass
finally:
    sys.settrace(None)
open(out,"w").write(json.dumps(counts,indent=2))
'''

PY = "/tmp/opensip-architecture-review-env/bin/python"
WORK = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/discriminate"
DC = "docs/coop/design-corrections"
here = os.path.dirname(os.path.abspath(__file__))
drv = os.path.join(here, "_p12_driver.py")
open(drv, "w").write(DRIVER)

out = {}
for tag in ("A_v11check_v11model", "C_v10check_v10model", "B_v11check_v10model"):
    root = os.path.join(WORK, tag)
    target = os.path.join(root, DC, "foundation/check-identity.py")
    model = os.path.join(root, DC, "foundation/identity-model.py")
    res = os.path.join(root, "reach.json")
    proc = subprocess.run([PY, "-I", "-B", drv, target, model, res],
                          cwd=root, capture_output=True, text=True)
    out[tag] = {
        "counts": json.load(open(res)) if os.path.isfile(res) else None,
        "stderrTail": proc.stderr[-300:],
    }

a = out["A_v11check_v11model"]["counts"] or {}
c = out["C_v10check_v10model"]["counts"] or {}
out["verdict"] = {
    "v10MergeBranchExecutions": c.get("record.mergeBranch.v10merge"),
    "v10PoisonTestExecutions": c.get("record.mergeBranch.v10poisonTest"),
    "v11MergeBranchExecutions": a.get("record.mergeBranch.v11merge"),
    "v11MissingMonotonicExecutions": a.get("record.mergeBranch.missingMonotonic"),
    "v11ConflictRaiseExecutions": a.get("law.conflictRaise"),
    "v11SkipMissingSightingExecutions": a.get("law.skipMissingSighting"),
    "v10AdvisoryA3Reproduced": c.get("record.mergeBranch.v10merge") == 0,
    "v11MergeBranchNowReached": (a.get("record.mergeBranch.v11merge") or 0) > 0,
}
print(json.dumps(out, indent=2))
