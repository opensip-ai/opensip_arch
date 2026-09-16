"""Which pin-ledger entries go stale for the three changed paths? Reported, never edited."""
import hashlib
import json
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
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
now = {t: hashlib.sha256((S / t).read_bytes()).hexdigest() for t in TARGETS}
tails = {t.rsplit("/", 1)[-1] for t in TARGETS}

rows = []
for rel in LEDGERS:
    doc = json.loads((S / rel).read_text())

    def walk(node, trail):
        if isinstance(node, dict):
            text = json.dumps(node)
            if any(t in text for t in tails):
                path = node.get("path") or node.get("file") or node.get("sourcePath")
                digest = node.get("sha256") or node.get("digest") or node.get("contentSha256")
                if path and digest and any(path.endswith(t) for t in tails):
                    match = next((t for t in TARGETS if path.endswith(t.rsplit("/", 1)[-1])), None)
                    rows.append({
                        "ledger": rel, "trail": "/".join(trail), "pinnedPath": path,
                        "pinnedSha256": digest,
                        "successorSha256": now.get(match),
                        "stale": digest != now.get(match),
                    })
                    return
            for k, v in node.items():
                walk(v, trail + [str(k)])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, trail + [str(i)])

    walk(doc, [])

print(json.dumps({"currentSha256": now, "pinEntries": rows,
                  "staleCount": sum(1 for r in rows if r["stale"])}, indent=2))
