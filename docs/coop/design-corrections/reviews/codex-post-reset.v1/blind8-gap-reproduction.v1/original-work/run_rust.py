"""CB-RUN-RS: a complete minimal positive Rust Run descriptor graph.

A MIXED-EDITION Cargo workspace with:
  * a target-specific edition that differs from its package default,
  * the same physical source file under two distinct explicitly selected
    target editions (two selections => two universes => two valid forms),
  * a valid `#` marker directory,
  * a representative large edition map,
  * the nested dependency-source / unified-features / cargo-config-projection /
    prepared-output records retained and joined.
"""
from __future__ import annotations

import hashlib

import assemble
import build
import closure as CL
import osip
from build import Fixture, coverage_entry
from osip import C, H, record_digest, raw_sha256

PLATFORM = "linux-x86_64-gnu"
TRIPLE = "x86_64-unknown-linux-gnu"
RUSTC_VERSION = "1.83.0"
RUST_COMMIT = "a" * 40

SHARED_BODY = b"{\n    let n = a + b;\n    n\n}"
SHARED_RS = b"pub fn add(a: i32, b: i32) -> i32 " + SHARED_BODY + b"\n"

LARGE_EDITIONS = {"cb-core": 2021, "cb-legacy": 2015, "cb-tools": 2024}
for i in range(1, 19):
    LARGE_EDITIONS["cb-aux-%02d" % i] = [2015, 2018, 2021, 2024][i % 4]

CAP_MANIFEST = {
    "schemaVersion": 1, "profile": "default",
    "providers": [
        {"providerId": "opensip.provider.rust", "language": "rust",
         "providerVersionSource": "closure-manifest",
         "toolchainIdentitySource": "native-context",
         "relations": {"clones": "normalized-body-hash", "file": "enumerated",
                       "package": "manifest-declared",
                       "unresolved-edge": "observed"},
         "platformIds": [PLATFORM]},
    ],
    "coverageForAbsent": [],
}


def unit_id(marker, kind, name):
    return "sha256:" + H("native.compilation-unit.v1",
                         {"schemaVersion": 1, "markerPath": marker,
                          "targetKind": kind, "targetName": name})


def build_run(selection="lib", mutate=None, prepared=False):
    """selection: 'lib' | 'test2024' | 'lib+bin' | 'ambiguous' | 'partial' | 'none'"""
    fx = Fixture("cb-rs-" + selection + ("-prepared" if prepared else ""))
    m = mutate or {}

    ws = b'[workspace]\nmembers = ["crates/core", "crates/legacy", "crates/tools#gen"]\n'
    lock = (b'version = 3\n\n[[package]]\nname = "serde"\nversion = "1.0.0"\n'
            b'source = "registry+https://example.invalid/index"\n'
            b'checksum = "' + b"b" * 64 + b'"\n')
    core_toml = b'[package]\nname = "cb-core"\nversion = "0.1.0"\nedition = "2021"\n'
    legacy_toml = b'[package]\nname = "cb-legacy"\nversion = "0.1.0"\nedition = "2015"\n'
    tools_toml = b'[package]\nname = "cb-tools"\nversion = "0.1.0"\nedition = "2024"\n'
    cargo_cfg = b'[build]\nrustflags = ["--cfg", "feature=\\"x\\""]\n'
    vendor_toml = b'[package]\nname = "serde"\nversion = "1.0.0"\nedition = "2018"\n'
    vendor_lib = b"pub fn ser() {}\n"

    fx.add_file("Cargo.toml", ws)
    fx.add_file("Cargo.lock", lock)
    fx.add_file(".cargo/config.toml", cargo_cfg)
    fx.add_file("crates/core/Cargo.toml", core_toml)
    fx.add_file("crates/core/src/lib.rs", b"pub mod shared;\n")
    fx.add_file("crates/core/src/shared.rs", SHARED_RS)
    fx.add_file("crates/legacy/Cargo.toml", legacy_toml)
    fx.add_file("crates/legacy/src/lib.rs", b"pub fn old() {}\n")
    fx.add_file("crates/tools#gen/Cargo.toml", tools_toml)   # a `#` marker directory
    fx.add_file("crates/tools#gen/src/main.rs", b"fn main() {}\n")
    fx.add_file("vendor/serde-1.0.0/Cargo.toml", vendor_toml)
    fx.add_file("vendor/serde-1.0.0/src/lib.rs", vendor_lib)
    inv = {r["path"]: r for r in fx.inventory()}

    # ---- closures ------------------------------------------------------
    tool_cid, _, tool_members = fx.closure(
        "rust-toolchain", "toolchain",
        {"bin/rustc": b"#bundled rustc\n", "bin/cargo": b"#bundled cargo\n",
         "bin/ld": b"#bundled linker\n", "bin/ar": b"#bundled ar\n",
         "bin/proc-macro-srv": b"#bundled proc-macro server\n"},
        RUSTC_VERSION, PLATFORM)
    llvm_cid, _, _ = fx.closure("rust-dev-llvm", "rust-dev-llvm",
                                {"lib/libLLVM.so": b"#llvm\n"}, RUSTC_VERSION, PLATFORM)
    prov_cid, _, _ = fx.closure("rust-provider", "provider",
                                {"bin/provider": b"#rust semantic provider\n"},
                                "1.0.0", PLATFORM)
    eval_cid, _, _ = fx.closure("evaluator", "evaluator",
                                {"bin/evaluator": b"#pure evaluator\n"},
                                "1.0.0", PLATFORM)

    # ---- nested native records (native section 3) ------------------------
    manifest_rows = sorted(
        [{"path": "Cargo.toml", "contentSha256": raw_sha256(vendor_toml),
          "byteLength": len(vendor_toml)},
         {"path": "src/lib.rs", "contentSha256": raw_sha256(vendor_lib),
          "byteLength": len(vendor_lib)}],
        key=lambda r: r["path"].encode())
    fmh = fx.hid("native.dependency-file-manifest.v1", manifest_rows, "native",
                 "#/$defs/DependencyFileManifestV1", "dependency-file-manifest")
    lockid = {"path": "Cargo.lock", "contentSha256": inv["Cargo.lock"]["sha256"],
              "lockfileVersion": 3}
    dss = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lockid,
           "packages": [{"name": "serde", "version": "1.0.0", "sourceKind": "vendored",
                         "sourceId": "registry+https://example.invalid/index",
                         "lockChecksum": "b" * 64, "fileManifestSha256": fmh,
                         "fileCount": 2,
                         "totalBytes": len(vendor_toml) + len(vendor_lib),
                         "acquisition": {"mode": "in-snapshot-vendored",
                                         "descriptorId": None,
                                         "vendorPath": "vendor/serde-1.0.0"},
                         # DS-1: a vendored .cargo-checksum.json proves nothing
                         # about the files, so this stays self-consistent/declared
                         "checksumVerification": "self-consistent",
                         "provenanceAssurance": "declared"}],
           "completeness": {"state": "complete", "missing": []}}
    dss_h = fx.hid("native.dependency-source-set.v1", dss, "native",
                   "#/$defs/DependencySourceSetV1", "dependency-source-set")
    uf = {"schemaVersion": 1, "resolverVersion": 2, "targetTriple": TRIPLE,
          "activated": [{"packageKey": "serde 1.0.0", "features": ["std"]}],
          "computedBy": {"producer": "opensip-cargo-adapter",
                         "producerBuildId": "cb-adapter-1"}}
    uf_h = fx.hid("native.unified-features.rust.v1", uf, "native",
                  "#/$defs/UnifiedFeaturesV1", "unified-features")
    projected = b'[source.vendored]\ndirectory = "vendor"\n'
    proj_digest = fx.s.put_raw(projected, "projected .cargo/config.toml")
    cfgproj = {"schemaVersion": 2,
               "honoredKeys": ["build.rustflags", "source.vendored.directory"],
               "strippedKeys": ["build.rustc", "target.*.linker"],
               "replacedSnapshotConfigs": [".cargo/config.toml"],
               "rustflags": {"honored": ['--cfg feature="x"'],
                             "stripped": [{"flag": "-C linker=cc",
                                           "reason": "codegen-option-not-allowlisted"}],
                             "executableSelected": False},
               "ancestorCarrierVerified": True, "cargoHome": "private-empty",
               "environmentProjection": "none", "claimsCargoSwitch": False,
               "projectionSha256": proj_digest}
    cfgproj_h = fx.hid("native.cargo-config-projection.v2", cfgproj, "native",
                       "#/$defs/CargoConfigProjectionV2", "cargo-config-projection")

    # ---- SourceUnitOwnershipV1 -----------------------------------------
    core_marker = "crates/core/Cargo.toml"
    tools_marker = "crates/tools#gen/Cargo.toml"
    legacy_marker = "crates/legacy/Cargo.toml"
    u_lib = {"unitId": unit_id(core_marker, "lib", "cb_core"),
             "markerPath": core_marker, "crateName": "cb-core",
             "targetKind": "lib", "targetName": "cb_core", "targetEdition": None}
    # a TARGET-SPECIFIC edition that differs from its package default (2021)
    u_test = {"unitId": unit_id(core_marker, "test", "shared_it"),
              "markerPath": core_marker, "crateName": "cb-core",
              "targetKind": "test", "targetName": "shared_it", "targetEdition": 2024}
    u_bin = {"unitId": unit_id(tools_marker, "bin", "gen"),
             "markerPath": tools_marker, "crateName": "cb-tools",
             "targetKind": "bin", "targetName": "gen", "targetEdition": None}
    u_legacy = {"unitId": unit_id(legacy_marker, "lib", "cb_legacy"),
                "markerPath": legacy_marker, "crateName": "cb-legacy",
                "targetKind": "lib", "targetName": "cb_legacy", "targetEdition": None}
    units = sorted([u_lib, u_test, u_bin, u_legacy],
                   key=lambda u: u["unitId"].encode())
    ownership = sorted(
        [{"path": "crates/core/src/shared.rs", "unitId": u_lib["unitId"]},
         {"path": "crates/core/src/shared.rs", "unitId": u_test["unitId"]},
         {"path": "crates/core/src/lib.rs", "unitId": u_lib["unitId"]},
         {"path": "crates/legacy/src/lib.rs", "unitId": u_legacy["unitId"]},
         {"path": "crates/tools#gen/src/main.rs", "unitId": u_bin["unitId"]}],
        key=lambda o: (o["path"].encode(), o["unitId"].encode()))
    sel = {"lib": [u_lib["unitId"]],
           "test2024": [u_test["unitId"]],
           "lib+bin": sorted([u_lib["unitId"], u_bin["unitId"]],
                             key=lambda x: x.encode()),
           "ambiguous": sorted([u_lib["unitId"], u_test["unitId"]],
                               key=lambda x: x.encode()),
           "partial": [u_lib["unitId"]],
           "none": [u_lib["unitId"]]}[selection]
    own = {"schemaVersion": 1,
           "enumeration": "partial" if selection == "partial" else "complete",
           "units": units, "selectedUnitIds": sorted(sel, key=lambda x: x.encode()),
           "ownership": ownership}
    own_h = fx.hid("native.source-unit-ownership.v1", own, "native",
                   "#/$defs/SourceUnitOwnershipV1", "source-unit-ownership")

    # ---- rust-cargo-prepared: an admitted PreparedOutputSetV3 of INERT rows ---
    prep_h = owner_digest = None
    toolchain_rec = {"rustCommitHash": RUST_COMMIT, "rustcVersion": RUSTC_VERSION,
                     "cargoVersion": RUSTC_VERSION,
                     "sysrootDigest": raw_sha256(b"#sysroot manifest\n"),
                     "rustcDevLlvmDigest": llvm_cid.split(":")[1],
                     "standardLibraryComponentDigests": [], "targetTriple": TRIPLE}
    if prepared:
        directives = b"cargo:rustc-cfg=have_feature\n"
        genfile = b"pub const GENERATED: u32 = 1;\n"
        fx.s.put_raw(directives, "prepared build-script directives")
        fx.s.put_raw(genfile, "prepared generated file")
        owner_manifest = C([{"path": "build.rs", "contentSha256": raw_sha256(b"fn main(){}\n"),
                             "byteLength": 12}])
        owner_digest = fx.s.put_raw(owner_manifest, "owner file manifest (security)")
        binding = {"ownerFileManifestSha256": owner_digest,
                   "dependencySourceSetId": "sha256:" + dss_h,
                   "toolchainDigest": raw_sha256(C(toolchain_rec)),
                   "cfgSetId": "primary"}
        fx.s.put_raw(C(toolchain_rec), "preparing ToolchainIdentityV1")
        prep = {"schemaVersion": 3,
                "preparation": {"kind": "authorized-execution",
                                "authorizationId": "sha256:" + "3" * 64,
                                "importId": None, "toolchain": toolchain_rec,
                                "dependencySourceSetId": "sha256:" + dss_h,
                                "cfgSetId": "primary",
                                "producer": {"id": "opensip-native-prepare",
                                             "version": "1.0.0"}},
                "rows": [
                    {"kind": "build-script-directives", "ownerKey": "cb-core 0.1.0",
                     "configuration": ["primary"], "site": None, "generated": None,
                     "inputBinding": binding,
                     "blob": {"sha256": raw_sha256(directives),
                              "byteLength": len(directives),
                              "mediaType": "text/x-cargo-directives"},
                     "status": "ok", "failureDetail": None},
                    {"kind": "generated-file", "ownerKey": "cb-core 0.1.0",
                     "configuration": ["primary"], "site": None,
                     "generated": {"logicalPath": "generated.rs",
                                   "blob": {"sha256": raw_sha256(genfile),
                                            "byteLength": len(genfile),
                                            "mediaType": "text/x-rust-source"}},
                     "inputBinding": binding,
                     "blob": {"sha256": raw_sha256(genfile),
                              "byteLength": len(genfile),
                              "mediaType": "text/x-rust-source"},
                     "status": "ok", "failureDetail": None}]}
        if m.get("non_inert_row"):
            prep["rows"][0]["kind"] = "proc-macro-dylib"
            prep["rows"][0]["blob"]["mediaType"] = "text/x-cargo-directives"
        prep_h = fx.hid("native.prepared-output-set.v3", prep, "native",
                        "#/$defs/PreparedOutputSetV3", "prepared-output-set")

    ctx = {"schemaVersion": 2, "targetTriple": TRIPLE, "hostTriple": TRIPLE,
           "toolchain": {"rustCommitHash": RUST_COMMIT, "rustcVersion": RUSTC_VERSION,
                         "cargoVersion": RUSTC_VERSION,
                         "sysrootDigest": raw_sha256(b"#sysroot manifest\n"),
                         "rustcDevLlvmDigest": llvm_cid.split(":")[1],
                         "standardLibraryComponentDigests": [],
                         "targetTriple": TRIPLE},
           "toolClosure": {"rustc": tool_members["bin/rustc"],
                           "cargo": tool_members["bin/cargo"],
                           "linker": tool_members["bin/ld"],
                           "ar": tool_members["bin/ar"],
                           "procMacroServer": tool_members["bin/proc-macro-srv"],
                           "closureId": tool_cid},
           "baseCfg": ["target_os=\"linux\""], "resolverVersion": 2,
           "dependencySourceSetId": "sha256:" + dss_h,
           "unifiedFeaturesId": "sha256:" + uf_h,
           "preparedOutputSetId": ("sha256:" + prep_h) if prepared else None,
           "configProjection": cfgproj}
    fx.s.put_raw(b"#sysroot manifest\n", "sysroot manifest")
    if m.get("cfgset_drops_base"):
        pass

    uni = {"schemaVersion": 2, "edition": dict(LARGE_EDITIONS),
           "lockfileIdentity": lockid,
           "dependencySourceSetId": "sha256:" + dss_h,
           "unifiedFeaturesId": "sha256:" + uf_h,
           "nativeContextId": None,
           "cfgSets": [{"cfgSetId": "primary", "cfg": ["target_os=\"linux\""]},
                       {"cfgSetId": "primary+test",
                        "cfg": ["target_os=\"linux\"", "test"]}],
           "rustflags": cfgproj["rustflags"],
           "crateRootPaths": sorted(["crates/core/src/lib.rs",
                                     "crates/legacy/src/lib.rs",
                                     "crates/tools#gen/src/main.rs"],
                                    key=lambda x: x.encode()),
           "configProjectionSha256": cfgproj_h,
           "executionCapableResolution": bool(prepared),
           "preparedOutputSetId": ("sha256:" + prep_h) if prepared else None,
           "preparedResolution": ("imported-inert" if (prepared and m.get("imported_inert")) else ("host-prepared" if prepared else "none")),
           "sourceUnitOwnershipId": None if selection == "none" else "sha256:" + own_h}
    if m.get("cfgset_drops_base"):
        uni["cfgSets"][1]["cfg"] = ["test"]
    if m.get("crate_root_outside_snapshot"):
        uni["crateRootPaths"] = sorted(uni["crateRootPaths"] + ["crates/ghost/src/lib.rs"],
                                       key=lambda x: x.encode())

    A = assemble.Assembly(
        fx, capabilities=["inventory", "clones-fact", "unresolved-edge"],
        spec_rows=[{"capabilityId": c,
                    "languageMode": "rust-cargo-prepared" if prepared else "rust-cargo",
                    "workspaceRoot": ".", "required": True}
                   for c in ("inventory", "clones-fact", "unresolved-edge")],
        grant_ops=((("read-source", "native-analysis", "read-import")
                    if m.get("imported_inert")
                    else ("read-source", "native-analysis", "prepare-code"))
                   if prepared else ("read-source", "native-analysis")),
        capability_manifest=CAP_MANIFEST)
    if prepared and m.get("imported_inert") and m.get("false_repo_principal"):
        oss = [{"ownerKey": "cb-core 0.1.0", "source": "snapshot-member",
                "ownerFileManifestSha256": owner_digest}]
        oss_digest = fx.rec(oss, "identity", "#/$defs/owner-source-set",
                            "owner-source-set")
        A.extra_principal = {"kind": "trusted-repository-code",
                             "closureId": tool_cid,
                             "ownerSourceDigest": oss_digest}
    if prepared and not m.get("imported_inert"):
        # the semantic-grant projection of native section 5.1 / S10: a
        # trusted-repository-code principal with its admitted owner-source digest.
        # The OPERATIONAL authorizationRef stays outside the Plan descriptor.
        oss = [{"ownerKey": "cb-core 0.1.0", "source": "snapshot-member",
                "ownerFileManifestSha256": owner_digest}]
        oss_digest = fx.rec(oss, "identity", "#/$defs/owner-source-set",
                            "owner-source-set")
        A.extra_principal = {"kind": "trusted-repository-code",
                             "closureId": tool_cid,
                             "ownerSourceDigest": oss_digest}
    ctx_hex = A.add_context("native.context.rust.v2", ctx, "#/$defs/NativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.rust.v2", uni,
                             "#/$defs/RustUniverseV2ResolvedInputs", "rust-universe")
    A.seal_snapshot()
    A.seal_plan([prov_cid, eval_cid, tool_cid, llvm_cid])

    lvb = CL.DOMAIN_SETS["native-semantic-universe"][
        "native.semantic-universe.rust.v2"]["languageVersionBinding"]

    # ---- a clones fact only where a dialect is selectable -----------------
    body_id = None
    blv = None
    clone_facts = []
    dialect_ok = selection in ("lib", "test2024", "lib+bin")
    if dialect_ok:
        c = CL.Closure(fx.s)
        blv, cause = CL.derive_body_language_version(
            lvb, ctx, uni, "crates/core/src/shared.rs", c)
        assert blv is not None, cause
        spec = ("opensip.normalisation-level-specification\nlevel=L0-verbatim\n"
                "rust-lexical-boundaries=v1\n").encode()
        lvhex = fx.s.put_raw(spec, "level-spec")
        src = fx.files["crates/core/src/shared.rs"]
        start = src.index(SHARED_BODY)
        end = start + len(SHARED_BODY)
        body_id, frame = osip.body_identity("L0-verbatim", lvhex, blv["languageId"],
                                            blv, osip.l0_payload(src[start:end]))
        fx.s.blobs[body_id.split(":")[1]] = frame
        clone_facts.append(A.add_fact(
            "clones", "normalized-body-hash", uni_hex, uni_hex, prov_cid,
            {"bodyIdentity": body_id, "normalisationLevel": "L0-verbatim",
             "normalisationVersion": lvhex},
            [{"path": "crates/core/src/shared.rs",
              "blobDigest": inv["crates/core/src/shared.rs"]["sha256"],
              "startByte": start, "endByte": end}]))

    file_facts = []
    for p, r in sorted(inv.items()):
        file_facts.append(A.add_fact(
            "file", "enumerated", uni_hex, uni_hex, prov_cid,
            {"path": p, "contentSha256": r["sha256"], "byteLength": r["bytes"]}, []))

    all_paths = sorted(inv)
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 all_paths)
    c_file = A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(all_paths), "complete"))

    s_cl, h_cl = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                             prov_cid, ["crates/core/src/shared.rs"])
    if dialect_ok:
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "complete")
    else:
        cause_map = {"ambiguous": "body-language-owner-ambiguous",
                     "partial": "body-language-owner-unenumerated",
                     "none": "body-language-ownership-missing"}
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "unknown",
                                  deficiency="input-closure-incomplete",
                                  cause=cause_map[selection])
    if m.get("false_complete_under_partial_ownership"):
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "complete")
    if m.get("undisclosed_null_deficiency"):
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "unknown")
    if m.get("wrong_cause"):
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "unknown",
                                  deficiency="input-closure-incomplete",
                                  cause="lockfile-missing")
    if m.get("unrelated_budget_deficiency"):
        cl_entry = coverage_entry("clones", "normalized-body-hash",
                                  "sha256:" + h_cl, 1, "unknown",
                                  deficiency="budget-exhausted",
                                  stage_terminal="budget-exhausted")
    c_cl = A.add_coverage(s_cl, h_cl, cl_entry)

    s_ue, h_ue = A.add_scope("unresolved-edge", "observed", uni_hex, uni_hex,
                             prov_cid, [])
    c_ue = A.add_coverage(s_ue, h_ue, coverage_entry(
        "unresolved-edge", "observed", "sha256:" + h_ue, 0, "complete"))

    view = A.seal_view(prov_cid, [s_file, s_cl, s_ue],
                       file_facts + clone_facts, [c_file, c_cl, c_ue],
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST])
    run_id = A.seal_run(eval_cid, prov_cid, [view])
    A.extra = {"bodyIdentity": body_id, "bodyLanguageVersion": blv,
               "universeHex": uni_hex, "contextHex": ctx_hex,
               "ownershipHex": own_h, "selection": selection,
               "editionMapSize": len(LARGE_EDITIONS),
               "unitIds": {"lib": u_lib["unitId"], "test2024": u_test["unitId"],
                           "bin": u_bin["unitId"]}}
    return fx, A, run_id
