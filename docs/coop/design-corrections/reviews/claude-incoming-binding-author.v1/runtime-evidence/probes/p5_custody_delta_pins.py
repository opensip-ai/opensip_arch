"""P5 — custody, full three-file delta, frozen34 drift and stale pin rows. Read-only on every tree.

Writes only under this runtime: the unified diffs go to receipts/p5-diffs/.
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SUCC = Path("/tmp/opensip-design-corrections/incoming-binding-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v34")
MAN = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v34.json")
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


def tree(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


raw = MAN.read_bytes()
manifest = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
succ, froz = tree(SUCC), tree(FROZ)

diff_dir = HERE / "probes" / "receipts" / "p5-diffs"
diff_dir.mkdir(parents=True, exist_ok=True)
delta = []
for rel in TARGETS:
    old = (HERE / "before" / rel.replace("/", "__")).read_text().splitlines(keepends=True)
    new = (SUCC / rel).read_text().splitlines(keepends=True)
    lines = list(difflib.unified_diff(old, new, f"frozen34/{rel}", f"successor/{rel}", n=3))
    (diff_dir / (rel.replace("/", "__") + ".diff")).write_text("".join(lines))
    delta.append({"path": rel, "beforeSha256": froz[rel], "afterSha256": succ[rel],
                  "added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                  "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                  "diff": str(diff_dir / (rel.replace("/", "__") + ".diff"))})

pins = []
for rel in LEDGERS:
    doc = json.loads((SUCC / rel).read_text())

    def walk(node, trail):
        if isinstance(node, dict):
            path = node.get("path") or node.get("file")
            digest = node.get("sha256") or node.get("digest")
            if path in TARGETS and digest:
                pins.append({"ledger": rel, "trail": "/".join(trail), "path": path, "pinnedSha256": digest,
                             "successorSha256": succ[path], "stale": digest != succ[path]})
                return
            for k, v in node.items():
                walk(v, trail + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, trail + [str(i)])

    walk(doc, [])

print(json.dumps({
    "manifestSha256": hashlib.sha256(raw).hexdigest(),
    "frozen34": {"files": len(froz), "manifestRows": len(manifest),
                 "driftVsManifest": sorted(p for p, h in manifest.items() if froz.get(p) != h),
                 "extraVsManifest": sorted(set(froz) - set(manifest))},
    "successor": {"files": len(succ),
                  "onlyInSuccessor": sorted(set(succ) - set(froz)),
                  "onlyInFrozen34": sorted(set(froz) - set(succ)),
                  "changedVsFrozen34": sorted(p for p in set(succ) & set(froz) if succ[p] != froz[p])},
    "delta": delta,
    "pinRows": pins,
    "stalePinRows": sum(1 for p in pins if p["stale"]),
    "newFilesAdded": [],
    "pinAdditionOwed": False,
}, indent=1))
