"""Cumulative delta against frozen43 and incremental delta against the wire43 handoff work copy.

usage: make_delta_two_bases.py <frozen43-root> <wire43-work-root> <work-root> <out-dir>

Writes <out-dir>/cumulative-vs-frozen43/{files.json,unified.patch,repin-index.json} and
<out-dir>/incremental-vs-wire43/{files.json,unified.patch}. BEFORE hashes of the cumulative delta come from the
frozen43 manifest; parent hashes of the incremental delta come from hashing the verified wire43 work copy.
"""
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json"
frozen, wire, work, out = (Path(p) for p in sys.argv[1:5])
out.mkdir(parents=True, exist_ok=False)


def tree(root):
    rows = {}
    for d, _, files in os.walk(root):
        for f in files:
            p = Path(d) / f
            b = p.read_bytes()
            rows[str(p.relative_to(root))] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return rows


def delta(base_rows, base_root, target_rows, label_base, label_target):
    changed, patch = [], []
    for rel in sorted(set(base_rows) | set(target_rows)):
        b, t = base_rows.get(rel), target_rows.get(rel)
        if b and t and b["sha256"] == t["sha256"]:
            continue
        status = "modified" if b and t else ("added" if t else "removed")
        changed.append({"path": rel, "status": status, label_base + "Sha256": b["sha256"] if b else None,
                        label_base + "Bytes": b["bytes"] if b else None, label_target + "Sha256": t["sha256"] if t else None,
                        label_target + "Bytes": t["bytes"] if t else None})
        old = (base_root / rel).read_text(encoding="utf-8").splitlines(keepends=True) if b else []
        new = (work / rel).read_text(encoding="utf-8").splitlines(keepends=True) if t else []
        hunk = list(difflib.unified_diff(old, new, fromfile="a/" + rel if b else "/dev/null", tofile="b/" + rel if t else "/dev/null", n=3))
        if hunk and not hunk[-1].endswith("\n"):
            hunk[-1] += "\n\\ No newline at end of file\n"
        patch.extend(hunk)
    return changed, patch


manifest = {m["path"]: {"sha256": m["sha256"], "bytes": m["bytes"]} for m in json.loads(Path(MANIFEST).read_bytes())["files"]}
work_rows = tree(work)
wire_rows = tree(wire)
cum, cum_patch = delta(manifest, frozen, work_rows, "frozen43", "current")
inc, inc_patch = delta(wire_rows, wire, work_rows, "wire43Parent", "current")
cum_dir, inc_dir = out / "cumulative-vs-frozen43", out / "incremental-vs-wire43"
cum_dir.mkdir()
inc_dir.mkdir()
(cum_dir / "files.json").write_text(json.dumps({"base": "frozen43 manifest " + MANIFEST, "changed": cum}, indent=1) + "\n", encoding="utf-8")
(cum_dir / "unified.patch").write_text("".join(cum_patch), encoding="utf-8")
(inc_dir / "files.json").write_text(json.dumps({"base": str(wire), "changed": inc}, indent=1) + "\n", encoding="utf-8")
(inc_dir / "unified.patch").write_text("".join(inc_patch), encoding="utf-8")
before = {r["frozen43Sha256"]: r["path"] for r in cum if r["frozen43Sha256"]}
ledgers = []
for d, _, files in os.walk(work / "docs"):
    for f in files:
        if f.endswith((".json", ".md")):
            p = Path(d) / f
            rel = str(p.relative_to(work))
            text = p.read_text(encoding="utf-8", errors="replace")
            hits = sorted({path for sha, path in before.items() if sha in text and path != rel})
            if hits:
                ledgers.append({"ledger": rel, "namesFrozen43DigestOf": hits})
(cum_dir / "repin-index.json").write_text(json.dumps({"note": "ledgers in the corrected copy that still name a frozen43 digest of a changed file; not edited by this author runtime", "ledgers": ledgers}, indent=1) + "\n", encoding="utf-8")
print(json.dumps({"cumulativeChanged": len(cum), "cumulativeAdded": sum(r["status"] == "added" for r in cum),
                  "cumulativePatchLines": len(cum_patch), "incrementalChanged": len(inc),
                  "incrementalAdded": sum(r["status"] == "added" for r in inc), "incrementalPatchLines": len(inc_patch),
                  "ledgersNamingFrozen43Digests": len(ledgers)}, indent=1))
