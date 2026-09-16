"""Byte custody for this diagnosis: frozen33 against its manifest, and every input I read."""
import hashlib
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
MAN = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
           "candidate-subject.v33.json")
ROOT = B / "candidate-subject.v33"
EXPECT = "1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


raw = MAN.read_bytes()
man = json.loads(raw)
bad, missing, total = [], [], 0
seen = set()
for row in man["files"]:
    rel = row["path"]
    seen.add(rel)
    t = ROOT / rel
    if not t.is_file():
        missing.append(rel)
        continue
    data = t.read_bytes()
    total += len(data)
    if hashlib.sha256(data).hexdigest() != row["sha256"]:
        bad.append(rel)
on_disk = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and not p.is_symlink()}

out = {
    "standing": "READ-ONLY byte custody for this diagnosis. Not acceptance.",
    "manifestPath": str(MAN), "manifestSha256": hashlib.sha256(raw).hexdigest(),
    "manifestMatchesDeclared": hashlib.sha256(raw).hexdigest() == EXPECT,
    "declaredFileCount": man.get("fileCount"), "declaredTotalBytes": man.get("totalBytes"),
    "verifiedFileCount": len(seen) - len(missing), "verifiedTotalBytes": total,
    "mismatched": bad, "missing": missing, "extraOnDisk": sorted(on_disk - seen),
    "allFrozenBytesVerified": not bad and not missing and not (on_disk - seen)
    and len(seen) == man.get("fileCount") and total == man.get("totalBytes"),
}

inputs = {}
for label, p in [
    ("root.replay.summary", B / "root-blind20-final33-replay.v1/summary.json"),
    ("root.proofDiff.report", B / "root-blind20-proof-differences33.v1/report.json"),
    ("root.proofDiff.diagnose", B / "root-blind20-proof-differences33.v1/diagnose.py"),
    ("root.envelope.report", B / "root-blind20-envelope-schemas.v1/report.json"),
    ("root.token33.assessment", B / "root-blind19-protocol-token33.v1/assessment.json"),
    ("transport", B / "check-blind-successor33-export.v1.py"),
    ("source.atom_model", ROOT / "docs/coop/design-corrections/foundation/atom_model.v1.py"),
    ("source.atom_contract",
     ROOT / "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md"),
    ("source.composition_model",
     ROOT / "docs/coop/design-corrections/foundation/evaluator_composition_model.v3.py"),
    ("source.composition_contract",
     ROOT / "docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md"),
    ("source.replay_model",
     ROOT / "docs/coop/design-corrections/foundation/evaluator_replay_model.v3.py"),
    ("source.native_model",
     ROOT / "docs/coop/design-corrections/native/native_evidence_model.v2.py"),
    ("source.native_contract", ROOT / "docs/v2/contracts/product-v1/native-evidence.md"),
    ("consumer20.phase3_traces", B / "consumer-b.v20/output/lib/phase3_traces.py"),
    ("consumer20.mutation-keys", B / "consumer-b.v20/output/vectors/mutation-keys.json"),
    ("consumer20.indep-mutation-surface",
     B / "consumer-b.v20/output/vectors/indep-mutation-surface.json"),
    ("consumer20.traces.complete", B / "consumer-b.v20/output/traces/complete.json"),
]:
    inputs[label] = {"path": str(p), "sha256": sha(p) if p.is_file() else None,
                     "present": p.is_file()}
for n in ["syntax-code", "typescript", "rust", "rust-partial", "syntax-data"]:
    p = B / "root-blind20-final33-replay.v1/captured" / (n + ".store.json")
    inputs["capturedExport." + n] = {"path": str(p), "sha256": sha(p), "present": True}
out["inputHashes"] = inputs

manifest_pub = B / "consumer-b.v20/final-public-artifact-manifest.json"
out["consumer20PublicManifest"] = {
    "path": str(manifest_pub), "present": manifest_pub.is_file(),
    "sha256": sha(manifest_pub) if manifest_pub.is_file() else None,
}
print(json.dumps(out, indent=2, default=str))
