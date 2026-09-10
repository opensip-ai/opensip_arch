#!/usr/bin/env python3
"""Rust partial-enumeration empty clones Run.

Clones Coverage is unknown with input-closure-incomplete /
body-language-owner-unenumerated. No clone facts. Inventory remains complete.
Does not claim complete clones Coverage from partial ownership.
"""
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
from helper.graph_seal import ENUM, EMIS, IDENT, NATIVE, POL2, REL, make_closure, sort_set  # noqa: E402
from helper.identity import H  # noqa: E402
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
a_toml = b'[package]\nname="a"\nversion="0.1.0"\nedition="2018"\n'
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
vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_digest}
vcs_d = store.put_canonical(vcs, label="vcs")
scope_d = store.put_canonical({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}, label="scope")
sem_cfg = {"analysis": {"profileId": "core", "capabilities": ["clones-fact", "inventory"], "budget": {"unit": "work-units", "limit": 100000}}, "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
sem_cfg["analysis"]["capabilities"] = sorted(sem_cfg["analysis"]["capabilities"])
cfg_d = store.put_canonical(sem_cfg, label="cfg")
project_id = "prj1-" + hashlib.sha256(b"consumer-b.v12.rust-partial").hexdigest()
snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
snap_h = store.put_h("snapshot", snapshot, label="snapshot")
snapshot_id = snap_h["typedId"]

prov_c, _ = make_closure(store, "provider")
eval_c, _ = make_closure(store, "evaluator")
det_c, _ = make_closure(store, "detector")
rustc_bin = store.put_raw(b"rustc-bin", label="rustc-bin")
cargo_bin = store.put_raw(b"cargo-bin", label="cargo-bin")
pm_bin = store.put_raw(b"proc-macro-srv", label="pm-bin")
tool_c, tool_rec = make_closure(store, "toolchain", extra_files=[
    {"path": "bin/rustc", "sha256": rustc_bin, "bytes": 9},
    {"path": "bin/cargo", "sha256": cargo_bin, "bytes": 9},
    {"path": "bin/proc-macro-srv", "sha256": pm_bin, "bytes": len(b"proc-macro-srv")},
])
llvm_c, _ = make_closure(store, "rust-dev-llvm")
enum_schema_d = retain_schema(ENUM)
emis_schema_d = retain_schema(EMIS)
rel_schema_d = retain_schema(REL)
native_schema_d = retain_schema(NATIVE)

rf = {"honored": [], "stripped": [], "executableSelected": False}
cargo_proj = {
    "schemaVersion": 2, "honoredKeys": [], "strippedKeys": [], "replacedSnapshotConfigs": [],
    "rustflags": rf, "ancestorCarrierVerified": True, "cargoHome": "private-empty",
    "environmentProjection": "none", "claimsCargoSwitch": False,
    "projectionSha256": store.put_raw(b"empty-cargo-config", label="cargo-config.toml"),
}
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
own = {
    "schemaVersion": 1,
    "enumeration": "partial",
    "units": [{"unitId": u_lib, "markerPath": "#/a/Cargo.toml", "crateName": "a", "targetKind": "lib", "targetName": "a", "targetEdition": None}],
    "selectedUnitIds": [u_lib],
    "ownership": [{"path": "#/a/src/lib.rs", "unitId": u_lib}],
}
own_h = store.put_h("native.source-unit-ownership.v1", own, label="ownership-partial")
toolchain = {
    "rustCommitHash": "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef",
    "rustcVersion": tool_rec["semanticVersion"], "cargoVersion": "1.80.0",
    "sysrootDigest": store.put_raw(b"sysroot", label="sysroot"),
    "rustcDevLlvmDigest": llvm_c["digest"],
    "standardLibraryComponentDigests": [],
    "targetTriple": "aarch64-apple-darwin",
}
rust_ctx = {
    "schemaVersion": 2, "targetTriple": "aarch64-apple-darwin", "hostTriple": "aarch64-apple-darwin",
    "toolchain": toolchain,
    "toolClosure": {"closureId": tool_c["typedId"], "rustc": rustc_bin, "cargo": cargo_bin, "linker": None, "ar": None, "procMacroServer": pm_bin},
    "baseCfg": [], "resolverVersion": 2,
    "dependencySourceSetId": dep_h["sha256Text"], "unifiedFeaturesId": uf_h["sha256Text"],
    "preparedOutputSetId": None, "configProjection": cargo_proj,
}
ctx_h = store.put_h("native.context.rust.v2", rust_ctx, label="rust-ctx")
uni = {
    "schemaVersion": 2, "edition": {"a": 2018}, "lockfileIdentity": lock_id,
    "dependencySourceSetId": dep_h["sha256Text"], "unifiedFeaturesId": uf_h["sha256Text"],
    "nativeContextId": ctx_h["sha256Text"], "cfgSets": [{"cfgSetId": "default", "cfg": ["unix"]}],
    "rustflags": rf, "crateRootPaths": ["#/a/Cargo.toml"], "configProjectionSha256": cp_h["digest"],
    "executionCapableResolution": False, "preparedOutputSetId": None, "preparedResolution": "none",
    "sourceUnitOwnershipId": own_h["sha256Text"],
}
uni_h = store.put_h("native.semantic-universe.rust.v2", uni, label="uni-partial")
ctx_hex, uni_hex = ctx_h["digest"], uni_h["digest"]

cap_man = {
    "schemaVersion": 1, "profile": "core",
    "providers": [{"providerId": "rust-semantic", "language": "rust", "providerVersionSource": "release.rust-provider", "toolchainIdentitySource": "release.rustc",
        "relations": {"clones": "normalized-body-hash", "file": "enumerated", "package": "manifest-declared", "vcs-change": "vcs-reported"},
        "platformIds": ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"]}],
    "coverageForAbsent": [],
}
cap = capability_manifest_id(cap_man)
cap_bytes_d = store.put_raw(bytes.fromhex(cap["committedBytesHex"]), label="cap-bytes")
atom = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "#/a/src/lib.rs"}]}
det_prog = store.put_raw(b"det-rust-partial", label="det")
policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "error", "rules": [{"ruleId": "file-present", "ruleProgramRef": {"contributionId": "opensip.rules.rust-partial", "ruleStableId": "file-present", "semanticsMajor": 1, "programDigest": det_prog}, "enabled": True, "severity": "error", "gate": True, "subjectEnumeration": {"universe": "rust", "subjectKind": "file"}, "emitWhen": atom, "evidenceUse": []}]}
policy_d = store.put_canonical(policy, label="policy")
rp = {"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}
rp_d = store.put_canonical(rp, label="rp")
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
    return {"ordinal": 0, "provenance": "default-unit", "enumerator": {"status": "selected", "closureId": prov_c["typedId"]}, "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": None, "extents": sorted(extents, key=lambda x: x["kind"].encode())}

cells = [
    {"capabilityId": "clones-fact", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind(["file"])]},
    {"capabilityId": "inventory", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True, "kinds": sorted(["file", "package"]), "programBindings": [bind(["file", "package"])]},
]
enum_d = store.put_canonical({"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}, label="enum")
emis_d = store.put_canonical({"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": "opensip.rules.rust-partial", "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}, label="emis")
params = sort_set([{"schemaDigest": enum_schema_d, "payloadDigest": enum_d}, {"schemaDigest": emis_schema_d, "payloadDigest": emis_d}])
as_d = store.put_canonical({"schemaVersion": 2, "requestedCapabilities": sort_set([{"capabilityId": c["capabilityId"], "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True} for c in cells]), "policyPackIds": [], "parameters": params}, label="as")
plan = {"schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": cap["capabilityManifestId"], "semanticClosures": plan_semantic_closures(provider=prov_c["typedId"], evaluator=eval_c["typedId"], detector=det_c["typedId"], extras=[tool_c["typedId"], llvm_c["typedId"]]), "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex], "importIds": [], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d, "budget": {"unit": "work-units", "limit": 100000}, "semanticGrantDigest": grant_d, "capabilityManifestBytesDigest": cap_bytes_d}
plan_h = store.put_h("plan", plan, label="plan")
plan_id = plan_h["typedId"]
ss = {"schemaVersion": 2, "planId": plan_id, "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": ["view"], "outputSchemaDigest": native_schema_d}
ss_d = store.put_canonical(ss, label="ss")
ep_h = store.put_h("execution-plan", {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": ss["outputDomains"]}]}, label="ep")

libf = next(f for f in files if f["path"] == "#/a/src/lib.rs")
pkg_payload = {"manifestPath": "#/a/Cargo.toml", "packageName": "a", "packageVersion": "0.1.0"}
pkg_pd = store.put_canonical(pkg_payload, label="pkg")


def fact(rel, rung, pd, anchors, label=None):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "producerClosure": prov_c["typedId"], "payloadSchemaDigest": rel_schema_d, "payloadDigest": pd, "anchors": sort_set(anchors), "confidenceMillionths": 1000000}
    return store.put_h("fact", rec, label=label or f"f-{rel}"), rec

all_paths = sorted(f["path"] for f in files)
file_fact_ids = []
file_fact_recs = {}
file_payloads = {}
for frow in sorted(files, key=lambda r: r["path"].encode()):
    pl = {"path": frow["path"], "contentSha256": frow["sha256"], "byteLength": frow["bytes"]}
    pd = store.put_canonical(pl, label=f"fp-{frow['path']}")
    fh, fr = fact("file", "enumerated", pd, [], label=f"f-file-{frow['path']}")
    file_fact_ids.append(fh["typedId"])
    file_fact_recs[fh["typedId"]] = fr
    file_payloads[fh["typedId"]] = pl
pkf, pkfr = fact("package", "manifest-declared", pkg_pd, [])


def scope(rel, rung, subjects):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": rel, "resolution": rung, "enumeratorClosure": prov_c["typedId"], "subjects": sorted(subjects)}
    return store.put_h("subject-scope", rec, label=f"s-{rel}"), rec

sf, _ = scope("file", "enumerated", all_paths)
sc, _ = scope("clones", "normalized-body-hash", ["#/a/src/lib.rs"])
sp, _ = scope("package", "manifest-declared", ["a"])


def coverage(rel, rung, sh, n, cov="complete", defic=None, cause=None, exhaustive=None):
    if exhaustive is None:
        exhaustive = cov == "complete"
    commit = "sha256:" + sh["digest"]
    key = {"relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit}
    entry = {"relation": rel, "resolution": rung, "coverage": cov, "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": n}, "resolutionCompleteness": {"state": "not-applicable", "attempted": False, "examinedExhaustive": exhaustive, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}, "closedWorld": {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False}, "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": defic, "nativeCause": cause}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"cvp-{rel}")
    rec = {"schemaVersion": 2, "scopeId": sh["typedId"], "payloadSchemaDigest": native_schema_d, "payloadDigest": pd}
    return store.put_h("coverage", rec, label=f"cv-{rel}"), rec, payload

cf, _, cfp = coverage("file", "enumerated", sf, len(all_paths))
cc, _, ccp = coverage("clones", "normalized-body-hash", sc, 1, cov="unknown", defic="input-closure-incomplete", cause="body-language-owner-unenumerated", exhaustive=False)
cp, _, cpp = coverage("package", "manifest-declared", sp, 1)
view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": sort_set([sf["typedId"], sc["typedId"], sp["typedId"]]), "facts": sort_set(file_fact_ids + [pkf["typedId"]]), "coverageIds": sort_set([cf["typedId"], cc["typedId"], cp["typedId"]]), "producerClosure": prov_c["typedId"], "schemaDigests": sort_set([rel_schema_d, native_schema_d])}
view_h = store.put_h("view", view, label="view")
file_row = {"nativeSubjectId": "#/a/src/lib.rs", "kind": "file", "path": "#/a/src/lib.rs", "qualifiedName": "#/a/src/lib.rs", "subjectLanguage": "rust", "signatureTokens": [], "projections": []}
pkg_row = {"nativeSubjectId": "a", "kind": "package", "path": "#/a/Cargo.toml", "qualifiedName": "a", "subjectLanguage": "toml", "signatureTokens": [], "projections": []}
invs = [
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=0, kind="file", rows=[], examined=["#/a/src/lib.rs"], state="partial", deficiency="input-closure-incomplete", native_cause="body-language-owner-unenumerated"),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=1, kind="file", rows=[file_row], examined=["#/a/src/lib.rs"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=1, kind="package", rows=[pkg_row], examined=["#/a/Cargo.toml"]),
]
coverages_full = []
for hid, payload in [(cf, cfp), (cc, ccp), (cp, cpp)]:
    coverages_full.append({"id": hid["typedId"], "digest": hid["digest"], "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]}, "payload": payload, "entry": payload["entry"]})
nca = [
    {"cellOrdinal": 0, "programOrdinal": 0, "relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cc["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "package", "resolution": "manifest-declared", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cp["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "vcs-change", "resolution": "vcs-reported", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": vcs_applicability(vcs), "coverageIds": []},
]
pre_checks = []
for label, inst, rel, sel in [
    ("snapshot", snapshot, IDENT, "#/$defs/snapshot"),
    ("plan", plan, IDENT, "#/$defs/plan"),
    ("rust_ctx", rust_ctx, NATIVE, "#/$defs/NativeContextV2"),
    ("uni", uni, NATIVE, "#/$defs/RustUniverseV2ResolvedInputs"),
    ("own", own, NATIVE, "#/$defs/SourceUnitOwnershipV1"),
    ("clones-cov", ccp, NATIVE, "#/$defs/CoverageResultV3"),
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
    facts_for_eval=[{"id": fid, "record": file_fact_recs[fid]} for fid in file_fact_ids] + [{"id": pkf["typedId"], "record": pkfr}],
    payloads={**file_payloads, pkf["typedId"]: pkg_payload},
    coverages_full=coverages_full,
    inventories=invs,
    nca=nca,
    vcs=vcs,
    import_ids=[],
    file_scope_id=sf["typedId"],
    atom=atom,
    project_id=project_id,
    snapshot_id=snapshot_id,
    cap_id=cap["capabilityManifestId"],
    export_stem="rust-partial-clones",
    extra_meta={
        "emptyCloneFacts": True,
        "clonesCoverage": "unknown",
        "deficiency": "input-closure-incomplete",
        "nativeCause": "body-language-owner-unenumerated",
        "enumeration": "partial",
        "doesNotClaimCompleteCoverageFromPartialOwnership": True,
    },
    schema_checks=pre_checks,
)
print(json.dumps({"rust-partial": out["runId"], "verdict": out["verdict"], "failed": out["failed"], "derived": out["derived"]}, indent=2, default=str))
for c in out["failed"]:
    print("FAIL", c)
