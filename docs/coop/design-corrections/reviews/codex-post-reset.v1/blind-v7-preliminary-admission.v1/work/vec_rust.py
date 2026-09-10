"""RUN-RS: a mixed-edition Rust workspace, with the compilation-target
ownership relation, an explicit selection, a `#` marker directory, a
target-specific edition differing from its package default, and the same
physical source path under two distinct explicitly selected target editions.
"""

import hashlib

import oslib as O
import graph as G
import build as B
from oslib import C, H, sha256hex, raw_digest

LIB_BODY = b"fn helper(x: u32) -> u32 {\n    x + 1\n}\n"
DUAL_BODY = b"fn shared(v: &str) -> usize {\n    v.len()\n}\n"
TOOL_BODY = b"fn main() {\n    println!(\"tool\");\n}\n"
ODD_BODY = b"fn odd(n: i64) -> i64 {\n    n * 2\n}\n"

RUSTC_TREE = {"bin/rustc": b"rustc-binary\n", "bin/cargo": b"cargo-binary\n",
              "bin/ld": b"linker-binary\n", "bin/ar": b"ar-binary\n",
              "libexec/proc-macro-srv": b"pms-binary\n"}
LLVM_TREE = {"lib/librustc_llvm.so": b"llvm-shared-object\n"}

# a representative LARGE edition map (21 crates), per native S3's own example
BIG_CRATES = ["wsroot", "legacy", "modern", "odd"] + [
    "aux%02d" % i for i in range(1, 18)]


def build(selection="A", mutate=""):
    kit = B.Kit()
    w = kit.w
    lv = B.retain_level_specs(kit)

    f_ws = kit.file("Cargo.toml", '[workspace]\nmembers=["crates/*"]\n'
                                  '[package]\nname="wsroot"\nedition="2021"\n')
    f_lock = kit.file("Cargo.lock", 'version = 4\n[[package]]\nname = "serde"\n'
                                    'version = "1.0.0"\n'
                                    'source = "registry+https://example.invalid/index"\n'
                                    'checksum = "%s"\n' % ("ab" * 32))
    f_cargo_cfg = kit.file(".cargo/config.toml", '[build]\nrustflags=["--cfg","x"]\n')
    f_leg_m = kit.file("crates/legacy/Cargo.toml",
                       '[package]\nname="legacy"\nedition="2018"\n')
    f_leg = kit.file("crates/legacy/src/lib.rs", LIB_BODY)
    f_mod_m = kit.file("crates/modern/Cargo.toml",
                       '[package]\nname="modern"\nedition="2021"\n'
                       '[[bin]]\nname="tool"\nedition="2024"\n')
    f_mod = kit.file("crates/modern/src/lib.rs", LIB_BODY)
    f_tool = kit.file("crates/modern/src/bin/tool.rs", TOOL_BODY)
    f_odd_m = kit.file("crates/#odd/Cargo.toml",
                       '[package]\nname="odd"\nedition="2021"\n')
    f_odd = kit.file("crates/#odd/src/lib.rs", ODD_BODY)
    f_dual = kit.file("shared/dual.rs", DUAL_BODY)

    # ---- closures --------------------------------------------------------
    tool_id, tool_desc = kit.closure("toolchain", RUSTC_TREE, "1.83.0")
    llvm_id, llvm_desc = kit.closure("rust-dev-llvm", LLVM_TREE, "1.83.0")
    prov_id, _ = kit.closure("provider", {"bin/rsprovider": b"provider\n"},
                             "3.0.0")
    eval_id, _ = kit.closure("evaluator", {"bin/eval": b"evaluator\n"}, "1.0.0")
    det_id, _ = kit.closure("detector", {"rules/inv.json": b"{}\n"}, "1.0.0")
    tm = {r["path"]: r["sha256"] for r in tool_desc["tree"]}

    # ---- nested Rust input records --------------------------------------
    dep_files = [{"path": "src/lib.rs",
                  "contentSha256": w.raw(b"pub fn de() {}\n"),
                  "byteLength": len(b"pub fn de() {}\n")}]
    _, dep_manifest_hx = w.mint("native.dependency-file-manifest.v1", dep_files)
    lockid = {"path": "Cargo.lock", "contentSha256": f_lock["sha256"],
              "lockfileVersion": 4}
    depset = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lockid,
              "packages": [{"name": "serde", "version": "1.0.0",
                            "sourceKind": "registry",
                            "sourceId": "registry+https://example.invalid/index",
                            "lockChecksum": "ab" * 32,
                            "fileManifestSha256": dep_manifest_hx,
                            "fileCount": 1, "totalBytes": 15,
                            "acquisition": {"mode": "in-snapshot-vendored",
                                            "descriptorId": None,
                                            "vendorPath": "vendor/serde"},
                            "checksumVerification": "self-consistent",
                            "provenanceAssurance": "declared"}],
              "completeness": {"state": "complete", "missing": []}}
    depset_ref, depset_hx = kit.mint_native("native.dependency-source-set.v1",
                                            depset)
    feats = {"schemaVersion": 1, "resolverVersion": 2,
             "targetTriple": "aarch64-apple-darwin",
             "activated": [{"packageKey": "serde 1.0.0", "features": ["std"]}],
             "computedBy": {"producer": "opensip-cargo-adapter",
                            "producerBuildId": "adapter-1"}}
    feats_ref, feats_hx = kit.mint_native("native.unified-features.rust.v1", feats)

    projected = b'[build]\nrustflags = ["--cfg", "x"]\n'
    projection = {"schemaVersion": 2,
                  "honoredKeys": ["build.rustflags"],
                  "strippedKeys": ["build.target-dir", "net"],
                  "replacedSnapshotConfigs": [".cargo/config.toml"],
                  "rustflags": {"honored": ["--cfg", "x"], "stripped": [],
                                "executableSelected": False},
                  "ancestorCarrierVerified": True, "cargoHome": "private-empty",
                  "environmentProjection": "none", "claimsCargoSwitch": False,
                  "projectionSha256": w.raw(projected)}
    proj_hx = H("native.cargo-config-projection.v2", projection)
    w.mint("native.cargo-config-projection.v2", projection)

    # ---- SourceUnitOwnershipV1 ------------------------------------------
    def unit(marker, crate, kind, name, edition=None):
        uid, _ = G.unit_id(marker, kind, name)
        return {"unitId": uid, "markerPath": marker, "crateName": crate,
                "targetKind": kind, "targetName": name, "targetEdition": edition}

    u_leg = unit("crates/legacy/Cargo.toml", "legacy", "lib", "legacy")
    u_legt = unit("crates/legacy/Cargo.toml", "legacy", "test", "legacy_tests")
    u_mod = unit("crates/modern/Cargo.toml", "modern", "lib", "modern")
    u_tool = unit("crates/modern/Cargo.toml", "modern", "bin", "tool", 2024)
    u_odd = unit("crates/#odd/Cargo.toml", "odd", "lib", "odd")
    units = sorted([u_leg, u_legt, u_mod, u_tool, u_odd],
                   key=lambda u: u["unitId"].encode())

    ownership = sorted([
        {"path": "crates/legacy/src/lib.rs", "unitId": u_leg["unitId"]},
        {"path": "crates/legacy/src/lib.rs", "unitId": u_legt["unitId"]},
        {"path": "crates/modern/src/lib.rs", "unitId": u_mod["unitId"]},
        {"path": "crates/modern/src/bin/tool.rs", "unitId": u_tool["unitId"]},
        {"path": "crates/#odd/src/lib.rs", "unitId": u_odd["unitId"]},
        {"path": "shared/dual.rs", "unitId": u_leg["unitId"]},
        {"path": "shared/dual.rs", "unitId": u_mod["unitId"]},
    ], key=lambda r: (r["path"].encode(), r["unitId"].encode()))

    SELECTIONS = {
        # A: legacy owns shared/dual.rs among the selected targets -> 2018
        "A": [u_leg["unitId"], u_tool["unitId"], u_odd["unitId"]],
        # A2: same effective dialects, one MORE selected owner (test target,
        # also edition 2018): a different universe, the SAME body identity
        "A2": [u_leg["unitId"], u_legt["unitId"], u_tool["unitId"],
               u_odd["unitId"]],
        # B: the SAME physical path under the other explicitly selected target
        "B": [u_mod["unitId"], u_tool["unitId"], u_odd["unitId"]],
        # AMB: both owners of shared/dual.rs selected, editions disagree
        "AMB": [u_leg["unitId"], u_mod["unitId"], u_tool["unitId"],
                u_odd["unitId"]],
    }
    own = {"schemaVersion": 1,
           "enumeration": "partial" if mutate in ("partial-enumeration",
                                                  "partial-enumeration-false-complete")
                          else "complete",
           "units": units,
           "selectedUnitIds": sorted(SELECTIONS[selection], key=lambda s: s.encode()),
           "ownership": ownership}
    own_ref, own_hx = kit.mint_native("native.source-unit-ownership.v1", own)
    if mutate == "no-ownership":
        own_ref = None

    # ---- native context --------------------------------------------------
    ctx = {"schemaVersion": 2, "targetTriple": "aarch64-apple-darwin",
           "hostTriple": "aarch64-apple-darwin",
           "toolchain": {"rustCommitHash": "9d" * 20, "rustcVersion": "1.83.0",
                         "cargoVersion": "1.83.0",
                         "sysrootDigest": w.raw(b"sysroot-manifest\n"),
                         "rustcDevLlvmDigest": llvm_id.split(":", 1)[1],
                         "standardLibraryComponentDigests": [
                             {"component": "core", "sha256": w.raw(b"core-rlib\n")},
                             {"component": "std", "sha256": w.raw(b"std-rlib\n")}],
                         "targetTriple": "aarch64-apple-darwin"},
           "toolClosure": {"rustc": tm["bin/rustc"], "cargo": tm["bin/cargo"],
                           "linker": tm["bin/ld"], "ar": tm["bin/ar"],
                           "procMacroServer": tm["libexec/proc-macro-srv"],
                           "closureId": tool_id},
           "baseCfg": ["target_arch=\"aarch64\"", "target_os=\"macos\""],
           "resolverVersion": 2,
           "dependencySourceSetId": depset_ref,
           "unifiedFeaturesId": feats_ref,
           "preparedOutputSetId": None,
           "configProjection": projection}
    ctx_ref, ctx_hx = kit.mint_native("native.context.rust.v2", ctx)

    # ---- universe --------------------------------------------------------
    edition_map = {}
    for c in BIG_CRATES:
        edition_map[c] = {"legacy": 2018}.get(c, 2021)
    uni = {"schemaVersion": 2, "edition": edition_map,
           "lockfileIdentity": lockid,
           "dependencySourceSetId": depset_ref,
           "unifiedFeaturesId": feats_ref,
           "nativeContextId": ctx_ref,
           "cfgSets": [{"cfgSetId": "primary",
                        "cfg": ["target_arch=\"aarch64\"", "target_os=\"macos\""]},
                       {"cfgSetId": "primary+test",
                        "cfg": ["target_arch=\"aarch64\"", "target_os=\"macos\"",
                                "test"]}],
           "rustflags": {"honored": ["--cfg", "x"], "stripped": [],
                         "executableSelected": False},
           "crateRootPaths": sorted(["crates/legacy/src/lib.rs",
                                     "crates/modern/src/lib.rs",
                                     "crates/#odd/src/lib.rs"]),
           "configProjectionSha256": proj_hx,
           "preparedResolution": "none",
           "executionCapableResolution": False,
           "preparedOutputSetId": None,
           "sourceUnitOwnershipId": own_ref}
    u_ref, u_hx = kit.mint_native("native.semantic-universe.rust.v2", uni)

    # ---- plan scaffolding ------------------------------------------------
    scope_desc = {"schemaVersion": 2, "workspaceRoots": ["."],
                  "pathPrefixes": [], "excludedPathPrefixes": sorted(
                      [".git", "target"])}
    budget = {"unit": "work-units", "limit": 250000}
    config = {"analysis": {"profileId": "default",
                           "capabilities": sorted(["inventory", "syntax",
                                                   "clones-fact"]),
                           "budget": dict(budget)},
              "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted(
                [{"capabilityId": c, "languageMode": "rust-cargo",
                  "workspaceRoot": ".", "required": True}
                 for c in ("inventory", "syntax", "clones-fact")],
                key=lambda x: C(x)),
            "policyPackIds": ["opensip.builtin"], "parameters": []}
    grant = {"schemaVersion": 2, "projectId": w.projectId,
             "principals": [{"kind": "first-party", "closureId": prov_id,
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(["read-source", "native-analysis"]),
             "scopeDigest": w.record(scope_desc)}
    snap_id, snap = kit.snapshot(config, scope_desc)

    providers = [{"providerId": "rust-semantic", "language": "rust",
                  "providerVersionSource": "signed-closure-manifest",
                  "toolchainIdentitySource": "native-context-v2",
                  "relations": {"file": "enumerated", "clones": "normalized-body-hash",
                                "declares": "syntactic",
                                "unresolved-edge": "observed"},
                  "platformIds": ["macos-aarch64"]}]
    cm, cm_bytes, cm_bytes_digest, cap_id = B.capability_manifest(kit, providers)
    policy, pd, waivers, wd, program, rpd, rule = B.policy_and_program(kit)
    plan_id, plan_desc = B.plan(
        kit, snap_id, cm_bytes_digest, cap_id, [prov_id, eval_id, det_id],
        w.record(spec), w.record(config), [ctx_hx], [], pd, wd,
        w.record(scope_desc), budget, w.record(grant))

    retained = {"sourceUnitOwnership": own if own_ref else None,
                "dependencySourceSet": depset, "unifiedFeatures": feats}
    if own_ref is None:
        retained.pop("sourceUnitOwnership")

    # ---- facts -----------------------------------------------------------
    facts, file_subjects = [], []
    for row in snap["sourceInventory"]:
        fid, _ = kit.fact(snap_id, "file", "enumerated", u_hx, u_hx, prov_id,
                          {"path": row["path"], "contentSha256": row["sha256"],
                           "byteLength": row["bytes"]}, [])
        facts.append(fid)
        file_subjects.append(row["path"])

    clone_paths = {"A": [("crates/legacy/src/lib.rs", f_leg, LIB_BODY),
                         ("crates/modern/src/bin/tool.rs", f_tool, TOOL_BODY),
                         ("crates/#odd/src/lib.rs", f_odd, ODD_BODY),
                         ("shared/dual.rs", f_dual, DUAL_BODY)],
                   "A2": [("crates/legacy/src/lib.rs", f_leg, LIB_BODY),
                          ("crates/modern/src/bin/tool.rs", f_tool, TOOL_BODY),
                          ("crates/#odd/src/lib.rs", f_odd, ODD_BODY),
                          ("shared/dual.rs", f_dual, DUAL_BODY)],
                   "B": [("crates/modern/src/bin/tool.rs", f_tool, TOOL_BODY),
                         ("crates/#odd/src/lib.rs", f_odd, ODD_BODY),
                         ("shared/dual.rs", f_dual, DUAL_BODY)],
                   "AMB": [("shared/dual.rs", f_dual, DUAL_BODY)]}[selection]

    clone_facts, body_ids, dialects = [], {}, {}
    empty_clone_scope = (mutate in ("partial-enumeration", "no-ownership",
                                   "partial-enumeration-false-complete"))
    if not empty_clone_scope:
        for path, blob, body in clone_paths:
            try:
                ident, blv, lang = B.mint_body_identity(
                    kit, "native.semantic-universe.rust.v2", uni, ctx, retained,
                    path, body, "L0-verbatim", lv["L0-verbatim"])
            except G.DialectRefusal as r:
                dialects[path] = "REFUSED:" + r.code
                continue
            body_ids[path] = ident
            dialects[path] = blv["dialect"]
            data = w.cas[blob["sha256"]]
            i = data.index(body)
            fid, _ = kit.fact(snap_id, "clones", "normalized-body-hash", u_hx,
                              u_hx, prov_id,
                              {"bodyIdentity": ident,
                               "normalisationLevel": "L0-verbatim",
                               "normalisationVersion": lv["L0-verbatim"]},
                              [{"path": path, "blobDigest": blob["sha256"],
                                "startByte": i, "endByte": i + len(body)}])
            clone_facts.append(fid)

    # ---- scopes / coverage ----------------------------------------------
    fs_id, fs_hx, fs = kit.scope(snap_id, u_hx, u_hx, "file", "enumerated",
                                 prov_id, file_subjects)
    cs_subjects = [p for p, _, _ in clone_paths]
    cs_id, cs_hx, cs = kit.scope(snap_id, u_hx, u_hx, "clones",
                                 "normalized-body-hash", prov_id, cs_subjects)
    covs = [kit.coverage(fs_id, fs_hx, fs, B.entry_complete())]
    if empty_clone_scope:
        cause = ("body-language-ownership-missing" if mutate == "no-ownership"
                 else "body-language-owner-unenumerated")
        entry = B.entry_complete(coverage="unknown",
                                 deficiency="input-closure-incomplete",
                                 nativeCause=cause)
        if mutate == "partial-enumeration-false-complete":
            entry = B.entry_complete()          # the FALSE `complete` control
        covs.append(kit.coverage(cs_id, cs_hx, cs, entry))
    else:
        covs.append(kit.coverage(cs_id, cs_hx, cs, B.entry_complete()))

    all_facts = facts + clone_facts
    view_id, view = kit.view(plan_id, [fs_id, cs_id], all_facts,
                             [c[0] for c in covs], prov_id,
                             [G.REL_DOC_DIGEST, G.NATIVE_DOC_DIGEST])
    exec_plan_id = B.build_exec_plan(kit, plan_id, prov_id)
    extra_inputs = [{"domain": "policy", "digest": pd},
                    {"domain": "waiver", "digest": wd},
                    {"domain": "analysis-spec", "digest": w.record(spec)},
                    {"domain": "configuration", "digest": w.record(config)},
                    {"domain": "capability-manifest", "digest": cap_id},
                    {"domain": "native-context", "digest": ctx_hx},
                    {"domain": "schema", "digest": G.NATIVE_DOC_DIGEST}]
    proof_id, finding_ids = B.build_proof(
        kit, plan_id, exec_plan_id, eval_id, det_id, rule, rpd, view_id,
        facts[0], covs[0][0], extra_inputs,
        verdict="indeterminate" if empty_clone_scope else "pass")
    ev_id = B.evidence(kit, plan_id, [view_id], [c[0] for c in covs], [],
                       finding_ids, proof_id)
    seal_id, run_id = B.seal_and_run(
        kit, plan_id, exec_plan_id, ev_id, eval_id, pd, proof_id, snap_id,
        cap_id, verdict="indeterminate" if empty_clone_scope else "pass")

    return dict(kit=kit, run=run_id, plan=plan_id, snapshot=snap_id,
                universe=u_hx, context=ctx_hx, ownership=own_ref,
                bodyIdentities=body_ids, dialects=dialects,
                selection=selection, capabilityManifestId=cap_id,
                units={u["targetName"]: u["unitId"] for u in units})
