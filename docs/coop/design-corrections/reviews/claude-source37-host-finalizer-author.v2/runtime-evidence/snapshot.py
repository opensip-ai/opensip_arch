#!/usr/bin/env python3
"""v2 BEFORE/AFTER images, SHA-256, v1-to-v2 and frozen37-to-final diffs, and a whole-tree manifest check.

Usage: snapshot.py before|after
`before` images every TARGET from this runtime's copy, which must still equal the v1 after-image (or be
absent when the target is new in v2). `after` writes diffs-v1-to-v2/, diffs-frozen37-to-final/, the combined
v1-to-v2.diff and frozen37-to-final.diff, and compares the whole copy against frozen37 manifest + v1 targets,
so any change outside TARGETS is reported. Writes only under this runtime.
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
V1 = Path("/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1")
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


def text_lines(p: Path) -> list[str]:
    return p.read_text().splitlines(keepends=True) if p.is_file() else []


def udiff(a: Path, b: Path, rel: str, a_label: str) -> list[str]:
    return list(difflib.unified_diff(text_lines(a), text_lines(b),
                                     f"{a_label}/{rel}" if a.is_file() else "/dev/null", f"b/{rel}", n=3))


def main(phase: str) -> int:
    raw = MANIFEST.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise SystemExit("manifest hash mismatch")
    manifest = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
    v1_after = {r["path"]: r["sha256"] for r in json.loads((V1 / "after-manifest.json").read_text())["files"]}
    out = HERE / phase
    out.mkdir(parents=True, exist_ok=True)
    rows, d12, d37 = [], [], []
    for rel in TARGETS:
        flat = rel.replace("/", "__")
        p, v1p, fp = SRC / rel, V1 / "source" / rel, FROZEN / rel
        row = {"path": rel, "frozen37Sha256": manifest.get(rel), "v1Sha256": v1_after.get(rel),
               "v1SourceSha256": sha(v1p) if v1p.is_file() else None}
        if p.is_file():
            shutil.copy2(p, out / flat)
            row.update({"sha256": sha(p), "bytes": p.stat().st_size, "image": str(out / flat)})
        row["equalsV1"] = row.get("sha256") == row["v1Sha256"]
        row["equalsFrozen37"] = row.get("sha256") == row["frozen37Sha256"]
        if phase == "before" and p.is_file() and not row["equalsV1"]:
            raise SystemExit(f"before-image of {rel} does not equal v1 after-image; refusing")
        if phase == "after" and p.is_file():
            for label, base, bucket, acc in (("v1", v1p, "diffs-v1-to-v2", d12), ("frozen37", fp, "diffs-frozen37-to-final", d37)):
                lines = udiff(base, p, rel, "a")
                if not lines:
                    continue
                dp = HERE / bucket / (flat + ".diff")
                dp.parent.mkdir(parents=True, exist_ok=True)
                dp.write_text("".join(lines))
                acc.extend(lines)
                row[label + "Delta"] = {"added": sum(1 for x in lines if x.startswith("+") and not x.startswith("+++")),
                                        "removed": sum(1 for x in lines if x.startswith("-") and not x.startswith("---")),
                                        "diff": str(dp), "diffSha256": sha(dp)}
        rows.append(row)
    doc = {"phase": phase, "manifestSha256": MANIFEST_SHA, "v1AfterManifestSha256": sha(V1 / "after-manifest.json"), "files": rows}
    if phase == "after":
        for name, acc in (("v1-to-v2.diff", d12), ("frozen37-to-final.diff", d37)):
            (HERE / name).write_text("".join(acc))
            doc[name] = {"path": str(HERE / name), "sha256": sha(HERE / name)}
        expected = dict(manifest)
        expected.update(v1_after)
        got = {str(q.relative_to(SRC)): sha(q) for q in SRC.rglob("*") if q.is_file() and "__pycache__" not in q.parts}
        doc["tree"] = {
            "differsFromFrozen37PlusV1": sorted(k for k in expected if got.get(k) != expected[k]),
            "extra": sorted(set(got) - set(expected)),
            "outsideTargets": sorted((set(k for k in expected if got.get(k) != expected[k]) | (set(got) - set(expected))) - set(TARGETS)),
        }
    (HERE / f"{phase}-manifest.json").write_text(json.dumps(doc, indent=2) + "\n")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
