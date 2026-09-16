"""Reviewer probe: verify the frozen snapshot against its manifest (read-only).

Writes only results/manifest-check.json under the review directory.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
REVIEW = Path(__file__).resolve().parents[1]
BASE = Path("/tmp/opensip-implementation")
MANIFEST = BASE / "m1-canonical-subject-01.json"
SNAPSHOT = BASE / "m1-canonical-subject-01"
EXPECTED_MANIFEST_SHA256 = "8b2c31253d4699c9b25539000930234553df7f915eea011643ec675d70a3ef07"


def main():
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    result = {
        "manifestSha256": hashlib.sha256(raw).hexdigest(),
        "rows": [],
        "missingFiles": [],
        "extraFiles": [],
    }
    result["manifestSha256Matches"] = result["manifestSha256"] == EXPECTED_MANIFEST_SHA256
    listed = set()
    for row in manifest["files"]:
        listed.add(row["path"])
        path = SNAPSHOT / row["path"]
        if path.is_symlink() or not path.is_file():
            result["missingFiles"].append(row["path"])
            continue
        data = path.read_bytes()
        result["rows"].append({
            "path": row["path"],
            "sha256Matches": hashlib.sha256(data).hexdigest() == row["sha256"],
            "bytesMatch": len(data) == row["bytes"],
        })
    for path in sorted(SNAPSHOT.rglob("*")):
        if path.is_file() or path.is_symlink():
            relative = path.relative_to(SNAPSHOT).as_posix()
            if relative not in listed:
                result["extraFiles"].append(relative)
    lock = (SNAPSHOT / "design-lock.json").read_bytes()
    result["designLockSha256Matches"] = hashlib.sha256(lock).hexdigest() == manifest["designLockSha256"]
    result["passed"] = (
        result["manifestSha256Matches"]
        and result["designLockSha256Matches"]
        and not result["missingFiles"]
        and not result["extraFiles"]
        and all(r["sha256Matches"] and r["bytesMatch"] for r in result["rows"])
    )
    out = REVIEW / "results" / "manifest-check.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"passed": result["passed"], "manifestSha256": result["manifestSha256"]}))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
