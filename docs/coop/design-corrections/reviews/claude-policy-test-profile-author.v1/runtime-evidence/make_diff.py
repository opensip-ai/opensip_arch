"""Exact correction manifest and diff of work/source against its own capture custody.

Walks the whole edited copy (no __pycache__), compares every file with custody/captured-source.json, and classifies
modified / added / removed. Modified files are diffed against the pre-edit snapshot work/baseline-files (and refused if a
modified path has no snapshot or the snapshot does not equal the captured bytes); added files are diffed from /dev/null.
Writes custody/correction-manifest.json and output/correction.diff. Usage: make_diff.py
"""
import difflib
import hashlib
import json
import os
from pathlib import Path

R = Path(__file__).resolve().parent
S, B = R / "work/source", R / "work/baseline-files"
captured = {f["path"]: f for f in json.loads((R / "custody/captured-source.json").read_text())["files"]}
now = {}
for d, dirs, files in os.walk(S):
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        p = Path(d) / name
        data = p.read_bytes()
        now[p.relative_to(S).as_posix()] = (hashlib.sha256(data).hexdigest(), len(data))
pycache = sorted(str(Path(d).relative_to(S)) for d, dirs, _ in os.walk(S) for x in dirs if x == "__pycache__")
rows, parts = [], []
for rel in sorted(set(now) | set(captured), key=lambda s: s.encode()):
    before = captured.get(rel)
    after = now.get(rel)
    if before and after and before["sha256"] == after[0]:
        continue
    status = "modified" if before and after else "added" if after else "removed"
    row = {"path": rel, "status": status, "beforeSha256": before["sha256"] if before else None, "beforeBytes": before["bytes"] if before else None,
           "afterSha256": after[0] if after else None, "afterBytes": after[1] if after else None}
    old_text = ""
    if status == "modified":
        snap = B / rel
        if not snap.exists() or hashlib.sha256(snap.read_bytes()).hexdigest() != before["sha256"]:
            raise SystemExit("no faithful pre-edit snapshot for " + rel)
        old_text = snap.read_text()
    new_text = (S / rel).read_text() if after else ""
    diff = list(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                     fromfile=("a/" + rel) if before else "/dev/null", tofile=("b/" + rel) if after else "/dev/null", n=3))
    row["diffLines"] = len(diff)
    rows.append(row)
    parts.extend(diff if not diff or diff[-1].endswith("\n") else diff + ["\n"])
text = "".join(parts)
(R / "output").mkdir(exist_ok=True)
(R / "output/correction.diff").write_text(text)
manifest = {"artifact": "policy-test-profile-author.correction-manifest", "version": 1,
            "capturedFileListManifestSha256": json.loads((R / "custody/captured-source.json").read_text())["fileListManifestSha256"],
            "editedCopyFiles": len(now), "pycacheDirectories": pycache, "changes": rows,
            "diff": "output/correction.diff", "diffSha256": hashlib.sha256(text.encode()).hexdigest(), "diffLines": text.count("\n")}
(R / "custody/correction-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
print(json.dumps({k: manifest[k] for k in ("editedCopyFiles", "pycacheDirectories", "diffSha256", "diffLines")}
                 | {"changes": [(r["status"], r["path"], r["diffLines"]) for r in rows]}, indent=1))
