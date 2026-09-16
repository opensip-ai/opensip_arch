"""Q6 — custody, full three-file delta against frozen35, frozen35 drift and stale pin rows. Read-only on every tree.

Also separates authorship: the BEFORE images are frozen35 bytes, which already contain root's later
contract/check changes on top of the incoming-binding author v1 after-images; that split is reported.
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SUCC = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v35")
MAN = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json")
V1_AFTER = Path("/tmp/opensip-design-corrections/claude-incoming-binding-author.v1/after")
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
WATCH = ["/tmp/opensip-design-corrections/root-dependency-scope35-investigation.v1",
         "/tmp/opensip-design-corrections/root-source36-preparation.v1",
         "/tmp/opensip-design-corrections/claude-incoming-binding-author.v1"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tree(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


raw = MAN.read_bytes()
manifest = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
succ, froz = tree(SUCC), tree(FROZ)
diff_dir = HERE / "probes" / "receipts" / "q6-diffs"
diff_dir.mkdir(parents=True, exist_ok=True)


def udiff(old_text, new_text, a, b):
    return list(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True), a, b, n=3))


delta, root_layer = [], []
for rel in TARGETS:
    flat = rel.replace("/", "__")
    lines = udiff((FROZ / rel).read_text(), (SUCC / rel).read_text(), f"frozen35/{rel}", f"successor/{rel}")
    (diff_dir / (flat + ".author.diff")).write_text("".join(lines))
    delta.append({"path": rel, "frozen35Sha256": froz[rel], "successorSha256": succ[rel],
                  "added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                  "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                  "diff": str(diff_dir / (flat + ".author.diff"))})
    v1 = V1_AFTER / flat
    rl = udiff(v1.read_text(), (FROZ / rel).read_text(), f"incoming-binding-author-v1-after/{rel}", f"frozen35/{rel}")
    (diff_dir / (flat + ".root-after-v1.diff")).write_text("".join(rl))
    root_layer.append({"path": rel, "v1AfterSha256": sha(v1), "frozen35Sha256": froz[rel],
                       "rootChangedAfterV1": sha(v1) != froz[rel],
                       "added": sum(1 for x in rl if x.startswith("+") and not x.startswith("+++")),
                       "removed": sum(1 for x in rl if x.startswith("-") and not x.startswith("---"))})

pins = []
for rel in LEDGERS:
    doc = json.loads((SUCC / rel).read_text())

    def walk(node, trail):
        if isinstance(node, dict):
            path, digest = node.get("path") or node.get("file"), node.get("sha256") or node.get("digest")
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

started = (HERE / "before-hashes.json").stat().st_mtime
watch = {w: sorted(str(p.relative_to(w)) for p in Path(w).rglob("*") if p.is_file() and p.stat().st_mtime > started)
         for w in WATCH}
print(json.dumps({
    "manifestSha256": hashlib.sha256(raw).hexdigest(),
    "frozen35": {"files": len(froz), "driftVsManifest": sorted(p for p, h in manifest.items() if froz.get(p) != h),
                 "extraVsManifest": sorted(set(froz) - set(manifest))},
    "successor": {"files": len(succ), "onlyInSuccessor": sorted(set(succ) - set(froz)),
                  "onlyInFrozen35": sorted(set(froz) - set(succ)),
                  "changedVsFrozen35": sorted(p for p in set(succ) & set(froz) if succ[p] != froz[p])},
    "authorDelta": delta, "rootLayerAfterIncomingBindingV1": root_layer,
    "pinRows": pins, "stalePinRows": sum(1 for p in pins if p["stale"]),
    "filesModifiedAfterThisRuntimeBegan": watch,
}, indent=1))
