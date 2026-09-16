"""Custody: verify the isolated successor copy against frozen33, and list what I may edit."""
import hashlib
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
FROZEN = B / "candidate-subject.v33"
WORK = B / "atom-cause-successor.v1/source"
MAN = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
           "candidate-subject.v33.json")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def index(root):
    return {str(p.relative_to(root)): (p.stat().st_size, sha(p))
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


out = {"standing": "READ-ONLY custody check before any edit."}
out["workExists"] = WORK.is_dir()
out["siblings"] = sorted(p.name for p in (B / "atom-cause-successor.v1").iterdir()) \
    if (B / "atom-cause-successor.v1").is_dir() else None

if WORK.is_dir():
    a, b = index(FROZEN), index(WORK)
    changed = sorted(k for k in a.keys() & b.keys() if a[k][1] != b[k][1])
    out["frozenFiles"] = len(a)
    out["workFiles"] = len(b)
    out["changedVsFrozen33"] = changed
    out["addedVsFrozen33"] = sorted(b.keys() - a.keys())[:20]
    out["removedVsFrozen33"] = sorted(a.keys() - b.keys())[:20]
    out["isExactCopyOfFrozen33"] = (a == b)

man = json.loads(MAN.read_bytes())
out["manifestSha256"] = sha(MAN)
out["manifestDeclaredFiles"] = man.get("fileCount")

TARGETS = [
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md",
    "docs/coop/design-corrections/foundation/atom_model.v1.py",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py",
    "docs/coop/design-corrections/native/native_evidence_model.v2.py",
    "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md",
    "docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json",
]
out["candidateTargets"] = [
    {"path": t, "existsInWork": (WORK / t).is_file(),
     "frozenSha256": sha(FROZEN / t) if (FROZEN / t).is_file() else None,
     "workSha256": sha(WORK / t) if (WORK / t).is_file() else None,
     "bytes": (WORK / t).stat().st_size if (WORK / t).is_file() else None}
    for t in TARGETS
]
print(json.dumps(out, indent=2, default=str))
