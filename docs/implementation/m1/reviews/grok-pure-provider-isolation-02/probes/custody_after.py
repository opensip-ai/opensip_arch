"""Re-hash frozen subject and live shared sources after independent execution."""
from __future__ import annotations

import hashlib
import json
import stat
import sys
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
PRODUCT = Path("/Users/sb/code/opensip-ai/opensip")
REVIEW = Path("/tmp/opensip-implementation/m1-grok-pure-provider-isolation-02-review/review")
SUBJECT_REL = "docs/implementation/m1/trials/pure-provider-isolation-02/subject.json"
EXPECTED_SUBJECT_SHA = "3147a63a43825c4c9b1236d72f6b0afa36b507e3b518c13db4147f58c3479280"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not sys.flags.isolated or sys.flags.optimize:
        raise SystemExit("isolated Python without optimization required")
    before = json.loads((REVIEW / "results" / "custody-before.json").read_bytes())
    subject_path = ARCH / SUBJECT_REL
    subject_sha = sha256_file(subject_path)
    subject = json.loads(subject_path.read_bytes())
    mismatches = []
    members = []
    for row in subject["files"]:
        path = ARCH / row["path"]
        raw = path.read_bytes()
        actual = {
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "mode": stat.S_IMODE(path.stat().st_mode),
        }
        ok = actual["bytes"] == row["bytes"] and actual["sha256"] == row["sha256"]
        members.append({"path": row["path"], "match": ok, **actual})
        if not ok:
            mismatches.append(row["path"])
    live_mismatches = []
    live_rows = []
    for row in before["shared"]:
        live = PRODUCT / row["path"]
        raw = live.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        ok = sha == row["pin"]["sha256"] and len(raw) == row["pin"]["bytes"]
        live_rows.append({"path": row["path"], "sha256": sha, "bytes": len(raw), "matchPin": ok})
        if not ok:
            live_mismatches.append(row["path"])
    out = {
        "subjectSha256": subject_sha,
        "subjectShaMatch": subject_sha == EXPECTED_SUBJECT_SHA,
        "subjectUnchangedFromBefore": subject_sha == before["subjectSha256"],
        "membersMatch": not mismatches,
        "mismatches": mismatches,
        "memberCount": len(members),
        "liveSharedMatchPins": not live_mismatches,
        "liveMismatches": live_mismatches,
        "liveShared": live_rows,
        "frozenFilesOrLiveProductAltered": bool(mismatches or live_mismatches or subject_sha != EXPECTED_SUBJECT_SHA),
    }
    (REVIEW / "results" / "custody-after.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in (
        "subjectShaMatch", "subjectUnchangedFromBefore", "membersMatch",
        "liveSharedMatchPins", "frozenFilesOrLiveProductAltered", "mismatches", "liveMismatches",
    )}, indent=2))


if __name__ == "__main__":
    main()
