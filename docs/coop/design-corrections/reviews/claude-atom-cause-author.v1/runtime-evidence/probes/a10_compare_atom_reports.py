"""Compare the frozen33 and successor check-atoms reports, and re-verify custody of both trees."""
import hashlib
import json
from pathlib import Path

R = Path("/private/tmp/opensip-design-corrections/claude-atom-cause-author.v1/probes/receipts")
SUCC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v33")

old = json.loads((R / "frozen33-check-atoms.v1" / "stdout.txt").read_text())
new = json.loads((R / "check-atoms-after-controls" / "stdout.txt").read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def walk(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


a, b = walk(SUCC), walk(FROZ)
changed = sorted(f for f in (set(a) & set(b)) if a[f] != b[f])

print(json.dumps({
    "frozen33Report": {"ok": old["ok"], "passed": old["passed"], "failed": old["failed"],
                       "cases": len(old["results"])},
    "successorReport": {"ok": new["ok"], "passed": new["passed"], "failed": new["failed"],
                        "cases": len(new["results"])},
    "sharedCasesIdentical": old["results"] == new["results"][:len(old["results"])],
    "addedCases": [r["case"] for r in new["results"][len(old["results"]):]],
    "custody": {
        "successorFiles": len(a), "frozen33Files": len(b),
        "onlyInSuccessor": sorted(set(a) - set(b)),
        "onlyInFrozen33": sorted(set(b) - set(a)),
        "changedVsFrozen33": changed,
    },
}, indent=2))
