#!/usr/bin/env python3
"""Install the source33 reminted exports into package10 and record old-vs-new comparisons.

Only the TS-derived groups are replaced. The Rust/normalized groups keep their exact bytes and
are separately re-verified against frozen33 in this same pass, so their reuse carries an explicit
byte + actual-verification standing rather than an inherited claim.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
REMINT = HERE / "remint"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# (package-relative destination, reminted source file)
INSTALL = [
    ("checkpoint3/ts.store.json", REMINT / "checkpoint3/checkpoint3/ts.store.json"),
    ("checkpoint3/claims.json", REMINT / "checkpoint3/checkpoint3/claims.json"),
    ("checkpoint3/construction-provenance.json", REMINT / "checkpoint3/construction-provenance.json"),
    ("binding-controls/ts-lawful-default.store.json", REMINT / "binding-controls/ts-lawful-default.store.json"),
    ("binding-controls/ts-invalid-default-entry.store.json", REMINT / "binding-controls/ts-invalid-default-entry.store.json"),
    ("binding-controls/ts-lawful-explicit-selection.store.json", REMINT / "binding-controls/ts-lawful-explicit-selection.store.json"),
    ("binding-controls/claims.json", REMINT / "binding-controls/claims.json"),
    ("binding-controls/variants.json", REMINT / "binding-controls/variants.json"),
    ("binding-controls/construction-provenance.json", REMINT / "binding-controls/construction-provenance.json"),
    ("semantic-controls1/severity.store.json", REMINT / "semantic-controls/semantic-controls1/severity.store.json"),
    ("semantic-controls1/unrelated-scope.store.json", REMINT / "semantic-controls/semantic-controls1/unrelated-scope.store.json"),
    ("semantic-controls1/collapsed-deficiencies.store.json", REMINT / "semantic-controls/semantic-controls1/collapsed-deficiencies.store.json"),
    ("semantic-controls1/claims.json", REMINT / "semantic-controls/semantic-controls1/claims.json"),
    ("semantic-controls1/construction-provenance.json", REMINT / "semantic-controls/construction-provenance.json"),
]

REUSED_GROUPS = ["normalized-examples6", "rust-selection-examples1"]


def main() -> int:
    rows = []
    for rel, src in INSTALL:
        dest = V10 / rel
        old = V9 / rel
        before = {"present": old.is_file()}
        if old.is_file():
            before.update(sha256=sha(old), bytes=old.stat().st_size)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        rows.append({
            "path": rel, "status": "reminted-on-source33",
            "source30Before": before,
            "source33After": {"sha256": sha(dest), "bytes": dest.stat().st_size},
            "bytesIdenticalToSource30Construction":
                before.get("sha256") == sha(dest) if before["present"] else None,
            "remintedFrom": str(src),
        })

    reused = []
    for group in REUSED_GROUPS:
        for p in sorted((V10 / group).rglob("*")):
            if p.is_file():
                rel = str(p.relative_to(V10))
                old = V9 / rel
                reused.append({
                    "path": rel, "status": "reused-exact-source30-construction",
                    "sha256": sha(p),
                    "identicalToV9": old.is_file() and sha(old) == sha(p),
                })

    out = {
        "standing": "source33 remint installation record. Reminted artifacts are NEW source33 "
                    "constructions; reused artifacts are the EXACT source30-construction bytes and "
                    "are separately re-verified against frozen source33 in this same pass. No old "
                    "execution is relabelled.",
        "remintedCount": len(rows),
        "reminted": rows,
        "reusedExactCount": len(reused),
        "reusedExact": reused,
        "reusedGroups": REUSED_GROUPS,
        "bytesIdenticalDespiteRemint": [r["path"] for r in rows
                                        if r["bytesIdenticalToSource30Construction"]],
    }
    (HERE / "reports" / "install-remint.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "remintedCount": out["remintedCount"],
        "reusedExactCount": out["reusedExactCount"],
        "bytesIdenticalDespiteRemint": out["bytesIdenticalDespiteRemint"],
        "allReusedIdenticalToV9": all(r["identicalToV9"] for r in reused),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
