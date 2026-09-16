#!/usr/bin/env python3
"""BEFORE/AFTER images, SHA-256 and a changed-file manifest for the owner files this correction may touch.

Usage: snapshot.py before|after. `after` also diffs the whole assembly against frozen36 so any file
changed outside TARGETS is reported, never hidden.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source")
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v36")
TARGETS = [
    "docs/coop/design-corrections/workflows/query-projection-contract.v3.md",
    "docs/coop/design-corrections/workflows/query_projection_model.v3.py",
    "docs/coop/design-corrections/workflows/check-query-projection.v3.py",
    "docs/v2/contracts/product-v1/native-evidence.md",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/native/native_evidence_model.v2.py",
    "docs/coop/design-corrections/native/native-cases.v2.json",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(phase):
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for rel in TARGETS:
        p = SRC / rel
        flat = rel.replace("/", "__")
        shutil.copy2(p, out / flat)
        row = {"path": rel, "bytes": p.stat().st_size, "sha256": sha(p), "frozen36Sha256": sha(FROZEN / rel),
               "equalsFrozen36": sha(p) == sha(FROZEN / rel), "image": str(out / flat)}
        if phase == "after":
            before = (FROZEN / rel).read_text().splitlines(keepends=True)
            after = p.read_text().splitlines(keepends=True)
            lines = list(difflib.unified_diff(before, after, f"frozen36/{rel}", f"assembly/{rel}", n=3))
            diff_path = HERE / "diffs" / (flat + ".diff")
            diff_path.parent.mkdir(parents=True, exist_ok=True)
            diff_path.write_text("".join(lines))
            row.update({"added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                        "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                        "diff": str(diff_path), "diffSha256": sha(diff_path)})
        rows.append(row)
    doc = {"phase": phase, "files": rows}
    if phase == "after":
        def tree(root):
            return {str(q.relative_to(root)): sha(q) for q in root.rglob("*") if q.is_file()}
        a, b = tree(SRC), tree(FROZEN)
        doc["assembly"] = {"files": len(a), "frozen36Files": len(b),
                           "onlyInAssembly": sorted(set(a) - set(b)), "onlyInFrozen36": sorted(set(b) - set(a)),
                           "changedVsFrozen36": sorted(k for k in set(a) & set(b) if a[k] != b[k])}
        doc["assembly"]["changedOutsideTargets"] = sorted(set(doc["assembly"]["changedVsFrozen36"]) - set(TARGETS))
    (HERE / f"{phase}-manifest.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
