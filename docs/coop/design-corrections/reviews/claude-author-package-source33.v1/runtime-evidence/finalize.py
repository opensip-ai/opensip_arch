#!/usr/bin/env python3
"""Final integrity check: package10 on disk still matches its manifest and the verified bytes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
FINAL = HERE / "verification" / "final" / "verification.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    manifest = json.loads((V10 / "artifact-manifest.json").read_text())
    drift, missing = [], []
    listed = set()
    for row in manifest["files"]:
        listed.add(row["path"])
        p = V10 / row["path"]
        if not p.is_file():
            missing.append(row["path"])
            continue
        if sha(p) != row["sha256"] or p.stat().st_size != row["bytes"]:
            drift.append(row["path"])
    on_disk = {str(p.relative_to(V10)) for p in V10.rglob("*")
               if p.is_file() and not p.is_symlink()}
    unlisted = sorted(on_disk - listed)

    final = json.loads(FINAL.read_text())
    out = {
        "standing": "Final integrity check of the owned package10 and this runtime. Not acceptance.",
        "package10ArtifactManifestSha256": sha(V10 / "artifact-manifest.json"),
        "manifestMatchesVerifiedRun":
            sha(V10 / "artifact-manifest.json") == final["packageManifestSha256"],
        "manifestDrift": drift, "manifestMissing": missing,
        "filesOnDiskNotListed": unlisted,
        "onlyUnlistedIsTheManifestItself": unlisted == ["artifact-manifest.json"],
        "package9Untouched": sha(V9 / "artifact-manifest.json")
        == "55066ece33a25ccb1f5b2984227196863a168ea9814049a4285f275ad905b028",
        "finalVerificationPassed": final["passed"],
        "runtimeDeliverables": [
            {"file": n, "exists": (HERE / n).is_file(),
             "sha256": sha(HERE / n) if (HERE / n).is_file() else None}
            for n in ("author-review.md", "author-review.json", "handoff.md",
                      "reports/frozen33-verification.json", "reports/preservation.json",
                      "reports/honest-failure-demo.json", "reports/install-remint.json",
                      "reports/finalize-package10.json")
        ],
        "note": "author-review.md/json live in this runtime, not inside package10, so that no "
                "package artifact states the package manifest hash and no circular claim exists.",
    }
    (HERE / "reports" / "finalize.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "runtimeDeliverables"} |
                     {"missingDeliverables": [d["file"] for d in out["runtimeDeliverables"]
                                              if not d["exists"]]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
