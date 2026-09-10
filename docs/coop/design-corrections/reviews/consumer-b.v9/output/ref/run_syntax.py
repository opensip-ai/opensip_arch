"""RUN-SYN-*: compiler-free syntax-only Runs.

  * SYN-CODE   a supported CODE grammar, with inventory and syntax/clone facts
  * SYN-DATA   an already bundled DATA/DOCUMENT grammar: its declared inventory
               capability, and explicit unavailability for the capabilities its
               class does not support
  * SYN-NONE   a repository with NO TypeScript and NO Rust compilation unit,
               including a path no bundled grammar reads at all
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

JS_SRC = b"export function tick() {\n  return 1 + 1;\n}\n"
TS_SRC = b"export function tock(): number {\n  return 1 + 1;\n}\n"
MD = b"# readme\n\nsome prose\n"
JSON_DOC = b'{"a":1}\n'
TOML_DOC = b"a = 1\n"
YAML_DOC = b"a: 1\n"
PY_SRC = b"def main():\n    return 1\n"

JS_BODY_START = JS_SRC.index(b"{")
JS_BODY_END = JS_SRC.index(b"}\n") + 1
JS_BODY = JS_SRC[JS_BODY_START:JS_BODY_END]


def build(kind="code", *, bad_anchor=False, false_complete=False,
          wrong_pair=None, tamper=None):
    s = Store()
    if kind == "code":
        files = {"src/app.js": JS_SRC, "src/app.ts": TS_SRC, "README.md": MD}
        grammars = ["g-javascript", "g-markdown", "g-typescript"]
    elif kind == "data":
        files = {"config.json": JSON_DOC, "Config.toml": TOML_DOC,
                 "README.md": MD, "ci.yaml": YAML_DOC}
        grammars = ["g-json", "g-markdown", "g-toml", "g-yaml"]
    else:                      # "none": no TS/Rust unit, and an unbundled suffix
        files = {"tool/main.py": PY_SRC, "README.md": MD, "data.yaml": YAML_DOC}
        grammars = ["g-markdown", "g-yaml"]

    scope = B.scope_descriptor(["."], excluded=[".git"])
    config = B.default_config(["inventory", "syntax", "clones-fact"])
    snap_id, snap, inventory = B.make_snapshot(s, files, scope, config)
    inv = {r["path"]: r for r in inventory}

    ctx, ctx_hex = S.syntax_context(s)
    u, u_hex = S.syntax_universe(s, ctx, ctx_hex, grammars)

    prov_id, _ = S.provider_closure(s, "syntax-all")
    eval_id, _ = S.evaluator_closure(s)
    det_id, _ = S.detector_closure(s)
    manifest = B.capability_manifest(providers=[B.provider_capability(
        "syntax-all", "*", {"file": "enumerated", "declares": "syntactic",
                            "clones": "normalized-body-hash"},
        ["all-supported"])])
    cm_id, cm_bytes_digest, _ = B.commit_capability_manifest(s, manifest)
    spec = {"schemaVersion": 2, "requestedCapabilities": sorted([
        {"capabilityId": "inventory", "languageMode": "syntax-only",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "syntax", "languageMode": "syntax-only",
         "workspaceRoot": ".", "required": True},
        {"capabilityId": "clones-fact", "languageMode": "syntax-only",
         "workspaceRoot": ".", "required": True}], key=K.C),
        "policyPackIds": ["cb9.pack"], "parameters": []}
    grant_digest, _ = A.semantic_grant(s, snap["scopeDigest"])
    policy = POLICY_CODE if kind == "code" else POLICY_INVENTORY
    policy_digest = s.put_record(policy)
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    waiver_digest = s.put_record(waivers)
    plan_id, plan = B.make_plan(s, snap_id, snap, cm_id, cm_bytes_digest,
                                [prov_id, eval_id, det_id], spec, [ctx_hex],
                                policy_digest, waiver_digest, grant_digest,
                                {"unit": "work-units", "limit": 100000})

    scopes, facts, coverages = {}, {}, {}
    # inventory scope over EVERY inventoried path, including ones no bundled
    # grammar reads (tool/main.py) -- inventory is never grammar-gated
    s1_id, s1 = B.make_scope(s, snap_id, u_hex, u_hex, "file", "enumerated",
                             prov_id, [r["path"] for r in inventory])
    scopes[s1_id] = s1
    for row in inventory:
        fid, f = B.make_fact(s, snap_id, "file", "enumerated", u_hex, u_hex,
                             prov_id,
                             {"path": row["path"], "contentSha256": row["sha256"],
                              "byteLength": row["bytes"]}, [])
        facts[fid] = f

    if kind == "code":
        # declares@syntactic over a code path
        anchor_path = "README.md" if bad_anchor else "src/app.js"
        anchor = {"path": anchor_path,
                  "blobDigest": inv[anchor_path]["sha256"],
                  "startByte": 0, "endByte": 5}
        s2_id, s2 = B.make_scope(s, snap_id, u_hex, u_hex, "declares",
                                 "syntactic", prov_id, ["sym:tick"])
        scopes[s2_id] = s2
        did, df = B.make_fact(s, snap_id, "declares", "syntactic", u_hex, u_hex,
                              prov_id,
                              {"container": "mod:src/app.js",
                               "declared": "sym:tick",
                               "declarationKind": "function"}, [anchor])
        facts[did] = df
        # a GRAMMAR-parsed clone body: dialect {grammarVariant}, languageId js
        blv, language_id = N.derive_body_language_version(
            "native.semantic-universe.syntax.v2", u, ctx, "src/app.js", {})
        lv_digest = s.put_blob(S.LEVEL_SPEC_L0)
        frame = K.body_identity_frame(
            "L0-verbatim", hashlib.sha256(S.LEVEL_SPEC_L0).digest(), language_id,
            hashlib.sha256(K.C(blv)).digest(), K.l0_payload(JS_BODY))
        body_hex = s.put_blob(frame)
        s3_id, s3 = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                                 "normalized-body-hash", prov_id, ["src/app.js"])
        scopes[s3_id] = s3
        cfid, cf = B.make_fact(
            s, snap_id, "clones", "normalized-body-hash", u_hex, u_hex, prov_id,
            {"bodyIdentity": "sha256:" + body_hex,
             "normalisationLevel": "L0-verbatim",
             "normalisationVersion": lv_digest},
            [{"path": "src/app.js", "blobDigest": inv["src/app.js"]["sha256"],
              "startByte": JS_BODY_START, "endByte": JS_BODY_END}])
        facts[cfid] = cf
        grammar_body_identity = "sha256:" + body_hex
        grammar_blv = blv
    else:
        # A capability this universe cannot serve: disclosed, never refused.
        s2_id, s2 = B.make_scope(s, snap_id, u_hex, u_hex, "declares",
                                 "syntactic", prov_id, ["sym:none"])
        scopes[s2_id] = s2
        s3_id, s3 = B.make_scope(s, snap_id, u_hex, u_hex, "clones",
                                 "normalized-body-hash", prov_id,
                                 [p for p in inv if p.endswith((".md", ".json",
                                                                ".toml", ".yaml",
                                                                ".py"))][:1])
        scopes[s3_id] = s3
        grammar_body_identity = None
        grammar_blv = None

    for sid, sc in scopes.items():
        commitment = "sha256:" + split_id(sid, "scope2")
        kw = {}
        if kind != "code" and sc["relation"] in ("declares", "clones"):
            kw = {"coverage": "unknown",
                  "deficiency": "language-tier-unsupported",
                  "native_cause": "capability-missing"}
            if false_complete:
                kw = {"coverage": "complete", "deficiency": None,
                      "native_cause": None}
            elif wrong_pair == "deficiency":
                kw["deficiency"] = "provider-unavailable"
            elif wrong_pair == "cause":
                kw["native_cause"] = "lockfile-missing"
        cid, _, payload = B.make_coverage(
            s, sid, sc, B.coverage_entry(sc["relation"], sc["resolution"],
                                         commitment, len(sc["subjects"]), **kw))
        coverages[cid] = {"scopeId": sid, "payload": payload}

    view_id, view = B.make_view(s, plan_id, list(scopes), list(facts),
                                list(coverages), prov_id)
    stage_digest, _ = B.make_stage(s, plan_id, prov_id, "syntax.analyze",
                                   ["fact", "coverage", "subject-scope"],
                                   kit.doc_digest("native"))
    ep_id, _ = B.make_exec_plan(s, plan_id, [
        {"ordinal": 0, "stageSpecDigest": stage_digest, "requires": [],
         "outputDomains": sorted(["fact", "coverage", "subject-scope"], key=K.C)}])
    out = A.finish_run(s, plan_id=plan_id, plan=plan, snapshot_id=snap_id,
                       views={view_id: view}, view_ids=[view_id], scopes=scopes,
                       facts=facts, coverages=coverages, policy=policy,
                       policy_digest=policy_digest, waivers=waivers,
                       rule_program=A.compile_program(policy, policy_digest),
                       evaluator_closure_id=eval_id, detector_closure_id=det_id,
                       exec_plan_id=ep_id, universe_language={u_hex: "syntax"},
                       capability_manifest_id=cm_id, tamper=tamper)
    out.update({"store": s, "universeHex": u_hex, "contextHex": ctx_hex,
                "grammarBodyIdentity": grammar_body_identity,
                "grammarBodyLanguageVersion": grammar_blv,
                "inventory": inventory, "planId": plan_id})
    return out


POLICY_CODE = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{"ruleId": "cb9.syntax-clone", "enabled": True, "severity": "error",
               "gate": True,
               "ruleProgramRef": {"contributionId": "cb9.native",
                                  "ruleStableId": "cb9.syntax-clone",
                                  "semanticsMajor": 1, "programDigest": "44" * 32},
               "subjectEnumeration": {"universe": "syntax", "subjectKind": "file",
                                      "include": ["src/app.js"]},
               "emitWhen": {"op": "exists", "relation": "clones",
                            "minResolution": "normalized-body-hash",
                            "filters": []},
               "evidenceUse": [], "messageCode": "cb9.syntax.clone"}]}

POLICY_INVENTORY = {
    "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{"ruleId": "cb9.no-clone-here", "enabled": True, "severity": "error",
               "gate": True,
               "ruleProgramRef": {"contributionId": "cb9.native",
                                  "ruleStableId": "cb9.no-clone-here",
                                  "semanticsMajor": 1, "programDigest": "55" * 32},
               "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"},
               "emitWhen": {"op": "none", "relation": "clones",
                            "minResolution": "normalized-body-hash",
                            "filters": []},
               "evidenceUse": [], "messageCode": "cb9.syntax.noclone"}]}
