"""Rust Run scenarios: mixed-edition workspace, target-specific edition override,
`#` marker directory, per-selection dialect, ambiguity, partial enumeration."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import osip  # noqa: E402

L0_ID = "L0-verbatim"
L1_ID = "L1-lexical"
RS_L1_SPEC = b"level-specification L1-lexical: Rust lexical boundary rules v1"

BODY = b"{\n    a + b\n}"

# A representative LARGE edition map: 21 crates, three editions.
LARGE_EDITION_MAP = {}
for _i in range(18):
    LARGE_EDITION_MAP["util_%02d" % _i] = 2021
LARGE_EDITION_MAP["core_lib"] = 2021
LARGE_EDITION_MAP["legacy_lib"] = 2015
LARGE_EDITION_MAP["bridge"] = 2018


def _files():
    f = {
        "Cargo.toml": b'[workspace]\nmembers=["crates/*"]\n',
        "Cargo.lock": b'version = 4\n',
        ".cargo/config.toml": b'[build]\nrustflags=["--cfg","feature=\\"x\\""]\n',
        "crates/core_lib/Cargo.toml": b'[package]\nname="core_lib"\nedition="2021"\n',
        "crates/core_lib/src/lib.rs": b"pub fn add(a: i32, b: i32) -> i32 " + BODY,
        # one physical file compiled by two targets (lib and an edition-2018 bin)
        "crates/core_lib/src/shared.rs": b"pub fn mix(a: i32, b: i32) -> i32 " + BODY,
        "crates/legacy_lib/Cargo.toml": b'[package]\nname="legacy_lib"\nedition="2015"\n',
        "crates/legacy_lib/src/lib.rs": b"pub fn old(a: i32, b: i32) -> i32 " + BODY,
        # a valid `#` marker directory: the canonical path contract admits it
        "crates/v#1/Cargo.toml": b'[package]\nname="bridge"\nedition="2018"\n',
        "crates/v#1/src/lib.rs": b"pub fn bridge(a: i32, b: i32) -> i32 " + BODY,
    }
    for i in range(18):
        f["crates/util_%02d/Cargo.toml" % i] = (
            '[package]\nname="util_%02d"\nedition="2021"\n' % i).encode()
        f["crates/util_%02d/src/lib.rs" % i] = b"pub fn u() {}\n"
    return f


def _units():
    """Closed table of compilation TARGETS. `bin_shared` overrides its package
    edition (2018) while its package core_lib defaults to 2021 (Cargo permits it)."""
    u = [
        F.unit("crates/core_lib/Cargo.toml", "core_lib", "lib", "core_lib", None),
        F.unit("crates/core_lib/Cargo.toml", "core_lib", "bin", "bin_shared", 2018),
        F.unit("crates/core_lib/Cargo.toml", "core_lib", "test", "core_lib_test", None),
        F.unit("crates/legacy_lib/Cargo.toml", "legacy_lib", "lib", "legacy_lib", None),
        F.unit("crates/v#1/Cargo.toml", "bridge", "lib", "bridge", None),
    ]
    for i in range(18):
        u.append(F.unit("crates/util_%02d/Cargo.toml" % i, "util_%02d" % i,
                        "lib", "util_%02d" % i, None))
    return u


def _rows(units):
    by = {(u["markerPath"], u["targetKind"], u["targetName"]): u["unitId"] for u in units}
    lib = by[("crates/core_lib/Cargo.toml", "lib", "core_lib")]
    binu = by[("crates/core_lib/Cargo.toml", "bin", "bin_shared")]
    test = by[("crates/core_lib/Cargo.toml", "test", "core_lib_test")]
    legacy = by[("crates/legacy_lib/Cargo.toml", "lib", "legacy_lib")]
    bridge = by[("crates/v#1/Cargo.toml", "lib", "bridge")]
    rows = [
        {"path": "crates/core_lib/src/lib.rs", "unitId": lib},
        {"path": "crates/core_lib/src/lib.rs", "unitId": test},   # lib+test agree (2021)
        {"path": "crates/core_lib/src/shared.rs", "unitId": lib},     # 2021
        {"path": "crates/core_lib/src/shared.rs", "unitId": binu},    # 2018 override
        {"path": "crates/legacy_lib/src/lib.rs", "unitId": legacy},
        {"path": "crates/v#1/src/lib.rs", "unitId": bridge},
    ]
    for i in range(18):
        rows.append({"path": "crates/util_%02d/src/lib.rs" % i,
                     "unitId": by[("crates/util_%02d/Cargo.toml" % i, "lib",
                                   "util_%02d" % i)]})
    return rows, {"lib": lib, "bin": binu, "test": test, "legacy": legacy,
                  "bridge": bridge}


def build(store, selection="lib-only", enumeration="complete", tamper=None):
    """selection: lib-only | bin-only | lib-plus-test | both-targets(ambiguous)"""
    out = {"selection": selection, "enumeration": enumeration, "assumptions": [
        "Cargo target table, editions, lockfile bytes and source bytes are SYNTHETIC "
        "trusted observations; no cargo, rustc, build script or proc macro was run"]}
    tool = F.rust_toolchain(store)
    llvm = F.rust_dev_llvm(store)
    prov = F.provider_closure(store, "rust-semantic")
    ev = F.evaluator_closure(store)
    rc = F.rule_closure(store)
    closures = {c["hex"]: c for c in (tool, llvm, prov, ev, rc)}

    files = _files()
    cfg = F.config(["clones", "declares", "file"])
    scope = F.scope(["."], excluded=[".git", "target"])
    snap = G.make_snapshot(store, files, scope, cfg, "git", "d" * 40, False)

    lockfile = {"path": "Cargo.lock",
                "contentSha256": snap["inventory"]["Cargo.lock"]["sha256"],
                "lockfileVersion": 4}
    dep = F.dependency_source_set(lockfile)
    feats = F.unified_features()
    proj = F.cargo_projection(store, [".cargo/config.toml"])
    ctx = F.rust_context(store, tool, llvm, proj,
                         "sha256:" + osip.H("native.dependency-source-set.v1", dep),
                         "sha256:" + osip.H("native.unified-features.rust.v1", feats))
    if tamper == "context-rustc-dev-llvm-not-retained":
        bad = dict(ctx["descriptor"])
        bad["toolchain"] = dict(bad["toolchain"], rustcDevLlvmDigest="e" * 64)
        ctx = G.mint_context(store, G.RS_CONTEXT_DOMAIN, bad)
    if tamper == "context-tool-digest-outside-closure":
        bad = dict(ctx["descriptor"])
        bad["toolClosure"] = dict(bad["toolClosure"],
                                  rustc=osip.raw_sha256(b"a system rustc"))
        ctx = G.mint_context(store, G.RS_CONTEXT_DOMAIN, bad)
    if tamper == "context-config-outside-snapshot":
        bad = dict(ctx["descriptor"])
        bad["configProjection"] = dict(bad["configProjection"],
                                       replacedSnapshotConfigs=["vendor/.cargo/config.toml"])
        ctx = G.mint_context(store, G.RS_CONTEXT_DOMAIN, bad)

    retained_ctx = {"dependencySourceSet": dep, "unifiedFeatures": feats}
    G.admit_native_context(store, ctx, closures, snap, retained_ctx)

    units = _units()
    rows, ids = _rows(units)
    sel = {"lib-only": [ids["lib"], ids["legacy"], ids["bridge"]],
           "bin-only": [ids["bin"], ids["legacy"], ids["bridge"]],
           "lib-plus-test": [ids["lib"], ids["test"], ids["legacy"], ids["bridge"]],
           "both-targets": [ids["lib"], ids["bin"], ids["legacy"], ids["bridge"]]}[selection]
    for i in range(18):
        sel = sel + [u["unitId"] for u in units if u["crateName"] == "util_%02d" % i]
    own = F.ownership(units, sel, rows, enumeration)
    own_id = "sha256:" + osip.H("native.source-unit-ownership.v1", own)

    crate_roots = sorted([p for p in files if p.endswith("src/lib.rs")]
                         + ["crates/core_lib/src/shared.rs"])
    uni = F.rust_universe(store, ctx, LARGE_EDITION_MAP, lockfile, crate_roots,
                          None if tamper == "no-committed-ownership" else own_id)
    retained = dict(retained_ctx)
    if tamper != "no-committed-ownership":
        retained["sourceUnitOwnership"] = own
    G.bind_universe(store, uni, ctx, None, snap, retained)

    facts, scopes, coverages = [], [], []

    # file fact with the full inventoried path/hash/length join
    fp = "crates/core_lib/src/lib.rs"
    inv = snap["inventory"][fp]
    facts.append(G.make_fact(store, snap, "file", "enumerated", uni["hex"], uni["hex"],
                             prov["id"],
                             {"path": fp, "contentSha256": inv["sha256"],
                              "byteLength": inv["bytes"]},
                             [{"path": fp, "blobDigest": inv["sha256"],
                               "startByte": 0, "endByte": inv["bytes"]}]))
    facts.append(G.make_fact(store, snap, "package", "manifest-declared", uni["hex"],
                             uni["hex"], prov["id"],
                             {"packageName": "bridge", "packageVersion": "0.1.0",
                              "manifestPath": "crates/v#1/Cargo.toml"}, []))

    # clone bodies, one per selected-dialect case
    body_ids = {}
    clone_paths = ["crates/core_lib/src/lib.rs", "crates/legacy_lib/src/lib.rs",
                   "crates/v#1/src/lib.rs", "crates/core_lib/src/shared.rs"]
    clone_errors = {}
    for p in clone_paths:
        src = files[p]
        start = src.index(b"{")
        anchor = [{"path": p, "blobDigest": snap["inventory"][p]["sha256"],
                   "startByte": start, "endByte": len(src)}]
        try:
            payload, ident, blv = G.clone_body_fact_parts(
                store, uni, ctx, p, src[start:], L0_ID, RS_L1_SPEC, None, retained)
            body_ids[p] = {"bodyIdentity": ident, "dialect": blv["dialect"],
                           "languageId": blv["languageId"]}
            facts.append(G.make_fact(store, snap, "clones", "normalized-body-hash",
                                     uni["hex"], uni["hex"], prov["id"], payload, anchor))
        except G.Refusal as exc:
            clone_errors[p] = exc.cause
    out["bodyIdentities"] = body_ids
    out["cloneRefusals"] = clone_errors

    file_scope = G.make_subject_scope(store, snap, "file", "enumerated", uni["hex"],
                                      uni["hex"], prov["id"], sorted(files))
    scopes.append(file_scope)
    coverages.append(G.make_coverage(store, file_scope,
                                     F.na_entry("file", "enumerated", file_scope)))

    # clones scope: the subjects the analysis asked about
    clone_scope = G.make_subject_scope(store, snap, "clones", "normalized-body-hash",
                                       uni["hex"], uni["hex"], prov["id"],
                                       sorted(clone_paths))
    scopes.append(clone_scope)
    deficiency, cause = _owed_disclosure(own if tamper != "no-committed-ownership" else None,
                                         clone_paths, LARGE_EDITION_MAP, units)
    coverages.append(G.make_coverage(
        store, clone_scope,
        F.na_entry("clones", "normalized-body-hash", clone_scope,
                   "complete" if deficiency is None else "unknown",
                   deficiency, cause)))
    out["clonesCoverage"] = {"deficiency": deficiency, "nativeCause": cause,
                             "coverage": "complete" if deficiency is None else "unknown"}

    return dict(out, store=store, snapshot=snap, closures=closures, context=ctx,
                universe=uni, retained=retained, facts=facts, scopes=scopes,
                coverages=coverages, provider=prov, evaluator=ev, rule=rc,
                ownership=own, ownershipId=own_id, files=files,
                language="rust", languageMode="rust-cargo",
                declaredRelations={"file": "enumerated", "package": "manifest-declared",
                                   "clones": "normalized-body-hash"})


def _owed_disclosure(own, subjects, editions, units):
    """Derive the owed (deficiency, nativeCause) from the COMMITTED ownership record
    and THIS scope's subjects, in the selection law's own order (native section 10)."""
    if own is None:
        return "input-closure-incomplete", "body-language-ownership-missing"
    if own["enumeration"] == "partial":
        return "input-closure-incomplete", "body-language-owner-unenumerated"
    unit_by_id = {u["unitId"]: u for u in own["units"]}
    for p in subjects:
        rows = [r for r in own["ownership"] if r["path"] == p
                and r["unitId"] in own["selectedUnitIds"]]
        eds = set()
        for r in rows:
            u = unit_by_id[r["unitId"]]
            eds.add(u["targetEdition"] if u["targetEdition"] is not None
                    else editions[u["crateName"]])
        if len(eds) > 1:
            return "input-closure-incomplete", "body-language-owner-ambiguous"
    return None, None
