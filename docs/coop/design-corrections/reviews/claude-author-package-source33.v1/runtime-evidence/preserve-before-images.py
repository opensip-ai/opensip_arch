#!/usr/bin/env python3
"""Preserve the v9 BEFORE-images of every artifact this remint will replace.

Written into package10/historical-source33-before-remint/, a NEW name that collides with none of
the existing historical-source25/26/27/28/30/31/32 or historical-consumer-custody directories.
The images are copied from the IMMUTABLE v9, never from the working copy.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
DEST = V10 / "historical-source33-before-remint"

# Everything this pass will edit or regenerate.
TARGETS = [
    "author-helpers/evaluator.py",
    "checkpoint3/claims.json",
    "checkpoint3/ts.store.json",
    "binding-controls/claims.json",
    "binding-controls/variants.json",
    "binding-controls/construction-provenance.json",
    "binding-controls/ts-lawful-default.store.json",
    "binding-controls/ts-invalid-default-entry.store.json",
    "binding-controls/ts-lawful-explicit-selection.store.json",
    "semantic-controls1/claims.json",
    "semantic-controls1/severity.store.json",
    "semantic-controls1/unrelated-scope.store.json",
    "semantic-controls1/collapsed-deficiencies.store.json",
    "artifact-manifest.json",
    "README.md",
    "query-assessment.json",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=False)
    rows = []
    for rel in TARGETS:
        src = V9 / rel
        if not src.is_file():
            rows.append({"path": rel, "presentInV9": False})
            continue
        flat = rel.replace("/", "__")
        shutil.copy2(src, DEST / flat)
        rows.append({"path": rel, "presentInV9": True, "image": flat,
                     "bytes": src.stat().st_size, "sha256": sha(src)})
    index = {
        "standing": "BEFORE-images of the package9 artifacts this source33 remint replaces. "
                    "These are the EXACT immutable v9 bytes, preserved so the old source30 "
                    "construction and the new source33 remint can be compared. package9 itself is "
                    "untouched and remains the authority for its own bytes.",
        "packageBeforeRemint": str(V9),
        "distinctFromExistingHistoricalDirectories": [
            "historical-source25-preparation", "historical-source26-preparation",
            "historical-source27-preparation", "historical-source28-preparation",
            "historical-source30-preparation", "historical-source31-preparation",
            "historical-source32-preparation", "historical-consumer-custody",
            "historical-intermediate-preparation",
        ],
        "note": "These images are HISTORICAL SOURCE30-era constructions. They are not reminted and "
                "must not be presented as source33 evidence.",
        "images": rows,
    }
    (DEST / "before-image-index.json").write_text(json.dumps(index, indent=2) + "\n")
    (HERE / "reports" / "before-images.json").write_text(json.dumps(index, indent=2) + "\n")
    print(json.dumps({"destination": str(DEST), "imageCount": sum(1 for r in rows if r.get("image")),
                      "missingInV9": [r["path"] for r in rows if not r["presentInV9"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
