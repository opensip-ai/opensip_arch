"""Startup mutation controls: each deliberate defect must make the corrected native checker FAIL.

usage: mutation_controls_startup.py <scratch-candidate-root> <json-out>
Runs only inside this runtime's scratch-* copies; restores every byte and refreshes scratch pins after each run.
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
SM = NATIVE / "provider_startup_model.v1.py"
MUTATIONS = [
    ("ts-order-drops-native-context-insertion", NATIVE / "typescript-protocol2-order.v1.json",
     '"frame": "SnapshotAccepted",\n      "next": "WAIT_NATIVE_CONTEXT_VERIFIED",',
     '"frame": "SnapshotAccepted",\n      "next": "READY_ANALYZE",',
     "typescript order table does not carry the section 9.7 insertions"),
    ("section-9.4-reason-prose-drift", CONTRACT,
     "`identity-version-mismatch`, `node-modules-outside-read-set`.\n",
     "`identity-version-mismatch`.\n",
     "typescript post-Analyze reasons"),
    ("p3-derived-observation-renamed", NATIVE / "protocol3-transitions.v1.json",
     '  "preparedMode": "repositoryResolution.preparedOutputSetId',
     '  "preparedModeRenamed": "repositoryResolution.preparedOutputSetId',
     "derivedObservations must name exactly"),
    ("startup-model-skips-universe-key", SM,
     'if payload["universeKey"] != universe_identity(language, universe):',
     'if False:',
     "startup-ts2-open-universe-v1-universe-key-refused"),
    ("startup-model-admits-pre-analyze-payload-after-analyze", SM,
     "    if phase == PRE_ANALYZE_PHASE:",
     "    if phase in (PRE_ANALYZE_PHASE, POST_ANALYZE_PHASE):",
     "startup-ts2-pre-analyze-payload-after-analyze-refused"),
    ("startup-model-derives-dependency-mode-false", SM,
     'event.update({"dependencyMode": True,',
     'event.update({"dependencyMode": False,',
     "startup-rust3-empty-dependency-set-custody-then-complete"),
    ("startup-model-skips-cancel-interval-law", SM,
     'if cancel_phase in rule["hostPhasesAtCancel"] and observed != rule["observedPhase"]:',
     'if False:',
     "startup-ts2-cancel-in-native-context-interval-observing-analysis-refused"),
    ("exchange-catches-only-the-native-admission-error", NATIVE / "native_evidence_model.v2.py",
     "except (AdmissionError, STARTUP.C.AdmissionError, WIRE.C.AdmissionError) as exc:",
     "except AdmissionError as exc:",
     "startup-ts2-open-universe-plan1-plan-id-refused"),
    ("conversion-takes-no-planned-stage", NATIVE / "native_evidence_model.v2.py",
     '    for stage in planned_stages:\n        admissions = []',
     '    for stage in planned_stages[:0]:\n        admissions = []',
     "startup-ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage"),
]


def repin(tag):
    delta = RUNTIME / "receipts" / f"42-mutation-{tag}-repin.json"
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
