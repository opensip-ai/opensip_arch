"""Rust reconstruction vectors: mixed editions, target-level overrides, ownership
selection, ambiguity, partial enumeration, a `#` marker directory and a large map."""

from __future__ import annotations

import hashlib
import json

import opensip_ref as R
import closure as CL
import world as W
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes
from build_ts import L0_SPEC, L1_SPEC

RS_BODY = b"fn helper(x: u32) -> u32 {\n    x + 1\n}\n"

FILES = {
    "Cargo.lock": b'version = 3\n[[package]]\nname = "core"\nversion = "0.1.0"\n',
    "Cargo.toml": b'[workspace]\nmembers = ["crates/core","crates/legacy","tools/#gen"]\n',
    "crates/core/Cargo.toml": b'[package]\nname = "core"\nedition = "2021"\n',
    "crates/core/src/lib.rs": b"pub mod shared;\n" + RS_BODY,
    "crates/core/src/shared.rs": b"// shared\n" + RS_BODY,
    "crates/legacy/Cargo.toml": b'[package]\nname = "legacy"\nedition = "2015"\n',
    "crates/legacy/src/lib.rs": b"// legacy\n" + RS_BODY,
    "tools/#gen/Cargo.toml": b'[package]\nname = "gen"\nedition = "2024"\n',
    "tools/#gen/src/main.rs": b"fn main() {}\n" + RS_BODY,
    ".cargo/config.toml": b'[build]\nrustflags = ["--cfg","feature_x"]\n',
}

# A REPRESENTATIVE LARGE EDITION MAP: 21 crates, exactly the case identity section 3
# uses to show why the map cannot be embedded inside the inherited u8 component length.
LARGE_EDITION_MAP = {"core": 2021, "legacy": 2015, "gen": 2024}
for i in range(18):
    LARGE_EDITION_MAP["workspace_support_crate_%02d" % i] = 2021


def unit(marker, kind, name, crate, edition):
    uid = sha256_text("native.compilation-unit.v1",
                      {"schemaVersion": 1, "markerPath": marker,
                       "targetKind": kind, "targetName": name})
    return {"unitId": uid, "markerPath": marker, "crateName": crate,
            "targetKind": kind, "targetName": name, "targetEdition": edition}


U_LIB = unit("crates/core/Cargo.toml", "lib", "core", "core", None)          # package default 2021
U_TEST = unit("crates/core/Cargo.toml", "test", "shared_it", "core", 2018)   # TARGET OVERRIDE
U_LEGACY = unit("crates/legacy/Cargo.toml", "lib", "legacy", "legacy", None)  # 2015
U_GEN = unit("tools/#gen/Cargo.toml", "bin", "gen", "gen", None)              # 2024, '#' dir

ALL_UNITS = sorted([U_LIB, U_TEST, U_LEGACY, U_GEN],
                   key=lambda u: u["unitId"].encode("utf-8"))
OWNERSHIP = sorted(
    [
        {"path": "crates/core/src/lib.rs", "unitId": U_LIB["unitId"]},
        {"path": "crates/core/src/shared.rs", "unitId": U_LIB["unitId"]},
        {"path": "crates/core/src/shared.rs", "unitId": U_TEST["unitId"]},
        {"path": "crates/legacy/src/lib.rs", "unitId": U_LEGACY["unitId"]},
        {"path": "tools/#gen/src/main.rs", "unitId": U_GEN["unitId"]},
    ],
    key=lambda o: (o["path"].encode("utf-8"), o["unitId"].encode("utf-8")),
)


def ownership_record(selected, enumeration="complete", units=None, ownership=None):
    rec = {
        "schemaVersion": 1,
        "enumeration": enumeration,
        "units": units if units is not None else ALL_UNITS,
        "selectedUnitIds": sorted(selected, key=lambda s: s.encode("utf-8")),
        "ownership": ownership if ownership is not None else OWNERSHIP,
    }
    R.validate("native", "#/$defs/SourceUnitOwnershipV1", rec)
    return rec


def build(selected, *, enumeration="complete", ownership_null=False,
          units=None, ownership=None, edition_map=None, prepared=None):
    g = CL.Graph("rust")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]
    caps = ["inventory", "syntax", "imports", "references", "calls", "types",
            "reachability", "clones-fact", "clones-near", "unresolved-edge"]
    cfg = W.resolved_config(caps)
    sd = W.scope_descriptor(["."], excluded=[".git", "target"])
    W.build_snapshot(g, FILES, sd, cfg)

    # -- nested retained records ------------------------------------------
    dep_manifest = [
        {"path": "src/lib.rs", "contentSha256": raw_bytes(b"pub fn s(){}\n"), "byteLength": 13},
    ]
    g.cas.put_bytes(b"pub fn s(){}\n")
    R.validate("native", "#/$defs/DependencyFileManifestV1", dep_manifest)
    dep_manifest_id = g.add_nested("native.dependency-file-manifest.v1", dep_manifest)
    lock_id = {"path": "Cargo.lock", "contentSha256": g.inv_row("Cargo.lock")["sha256"],
               "lockfileVersion": 3}
    dss = {
        "schemaVersion": 1,
        "language": "rust",
        "lockfileIdentity": lock_id,
        "packages": [{
            "name": "serde", "version": "1.0.210", "sourceKind": "registry",
            "sourceId": "registry+https://github.com/rust-lang/crates.io-index",
            "lockChecksum": raw_bytes(b"tarball-bytes"),
            "fileManifestSha256": dep_manifest_id[len("sha256:"):],
            "fileCount": 1, "totalBytes": 13,
            "acquisition": {"mode": "imported-descriptor",
                            "descriptorId": "import2:" + "1" * 64, "vendorPath": None},
            "checksumVerification": "tarball-matched",
            "provenanceAssurance": "registry-authenticated",
        }],
        "completeness": {"state": "complete", "missing": []},
    }
    R.validate("native", "#/$defs/DependencySourceSetV1", dss)
    dss_id = g.add_nested("native.dependency-source-set.v1", dss)

    uf = {
        "schemaVersion": 1, "resolverVersion": 2, "targetTriple": "aarch64-apple-darwin",
        "activated": [{"packageKey": "serde 1.0.210", "features": ["std"]}],
        "computedBy": {"producer": "opensip-cargo-adapter", "producerBuildId": "adapter-1.0.0"},
    }
    R.validate("native", "#/$defs/UnifiedFeaturesV1", uf)
    uf_id = g.add_nested("native.unified-features.rust.v1", uf)

    projected_config = b'[build]\nrustflags = ["--cfg","feature_x"]\n'
    g.cas.put_bytes(projected_config)
    rustflags = {"honored": ["--cfg", "feature_x"],
                 "stripped": [{"flag": "-C linker=cc", "reason": "codegen-option-not-allowlisted"}],
                 "executableSelected": False}
    ccp = {
        "schemaVersion": 2,
        "honoredKeys": ["build.rustflags"],
        "strippedKeys": ["build.rustc", "target.aarch64-apple-darwin.linker"],
        "replacedSnapshotConfigs": [".cargo/config.toml"],
        "rustflags": rustflags,
        "ancestorCarrierVerified": True,
        "cargoHome": "private-empty",
        "environmentProjection": "none",
        "claimsCargoSwitch": False,
        "projectionSha256": raw_bytes(projected_config),
    }
    R.validate("native", "#/$defs/CargoConfigProjectionV2", ccp)
    ccp_id = g.add_nested("native.cargo-config-projection.v2", ccp)

    tool = g.closures[cl["rust-toolchain"]]
    dig = {b["path"]: b["sha256"] for b in tool["tree"]}
    stdlib_rows = []
    ctx = {
        "schemaVersion": 2,
        "targetTriple": "aarch64-apple-darwin",
        "hostTriple": "aarch64-apple-darwin",
        "toolchain": {
            "rustCommitHash": "9b" + "0" * 38,
            "rustcVersion": tool["semanticVersion"],
            "cargoVersion": tool["semanticVersion"],
            "sysrootDigest": raw_bytes(b"SYSROOT-TREE-MANIFEST"),
            "rustcDevLlvmDigest": cl["rust-dev-llvm"][len("closure2:"):],
            "standardLibraryComponentDigests": stdlib_rows,
            "targetTriple": "aarch64-apple-darwin",
        },
        "toolClosure": {"rustc": dig["bin/rustc"], "cargo": dig["bin/cargo"],
                        "linker": dig["bin/ld"], "ar": dig["bin/ar"],
                        "procMacroServer": dig["bin/proc-macro-srv"],
                        "closureId": cl["rust-toolchain"]},
        "baseCfg": ["target_arch=\"aarch64\"", "target_os=\"macos\""],
        "resolverVersion": 2,
        "dependencySourceSetId": dss_id,
        "unifiedFeaturesId": uf_id,
        "preparedOutputSetId": None,
        "configProjection": ccp,
    }
    g.cas.put_bytes(b"SYSROOT-TREE-MANIFEST")
    R.validate("native", "#/$defs/NativeContextV2", ctx)
    ctx_hex = g.add_context("native.context.rust.v2", ctx)

    own = None if ownership_null else ownership_record(
        selected, enumeration=enumeration, units=units, ownership=ownership)
    own_id = None if own is None else g.add_nested("native.source-unit-ownership.v1", own)

    u = {
        "schemaVersion": 2,
        "edition": edition_map if edition_map is not None else LARGE_EDITION_MAP,
        "lockfileIdentity": lock_id,
        "dependencySourceSetId": dss_id,
        "unifiedFeaturesId": uf_id,
        "nativeContextId": sha256_text("native.context.rust.v2", ctx),
        "cfgSets": [
            {"cfgSetId": "primary", "cfg": ctx["baseCfg"]},
            {"cfgSetId": "primary+test", "cfg": ctx["baseCfg"] + ["test"]},
        ],
        "rustflags": rustflags,
        "crateRootPaths": sorted(["crates/core/src/lib.rs", "crates/legacy/src/lib.rs",
                                  "tools/#gen/src/main.rs"], key=lambda p: p.encode("utf-8")),
        "configProjectionSha256": ccp_id[len("sha256:"):],
        "executionCapableResolution": False,
        "preparedOutputSetId": None,
        "preparedResolution": "none",
        "sourceUnitOwnershipId": own_id,
    }
    R.validate("native", "#/$defs/RustUniverseV2ResolvedInputs", u)
    uh = g.add_universe("native.semantic-universe.rust.v2", u)
    retained = {uh: {"dependencySourceSet": dss, "unifiedFeatures": uf,
                     "sourceUnitOwnership": own}}
    if own is None:
        del retained[uh]["sourceUnitOwnership"]

    manifest = W.capability_manifest("default", [], [])
    policy = W.simple_policy("rust-clone", "clones", "normalized-body-hash", op="none")
    g.rule_program = W.compile_program(policy)
    g.cas.put_record(g.rule_program)
    spec = W.analysis_spec([
        {"capabilityId": c, "languageMode": "rust-cargo", "workspaceRoot": ".",
         "required": True} for c in caps])
    grant = W.semantic_grant(["read-source", "native-analysis"], raw(sd))
    plan_id = W.build_plan(g, [cl["provider-rust"], cl["evaluator"]], [ctx_hex],
                           spec, grant, policy, W.EMPTY_WAIVERS, manifest)
    return g, cl, ctx, ctx_hex, u, uh, retained, plan_id, own


def rust_body(g, uh, retained, path, level=None, spec=None):
    data = g.blobs[path]
    start = data.index(RS_BODY)
    end = start + len(RS_BODY)
    level = level or "L0-verbatim"
    spec = spec or L0_SPEC
    bl = CL.body_language_version(g, uh, path, retained[uh])
    lv32 = R.language_version_raw32(bl)
    lev32 = hashlib.sha256(spec).digest()
    payload = R.body_payload_L0(data[start:end])
    pre, bid = R.body_identity(level, lev32, bl["languageId"], lv32, payload)
    g.cas.put_bytes(pre)
    g.cas.put_bytes(spec)
    return bid, bl, lev32.hex(), start, end


def _inventory_and_clones(g, cl, uh, retained, plan_id, clone_paths,
                          clone_entry=None):
    prov = cl["provider-rust"]
    subjects = [r["path"] for r in g.inventory]
    sid, sc = W.make_scope(g, "file", "enumerated", uh, uh, prov, subjects)
    facts = []
    for row in g.inventory:
        p = {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}
        fid, _ = W.make_fact(g, "file", "enumerated", uh, uh, prov, p, anchors=[])
        facts.append(fid)
    cid, _ = W.make_coverage(g, sid, sc, W.entry("file", "enumerated", "complete",
                                                 "not-applicable", False, True, None))
    scopes, covs = [sid], [cid]
    bids = {}
    csid, csc = W.make_scope(g, "clones", "normalized-body-hash", uh, uh, prov,
                             sorted(clone_paths) or ["crates/core/src/shared.rs"])
    scopes.append(csid)
    for path in clone_paths:
        bid, bl, lvh, s, e = rust_body(g, uh, retained, path)
        bids[path] = (bid, bl)
        p = {"bodyIdentity": bid, "normalisationLevel": "L0-verbatim",
             "normalisationVersion": lvh}
        fid, _ = W.make_fact(g, "clones", "normalized-body-hash", uh, uh, prov, p,
                             anchors=[W.anchor(g, path, s, e)])
        facts.append(fid)
    ce = clone_entry or W.entry("clones", "normalized-body-hash", "complete",
                                "not-applicable", False, True, None)
    ccid, _ = W.make_coverage(g, csid, csc, ce)
    covs.append(ccid)
    vid, _ = W.make_view(g, plan_id, scopes, facts, covs, prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="pass",
                                            scope_ids=[csid], coverage_ids=[ccid])
    out = CL.close_run(g, retained, [vid], proof, evidence, seal, run)
    return out, bids


def scenario_mixed_edition(results):
    """RS-1: mixed-edition workspace; a `#` marker directory; target override present
    but unselected; bodies of THREE editions in ONE universe."""
    sel = [U_LIB["unitId"], U_LEGACY["unitId"], U_GEN["unitId"]]
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id, own = build(sel)
    paths = ["crates/core/src/lib.rs", "crates/core/src/shared.rs",
             "crates/legacy/src/lib.rs", "tools/#gen/src/main.rs"]
    out, bids = _inventory_and_clones(g, cl, uh, retained, plan_id, paths)
    results["rust-mixed-edition"] = {
        "verdict": "ADMIT",
        "runId": out["runId"],
        "sourceUniverse": uh,
        "sourceUnitOwnershipId": u["sourceUnitOwnershipId"],
        "editionMapSize": len(u["edition"]),
        "editionMapCanonicalBytes": len(C(u["edition"])),
        "editionMapExceedsInheritedU8ComponentLength": len(C(u["edition"])) > 255,
        "languageVersionIsFixedWidth32Bytes": True,
        "markerDirectoryWithHash": "tools/#gen/Cargo.toml",
        "bodyDialects": {p: bids[p][1]["dialect"] for p in paths},
        "bodyIdentities": {p: bids[p][0] for p in paths},
        "compilerBoundFrom": {
            "compilerName": "const rustc (languageVersionBinding)",
            "compilerVersion": "native-context.toolchain.rustcVersion = "
                               + ctx["toolchain"]["rustcVersion"],
            "compilerBuild": "native-context.toolchain.rustCommitHash",
        },
        "trace": out["trace"],
    }
    return g, uh, retained, bids


def scenario_two_selections(results):
    """RS-2: the SAME physical path under two distinct explicitly selected target
    editions -> two universes, two body identities, no ambiguous claim.
    Plus: stable body identity when only the SELECTION changes without changing the
    effective dialect of that body."""
    shared = "crates/core/src/shared.rs"
    lib = "crates/core/src/lib.rs"

    gA, clA, ctxA, _, uA, uhA, retA, planA, _ = build(
        [U_LIB["unitId"], U_LEGACY["unitId"], U_GEN["unitId"]])
    bidA_shared, blA, _, _, _ = rust_body(gA, uhA, retA, shared)
    bidA_lib, _, _, _, _ = rust_body(gA, uhA, retA, lib)

    gB, clB, ctxB, _, uB, uhB, retB, planB, _ = build([U_TEST["unitId"]])
    bidB_shared, blB, _, _, _ = rust_body(gB, uhB, retB, shared)

    # selection changes (U_GEN dropped) but the effective dialect of lib.rs does not
    gC, clC, ctxC, _, uC, uhC, retC, planC, _ = build(
        [U_LIB["unitId"], U_LEGACY["unitId"]])
    bidC_lib, _, _, _, _ = rust_body(gC, uhC, retC, lib)

    results["rust-two-selections"] = {
        "sameFile": shared,
        "universeA_selection": "lib(core)@2021 + legacy + gen",
        "universeB_selection": "test(shared_it)@2018 only",
        "universeA": uhA, "universeB": uhB,
        "dialectA": blA["dialect"], "dialectB": blB["dialect"],
        "bodyIdentityA": bidA_shared, "bodyIdentityB": bidB_shared,
        "distinctBodyIdentities": bidA_shared != bidB_shared,
        "distinctUniverses": uhA != uhB,
        "stableBodyIdentityWhenOnlySelectionChanges": {
            "path": lib,
            "universeA": uhA, "universeC": uhC,
            "universesDiffer": uhA != uhC,
            "bodyIdentityA": bidA_lib, "bodyIdentityC": bidC_lib,
            "bodyIdentityUnchanged": bidA_lib == bidC_lib,
        },
    }


def scenario_ownership_deficiencies(results):
    """RS-3: the three published (deficiency, nativeCause) pairings the clones
    ownership law owes, each DERIVED from the committed record and this scope's
    subjects, plus their output projection."""
    out = {}
    shared = "crates/core/src/shared.rs"

    cases = [
        ("ambiguous", dict(selected=[U_LIB["unitId"], U_TEST["unitId"]]),
         "BODY_LANGUAGE_OWNER_AMBIGUOUS", "body-language-owner-ambiguous"),
        ("partial-enumeration", dict(selected=[U_LIB["unitId"]], enumeration="partial"),
         "BODY_LANGUAGE_OWNER_UNENUMERATED", "body-language-owner-unenumerated"),
        ("no-committed-ownership", dict(selected=[U_LIB["unitId"]], ownership_null=True),
         "BODY_LANGUAGE_OWNERSHIP_REQUIRED", "body-language-ownership-missing"),
    ]
    for name, kw, expected_key, expected_cause in cases:
        sel = kw.pop("selected")
        g, cl, ctx, _, u, uh, retained, plan_id, own = build(sel, **kw)
        try:
            rust_body(g, uh, retained, shared)
            refusal = "ADMITTED(!)"
        except R.Refuse as exc:
            refusal = exc.code
        # the owed Coverage: unknown + input-closure-incomplete + the matching cause
        ent = W.entry("clones", "normalized-body-hash", "unknown", "not-applicable",
                      False, True, None, deficiency="input-closure-incomplete",
                      cause=expected_cause)
        prov = cl["provider-rust"]
        sid, sc = W.make_scope(g, "clones", "normalized-body-hash", uh, uh, prov, [shared])
        cid, payload = W.make_coverage(g, sid, sc, ent)
        CL.admit_coverage_result_v3(g, sid, payload)
        # negatives: a FALSE complete, a null cause, a wrong cause and an unrelated
        # deficiency each refuse -- against the DERIVED pair, not merely the vocabulary.
        negs = {}
        for label, bad in (
            ("false-complete", W.entry("clones", "normalized-body-hash", "complete",
                                       "not-applicable", False, True, None)),
            ("undisclosed-null-deficiency",
             W.entry("clones", "normalized-body-hash", "unknown", "not-applicable",
                     False, True, None)),
            ("null-cause", W.entry("clones", "normalized-body-hash", "unknown",
                                   "not-applicable", False, True, None,
                                   deficiency="input-closure-incomplete", cause=None)),
            ("wrong-cause", W.entry("clones", "normalized-body-hash", "unknown",
                                    "not-applicable", False, True, None,
                                    deficiency="input-closure-incomplete",
                                    cause="lockfile-missing")),
            ("unrelated-deficiency",
             W.entry("clones", "normalized-body-hash", "unknown", "not-applicable",
                     False, True, "budget-exhausted", deficiency="budget-exhausted",
                     cause=None)),
        ):
            bad = dict(bad)
            bad["examinedUniverse"] = {
                "subjectScopeCommitment": "sha256:" + sid[len("scope2:"):],
                "subjectCount": 1}
            p2 = {"schemaVersion": 3, "key": {
                "relation": "clones", "resolution": "normalized-body-hash",
                "sourceUniverse": uh, "targetUniverse": uh,
                "subjectScopeCommitment": "sha256:" + sid[len("scope2:"):]}, "entry": bad}
            try:
                CL.admit_coverage_result_v3(g, sid, p2)
                CL.check_clone_ownership_disclosure(g, sc, bad, retained.get(uh, {}))
                negs[label] = "ADMITTED(!)"
            except R.Refuse as exc:
                negs[label] = exc.code + (":" + exc.detail if exc.detail else "")
        derived = CL.check_clone_ownership_disclosure(g, sc, ent, retained.get(uh, {}))
        out[name] = {
            "selectionLawRefusal": refusal,
            "expectedSelectionLawRefusal": expected_key,
            "owedPair": ["input-closure-incomplete", expected_cause],
            "coverageAdmitted": True,
            "ownershipDisclosureDerived": derived,
            "emptyCloneViewClaimsComplete": False,
            "negatives": negs,
            "publicProjection": {
                "class": "indeterminate", "exitCode": 3,
                "reasonCodes": ["VERDICT.INDETERMINATE"],
                "typedDetailCarrier": "the coverage2 record named by termination.coverageId",
                "publicDomainDetailCode": "input-closure-incomplete",
            },
        }
    results["rust-ownership-deficiencies"] = out


def scenario_rust_negatives(results):
    """RS-N: refused hidden / mismatched inputs on the Rust path."""
    sel = [U_LIB["unitId"], U_LEGACY["unitId"], U_GEN["unitId"]]
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id, own = build(sel)
    neg = {}

    def probe(name, fn):
        try:
            fn()
            neg[name] = "ADMITTED(!)"
        except R.Refuse as exc:
            neg[name] = exc.code + (":" + exc.detail if exc.detail else "")

    bad = json.loads(json.dumps(ctx))
    bad["toolchain"]["rustcVersion"] = "0.0.1"
    probe("rustc-version-not-from-manifest",
          lambda: CL.admit_native_context(g, "native.context.rust.v2", bad))
    bad2 = json.loads(json.dumps(ctx))
    bad2["toolchain"]["rustcDevLlvmDigest"] = "a" * 64
    probe("rust-dev-llvm-digest-names-no-retained-closure",
          lambda: CL.admit_native_context(g, "native.context.rust.v2", bad2))
    bad3 = json.loads(json.dumps(ctx))
    bad3["configProjection"]["replacedSnapshotConfigs"] = ["outside/.cargo/config.toml"]
    probe("replaced-config-path-outside-snapshot",
          lambda: CL.admit_native_context(g, "native.context.rust.v2", bad3))

    def bind(mod_u=None, mod_ret=None):
        uu = json.loads(json.dumps(u)) if mod_u is None else mod_u
        rr = dict(retained[uh]) if mod_ret is None else mod_ret
        CL.bind_universe(g, "native.semantic-universe.rust.v2", uu,
                         "native.context.rust.v2", ctx, rr)

    u_bad = json.loads(json.dumps(u)); u_bad["crateRootPaths"] = ["nowhere/lib.rs"]
    probe("crate-root-outside-snapshot", lambda: bind(u_bad))
    u_bad2 = json.loads(json.dumps(u)); u_bad2["lockfileIdentity"]["contentSha256"] = "b" * 64
    probe("lockfile-bytes-differ", lambda: bind(u_bad2))
    u_bad3 = json.loads(json.dumps(u))
    u_bad3["cfgSets"][0]["cfg"] = ['target_arch="aarch64"']       # drops a base cfg
    probe("cfg-set-drops-a-base-cfg", lambda: bind(u_bad3))
    u_bad4 = json.loads(json.dumps(u)); u_bad4["configProjectionSha256"] = "c" * 64
    probe("config-projection-suffix-mismatch", lambda: bind(u_bad4))
    u_bad5 = json.loads(json.dumps(u)); u_bad5["executionCapableResolution"] = True
    probe("execution-capable-without-prepared", lambda: bind(u_bad5))
    ret_bad = dict(retained[uh])
    ret_bad["unifiedFeatures"] = dict(retained[uh]["unifiedFeatures"],
                                      targetTriple="x86_64-unknown-linux-gnu")
    probe("unified-features-for-another-target",
          lambda: bind(None, dict(ret_bad,
                                  unifiedFeatures=ret_bad["unifiedFeatures"])))
    ret_bad2 = dict(retained[uh])
    ret_bad2["preparedOutputSet"] = {"schemaVersion": 3}
    probe("prepared-set-retained-but-unselected", lambda: bind(None, ret_bad2))

    # ownership record faults
    contradictory = [dict(U_LIB, targetName="not-core")] + ALL_UNITS[1:]
    probe("unit-id-not-derived-from-its-own-row",
          lambda: CL.admit_source_unit_ownership(g, u, ownership_record(
              [U_LIB["unitId"]], units=contradictory)))
    probe("selection-names-an-undeclared-unit",
          lambda: CL.admit_source_unit_ownership(g, u, ownership_record(
              ["sha256:" + "f" * 64])))
    outside = OWNERSHIP + [{"path": "not/in/snapshot.rs", "unitId": U_LIB["unitId"]}]
    probe("ownership-path-outside-snapshot",
          lambda: CL.admit_source_unit_ownership(g, u, ownership_record(
              sel, ownership=sorted(outside, key=lambda o: (o["path"].encode(),
                                                            o["unitId"].encode())))))
    # a NEAREST-DIRECTORY inference is refused: rows are those whose path EQUALS the anchor
    dir_only = [{"path": "crates/core/src", "unitId": U_LIB["unitId"]}]
    g2, cl2, ctx2, _, u2, uh2, ret2, plan2, _ = build(
        [U_LIB["unitId"]], ownership=dir_only)
    probe("nearest-directory-ownership-inference-refused",
          lambda: CL.body_language_version(g2, uh2, "crates/core/src/lib.rs", ret2[uh2]))
    results["rust-negatives"] = neg


def scenario_native_preimages(results):
    """Native dependency/configuration H preimages, reconstructed from the recipes."""
    sel = [U_LIB["unitId"], U_LEGACY["unitId"], U_GEN["unitId"]]
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id, own = build(sel)
    out = {}
    for label, domain, record in [
        ("dependency-source-set", "native.dependency-source-set.v1",
         retained[uh]["dependencySourceSet"]),
        ("unified-features", "native.unified-features.rust.v1",
         retained[uh]["unifiedFeatures"]),
        ("cargo-config-projection", "native.cargo-config-projection.v2",
         ctx["configProjection"]),
        ("source-unit-ownership", "native.source-unit-ownership.v1", own),
        ("compilation-unit", "native.compilation-unit.v1",
         {"schemaVersion": 1, "markerPath": U_TEST["markerPath"],
          "targetKind": U_TEST["targetKind"], "targetName": U_TEST["targetName"]}),
    ]:
        fr = R.frame(domain, record)
        out[label] = {
            "domain": domain,
            "canonicalPayloadBytes": len(C(record)),
            "canonicalPayloadSha256": raw(record),
            "framePrefixHex": fr[:len(b"opensip.product.v1") + 1 + len(domain) + 1 + 8].hex(),
            "frameLength": len(fr),
            "H": H(domain, record),
            "sha256TextSpelling": sha256_text(domain, record),
            "bareHexSuffixSpelling": H(domain, record),
            "frameDigestIsNotThePayloadDigest": H(domain, record) != raw(record),
        }
    # the two Cargo digests that are NOT interchangeable
    out["cargo-two-digests"] = {
        "projectionSha256_rawFileDigest": ctx["configProjection"]["projectionSha256"],
        "configProjectionSha256_hSuffixOverTheWholeRecord": u["configProjectionSha256"],
        "rawSha256OfCanonicalProjectionRecord": raw(ctx["configProjection"]),
        "allThreeDistinct": len({ctx["configProjection"]["projectionSha256"],
                                 u["configProjectionSha256"],
                                 raw(ctx["configProjection"])}) == 3,
    }
    dep = retained[uh]["dependencySourceSet"]["packages"][0]
    out["dependency-file-manifest-chain"] = {
        "fileManifestSha256": dep["fileManifestSha256"],
        "isAnHIdentityOfNativeDependencyFileManifestV1": True,
        "everyRowsContentSha256MustBeRetainedAtItsDeclaredByteLength": True,
        "retainedMemberDigest": raw_bytes(b"pub fn s(){}\n"),
        "retainedMemberLength": len(b"pub fn s(){}\n"),
    }
    results["native-h-preimages"] = out
