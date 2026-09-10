"""Construct the two complete minimal positive Run descriptor graphs
(TypeScript and Rust) and run the identity-contract Run closure over them.

All provider / OS / compiler / cargo observations below are SYNTHETIC TRUSTED
OBSERVATIONS asserted by this reference, never native enforcement proof.
"""

import copy
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osref as O
from osref import C, H, RAW, REC, Refuse
import graph as G
from graph import Store, sha_text, bare, build_closure, build_snapshot, \
    admit_native_context, bind_typescript_universe, bind_rust_universe, \
    admit_coverage_result_v3, inventory_map, NATIVE_DOC_BYTES, NATIVE_DOC_DIGEST

PROJECT_ID = "prj1-" + "3f" * 32
PLATFORM = "macos-aarch64"


# ------------------------------------------------------------ shared parts --

def base_config(profile, caps):
    return {
        "analysis": {"profileId": profile, "capabilities": sorted(caps),
                     "budget": {"unit": "work-units", "limit": 100000}},
        "components": {},
        "discovery": {},
        "policy": {"packIds": ["opensip.pack.core"]},
        "evidence": {},
    }


def policy_pair(store):
    """A real PolicyDocumentV1 and its compiled RuleProgramV1 projection."""
    emit_when = {"op": "none", "relation": "declares", "minResolution": "syntax",
                 "filters": [{"field": "subjectKind", "cmp": "eq", "value": "symbol"}]}
    rule_ref = {"contributionId": "opensip.core", "ruleStableId": "no-declares",
                "semanticsMajor": 1, "programDigest": RAW(b"rule-program-bytes-v1")}
    store.put_raw(b"rule-program-bytes-v1", "rule-program-artifact")
    policy = {
        "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
        "gateSeverityAtLeast": "error",
        "rules": [{
            "ruleId": "core.no-undeclared", "ruleProgramRef": rule_ref,
            "enabled": True, "severity": "error", "gate": True,
            "subjectEnumeration": {"universe": "unit", "subjectKind": "symbol"},
            "emitWhen": emit_when, "evidenceUse": [],
        }],
    }
    O.check_order("ruleId", policy["rules"], "PolicyDocumentV1.rules")
    policy_digest = store.put_record(policy, "PolicyDocumentV1")
    # identity 3: the compiled program is exactly the projection of the
    # Plan-selected policy's rules, in the policy's own ruleId order.
    program = {"schemaVersion": 1, "policyDigest": policy_digest,
               "rules": [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"],
                          "emitWhen": r["emitWhen"]} for r in policy["rules"]]}
    program_digest = store.put_record(program, "RuleProgramV1")
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
    waiver_digest = store.put_record(waivers, "WaiverSetV1")
    return policy, policy_digest, program, program_digest, waivers, waiver_digest


def capability_manifest(store, profile, providers, absent):
    """CAP-MANIFEST-ID-V1: ADM-TYPE/CLOSED/DOMAIN/ORDER then CVE1 then digest."""
    FP_RELATIONS = {"calls": ["syntactic-callee-name", "resolved-callee"],
                    "clones": ["normalized-body-hash"], "control-flow": ["syntactic"],
                    "declares": ["syntactic"], "file": ["enumerated"],
                    "imports": ["syntactic-specifier", "resolved-target"],
                    "literal": ["syntactic"], "package": ["manifest-declared"],
                    "reachability": ["from-resolved-calls"],
                    "references": ["syntactic-name-match", "resolved-binding"],
                    "types": ["annotated", "checked"], "vcs-change": ["vcs-reported"]}
    PLATFORM_IDS = {"all-supported", "linux-x86_64-gnu", "linux-aarch64-gnu",
                    "macos-aarch64", "macos-x86_64", "windows-x86_64-msvc",
                    "windows-aarch64-msvc", "linux-x86_64-musl"}
    DEFICIENCIES = {"required-relation-missing", "provider-unavailable",
                    "language-tier-unsupported", "budget-exhausted",
                    "confidence-floor-unmet"}
    manifest = {"schemaVersion": 1, "profile": profile,
                "providers": providers, "coverageForAbsent": absent}
    # ADM-CLOSED
    if set(manifest) != {"schemaVersion", "profile", "providers", "coverageForAbsent"}:
        raise Refuse("RELEASE.CAPABILITY_MANIFEST_NOT_CLOSED", "CapabilityManifestV1")
    for p in providers:
        if set(p) != {"providerId", "language", "providerVersionSource",
                      "toolchainIdentitySource", "relations", "platformIds"}:
            raise Refuse("RELEASE.CAPABILITY_MANIFEST_NOT_CLOSED", "ProviderCapability")
    for a in absent:
        if set(a) != {"providerId", "language", "relationIds", "coverageState", "deficiency"}:
            raise Refuse("RELEASE.CAPABILITY_MANIFEST_NOT_CLOSED", "AbsentCapability")
    # ADM-TYPE
    if not isinstance(manifest["schemaVersion"], int) or isinstance(manifest["schemaVersion"], bool):
        raise Refuse("RELEASE.CAPABILITY_MANIFEST_TYPE", "schemaVersion")
    # ADM-DOMAIN
    for p in providers:
        for k, v in p["relations"].items():
            if k not in FP_RELATIONS:
                raise Refuse("RELEASE.CAPABILITY_MANIFEST_DOMAIN", "relation:" + k)
            if v not in FP_RELATIONS[k]:
                raise Refuse("RELEASE.CAPABILITY_MANIFEST_DOMAIN", "rung:%s=%s" % (k, v))
        for pid in p["platformIds"]:
            if pid not in PLATFORM_IDS:
                raise Refuse("RELEASE.CAPABILITY_MANIFEST_DOMAIN", "platformId:" + pid)
    for a in absent:
        for r in a["relationIds"]:
            if r not in FP_RELATIONS:
                raise Refuse("RELEASE.CAPABILITY_MANIFEST_DOMAIN", "relationId:" + r)
        if a["deficiency"] not in DEFICIENCIES:
            raise Refuse("RELEASE.CAPABILITY_MANIFEST_DOMAIN", "deficiency:" + a["deficiency"])
    # ADM-ORDER, in the declared traversal order
    for p in providers:
        _strict_ascending(p["platformIds"], "ProviderCapability.platformIds")
    for a in absent:
        _strict_ascending(a["relationIds"], "AbsentCapability.relationIds")
    _strict_ascending([p["providerId"] for p in providers], "CapabilityManifestV1.providers")
    _strict_ascending([a["providerId"] for a in absent], "CapabilityManifestV1.coverageForAbsent")
    committed = O.cve1(manifest)
    digest = store.put_raw(committed, "capability-manifest-artifact")
    return manifest, committed, digest, O.capability_manifest_id(committed)


def _strict_ascending(values, where):
    keys = [v.encode("utf-8") for v in values]
    for a, b in zip(keys, keys[1:]):
        if not a < b:
            raise Refuse("RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", where)
    if len(set(keys)) != len(keys):
        raise Refuse("RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", where + ":duplicate")


# ============================================================ TypeScript ====

def build_typescript(store):
    out = {}
    # ---- signed closures (synthetic trusted release observation)
    stdlib_files = {
        "lib/lib.dom.d.ts": b"declare interface Window {}\n",
        "lib/lib.es2022.d.ts": b"declare interface Array<T> {}\n",
        "lib/lib.es5.d.ts": b"declare interface Object {}\n",
        "LICENSE": b"Apache-2.0\n",
    }
    stdlib_id, stdlib_desc = build_closure(
        store, "stdlib", stdlib_files, "5.6.2", 2, PLATFORM, b"manifest:ts-stdlib\n")
    tool_files = {
        "bin/node": b"\x7fELF-synthetic-node-runtime\n",
        "lib/tsc.js": b"// synthetic tsc\n",
        "package.json": b'{"name":"typescript","version":"5.6.2"}\n',
    }
    tool_id, tool_desc = build_closure(
        store, "toolchain", tool_files, "5.6.2", 2, PLATFORM, b"manifest:ts-toolchain\n")
    provider_id, provider_desc = build_closure(
        store, "provider", {"bin/tsprovider": b"synthetic-ts-provider\n"},
        "1.0.0", 2, PLATFORM, b"manifest:ts-provider\n")
    evaluator_id, evaluator_desc = build_closure(
        store, "evaluator", {"bin/evaluator": b"synthetic-evaluator\n"},
        "1.0.0", 2, PLATFORM, b"manifest:evaluator\n")
    retained_closures = {stdlib_id: stdlib_desc, tool_id: tool_desc,
                         provider_id: provider_desc, evaluator_id: evaluator_desc}

    # ---- snapshot
    tsconfig = b'{"compilerOptions":{"module":"node16","target":"es2022"}}\n'
    lockbytes = b'{"lockfileVersion":3,"packages":{}}\n'
    files = {
        "package-lock.json": lockbytes,
        "src/a.ts": b"export function foo(){return 1;}\n",
        "src/b.ts": b"import {foo} from './a'; foo();\n",
        "tsconfig.json": tsconfig,
    }
    scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["src"],
             "excludedPathPrefixes": ["node_modules"]}
    for k in ("workspaceRoots", "pathPrefixes", "excludedPathPrefixes"):
        O.check_order("canonical-set", scope[k], "scope-descriptor." + k)
    config = base_config("default", ["declares", "references"])
    snap_id, snap_desc, inventory, scope_digest, config_digest = build_snapshot(
        store, PROJECT_ID, files, scope, "git", "a" * 40, False, config)
    inv = inventory_map(inventory)

    # ---- TypeScriptNativeContextV2 (native 2.4 producing recipe)
    stdlib_components = sorted(
        [{"component": r["path"].rsplit("/", 1)[-1], "sha256": r["sha256"]}
         for r in stdlib_desc["tree"] if r["path"].endswith(".d.ts")],
        key=lambda r: r["component"].encode("utf-8"))
    honored = {
        "allowJs": False, "checkJs": False, "module": "node16",
        "moduleResolution": "node16", "target": "es2022", "strict": True,
        "skipLibCheck": True, "noEmit": True, "types": None,
        "lib": ["ES2022", "DOM"], "baseUrl": None, "paths": [], "rootDirs": [],
        "resolveJsonModule": False, "allowSyntheticDefaultImports": True,
        "esModuleInterop": True, "customConditions": [], "jsx": None,
    }
    ts_ctx = {
        "schemaVersion": 2, "languageMode": "ts-tsconfig",
        "toolchain": {
            "compilerName": "typescript", "compilerVersion": "5.6.2",
            "compilerPackageDigest": [r["sha256"] for r in tool_desc["tree"]
                                      if r["path"] == "package.json"][0],
            "typescriptStdlibMerkleRoot": bare(stdlib_id),
            "standardLibraryComponentDigests": stdlib_components,
            "libSelection": ["dom", "es2022"],
        },
        "toolClosure": {
            "compiler": [r["sha256"] for r in tool_desc["tree"] if r["path"] == "lib/tsc.js"][0],
            "runtime": [r["sha256"] for r in tool_desc["tree"] if r["path"] == "bin/node"][0],
            "closureId": tool_id,
        },
        "configProjection": {
            "schemaVersion": 2, "ancestorCarrierVerified": True,
            "environmentSanitized": True, "typeAcquisitionEnabled": False,
            "executableSelected": False, "honoredOptions": honored,
            "strippedOptions": [{"option": "outDir", "reason": "emits-output"}],
            "configGraphPaths": ["tsconfig.json"],
        },
        "moduleResolutionMode": "node16", "packageModuleType": "module",
        "nodeModulesLayoutDigest": None,
        "lockfileIdentity": {"kind": "package-lock", "path": "package-lock.json",
                             "contentSha256": inv["package-lock.json"]["sha256"]},
    }
    retained = {"closures": retained_closures, "nested": {}, "blobs": set(store.objects)}
    ts_admission = admit_native_context("typescript", ts_ctx, retained, inventory)
    ctx_hex = ts_admission["contextId"]
    store.put_frame("native.context.typescript.v2", ts_ctx, "ts-context")

    ts_universe = {
        "schemaVersion": 2, "languageMode": "ts-tsconfig", "configOrigin": "tsconfig",
        "synthesizerVersion": None, "synthesizedOptions": None,
        "packageModuleType": "module", "allowJs": False, "checkJs": False,
        "jsAdmittedToProgram": False, "jsDiagnosticsEnabled": False,
        "resolutionCompletenessImplied": False, "jsRootFiles": [],
        "programRootFiles": ["src/a.ts", "src/b.ts"], "lockfileKind": "package-lock",
        "nodeModulesInReadSet": False, "executionCapableResolution": False,
        # INVENTED: no producing recipe exists for tsconfigGraphHash anywhere in
        # the kit.  This reference uses raw SHA-256 of the canonical array of
        # {path, sha256} rows of the resolved extends graph and reports the gap.
        "tsconfigGraphHash": REC([{"path": "tsconfig.json",
                                   "sha256": inv["tsconfig.json"]["sha256"]}]),
        "nativeContextId": sha_text(ctx_hex),
    }
    ts_binding = bind_typescript_universe(ts_universe, ts_admission, ts_ctx)
    store.put_frame("native.semantic-universe.typescript.v2", ts_universe, "ts-universe")
    out.update(closures=retained_closures, snapshotId=snap_id, snapshot=snap_desc,
               inventory=inventory, scopeDigest=scope_digest, configDigest=config_digest,
               config=config, context=ts_ctx, contextHex=ctx_hex, universe=ts_universe,
               universeHex=ts_binding["universeId"], providerClosure=provider_id,
               evaluatorClosure=evaluator_id, language="typescript",
               relation="declares", rung="syntactic",
               subjects=["src/a.ts#foo"], retained=retained)
    return out


# ================================================================= Rust =====

def build_rust(store):
    out = {}
    llvm_id, llvm_desc = build_closure(
        store, "rust-dev-llvm", {"lib/librustc_driver.so": b"synthetic-llvm\n"},
        "1.83.0", 3, PLATFORM, b"manifest:rust-dev-llvm\n")
    tool_files = {
        "bin/ar": b"synthetic-ar\n", "bin/cargo": b"synthetic-cargo\n",
        "bin/ld": b"synthetic-linker\n", "bin/proc-macro-srv": b"synthetic-pms\n",
        "bin/rustc": b"synthetic-rustc\n",
    }
    tool_id, tool_desc = build_closure(
        store, "toolchain", tool_files, "1.83.0", 3, PLATFORM, b"manifest:rust-toolchain\n")
    provider_id, provider_desc = build_closure(
        store, "provider", {"bin/rsprovider": b"synthetic-rs-provider\n"},
        "1.0.0", 3, PLATFORM, b"manifest:rs-provider\n")
    evaluator_id, evaluator_desc = build_closure(
        store, "evaluator", {"bin/evaluator": b"synthetic-evaluator\n"},
        "1.0.0", 3, PLATFORM, b"manifest:evaluator\n")
    retained_closures = {llvm_id: llvm_desc, tool_id: tool_desc,
                         provider_id: provider_desc, evaluator_id: evaluator_desc}
    tm = dict((r["path"], r["sha256"]) for r in tool_desc["tree"])

    lockbytes = b'[[package]]\nname = "serde"\nversion = "1.0.0"\n'
    cargo_toml = b'[package]\nname = "app"\nversion = "0.1.0"\n'
    inner_cargo_cfg = b'[build]\ntarget-dir = "ignored"\n'
    files = {
        ".cargo/config.toml": inner_cargo_cfg,
        "Cargo.lock": lockbytes,
        "Cargo.toml": cargo_toml,
        "src/lib.rs": b"pub fn foo() -> u32 { 1 }\n",
    }
    scope = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["src"],
             "excludedPathPrefixes": ["target"]}
    config = base_config("default", ["declares"])
    snap_id, snap_desc, inventory, scope_digest, config_digest = build_snapshot(
        store, PROJECT_ID, files, scope, "git", "b" * 40, False, config)
    inv = inventory_map(inventory)

    # ---- nested native semantic records (records, not opaque strings)
    dep_files = {"src/lib.rs": b"pub fn serde() {}\n", "Cargo.toml": b'[package]\nname="serde"\n'}
    manifest_rows = sorted(
        [{"path": p, "contentSha256": RAW(b), "byteLength": len(b)}
         for p, b in dep_files.items()], key=lambda r: r["path"].encode("utf-8"))
    O.check_order("path", manifest_rows, "DependencyFileManifestV1")
    for b in dep_files.values():
        store.put_raw(b, "dependency-member")
    file_manifest_hex = H("native.dependency-file-manifest.v1", manifest_rows)
    store.put_frame("native.dependency-file-manifest.v1", manifest_rows, "dep-file-manifest")

    dep_set = {
        "schemaVersion": 1, "language": "rust",
        "lockfileIdentity": {"path": "Cargo.lock",
                             "contentSha256": inv["Cargo.lock"]["sha256"],
                             "lockfileVersion": 3},
        "packages": [{
            "name": "serde", "version": "1.0.0", "sourceKind": "registry",
            "sourceId": "registry+https://github.com/rust-lang/crates.io-index",
            "lockChecksum": RAW(b"synthetic-crate-tarball\n"),
            "fileManifestSha256": file_manifest_hex,
            "fileCount": len(manifest_rows),
            "totalBytes": sum(r["byteLength"] for r in manifest_rows),
            "acquisition": {"mode": "in-snapshot-vendored", "descriptorId": None,
                            "vendorPath": "vendor/serde"},
            "checksumVerification": "self-consistent",
            "provenanceAssurance": "declared",
        }],
        "completeness": {"state": "complete", "missing": []},
    }
    O.check_order({"by": ["name", "version", "sourceId"]}, dep_set["packages"],
                  "DependencySourceSetV1.packages")
    dep_hex = H("native.dependency-source-set.v1", dep_set)
    store.put_frame("native.dependency-source-set.v1", dep_set, "dep-source-set")

    features = {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": "aarch64-apple-darwin",
                "activated": [{"packageKey": "serde 1.0.0", "features": ["std"]}],
                "computedBy": {"producer": "opensip-cargo-adapter",
                               "producerBuildId": "synthetic-build-1"}}
    feat_hex = H("native.unified-features.rust.v1", features)
    store.put_frame("native.unified-features.rust.v1", features, "unified-features")

    projected_config = b'[build]\ntarget = "aarch64-apple-darwin"\nrustflags = ["--cfg", "opensip"]\n'
    proj_digest = store.put_raw(projected_config, "projected-cargo-config")
    rustflags = {"honored": ["--cfg", "opensip"],
                 "stripped": [{"flag": "-C linker=cc", "reason": "not-allowlisted"}],
                 "executableSelected": False}
    cargo_projection = {
        "schemaVersion": 2, "honoredKeys": ["build.rustflags", "build.target"],
        "strippedKeys": ["build.target-dir"],
        "replacedSnapshotConfigs": [".cargo/config.toml"],
        "rustflags": rustflags, "ancestorCarrierVerified": True,
        "cargoHome": "private-empty", "environmentProjection": "none",
        "claimsCargoSwitch": False, "projectionSha256": proj_digest,
    }
    proj_hex = H("native.cargo-config-projection.v2", cargo_projection)
    store.put_frame("native.cargo-config-projection.v2", cargo_projection, "cargo-projection")

    rs_ctx = {
        "schemaVersion": 2, "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "c" * 40, "rustcVersion": "1.83.0", "cargoVersion": "1.83.0",
            "sysrootDigest": RAW(b"synthetic-sysroot\n"),
            "rustcDevLlvmDigest": bare(llvm_id),
            "standardLibraryComponentDigests": [
                {"component": "core", "sha256": RAW(b"synthetic-core\n")},
                {"component": "std", "sha256": RAW(b"synthetic-std\n")}],
            "targetTriple": "aarch64-apple-darwin",
        },
        "toolClosure": {"rustc": tm["bin/rustc"], "cargo": tm["bin/cargo"],
                        "linker": tm["bin/ld"], "ar": tm["bin/ar"],
                        "procMacroServer": tm["bin/proc-macro-srv"], "closureId": tool_id},
        "baseCfg": ["target_arch=\"aarch64\"", "target_os=\"macos\""],
        "resolverVersion": 2,
        "dependencySourceSetId": sha_text(dep_hex),
        "unifiedFeaturesId": sha_text(feat_hex),
        "preparedOutputSetId": None,
        "configProjection": cargo_projection,
    }
    retained = {"closures": retained_closures,
                "nested": {sha_text(dep_hex): {"domain": "native.dependency-source-set.v1",
                                               "record": dep_set},
                           sha_text(feat_hex): {"domain": "native.unified-features.rust.v1",
                                                "record": features}},
                "blobs": set(store.objects)}
    rs_admission = admit_native_context("rust", rs_ctx, retained, inventory)
    ctx_hex = rs_admission["contextId"]
    store.put_frame("native.context.rust.v2", rs_ctx, "rust-context")

    rs_universe = {
        "schemaVersion": 2,
        "edition": {"app 0.1.0": 2021},
        "lockfileIdentity": dep_set["lockfileIdentity"],
        "dependencySourceSetId": sha_text(dep_hex),
        "unifiedFeaturesId": sha_text(feat_hex),
        "nativeContextId": sha_text(ctx_hex),
        "cfgSets": [{"cfgSetId": "primary", "cfg": list(rs_ctx["baseCfg"])},
                    {"cfgSetId": "primary+test",
                     "cfg": list(rs_ctx["baseCfg"]) + ["test"]}],
        "rustflags": rustflags,
        "crateRootPaths": ["src/lib.rs"],
        "configProjectionSha256": proj_hex,
        "preparedResolution": "none",
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
    }
    rs_binding = bind_rust_universe(rs_universe, rs_admission, rs_ctx, retained, inventory)
    store.put_frame("native.semantic-universe.rust.v2", rs_universe, "rust-universe")
    out.update(closures=retained_closures, snapshotId=snap_id, snapshot=snap_desc,
               inventory=inventory, scopeDigest=scope_digest, configDigest=config_digest,
               config=config, context=rs_ctx, contextHex=ctx_hex, universe=rs_universe,
               universeHex=rs_binding["universeId"], providerClosure=provider_id,
               evaluatorClosure=evaluator_id, language="rust",
               relation="declares", rung="syntactic",
               subjects=["src/lib.rs#foo"], retained=retained,
               nested={"dependencySourceSet": dep_set, "unifiedFeatures": features,
                       "fileManifest": manifest_rows, "cargoProjection": cargo_projection},
               requiredGrantOperation=rs_binding["requiredGrantOperation"])
    return out


# ======================================================== Run assembly ======

def assemble_run(store, part):
    """Plan -> facts/Coverage/view -> proof -> evidence -> seal -> Run."""
    lang = part["language"]
    uni_hex = part["universeHex"]
    ctx_hex = part["contextHex"]
    snap_id = part["snapshotId"]
    provider = part["providerClosure"]

    # ---- capability manifest (CVE1)
    providers = [{
        "providerId": "provider-" + ("typescript" if lang == "typescript" else "rust"),
        "language": lang,
        "providerVersionSource": "signed-release-manifest",
        "toolchainIdentitySource": "native-context-v2",
        "relations": {"declares": "syntactic"},
        "platformIds": ["macos-aarch64"],
    }]
    absent = [{"providerId": "provider-syntax-all", "language": "text",
               "relationIds": ["clones", "literal"], "coverageState": "unknown",
               "deficiency": "language-tier-unsupported"}]
    cap_manifest, cap_bytes, cap_bytes_digest, cap_id = capability_manifest(
        store, "default", providers, absent)

    policy, policy_digest, program, program_digest, waivers, waiver_digest = policy_pair(store)

    analysis_spec = {
        "schemaVersion": 2,
        "requestedCapabilities": sorted(
            [{"capabilityId": "declares", "languageMode":
              "ts-tsconfig" if lang == "typescript" else "rust-cargo",
              "workspaceRoot": ".", "required": True}],
            key=lambda r: C(r)),
        "policyPackIds": ["opensip.pack.core"],
        "parameters": [],
    }
    O.check_order("canonical-set", analysis_spec["requestedCapabilities"],
                  "analysis-spec.requestedCapabilities")
    analysis_digest = store.put_record(analysis_spec, "analysis-spec")

    grant = {"schemaVersion": 2, "projectId": PROJECT_ID,
             "principals": [{"kind": "first-party", "closureId": provider,
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(["native-analysis", "read-source"],
                                          key=lambda s: C(s)),
             "scopeDigest": part["scopeDigest"]}
    O.check_order("canonical-set", grant["analysisOperations"],
                  "semantic-grant.analysisOperations")
    grant_digest = store.put_record(grant, "semantic-grant")

    plan = {
        "schemaVersion": 2, "snapshotId": snap_id, "capabilityManifestId": cap_id,
        "semanticClosures": sorted([provider, part["evaluatorClosure"]], key=lambda s: C(s)),
        "analysisSpecDigest": analysis_digest,
        "resolvedConfigDigest": part["configDigest"],
        "nativeContextDigests": [ctx_hex],
        "importIds": [], "policyDigest": policy_digest, "waiverDigest": waiver_digest,
        "scopeDigest": part["scopeDigest"],
        "budget": {"unit": "work-units", "limit": 100000},
        "semanticGrantDigest": grant_digest,
        "capabilityManifestBytesDigest": cap_bytes_digest,
    }
    O.check_order("canonical-set", plan["semanticClosures"], "plan.semanticClosures")
    O.check_order("canonical-set", plan["nativeContextDigests"], "plan.nativeContextDigests")
    plan_id = "plan2:" + store.put_frame("plan", plan, "plan")

    # ---- subject scope + Coverage (host-owned enumeration)
    scope_desc = {"schemaVersion": 2, "snapshotId": snap_id, "sourceUniverse": uni_hex,
                  "targetUniverse": uni_hex, "relation": part["relation"],
                  "resolution": part["rung"], "enumeratorClosure": provider,
                  "subjects": sorted(part["subjects"], key=lambda s: C(s))}
    O.check_order("canonical-set", scope_desc["subjects"], "subject-scope.subjects")
    cov_payload = {
        "schemaVersion": 3,
        "key": {"relation": part["relation"], "resolution": part["rung"],
                "sourceUniverse": uni_hex, "targetUniverse": uni_hex,
                "subjectScopeCommitment": sha_text(H("subject-scope", scope_desc))},
        "entry": {
            "relation": part["relation"], "resolution": part["rung"],
            "coverage": "complete",
            "examinedUniverse": {"subjectScopeCommitment":
                                 sha_text(H("subject-scope", scope_desc)),
                                 "subjectCount": len(scope_desc["subjects"])},
            "resolutionCompleteness": {"state": "not-applicable", "attempted": False,
                                       "examinedExhaustive": True, "stageTerminal": "complete",
                                       "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
            "closedWorld": {"exportsClosed": "closed", "entryPointsRecognized": "all",
                            "nonliteralLoading": "none", "externalConsumers": "none-declared",
                            "dynamicDispatch": "not-applicable", "reasons": [],
                            "deadCodeRepairEligible": True},
            "derivationKinds": [], "confidenceMillionths": 1000000,
            "deficiency": None, "nativeCause": None,
        },
    }
    cov_id, cov_desc, scope_id, _, commitment = admit_coverage_result_v3(
        store, scope_desc, cov_payload, NATIVE_DOC_DIGEST)

    # ---- fact  (relation payload schema document: INVENTED, see report)
    fact_payload = {"container": part["subjects"][0].split("#")[0],
                    "declared": part["subjects"][0], "declarationKind": "function"}
    fact_payload_digest = store.put_record(fact_payload, "relation.declares.v1")
    anchor_path = part["subjects"][0].split("#")[0]
    anchor_row = inventory_map(part["inventory"])[anchor_path]
    anchor = {"path": anchor_path, "blobDigest": anchor_row["sha256"],
              "startByte": 0, "endByte": anchor_row["bytes"]}
    fact = {"schemaVersion": 2, "snapshotId": snap_id, "relation": part["relation"],
            "resolution": part["rung"], "sourceUniverse": uni_hex, "targetUniverse": uni_hex,
            "producerClosure": provider, "payloadSchemaDigest": NATIVE_DOC_DIGEST,
            "payloadDigest": fact_payload_digest, "anchors": [anchor],
            "confidenceMillionths": 1000000}
    O.check_order("canonical-set", fact["anchors"], "fact.anchors")
    fact_id = "fact2:" + store.put_frame("fact", fact, "fact")

    view = {"schemaVersion": 2, "planId": plan_id, "scopeIds": [scope_id],
            "facts": [fact_id], "coverageIds": [cov_id], "producerClosure": provider,
            "schemaDigests": [NATIVE_DOC_DIGEST]}
    view_id = "view2:" + store.put_frame("view", view, "view")

    # ---- derivation DAG
    stage_spec = {"schemaVersion": 2, "planId": plan_id, "producerClosure": provider,
                  "operation": "native-analysis", "parameters": [],
                  "outputDomains": sorted(["coverage", "fact"], key=lambda s: C(s)),
                  "outputSchemaDigest": NATIVE_DOC_DIGEST}
    stage_digest = store.put_record(stage_spec, "stage-spec")
    exec_plan = {"schemaVersion": 2, "planId": plan_id,
                 "stages": [{"ordinal": 0, "stageSpecDigest": stage_digest,
                             "requires": [], "outputDomains": stage_spec["outputDomains"]}]}
    O.check_order("ordinal", exec_plan["stages"], "execution-plan.stages")
    exec_id = "exec-plan2:" + store.put_frame("execution-plan", exec_plan, "exec-plan")

    # ---- proof
    node = policy["rules"][0]["emitWhen"]
    node_digest = store.put_record(node, "Predicate-node")
    prog_pred = {"schemaVersion": 2, "ruleProgramDigest": program_digest,
                 "ruleId": "core.no-undeclared", "predicateId": "p",
                 "operation": "none", "nodeDigest": node_digest}
    prog_pred_digest = store.put_record(prog_pred, "program-predicate")
    witness = {"schemaVersion": 2, "programPredicateDigest": prog_pred_digest,
               "matchingFactIds": [fact_id], "coverageIds": [cov_id],
               "countLimit": None, "childPredicateIds": []}
    witness_digest = store.put_record(witness, "predicate-witness")
    inputs = sorted([{"domain": "view", "digest": bare(view_id)},
                     {"domain": "coverage", "digest": bare(cov_id)},
                     {"domain": "rule-program", "digest": program_digest},
                     {"domain": "policy", "digest": policy_digest},
                     {"domain": "waiver", "digest": waiver_digest},
                     {"domain": "native-context", "digest": ctx_hex}],
                    key=lambda r: C(r))
    O.check_order("canonical-set", inputs, "proof.evaluationInputRefs")
    pp_inputs = sorted([{"domain": "view", "digest": bare(view_id)},
                        {"domain": "coverage", "digest": bare(cov_id)}], key=lambda r: C(r))
    proof = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": exec_id,
             "evaluatorClosure": part["evaluatorClosure"], "ruleProgramDigest": program_digest,
             "evaluationInputRefs": inputs,
             "predicateProofs": [{"ruleId": "core.no-undeclared",
                                  "subjectId": part["subjects"][0], "predicateId": "p",
                                  "operation": "none", "inputRefs": pp_inputs,
                                  "scopeIds": [scope_id], "value": "false",
                                  "witnessDigest": witness_digest}],
             "findingIds": [], "verdict": "pass"}
    O.check_order("predicate", proof["predicateProofs"], "proof.predicateProofs")
    proof_id = "proof2:" + store.put_frame("proof-bundle", proof, "proof")

    evidence = {"schemaVersion": 2, "planId": plan_id, "viewIds": [view_id],
                "coverageIds": [cov_id], "importIds": [], "findingIds": [],
                "proofBundleId": proof_id}
    evidence_id = "evidence2:" + store.put_frame("semantic-evidence", evidence, "evidence")
    seal = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": exec_id,
            "evidenceId": evidence_id, "evaluatorClosure": part["evaluatorClosure"],
            "policyDigest": policy_digest, "proofBundleId": proof_id, "verdict": "pass"}
    seal_id = "seal2:" + store.put_frame("evaluation-seal", seal, "seal")
    run = {"schemaVersion": 2, "projectId": PROJECT_ID, "snapshotId": snap_id,
           "planId": plan_id, "evidenceId": evidence_id, "evaluationSealId": seal_id,
           "capabilityManifestId": cap_id}
    run_id = "run2:" + store.put_frame("run", run, "run")

    return {
        "language": lang, "runId": run_id, "run": run, "seal": seal, "sealId": seal_id,
        "evidence": evidence, "evidenceId": evidence_id, "proof": proof, "proofId": proof_id,
        "view": view, "viewId": view_id, "fact": fact, "factId": fact_id,
        "coverage": cov_desc, "coverageId": cov_id, "scope": scope_desc, "scopeId": scope_id,
        "subjectScopeCommitment": commitment, "plan": plan, "planId": plan_id,
        "execPlan": exec_plan, "execPlanId": exec_id, "stageSpec": stage_spec,
        "capabilityManifest": cap_manifest, "capabilityManifestId": cap_id,
        "capabilityManifestBytes": cap_bytes, "policy": policy, "program": program,
        "witness": witness, "programPredicate": prog_pred, "grant": grant,
        "analysisSpec": analysis_spec, "part": part,
    }
