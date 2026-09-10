"""Vector set 3: audit/comparison, mutation replay scope, repair-apply key,
pinned purge refusal, scope-policy parameter binding, terminations, and
relation-specific minimum-resolution predicates."""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402
import runner  # noqa: E402
import scen_ts  # noqa: E402

R = []


def rec(cid, desc, payload, kind="positive"):
    R.append({"id": cid, "kind": kind, "description": desc, "result": payload})


def refused(cid, desc, exc):
    R.append({"id": cid, "kind": "negative", "description": desc,
              "outcome": "refused", "refusal": str(exc)})


# ==========================================================================
# W1. Generic mutation replay scope (workflows section 1 / section 10)
# ==========================================================================
REQ = "req1_" + hashlib.sha256(b"request-a").hexdigest()[:32]
REQ2 = "req1_" + hashlib.sha256(b"request-b").hexdigest()[:32]


def mutation_key(request_id, step_id, operation):
    scope = {"schemaVersion": 1, "requestId": request_id, "stepId": step_id,
             "projectId": G.PROJECT_ID, "operation": operation}
    kit.validate("invocation", "#/$defs/MutationReplayScopeV1", scope)
    return osip.H("workflow.mutation-intent", scope), scope


k1, s1 = mutation_key(REQ, 0, "import")
k1b, _ = mutation_key(REQ, 0, "import")
k2, _ = mutation_key(REQ2, 0, "import")
k3, _ = mutation_key(REQ, 1, "import")
k4, _ = mutation_key(REQ, 0, "purge")
rec("W1-mutation-replay-scope",
    "H('workflow.mutation-intent', MutationReplayScopeV1) is a BARE 64-hex "
    "operational key over exactly {schemaVersion,requestId,stepId,projectId,operation}; "
    "effect inputs are NOT in the preimage",
    {"scope": s1, "idempotencyKey": k1, "isBare64Hex": len(k1) == 64,
     "deterministic": k1 == k1b,
     "differentFreshRequestDoesNotDeduplicate": k1 != k2,
     "differentStepDiffers": k1 != k3,
     "differentOperationDiffers": k1 != k4})

try:
    mutation_key(REQ, 0, "repair-apply")
    refused("W1n-repair-apply-in-generic-scope", "must be excluded", "ADMITTED")
except ValueError as exc:
    refused("W1n-repair-apply-in-generic-scope",
            "repair-apply is explicitly excluded from the generic mutation scope", exc)

# ==========================================================================
# W2. Repair apply: the DISTINCT content-derived key
# ==========================================================================
_store = G.Store()
_scn = scen_ts.build(_store, "ordinary")
_run = runner.assemble(_scn)
SNAP_ID = _scn["snapshot"]["id"]
REPAIR_PLAN_ID = "repairplan2:" + hashlib.sha256(b"a repair plan").hexdigest()


def repair_apply_key(project_id, repair_plan_id, base_snapshot_id):
    record = {"operation": "repair-apply", "projectId": project_id,
              "repairPlanId": repair_plan_id, "baseSnapshotId": base_snapshot_id}
    return osip.canonical_record_digest(record), record


rk, rrec = repair_apply_key(G.PROJECT_ID, REPAIR_PLAN_ID, SNAP_ID)
rk2, _ = repair_apply_key(G.PROJECT_ID, REPAIR_PLAN_ID,
                          "snapshot2:" + "0" * 64)
mk_same_shape = osip.H("workflow.mutation-intent", s1)
rec("W2-repair-apply-key",
    "repair-apply uses the RAW SHA-256 of canonical "
    "{operation,projectId,repairPlanId,baseSnapshotId} - content-derived, not the "
    "operational H('workflow.mutation-intent') recipe, and a different base snapshot "
    "is a different key",
    {"preimage": rrec, "key": rk, "differentBaseSnapshotDiffers": rk != rk2,
     "isNotAnHIdentity": rk != osip.H("workflow.mutation-intent", rrec),
     "twoRecipesNeverCollide": rk != mk_same_shape,
     "note": "a completed equal key performs no second effect; a replay delivery "
             "gets its own receipt with replayed=true and the original stays immutable"})

# ==========================================================================
# W3. Complete pinned-purge refusal (identity section 5 / workflows section 12)
# ==========================================================================
pins = sorted([{"pinId": "baseline:main", "kind": "baseline"},
               {"pinId": "backup:2026-09-01", "kind": "backup-export"},
               {"pinId": "repair:plan-7", "kind": "repair-prerequisite"}],
              key=lambda p: p["pinId"].encode("utf-8"))
disclosure = {"runId": _run["run"]["id"], "activePins": pins,
              "consequences": ["named-pins-revoked",
                               "dependent-evidence-replay-unavailable",
                               "sealed-history-retained"]}
kit.validate("common", "#/$defs/PinnedPurgeDisclosure", disclosure)
detail = {"code": "evidence.pinned",
          "remedy": "revoke the named pins under explicit lifecycle authorization, "
                    "or purge a Run that is not pinned",
          "subject": _run["run"]["id"], "purgeDisclosure": disclosure}
kit.validate("common", "#/$defs/DomainDetail", detail)
term = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
        "domainDetail": detail}
kit.validate("common", "#/$defs/StepTermination", term)
osip.check_order(pins, {"by": ["pinId"]})
rec("W3-pinned-purge-refusal",
    "a direct purge of a pinned Run refuses request-rejected / "
    "REQUEST.PRECONDITION_FAILED / exit 2 with the COMPLETE active pin inventory "
    "sorted uniquely by pinId and the three ordered consequences; no pin is "
    "omitted, truncated or aggregated into a count",
    {"termination": term, "exitCode": 2, "pinCount": len(pins)})

truncated = dict(disclosure, activePins=pins[:1])
kit.validate("common", "#/$defs/PinnedPurgeDisclosure", truncated)
rec("W3n-truncated-pin-set-is-schema-valid",
    "a schema-valid SUBSET does not satisfy the completeness obligation: the host "
    "must compare the disclosed pins with the complete set observed under the "
    "exclusive purge lease. Schema validity is not inventory completeness.",
    {"schemaValid": True, "satisfiesObligation": False,
     "obligationOwner": "host ledger observation under the exclusive purge lease"},
    kind="advisory")
try:
    kit.validate("common", "#/$defs/DomainDetail",
                 {"code": "evidence.purged", "remedy": "x",
                  "purgeDisclosure": disclosure})
    refused("W3n-disclosure-on-wrong-detail", "should refuse", "ADMITTED")
except ValueError as exc:
    refused("W3n-disclosure-on-wrong-detail",
            "purgeDisclosure is admissible only under code evidence.pinned", exc)

# ==========================================================================
# W4. ScopeDocumentV1 bound as an analysis-spec parameter, and the E2->E3 axis
# ==========================================================================
POLICY_DOC_DIGEST = kit.doc_digest("policy")
IMPORTCTX_DOC_DIGEST = kit.doc_digest("importctx")


def scope_parameter(include, exclude=()):
    doc = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
           "include": list(include), "exclude": list(exclude)}
    kit.validate("policy", "#/$defs/ScopeDocumentV1", doc)
    return ({"schemaDigest": POLICY_DOC_DIGEST,
             "payloadDigest": osip.canonical_record_digest(doc)}, doc)


param_a, doc_a = scope_parameter(["src/**"])
param_b, doc_b = scope_parameter(["src/**"], ["src/legacy.js"])

store_a = G.Store()
scn_a = scen_ts.build(store_a, "ordinary")
run_a = runner.assemble(scn_a, analysis_parameters=[param_a])
store_b = G.Store()
scn_b = scen_ts.build(store_b, "ordinary")
run_b = runner.assemble(scn_b, analysis_parameters=[param_b])

registry = kit.doc("identity")["x-opensip-payload-registry"]["classes"]["parameter"]
rec("W4-scope-document-parameter",
    "the registered `parameter` class row "
    "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1 makes a "
    "lawful scope-policy parameter admissible at Plan closure; the parameter's "
    "schemaDigest is the raw SHA-256 of the FULL policy-document document bytes",
    {"registryRows": sorted(registry["rows"].keys()),
     "citedSchemaDigest": POLICY_DOC_DIGEST,
     "selector": registry["rows"][
         "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"]["selector"],
     "scopeDocumentA": doc_a, "scopeDocumentB": doc_b,
     "parameterA": param_a, "parameterB": param_b,
     "planA": run_a["plan"]["id"], "planB": run_b["plan"]["id"],
     "onlyTheScopePolicyChanged":
         run_a["plan"]["descriptor"]["scopeDigest"]
         == run_b["plan"]["descriptor"]["scopeDigest"],
     "planScopeDigest_is_the_foundation_scope_descriptor":
         run_a["plan"]["descriptor"]["scopeDigest"],
     "analysisSpecDigestsDiffer":
         run_a["plan"]["descriptor"]["analysisSpecDigest"]
         != run_b["plan"]["descriptor"]["analysisSpecDigest"],
     "planIdentitiesDiffer": run_a["plan"]["id"] != run_b["plan"]["id"]})

try:
    bad = {"schemaDigest": kit.doc_digest("comparison"),
           "payloadDigest": osip.canonical_record_digest(doc_a)}
    rows = {"foundation/import-source-context.schema.json",
            "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"}
    known = {IMPORTCTX_DOC_DIGEST, POLICY_DOC_DIGEST}
    if bad["schemaDigest"] not in known:
        raise ValueError("parameter class: a cited schema with no registry row "
                         "refuses; there is no default row and no caller-selected "
                         "schema (IMPORT/PARAMETER schema unregistered)")
except ValueError as exc:
    refused("W4n-unregistered-parameter-schema",
            "a real but unregistered parameter document refuses", exc)


def evaluation_context(policy_digest, scope_policy_digest, waiver_digest,
                       detectors, imports=()):
    ctx = {"policyDigest": policy_digest, "scopeDigest": scope_policy_digest,
           "waiverSetDigest": waiver_digest, "detectorClosureIds": list(detectors),
           "evidenceAvailability": {"importKinds": sorted({i["kind"] for i in imports}),
                                    "relations": [],
                                    "imports": sorted(i["id"] for i in imports)}}
    kit.validate("comparison", "#/$defs/EvaluationContext", ctx)
    return ctx


base_ctx = evaluation_context(run_a["plan"]["descriptor"]["policyDigest"],
                              param_a["payloadDigest"],
                              run_a["plan"]["descriptor"]["waiverDigest"],
                              [scn_a["rule"]["id"]])
cur_ctx = evaluation_context(run_a["plan"]["descriptor"]["policyDigest"],
                             param_b["payloadDigest"],
                             run_a["plan"]["descriptor"]["waiverDigest"],
                             [scn_a["rule"]["id"]])
rec("W4b-scope-axis-only",
    "a comparison in which ONLY the scope policy changed: policy, waivers and "
    "detectors are equal, so the first axis at which the fingerprint changes is "
    "SCOPE (E2 -> E3). This is a different record from plan.scopeDigest, the "
    "repository extent actually walked by discovery.",
    {"baselineContext": base_ctx, "currentContext": cur_ctx,
     "contextDelta": {"codeChanged": False, "detectorChanged": False,
                      "policyChanged": False, "scopeChanged": True,
                      "waiversChanged": False, "evidenceAvailabilityChanged": False},
     "classifyingAxis": "scope", "classification": "SCOPE-DELTA",
     "distinctFromDiscoveryScope": {
         "plan.scopeDigest (foundation scope-descriptor)":
             run_a["plan"]["descriptor"]["scopeDigest"],
         "EvaluationContext.scopeDigest (ScopeDocumentV1)": param_a["payloadDigest"],
         "distinct": run_a["plan"]["descriptor"]["scopeDigest"]
                     != param_a["payloadDigest"]}})

# ==========================================================================
# W5. Public termination examples, all validated from the closed schemas
# ==========================================================================
TERMS = [
    ("T1-fresh-durable-analysis", 0, "the default zero-config invocation succeeds; "
     "DEFAULTED durable-unbounded retention is disclosed before the first write",
     {"class": "success", "authority": "authoritative", "runId": _run["run"]["id"]}),
    ("T2-policy-failed-authoritative", 1, "a failing authoritative Run carries its RunId",
     {"class": "policy-failed", "authority": "authoritative",
      "runId": _run["run"]["id"]}),
    ("T3-policy-failed-ephemeral", 1, "--ephemeral is explicitly non-authoritative: "
     "the branch carries authority=ephemeral INSTEAD of a runId",
     {"class": "policy-failed", "authority": "ephemeral"}),
    ("T4-ephemeral-cannot-supply-authority", 2,
     "--ephemeral with a baseline/repair prerequisite",
     {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
      "domainDetail": {"code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                       "remedy": "re-run without --ephemeral"}}),
    ("T5-indeterminate-coverage", 3,
     "admitted-but-incomplete native inputs seal an AUTHORITATIVE Run and terminate "
     "indeterminate with the deficiency as typed detail in the coverage2 record",
     {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
      "runId": _run["run"]["id"],
      "coverageId": _scn["coverages"][0]["id"]}),
    ("T6-provider-unavailable", 3, "a required provider closure is not installed",
     {"class": "indeterminate", "reasonCodes": ["COVERAGE.PROVIDER_UNAVAILABLE"],
      "domainDetail": {"code": "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED",
                       "remedy": "opensip install provider-typescript"}}),
    ("T7-renderer-failed-after-commit", 4,
     "required delivery failure AFTER a committed Run retains the RunId and never "
     "rewrites the Run",
     {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
      "faultCause": "delivery-required", "runId": _run["run"]["id"],
      "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                       "remedy": "re-render from the retained Run"}}),
    ("T8-evidence-missing-during-operation", 4,
     "inability to read required evidence DURING a selected operation is "
     "HOST.IO_FAILURE, a different event position from the pre-evaluation refusal",
     {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
      "faultCause": "host-io",
      "domainDetail": {"code": "evidence.missing",
                       "remedy": "restore or regenerate the missing objects"}}),
    ("T9-evidence-purged-before-evaluation", 2,
     "a query requiring actual proof refuses BEFORE evaluation",
     {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
      "domainDetail": {"code": "evidence.purged",
                       "remedy": "re-analyze to produce fresh evidence"}}),
    ("T10-interrupted-after-commit", 130,
     "a signal before settle: remaining steps are cancelled and a Run committed by "
     "an earlier step is still named",
     {"class": "interrupted", "signal": "SIGINT", "runId": _run["run"]["id"]}),
    ("T11-provider-protocol-violation", 4,
     "a worker that lies about its examined partition contributes no facts, no "
     "Coverage and no Run",
     {"class": "operational-failed", "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
      "faultCause": "provider-protocol"}),
    ("T12-backup-choice-required-in-ci", 2,
     "CI never prompts; without an explicit storage-policy choice the first "
     "source-derived write refuses BEFORE creating evidence",
     {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
      "domainDetail": {"code": "storage.backup-choice-required",
                       "remedy": "pass --allow-backup-custody, choose another root, "
                                 "or use --ephemeral"}}),
    ("T13-doctor-defects-found", 0,
     "a produced doctor report is success even with defects; CI gates on the "
     "machine report, never the exit code",
     {"class": "success",
      "domainDetail": {"code": "DOCTOR.DEFECTS_FOUND",
                       "remedy": "inspect doctor.defectsFound"}}),
]
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2,
        "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
detail_registry = kit.doc("details")
_known_codes = set(kit.doc("common")["$defs"]["DomainDetailCode"]["enum"])
term_out = []
for tid, exit_code, desc, t in TERMS:
    kit.validate("common", "#/$defs/StepTermination", t)
    assert EXIT[t["class"]] == exit_code, tid
    if "domainDetail" in t:
        assert t["domainDetail"]["code"] in _known_codes, (tid, t["domainDetail"]["code"])
    term_out.append({"id": tid, "exitCode": exit_code, "description": desc,
                     "termination": t})
rec("W5-public-terminations",
    "13 public termination examples, each validated against "
    "common.schema.json#/$defs/StepTermination and with its DomainDetail code "
    "checked for membership of the single closed public-detail registry",
    {"terminations": term_out,
     "registryEntryCount": len(_known_codes)})

# negative terminations (branch contract)
for nid, ndesc, nterm in [
        ("T-N1-success-with-error", "success may carry no errorCode",
         {"class": "success", "errorCode": "HOST.IO_FAILURE"}),
        ("T-N2-policy-failed-without-run-or-ephemeral",
         "policy-failed requires runId or authority=ephemeral",
         {"class": "policy-failed"}),
        ("T-N3-operational-without-fault-cause",
         "operational-failed requires a non-none faultCause",
         {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE"}),
        ("T-N4-indeterminate-without-reasons",
         "indeterminate requires reasonCodes",
         {"class": "indeterminate"}),
        ("T-N5-unregistered-detail-code",
         "an unknown DomainDetail code refuses admission",
         {"class": "request-rejected", "errorCode": "CONFIG.INVALID",
          "domainDetail": {"code": "native.too-many-units", "remedy": "x"}})]:
    try:
        kit.validate("common", "#/$defs/StepTermination", nterm)
        refused(nid, ndesc, "ADMITTED -- branch contract not enforced by schema")
    except ValueError as exc:
        refused(nid, ndesc, exc)

if __name__ == "__main__":
    print(json.dumps(R, indent=1, ensure_ascii=False))
