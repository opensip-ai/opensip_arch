"""Exact delta manifest and patch of the corrected capture against the verified frozen39 manifest.

Walks the whole edited copy (no __pycache__), compares every file with the frozen39 manifest members (the capture's
verified bytes), and classifies modified / added / removed. Modified files are diffed against work/staging, the pre-edit
copy of the same frozen bytes (refused unless the staged bytes equal the manifest digest). Writes
custody/delta-manifest.json and output/correction.patch (unified, a/ b/ prefixes). Usage: make_delta.py
"""
import difflib
import hashlib
import json
import os
from pathlib import Path

R = Path(__file__).resolve().parent
S, G = R / "work/source39", R / "work/staging"
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
raw = MANIFEST.read_bytes()
if hashlib.sha256(raw).hexdigest() != "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009":
    raise SystemExit("manifest digest mismatch")
frozen = {f["path"]: f for f in json.loads(raw)["files"]}
now, pycache = {}, []
for d, dirs, files in os.walk(S):
    pycache += [str((Path(d) / x).relative_to(S)) for x in dirs if x == "__pycache__"]
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        p = Path(d) / name
        data = p.read_bytes()
        now[p.relative_to(S).as_posix()] = (hashlib.sha256(data).hexdigest(), len(data))
rows, parts = [], []
for rel in sorted(set(now) | set(frozen), key=lambda s: s.encode()):
    before, after = frozen.get(rel), now.get(rel)
    if before and after and before["sha256"] == after[0]:
        continue
    status = "modified" if before and after else "added" if after else "removed"
    old_text = ""
    if before:
        staged = G / rel
        if not staged.exists() or hashlib.sha256(staged.read_bytes()).hexdigest() != before["sha256"]:
            raise SystemExit("no faithful pre-edit copy for " + rel)
        old_text = staged.read_text()
    new_text = (S / rel).read_text() if after else ""
    diff = list(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                     fromfile="a/" + rel if before else "/dev/null", tofile="b/" + rel if after else "/dev/null", n=3))
    rows.append({"path": rel, "status": status, "beforeSha256": before["sha256"] if before else None, "beforeBytes": before["bytes"] if before else None,
                 "afterSha256": after[0] if after else None, "afterBytes": after[1] if after else None, "patchLines": len(diff)})
    parts.extend(diff)
text = "".join(parts)
(R / "output").mkdir(exist_ok=True)
(R / "output/correction.patch").write_text(text)
manifest = {"artifact": "policy-test-known-hit-author.delta-manifest", "version": 1, "base": str(MANIFEST),
            "baseManifestSha256": hashlib.sha256(raw).hexdigest(), "editedCopyFiles": len(now), "pycacheDirectories": sorted(pycache),
            "changes": rows, "patch": "output/correction.patch", "patchSha256": hashlib.sha256(text.encode()).hexdigest(), "patchLines": text.count("\n")}
(R / "custody/delta-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
print(json.dumps({k: manifest[k] for k in ("editedCopyFiles", "pycacheDirectories", "patchSha256", "patchLines")}
                 | {"changes": [(r["status"], r["path"], r["patchLines"]) for r in rows]}, indent=1))
