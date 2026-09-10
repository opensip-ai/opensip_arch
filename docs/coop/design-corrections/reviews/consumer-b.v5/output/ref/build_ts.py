"""TypeScript / JavaScript reconstruction vectors."""

from __future__ import annotations

import hashlib
import json

import opensip_ref as R
import closure as CL
import world as W
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes

L0_SPEC = b"OPENSIP-LEVEL-SPEC L0-verbatim: no tokenisation; raw body span bytes.\n"
L1_SPEC = (b"OPENSIP-LEVEL-SPEC L1-lexical v1\n"
           b"token-kind-registry: kw,id,punct,str,num\n"
           b"boundary-rules: ts/js/rust lexical\n"
           b"transform-order: strip-insignificant-whitespace, normalise-line-endings\n"
           b"replacement-bytes: none\n")


def ts_context(g, closures, *, language_mode, config_projection, module_resolution,
               package_module_type, node_modules_layout_digest, lockfile_identity,
               lib_selection=("es2022",)):
    tool = g.closures[closures["ts-toolchain"]]
    stdlib = g.closures[closures["ts-stdlib"]]
    comp = next(b["sha256"] for b in tool["tree"] if b["path"] == "bin/tsc.js")
    runtime = next(b["sha256"] for b in tool["tree"] if b["path"] == "bin/node")
    decls = sorted(
        [{"component": b["path"].rsplit("/", 1)[-1], "sha256": b["sha256"]}
         for b in stdlib["tree"] if b["path"].endswith(".d.ts")],
        key=lambda r: r["component"].encode("utf-8"),
    )
    ctx = {
        "schemaVersion": 2,
        "languageMode": language_mode,
        "toolchain": {
            "compilerName": "typescript",
            "compilerVersion": tool["semanticVersion"],
            "compilerPackageDigest": comp,
            "typescriptStdlibMerkleRoot": closures["ts-stdlib"][len("closure2:"):],
            "standardLibraryComponentDigests": decls,
            "libSelection": sorted(lib_selection),
        },
        "toolClosure": {"compiler": comp, "runtime": runtime,
                        "closureId": closures["ts-toolchain"]},
        "configProjection": config_projection,
        "moduleResolutionMode": module_resolution,
        "packageModuleType": package_module_type,
        "nodeModulesLayoutDigest": node_modules_layout_digest,
        "lockfileIdentity": lockfile_identity,
    }
    R.validate("native", "#/$defs/TypeScriptNativeContextV2", ctx)
    return ctx


def honored(**over):
    base = {
        "allowJs": False, "checkJs": False, "module": "node16",
        "moduleResolution": "node16", "target": "es2022", "strict": True,
        "skipLibCheck": True, "noEmit": True, "types": [], "lib": ["es2022"],
        "baseUrl": None, "paths": [], "rootDirs": [], "resolveJsonModule": False,
        "allowSyntheticDefaultImports": True, "esModuleInterop": True,
        "customConditions": [], "jsx": None,
    }
    base.update(over)
    return base


def config_projection(paths, honored_options, stripped=()):
    cp = {
        "schemaVersion": 2,
        "ancestorCarrierVerified": True,
        "environmentSanitized": True,
        "typeAcquisitionEnabled": False,
        "executableSelected": False,
        "honoredOptions": honored_options,
        "strippedOptions": list(stripped),
        "configGraphPaths": sorted(paths, key=lambda p: p.encode("utf-8")),
    }
    R.validate("native", "#/$defs/TypeScriptConfigProjectionV2", cp)
    return cp


def config_graph(entry, nodes):
    cg = {"schemaVersion": 1, "entryConfigPath": entry,
          "nodes": sorted(nodes, key=lambda n: n["path"].encode("utf-8"))}
    R.validate("native", "#/$defs/TypeScriptConfigGraphV1", cg)
    return cg


def ts_universe(g, ctx, cg, *, language_mode, config_origin, package_module_type,
                program_roots, js_roots, lockfile_kind, node_modules_in_read_set,
                synthesized=None, allow_js=None, check_js=None):
    hon = ctx["configProjection"]["honoredOptions"]
    u = {
        "schemaVersion": 2,
        "languageMode": language_mode,
        "configOrigin": config_origin,
        "synthesizerVersion": 1 if synthesized else None,
        "synthesizedOptions": synthesized,
        "packageModuleType": package_module_type,
        "allowJs": hon["allowJs"] if allow_js is None else allow_js,
        "checkJs": hon["checkJs"] if check_js is None else check_js,
        "jsAdmittedToProgram": hon["allowJs"],
        "jsDiagnosticsEnabled": hon["checkJs"],
        "resolutionCompletenessImplied": False,
        "jsRootFiles": list(js_roots),
        "programRootFiles": list(program_roots),
        "lockfileKind": lockfile_kind,
        "nodeModulesInReadSet": node_modules_in_read_set,
        "executionCapableResolution": False,
        "tsconfigGraphHash": raw(cg),
        "nativeContextId": sha256_text("native.context.typescript.v2", ctx),
    }
    R.validate("native", "#/$defs/TypeScriptUniverseV2ResolvedInputs", u)
    return u


def body_id(g, universe_hex, path, start, end, level, spec_bytes, retained):
    bl = CL.body_language_version(g, universe_hex, path, retained)
    lv32 = R.language_version_raw32(bl)
    lev32 = hashlib.sha256(spec_bytes).digest()
    span = g.blobs[path][start:end]
    if level == "L0-verbatim":
        payload = R.body_payload_L0(span)
    else:
        toks = [("id", t) for t in span.decode().split() if t]
        payload = R.body_payload_tokens(toks)
    pre, bid = R.body_identity(level, lev32, bl["languageId"], lv32, payload)
    g.cas.put_bytes(pre)
    g.cas.put_bytes(spec_bytes)
    return bid, bl, lev32.hex(), pre


# ---------------------------------------------------------------------------


TS_BODY = b"function pad(n) {\n  return n + 1;\n}\n"


def scenario_ordinary(results):
    """TS-1: ordinary TypeScript project that reads node_modules and resolves bare
    specifiers, with its retained configuration graph and dependency layout, plus a
    JavaScript clone body through the SAME TypeScript analyzer universe."""
    g = CL.Graph("ts-ordinary")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]

    a_ts = b"export function alpha(): number {\n  return 1;\n}\n" + TS_BODY
    legacy_js = b"// legacy\n" + TS_BODY
    files = {
        "package.json": b'{"name":"app","version":"1.0.0","type":"module","private":true}\n',
        "package-lock.json": b'{"lockfileVersion":3}\n',
        "src/a.ts": a_ts,
        "src/b.ts": b"import pad from 'left-pad';\nexport const x = pad;\n",
        "src/legacy.js": legacy_js,
        "tsconfig.json": b'{"compilerOptions":{"allowJs":true,"module":"node16"}}\n',
    }
    caps = ["inventory", "syntax", "imports", "references", "calls", "types",
            "reachability", "clones-fact", "clones-near", "clones-cross-tsjs",
            "unresolved-edge"]
    cfg = W.resolved_config(caps)
    sd = W.scope_descriptor(["."], excluded=["node_modules", ".git"])
    W.build_snapshot(g, files, sd, cfg)

    # node_modules is PRUNED from the snapshot; the layout is a retained read-set
    # observation joined by digest, never an inventory row (native section 2.2).
    lp_manifest = b'{"name":"left-pad","version":"1.3.0","main":"index.js"}\n'
    g.cas.put_bytes(lp_manifest)
    layout = {
        "schemaVersion": 1,
        "entries": [
            {"packageName": "left-pad", "packageVersion": "1.3.0",
             "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad",
             "contentSha256": raw_bytes(lp_manifest)},
        ],
    }
    R.validate("native", "#/$defs/ResolvedNodeModulesLayoutV1", layout)
    g.cas.put_record(layout)

    hon = honored(allowJs=True, checkJs=False)
    cp = config_projection(["tsconfig.json"], hon,
                           stripped=[{"option": "outDir", "reason": "emits-output"}])
    lock = {"kind": "package-lock", "path": "package-lock.json",
            "contentSha256": g.inv_row("package-lock.json")["sha256"]}
    ctx = ts_context(g, cl, language_mode="js-allowjs", config_projection=cp,
                     module_resolution="node16", package_module_type="module",
                     node_modules_layout_digest=raw(layout), lockfile_identity=lock)
    ctx_hex = g.add_context("native.context.typescript.v2", ctx)

    cg = config_graph("tsconfig.json", [
        {"path": "tsconfig.json", "contentSha256": g.inv_row("tsconfig.json")["sha256"],
         "kind": "tsconfig", "extendsResolved": []},
    ])
    g.cas.put_record(cg)
    u = ts_universe(g, ctx, cg, language_mode="js-allowjs", config_origin="tsconfig",
                    package_module_type="module",
                    program_roots=["src/a.ts", "src/b.ts", "src/legacy.js"],
                    js_roots=["src/legacy.js"], lockfile_kind="package-lock",
                    node_modules_in_read_set=True)
    uh = g.add_universe("native.semantic-universe.typescript.v2", u)
    retained = {uh: {"configGraph": cg, "nodeModulesLayout": layout}}

    manifest = W.capability_manifest(
        "default",
        [{"providerId": "typescript-semantic", "language": "typescript",
          "providerVersionSource": "release-manifest:typescript-semantic",
          "toolchainIdentitySource": "native-context:typescript-v2",
          "relations": {"declares": "syntactic", "file": "enumerated",
                        "references": "resolved-binding", "imports": "resolved-target",
                        "clones": "normalized-body-hash"},
          "platformIds": ["all-supported"]}],
        [],
    )
    policy = W.simple_policy("no-unused-export", "references", "resolved-binding", op="none")
    g.rule_program = W.compile_program(policy)
    g.cas.put_record(g.rule_program)
    spec = W.analysis_spec([
        {"capabilityId": c, "languageMode": "js-allowjs", "workspaceRoot": ".", "required": True}
        for c in caps if R.CELLS[(c, "js-allowjs")]["state"] != "NOT-SELECTED"
    ])
    grant = W.semantic_grant(["read-source", "native-analysis"], raw(sd))
    plan_id = W.build_plan(g, [cl["provider-ts"], cl["evaluator"], cl["detector"]],
                           [ctx_hex], spec, grant, policy, W.EMPTY_WAIVERS, manifest)

    prov = cl["provider-ts"]
    facts, scopes, covs = [], [], []

    # inventory class: EXACTLY ZERO anchors, joined by the relation snapshotJoins
    file_subjects = [r["path"] for r in g.inventory]
    sid, sc = W.make_scope(g, "file", "enumerated", uh, uh, prov, file_subjects)
    scopes.append(sid)
    for row in g.inventory:
        p = {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}
        fid, _ = W.make_fact(g, "file", "enumerated", uh, uh, prov, p, anchors=[])
        facts.append(fid)
    cid, _ = W.make_coverage(g, sid, sc, W.entry("file", "enumerated", "complete",
                                                 "not-applicable", False, True, None))
    covs.append(cid)

    sid2, sc2 = W.make_scope(g, "package", "manifest-declared", uh, uh, prov, ["app"])
    scopes.append(sid2)
    fid, _ = W.make_fact(g, "package", "manifest-declared", uh, uh, prov,
                         {"packageName": "app", "packageVersion": "1.0.0",
                          "manifestPath": "package.json"}, anchors=[])
    facts.append(fid)
    cid2, _ = W.make_coverage(g, sid2, sc2, W.entry("package", "manifest-declared", "complete",
                                                    "not-applicable", False, True, None))
    covs.append(cid2)

    # references@resolved-binding: RC-3 honest entry (complete examination, incomplete
    # resolution, no deficiency, nativeCause null by design)
    ref_subject = "symbol:src/a.ts#alpha"
    edge_subject = "symbol:src/b.ts#dyn"
    sid3, sc3 = W.make_scope(g, "references", "resolved-binding", uh, uh, prov,
                             [ref_subject, edge_subject])
    scopes.append(sid3)
    fid, _ = W.make_fact(g, "references", "resolved-binding", uh, uh, prov,
                         {"referrer": "symbol:src/b.ts#x", "name": "alpha",
                          "resolvedBinding": ref_subject},
                         anchors=[W.anchor(g, "src/b.ts", 0, 27)])
    facts.append(fid)
    ue_payload = {"referrer": edge_subject, "relation": "references",
                  "edgeKind": "computed-member-access", "targetScope": "module",
                  "targetModule": "src/a.ts", "detail": "m[k] with runtime key"}
    fid_ue, _ = W.make_fact(g, "unresolved-edge", "observed", uh, uh, prov, ue_payload,
                            anchors=[W.anchor(g, "src/b.ts", 0, 27)])
    facts.append(fid_ue)
    cid3, _ = W.make_coverage(g, sid3, sc3, W.entry(
        "references", "resolved-binding", "complete", "incomplete", True, True, "complete",
        edge_count=1, edge_classes=["computed-member-access"],
        exports_closed="open", external="possible", dead_code=False))
    covs.append(cid3)

    sid4, sc4 = W.make_scope(g, "unresolved-edge", "observed", uh, uh, prov, [edge_subject])
    scopes.append(sid4)
    cid4, _ = W.make_coverage(g, sid4, sc4, W.entry(
        "unresolved-edge", "observed", "complete", "complete", True, True, "complete"))
    covs.append(cid4)

    # clones: a TypeScript body and a JavaScript body with the SAME bytes.
    ts_start = a_ts.index(TS_BODY)
    ts_end = ts_start + len(TS_BODY)
    js_start = legacy_js.index(TS_BODY)
    js_end = js_start + len(TS_BODY)
    bid_ts, bl_ts, lev0, _ = body_id(g, uh, "src/a.ts", ts_start, ts_end,
                                     "L0-verbatim", L0_SPEC, retained[uh])
    bid_js, bl_js, _, _ = body_id(g, uh, "src/legacy.js", js_start, js_end,
                                  "L0-verbatim", L0_SPEC, retained[uh])
    bid_ts_l1, _, lev1, _ = body_id(g, uh, "src/a.ts", ts_start, ts_end,
                                    "L1-lexical", L1_SPEC, retained[uh])
    sid5, sc5 = W.make_scope(g, "clones", "normalized-body-hash", uh, uh, prov,
                             ["src/a.ts", "src/legacy.js"])
    scopes.append(sid5)
    for bid, path, s, e, lev, lvh in (
        (bid_ts, "src/a.ts", ts_start, ts_end, "L0-verbatim", lev0),
        (bid_js, "src/legacy.js", js_start, js_end, "L0-verbatim", lev0),
        (bid_ts_l1, "src/a.ts", ts_start, ts_end, "L1-lexical", lev1),
    ):
        p = {"bodyIdentity": bid, "normalisationLevel": lev, "normalisationVersion": lvh}
        fid, _ = W.make_fact(g, "clones", "normalized-body-hash", uh, uh, prov, p,
                             anchors=[W.anchor(g, path, s, e)])
        facts.append(fid)
    cid5, _ = W.make_coverage(g, sid5, sc5, W.entry("clones", "normalized-body-hash",
                                                    "complete", "not-applicable", False,
                                                    True, None))
    covs.append(cid5)

    vid, _ = W.make_view(g, plan_id, scopes, facts, covs, prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="pass",
                                            scope_ids=[sid3], coverage_ids=[cid3])
    out = CL.close_run(g, retained, [vid], proof, evidence, seal, run)

    results["ts-ordinary"] = {
        "verdict": "ADMIT",
        "runId": out["runId"],
        "planId": plan_id,
        "snapshotId": g.snapshot_id,
        "nativeContextId": u["nativeContextId"],
        "sourceUniverse": uh,
        "capabilityManifestId": g.plan["capabilityManifestId"],
        "tsconfigGraphHash": u["tsconfigGraphHash"],
        "nodeModulesLayoutDigest": ctx["nodeModulesLayoutDigest"],
        "typescriptStdlibMerkleRoot": ctx["toolchain"]["typescriptStdlibMerkleRoot"],
        "bodyIdentityTypeScriptL0": bid_ts,
        "bodyIdentityJavaScriptL0_sameBytes": bid_js,
        "bodyIdentityTypeScriptL1": bid_ts_l1,
        "bodyLanguageVersionTypeScript": bl_ts,
        "bodyLanguageVersionJavaScript": bl_js,
        "factCount": len(g.facts), "scopeCount": len(g.scopes),
        "coverageCount": len(g.coverages),
        "trace": out["trace"],
    }
    return g, uh, retained, plan_id, out


def _minimal_ts_world(files, language_mode, config_origin, cg, cp, *,
                      package_module_type="absent", lockfile=None, layout=None,
                      synthesized=None, program_roots=(), js_roots=(),
                      lockfile_kind="none", caps=("inventory", "syntax")):
    g = CL.Graph("ts-min")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]
    cfg = W.resolved_config(list(caps))
    sd = W.scope_descriptor(["."], excluded=["node_modules", ".git"])
    W.build_snapshot(g, files, sd, cfg)
    # config-graph node digests must be the snapshot's
    cg = dict(cg)
    cg["nodes"] = [dict(n, contentSha256=g.inv_row(n["path"])["sha256"]) for n in cg["nodes"]]
    R.validate("native", "#/$defs/TypeScriptConfigGraphV1", cg)
    g.cas.put_record(cg)
    layout_digest = None
    if layout is not None:
        g.cas.put_record(layout)
        layout_digest = raw(layout)
    lock_id = None
    if lockfile:
        lock_id = {"kind": lockfile, "path": {"package-lock": "package-lock.json"}[lockfile],
                   "contentSha256": g.inv_row("package-lock.json")["sha256"]}
    ctx = ts_context(g, cl, language_mode=language_mode, config_projection=cp,
                     module_resolution=cp["honoredOptions"]["moduleResolution"],
                     package_module_type=package_module_type,
                     node_modules_layout_digest=layout_digest, lockfile_identity=lock_id)
    ctx_hex = g.add_context("native.context.typescript.v2", ctx)
    u = ts_universe(g, ctx, cg, language_mode=language_mode, config_origin=config_origin,
                    package_module_type=package_module_type,
                    program_roots=list(program_roots), js_roots=list(js_roots),
                    lockfile_kind=lockfile_kind,
                    node_modules_in_read_set=layout_digest is not None,
                    synthesized=synthesized)
    uh = g.add_universe("native.semantic-universe.typescript.v2", u)
    retained = {uh: {"configGraph": cg}}
    if layout is not None:
        retained[uh]["nodeModulesLayout"] = layout
    manifest = W.capability_manifest("default", [], [])
    policy = W.simple_policy("r1", "declares", "syntactic", op="none")
    g.rule_program = W.compile_program(policy)
    g.cas.put_record(g.rule_program)
    spec = W.analysis_spec([
        {"capabilityId": c, "languageMode": language_mode, "workspaceRoot": ".",
         "required": True} for c in caps])
    grant = W.semantic_grant(["read-source", "native-analysis"], raw(sd))
    plan_id = W.build_plan(g, [cl["provider-ts"], cl["evaluator"]], [ctx_hex],
                           spec, grant, policy, W.EMPTY_WAIVERS, manifest)
    return g, cl, ctx, ctx_hex, u, uh, retained, plan_id


def _close_inventory_only(g, cl, uh, retained, plan_id, extra_facts=(), extra_scopes=(),
                          extra_covs=()):
    prov = cl["provider-ts"]
    subjects = [r["path"] for r in g.inventory]
    sid, sc = W.make_scope(g, "file", "enumerated", uh, uh, prov, subjects)
    facts = []
    for row in g.inventory:
        p = {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}
        fid, _ = W.make_fact(g, "file", "enumerated", uh, uh, prov, p, anchors=[])
        facts.append(fid)
    cid, _ = W.make_coverage(g, sid, sc, W.entry("file", "enumerated", "complete",
                                                 "not-applicable", False, True, None))
    vid, _ = W.make_view(g, plan_id, [sid] + list(extra_scopes),
                         facts + list(extra_facts), [cid] + list(extra_covs), prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="pass",
                                            scope_ids=[sid], coverage_ids=[cid])
    return CL.close_run(g, retained, [vid], proof, evidence, seal, run)


def scenario_synthesized(results):
    """TS-2: synthesized configuration (js-synthesized), no tsconfig/jsconfig at all."""
    files = {
        "package.json": b'{"name":"tool","version":"0.1.0","private":true}\n',
        "src/index.js": b"export function go() { return 1; }\n",
    }
    syn = {"allowJs": True, "checkJs": False, "module": "node16",
           "moduleResolution": "node16", "target": "es2022", "strict": False,
           "skipLibCheck": True, "types": [], "noEmit": True}
    hon = honored(allowJs=True, checkJs=False, strict=False, skipLibCheck=True,
                  types=[], module="node16", moduleResolution="node16",
                  target="es2022", jsx=None)
    cp = config_projection([], hon)
    cg = config_graph(None, [])
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id = _minimal_ts_world(
        files, "js-synthesized", "synthesized", cg, cp,
        package_module_type="absent", synthesized=syn,
        program_roots=["src/index.js"], js_roots=["src/index.js"])
    out = _close_inventory_only(g, cl, uh, retained, plan_id)
    results["ts-synthesized"] = {
        "verdict": "ADMIT", "runId": out["runId"],
        "configOrigin": "synthesized (derived: entry null and nodes empty)",
        "tsconfigGraphHash": u["tsconfigGraphHash"],
        "nativeContextId": u["nativeContextId"],
        "nodeModulesInReadSet": u["nodeModulesInReadSet"],
        "note": "nodeModulesInReadSet=false: every bare specifier is an "
                "unresolved-module-specifier edge with scope external, never an implicit install",
    }


def scenario_custom_named_multi_base(results):
    """TS-3: explicitly selected CUSTOM-NAMED project config inheriting from several
    ordered bases, including a REPEATED base whose precedence must be retained."""
    files = {
        "config/base.strict.json": b'{"compilerOptions":{"strict":true}}\n',
        "config/base.node.json": b'{"compilerOptions":{"module":"node16"}}\n',
        "package.json": b'{"name":"multi","version":"2.0.0","private":true}\n',
        "src/m.ts": b"export const m = 1;\n",
        "tsconfig.build.json": (b'{"extends":["./config/base.strict.json",'
                                b'"./config/base.node.json","./config/base.strict.json"],'
                                b'"compilerOptions":{}}\n'),
    }
    hon = honored(strict=True, module="node16", moduleResolution="node16")
    cp = config_projection(
        ["config/base.node.json", "config/base.strict.json", "tsconfig.build.json"], hon)
    cg = config_graph("tsconfig.build.json", [
        {"path": "config/base.node.json", "contentSha256": "0" * 64, "kind": "other",
         "extendsResolved": []},
        {"path": "config/base.strict.json", "contentSha256": "0" * 64, "kind": "other",
         "extendsResolved": []},
        # ORDER IS PRECEDENCE and repetitions are retained (sequence, later wins)
        {"path": "tsconfig.build.json", "contentSha256": "0" * 64, "kind": "other",
         "extendsResolved": ["config/base.strict.json", "config/base.node.json",
                             "config/base.strict.json"]},
    ])
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id = _minimal_ts_world(
        files, "ts-tsconfig", "tsconfig", cg, cp, program_roots=["src/m.ts"])
    out = _close_inventory_only(g, cl, uh, retained, plan_id)

    # negative control: dropping the repeated base is a DIFFERENT universe identity
    cg2 = json.loads(json.dumps(cg))
    cg2["nodes"][2]["extendsResolved"] = ["config/base.strict.json", "config/base.node.json"]
    u2 = dict(u, tsconfigGraphHash=raw(cg2))
    results["ts-custom-named-multi-base"] = {
        "verdict": "ADMIT", "runId": out["runId"],
        "entryConfigPath": "tsconfig.build.json",
        "entryKind": "other -> derived configOrigin tsconfig",
        "extendsResolvedRetained": cg["nodes"][2]["extendsResolved"],
        "tsconfigGraphHash": u["tsconfigGraphHash"],
        "tsconfigGraphHashWithoutRepeatedBase": u2["tsconfigGraphHash"],
        "repeatedBaseChangesIdentity":
            u["tsconfigGraphHash"] != u2["tsconfigGraphHash"],
        "universeId": uh,
        "universeIdWithoutRepeatedBase":
            H("native.semantic-universe.typescript.v2", u2),
    }


def scenario_jsconfig_shared_base(results):
    """TS-4: JavaScript config inheriting a shared base with ANOTHER filename.
    A jsconfig entry extending a shared base remains a jsconfig program."""
    files = {
        "jsconfig.json": b'{"extends":"./shared/common.settings.json"}\n',
        "package.json": b'{"name":"jsapp","version":"3.0.0","private":true}\n',
        "shared/common.settings.json": b'{"compilerOptions":{"target":"es2022"}}\n',
        "src/app.js": b"export const app = () => 1;\n",
    }
    hon = honored(allowJs=True, checkJs=False)
    cp = config_projection(["jsconfig.json", "shared/common.settings.json"], hon)
    cg = config_graph("jsconfig.json", [
        {"path": "jsconfig.json", "contentSha256": "0" * 64, "kind": "jsconfig",
         "extendsResolved": ["shared/common.settings.json"]},
        {"path": "shared/common.settings.json", "contentSha256": "0" * 64,
         "kind": "other", "extendsResolved": []},
    ])
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id = _minimal_ts_world(
        files, "js-allowjs", "jsconfig", cg, cp,
        program_roots=["src/app.js"], js_roots=["src/app.js"])
    out = _close_inventory_only(g, cl, uh, retained, plan_id)
    # negative: asserting configOrigin=tsconfig for a jsconfig entry refuses
    bad = dict(u, configOrigin="tsconfig")
    try:
        CL.bind_universe(g, "native.semantic-universe.typescript.v2", bad,
                         "native.context.typescript.v2", ctx, retained[uh])
        neg = "ADMITTED(!)"
    except R.Refuse as exc:
        neg = exc.code + ":" + exc.detail
    results["ts-jsconfig-shared-base"] = {
        "verdict": "ADMIT", "runId": out["runId"],
        "configOriginDerivedFromEntryKind": "jsconfig",
        "sharedBaseFilename": "shared/common.settings.json (kind=other)",
        "negativeAssertedTsconfigOrigin": neg,
    }


def scenario_negatives(results):
    """TS-N: refused hidden / mismatched inputs for the TypeScript path."""
    g = CL.Graph("ts-neg")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]
    files = {
        "package.json": b'{"name":"n","version":"1.0.0","private":true}\n',
        "src/a.ts": b"export const a = 1;\n",
        "tsconfig.json": b'{"compilerOptions":{}}\n',
    }
    cfg = W.resolved_config(["inventory"])
    sd = W.scope_descriptor(["."])
    W.build_snapshot(g, files, sd, cfg)
    hon = honored()
    cp = config_projection(["tsconfig.json"], hon)
    ctx = ts_context(g, cl, language_mode="ts-tsconfig", config_projection=cp,
                     module_resolution="node16", package_module_type="absent",
                     node_modules_layout_digest=None, lockfile_identity=None)
    ctx_hex = g.add_context("native.context.typescript.v2", ctx)
    cg = config_graph("tsconfig.json", [
        {"path": "tsconfig.json", "contentSha256": g.inv_row("tsconfig.json")["sha256"],
         "kind": "tsconfig", "extendsResolved": []}])
    g.cas.put_record(cg)
    u = ts_universe(g, ctx, cg, language_mode="ts-tsconfig", config_origin="tsconfig",
                    package_module_type="absent", program_roots=["src/a.ts"],
                    js_roots=[], lockfile_kind="none", node_modules_in_read_set=False)
    uh = g.add_universe("native.semantic-universe.typescript.v2", u)
    retained = {"configGraph": cg}
    neg = {}

    def probe(name, fn):
        try:
            fn()
            neg[name] = "ADMITTED(!)"
        except R.Refuse as exc:
            neg[name] = exc.code + (":" + exc.detail if exc.detail else "")

    # 1. compiler version not from the admitted manifest
    bad_ctx = json.loads(json.dumps(ctx))
    bad_ctx["toolchain"]["compilerVersion"] = "9.9.9"
    probe("compiler-version-not-from-manifest",
          lambda: CL.admit_native_context(g, "native.context.typescript.v2", bad_ctx))
    # 2. a tool digest outside the named closure tree
    bad2 = json.loads(json.dumps(ctx))
    bad2["toolClosure"]["compiler"] = "b" * 64
    probe("tool-digest-outside-closure",
          lambda: CL.admit_native_context(g, "native.context.typescript.v2", bad2))
    # 3. an incomplete stdlib declaration inventory
    bad3 = json.loads(json.dumps(ctx))
    bad3["toolchain"]["standardLibraryComponentDigests"] = \
        bad3["toolchain"]["standardLibraryComponentDigests"][:1]
    bad3["toolchain"]["libSelection"] = ["dom"]
    probe("stdlib-inventory-incomplete",
          lambda: CL.admit_native_context(g, "native.context.typescript.v2", bad3))
    # 4. a stdlib merkle root that names no retained closure
    bad4 = json.loads(json.dumps(ctx))
    bad4["toolchain"]["typescriptStdlibMerkleRoot"] = "c" * 64
    probe("stdlib-merkle-root-names-no-retained-closure",
          lambda: CL.admit_native_context(g, "native.context.typescript.v2", bad4))
    # 5. a config graph path outside the snapshot
    bad5 = json.loads(json.dumps(ctx))
    bad5["configProjection"]["configGraphPaths"] = ["elsewhere/tsconfig.json"]
    probe("config-graph-path-outside-snapshot",
          lambda: CL.admit_native_context(g, "native.context.typescript.v2", bad5))
    # 6. a Rust context offered as the TypeScript context
    probe("rust-context-offered-as-typescript",
          lambda: CL.bind_universe(g, "native.semantic-universe.typescript.v2", u,
                                   "native.context.rust.v2", ctx, retained))
    # 7. a universe bound WITHOUT the retained config graph
    probe("universe-bound-without-retained-inputs",
          lambda: CL.bind_universe(g, "native.semantic-universe.typescript.v2", u,
                                   "native.context.typescript.v2", ctx, {}))
    # 8. context bytes that are not the admitted ones
    other_ctx = json.loads(json.dumps(ctx))
    other_ctx["packageModuleType"] = "commonjs"
    probe("context-bytes-are-not-the-admitted-ones",
          lambda: CL.bind_universe(g, "native.semantic-universe.typescript.v2", u,
                                   "native.context.typescript.v2", other_ctx, retained))
    # 9. a retained node_modules layout that no context selected
    probe("retained-layout-unselected",
          lambda: CL.bind_universe(g, "native.semantic-universe.typescript.v2", u,
                                   "native.context.typescript.v2", ctx,
                                   dict(retained, nodeModulesLayout={"schemaVersion": 1,
                                                                     "entries": []})))
    # 10. a raw canonical payload offered where an H frame is required
    payload_digest = g.cas.put_record(ctx)
    probe("raw-payload-offered-as-h-identity",
          lambda: g.cas.parse_frame(payload_digest, CL.CONTEXT_DOMAINS))
    # 11. an unregistered H domain in a frame
    d = g.cas.put_frame("native.context.invented.v9", ctx)
    probe("unregistered-h-domain", lambda: g.cas.parse_frame(d, CL.CONTEXT_DOMAINS))
    # 12. a missing preimage
    probe("missing-preimage", lambda: g.cas.get("d" * 64))
    # 13. a hidden input: a well-formed context frame the Plan never selected
    hidden = json.loads(json.dumps(ctx))
    hidden["packageModuleType"] = "commonjs"
    hidden_hex = g.add_context("native.context.typescript.v2", hidden)
    plan = {"nativeContextDigests": [ctx_hex]}

    def hidden_check():
        if set(plan["nativeContextDigests"]) != set(g.contexts):
            raise R.Refuse("PLAN_CONTEXT_SET_MISMATCH", hidden_hex)
    probe("hidden-context-not-reached-by-plan", hidden_check)
    # 14. an unanchored CODE fact under a TypeScript universe
    def unanchored():
        p = {"container": "symbol:src/a.ts", "declared": "symbol:src/a.ts#a",
             "declarationKind": "variable"}
        fd = {"schemaVersion": 2, "snapshotId": g.snapshot_id, "relation": "declares",
              "resolution": "syntactic", "sourceUniverse": uh, "targetUniverse": uh,
              "producerClosure": cl["provider-ts"],
              "payloadSchemaDigest": R.RELATION_DOC_DIGEST,
              "payloadDigest": raw(p), "anchors": [], "confidenceMillionths": 1000000}
        CL.check_fact(g, fd, p, {})
    probe("unanchored-code-fact-under-typescript-universe", unanchored)
    # 15. an inventory fact carrying an anchor
    def anchored_inventory():
        row = g.inv_row("src/a.ts")
        p = {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}
        fd = {"schemaVersion": 2, "snapshotId": g.snapshot_id, "relation": "file",
              "resolution": "enumerated", "sourceUniverse": uh, "targetUniverse": uh,
              "producerClosure": cl["provider-ts"],
              "payloadSchemaDigest": R.RELATION_DOC_DIGEST, "payloadDigest": raw(p),
              "anchors": [W.anchor(g, "src/a.ts", 0, 4)], "confidenceMillionths": 1000000}
        CL.check_fact(g, fd, p, {})
    probe("inventory-fact-with-an-anchor", anchored_inventory)
    # 16. a file payload claiming a wrong content hash
    def wrong_hash():
        row = g.inv_row("src/a.ts")
        p = {"path": row["path"], "contentSha256": "e" * 64, "byteLength": row["bytes"]}
        fd = {"schemaVersion": 2, "snapshotId": g.snapshot_id, "relation": "file",
              "resolution": "enumerated", "sourceUniverse": uh, "targetUniverse": uh,
              "producerClosure": cl["provider-ts"],
              "payloadSchemaDigest": R.RELATION_DOC_DIGEST, "payloadDigest": raw(p),
              "anchors": [], "confidenceMillionths": 1000000}
        CL.check_fact(g, fd, p, {})
    probe("file-payload-wrong-content-hash", wrong_hash)
    # 17. a rung of ANOTHER relation
    probe("cross-relation-rung", lambda: R.rung_index("declares", "resolved-callee"))
    # 18. an unlisted TypeScript source suffix
    probe("unlisted-source-variant-suffix",
          lambda: CL.body_language_version(g, uh, "src/data.vue", {"configGraph": cg}))
    results["ts-negatives"] = neg


def scenario_two_typescript_contexts(results):
    """TS-5: TWO TypeScript contexts under ONE Plan (ordinary, not exceptional), and
    the coverageTotality `matchOn` law: a fact of one universe does NOT discharge the
    other universe's missing-file obligation."""
    g = CL.Graph("ts-two-contexts")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]
    files = {
        "apps/web/package.json": b'{"name":"web","version":"1.0.0","type":"module","private":true}\n',
        "apps/web/src/w.ts": b"export const w = 1;\n",
        "apps/web/tsconfig.json": b'{"compilerOptions":{}}\n',
        "libs/core/package.json": b'{"name":"core","version":"1.0.0","private":true}\n',
        "libs/core/src/c.ts": b"export const c = 2;\n",
        "libs/core/tsconfig.json": b'{"compilerOptions":{}}\n',
    }
    cfg = W.resolved_config(["inventory"])
    sd = W.scope_descriptor(["apps/web", "libs/core"], excluded=["node_modules"])
    W.build_snapshot(g, files, sd, cfg)

    universes, retained, ctx_hexes = {}, {}, []
    for root, module_type in (("apps/web", "module"), ("libs/core", "absent")):
        cfgpath = root + "/tsconfig.json"
        hon = honored()
        cp = config_projection([cfgpath], hon)
        ctx = ts_context(g, cl, language_mode="ts-tsconfig", config_projection=cp,
                         module_resolution="node16", package_module_type=module_type,
                         node_modules_layout_digest=None, lockfile_identity=None)
        ctx_hex = g.add_context("native.context.typescript.v2", ctx)
        ctx_hexes.append(ctx_hex)
        cg = config_graph(cfgpath, [
            {"path": cfgpath, "contentSha256": g.inv_row(cfgpath)["sha256"],
             "kind": "tsconfig", "extendsResolved": []}])
        g.cas.put_record(cg)
        src = root + "/src/" + ("w.ts" if root == "apps/web" else "c.ts")
        u = ts_universe(g, ctx, cg, language_mode="ts-tsconfig", config_origin="tsconfig",
                        package_module_type=module_type, program_roots=[src],
                        js_roots=[], lockfile_kind="none", node_modules_in_read_set=False)
        uh = g.add_universe("native.semantic-universe.typescript.v2", u)
        universes[root] = uh
        retained[uh] = {"configGraph": cg}

    manifest = W.capability_manifest("default", [], [])
    policy = W.simple_policy("two", "file", "enumerated", op="exists", subject_kind="file")
    g.rule_program = W.compile_program(policy)
    g.cas.put_record(g.rule_program)
    spec = W.analysis_spec([
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": r, "required": True} for r in universes])
    grant = W.semantic_grant(["read-source", "native-analysis"], raw(sd))
    plan_id = W.build_plan(g, [cl["provider-ts"], cl["evaluator"]], ctx_hexes,
                           spec, grant, policy, W.EMPTY_WAIVERS, manifest)

    prov = cl["provider-ts"]
    subjects = {"apps/web": ["apps/web/src/w.ts"], "libs/core": ["libs/core/src/c.ts"]}
    scopes, covs, facts = [], [], []
    for root, uh in universes.items():
        sid, sc = W.make_scope(g, "file", "enumerated", uh, uh, prov, subjects[root])
        scopes.append(sid)
        p = {"path": subjects[root][0],
             "contentSha256": g.inv_row(subjects[root][0])["sha256"],
             "byteLength": g.inv_row(subjects[root][0])["bytes"]}
        fid, _ = W.make_fact(g, "file", "enumerated", uh, uh, prov, p, anchors=[])
        facts.append(fid)
        cid, _ = W.make_coverage(g, sid, sc, W.entry("file", "enumerated", "complete",
                                                     "not-applicable", False, True, None))
        covs.append(cid)
    vid, _ = W.make_view(g, plan_id, scopes, facts, covs, prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="pass",
                                            scope_ids=[scopes[0]], coverage_ids=[covs[0]])
    out = CL.close_run(g, retained, [vid], proof, evidence, seal, run)

    # NEGATIVE: drop the second universe's own fact.  The remaining fact is in the same
    # view and satisfies the existential fact/scope join through the FIRST scope, but it
    # does not pay the SECOND scope's totality obligation (matchOn includes both universes).
    bad_view = dict(g.views[vid])
    bad_view["facts"] = [facts[0]]
    bad_vid = g.add_view(bad_view)
    try:
        CL.close_run(g, retained, [bad_vid], proof, evidence, seal, run)
        neg = "ADMITTED(!)"
    except R.Refuse as exc:
        neg = exc.code + ":" + exc.detail

    results["ts-two-contexts-one-plan"] = {
        "verdict": "ADMIT",
        "runId": out["runId"],
        "planNativeContextDigests": g.plan["nativeContextDigests"],
        "twoContextsOfTheSameLanguage": len(set(ctx_hexes)) == 2,
        "universes": universes,
        "nothingElectsOneByPosition":
            "a fact's sourceUniverse names its OWN nativeContextId; that is what selects "
            "the context, and the closure requires it to be one the Plan committed to",
        "crossUniverseTotalityNegative": neg,
        "matchOn": R.RELATION_REGISTRY["file"]["coverageTotality"]["matchOn"],
    }


def scenario_cache_key(results):
    """Constructing a cache key and ADMITTING a hit are two different acts."""
    plan_id = "plan2:" + "f1" * 32
    producer = "closure2:" + "f2" * 32
    stage_spec = {"schemaVersion": 2, "planId": plan_id, "producerClosure": producer,
                  "operation": "native-analysis", "parameters": [],
                  "outputDomains": ["coverage", "fact"],
                  "outputSchemaDigest": R.NATIVE_DOC_DIGEST}
    R.validate("identity", "#/$defs/stage-spec", stage_spec)
    key_record = {
        "schemaVersion": 2, "planId": plan_id, "producerClosure": producer,
        "stageSpecDigest": raw(stage_spec),
        "scopeIds": ["scope2:" + "f3" * 32],
        "inputRefs": [{"domain": "native-context", "digest": "f4" * 32}],
        "outputSchemaDigest": R.NATIVE_DOC_DIGEST,
    }
    ok, why = R.schema_ok("identity", "#/$defs/cache-key", key_record)
    results["cache-key-versus-hit"] = {
        "cacheKeyRecordAdmitted": ok, "detail": why,
        "cacheKeyId": ident("cache-key", key_record) if ok else None,
        "regenerationKeyId": ident("regeneration-key", key_record) if ok else None,
        "sameRecordDifferentDomain": (ident("cache-key", key_record)
                                      != ident("regeneration-key", key_record)) if ok else None,
        "constructionIsPure": "exact schema admission and canonical order over the "
                              "cache-key record, nothing more: it reads no bytes and "
                              "resolves no reference",
        "admittingAHitRequiresTheRunsWholeClosure": [
            "stage spec retained and joined to this Plan",
            "producing closure retained and Plan-selected",
            "every scopeIds member a retained subject-scope of this snapshot",
            "the output schema document retained",
            "every inputRefs entry resolved through x-opensip-digest-domains",
            "a bare coverage-payload / import-payload / fact-payload reference is "
            "REFUSED as an authoritative root",
        ],
        "aHitIsNeverEvidenceAuthority": True,
    }
