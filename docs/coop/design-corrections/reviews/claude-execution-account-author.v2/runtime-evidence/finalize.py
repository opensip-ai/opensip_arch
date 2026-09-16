#!/usr/bin/env python3
"""Final consistency check for the v2 runtime, including that the v1 runtime is untouched."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")
V1 = Path("/tmp/opensip-design-corrections/claude-execution-account-author.v1")


def main() -> int:
    after = json.loads((HERE / "after-hashes.json").read_text())
    drift = [
        {"path": r["path"], "recorded": r["sha256"],
         "now": hashlib.sha256((SRC / r["path"]).read_bytes()).hexdigest()}
        for r in after
        if hashlib.sha256((SRC / r["path"]).read_bytes()).hexdigest() != r["sha256"]
    ]

    # The v1 runtime's own recorded hashes must still describe its own files.
    v1_ok, v1_bad = True, []
    for phase in ("before", "after"):
        for row in json.loads((V1 / f"{phase}-hashes.json").read_text()):
            image = Path(row["image"])
            if not image.is_file() or hashlib.sha256(image.read_bytes()).hexdigest() != row["sha256"]:
                v1_ok = False
                v1_bad.append(f"{phase}:{row['path']}")

    deliverables = [
        "author-review.md", "author-review.json", "changed-file-handoff.json",
        "tree-delta.json", "focused-checks-report.json",
        "before-hashes.json", "after-hashes.json", "README.md",
    ]
    out = {
        "standing": "Final consistency check of the v2 source-author runtime. Not acceptance.",
        "afterHashDrift": drift,
        "v1RuntimeImagesIntact": v1_ok,
        "v1RuntimeImageMismatches": v1_bad,
        "deliverables": [
            {"file": f, "exists": (HERE / f).is_file(),
             "sha256": hashlib.sha256((HERE / f).read_bytes()).hexdigest()
             if (HERE / f).is_file() else None,
             "bytes": (HERE / f).stat().st_size if (HERE / f).is_file() else None}
            for f in deliverables
        ],
    }
    (HERE / "finalize-report.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "afterHashDrift": drift,
        "v1RuntimeImagesIntact": v1_ok,
        "v1RuntimeImageMismatches": v1_bad,
        "missingDeliverables": [d["file"] for d in out["deliverables"] if not d["exists"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
