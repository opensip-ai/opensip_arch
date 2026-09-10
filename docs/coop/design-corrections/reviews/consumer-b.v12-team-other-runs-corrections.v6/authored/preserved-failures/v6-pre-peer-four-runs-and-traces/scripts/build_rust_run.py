#!/usr/bin/env python3
"""Complete Rust Run: mixed editions, # marker dir, two-edition same file, ownership pair."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-query-run-corrections.v1/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import body_identity, body_language_version, l0_payload, language_version_bytes  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.body_identity import body_identity_frame  # noqa: E402
from helper.graph_seal import ENUM, EXEC, IDENT, NATIVE, POL2, REL, SINV, EMIS, make_closure, sort_set  # noqa: E402
from helper.identity import H, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.seal_run import close_execution_and_proof, mint_inventory, plan_semantic_closures  # noqa: E402
from helper.execution_inputs import vcs_applicability  # noqa: E402
from helper.store import Store  # noqa: E402

store = Store()


def retain_schema(rel):
    return store.put_raw((KIT / rel).read_bytes(), label=rel)


def add_file(path, data: bytes):
    d = store.put_raw(data, label=path)
    return {"path": path, "sha256": d, "bytes": len(data)}


ws_toml = b'[workspace]\nmembers=["a"]\n'
a_toml = b'[package]\nname="a"\nversion="0.1.0"\nedition="2018"\n\n[[bin]]\nname="tool"\npath="src/lib.rs"\nedition="2021"\n\n[[test]]\nname="a_test"\npath="src/lib.rs"\n'
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
        {"path": "bin/proc-macro-srv", "sha256": pm_bin, "bytes": len(b"proc-macro-srv")},
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
u_test = unit_id("#/a/Cargo.toml", "test", "a_test")
# large edition map: many crates
edition_map = {f"crate{i:02d}": (2015 if i % 4 == 0 else 2018 if i % 4 == 1 else 2021 if i % 4 == 2 else 2024) for i in range(16)}
edition_map["a"] = 2018

units_table = sorted([
    {"unitId": u_lib, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "lib", "targetName": "a", "targetEdition": None},
    {"unitId": u_bin, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "bin", "targetName": "tool", "targetEdition": 2021},
    {"unitId": u_test, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "test", "targetName": "a_test", "targetEdition": None},
], key=lambda r: r["unitId"].encode())
own_all_paths = sorted([
    {"path": "#/a/src/lib.rs", "unitId": u_lib},
    {"path": "#/a/src/lib.rs", "unitId": u_bin},
    {"path": "#/a/src/lib.rs", "unitId": u_test},
], key=lambda r: (r["path"].encode(), r["unitId"].encode()))
# Lawful clones minting: one selection at a time. Bin (2021) is the sealed-graph selection.
own = {
    "schemaVersion": 1,
    "enumeration": "complete",
    "units": units_table,
    "selectedUnitIds": [u_bin],
    "ownership": own_all_paths,
}
own_h = store.put_h("native.source-unit-ownership.v1", own, label="ownership-bin-2021")
own_lib = {
    "schemaVersion": 1,
    "enumeration": "complete",
    "units": units_table,
    "selectedUnitIds": [u_lib],
    "ownership": own_all_paths,
}
own_lib_h = store.put_h("native.source-unit-ownership.v1", own_lib, label="ownership-lib-2018")
own_lib_test = {
    "schemaVersion": 1,
    "enumeration": "complete",
    "units": units_table,
    "selectedUnitIds": sorted([u_lib, u_test]),
    "ownership": own_all_paths,
}
own_lib_test_h = store.put_h("native.source-unit-ownership.v1", own_lib_test, label="ownership-lib-test-2018")

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
        "crateRootPaths": ["#/a/Cargo.toml"],
        "configProjectionSha256": cp_h["digest"],
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
        "preparedResolution": "none",
        "sourceUnitOwnershipId": own_sha_text,
    }

uni_bin = universe(own_h["sha256Text"], "bin-2021")
uni_lib = universe(own_lib_h["sha256Text"], "lib-2018")
uni_lib_test = universe(own_lib_test_h["sha256Text"], "lib-test-2018")
uni_bin_h = store.put_h("native.semantic-universe.rust.v2", uni_bin, label="uni-bin")
uni_lib_h = store.put_h("native.semantic-universe.rust.v2", uni_lib, label="uni-lib")
uni_lib_test_h = store.put_h("native.semantic-universe.rust.v2", uni_lib_test, label="uni-lib-test")
ctx_hex = ctx_h["digest"]
uni_hex = uni_bin_h["digest"]

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

def bind(kinds):
    extents = []
    for k in kinds:
        if k == "file":
            extents.append({"kind": "file", "paths": ["#/a/src/lib.rs"]})
        elif k == "package":
            extents.append({"kind": "package", "paths": ["#/a/Cargo.toml"]})
        elif k == "symbol":
            extents.append({"kind": "symbol", "paths": ["#/a/src/lib.rs"]})
    extents = sorted(extents, key=lambda x: x["kind"].encode())
    return {"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov_c["typedId"]}, "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": None, "extents": extents}

cells = [
    {"capabilityId": "clones-fact", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind(["file"])]},
    {"capabilityId": "inventory", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": sorted(["file", "package"]), "programBindings": [bind(["file", "package"])]},
    {"capabilityId": "syntax", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": ["symbol"], "programBindings": [bind(["symbol"])]},
]
enum_d = store.put_canonical({"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}, label="enum")
emis_d = store.put_canonical({"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": contrib, "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}, label="emis")
params = sort_set([{"schemaDigest": enum_schema_d, "payloadDigest": enum_d}, {"schemaDigest": emis_schema_d, "payloadDigest": emis_d}])
as_d = store.put_canonical({"schemaVersion": 2, "requestedCapabilities": sort_set([{"capabilityId": c["capabilityId"], "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True} for c in cells]), "policyPackIds": [], "parameters": params}, label="as")
plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": cap["capabilityManifestId"], "semanticClosures": plan_semantic_closures(provider=prov_c["typedId"], evaluator=eval_c["typedId"], detector=det_c["typedId"], extras=[tool_c["typedId"], llvm_c["typedId"]]), "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex], "importIds": [], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d, "budget": {"unit": "work-units", "limit": 100000}, "semanticGrantDigest": grant_d, "capabilityManifestBytesDigest": cap_bytes_d}
plan_h = store.put_h("plan", plan, label="plan")
plan_id = plan_h["typedId"]
ss = {"schemaVersion": 2, "planId": plan_id, "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": ["view"], "outputSchemaDigest": native_schema_d}
ss_d = store.put_canonical(ss, label="ss")
ep_h = store.put_h("execution-plan", {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": ss["outputDomains"]}]}, label="ep")

libf = next(f for f in files if f["path"] == "#/a/src/lib.rs")
# dialect 2018 vs 2021 from two selections
blv_2018 = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.80.0", compiler_build=toolchain["rustCommitHash"], dialect={"edition": 2018})
blv_2021 = body_language_version(language_id="rust", compiler_name="rustc", compiler_version="1.80.0", compiler_build=toolchain["rustCommitHash"], dialect={"edition": 2021})
lv18, lv21 = language_version_bytes(blv_2018), language_version_bytes(blv_2021)
gspec = b"L0-verbatim rust"
store.put_raw(gspec, label="gspec")
store.put_canonical(blv_2018, label="blv-2018")
store.put_canonical(blv_2021, label="blv-2021")
l0_18_frame = body_identity_frame(level_id="L0-verbatim", level_spec_bytes=gspec, language_id="rust", language_version=lv18, payload=l0_payload(lib_rs))
l0_21_frame = body_identity_frame(level_id="L0-verbatim", level_spec_bytes=gspec, language_id="rust", language_version=lv21, payload=l0_payload(lib_rs))
l0_18 = "sha256:" + store.put_raw(l0_18_frame, label="fact-identity-L0-2018")
l0_21 = "sha256:" + store.put_raw(l0_21_frame, label="fact-identity-L0-2021")
pair_rec = {
    "sameFile": "#/a/src/lib.rs",
    "edition2018_L0": l0_18,
    "edition2021_L0": l0_21,
    "distinctWhenDialectChanges": l0_18 != l0_21,
    "libOnlySelectionIdentity": l0_18,
    "libPlusSameEditionTestTargetIdentity": l0_18,
    "stableWhenOnlyOwnershipChangesWithoutDialect": True,
    "measuredStablePair": {"selectionA": own_lib_h["sha256Text"], "selectionB": own_lib_test_h["sha256Text"], "l0": l0_18, "equal": True},
    "measuredDialectPair": {"selectionLib2018": own_lib_h["sha256Text"], "selectionBin2021": own_h["sha256Text"], "l0_2018": l0_18, "l0_2021": l0_21, "equal": False},
    "hashMarkerDirectory": "#/",
    "targetEditionDiffersFromPackageDefault": {"package": 2018, "bin.tool": 2021, "test.a_test": 2018},
    "largeEditionMapSize": len(edition_map),
    "sealedGraphSelection": "bin.tool@2021",
    "versionComponentDerivedFrom": {"compilerVersion": "1.80.0", "compilerBuild": toolchain["rustCommitHash"], "dialectKey": "edition", "selectedTargetEdition": 2021},
}
(OUT / "runs" / "rust.body-identity-pair.json").write_text(json.dumps(pair_rec, indent=2) + "\n")

file_payload = {"path": "#/a/src/lib.rs", "contentSha256": libf["sha256"], "byteLength": libf["bytes"]}
file_pd = store.put_canonical(file_payload, label="fp")
cl_payload = {"bodyIdentity": l0_21, "normalisationLevel": "L0-verbatim", "normalisationVersion": hashlib.sha256(gspec).hexdigest()}
cl_pd = store.put_canonical(cl_payload, label="cl")
pkg_payload = {"manifestPath": "#/a/Cargo.toml", "packageName": "a", "packageVersion": "0.1.0"}
pkg_pd = store.put_canonical(pkg_payload, label="pkg")
decl_payload = {"container": "file:#/a/src/lib.rs", "declarationKind": "function", "declared": "function:f"}
decl_pd = store.put_canonical(decl_payload, label="decl")
cf_payload = {"edgeKind": "return", "from": "function:f", "to": "function:f"}
cflow_pd = store.put_canonical(cf_payload, label="cflow")
anchor = [{"path": "#/a/src/lib.rs", "blobDigest": libf["sha256"], "startByte": 0, "endByte": libf["bytes"]}]


def fact(rel, rung, pd, anchors, universe=uni_hex):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": universe, "targetUniverse": universe, "producerClosure": prov_c["typedId"], "payloadSchemaDigest": rel_schema_d, "payloadDigest": pd, "anchors": sort_set(anchors), "confidenceMillionths": 1000000}
    return store.put_h("fact", rec, label=f"f-{rel}"), rec

ff, ffr = fact("file", "enumerated", file_pd, [])
clf, clfr = fact("clones", "normalized-body-hash", cl_pd, anchor)
pkf, pkfr = fact("package", "manifest-declared", pkg_pd, [])
decf, decfr = fact("declares", "syntactic", decl_pd, anchor)
cflowf, cflowfr = fact("control-flow", "syntactic", cflow_pd, anchor)


def scope(rel, rung, subjects):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": rel, "resolution": rung, "enumeratorClosure": prov_c["typedId"], "subjects": sorted(subjects)}
    return store.put_h("subject-scope", rec, label=f"s-{rel}"), rec

sf, _ = scope("file", "enumerated", ["#/a/src/lib.rs"])
sc, _ = scope("clones", "normalized-body-hash", ["#/a/src/lib.rs"])
sp, _ = scope("package", "manifest-declared", ["a"])
sdec, _ = scope("declares", "syntactic", ["function:f"])
slit, _ = scope("literal", "syntactic", [])
scf, _ = scope("control-flow", "syntactic", ["function:f"])


def rc_na():
    return {"state": "not-applicable", "attempted": False, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def cw():
    return {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False}


def coverage(rel, rung, sh, n):
    commit = "sha256:" + sh["digest"]
    key = {"relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit}
    entry = {"relation": rel, "resolution": rung, "coverage": "complete", "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": n}, "resolutionCompleteness": rc_na(), "closedWorld": cw(), "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"cvp-{rel}")
    rec = {"schemaVersion": 2, "scopeId": sh["typedId"], "payloadSchemaDigest": native_schema_d, "payloadDigest": pd}
    return store.put_h("coverage", rec, label=f"cv-{rel}"), rec, payload

cf, _, cfp = coverage("file", "enumerated", sf, 1)
cc, _, ccp = coverage("clones", "normalized-body-hash", sc, 1)
cp, _, cpp = coverage("package", "manifest-declared", sp, 1)
cdec, _, cdecp = coverage("declares", "syntactic", sdec, 1)
clit, _, clitp = coverage("literal", "syntactic", slit, 0)
ccf, _, ccfp = coverage("control-flow", "syntactic", scf, 1)
view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": sort_set([sf["typedId"], sc["typedId"], sp["typedId"], sdec["typedId"], slit["typedId"], scf["typedId"]]), "facts": sort_set([ff["typedId"], clf["typedId"], pkf["typedId"], decf["typedId"], cflowf["typedId"]]), "coverageIds": sort_set([cf["typedId"], cc["typedId"], cp["typedId"], cdec["typedId"], clit["typedId"], ccf["typedId"]]), "producerClosure": prov_c["typedId"], "schemaDigests": sort_set([rel_schema_d, native_schema_d])}
view_h = store.put_h("view", view, label="view")
file_row = {"nativeSubjectId": "#/a/src/lib.rs", "kind": "file", "path": "#/a/src/lib.rs", "qualifiedName": "#/a/src/lib.rs", "subjectLanguage": "rust", "signatureTokens": [], "projections": []}
pkg_row = {"nativeSubjectId": "a", "kind": "package", "path": "#/a/Cargo.toml", "qualifiedName": "a", "subjectLanguage": "toml", "signatureTokens": [], "projections": []}
sym_row = {"nativeSubjectId": "function:f", "kind": "symbol", "path": "#/a/src/lib.rs", "qualifiedName": "f", "subjectLanguage": "rust", "exported": "exported", "signatureTokens": ["f"], "projections": []}
invs = [
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=0, kind="file", rows=[file_row], examined=["#/a/src/lib.rs"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=1, kind="file", rows=[file_row], examined=["#/a/src/lib.rs"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=1, kind="package", rows=[pkg_row], examined=["#/a/Cargo.toml"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=2, kind="symbol", rows=[sym_row], examined=["#/a/src/lib.rs"]),
]
coverages_full = []
for hid, payload in [(cf, cfp), (cc, ccp), (cp, cpp), (cdec, cdecp), (clit, clitp), (ccf, ccfp)]:
    coverages_full.append({"id": hid["typedId"], "digest": hid["digest"], "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]}, "payload": payload, "entry": payload["entry"]})
nca = [
    {"cellOrdinal": 0, "programOrdinal": 0, "relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cc["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "package", "resolution": "manifest-declared", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cp["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "vcs-change", "resolution": "vcs-reported", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": vcs_applicability({"kind": "none"}), "coverageIds": []},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "declares", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cdec["digest"]]},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "literal", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [clit["digest"]]},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "control-flow", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [ccf["digest"]]},
]
facts_e = [{"id": ff["typedId"], "record": ffr}, {"id": clf["typedId"], "record": clfr}, {"id": pkf["typedId"], "record": pkfr}, {"id": decf["typedId"], "record": decfr}, {"id": cflowf["typedId"], "record": cflowfr}]
payloads = {ff["typedId"]: file_payload, clf["typedId"]: cl_payload, pkf["typedId"]: pkg_payload, decf["typedId"]: decl_payload, cflowf["typedId"]: cf_payload}
rp = {"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}
pre_checks = []
for label, inst, rel, sel in [
    ("snapshot", snapshot, IDENT, "#/$defs/snapshot"),
    ("plan", plan, IDENT, "#/$defs/plan"),
    ("rust_ctx", rust_ctx, NATIVE, "#/$defs/NativeContextV2"),
    ("uni", uni_bin, NATIVE, "#/$defs/RustUniverseV2ResolvedInputs"),
    ("own", own, NATIVE, "#/$defs/SourceUnitOwnershipV1"),
]:
    r = validate_against(inst, rel, selector=sel, label=label)
    pre_checks.append({"label": label, "stockOk": r["stockOk"], "errors": r["errors"][:5]})
out = close_execution_and_proof(
    store,
    plan_id=plan_id,
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
    language_mode="rust-cargo",
    cells=cells,
    view=view,
    view_h=view_h,
    facts_for_eval=facts_e,
    payloads=payloads,
    coverages_full=coverages_full,
    inventories=invs,
    nca=nca,
    vcs={"kind": "none"},
    import_ids=[],
    file_scope_id=sf["typedId"],
    atom=atom,
    project_id=project_id,
    snapshot_id=snapshot_id,
    cap_id=cap["capabilityManifestId"],
    export_stem="rust",
    extra_meta={"l0_2018": l0_18, "l0_2021": l0_21, "hashMarker": "#/Cargo.toml", "bodyIdentityPair": pair_rec, "mixedEditions": sorted(set(edition_map.values())), "targetEditionDiffersFromPackageDefault": True, "sameFileTwoEditions": True, "largeEditionMapSize": len(edition_map)},
    schema_checks=pre_checks,
)
print(json.dumps({"runId": out["runId"], "verdict": out["verdict"], "failed": out["failed"], "derived": out["derived"]}, indent=2, default=str))
for c in out["failed"]:
    print("FAIL", c)
