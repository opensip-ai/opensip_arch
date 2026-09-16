"""Make a run copy of a source tree so suites that write reports into their own directories never touch SRC.

Usage: make_run_copy.py SRC DEST OUT_JSON [--pin-overlay DELTA_MANIFEST_JSON]

Every regular file under SRC (no symlinks; __pycache__ skipped and reported) is written to DEST with open('xb') and
re-hashed. With --pin-overlay, in the COPY ONLY, every `*source-pins*.json` under docs/coop/design-corrections (reviews/
excluded) has the sha256 of each entry whose path is a delta file rewritten from the delta's before-sha256 to its
after-sha256; every replacement and every entry not at its before value is recorded. This lets pin-verifying suites
exercise the corrected bytes without the delta itself touching any registered pin file.
"""
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

src, dest, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
overlay = Path(sys.argv[sys.argv.index("--pin-overlay") + 1]).resolve() if "--pin-overlay" in sys.argv else None
if dest.exists():
    raise SystemExit("destination exists: %s" % dest)
files, symlinks, pycache, total = [], [], [], 0
for d, dirs, names in os.walk(src):
    pycache += [str((Path(d) / x).relative_to(src)) for x in dirs if x == "__pycache__"]
    dirs[:] = sorted(x for x in dirs if x != "__pycache__")
    for n in sorted(names):
        p = Path(d) / n
        if p.is_symlink():
            symlinks.append(str(p.relative_to(src)))
        else:
            files.append(p.relative_to(src))
            total += p.stat().st_size
free = shutil.disk_usage(dest.parent).free
if symlinks or free < 2 * total:
    raise SystemExit(json.dumps({"symlinks": symlinks[:20], "freeBytes": free, "neededBytes": 2 * total}))
faults = []
for rel in files:
    data = (src / rel).read_bytes()
    target = dest / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "xb") as fh:
        fh.write(data)
    if hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(data).digest() or os.stat(target).st_nlink != 1:
        faults.append(str(rel))
record = {"artifact": "nested-workspace-author.run-copy", "version": 1, "source": str(src), "copy": str(dest),
          "fileCount": len(files), "totalBytes": total, "copyFaults": faults, "pycacheDirsSkipped": pycache, "pinOverlay": None}
if overlay is not None:
    delta = json.loads(overlay.read_text())
    replaced, not_at_before = [], []
    kit = dest / "docs/coop/design-corrections"
    for pin_file in sorted(kit.rglob("*source-pins*.json")):
        rel = pin_file.relative_to(dest).as_posix()
        if "/reviews/" in rel:
            continue
        text = pin_file.read_text(encoding="utf-8")
        before_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
        changed = False
        for f in delta["files"]:
            pattern = re.compile(r'("path": "%s",\s*"sha256": ")([0-9a-f]{64})(")' % re.escape(f["path"]))
            for mt in pattern.finditer(text):
                if mt.group(2) != f["before"]["sha256"]:
                    not_at_before.append({"pinFile": rel, "path": f["path"], "pinned": mt.group(2)})
            text, n = pattern.subn(lambda mt: mt.group(1) + f["after"]["sha256"] + mt.group(3)
                                   if mt.group(2) == f["before"]["sha256"] else mt.group(0), text)
            if n:
                replaced.append({"pinFile": rel, "path": f["path"], "matches": n})
                changed = True
        if changed:
            pin_file.write_text(text, encoding="utf-8")
            record.setdefault("pinFilesRewritten", []).append(
                {"pinFile": rel, "beforeSha256": before_sha, "afterSha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})
    record["pinOverlay"] = {"deltaManifest": str(overlay), "deltaManifestSha256": hashlib.sha256(overlay.read_bytes()).hexdigest(),
                            "replaced": replaced, "entriesNotAtBefore": not_at_before}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(record, indent=1) + "\n")
print(json.dumps({k: record[k] for k in ("fileCount", "totalBytes", "copyFaults")} | {"pinOverlay": record["pinOverlay"]}, indent=1))
raise SystemExit(1 if faults else 0)
