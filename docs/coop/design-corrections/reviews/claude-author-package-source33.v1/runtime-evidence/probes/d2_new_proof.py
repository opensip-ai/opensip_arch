"""Confirm the reminted TS proof carries the source33 carrier law, and compare old vs new."""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
F = SRC / "docs/coop/design-corrections/foundation"
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")
NEW = HERE / "remint" / "checkpoint3" / "checkpoint3"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("d2_identity", F / "identity-model.v3.py")
R = load("d2_replay", F / "evaluator_replay_model.v3.py")
E = load("d2_composition", F / "evaluator_composition_model.v3.py")
T = load("d2_transport", V10 / "check-export.v4.py")


def proof_of(store_path, claims_path):
    raw = Path(store_path).read_bytes()
    objects, blobs = T.decode_store(raw, M)
    rid = json.loads(Path(claims_path).read_text())[0]["runId"]
    run = objects[rid][1]
    seal = objects[run["evaluationSealId"]][1]
    return rid, objects, blobs, run, seal, objects[seal["proofBundleId"]][1]


out = {"standing": "Old source30 construction vs new source33 remint of the TS Run."}

old_rid, *_rest, old_proof = proof_of(V9 / "checkpoint3" / "ts.store.json",
                                      V9 / "checkpoint3" / "claims.json")
new_rid, objects, blobs, run, seal, new_proof = proof_of(NEW / "ts.store.json",
                                                         NEW / "claims.json")
out["oldRunId"], out["newRunId"] = old_rid, new_rid
out["runIdChanged"] = old_rid != new_rid
out["oldExecutionDeficiencies"] = old_proof["executionDeficiencies"]
out["newExecutionDeficiencies"] = new_proof["executionDeficiencies"]
out["oldVerdict"], out["newVerdict"] = old_proof["verdict"], new_proof["verdict"]
out["proofFieldsDifferingOldVsNew"] = sorted(
    k for k in set(old_proof) | set(new_proof) if old_proof.get(k) != new_proof.get(k))

# The owner's own derivation of the NEW export must equal the retained new proof.
rid, owner = M.open_run_closure(run, objects, blobs)
derived = R.derive(run["planId"], seal["executionPlanId"], seal["evaluatorClosure"],
                   new_proof["evaluationInputRefs"], objects, blobs, owner)
out["ownerDerivedEqualsRetained"] = derived["proof"] == new_proof
out["ownerDerivedProofBundleIdEqualsSeal"] = derived["proofBundleId"] == seal["proofBundleId"]
try:
    E.compare_complete_replay(new_proof, derived, objects, blobs)
    out["compareCompleteReplay"] = "ADMIT"
except Exception as exc:  # noqa: BLE001
    out["compareCompleteReplay"] = f"{type(exc).__name__}: {exc}"

# Which retained Coverage records back each new proof item.
out["carrierLawWitness"] = {
    "itemCount": len(new_proof["executionDeficiencies"]),
    "items": [
        {"cause": d["cause"], "nativeCause": d["nativeCause"],
         "coverageRefs": [r["digest"] for r in d["inputRefs"] if r["domain"] == "coverage"]}
        for d in new_proof["executionDeficiencies"]
    ],
}
for item in out["carrierLawWitness"]["items"]:
    for digest in item["coverageRefs"]:
        env = objects.get("coverage2:" + digest)
        if env is None:
            item["retainedEntry"] = "coverage envelope not retained under that identity"
            continue
        payload = json.loads(blobs[env[1]["payloadDigest"]])
        entry = payload.get("entry") or {}
        item["retainedEntry"] = {"coverage": entry.get("coverage"),
                                 "deficiency": entry.get("deficiency"),
                                 "nativeCause": entry.get("nativeCause")}

print(json.dumps(out, indent=2, default=str))
