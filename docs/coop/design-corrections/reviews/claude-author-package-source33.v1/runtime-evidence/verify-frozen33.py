#!/usr/bin/env python3
"""Verify every byte of frozen source33 against its authenticated manifest. READ ONLY."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
                "candidate-subject.v33.json")
ROOT = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
EXPECTED_MANIFEST_SHA = "1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299"


def main() -> int:
    raw = MANIFEST.read_bytes()
    manifest_sha = hashlib.sha256(raw).hexdigest()
    man = json.loads(raw)
    rows = man["files"]
    key_path = "path"
    key_sha = "sha256"
    mismatched, missing, extra = [], [], []
    seen = set()
    total = 0
    for row in rows:
        rel = row[key_path]
        seen.add(rel)
        target = ROOT / rel
        if not target.is_file():
            missing.append(rel)
            continue
        data = target.read_bytes()
        total += len(data)
        if hashlib.sha256(data).hexdigest() != row[key_sha]:
            mismatched.append({"path": rel, "manifest": row[key_sha],
                               "actual": hashlib.sha256(data).hexdigest()})
    on_disk = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*")
               if p.is_file() and not p.is_symlink()}
    extra = sorted(on_disk - seen)
    out = {
        "standing": "READ-ONLY byte verification of frozen source33 against its authenticated "
                    "manifest. Not acceptance.",
        "manifestPath": str(MANIFEST),
        "manifestSha256": manifest_sha,
        "manifestShaMatchesExpected": manifest_sha == EXPECTED_MANIFEST_SHA,
        "parentManifestSha256": man.get("parentManifestSha256"),
        "declaredFileCount": man.get("fileCount"),
        "declaredTotalBytes": man.get("totalBytes"),
        "verifiedFileCount": len(seen) - len(missing),
        "verifiedTotalBytes": total,
        "mismatchedCount": len(mismatched), "mismatched": mismatched[:50],
        "missingCount": len(missing), "missing": missing[:50],
        "extraOnDiskCount": len(extra), "extraOnDisk": extra[:50],
        "allBytesVerified": not mismatched and not missing and not extra
        and len(seen) == man.get("fileCount") and total == man.get("totalBytes"),
    }
    (HERE / "reports" / "frozen33-verification.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("mismatched", "missing", "extraOnDisk")}, indent=2))
    return 0 if out["allBytesVerified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
