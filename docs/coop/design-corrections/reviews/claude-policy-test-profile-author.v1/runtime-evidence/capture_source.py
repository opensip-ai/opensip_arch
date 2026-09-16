"""Capture a regular-file copy of the mutable successor source and record its custody.

1. Walks INPUT (excluding __pycache__) and hashes every file (pass 1); symlinks are refused.
2. Copies each file byte-for-byte into DEST (fresh regular files, never hardlinks), hashing the bytes actually written.
3. Re-hashes INPUT (pass 2). Any drift between passes, or a copied file that differs from pass 1, refuses (exit 1).
4. Compares the capture with two earlier custody manifests: the policy-test assessment's fixed capture (root
   root-repair-owner-probe.v2/capture.json, paths relative to the same root) and the author-package-migration capture.
Writes OUT_JSON and prints a summary.
Usage: capture_source.py INPUT DEST OUT_JSON
"""
import hashlib
import json
import os
import sys
from pathlib import Path

ASSESSMENT = Path("/tmp/opensip-design-corrections/root-repair-owner-probe.v2/capture.json")
MIGRATION = Path("/private/tmp/opensip-design-corrections/claude-author-package-migration.v1/custody/captured-source.json")
src, dest, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
if dest.exists():
    raise SystemExit("destination exists: %s" % dest)


def walk(root):
    rows = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x != "__pycache__")
        for name in sorted(files):
            p = Path(d) / name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink():
                raise SystemExit("symlink refused: %s" % rel)
            data = p.read_bytes()
            rows[rel] = (hashlib.sha256(data).hexdigest(), len(data))
    return rows


def compare(label, manifest_path, rows):
    raw = manifest_path.read_bytes()
    listed = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
    common = set(listed) & set(rows)
    return {"manifest": str(manifest_path), "manifestSha256": hashlib.sha256(raw).hexdigest(), "listed": len(listed),
            "modified": sorted(r for r in common if listed[r] != rows[r][0]),
            "onlyInCapture": len(set(rows) - set(listed)),
            "onlyInCaptureUnderDesignCorrections": sorted(r for r in set(rows) - set(listed) if r.startswith("docs/coop/design-corrections/") and label == "assessment")[:200],
            "missingFromCapture": sorted(set(listed) - set(rows))}


first = walk(src)
copy_faults = []
for rel, (digest, size) in first.items():
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    data = (src / rel).read_bytes()
    with open(target, "xb") as fh:
        fh.write(data)
    written = target.read_bytes()
    if hashlib.sha256(written).hexdigest() != digest or len(written) != size or os.stat(target).st_nlink != 1:
        copy_faults.append(rel)
second = walk(src)
drift = sorted(set(first) ^ set(second)) + sorted(r for r in set(first) & set(second) if first[r] != second[r])
files = [{"path": rel, "sha256": d, "bytes": s} for rel, (d, s) in sorted(first.items(), key=lambda kv: kv[0].encode())]
manifest_bytes = json.dumps({"files": files}, indent=1).encode() + b"\n"
report = {
    "artifact": "policy-test-profile-author.captured-source", "version": 1,
    "standing": "Provisional regular-file capture of a MUTABLE integration tree for a bounded author correction; not a frozen candidate.",
    "input": str(src), "capture": str(dest), "fileCount": len(first), "totalBytes": sum(s for _, s in first.values()),
    "copyFaults": copy_faults, "inputDriftDuringCapture": drift,
    "fileListManifestSha256": hashlib.sha256(manifest_bytes).hexdigest(),
    "vsAssessmentFixedCapture": compare("assessment", ASSESSMENT, first),
    "vsAuthorPackageMigrationCapture": compare("migration", MIGRATION, first),
    "files": files,
}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=1) + "\n")
(out_json.parent / "captured-source.file-list.json").write_bytes(manifest_bytes)
print(json.dumps({k: report[k] for k in ("fileCount", "totalBytes", "copyFaults", "inputDriftDuringCapture", "fileListManifestSha256")}
                 | {"vsAssessmentModified": report["vsAssessmentFixedCapture"]["modified"],
                    "vsAssessmentMissing": report["vsAssessmentFixedCapture"]["missingFromCapture"][:50],
                    "vsMigrationModified": report["vsAuthorPackageMigrationCapture"]["modified"],
                    "vsMigrationMissing": report["vsAuthorPackageMigrationCapture"]["missingFromCapture"][:50],
                    "vsMigrationOnlyInCapture": report["vsAuthorPackageMigrationCapture"]["onlyInCapture"]}, indent=1))
raise SystemExit(1 if copy_faults or drift else 0)
