#!/usr/bin/env python3
"""BEFORE/AFTER images, SHA-256 and a changed-file manifest for this author's owner files.

Usage: snapshot.py before|after
`before` copies each existing TARGET from the verified runtime copy (which must still equal frozen37).
`after` records every TARGET (existing or NEW), writes unified diffs against frozen37 into diffs/ and one
combined proposed-edits.diff, and compares the whole runtime copy against the frozen37 manifest so any
change outside TARGETS is reported, never hidden. Writes only under this runtime.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "source"
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v37")
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json")
MANIFEST_SHA = "245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680"
TARGETS = [
    "docs/coop/design-corrections/foundation/run-termination-contract.v1.md",
    "docs/coop/design-corrections/foundation/run_termination_model.v1.py",
    "docs/coop/design-corrections/foundation/run-termination-goldens.v1.json",
    "docs/coop/design-corrections/foundation/check-semantic-replay.v3.py",
    "docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py",
    "docs/v2/contracts/product-v1/native-evidence.md",
    "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
    "docs/coop/design-corrections/workflows/workflow-projection-contract.v3.md",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def manifest_rows() -> dict:
    raw = MANIFEST.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise SystemExit("manifest hash mismatch")
    return {f["path"]: f for f in json.loads(raw)["files"]}


def main(phase: str) -> int:
    rows_by_path = manifest_rows()
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    diff_text = []
    for rel in TARGETS:
        flat = rel.replace("/", "__")
        p, f = SRC / rel, FROZEN / rel
        row = {"path": rel, "inFrozen37": f.is_file(), "manifestSha256": (rows_by_path.get(rel) or {}).get("sha256")}
        if f.is_file():
            row["frozen37Sha256"] = sha(f)
            row["frozen37Bytes"] = f.stat().st_size
        if p.is_file():
            shutil.copy2(p, out / flat)
            row.update({"sha256": sha(p), "bytes": p.stat().st_size, "image": str(out / flat)})
        row["equalsFrozen37"] = f.is_file() and p.is_file() and sha(p) == sha(f)
        if phase == "before" and f.is_file() and not row["equalsFrozen37"]:
            raise SystemExit(f"before-image of {rel} does not equal frozen37; refusing")
        if phase == "after" and p.is_file() and not row["equalsFrozen37"]:
            before = f.read_text().splitlines(keepends=True) if f.is_file() else []
            after = p.read_text().splitlines(keepends=True)
            lines = list(difflib.unified_diff(before, after, f"a/{rel}" if f.is_file() else "/dev/null", f"b/{rel}", n=3))
            diff_path = HERE / "diffs" / (flat + ".diff")
            diff_path.parent.mkdir(parents=True, exist_ok=True)
            diff_path.write_text("".join(lines))
            diff_text.extend(lines)
            row.update({"added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                        "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                        "diff": str(diff_path), "diffSha256": sha(diff_path)})
        rows.append(row)
    doc = {"phase": phase, "manifestSha256": MANIFEST_SHA, "files": rows}
    if phase == "after":
        combined = HERE / "proposed-edits.diff"
        combined.write_text("".join(diff_text))
        doc["proposedEditsDiff"] = {"path": str(combined), "sha256": sha(combined)}
        changed, missing, extra = [], [], []
        for rel, f in rows_by_path.items():
            p = SRC / rel
            if not p.is_file():
                missing.append(rel)
            elif sha(p) != f["sha256"]:
                changed.append(rel)
        listed = set(rows_by_path)
        for q in SRC.rglob("*"):
            if q.is_file() and "__pycache__" not in q.parts:
                rel = str(q.relative_to(SRC))
                if rel not in listed:
                    extra.append(rel)
        doc["tree"] = {"changedVsManifest": sorted(changed), "missingVsManifest": sorted(missing), "newFiles": sorted(extra),
                       "outsideTargets": sorted(set(changed + missing + extra) - set(TARGETS))}
    (HERE / f"{phase}-manifest.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
