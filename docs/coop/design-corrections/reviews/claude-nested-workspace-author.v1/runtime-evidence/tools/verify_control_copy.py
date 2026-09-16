"""Record the ACTUAL state of the control-discrimination copy after tools/mutate_run_copy.py.

mutate_run_copy.py changed the copy but then failed to write its record (its OUT_JSON directory did not exist; receipt
control-copy-mutate is kept). It cannot be re-run: its precondition (model at after-bytes) no longer holds. This reads
the copy and states what it holds, instead of assuming the mutation completed.

Usage: verify_control_copy.py DIR DELTA_MANIFEST OUT_JSON REVERTED_REL_PATH
Holds when: REVERTED_REL_PATH is at the delta before-sha256 (frozen39 bytes); every other delta file is at its after-sha256;
in every non-review *source-pins*.json the REVERTED path's entries are at before and every other delta path's entries
are at after; and no pin entry of a delta path is at any other value.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

d, delta_path, out_json, reverted = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(), sys.argv[4]
delta = json.loads(delta_path.read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
files, pins, faults = [], [], []
for f in delta["files"]:
    want = f["before"] if f["path"] == reverted else f["after"]
    data = (d / f["path"]).read_bytes()
    ok = sha(data) == want["sha256"] and len(data) == want["bytes"]
    files.append({"path": f["path"], "expected": "before" if f["path"] == reverted else "after", "sha256": sha(data), "holds": ok})
    if not ok:
        faults.append({"path": f["path"], "fault": "file not at expected bytes"})
for pin_file in sorted((d / "docs/coop/design-corrections").rglob("*source-pins*.json")):
    rel = pin_file.relative_to(d).as_posix()
    if "/reviews/" in rel:
        continue
    text = pin_file.read_text(encoding="utf-8")
    for f in delta["files"]:
        want = (f["before"] if f["path"] == reverted else f["after"])["sha256"]
        for mt in re.finditer(r'"path": "%s",\s*"sha256": "([0-9a-f]{64})"' % re.escape(f["path"]), text):
            ok = mt.group(1) == want
            pins.append({"pinFile": rel, "path": f["path"], "pinned": mt.group(1), "holds": ok})
            if not ok:
                faults.append({"pinFile": rel, "path": f["path"], "fault": "pin entry not at expected value"})
record = {"artifact": "nested-workspace-author.control-copy-state", "version": 1, "copy": str(d), "delta": str(delta_path),
          "deltaSha256": sha(delta_path.read_bytes()), "reverted": reverted, "files": files, "pinEntries": pins,
          "pinEntryCount": len(pins), "faults": faults, "holds": not faults}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(record, indent=1) + "\n")
print(json.dumps({"files": files, "pinEntryCount": len(pins), "faults": faults, "holds": not faults}, indent=1))
raise SystemExit(0 if not faults else 1)
