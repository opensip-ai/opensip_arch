"""Combined (vs frozen39) and incremental (vs the applied v1 delta) delta manifests and patches of the corrected copy.

Combined: walks the whole edited copy (no __pycache__), compares every file with the verified frozen39 manifest members and
diffs changed files against work/before-images-v39 (refused unless the image equals the manifest digest).
Incremental: compares the six v1 after-files (custody/before-images-v1.json, images under work/before-images-v1) plus any
file outside them with the current copy, so it lists exactly the changes made after the v1 delta was applied.
Writes custody/combined-delta-manifest.json, output/combined.patch, custody/incremental-delta-manifest.json and
output/incremental.patch. Usage: make_delta.py
"""
import difflib
import hashlib
import json
import os
from pathlib import Path

R = Path(__file__).resolve().parent
S = R / "work/source"
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
F39 = "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009"
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = MANIFEST.read_bytes()
if sha(raw) != F39:
    raise SystemExit("manifest digest mismatch")
frozen = {f["path"]: f for f in json.loads(raw)["files"]}
now, pycache = {}, []
for d, dirs, files in os.walk(S):
    pycache += [str((Path(d) / x).relative_to(S)) for x in dirs if x == "__pycache__"]
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for name in files:
        data = (Path(d) / name).read_bytes()
        now[(Path(d) / name).relative_to(S).as_posix()] = (sha(data), len(data))


def build(label, base, image_root):
    rows, parts = [], []
    for rel in sorted(set(now) | set(base), key=lambda s: s.encode()):
        before, after = base.get(rel), now.get(rel)
        if before and after and before["sha256"] == after[0]:
            continue
        status = "modified" if before and after else "added" if after else "removed"
        old_text = ""
        if before:
            image = image_root / rel
            if not image.exists() or sha(image.read_bytes()) != before["sha256"]:
                raise SystemExit("%s: no faithful before-image for %s" % (label, rel))
            old_text = image.read_text()
        new_text = (S / rel).read_text() if after else ""
        diff = list(difflib.unified_diff(old_text.splitlines(keepends=True), new_text.splitlines(keepends=True),
                                         fromfile="a/" + rel if before else "/dev/null", tofile="b/" + rel if after else "/dev/null", n=3))
        rows.append({"path": rel, "status": status, "beforeSha256": before["sha256"] if before else None, "beforeBytes": before["bytes"] if before else None,
                     "afterSha256": after[0] if after else None, "afterBytes": after[1] if after else None, "patchLines": len(diff)})
        parts.extend(diff)
    return rows, "".join(parts)


combined_rows, combined_patch = build("combined", frozen, R / "work/before-images-v39")
v1_after = {f["path"]: f for f in json.loads((R / "custody/before-images-v1.json").read_text())["files"]}
v1_base = {rel: row for rel, row in frozen.items() if rel not in v1_after} | v1_after
incremental_rows, incremental_patch = build("incremental", v1_base, R / "work/before-images-v1")
(R / "output").mkdir(exist_ok=True)
(R / "output/combined.patch").write_text(combined_patch)
(R / "output/incremental.patch").write_text(incremental_patch)
common = {"editedCopyFiles": len(now), "pycacheDirectories": sorted(pycache)}
combined = {"artifact": "policy-test-imported-universe-author.combined-delta", "version": 1, "base": str(MANIFEST), "baseManifestSha256": F39,
            **common, "changes": combined_rows, "patch": "output/combined.patch", "patchSha256": sha(combined_patch.encode()), "patchLines": combined_patch.count("\n")}
incremental = {"artifact": "policy-test-imported-universe-author.incremental-delta", "version": 1,
               "base": "frozen39 + completed v1 delta (patch 8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28)",
               "v1AfterImages": "custody/before-images-v1.json", **common, "changes": incremental_rows, "patch": "output/incremental.patch",
               "patchSha256": sha(incremental_patch.encode()), "patchLines": incremental_patch.count("\n")}
(R / "custody/combined-delta-manifest.json").write_text(json.dumps(combined, indent=1) + "\n")
(R / "custody/incremental-delta-manifest.json").write_text(json.dumps(incremental, indent=1) + "\n")
print(json.dumps({"combined": {k: combined[k] for k in ("patchSha256", "patchLines", "pycacheDirectories")} | {"changes": [(r["status"], r["path"], r["patchLines"]) for r in combined_rows]},
                  "incremental": {k: incremental[k] for k in ("patchSha256", "patchLines")} | {"changes": [(r["status"], r["path"], r["patchLines"]) for r in incremental_rows]}}, indent=1))
