"""Vector suite C: native context admission, universe binding, and the
nested dependency / configuration H preimages, per language."""
from __future__ import annotations

import copy
import hashlib

import build as B
import canon as K
import kit
import native as N
import scenarios as S
from store import Refusal, Store, split_id

RESULTS = []


def rec(vid, kind, detail, **extra):
    row = {"id": vid, "kind": kind, "detail": detail}
    row.update(extra)
    RESULTS.append(row)


def refuses(vid, fn, note=""):
    try:
        fn()
        rec(vid, "NEGATIVE-FAILED", "no refusal raised", note=note)
    except (Refusal, K.AdmissionError, kit.SchemaRefusal) as exc:
        rec(vid, "refused", str(exc)[:180],
            firstObservedBoundary=getattr(exc, "code", type(exc).__name__),
            note=note)


def ts_fixture():
    s = Store()
    files = {"tsconfig.json": b'{"compilerOptions":{}}\n', "src/a.ts": b"x\n",
             "package-lock.json": b"{}\n"}
    snap_id, snap, inventory = B.make_snapshot(
        s, files, B.scope_descriptor(["."]), B.default_config(["inventory"]))
    inv = {r["path"]: r for r in inventory}
    lock = {"kind": "package-lock", "path": "package-lock.json",
            "contentSha256": inv["package-lock.json"]["sha256"]}
    ctx, ctx_hex, ids = S.ts_context(
        s, language_mode="ts-tsconfig", config_graph_paths=["tsconfig.json"],
        lockfile=lock, node_modules_digest=None)
    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json", "nodes": [
        {"path": "tsconfig.json", "contentSha256": inv["tsconfig.json"]["sha256"],
         "kind": "tsconfig", "extendsResolved": []}]}
    u, u_hex = S.ts_universe(s, ctx, ctx_hex, language_mode="ts-tsconfig",
                             config_graph=graph, program_roots=["src/a.ts"],
                             lockfile_kind="package-lock")
    return s, ctx, ctx_hex, u, u_hex, inventory, ids


def rust_fixture():
    s = Store()
    files = {"Cargo.toml": b"[package]\nname='a'\n", "Cargo.lock": b"version = 3\n",
             "src/lib.rs": b"pub fn a() {}\n", ".cargo/config.toml": b"[build]\n"}
    snap_id, snap, inventory = B.make_snapshot(
        s, files, B.scope_descriptor(["."]), B.default_config(["inventory"]))
    inv = {r["path"]: r for r in inventory}
    lock = {"path": "Cargo.lock", "contentSha256": inv["Cargo.lock"]["sha256"],
            "lockfileVersion": 3}
    # a real dependency package with a nested file manifest down to raw bytes
    dep_bytes = b"pub fn dep() {}\n"
    dep_digest = s.put_blob(dep_bytes)
    manifest = [{"path": "src/lib.rs", "contentSha256": dep_digest,
                 "byteLength": len(dep_bytes)}]
    fm_hex = split_id(
        s.put_native_identity("native.dependency-file-manifest.v1", manifest),
        "sha256")
    pkg = {"name": "left-pad-rs", "version": "1.0.0", "sourceKind": "registry",
           "sourceId": "registry+https://example.invalid/index",
           "lockChecksum": hashlib.sha256(b"crate").hexdigest(),
           "fileManifestSha256": fm_hex, "fileCount": 1,
           "totalBytes": len(dep_bytes),
           "acquisition": {"mode": "imported-descriptor",
                           "descriptorId": None, "vendorPath": None},
           "checksumVerification": "self-consistent",
           "provenanceAssurance": "declared"}
    dss_id, dss = S.dependency_source_set(s, lock, [pkg])
    uf_id, _ = S.unified_features(s, "x86_64-unknown-linux-gnu")
    ctx, ctx_hex = S.rust_context(s, dependency_set_id=dss_id,
                                  unified_features_id=uf_id,
                                  replaced_configs=[".cargo/config.toml"])
    unit = S.unit("Cargo.toml", "lib", "a", "a", None)
    sou_id, _ = S.source_unit_ownership(
        s, [unit], [unit["unitId"]],
        [{"path": "src/lib.rs", "unitId": unit["unitId"]}])
    u, u_hex = S.rust_universe(s, ctx, ctx_hex, edition={"a": 2021},
                               lockfile=lock, crate_roots=["src/lib.rs"],
                               ownership_id=sou_id)
    return s, ctx, ctx_hex, u, u_hex, inventory, dss_id, pkg, fm_hex


def run_all():
    # ---------- TypeScript ----------
    s, ctx, ctx_hex, u, u_hex, inventory, ids = ts_fixture()
    adm = N.admit_native_context(s, "native.context.typescript.v2", ctx, inventory)
    rec("C1-POS-ts-context-admits", "admitted", adm["contextId"])
    got = N.bind_universe(s, "native.semantic-universe.typescript.v2", u, adm,
                          ctx, {}, inventory)
    rec("C1-POS-ts-universe-binds", "admitted", got,
        agrees=got == "sha256:" + u_hex)
    rec("C1-V-fold-discriminators", "computed",
        "; ".join(f"{n!r}->{N.lib_name_fold(n)!r}"
                  for n in ["İ", "ΟΣ", "ΣΟ", "ß"]),
        unicodeCaseData=N.UNICODE_CASE_DATA_VERSION)

    def mut(fn):
        c = copy.deepcopy(ctx)
        fn(c)
        return lambda: N.admit_native_context(
            s, "native.context.typescript.v2", c, inventory)

    refuses("C1-N1-compiler-version-not-from-manifest",
            mut(lambda c: c["toolchain"].__setitem__("compilerVersion", "9.9.9")),
            note="must equal the admitted signed closure manifest semanticVersion")
    refuses("C1-N2-tool-digest-outside-closure",
            mut(lambda c: c["toolClosure"].__setitem__("compiler", "ab" * 32)),
            note="every tool digest is a member of the named closure tree")
    refuses("C1-N3-stdlib-inventory-incomplete",
            mut(lambda c: c["toolchain"]["standardLibraryComponentDigests"].pop(0)),
            note="the COMPLETE .d.ts inventory of the retained stdlib tree")
    refuses("C1-N4-stdlib-component-digest-disagrees",
            mut(lambda c: c["toolchain"]["standardLibraryComponentDigests"][0]
                .__setitem__("sha256", "cd" * 32)),
            note="a declared component digest must be the retained tree's")
    refuses("C1-N5-lib-not-retained",
            mut(lambda c: (c["toolchain"].__setitem__("libSelection", ["es2030"]),
                           c["configProjection"]["honoredOptions"]
                           .__setitem__("lib", ["es2030"]))),
            note="component(n) must be an element of the declared component set")
    refuses("C1-N6-libSelection-disagrees-with-honored-lib",
            mut(lambda c: c["configProjection"]["honoredOptions"]
                .__setitem__("lib", ["dom"])),
            note="the folded name SETS must be equal")
    refuses("C1-N7-moduleResolutionMode-disagrees",
            mut(lambda c: c.__setitem__("moduleResolutionMode", "bundler")),
            note="equals configProjection.honoredOptions.moduleResolution")
    refuses("C1-N8-config-graph-path-outside-snapshot",
            mut(lambda c: c["configProjection"]["configGraphPaths"]
                .append("elsewhere/tsconfig.json")),
            note="every repository path a context names must be inventoried")
    refuses("C1-N9-lockfile-digest-mismatch",
            mut(lambda c: c["lockfileIdentity"].__setitem__("contentSha256",
                                                            "ef" * 32)),
            note="a named lockfile must match its inventory digest")
    # a Rust-minted context offered as the TypeScript one
    rs, rctx, rctx_hex, ru, ru_hex, rinv, dss_id, pkg, fm_hex = rust_fixture()
    radm = N.admit_native_context(rs, "native.context.rust.v2", rctx, rinv)
    refuses("C1-N10-rust-context-offered-as-typescript",
            lambda: N.bind_universe(s, "native.semantic-universe.typescript.v2",
                                    u, radm, rctx, {}, inventory),
            note="a universe binds the record of its OWN language")
    refuses("C1-N11-universe-without-the-retained-context",
            lambda: N.bind_universe(s, "native.semantic-universe.typescript.v2",
                                    u, adm, None, {}, inventory),
            note="there is no context-free admit path")
    other = copy.deepcopy(ctx)
    other["packageModuleType"] = "module"
    refuses("C1-N12-context-bytes-are-not-the-admitted-ones",
            lambda: N.bind_universe(s, "native.semantic-universe.typescript.v2",
                                    u, adm, other, {}, inventory),
            note="an identity commits to the context bytes")
    bad_u = copy.deepcopy(u)
    bad_u["allowJs"] = True
    refuses("C1-N13-universe-field-contradicts-context",
            lambda: N.bind_universe(s, "native.semantic-universe.typescript.v2",
                                    bad_u, adm, ctx, {}, inventory),
            note="the two records must AGREE where they overlap")

    # ---------- Rust ----------
    rec("C2-POS-rust-context-admits", "admitted", radm["contextId"])
    rgot = N.bind_universe(rs, "native.semantic-universe.rust.v2", ru, radm,
                           rctx, {"sourceUnitOwnership":
                                  rs.objects["sha256:" + split_id(
                                      ru["sourceUnitOwnershipId"], "sha256")]},
                           rinv)
    rec("C2-POS-rust-universe-binds", "admitted", rgot,
        agrees=rgot == "sha256:" + ru_hex)
    # the nested dependency / configuration H PREIMAGES, spelled out
    dep_manifest = rs.objects["sha256:" + fm_hex]
    rec("C2-V-dependency-file-manifest-preimage", "computed",
        K.C(dep_manifest).decode(),
        domain="native.dependency-file-manifest.v1",
        identity="sha256:" + K.H("native.dependency-file-manifest.v1", dep_manifest),
        agrees=K.H("native.dependency-file-manifest.v1", dep_manifest) == fm_hex)
    dss = rs.objects[dss_id]
    rec("C2-V-dependency-source-set-preimage", "computed",
        K.C(dss).decode()[:400] + "...",
        domain="native.dependency-source-set.v1", identity=dss_id)
    proj = rctx["configProjection"]
    proj_h = K.H("native.cargo-config-projection.v2", proj)
    rec("C2-V-cargo-config-projection-two-digests", "computed",
        f"projectionSha256(file bytes)={proj['projectionSha256']} ; "
        f"H(native.cargo-config-projection.v2, record)={proj_h} ; "
        f"raw SHA256(C(record))={K.canonical_record_digest(proj)}",
        universeField=ru["configProjectionSha256"],
        universeFieldIsTheHSuffix=ru["configProjectionSha256"] == proj_h,
        allThreeDistinct=len({proj["projectionSha256"], proj_h,
                              K.canonical_record_digest(proj)}) == 3)
    unit_row = rs.objects["sha256:" + split_id(
        ru["sourceUnitOwnershipId"], "sha256")]["units"][0]
    pre = {"schemaVersion": 1, "markerPath": unit_row["markerPath"],
           "targetKind": unit_row["targetKind"], "targetName": unit_row["targetName"]}
    rec("C2-V-compilation-unit-preimage", "computed", K.C(pre).decode(),
        identity="sha256:" + K.H("native.compilation-unit.v1", pre),
        agrees="sha256:" + K.H("native.compilation-unit.v1", pre) == unit_row["unitId"])

    def rmut(fn):
        c = copy.deepcopy(rctx)
        fn(c)
        return lambda: N.admit_native_context(rs, "native.context.rust.v2", c, rinv)

    refuses("C2-N1-rustc-version-not-from-manifest",
            rmut(lambda c: c["toolchain"].__setitem__("rustcVersion", "9.9.9")),
            note="must equal the admitted tool closure semanticVersion")
    refuses("C2-N2-rust-dev-llvm-wrong-kind",
            rmut(lambda c: c["toolchain"].__setitem__(
                "rustcDevLlvmDigest", split_id(c["toolClosure"]["closureId"],
                                               "closure2"))),
            note="closure2:<value> must name a retained closure of kind rust-dev-llvm")
    refuses("C2-N3-replaced-config-outside-snapshot",
            rmut(lambda c: c["configProjection"]["replacedSnapshotConfigs"]
                 .append("elsewhere/.cargo/config.toml")),
            note="every replacedSnapshotConfigs entry must be inventoried")
    refuses("C2-N4-linker-outside-closure",
            rmut(lambda c: c["toolClosure"].__setitem__("linker", "ab" * 32)),
            note="every tool that runs is in the closure")
    bad_dep = copy.deepcopy(rs.objects[dss_id])
    bad_dep["packages"][0]["totalBytes"] += 1
    refuses("C2-N5-dependency-total-bytes-mismatch",
            lambda: N._admit_dependency_set(rs, bad_dep),
            note="the chain continues to raw bytes at exactly the declared length")
    bad_ru = copy.deepcopy(ru)
    bad_ru["configProjectionSha256"] = proj["projectionSha256"]
    refuses("C2-N6-config-projection-raw-file-digest-offered-as-the-H-suffix",
            lambda: N.bind_universe(rs, "native.semantic-universe.rust.v2",
                                    bad_ru, radm, rctx, {}, rinv),
            note="two digests that are not interchangeable")
    bad_cfg = copy.deepcopy(ru)
    bad_cfg["cfgSets"] = [{"cfgSetId": "primary", "cfg": []}]
    refuses("C2-N7-cfgset-drops-a-base-cfg",
            lambda: N.bind_universe(rs, "native.semantic-universe.rust.v2",
                                    bad_cfg, radm, rctx, {}, rinv),
            note="every set's cfg contains every member of baseCfg")
    bad_root = copy.deepcopy(ru)
    bad_root["crateRootPaths"] = ["elsewhere/lib.rs"]
    refuses("C2-N8-crate-root-outside-snapshot",
            lambda: N.bind_universe(rs, "native.semantic-universe.rust.v2",
                                    bad_root, radm, rctx, {}, rinv),
            note="every crateRootPaths entry must be inventoried")

    # ---------- syntax ----------
    ss = Store()
    sctx, sctx_hex = S.syntax_context(ss)
    sadm = N.admit_native_context(ss, "native.context.syntax.v2", sctx, [])
    rec("C3-POS-syntax-context-admits", "admitted", sadm["contextId"])
    su, su_hex = S.syntax_universe(ss, sctx, sctx_hex, ["g-typescript"])
    sgot = N.bind_universe(ss, "native.semantic-universe.syntax.v2", su, sadm,
                           sctx, {}, [])
    rec("C3-POS-syntax-universe-binds", "admitted", sgot,
        agrees=sgot == "sha256:" + su_hex)
    bad_sel = copy.deepcopy(su)
    bad_sel["selectedGrammarIds"] = ["g-cobol"]
    refuses("C3-N1-grammar-not-in-bundle",
            lambda: N.bind_universe(ss, "native.semantic-universe.syntax.v2",
                                    bad_sel, sadm, sctx, {}, []),
            note="a selection naming a grammar the bundle does not contain")

    def smut(fn):
        c = copy.deepcopy(sctx)
        fn(c)
        return lambda: N.admit_native_context(ss, "native.context.syntax.v2", c, [])

    refuses("C3-N2-parser-version-not-from-manifest",
            smut(lambda c: c["grammarBundle"].__setitem__("parserVersion", "9.9")),
            note="parserVersion must equal the grammar closure manifest version")
    refuses("C3-N3-data-grammar-claiming-code",
            smut(lambda c: next(g for g in c["grammarBundle"]["grammars"]
                                if g["languageId"] == "json")
                 .__setitem__("syntaxClass", "code")),
            note="a data grammar claiming `code` refuses at bundle admission")
    refuses("C3-N4-code-grammar-demoted-to-data",
            smut(lambda c: next(g for g in c["grammarBundle"]["grammars"]
                                if g["languageId"] == "rust")
                 .__setitem__("syntaxClass", "data-document")),
            note="both directions are enforced")
    refuses("C3-N5-row-claiming-another-language-suffix",
            smut(lambda c: next(g for g in c["grammarBundle"]["grammars"]
                                if g["languageId"] == "json")["suffixes"]
                 .append(".ts")),
            note="a row claiming a suffix the table routes to another language")
    return RESULTS
