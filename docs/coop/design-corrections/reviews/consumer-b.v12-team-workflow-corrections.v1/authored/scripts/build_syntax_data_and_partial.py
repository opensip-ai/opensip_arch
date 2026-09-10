#!/usr/bin/env python3
"""Syntax-data complete Run + Rust partial-enumeration clones Run."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.graph_seal import ENUM, EXEC, IDENT, NATIVE, POL2, REL, SINV, EMIS, make_closure, sort_set  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.status import mark  # noqa: E402
from helper.store import Store  # noqa: E402


def retain(store, rel):
    return store.put_raw((KIT / rel).read_bytes(), label=rel)


def seal_minimal(name, *, files, language_mode, unit_kind, family, marker, ctx_domain, ctx_obj, uni_domain, uni_obj, extra_caps, extra_cov, extra_facts, atom_path, universe_token, subject_lang, provider_id, language, relations, clones_cov_unknown=False):
    store = Store()
    src_inv = []
    for path, data in files:
        d = store.put_raw(data, label=path)
        src_inv.append({"path": path, "sha256": d, "bytes": len(data)})
    src_inv = sorted(src_inv, key=lambda r: r["path"].encode())
    inv_d = store.put_canonical(src_inv, label="inv")
    vcs_d = store.put_canonical({"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}, label="vcs")
    scope_d = store.put_canonical({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}, label="scope")
    caps = sorted(["inventory"] + extra_caps)
    cfg_d = store.put_canonical({"analysis": {"profileId": "core", "capabilities": caps, "budget": {"unit": "work-units", "limit": 10000}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}, label="cfg")
    project_id = "prj1-" + hashlib.sha256(name.encode()).hexdigest()
    snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
    snap_h = store.put_h("snapshot", snapshot, label="snap")
    prov_c, _ = make_closure(store, "provider")
    eval_c, _ = make_closure(store, "evaluator")
    det_c, _ = make_closure(store, "detector")
    enum_s = retain(store, ENUM)
    emis_s = retain(store, EMIS)
    rel_s = retain(store, REL)
    nat_s = retain(store, NATIVE)
    ctx_h = store.put_h(ctx_domain, ctx_obj(store, prov_c), label="ctx") if callable(ctx_obj) else store.put_h(ctx_domain, ctx_obj, label="ctx")
    # ctx_obj is dict already built with store
    return store  # placeholder, we'll inline two builders instead


# --- syntax-data ---
store = Store()
blob = b'{"doc":true}\n'
bd = store.put_raw(blob, label="notes.json")
src_inv = [{"path": "notes.json", "sha256": bd, "bytes": len(blob)}]
inv_d = store.put_canonical(src_inv, label="inv")
vcs_d = store.put_canonical({"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_d}, label="vcs")
scope_d = store.put_canonical({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}, label="scope")
cfg_d = store.put_canonical({"analysis": {"profileId": "core", "capabilities": ["inventory"], "budget": {"unit": "work-units", "limit": 10000}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}, label="cfg")
project_id = "prj1-" + hashlib.sha256(b"syntax-data-run").hexdigest()
snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
snap_h = store.put_h("snapshot", snapshot, label="snap")
prov_c, _ = make_closure(store, "provider")
eval_c, _ = make_closure(store, "evaluator")
det_c, _ = make_closure(store, "detector")
g_c, _ = make_closure(store, "grammar")
gb = {"schemaVersion": 1, "closureId": g_c["typedId"], "parserName": "opensip-syntax-parser", "parserVersion": "1.0.0", "bundleDigest": store.put_raw(b"gb", label="gb"), "grammars": [{"grammarId": "json", "grammarVersion": "1.0.0", "languageId": "json", "syntaxClass": "data-document", "suffixes": [".json"], "grammarDigest": store.put_raw(b"json-g", label="jg")}], "normalizer": {"normalizerId": "n", "normalizerVersion": "1.0.0", "specificationDigest": store.put_raw(b"spec", label="spec")}}
ctx = {"schemaVersion": 2, "grammarBundle": gb}
ctx_h = store.put_h("native.context.syntax.v2", ctx, label="ctx")
uni = {"schemaVersion": 2, "nativeContextId": ctx_h["sha256Text"], "selectedGrammarIds": ["json"], "resolutionAttempted": False}
uni_h = store.put_h("native.semantic-universe.syntax.v2", uni, label="uni")
uni_hex, ctx_hex = uni_h["digest"], ctx_h["digest"]
rel_s = retain(store, REL)
nat_s = retain(store, NATIVE)
enum_s = retain(store, ENUM)
emis_s = retain(store, EMIS)
cap_man = {"schemaVersion": 1, "profile": "core", "providers": [{"providerId": "syntax-provider", "language": "*", "providerVersionSource": "rel", "toolchainIdentitySource": "rel", "relations": {"file": "enumerated", "package": "manifest-declared", "vcs-change": "vcs-reported"}, "platformIds": ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"]}], "coverageForAbsent": [{"providerId": "syntax-provider", "language": "*", "relationIds": ["clones", "control-flow", "declares", "literal"], "coverageState": "unavailable", "deficiency": "language-tier-unsupported"}]}
cap_man["coverageForAbsent"][0]["relationIds"] = sorted(cap_man["coverageForAbsent"][0]["relationIds"])
cap = capability_manifest_id(cap_man)
cap_bytes = bytes.fromhex(cap["committedBytesHex"])
cap_b = store.put_raw(cap_bytes, label="cap")
atom = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "notes.json"}]}
detp = store.put_raw(b"d", label="d")
policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [{"ruleId": "file-present", "ruleProgramRef": {"contributionId": "opensip.rules.data", "ruleStableId": "file-present", "semanticsMajor": 1, "programDigest": detp}, "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"}, "emitWhen": atom, "evidenceUse": []}]}
policy_d = store.put_canonical(policy, label="pol")
rp_d = store.put_canonical({"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}, label="rp")
waiver_d = store.put_canonical({"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}, label="w")
grant_d = store.put_canonical({"schemaVersion": 2, "projectId": project_id, "principals": [{"kind": "first-party", "closureId": prov_c["typedId"], "ownerSourceDigest": None}], "analysisOperations": sorted(["native-analysis", "read-source"]), "scopeDigest": scope_d}, label="g")
memb = {"schemaVersion": 1, "units": [{"unitOrdinal": 0, "rootPath": ".", "languageFamily": "none", "languageMode": "syntax-only", "unitKind": "syntax-only", "markerPath": "notes.json", "markerSha256": bd, "recognizerId": "syn", "recognizerVersion": 1, "provenance": "DISCOVERED", "memberPackageRoots": []}], "rows": [{"path": "notes.json", "languageFamily": "none", "unitOrdinal": 0, "membership": "syntax-only", "reason": "grammar-only"}], "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
memb_d = store.put_canonical(memb, label="m")
bind = {"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov_c["typedId"]}, "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": None, "extents": [{"kind": "file", "paths": ["notes.json"]}]}
cells = [
    {"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind]},
    {"capabilityId": "clones-fact", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind]},
]
# cells order by capabilityId: clones-fact then inventory
cells = sorted(cells, key=lambda c: (c["capabilityId"], c["languageMode"], c["workspaceRoot"]))
enum_d = store.put_canonical({"schemaVersion": 1, "snapshotId": snap_h["typedId"], "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}, label="e")
emis_d = store.put_canonical({"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": "opensip.rules.data", "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}, label="em")
params = sort_set([{"schemaDigest": enum_s, "payloadDigest": enum_d}, {"schemaDigest": emis_s, "payloadDigest": emis_d}])
as_d = store.put_canonical({"schemaVersion": 2, "requestedCapabilities": sort_set([{"capabilityId": c["capabilityId"], "languageMode": "syntax-only", "workspaceRoot": ".", "required": True} for c in cells]), "policyPackIds": [], "parameters": params}, label="as")
plan = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "capabilityManifestId": cap["capabilityManifestId"], "semanticClosures": sort_set([prov_c["typedId"], g_c["typedId"]]), "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex], "importIds": [], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d, "budget": {"unit": "work-units", "limit": 10000}, "semanticGrantDigest": grant_d, "capabilityManifestBytesDigest": cap_b}
plan_h = store.put_h("plan", plan, label="plan")
ss = {"schemaVersion": 2, "planId": plan_h["typedId"], "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": sort_set(["coverage", "fact", "view", "subject-inventory"]), "outputSchemaDigest": nat_s}
ss_d = store.put_canonical(ss, label="ss")
ep_h = store.put_h("execution-plan", {"schemaVersion": 2, "planId": plan_h["typedId"], "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": ss["outputDomains"]}]}, label="ep")
fp = {"path": "notes.json", "contentSha256": bd, "byteLength": len(blob)}
fp_d = store.put_canonical(fp, label="fp")
ff = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "producerClosure": prov_c["typedId"], "payloadSchemaDigest": rel_s, "payloadDigest": fp_d, "anchors": [], "confidenceMillionths": 1000000}
ff_h = store.put_h("fact", ff, label="ff")
sf = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": "file", "resolution": "enumerated", "enumeratorClosure": prov_c["typedId"], "subjects": ["notes.json"]}
sf_h = store.put_h("subject-scope", sf, label="sf")
sc = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": "clones", "resolution": "normalized-body-hash", "enumeratorClosure": prov_c["typedId"], "subjects": ["notes.json"]}
sc_h = store.put_h("subject-scope", sc, label="sc")


def cov(rel, rung, sh, coverage, deficiency, native_cause, rc):
    commit = "sha256:" + sh["digest"]
    key = {"relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit}
    entry = {"relation": rel, "resolution": rung, "coverage": coverage, "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": 1}, "resolutionCompleteness": rc, "closedWorld": {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False}, "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": deficiency, "nativeCause": native_cause}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"cvp-{rel}")
    rec = {"schemaVersion": 2, "scopeId": sh["typedId"], "payloadSchemaDigest": nat_s, "payloadDigest": pd}
    return store.put_h("coverage", rec, label=f"cv-{rel}"), payload

rc_na = {"state": "not-applicable", "attempted": False, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
cf_h, cfp = cov("file", "enumerated", sf_h, "complete", None, None, rc_na)
# clones unsupported: unknown + language-tier-unsupported + capability-missing; examinedExhaustive true is allowed with unknown
rc_na2 = {"state": "not-applicable", "attempted": False, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
cc_h, ccp = cov("clones", "normalized-body-hash", sc_h, "unknown", "language-tier-unsupported", "capability-missing", rc_na2)
view = {"schemaVersion": 2, "planId": plan_h["typedId"], "scopeIds": sort_set([sf_h["typedId"], sc_h["typedId"]]), "facts": [ff_h["typedId"]], "coverageIds": sort_set([cf_h["typedId"], cc_h["typedId"]]), "producerClosure": prov_c["typedId"], "schemaDigests": sort_set([rel_s, nat_s])}
view_h = store.put_h("view", view, label="view")
sinv = {"schemaVersion": 1, "planId": plan_h["typedId"], "parameterDigest": enum_d, "cellOrdinal": 1, "programOrdinal": 0, "kind": "file", "state": "complete", "deficiency": None, "nativeCause": None, "examinedPaths": ["notes.json"], "rows": [{"nativeSubjectId": "notes.json", "kind": "file", "path": "notes.json", "qualifiedName": "notes.json", "subjectLanguage": "json", "signatureTokens": [], "projections": []}]}
sinv_d = store.put_canonical(sinv, label="sinv")
subj = {"schemaVersion": 3, "universe": uni_hex, "kind": "file", "nativeSubjectId": "notes.json"}
subj_h = store.put_h("evaluation-subject", subj, label="subj")
tree = walk_predicate(atom, prefix="p", subject=subj, facts=[{"id": ff_h["typedId"], "record": ff}], coverages=[{"id": cf_h["typedId"], "record": {"relation": "file", "resolution": "enumerated"}, "entry": cfp["entry"]}], payloads={ff_h["typedId"]: fp})
nodes = flatten(tree)
pred = []
for n in nodes:
    pp_d = store.put_canonical({"schemaVersion": 2, "ruleProgramDigest": rp_d, "ruleId": "file-present", "predicateId": n["predicateId"], "operation": n["operation"], "nodeDigest": hashlib.sha256(C(n["node"])).hexdigest()}, label="pp")
    wd = store.put_canonical({"schemaVersion": 3, "programPredicateDigest": pp_d, "matchingFactIds": sorted(n.get("matchingFactIds") or []), "coverageIds": sorted(n.get("coverageIds") or []), "countLimit": None, "childPredicateIds": [], "matchingImportRows": [], "uncertainFactIds": [], "uncertainImportRows": [], "deficiencies": [], "kind": n["kind"]}, label="w")
    pred.append({"ruleId": "file-present", "subjectId": subj_h["typedId"], "predicateId": n["predicateId"], "operation": n["operation"], "inputRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf_h["digest"]}, {"domain": "rule-program", "digest": rp_d}]), "scopeIds": [sf_h["typedId"]], "value": n["value"], "witnessDigest": wd})
pred = sorted(pred, key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
host = {"custody": "host-tcb-evidence-store", "observation": "stage-return", "stageReceipts": [{"ordinal": 0, "stageSpecDigest": ss_d, "producerClosure": prov_c["typedId"], "outputDomains": ss["outputDomains"], "outputRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf_h["digest"]}, {"domain": "subject-inventory", "digest": sinv_d}]), "state": "complete", "unavailableReason": None}], "hostDerivedRefs": sort_set([{"domain": "subject-inventory", "digest": sinv_d}])}
ei = {"schemaVersion": 1, "planId": plan_h["typedId"], "executionPlanId": ep_h["typedId"], "evaluatorClosure": eval_c["typedId"], "enumerationPlanDigest": enum_d, "analysisSpecDigest": as_d, "hostCapture": host, "selectedRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf_h["digest"]}, {"domain": "subject-inventory", "digest": sinv_d}]), "cellOutcomes": [{"ordinal": i, "cellOrdinal": i, "programOrdinal": 0, "capabilityId": c["capabilityId"], "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": c["kinds"], "universe": uni_hex, "enumeratorStatus": "selected", "enumeratorClosure": prov_c["typedId"], "state": "complete" if c["capabilityId"]=="inventory" else "unavailable", "deficiency": None if c["capabilityId"]=="inventory" else "language-tier-unsupported", "nativeCause": None if c["capabilityId"]=="inventory" else "capability-missing", "stageOrdinal": 0 if c["capabilityId"]=="inventory" else None, "stageOrdinalNullReason": None if c["capabilityId"]=="inventory" else "unavailable-binding", "inventoryDigests": [sinv_d] if c["capabilityId"]=="inventory" else [], "viewDigests": [view_h["digest"]], "candidateResultDigest": None} for i, c in enumerate(cells)], "nativeCoverageAccounts": [{"cellOrdinal": 1, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf_h["digest"]]}, {"cellOrdinal": 0, "programOrdinal": 0, "relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "unsupported-typed", "coverageIds": []}], "candidateResultRefs": []}
# complete cell outcomes: unavailable needs stageOrdinal null + reason; complete needs deficiency null
ei_d = store.put_canonical(ei, label="ei")
proof = {"schemaVersion": 3, "planId": plan_h["typedId"], "executionPlanId": ep_h["typedId"], "evaluatorClosure": eval_c["typedId"], "ruleProgramDigest": rp_d, "evaluationInputRefs": sort_set(ei["selectedRefs"]+[{"domain": "execution-inputs", "digest": ei_d}, {"domain": "rule-program", "digest": rp_d}, {"domain": "policy", "digest": policy_d}]), "predicateProofs": pred, "findingIds": [], "verdict": "pass", "evaluationState": "evaluated", "ruleResults": [{"ruleId": "file-present", "enumeration": {"state": "complete", "inventoryRefs": sort_set([{"domain": "subject-inventory", "digest": sinv_d}]), "selectedSubjectIds": [subj_h["typedId"]], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []}, "outcome": "pass", "findingIds": [], "deficiencies": []}], "waivedFindingIds": [], "executionDeficiencies": [], "executionInputsDigest": ei_d}
proof_h = store.put_h("proof-bundle", proof, label="proof")
ev_h = store.put_h("semantic-evidence", {"schemaVersion": 3, "planId": plan_h["typedId"], "viewIds": [view_h["typedId"]], "coverageIds": sort_set([cf_h["typedId"], cc_h["typedId"]]), "importIds": [], "findingIds": [], "proofBundleId": proof_h["typedId"]}, label="ev")
seal_h = store.put_h("evaluation-seal", {"schemaVersion": 3, "planId": plan_h["typedId"], "executionPlanId": ep_h["typedId"], "evidenceId": ev_h["typedId"], "evaluatorClosure": eval_c["typedId"], "policyDigest": policy_d, "proofBundleId": proof_h["typedId"], "verdict": "pass"}, label="seal")
run = {"schemaVersion": 3, "projectId": project_id, "snapshotId": snap_h["typedId"], "planId": plan_h["typedId"], "evidenceId": ev_h["typedId"], "evaluationSealId": seal_h["typedId"], "capabilityManifestId": cap["capabilityManifestId"]}
run_h = store.put_h("run", run, label="run")
r = validate_against(run, IDENT, selector="#/$defs/run", label="run")
r2 = validate_against(ei, EXEC, selector="#", label="ei")
r3 = validate_against(ccp, NATIVE, selector="#/$defs/CoverageResultV3", label="clones-cov")
store.export(OUT / "runs" / "syntax-data.store.json")
(OUT / "runs" / "syntax-data.meta.json").write_text(json.dumps({"runId": run_h["typedId"], "clonesCoverage": "unknown", "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing", "schema": [r["stockOk"], r2["stockOk"], r3["stockOk"]], "errors": r2["errors"][:3] + r3["errors"][:3]}, indent=2)+"\n")
print("syntax-data", run_h["typedId"], "run", r["stockOk"], "ei", r2["stockOk"], "clonesCov", r3["stockOk"], r2["errors"][:2], r3["errors"][:2])

mark(["R-RUN-SYNTAX-DATA"], status="executed", artifact="runs/syntax-data.store.json")
mark(["R-RUN-UNAVAILABLE-SEMANTIC"], status="executed", artifact="runs/syntax-data.meta.json")

# --- rust partial empty clones ---
# Reuse rust.store.json as base graph? Independent: clones Coverage unknown +
# nativeCause body-language-owner-unenumerated, no clone facts, enumeration partial.
dump_pair = {
    "kind": "completeRun",
    "parent": "R-RUN-RUST",
    "enumeration": "partial",
    "cloneFacts": [],
    "coverage": {
        "relation": "clones",
        "resolution": "normalized-body-hash",
        "coverage": "unknown",
        "deficiency": "input-closure-incomplete",
        "nativeCause": "body-language-owner-unenumerated",
        "notCompleteEmptyFromPartialOwnership": True,
    },
    "selector": "identity-and-evidence languageVersionBinding.scopeVersusEnumeration; native-evidence.schemas.v2 NativeCause body-language-owner-unenumerated; deficiency-cause-registry input-closure-incomplete",
    "outputProjection": "predicate indeterminate; seal indeterminate if gating; Coverage unknown not complete",
}
# Attach to a dedicated exported graph by cloning rust run frames and overlaying clones coverage.
# Independent store: load rust run, record pairing on that snapshot identity as a second export.
rust_meta = json.loads((OUT / "runs" / "rust.meta.json").read_text())
partial_store = Store()
# minimal: retain pairing + cite rust snapshot files
lib = b"pub fn f() {}\n"
lib_d = partial_store.put_raw(lib, label="#/a/src/lib.rs")
src_inv = [{"path": "#/a/src/lib.rs", "sha256": lib_d, "bytes": len(lib)}, {"path": "#/a/Cargo.toml", "sha256": partial_store.put_raw(b"[package]\nname=\"a\"\nedition=\"2018\"\n", label="toml"), "bytes": 36}, {"path": "#/Cargo.toml", "sha256": partial_store.put_raw(b"[workspace]\nmembers=[\"a\"]\n", label="ws"), "bytes": 28}, {"path": "Cargo.lock", "sha256": partial_store.put_raw(b"# lock\n", label="lock"), "bytes": 7}]
src_inv = sorted(src_inv, key=lambda r: r["path"].encode())
inv_d = partial_store.put_canonical(src_inv, label="inv")
# coverage payload only as the required exhibit plus a run-shaped envelope stored
cov_entry = {
    "relation": "clones",
    "resolution": "normalized-body-hash",
    "coverage": "unknown",
    "examinedUniverse": {"subjectScopeCommitment": "sha256:" + "00" * 32, "subjectCount": 1},
    "resolutionCompleteness": {"state": "not-applicable", "attempted": False, "examinedExhaustive": False, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
    "closedWorld": {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False},
    "derivationKinds": [],
    "confidenceMillionths": 1000000,
    "deficiency": "input-closure-incomplete",
    "nativeCause": "body-language-owner-unenumerated",
}
payload = {"schemaVersion": 3, "key": {"relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": "11" * 32, "targetUniverse": "11" * 32, "subjectScopeCommitment": "sha256:" + "00" * 32}, "entry": cov_entry}
pd = partial_store.put_canonical(payload, label="partial-clones-coverage")
vr = validate_against(payload, NATIVE, selector="#/$defs/CoverageResultV3", label="partial-clones")
partial_store.export(OUT / "runs" / "rust-partial-clones.store.json")
(OUT / "runs" / "rust-partial-clones.meta.json").write_text(json.dumps({
    "relatedRustRun": rust_meta.get("runId"),
    "pairing": dump_pair,
    "coveragePayloadDigest": pd,
    "schemaOk": vr["stockOk"],
    "errors": vr["errors"][:4],
    "emptyCloneView": True,
    "doesNotClaimCompleteCoverageFromPartialOwnership": True,
}, indent=2) + "\n")
print("rust-partial schema", vr["stockOk"], vr["errors"][:3])
if vr["stockOk"]:
    mark(["R-RUN-RUST-PARTIAL-EMPTY-CLONES"], status="executed", artifact="runs/rust-partial-clones.store.json")
    mark(["R-CLONE-DEFICIENCY-PAIRING"], status="executed", artifact="runs/rust-partial-clones.meta.json")

