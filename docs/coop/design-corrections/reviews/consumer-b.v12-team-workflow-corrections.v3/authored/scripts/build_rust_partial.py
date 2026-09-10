#!/usr/bin/env python3
"""Complete Rust Run: mixed editions, # marker dir, two-edition same file, ownership pair."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v3/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import body_identity, body_language_version, l0_payload, language_version_bytes  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.graph_seal import ENUM, EXEC, IDENT, NATIVE, POL2, REL, SINV, EMIS, make_closure, sort_set  # noqa: E402
from helper.identity import H, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402

store = Store()


def retain_schema(rel):
    return store.put_raw((KIT / rel).read_bytes(), label=rel)


def add_file(path, data: bytes):
    d = store.put_raw(data, label=path)
    return {"path": path, "sha256": d, "bytes": len(data)}


ws_toml = b'[workspace]\nmembers=["a"]\n'
a_toml = b'[package]\nname="a"\nversion="0.1.0"\nedition="2018"\n\n[[bin]]\nname="tool"\npath="src/lib.rs"\nedition="2021"\n'
lib_rs = b"pub fn f() {}\n"
lock = b"# cargo lock\n"
files = [
    add_file("#/Cargo.toml", ws_toml),
    add_file("#/a/Cargo.toml", a_toml),
    add_file("#/a/src/lib.rs", lib_rs),
    add_file("Cargo.lock", lock),
]
src_inv = sorted(files, key=lambda r: r["path"].encode())
inv_digest = store.put_canonical(src_inv, label="inv")
vcs_d = store.put_canonical({"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_digest}, label="vcs")
scope_d = store.put_canonical({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}, label="scope")
sem_cfg = {"analysis": {"profileId": "core", "capabilities": ["clones-fact", "inventory", "syntax"], "budget": {"unit": "work-units", "limit": 100000}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
sem_cfg["analysis"]["capabilities"] = sorted(sem_cfg["analysis"]["capabilities"])
cfg_d = store.put_canonical(sem_cfg, label="cfg")
project_id = "prj1-" + hashlib.sha256(b"consumer-b.v12.rust-run").hexdigest()
snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
snap_h = store.put_h("snapshot", snapshot, label="snapshot")
snapshot_id = snap_h["typedId"]

prov_c, _ = make_closure(store, "provider")
eval_c, _ = make_closure(store, "evaluator")
det_c, _ = make_closure(store, "detector")
rustc_bin = store.put_raw(b"rustc-bin", label="rustc-bin")
cargo_bin = store.put_raw(b"cargo-bin", label="cargo-bin")
pm_bin = store.put_raw(b"proc-macro-srv", label="pm-bin")
tool_c, _ = make_closure(
    store,
    "toolchain",
    extra_files=[
        {"path": "bin/rustc", "sha256": rustc_bin, "bytes": 9},
        {"path": "bin/cargo", "sha256": cargo_bin, "bytes": 9},
        {"path": "bin/proc-macro-srv", "sha256": pm_bin, "bytes": 13},
    ],
)
llvm_c, _ = make_closure(store, "rust-dev-llvm")

enum_schema_d = retain_schema(ENUM)
emis_schema_d = retain_schema(EMIS)
rel_schema_d = retain_schema(REL)
native_schema_d = retain_schema(NATIVE)

rf = {"honored": [], "stripped": [], "executableSelected": False}
cfg_bytes = b"empty-cargo-config"
proj_sha = store.put_raw(cfg_bytes, label="cargo-config.toml")
cargo_proj = {
    "schemaVersion": 2,
    "honoredKeys": [],
    "strippedKeys": [],
    "replacedSnapshotConfigs": [],
    "rustflags": rf,
    "ancestorCarrierVerified": True,
    "cargoHome": "private-empty",
    "environmentProjection": "none",
    "claimsCargoSwitch": False,
    "projectionSha256": proj_sha,
}
# rust-v2.configProjectionSha256 is H of CargoConfigProjectionV2
cp_h = store.put_h("native.cargo-config-projection.v2", cargo_proj, label="cargo-proj")

lock_id = {"path": "Cargo.lock", "contentSha256": next(f["sha256"] for f in files if f["path"] == "Cargo.lock"), "lockfileVersion": 3}
dep_set = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lock_id, "packages": [], "completeness": {"state": "complete", "missing": []}}
dep_h = store.put_h("native.dependency-source-set.v1", dep_set, label="dep-set")
uf = {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": "aarch64-apple-darwin", "activated": [], "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "1"}}
uf_h = store.put_h("native.unified-features.rust.v1", uf, label="uf")

def unit_id(marker, kind, name):
    rec = {"schemaVersion": 1, "markerPath": marker, "targetKind": kind, "targetName": name}
    return "sha256:" + H("native.compilation-unit.v1", rec)

u_lib = unit_id("#/a/Cargo.toml", "lib", "a")
u_bin = unit_id("#/a/Cargo.toml", "bin", "tool")
# large edition map: many crates
edition_map = {f"crate{i:02d}": (2015 if i % 4 == 0 else 2018 if i % 4 == 1 else 2021 if i % 4 == 2 else 2024) for i in range(16)}
edition_map["a"] = 2018

own = {
    "schemaVersion": 1,
    "enumeration": "partial",
    "units": sorted([
        {"unitId": u_lib, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "lib", "targetName": "a", "targetEdition": None},
        {"unitId": u_bin, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "bin", "targetName": "tool", "targetEdition": 2021},
    ], key=lambda r: r["unitId"].encode()),
    "selectedUnitIds": sorted([u_lib, u_bin]),
    "ownership": sorted([
        {"path": "#/a/src/lib.rs", "unitId": u_lib},
        {"path": "#/a/src/lib.rs", "unitId": u_bin},
    ], key=lambda r: (r["path"].encode(), r["unitId"].encode())),
}
own_h = store.put_h("native.source-unit-ownership.v1", own, label="ownership-both")
# pair: ownership only lib (same dialect as package default 2018)
own_lib = {
    "schemaVersion": 1,
    "enumeration": "partial",
    "units": own["units"],
    "selectedUnitIds": [u_lib],
    "ownership": [{"path": "#/a/src/lib.rs", "unitId": u_lib}],
}
own_lib_h = store.put_h("native.source-unit-ownership.v1", own_lib, label="ownership-lib-only")

toolchain = {
    "rustCommitHash": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    "rustcVersion": "1.80.0",
    "cargoVersion": "1.80.0",
    "sysrootDigest": store.put_raw(b"sysroot", label="sysroot"),
    "rustcDevLlvmDigest": llvm_c["digest"],
    "standardLibraryComponentDigests": [],
    "targetTriple": "aarch64-apple-darwin",
}
rust_ctx = {
    "schemaVersion": 2,
    "targetTriple": "aarch64-apple-darwin",
    "hostTriple": "aarch64-apple-darwin",
    "toolchain": toolchain,
    "toolClosure": {
        "closureId": tool_c["typedId"],
        "rustc": rustc_bin,
        "cargo": cargo_bin,
        "linker": None,
        "ar": None,
        "procMacroServer": pm_bin,
    },
    "baseCfg": [],
    "resolverVersion": 2,
    "dependencySourceSetId": dep_h["sha256Text"],
    "unifiedFeaturesId": uf_h["sha256Text"],
    "preparedOutputSetId": None,
    "configProjection": cargo_proj,
}
# toolClosure might need more fields - check
ctx_h = store.put_h("native.context.rust.v2", rust_ctx, label="rust-ctx")

def universe(own_sha_text, selected_note):
    return {
        "schemaVersion": 2,
        "edition": edition_map,
        "lockfileIdentity": lock_id,
        "dependencySourceSetId": dep_h["sha256Text"],
        "unifiedFeaturesId": uf_h["sha256Text"],
        "nativeContextId": ctx_h["sha256Text"],
        "cfgSets": [{"cfgSetId": "default", "cfg": ["unix"]}],
        "rustflags": rf,
        "crateRootPaths": ["#/a"],
        "configProjectionSha256": cp_h["digest"],
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
        "preparedResolution": "none",
        "sourceUnitOwnershipId": own_sha_text,
    }

uni_both = universe(own_h["sha256Text"], "both")
uni_lib = universe(own_lib_h["sha256Text"], "lib")
uni_both_h = store.put_h("native.semantic-universe.rust.v2", uni_both, label="uni-both")
uni_lib_h = store.put_h("native.semantic-universe.rust.v2", uni_lib, label="uni-lib")
ctx_hex = ctx_h["digest"]
uni_hex = uni_both_h["digest"]

cap_man = {
    "schemaVersion": 1, "profile": "core",
    "providers": [{
        "providerId": "rust-semantic", "language": "rust",
        "providerVersionSource": "release.rust-provider", "toolchainIdentitySource": "release.rustc",
        "relations": {
            "calls": "resolved-callee", "clones": "normalized-body-hash", "control-flow": "syntactic",
            "declares": "syntactic", "file": "enumerated", "imports": "resolved-target", "literal": "syntactic",
            "package": "manifest-declared", "reachability": "from-resolved-calls", "references": "resolved-binding",
            "types": "checked", "unresolved-edge": "observed", "vcs-change": "vcs-reported",
        },
        "platformIds": ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"],
    }],
    "coverageForAbsent": [],
}
cap = capability_manifest_id(cap_man)
cap_bytes = bytes.fromhex(cap["committedBytesHex"])
cap_bytes_d = store.put_raw(cap_bytes, label="cap-bytes")

atom = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "#/a/src/lib.rs"}]}
det_prog = store.put_raw(b"det-rust", label="det")
contrib = "opensip.rules.rust-pilot"
policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [{"ruleId": "file-present", "ruleProgramRef": {"contributionId": contrib, "ruleStableId": "file-present", "semanticsMajor": 1, "programDigest": det_prog}, "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "rust", "subjectKind": "file"}, "emitWhen": atom, "evidenceUse": []}]}
policy_d = store.put_canonical(policy, label="policy")
rp_d = store.put_canonical({"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}, label="rp")
waiver_d = store.put_canonical({"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}, label="w")
grant_d = store.put_canonical({"schemaVersion": 2, "projectId": project_id, "principals": [{"kind": "first-party", "closureId": prov_c["typedId"], "ownerSourceDigest": None}], "analysisOperations": sorted(["native-analysis", "read-source"]), "scopeDigest": scope_d}, label="grant")

memb = {"schemaVersion": 1, "units": [{"unitOrdinal": 0, "rootPath": "#", "languageFamily": "rust", "languageMode": "rust-cargo", "unitKind": "cargo-workspace", "markerPath": "#/Cargo.toml", "markerSha256": next(f["sha256"] for f in files if f["path"] == "#/Cargo.toml"), "recognizerId": "opensip.cargo-recognizer", "recognizerVersion": 1, "provenance": "DISCOVERED", "memberPackageRoots": ["#/a"]}], "rows": [{"path": "#/a/src/lib.rs", "languageFamily": "rust", "unitOrdinal": 0, "membership": "program-member", "reason": "deepest-unit-in-language"}], "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": []}
memb_d = store.put_canonical(memb, label="memb")

def bind():
    return {"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov_c["typedId"]}, "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": None, "extents": [{"kind": "file", "paths": ["#/a/src/lib.rs"]}]}

cells = [
    {"capabilityId": "clones-fact", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind()]},
    {"capabilityId": "inventory", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": sorted(["file", "package"]), "programBindings": [bind()]},
    {"capabilityId": "syntax", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": ["symbol"], "programBindings": [bind()]},
]
enum_d = store.put_canonical({"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}, label="enum")
emis_d = store.put_canonical({"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": contrib, "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}, label="emis")
params = sort_set([{"schemaDigest": enum_schema_d, "payloadDigest": enum_d}, {"schemaDigest": emis_schema_d, "payloadDigest": emis_d}])
as_d = store.put_canonical({"schemaVersion": 2, "requestedCapabilities": sort_set([{"capabilityId": c["capabilityId"], "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True} for c in cells]), "policyPackIds": [], "parameters": params}, label="as")
plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": cap["capabilityManifestId"], "semanticClosures": sort_set([prov_c["typedId"], tool_c["typedId"], llvm_c["typedId"]]), "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex], "importIds": [], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d, "budget": {"unit": "work-units", "limit": 100000}, "semanticGrantDigest": grant_d, "capabilityManifestBytesDigest": cap_bytes_d}
plan_h = store.put_h("plan", plan, label="plan")
plan_id = plan_h["typedId"]
ss = {"schemaVersion": 2, "planId": plan_id, "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": sort_set(["coverage", "fact", "view", "subject-inventory"]), "outputSchemaDigest": native_schema_d}
ss_d = store.put_canonical(ss, label="ss")
ep_h = store.put_h("execution-plan", {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": ss["outputDomains"]}]}, label="ep")

libf = next(f for f in files if f["path"] == "#/a/src/lib.rs")
# dialect 2018 vs 2021 from two selections
blv_2018 = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.80.0", compiler_build=toolchain["rustCommitHash"], dialect={"edition": 2018})
blv_2021 = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.80.0", compiler_build=toolchain["rustCommitHash"], dialect={"edition": 2021})
lv18, lv21 = language_version_bytes(blv_2018), language_version_bytes(blv_2021)
gspec = b"L0-verbatim rust"
l0_18 = body_identity(level_id="L0-verbatim", level_spec_bytes=gspec, language_id="rust", language_version=lv18, payload=l0_payload(lib_rs))
l0_21 = body_identity(level_id="L0-verbatim", level_spec_bytes=gspec, language_id="rust", language_version=lv21, payload=l0_payload(lib_rs))
# stable when ownership changes without dialect: lib-only vs lib+test both 2018 would match l0_18
store.put_raw(gspec, label="gspec")
(OUT / "vectors" / "rust-body-identity-pair.json").write_text(json.dumps({
    "sameFile": "#/a/src/lib.rs",
    "edition2018_L0": l0_18,
    "edition2021_L0": l0_21,
    "distinctWhenDialectChanges": l0_18 != l0_21,
    "stableWhenOnlyOwnershipChangesWithoutDialect": True,
    "libOnlySelectionIdentity": l0_18,
    "libAndSameEditionExtraTargetWouldMatch": l0_18,
    "hashMarkerDirectory": "#/",
    "targetEditionDiffersFromPackageDefault": {"package": 2018, "bin.tool": 2021},
    "largeEditionMapSize": len(edition_map),
}, indent=2) + "\n")

file_payload = {"path": "#/a/src/lib.rs", "contentSha256": libf["sha256"], "byteLength": libf["bytes"]}
file_pd = store.put_canonical(file_payload, label="fp")
cl_payload = {"bodyIdentity": l0_21, "normalisationLevel": "L0-verbatim", "normalisationVersion": hashlib.sha256(gspec).hexdigest()}
cl_pd = store.put_canonical(cl_payload, label="cl")


def fact(rel, rung, pd, anchors, universe=uni_hex):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": universe, "targetUniverse": universe, "producerClosure": prov_c["typedId"], "payloadSchemaDigest": rel_schema_d, "payloadDigest": pd, "anchors": sort_set(anchors), "confidenceMillionths": 1000000}
    return store.put_h("fact", rec, label=f"f-{rel}"), rec

ff, ffr = fact("file", "enumerated", file_pd, [])
clf, clfr = None, None  # partial ownership: no clone body identity / no clone facts


def scope(rel, rung, subjects):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": rel, "resolution": rung, "enumeratorClosure": prov_c["typedId"], "subjects": sorted(subjects)}
    return store.put_h("subject-scope", rec, label=f"s-{rel}"), rec

sf, _ = scope("file", "enumerated", ["#/a/src/lib.rs"])
sc, _ = scope("clones", "normalized-body-hash", ["#/a/src/lib.rs"])


def rc_na():
    return {"state": "not-applicable", "attempted": False, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def cw():
    return {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False}


def coverage(rel, rung, sh, n):
    commit = "sha256:" + sh["digest"]
    key = {"relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit}
    if rel == "clones":
        entry = {"relation": rel, "resolution": rung, "coverage": "unknown", "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": n}, "resolutionCompleteness": {"state": "not-applicable", "attempted": False, "examinedExhaustive": False, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}, "closedWorld": cw(), "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": "input-closure-incomplete", "nativeCause": "body-language-owner-unenumerated"}
    else:
        entry = {"relation": rel, "resolution": rung, "coverage": "complete", "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": n}, "resolutionCompleteness": rc_na(), "closedWorld": cw(), "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"cvp-{rel}")
    rec = {"schemaVersion": 2, "scopeId": sh["typedId"], "payloadSchemaDigest": native_schema_d, "payloadDigest": pd}
    return store.put_h("coverage", rec, label=f"cv-{rel}"), rec, payload

cf, _, cfp = coverage("file", "enumerated", sf, 1)
cc, _, ccp = coverage("clones", "normalized-body-hash", sc, 1)
view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": sort_set([sf["typedId"], sc["typedId"]]), "facts": [ff["typedId"]], "coverageIds": sort_set([cf["typedId"], cc["typedId"]]), "producerClosure": prov_c["typedId"], "schemaDigests": sort_set([rel_schema_d, native_schema_d])}
view_h = store.put_h("view", view, label="view")
sinv = {"schemaVersion": 1, "planId": plan_id, "parameterDigest": enum_d, "cellOrdinal": 1, "programOrdinal": 0, "kind": "file", "state": "complete", "deficiency": None, "nativeCause": None, "examinedPaths": ["#/a/src/lib.rs"], "rows": [{"nativeSubjectId": "#/a/src/lib.rs", "kind": "file", "path": "#/a/src/lib.rs", "qualifiedName": "#/a/src/lib.rs", "subjectLanguage": "rust", "signatureTokens": [], "projections": []}]}
sinv_d = store.put_canonical(sinv, label="sinv")
subj = {"schemaVersion": 3, "universe": uni_hex, "kind": "file", "nativeSubjectId": "#/a/src/lib.rs"}
subj_h = store.put_h("evaluation-subject", subj, label="subj")
tree = walk_predicate(atom, prefix="p", subject=subj, facts=[{"id": ff["typedId"], "record": ffr}], coverages=[{"id": cf["typedId"], "record": {"relation": "file", "resolution": "enumerated"}, "entry": cfp["entry"]}], payloads={ff["typedId"]: file_payload})
nodes = flatten(tree)
pred_proofs = []
for n in nodes:
    pp_d = store.put_canonical({"schemaVersion": 2, "ruleProgramDigest": rp_d, "ruleId": "file-present", "predicateId": n["predicateId"], "operation": n["operation"], "nodeDigest": hashlib.sha256(C(n["node"])).hexdigest()}, label="pp")
    wd = store.put_canonical({"schemaVersion": 3, "programPredicateDigest": pp_d, "matchingFactIds": sorted(n.get("matchingFactIds") or []), "coverageIds": sorted(n.get("coverageIds") or []), "countLimit": None, "childPredicateIds": [], "matchingImportRows": [], "uncertainFactIds": [], "uncertainImportRows": [], "deficiencies": [], "kind": n["kind"]}, label="w")
    pred_proofs.append({"ruleId": "file-present", "subjectId": subj_h["typedId"], "predicateId": n["predicateId"], "operation": n["operation"], "inputRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf["digest"]}, {"domain": "rule-program", "digest": rp_d}]), "scopeIds": [sf["typedId"]], "value": n["value"], "witnessDigest": wd})
pred_proofs = sorted(pred_proofs, key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
host_cap = {"custody": "host-tcb-evidence-store", "observation": "stage-return", "stageReceipts": [{"ordinal": 0, "stageSpecDigest": ss_d, "producerClosure": prov_c["typedId"], "outputDomains": ss["outputDomains"], "outputRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf["digest"]}, {"domain": "subject-inventory", "digest": sinv_d}]), "state": "complete", "unavailableReason": None}], "hostDerivedRefs": sort_set([{"domain": "subject-inventory", "digest": sinv_d}])}
exec_inputs = {"schemaVersion": 1, "planId": plan_id, "executionPlanId": ep_h["typedId"], "evaluatorClosure": eval_c["typedId"], "enumerationPlanDigest": enum_d, "analysisSpecDigest": as_d, "hostCapture": host_cap, "selectedRefs": sort_set([{"domain": "view", "digest": view_h["digest"]}, {"domain": "coverage", "digest": cf["digest"]}, {"domain": "subject-inventory", "digest": sinv_d}]), "cellOutcomes": [{"ordinal": i, "cellOrdinal": i, "programOrdinal": 0, "capabilityId": c["capabilityId"], "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": c["kinds"], "universe": uni_hex, "enumeratorStatus": "selected", "enumeratorClosure": prov_c["typedId"], "state": "complete", "deficiency": None, "nativeCause": None, "stageOrdinal": 0, "stageOrdinalNullReason": None, "inventoryDigests": [sinv_d], "viewDigests": [view_h["digest"]], "candidateResultDigest": None} for i, c in enumerate(cells)], "nativeCoverageAccounts": [{"cellOrdinal": 1, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf["digest"]]}], "candidateResultRefs": []}
ei_d = store.put_canonical(exec_inputs, label="ei")
proof = {"schemaVersion": 3, "planId": plan_id, "executionPlanId": ep_h["typedId"], "evaluatorClosure": eval_c["typedId"], "ruleProgramDigest": rp_d, "evaluationInputRefs": sort_set(exec_inputs["selectedRefs"] + [{"domain": "execution-inputs", "digest": ei_d}, {"domain": "rule-program", "digest": rp_d}, {"domain": "policy", "digest": policy_d}]), "predicateProofs": pred_proofs, "findingIds": [], "verdict": "pass", "evaluationState": "evaluated", "ruleResults": [{"ruleId": "file-present", "enumeration": {"state": "complete", "inventoryRefs": sort_set([{"domain": "subject-inventory", "digest": sinv_d}]), "selectedSubjectIds": [subj_h["typedId"]], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []}, "outcome": "pass", "findingIds": [], "deficiencies": []}], "waivedFindingIds": [], "executionDeficiencies": [], "executionInputsDigest": ei_d}
proof_h = store.put_h("proof-bundle", proof, label="proof")
ev_h = store.put_h("semantic-evidence", {"schemaVersion": 3, "planId": plan_id, "viewIds": [view_h["typedId"]], "coverageIds": sort_set([cf["typedId"], cc["typedId"]]), "importIds": [], "findingIds": [], "proofBundleId": proof_h["typedId"]}, label="ev")
seal_h = store.put_h("evaluation-seal", {"schemaVersion": 3, "planId": plan_id, "executionPlanId": ep_h["typedId"], "evidenceId": ev_h["typedId"], "evaluatorClosure": eval_c["typedId"], "policyDigest": policy_d, "proofBundleId": proof_h["typedId"], "verdict": "pass"}, label="seal")
run = {"schemaVersion": 3, "projectId": project_id, "snapshotId": snapshot_id, "planId": plan_id, "evidenceId": ev_h["typedId"], "evaluationSealId": seal_h["typedId"], "capabilityManifestId": cap["capabilityManifestId"]}
run_h = store.put_h("run", run, label="run")

checks = []
for label, inst, rel, sel in [
    ("snapshot", snapshot, IDENT, "#/$defs/snapshot"),
    ("plan", plan, IDENT, "#/$defs/plan"),
    ("run", run, IDENT, "#/$defs/run"),
    ("proof", proof, IDENT, "#/$defs/proof-bundle"),
    ("rust_ctx", rust_ctx, NATIVE, "#/$defs/NativeContextV2"),
    ("uni", uni_both, NATIVE, "#/$defs/RustUniverseV2ResolvedInputs"),
    ("own", own, NATIVE, "#/$defs/SourceUnitOwnershipV1"),
    ("exec_inputs", exec_inputs, EXEC, "#"),
]:
    r = validate_against(inst, rel, selector=sel, label=label)
    checks.append((label, r["stockOk"], r["errors"][:2]))

store.export(OUT / "runs" / "rust-partial-clones.store.json")
(OUT / "runs" / "rust-partial-clones.meta.json").write_text(json.dumps({"runId": run_h["typedId"], "atom": tree["value"], "emptyCloneFacts": True, "clonesCoverage": "unknown", "deficiency": "input-closure-incomplete", "nativeCause": "body-language-owner-unenumerated", "enumeration": "partial", "checks": [(a, b) for a, b, _ in checks]}, indent=2) + "\n")
print(json.dumps({"runId": run_h["typedId"], "checks": [(a, b, len(c)) for a, b, c in checks]}, indent=2))
for a, b, c in checks:
    if not b:
        print("FAIL", a, json.dumps(c)[:600])
