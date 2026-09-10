#!/usr/bin/env python3
"""Execute bounded workflow reconstructions from kit laws.

Does not rewrite frozen Run stores. Does not treat prior reviewer grades as
acceptance. Tests live in workflow_correct_test.py (nonzero exit on failure).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-query-recheck.v6/output/isolated-snapshot")
OUT = ROOT
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.errors import AdmissionError  # noqa: E402
from helper.evaluator import eval_atom  # noqa: E402
from helper.identity import H  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.workflow_laws import (  # noqa: E402
    GRAPH_PROJECTABLE,
    admit_clones_fact,
    admit_config_path,
    admit_edition_map_crate,
    admit_syntax_suffix,
    classify_presence,
    committed_id,
    config_graph,
    counts_from_entries,
    cursor_token,
    derive_rust_edition,
    finish_baseline,
    finish_comparison,
    finish_repair_plan,
    mutation_intent_key,
    neighbors,
    page_items,
    project_edges,
    reach,
    render_parity,
    repair_apply_key,
    repair_target_join,
    rust_body_l0,
    rust_body_l0_retained,
    selection_hash,
    shortest_path,
    unit_id,
    zero_config_unit,
)

CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
INV = "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json"
CMP = "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json"
BASE = "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json"
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
REP = "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json"
MRS = "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
TA = "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json"
COMMON = "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"
OWN = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"

CLASS_TO_EXIT = {
    "success": 0,
    "policy-failed": 1,
    "request-rejected": 2,
    "indeterminate": 3,
    "operational-failed": 4,
    "interrupted": 130,
}

HEX_A = "a" * 64
HEX_B = "b" * 64
HEX_C = "c" * 64
HEX_D = "d" * 64
REQ = "req1_" + "ab" * 16
PRJ = "prj1-" + HEX_A
meta_syn = json.loads((OUT / "runs/syntax-code.meta.json").read_text())
meta_ts = json.loads((OUT / "runs/ts.meta.json").read_text())
RUN_SYN = meta_syn["runId"]
SNAP_SYN = meta_syn["snapshotId"]
PLAN_SYN = meta_syn["planId"]
RUN_TS = meta_ts["runId"]
PLAN_TS = meta_ts["planId"]
EXEC = "exec1_" + "cd" * 16
CLOSURE = "closure2:" + HEX_A
FINGER = "finding-key2:" + HEX_B
BUILD = HEX_A

results = []


def dump(rel: str, obj) -> Path:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def chk(label, inst, rel, selector=None):
    r = validate_against(inst, rel, selector=selector, label=label)
    rec = {"label": label, "stockOk": r["stockOk"], "nErrors": len(r["errors"]), "errors": r["errors"][:8]}
    if not r["stockOk"]:
        raise SystemExit(f"SCHEMA {label}: {r['errors'][:3]}")
    return rec


def record(req_id, artifact, checks, extra=None):
    rec = {"id": req_id, "artifact": artifact, "checks": checks, "executed": True}
    if extra:
        rec.update(extra)
    results.append(rec)


def domain_detail(code, remedy, **more):
    d = {"code": code, "remedy": remedy}
    d.update(more)
    return d


def termination(*, klass, error_code=None, fault_cause=None, reason_codes=None, signal=None, domain_detail=None, run_id=None):
    t = {"class": klass}
    if error_code is not None:
        t["errorCode"] = error_code
    if fault_cause is not None:
        t["faultCause"] = fault_cause
    if reason_codes is not None:
        t["reasonCodes"] = reason_codes
    if signal is not None:
        t["signal"] = signal
    if domain_detail is not None:
        t["domainDetail"] = domain_detail
    if run_id is not None:
        t["runId"] = run_id
    return t


def failure_envelope(*, request_id, klass, error_code=None, domain, extra_term=None):
    term = termination(klass=klass, error_code=error_code, domain_detail=domain, **(extra_term or {}))
    if klass == "operational-failed" and "faultCause" not in term:
        term["faultCause"] = "host-io"
    return {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "failure",
        "requestId": request_id,
        "termination": term,
        "exitCode": CLASS_TO_EXIT[klass],
        "errors": [domain],
    }


def catch(fn):
    try:
        return {"ok": True, "value": fn(), "firstRefusal": None}
    except AdmissionError as e:
        return {"ok": False, "value": None, "firstRefusal": e.as_dict()}


# --- envelopes (re-executed; D9 derived) ---
envelopes = {
    "config-input": failure_envelope(
        request_id="req1_" + "11" * 16, klass="request-rejected", error_code="CONFIG.INVALID",
        domain=domain_detail("CONFIG.INVALID", "correct the configuration input and retry"),
    ),
    "retained-external-input": failure_envelope(
        request_id="req1_" + "12" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("IMPORT.STALE_FOR_PLAN", "re-import retained external evidence against the current Plan"),
    ),
    "host-invalid-internal": failure_envelope(
        request_id="req1_" + "13" * 16, klass="operational-failed", error_code="HOST.IO_FAILURE",
        domain=domain_detail("HOST.INVARIANT_VIOLATED", "discard the host-generated invalid internal record; re-run admission"),
        extra_term={"fault_cause": "host-invariant"},
    ),
    "producer-boundary": failure_envelope(
        request_id="req1_" + "14" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("GRANT.REFUSED", "producer is outside the admitted principal boundary"),
    ),
    "public-from-internal": failure_envelope(
        request_id="req1_" + "15" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("ENVELOPE.KIND", "public envelope was projected from an internal refusal; do not treat internal fields as public"),
    ),
    "pinned-purge": failure_envelope(
        request_id="req1_" + "16" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail(
            "evidence.pinned", "remove or wait out active retention pins before purge",
            subject="run " + RUN_SYN,
            purgeDisclosure={
                "runId": RUN_SYN,
                "activePins": [{"pinId": "pin-replayable", "kind": "baseline"}],
                "consequences": ["named-pins-revoked", "dependent-evidence-replay-unavailable", "sealed-history-retained"],
            },
        ),
        extra_term={"run_id": RUN_SYN},
    ),
    "purge-replay-output-failure": failure_envelope(
        request_id="req1_" + "17" * 16, klass="operational-failed", error_code="OUTPUT.SERIALIZATION_FAILED",
        domain=domain_detail("EVALUATION.REQUIRED_OUTPUT_OMITTED", "required replay output could not be materialized"),
        extra_term={"fault_cause": "output-serialization"},
    ),
    "failure-d9-complete": failure_envelope(
        request_id="req1_" + "18" * 16, klass="policy-failed",
        domain=domain_detail("EVALUATION.PROOF_VERDICT_INCONSISTENT", "sealed verdict is fail; inspect findings"),
        extra_term={"run_id": RUN_SYN},
    ),
}
file_map = {
    "config-input": "R-ENVELOPE-CONFIG-INPUT",
    "retained-external-input": "R-ENVELOPE-EXTERNAL-INPUT",
    "host-invalid-internal": "R-ENVELOPE-HOST-INVALID",
    "producer-boundary": "R-ENVELOPE-PRODUCER-BOUNDARY",
    "public-from-internal": "R-PUBLIC-FROM-INTERNAL-REFUSAL",
    "pinned-purge": "R-PINNED-PURGE",
    "purge-replay-output-failure": "R-PURGE-REPLAY-OUTPUT-FAILURE",
    "failure-d9-complete": "R-FAILURE-ENVELOPES-D9",
}
for name, env in envelopes.items():
    dump(f"envelopes/{name}.json", env)
    c = chk(name, env, CE, "#")
    record(file_map[name], f"envelopes/{name}.json", [c], extra={"exitCodeDerived": env["exitCode"], "class": env["termination"]["class"]})

term_examples = {
    "success": termination(klass="success"),
    "policy-failed": termination(klass="policy-failed", run_id=RUN_SYN),
    "request-rejected": termination(klass="request-rejected", error_code="CONFIG.INVALID"),
    "indeterminate": termination(klass="indeterminate", reason_codes=["VERDICT.INDETERMINATE"]),
    "operational-failed": termination(klass="operational-failed", error_code="HOST.IO_FAILURE", fault_cause="host-io"),
    "interrupted": termination(klass="interrupted", signal="SIGINT"),
}
dump("envelopes/public-termination.json", {"examples": term_examples, "owningRecord": "evaluator3 common.schema.json#/$defs/StepTermination"})
record("R-PUBLIC-TERMINATION-EXAMPLES", "envelopes/public-termination.json", [chk(f"term-{k}", v, COMMON, "#/$defs/StepTermination") for k, v in term_examples.items()])

d9 = json.loads((KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json").read_text())["classToExitCode"]
d9_vec = {
    "inheritedArtifact": "docs/coop/artifacts/d9-exit-contract.v1.14.json#/classToExitCode",
    "selectedComposition": "evaluator3 CommandEnvelope.exitCode derived from StepTermination.class",
    "inherited": d9,
    "selected": CLASS_TO_EXIT,
    "equal": d9 == CLASS_TO_EXIT,
}
dump("vectors/d9-extension-precedence.json", d9_vec)
record("R-D9-EXTENSION-PRECEDENCE", "vectors/d9-extension-precedence.json", [], extra={"computedEqual": d9 == CLASS_TO_EXIT})

def analysis_params(profile, role="primary"):
    return {"kind": "analysis", "profile": profile, "role": role, "durability": "authoritative", "snapshotSource": "live-worktree", "verdictGate": "self" if role == "primary" else "delegated"}

single = {
    "schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": "req1_" + "21" * 16, "projectId": PRJ,
    "workflow": {"kind": "builtin", "name": "analyze"}, "mode": {"interactive": False, "ci": True, "ephemeral": False},
    "orderedSteps": [{"stepId": 0, "kind": "analysis", "requirement": "required", "dependsOn": [], "dependencyGate": "completed", "retryPolicy": "idempotent-retry", "params": analysis_params("default")}],
}
multi = {
    "schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": "req1_" + "22" * 16, "projectId": PRJ,
    "workflow": {"kind": "builtin", "name": "audit"}, "mode": {"interactive": False, "ci": True, "ephemeral": False},
    "orderedSteps": [
        {"stepId": 0, "kind": "analysis", "requirement": "required", "dependsOn": [], "dependencyGate": "completed", "retryPolicy": "idempotent-retry", "params": analysis_params("default")},
        {"stepId": 1, "kind": "analysis", "requirement": "required", "dependsOn": [0], "dependencyGate": "completed", "retryPolicy": "idempotent-retry", "params": analysis_params("fit")},
    ],
}
dump("envelopes/single-step.json", single)
dump("envelopes/multi-step.json", multi)
record("R-SINGLE-STEP", "envelopes/single-step.json", [chk("single", single, INV, "#")])
record("R-MULTI-STEP-DIFFERENT-SELECTIONS", "envelopes/multi-step.json", [chk("multi", multi, INV, "#")], extra={"profiles": [s["params"]["profile"] for s in multi["orderedSteps"]]})

ci = json.loads((KIT / "docs/coop/design-corrections/workflows/command-inventory.v3.json").read_text())
qcmd = next(c for c in ci["commands"] if c["name"] == "query")
acmd = next(c for c in ci["commands"] if c["name"] == "analyze")
disclosure = {
    "source": "docs/coop/design-corrections/workflows/command-inventory.v3.json",
    "commandCount": len(ci["commands"]),
    "analyze": {k: acmd.get(k) for k in ("name", "owner", "requestClass", "authority", "steps", "formats", "parityFields")},
    "query": {k: qcmd.get(k) for k in ("name", "formats", "parityFields", "steps", "authority")},
    "ordering": "command-inventory.v3 commands sequence; InvocationRecord.orderedSteps sequence",
}
disclosure["analyze"]["boundedCardinality"] = {"commands": len(ci["commands"]), "steps.maxItems": 64, "requestedCapabilities.maxItems": 1024}
dump("envelopes/invocation-disclosure.json", disclosure)
record("R-INVOCATION-DISCLOSURE", "envelopes/invocation-disclosure.json", [], extra={"commandCount": len(ci["commands"])})

receipt = {"schemaVersion": 2, "runId": RUN_SYN, "executionId": EXEC, "namespaceId": "local", "commitSequence": 0, "inventoryDigest": hashlib.sha256(C({"runId": RUN_SYN, "kind": "inventory"})).hexdigest(), "sealedAssurance": "replayable", "signerKeyId": "synthetic-host-key"}
availability = {"schemaVersion": 2, "runId": RUN_SYN, "generation": 0, "state": "retained", "missingRefs": [], "reason": "complete"}
dump("envelopes/receipt-availability.json", {"receipt": receipt, "availability": availability, "syntheticHostObservation": True, "joinedRunId": RUN_SYN})
record("R-DURABLE-RECEIPT-AVAILABILITY", "envelopes/receipt-availability.json", [chk("receipt", receipt, IDENT, "#/$defs/commit-receipt"), chk("availability", availability, IDENT, "#/$defs/availability")])

# --- config graphs ---
g_syn = config_graph(entry=None, nodes=[])
g_custom = config_graph(
    entry="tsconfig.app.json",
    nodes=[
        {"path": "tsconfig.base.json", "bytes": b'{"compilerOptions":{"strict":true}}', "extendsResolved": []},
        {"path": "tsconfig.strict.json", "bytes": b'{"compilerOptions":{"noImplicitAny":true}}', "extendsResolved": ["tsconfig.base.json"]},
        {"path": "tsconfig.app.json", "bytes": b'{"extends":["tsconfig.base.json","tsconfig.strict.json","tsconfig.base.json"]}', "extendsResolved": ["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"]},
    ],
)
g_js = config_graph(
    entry="jsconfig.json",
    nodes=[
        {"path": "jsconfig.json", "bytes": b'{"extends":"./tsconfig.shared.json"}', "extendsResolved": ["tsconfig.shared.json"]},
        {"path": "tsconfig.shared.json", "bytes": b'{"compilerOptions":{"allowJs":true}}', "extendsResolved": []},
    ],
)
for rel, g, rid, note in [
    ("vectors/config-synthesized.json", g_syn, "R-CONFIG-SYNTHESIZED", "entryConfigPath null, nodes empty"),
    ("vectors/config-custom-multi-base.json", g_custom, "R-CONFIG-CUSTOM-MULTI-BASE", "custom entry kind=other; extendsResolved is a sequence with a repeated later-wins base edge"),
    ("vectors/config-js-shared-base.json", g_js, "R-CONFIG-JS-SHARED-BASE", "jsconfig inheriting other-filename base"),
]:
    payload = {**g, "tsconfigGraphHashIsNotAGraphField": True, "note": note}
    if rid == "R-CONFIG-CUSTOM-MULTI-BASE":
        entry_node = next(n for n in g["graph"]["nodes"] if n["path"] == g["graph"]["entryConfigPath"])
        payload["repeatedBaseSequence"] = entry_node["extendsResolved"]
        payload["laterWins"] = True
        payload["laterWinningBase"] = entry_node["extendsResolved"][-1]
        payload["orderIsSequenceNotSet"] = True
        payload["selector"] = "native-evidence.schemas.v2.json TypeScriptConfigGraphV1.nodes[].extendsResolved x-opensip-order sequence; later entry wins; repeated edges retained"
        payload["retainedConfigBytes"] = {
            n["path"]: hashlib.sha256(
                {
                    "tsconfig.base.json": b'{"compilerOptions":{"strict":true}}',
                    "tsconfig.strict.json": b'{"compilerOptions":{"noImplicitAny":true}}',
                    "tsconfig.app.json": b'{"extends":["tsconfig.base.json","tsconfig.strict.json","tsconfig.base.json"]}',
                }[n["path"]]
            ).hexdigest()
            for n in g["graph"]["nodes"]
        }
        payload["preservedPeerRefusedDiamond"] = "preserved-failures/workflow-selfaudit-v4-peer-refused/vectors/config-custom-multi-base.json"
    dump(rel, payload)
    record(rid, rel, [chk(rid, g["graph"], NATIVE, "#/$defs/TypeScriptConfigGraphV1")], extra={"graphDigestSha256": g["graphDigestSha256"]})

# --- identity recipes: repair / mutation ---
mrs = {"schemaVersion": 1, "requestId": REQ, "stepId": 0, "projectId": PRJ, "operation": "purge"}
intent = mutation_intent_key(mrs)
dump("vectors/mutation-replay-scope.json", {**mrs, "mutationIntentKey": intent, "recipe": "H(\"workflow.mutation-intent\", MutationReplayScopeV1)"})
record("R-MUTATION-REPLAY-SCOPE", "vectors/mutation-replay-scope.json", [chk("mrs", mrs, MRS, "#/$defs/MutationReplayScopeV1")], extra={"mutationIntentKey": intent})

repair_desc = {
    "schemaFamily": "opensip.product.repair-plan", "schemaMajor": 2, "projectId": PRJ, "snapshotId": SNAP_SYN,
    "evidenceRunId": RUN_SYN, "planId": PLAN_SYN,
    "recipe": {"contributionId": "opensip.rules.syntax-pilot", "recipeId": "noop", "recipeVersion": "1.0.0", "closureId": CLOSURE},
    "recipeTrust": "admitted", "evidenceOrigin": "native-analysis",
    "closedWorld": {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "deadCodeRepairEligible": False},
    "targets": [FINGER], "edits": [], "totalPostimageBytes": 0,
    "evidenceRequirements": [{"relation": "file", "minResolution": "enumerated", "completeness": "complete", "satisfied": True}],
    "permittedEditScope": ["hello.rs"], "applicable": False, "unmetPreconditions": [], "limitations": ["preview-is-not-apply"],
}
repair_plan = finish_repair_plan(repair_desc)
dump("vectors/repair-descriptor.json", repair_plan)
record("R-REPAIR-DESCRIPTOR", "vectors/repair-descriptor.json", [chk("repair", repair_plan, REP, "#/$defs/RepairPlanV1")], extra={"repairPlanId": repair_plan["repairPlanId"], "recipe": "H('workflow.repair-plan', descriptor)"})

rak = repair_apply_key(project_id=PRJ, repair_plan_id=repair_plan["repairPlanId"], base_snapshot_id=SNAP_SYN)
apply_vec = {
    "recipe": rak["recipe"],
    "applyKeyPreimage": rak["preimage"],
    "repairApplyKey": rak["key"],
    "mutationReplayScope": mrs,
    "mutationIntentKey": intent,
    "unequal": rak["key"] != intent,
    "preservedOriginalWrongPreimage": "preserved-failures/workflow-review-v2-refused-original/vectors/repair-apply-key.json",
}
dump("vectors/repair-apply-key.json", apply_vec)
record("R-REPAIR-APPLY-KEY", "vectors/repair-apply-key.json", [], extra={"repairApplyKey": rak["key"], "unequalToMutationIntent": rak["key"] != intent})

matched = {FINGER}
pos = catch(lambda: repair_target_join(target=FINGER, matched_fingerprints=matched))
neg = catch(lambda: repair_target_join(target="finding-key2:" + HEX_D, matched_fingerprints=matched))
dump("vectors/repair-authority-per-target.json", {
    "function": "helper.workflow_laws.repair_target_join",
    "matchedFingerprints": sorted(matched),
    "positive": {"target": FINGER, "result": pos},
    "negative": {"target": "finding-key2:" + HEX_D, "result": neg},
})
record("R-REPAIR-AUTHORITY-PER-TARGET", "vectors/repair-authority-per-target.json", [], extra={"negativeCode": (neg["firstRefusal"] or {}).get("code")})

# --- min-resolution three levels × qualifying/insufficient ---
subj = {"kind": "file", "nativeSubjectId": "a.ts"}
facts_syn = [{"id": "fact2:" + HEX_A, "record": {"relation": "imports", "resolution": "syntactic-specifier"}}]
pl_syn = {"fact2:" + HEX_A: {"path": "a.ts", "importer": "a.ts", "specifier": "./b"}}
cov_syn = [{"id": "coverage2:" + HEX_A, "record": {"relation": "imports", "resolution": "syntactic-specifier"}, "entry": {"coverage": "complete"}}]
facts_res = [{"id": "fact2:" + HEX_B, "record": {"relation": "imports", "resolution": "resolved-target"}}]
pl_res = {"fact2:" + HEX_B: {"path": "a.ts", "importer": "a.ts", "specifier": "./b", "resolvedTarget": "b.ts"}}
cov_res = [{"id": "coverage2:" + HEX_B, "record": {"relation": "imports", "resolution": "resolved-target"}, "entry": {"coverage": "complete"}}]
facts_ty = [{"id": "fact2:" + HEX_C, "record": {"relation": "types", "resolution": "checked"}}]
pl_ty = {"fact2:" + HEX_C: {"path": "a.ts", "symbol": "n", "type": "number"}}
cov_ty = [{"id": "coverage2:" + HEX_C, "record": {"relation": "types", "resolution": "checked"}, "entry": {"coverage": "complete"}}]
atom_syn = {"op": "exists", "relation": "imports", "minResolution": "syntactic-specifier", "filters": []}
atom_res = {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []}
atom_ty = {"op": "exists", "relation": "types", "minResolution": "checked", "filters": []}
minres_cases = [
    {"level": "syntactic", "relation": "imports", "minResolution": "syntactic-specifier",
     "qualifying": eval_atom(atom_syn, subject=subj, facts=facts_syn, coverages=cov_syn, payloads=pl_syn),
     "insufficient": eval_atom(atom_syn, subject=subj, facts=[], coverages=[], payloads={})},
    {"level": "resolved", "relation": "imports", "minResolution": "resolved-target",
     "qualifying": eval_atom(atom_res, subject=subj, facts=facts_res, coverages=cov_res, payloads=pl_res),
     "insufficient": eval_atom(atom_res, subject=subj, facts=facts_syn, coverages=cov_res, payloads=pl_syn)},
    {"level": "type", "relation": "types", "minResolution": "checked",
     "qualifying": eval_atom(atom_ty, subject=subj, facts=facts_ty, coverages=cov_ty, payloads=pl_ty),
     "insufficient": eval_atom(atom_ty, subject=subj, facts=[], coverages=cov_ty, payloads={})},
]
# expected from kit: qualifying true; syntactic insufficient no-coverage => indeterminate; resolved/type complete-absence => false
expected = {"syntactic": ("true", "indeterminate"), "resolved": ("true", "false"), "type": ("true", "false")}
inputs = {
    "syntactic": {"qualifyingFacts": facts_syn, "qualifyingPayloads": pl_syn, "qualifyingCoverages": cov_syn, "insufficientFacts": [], "insufficientPayloads": {}, "insufficientCoverages": []},
    "resolved": {"qualifyingFacts": facts_res, "qualifyingPayloads": pl_res, "qualifyingCoverages": cov_res, "insufficientFacts": facts_syn, "insufficientPayloads": pl_syn, "insufficientCoverages": cov_res},
    "type": {"qualifyingFacts": facts_ty, "qualifyingPayloads": pl_ty, "qualifyingCoverages": cov_ty, "insufficientFacts": [], "insufficientPayloads": {}, "insufficientCoverages": cov_ty},
}
minres = {
    "function": "helper.evaluator.eval_atom over retained facts/Coverage, not helper agreement labels",
    "selector": "atom-evaluation-contract.v1.md; evaluator-composition-contract.v3.md §3",
    "subject": subj,
    "cases": [],
    "preservedPeerRefusedLabelsOnly": "preserved-failures/workflow-selfaudit-v4-peer-refused/vectors/min-resolution.json",
}
for c in minres_cases:
    q, i = c["qualifying"]["value"], c["insufficient"]["value"]
    eq, ei = expected[c["level"]]
    inp = inputs[c["level"]]
    minres["cases"].append({
        "level": c["level"], "relation": c["relation"], "minResolution": c["minResolution"],
        "atom": {"op": "exists", "relation": c["relation"], "minResolution": c["minResolution"], "filters": []},
        "qualifying": {
            "facts": inp["qualifyingFacts"],
            "payloads": inp["qualifyingPayloads"],
            "coverages": inp["qualifyingCoverages"],
            "value": q,
        },
        "insufficient": {
            "facts": inp["insufficientFacts"],
            "payloads": inp["insufficientPayloads"],
            "coverages": inp["insufficientCoverages"],
            "value": i,
            "kind": "no-coverage" if not inp["insufficientCoverages"] else "complete-coverage-no-match",
        },
        "qualifyingExpected": eq, "insufficientExpected": ei,
        "qualifyingAgrees": q == eq, "insufficientAgrees": i == ei,
    })
dump("vectors/min-resolution.json", minres)
record("R-MIN-RESOLUTION-THREE-LEVELS", "vectors/min-resolution.json", [], extra={"cases": [{"level": c["level"], "qualifyingValue": c["qualifying"]["value"], "insufficientValue": c["insufficient"]["value"]} for c in minres["cases"]]})

# repair evidence records bound to those cases (not prose)
rep_ev_reqs = []
for c in minres["cases"]:
    sat = c["qualifyingAgrees"] and c["qualifying"]["value"] == "true"
    rep_ev_reqs.append({
        "relation": c["relation"], "minResolution": c["minResolution"], "completeness": "complete",
        "satisfied": sat, "level": c["level"],
        "qualifyingValue": c["qualifying"]["value"], "insufficientValue": c["insufficient"]["value"],
    })
rep_ev_desc = dict(repair_desc)
rep_ev_desc["evidenceRequirements"] = [{k: v for k, v in r.items() if k in ("relation", "minResolution", "completeness", "satisfied")} for r in rep_ev_reqs]
rep_ev_plan = finish_repair_plan(rep_ev_desc)
dump("vectors/min-resolution-repair-evidence.json", {
    "tiedTo": "vectors/min-resolution.json",
    "repairPlan": rep_ev_plan,
    "requirements": rep_ev_reqs,
    "preservedOriginalProse": "preserved-failures/workflow-review-v2-refused-original/vectors/min-resolution-repair-evidence.json",
})
record("R-MIN-RESOLUTION-REPAIR-EVIDENCE", "vectors/min-resolution-repair-evidence.json", [chk("minres-repair", rep_ev_plan, REP, "#/$defs/RepairPlanV1")])

# --- negatives executed ---
ug_ok = catch(lambda: admit_syntax_suffix("hello.rs"))
ug_bad = catch(lambda: admit_syntax_suffix("notes.unknownlang"))
dump("vectors/unsupported-grammar.json", {
    "function": "helper.workflow_laws.admit_syntax_suffix",
    "table": "bundled syntax suffix table in workflow_laws.SYNTAX_SUFFIX_TABLE",
    "positive": {"path": "hello.rs", "result": ug_ok},
    "negative": {"path": "notes.unknownlang", "result": ug_bad},
    "didNotAssumeTypescriptCompiler": True,
    "preservedOriginalDeclaredFlag": "preserved-failures/workflow-review-v2-refused-original/vectors/unsupported-grammar.json",
})
record("R-RUN-UNSUPPORTED-GRAMMAR", "vectors/unsupported-grammar.json", [], extra={"negativeCode": (ug_bad["firstRefusal"] or {}).get("code")})

hm_ts = catch(lambda: admit_config_path("missing.tsconfig.json", {"tsconfig.json"}))
hm_rs = catch(lambda: admit_edition_map_crate("ghost-crate", {"demo"}))
hm_ts_ok = catch(lambda: admit_config_path("tsconfig.json", {"tsconfig.json"}))
hm_rs_ok = catch(lambda: admit_edition_map_crate("demo", {"demo"}))
dump("vectors/hidden-mismatch.json", {
    "function": "admit_config_path / admit_edition_map_crate",
    "typescript": {"input": "claimed tsconfig path not in snapshot inventory", "positive": hm_ts_ok, "negative": hm_ts, "masksLater": True},
    "rust": {"input": "Cargo.toml edition map key without retained crate root", "positive": hm_rs_ok, "negative": hm_rs, "masksLater": True},
})
record("R-HIDDEN-MISMATCH-PER-LANGUAGE", "vectors/hidden-mismatch.json", [], extra={"ts": (hm_ts["firstRefusal"] or {}).get("code"), "rust": (hm_rs["firstRefusal"] or {}).get("code")})

cl0 = catch(lambda: admit_clones_fact(anchors=[], level_spec_bytes=b"L1", language_id="javascript", provider_language="typescript"))
cl1 = catch(lambda: admit_clones_fact(anchors=["a.js"], level_spec_bytes=None, language_id="javascript", provider_language="typescript"))
cl2 = catch(lambda: admit_clones_fact(anchors=["a.js"], level_spec_bytes=b"L1", language_id="typescript", provider_language="typescript"))
cl_ok = catch(lambda: admit_clones_fact(anchors=["a.js"], level_spec_bytes=b"L1", language_id="javascript", provider_language="typescript"))
dump("vectors/clones-negatives.json", {
    "function": "helper.workflow_laws.admit_clones_fact",
    "vectors": [
        {"name": "zero-anchors", **cl0, "observedAnchorCount": 0, "requiredCardinality": 1},
        {"name": "missing-level-spec", **cl1},
        {"name": "languageId-from-provider-not-body", **cl2},
        {"name": "javascript-body-through-ts-ok", **cl_ok},
    ],
})
record("R-CLONES-NEGATIVE-VECTORS", "vectors/clones-negatives.json", [], extra={"codes": [(cl0["firstRefusal"] or {}).get("code"), (cl1["firstRefusal"] or {}).get("code"), (cl2["firstRefusal"] or {}).get("code")]})

# --- ownership pair with retained SourceUnitOwnershipV1 ---
span = b"pub fn add(a: i32, b: i32) -> i32 { a + b }\n"
lib_id = unit_id(marker_path="Cargo.toml", target_kind="lib", target_name="demo")
bin_id = unit_id(marker_path="Cargo.toml", target_kind="bin", target_name="extra")
bin21_id = unit_id(marker_path="Cargo.toml", target_kind="bin", target_name="newer")
unit_lib = {"unitId": lib_id, "markerPath": "Cargo.toml", "crateName": "demo", "targetKind": "lib", "targetName": "demo", "targetEdition": 2018}
unit_bin = {"unitId": bin_id, "markerPath": "Cargo.toml", "crateName": "demo", "targetKind": "bin", "targetName": "extra", "targetEdition": 2018}
unit_bin21 = {"unitId": bin21_id, "markerPath": "Cargo.toml", "crateName": "demo", "targetKind": "bin", "targetName": "newer", "targetEdition": 2021}
own1 = {"schemaVersion": 1, "enumeration": "complete",
        "units": sorted([unit_lib], key=lambda u: u["unitId"]),
        "selectedUnitIds": sorted([lib_id]),
        "ownership": [{"path": "src/lib.rs", "unitId": lib_id}]}
own2 = {"schemaVersion": 1, "enumeration": "complete",
        "units": sorted([unit_lib, unit_bin], key=lambda u: u["unitId"]),
        "selectedUnitIds": sorted([lib_id, bin_id]),
        "ownership": sorted([{"path": "src/lib.rs", "unitId": lib_id}, {"path": "src/lib.rs", "unitId": bin_id}], key=lambda r: (r["path"].encode(), r["unitId"]))}
own21 = {"schemaVersion": 1, "enumeration": "complete",
         "units": sorted([unit_bin21], key=lambda u: u["unitId"]),
         "selectedUnitIds": sorted([bin21_id]),
         "ownership": [{"path": "src/lib.rs", "unitId": bin21_id}]}
ed_map = {"demo": 2018}
e1 = derive_rust_edition(ownership=own1, body_path="src/lib.rs", edition_map=ed_map)
e2 = derive_rust_edition(ownership=own2, body_path="src/lib.rs", edition_map=ed_map)
e21 = derive_rust_edition(ownership=own21, body_path="src/lib.rs", edition_map=ed_map)
LEVEL_SPEC = b"opensip.l0-verbatim.spec.v1"
ret1 = rust_body_l0_retained(edition=e1, span=span, compiler_build=BUILD, level_spec_bytes=LEVEL_SPEC)
ret2 = rust_body_l0_retained(edition=e2, span=span, compiler_build=BUILD, level_spec_bytes=LEVEL_SPEC)
ret21 = rust_body_l0_retained(edition=e21, span=span, compiler_build=BUILD, level_spec_bytes=LEVEL_SPEC)
l0_1, l0_2, l0_21 = ret1["bodyIdentity"], ret2["bodyIdentity"], ret21["bodyIdentity"]
for name, rec in [("own1", own1), ("own2", own2), ("own21", own21)]:
    chk(f"ownership-{name}", rec, NATIVE, "#/$defs/SourceUnitOwnershipV1")
chk("blv-2018", ret1["bodyLanguageVersion"], IDENT, "#/$defs/body-language-version")
chk("blv-2021", ret21["bodyLanguageVersion"], IDENT, "#/$defs/body-language-version")
own_pair = {
    "function": "derive_rust_edition then rust_body_l0_retained; ownership maps never enter BLV",
    "selector": "identity-schemas.v3.json languageVersionBindingLaw; rust dialect.edition integer enum; FACT-IDENTITY frame retained under 64-hex suffix",
    "bodyPath": "src/lib.rs",
    "retainedSpanUtf8": span.decode("utf-8"),
    "retainedSpanSha256": hashlib.sha256(span).hexdigest(),
    "retainedCompilerBuild": BUILD,
    "retainedLevelSpecUtf8": LEVEL_SPEC.decode("utf-8"),
    "syntheticNativeContextObservation": True,
    "sameDialectOwnershipSelections": [
        {"selection": own1["selectedUnitIds"], "ownership": own1, "effectiveEdition": e1, "l0": l0_1, "retained": ret1},
        {"selection": own2["selectedUnitIds"], "ownership": own2, "effectiveEdition": e2, "l0": l0_2, "retained": ret2},
    ],
    "stableWhenOnlyOwnershipChangesWithoutDialect": l0_1 == l0_2 and e1 == e2 == 2018,
    "distinctWhenDialectChanges": l0_1 != l0_21,
    "dialectChange": {"ownership": own21, "effectiveEdition": e21, "l0": l0_21, "retained": ret21},
    "preservedPeerRefusedClaimedHashesOnly": "preserved-failures/workflow-selfaudit-v4-peer-refused/vectors/rust-body-identity-pair.json",
}
dump("vectors/rust-body-identity-pair.json", own_pair)
record("R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", "vectors/rust-body-identity-pair.json", [], extra={"stable": l0_1 == l0_2, "dialectMoves": l0_1 != l0_21})

# JS body through TS (keep executed identity)
from helper.body_identity import body_identity, body_language_version, l0_payload, language_version_bytes  # noqa: E402
js_span = b"export const n = 1;\n"
def l0_lang(lang, dialect):
    blv = body_language_version(language_id=lang, compiler_name="tsc", compiler_version="5.4.5", compiler_build=BUILD, dialect=dialect)
    return body_identity(level_id="L0-verbatim", level_spec_bytes=b"L0-verbatim", language_id=lang, language_version=language_version_bytes(blv), payload=l0_payload(js_span))
l0_js = l0_lang("javascript", {"grammarVariant": "js"})
l0_ts = l0_lang("typescript", {"grammarVariant": "ts"})
dump("vectors/js-body-through-ts.json", {"providerUniverse": "native.semantic-universe.typescript.v2", "bodyLanguageId": "javascript", "providerLanguageId": "typescript", "distinct": l0_js != l0_ts, "javascriptL0": l0_js, "typescriptL0OverSameBytes": l0_ts})
record("R-JS-CLONE-BODY-THROUGH-TS", "vectors/js-body-through-ts.json", [], extra={"distinct": l0_js != l0_ts})

tv = eval_atom({"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}, subject={"kind": "file", "nativeSubjectId": "missing.rs"}, facts=[], coverages=[], payloads={})
dump("vectors/replay-three-valued.json", {"op": "exists", "coverage": "absent", "matches": [], "value": tv["value"], "notVacuousTrue": tv["value"] != "true", "notVacuousFalse": tv["value"] != "false"})
record("R-REPLAY-THREE-VALUED", "vectors/replay-three-valued.json", [], extra={"value": tv["value"]})

# --- comparisons with H identities and consistent counts ---
policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [{"ruleId": "file-present", "ruleProgramRef": {"contributionId": "opensip.rules.syntax-pilot", "ruleStableId": "file-present", "semanticsMajor": 1, "programDigest": HEX_A}, "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"}, "emitWhen": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "hello.rs"}]}, "evidenceUse": []}]}
scope_a = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**/*"], "exclude": []}
scope_b = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**/*"], "exclude": ["tmp/**"]}
waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
pol_d = hashlib.sha256(C(policy)).hexdigest()
scope_a_d = hashlib.sha256(C(scope_a)).hexdigest()
scope_b_d = hashlib.sha256(C(scope_b)).hexdigest()
wav_d = hashlib.sha256(C(waivers)).hexdigest()

def ctx(scope_digest, evid_rel=("file",)):
    return {"policyDigest": pol_d, "scopeDigest": scope_digest, "waiverSetDigest": wav_d, "detectorClosureIds": [CLOSURE], "evidenceAvailability": {"importKinds": [], "relations": list(evid_rel), "imports": []}}

def delta(**kw):
    d = {"codeChanged": False, "detectorChanged": False, "policyChanged": False, "scopeChanged": False, "waiversChanged": False, "evidenceAvailabilityChanged": False}
    d.update(kw)
    return d

def pivots(**kw):
    p = {"E0": "not-needed", "E1": "not-needed", "E2": "not-needed", "E3": "not-needed"}
    p.update(kw)
    return p

def entry(fp, presence, **more):
    cls, live = classify_presence(presence)
    e = {"fingerprint": fp, "ruleId": "file-present", "detectorId": "opensip.rules.syntax-pilot", "presence": presence, "classification": cls, "subsequentDeltas": [], "liveInCurrent": live, "gates": False}
    e.update(more)
    if cls != "UNCHANGED" and "direction" not in e:
        e["direction"] = "appeared" if presence.get("B") is not True else "vanished"
    return e

def cmp_desc(*, performed, verdict, dlt, pvt, entries, unmatched, reason=None, bctx=None, cctx=None):
    desc = {
        "schemaFamily": "opensip.product.comparison", "schemaMajor": 2, "baselineId": "baseline2:" + HEX_A,
        "currentRunId": RUN_SYN, "currentSnapshotId": SNAP_SYN,
        "auditProfile": {"name": "report-only", "gateCodeNetNew": False, "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False, "newWaiverSuppressesCodeNetNew": False, "gateRuleUnder": "current-only"},
        "projectCorrespondence": "same-project", "comparisonPerformed": performed,
        "baselineContext": bctx or ctx(scope_a_d), "currentContext": cctx or ctx(scope_a_d),
        "contextDelta": dlt, "pivotsAvailable": pvt, "detectors": [], "ruleDeficiencies": [],
        "entries": entries, "verdict": verdict, "unmatchedOccurrences": unmatched,
        "correspondenceCoverage": [{"ruleId": "file-present", "gating": True, "matchedCount": len(entries), "unmatchedCount": len(unmatched), "populationUnknown": False, "zeroFindings": len(entries) == 0}],
        "currentEvaluationState": "evaluated", "currentExecutionDeficiencies": [],
    }
    if reason:
        desc["wholeIndeterminateReason"] = reason
        desc["remedy"] = domain_detail("COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE", "bind the missing required evidence and re-compare")
        if performed is False:
            desc["correspondenceCoverage"] = []
    return finish_comparison(desc)

cmp_empty = cmp_desc(performed=True, verdict="pass", dlt=delta(), pvt=pivots(), entries=[], unmatched=[])
cmp_missing = cmp_desc(performed=False, verdict="indeterminate", dlt=delta(evidenceAvailabilityChanged=True), pvt=pivots(E0="unavailable", E1="unavailable", E2="unavailable", E3="unavailable"), entries=[], unmatched=[], reason="required-evidence-unavailable")
cmp_evidence = cmp_desc(performed=True, verdict="indeterminate", dlt=delta(evidenceAvailabilityChanged=True), pvt=pivots(), entries=[], unmatched=[], reason="evidence-availability-changed")
cmp_scope = cmp_desc(performed=True, verdict="pass", dlt=delta(scopeChanged=True), pvt=pivots(), entries=[], unmatched=[], bctx=ctx(scope_a_d), cctx=ctx(scope_b_d))
cmp_scope_exhibit = {
    "comparison": cmp_scope,
    "retainedScopeDocuments": {
        "baseline": scope_a,
        "current": scope_b,
        "baselineScopeDigest": scope_a_d,
        "currentScopeDigest": scope_b_d,
        "policyUnchanged": True,
        "digestsUnequal": scope_a_d != scope_b_d,
    },
}

pres_e0 = {"B": True, "E0": True, "E1": None, "E2": None, "E3": None, "E4": True, "waivedB": False, "waivedC": False}
pres_e13 = {"B": True, "E0": None, "E1": True, "E2": True, "E3": True, "E4": True, "waivedB": False, "waivedC": False}
pres_pivot = {"B": False, "E0": True, "E1": None, "E2": None, "E3": None, "E4": False, "waivedB": False, "waivedC": False}
cmp_e0 = cmp_desc(performed=True, verdict="pass", dlt=delta(), pvt=pivots(E0="available"), entries=[entry(FINGER, pres_e0)], unmatched=[])
cmp_e13 = cmp_desc(performed=True, verdict="pass", dlt=delta(), pvt=pivots(E0="not-needed", E1="available", E2="available", E3="available"), entries=[entry(FINGER, pres_e13)], unmatched=[])
cmp_pivot = cmp_desc(performed=True, verdict="pass", dlt=delta(), pvt=pivots(E0="available"), entries=[entry("finding-key2:" + HEX_C, pres_pivot)], unmatched=[])

for rel, obj, rid in [
    ("vectors/comparison-empty-result.json", cmp_empty, "R-CMP-EMPTY-RESULT"),
    ("vectors/comparison-missing.json", cmp_missing, "R-CMP-MISSING"),
    ("vectors/comparison-evidence-changed.json", cmp_evidence, "R-CMP-EVIDENCE-CHANGED"),
    ("vectors/comparison-scope-policy-only.json", cmp_scope_exhibit, "R-SCOPE-POLICY-ONLY-COMPARISON"),
    ("vectors/pivot-only-fingerprints.json", cmp_pivot, "R-PIVOT-ONLY-FINGERPRINTS"),
]:
    dump(rel, obj)
    inst = obj["comparison"] if "comparison" in obj and "comparisonResultId" in obj.get("comparison", {}) else obj
    record(rid, rel, [chk(rid, inst, CMP, "#")], extra={"comparisonResultId": inst["comparisonResultId"], "counts": inst["descriptor"]["counts"]})
dump("vectors/baseline-e0-e3.json", {"E0": cmp_e0, "E1E3": cmp_e13, "distinction": "E0 is prior detector execution; E1–E3 re-evaluate current retained evidence"})
record("R-E0-VS-E1-E3", "vectors/baseline-e0-e3.json", [chk("e0", cmp_e0, CMP, "#"), chk("e13", cmp_e13, CMP, "#")])

base_desc = {
    "schemaFamily": "opensip.product.baseline", "schemaMajor": 2, "originProjectId": PRJ,
    "source": {"snapshotId": SNAP_SYN}, "runId": RUN_SYN, "planId": PLAN_SYN,
    "fingerprintRecipe": {"domain": "finding-fingerprint", "recipeMajor": 2},
    "detectorClosure": [{"detectorId": "opensip.rules.syntax-pilot", "closureId": CLOSURE, "semanticsMajor": 1, "semanticVersion": "1.0.0", "contributionId": "opensip.rules.syntax-pilot", "manifestDigest": HEX_A}],
    "pivotClosure": [{"closureId": CLOSURE, "kind": "detector", "manifestDigest": HEX_A, "protocolMajor": 1, "platform": "macos-aarch64"}],
    "context": ctx(scope_a_d), "contextDocuments": {"policy": policy, "scope": scope_a, "waivers": waivers},
    "ruleCoverage": [], "entries": [], "unmatchedOccurrences": [],
}
custody = {"exportedByHostRelease": "1.0.0", "exportedAtUtc": "2026-09-08T00:00:00Z", "runRetainedAtExport": True, "retentionPins": [RUN_SYN]}
baseline = finish_baseline(base_desc, custody)
dump("vectors/baseline-audit.json", baseline)
record("R-BASELINE-AUDIT", "vectors/baseline-audit.json", [chk("baseline", baseline, BASE, "#")], extra={"baselineId": baseline["baselineId"]})

auth = {
    "test": failure_envelope(request_id="req1_" + "31" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED", domain=domain_detail("TEST.PRINCIPAL_NOT_ADMITTED", "admit the test principal before test-run")),
    "preparation": failure_envelope(request_id="req1_" + "32" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED", domain=domain_detail("native.execution-not-authorized", "native-prepare is not authorized on this grant")),
    "repair": failure_envelope(request_id="req1_" + "33" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED", domain=domain_detail("AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR", "policy does not admit repair-apply")),
}
dump("vectors/test-prep-repair-authorization.json", auth)
record("R-TEST-PREP-REPAIR-AUTH", "vectors/test-prep-repair-authorization.json", [chk(k, v, CE, "#") for k, v in auth.items()])

# --- multi-unit / candidate-only / host-captured executed records ---
u0 = zero_config_unit(workspace_root=".", advertised=["inventory", "syntax", "clones-near", "clones-cross-tsjs"], installed=["inventory", "syntax"], candidate_only=["clones-near", "clones-cross-tsjs"], candidate_paths={"clones-near": ["src/a.ts"], "clones-cross-tsjs": []})
u1 = zero_config_unit(workspace_root="packages/a", advertised=["inventory", "syntax"], installed=["inventory"], candidate_only=[], candidate_paths={})
multi_unit = {"function": "zero_config_unit over multiple workspace roots", "units": [u0, u1], "synthesizedGraphs": True}
dump("vectors/multi-unit-missing-caps.json", multi_unit)
record("R-MULTI-UNIT-MISSING-CAPS", "vectors/multi-unit-missing-caps.json", [chk("mu0", u0["configGraph"], NATIVE, "#/$defs/TypeScriptConfigGraphV1")])

cand = {
    "function": "candidate-only cells kinds=[] extents=[] with candidateSourcePaths",
    "cells": [c for c in u0["cells"] if c["capabilityId"] in ("clones-near", "clones-cross-tsjs")],
    "notSelectedCompleteClones": True,
    "selector": "enumeration-contract.v1.md candidate-only cells",
}
dump("vectors/candidate-only-clones.json", cand)
record("R-CANDIDATE-ONLY-CLONES", "vectors/candidate-only-clones.json", [], extra={"kindsEmpty": all(c["kinds"] == [] for c in cand["cells"])})

host_obs = {
    "schemaVersion": 1,
    "syntheticHostObservation": True,
    "hostCapture": {"custody": "host-tcb-evidence-store", "observation": "stage-return", "stageReceipts": [{"ordinal": 0, "stage": "enumerate", "status": "returned"}], "hostDerivedRefs": []},
    "selectedRefs": [{"domain": "subject-inventory", "digest": HEX_A}],
    "candidateResultRefs": [{"domain": "candidate-producer-result", "digest": HEX_B}],
    "requiredWork": "selectedRefs + hostCapture.stageReceipts",
    "candidateOnly": "candidateResultRefs; clone cells kinds=[]",
    "distinct": True,
}
dump("vectors/host-captured-vs-candidate.json", {
    "function": "retained observation records (synthetic TCB, labeled)",
    "hostCaptured": host_obs["hostCapture"],
    "selectedRefs": host_obs["selectedRefs"],
    "candidateResultRefs": host_obs["candidateResultRefs"],
    "candidateOnlyCells": cand["cells"],
    "syntheticHostObservation": True,
    "distinct": True,
    "selector": "execution-inputs-contract.v1.md; enumeration-contract.v1.md",
})
record("R-HOST-CAPTURED-VS-CANDIDATE", "vectors/host-captured-vs-candidate.json", [])

# chain: executed traces + envelopes + named frozen Run store bytes. close_run of those stores is pending, not accepted.
frozen_runs = json.loads((OUT / "frozen-run-hashes.json").read_text())["runs"]
trace_complete = OUT / "traces/complete.json"
trace_terminal = OUT / "traces/terminal.json"
chain = {
    "function": "measured reconstruction of zero-config → invocation → envelope → receipt → frozen Run store bytes",
    "selector": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT exhibited by executed traces, envelopes, and complete Runs together, not a checklist sentence",
    "arrows": [
        {"arrow": "zero-config selection", "artifact": "vectors/config-synthesized.json", "measured": g_syn["graphDigestSha256"], "kind": "TypeScriptConfigGraphV1 digest", "role": "workflow-config"},
        {"arrow": "invocation", "artifact": "envelopes/single-step.json", "measured": single["requestId"], "kind": "InvocationRecord requestId", "role": "workflow-envelope"},
        {"arrow": "failure/public envelopes", "artifact": "envelopes/config-input.json", "measured": envelopes["config-input"]["exitCode"], "kind": "derived D9 exitCode", "role": "workflow-envelope"},
        {"arrow": "durable receipt", "artifact": "envelopes/receipt-availability.json", "measured": receipt["inventoryDigest"], "kind": "commit-receipt inventoryDigest", "role": "workflow-envelope"},
        {"arrow": "protocol trace complete", "artifact": "traces/complete.json", "measured": hashlib.sha256(trace_complete.read_bytes()).hexdigest() if trace_complete.exists() else None, "kind": "trace file SHA-256", "role": "workflow-trace"},
        {"arrow": "protocol trace terminal", "artifact": "traces/terminal.json", "measured": hashlib.sha256(trace_terminal.read_bytes()).hexdigest() if trace_terminal.exists() else None, "kind": "trace file SHA-256", "role": "workflow-trace"},
        {"arrow": "frozen syntax-code Run store bytes", "artifact": "runs/syntax-code.store.json", "measured": frozen_runs["syntax-code.store.json"]["sha256"], "kind": "frozen Run object-table+blobs SHA-256", "role": "complete-run-bytes", "closeRun": "pending"},
        {"arrow": "frozen ts Run store bytes", "artifact": "runs/ts.store.json", "measured": frozen_runs["ts.store.json"]["sha256"], "kind": "frozen Run object-table+blobs SHA-256", "role": "complete-run-bytes", "closeRun": "pending"},
        {"arrow": "frozen rust Run store bytes", "artifact": "runs/rust.store.json", "measured": frozen_runs["rust.store.json"]["sha256"], "kind": "frozen Run object-table+blobs SHA-256", "role": "complete-run-bytes", "closeRun": "pending"},
    ],
    "notAChecklistSentence": True,
    "frozenRunAdmission": {
        "status": "pending-final-integration",
        "accepted": False,
        "concreteDependency": "identity-and-evidence.md §3 / identity-schemas.v3 close_run of retained complete Run bytes joined to the already-executed traces and envelopes above. If a later B12-corrected store supersedes the current frozen syntax-code.store.json sha256 2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7, bind that successor store instead of keeping a stale hash. This workflow-scope pass does not rewrite frozen stores and does not claim close_run.",
        "outOfScopeHere": True,
    },
    "preservedOriginalChecklist": "preserved-failures/workflow-review-v2-refused-original/vectors/chain-zero-config-to-receipt.json",
    "preservedPeerRefusedFourArrows": "preserved-failures/workflow-selfaudit-v4-peer-refused/vectors/chain-zero-config-to-receipt.json",
}
dump("vectors/chain-zero-config-to-receipt.json", chain)
record("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "vectors/chain-zero-config-to-receipt.json", [], extra={"measuredArrows": [a["measured"] for a in chain["arrows"]], "pendingCloseRun": True})

# standing content (keep cited, content-reviewed)
dump("vectors/subsystem-owners.json", {
    "CommandEnvelope": "workflows-and-surfaces / evaluator3 command-envelope",
    "InvocationRecord": "evaluator3 invocation-record",
    "StepTermination": "evaluator3 common / inherited d9-exit-contract classToExitCode",
    "ComparisonResult": "evaluator3 comparison-result",
    "BaselineArtifact": "evaluator3 baseline-artifact",
    "TypeScriptConfigGraphV1": "native-evidence.schemas.v2",
    "GraphQuery": "query-projection-contract.v3 + evaluator3 graph-query",
    "RepairPlanV1": "evaluator3 repair",
    "MutationReplayScopeV1": "workflows invocation-record (generic mutation, not repair-apply)",
})
record("R-SUBSYSTEM-OWNERS", "vectors/subsystem-owners.json", [])
dump("vectors/promise-vs-availability.json", {"productPromise": "native-evidence.md advertised cells", "installedAvailability": "capability-manifest + release declaration", "explicitOverrides": "analysis-spec.requestedCapabilities", "semanticPrerequisites": "selected universe / covering program", "distinct": True})
record("R-PROMISE-VS-AVAILABILITY", "vectors/promise-vs-availability.json", [])
dump("vectors/semantic-vs-operational.json", {"semanticIdentities": "run3/proof3/fact2 C/H", "operationalAuthority": "host mutation receipts / grants / leases", "selector": "identity-and-evidence.md §3; security-and-lifecycle", "distinct": True})
record("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/semantic-vs-operational.json", [])
dump("vectors/mutation-vs-analysis-steps.json", {"analysisSealsRun3": True, "mutationDoesNotSealRun3": True, "repairApplyDoesNotSealRun3": True, "verifyAfterApplySealsNewRun": True, "selector": "evaluator3/repair.schema.json; invocation StepKind"})
record("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/mutation-vs-analysis-steps.json", [])
dump("vectors/detector-compat-file.json", {"listingFile": ".opensip/detector-compatibility.json", "not": "component-manifest body (closure.manifestDigest)", "selector": "workflows-and-surfaces.md §2"})
record("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json", [])
empty_inv = {
    "schemaVersion": 1, "planId": PLAN_SYN, "parameterDigest": HEX_A,
    "cellOrdinal": 1, "programOrdinal": 0, "kind": "package",
    "state": "complete", "deficiency": None, "nativeCause": None,
    "examinedPaths": [], "rows": [],
}
partial_inv = {
    "schemaVersion": 1, "planId": PLAN_SYN, "parameterDigest": HEX_A,
    "cellOrdinal": 0, "programOrdinal": 0, "kind": "file",
    "state": "partial", "deficiency": "budget-exhausted", "nativeCause": None,
    "examinedPaths": ["src/lib.rs"],
    "rows": [{"nativeSubjectId": "src/lib.rs", "kind": "file", "path": "src/lib.rs", "qualifiedName": "src/lib.rs", "subjectLanguage": "rust", "signatureTokens": [], "projections": []}],
}
unavail_inv = {
    "schemaVersion": 1, "planId": PLAN_SYN, "parameterDigest": HEX_A,
    "cellOrdinal": 2, "programOrdinal": 0, "kind": "symbol",
    "state": "unavailable", "deficiency": "provider-unavailable", "nativeCause": None,
    "examinedPaths": [], "rows": [],
}
missing_bytes = {
    "condition": "pointer present, object/blob absent",
    "code": "EXECUTION_INPUTS_REF_LOST_BYTES",
    "selector": "execution-inputs-contract.v1.md §2",
    "pointer": {"domain": "subject-inventory", "digest": HEX_D},
    "blobPresent": False,
    "notANarrativeLabel": True,
}
for label, inst in [("empty-pkg", empty_inv), ("partial-file", partial_inv), ("unavail-symbol", unavail_inv)]:
    chk(label, inst, "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json", "#")
dump("vectors/empty-partial-unavailable-missing.json", {
    "selector": "enumeration-contract.v1.md; execution-inputs-contract.v1.md §2; subject-inventory.schema.v1.json",
    "completeEmpty": empty_inv,
    "partial": partial_inv,
    "unavailable": unavail_inv,
    "missingCommittedBytes": missing_bytes,
    "distinctStates": sorted({empty_inv["state"], partial_inv["state"], unavail_inv["state"], "lost-bytes"}),
    "distinct": True,
    "notASingleLabel": True,
    "preservedPeerRefusedNarratives": "preserved-failures/workflow-selfaudit-v4-peer-refused/vectors/empty-partial-unavailable-missing.json",
})
record("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json", [])

# --- graph query: projectable calls@resolved-callee, plus RELATION_UNSUPPORTED failure ---
UNI = HEX_A
def ep(name):
    return {"universe": UNI, "kind": "symbol", "nativeSubjectId": name}

def mint_fact(i, caller, callee):
    rec = {"schemaVersion": 1, "relation": "calls", "resolution": "resolved-callee", "sourceUniverse": UNI, "targetUniverse": UNI, "producerClosure": CLOSURE, "payload": {"caller": caller, "resolvedCallee": callee}, "ordinal": i}
    fid = "fact2:" + H("fact", rec)
    return {"factId": fid, "relation": "calls", "resolution": "resolved-callee", "sourceUniverse": UNI, "targetUniverse": UNI, "producerClosure": CLOSURE, "payload": rec["payload"], "record": rec}

facts = [mint_fact(0, "mod.a", "mod.b"), mint_fact(1, "mod.a", "mod.c"), mint_fact(2, "mod.b", "mod.c")]
facts.sort(key=lambda f: f["factId"])
edges = project_edges(facts, relation="calls", min_resolution="resolved-callee")
cov_rec = {"schemaVersion": 1, "relation": "calls", "resolution": "resolved-callee", "coverage": "complete"}
cov_id = "coverage2:" + H("coverage", cov_rec)
scope_id = "scope2:" + H("subject-scope", {"schemaVersion": 1, "include": ["**/*"]})
view_id = "view2:" + H("view", {"schemaVersion": 1, "facts": [f["factId"] for f in facts]})

nb = neighbors(edges=edges, endpoint=ep("mod.a"), direction="outgoing")
path_ac = shortest_path(edges=edges, start=ep("mod.a"), target=ep("mod.c"), max_depth=8)
path_zero = shortest_path(edges=edges, start=ep("mod.a"), target=ep("mod.a"), max_depth=8)
reach_rows = reach(edges=edges, start=ep("mod.a"), max_depth=8, include_start=True)
sel = selection_hash(project_id=PRJ, run_id=RUN_TS, fact_view_digests=[view_id], operation="graph.neighbors", params={"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("mod.a")})
page0, restpos = page_items(nb, size=1, position=0)
next_c = cursor_token(run_id=RUN_TS, selection=sel, position=int(restpos)) if restpos is not None else None

def gq_req(op, params, page):
    return {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "projectId": PRJ, "view": {"runId": RUN_TS}, "operation": op, "params": params, "completeness": "best-effort", "page": page}

def gq_ctx(*, total, produced, truncated, traversal_coverage, count_basis, nxt=None, visited=None):
    ctx = {
        "projectId": PRJ, "resolvedView": {"runId": RUN_TS}, "factViewDigests": [view_id],
        "availability": "retained", "truncated": truncated, "totalItems": total, "countBasis": count_basis,
        "traversalCoverage": traversal_coverage,
        "visitedNodes": visited if visited is not None else max(1, produced),
        "producedItems": produced, "advisory": False,
        "evidence": {"coverageIds": [cov_id], "scopeIds": [scope_id], "deficiencyCitations": [], "resolutionLimitations": []},
    }
    if nxt:
        ctx["nextCursor"] = nxt
    return ctx

def gq_resp(op, items, ctx):
    return {"schemaFamily": "opensip.product.query", "schemaMajor": 3, "operation": op, "context": ctx, "items": items}

nb_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "endpoint": ep("mod.a")}
path_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("mod.a"), "target": ep("mod.c"), "maxDepth": 8}
path0_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("mod.a"), "target": ep("mod.a"), "maxDepth": 1}
reach_params = {"relation": "calls", "minResolution": "resolved-callee", "direction": "outgoing", "start": ep("mod.a"), "maxDepth": 8, "includeStart": True}

req_nb = gq_req("graph.neighbors", nb_params, {"size": 100})
req_path = gq_req("graph.path", path_params, {"size": 1})
req_path0 = gq_req("graph.path", path0_params, {"size": 1})
req_reach = gq_req("graph.reach", reach_params, {"size": 100})
req_page = gq_req("graph.neighbors", nb_params, {"size": 1})
req_page2 = gq_req("graph.neighbors", nb_params, {"size": 1, "cursor": next_c})
page1, restpos2 = page_items(nb, size=1, position=int(restpos) if restpos is not None else 1)
next_c2 = cursor_token(run_id=RUN_TS, selection=sel, position=int(restpos2)) if restpos2 is not None else None
resp_nb = gq_resp("graph.neighbors", nb, gq_ctx(total=len(nb), produced=len(nb), truncated=False, traversal_coverage="complete", count_basis="exact", visited=1))
resp_path = gq_resp("graph.path", [path_ac], gq_ctx(total=1, produced=1, truncated=False, traversal_coverage="complete", count_basis="exact", visited=path_ac["hopCount"] + 1))
resp_path0 = gq_resp("graph.path", [path_zero], gq_ctx(total=1, produced=1, truncated=False, traversal_coverage="complete", count_basis="exact", visited=1))
resp_reach = gq_resp("graph.reach", reach_rows, gq_ctx(total=len(reach_rows), produced=len(reach_rows), truncated=False, traversal_coverage="complete", count_basis="exact", visited=len(reach_rows)))
resp_page = gq_resp("graph.neighbors", page0, gq_ctx(total=len(nb), produced=len(page0), truncated=False, traversal_coverage="truncated-page", count_basis="exact", nxt=next_c, visited=1))
resp_page2 = gq_resp("graph.neighbors", page1, gq_ctx(total=len(nb), produced=len(page1), truncated=False, traversal_coverage="complete", count_basis="exact", nxt=next_c2, visited=1))

# unsupported relation failure (not a success body)
unsup_req = gq_req("graph.neighbors", {"relation": "file", "minResolution": "enumerated", "direction": "outgoing", "endpoint": {"universe": UNI, "kind": "file", "nativeSubjectId": "src/index.ts"}}, {"size": 100})
unsup = catch(lambda: project_edges([], relation="file", min_resolution="enumerated"))
fail_rel = failure_envelope(
    request_id="req1_" + "41" * 16, klass="request-rejected", error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail("QUERY.RELATION_UNSUPPORTED", "file@enumerated is not graph-projectable"),
)

parity = render_parity(resp_nb, qcmd.get("formats") or ["human", "json", "agent"])

gq_bundle = {
    "underlyingRunAdmissionUnverified": True,
    "didNotClaimCloseRun": True,
    "runId": RUN_TS,
    "viewId": view_id,
    "projectableRelation": ["calls", "resolved-callee"],
    "syntheticFacts": facts,
    "coverageId": cov_id,
    "scopeId": scope_id,
    "requests": {"neighbors": req_nb, "path": req_path, "pathZeroHop": req_path0, "reach": req_reach, "neighborsPaged": req_page, "neighborsPage2": req_page2, "unsupportedFileEnumerated": unsup_req},
    "responses": {"neighbors": resp_nb, "path": resp_path, "pathZeroHop": resp_path0, "reach": resp_reach, "neighborsPaged": resp_page, "neighborsPage2": resp_page2},
    "failureEnvelope": fail_rel,
    "unsupportedRelationRefusal": unsup,
    "rendererParity": {"formats": qcmd.get("formats"), "parityFields": qcmd.get("parityFields"), "rendered": parity},
    "cursor": {
        "requestPageSize": 1,
        "nextCursor": next_c,
        "page2Cursor": next_c,
        "page2NextCursor": next_c2,
        "form": "q3.<runId-64hex>.<selectionHash64>.<position>",
        "selectionHash": sel,
        "remainingNeighborFactId": (page1[0]["factId"] if page1 else None),
        "pageFullnessLaw": "truncated-page with truncated=false",
    },
    "preservedOriginalUnsupportedSuccess": "preserved-failures/workflow-review-v2-refused-original/query/graph-query-bundle.json",
    "preservedPeerRefusedParity": "preserved-failures/workflow-selfaudit-v4-peer-refused/query/parity.json",
}
dump("query/graph-query-bundle.json", gq_bundle)
dump("query/graph-neighbors.json", {"request": req_nb, "response": resp_nb, "underlyingRunAdmissionUnverified": True})
dump("query/graph-path.json", {"request": req_path, "response": resp_path, "zeroHop": False, "nontrivialHopCount": path_ac["hopCount"], "underlyingRunAdmissionUnverified": True})
dump("query/graph-reach.json", {"request": req_reach, "response": resp_reach, "includeStart": True, "underlyingRunAdmissionUnverified": True})
dump("query/measured-neighbors.json", {"edges": edges, "neighborsOfA": nb, "underlyingRunAdmissionUnverified": True})
dump("query/parity.json", {"formats": qcmd.get("formats"), "parityFields": qcmd.get("parityFields"), "rendered": parity, "source": "command-inventory.v3 query command"})
dump("query/failures.json", fail_rel)

for label, inst, sel in [
    ("gq-req-nb", req_nb, "#/$defs/GraphQueryRequestV1"),
    ("gq-req-path", req_path, "#/$defs/GraphQueryRequestV1"),
    ("gq-req-reach", req_reach, "#/$defs/GraphQueryRequestV1"),
    ("gq-resp-nb", resp_nb, "#/$defs/GraphQueryResponseV1"),
    ("gq-resp-path", resp_path, "#/$defs/GraphQueryResponseV1"),
    ("gq-resp-reach", resp_reach, "#/$defs/GraphQueryResponseV1"),
    ("gq-resp-page", resp_page, "#/$defs/GraphQueryResponseV1"),
    ("gq-resp-page2", resp_page2, "#/$defs/GraphQueryResponseV1"),
    ("gq-fail", fail_rel, None),
]:
    schema, selector = (CE, "#") if label == "gq-fail" else (GQ, sel)
    chk(label, inst, schema, selector)
record("R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR", "query/graph-query-bundle.json", [], extra={
    "executed": False,
    "status": "incomplete-pending-admitted-run",
    "projectable": True,
    "pathHops": path_ac["hopCount"],
    "nextCursor": next_c,
    "coverageIds": [cov_id],
    "note": "Algorithmic vectors retained. Charter requires reconstruction over already admitted retained Run(s). close_run of frozen stores is unverified; execute_graph_query without close_run refuses QUERY.VIEW_UNKNOWN. Do not claim this ID executed.",
})

# freeze check
frozen = json.loads((OUT / "frozen-run-hashes.json").read_text())
for name, exp in frozen["runs"].items():
    b = (OUT / "runs" / name).read_bytes()
    got = hashlib.sha256(b).hexdigest()
    if got != exp["sha256"] or len(b) != exp["bytes"]:
        raise SystemExit(f"FROZEN_STORE_MUTATED {name}")

dump("workflow-correct-results.json", {"results": results, "n": len(results), "frozenRunHashes": frozen["runs"]})
print("DONE", len(results))
for r in results:
    print(r["id"], r["artifact"])
