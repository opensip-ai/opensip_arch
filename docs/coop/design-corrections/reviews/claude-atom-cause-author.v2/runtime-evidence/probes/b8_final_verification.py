"""Final verification: source custody, and that v1 / root-review / frozen33 were not written."""
import hashlib
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
V1 = Path("/tmp/opensip-design-corrections/claude-atom-cause-author.v1")
ROOTREV = Path("/tmp/opensip-design-corrections/root-atom-cause-draft-review.v1")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tree(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


a, b = tree(SRC), tree(FROZ)
v2_started = (Path(__file__).resolve().parent.parent / "before-hashes.json").stat().st_mtime
touched = {}
for label, root in (("v1", V1), ("rootReview", ROOTREV), ("frozen33", FROZ)):
    touched[label] = sorted(str(p.relative_to(root)) for p in root.rglob("*")
                            if p.is_file() and p.stat().st_mtime > v2_started)

print(json.dumps({
    "custody": {
        "successorFiles": len(a), "frozen33Files": len(b),
        "onlyInSuccessor": sorted(set(a) - set(b)),
        "onlyInFrozen33": sorted(set(b) - set(a)),
        "changedVsFrozen33": sorted(f for f in (set(a) & set(b)) if a[f] != b[f]),
    },
    "v2StartedAt": v2_started,
    "filesModifiedAfterV2Started": touched,
    "readOnlyTreesUntouched": all(not v for v in touched.values()),
}, indent=2))
