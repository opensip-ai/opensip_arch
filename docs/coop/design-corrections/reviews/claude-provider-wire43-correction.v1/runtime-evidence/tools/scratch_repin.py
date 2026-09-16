"""Scratch-only pin refresh so the native checker can run over the corrected bytes.

usage: scratch_repin.py <scratch-candidate-root> <delta-json-out>

Refuses any root that is not inside this runtime's scratch-* directories. For native/source-pins.v2.json
it recomputes the sha256 of every existing entry and appends entries for consumed sources the checker
names that the ledger lacks. The work copy's ledger is never touched; the written delta is exactly the
repin that root must perform after integration. No other pin ledger is modified.
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
if not (str(root).startswith(str(RUNTIME / "scratch-")) and root.is_dir()):
    raise SystemExit("refusing: not a scratch root of this runtime: " + str(root))
native = root / "docs" / "coop" / "design-corrections" / "native"
spec = importlib.util.spec_from_file_location("scratch_checker", native / "check_native_evidence.v2.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
pins_path = native / "source-pins.v2.json"
doc = json.loads(pins_path.read_text(encoding="utf-8"))
delta = []
for pin in doc["pins"]:
    target = root / pin["path"]
    actual = hashlib.sha256(target.read_bytes()).hexdigest() if target.exists() else None
    if actual != pin["sha256"]:
        delta.append({"path": pin["path"], "change": "resha", "before": pin["sha256"], "after": actual})
        pin["sha256"] = actual
pinned = {pin["path"] for pin in doc["pins"]}
for path, why in checker.CONSUMED_SOURCES:
    if path not in pinned:
        sha = hashlib.sha256((root / path).read_bytes()).hexdigest()
        doc["pins"].append({"path": path, "sha256": sha, "consumedFor": why})
        delta.append({"path": path, "change": "added", "before": None, "after": sha})
pins_path.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
out.write_text(json.dumps({"scratchRoot": str(root), "ledger": "docs/coop/design-corrections/native/source-pins.v2.json",
                           "entries": len(doc["pins"]), "delta": delta}, indent=1) + "\n", encoding="utf-8")
print(json.dumps({"entries": len(doc["pins"]), "changed": len(delta)}, indent=1))
