"""Follow-up wording edit: keep the section 9.4 order sentence from silently choosing a Coverage frame name.

usage: apply_followup_edit.py <candidate-root>   (run for the work copy and the scratch-after copy)
"""
import hashlib
import sys
from pathlib import Path

path = Path(sys.argv[1]) / "docs" / "v2" / "contracts" / "product-v1" / "native-evidence.md"
old = ("**Order to Analyze.** The major-2 normal order is Hello/HelloAck,\n"
       "OpenUniverse/UniverseAccepted, SnapshotManifest/SnapshotFileChunk*/SnapshotSeal/\n"
       "SnapshotAccepted, `NativeContextVerified`, Analyze, per-stage FactBatch*/Coverage,\n"
       "Complete, zero-exit/EOF; `NativeContextVerified` is a worker→host frame with the\n"
       "§9.2 payload (§0).")
new = ("**Normal order.** The major-2 normal order is Hello/HelloAck,\n"
       "OpenUniverse/UniverseAccepted, SnapshotManifest/SnapshotFileChunk*/SnapshotSeal/\n"
       "SnapshotAccepted, `NativeContextVerified`, Analyze, then the inherited per-stage\n"
       "FactBatch*/Coverage sequence, Complete, zero-exit/EOF; `NativeContextVerified` is a\n"
       "worker→host frame with the §9.2 payload (§0). This sentence changes no Coverage frame\n"
       "selector: §9.2 names only the `rust-semantic` frame `CoverageV3`.")
text = path.read_text(encoding="utf-8")
if text.count(old) != 1:
    raise SystemExit(f"expected one occurrence, found {text.count(old)}")
before = hashlib.sha256(text.encode("utf-8")).hexdigest()
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print(path, before, hashlib.sha256(text.encode("utf-8")).hexdigest())
