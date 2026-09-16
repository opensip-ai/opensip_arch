"""Per-file before/after hashes, unified patch and repin index for the work copy against frozen43.

usage: make_delta.py <frozen43-root> <work-candidate-root> <delta-dir>

Reads the frozen43 manifest for BEFORE hashes, hashes every work-copy file for AFTER, writes
files.json and unified.patch, and lists every JSON/MD ledger in the work copy that still names a
changed file's BEFORE digest (the repins root must perform; none are edited here).
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json"
frozen, work, delta = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
delta.mkdir(parents=True, exist_ok=False)
manifest = {m["path"]: m for m in json.loads(Path(MANIFEST).read_bytes())["files"]}
after = {}
for d, _, files in os.walk(work):
    for f in files:
        p = Path(d) / f
        rel = str(p.relative_to(work))
        b = p.read_bytes()
        after[rel] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
rows, patch = [], []
for rel in sorted(set(manifest) | set(after)):
    m, a = manifest.get(rel), after.get(rel)
    if m and a and m["sha256"] == a["sha256"]:
        continue
    status = "modified" if m and a else ("added" if a else "removed")
    rows.append({"path": rel, "status": status, "beforeSha256": m["sha256"] if m else None,
                 "beforeBytes": m["bytes"] if m else None, "afterSha256": a["sha256"] if a else None,
                 "afterBytes": a["bytes"] if a else None})
    old_lines = (frozen / rel).read_text(encoding="utf-8").splitlines(keepends=True) if m else []
    new_lines = (work / rel).read_text(encoding="utf-8").splitlines(keepends=True) if a else []
    patch.extend(difflib.unified_diff(old_lines, new_lines, fromfile="a/" + rel if m else "/dev/null",
                                      tofile="b/" + rel if a else "/dev/null", n=3))
    if patch and not patch[-1].endswith("\n"):
        patch[-1] += "\n\\ No newline at end of file\n"
changed_before = {r["beforeSha256"]: r["path"] for r in rows if r["beforeSha256"]}
ledgers = []
for d, _, files in os.walk(work / "docs"):
    for f in files:
        if not f.endswith((".json", ".md")):
            continue
        p = Path(d) / f
        rel = str(p.relative_to(work))
        text = p.read_text(encoding="utf-8", errors="replace")
        hits = sorted({path for sha, path in changed_before.items() if sha in text and path != rel})
        if hits:
            ledgers.append({"ledger": rel, "namesBeforeDigestOf": hits})
(delta / "files.json").write_text(json.dumps({"frozenManifest": MANIFEST, "changed": rows}, indent=1) + "\n", encoding="utf-8")
(delta / "unified.patch").write_text("".join(patch), encoding="utf-8")
(delta / "repin-index.json").write_text(json.dumps({"note": "ledgers in the corrected copy that still name a BEFORE digest of a changed file; not edited by this author runtime", "ledgers": ledgers}, indent=1) + "\n", encoding="utf-8")
print(json.dumps({"changed": len(rows), "added": sum(r["status"] == "added" for r in rows),
                  "patchLines": len(patch), "ledgersNamingBeforeDigests": len(ledgers)}, indent=1))
