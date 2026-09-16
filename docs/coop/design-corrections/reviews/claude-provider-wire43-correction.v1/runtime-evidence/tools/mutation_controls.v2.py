"""Mutation controls, second run. Receipt 32 (mutation_controls.py) is kept as recorded: two of its six
mutations were NOT applied because their `old` strings were constructed with the wrong indentation
(one matched twice, one matched nothing). This run corrects those two constructors and repeats all six.

usage: mutation_controls.v2.py <scratch-candidate-root> <json-out>
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
HS = NATIVE / "provider-handshake.schemas.v1.json"

MUTATIONS = [
    # corrected: include the TypeScript map's closing brace so only the TypeScript member matches
    ("ts-limits-rename-maxStderrBytes", HS,
     '"maxStderrBytes": {\n          "const": 262144\n        }\n      },',
     '"maxStderrBytesRenamed": {\n          "const": 262144\n        }\n      },',
     "TypeScriptProtocolLimitsV1"),
    # corrected: required-array members are indented eight spaces
    ("rust-hello-drops-contract-digest", HS,
     '"hostBuildId",\n        "expectedProtocolContractSha256",\n        "expectedIdentity",',
     '"hostBuildId",\n        "expectedIdentity",',
     "HelloV3 drops inherited members"),
    ("section-9.3-limit-value-drift", CONTRACT, "`maxCfgSets 4`", "`maxCfgSets 5`", "ProtocolLimitsV3"),
    ("ts-ack-field-unbound-from-descriptor", HS,
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
    delta = RUNTIME / "receipts" / f"34-mutation-{tag}-repin.json"
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
out.write_text(json.dumps({"root": str(root), "supersedesRunRecord": "receipts/32-mutation-controls-results.json (kept)",
                           "mutations": results}, indent=1) + "\n", encoding="utf-8")
for r in results:
    print(r["mutation"], "applied" if r.get("applied") else "NOT-APPLIED", "exit", r.get("exitCode"), "detected", r.get("detected"))
