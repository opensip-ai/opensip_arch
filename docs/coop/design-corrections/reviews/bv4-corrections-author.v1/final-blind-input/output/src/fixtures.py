"""Shared synthetic fixtures. Every observation here is a SYNTHETIC TCB ASSUMPTION."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402

PLATFORM = "macos-aarch64"
BUDGET = {"unit": "work-units", "limit": 100000}


def config(capabilities):
    return {"analysis": {"profileId": "default", "capabilities": sorted(capabilities),
                         "budget": dict(BUDGET)},
            "components": {}, "discovery": {}, "policy": {}, "evidence": {}}


def scope(roots=(".",), prefixes=(), excluded=()):
    return {"schemaVersion": 2, "workspaceRoots": sorted(set(roots)),
            "pathPrefixes": sorted(set(prefixes)),
            "excludedPathPrefixes": sorted(set(excluded))}


def capability_manifest(providers, absent=()):
    m = {"schemaVersion": 1, "profile": "full",
         "providers": sorted(providers, key=lambda p: p["providerId"].encode()),
         "coverageForAbsent": sorted(absent, key=lambda a: a["providerId"].encode())}
    reg = kit.doc("capdomains")["registries"]
    for p in m["providers"]:
        p["platformIds"] = sorted(set(p["platformIds"]))
        for pid in p["platformIds"]:
            assert pid in reg["PLATFORM-ID-DOMAIN-V1"]["members"], pid
        for rel, rung in p["relations"].items():
            assert rel in reg["RELATION-DOMAIN-V2"]["members"], rel
            assert rung in reg["RELATION-LADDER-DOMAIN-V2"]["ladders"][rel], (rel, rung)
    for a in m["coverageForAbsent"]:
        a["relationIds"] = sorted(set(a["relationIds"]))
        assert a["coverageState"] in reg["COVERAGE-STATE-DOMAIN-V1"]["members"]
        assert a["deficiency"] in reg["DEFICIENCY-DOMAIN-V1"]["members"]
    return m


# --- closures -------------------------------------------------------------

def ts_toolchain(store, version="5.6.2", platform=PLATFORM, extra=b""):
    files = {"bin/tsc.js": b"// bundled typescript compiler" + extra,
             "bin/node": b"\x7fELF bundled javascript runtime" + extra}
    return G.make_closure(store, "toolchain", files, version, 2, platform)


def ts_stdlib(store, version="5.6.2", platform=PLATFORM, extra_lib=None, drop=None):
    files = {"lib/lib.dom.d.ts": b"declare var window: any;",
             "lib/lib.es2022.d.ts": b"declare var Promise: any;",
             "lib/lib.esnext.d.ts": b"declare var structuredClone: any;"}
    if extra_lib:
        files.update(extra_lib)
    if drop:
        files.pop(drop, None)
    return G.make_closure(store, "stdlib", files, version, 2, platform)


def rust_toolchain(store, version="1.82.0", platform=PLATFORM):
    files = {"bin/rustc": b"\x7fELF rustc", "bin/cargo": b"\x7fELF cargo",
             "bin/lld": b"\x7fELF linker", "bin/ar": b"\x7fELF ar",
             "libexec/proc-macro-srv": b"\x7fELF proc macro server"}
    return G.make_closure(store, "toolchain", files, version, 3, platform)


def rust_dev_llvm(store, version="1.82.0", platform=PLATFORM):
    return G.make_closure(store, "rust-dev-llvm",
                          {"lib/librustc_dev_llvm.so": b"\x7fELF llvm"},
                          version, 3, platform)


def grammar_bundle_closure(store, version="0.9.0", platform=PLATFORM):
    files = {"grammars/rust.grammar": b"grammar rust",
             "grammars/typescript.grammar": b"grammar typescript",
             "grammars/javascript.grammar": b"grammar javascript",
             "grammars/json.grammar": b"grammar json",
             "grammars/toml.grammar": b"grammar toml",
             "grammars/markdown.grammar": b"grammar markdown",
             "grammars/yaml.grammar": b"grammar yaml",
             "bundle.manifest": b"bundle manifest v1",
             "normalizer/level-spec.txt": b"L1 lexical spec"}
    return G.make_closure(store, "grammar", files, version, 1, platform)


def provider_closure(store, name, version="1.0.0", platform=PLATFORM):
    return G.make_closure(store, "provider", {"bin/" + name: ("\x7fELF " + name).encode()},
                          version, 3, platform)


def evaluator_closure(store, version="1.0.0", platform=PLATFORM):
    return G.make_closure(store, "evaluator", {"bin/evaluator": b"\x7fELF evaluator"},
                          version, 1, platform)


def rule_closure(store, version="1.0.0", platform=PLATFORM):
    return G.make_closure(store, "detector", {"rules/no-clone.rule": b"rule bytes"},
                          version, 1, platform)


# --- TypeScript context/universe -----------------------------------------

def ts_honored(lib, allow_js, check_js, module_res="node16", jsx=None):
    return {"allowJs": allow_js, "checkJs": check_js, "module": "node16",
            "moduleResolution": module_res, "target": "es2022", "strict": True,
            "skipLibCheck": True, "noEmit": True, "types": [], "lib": list(lib),
            "baseUrl": None, "paths": [], "rootDirs": [], "resolveJsonModule": True,
            "allowSyntheticDefaultImports": True, "esModuleInterop": True,
            "customConditions": [], "jsx": jsx}


def ts_context(store, tool, std, config_graph_paths, language_mode, honored,
               node_modules_digest, lockfile, package_module_type="commonjs",
               stripped=()):
    dts = sorted((os.path.basename(r["path"]), r["sha256"])
                 for r in std["descriptor"]["tree"] if r["path"].endswith(".d.ts"))
    desc = {
        "schemaVersion": 2, "languageMode": language_mode,
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": tool["descriptor"]["semanticVersion"],
            "compilerPackageDigest": tool["members"]["bin/tsc.js"],
            "typescriptStdlibMerkleRoot": std["hex"],
            "standardLibraryComponentDigests": [{"component": c, "sha256": s}
                                                for c, s in dts],
            "libSelection": sorted(honored["lib"], key=lambda x: x.encode()),
        },
        "toolClosure": {"compiler": tool["members"]["bin/tsc.js"],
                        "runtime": tool["members"]["bin/node"],
                        "closureId": tool["id"]},
        "configProjection": {
            "schemaVersion": 2, "ancestorCarrierVerified": True,
            "environmentSanitized": True, "typeAcquisitionEnabled": False,
            "executableSelected": False, "honoredOptions": honored,
            "strippedOptions": list(stripped),
            "configGraphPaths": sorted(config_graph_paths)},
        "moduleResolutionMode": honored["moduleResolution"],
        "packageModuleType": package_module_type,
        "nodeModulesLayoutDigest": node_modules_digest,
        "lockfileIdentity": lockfile,
    }
    return G.mint_context(store, G.TS_CONTEXT_DOMAIN, desc)


def ts_universe(store, ctx, graph_record, program_roots, js_roots, config_origin,
                synthesized=None, synthesizer_version=None):
    C = ctx["descriptor"]
    ho = C["configProjection"]["honoredOptions"]
    desc = {"schemaVersion": 2, "languageMode": C["languageMode"],
            "configOrigin": config_origin,
            "synthesizerVersion": synthesizer_version,
            "synthesizedOptions": synthesized,
            "packageModuleType": C["packageModuleType"],
            "allowJs": ho["allowJs"], "checkJs": ho["checkJs"],
            "jsAdmittedToProgram": ho["allowJs"],
            "jsDiagnosticsEnabled": ho["checkJs"],
            "resolutionCompletenessImplied": False,
            "jsRootFiles": sorted(js_roots),
            "programRootFiles": sorted(program_roots),
            "lockfileKind": "none" if C["lockfileIdentity"] is None
            else C["lockfileIdentity"]["kind"],
            "nodeModulesInReadSet": C["nodeModulesLayoutDigest"] is not None,
            "executionCapableResolution": False,
            "tsconfigGraphHash": osip.canonical_record_digest(graph_record),
            "nativeContextId": ctx["sha256text"]}
    return G.mint_universe(store, G.TS_UNIVERSE_DOMAIN, desc)


# --- Rust context/universe ------------------------------------------------

def cargo_projection(store, replaced_configs, projected_bytes=b"[build]\n"):
    return {"schemaVersion": 2,
            "honoredKeys": sorted(["build.rustflags", "resolver"]),
            "strippedKeys": sorted(["build.rustc", "target.*.linker", "net"]),
            "replacedSnapshotConfigs": sorted(replaced_configs),
            "rustflags": {"honored": ["--cfg", "feature=\"x\""],
                          "stripped": [], "executableSelected": False},
            "ancestorCarrierVerified": True, "cargoHome": "private-empty",
            "environmentProjection": "none", "claimsCargoSwitch": False,
            "projectionSha256": store.put_blob(projected_bytes)}


def rust_context(store, tool, llvm, projection, dep_set_id, features_id,
                 prepared_id=None, target="aarch64-apple-darwin"):
    desc = {"schemaVersion": 2, "targetTriple": target, "hostTriple": target,
            "toolchain": {"rustCommitHash": "a1b2c3d4" * 5,
                          "rustcVersion": tool["descriptor"]["semanticVersion"],
                          "cargoVersion": tool["descriptor"]["semanticVersion"],
                          "sysrootDigest": osip.raw_sha256(b"sysroot"),
                          "rustcDevLlvmDigest": llvm["hex"],
                          "standardLibraryComponentDigests": [
                              {"component": "core", "sha256": osip.raw_sha256(b"core")},
                              {"component": "std", "sha256": osip.raw_sha256(b"std")}],
                          "targetTriple": target},
            "toolClosure": {"rustc": tool["members"]["bin/rustc"],
                            "cargo": tool["members"]["bin/cargo"],
                            "linker": tool["members"]["bin/lld"],
                            "ar": tool["members"]["bin/ar"],
                            "procMacroServer": tool["members"]["libexec/proc-macro-srv"],
                            "closureId": tool["id"]},
            "baseCfg": sorted(["target_arch=\"aarch64\"", "target_os=\"macos\""]),
            "resolverVersion": 2,
            "dependencySourceSetId": dep_set_id,
            "unifiedFeaturesId": features_id,
            "preparedOutputSetId": prepared_id,
            "configProjection": projection}
    return G.mint_context(store, G.RS_CONTEXT_DOMAIN, desc)


def dependency_source_set(lockfile):
    return {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lockfile,
            "packages": [], "completeness": {"state": "complete", "missing": []}}


def unified_features(target="aarch64-apple-darwin"):
    return {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": target,
            "activated": [], "computedBy": {"tool": "cargo", "version": "1.82.0",
                                            "invocation": "metadata --offline --frozen --locked"}}


def rust_universe(store, ctx, editions, lockfile, crate_roots, ownership_id,
                  prepared_resolution="none", prepared_id=None):
    C = ctx["descriptor"]
    desc = {"schemaVersion": 2, "edition": dict(editions),
            "lockfileIdentity": lockfile,
            "dependencySourceSetId": C["dependencySourceSetId"],
            "unifiedFeaturesId": C["unifiedFeaturesId"],
            "nativeContextId": ctx["sha256text"],
            "cfgSets": [{"cfgSetId": "primary", "cfg": list(C["baseCfg"])},
                        {"cfgSetId": "primary+test",
                         "cfg": sorted(list(C["baseCfg"]) + ["test"])}],
            "rustflags": C["configProjection"]["rustflags"],
            "crateRootPaths": sorted(crate_roots),
            "configProjectionSha256": osip.H("native.cargo-config-projection.v2",
                                             C["configProjection"]),
            "executionCapableResolution": prepared_resolution != "none",
            "preparedOutputSetId": prepared_id,
            "preparedResolution": prepared_resolution,
            "sourceUnitOwnershipId": ownership_id}
    return G.mint_universe(store, G.RS_UNIVERSE_DOMAIN, desc)


def unit(marker, crate, kind, name, edition=None):
    uid = "sha256:" + osip.H("native.compilation-unit.v1",
                             {"schemaVersion": 1, "markerPath": marker,
                              "targetKind": kind, "targetName": name})
    return {"unitId": uid, "markerPath": marker, "crateName": crate,
            "targetKind": kind, "targetName": name, "targetEdition": edition}


def ownership(units, selected, rows, enumeration="complete"):
    return {"schemaVersion": 1, "enumeration": enumeration,
            "units": sorted(units, key=lambda u: u["unitId"]),
            "selectedUnitIds": sorted(set(selected)),
            "ownership": sorted(rows, key=lambda r: (r["path"], r["unitId"]))}


# --- syntax context/universe ---------------------------------------------

REG = kit.doc("native")["x-opensip-grammar-capability-registry"]["languages"]


def syntax_context(store, gclosure, languages=None):
    languages = languages or sorted(REG)
    grammars = []
    for lang in languages:
        row = REG[lang]
        grammars.append({"grammarId": "g." + lang, "grammarVersion": "1",
                         "languageId": lang, "syntaxClass": row["syntaxClass"],
                         "suffixes": sorted(row["suffixes"]),
                         "grammarDigest": gclosure["members"]["grammars/%s.grammar" % lang]})
    desc = {"schemaVersion": 2,
            "grammarBundle": {
                "schemaVersion": 1, "closureId": gclosure["id"],
                "parserName": "opensip-grammar-parser",
                "parserVersion": gclosure["descriptor"]["semanticVersion"],
                "bundleDigest": gclosure["members"]["bundle.manifest"],
                "grammars": sorted(grammars, key=lambda g: g["grammarId"]),
                "normalizer": {"normalizerId": "syntax-normalizer",
                               "normalizerVersion": "1",
                               "specificationDigest":
                                   gclosure["members"]["normalizer/level-spec.txt"]}}}
    return G.mint_context(store, G.SX_CONTEXT_DOMAIN, desc)


def syntax_universe(store, ctx, selected):
    desc = {"schemaVersion": 2, "nativeContextId": ctx["sha256text"],
            "selectedGrammarIds": sorted(selected), "resolutionAttempted": False}
    return G.mint_universe(store, G.SX_UNIVERSE_DOMAIN, desc)


# --- Coverage entries -----------------------------------------------------

CLOSED_WORLD_UNKNOWN = {"exportsClosed": "unknown", "entryPointsRecognized": "none",
                        "nonliteralLoading": "none", "externalConsumers": "unknown",
                        "dynamicDispatch": "not-applicable", "reasons": [],
                        "deadCodeRepairEligible": False}


def entry(relation, rung, coverage, commitment, count, state, attempted,
          exhaustive, terminal, edge_count=0, classes=(), deficiency=None,
          cause=None, closed_world=None, derivation_kinds=()):
    return {"relation": relation, "resolution": rung, "coverage": coverage,
            "examinedUniverse": {"subjectScopeCommitment": commitment,
                                 "subjectCount": count},
            "resolutionCompleteness": {"state": state, "attempted": attempted,
                                       "examinedExhaustive": exhaustive,
                                       "stageTerminal": terminal,
                                       "unresolvedEdgeCount": edge_count,
                                       "unresolvedEdgeClasses": sorted(set(classes))},
            "closedWorld": dict(closed_world or CLOSED_WORLD_UNKNOWN),
            "derivationKinds": sorted(set(derivation_kinds)),
            "confidenceMillionths": 1000000,
            "deficiency": deficiency, "nativeCause": cause}


def na_entry(relation, rung, scope, coverage="complete", deficiency=None, cause=None):
    return entry(relation, rung, coverage, scope["commitment"], scope["subjectCount"],
                 "not-applicable", False, True, None, 0, (), deficiency, cause)
