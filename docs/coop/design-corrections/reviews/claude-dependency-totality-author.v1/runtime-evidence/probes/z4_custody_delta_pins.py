"""Z4 — custody, exact author delta, frozen35 delta, stale pins and watched-runtime changes. Read-only on every tree.

authorDelta   : dependency-scope-successor (previous completed author bytes, = this tree's BEFORE) -> successor
frozen35Delta : frozen35 -> successor (the cumulative unfrozen source36 candidate for these three files)
A file ROOT adds to a watched preparation runtime while this runs is reported, not treated as a custody violation.
"""
import difflib
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SUCC = Path("/tmp/opensip-design-corrections/dependency-totality-successor.v1/source")
PREV = Path("/tmp/opensip-design-corrections/dependency-scope-successor.v1/source")
FROZ = Path("/tmp/opensip-design-corrections/candidate-subject.v35")
MAN = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json")
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
WATCH = ["/tmp/opensip-design-corrections/dependency-scope-successor.v1/source",
         "/tmp/opensip-design-corrections/claude-dependency-scope-author.v1",
         "/tmp/opensip-design-corrections/root-dependency-totality35-investigation.v1",
         "/tmp/opensip-design-corrections/root-source36-preparation.v1"]
PLACEHOLDERS = ("[DECISION]", "TODO", "TBD", "XXX")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tree(root):
    return {str(p.relative_to(root)): sha(p) for p in root.rglob("*") if p.is_file()}


def delta(old_root, new_root, tag, out_dir):
    rows = []
    for rel in TARGETS:
        a, b = (old_root / rel).read_text(), (new_root / rel).read_text()
        lines = list(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True),
                                          f"{tag}/{rel}", f"successor/{rel}", n=3))
        path = out_dir / (rel.replace("/", "__") + f".{tag}.diff")
        path.write_text("".join(lines))
        rows.append({"path": rel, "beforeSha256": sha(old_root / rel), "afterSha256": sha(new_root / rel),
                     "added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                     "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                     "diff": str(path), "diffSha256": sha(path)})
    return rows


out_dir = HERE / "probes" / "receipts" / "z4-diffs"
out_dir.mkdir(parents=True, exist_ok=True)
raw = MAN.read_bytes()
manifest = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
succ, froz = tree(SUCC), tree(FROZ)

pins = []
for rel in LEDGERS:
    doc = json.loads((SUCC / rel).read_text())

    def walk(node, trail):
        if isinstance(node, dict):
            path, digest = node.get("path") or node.get("file"), node.get("sha256") or node.get("digest")
            if path in TARGETS and digest:
                pins.append({"ledger": rel, "trail": "/".join(trail), "path": path, "pinnedSha256": digest,
                             "pinnedEqualsFrozen35": digest == froz[path], "successorSha256": succ[path],
                             "stale": digest != succ[path]})
                return
            for k, v in node.items():
                walk(v, trail + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, trail + [str(i)])

    walk(doc, [])

started = (HERE / "before-hashes.json").stat().st_mtime
print(json.dumps({
    "manifestSha256": hashlib.sha256(raw).hexdigest(),
    "frozen35": {"files": len(froz), "driftVsManifest": sorted(p for p, h in manifest.items() if froz.get(p) != h)},
    "successor": {"files": len(succ), "onlyInSuccessor": sorted(set(succ) - set(froz)),
                  "onlyInFrozen35": sorted(set(froz) - set(succ)),
                  "changedVsFrozen35": sorted(p for p in set(succ) & set(froz) if succ[p] != froz[p])},
    "authorDelta": delta(PREV, SUCC, "dependency-scope-successor", out_dir),
    "frozen35Delta": delta(FROZ, SUCC, "frozen35", out_dir),
    "placeholders": {rel: [p for p in PLACEHOLDERS if p in (SUCC / rel).read_text()] for rel in TARGETS},
    "pinRows": pins, "stalePinRows": sum(1 for p in pins if p["stale"]),
    "watchedFilesModifiedAfterThisRuntimeBegan": {
        w: sorted(str(p.relative_to(w)) for p in Path(w).rglob("*") if p.is_file() and p.stat().st_mtime > started)
        for w in WATCH},
}, indent=1))
