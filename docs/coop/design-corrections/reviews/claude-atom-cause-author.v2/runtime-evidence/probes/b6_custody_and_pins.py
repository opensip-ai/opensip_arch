"""Custody of the isolated source copy, and which pin entries go stale. Ledgers are never edited."""
import hashlib
import json
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
V1_AFTER = Path("/tmp/opensip-design-corrections/claude-atom-cause-author.v1/after-hashes.json")

TARGETS = [
    "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md",
    "docs/coop/design-corrections/foundation/atom_model.v1.py",
    "docs/coop/design-corrections/foundation/check-atoms.v1.py",
]
LEDGERS = [
    "docs/coop/design-corrections/native/source-pins.v2.json",
    "docs/coop/design-corrections/security/source-pins.v1.json",
    "docs/coop/design-corrections/workflows/source-pins.v1.json",
    "docs/coop/design-corrections/foundation/source-pins.v1.json",
    "docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json",
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def walk(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


a, b = walk(SRC), walk(FROZ)
v1 = {r["path"]: r["sha256"] for r in json.loads(V1_AFTER.read_text())}
now = {t: a[t] for t in TARGETS}
tails = {t.rsplit("/", 1)[-1] for t in TARGETS}

pins = []
for rel in LEDGERS:
    doc = json.loads((SRC / rel).read_text())

    def walk_doc(node, trail):
        if isinstance(node, dict):
            path = node.get("path") or node.get("file") or node.get("sourcePath")
            digest = node.get("sha256") or node.get("digest") or node.get("contentSha256")
            if path and digest and any(path.endswith(t) for t in tails):
                match = next((t for t in TARGETS if path.endswith(t.rsplit("/", 1)[-1])), None)
                pins.append({"ledger": rel, "trail": "/".join(trail), "pinnedPath": path,
                             "pinnedSha256": digest, "successorSha256": now.get(match),
                             "stale": digest != now.get(match)})
                return
            for k, v in node.items():
                walk_doc(v, trail + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk_doc(v, trail + [str(i)])

    walk_doc(doc, [])

print(json.dumps({
    "custody": {
        "successorFiles": len(a), "frozen33Files": len(b),
        "onlyInSuccessor": sorted(set(a) - set(b)),
        "onlyInFrozen33": sorted(set(b) - set(a)),
        "changedVsFrozen33": sorted(f for f in (set(a) & set(b)) if a[f] != b[f]),
        "changedVsV1Final": sorted(t for t in TARGETS if a[t] != v1[t]),
        "unchangedVsV1Final": sorted(t for t in TARGETS if a[t] == v1[t]),
    },
    "currentSha256": now,
    "pinEntries": pins,
    "staleCount": sum(1 for p in pins if p["stale"]),
    "newCheckerFilesAdded": [],
    "referenceRunnerWiring": "check-atoms.v1.py is already job 'atoms' in "
                             "foundation/run-evaluator3-checks.py; no checker file was added, so "
                             "no pin ADDITION is owed - only the three existing pin digests change.",
}, indent=2))
