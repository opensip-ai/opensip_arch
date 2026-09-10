"""RUN-TS: a complete minimal positive TypeScript Run descriptor graph.

Repository shape (chosen by this session):
  package.json                 tsjs marker, module type commonjs
  package-lock.json            lockfile
  project.tsconfig.json        EXPLICITLY SELECTED custom-named entry config
                               extending THREE ordered bases, one REPEATED
  tsconfig.base.json           base (kind `other` by the exact-basename law)
  tsconfig.strict.json         base (kind `other`)
  src/a.ts                     TypeScript body
  src/b.js                     JavaScript body read by the SAME TS engine
  shared/config.base.json      shared base with ANOTHER FILENAME
  web/jsconfig.json            jsconfig entry inheriting that shared base
  web/app.js
  pkg/package.json             marker-only unit -> SYNTHESIZED configuration
  pkg/index.js
  node_modules/left-pad/package.json   pruned from the inventory, retained as a
                                       ResolvedNodeModulesLayoutV1 read-set row
"""

import hashlib

import oslib as O
import graph as G
import build as B
from oslib import C, H, sha256hex, raw_digest

TS_BODY = b"function pad(n: number): string {\n  return String(n);\n}\n"
JS_BODY = b"function pad(n) {\n  return String(n);\n}\n"

SRC_A = b"import lp from 'left-pad';\n" + TS_BODY
SRC_B = b"'use strict';\n" + JS_BODY

STDLIB_TREE = {
    "lib.es2022.d.ts": b"declare const es2022Marker: unique symbol;\n",
    "lib.dom.d.ts": b"declare const domMarker: unique symbol;\n",
}
COMPILER_TREE = {
    "bin/tsc.js": b"#!/usr/bin/env node\n// bundled first-party compiler\n",
    "bin/node": b"\x7fELF-not-really-a-runtime\n",
}


def honored(lib=("es2022",), allow_js=False, check_js=False,
            module="node16", mr="node16", jsx=None):
    return {"allowJs": allow_js, "checkJs": check_js, "module": module,
            "moduleResolution": mr, "target": "es2022", "strict": True,
            "skipLibCheck": True, "noEmit": True, "types": [],
            "lib": list(lib), "baseUrl": None, "paths": [], "rootDirs": [],
            "resolveJsonModule": False, "allowSyntheticDefaultImports": True,
            "esModuleInterop": True, "customConditions": [],
            "jsx": jsx}


def build(mutate=None):
    """mutate: name of a single-field negative mutation, or None."""
    mutate = mutate or ""
    kit = B.Kit()
    w = kit.w
    lv = B.retain_level_specs(kit)

    # ---- repository -----------------------------------------------------
    f_pkg = kit.file("package.json", '{"name":"app","version":"1.0.0"}\n')
    f_lock = kit.file("package-lock.json", '{"lockfileVersion":3}\n')
    f_entry = kit.file("project.tsconfig.json",
                       '{"extends":["./tsconfig.base.json",'
                       '"./tsconfig.strict.json","./tsconfig.base.json"]}\n')
    f_base = kit.file("tsconfig.base.json", '{"compilerOptions":{"target":"es2022"}}\n')
    f_strict = kit.file("tsconfig.strict.json", '{"compilerOptions":{"strict":true}}\n')
    f_a = kit.file("src/a.ts", SRC_A)
    f_b = kit.file("src/b.js", SRC_B)
    f_sh = kit.file("shared/config.base.json", '{"compilerOptions":{"allowJs":true}}\n')
    f_web = kit.file("web/jsconfig.json", '{"extends":"../shared/config.base.json"}\n')
    f_webapp = kit.file("web/app.js", JS_BODY)
    f_pkg2 = kit.file("pkg/package.json", '{"name":"leaf","private":true}\n')
    f_idx = kit.file("pkg/index.js", JS_BODY)

    # node_modules is PRUNED from the inventory but its manifest bytes are in
    # the read set and retained (native S1.4 U-4a / S2.2).
    nm_bytes = b'{"name":"left-pad","version":"1.3.0","main":"index.js"}\n'
    nm_digest = w.raw(nm_bytes)
    layout = {"schemaVersion": 1, "entries": [
        {"packageName": "left-pad", "packageVersion": "1.3.0",
         "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad",
         "contentSha256": nm_digest}]}
    layout_digest = w.record(layout)

    # ---- closures --------------------------------------------------------
    std_id, std_desc = kit.closure("stdlib", STDLIB_TREE, "5.6.2")
    tool_id, tool_desc = kit.closure("toolchain", COMPILER_TREE, "5.6.2")
    prov_id, _ = kit.closure("provider", {"bin/tsprovider": b"provider\n"},
                             "2.0.0", protocol_major=2)
    eval_id, _ = kit.closure("evaluator", {"bin/eval": b"evaluator\n"}, "1.0.0")
    det_id, _ = kit.closure("detector", {"rules/inv.json": b"{}\n"}, "1.0.0")

    tool_members = {r["sha256"]: r["path"] for r in tool_desc["tree"]}
    compiler_digest = [d for d, p in tool_members.items() if p == "bin/tsc.js"][0]
    runtime_digest = [d for d, p in tool_members.items() if p == "bin/node"][0]
    std_components = sorted(
        [{"component": r["path"], "sha256": r["sha256"]} for r in std_desc["tree"]],
        key=lambda x: x["component"].encode())
    if mutate == "stdlib-inventory-incomplete":
        std_components = [c for c in std_components if c["component"] != "lib.dom.d.ts"]

    def toolchain(lib=("es2022",)):
        return {"compilerName": "typescript",
                "compilerVersion": "5.6.2" if mutate != "compiler-version-not-from-manifest"
                                   else "9.9.9",
                "compilerPackageDigest": compiler_digest,
                "typescriptStdlibMerkleRoot": std_id.split(":", 1)[1],
                "standardLibraryComponentDigests": std_components,
                "libSelection": sorted(lib)}

    toolclosure = {"compiler": compiler_digest, "runtime": runtime_digest,
                   "closureId": tool_id}

    def projection(paths, ho):
        return {"schemaVersion": 2, "ancestorCarrierVerified": True,
                "environmentSanitized": True, "typeAcquisitionEnabled": False,
                "executableSelected": False, "honoredOptions": ho,
                "strippedOptions": [
                    {"option": "outDir", "reason": "emits-output"}],
                "configGraphPaths": sorted(paths)}

    # ---- context 1: the ordinary project with node_modules ---------------
    ho1 = honored()
    ctx1 = {"schemaVersion": 2, "languageMode": "ts-tsconfig",
            "toolchain": toolchain(), "toolClosure": toolclosure,
            "configProjection": projection(
                ["project.tsconfig.json", "tsconfig.base.json",
                 "tsconfig.strict.json"], ho1),
            "moduleResolutionMode": "node16", "packageModuleType": "commonjs",
            "nodeModulesLayoutDigest": layout_digest,
            "lockfileIdentity": {"kind": "package-lock", "path": "package-lock.json",
                                 "contentSha256": f_lock["sha256"]}}
    if mutate == "lockfile-outside-snapshot":
        ctx1["lockfileIdentity"]["path"] = "vendor/package-lock.json"
    ctx1_ref, ctx1_hx = kit.mint_native("native.context.typescript.v2", ctx1)

    # ---- context 2: jsconfig entry inheriting a shared differently-named base
    ho2 = honored(allow_js=True, check_js=False)
    ctx2 = {"schemaVersion": 2, "languageMode": "js-allowjs",
            "toolchain": toolchain(), "toolClosure": toolclosure,
            "configProjection": projection(
                ["shared/config.base.json", "web/jsconfig.json"], ho2),
            "moduleResolutionMode": "node16", "packageModuleType": "absent",
            "nodeModulesLayoutDigest": None, "lockfileIdentity": None}
    ctx2_ref, ctx2_hx = kit.mint_native("native.context.typescript.v2", ctx2)

    # ---- context 3: synthesized configuration ----------------------------
    ho3 = honored(allow_js=True)
    ctx3 = {"schemaVersion": 2, "languageMode": "js-synthesized",
            "toolchain": toolchain(), "toolClosure": toolclosure,
            "configProjection": projection([], ho3),
            "moduleResolutionMode": "node16", "packageModuleType": "absent",
            "nodeModulesLayoutDigest": None, "lockfileIdentity": None}
    ctx3_ref, ctx3_hx = kit.mint_native("native.context.typescript.v2", ctx3)

    # ---- config graphs ---------------------------------------------------
    def node(path, blob, extends):
        k = G._config_node_kind(path)
        if mutate == "config-node-kind-relabelled" and path == "tsconfig.base.json":
            k = "tsconfig"
        return {"path": path, "contentSha256": blob["sha256"], "kind": k,
                "extendsResolved": extends}

    graph1 = {"schemaVersion": 1, "entryConfigPath": "project.tsconfig.json",
              "nodes": sorted([
                  node("project.tsconfig.json", f_entry,
                       ["tsconfig.base.json", "tsconfig.strict.json",
                        "tsconfig.base.json"]),
                  node("tsconfig.base.json", f_base, []),
                  node("tsconfig.strict.json", f_strict, [])],
                  key=lambda n: n["path"].encode())}
    g1d = w.record(graph1)
    graph2 = {"schemaVersion": 1, "entryConfigPath": "web/jsconfig.json",
              "nodes": sorted([
                  node("web/jsconfig.json", f_web, ["shared/config.base.json"]),
                  node("shared/config.base.json", f_sh, [])],
                  key=lambda n: n["path"].encode())}
    g2d = w.record(graph2)
    graph3 = {"schemaVersion": 1, "entryConfigPath": None, "nodes": []}
    g3d = w.record(graph3)

    # ---- universes -------------------------------------------------------
    def universe(mode, origin, ctx_ref, graph_digest, roots, js_roots,
                 allow_js, lockkind, nm, synth=None):
        u = {"schemaVersion": 2, "languageMode": mode, "configOrigin": origin,
             "synthesizerVersion": 1 if mode == "js-synthesized" else None,
             "synthesizedOptions": synth, "packageModuleType":
                 "commonjs" if mode == "ts-tsconfig" else "absent",
             "allowJs": allow_js, "checkJs": False,
             "jsAdmittedToProgram": allow_js, "jsDiagnosticsEnabled": False,
             "resolutionCompletenessImplied": False,
             "jsRootFiles": sorted(js_roots), "programRootFiles": sorted(roots),
             "lockfileKind": lockkind, "nodeModulesInReadSet": nm,
             "executionCapableResolution": False,
             "tsconfigGraphHash": graph_digest, "nativeContextId": ctx_ref}
        return kit.mint_native("native.semantic-universe.typescript.v2", u) + (u,)

    u1_ref, u1_hx, u1 = universe("ts-tsconfig", "tsconfig", ctx1_ref, g1d,
                                 ["src/a.ts"], [], False, "package-lock", True)
    u2_ref, u2_hx, u2 = universe("js-allowjs", "jsconfig", ctx2_ref, g2d,
                                 ["web/app.js"], ["web/app.js"], True, "none",
                                 False)
    synth = {"allowJs": True, "checkJs": False, "module": "node16",
             "moduleResolution": "node16", "target": "es2022", "strict": False,
             "skipLibCheck": True, "types": [], "noEmit": True}
    u3_ref, u3_hx, u3 = universe("js-synthesized", "synthesized", ctx3_ref, g3d,
                                 ["pkg/index.js"], ["pkg/index.js"], True,
                                 "none", False, synth)

    # ---- configuration / scope / spec / grant ----------------------------
    scope_desc = {"schemaVersion": 2, "workspaceRoots": sorted([".", "pkg", "web"]),
                  "pathPrefixes": [], "excludedPathPrefixes": sorted(
                      [".git", "node_modules", "pkg/node_modules",
                       "web/node_modules"])}
    budget = {"unit": "work-units", "limit": 100000}
    config = {"analysis": {"profileId": "default",
                           "capabilities": sorted(["inventory", "syntax",
                                                   "clones-fact", "imports"]),
                           "budget": dict(budget)},
              "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    if mutate == "plan-budget-contradicts-config":
        budget = {"unit": "work-units", "limit": 99999}
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted(
                [{"capabilityId": c, "languageMode": m, "workspaceRoot": r,
                  "required": True}
                 for c, m, r in [("inventory", "ts-tsconfig", "."),
                                 ("syntax", "ts-tsconfig", "."),
                                 ("clones-fact", "ts-tsconfig", "."),
                                 ("imports", "ts-tsconfig", "."),
                                 ("inventory", "js-allowjs", "web"),
                                 ("inventory", "js-synthesized", "pkg")]],
                key=lambda x: C(x)),
            "policyPackIds": ["opensip.builtin"],
            "parameters": []}
    grant = {"schemaVersion": 2, "projectId": w.projectId,
             "principals": [{"kind": "first-party", "closureId": prov_id,
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(["read-source", "native-analysis"]),
             "scopeDigest": w.record(scope_desc)}

    snap_id, snap = kit.snapshot(config, scope_desc)
    inv_by_path = {r["path"]: r for r in snap["sourceInventory"]}

    # ---- capability manifest --------------------------------------------
    providers = [{"providerId": "typescript-semantic", "language": "typescript",
                  "providerVersionSource": "signed-closure-manifest",
                  "toolchainIdentitySource": "native-context-v2",
                  "relations": {"file": "enumerated", "declares": "syntactic",
                                "clones": "normalized-body-hash",
                                "imports": "resolved-target",
                                "unresolved-edge": "observed"},
                  "platformIds": ["macos-aarch64"]}]
    cm, cm_bytes, cm_bytes_digest, cap_id = B.capability_manifest(kit, providers)

    policy, pd, waivers, wd, program, rpd, rule = B.policy_and_program(kit)

    plan_id, plan_desc = B.plan(
        kit, snap_id, cm_bytes_digest, cap_id,
        [prov_id, eval_id, det_id], w.record(spec), w.record(config),
        [ctx1_hx, ctx2_hx, ctx3_hx] if mutate != "plan-omits-a-retained-context"
        else [ctx1_hx, ctx2_hx],
        [], pd, wd, w.record(scope_desc), budget, w.record(grant))

    # ---- facts -----------------------------------------------------------
    facts = []
    file_subjects = []
    for row in snap["sourceInventory"]:
        p = {"path": row["path"], "contentSha256": row["sha256"],
             "byteLength": row["bytes"]}
        if mutate == "file-payload-digest-wrong" and row["path"] == "src/a.ts":
            p["contentSha256"] = sha256hex(b"not the bytes")
        anchors = []
        if mutate == "inventory-fact-carries-an-anchor" and row["path"] == "src/a.ts":
            anchors = [{"path": "src/a.ts", "blobDigest": f_a["sha256"],
                        "startByte": 0, "endByte": 3}]
        fid, _ = kit.fact(snap_id, "file", "enumerated", u1_hx, u1_hx, prov_id,
                          p, anchors)
        facts.append(fid)
        file_subjects.append(row["path"])
    if mutate == "totality-omits-an-inventoried-path":
        facts = facts[1:]

    # declares@syntactic over src/a.ts
    dec_anchors = [{"path": "src/a.ts", "blobDigest": f_a["sha256"],
                    "startByte": 26, "endByte": 26 + len(TS_BODY)}]
    if mutate == "unanchored-code-fact":
        dec_anchors = []
    dec_id, _ = kit.fact(snap_id, "declares",
                         "resolved-callee" if mutate == "rung-of-another-relation"
                         else "syntactic",
                         u1_hx, u1_hx, prov_id,
                         {"container": "module:src/a.ts",
                          "declared": "function:src/a.ts#pad",
                          "declarationKind": "function"}, dec_anchors)

    # imports@resolved-target: a BARE SPECIFIER resolved through node_modules
    imp_id, _ = kit.fact(snap_id, "imports", "resolved-target", u1_hx, u1_hx,
                         prov_id,
                         {"importer": "module:src/a.ts", "specifier": "left-pad",
                          "resolvedTarget": "module:node_modules/left-pad/index.js"},
                         [{"path": "src/a.ts", "blobDigest": f_a["sha256"],
                           "startByte": 0, "endByte": 26}])

    # ---- clones: L0 + a normalized level, TS body and JS body ------------
    def clone_fact(path, blob, span, level, universe_ref_hx, uni, ctx, retained,
                   tokens=None):
        ident, blv, lang = B.mint_body_identity(
            kit, "native.semantic-universe.typescript.v2", uni, ctx, retained,
            path, span, level, lv[level], tokens)
        payload = {"bodyIdentity": ident, "normalisationLevel": level,
                   "normalisationVersion": lv[level]}
        anchors = [{"path": path, "blobDigest": blob["sha256"],
                    "startByte": blob_span(blob, span)[0],
                    "endByte": blob_span(blob, span)[1]}]
        fid, _ = kit.fact(snap_id, "clones", "normalized-body-hash",
                          universe_ref_hx, universe_ref_hx, prov_id, payload,
                          anchors)
        return fid, ident, lang, blv

    def blob_span(blob, span):
        data = w.cas[blob["sha256"]]
        i = data.index(span)
        return i, i + len(span)

    ts_l0, ts_l0_id, ts_lang, ts_blv = clone_fact(
        "src/a.ts", f_a, TS_BODY, "L0-verbatim", u1_hx, u1, ctx1, {})
    ts_l1, ts_l1_id, _, _ = clone_fact(
        "src/a.ts", f_a, TS_BODY, "L1-lexical", u1_hx, u1, ctx1, {},
        tokens=[("kw", "function"), ("ident", "pad"), ("punct", "("),
                ("ident", "n"), ("punct", ")"), ("punct", "{"),
                ("kw", "return"), ("ident", "String"), ("punct", "("),
                ("ident", "n"), ("punct", ")"), ("punct", ";"),
                ("punct", "}")])
    js_l0, js_l0_id, js_lang, js_blv = clone_fact(
        "src/b.js", f_b, JS_BODY, "L0-verbatim", u1_hx, u1, ctx1, {})

    # ---- scopes ----------------------------------------------------------
    fs_id, fs_hx, fs = kit.scope(snap_id, u1_hx, u1_hx, "file", "enumerated",
                                 prov_id, file_subjects)
    ds_id, ds_hx, ds = kit.scope(snap_id, u1_hx, u1_hx, "declares", "syntactic",
                                 prov_id, ["symbol:function:src/a.ts#pad"])
    cs_id, cs_hx, cs = kit.scope(snap_id, u1_hx, u1_hx, "clones",
                                 "normalized-body-hash", prov_id,
                                 ["src/a.ts", "src/b.js"])
    is_id, is_hx, isc = kit.scope(snap_id, u1_hx, u1_hx, "imports",
                                  "resolved-target", prov_id,
                                  ["symbol:module:src/a.ts"])
    scopes = [(fs_id, fs_hx, fs), (ds_id, ds_hx, ds), (cs_id, cs_hx, cs),
              (is_id, is_hx, isc)]
    extra_scope = []
    if mutate == "partition-overlap":
        ov_id, ov_hx, ov = kit.scope(snap_id, u1_hx, u1_hx, "declares",
                                     "syntactic", prov_id,
                                     ["symbol:function:src/a.ts#pad"] )
        # a second scope of the SAME owning tuple sharing a subject requires a
        # different subject set to be a distinct object: add one and overlap.
        ov_id, ov_hx, ov = kit.scope(snap_id, u1_hx, u1_hx, "declares",
                                     "syntactic", prov_id,
                                     ["symbol:function:src/a.ts#pad",
                                      "symbol:function:src/a.ts#other"])
        extra_scope = [(ov_id, ov_hx, ov)]

    # ---- coverage --------------------------------------------------------
    covs = []
    fc = kit.coverage(fs_id, fs_hx, fs, B.entry_complete())
    covs.append(fc)
    covs.append(kit.coverage(ds_id, ds_hx, ds, B.entry_complete()))
    covs.append(kit.coverage(cs_id, cs_hx, cs, B.entry_complete()))
    covs.append(kit.coverage(
        is_id, is_hx, isc,
        B.entry_complete(resolutionCompleteness={
            "state": "complete", "attempted": True, "examinedExhaustive": True,
            "stageTerminal": "complete", "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": []})))
    for sid, shx, sd in extra_scope:
        covs.append(kit.coverage(sid, shx, sd, B.entry_complete()))

    # ---- view / evidence / proof / seal / run ----------------------------
    all_facts = facts + [dec_id, imp_id, ts_l0, ts_l1, js_l0]
    view_id, view = kit.view(
        plan_id, [s[0] for s in scopes + extra_scope], all_facts,
        [c[0] for c in covs], prov_id,
        [G.REL_DOC_DIGEST, G.NATIVE_DOC_DIGEST])

    exec_plan_id = B.build_exec_plan(kit, plan_id, prov_id)
    extra_inputs = [
        {"domain": "policy", "digest": pd},
        {"domain": "waiver", "digest": wd},
        {"domain": "analysis-spec", "digest": w.record(spec)},
        {"domain": "configuration", "digest": w.record(config)},
        {"domain": "capability-manifest", "digest": cap_id},
        {"domain": "native-context", "digest": ctx1_hx},
        {"domain": "schema", "digest": G.NATIVE_DOC_DIGEST}]
    proof_id, finding_ids = B.build_proof(
        kit, plan_id, exec_plan_id, eval_id, det_id, rule, rpd, view_id,
        facts[0] if facts else all_facts[0], fc[0], extra_inputs)
    ev_id = B.evidence(kit, plan_id, [view_id], [c[0] for c in covs], [],
                       finding_ids, proof_id)
    seal_id, run_id = B.seal_and_run(kit, plan_id, exec_plan_id, ev_id, eval_id,
                                     pd, proof_id, snap_id, cap_id)

    # single-field frame/preimage mutations applied AFTER minting
    if mutate == "raw-payload-offered-as-an-h-identity":
        w.cas[ctx1_hx] = C(ctx1)
    if mutate == "altered-frame":
        bad = dict(ctx1)
        bad["packageModuleType"] = "module"
        w.cas[ctx1_hx] = O.h_frame("native.context.typescript.v2", bad)
    if mutate == "missing-preimage":
        del w.cas[ctx1_hx]
    if mutate == "unregistered-h-domain":
        w.cas[ctx1_hx] = O.h_frame("native.context.made-up.v9", ctx1)
    if mutate == "clone-level-specification-not-retained":
        del w.cas[lv["L0-verbatim"]]

    return dict(kit=kit, run=run_id, plan=plan_id, snapshot=snap_id,
                universes={"main": u1_hx, "web": u2_hx, "pkg": u3_hx},
                contexts={"main": ctx1_hx, "web": ctx2_hx, "pkg": ctx3_hx},
                bodyIdentities={"ts-a.ts@L0": ts_l0_id, "ts-a.ts@L1": ts_l1_id,
                                "js-b.js@L0": js_l0_id},
                bodyLanguages={"src/a.ts": ts_lang, "src/b.js": js_lang},
                bodyLanguageVersions={"src/a.ts": ts_blv, "src/b.js": js_blv},
                capabilityManifestId=cap_id, view=view_id, evidence=ev_id,
                seal=seal_id, facts=all_facts, coverages=[c[0] for c in covs],
                scopes=[s[0] for s in scopes])
