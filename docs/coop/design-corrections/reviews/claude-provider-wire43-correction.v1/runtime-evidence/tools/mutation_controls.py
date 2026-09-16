"""Mutation controls: each deliberate defect must make the corrected native checker FAIL.

usage: mutation_controls.py <scratch-candidate-root> <json-out>

Runs only inside this runtime's scratch-* copies. For each mutation: apply one exact replacement,
refresh scratch pins, run the checker, record exit and FAIL lines, restore the original bytes and
refresh pins again. Expected failures are the point and are kept verbatim.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
PY = "/tmp/opensip-architecture-review-env/bin/python"
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
if not str(root).startswith(str(RUNTIME / "scratch-")):
    raise SystemExit("refusing: not a scratch root")
NATIVE = root / "docs" / "coop" / "design-corrections" / "native"
CONTRACT = root / "docs" / "v2" / "contracts" / "product-v1" / "native-evidence.md"

MUTATIONS = [
    ("ts-limits-drop-maxStderrBytes", NATIVE / "provider-handshake.schemas.v1.json",
     '"maxStderrBytes": {\n          "const": 262144\n        }', '"maxStderrBytesRenamed": {\n          "const": 262144\n        }',
     "TypeScriptProtocolLimitsV1"),
    ("rust-hello-drops-contract-digest", NATIVE / "provider-handshake.schemas.v1.json",
     '"hostBuildId",\n          "expectedProtocolContractSha256",\n          "expectedIdentity",',
     '"hostBuildId",\n          "expectedIdentity",',
     "HelloV3 drops inherited members"),
    ("section-9.3-limit-value-drift", CONTRACT,
     "`maxCfgSets 4`", "`maxCfgSets 5`", "ProtocolLimitsV3"),
    ("ts-ack-field-unbound-from-descriptor", NATIVE / "provider-handshake.schemas.v1.json",
     '"runtimeDescriptorFields": [\n        "nodeVersion",', '"runtimeDescriptorFields": [',
     "bound to no descriptor or echo"),
    ("wire-model-skips-batch-commitment", NATIVE / "provider_wire_model.v1.py",
     'if batch["batchCommitment"] != commitment:', 'if False and batch["batchCommitment"] != commitment:',
     "provider-wire-ts-fact-batch-v1-wrong-batch-commitment-refused"),
    ("wire-model-skips-rust-identity-echo", NATIVE / "provider_wire_model.v1.py",
     'if not C.equal_typed(ack[field], identity[field]):', 'if False:',
     "provider-wire-rust3-hello-ack-changed-identity-echo-refused"),
]


def repin(tag):
    delta = RUNTIME / "receipts" / f"32-mutation-{tag}-repin.json"
    if delta.exists():
        raise SystemExit("exists " + str(delta))
    subprocess.run([PY, "-I", "-B", str(RUNTIME / "tools" / "scratch_repin.py"), str(root), str(delta)],
                   check=True, capture_output=True, text=True)


results = []
for mid, path, old, new, expect in MUTATIONS:
    original = path.read_bytes()
    text = original.decode("utf-8")
    if text.count(old) != 1:
        results.append({"mutation": mid, "applied": False, "reason": f"old occurs {text.count(old)} times"})
        continue
    try:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        repin(mid + "-apply")
        proc = subprocess.run([PY, "-I", "-B", "check_native_evidence.v2.py"], cwd=NATIVE, capture_output=True, text=True)
        fail_lines = [line for line in proc.stdout.splitlines() if line.startswith("FAIL")]
        results.append({"mutation": mid, "file": str(path.relative_to(root)), "applied": True, "exitCode": proc.returncode,
                        "expectedEvidence": expect, "detected": proc.returncode != 0 and any(expect in l for l in fail_lines),
                        "failLines": fail_lines[:40], "stderrTail": proc.stderr[-2000:]})
    finally:
        path.write_bytes(original)
        repin(mid + "-restore")
    assert hashlib.sha256(path.read_bytes()).hexdigest() == hashlib.sha256(original).hexdigest()
out.write_text(json.dumps({"root": str(root), "mutations": results}, indent=1) + "\n", encoding="utf-8")
for r in results:
    print(r["mutation"], "applied" if r.get("applied") else "NOT-APPLIED", "exit", r.get("exitCode"), "detected", r.get("detected"))
