"""CB-CFG: TypeScript configuration-graph variants.

  synthesized      - no tsconfig/jsconfig at all; host-synthesized options
  custom-multibase - an explicitly selected CUSTOM-NAMED project config
                     inheriting from multiple ORDERED bases, including a
                     REPEATED base whose precedence must be retained
  jsconfig-shared  - a JavaScript config inheriting a shared base with
                     another filename
"""
from __future__ import annotations

import assemble
import build
import closure as CL
import osip
from build import Fixture, coverage_entry
from osip import raw_sha256

PLATFORM = "macos-aarch64"
TS_VERSION = "5.6.3"

CAP_MANIFEST = {
    "schemaVersion": 1, "profile": "default",
    "providers": [{"providerId": "opensip.provider.typescript",
                   "language": "typescript",
                   "providerVersionSource": "closure-manifest",
                   "toolchainIdentitySource": "native-context",
                   "relations": {"file": "enumerated"},
                   "platformIds": [PLATFORM]}],
    "coverageForAbsent": [],
}


def build_run(shape, mutate=None, spec_parameters=None, seed=None):
    fx = Fixture("cb-cfg-" + (seed or shape))
    m = mutate or {}
    fx.add_file("package.json", b'{"name":"cb","version":"1.0.0","private":true}\n')
    fx.add_file("src/a.ts", b"export const a = 1;\n")

    if shape == "synthesized":
        entry, nodes = None, []
        language_mode, config_origin = "js-synthesized", "synthesized"
        fx.add_file("src/b.js", b"module.exports = 1;\n")
    elif shape == "custom-multibase":
        fx.add_file("configs/app.build.json",
                    b'{"extends":["./tsconfig.base.json","./shared.json",'
                    b'"./tsconfig.base.json"],"compilerOptions":{}}\n')
        fx.add_file("tsconfig.base.json", b'{"compilerOptions":{"strict":true}}\n')
        fx.add_file("configs/shared.json", b'{"compilerOptions":{"noEmit":true}}\n')
        entry = "configs/app.build.json"
        language_mode, config_origin = "ts-tsconfig", "tsconfig"
    elif shape == "jsconfig-shared":
        fx.add_file("jsconfig.json", b'{"extends":"./base.settings.json"}\n')
        fx.add_file("base.settings.json", b'{"compilerOptions":{"allowJs":true}}\n')
        entry = "jsconfig.json"
        language_mode, config_origin = "js-allowjs", "jsconfig"
    else:
        raise ValueError(shape)

    inv = {r["path"]: r for r in fx.inventory()}

    def node(path, extends):
        base = path.rsplit("/", 1)[-1]
        kind = CL.CONFIG_KIND_LAW["basenames"].get(
            base, CL.CONFIG_KIND_LAW["otherwise"])
        return {"path": path, "contentSha256": inv[path]["sha256"], "kind": kind,
                "extendsResolved": extends}

    if shape == "custom-multibase":
        # REPETITIONS ARE RETAINED, later entries take precedence
        nodes = [node("configs/app.build.json",
                      ["tsconfig.base.json", "configs/shared.json",
                       "tsconfig.base.json"]),
                 node("configs/shared.json", []),
                 node("tsconfig.base.json", [])]
    elif shape == "jsconfig-shared":
        nodes = [node("base.settings.json", []),
                 node("jsconfig.json", ["base.settings.json"])]
    nodes = sorted(nodes, key=lambda n: n["path"].encode())
    if m.get("drop_repeated_base"):
        for n in nodes:
            if n["path"] == "configs/app.build.json":
                n["extendsResolved"] = ["tsconfig.base.json", "configs/shared.json"]
    if m.get("claim_tsconfig_kind"):
        for n in nodes:
            if n["path"] == "configs/app.build.json":
                n["kind"] = "tsconfig"

    graph = {"schemaVersion": 1, "entryConfigPath": entry, "nodes": nodes}
    graph_digest = fx.rec(graph, "native", "#/$defs/TypeScriptConfigGraphV1", "graph")

    tool_cid, _, tool_members = fx.closure(
        "typescript-toolchain", "toolchain",
        {"bin/tsc.js": b"#tsc\n", "bin/node": b"#node\n"},
        TS_VERSION, PLATFORM, protocol_major=2)
    stdlib_cid, _, std_members = fx.closure(
        "typescript-stdlib", "stdlib", {"lib/lib.es2022.d.ts": b"declare var y: any;\n"},
        TS_VERSION, PLATFORM, protocol_major=2)
    prov_cid, _, _ = fx.closure("typescript-provider", "provider",
                                {"bin/p": b"#p\n"}, "1.0.0", PLATFORM, protocol_major=2)
    eval_cid, _, _ = fx.closure("evaluator", "evaluator", {"bin/e": b"#e\n"},
                                "1.0.0", PLATFORM, protocol_major=2)

    allow_js = shape in ("synthesized", "jsconfig-shared")
    honored = {"allowJs": allow_js, "checkJs": False, "module": "node16",
               "moduleResolution": "node16", "target": "es2022",
               "strict": shape == "custom-multibase", "skipLibCheck": True,
               "noEmit": True, "types": [] if shape == "synthesized" else None,
               "lib": ["es2022"], "baseUrl": None, "paths": [], "rootDirs": [],
               "resolveJsonModule": False, "allowSyntheticDefaultImports": False,
               "esModuleInterop": False, "customConditions": [], "jsx": None}
    ctx = {"schemaVersion": 2, "languageMode": language_mode,
           "toolchain": {"compilerName": "typescript", "compilerVersion": TS_VERSION,
                         "compilerPackageDigest": tool_members["bin/tsc.js"],
                         "typescriptStdlibMerkleRoot": stdlib_cid.split(":")[1],
                         "standardLibraryComponentDigests": [
                             {"component": "lib.es2022.d.ts",
                              "sha256": std_members["lib/lib.es2022.d.ts"]}],
                         "libSelection": ["es2022"]},
           "toolClosure": {"compiler": tool_members["bin/tsc.js"],
                           "runtime": tool_members["bin/node"],
                           "closureId": tool_cid},
           "configProjection": {"schemaVersion": 2, "ancestorCarrierVerified": True,
                                "environmentSanitized": True,
                                "typeAcquisitionEnabled": False,
                                "executableSelected": False,
                                "honoredOptions": honored, "strippedOptions": [],
                                "configGraphPaths": sorted(
                                    [n["path"] for n in nodes],
                                    key=lambda x: x.encode())},
           "moduleResolutionMode": "node16", "packageModuleType": "absent",
           "nodeModulesLayoutDigest": None, "lockfileIdentity": None}

    synth = None
    if shape == "synthesized":
        synth = {"allowJs": True, "checkJs": False, "module": "node16",
                 "moduleResolution": "node16", "target": "es2022", "strict": False,
                 "skipLibCheck": True, "types": [], "noEmit": True}
    uni = {"schemaVersion": 2, "languageMode": language_mode,
           "configOrigin": config_origin,
           "synthesizerVersion": 1 if shape == "synthesized" else None,
           "synthesizedOptions": synth, "packageModuleType": "absent",
           "allowJs": allow_js, "checkJs": False,
           "jsAdmittedToProgram": allow_js, "jsDiagnosticsEnabled": False,
           "resolutionCompletenessImplied": False,
           "jsRootFiles": ["src/b.js"] if shape == "synthesized" else [],
           "programRootFiles": sorted([p for p in inv if p.endswith((".ts", ".js"))],
                                      key=lambda x: x.encode()),
           "lockfileKind": "none", "nodeModulesInReadSet": False,
           "executionCapableResolution": False,
           "tsconfigGraphHash": graph_digest, "nativeContextId": None}
    if m.get("assert_configorigin_tsconfig_on_jsconfig"):
        uni["configOrigin"] = "tsconfig"

    A = assemble.Assembly(
        fx, capabilities=["inventory"],
        spec_rows=[{"capabilityId": "inventory", "languageMode": language_mode,
                    "workspaceRoot": ".", "required": True}],
        spec_parameters=spec_parameters,
        capability_manifest=CAP_MANIFEST)
    ctx_hex = A.add_context("native.context.typescript.v2", ctx,
                            "#/$defs/TypeScriptNativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.typescript.v2", uni,
                             "#/$defs/TypeScriptUniverseV2ResolvedInputs", "universe")
    A.seal_snapshot()
    A.seal_plan([prov_cid, eval_cid, tool_cid, stdlib_cid])

    facts = [A.add_fact("file", "enumerated", uni_hex, uni_hex, prov_cid,
                        {"path": p, "contentSha256": r["sha256"],
                         "byteLength": r["bytes"]}, [])
             for p, r in sorted(inv.items())]
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 sorted(inv))
    c_file = A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(inv), "complete"))
    view = A.seal_view(prov_cid, [s_file], facts, [c_file],
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST])
    run_id = A.seal_run(eval_cid, prov_cid, [view])
    A.extra = {"tsconfigGraphHash": graph_digest, "configOrigin": config_origin,
               "nodes": nodes, "entry": entry, "universeHex": uni_hex,
               "planId": A.plan_id, "snapshotId": A.snapshot_id,
               "scopeDigest": A.scope_digest, "specDigest": A.spec_digest,
               "policyDigest": A.policy_digest, "waiverDigest": A.waiver_digest,
               "projectId": fx.project_id, "evaluatorClosure": eval_cid,
               "providerClosure": prov_cid}
    return fx, A, run_id
