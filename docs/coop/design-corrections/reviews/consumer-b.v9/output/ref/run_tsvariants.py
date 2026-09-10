"""RUN-TSV-*: the TypeScript configuration variants and the JavaScript body.

  * synth     synthesized configuration (js-synthesized; null entry, no nodes)
  * custom    an explicitly selected CUSTOM-NAMED project config inheriting
              from MULTIPLE ORDERED bases, including a REPEATED base whose
              precedence order must be retained
  * jsconfig  a JavaScript config inheriting a shared base with ANOTHER filename
  * jsbody    a JavaScript clone body through the TypeScript analyzer universe
"""
from __future__ import annotations

import hashlib

import assemble as A
import build as B
import canon as K
import kit
import native as N
import scenarios as S
from store import Store, split_id

JS = b"export function tick() {\n  return 1 + 1;\n}\n"
TS = b"export function tock(): number {\n  return 2;\n}\n"
PKG = b'{"name":"cb9-variant","version":"1.0.0","private":true}\n'
BASE = b'{"compilerOptions":{"target":"es2022"}}\n'
OVERRIDE = b'{"compilerOptions":{"module":"node16"}}\n'
CUSTOM = b'{"extends":["./configs/base.json","./configs/override.json","./configs/base.json"]}\n'
JSCONFIG = b'{"extends":"./configs/shared.base.json"}\n'
SHARED = b'{"compilerOptions":{"allowJs":true}}\n'

JS_BODY_START = JS.index(b"{")
JS_BODY_END = JS.index(b"}\n") + 1
JS_BODY = JS[JS_BODY_START:JS_BODY_END]


def build(variant="custom", *, kind_lie=False, tamper=None):
    s = Store()
    if variant == "synth":
        files = {"package.json": PKG, "src/app.js": JS}
        graph = {"schemaVersion": 1, "entryConfigPath": None, "nodes": []}
        graph_paths, mode, allow_js, jsx = [], "js-synthesized", True, None
    elif variant == "custom":
        files = {"package.json": PKG, "tsconfig.build.json": CUSTOM,
                 "configs/base.json": BASE, "configs/override.json": OVERRIDE,
                 "src/app.ts": TS}
        graph_paths = ["tsconfig.build.json", "configs/base.json",
                       "configs/override.json"]
        mode, allow_js, jsx = "ts-tsconfig", False, None
    elif variant == "jsconfig":
        files = {"package.json": PKG, "jsconfig.json": JSCONFIG,
                 "configs/shared.base.json": SHARED, "src/app.js": JS}
        graph_paths = ["jsconfig.json", "configs/shared.base.json"]
        mode, allow_js, jsx = "js-allowjs", True, None
    else:                                   # jsbody
        files = {"package.json": PKG, "tsconfig.json": b'{"compilerOptions":{"allowJs":true}}\n',
                 "src/app.js": JS, "src/app.ts": TS}
        graph_paths = ["tsconfig.json"]
        mode, allow_js, jsx = "js-allowjs", True, None

    scope = B.scope_descriptor(["."], excluded=["node_modules", ".git"])
    config = B.default_config(["inventory", "clones-fact"])
    snap_id, snap, inventory = B.make_snapshot(s, files, scope, config)
    inv = {r["path"]: r for r in inventory}

    ctx, ctx_hex, _ = S.ts_context(
        s, language_mode=mode, config_graph_paths=graph_paths, lockfile=None,
        node_modules_digest=None, package_module_type="commonjs",
        allow_js=allow_js, jsx=jsx,
        strict=(variant != "synth"))

    if variant == "synth":
        pass
    elif variant == "custom":
        graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.build.json",
                 "nodes": sorted([
                     {"path": "configs/base.json",
                      "contentSha256": inv["configs/base.json"]["sha256"],
                      "kind": "other", "extendsResolved": []},
                     {"path": "configs/override.json",
                      "contentSha256": inv["configs/override.json"]["sha256"],
                      "kind": "other", "extendsResolved": []},
                     {"path": "tsconfig.build.json",
                      "contentSha256": inv["tsconfig.build.json"]["sha256"],
                      "kind": "tsconfig" if kind_lie else "other",
                      # ORDERED, with the repeated base RETAINED
                      "extendsResolved": ["configs/base.json",
                                          "configs/override.json",
                                          "configs/base.json"]}],
                     key=lambda n: n["path"].encode())}
    elif variant == "jsconfig":
        graph = {"schemaVersion": 1, "entryConfigPath": "jsconfig.json",
                 "nodes": sorted([
                     {"path": "configs/shared.base.json",
                      "contentSha256": inv["configs/shared.base.json"]["sha256"],
                      "kind": "other", "extendsResolved": []},
                     {"path": "jsconfig.json",
                      "contentSha256": inv["jsconfig.json"]["sha256"],
                      "kind": "jsconfig",
                      "extendsResolved": ["configs/shared.base.json"]}],
                     key=lambda n: n["path"].encode())}
    else:
        graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json", "nodes": [
            {"path": "tsconfig.json", "contentSha256": inv["tsconfig.json"]["sha256"],
             "kind": "tsconfig", "extendsResolved": []}]}

    roots = [p for p in inv if p.endswith((".ts", ".js"))]
    js_roots = [p for p in roots if p.endswith(".js")]
    u, u_hex = S.ts_universe(s, ctx, ctx_hex, language_mode=mode,
                             config_graph=graph, program_roots=sorted(roots),
                             js_roots=sorted(js_roots), lockfile_kind="none")

    prov_id, _ = S.provider_closure(s, "typescript-semantic")
    eval_id, _ = S.evaluator_closure(s)
    det_id, _ = S.detector_closure(s)
    manifest = B.capability_manifest(providers=[B.provider_capability(
        "typescript-semantic", "typescript",
        {"clones": "normalized-body-hash", "file": "enumerated"},
        ["linux-x86_64-gnu"])])
    cm_id, cm_bd, _ = B.commit_capability_manifest(s, manifest)
    spec = {"schemaVersion": 2, "requestedCapabilities": [
        {"capabilityId": "inventory", "languageMode": mode,
         "workspaceRoot": ".", "required": True}],
        "policyPackIds": ["cb9.pack"], "parameters": []}
    grant_digest, _ = A.semantic_grant(s, snap["scopeDigest"])
    policy_digest = s.put_record(POLICY)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    waiver_digest = s.put_record(waivers)
    plan_id, plan = B.make_plan(s, snap_id, snap, cm_id, cm_bd,
                                [prov_id, eval_id, det_id], spec, [ctx_hex],
                                policy_digest, waiver_digest, grant_digest,
                                {"unit": "work-units", "limit": 100000})

    scopes, facts, coverages = {}, {}, {}
    s1_id, s1 = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                             prov_id, [r["path"] for r in inventory])
    scopes[s1_id] = s1
    for row in inventory:
        fid, f = B.make_fact(s, snap_id, "file", "enumerated", u_hex, u_hex,
                             prov_id, {"path": row["path"],
                                       "contentSha256": row["sha256"],
                                       "byteLength": row["bytes"]}, [])
        facts[fid] = f

    body_identity = blv = None
    if "src/app.js" in inv:
        blv, language_id = N.derive_body_language_version(
            "native.semantic-universe.typescript.v2", u, ctx, "src/app.js", {})
        lv = s.put_blob(S.LEVEL_SPEC_L0)
        frame = K.body_identity_frame(
            "L0-verbatim", hashlib.sha256(S.LEVEL_SPEC_L0).digest(), language_id,
            hashlib.sha256(K.C(blv)).digest(), K.l0_payload(JS_BODY))
        bh = s.put_blob(frame)
        body_identity = "sha256:" + bh
        s2_id, s2 = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                                 "normalized-body-hash", prov_id, ["src/app.js"])
        scopes[s2_id] = s2
        cfid, cf = B.make_fact(
            s, snap_id, "clones", "normalized-body-hash", u_hex, u_hex, prov_id,
            {"bodyIdentity": body_identity, "normalisationLevel": "L0-verbatim",
             "normalisationVersion": lv},
            [{"path": "src/app.js", "blobDigest": inv["src/app.js"]["sha256"],
              "startByte": JS_BODY_START, "endByte": JS_BODY_END}])
        facts[cfid] = cf

    for sid, sc in scopes.items():
        cid, _, payload = B.make_coverage(
            s, sid, sc, B.coverage_entry(
                sc["relation"], sc["resolution"],
                "sha256:" + split_id(sid, "scope2"), len(sc["subjects"])))
        coverages[cid] = {"scopeId": sid, "payload": payload}

    view_id, view = B.make_view(s, plan_id, list(scopes), list(facts),
                                list(coverages), prov_id)
    sd, _ = B.make_stage(s, plan_id, prov_id, "native.analyze",
                         ["fact", "coverage"], kit.doc_digest("native"))
    ep_id, _ = B.make_exec_plan(s, plan_id, [
        {"ordinal": 0, "stageSpecDigest": sd, "requires": [],
         "outputDomains": sorted(["fact", "coverage"], key=K.C)}])
    out = A.finish_run(s, plan_id=plan_id, plan=plan, snapshot_id=snap_id,
                       views={view_id: view}, view_ids=[view_id], scopes=scopes,
                       facts=facts, coverages=coverages, policy=POLICY,
                       policy_digest=policy_digest, waivers=waivers,
                       rule_program=A.compile_program(POLICY, policy_digest),
                       evaluator_closure_id=eval_id, detector_closure_id=det_id,
                       exec_plan_id=ep_id, universe_language={u_hex: "typescript"},
                       capability_manifest_id=cm_id, tamper=tamper)
    out.update({"store": s, "universeHex": u_hex, "contextHex": ctx_hex,
                "configOrigin": u["configOrigin"], "graph": graph,
                "bodyIdentity": body_identity, "bodyLanguageVersion": blv,
                "planId": plan_id})
    return out


POLICY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{"ruleId": "cb9.variant", "enabled": True, "severity": "note",
               "gate": False,
               "ruleProgramRef": {"contributionId": "cb9.native",
                                  "ruleStableId": "cb9.variant",
                                  "semanticsMajor": 1, "programDigest": "66" * 32},
               "subjectEnumeration": {"universe": "typescript",
                                      "subjectKind": "file"},
               "emitWhen": {"op": "exists", "relation": "file",
                            "minResolution": "enumerated", "filters": []},
               "evidenceUse": [], "messageCode": "cb9.variant.file"}]}
