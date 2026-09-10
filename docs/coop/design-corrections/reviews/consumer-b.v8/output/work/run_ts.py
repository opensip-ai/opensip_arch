"""CB-RUN-TS: a complete minimal positive TypeScript Run descriptor graph.

An ORDINARY TypeScript project: it reads node_modules and resolves bare
specifiers, with its retained configuration graph and dependency layout.
It also carries a JavaScript clone body read by the TypeScript analyzer
universe, so BODY language and PROVIDER identity are distinguished.
"""
from __future__ import annotations

import hashlib
import struct

import assemble
import build
import closure as CL
import osip
from build import Fixture, coverage_entry
from osip import C, H, record_digest, raw_sha256

PLATFORM = "macos-aarch64"
TS_VERSION = "5.6.3"

# The SAME body bytes appear in a .ts and a .js file on purpose.
BODY = b"{\n  const total = a + b;\n  return total;\n}"
A_TS = b"export function add(a: number, b: number): number " + BODY + b"\n"
U_JS = b"export function add(a, b) " + BODY + b"\n"

CAP_MANIFEST = {
    "schemaVersion": 1, "profile": "default",
    "providers": [
        {"providerId": "opensip.provider.typescript", "language": "typescript",
         "providerVersionSource": "closure-manifest",
         "toolchainIdentitySource": "native-context",
         "relations": {"clones": "normalized-body-hash", "declares": "syntactic",
                       "file": "enumerated", "package": "manifest-declared",
                       "unresolved-edge": "observed"},
         "platformIds": [PLATFORM]},
    ],
    "coverageForAbsent": [],
}


def make_level_spec(level):
    return ("opensip.normalisation-level-specification\nlevel=%s\n"
            "lexical-boundaries=v1\ntoken-kind-registry=v1\n"
            "directive-classification=v1\ntransform-order=v1\n"
            "replacement-bytes=v1\n" % level).encode()


def build_run(mutate=None):
    fx = Fixture("cb-ts")
    m = mutate or {}

    pkg = b'{"name":"cb-app","version":"1.0.0","type":"commonjs","private":true}\n'
    lock = b'{"lockfileVersion":3,"packages":{"node_modules/left-pad":{"version":"1.3.0"}}}\n'
    tsconfig = (b'{"compilerOptions":{"module":"node16","moduleResolution":"node16",'
                b'"target":"es2022","lib":["es2022"],"allowJs":true,"strict":true,'
                b'"noEmit":true},"include":["src"]}\n')
    readme = b"# cb-app\n"

    fx.add_file("package.json", pkg)
    fx.add_file("package-lock.json", lock)
    fx.add_file("tsconfig.json", tsconfig)
    fx.add_file("src/a.ts", A_TS)
    fx.add_file("src/util.js", U_JS)
    fx.add_file("README.md", readme)
    inv = {r["path"]: r for r in fx.inventory()}

    # ---- closures ------------------------------------------------------
    tool_cid, _, tool_members = fx.closure(
        "typescript-toolchain", "toolchain",
        {"bin/tsc.js": b"#tsc bundled compiler bytes\n",
         "bin/node": b"#bundled javascript runtime bytes\n"},
        TS_VERSION, PLATFORM, protocol_major=2)
    stdlib_cid, _, std_members = fx.closure(
        "typescript-stdlib", "stdlib",
        {"lib/lib.es5.d.ts": b"declare var x: any;\n",
         "lib/lib.es2022.d.ts": b"declare var y: any;\n",
         "lib/lib.dom.d.ts": b"declare var z: any;\n"},
        TS_VERSION, PLATFORM, protocol_major=2)
    prov_cid, _, _ = fx.closure("typescript-provider", "provider",
                                {"bin/provider": b"#ts semantic provider\n"},
                                "1.0.0", PLATFORM, protocol_major=2)
    eval_cid, _, _ = fx.closure("evaluator", "evaluator",
                                {"bin/evaluator": b"#pure evaluator\n"},
                                "1.0.0", PLATFORM, protocol_major=2)

    # ---- retained node_modules layout (a resolution read-set observation,
    #      NOT a snapshot inventory row: node_modules is pruned by segment) --
    dep_manifest = b'{"name":"left-pad","version":"1.3.0","main":"index.js"}\n'
    fx.s.put_raw(dep_manifest, "node_modules manifest bytes")
    layout = {"schemaVersion": 1, "entries": [
        {"packageName": "left-pad", "packageVersion": "1.3.0",
         "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad",
         "contentSha256": raw_sha256(dep_manifest)}]}
    layout_digest = fx.rec(layout, "native", "#/$defs/ResolvedNodeModulesLayoutV1",
                           "node-modules-layout")

    # ---- config graph ---------------------------------------------------
    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json",
             "nodes": [{"path": "tsconfig.json",
                        "contentSha256": inv["tsconfig.json"]["sha256"],
                        "kind": "tsconfig", "extendsResolved": []}]}
    if m.get("relabel_config_kind"):
        graph["nodes"][0]["kind"] = "other"
    graph_digest = fx.rec(graph, "native", "#/$defs/TypeScriptConfigGraphV1",
                          "typescript-config-graph")

    honored = {"allowJs": True, "checkJs": False, "module": "node16",
               "moduleResolution": "node16", "target": "es2022", "strict": True,
               "skipLibCheck": False, "noEmit": True, "types": None,
               "lib": ["es2022"], "baseUrl": None, "paths": [], "rootDirs": [],
               "resolveJsonModule": False, "allowSyntheticDefaultImports": False,
               "esModuleInterop": False, "customConditions": [], "jsx": None}
    ctx = {"schemaVersion": 2, "languageMode": "js-allowjs",
           "toolchain": {"compilerName": "typescript", "compilerVersion": TS_VERSION,
                         "compilerPackageDigest": tool_members["bin/tsc.js"],
                         "typescriptStdlibMerkleRoot": stdlib_cid.split(":")[1],
                         "standardLibraryComponentDigests": sorted(
                             [{"component": p.rsplit("/", 1)[-1], "sha256": d}
                              for p, d in std_members.items()],
                             key=lambda r: r["component"].encode()),
                         "libSelection": ["es2022"]},
           "toolClosure": {"compiler": tool_members["bin/tsc.js"],
                           "runtime": tool_members["bin/node"],
                           "closureId": tool_cid},
           "configProjection": {"schemaVersion": 2, "ancestorCarrierVerified": True,
                                "environmentSanitized": True,
                                "typeAcquisitionEnabled": False,
                                "executableSelected": False,
                                "honoredOptions": honored,
                                "strippedOptions": [
                                    {"option": "outDir", "reason": "emits-output"}],
                                "configGraphPaths": ["tsconfig.json"]},
           "moduleResolutionMode": "node16", "packageModuleType": "commonjs",
           "nodeModulesLayoutDigest": layout_digest,
           "lockfileIdentity": {"kind": "package-lock", "path": "package-lock.json",
                                "contentSha256": inv["package-lock.json"]["sha256"]}}
    if m.get("stdlib_partial_inventory"):
        ctx["toolchain"]["standardLibraryComponentDigests"] = [
            r for r in ctx["toolchain"]["standardLibraryComponentDigests"]
            if r["component"] != "lib.dom.d.ts"]
    if m.get("compiler_version_not_from_manifest"):
        ctx["toolchain"]["compilerVersion"] = "5.6.4"
    if m.get("tool_outside_closure"):
        ctx["toolClosure"]["compiler"] = "0" * 64

    uni = {"schemaVersion": 2, "languageMode": "js-allowjs", "configOrigin": "tsconfig",
           "synthesizerVersion": None, "synthesizedOptions": None,
           "packageModuleType": "commonjs", "allowJs": True, "checkJs": False,
           "jsAdmittedToProgram": True, "jsDiagnosticsEnabled": False,
           "resolutionCompletenessImplied": False,
           "jsRootFiles": ["src/util.js"],
           "programRootFiles": ["src/a.ts", "src/util.js"],
           "lockfileKind": "package-lock", "nodeModulesInReadSet": True,
           "executionCapableResolution": False,
           "tsconfigGraphHash": graph_digest, "nativeContextId": None}
    if m.get("universe_contradicts_context"):
        uni["checkJs"] = True

    A = assemble.Assembly(
        fx, capabilities=["inventory", "syntax", "clones-fact", "unresolved-edge"],
        spec_rows=[{"capabilityId": c, "languageMode": "js-allowjs",
                    "workspaceRoot": ".", "required": True}
                   for c in ("inventory", "syntax", "clones-fact", "unresolved-edge")],
        capability_manifest=CAP_MANIFEST)

    ctx_hex = A.add_context("native.context.typescript.v2", ctx,
                            "#/$defs/TypeScriptNativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.typescript.v2", uni,
                             "#/$defs/TypeScriptUniverseV2ResolvedInputs",
                             "typescript-universe")

    A.seal_snapshot()
    A.seal_plan([prov_cid, eval_cid, tool_cid, stdlib_cid])

    # ---- body-language-version, derived, per body ------------------------
    lvb = CL.DOMAIN_SETS["native-semantic-universe"][
        "native.semantic-universe.typescript.v2"]["languageVersionBinding"]

    def clone_fact(path, level, tokens=None, label=""):
        blv, cause = CL.derive_body_language_version(lvb, ctx, uni, path)
        assert blv is not None, cause
        spec = make_level_spec(level)
        lvhex = fx.s.put_raw(spec, "level-spec:" + level)
        src = fx.files[path]
        start = src.index(BODY)
        end = start + len(BODY)
        if level == "L0-verbatim":
            payload = osip.l0_payload(src[start:end])
        else:
            payload = osip.token_stream_payload(tokens)
        lang = blv["languageId"]
        if m.get("clone_wrong_language_id") and path.endswith(".js"):
            lang = "typescript"      # the PROVIDER's language, not the BODY's
        if m.get("clone_l0_payload_not_span") and level == "L0-verbatim":
            payload = osip.l0_payload(b"different body bytes")
        bid, frame = osip.body_identity(level, lvhex, lang, blv, payload)
        fx.s.blobs[bid.split(":")[1]] = frame
        if m.get("clone_level_spec_not_retained"):
            fx.s.blobs.pop(lvhex, None)
        declared_lv = lvhex
        if m.get("clone_wrong_level_version"):
            declared_lv = fx.s.put_raw(make_level_spec(level) + b"#drift\n",
                                       "level-spec-drift")
        p = {"bodyIdentity": bid, "normalisationLevel": level,
             "normalisationVersion": declared_lv}
        anchors = [{"path": path, "blobDigest": inv[path]["sha256"],
                    "startByte": start, "endByte": end}]
        if m.get("clone_two_anchors"):
            anchors = anchors + [{"path": path, "blobDigest": inv[path]["sha256"],
                                  "startByte": 0, "endByte": 1}]
        return A.add_fact("clones", "normalized-body-hash", uni_hex, uni_hex, prov_cid, p,
                          anchors, label=label), blv, bid

    # ---- facts ----------------------------------------------------------
    file_facts = []
    for p, r in sorted(inv.items()):
        payload = {"path": p, "contentSha256": r["sha256"], "byteLength": r["bytes"]}
        anchors = []
        if p == "README.md":
            if m.get("file_fact_wrong_hash"):
                payload["contentSha256"] = "0" * 64
            if m.get("file_fact_wrong_length"):
                payload["byteLength"] = r["bytes"] + 1
            if m.get("file_fact_path_not_inventoried"):
                payload["path"] = "does/not/exist.md"
            if m.get("file_fact_with_anchor"):
                anchors = [{"path": p, "blobDigest": r["sha256"],
                            "startByte": 0, "endByte": 1}]
        file_facts.append(A.add_fact("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                     payload, anchors, label=p))
    pkg_fact = A.add_fact("package", "manifest-declared", uni_hex, uni_hex, prov_cid,
                          {"manifestPath": "package.json", "packageName": "cb-app",
                           "packageVersion": "1.0.0"}, [])
    decl_fact = A.add_fact(
        "declares", "syntactic", uni_hex, uni_hex, prov_cid,
        {"container": "module:src/a.ts", "declared": "function:src/a.ts#add",
         "declarationKind": "function"},
        [] if m.get("declares_without_anchor") else
        [{"path": "src/a.ts", "blobDigest": inv["src/a.ts"]["sha256"],
          "startByte": 0, "endByte": len(A_TS)}])

    ts_clone, ts_blv, ts_bid = clone_fact("src/a.ts", "L0-verbatim", label="ts L0")
    js_clone, js_blv, js_bid = clone_fact("src/util.js", "L0-verbatim", label="js L0")
    l1_tokens = [("keyword", "const"), ("identifier", "total"), ("punct", "="),
                 ("identifier", "a"), ("punct", "+"), ("identifier", "b"),
                 ("punct", ";"), ("keyword", "return"), ("identifier", "total"),
                 ("punct", ";")]
    l1_clone, _, l1_bid = clone_fact("src/a.ts", "L1-lexical", l1_tokens, "ts L1")

    # ---- scopes and Coverage -------------------------------------------
    all_paths = sorted(inv)
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 all_paths)
    c_file = A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(all_paths), "complete"))
    s_pkg, h_pkg = A.add_scope("package", "manifest-declared", uni_hex, uni_hex,
                               prov_cid, ["cb-app"])
    c_pkg = A.add_coverage(s_pkg, h_pkg, coverage_entry(
        "package", "manifest-declared", "sha256:" + h_pkg, 1, "complete"))
    s_dec, h_dec = A.add_scope("declares", "syntactic", uni_hex, uni_hex, prov_cid,
                               ["module:src/a.ts"])
    c_dec = A.add_coverage(s_dec, h_dec, coverage_entry(
        "declares", "syntactic", "sha256:" + h_dec, 1, "complete"))
    s_cl, h_cl = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                             prov_cid, ["src/a.ts", "src/util.js"])
    c_cl = A.add_coverage(s_cl, h_cl, coverage_entry(
        "clones", "normalized-body-hash", "sha256:" + h_cl, 2, "complete"))
    # a clones scope over a path the TypeScript universe reads in NO dialect
    s_bad, h_bad = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                               prov_cid, ["package.json"], label="unsupported variant")
    bad_entry = coverage_entry("clones", "normalized-body-hash", "sha256:" + h_bad, 1,
                               "unknown", deficiency="language-tier-unsupported",
                               cause="capability-missing")
    if m.get("false_complete_unsupported_variant"):
        bad_entry = coverage_entry("clones", "normalized-body-hash",
                                   "sha256:" + h_bad, 1, "complete")
    c_bad = A.add_coverage(s_bad, h_bad, bad_entry)
    s_ue, h_ue = A.add_scope("unresolved-edge", "observed", uni_hex, uni_hex, prov_cid, [])
    c_ue = A.add_coverage(s_ue, h_ue, coverage_entry(
        "unresolved-edge", "observed", "sha256:" + h_ue, 0, "complete"))

    extra_scopes, extra_covs = [], []
    if m.get("partition_overlap"):
        s_ov, h_ov = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                                 prov_cid, ["src/a.ts"], label="overlapping")
        extra_scopes.append(s_ov)
        extra_covs.append(A.add_coverage(s_ov, h_ov, coverage_entry(
            "clones", "normalized-body-hash", "sha256:" + h_ov, 1, "complete")))
    facts = file_facts + [pkg_fact, decl_fact, ts_clone, js_clone, l1_clone]
    if m.get("omit_file_fact"):
        facts = [f for f in facts if f != file_facts[0]]
    view = A.seal_view(prov_cid, [s_file, s_pkg, s_dec, s_cl, s_bad, s_ue] + extra_scopes,
                       facts, [c_file, c_pkg, c_dec, c_cl, c_bad, c_ue] + extra_covs,
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST])
    run_id = A.seal_run(eval_cid, prov_cid, [view])
    A.extra = {"tsBodyIdentity": ts_bid, "jsBodyIdentity": js_bid,
               "l1BodyIdentity": l1_bid,
               "tsBodyLanguageVersion": ts_blv, "jsBodyLanguageVersion": js_blv,
               "contextHex": ctx_hex, "universeHex": uni_hex,
               "bodyBytesIdentical": True}
    return fx, A, run_id
