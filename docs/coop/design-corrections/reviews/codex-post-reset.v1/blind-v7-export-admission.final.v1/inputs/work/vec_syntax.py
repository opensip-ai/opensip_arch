"""Compiler-free syntax-only Runs.

SYN-CODE : a repository with NO TypeScript and NO Rust compilation unit at all.
           A bundled `javascript` CODE grammar and a `markdown` DATA-DOCUMENT
           grammar are selected.  Inventory + syntax + clone facts close; the
           semantic capabilities are correctly UNAVAILABLE; an unbundled `.py`
           path is still inventoried and bears no code fact.
SYN-DATA : an already bundled data/document grammar set only.  The declared
           inventory capability closes; every capability its class does not
           support is disclosed unavailable, and a complete EMPTY clone result
           is refused.
"""

import oslib as O
import graph as G
import build as B
from oslib import C, H, sha256hex

JS_BODY = b"function pad(n) {\n  return String(n);\n}\n"
GRAMMAR_TREE = {"grammars/javascript.bin": b"js-grammar-blob\n",
                "grammars/markdown.bin": b"md-grammar-blob\n",
                "grammars/json.bin": b"json-grammar-blob\n",
                "grammars/toml.bin": b"toml-grammar-blob\n",
                "grammars/yaml.bin": b"yaml-grammar-blob\n",
                "spec/normalizer.txt": b"normalizer-spec\n"}


def _grammar_row(kit, lang, digest_bytes):
    reg = G.GRAMMAR_REG["languages"][lang]
    return {"grammarId": "g." + lang, "grammarVersion": "1.0.0",
            "languageId": lang, "syntaxClass": reg["syntaxClass"],
            "suffixes": sorted(reg["suffixes"]),
            "grammarDigest": kit.w.raw(digest_bytes)}


def build(kind="code", mutate=""):
    kit = B.Kit()
    w = kit.w
    lv = B.retain_level_specs(kit)

    if kind == "code":
        f_js = kit.file("lib/util.js", JS_BODY)
        f_md = kit.file("README.md", "# project\n\nnotes\n")
        f_py = kit.file("tool/main.py", "def main():\n    pass\n")
        selected = ["g.javascript", "g.markdown"]
        langs = ["javascript", "markdown"]
    else:
        f_json = kit.file("data/config.json", '{"a":1}\n')
        f_toml = kit.file("data/settings.toml", "a = 1\n")
        f_md = kit.file("README.md", "# data only\n")
        f_yaml = kit.file("ci/pipeline.yaml", "steps: []\n")
        selected = ["g.json", "g.markdown", "g.toml", "g.yaml"]
        langs = ["json", "markdown", "toml", "yaml"]

    gclosure, gdesc = kit.closure("grammar", GRAMMAR_TREE, "4.2.0")
    prov_id, _ = kit.closure("provider", {"bin/syntax": b"provider\n"}, "1.0.0")
    eval_id, _ = kit.closure("evaluator", {"bin/eval": b"evaluator\n"}, "1.0.0")
    det_id, _ = kit.closure("detector", {"rules/inv.json": b"{}\n"}, "1.0.0")

    rows = sorted([_grammar_row(kit, l, ("grammar:" + l).encode())
                   for l in langs], key=lambda r: r["grammarId"].encode())
    if mutate == "data-grammar-claims-code":
        for r in rows:
            if r["languageId"] == "markdown":
                r["syntaxClass"] = "code"
    bundle = {"schemaVersion": 1, "closureId": gclosure,
              "parserName": "opensip-grammar-parser",
              "parserVersion": ("9.9.9"
                                if mutate == "grammar-version-not-from-manifest"
                                else "4.2.0"),
              "bundleDigest": w.raw(b"grammar-bundle-manifest\n"),
              "grammars": rows,
              "normalizer": {"normalizerId": "grammar-normalizer",
                             "normalizerVersion": "1.0.0",
                             "specificationDigest": w.raw(b"normalizer-spec\n")}}
    ctx = {"schemaVersion": 2, "grammarBundle": bundle}
    ctx_ref, ctx_hx = kit.mint_native("native.context.syntax.v2", ctx)

    sel = selected if mutate != "unselected-grammar" else [selected[0]]
    if mutate == "select-a-grammar-not-in-the-bundle":
        sel = selected + ["g.rust"]
    uni = {"schemaVersion": 2, "nativeContextId": ctx_ref,
           "selectedGrammarIds": sorted(sel), "resolutionAttempted": False}
    u_ref, u_hx = kit.mint_native("native.semantic-universe.syntax.v2", uni)

    scope_desc = {"schemaVersion": 2, "workspaceRoots": ["."],
                  "pathPrefixes": [], "excludedPathPrefixes": [".git"]}
    budget = {"unit": "work-units", "limit": 50000}
    config = {"analysis": {"profileId": "default",
                           "capabilities": sorted(["inventory", "syntax",
                                                   "clones-fact"]),
                           "budget": dict(budget)},
              "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted(
                [{"capabilityId": c, "languageMode": "syntax-only",
                  "workspaceRoot": ".", "required": True}
                 for c in ("inventory", "syntax", "clones-fact", "references")],
                key=lambda x: C(x)),
            "policyPackIds": ["opensip.builtin"], "parameters": []}
    grant = {"schemaVersion": 2, "projectId": w.projectId,
             "principals": [{"kind": "first-party", "closureId": prov_id,
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(["read-source", "native-analysis"]),
             "scopeDigest": w.record(scope_desc)}
    snap_id, snap = kit.snapshot(config, scope_desc)

    providers = [{"providerId": "syntax-all", "language": "*",
                  "providerVersionSource": "signed-closure-manifest",
                  "toolchainIdentitySource": "native-context-v2",
                  "relations": {"file": "enumerated", "declares": "syntactic",
                                "clones": "normalized-body-hash"},
                  "platformIds": ["macos-aarch64"]}]
    absent = [{"providerId": "syntax-all", "language": "*",
               "relationIds": sorted(["calls", "imports", "reachability",
                                      "references", "types",
                                      "unresolved-edge"]),
               "coverageState": "unavailable",
               "deficiency": "language-tier-unsupported"}]
    cm, cm_bytes, cm_bd, cap_id = B.capability_manifest(kit, providers, absent)
    policy, pd, waivers, wd, program, rpd, rule = B.policy_and_program(kit)
    plan_id, _ = B.plan(kit, snap_id, cm_bd, cap_id, [prov_id, eval_id, det_id],
                        w.record(spec), w.record(config),
                        [] if mutate == "hidden-context" else [ctx_hx], [], pd, wd,
                        w.record(scope_desc), budget, w.record(grant))

    # ---- facts: inventory over EVERY path, code facts only where supported
    facts, file_subjects = [], []
    for row in snap["sourceInventory"]:
        fid, _ = kit.fact(snap_id, "file", "enumerated", u_hx, u_hx, prov_id,
                          {"path": row["path"], "contentSha256": row["sha256"],
                           "byteLength": row["bytes"]}, [])
        facts.append(fid)
        file_subjects.append(row["path"])

    body_ids = {}
    if kind == "code":
        data = w.cas[f_js["sha256"]]
        i = data.index(JS_BODY)
        dec_id, _ = kit.fact(
            snap_id, "declares", "syntactic", u_hx, u_hx, prov_id,
            {"container": "module:lib/util.js",
             "declared": "function:lib/util.js#pad",
             "declarationKind": "function"},
            [{"path": "README.md" if mutate == "markdown-anchored-code-fact"
                      else "lib/util.js",
              "blobDigest": (f_md if mutate == "markdown-anchored-code-fact"
                             else f_js)["sha256"],
              "startByte": 0, "endByte": 5}])
        facts.append(dec_id)
        ident, blv, lang = B.mint_body_identity(
            kit, "native.semantic-universe.syntax.v2", uni, ctx, {},
            "lib/util.js", JS_BODY, "L0-verbatim", lv["L0-verbatim"])
        body_ids["lib/util.js@L0"] = ident
        body_ids["_languageId"] = lang
        cl_id, _ = kit.fact(snap_id, "clones", "normalized-body-hash", u_hx,
                            u_hx, prov_id,
                            {"bodyIdentity": ident,
                             "normalisationLevel": "L0-verbatim",
                             "normalisationVersion": lv["L0-verbatim"]},
                            [{"path": "lib/util.js",
                              "blobDigest": f_js["sha256"],
                              "startByte": i, "endByte": i + len(JS_BODY)}])
        facts.append(cl_id)

    # ---- scopes / coverage ----------------------------------------------
    scopes, covs = [], []

    def add(relation, rung, subjects, entry):
        sid, shx, sd = kit.scope(snap_id, u_hx, u_hx, relation, rung, prov_id,
                                 subjects)
        scopes.append((sid, shx, sd))
        covs.append(kit.coverage(sid, shx, sd, entry))
        return sid

    add("file", "enumerated", file_subjects, B.entry_complete())
    if kind == "code":
        add("declares", "syntactic", ["symbol:function:lib/util.js#pad"],
            B.entry_complete())
        add("clones", "normalized-body-hash", ["lib/util.js"],
            B.entry_complete())
        # a README.md-scoped clone request: UNAVAILABLE even in a mixed snapshot
        add("clones", "normalized-body-hash", ["README.md"],
            B.entry_complete() if mutate == "false-complete-on-unsupported-scope"
            else B.entry_unavailable())
    else:
        # a data/document grammar set bears NO body identity and no code fact
        add("clones", "normalized-body-hash", ["README.md", "data/config.json"],
            B.entry_complete() if mutate == "false-complete-on-unsupported-scope"
            else B.entry_unavailable())
        add("declares", "syntactic", ["symbol:module:data/config.json"],
            B.entry_unavailable())
    # a resolved semantic rung under a compiler-free universe
    add("references", "resolved-binding", ["symbol:module:x"],
        B.entry_unavailable(resolutionCompleteness={
            "state": "not-attempted", "attempted": False,
            "examinedExhaustive": False, "stageTerminal": None,
            "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}))

    view_id, _ = kit.view(plan_id, [s[0] for s in scopes], facts,
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
        facts[0], covs[0][0], extra_inputs)
    ev_id = B.evidence(kit, plan_id, [view_id], [c[0] for c in covs], [],
                       finding_ids, proof_id)
    seal_id, run_id = B.seal_and_run(kit, plan_id, exec_plan_id, ev_id, eval_id,
                                     pd, proof_id, snap_id, cap_id)
    return dict(kit=kit, run=run_id, plan=plan_id, universe=u_hx,
                context=ctx_hx, bodyIdentities=body_ids,
                capabilityManifestId=cap_id, inventory=file_subjects)
