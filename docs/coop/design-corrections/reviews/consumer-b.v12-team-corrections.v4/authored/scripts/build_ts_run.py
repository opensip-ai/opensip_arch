#!/usr/bin/env python3
"""Complete TypeScript Run: node_modules, bare specifiers, ScopeDocumentV1, import payload."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v4/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import body_identity, body_language_version, framed_token_stream, l0_payload, language_version_bytes  # noqa: E402
from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.body_identity import body_identity_frame  # noqa: E402
from helper.graph_seal import ENUM, EXEC, IDENT, NATIVE, POL1, POL2, REL, SINV, EMIS, make_closure, sort_set  # noqa: E402
from helper.identity import parse_h_frame, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.seal_run import close_execution_and_proof, mint_coverage, mint_inventory, mint_scope, plan_semantic_closures  # noqa: E402
from helper.store import Store  # noqa: E402
from helper.execution_inputs import vcs_applicability  # noqa: E402

store = Store()


def retain_schema(rel):
    return store.put_raw((KIT / rel).read_bytes(), label=rel)


def add_file(path, data: bytes):
    d = store.put_raw(data, label=path)
    return {"path": path, "sha256": d, "bytes": len(data)}


index_ts = b'import pad from "left-pad";\nexport const n = pad("1", 2, "0");\n'
left_js = b"module.exports = function pad(s,n,c){return String(s);};\n"
left_pkg = b'{"name":"left-pad","version":"1.3.0","main":"index.js"}\n'
pkg = b'{"name":"app","version":"1.0.0","type":"commonjs","dependencies":{"left-pad":"1.3.0"}}\n'
tsconfig = b'{"compilerOptions":{"module":"commonjs","moduleResolution":"node10","target":"ES2022","lib":["ES2022"],"strict":true,"noEmit":true},"include":["src/**/*"]}\n'
plock = b'{"name":"app","lockfileVersion":3,"packages":{}}\n'
lib_dts = b"interface Array<T> { length: number }\n"

files = [
    add_file("src/index.ts", index_ts),
    add_file("package.json", pkg),
    add_file("tsconfig.json", tsconfig),
    add_file("package-lock.json", plock),
    add_file("node_modules/left-pad/index.js", left_js),
    add_file("node_modules/left-pad/package.json", left_pkg),
]
src_inv = sorted(files, key=lambda r: r["path"].encode())
inv_digest = store.put_canonical(src_inv, label="source-inventory")
vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_digest}
vcs_d = store.put_canonical(vcs, label="vcs")
scope_desc = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []}
scope_d = store.put_canonical(scope_desc, label="scope-descriptor")
sem_cfg = {
    "analysis": {"profileId": "core", "capabilities": ["clones-fact", "imports", "inventory", "syntax"], "budget": {"unit": "work-units", "limit": 100000}},
    "components": {},
    "discovery": {},
    "policy": {},
    "evidence": {},
}
sem_cfg["analysis"]["capabilities"] = sorted(sem_cfg["analysis"]["capabilities"])
cfg_d = store.put_canonical(sem_cfg, label="semantic-configuration")
project_id = "prj1-" + hashlib.sha256(b"consumer-b.v12.ts-run").hexdigest()
snapshot = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": src_inv, "resolvedConfigDigest": cfg_d, "scopeDigest": scope_d, "vcsDigest": vcs_d}
snap_h = store.put_h("snapshot", snapshot, label="snapshot")
snapshot_id = snap_h["typedId"]

prov_c, _ = make_closure(store, "provider")
eval_c, _ = make_closure(store, "evaluator")
det_c, _ = make_closure(store, "detector")
tsc_bin = store.put_raw(b"tsc-bin", label="tsc-bin")
node_bin = store.put_raw(b"node-bin", label="node-bin")
tool_c, _ = make_closure(
    store,
    "toolchain",
    extra_files=[
        {"path": "bin/tsc", "sha256": tsc_bin, "bytes": 7},
        {"path": "bin/node", "sha256": node_bin, "bytes": 8},
    ],
)
stdlib_file = add_file("lib.es2022.d.ts", lib_dts)  # not in snapshot; closure tree
# put stdlib in closure tree not snapshot
stdlib_blob = store.put_raw(lib_dts, label="lib.es2022.d.ts")
stdlib_c, _ = make_closure(store, "stdlib", extra_files=[{"path": "lib.es2022.d.ts", "sha256": stdlib_blob, "bytes": len(lib_dts)}])
adapter_c, _ = make_closure(store, "adapter")

enum_schema_d = retain_schema(ENUM)
emis_schema_d = retain_schema(EMIS)
rel_schema_d = retain_schema(REL)
native_schema_d = retain_schema(NATIVE)
pol1_schema_d = retain_schema(POL1)
pol2_schema_d = retain_schema(POL2)

# node_modules layout
nm_layout = {
    "schemaVersion": 1,
    "entries": [
        {
            "packageName": "left-pad",
            "packageVersion": "1.3.0",
            "installPath": "node_modules/left-pad",
            "realPath": "node_modules/left-pad",
            "contentSha256": next(f["sha256"] for f in files if f["path"] == "node_modules/left-pad/package.json"),
        }
    ],
}
nm_d = store.put_canonical(nm_layout, label="ResolvedNodeModulesLayoutV1")

cfg_graph = {
    "schemaVersion": 1,
    "entryConfigPath": "tsconfig.json",
    "nodes": [
        {
            "path": "tsconfig.json",
            "contentSha256": next(f["sha256"] for f in files if f["path"] == "tsconfig.json"),
            "kind": "tsconfig",
            "extendsResolved": [],
        }
    ],
}
cg_d = store.put_canonical(cfg_graph, label="TypeScriptConfigGraphV1")

honored = {
    "allowJs": False,
    "allowSyntheticDefaultImports": False,
    "baseUrl": None,
    "checkJs": False,
    "customConditions": [],
    "esModuleInterop": False,
    "jsx": None,
    "lib": ["ES2022"],
    "module": "commonjs",
    "moduleResolution": "node10",
    "noEmit": True,
    "paths": [],
    "resolveJsonModule": False,
    "rootDirs": [],
    "skipLibCheck": True,
    "strict": True,
    "target": "ES2022",
    "types": None,
}
# libSelection utf8 of unfolded names - "ES2022" vs es2022. Description says fold to lowercase for component join.
# libSelection sorted by raw UTF-8 of retained unfolded names. Use "ES2022" matching honoredOptions.lib
proj = {
    "schemaVersion": 2,
    "ancestorCarrierVerified": True,
    "configGraphPaths": ["tsconfig.json"],
    "environmentSanitized": True,
    "executableSelected": False,
    "honoredOptions": honored,
    "strippedOptions": [],
    "typeAcquisitionEnabled": False,
}
lock = {
    "kind": "package-lock",
    "path": "package-lock.json",
    "contentSha256": next(f["sha256"] for f in files if f["path"] == "package-lock.json"),
}
toolchain = {
    "compilerName": "typescript",
    "compilerVersion": "1.0.0",
    "compilerPackageDigest": store.put_raw(b"tsc-pkg", label="tsc-pkg"),
    "typescriptStdlibMerkleRoot": stdlib_c["digest"],
    "standardLibraryComponentDigests": [{"component": "lib.es2022.d.ts", "sha256": stdlib_blob}],
    "libSelection": ["ES2022"],
}
tool_closure = {
    "compiler": tsc_bin,
    "runtime": node_bin,
    "closureId": tool_c["typedId"],
}
ts_ctx = {
    "schemaVersion": 2,
    "languageMode": "ts-tsconfig",
    "toolchain": toolchain,
    "toolClosure": tool_closure,
    "configProjection": proj,
    "moduleResolutionMode": "node10",
    "packageModuleType": "commonjs",
    "nodeModulesLayoutDigest": nm_d,
    "lockfileIdentity": lock,
}
ctx_h = store.put_h("native.context.typescript.v2", ts_ctx, label="ts-context")
uni = {
    "schemaVersion": 2,
    "languageMode": "ts-tsconfig",
    "configOrigin": "tsconfig",
    "synthesizerVersion": None,
    "synthesizedOptions": None,
    "packageModuleType": "commonjs",
    "allowJs": False,
    "checkJs": False,
    "jsAdmittedToProgram": False,
    "jsDiagnosticsEnabled": False,
    "resolutionCompletenessImplied": False,
    "jsRootFiles": [],
    "programRootFiles": ["src/index.ts"],
    "lockfileKind": "package-lock",
    "nodeModulesInReadSet": True,
    "executionCapableResolution": False,
    "tsconfigGraphHash": cg_d,
    "nativeContextId": ctx_h["sha256Text"],
}
# programRootFiles utf8?
uni_h = store.put_h("native.semantic-universe.typescript.v2", uni, label="ts-universe")
ctx_hex, uni_hex = ctx_h["digest"], uni_h["digest"]

# import2 runtime payload
rt_payload = {
    "payloadDomain": "workflow.import-payload.runtime.v1",
    "format": "json",
    "observationWindow": None,
    "observedPopulation": None,
    "subjects": [],
    "mappingGaps": [],
}
# dump format enum if fail
imp_schema = "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
imp_schema_d = retain_schema(imp_schema)
sc = {"kind": "exact-snapshot", "snapshotId": snapshot_id}
sc_d = store.put_canonical(sc, label="SourceCorrespondence")
build = {"schemaVersion": 1, "buildIdentity": "synthetic-build"}
build_d = store.put_canonical(build, label="BuildIdentityV1")
obs = {"schemaVersion": 1, "kind": "runtime", "window": None, "population": None, "selection": None, "revisionRange": None}
obs_d = store.put_canonical(obs, label="ImportObservationV1")
rt_pd = store.put_canonical(rt_payload, label="RuntimePayloadV1")
imp_rec = {
    "schemaVersion": 2,
    "kind": "runtime",
    "payloadSchemaDigest": imp_schema_d,
    "payloadDigest": rt_pd,
    "sourceCorrespondenceDigest": sc_d,
    "buildDigest": build_d,
    "producerClosure": adapter_c["typedId"],
    "adapterClosure": adapter_c["typedId"],
    "blobs": [],
    "scopeDigest": scope_d,
    "observationDigest": obs_d,
    "completeness": "complete",
    "omissions": [],
}
imp_h = store.put_h("import", imp_rec, label="import-runtime")

scope_doc = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1, "include": ["src/**/*.ts"], "exclude": ["node_modules/**"]}
sd_d = store.put_canonical(scope_doc, label="ScopeDocumentV1")

cap_man = {
    "schemaVersion": 1,
    "profile": "core",
    "providers": [
        {
            "providerId": "typescript-semantic",
            "language": "typescript",
            "providerVersionSource": "release.typescript-provider",
            "toolchainIdentitySource": "release.typescript-runtime",
            "relations": {
                "calls": "resolved-callee",
                "clones": "normalized-body-hash",
                "control-flow": "syntactic",
                "declares": "syntactic",
                "file": "enumerated",
                "imports": "resolved-target",
                "literal": "syntactic",
                "package": "manifest-declared",
                "reachability": "from-resolved-calls",
                "references": "resolved-binding",
                "types": "checked",
                "unresolved-edge": "observed",
                "vcs-change": "vcs-reported",
            },
            "platformIds": ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"],
        }
    ],
    "coverageForAbsent": [],
}
cap = capability_manifest_id(cap_man)
cap_bytes = bytes.fromhex(cap["committedBytesHex"])
cap_bytes_d = store.put_raw(cap_bytes, label="cve1-cap")

atom = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "src/index.ts"}]}
det_prog = store.put_raw(b"det-ts", label="det-prog")
contrib = "opensip.rules.ts-pilot"
policy = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [
        {
            "ruleId": "file-present",
            "ruleProgramRef": {"contributionId": contrib, "ruleStableId": "file-present", "semanticsMajor": 1, "programDigest": det_prog},
            "enabled": True,
            "severity": "error",
            "gate": True,
            "subjectEnumeration": {"universe": "typescript", "subjectKind": "file"},
            "emitWhen": atom,
            "evidenceUse": [],
        }
    ],
}
policy_d = store.put_canonical(policy, label="policy")
rp = {"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}
rp_d = store.put_canonical(rp, label="rule-program")
waiver_d = store.put_canonical({"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}, label="waivers")
grant = {
    "schemaVersion": 2,
    "projectId": project_id,
    "principals": [{"kind": "first-party", "closureId": prov_c["typedId"], "ownerSourceDigest": None}],
    "analysisOperations": sorted(["native-analysis", "read-source", "read-import"]),
    "scopeDigest": scope_d,
}
grant_d = store.put_canonical(grant, label="grant")

memb = {
    "schemaVersion": 1,
    "units": [{
        "unitOrdinal": 0, "rootPath": ".", "languageFamily": "tsjs", "languageMode": "ts-tsconfig",
        "unitKind": "ts-program", "markerPath": "tsconfig.json",
        "markerSha256": next(f["sha256"] for f in files if f["path"] == "tsconfig.json"),
        "recognizerId": "opensip.ts-recognizer", "recognizerVersion": 1, "provenance": "DISCOVERED", "memberPackageRoots": [],
    }],
    "rows": [{"path": "src/index.ts", "languageFamily": "tsjs", "unitOrdinal": 0, "membership": "program-member", "reason": "deepest-unit-in-language"}],
    "unsupportedFiles": [], "outsideBoundaryFiles": [], "erasedFiles": [],
}
memb_d = store.put_canonical(memb, label="membership")

def bind(kinds):
    return {
        "ordinal": 0, "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": prov_c["typedId"]},
        "nativeContextDigest": ctx_hex, "universe": uni_hex, "programEntry": "tsconfig.json",
        "extents": sorted([{"kind": k, "paths": ["src/index.ts"] if k != "package" else ["package.json"]} for k in kinds], key=lambda x: x["kind"].encode()),
    }

cells = [
    {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True, "kinds": ["file"], "programBindings": [bind(["file"])]},
    {"capabilityId": "imports", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True, "kinds": ["symbol"], "programBindings": [bind(["symbol"])]},
    {"capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True, "kinds": sorted(["file", "package"]), "programBindings": [bind(["file", "package"])]},
    {"capabilityId": "syntax", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True, "kinds": ["symbol"], "programBindings": [bind(["symbol"])]},
]
enum_plan = {"schemaVersion": 1, "snapshotId": snapshot_id, "scopeDigest": scope_d, "membershipDigest": memb_d, "cells": cells}
enum_d = store.put_canonical(enum_plan, label="enum")
emis = {"schemaVersion": 1, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "contributionId": contrib, "ruleStableId": "file-present", "semanticsMajor": 1, "detectorClosure": det_c["typedId"], "stabilityClass": "path-stable", "emissionProfile": "declarative-subject-v1"}]}
emis_d = store.put_canonical(emis, label="emis")
params = sort_set([
    {"schemaDigest": enum_schema_d, "payloadDigest": enum_d},
    {"schemaDigest": emis_schema_d, "payloadDigest": emis_d},
    {"schemaDigest": pol1_schema_d, "payloadDigest": sd_d},
])
req_caps = sort_set([{"capabilityId": c["capabilityId"], "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": True} for c in cells])
analysis_spec = {"schemaVersion": 2, "requestedCapabilities": req_caps, "policyPackIds": [], "parameters": params}
as_d = store.put_canonical(analysis_spec, label="analysis-spec")

plan = {
    "schemaVersion": 2, "snapshotId": snapshot_id, "capabilityManifestId": cap["capabilityManifestId"],
    "semanticClosures": plan_semantic_closures(
        provider=prov_c["typedId"],
        evaluator=eval_c["typedId"],
        detector=det_c["typedId"],
        extras=[tool_c["typedId"], stdlib_c["typedId"], adapter_c["typedId"]],
    ),
    "analysisSpecDigest": as_d, "resolvedConfigDigest": cfg_d, "nativeContextDigests": [ctx_hex],
    "importIds": [imp_h["typedId"]], "policyDigest": policy_d, "waiverDigest": waiver_d, "scopeDigest": scope_d,
    "budget": {"unit": "work-units", "limit": 100000}, "semanticGrantDigest": grant_d,
    "capabilityManifestBytesDigest": cap_bytes_d,
}
plan_h = store.put_h("plan", plan, label="plan")
plan_id = plan_h["typedId"]
ss = {"schemaVersion": 2, "planId": plan_id, "producerClosure": prov_c["typedId"], "operation": "analyze", "parameters": params, "outputDomains": ["view"], "outputSchemaDigest": native_schema_d}
ss_d = store.put_canonical(ss, label="stage-spec")
ep = {"schemaVersion": 2, "planId": plan_id, "stages": [{"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": ss["outputDomains"]}]}
ep_h = store.put_h("execution-plan", ep, label="exec-plan")

idx = next(f for f in files if f["path"] == "src/index.ts")
blv = body_language_version(language_id="typescript", compiler_name="typescript", compiler_version="1.0.0", compiler_build=toolchain["compilerPackageDigest"], dialect={"sourceVariant": "ts"})
lv = language_version_bytes(blv)
grammar_spec = b"L0-verbatim ts"
store.put_raw(grammar_spec, label="level-spec")
store.put_canonical(blv, label="body-language-version")
l0_frame = body_identity_frame(level_id="L0-verbatim", level_spec_bytes=grammar_spec, language_id="typescript", language_version=lv, payload=l0_payload(index_ts))
l0 = "sha256:" + store.put_raw(l0_frame, label="fact-identity-L0-verbatim")

file_payload = {"path": "src/index.ts", "contentSha256": idx["sha256"], "byteLength": idx["bytes"]}
file_pd = store.put_canonical(file_payload, label="file-payload")
imp_payload = {"importer": "file:src/index.ts", "specifier": "left-pad", "resolvedTarget": "file:node_modules/left-pad/index.js"}
imp_pd = store.put_canonical(imp_payload, label="imports-payload")
cl_payload = {"bodyIdentity": l0, "normalisationLevel": "L0-verbatim", "normalisationVersion": hashlib.sha256(grammar_spec).hexdigest()}
cl_pd = store.put_canonical(cl_payload, label="clones-payload")
pkg_payload = {"manifestPath": "package.json", "packageName": "app", "packageVersion": "1.0.0"}
pkg_pd = store.put_canonical(pkg_payload, label="package-payload")


def fact(rel, rung, pd, anchors):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "producerClosure": prov_c["typedId"], "payloadSchemaDigest": rel_schema_d, "payloadDigest": pd, "anchors": sort_set(anchors), "confidenceMillionths": 1000000}
    return store.put_h("fact", rec, label=f"fact-{rel}"), rec

anchor = [{"path": "src/index.ts", "blobDigest": idx["sha256"], "startByte": 0, "endByte": idx["bytes"]}]
ff, ffr = fact("file", "enumerated", file_pd, [])
imf, imfr = fact("imports", "resolved-target", imp_pd, anchor)
clf, clfr = fact("clones", "normalized-body-hash", cl_pd, anchor)
pkf, pkfr = fact("package", "manifest-declared", pkg_pd, [])


def scope(rel, rung, subjects):
    rec = {"schemaVersion": 2, "snapshotId": snapshot_id, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "relation": rel, "resolution": rung, "enumeratorClosure": prov_c["typedId"], "subjects": sorted(subjects)}
    return store.put_h("subject-scope", rec, label=f"scope-{rel}"), rec

sf, _ = scope("file", "enumerated", ["src/index.ts"])
si, _ = scope("imports", "resolved-target", ["src/index.ts"])
sc_, _ = scope("clones", "normalized-body-hash", ["src/index.ts"])
sp, _ = scope("package", "manifest-declared", ["app"])


def rc_na():
    return {"state": "not-applicable", "attempted": False, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def rc_complete():
    return {"state": "complete", "attempted": True, "examinedExhaustive": True, "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def cw():
    return {"exportsClosed": "unknown", "entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False}


def coverage(rel, rung, sh, nsubj, resolved=False):
    commit = "sha256:" + sh["digest"]
    key = {"relation": rel, "resolution": rung, "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "subjectScopeCommitment": commit}
    entry = {"relation": rel, "resolution": rung, "coverage": "complete", "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": nsubj}, "resolutionCompleteness": rc_complete() if resolved else rc_na(), "closedWorld": cw(), "derivationKinds": [], "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"covp-{rel}")
    rec = {"schemaVersion": 2, "scopeId": sh["typedId"], "payloadSchemaDigest": native_schema_d, "payloadDigest": pd}
    return store.put_h("coverage", rec, label=f"cov-{rel}"), rec, payload

cf, _, cfp = coverage("file", "enumerated", sf, 1)
ci, _, cip = coverage("imports", "resolved-target", si, 1, resolved=True)
cc, _, ccp = coverage("clones", "normalized-body-hash", sc_, 1)
cp, _, cpp = coverage("package", "manifest-declared", sp, 1)

decl_payload = {"container": "file:src/index.ts", "declarationKind": "variable", "declared": "variable:n"}
decl_pd = store.put_canonical(decl_payload, label="decl-payload")
decf, decfr = fact("declares", "syntactic", decl_pd, anchor)
lit_payload = {"literalKind": "string", "owner": "variable:n", "valueText": "1"}
lit_pd = store.put_canonical(lit_payload, label="lit-payload")
litf, litfr = fact("literal", "syntactic", lit_pd, anchor)
cf_payload = {"edgeKind": "fallthrough", "from": "variable:n", "to": "variable:n"}
cflow_pd = store.put_canonical(cf_payload, label="cf-payload")
cflowf, cflowfr = fact("control-flow", "syntactic", cflow_pd, anchor)
sdec, _ = scope("declares", "syntactic", ["variable:n"])
slit, _ = scope("literal", "syntactic", ["variable:n"])
scf, _ = scope("control-flow", "syntactic", ["variable:n"])
cdec, _, cdecp = coverage("declares", "syntactic", sdec, 1)
clit, _, clitp = coverage("literal", "syntactic", slit, 1)
ccf, _, ccfp = coverage("control-flow", "syntactic", scf, 1)

view = {
    "schemaVersion": 2,
    "planId": plan_id,
    "scopeIds": sort_set([sf["typedId"], si["typedId"], sc_["typedId"], sp["typedId"], sdec["typedId"], slit["typedId"], scf["typedId"]]),
    "facts": sort_set([ff["typedId"], imf["typedId"], clf["typedId"], pkf["typedId"], decf["typedId"], litf["typedId"], cflowf["typedId"]]),
    "coverageIds": sort_set([cf["typedId"], ci["typedId"], cc["typedId"], cp["typedId"], cdec["typedId"], clit["typedId"], ccf["typedId"]]),
    "producerClosure": prov_c["typedId"],
    "schemaDigests": sort_set([rel_schema_d, native_schema_d]),
}
view_h = store.put_h("view", view, label="view")

file_row = {"nativeSubjectId": "src/index.ts", "kind": "file", "path": "src/index.ts", "qualifiedName": "src/index.ts", "subjectLanguage": "typescript", "signatureTokens": [], "projections": []}
pkg_row = {"nativeSubjectId": "app", "kind": "package", "path": "package.json", "qualifiedName": "app", "subjectLanguage": "json", "signatureTokens": [], "projections": []}
sym_row = {"nativeSubjectId": "variable:n", "kind": "symbol", "path": "src/index.ts", "qualifiedName": "n", "subjectLanguage": "typescript", "exported": "exported", "signatureTokens": ["n"], "projections": []}
invs = [
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=0, kind="file", rows=[file_row], examined=["src/index.ts"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=1, kind="symbol", rows=[sym_row], examined=["src/index.ts"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=2, kind="file", rows=[file_row], examined=["src/index.ts"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=2, kind="package", rows=[pkg_row], examined=["package.json"]),
    mint_inventory(store, plan_id=plan_id, enum_d=enum_d, cell_ordinal=3, kind="symbol", rows=[sym_row], examined=["src/index.ts"]),
]
coverages_full = []
for hid, payload in [(cf, cfp), (ci, cip), (cc, ccp), (cp, cpp), (cdec, cdecp), (clit, clitp), (ccf, ccfp)]:
    coverages_full.append({"id": hid["typedId"], "digest": hid["digest"], "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]}, "payload": payload, "entry": payload["entry"]})
nca = [
    {"cellOrdinal": 0, "programOrdinal": 0, "relation": "clones", "resolution": "normalized-body-hash", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cc["digest"]]},
    {"cellOrdinal": 1, "programOrdinal": 0, "relation": "imports", "resolution": "resolved-target", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [ci["digest"]]},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "file", "resolution": "enumerated", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cf["digest"]]},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "package", "resolution": "manifest-declared", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cp["digest"]]},
    {"cellOrdinal": 2, "programOrdinal": 0, "relation": "vcs-change", "resolution": "vcs-reported", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": vcs_applicability(vcs), "coverageIds": []},
    {"cellOrdinal": 3, "programOrdinal": 0, "relation": "declares", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [cdec["digest"]]},
    {"cellOrdinal": 3, "programOrdinal": 0, "relation": "literal", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [clit["digest"]]},
    {"cellOrdinal": 3, "programOrdinal": 0, "relation": "control-flow", "resolution": "syntactic", "sourceUniverse": uni_hex, "targetUniverse": uni_hex, "applicability": "supported-available", "coverageIds": [ccf["digest"]]},
]
facts_e = [
    {"id": ff["typedId"], "record": ffr},
    {"id": imf["typedId"], "record": imfr},
    {"id": clf["typedId"], "record": clfr},
    {"id": pkf["typedId"], "record": pkfr},
    {"id": decf["typedId"], "record": decfr},
    {"id": litf["typedId"], "record": litfr},
    {"id": cflowf["typedId"], "record": cflowfr},
]
payloads = {
    ff["typedId"]: file_payload,
    imf["typedId"]: imp_payload,
    clf["typedId"]: cl_payload,
    pkf["typedId"]: pkg_payload,
    decf["typedId"]: decl_payload,
    litf["typedId"]: lit_payload,
    cflowf["typedId"]: cf_payload,
}
rp = {"schemaVersion": 2, "policyDigest": policy_d, "rules": [{"ruleId": "file-present", "ruleProgramRef": policy["rules"][0]["ruleProgramRef"], "emitWhen": atom}]}
pre_checks = []
for label, inst, rel, sel in [
    ("snapshot", snapshot, IDENT, "#/$defs/snapshot"),
    ("plan", plan, IDENT, "#/$defs/plan"),
    ("ts_ctx", ts_ctx, NATIVE, "#/$defs/TypeScriptNativeContextV2"),
    ("ts_uni", uni, NATIVE, "#/$defs/TypeScriptUniverseV2ResolvedInputs"),
    ("import", imp_rec, IDENT, "#/$defs/import"),
    ("scope_doc", scope_doc, POL1, "#/$defs/ScopeDocumentV1"),
    ("analysis_spec", analysis_spec, IDENT, "#/$defs/analysis-spec"),
    ("nm", nm_layout, NATIVE, "#/$defs/ResolvedNodeModulesLayoutV1"),
    ("cfg_graph", cfg_graph, NATIVE, "#/$defs/TypeScriptConfigGraphV1"),
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
    language_mode="ts-tsconfig",
    cells=cells,
    view=view,
    view_h=view_h,
    facts_for_eval=facts_e,
    payloads=payloads,
    coverages_full=coverages_full,
    inventories=invs,
    nca=nca,
    vcs=vcs,
    import_ids=[imp_h["typedId"]],
    file_scope_id=sf["typedId"],
    atom=atom,
    project_id=project_id,
    snapshot_id=snapshot_id,
    cap_id=cap["capabilityManifestId"],
    export_stem="ts",
    extra_meta={"importId": imp_h["typedId"], "scopeDocDigest": sd_d, "nodeModules": True, "bareSpecifier": "left-pad", "l0Identity": l0},
    schema_checks=pre_checks,
)
print(json.dumps({"runId": out["runId"], "verdict": out["verdict"], "failed": out["failed"], "derived": out["derived"]}, indent=2, default=str))
for c in out["failed"]:
    print("FAIL", c)
