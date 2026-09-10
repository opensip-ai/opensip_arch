"""Measured tests of the candidate design gaps found during reconstruction.

Each case is CONSTRUCTED and RUN; the reported result is what my independent
closure actually observed, not a label.
"""
import copy
import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import osip
import run_ts
import run_ts_config
import schemas
from osip import C, record_digest

FINDINGS = []


def report(idc, title, observed, expected_if_closed, severity, detail):
    FINDINGS.append({"id": idc, "title": title, "observedResult": observed,
                     "whatAClosedContractWouldHaveDone": expected_if_closed,
                     "severity": severity, "detail": detail})
    print("%-12s %-9s %s" % (idc, severity, title))
    print("             observed: %s" % observed)


# ===========================================================================
# G1. TWO analysis-spec parameter rows citing the SAME registered document
# ===========================================================================
SCOPE_A = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": []}
SCOPE_B = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": ["src/**"], "exclude": ["src/generated/**"]}
p_a = {"schemaDigest": CL.POLICY_DOC_DIGEST, "payloadDigest": record_digest(SCOPE_A)}
p_b = {"schemaDigest": CL.POLICY_DOC_DIGEST, "payloadDigest": record_digest(SCOPE_B)}
fx, A, run_id = run_ts_config.build_run("custom-multibase",
                                        spec_parameters=[p_a, p_b], seed="two-scope")
fx.s.put_record(SCOPE_A)
fx.s.put_record(SCOPE_B)
rep = CL.Closure(fx.s).close_run(run_id)
report("CB-GAP-1",
       "the `parameter` payload class is keyed by the cited DOCUMENT digest, so "
       "a Plan may select TWO ScopeDocumentV1 parameters and nothing decides "
       "which one is the Plan's scope policy",
       "the Run CLOSES with %d checks and no fault; both rows validate under the "
       "one registered selector and the existential verifier "
       "(`the payloadDigest of A selected parameter row citing the registered "
       "ScopeDocumentV1 document digest`) is satisfied by EITHER"
       % rep["checks"] if rep["ok"] else "refused: " + str(rep["faults"][:1]),
       "either a stated cardinality bound (as identity section 3 already gives "
       "the ImportSourceContextV1 row: `No parameter means an empty set; more "
       "than one is refused`) or a published selection rule",
       "MUST",
       {"runId": run_id, "closureOk": rep["ok"], "checks": rep["checks"],
        "parameterRows": [p_a, p_b],
        "scopeDocumentADigest": record_digest(SCOPE_A),
        "scopeDocumentBDigest": record_digest(SCOPE_B),
        "consequence": "ComparisonDescriptor.baselineContext/currentContext "
                       "scopeDigest is the E2->E3 comparison axis. Two conforming "
                       "hosts can bind different scope documents from ONE admitted "
                       "Plan, so the scope axis attributes differently for one "
                       "PlanId. identity section 3 reasons explicitly about the "
                       "analogous REGISTRY-key ambiguity and refuses it "
                       "(PAYLOAD_PARAMETER_AMBIGUOUS_ROW); the SPEC-row case is "
                       "the same ambiguity one level down and is unstated.",
        "notMitigatedBy": "analysis-spec.parameters uniqueItems - the two rows "
                          "are distinct items because their payloadDigests differ; "
                          "and x-opensip-order canonical-set, which orders them "
                          "rather than refusing them."})

# ===========================================================================
# G2. two requestedCapabilities rows for one (capability, mode, root)
# ===========================================================================
rows = [{"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": False}]
spec = {"schemaVersion": 2, "requestedCapabilities": sorted(rows, key=lambda r: C(r)),
        "policyPackIds": [], "parameters": []}
errs = schemas.validate(spec, "identity", "#/$defs/analysis-spec")
import workflow as W
admit = W.admit_requested_capabilities(spec["requestedCapabilities"])
report("CB-GAP-2",
       "an analysis-spec may carry TWO requestedCapabilities rows for the same "
       "(capabilityId, languageMode, workspaceRoot) differing only in `required`",
       "schema validation: %s; capability admission: %s"
       % ("admits" if not errs else errs[:1], admit or "admits"),
       "native section 1.4 refuses a duplicate capabilityId in the RELEASE "
       "declaration for exactly this reason (`two rows ... would leave default "
       "selection ambiguous`); the analysis-spec has no analogous uniqueness rule "
       "on the (capability, mode, workspaceRoot) key",
       "SHOULD",
       {"spec": spec, "schemaErrors": errs, "capabilityAdmission": admit,
        "consequence": "requiredness decides whether a missing Coverage entry "
                       "contributes indeterminate. Two contradictory rows for one "
                       "cell make that undetermined, and both rows enter "
                       "analysisSpecDigest and therefore PlanId, so the "
                       "contradiction is COMMITTED.",
        "notMitigatedBy": "uniqueItems - the two rows differ in `required`."})

# ===========================================================================
# G3. coverage vs examinedExhaustive: one claim, two committed encodings,
#     no published join
# ===========================================================================
fx, A, run_id = run_ts.build_run()
c = CL.Closure(fx.s)
rep0 = c.close_run(run_id)
assert rep0["ok"]


def contradictory_entry(fx, A, run_id):
    """coverage: complete AND examinedExhaustive: false on one entry."""
    for h, blob in list(fx.s.blobs.items()):
        if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
            continue
        dom, val = osip.parse_frame(blob)
        if dom != "coverage":
            continue
        payload, _ = osip.admit_raw(fx.s.get(val["payloadDigest"]))
        if payload["entry"]["relation"] != "file":
            continue
        p2 = copy.deepcopy(payload)
        p2["entry"]["resolutionCompleteness"]["examinedExhaustive"] = False
        assert p2["entry"]["coverage"] == "complete"
        pd = fx.s.put_record(p2)
        v2 = dict(val); v2["payloadDigest"] = pd
        h2 = fx.s.put_h("coverage", v2)
        return h, "coverage2:" + h2, p2
    raise AssertionError


old_h, new_cov, p2 = contradictory_entry(fx, A, run_id)
# rebuild the view/evidence/seal/run around the replacement Coverage
def rekey(fx, A, run_id, old_h, new_cov):
    seal = osip.parse_frame(fx.s.blobs[A.run["evaluationSealId"].split(":")[1]])[1]
    ev = osip.parse_frame(fx.s.blobs[seal["evidenceId"].split(":")[1]])[1]
    proof = osip.parse_frame(fx.s.blobs[seal["proofBundleId"].split(":")[1]])[1]
    old_cov = "coverage2:" + old_h
    view = osip.parse_frame(fx.s.blobs[ev["viewIds"][0].split(":")[1]])[1]
    view = dict(view)
    view["coverageIds"] = sorted([c for c in view["coverageIds"] if c != old_cov]
                                 + [new_cov], key=lambda x: C(x))
    vh = fx.s.put_h("view", view)
    covs = sorted([c for c in ev["coverageIds"] if c != old_cov] + [new_cov],
                  key=lambda x: C(x))
    proof = copy.deepcopy(proof)
    proof["evaluationInputRefs"] = sorted(
        [r for r in proof["evaluationInputRefs"]
         if r["digest"] not in (old_h, ev["viewIds"][0].split(":")[1])]
        + [{"domain": "coverage", "digest": new_cov.split(":")[1]},
           {"domain": "view", "digest": vh}], key=lambda r: C(r))
    w, _ = osip.admit_raw(fx.s.get(proof["predicateProofs"][0]["witnessDigest"]))
    w = dict(w); w["coverageIds"] = covs
    nwd = fx.s.put_record(w)
    pp = dict(proof["predicateProofs"][0])
    pp["witnessDigest"] = nwd
    pp["inputRefs"] = proof["evaluationInputRefs"]
    proof["predicateProofs"] = [pp]
    ph = fx.s.put_h("proof-bundle", proof)
    ev = dict(ev); ev["viewIds"] = ["view2:" + vh]; ev["coverageIds"] = covs
    ev["proofBundleId"] = "proof2:" + ph
    eh = fx.s.put_h("semantic-evidence", ev)
    seal = dict(seal); seal["evidenceId"] = "evidence2:" + eh
    seal["proofBundleId"] = "proof2:" + ph
    sh = fx.s.put_h("evaluation-seal", seal)
    run = dict(A.run); run["evidenceId"] = "evidence2:" + eh
    run["evaluationSealId"] = "seal2:" + sh
    return "run2:" + fx.s.put_h("run", run)


new_run = rekey(fx, A, run_id, old_h, new_cov)
rep = CL.Closure(fx.s).close_run(new_run)
report("CB-GAP-3",
       "`coverage` and `resolutionCompleteness.examinedExhaustive` are TWO "
       "committed encodings of ONE claim (section 4.1 claim 1) with no published "
       "join, so a sealed entry can assert `complete` and `examinedExhaustive: "
       "false` at once",
       ("the Run CLOSES with %d checks and no fault" % rep["checks"]) if rep["ok"]
       else "refused: " + str(rep["faults"][:1]),
       "the same rule identity section 3 states for plan.budget versus the "
       "resolved configuration - `the value is committed in two places and "
       "neither silently wins` - i.e. an equality the closure decides",
       "MUST",
       {"runId": new_run, "closureOk": rep["ok"], "checks": rep["checks"],
        "entry": {k: p2["entry"][k] for k in ("relation", "resolution", "coverage",
                                              "resolutionCompleteness")},
        "consequence": "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH keys on `coverage` "
                       "alone, so this entry simultaneously carries the total "
                       "file@enumerated obligation and denies that the partition "
                       "was examined exhaustively. RC-2 reads examinedExhaustive "
                       "for a RESOLVED rung only, so on the twelve non-resolved "
                       "pairs nothing reads it at all.",
        "notAnRC1Escape": "RC-1 explicitly declines to constrain "
                          "examinedExhaustive (`examinedExhaustive stays the "
                          "independent examined-partition claim of section 4.1`), "
                          "which is what leaves the join unstated rather than "
                          "deliberately relaxed."})

print()
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-gaps.json",
          "w") as f:
    json.dump(FINDINGS, f, indent=1, sort_keys=True, default=str)
print("findings recorded:", len(FINDINGS))
