#!/usr/bin/env python3
"""Syntax-data complete Run + Rust partial-enumeration clones Run."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-foundation-phase4-corrections.v3/subject")
sys.path.insert(0, str(OUT))

from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.graph_seal import ENUM, EXEC, IDENT, NATIVE, POL2, REL, SINV, EMIS, make_closure, sort_set  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.seal_run import close_execution_and_proof, mint_inventory, plan_semantic_closures  # noqa: E402
from helper.execution_inputs import vcs_applicability  # noqa: E402
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
bundle_blob = store.put_raw(b"gb", label="gb")
g_file = store.put_raw(b"json-g", label="jg")
spec_d = store.put_raw(b"spec", label="spec")
g_c, _ = make_closure(
    store,
    "grammar",
    extra_files=[
        {"path": "bundle/archive", "sha256": bundle_blob, "bytes": 2},
        {"path": "grammars/json.bin", "sha256": g_file, "bytes": 6},
        {"path": "normalizer/specification", "sha256": spec_d, "bytes": 4},
    ],
)
gb = {"schemaVersion": 1, "closureId": g_c["typedId"], "parserName": "opensip-syntax-parser", "parserVersion": "1.0.0", "bundleDigest": bundle_blob, "grammars": [{"grammarId": "json", "grammarVersion": "1.0.0", "languageId": "json", "syntaxClass": "data-document", "suffixes": [".json"], "grammarDigest": g_file}], "normalizer": {"normalizerId": "n", "normalizerVersion": "1.0.0", "specificationDigest": spec_d}}
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
memb = {"schemaVersion": 1, "units": [], "rows": [{"path": "notes.json", "languageFamily": "none", "unitOrdinal": None, "membership": "syntax-only", "reason": "grammar-only"}], "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
memb_d = store.put_canonical(memb, label="m")
def bind(kinds):
    extents = []
    for k in kinds:
        if k == "file":
            extents.append({"kind": "file", "paths": ["notes.json"]})
        elif k == "package":
            extents.append({"kind": "package", "paths": []})
        elif k == "symbol":
            extents.append({"kind": "symbol", "paths": ["notes.json"]})
    return {"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov_c["typedId"]}, "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": None, "extents": sorted(extents, key=lambda x: x["kind"].encode())}

cells = [
    {"capabilityId": "clones-fact", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind(["file"])]},
    {"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True, "kinds": sorted(["file", "package"]), "programBindings": [bind(["file", "package"])]},
]
# cells order by capabilityId: clones-fact then inventory
cells = sorted(cells, key=lambda c: (c["capabilityId"], c["languageMode"], c["workspaceRoot"]))
enum_d = store.put_canonical({"schemaVersion": 1, "snapshotId": snap_h["typedId"], "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}, label="e")
emis_d = store.put_canonical({"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": "opensip.rules.data", "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}, label="em")
params = sort_set([{"schemaDigest": enum_s, "payloadDigest": enum_d}, {"schemaDigest": emis_s, "payloadDigest": emis_d}])
as_d = store.put_canonical({"schemaVersion": 2, "requestedCapabilities": sort_set([{"capabilityId": c["capabilityId"], "languageMode": "syntax-only", "workspaceRoot": ".", "required": True} for c in cells]), "policyPackIds": [], "parameters": params}, label="as")
plan = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "capabilityManifestId": cap["capabilityManifestId"], "semanticClosures": plan_semantic_closures(provider=prov_c["typedId"], evaluator=eval_c["typedId"], detector=det_c["typedId"], extras=[g_c["typedId"]]), "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex], "importIds": [], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d, "budget": {"unit": "work-units", "limit": 10000}, "semanticGrantDigest": grant_d, "capabilityManifestBytesDigest": cap_b}
plan_h = store.put_h("plan", plan, label="plan")
ss = {"schemaVersion": 2, "planId": plan_h["typedId"], "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": ["view"], "outputSchemaDigest": nat_s}
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
sp = {"schemaVersion": 2, "snapshotId": snap_h["typedId"], "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": "package", "resolution": "manifest-declared", "enumeratorClosure": prov_c["typedId"], "subjects": []}
sp_h = store.put_h("subject-scope", sp, label="sp")
cp_h, cpp = cov("package", "manifest-declared", sp_h, "complete", None, None, {**rc_na, "examinedExhaustive": True})
# cov() uses subjectCount 1 always - package empty needs 0. remint:
commit_p = "sha256:" + sp_h["digest"]
cpp = {"schemaVersion": 3, "key": {"relation": "package", "resolution": "manifest-declared", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit_p}, "entry": {"relation": "package", "resolution": "manifest-declared", "coverage": "complete", "examinedUniverse": {"subjectScopeCommitment": commit_p, "subjectCount": 0}, "resolutionCompleteness": rc_na, "closedWorld": cfp["entry"]["closedWorld"], "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}}
pd_pkg = store.put_canonical(cpp, label="cvp-package")
cp_rec = {"schemaVersion": 2, "scopeId": sp_h["typedId"], "payloadSchemaDigest": nat_s, "payloadDigest": pd_pkg}
cp_h = store.put_h("coverage", cp_rec, label="cv-package")
view = {"schemaVersion": 2, "planId": plan_h["typedId"], "scopeIds": sort_set([sf_h["typedId"], sc_h["typedId"], sp_h["typedId"]]), "facts": [ff_h["typedId"]], "coverageIds": sort_set([cf_h["typedId"], cc_h["typedId"], cp_h["typedId"]]), "producerClosure": prov_c["typedId"], "schemaDigests": sort_set([rel_s, nat_s])}
view_h = store.put_h("view", view, label="view")
file_row = {"nativeSubjectId": "notes.json", "kind": "file", "path": "notes.json", "qualifiedName": "notes.json", "subjectLanguage": "json", "signatureTokens": [], "projections": []}
invs = [
    mint_inventory(store, plan_id=plan_h["typedId"], enum_d=enum_d, cell_ordinal=0, kind="file", rows=[file_row], examined=["notes.json"]),
    mint_inventory(store, plan_id=plan_h["typedId"], enum_d=enum_d, cell_ordinal=1, kind="file", rows=[file_row], examined=["notes.json"]),
    mint_inventory(store, plan_id=plan_h["typedId"], enum_d=enum_d, cell_ordinal=1, kind="package", rows=[], examined=[]),
]
coverages_full = []
for hid, payload in [(cf_h, cfp), (cc_h, ccp), (cp_h, cpp)]:
    coverages_full.append({"id": hid["typedId"], "digest": hid["digest"], "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]}, "payload": payload, "entry": payload["entry"]})
nca = [
    {"cellOrdinal": 0, "programOrdinal": 0, "relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cc_h["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf_h["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "package", "resolution": "manifest-declared", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cp_h["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "vcs-change", "resolution": "vcs-reported", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": vcs_applicability({"kind": "none"}), "coverageIds": []},
]
rp = {"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}
pre_checks = [
    {"label": "clones-cov", "stockOk": validate_against(ccp, NATIVE, selector="#/$defs/CoverageResultV3", label="clones-cov")["stockOk"], "errors": []},
    {"label": "plan", "stockOk": validate_against(plan, IDENT, selector="#/$defs/plan", label="plan")["stockOk"], "errors": []},
]
out = close_execution_and_proof(
    store,
    plan_id=plan_h["typedId"],
    exec_plan_id=ep_h["typedId"],
    ss_d=ss_d,
    prov_c=prov_c["typedId"],
    eval_c=eval_c["typedId"],
    policy=policy,
    policy_d=policy_d,
    rule_program=rp,
    rp_d=rp_d,
    enum_d=enum_d,
    as_d=as_d,
    uni_hex=uni_hex,
    language_mode="syntax-only",
    cells=cells,
    view=view,
    view_h=view_h,
    facts_for_eval=[{"id": ff_h["typedId"], "record": ff}],
    payloads={ff_h["typedId"]: fp},
    coverages_full=coverages_full,
    inventories=invs,
    nca=nca,
    vcs={"kind": "none"},
    import_ids=[],
    file_scope_id=sf_h["typedId"],
    atom=atom,
    project_id=project_id,
    snapshot_id=snap_h["typedId"],
    cap_id=cap["capabilityManifestId"],
    export_stem="syntax-data",
    extra_meta={"clonesCoverage": "unknown", "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"},
    schema_checks=pre_checks,
)
print(json.dumps({"syntax-data": out["runId"], "verdict": out["verdict"], "failed": out["failed"], "derived": out["derived"]}, indent=2, default=str))
for c in out["failed"]:
    print("FAIL", c)


