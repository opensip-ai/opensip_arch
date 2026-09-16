"""Did the consumer's own export contain everything the published pairing law needs?

If the reference finds containing scopes using only records the CONSUMER itself exported, the
disagreement is in the consumer's algorithm, not in missing evidence. READ-ONLY.
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


T = load("t8", B / "check-blind-successor33-export.v1.py")
R = load("r8", F / "evaluator_replay_model.v3.py")
M = R.M
I = load("i8", F / "evaluator_input_model.v3.py")
A = load("a8", F / "atom_model.v1.py")
N = load("n8", S / "docs/coop/design-corrections/native/native_evidence_model.v2.py")

out = {"standing": "READ-ONLY check that the pairing inputs were present in the consumer export."}

for n in ["typescript", "rust", "syntax-code"]:
    raw = (IN / "captured" / (n + ".store.json")).read_bytes()
    o, b, _ = T.decode(raw, M)
    rid = T.parse(raw)["claim"]["runId"]
    run = o[rid][1]
    _, owner = M.open_run_closure(run, o, b)
    seal = o[run["evaluationSealId"]][1]
    cproof = o[seal["proofBundleId"]][1]
    normalized, atom_inputs = I.reconstruct(run["planId"], seal["executionPlanId"],
                                            seal["evaluatorClosure"],
                                            cproof["evaluationInputRefs"], o, b, owner, M)
    # Everything the pairing law reads.
    scopes = atom_inputs.get("scopes") or {}
    covs = atom_inputs.get("coverages") or {}
    cov_scopes = atom_inputs.get("coverageScopes") or {}
    # Are those scope descriptors present in the CONSUMER's own object table?
    scope_in_export = {sid: (sid in o) for sid in scopes}
    # Exercise the published commitment pairing on the reference's own helper.
    commitments = {}
    for sid, sc in scopes.items():
        try:
            commitments[sid] = json.dumps(N.subject_scope_commitment(sc), sort_keys=True)
        except Exception as exc:  # noqa: BLE001
            commitments[sid] = "ERROR:" + type(exc).__name__
    matched = 0
    for cid, cov in covs.items():
        want = (cov.get("key") or {}).get("subjectScopeCommitment")
        vals = set()
        for v in commitments.values():
            if isinstance(v, str) and not v.startswith("ERROR:"):
                try:
                    j = json.loads(v)
                except Exception:
                    continue
                vals.add(j if isinstance(j, str) else json.dumps(j, sort_keys=True))
        probe = want if isinstance(want, str) else json.dumps(want, sort_keys=True)
        if probe in vals:
            matched += 1
    out[n] = {
        "runId": rid,
        "scopeCount": len(scopes), "coverageCount": len(covs),
        "coverageScopesMappingPresent": bool(cov_scopes), "coverageScopesSize": len(cov_scopes),
        "everyScopeDescriptorInConsumerExport": all(scope_in_export.values()),
        "scopeDescriptorsMissingFromExport":
            sorted(s for s, ok in scope_in_export.items() if not ok),
        "commitmentsComputable": sum(1 for v in commitments.values()
                                     if isinstance(v, str) and not v.startswith("ERROR:")),
        "commitmentErrors": sorted({v for v in commitments.values()
                                    if isinstance(v, str) and v.startswith("ERROR:")}),
        "coveragesWhoseCommitmentMatchesARetainedScope": matched,
        "coveragesTotal": len(covs),
        "everyCoverageCommitmentResolves": matched == len(covs),
        "enumerationPlanCellCount": len((atom_inputs.get("enumerationPlan") or {}).get("cells") or []),
        "inventoryCount": len(atom_inputs.get("inventories") or []),
    }
print(json.dumps(out, indent=2, default=str))
