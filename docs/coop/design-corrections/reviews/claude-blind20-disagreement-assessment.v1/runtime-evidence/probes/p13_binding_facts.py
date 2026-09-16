"""RC-3: does the consumer's OWN retained EnumerationPlan contain bindings for that capability?

`missing-relation-coverage` is emitted only when there are NO bindings at all; `selector-unbound`
when bindings exist but none at the subject's universe. This settles which is factually right on
the consumer's own retained plan. READ-ONLY.
"""
import importlib.util
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
S = B / "candidate-subject.v33"
F = S / "docs/coop/design-corrections/foundation"
IN = B / "root-blind20-final33-replay.v1"


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


T = load("t13", B / "check-blind-successor33-export.v1.py")
R = load("r13", F / "evaluator_replay_model.v3.py")
M = R.M
I = load("i13", F / "evaluator_input_model.v3.py")
A = load("a13", F / "atom_model.v1.py")

out = {"standing": "READ-ONLY binding-availability fact check on the consumer's own retained plan."}
REL_BY_RUN = {"syntax-code": "unresolved-edge", "rust": "clones", "typescript": "clones"}

for n, rel in REL_BY_RUN.items():
    raw = (IN / "captured" / (n + ".store.json")).read_bytes()
    o, b, _ = T.decode(raw, M)
    rid = T.parse(raw)["claim"]["runId"]
    run = o[rid][1]
    _, owner = M.open_run_closure(run, o, b)
    seal = o[run["evaluationSealId"]][1]
    cproof = o[seal["proofBundleId"]][1]
    _, atom_inputs = I.reconstruct(run["planId"], seal["executionPlanId"],
                                   seal["evaluatorClosure"],
                                   cproof["evaluationInputRefs"], o, b, owner, M)
    plan = atom_inputs.get("enumerationPlan") or {"cells": []}
    cap = A.REGISTRY["capabilityForRelation"].get(rel)
    avail, unavail = A._owed_source_bindings(rel, atom_inputs)
    cells = [{"capabilityId": c.get("capabilityId"), "languageMode": c.get("languageMode"),
              "bindingCount": len(c.get("programBindings") or []),
              "universes": [bb.get("universe") for bb in (c.get("programBindings") or [])]}
             for c in plan.get("cells") or []]
    out[n] = {
        "runId": rid, "relation": rel, "capabilityForRelation": cap,
        "enumerationPlanCells": cells,
        "cellsMatchingThatCapability": [c for c in cells if c["capabilityId"] == cap],
        "availableBindingCount": len(avail), "unavailableBindingCount": len(unavail),
        "anyBindingAtAllForCapability": bool(avail or unavail),
        "referenceWouldEmitMissingRelationCoverage": not avail and not unavail,
        "note": "missing-relation-coverage requires NO bindings at all for the capability; "
                "selector-unbound requires bindings that do not include the subject's universe.",
    }
print(json.dumps(out, indent=2, default=str))
