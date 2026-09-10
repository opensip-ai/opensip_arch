"""Rust, syntax-only, ownership-deficiency, and JS-body graphs."""
from __future__ import annotations

from . import capability as cap
from .codec import (
    body_identity,
    body_identity_frame,
    body_language_id_for_variant,
    body_language_version_record,
    canonical_digest,
    framed_token_stream,
    h_hex,
    l0_payload,
    language_version_bytes,
    sha256,
    sort_canonical_set,
    sort_utf8,
    ts_source_variant,
)
from .graphs import (
    ENUM_DOC,
    Graph,
    NAT_DOC,
    REL_DOC,
    _assemble_v2,
    build_policy,
    file_coverage_entry,
    mk_closure,
    mk_config,
    mk_scope_descriptor,
    ts_config_projection,
    unit_membership_ts,
)
from .schema_val import validate_def


def rust_mixed_graph(*, ownership="complete", select="lib-bin", large_edition=False) -> dict:
    g = Graph(f"rust-{ownership}-{select}")
    lib_rs = b"pub fn f(){ let x = 1; }\n"
    bin_rs = b"fn main(){ println!(\"hi\"); }\n"
    shared = b"pub fn shared() {}\n"
    cargo_root = b'[workspace]\nmembers=["alpha","beta"]\n'
    cargo_a = b'[package]\nname="alpha"\nedition="2021"\n[lib]\npath="src/lib.rs"\n[[bin]]\nname="alpha-bin"\npath="src/bin.rs"\nedition="2024"\n'
    cargo_b = b'[package]\nname="beta"\nedition="2018"\n'
    lock = b'# cargo lock\n'
    files = {
        "Cargo.toml": cargo_root,
        "alpha/Cargo.toml": cargo_a,
        "alpha/src/lib.rs": lib_rs,
        "alpha/src/bin.rs": bin_rs,
        "alpha/src/shared.rs": shared,
        "beta/Cargo.toml": cargo_b,
        "beta/src/lib.rs": b"pub fn g(){}\n",
        "crates/foo#bar/Cargo.toml": b'[package]\nname="hashy"\nedition="2021"\n',
        "crates/foo#bar/src/lib.rs": b"pub fn h(){}\n",
        "Cargo.lock": lock,
    }
    inv = [g.blob(p, d) for p, d in sorted(files.items())]
    inv.sort(key=lambda r: r["path"].encode())

    provider = mk_closure(g, kind="provider", name="rust-provider", protocol_major=3, files={"bin/rustc-prov": b"p"})
    toolchain = mk_closure(g, kind="toolchain", name="rust-toolchain", protocol_major=0, files={
        "bin/rustc": b"rustc",
        "bin/cargo": b"cargo",
        "bin/proc": b"proc",
    })
    llvm = mk_closure(g, kind="rust-dev-llvm", name="llvm", protocol_major=0, files={"lib/LLVM": b"llvm"})
    stdlib = mk_closure(g, kind="stdlib", name="rust-std", protocol_major=0, files={"lib/libcore.rlib": b"core"})
    evaluator = mk_closure(g, kind="evaluator", name="evaluator", protocol_major=0, files={"bin/ev": b"e"})
    detector = mk_closure(g, kind="detector", name="detector", protocol_major=0, files={"bin/det": b"d"})

    # compilation units
    def unit(marker, kind, name):
        ident = {
            "schemaVersion": 1,
            "markerPath": marker,
            "targetKind": kind,
            "targetName": name,
        }
        uid = "sha256:" + h_hex("native.compilation-unit.v1", ident)
        return ident, uid

    u_lib, id_lib = unit("alpha/Cargo.toml", "lib", "alpha")
    u_bin, id_bin = unit("alpha/Cargo.toml", "bin", "alpha-bin")
    u_beta, id_beta = unit("beta/Cargo.toml", "lib", "beta")
    u_hash, id_hash = unit("crates/foo#bar/Cargo.toml", "lib", "hashy")

    units = [
        {"unitId": id_lib, "markerPath": "alpha/Cargo.toml", "crateName": "alpha", "targetKind": "lib", "targetName": "alpha", "targetEdition": 2021},
        {"unitId": id_bin, "markerPath": "alpha/Cargo.toml", "crateName": "alpha", "targetKind": "bin", "targetName": "alpha-bin", "targetEdition": 2024},
        {"unitId": id_beta, "markerPath": "beta/Cargo.toml", "crateName": "beta", "targetKind": "lib", "targetName": "beta", "targetEdition": 2018},
        {"unitId": id_hash, "markerPath": "crates/foo#bar/Cargo.toml", "crateName": "hashy", "targetKind": "lib", "targetName": "hashy", "targetEdition": 2021},
    ]
    units = sorted(units, key=lambda r: r["unitId"].encode())
    ownership_rows = [
        {"path": "alpha/src/lib.rs", "unitId": id_lib},
        {"path": "alpha/src/shared.rs", "unitId": id_lib},
        {"path": "alpha/src/shared.rs", "unitId": id_bin},  # same physical file, two targets
        {"path": "alpha/src/bin.rs", "unitId": id_bin},
        {"path": "beta/src/lib.rs", "unitId": id_beta},
        {"path": "crates/foo#bar/src/lib.rs", "unitId": id_hash},
    ]
    ownership_rows = sorted(ownership_rows, key=lambda r: (r["path"].encode(), r["unitId"].encode()))
    if select == "lib-bin":
        selected = sort_utf8([id_lib, id_bin, id_beta, id_hash])
    elif select == "lib-only":
        selected = sort_utf8([id_lib])
    else:
        selected = sort_utf8([id_lib, id_bin])
    own = {
        "schemaVersion": 1,
        "enumeration": "complete" if ownership == "complete" else "partial",
        "units": units,
        "selectedUnitIds": selected,
        "ownership": ownership_rows,
    }
    g.v(own, NAT_DOC, "SourceUnitOwnershipV1", "ownership")
    own_row_hex = h_hex("native.source-unit-ownership.v1", own)
    g.store.put_canonical("native.source-unit-ownership.v1", own)

    # empty deps
    dep_manifest = []
    dep_man_hex = h_hex("native.dependency-file-manifest.v1", dep_manifest)
    g.store.put_canonical("native.dependency-file-manifest.v1", dep_manifest)
    dep_set = {
        "schemaVersion": 1,
        "language": "rust",
        "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha256(lock), "lockfileVersion": 3},
        "packages": [],
        "completeness": {"state": "complete", "missing": []},
    }
    g.v(dep_set, NAT_DOC, "DependencySourceSetV1", "depset")
    dep_hex = h_hex("native.dependency-source-set.v1", dep_set)
    g.store.put_canonical("native.dependency-source-set.v1", dep_set)

    features = {
        "schemaVersion": 1,
        "resolverVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "activated": [],
        "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "cargo-1.87.0"},
    }
    g.v(features, NAT_DOC, "UnifiedFeaturesV1", "features")
    feat_hex = h_hex("native.unified-features.rust.v1", features)
    g.store.put_canonical("native.unified-features.rust.v1", features)

    cargo_proj = {
        "schemaVersion": 2,
        "honoredKeys": [],
        "strippedKeys": [],
        "replacedSnapshotConfigs": [],
        "rustflags": {"honored": [], "stripped": [], "executableSelected": False},
        "ancestorCarrierVerified": True,
        "cargoHome": "private-empty",
        "environmentProjection": "none",
        "claimsCargoSwitch": False,
        "projectionSha256": sha256(b""),
    }
    g.v(cargo_proj, NAT_DOC, "CargoConfigProjectionV2", "cargo-proj")
    cargo_hex = h_hex("native.cargo-config-projection.v2", cargo_proj)
    g.store.put_canonical("native.cargo-config-projection.v2", cargo_proj)

    ctx = {
        "schemaVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "a" * 40,
            "rustcVersion": "1.87.0",
            "cargoVersion": "1.87.0",
            "sysrootDigest": stdlib["tree"][0]["sha256"],
            "rustcDevLlvmDigest": llvm["hex"],
            "standardLibraryComponentDigests": [{"component": "core", "sha256": stdlib["tree"][0]["sha256"]}],
            "targetTriple": "aarch64-apple-darwin",
        },
        "toolClosure": {
            "rustc": toolchain["tree"][0]["sha256"],
            "cargo": toolchain["tree"][1]["sha256"],
            "linker": None,
            "ar": None,
            "procMacroServer": toolchain["tree"][2]["sha256"],
            "closureId": toolchain["id"],
        },
        "baseCfg": ["unix", "target_os=\"macos\""],
        "resolverVersion": 2,
        "dependencySourceSetId": "sha256:" + dep_hex,
        "unifiedFeaturesId": "sha256:" + feat_hex,
        "preparedOutputSetId": None,
        "configProjection": cargo_proj,
    }
    g.v(ctx, NAT_DOC, "NativeContextV2", "rust-context")
    ctx_hex = h_hex("native.context.rust.v2", ctx)
    g.store.put_canonical("native.context.rust.v2", ctx)

    edition_map = {"alpha": 2021, "beta": 2018, "hashy": 2021}
    if large_edition:
        for i in range(21):
            edition_map[f"crate{i:02d}"] = 2021 if i % 2 == 0 else 2018
    uni = {
        "schemaVersion": 2,
        "edition": edition_map,
        "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": sha256(lock), "lockfileVersion": 3},
        "dependencySourceSetId": "sha256:" + dep_hex,
        "unifiedFeaturesId": "sha256:" + feat_hex,
        "nativeContextId": "sha256:" + ctx_hex,
        "cfgSets": [{"cfgSetId": "default", "cfg": ["unix"]}],
        "rustflags": {"honored": [], "stripped": [], "executableSelected": False},
        "crateRootPaths": sort_utf8(["alpha", "beta", "crates/foo#bar"]),
        "configProjectionSha256": cargo_hex,
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
        "preparedResolution": "none",
        "sourceUnitOwnershipId": "sha256:" + own_row_hex,
    }
    g.v(uni, NAT_DOC, "RustUniverseV2ResolvedInputs", "rust-universe")
    uni_hex = h_hex("native.semantic-universe.rust.v2", uni)
    g.store.put_canonical("native.semantic-universe.rust.v2", uni)

    man = cap.minimal_manifest(
        profile="default",
        providers=[
            {
                "providerId": "rust-semantic",
                "language": "rust",
                "providerVersionSource": "closure",
                "toolchainIdentitySource": "closure",
                "relations": {"file": "enumerated", "clones": "normalized-body-hash"},
                "platformIds": ["macos-aarch64"],
            }
        ],
    )
    adm = cap.admit_capability_manifest(man)
    assert adm["admitted"], adm
    g.store.put_raw("capability-manifest", adm["committedBytes"])

    level_spec = b"L0 rust body spec\n"
    level_ver = __import__("hashlib").sha256(level_spec).digest()
    g.store.put_blob(level_spec)

    facts = []
    for p, d in files.items():
        facts.append(
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "relation": "file",
                "resolution": "enumerated",
                "sourceUniverse": uni_hex,
                "targetUniverse": uni_hex,
                "producerClosure": provider["id"],
                "payloadSchemaDigest": g.rel_schema_digest,
                "payloadDigest": "pending",
                "anchors": [{"path": p, "blobDigest": sha256(d), "startByte": 0, "endByte": len(d)}],
                "confidenceMillionths": 1000000,
                "_payload": {"path": p, "contentSha256": sha256(d), "byteLength": len(d)},
            }
        )

    clone_subjects = ["alpha/src/lib.rs", "alpha/src/bin.rs", "alpha/src/shared.rs"]
    if ownership == "complete" and select != "lib-only":
        # mint clones only when dialect selectable: shared.rs has two selected owners 2021 vs 2024 → ambiguous
        # lib.rs only lib 2021; bin.rs only bin 2024
        for path, data, edition, lang_path in [
            ("alpha/src/lib.rs", lib_rs, 2021, "lib"),
            ("alpha/src/bin.rs", bin_rs, 2024, "bin"),
        ]:
            blv = body_language_version_record(
                language_id="rust",
                compiler_name="rustc",
                compiler_version="1.87.0",
                compiler_build="a" * 40,
                dialect={"edition": edition},
            )
            lv = language_version_bytes(blv)
            g.rec(f"blv-{lang_path}", blv)
            frame = body_identity_frame(
                level_id="L0-verbatim",
                level_version=level_ver,
                language_id="rust",
                language_version=lv,
                payload=l0_payload(data),
            )
            bid = body_identity(frame)
            g.store.put_raw(f"body-frame:{bid}", frame)
            facts.append(
                {
                    "schemaVersion": 2,
                    "snapshotId": "pending",
                    "relation": "clones",
                    "resolution": "normalized-body-hash",
                    "sourceUniverse": uni_hex,
                    "targetUniverse": uni_hex,
                    "producerClosure": provider["id"],
                    "payloadSchemaDigest": g.rel_schema_digest,
                    "payloadDigest": "pending",
                    "anchors": [{"path": path, "blobDigest": sha256(data), "startByte": 0, "endByte": len(data)}],
                    "confidenceMillionths": 1000000,
                    "_payload": {
                        "bodyIdentity": bid,
                        "normalisationLevel": "L0-verbatim",
                        "normalisationVersion": sha256(level_spec),
                    },
                }
            )

    # clone coverage pairing
    if ownership == "partial":
        clone_cov = file_coverage_entry(
            "clones",
            "normalized-body-hash",
            "0" * 64,
            uni_hex,
            0,
            coverage="unknown",
            deficiency="input-closure-incomplete",
            native_cause="body-language-owner-unenumerated",
            exhaustive=False,
        )
        clone_subjects = []
    elif select == "lib-only":
        # empty clone view: selected lib only, shared also owned by unselected bin — complete empty lawful for unselected
        clone_cov = file_coverage_entry("clones", "normalized-body-hash", "0" * 64, uni_hex, 1)
        clone_subjects = ["alpha/src/lib.rs"]
    else:
        clone_cov = file_coverage_entry("clones", "normalized-body-hash", "0" * 64, uni_hex, 2)

    file_subjects = sort_utf8(list(files))
    membership = {
        "schemaVersion": 1,
        "units": [
            {
                "unitOrdinal": 0,
                "rootPath": ".",
                "languageFamily": "rust",
                "languageMode": "rust-cargo",
                "unitKind": "cargo-workspace",
                "markerPath": "Cargo.toml",
                "markerSha256": sha256(cargo_root),
                "recognizerId": "cargo-workspace",
                "recognizerVersion": 1,
                "provenance": "DISCOVERED",
                "memberPackageRoots": ["alpha", "beta", "crates/foo#bar"],
            }
        ],
        "rows": [],
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }
    g.rec("unit-membership", membership)

    pieces = {
        "policy_bundle": build_policy("file.inventoried", "rust", "file", "enumerated", emit_op="exists", gate=False, severity="note"),
        "enum_plan": {
            "schemaVersion": 1,
            "snapshotId": "snapshot2:" + "0" * 64,
            "scopeDigest": canonical_digest(mk_scope_descriptor()),
            "membershipDigest": canonical_digest(membership),
            "cells": [
                {
                    "capabilityId": "inventory",
                    "languageMode": "rust-cargo",
                    "workspaceRoot": ".",
                    "required": True,
                    "kinds": ["file"],
                    "programBindings": [
                        {
                            "ordinal": 0,
                            "provenance": "default-unit",
                            "enumerator": {"status": "selected", "closureId": provider["id"]},
                            "nativeContextDigest": ctx_hex,
                            "universe": uni_hex,
                            "programEntry": None,
                            "extents": [{"kind": "file", "paths": file_subjects}],
                        }
                    ],
                }
            ],
        },
        "emission": {
            "schemaVersion": 1,
            "policyDigest": "pending",
            "rules": [
                {
                    "ruleId": "file.inventoried",
                    "contributionId": "contrib-file-inventoried",
                    "ruleStableId": "file.inventoried",
                    "semanticsMajor": 1,
                    "detectorClosure": detector["id"],
                    "stabilityClass": "path-stable",
                    "emissionProfile": "declarative-subject-v1",
                }
            ],
        },
        "analysis_spec": {
            "requestedCapabilities": sort_canonical_set(
                [
                    {"capabilityId": "inventory", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True},
                    {"capabilityId": "clones-fact", "languageMode": "rust-cargo", "workspaceRoot": ".", "required": True},
                ]
            )
        },
        "scope_desc": mk_scope_descriptor(),
        "config": mk_config("default", ["inventory", "clones-fact"]),
        "grant": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "principals": [{"kind": "first-party", "closureId": provider["id"], "ownerSourceDigest": None}],
            "analysisOperations": sort_utf8(["native-analysis", "read-source"]),
            "scopeDigest": "pending",
        },
        "vcs": {
            "schemaVersion": 2,
            "kind": "none",
            "commitId": None,
            "dirty": False,
            "sourceInventoryDigest": canonical_digest(inv),
        },
        "snapshot": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "sourceInventory": inv,
            "resolvedConfigDigest": "pending",
            "scopeDigest": "pending",
            "vcsDigest": "pending",
        },
        "plan": {
            "schemaVersion": 2,
            "snapshotId": "pending",
            "capabilityManifestId": adm["capabilityManifestId"],
            "semanticClosures": sort_utf8([provider["id"], evaluator["id"], detector["id"], toolchain["id"], llvm["id"], stdlib["id"]]),
            "analysisSpecDigest": "pending",
            "resolvedConfigDigest": "pending",
            "nativeContextDigests": [ctx_hex],
            "importIds": [],
            "policyDigest": "pending",
            "waiverDigest": "pending",
            "scopeDigest": "pending",
            "budget": {"unit": "work-units", "limit": 10_000_000},
            "semanticGrantDigest": "pending",
            "capabilityManifestBytesDigest": adm["capabilityManifestBytesDigest"],
        },
        "inventories": [
            {
                "schemaVersion": 1,
                "planId": "plan2:" + "0" * 64,
                "parameterDigest": "0" * 64,
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "kind": "file",
                "state": "complete",
                "deficiency": None,
                "nativeCause": None,
                "examinedPaths": file_subjects,
                "rows": [
                    {
                        "nativeSubjectId": p,
                        "kind": "file",
                        "path": p,
                        "qualifiedName": p,
                        "subjectLanguage": "rust" if p.endswith(".rs") else "toml" if p.endswith(".toml") else "unspecified",
                        "signatureTokens": [],
                        "projections": [],
                    }
                    for p in file_subjects
                ],
            }
        ],
        "scopes": [
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "sourceUniverse": uni_hex,
                "targetUniverse": uni_hex,
                "relation": "file",
                "resolution": "enumerated",
                "enumeratorClosure": provider["id"],
                "subjects": file_subjects,
            },
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "sourceUniverse": uni_hex,
                "targetUniverse": uni_hex,
                "relation": "clones",
                "resolution": "normalized-body-hash",
                "enumeratorClosure": provider["id"],
                "subjects": clone_subjects,
            },
        ],
        "facts": facts,
        "payload_def_for": {"file": "FilePayloadV1", "clones": "ClonesPayloadV1"},
        "coverages": [
            {"_match": ("file", "enumerated"), "_payload": file_coverage_entry("file", "enumerated", "0" * 64, uni_hex, len(file_subjects))},
            {"_match": ("clones", "normalized-body-hash"), "_payload": clone_cov},
        ],
        "provider_closure_id": provider["id"],
        "evaluator_closure_id": evaluator["id"],
        "detector_closure_id": detector["id"],
        "universe_hex": uni_hex,
        "universe_token": "rust",
        "context_hex": ctx_hex,
        "language_mode": "rust-cargo",
        "primary_capability": "inventory",
        "context_domain": "native.context.rust.v2",
        "universe_domain": "native.semantic-universe.rust.v2",
        "ownership": own,
        "notes": {
            "hashMarkerDir": "crates/foo#bar",
            "sharedFileTwoEditions": "alpha/src/shared.rs",
            "targetEditionVsPackage": {"lib": 2021, "bin": 2024, "packageDefault": 2021},
            "enumeration": ownership,
            "selection": selected,
        },
    }
    g.rec("source-inventory", inv)
    out = _assemble_v2(g, pieces)
    out["notes"] = pieces["notes"]
    out["bodyIdentities"] = [f["_payload"]["bodyIdentity"] for f in facts if f["relation"] == "clones"]
    return out


def syntax_graph(*, grammar="typescript", extra_json=False, request_clones=True) -> dict:
    g = Graph(f"syntax-{grammar}")
    if grammar == "typescript":
        files = {"src/a.ts": b"const a = 1;\n", "README.md": b"# demo\n"}
        lang = "typescript"
        suffixes = [".cts", ".mts", ".ts", ".tsx"]
        syn_class = "code"
        mode_caps = ["file@enumerated", "declares@syntactic", "clones@normalized-body-hash"]
    elif grammar == "json":
        files = {"data/config.json": b'{"a":1}\n', "README.md": b"# data\n"}
        lang = "json"
        suffixes = [".json"]
        syn_class = "data-document"
        mode_caps = ["file@enumerated"]
    else:
        raise ValueError(grammar)
    inv = [g.blob(p, d) for p, d in sorted(files.items())]
    inv.sort(key=lambda r: r["path"].encode())

    provider = mk_closure(g, kind="provider", name="syntax-provider", protocol_major=0, files={"bin/syn": b"s"})
    grammar_c = mk_closure(g, kind="grammar", name="grammar-bundle", protocol_major=0, files={"grammars/ts.json": b"{}"})
    evaluator = mk_closure(g, kind="evaluator", name="evaluator", protocol_major=0, files={"bin/ev": b"e"})
    detector = mk_closure(g, kind="detector", name="detector", protocol_major=0, files={"bin/det": b"d"})

    gdef = b"grammar-bytes"
    ndef = b"normalizer-spec"
    bundle = {
        "schemaVersion": 1,
        "closureId": grammar_c["id"],
        "parserName": "opensip-syntax",
        "parserVersion": "1.0.0",
        "bundleDigest": sha256(gdef),
        "grammars": [
            {
                "grammarId": f"{lang}-v1",
                "grammarVersion": "1",
                "languageId": lang,
                "suffixes": sort_utf8(suffixes),
                "syntaxClass": syn_class,
                "grammarDigest": sha256(gdef),
            }
        ],
        "normalizer": {
            "normalizerId": "opensip-norm",
            "normalizerVersion": "1",
            "specificationDigest": sha256(ndef),
        },
    }
    g.store.put_blob(gdef)
    g.store.put_blob(ndef)
    g.v(bundle, NAT_DOC, "SyntaxGrammarBundleV1", "grammar-bundle")
    ctx = {"schemaVersion": 2, "grammarBundle": bundle}
    g.v(ctx, NAT_DOC, "SyntaxNativeContextV2", "syntax-context")
    ctx_hex = h_hex("native.context.syntax.v2", ctx)
    g.store.put_canonical("native.context.syntax.v2", ctx)
    uni = {
        "schemaVersion": 2,
        "nativeContextId": "sha256:" + ctx_hex,
        "selectedGrammarIds": [f"{lang}-v1"],
        "resolutionAttempted": False,
    }
    g.v(uni, NAT_DOC, "SyntaxUniverseV2ResolvedInputs", "syntax-universe")
    uni_hex = h_hex("native.semantic-universe.syntax.v2", uni)
    g.store.put_canonical("native.semantic-universe.syntax.v2", uni)

    man = cap.minimal_manifest(
        profile="default",
        providers=[
            {
                "providerId": "syntax-only",
                "language": "*",
                "providerVersionSource": "bundle",
                "toolchainIdentitySource": "bundle",
                "relations": {"file": "enumerated", "clones": "normalized-body-hash"} if syn_class == "code" else {"file": "enumerated"},
                "platformIds": ["macos-aarch64"],
            }
        ],
    )
    adm = cap.admit_capability_manifest(man)
    assert adm["admitted"], adm
    g.store.put_raw("capability-manifest", adm["committedBytes"])

    file_subjects = sort_utf8(list(files))
    facts = []
    for p, d in files.items():
        facts.append(
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "relation": "file",
                "resolution": "enumerated",
                "sourceUniverse": uni_hex,
                "targetUniverse": uni_hex,
                "producerClosure": provider["id"],
                "payloadSchemaDigest": g.rel_schema_digest,
                "payloadDigest": "pending",
                "anchors": [{"path": p, "blobDigest": sha256(d), "startByte": 0, "endByte": len(d)}],
                "confidenceMillionths": 1000000,
                "_payload": {"path": p, "contentSha256": sha256(d), "byteLength": len(d)},
            }
        )

    coverages = [
        {"_match": ("file", "enumerated"), "_payload": file_coverage_entry("file", "enumerated", "0" * 64, uni_hex, len(file_subjects))}
    ]
    scopes = [
        {
            "schemaVersion": 2,
            "snapshotId": "pending",
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "relation": "file",
            "resolution": "enumerated",
            "enumeratorClosure": provider["id"],
            "subjects": file_subjects,
        }
    ]
    if request_clones:
        scopes.append(
            {
                "schemaVersion": 2,
                "snapshotId": "pending",
                "sourceUniverse": uni_hex,
                "targetUniverse": uni_hex,
                "relation": "clones",
                "resolution": "normalized-body-hash",
                "enumeratorClosure": provider["id"],
                "subjects": [p for p in file_subjects if p.endswith(".ts") or p.endswith(".json")],
            }
        )
        if syn_class == "data-document":
            # must NOT claim complete empty clones
            coverages.append(
                {
                    "_match": ("clones", "normalized-body-hash"),
                    "_payload": file_coverage_entry(
                        "clones",
                        "normalized-body-hash",
                        "0" * 64,
                        uni_hex,
                        1,
                        coverage="unknown",
                        deficiency="language-tier-unsupported",
                        native_cause="capability-missing",
                    ),
                }
            )
        else:
            # code grammar: clones lawful; mint L0 for .ts
            ts_path, ts_data = "src/a.ts", files["src/a.ts"]
            blv = body_language_version_record(
                language_id="typescript",
                compiler_name="opensip-syntax",
                compiler_version="1.0.0",
                compiler_build=sha256(b"grammar"),
                dialect={"grammarVariant": "ts"},
            )
            lv = language_version_bytes(blv)
            g.rec("blv-syntax-ts", blv)
            level_spec = b"L0 syntax"
            frame = body_identity_frame(
                level_id="L0-verbatim",
                level_version=__import__("hashlib").sha256(level_spec).digest(),
                language_id="typescript",
                language_version=lv,
                payload=l0_payload(ts_data),
            )
            bid = body_identity(frame)
            g.store.put_raw(f"body-frame:{bid}", frame)
            g.store.put_blob(level_spec)
            facts.append(
                {
                    "schemaVersion": 2,
                    "snapshotId": "pending",
                    "relation": "clones",
                    "resolution": "normalized-body-hash",
                    "sourceUniverse": uni_hex,
                    "targetUniverse": uni_hex,
                    "producerClosure": provider["id"],
                    "payloadSchemaDigest": g.rel_schema_digest,
                    "payloadDigest": "pending",
                    "anchors": [{"path": ts_path, "blobDigest": sha256(ts_data), "startByte": 0, "endByte": len(ts_data)}],
                    "confidenceMillionths": 1000000,
                    "_payload": {
                        "bodyIdentity": bid,
                        "normalisationLevel": "L0-verbatim",
                        "normalisationVersion": sha256(level_spec),
                    },
                }
            )
            coverages.append(
                {
                    "_match": ("clones", "normalized-body-hash"),
                    "_payload": file_coverage_entry("clones", "normalized-body-hash", "0" * 64, uni_hex, 1),
                }
            )

    membership = {
        "schemaVersion": 1,
        "units": [
            {
                "unitOrdinal": 0,
                "rootPath": ".",
                "languageFamily": "none",
                "languageMode": "syntax-only",
                "unitKind": "syntax-only",
                "markerPath": file_subjects[0],
                "markerSha256": sha256(list(files.values())[0]),
                "recognizerId": "bundled-grammar",
                "recognizerVersion": 1,
                "provenance": "DISCOVERED",
                "memberPackageRoots": [],
            }
        ],
        "rows": [],
        "unsupportedFiles": [],
        "outsideBoundaryFiles": [],
        "erasedFiles": [],
    }

    pieces = {
        "policy_bundle": build_policy("file.inventoried", "syntax", "file", "enumerated", emit_op="exists", gate=False, severity="note"),
        "enum_plan": {
            "schemaVersion": 1,
            "snapshotId": "snapshot2:" + "0" * 64,
            "scopeDigest": canonical_digest(mk_scope_descriptor()),
            "membershipDigest": canonical_digest(membership),
            "cells": [
                {
                    "capabilityId": "inventory",
                    "languageMode": "syntax-only",
                    "workspaceRoot": ".",
                    "required": True,
                    "kinds": ["file"],
                    "programBindings": [
                        {
                            "ordinal": 0,
                            "provenance": "default-unit",
                            "enumerator": {"status": "selected", "closureId": provider["id"]},
                            "nativeContextDigest": ctx_hex,
                            "universe": uni_hex,
                            "programEntry": None,
                            "extents": [{"kind": "file", "paths": file_subjects}],
                        }
                    ],
                }
            ],
        },
        "emission": {
            "schemaVersion": 1,
            "policyDigest": "pending",
            "rules": [
                {
                    "ruleId": "file.inventoried",
                    "contributionId": "contrib-file-inventoried",
                    "ruleStableId": "file.inventoried",
                    "semanticsMajor": 1,
                    "detectorClosure": detector["id"],
                    "stabilityClass": "path-stable",
                    "emissionProfile": "declarative-subject-v1",
                }
            ],
        },
        "analysis_spec": {
            "requestedCapabilities": sort_canonical_set(
                [
                    {"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True},
                    {"capabilityId": "clones-fact", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True},
                ]
            )
        },
        "scope_desc": mk_scope_descriptor(),
        "config": mk_config("default", ["inventory", "clones-fact"]),
        "grant": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "principals": [{"kind": "first-party", "closureId": provider["id"], "ownerSourceDigest": None}],
            "analysisOperations": sort_utf8(["native-analysis", "read-source"]),
            "scopeDigest": "pending",
        },
        "vcs": {
            "schemaVersion": 2,
            "kind": "none",
            "commitId": None,
            "dirty": False,
            "sourceInventoryDigest": canonical_digest(inv),
        },
        "snapshot": {
            "schemaVersion": 2,
            "projectId": g.project_id,
            "sourceInventory": inv,
            "resolvedConfigDigest": "pending",
            "scopeDigest": "pending",
            "vcsDigest": "pending",
        },
        "plan": {
            "schemaVersion": 2,
            "snapshotId": "pending",
            "capabilityManifestId": adm["capabilityManifestId"],
            "semanticClosures": sort_utf8([provider["id"], evaluator["id"], detector["id"], grammar_c["id"]]),
            "analysisSpecDigest": "pending",
            "resolvedConfigDigest": "pending",
            "nativeContextDigests": [ctx_hex],
            "importIds": [],
            "policyDigest": "pending",
            "waiverDigest": "pending",
            "scopeDigest": "pending",
            "budget": {"unit": "work-units", "limit": 10_000_000},
            "semanticGrantDigest": "pending",
            "capabilityManifestBytesDigest": adm["capabilityManifestBytesDigest"],
        },
        "inventories": [
            {
                "schemaVersion": 1,
                "planId": "plan2:" + "0" * 64,
                "parameterDigest": "0" * 64,
                "cellOrdinal": 0,
                "programOrdinal": 0,
                "kind": "file",
                "state": "complete",
                "deficiency": None,
                "nativeCause": None,
                "examinedPaths": file_subjects,
                "rows": [
                    {
                        "nativeSubjectId": p,
                        "kind": "file",
                        "path": p,
                        "qualifiedName": p,
                        "subjectLanguage": lang if p.endswith(tuple(suffixes)) else "markdown" if p.endswith(".md") else "unspecified",
                        "signatureTokens": [],
                        "projections": [],
                    }
                    for p in file_subjects
                ],
            }
        ],
        "scopes": scopes,
        "facts": facts,
        "payload_def_for": {"file": "FilePayloadV1", "clones": "ClonesPayloadV1"},
        "coverages": coverages,
        "provider_closure_id": provider["id"],
        "evaluator_closure_id": evaluator["id"],
        "detector_closure_id": detector["id"],
        "universe_hex": uni_hex,
        "universe_token": "syntax",
        "context_hex": ctx_hex,
        "language_mode": "syntax-only",
        "primary_capability": "inventory",
        "context_domain": "native.context.syntax.v2",
        "universe_domain": "native.semantic-universe.syntax.v2",
        "coverage_applicability": "supported-available",
        "coverage_applicability_by_relation": (
            {"file": "supported-available", "clones": "unsupported-typed"}
            if syn_class == "data-document" and request_clones
            else {}
        ),
        "cell_deficiency": None,
        "cell_native_cause": None,
    }
    g.rec("source-inventory", inv)
    g.rec("unit-membership", membership)
    out = _assemble_v2(g, pieces)
    out["syntaxClass"] = syn_class
    out["grammar"] = grammar
    return out
