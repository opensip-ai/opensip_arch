"""Build the correction delta of the edited capture against the formal frozen39 manifest.

Usage: build_delta.py EDITED_ROOT PATCH_OUT MANIFEST_OUT

Every frozen39 member is hashed in EDITED_ROOT; any file present in EDITED_ROOT but not listed (except __pycache__, which
is a fault) is an addition. Changed members get before/after sha256 and byte lengths from the manifest and the edited
bytes; the before bytes are read from the frozen39 snapshot and re-verified against the manifest before diffing. The
patch is a unified diff (a/ b/ prefixes, repo-relative paths, 3 lines of context) in path order.
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
EXPECTED = "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009"
edited, patch_out, manifest_out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
raw = MANIFEST.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise SystemExit("manifest sha mismatch")
manifest = json.loads(raw)
frozen = Path(manifest["snapshotRoot"])
listed = {f["path"]: f for f in manifest["files"]}
changed, missing, faults = [], [], []
for path, f in sorted(listed.items(), key=lambda kv: kv[0].encode("utf-8")):
    p = edited / path
    if p.is_symlink() or not p.is_file():
        missing.append(path)
        continue
    data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != f["sha256"] or len(data) != f["bytes"]:
        before = (frozen / path).read_bytes()
        if hashlib.sha256(before).hexdigest() != f["sha256"] or len(before) != f["bytes"]:
            faults.append({"path": path, "fault": "frozen39 member drifted"})
            continue
        changed.append((path, before, data))
added, pycache = [], []
for d, dirs, names in os.walk(edited):
    pycache += [str((Path(d) / x).relative_to(edited)) for x in dirs if x == "__pycache__"]
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for n in names:
        rel = (Path(d) / n).relative_to(edited).as_posix()
        if rel not in listed:
            added.append(rel)
chunks = []
for path, before, after in changed:
    chunks.extend(difflib.unified_diff(before.decode("utf-8").splitlines(keepends=True), after.decode("utf-8").splitlines(keepends=True),
                                       fromfile="a/" + path, tofile="b/" + path, n=3))
patch = "".join(chunks).encode("utf-8")
patch_out.parent.mkdir(parents=True, exist_ok=True)
patch_out.write_bytes(patch)
doc = {"artifact": "nested-workspace-author.delta-manifest", "version": 1,
       "standing": "bounded author correction delta over frozen39 bytes for root integration; not a freeze, repin, successor, acceptance or readiness claim",
       "base": {"manifest": str(MANIFEST), "manifestSha256": EXPECTED, "snapshotRoot": str(frozen), "memberCount": len(listed)},
       "patch": {"path": patch_out.name, "sha256": hashlib.sha256(patch).hexdigest(), "bytes": len(patch), "format": "unified diff, a/ b/ repo-relative, 3 context lines"},
       "files": [{"path": path, "before": {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)},
                  "after": {"sha256": hashlib.sha256(a).hexdigest(), "bytes": len(a)}} for path, b, a in changed],
       "addedFiles": sorted(added), "removedFiles": missing, "pycacheDirs": pycache, "faults": faults}
manifest_out.write_text(json.dumps(doc, indent=1) + "\n")
print(json.dumps({"changed": [c[0] for c in changed], "added": added, "removed": missing, "pycache": pycache, "faults": faults,
                  "patchSha256": doc["patch"]["sha256"], "patchBytes": len(patch)}, indent=1))
raise SystemExit(1 if faults or missing or added or pycache else 0)
