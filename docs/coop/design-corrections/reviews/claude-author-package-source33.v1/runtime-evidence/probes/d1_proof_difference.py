"""Diagnose the EXACT proof difference that makes the TS positive export refuse on source33.

READ ONLY on the frozen source and on package v9. Writes only into this runtime.
Replays the retained export through the frozen owner exactly as check-export.v4.py does, then
compares the RETAINED proof bundle to what source33's composition now derives, field by field.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
F = SRC / "docs/coop/design-corrections/foundation"
PKG = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("d1_identity", F / "identity-model.v3.py")
R = load("d1_replay", F / "evaluator_replay_model.v3.py")
E = load("d1_composition", F / "evaluator_composition_model.v3.py")
T = load("d1_transport", PKG / "check-export.v4.py")

out = {"standing": "READ-ONLY diagnosis of the retained TS export against frozen source33."}

raw = (PKG / "checkpoint3" / "ts.store.json").read_bytes()
notes = []
objects, blobs = T.decode_store(raw, M, transport_notes=notes)
claims = json.loads((PKG / "checkpoint3" / "claims.json").read_text())
run_id = claims[0]["runId"]
out["claimedRunId"] = run_id
out["transportNoteCount"] = len(notes)

run = objects[run_id][1]
seal = objects[run["evaluationSealId"]][1]
retained_proof = objects[seal["proofBundleId"]][1]
out["retainedProofBundleId"] = seal["proofBundleId"]

# Structural owner first, exactly as the transport check does.
try:
    rid, owner = M.open_run_closure(run, objects, blobs)
    out["ownerAdmission"] = "ADMIT"
except Exception as exc:  # noqa: BLE001
    out["ownerAdmission"] = "REFUSE"
    out["ownerReason"] = f"{type(exc).__name__}: {exc}"
    print(json.dumps(out, indent=2, default=str))
    sys.exit(0)

# Re-derive with source33 composition.
try:
    derived = R.derive(run["planId"], seal["executionPlanId"], seal["evaluatorClosure"],
                       retained_proof["evaluationInputRefs"], objects, blobs, owner)
    out["deriveOk"] = True
except Exception as exc:  # noqa: BLE001
    out["deriveOk"] = False
    out["deriveReason"] = f"{type(exc).__name__}: {exc}"
    print(json.dumps(out, indent=2, default=str))
    sys.exit(0)

new_proof = derived["proof"]
out["derivedProofBundleId"] = derived.get("proofBundleId")
out["proofIdsEqual"] = derived.get("proofBundleId") == seal["proofBundleId"]

# Field-by-field difference of the two proof bundles.
diffs = {}
for key in sorted(set(retained_proof) | set(new_proof)):
    a, b = retained_proof.get(key), new_proof.get(key)
    if a != b:
        diffs[key] = {"retained": a, "derived": b}
out["proofFieldDifferences"] = diffs
out["differingFieldNames"] = sorted(diffs)

# What the owner's own comparator says.
try:
    E.compare_complete_replay(retained_proof, derived, objects, blobs)
    out["compareCompleteReplay"] = "ADMIT"
except Exception as exc:  # noqa: BLE001
    out["compareCompleteReplay"] = f"{type(exc).__name__}: {exc}"

print(json.dumps(out, indent=2, default=str))
