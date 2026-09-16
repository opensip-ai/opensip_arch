"""Changed-file digest manifest and full unified diff of this runtime's working source against frozen source38.

Reads the pinned source38 manifest (verified by digest) and the frozen snapshot read-only; walks ./source (excluding
__pycache__). Writes OUTDIR/changed-files.v1.json and OUTDIR/source38-to-corrected.diff, and prints a summary.
Usage: diff_report.py OUTDIR
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v38.json"
EXPECTED = "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5"
raw = open(MANIFEST, "rb").read()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit("manifest hash mismatch")
manifest = json.loads(raw)
parent_root = Path(manifest["snapshotRoot"])
rows = {f["path"]: f for f in manifest["files"]}
source = HERE / "source"
out_dir = Path(sys.argv[1])
out_dir.mkdir(parents=True, exist_ok=True)


def sha(data):
    return hashlib.sha256(data).hexdigest()


changed, added, missing = [], [], []
for rel, row in sorted(rows.items()):
    p = source / rel
    if not p.is_file():
        missing.append(rel)
        continue
    data = p.read_bytes()
    if sha(data) != row["sha256"] or len(data) != row["bytes"]:
        parent = (parent_root / rel).read_bytes()
        if sha(parent) != row["sha256"]:
            raise SystemExit("frozen parent file differs from its manifest: " + rel)
        changed.append({"path": rel, "status": "modified", "parentSha256": row["sha256"], "parentBytes": row["bytes"],
                        "sha256": sha(data), "bytes": len(data)})
for d, _, files in os.walk(source):
    for name in files:
        rel = os.path.relpath(os.path.join(d, name), source)
        if "__pycache__" in rel.split(os.sep) or rel in rows:
            continue
        data = (source / rel).read_bytes()
        added.append({"path": rel, "status": "added", "parentSha256": None, "parentBytes": None,
                      "sha256": sha(data), "bytes": len(data)})
entries = sorted(changed + added, key=lambda r: r["path"].encode("utf-8"))
diff_parts = []
for entry in entries:
    rel = entry["path"]
    before = (parent_root / rel).read_bytes().decode("utf-8") if entry["status"] == "modified" else ""
    after = (source / rel).read_bytes().decode("utf-8")
    diff_parts.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                           fromfile="a/" + rel if before else "/dev/null", tofile="b/" + rel, n=3))
    if diff_parts and not diff_parts[-1].endswith("\n"):
        diff_parts[-1] += "\n\\ No newline at end of file\n"
diff_text = "".join(diff_parts)
(out_dir / "source38-to-corrected.diff").write_text(diff_text)
report = {"artifact": "consumer24-native-author.changed-files", "version": 1,
          "parentManifest": MANIFEST, "parentManifestSha256": EXPECTED, "parentSnapshotRoot": str(parent_root),
          "parentFileCount": len(rows), "missingFromCorrected": missing, "changedCount": len(changed), "addedCount": len(added),
          "files": entries, "diffSha256": sha(diff_text.encode("utf-8")), "diffBytes": len(diff_text.encode("utf-8"))}
(out_dir / "changed-files.v1.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({k: report[k] for k in ("changedCount", "addedCount", "missingFromCorrected", "diffSha256", "diffBytes")}
                 | {"paths": [e["path"] for e in entries]}, indent=1))
