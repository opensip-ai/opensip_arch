"""Q2 — root's nine dependency-scope mutations at the NATIVE PRODUCER boundary, frozen35 only.

For each mutation, the baseline calls Coverage payload is judged against the mutated scope by
`native_evidence_model.v2.admit_coverage_result_v3`, which is what `identity-model.v3` close_run re-runs
for every retained Coverage over its retained scope descriptor. Also re-measures root's direct carrier.

STANDING: native producer admission of one Coverage + one scope descriptor. NOT closed enumeration
admission, NOT a closed Run, NOT a retained Run. Read-level closure joins are cited separately in the review.
"""
import copy
import importlib.util
import json
import sys
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/candidate-subject.v35/docs/coop/design-corrections/foundation")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load("check_atoms_q2", F / "check-atoms.v1.py")
AM = K.AM
N = AM.N
sid, scope = K.scope("calls", "resolved-callee", K.U1, K.U1, [K.F_SYM], sid="2")
cid, cov = K.coverage("calls", "resolved-callee", K.U1, K.U1, cid="2")
desc = AM._scope_descriptor(scope)
cov = copy.deepcopy(cov)
commit = N.subject_scope_commitment(copy.deepcopy(desc))
cov["key"]["subjectScopeCommitment"] = commit["subjectScopeCommitment"]
cov["entry"]["examinedUniverse"] = {"subjectScopeCommitment": commit["subjectScopeCommitment"],
                                    "subjectCount": commit["subjectCount"]}


def producer(d):
    try:
        out = N.admit_coverage_result_v3(copy.deepcopy(cov), copy.deepcopy(d), [])
        return {"result": out["result"], "refusals": out["refusals"], "faults": out["faults"]}
    except Exception as exc:  # noqa: BLE001 - owner raises for carrier-invalid descriptors
        return {"result": "RAISE", "error": f"{type(exc).__name__}: {str(exc)[:160]}"}


def carrier(d):
    try:
        N.subject_scope_commitment(copy.deepcopy(d))
        return "ADMIT"
    except Exception as exc:  # noqa: BLE001
        return f"REFUSE {type(exc).__name__}"


rows = {"baseline": {"carrier": carrier(desc), "producer": producer(desc)}}
for field, other in (("sourceUniverse", K.U2), ("relation", "references"),
                     ("resolution", "resolved-binding"), ("resolution", "syntactic-callee-name")):
    for mode in ("absent", "null", "different"):
        if mode != "different" and other not in (K.U2, "references", "resolved-binding"):
            continue
        d = copy.deepcopy(desc)
        if mode == "absent":
            d.pop(field)
        else:
            d[field] = None if mode == "null" else other
        label = f"{field}/{mode}" + (f"={other}" if mode == "different" else "")
        rows[label] = {"carrier": carrier(d), "producer": producer(d)}
print(json.dumps({"standing": "native producer admission (admit_coverage_result_v3) + direct carrier, frozen35; "
                               "not closed enumeration, not a Run",
                  "rows": rows}, indent=1))
