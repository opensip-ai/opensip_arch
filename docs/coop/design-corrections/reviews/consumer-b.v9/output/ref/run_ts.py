"""RUN-TS-1: an ordinary TypeScript project that reads node_modules and
resolves bare specifiers, with its retained configuration graph and dependency
layout.  Complete positive Run: identity + schema + closure + proof replay.
"""
from __future__ import annotations

import hashlib

import assemble as A
import build as B
import canon as K
import closure as CL
import kit
import scenarios as S
from store import Store, split_id

TS_A = (b'import {pad} from "left-pad";\n'
        b'export function hello(): string { return pad("x", 3); }\n')
TS_B = b'import {hello} from "./a";\nexport const greeting = hello();\n'
PKG = b'{"name":"cb9-app","version":"1.0.0","private":true}\n'
TSCONFIG = b'{"extends":"./configs/base.json","compilerOptions":{"lib":["es2022"]}}\n'
BASE = b'{"compilerOptions":{"module":"node16","target":"es2022"}}\n'
LOCK = b'{"lockfileVersion":3,"packages":{}}\n'
LICENSE = b"MIT\n"
README = b"# cb9\n"

# the exact body span of hello(): the brace-delimited body
BODY_START = TS_A.index(b"{ return")
BODY_END = TS_A.index(b"}\n", BODY_START) + 1
BODY = TS_A[BODY_START:BODY_END]


def build(store=None, *, tamper=None, break_totality=False,
          body_mutation=None, l0_span_lie=False, anchor_range_lie=False):
    s = store or Store()
    files = {"package.json": PKG, "tsconfig.json": TSCONFIG,
             "configs/base.json": BASE, "package-lock.json": LOCK,
             "src/a.ts": TS_A, "src/b.ts": TS_B,
             "LICENSE": LICENSE, "README.md": README}
    scope = B.scope_descriptor(["."], excluded=["node_modules", ".git"])
    config = B.default_config(["inventory", "syntax", "clones-fact",
                               "references", "unresolved-edge"])
    snap_id, snap, inventory = B.make_snapshot(s, files, scope, config)
    inv = {r["path"]: r for r in inventory}

    # --- node_modules layout: a retained resolution observation, NOT inventory
    nm_manifest = b'{"name":"left-pad","version":"1.3.0","main":"index.js"}\n'
    nm_digest = s.put_blob(nm_manifest)
    layout = {"schemaVersion": 1, "entries": [
        {"packageName": "left-pad", "packageVersion": "1.3.0",
         "installPath": "node_modules/left-pad", "realPath": "node_modules/left-pad",
         "contentSha256": nm_digest}]}
    layout_digest = s.put_record(layout)

    lockfile = {"kind": "package-lock", "path": "package-lock.json",
                "contentSha256": inv["package-lock.json"]["sha256"]}
    ctx, ctx_hex, _ = S.ts_context(
        s, language_mode="ts-tsconfig",
        config_graph_paths=["tsconfig.json", "configs/base.json"],
        lockfile=lockfile, node_modules_digest=layout_digest,
        package_module_type="commonjs")

    graph = {"schemaVersion": 1, "entryConfigPath": "tsconfig.json", "nodes": [
        {"path": "configs/base.json", "contentSha256": inv["configs/base.json"]["sha256"],
         "kind": "other", "extendsResolved": []},
        {"path": "tsconfig.json", "contentSha256": inv["tsconfig.json"]["sha256"],
         "kind": "tsconfig", "extendsResolved": ["configs/base.json"]}]}
    u, u_hex = S.ts_universe(s, ctx, ctx_hex, language_mode="ts-tsconfig",
                             config_graph=graph,
                             program_roots=["src/a.ts", "src/b.ts"],
                             lockfile_kind="package-lock")

    prov_id, _ = S.provider_closure(s, "typescript-semantic")
    eval_id, _ = S.evaluator_closure(s)
    det_id, _ = S.detector_closure(s)

    # --- capability manifest -------------------------------------------------
    manifest = B.capability_manifest(
        providers=[B.provider_capability(
            "typescript-semantic", "typescript",
            {"clones": "normalized-body-hash", "file": "enumerated",
             "references": "resolved-binding"},
            ["linux-x86_64-gnu"])],
        absent=[B.absent_capability("rust-semantic", "rust",
                                    ["calls", "imports"], "unavailable",
                                    "provider-unavailable")])
    cm_id, cm_bytes_digest, cm_bytes = B.commit_capability_manifest(s, manifest)

    # --- analysis spec / grant ----------------------------------------------
    spec = {"schemaVersion": 2, "requestedCapabilities": sorted([
        {"capabilityId": "inventory", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "clones-fact", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "references", "languageMode": "ts-tsconfig",
         "workspaceRoot": ".", "required": True}], key=K.C),
        "policyPackIds": ["cb9.pack"], "parameters": []}
    grant_digest, _ = A.semantic_grant(s, snap["scopeDigest"])

    policy = POLICY
    policy_digest = s.put_record(policy)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    waiver_digest = s.put_record(waivers)

    plan_id, plan = B.make_plan(
        s, snap_id, snap, cm_id, cm_bytes_digest,
        [prov_id, eval_id, det_id], spec, [ctx_hex], policy_digest,
        waiver_digest, grant_digest, {"unit": "work-units", "limit": 100000})

    # --- scopes --------------------------------------------------------------
    file_subjects = [r["path"] for r in inventory]
    s1_id, s1 = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                             prov_id, file_subjects)
    s2_id, s2 = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                             "normalized-body-hash", prov_id, ["src/a.ts"])
    s3_id, s3 = B.make_scope(s, snap_id, u_hex, u_hex, "references",
                             "resolved-binding", prov_id, ["sym:hello"])

    # --- facts ---------------------------------------------------------------
    facts = {}
    for row in inventory:
        if break_totality and row["path"] == "LICENSE":
            continue
        fid, f = B.make_fact(s, snap_id, "file", "enumerated", u_hex, u_hex, prov_id,
                             {"path": row["path"], "contentSha256": row["sha256"],
                              "byteLength": row["bytes"]}, [])
        facts[fid] = f

    # clone body identity at L0 over the exact anchor span
    blv, language_id = _body_language(u, ctx, "src/a.ts")
    lv_spec_digest = s.put_blob(S.LEVEL_SPEC_L0)
    lv_raw = hashlib.sha256(S.LEVEL_SPEC_L0).digest()
    lang_raw = hashlib.sha256(K.C(blv)).digest()
    l0_bytes = (BODY + b" ") if l0_span_lie else BODY
    frame = K.body_identity_frame("L0-verbatim", lv_raw, language_id, lang_raw,
                                  K.l0_payload(l0_bytes))
    body_hex = s.put_blob(frame)
    clone_payload = {"bodyIdentity": "sha256:" + body_hex,
                     "normalisationLevel": "L0-verbatim",
                     "normalisationVersion": lv_spec_digest}
    anchor = {"path": "src/a.ts", "blobDigest": inv["src/a.ts"]["sha256"],
              "startByte": BODY_START,
              "endByte": (len(TS_A) + 5) if anchor_range_lie else BODY_END}
    cid_f, cf = B.make_fact(s, snap_id, "clones", "normalized-body-hash", u_hex,
                            u_hex, prov_id, clone_payload, [anchor])
    facts[cid_f] = cf

    # a NORMALIZED level over the same body: a framed token stream, retained.
    lv1_digest = s.put_blob(S.LEVEL_SPEC_L1)
    lv1_raw = hashlib.sha256(S.LEVEL_SPEC_L1).digest()
    tokens = [("punct", "{"), ("keyword", "return"), ("ident", "pad"),
              ("punct", "("), ("string", '"x"'), ("punct", ","),
              ("number", "3"), ("punct", ")"), ("punct", ";"), ("punct", "}")]
    l1_payload = K.framed_token_stream(tokens)
    m = body_mutation or {}
    frame1 = K.body_identity_frame(
        m.get("levelId", "L1-lexical"),
        m.get("levelVersion", lv1_raw),
        m.get("languageId", language_id),
        m.get("languageVersion", lang_raw),
        m.get("payload", l1_payload))
    body1_hex = s.put_blob(frame1)
    s3b_id, s3b = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                               "normalized-body-hash", prov_id, ["src/b.ts"])
    l1_anchor = {"path": "src/a.ts", "blobDigest": inv["src/a.ts"]["sha256"],
                 "startByte": BODY_START, "endByte": BODY_END}
    l1id, l1f = B.make_fact(s, snap_id, "clones", "normalized-body-hash", u_hex,
                            u_hex, prov_id,
                            {"bodyIdentity": "sha256:" + body1_hex,
                             "normalisationLevel": "L1-lexical",
                             "normalisationVersion": lv1_digest}, [l1_anchor])
    facts[l1id] = l1f

    ref_anchor = {"path": "src/b.ts", "blobDigest": inv["src/b.ts"]["sha256"],
                  "startByte": 0, "endByte": len(TS_B)}
    rid_f, rf = B.make_fact(s, snap_id, "references", "resolved-binding", u_hex,
                            u_hex, prov_id,
                            {"referrer": "sym:src/b.ts", "name": "hello",
                             "resolvedBinding": "sym:hello"}, [ref_anchor])
    facts[rid_f] = rf

    # --- coverage ------------------------------------------------------------
    coverages = {}
    for scope_id, scope_desc in ((s1_id, s1), (s2_id, s2), (s3_id, s3),
                                 (s3b_id, s3b)):
        commitment = "sha256:" + split_id(scope_id, "scope2")
        entry = B.coverage_entry(scope_desc["relation"], scope_desc["resolution"],
                                 commitment, len(scope_desc["subjects"]))
        cid, cdesc, payload = B.make_coverage(s, scope_id, scope_desc, entry)
        coverages[cid] = {"scopeId": scope_id, "payload": payload}

    view_id, view = B.make_view(s, plan_id, [s1_id, s2_id, s3_id, s3b_id],
                                list(facts), list(coverages), prov_id)

    stage_digest, _ = B.make_stage(s, plan_id, prov_id, "native.analyze",
                                   ["fact", "coverage", "subject-scope"],
                                   kit.doc_digest("native"))
    ep_id, _ = B.make_exec_plan(s, plan_id, [
        {"ordinal": 0, "stageSpecDigest": stage_digest, "requires": [],
         "outputDomains": sorted(["fact", "coverage", "subject-scope"], key=K.C)}])

    out = A.finish_run(
        s, plan_id=plan_id, plan=plan, snapshot_id=snap_id,
        views={view_id: view}, view_ids=[view_id],
        scopes={s1_id: s1, s2_id: s2, s3_id: s3, s3b_id: s3b}, facts=facts,
        coverages=coverages, policy=policy, policy_digest=policy_digest,
        waivers=waivers,
        rule_program=A.compile_program(policy, policy_digest),
        evaluator_closure_id=eval_id, detector_closure_id=det_id,
        exec_plan_id=ep_id, universe_language={u_hex: "typescript"},
        capability_manifest_id=cm_id, tamper=tamper)
    out.update({"store": s, "universeHex": u_hex, "contextHex": ctx_hex,
                "planId": plan_id, "snapshotId": snap_id, "viewId": view_id,
                "capabilityManifest": manifest, "capabilityBytes": cm_bytes,
                "capabilityManifestId": cm_id, "bodyIdentity": "sha256:" + body_hex,
                "bodyIdentityL1": "sha256:" + body1_hex,
                "l1Tokens": tokens, "levelSpecL1Digest": lv1_digest,
                "bodyLanguageVersion": blv})
    return out


def _body_language(u, ctx, anchor_path):
    import native as N
    return N.derive_body_language_version(
        "native.semantic-universe.typescript.v2", u, ctx, anchor_path, {})


POLICY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "warning",
    "rules": [
        {"ruleId": "cb9.clone-present", "enabled": True, "severity": "error",
         "gate": True,
         "ruleProgramRef": {"contributionId": "cb9.native",
                            "ruleStableId": "cb9.clone-present",
                            "semanticsMajor": 1, "programDigest": "11" * 32},
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "file",
                                "include": ["src/a.ts"]},
         "emitWhen": {"op": "and", "operands": [
             {"op": "exists", "relation": "clones",
              "minResolution": "normalized-body-hash", "filters": []},
             {"op": "all-covered", "relation": "references",
              "minResolution": "resolved-binding", "filters": []}]},
         "evidenceUse": [], "messageCode": "cb9.clone.present"},
        {"ruleId": "cb9.no-more-than-zero-clones", "enabled": True,
         "severity": "warning", "gate": False,
         "ruleProgramRef": {"contributionId": "cb9.native",
                            "ruleStableId": "cb9.no-more-than-zero-clones",
                            "semanticsMajor": 1, "programDigest": "22" * 32},
         "subjectEnumeration": {"universe": "typescript", "subjectKind": "file",
                                "include": ["src/a.ts"]},
         "emitWhen": {"op": "count-at-most", "relation": "clones",
                      "minResolution": "normalized-body-hash", "filters": [],
                      "n": 0},
         "evidenceUse": [], "messageCode": "cb9.clone.count"},
    ],
}
