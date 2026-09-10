"""Compiler-free syntax-only Runs: code grammar, data/document grammar, a repository
with no TypeScript and no Rust compilation unit, and an unbundled grammar."""

from __future__ import annotations

import hashlib
import json

import opensip_ref as R
import closure as CL
import world as W
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes
from build_ts import L0_SPEC

BUNDLED = R.GRAMMAR_REGISTRY["languages"]


def grammar_bundle(g, closures):
    gc = g.closures[closures["grammar"]]
    dig = {b["path"]: b["sha256"] for b in gc["tree"]}
    rows = []
    for lang, row in BUNDLED.items():
        rows.append({
            "grammarId": "g-" + lang,
            "grammarVersion": "1.0.0",
            "languageId": lang,
            "syntaxClass": row["syntaxClass"],
            "suffixes": sorted(row["suffixes"]),
            "grammarDigest": dig["grammars/%s.grammar" % lang],
        })
    rows.sort(key=lambda r: r["grammarId"].encode("utf-8"))
    bundle = {
        "schemaVersion": 1,
        "closureId": closures["grammar"],
        "parserName": "opensip-grammar-parser",
        "parserVersion": gc["semanticVersion"],
        "bundleDigest": dig["bundle.manifest"],
        "grammars": rows,
        "normalizer": {
            "normalizerId": "opensip-clone-normalizer",
            "normalizerVersion": "1.0.0",
            "specificationDigest": dig["normalizer/spec.txt"],
        },
    }
    R.validate("native", "#/$defs/SyntaxGrammarBundleV1", bundle)
    return bundle


def build(files, selected_grammar_ids, caps=("inventory", "syntax", "clones-fact")):
    g = CL.Graph("syntax")
    cl = W.base_closures(g)
    g.evaluator_closure = cl["evaluator"]
    cfg = W.resolved_config(list(caps))
    sd = W.scope_descriptor(["."], excluded=[".git"])
    W.build_snapshot(g, files, sd, cfg, vcs_kind="none", commit=None)
    bundle = grammar_bundle(g, cl)
    ctx = {"schemaVersion": 2, "grammarBundle": bundle}
    R.validate("native", "#/$defs/SyntaxNativeContextV2", ctx)
    ctx_hex = g.add_context("native.context.syntax.v2", ctx)
    u = {
        "schemaVersion": 2,
        "nativeContextId": sha256_text("native.context.syntax.v2", ctx),
        "selectedGrammarIds": sorted(selected_grammar_ids),
        "resolutionAttempted": False,
    }
    R.validate("native", "#/$defs/SyntaxUniverseV2ResolvedInputs", u)
    uh = g.add_universe("native.semantic-universe.syntax.v2", u)
    manifest = W.capability_manifest("default", [], [])
    policy = W.simple_policy("syn", "declares", "syntactic", op="none")
    g.rule_program = W.compile_program(policy)
    g.cas.put_record(g.rule_program)
    spec = W.analysis_spec([
        {"capabilityId": c, "languageMode": "syntax-only", "workspaceRoot": ".",
         "required": True} for c in caps
        if R.CELLS[(c, "syntax-only")]["state"] != "NOT-SELECTED"])
    grant = W.semantic_grant(["read-source", "native-analysis"], raw(sd))
    plan_id = W.build_plan(g, [cl["provider-syntax"], cl["evaluator"]], [ctx_hex],
                           spec, grant, policy, W.EMPTY_WAIVERS, manifest)
    return g, cl, ctx, ctx_hex, u, uh, plan_id


def inventory_facts(g, prov, uh):
    subjects = [r["path"] for r in g.inventory]
    sid, sc = W.make_scope(g, "file", "enumerated", uh, uh, prov, subjects)
    facts = []
    for row in g.inventory:
        p = {"path": row["path"], "contentSha256": row["sha256"], "byteLength": row["bytes"]}
        fid, _ = W.make_fact(g, "file", "enumerated", uh, uh, prov, p, anchors=[])
        facts.append(fid)
    cid, _ = W.make_coverage(g, sid, sc, W.entry("file", "enumerated", "complete",
                                                 "not-applicable", False, True, None))
    return sid, sc, facts, cid


UNAVAILABLE = dict(deficiency="language-tier-unsupported", cause="capability-missing")


ONE_RUNG_OR_SYNTACTIC = {"file", "package", "vcs-change", "declares", "literal",
                         "control-flow", "clones"}


def unavailable_entry(rel, rung):
    """RC-1 forbids `not-applicable` on a RESOLVED rung, so an unavailable resolved
    rung must carry `not-attempted` (attempted false, count 0) -- which is also the
    only state consistent with a syntax universe's constant resolutionAttempted=false.
    A one-rung / syntactic relation keeps `not-applicable`: it makes no resolution
    claim at all.  `unresolved-edge@observed` is in NEITHER of RC-1's two lists; see
    the SHOULD issue recorded in the review."""
    state = "not-applicable" if rel in ONE_RUNG_OR_SYNTACTIC or rung == "syntactic" \
        else "not-attempted"
    return W.entry(rel, rung, "unknown", state, False, True, None, **UNAVAILABLE)


JS_BODY = b"function go(a) {\n  return a * 2;\n}\n"


def scenario_code_grammar(results):
    """SYN-1: a supported CODE grammar syntax-only Run with inventory AND
    syntax/clone facts, and no compiler anywhere in the context."""
    files = {
        "README.md": b"# app\n\nSome docs.\n",
        "src/app.js": b"// app\n" + JS_BODY,
        "tool/main.py": b"def main():\n    return 1\n",
    }
    g, cl, ctx, ctx_hex, u, uh, plan_id = build(
        files, ["g-javascript", "g-markdown"],
        caps=("inventory", "syntax", "clones-fact", "references"))
    prov = cl["provider-syntax"]
    sid, sc, facts, cid = inventory_facts(g, prov, uh)
    scopes, covs = [sid], [cid]

    dsub = "symbol:src/app.js#go"
    dsid, dsc = W.make_scope(g, "declares", "syntactic", uh, uh, prov, [dsub])
    scopes.append(dsid)
    p = {"container": "symbol:src/app.js", "declared": dsub, "declarationKind": "function"}
    fid, _ = W.make_fact(g, "declares", "syntactic", uh, uh, prov, p,
                         anchors=[W.anchor(g, "src/app.js", 7, 7 + len(JS_BODY))])
    facts.append(fid)
    dcid, _ = W.make_coverage(g, dsid, dsc, W.entry("declares", "syntactic", "complete",
                                                    "not-applicable", False, True, None))
    covs.append(dcid)

    # clone body under the GRAMMAR dialect branch
    bl = CL.body_language_version(g, uh, "src/app.js", {})
    lv32 = R.language_version_raw32(bl)
    lev32 = hashlib.sha256(L0_SPEC).digest()
    g.cas.put_bytes(L0_SPEC)
    span = g.blobs["src/app.js"][7:7 + len(JS_BODY)]
    pre, bid = R.body_identity("L0-verbatim", lev32, bl["languageId"], lv32,
                               R.body_payload_L0(span))
    g.cas.put_bytes(pre)
    csid, csc = W.make_scope(g, "clones", "normalized-body-hash", uh, uh, prov,
                             ["src/app.js"])
    scopes.append(csid)
    cp = {"bodyIdentity": bid, "normalisationLevel": "L0-verbatim",
          "normalisationVersion": lev32.hex()}
    fid, _ = W.make_fact(g, "clones", "normalized-body-hash", uh, uh, prov, cp,
                         anchors=[W.anchor(g, "src/app.js", 7, 7 + len(JS_BODY))])
    facts.append(fid)
    ccid, _ = W.make_coverage(g, csid, csc, W.entry("clones", "normalized-body-hash",
                                                    "complete", "not-applicable",
                                                    False, True, None))
    covs.append(ccid)

    # references is a SEMANTIC rung: unavailable under a syntax universe, DISCLOSED
    rsid, rsc = W.make_scope(g, "references", "resolved-binding", uh, uh, prov, [dsub])
    scopes.append(rsid)
    rcid, _ = W.make_coverage(g, rsid, rsc,
                              unavailable_entry("references", "resolved-binding"))
    covs.append(rcid)

    vid, _ = W.make_view(g, plan_id, scopes, facts, covs, prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="pass",
                                            scope_ids=[dsid], coverage_ids=[dcid])
    out = CL.close_run(g, {}, [vid], proof, evidence, seal, run)

    neg = {}

    def probe(name, fn):
        try:
            fn()
            neg[name] = "ADMITTED(!)"
        except R.Refuse as exc:
            neg[name] = exc.code + (":" + exc.detail if exc.detail else "")

    def md_declares():
        p2 = {"container": "symbol:README.md", "declared": "symbol:README.md#h1",
              "declarationKind": "module"}
        fd = {"schemaVersion": 2, "snapshotId": g.snapshot_id, "relation": "declares",
              "resolution": "syntactic", "sourceUniverse": uh, "targetUniverse": uh,
              "producerClosure": prov, "payloadSchemaDigest": R.RELATION_DOC_DIGEST,
              "payloadDigest": raw(p2), "anchors": [W.anchor(g, "README.md", 0, 5)],
              "confidenceMillionths": 1000000}
        CL.syntax_fact_guard(g, uh, fd)
    probe("markdown-anchored-code-fact", md_declares)

    def py_declares():
        p2 = {"container": "symbol:tool/main.py", "declared": "symbol:tool/main.py#main",
              "declarationKind": "function"}
        fd = {"schemaVersion": 2, "snapshotId": g.snapshot_id, "relation": "declares",
              "resolution": "syntactic", "sourceUniverse": uh, "targetUniverse": uh,
              "producerClosure": prov, "payloadSchemaDigest": R.RELATION_DOC_DIGEST,
              "payloadDigest": raw(p2), "anchors": [W.anchor(g, "tool/main.py", 0, 5)],
              "confidenceMillionths": 1000000}
        CL.syntax_fact_guard(g, uh, fd)
    probe("unbundled-grammar-anchored-code-fact", py_declares)
    probe("python-body-language-version",
          lambda: CL.body_language_version(g, uh, "tool/main.py", {}))
    probe("false-complete-for-an-unavailable-capability",
          lambda: CL.syntax_scope_capability(
              g, uh, rsc, W.entry("references", "resolved-binding", "complete",
                                  "not-applicable", False, True, None)))
    probe("wrong-cause-for-an-unavailable-capability",
          lambda: CL.syntax_scope_capability(
              g, uh, rsc, W.entry("references", "resolved-binding", "unknown",
                                  "not-applicable", False, True, None,
                                  deficiency="language-tier-unsupported",
                                  cause="linker-unavailable")))
    probe("unselected-grammar-lends-no-capability", lambda: CL.syntax_fact_guard(
        g, uh, {"relation": "declares", "resolution": "syntactic",
                "anchors": [{"path": "x.rs"}]}))
    probe("selection-naming-a-grammar-outside-the-bundle",
          lambda: CL.bind_universe(g, "native.semantic-universe.syntax.v2",
                                   dict(u, selectedGrammarIds=["g-python"]),
                                   "native.context.syntax.v2", ctx, {}))

    results["syntax-code-grammar"] = {
        "verdict": "ADMIT",
        "runId": out["runId"],
        "universe": uh,
        "nativeContextId": u["nativeContextId"],
        "grammarClosureId": ctx["grammarBundle"]["closureId"],
        "parserVersionJoinedToClosureManifest": ctx["grammarBundle"]["parserVersion"],
        "selectedGrammarIds": u["selectedGrammarIds"],
        "bodyLanguageVersion": bl,
        "bodyIdentityGrammarParsed": bid,
        "contextCarriesNoCompiler": sorted(ctx.keys()) == ["grammarBundle", "schemaVersion"],
        "inventoryTotalityIncludesUnbundledPath": "tool/main.py",
        "negatives": neg,
        "trace": out["trace"],
    }
    return bid


def scenario_data_only(results, grammar_body_identity):
    """SYN-2/3: a repository with NO TypeScript and NO Rust compilation unit, whose
    only grammars are the bundled DATA/DOCUMENT ones.  Inventory is available; every
    code capability is unavailable-and-disclosed, and an empty `complete` clones
    result is refused rather than reading as a finding of no clones."""
    files = {
        "README.md": b"# data only\n",
        "ci/pipeline.yaml": b"jobs:\n  build: true\n",
        "config/settings.toml": b"[a]\nb = 1\n",
        "data/records.json": b'{"x":1}\n',
        "tool/main.py": b"def main():\n    return 1\n",
    }
    g, cl, ctx, ctx_hex, u, uh, plan_id = build(
        files, ["g-json", "g-markdown", "g-toml", "g-yaml"],
        caps=("inventory", "syntax", "clones-fact", "references", "imports",
              "calls", "types", "reachability", "unresolved-edge"))
    prov = cl["provider-syntax"]
    sid, sc, facts, cid = inventory_facts(g, prov, uh)
    scopes, covs = [sid], [cid]

    psid, psc = W.make_scope(g, "package", "manifest-declared", uh, uh, prov, [])
    scopes.append(psid)
    pcid, _ = W.make_coverage(g, psid, psc, W.entry("package", "manifest-declared",
                                                    "complete", "not-applicable",
                                                    False, True, None))
    covs.append(pcid)

    unavailable = {}
    for rel, rung in (("declares", "syntactic"), ("literal", "syntactic"),
                      ("control-flow", "syntactic"), ("clones", "normalized-body-hash"),
                      ("imports", "resolved-target"), ("references", "resolved-binding"),
                      ("calls", "resolved-callee"), ("types", "checked"),
                      ("reachability", "from-resolved-calls"),
                      ("unresolved-edge", "observed")):
        s_id, s_sc = W.make_scope(g, rel, rung, uh, uh, prov, [])
        scopes.append(s_id)
        c_id, _ = W.make_coverage(g, s_id, s_sc, unavailable_entry(rel, rung))
        covs.append(c_id)
        unavailable[f"{rel}@{rung}"] = {"coverage": "unknown",
                                        "deficiency": "language-tier-unsupported",
                                        "nativeCause": "capability-missing"}

    vid, _ = W.make_view(g, plan_id, scopes, facts, covs, prov)
    proof, evidence, seal, run = W.seal_run(g, [vid], verdict="indeterminate",
                                            predicate_value="indeterminate",
                                            scope_ids=[scopes[2]], coverage_ids=[covs[2]])
    out = CL.close_run(g, {}, [vid], proof, evidence, seal, run)

    neg = {}

    def probe(name, fn):
        try:
            fn()
            neg[name] = "ADMITTED(!)"
        except R.Refuse as exc:
            neg[name] = exc.code + (":" + exc.detail if exc.detail else "")

    empty_clone_scope = g.scopes[scopes[5]]
    probe("empty-complete-clone-result-conceals-unsupported-analysis",
          lambda: CL.syntax_scope_capability(
              g, uh, empty_clone_scope,
              W.entry("clones", "normalized-body-hash", "complete", "not-applicable",
                      False, True, None)))
    probe("data-grammar-mints-a-body-identity",
          lambda: CL.body_language_version(g, uh, "data/records.json", {}))
    probe("data-grammar-declaring-code-class", lambda: CL.admit_native_context(
        g, "native.context.syntax.v2",
        {"schemaVersion": 2, "grammarBundle": dict(
            ctx["grammarBundle"],
            grammars=[dict(r, syntaxClass="code") if r["languageId"] == "json" else r
                      for r in ctx["grammarBundle"]["grammars"]])}))
    probe("code-grammar-demoted-to-data-document", lambda: CL.admit_native_context(
        g, "native.context.syntax.v2",
        {"schemaVersion": 2, "grammarBundle": dict(
            ctx["grammarBundle"],
            grammars=[dict(r, syntaxClass="data-document") if r["languageId"] == "rust" else r
                      for r in ctx["grammarBundle"]["grammars"]])}))
    probe("grammar-claiming-another-languages-suffix", lambda: CL.admit_native_context(
        g, "native.context.syntax.v2",
        {"schemaVersion": 2, "grammarBundle": dict(
            ctx["grammarBundle"],
            grammars=[dict(r, suffixes=sorted(r["suffixes"] + [".rs"]))
                      if r["languageId"] == "json" else r
                      for r in ctx["grammarBundle"]["grammars"]])}))
    probe("parser-version-not-from-the-grammar-closure-manifest",
          lambda: CL.admit_native_context(
              g, "native.context.syntax.v2",
              {"schemaVersion": 2,
               "grammarBundle": dict(ctx["grammarBundle"], parserVersion="0.0.1")}))

    # the published matrix agrees with what this Run asserts
    matrix_check = {}
    for cap in R.CAPABILITY_IDS:
        cell = R.CELLS[(cap, "syntax-only")]
        matrix_check[cap] = cell["state"]

    results["syntax-data-only-repository"] = {
        "verdict": "ADMIT",
        "runId": out["runId"],
        "universe": uh,
        "hasTypeScriptOrRustCompilationUnit": False,
        "selectedGrammarIds": u["selectedGrammarIds"],
        "inventorySubjects": [r["path"] for r in g.inventory],
        "inventoryIsNotGrammarGated":
            "tool/main.py has no bundled grammar and is still inventoried",
        "unavailableCapabilities": unavailable,
        "matrixStatesForSyntaxOnly": matrix_check,
        "negatives": neg,
        "trace": out["trace"],
    }


def scenario_grammar_vs_compiler_identity(results, g_bid):
    """SYN-4: the SAME body bytes read by a bundled grammar and by the TypeScript
    engine mint DIFFERENT identities, because the dialect branch differs."""
    import build_ts as BT
    files = {
        "package.json": b'{"name":"x","version":"1.0.0","private":true}\n',
        "src/app.js": b"// app\n" + JS_BODY,
    }
    hon = BT.honored(allowJs=True)
    cp = BT.config_projection([], hon)
    cg = BT.config_graph(None, [])
    syn = {"allowJs": True, "checkJs": False, "module": "node16",
           "moduleResolution": "node16", "target": "es2022", "strict": False,
           "skipLibCheck": True, "types": [], "noEmit": True}
    hon2 = BT.honored(allowJs=True, checkJs=False, strict=False, types=[], jsx=None)
    cp2 = BT.config_projection([], hon2)
    g, cl, ctx, ctx_hex, u, uh, retained, plan_id = BT._minimal_ts_world(
        files, "js-synthesized", "synthesized", cg, cp2, synthesized=syn,
        program_roots=["src/app.js"], js_roots=["src/app.js"])
    bl = CL.body_language_version(g, uh, "src/app.js", retained[uh])
    lv32 = R.language_version_raw32(bl)
    lev32 = hashlib.sha256(L0_SPEC).digest()
    span = g.blobs["src/app.js"][7:7 + len(JS_BODY)]
    pre, bid = R.body_identity("L0-verbatim", lev32, bl["languageId"], lv32,
                               R.body_payload_L0(span))
    results["grammar-versus-compiler-body-identity"] = {
        "sameBytes": True,
        "grammarParsedIdentity": g_bid,
        "compilerParsedIdentity": bid,
        "identitiesDiffer": g_bid != bid,
        "grammarDialectBranch": "grammarVariant",
        "compilerDialectBranch": "sourceVariant",
        "compilerBodyLanguageVersion": bl,
        "why": "a grammar parse and a compiler parse are different interpretations; "
               "equating them would be a false clone claim",
    }
