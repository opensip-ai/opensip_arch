"""Turn an already-used run copy of the corrected capture into a CONTROL-DISCRIMINATION copy: corrected checkers and
cases, but the frozen39 (pre-fix) native model.

Usage: mutate_run_copy.py DIR DELTA_MANIFEST OUT_JSON --revert REL_PATH

1. REL_PATH in DIR must currently hold the delta's after-bytes; it is overwritten with the frozen39 member bytes, which
   must match the delta's before sha256/bytes (read from the formal manifest's snapshot root).
2. In every *source-pins*.json under DIR/docs/coop/design-corrections (reviews/ excluded) the entries of every OTHER
   delta file are rewritten from before to after sha256; REL_PATH's entries stay at before (which is what it now holds).
Every changed file's before/after sha256 is recorded. DIR's earlier receipts are unaffected; this only changes DIR.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

d, delta_path, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
revert = sys.argv[sys.argv.index("--revert") + 1]
delta = json.loads(delta_path.read_text())
manifest = json.loads(Path(delta["base"]["manifest"]).read_bytes())
if hashlib.sha256(Path(delta["base"]["manifest"]).read_bytes()).hexdigest() != delta["base"]["manifestSha256"]:
    raise SystemExit("manifest sha mismatch")
entry = next(f for f in delta["files"] if f["path"] == revert)
sha = lambda b: hashlib.sha256(b).hexdigest()
current = (d / revert).read_bytes()
frozen = (Path(manifest["snapshotRoot"]) / revert).read_bytes()
if sha(current) != entry["after"]["sha256"] or sha(frozen) != entry["before"]["sha256"] or len(frozen) != entry["before"]["bytes"]:
    raise SystemExit("revert preconditions failed")
(d / revert).write_bytes(frozen)
changes = [{"path": revert, "beforeSha256": sha(current), "afterSha256": sha(frozen), "role": "reverted to frozen39 bytes"}]
others = [f for f in delta["files"] if f["path"] != revert]
for pin_file in sorted((d / "docs/coop/design-corrections").rglob("*source-pins*.json")):
    rel = pin_file.relative_to(d).as_posix()
    if "/reviews/" in rel:
        continue
    text = pin_file.read_text(encoding="utf-8")
    new = text
    for f in others:
        pattern = re.compile(r'("path": "%s",\s*"sha256": ")%s(")' % (re.escape(f["path"]), f["before"]["sha256"]))
        new = pattern.sub(lambda mt: mt.group(1) + f["after"]["sha256"] + mt.group(2), new)
    if new != text:
        pin_file.write_text(new, encoding="utf-8")
        changes.append({"path": rel, "beforeSha256": sha(text.encode("utf-8")), "afterSha256": sha(new.encode("utf-8")),
                        "role": "pin overlay for delta files other than the reverted one"})
record = {"artifact": "nested-workspace-author.control-discrimination-copy", "version": 1, "copy": str(d), "delta": str(delta_path),
          "deltaSha256": sha(delta_path.read_bytes()), "reverted": revert, "changes": changes}
out_json.write_text(json.dumps(record, indent=1) + "\n")
print(json.dumps(record, indent=1))
