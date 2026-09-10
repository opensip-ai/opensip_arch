#!/usr/bin/env python3
"""p12b: faster reachability measurement of the record() merge branch.

Same question as p12 (v10-A3), but instead of sys.settrace over the whole suite it injects a
counter into a DISPOSABLE COPY of identity-model.py. The frozen source is never edited. The
injection is a pure side-effecting counter on the branch of interest; it adds no control flow, so
the suite's own pass/fail result must be unchanged -- which is asserted here as the guard that the
instrumentation is lawful.
"""
import json
import os
import shutil
import subprocess

PY = "/tmp/opensip-architecture-review-env/bin/python"
V11 = "/tmp/opensip-design-corrections/candidate-subject.v11"
V10 = "/tmp/opensip-design-corrections/candidate-subject.v10"
WORK = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/reach"
DC = "docs/coop/design-corrections"

MARKERS = {
    "v11": [("            missing=previous['missing'] or missing",
             "mergeBranch"),
            ("        missing=not annotations",
             "recordCall")],
    "v10": [("            annotations=previous['annotations']+[a for a in annotations if a not in previous['annotations']]",
             "mergeBranch"),
            ("    def record(path,form,field,joinable,annotations):",
             None)],
}


def instrument(tag, root, version):
    dst = os.path.join(WORK, tag)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(root, dst)
    mp = os.path.join(dst, DC, "foundation/identity-model.py")
    lines = open(mp).read().split("\n")
    counter_path = os.path.join(dst, "reach-counts.json")
    hits = {}
    out = []
    # a module-level counter dict, flushed by the checker's own exit
    for line in lines:
        stripped = line.rstrip()
        placed = False
        for text, name in MARKERS[version]:
            if name and stripped == text.rstrip():
                indent = line[:len(line) - len(line.lstrip())]
                out.append(indent + f"_REACH['{name}']=_REACH.get('{name}',0)+1")
                hits[name] = True
                placed = True
        out.append(line)
        if placed:
            pass
    src = "\n".join(out)
    src = ("import atexit as _atexit, json as _json\n"
           "_REACH={}\n"
           f"_atexit.register(lambda: open({counter_path!r},'w').write(_json.dumps(_REACH)))\n"
           + src)
    open(mp, "w").write(src)
    return dst, counter_path, sorted(hits)


results = {}
for tag, root, version in (("v11", V11, "v11"), ("v10", V10, "v10")):
    dst, counter_path, placed = instrument(tag, root, version)
    proc = subprocess.run(
        [PY, "-I", "-B", os.path.join(dst, DC, "foundation/check-identity.py")],
        cwd=dst, capture_output=True, text=True)
    counts = json.load(open(counter_path)) if os.path.isfile(counter_path) else {}
    results[tag] = {
        "markersPlaced": placed,
        "suiteStdout": proc.stdout.strip()[:200],
        "suiteExit": proc.returncode,
        "counts": counts,
    }

results["verdict"] = {
    "v10MergeBranchExecutions": results["v10"]["counts"].get("mergeBranch", 0),
    "v11MergeBranchExecutions": results["v11"]["counts"].get("mergeBranch", 0),
    "v11RecordCalls": results["v11"]["counts"].get("recordCall", 0),
    "v10AdvisoryA3Reproduced": results["v10"]["counts"].get("mergeBranch", 0) == 0,
    "v11MergeBranchNowReached": results["v11"]["counts"].get("mergeBranch", 0) > 0,
    "instrumentationLawful": (results["v10"]["suiteExit"] == 0
                              and results["v11"]["suiteExit"] == 0),
}
print(json.dumps(results, indent=2))
