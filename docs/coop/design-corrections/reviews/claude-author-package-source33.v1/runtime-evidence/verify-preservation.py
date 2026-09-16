#!/usr/bin/env python3
"""Confirm every preserved artifact is byte-unchanged, and describe package10's delta vs v9."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
V9_MANIFEST_EXPECTED = "MF55066ece33a25ccb1f5b2984227196863a168ea9814049a4285f275ad905b028"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def index(root: Path) -> dict:
    return {str(p.relative_to(root)): sha(p)
            for p in sorted(root.rglob("*")) if p.is_file() and not p.is_symlink()}


def main() -> int:
    a, b = index(V9), index(V10)
    changed = sorted(k for k in a.keys() & b.keys() if a[k] != b[k])
    added = sorted(b.keys() - a.keys())
    removed = sorted(a.keys() - b.keys())

    historical_prefixes = tuple(sorted(
        n.name for n in V9.iterdir() if n.is_dir() and n.name.startswith("historical-")))
    historical_changed = [k for k in changed if k.startswith(historical_prefixes)]

    out = {
        "standing": "Preservation check. package9 is immutable and is only READ here.",
        "v9ArtifactManifestSha256": sha(V9 / "artifact-manifest.json"),
        "v9ArtifactManifestIdClaimedByRoot": V9_MANIFEST_EXPECTED,
        "v9ArtifactManifestMatchesRootClaim":
            V9_MANIFEST_EXPECTED.removeprefix("MF") == sha(V9 / "artifact-manifest.json"),
        "v9FileCount": len(a), "v10FileCount": len(b),
        "changedVsV9": changed, "addedVsV9": added, "removedVsV9": removed,
        "removedCount": len(removed),
        "historicalDirectoriesInV9": list(historical_prefixes),
        "historicalArtifactsChanged": historical_changed,
        "historicalArtifactsPreserved": not historical_changed,
        "nothingRemoved": not removed,
        "sourceRebuildReceiptPreserved": a.get("source-rebuild.v1.json") == b.get("source-rebuild.v1.json"),
        "residualAssessmentPreserved":
            a.get("evaluation-residual-author-assessment.json")
            == b.get("evaluation-residual-author-assessment.json"),
        "originalRequirementHandoffPreserved":
            a.get("original-requirement-handoff.json") == b.get("original-requirement-handoff.json"),
        "workspaceHistoryPreserved":
            a.get("author-workspace-history.tar.gz") == b.get("author-workspace-history.tar.gz"),
    }
    (HERE / "reports" / "preservation.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "changedVsV9"} |
                     {"changedVsV9Count": len(changed), "changedVsV9": changed}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
