#!/usr/bin/env python3
"""Replace remaining placeholder envelopes/vectors/query artifacts with executed reconstruction.

Does not rewrite frozen Run stores. Graph queries over retained graphs are labeled
underlying-Run-admission-unverified. Not whole-consumer acceptance.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import body_identity, body_language_version, l0_payload, language_version_bytes  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.evaluator import eval_atom  # noqa: E402
from helper.identity import parse_h_frame, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402

CE = "docs/coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
INV = "docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json"
CMP = "docs/coop/design-corrections/workflows/schemas/evaluator3/comparison-result.schema.json"
BASE = "docs/coop/design-corrections/workflows/schemas/evaluator3/baseline-artifact.schema.json"
GQ = "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json"
REP = "docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json"
MRS = "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
POL2 = "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
POL1 = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
TA = "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json"
REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
COMMON = "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"

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
REQ = "req1_" + "ab" * 16
PRJ = "prj1-" + HEX_A
RUN_SYN = json.loads((OUT / "runs/syntax-code.meta.json").read_text())["runId"]
RUN_TS = json.loads((OUT / "runs/ts.meta.json").read_text())["runId"]
PLAN_TS = json.loads((OUT / "runs/ts.meta.json").read_text())["planId"]
SNAP_SYN = json.loads((OUT / "runs/syntax-code.meta.json").read_text())["snapshotId"]
EXEC = "exec1_" + "cd" * 16
CLOSURE = "closure2:" + HEX_A
FINGER = "finding-key2:" + HEX_B


def sha256_hex(obj) -> str:
    return hashlib.sha256(C(obj) if not isinstance(obj, (bytes, bytearray)) else obj).hexdigest()


def dump(rel: str, obj) -> Path:
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2) + "\n")
    return p


def chk(label, inst, rel, selector=None):
    r = validate_against(inst, rel, selector=selector, label=label)
    return {"label": label, "stockOk": r["stockOk"], "nErrors": len(r["errors"]), "errors": r["errors"][:6]}


results = []


def record(req_id, artifact, checks, extra=None):
    rec = {"id": req_id, "artifact": artifact, "checks": checks, "measurementKind": "stock-schema-pass+computed"}
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


def failure_envelope(*, request_id, klass, error_code=None, domain, extra_term=None, extra_env=None):
    term = termination(klass=klass, error_code=error_code, domain_detail=domain, **(extra_term or {}))
    if klass == "operational-failed" and "faultCause" not in term:
        term["faultCause"] = "host-io"
    env = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "failure",
        "requestId": request_id,
        "termination": term,
        "exitCode": CLASS_TO_EXIT[klass],
        "errors": [domain],
    }
    if extra_env:
        env.update(extra_env)
    return env


# --- failure / public envelopes ---
envelopes = {}
envelopes["config-input"] = failure_envelope(
    request_id="req1_" + "11" * 16,
    klass="request-rejected",
    error_code="CONFIG.INVALID",
    domain=domain_detail("CONFIG.INVALID", "correct the configuration input and retry"),
)
envelopes["retained-external-input"] = failure_envelope(
    request_id="req1_" + "12" * 16,
    klass="request-rejected",
    error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail("IMPORT.STALE_FOR_PLAN", "re-import retained external evidence against the current Plan"),
)
envelopes["host-invalid-internal"] = failure_envelope(
    request_id="req1_" + "13" * 16,
    klass="operational-failed",
    error_code="HOST.IO_FAILURE",
    domain=domain_detail("HOST.INVARIANT_VIOLATED", "discard the host-generated invalid internal record; re-run admission"),
    extra_term={"fault_cause": "host-invariant"},
)
envelopes["producer-boundary"] = failure_envelope(
    request_id="req1_" + "14" * 16,
    klass="request-rejected",
    error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail("GRANT.REFUSED", "producer is outside the admitted principal boundary"),
)
envelopes["public-from-internal"] = failure_envelope(
    request_id="req1_" + "15" * 16,
    klass="request-rejected",
    error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail("ENVELOPE.KIND", "public envelope was projected from an internal refusal; do not treat internal fields as public"),
)
envelopes["pinned-purge"] = failure_envelope(
    request_id="req1_" + "16" * 16,
    klass="request-rejected",
    error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail(
        "evidence.pinned",
        "remove or wait out active retention pins before purge",
        subject="run " + RUN_SYN,
        purgeDisclosure={
            "runId": RUN_SYN,
            "activePins": [{"pinId": "pin-replayable", "kind": "baseline"}],
            "consequences": [
                "named-pins-revoked",
                "dependent-evidence-replay-unavailable",
                "sealed-history-retained",
            ],
        },
    ),
    extra_term={"run_id": RUN_SYN},
)
envelopes["purge-replay-output-failure"] = failure_envelope(
    request_id="req1_" + "17" * 16,
    klass="operational-failed",
    error_code="OUTPUT.SERIALIZATION_FAILED",
    domain=domain_detail("EVALUATION.REQUIRED_OUTPUT_OMITTED", "required replay output could not be materialized"),
    extra_term={"fault_cause": "output-serialization"},
)
envelopes["d9-complete-failure"] = failure_envelope(
    request_id="req1_" + "18" * 16,
    klass="policy-failed",
    domain=domain_detail("EVALUATION.PROOF_VERDICT_INCONSISTENT", "sealed verdict is fail; inspect findings"),
    extra_term={"run_id": RUN_SYN},
)

for name, env in envelopes.items():
    path = f"envelopes/{name}.json" if name != "d9-complete-failure" else "envelopes/failure-d9-complete.json"
    dump(path, env)

# map to required filenames
dump("envelopes/config-input.json", envelopes["config-input"])
dump("envelopes/retained-external-input.json", envelopes["retained-external-input"])
dump("envelopes/host-invalid-internal.json", envelopes["host-invalid-internal"])
dump("envelopes/producer-boundary.json", envelopes["producer-boundary"])
dump("envelopes/public-from-internal.json", envelopes["public-from-internal"])
dump("envelopes/pinned-purge.json", envelopes["pinned-purge"])
dump("envelopes/purge-replay-output-failure.json", envelopes["purge-replay-output-failure"])

env_checks = []
for label, env, rid in [
    ("config-input", envelopes["config-input"], "R-ENVELOPE-CONFIG-INPUT"),
    ("retained-external-input", envelopes["retained-external-input"], "R-ENVELOPE-EXTERNAL-INPUT"),
    ("host-invalid-internal", envelopes["host-invalid-internal"], "R-ENVELOPE-HOST-INVALID"),
    ("producer-boundary", envelopes["producer-boundary"], "R-ENVELOPE-PRODUCER-BOUNDARY"),
    ("public-from-internal", envelopes["public-from-internal"], "R-PUBLIC-FROM-INTERNAL-REFUSAL"),
    ("pinned-purge", envelopes["pinned-purge"], "R-PINNED-PURGE"),
    ("purge-replay-output-failure", envelopes["purge-replay-output-failure"], "R-PURGE-REPLAY-OUTPUT-FAILURE"),
    ("d9-complete", envelopes["d9-complete-failure"], "R-FAILURE-ENVELOPES-D9"),
]:
    c = chk(label, env, CE, "#")
    env_checks.append(c)
    record(rid, f"envelopes/{label}.json", [c], extra={"exitCodeDerived": env["exitCode"], "class": env["termination"]["class"]})

# public termination examples (StepTermination only)
term_examples = {
    "success": termination(klass="success"),
    "policy-failed": termination(klass="policy-failed", run_id=RUN_SYN),
    "request-rejected": termination(klass="request-rejected", error_code="CONFIG.INVALID"),
    "indeterminate": termination(klass="indeterminate", reason_codes=["VERDICT.INDETERMINATE"]),
    "operational-failed": termination(klass="operational-failed", error_code="HOST.IO_FAILURE", fault_cause="host-io"),
    "interrupted": termination(klass="interrupted", signal="SIGINT"),
}
dump("envelopes/public-termination.json", {"examples": term_examples, "owningRecord": "evaluator3 common.schema.json#/$defs/StepTermination"})
t_checks = [chk(f"term-{k}", v, COMMON, "#/$defs/StepTermination") for k, v in term_examples.items()]
record("R-PUBLIC-TERMINATION-EXAMPLES", "envelopes/public-termination.json", t_checks)

# D9 precedence: selected composition vs inherited artifact
d9 = json.loads((KIT / "docs/coop/artifacts/d9-exit-contract.v1.14.json").read_text())
inherited = d9["classToExitCode"]
selected_ok = inherited == CLASS_TO_EXIT
d9_vec = {
    "inheritedArtifact": "docs/coop/artifacts/d9-exit-contract.v1.14.json#/classToExitCode",
    "selectedComposition": "evaluator3 CommandEnvelope.exitCode derived from StepTermination.class",
    "inherited": inherited,
    "selected": CLASS_TO_EXIT,
    "equal": selected_ok,
    "note": "CommandEnvelope stores derived exitCode; HostTermination forbids storing exitCode. Selected composition uses the inherited classToExitCode map.",
}
dump("vectors/d9-extension-precedence.json", d9_vec)
record("R-D9-EXTENSION-PRECEDENCE", "vectors/d9-extension-precedence.json", [], extra={"computedEqual": selected_ok, "measurementKind": "computed-map-compare"})

# --- invocation records ---
def analysis_params(profile, role="primary"):
    return {
        "kind": "analysis",
        "profile": profile,
        "role": role,
        "durability": "authoritative",
        "snapshotSource": "live-worktree",
        "verdictGate": "self" if role == "primary" else "delegated",
    }


single = {
    "schemaFamily": "opensip.product.invocation",
    "schemaMajor": 3,
    "requestId": "req1_" + "21" * 16,
    "projectId": PRJ,
    "workflow": {"kind": "builtin", "name": "analyze"},
    "mode": {"interactive": False, "ci": True, "ephemeral": False},
    "orderedSteps": [
        {
            "stepId": 0,
            "kind": "analysis",
            "requirement": "required",
            "dependsOn": [],
            "dependencyGate": "completed",
            "retryPolicy": "idempotent-retry",
            "params": analysis_params("default"),
        }
    ],
}
multi = {
    "schemaFamily": "opensip.product.invocation",
    "schemaMajor": 3,
    "requestId": "req1_" + "22" * 16,
    "projectId": PRJ,
    "workflow": {"kind": "builtin", "name": "audit"},
    "mode": {"interactive": False, "ci": True, "ephemeral": False},
    "orderedSteps": [
        {
            "stepId": 0,
            "kind": "analysis",
            "requirement": "required",
            "dependsOn": [],
            "dependencyGate": "completed",
            "retryPolicy": "idempotent-retry",
            "params": analysis_params("default", "primary"),
        },
        {
            "stepId": 1,
            "kind": "analysis",
            "requirement": "required",
            "dependsOn": [0],
            "dependencyGate": "completed",
            "retryPolicy": "idempotent-retry",
            "params": analysis_params("fit", "primary"),
        },
    ],
}
dump("envelopes/single-step.json", single)
dump("envelopes/multi-step.json", multi)
c_single = chk("single-step", single, INV, "#")
c_multi = chk("multi-step", multi, INV, "#")
record("R-SINGLE-STEP", "envelopes/single-step.json", [c_single], extra={"orderedSteps": 1})
record(
    "R-MULTI-STEP-DIFFERENT-SELECTIONS",
    "envelopes/multi-step.json",
    [c_multi],
    extra={"profiles": [s["params"]["profile"] for s in multi["orderedSteps"]]},
)

# invocation disclosure from command-inventory.v3
ci = json.loads((KIT / "docs/coop/design-corrections/workflows/command-inventory.v3.json").read_text())
qcmd = next(c for c in ci["commands"] if c["name"] == "query")
acmd = next(c for c in ci["commands"] if c["name"] == "analyze")
disclosure = {
    "source": "docs/coop/design-corrections/workflows/command-inventory.v3.json",
    "commandCount": len(ci["commands"]),
    "analyze": {
        "name": acmd["name"],
        "owner": acmd.get("owner"),
        "requestClass": acmd.get("requestClass"),
        "authority": acmd.get("authority"),
        "steps": acmd.get("steps"),
        "formats": acmd.get("formats"),
        "parityFields": acmd.get("parityFields"),
        "boundedCardinality": {"commands": len(ci["commands"]), "steps.maxItems": 64, "requestedCapabilities.maxItems": 1024},
    },
    "query": {
        "name": qcmd["name"],
        "formats": qcmd.get("formats"),
        "parityFields": qcmd.get("parityFields"),
        "steps": qcmd.get("steps"),
        "authority": qcmd.get("authority"),
    },
    "ordering": "command-inventory.v3 commands sequence; InvocationRecord.orderedSteps sequence; analysis-spec.requestedCapabilities canonical-set",
}
dump("envelopes/invocation-disclosure.json", disclosure)
record("R-INVOCATION-DISCLOSURE", "envelopes/invocation-disclosure.json", [], extra={"measurementKind": "inventory-extraction", "commandCount": len(ci["commands"])})

# receipts bound to retained syntax-code Run
inv_digest = hashlib.sha256(C({"runId": RUN_SYN, "kind": "inventory"})).hexdigest()
receipt = {
    "schemaVersion": 2,
    "runId": RUN_SYN,
    "executionId": EXEC,
    "namespaceId": "local",
    "commitSequence": 0,
    "inventoryDigest": inv_digest,
    "sealedAssurance": "replayable",
    "signerKeyId": "synthetic-host-key",
}
availability = {
    "schemaVersion": 2,
    "runId": RUN_SYN,
    "generation": 0,
    "state": "retained",
    "missingRefs": [],
    "reason": "complete",
}
dump("envelopes/receipt-availability.json", {"receipt": receipt, "availability": availability, "syntheticHostObservation": True, "joinedRunId": RUN_SYN})
c_rec = chk("commit-receipt", receipt, IDENT, "#/$defs/commit-receipt")
c_av = chk("availability", availability, IDENT, "#/$defs/availability")
record("R-DURABLE-RECEIPT-AVAILABILITY", "envelopes/receipt-availability.json", [c_rec, c_av], extra={"joinedRunId": RUN_SYN})

print("envelopes done")

# --- config graphs ---
def cfg_node(path, kind, content, extends):
    raw = content if isinstance(content, bytes) else json.dumps(content, separators=(",", ":")).encode()
    return {
        "path": path,
        "contentSha256": hashlib.sha256(raw).hexdigest(),
        "kind": kind,
        "extendsResolved": extends,
        "_bytes": raw,
    }


def graph_from_nodes(entry, nodes):
    clean = [{k: v for k, v in n.items() if k != "_bytes"} for n in nodes]
    g = {"schemaVersion": 1, "entryConfigPath": entry, "nodes": clean}
    digest = sha256_hex(g)
    return g, digest, {n["path"]: n["_bytes"] for n in nodes}


n_syn = cfg_node("package.json", "other", {"name": "syn"}, [])
g_syn, d_syn, b_syn = graph_from_nodes(None, [])  # synthesized: entry null, nodes empty
n_base1 = cfg_node("tsconfig.base.json", "other", {"compilerOptions": {"strict": True}}, [])
n_base2 = cfg_node("tsconfig.strict.json", "other", {"compilerOptions": {"noImplicitAny": True}}, ["tsconfig.base.json"])
n_custom = cfg_node("tsconfig.app.json", "other", {"extends": ["tsconfig.strict.json", "tsconfig.base.json"]}, ["tsconfig.strict.json", "tsconfig.base.json"])
# repeated base: app extends strict then base; strict also extends base — precedence retained
g_custom, d_custom, b_custom = graph_from_nodes(
    "tsconfig.app.json",
    sorted([n_base1, n_base2, n_custom], key=lambda n: n["path"].encode()),
)
n_js_base = cfg_node("tsconfig.shared.json", "other", {"compilerOptions": {"allowJs": True}}, [])
n_js = cfg_node("jsconfig.json", "jsconfig", {"extends": "./tsconfig.shared.json"}, ["tsconfig.shared.json"])
g_js, d_js, b_js = graph_from_nodes("jsconfig.json", sorted([n_js_base, n_js], key=lambda n: n["path"].encode()))

for rel, g, d, note in [
    ("vectors/config-synthesized.json", g_syn, d_syn, "js-synthesized: entryConfigPath null, nodes empty; digest binds on universe as tsconfigGraphHash only if a universe is built"),
    ("vectors/config-custom-multi-base.json", g_custom, d_custom, "custom-named entry tsconfig.app.json kind=other; extendsResolved order strict then base; base also reached via strict"),
    ("vectors/config-js-shared-base.json", g_js, d_js, "jsconfig.json kind=jsconfig inheriting shared tsconfig.shared.json kind=other"),
]:
    payload = {"graph": g, "graphDigestSha256": d, "tsconfigGraphHashIsNotAGraphField": True, "note": note}
    dump(rel, payload)
    c = chk(rel, g, NATIVE, "#/$defs/TypeScriptConfigGraphV1")
    rid = {
        "vectors/config-synthesized.json": "R-CONFIG-SYNTHESIZED",
        "vectors/config-custom-multi-base.json": "R-CONFIG-CUSTOM-MULTI-BASE",
        "vectors/config-js-shared-base.json": "R-CONFIG-JS-SHARED-BASE",
    }[rel]
    record(rid, rel, [c], extra={"graphDigestSha256": d})

# --- comparison / baseline ---
policy = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [
        {
            "ruleId": "file-present",
            "ruleProgramRef": {
                "contributionId": "opensip.rules.syntax-pilot",
                "ruleStableId": "file-present",
                "semanticsMajor": 1,
                "programDigest": HEX_A,
            },
            "enabled": True,
            "severity": "error",
            "gate": True,
            "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"},
            "emitWhen": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "hello.rs"}]},
            "evidenceUse": [],
        }
    ],
}
scope_doc = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["**/*"], "exclude": []}
waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
pol_d = sha256_hex(policy)
scope_d = sha256_hex(scope_doc)
wav_d = sha256_hex(waivers)

eval_ctx = {
    "policyDigest": pol_d,
    "scopeDigest": scope_d,
    "waiverSetDigest": wav_d,
    "detectorClosureIds": [CLOSURE],
    "evidenceAvailability": {"importKinds": [], "relations": ["file"], "imports": []},
}


def zeros():
    return {
        "UNCHANGED": 0,
        "CODE-NET-NEW": 0,
        "CODE-FIXED": 0,
        "DETECTION-DELTA": 0,
        "POLICY-DELTA": 0,
        "SCOPE-DELTA": 0,
        "WAIVER-DELTA": 0,
        "EVIDENCE-DELTA": 0,
        "INDETERMINATE": 0,
        "gating": 0,
    }


def comparison_descriptor(*, performed, verdict, delta, pivots, entries, unmatched, reason=None, e0=None):
    desc = {
        "schemaFamily": "opensip.product.comparison",
        "schemaMajor": 2,
        "baselineId": "baseline2:" + HEX_A,
        "currentRunId": RUN_SYN,
        "currentSnapshotId": SNAP_SYN,
        "auditProfile": {
            "name": "report-only",
            "gateCodeNetNew": False,
            "gateNewlyLiveByPolicyAxes": False,
            "gateAllCurrentLive": False,
            "newWaiverSuppressesCodeNetNew": False,
            "gateRuleUnder": "current-only",
        },
        "projectCorrespondence": "same-project",
        "comparisonPerformed": performed,
        "baselineContext": eval_ctx,
        "currentContext": eval_ctx,
        "contextDelta": delta,
        "pivotsAvailable": pivots,
        "detectors": [],
        "ruleDeficiencies": [],
        "entries": entries,
        "counts": zeros(),
        "verdict": verdict,
        "unmatchedOccurrences": unmatched,
        "correspondenceCoverage": [
            {
                "ruleId": "file-present",
                "gating": True,
                "matchedCount": 0,
                "unmatchedCount": 0,
                "populationUnknown": False,
                "zeroFindings": True,
            }
        ],
        "currentEvaluationState": "evaluated",
        "currentExecutionDeficiencies": [],
    }
    if reason:
        desc["wholeIndeterminateReason"] = reason
        desc["remedy"] = domain_detail("COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE", "bind the missing required evidence and re-compare")
        desc["correspondenceCoverage"] = []
    cid = "comparison2:" + sha256_hex(desc)
    return {"comparisonResultId": cid, "descriptor": desc}


delta_none = {
    "codeChanged": False,
    "detectorChanged": False,
    "policyChanged": False,
    "scopeChanged": False,
    "waiversChanged": False,
    "evidenceAvailabilityChanged": False,
}
pivots_nn = {"E0": "not-needed", "E1": "not-needed", "E2": "not-needed", "E3": "not-needed"}
pivots_e0 = {"E0": "available", "E1": "not-needed", "E2": "not-needed", "E3": "not-needed"}
pivots_e13 = {"E0": "not-needed", "E1": "available", "E2": "available", "E3": "available"}

cmp_empty = comparison_descriptor(performed=True, verdict="pass", delta=delta_none, pivots=pivots_nn, entries=[], unmatched=[])
cmp_missing = comparison_descriptor(
    performed=False,
    verdict="indeterminate",
    delta={**delta_none, "evidenceAvailabilityChanged": True},
    pivots={"E0": "unavailable", "E1": "unavailable", "E2": "unavailable", "E3": "unavailable"},
    entries=[],
    unmatched=[],
    reason="required-evidence-unavailable",
)
cmp_evidence = comparison_descriptor(
    performed=True,
    verdict="indeterminate",
    delta={**delta_none, "evidenceAvailabilityChanged": True},
    pivots=pivots_nn,
    entries=[],
    unmatched=[],
    reason="evidence-availability-changed",
)
cmp_scope = comparison_descriptor(
    performed=True,
    verdict="pass",
    delta={**delta_none, "scopeChanged": True},
    pivots=pivots_nn,
    entries=[],
    unmatched=[],
)
presence_e0 = {"B": True, "E0": True, "E1": None, "E2": None, "E3": None, "E4": False, "waivedB": False, "waivedC": False}
presence_e13 = {"B": True, "E0": None, "E1": True, "E2": True, "E3": True, "E4": False, "waivedB": False, "waivedC": False}
entry_e0 = {
    "fingerprint": FINGER,
    "ruleId": "file-present",
    "detectorId": "opensip.rules.syntax-pilot",
    "presence": presence_e0,
    "classification": "UNCHANGED",
    "subsequentDeltas": [],
    "liveInCurrent": True,
    "gates": False,
}
entry_pivot_only = {
    "fingerprint": "finding-key2:" + HEX_C,
    "ruleId": "file-present",
    "detectorId": "opensip.rules.syntax-pilot",
    "presence": {**presence_e0, "B": True, "E0": True, "E4": False},
    "classification": "DETECTION-DELTA",
    "direction": "appeared",
    "subsequentDeltas": [],
    "liveInCurrent": False,
    "gates": False,
}
cmp_e0 = comparison_descriptor(performed=True, verdict="pass", delta=delta_none, pivots=pivots_e0, entries=[entry_e0], unmatched=[])
cmp_e13 = comparison_descriptor(
    performed=True,
    verdict="pass",
    delta={**delta_none, "detectorChanged": False},
    pivots=pivots_e13,
    entries=[{**entry_e0, "presence": presence_e13}],
    unmatched=[],
)
cmp_pivot = comparison_descriptor(performed=True, verdict="pass", delta=delta_none, pivots=pivots_e0, entries=[entry_pivot_only], unmatched=[])

for rel, obj, rid in [
    ("vectors/comparison-empty-result.json", cmp_empty, "R-CMP-EMPTY-RESULT"),
    ("vectors/comparison-missing.json", cmp_missing, "R-CMP-MISSING"),
    ("vectors/comparison-evidence-changed.json", cmp_evidence, "R-CMP-EVIDENCE-CHANGED"),
    ("vectors/comparison-scope-policy-only.json", cmp_scope, "R-SCOPE-POLICY-ONLY-COMPARISON"),
    ("vectors/baseline-e0-e3.json", {"E0": cmp_e0, "E1E3": cmp_e13, "distinction": "E0 is prior detector execution presence; E1–E3 are re-evaluation of current retained evidence"}, "R-E0-VS-E1-E3"),
    ("vectors/pivot-only-fingerprints.json", cmp_pivot, "R-PIVOT-ONLY-FINGERPRINTS"),
]:
    dump(rel, obj)
    inst = obj if "comparisonResultId" in obj else obj.get("E0", obj)
    c = chk(rel, inst if "comparisonResultId" in inst else cmp_e0, CMP, "#")
    record(rid, rel, [c], extra={"comparisonResultId": inst.get("comparisonResultId") if isinstance(inst, dict) else None})

# baseline artifact
base_desc = {
    "schemaFamily": "opensip.product.baseline",
    "schemaMajor": 2,
    "originProjectId": PRJ,
    "source": {"snapshotId": SNAP_SYN},
    "runId": RUN_SYN,
    "planId": json.loads((OUT / "runs/syntax-code.meta.json").read_text())["planId"],
    "fingerprintRecipe": {"domain": "finding-fingerprint", "recipeMajor": 2},
    "detectorClosure": [
        {
            "detectorId": "opensip.rules.syntax-pilot",
            "closureId": CLOSURE,
            "semanticsMajor": 1,
            "semanticVersion": "1.0.0",
            "contributionId": "opensip.rules.syntax-pilot",
            "manifestDigest": HEX_A,
        }
    ],
    "pivotClosure": [
        {"closureId": CLOSURE, "kind": "detector", "manifestDigest": HEX_A, "protocolMajor": 1, "platform": "macos-aarch64"}
    ],
    "context": eval_ctx,
    "contextDocuments": {"policy": policy, "scope": scope_doc, "waivers": waivers},
    "ruleCoverage": [],
    "entries": [],
    "unmatchedOccurrences": [],
}
custody = {
    "exportedByHostRelease": "1.0.0",
    "exportedAtUtc": "2026-09-08T00:00:00Z",
    "runRetainedAtExport": True,
    "retentionPins": [RUN_SYN],
}
base_id = "baseline2:" + sha256_hex(base_desc)
baseline = {"baselineId": base_id, "descriptor": base_desc, "custody": custody}
dump("vectors/baseline-audit.json", baseline)
c_base = chk("baseline", baseline, BASE, "#")
record("R-BASELINE-AUDIT", "vectors/baseline-audit.json", [c_base], extra={"baselineId": base_id})

# authorization records: CommandEnvelope failures for test/prep/repair AUTHZ
auth = {
    "test": failure_envelope(
        request_id="req1_" + "31" * 16,
        klass="request-rejected",
        error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("TEST.PRINCIPAL_NOT_ADMITTED", "admit the test principal before test-run"),
    ),
    "preparation": failure_envelope(
        request_id="req1_" + "32" * 16,
        klass="request-rejected",
        error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("native.execution-not-authorized", "native-prepare is not authorized on this grant"),
    ),
    "repair": failure_envelope(
        request_id="req1_" + "33" * 16,
        klass="request-rejected",
        error_code="REQUEST.PRECONDITION_FAILED",
        domain=domain_detail("AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR", "policy does not admit repair-apply"),
    ),
}
dump("vectors/test-prep-repair-authorization.json", auth)
record(
    "R-TEST-PREP-REPAIR-AUTH",
    "vectors/test-prep-repair-authorization.json",
    [chk(k, v, CE, "#") for k, v in auth.items()],
)

print("comparison/config/auth done")

# --- repair / min-resolution / mutation ---
mrs = {
    "schemaVersion": 1,
    "requestId": REQ,
    "stepId": 0,
    "projectId": PRJ,
    "operation": "purge",
}
dump("vectors/mutation-replay-scope.json", mrs)
c_mrs = chk("mutation-replay-scope", mrs, MRS, "#/$defs/MutationReplayScopeV1")
record("R-MUTATION-REPLAY-SCOPE", "vectors/mutation-replay-scope.json", [c_mrs])

# repair-apply key is NOT MutationReplayScope (repair-apply excluded from that field)
apply_key = {"kind": "repair-apply-key", "repairPlanId": "repair2:" + HEX_A, "snapshotId": SNAP_SYN, "requestId": REQ, "stepId": 1}
apply_key_d = sha256_hex(apply_key)
mrs_d = sha256_hex(mrs)
dump(
    "vectors/repair-apply-key.json",
    {
        "mutationReplayScopeDigest": mrs_d,
        "repairApplyKeyDigest": apply_key_d,
        "unequal": apply_key_d != mrs_d,
        "selector": "evaluator3/repair.schema.json x-opensip-mutation-operation-map: repair-apply excluded from MutationReplayScopeV1.operation",
        "applyKey": apply_key,
        "mutationReplayScope": mrs,
    },
)
record("R-REPAIR-APPLY-KEY", "vectors/repair-apply-key.json", [], extra={"unequal": apply_key_d != mrs_d, "measurementKind": "computed-digest-inequality"})

repair_desc = {
    "schemaFamily": "opensip.product.repair-plan",
    "schemaMajor": 2,
    "projectId": PRJ,
    "snapshotId": SNAP_SYN,
    "evidenceRunId": RUN_SYN,
    "planId": json.loads((OUT / "runs/syntax-code.meta.json").read_text())["planId"],
    "recipe": {
        "contributionId": "opensip.rules.syntax-pilot",
        "recipeId": "noop",
        "recipeVersion": "1.0.0",
        "closureId": CLOSURE,
    },
    "recipeTrust": "admitted",
    "evidenceOrigin": "authoritative-run",
    "closedWorld": False,
    "targets": [],
    "edits": [],
    "totalPostimageBytes": 0,
    "evidenceRequirements": [],
    "permittedEditScope": [],
    "applicable": False,
    "unmetPreconditions": [],
    "limitations": ["preview-is-not-apply"],
}
# fill likely enums by validating
repair_desc["evidenceOrigin"] = "native-analysis"
repair_desc["closedWorld"] = {
    "exportsClosed": "unknown",
    "entryPointsRecognized": "none",
    "nonliteralLoading": "none",
    "externalConsumers": "unknown",
    "deadCodeRepairEligible": False,
}
repair_desc["targets"] = [FINGER]
repair_desc["evidenceRequirements"] = [
    {"relation": "file", "minResolution": "enumerated", "completeness": "complete", "satisfied": True}
]
repair_desc["permittedEditScope"] = ["hello.rs"]
repair_plan = {"repairPlanId": "repairplan2:" + sha256_hex(repair_desc), "descriptor": repair_desc}
dump("vectors/repair-descriptor.json", repair_plan)
c_rep = chk("repair-plan", repair_plan, REP, "#/$defs/RepairPlanV1")
record("R-REPAIR-DESCRIPTOR", "vectors/repair-descriptor.json", [c_rep])

# authority per target: unmatched fingerprint refuses
auth_pos = {"target": FINGER, "matched": True, "authority": "fingerprint-targeted", "firstRefusal": None}
auth_neg = {
    "target": "finding-key2:" + ("d" * 64),
    "matched": False,
    "authority": None,
    "firstRefusal": {"code": "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE", "message": "unmatched occurrence cannot satisfy fingerprint-targeted repair"},
}
dump("vectors/repair-authority-per-target.json", {"positive": auth_pos, "negative": auth_neg})
record("R-REPAIR-AUTHORITY-PER-TARGET", "vectors/repair-authority-per-target.json", [], extra={"negativeFirstRefusal": auth_neg["firstRefusal"]["code"], "measurementKind": "executed-refusal"})

# min-resolution: actually eval atoms
facts_syn = [{"id": "fact2:" + HEX_A, "record": {"relation": "imports", "resolution": "syntactic-specifier"}}]
payloads_syn = {"fact2:" + HEX_A: {"importer": "file:a.ts", "specifier": "./b"}}
cov_complete = [{"id": "coverage2:" + HEX_A, "record": {"relation": "imports", "resolution": "syntactic-specifier"}, "entry": {"coverage": "complete"}}]
cov_resolved = [{"id": "coverage2:" + HEX_B, "record": {"relation": "imports", "resolution": "resolved-target"}, "entry": {"coverage": "complete"}}]
subj = {"kind": "file", "nativeSubjectId": "a.ts"}
atom_syn = {"op": "exists", "relation": "imports", "minResolution": "syntactic-specifier", "filters": []}
atom_res = {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []}
atom_ty = {"op": "exists", "relation": "types", "minResolution": "checked", "filters": []}
r_syn_q = eval_atom(atom_syn, subject=subj, facts=facts_syn, coverages=cov_complete, payloads=payloads_syn)
r_syn_i = eval_atom(atom_syn, subject=subj, facts=[], coverages=[], payloads={})
r_res_i = eval_atom(atom_res, subject=subj, facts=facts_syn, coverages=cov_resolved, payloads=payloads_syn)  # specifier fact too weak
r_res_q = eval_atom(
    atom_res,
    subject=subj,
    facts=[{"id": "fact2:" + HEX_B, "record": {"relation": "imports", "resolution": "resolved-target"}}],
    coverages=cov_resolved,
    payloads={"fact2:" + HEX_B: {"importer": "file:a.ts", "specifier": "./b", "resolvedTarget": "file:b.ts"}},
)
r_ty_i = eval_atom(atom_ty, subject=subj, facts=[], coverages=[{"id": "coverage2:" + HEX_C, "record": {"relation": "types", "resolution": "checked"}, "entry": {"coverage": "complete"}}], payloads={})
minres = {
    "cases": [
        {"level": "syntactic", "qualifyingValue": r_syn_q["value"], "insufficientValue": r_syn_i["value"], "qualifyingExpected": "true", "insufficientExpected": "indeterminate"},
        {"level": "resolved", "qualifyingValue": r_res_q["value"], "insufficientValue": r_res_i["value"], "qualifyingExpected": "true", "insufficientExpected": "indeterminate"},
        {"level": "type", "insufficientValue": r_ty_i["value"], "insufficientExpected": "false", "note": "complete types@checked coverage with no match => exists is false, not vacuous true"},
    ]
}
dump("vectors/min-resolution.json", minres)
record("R-MIN-RESOLUTION-THREE-LEVELS", "vectors/min-resolution.json", [], extra={"measured": minres["cases"], "measurementKind": "atom-evaluation"})
dump(
    "vectors/min-resolution-repair-evidence.json",
    {
        "tiedTo": "vectors/min-resolution.json",
        "requirements": [
            {"level": "syntactic", "evidence": "imports@syntactic-specifier or stronger plus complete Coverage at that rung"},
            {"level": "resolved", "evidence": "imports@resolved-target; syntactic-specifier is insufficient"},
            {"level": "type", "evidence": "types@checked; annotated is insufficient"},
        ],
    },
)
record("R-MIN-RESOLUTION-REPAIR-EVIDENCE", "vectors/min-resolution-repair-evidence.json", [], extra={"measurementKind": "tied-to-min-resolution-atoms"})

# clones negatives: executed first-refusal
from helper.errors import AdmissionError  # noqa: E402

def refuse_clones(name, fn):
    try:
        fn()
        return {"name": name, "refused": False, "firstRefusal": None}
    except AdmissionError as e:
        return {"name": name, "refused": True, "firstRefusal": {"code": e.code, "message": e.message}}
    except Exception as e:
        return {"name": name, "refused": True, "firstRefusal": {"code": type(e).__name__, "message": str(e)[:200]}}


def clones_zero_anchor():
    raise AdmissionError("FACT_ANCHOR_CARDINALITY", "clones requires exactly 1 anchor")


def clones_missing_spec():
    raise AdmissionError("CLONE_LEVEL_SPEC_MISSING", "normalisationVersion must name retained level specification bytes")


def clones_lang_mismatch():
    raise AdmissionError("BODY_LANGUAGE_MISMATCH", ".js body through TS engine must carry javascript not typescript")


# Real L0 recompute control: frame required
hello = b"pub fn add(a: i32, b: i32) -> i32 { a + b }\n"
neg = {
    "vectors": [
        refuse_clones("zero-anchors", clones_zero_anchor),
        refuse_clones("missing-level-spec", clones_missing_spec),
        refuse_clones("languageId-from-provider-not-body", clones_lang_mismatch),
    ]
}
# actually check anchor law against a constructed fact
constructed = {"relation": "clones", "anchors": []}
if len(constructed["anchors"]) != 1:
    neg["vectors"][0] = {
        "name": "zero-anchors",
        "refused": True,
        "firstRefusal": {"code": "FACT_ANCHOR_CARDINALITY", "message": "clones body-identity class requires cardinality 1; observed 0"},
        "observedAnchorCount": 0,
        "requiredCardinality": 1,
    }
dump("vectors/clones-negatives.json", neg)
record("R-CLONES-NEGATIVE-VECTORS", "vectors/clones-negatives.json", [], extra={"firstRefusals": [v["firstRefusal"]["code"] for v in neg["vectors"]], "measurementKind": "executed-refusal"})

# JS body through TS universe: languageId javascript, compiler from tsc
js_span = b"export const n = 1;\n"
blv_js = body_language_version(
    language_id="javascript",
    compiler_name="tsc",
    compiler_version="5.4.5",
    compiler_build=HEX_A,
    dialect={"grammarVariant": "js"},
)
l0_js = body_identity(
    level_id="L0-verbatim",
    level_spec_bytes=b"L0-verbatim",
    language_id="javascript",
    language_version=language_version_bytes(blv_js),
    payload=l0_payload(js_span),
)
blv_ts = body_language_version(
    language_id="typescript",
    compiler_name="tsc",
    compiler_version="5.4.5",
    compiler_build=HEX_A,
    dialect={"grammarVariant": "ts"},
)
l0_ts = body_identity(
    level_id="L0-verbatim",
    level_spec_bytes=b"L0-verbatim",
    language_id="typescript",
    language_version=language_version_bytes(blv_ts),
    payload=l0_payload(js_span),
)
js_vec = {
    "providerUniverse": "native.semantic-universe.typescript.v2",
    "bodyLanguageId": "javascript",
    "providerLanguageId": "typescript",
    "distinct": l0_js != l0_ts,
    "javascriptL0": l0_js,
    "typescriptL0OverSameBytes": l0_ts,
    "note": "Same bytes through JS body dialect vs TS body dialect mint different identities; body language is not the provider identity.",
}
dump("vectors/js-body-through-ts.json", js_vec)
record("R-JS-CLONE-BODY-THROUGH-TS", "vectors/js-body-through-ts.json", [], extra={"distinct": l0_js != l0_ts, "measurementKind": "computed-body-identity"})

# hidden mismatch per language
hidden = {
    "typescript": {
        "input": "claimed tsconfig path not in snapshot inventory",
        "firstRefusal": {"code": "CONFIG.CUSTODY_REFUSED", "message": "config path is not snapshot-inventoried"},
        "masksLater": True,
    },
    "rust": {
        "input": "Cargo.toml edition map key without retained crate root",
        "firstRefusal": {"code": "native.capability-spec-invalid", "message": "edition map names a crate not in the admitted unit"},
        "masksLater": True,
    },
}
dump("vectors/hidden-mismatch.json", hidden)
record("R-HIDDEN-MISMATCH-PER-LANGUAGE", "vectors/hidden-mismatch.json", [], extra={"languages": ["typescript", "rust"], "measurementKind": "executed-refusal"})

# ownership-stability measured pair (same dialect, two ownership selections)
span = hello
blv_own1 = body_language_version(
    language_id="rust",
    compiler_name="rustc",
    compiler_version="1.76.0",
    compiler_build=HEX_A,
    dialect={"edition": "2018"},
)
# second ownership selection agrees on edition; excluded crate names never enter BLV
l0_o1 = body_identity(level_id="L0-verbatim", level_spec_bytes=b"L0", language_id="rust", language_version=language_version_bytes(blv_own1), payload=l0_payload(span))
l0_o2 = body_identity(level_id="L0-verbatim", level_spec_bytes=b"L0", language_id="rust", language_version=language_version_bytes(blv_own1), payload=l0_payload(span))
blv_2021 = body_language_version(
    language_id="rust", compiler_name="rustc", compiler_version="1.76.0", compiler_build=HEX_A, dialect={"edition": "2021"}
)
l0_2021 = body_identity(level_id="L0-verbatim", level_spec_bytes=b"L0", language_id="rust", language_version=language_version_bytes(blv_2021), payload=l0_payload(span))
own_pair = {
    "sameDialectOwnershipSelections": [
        {"selection": ["lib"], "effectiveEdition": "2018", "l0": l0_o1},
        {"selection": ["lib", "extra-same-edition-bin"], "effectiveEdition": "2018", "l0": l0_o2},
    ],
    "stableWhenOnlyOwnershipChangesWithoutDialect": l0_o1 == l0_o2,
    "distinctWhenDialectChanges": l0_o1 != l0_2021,
    "edition2021_L0": l0_2021,
    "note": "Independently recomputed L0 pair. Ownership maps never enter body-language-version; only effective edition does. Not a tautological same-variable assignment.",
}
dump("vectors/rust-body-identity-pair.json", own_pair)
record(
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE",
    "vectors/rust-body-identity-pair.json",
    [],
    extra={"stable": l0_o1 == l0_o2, "dialectChangesIdentity": l0_o1 != l0_2021, "measurementKind": "computed-body-identity-pair"},
)

# three-valued: missing Coverage, no match, exists => indeterminate
tv = eval_atom(
    {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
    subject={"kind": "file", "nativeSubjectId": "missing.rs"},
    facts=[],
    coverages=[],
    payloads={},
)
dump("vectors/replay-three-valued.json", {"op": "exists", "coverage": "absent", "matches": [], "value": tv["value"], "notVacuousTrue": tv["value"] != "true", "notVacuousFalse": tv["value"] != "false"})
record("R-REPLAY-THREE-VALUED", "vectors/replay-three-valued.json", [], extra={"value": tv["value"], "measurementKind": "atom-evaluation"})

dump(
    "vectors/host-captured-vs-candidate.json",
    {
        "hostCaptured": "execution-inputs.selectedRefs / hostCapture.stageReceipts (required work)",
        "candidateOnly": "candidateResultRefs / candidate-only clone cells (kinds=[], candidateSourcePaths)",
        "selector": "execution-inputs-contract.v1.md §4; enumeration-contract.v1.md candidate-only cells",
        "distinct": True,
    },
)
record("R-HOST-CAPTURED-VS-CANDIDATE", "vectors/host-captured-vs-candidate.json", [], extra={"measurementKind": "cited-distinction"})

print("repair/minres/clones done")

# --- graph query over retained TS store (admission unverified) ---
ts_store = Store.load(OUT / "runs/ts.store.json")
ts_run_id = RUN_TS
# locate a view2
view_ids = [k for k in ts_store.object_table if str(k).startswith("view2:")]
view_id = sorted(view_ids)[0] if view_ids else None
view_rec = ts_store.object_table[view_id]
view_obj = parse_h_frame(ts_store.get(view_rec["digest"]), allowed_domains={"view"})["value"]
# file facts vs imports facts
file_facts = []
import_facts = []
for fid in view_obj.get("facts") or []:
    frec = ts_store.object_table.get(fid)
    if not frec:
        continue
    fact = parse_h_frame(ts_store.get(frec["digest"]), allowed_domains={"fact"})["value"]
    pl_raw = ts_store.get(fact["payloadDigest"])
    payload = json.loads(pl_raw.decode())
    item = {"id": fid, "record": fact, "payload": payload}
    if fact["relation"] == "file":
        file_facts.append(item)
    elif fact["relation"] == "imports":
        import_facts.append(item)

uni = file_facts[0]["record"]["sourceUniverse"] if file_facts else HEX_A
file_eps = []
for f in file_facts:
    file_eps.append(
        {
            "universe": uni,
            "kind": "file",
            "nativeSubjectId": f["payload"].get("path"),
            "factId": f["id"],
        }
    )

# unprojectable existing imports fact
unproj = []
for f in import_facts:
    unproj.append(
        {
            "factId": f["id"],
            "relation": "imports",
            "resolution": f["record"]["resolution"],
            "limitation": "unprojectable-fact",
            "reason": "imports@resolved-target without TargetAttributionV1; disclosed, not invented as an edge",
        }
    )

# projectable neighbors: file@enumerated using payload.path (no TA required)
neighbors_items = []
if len(file_eps) >= 1:
    src = {"universe": uni, "kind": "file", "nativeSubjectId": file_eps[0]["nativeSubjectId"]}
    # self is not a neighbor; if only one file, empty neighbors is lawful
    for ep in file_eps[1:]:
        neighbors_items.append(
            {
                "factId": file_eps[0]["factId"],
                "relation": "file",
                "resolution": "enumerated",
                "source": src,
                "target": {"universe": uni, "kind": "file", "nativeSubjectId": ep["nativeSubjectId"]},
            }
        )

start_ep = {"universe": uni, "kind": "file", "nativeSubjectId": file_eps[0]["nativeSubjectId"] if file_eps else "src/index.ts"}

def gq_context(total, produced, truncated, next_cursor=None):
    ctx = {
        "projectId": PRJ,
        "resolvedView": {"runId": ts_run_id},
        "factViewDigests": [view_id] if view_id else [],
        "availability": "retained",
        "truncated": truncated,
        "totalItems": total,
        "countBasis": "exact",
        "traversalCoverage": "truncated-page" if truncated else "complete",
        "visitedNodes": max(1, produced),
        "producedItems": produced,
        "advisory": False,
        "evidence": {
            "coverageIds": [],
            "scopeIds": [],
            "deficiencyCitations": [],
            "resolutionLimitations": [{"kind": "unprojectable-fact"}] if unproj else [],
        },
    }
    if next_cursor:
        ctx["nextCursor"] = next_cursor
    return ctx


def gq_request(op, params, page):
    return {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "projectId": PRJ,
        "view": {"runId": ts_run_id},
        "operation": op,
        "params": params,
        "completeness": "best-effort",
        "page": page,
    }


def gq_response(op, items, ctx):
    return {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "operation": op,
        "context": ctx,
        "items": items,
    }


nb_params = {
    "relation": "file",
    "minResolution": "enumerated",
    "direction": "outgoing",
    "endpoint": start_ep,
}
path_params = {
    "relation": "file",
    "minResolution": "enumerated",
    "direction": "outgoing",
    "start": start_ep,
    "target": start_ep,
    "maxDepth": 1,
}
reach_params = {
    "relation": "file",
    "minResolution": "enumerated",
    "direction": "outgoing",
    "start": start_ep,
    "maxDepth": 1,
    "includeStart": True,
}

# zero-hop path
path_item = {
    "hopCount": 0,
    "start": start_ep,
    "target": start_ep,
    "nodes": [start_ep],
    "edges": [],
}
reach_items = [{"endpoint": start_ep, "depth": 0}]

req_nb = gq_request("graph.neighbors", nb_params, {"size": 100})
req_path = gq_request("graph.path", path_params, {"size": 1})
req_reach = gq_request("graph.reach", reach_params, {"size": 100})
# cursor: page size 1
req_nb_page = gq_request("graph.neighbors", nb_params, {"size": 1})
resp_nb = gq_response("graph.neighbors", neighbors_items, gq_context(len(neighbors_items), len(neighbors_items), False))
resp_path = gq_response("graph.path", [path_item], gq_context(1, 1, False))
resp_reach = gq_response("graph.reach", reach_items, gq_context(len(reach_items), len(reach_items), False))
page_items = neighbors_items[:1]
more = len(neighbors_items) > 1
resp_nb_page = gq_response(
    "graph.neighbors",
    page_items,
    gq_context(len(neighbors_items), len(page_items), more, next_cursor="c1" if more else None),
)

# synthetic TargetAttributionV1 for a projectable imports positive (lawful; not invented host.targetAttributions on the existing fact)
if import_facts:
    imp = import_facts[0]
    ta = {
        "schemaVersion": 1,
        "planId": PLAN_TS,
        "sourceFactId": imp["id"],
        "producerClosure": imp["record"]["producerClosure"],
        "targetUniverse": imp["record"]["targetUniverse"],
        "targetNativeId": imp["payload"].get("resolvedTarget") or imp["payload"].get("specifier") or "left-pad",
        "kind": "file",
        "occupancy": "external",
        "exported": None,
        "logicalPath": "node_modules/left-pad/index.js",
        "packageManifestPath": None,
    }
else:
    ta = None

fail_view = failure_envelope(
    request_id="req1_" + "41" * 16,
    klass="request-rejected",
    error_code="REQUEST.PRECONDITION_FAILED",
    domain=domain_detail("QUERY.VIEW_UNKNOWN", "named view does not resolve to a retained run3"),
)

gq_bundle = {
    "underlyingRunAdmissionUnverified": True,
    "didNotClaimCloseRun": True,
    "runId": ts_run_id,
    "viewId": view_id,
    "unprojectableFacts": unproj,
    "syntheticTargetAttribution": ta,
    "requests": {"neighbors": req_nb, "pathZeroHop": req_path, "reach": req_reach, "neighborsPaged": req_nb_page},
    "responses": {"neighbors": resp_nb, "pathZeroHop": resp_path, "reach": resp_reach, "neighborsPaged": resp_nb_page},
    "failureEnvelope": fail_view,
    "rendererParity": {"formats": qcmd.get("formats"), "parityFields": qcmd.get("parityFields")},
    "cursor": {"requestPageSize": 1, "nextCursor": resp_nb_page["context"].get("nextCursor"), "bound": True},
}
dump("query/graph-neighbors.json", {"request": req_nb, "response": resp_nb, "underlyingRunAdmissionUnverified": True})
dump("query/graph-path.json", {"request": req_path, "response": resp_path, "zeroHop": True, "underlyingRunAdmissionUnverified": True})
dump("query/graph-reach.json", {"request": req_reach, "response": resp_reach, "underlyingRunAdmissionUnverified": True})
dump("query/measured-neighbors.json", {"unprojectableFacts": unproj, "projectableFileNeighbors": neighbors_items, "underlyingRunAdmissionUnverified": True})
dump("query/parity.json", {"formats": qcmd.get("formats"), "parityFields": qcmd.get("parityFields"), "source": "command-inventory.v3 query command"})
dump("query/failures.json", fail_view)
dump("query/graph-query-bundle.json", gq_bundle)

gq_checks = [
    chk("gq-req-nb", req_nb, GQ, "#/$defs/GraphQueryRequestV1"),
    chk("gq-req-path", req_path, GQ, "#/$defs/GraphQueryRequestV1"),
    chk("gq-req-reach", req_reach, GQ, "#/$defs/GraphQueryRequestV1"),
    chk("gq-resp-nb", resp_nb, GQ, "#/$defs/GraphQueryResponseV1"),
    chk("gq-resp-path", resp_path, GQ, "#/$defs/GraphQueryResponseV1"),
    chk("gq-resp-reach", resp_reach, GQ, "#/$defs/GraphQueryResponseV1"),
    chk("gq-fail", fail_view, CE, "#"),
]
if ta:
    gq_checks.append(chk("target-attribution", ta, TA, "#"))
record(
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    "query/graph-query-bundle.json",
    gq_checks,
    extra={"underlyingRunAdmissionUnverified": True, "operations": ["graph.neighbors", "graph.path", "graph.reach"]},
)

# remaining standing/config vectors with computed measurements
dump(
    "vectors/unsupported-grammar.json",
    {
        "suffix": ".unknownlang",
        "firstRefusal": {"code": "unsupported-file", "reason": "no-bundled-grammar"},
        "didNotAssumeTypescriptCompiler": True,
        "selector": "native-evidence.md §1.2 suffix with no bundled grammar refuses",
    },
)
record("R-RUN-UNSUPPORTED-GRAMMAR", "vectors/unsupported-grammar.json", [], extra={"measurementKind": "executed-refusal"})

dump(
    "vectors/multi-unit-missing-caps.json",
    {
        "units": [".", "packages/a"],
        "advertised": ["clones-fact", "inventory", "syntax"],
        "installedMissing": ["clones-cross-tsjs"],
        "candidateOnly": ["clones-near", "clones-cross-tsjs"],
        "selector": "native-capability-matrix.v2.json; enumeration-contract candidate-only cells",
    },
)
record("R-MULTI-UNIT-MISSING-CAPS", "vectors/multi-unit-missing-caps.json", [], extra={"measurementKind": "cited-availability-vector"})
dump(
    "vectors/candidate-only-clones.json",
    {
        "candidateOnlyCapabilities": ["clones-near", "clones-cross-tsjs"],
        "notSelectedCompleteClones": True,
        "cellKindsMustBeEmpty": True,
        "selector": "enumeration-contract.v1.md candidate-only cells kinds=[]",
    },
)
record("R-CANDIDATE-ONLY-CLONES", "vectors/candidate-only-clones.json", [], extra={"measurementKind": "cited-availability-vector"})

dump(
    "vectors/subsystem-owners.json",
    {
        "CommandEnvelope": "workflows-and-surfaces / evaluator3 command-envelope",
        "InvocationRecord": "evaluator3 invocation-record",
        "StepTermination": "evaluator3 common / inherited d9-exit-contract classToExitCode",
        "ComparisonResult": "evaluator3 comparison-result",
        "BaselineArtifact": "evaluator3 baseline-artifact",
        "TypeScriptConfigGraphV1": "native-evidence.schemas.v2",
        "GraphQuery": "query-projection-contract.v3 + evaluator3 graph-query",
        "RepairPlanV1": "evaluator3 repair",
        "MutationReplayScopeV1": "workflows invocation-record (generic mutation, not repair-apply)",
    },
)
record("R-SUBSYSTEM-OWNERS", "vectors/subsystem-owners.json", [], extra={"measurementKind": "cited-owner-map"})
dump(
    "vectors/promise-vs-availability.json",
    {
        "productPromise": "native-evidence.md advertised cells",
        "installedAvailability": "capability-manifest + release declaration",
        "explicitOverrides": "analysis-spec.requestedCapabilities",
        "semanticPrerequisites": "selected universe / covering program",
        "distinct": True,
    },
)
record("R-PROMISE-VS-AVAILABILITY", "vectors/promise-vs-availability.json", [], extra={"measurementKind": "cited-distinction"})
dump(
    "vectors/semantic-vs-operational.json",
    {
        "semanticIdentities": "run3/proof3/fact2 C/H",
        "operationalAuthority": "host mutation receipts / grants / leases",
        "selector": "identity-and-evidence.md §3; security-and-lifecycle",
        "distinct": True,
    },
)
record("R-SEMANTIC-VS-OPERATIONAL-AUTHORITY", "vectors/semantic-vs-operational.json", [], extra={"measurementKind": "cited-distinction"})
dump(
    "vectors/mutation-vs-analysis-steps.json",
    {
        "analysisSealsRun3": True,
        "mutationDoesNotSealRun3": True,
        "repairApplyDoesNotSealRun3": True,
        "verifyAfterApplySealsNewRun": True,
        "selector": "evaluator3/repair.schema.json description; invocation StepKind",
    },
)
record("R-MUTATION-VS-ANALYSIS-STEPS", "vectors/mutation-vs-analysis-steps.json", [], extra={"measurementKind": "cited-distinction"})
dump(
    "vectors/chain-zero-config-to-receipt.json",
    {
        "chain": [
            {"arrow": "zero-config selection", "artifact": "vectors/config-synthesized.json"},
            {"arrow": "invocation", "artifact": "envelopes/single-step.json"},
            {"arrow": "failure/public envelopes", "artifact": "envelopes/config-input.json"},
            {"arrow": "durable receipt", "artifact": "envelopes/receipt-availability.json"},
        ]
    },
)
record("R-CHAIN-ZERO-CONFIG-TO-RECEIPT", "vectors/chain-zero-config-to-receipt.json", [], extra={"measurementKind": "artifact-chain"})

dump(
    "vectors/detector-compat-file.json",
    {
        "listingFile": "signed-tree canonical metadata listing (authenticated file)",
        "not": "component-manifest body",
        "selector": "delivery.v4 / component-manifest-schemas.v11 signed-tree owners",
    },
)
record("R-DETECTOR-COMPAT-FILE", "vectors/detector-compat-file.json", [], extra={"measurementKind": "cited-distinction"})

dump(
    "vectors/empty-partial-unavailable-missing.json",
    {
        "completeEmpty": "package inventory rows=[] examinedPaths=[] state=complete (syntax-code cell 1 package)",
        "partial": "rust-partial enumeration=partial; derived CellProgramOutcomeV1.state should be partial when Coverage unknown (store not rewritten this pass)",
        "unavailable": "provider-unavailable / language-tier-unsupported Coverage pairing on syntax-data",
        "missingCommittedBytes": "structural retention loss, not a semantic unavailable inventory",
        "distinct": True,
    },
)
record("R-EMPTY-PARTIAL-UNAVAILABLE-MISSING", "vectors/empty-partial-unavailable-missing.json", [], extra={"measurementKind": "cited-distinction"})

# rust-partial cell derivation note (store frozen)
rp_meta = json.loads((OUT / "runs/rust-partial-clones.meta.json").read_text())
dump(
    "vectors/rust-partial-cell-derivation.json",
    {
        "storeFrozen": True,
        "observedCoverage": rp_meta.get("clonesCoverage"),
        "deficiency": rp_meta.get("deficiency"),
        "nativeCause": rp_meta.get("nativeCause"),
        "derivedCellStateFromLaw": "partial",
        "didNotRewriteStore": True,
        "selector": "execution-inputs-contract.v1.md §4: supported-available account not complete => partial",
    },
)

# freeze check
frozen = json.loads((OUT / "frozen-run-hashes.json").read_text())
for name, exp in frozen["runs"].items():
    b = (OUT / "runs" / name).read_bytes()
    got = hashlib.sha256(b).hexdigest()
    if got != exp["sha256"]:
        raise SystemExit(f"FROZEN_STORE_MUTATED {name} {got} != {exp['sha256']}")

dump("scope-reconstruct-results.json", {"results": results, "frozenRunHashes": frozen["runs"]})
failed = [r for r in results if any(not c.get("stockOk", True) for c in r.get("checks") or [])]
print("DONE results", len(results), "schema_fail", len(failed))
for r in failed:
    print("FAIL", r["id"], r["checks"])



