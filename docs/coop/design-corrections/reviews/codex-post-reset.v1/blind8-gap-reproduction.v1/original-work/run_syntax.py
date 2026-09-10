"""CB-RUN-SX: complete compiler-free syntax-only Runs.

A repository with NO TypeScript and NO Rust compilation unit at all.
Exercises the advertised grammar capabilities:
  * a supported CODE grammar with inventory and syntax/clone facts,
  * an already bundled DATA/DOCUMENT grammar with its declared inventory
    capability and explicit unavailability for what its class cannot support,
  * an UNBUNDLED language (.py) that is still inventoried.
"""
from __future__ import annotations

import assemble
import build
import closure as CL
import osip
from build import Fixture, coverage_entry
from osip import C, H, raw_sha256

PLATFORM = "macos-x86_64"
PARSER_VERSION = "0.9.0"

JS_BODY = b"{\n  return a + b;\n}"
TOOL_JS = b"function add(a, b) " + JS_BODY + b"\n"

# native section 1.2: the bundled grammar set is CLOSED and has SEVEN languages.
BUNDLED = CL.GRAMMAR_CAP["languages"]

CAP_MANIFEST = {
    "schemaVersion": 1, "profile": "default",
    "providers": [
        {"providerId": "opensip.provider.syntax", "language": "*",
         "providerVersionSource": "closure-manifest",
         "toolchainIdentitySource": "native-context",
         "relations": {"clones": "normalized-body-hash", "declares": "syntactic",
                       "file": "enumerated"},
         "platformIds": [PLATFORM]},
    ],
    "coverageForAbsent": [
        {"providerId": "opensip.provider.syntax", "language": "*",
         "relationIds": sorted(["calls", "imports", "reachability", "references",
                                "types", "unresolved-edge"]),
         "coverageState": "unavailable",
         "deficiency": "language-tier-unsupported"},
    ],
}


def build_run(shape="mixed", selected=None, mutate=None):
    """shape: 'mixed' (code + data + unbundled) | 'data-only'"""
    fx = Fixture("cb-sx-" + shape)
    m = mutate or {}

    if shape == "mixed":
        fx.add_file("scripts/tool.js", TOOL_JS)
        fx.add_file("docs/notes.md", b"# notes\n\nsome prose\n")
        fx.add_file("data/config.yaml", b"key: value\n")
        fx.add_file("tool/main.py", b"def main():\n    pass\n")
    else:
        fx.add_file("docs/notes.md", b"# notes\n")
        fx.add_file("data/config.yaml", b"key: value\n")
        fx.add_file("data/config.json", b'{"key":"value"}\n')
    inv = {r["path"]: r for r in fx.inventory()}

    grammar_files = {}
    for lang in sorted(BUNDLED):
        grammar_files["grammars/%s.grammar" % lang] = ("#grammar %s\n" % lang).encode()
    grammar_files["bundle.manifest"] = b"#syntax grammar bundle manifest\n"
    grammar_files["normalizer/level-spec.txt"] = (
        b"opensip.normalisation-level-specification\nlevel=L0-verbatim\n"
        b"grammar-lexical-boundaries=v1\n")
    g_cid, _, g_members = fx.closure("syntax-grammars", "grammar", grammar_files,
                                     PARSER_VERSION, PLATFORM, protocol_major=1)
    prov_cid, _, _ = fx.closure("syntax-provider", "provider",
                                {"bin/provider": b"#grammar-only provider\n"},
                                "1.0.0", PLATFORM, protocol_major=1)
    eval_cid, _, _ = fx.closure("evaluator", "evaluator",
                                {"bin/evaluator": b"#pure evaluator\n"},
                                "1.0.0", PLATFORM, protocol_major=1)

    grammars = []
    for lang in sorted(BUNDLED):
        row = BUNDLED[lang]
        grammars.append({"grammarId": "g-" + lang, "grammarVersion": "1.0.0",
                         "languageId": lang, "syntaxClass": row["syntaxClass"],
                         "suffixes": sorted(row["suffixes"],
                                            key=lambda x: x.encode()),
                         "grammarDigest": g_members["grammars/%s.grammar" % lang]})
    grammars.sort(key=lambda g: g["grammarId"].encode())
    if m.get("data_grammar_claims_code"):
        for g in grammars:
            if g["languageId"] == "markdown":
                g["syntaxClass"] = "code"
    bundle = {"schemaVersion": 1, "closureId": g_cid, "parserName": "opensip-grammars",
              "parserVersion": PARSER_VERSION,
              "bundleDigest": g_members["bundle.manifest"],
              "grammars": grammars,
              "normalizer": {"normalizerId": "opensip.syntax-normalizer",
                             "normalizerVersion": "1.0.0",
                             "specificationDigest":
                                 g_members["normalizer/level-spec.txt"]}}
    if m.get("parser_version_not_from_manifest"):
        bundle["parserVersion"] = "0.9.1"
    ctx = {"schemaVersion": 2, "grammarBundle": bundle}

    sel = selected or (["g-javascript", "g-markdown", "g-yaml"] if shape == "mixed"
                       else ["g-json", "g-markdown", "g-yaml"])
    uni = {"schemaVersion": 2, "nativeContextId": None,
           "selectedGrammarIds": sorted(sel, key=lambda x: x.encode()),
           "resolutionAttempted": False}

    caps = ["inventory", "syntax", "clones-fact", "references"]
    A = assemble.Assembly(
        fx, capabilities=caps,
        spec_rows=[{"capabilityId": c, "languageMode": "syntax-only",
                    "workspaceRoot": ".", "required": True} for c in caps],
        capability_manifest=CAP_MANIFEST)
    ctx_hex = A.add_context("native.context.syntax.v2", ctx,
                            "#/$defs/SyntaxNativeContextV2")
    uni["nativeContextId"] = "sha256:" + ctx_hex
    uni_hex = A.add_universe("native.semantic-universe.syntax.v2", uni,
                             "#/$defs/SyntaxUniverseV2ResolvedInputs", "syntax-universe")
    A.seal_snapshot()
    A.seal_plan([prov_cid, eval_cid, g_cid])

    lvb = CL.DOMAIN_SETS["native-semantic-universe"][
        "native.semantic-universe.syntax.v2"]["languageVersionBinding"]

    # ---- inventory facts: NEVER grammar-gated, on EVERY inventoried path ----
    file_facts = []
    for p, r in sorted(inv.items()):
        file_facts.append(A.add_fact(
            "file", "enumerated", uni_hex, uni_hex, prov_cid,
            {"path": p, "contentSha256": r["sha256"], "byteLength": r["bytes"]}, []))

    code_facts, body_id, blv = [], None, None
    if shape == "mixed":
        blv, cause = CL.derive_body_language_version(lvb, ctx, uni, "scripts/tool.js")
        assert blv is not None, cause
        spec = grammar_files["normalizer/level-spec.txt"]
        lvhex = raw_sha256(spec)
        src = fx.files["scripts/tool.js"]
        start = src.index(JS_BODY)
        end = start + len(JS_BODY)
        body_id, frame = osip.body_identity("L0-verbatim", lvhex, blv["languageId"],
                                            blv, osip.l0_payload(src[start:end]))
        fx.s.blobs[body_id.split(":")[1]] = frame
        code_facts.append(A.add_fact(
            "clones", "normalized-body-hash", uni_hex, uni_hex, prov_cid,
            {"bodyIdentity": body_id, "normalisationLevel": "L0-verbatim",
             "normalisationVersion": lvhex},
            [{"path": "scripts/tool.js",
              "blobDigest": inv["scripts/tool.js"]["sha256"],
              "startByte": start, "endByte": end}]))
        anchors = [{"path": "scripts/tool.js",
                    "blobDigest": inv["scripts/tool.js"]["sha256"],
                    "startByte": 0, "endByte": len(TOOL_JS)}]
        if m.get("markdown_anchored_code_fact"):
            anchors = [{"path": "docs/notes.md",
                        "blobDigest": inv["docs/notes.md"]["sha256"],
                        "startByte": 0, "endByte": 3}]
        code_facts.append(A.add_fact(
            "declares", "syntactic", uni_hex, uni_hex, prov_cid,
            {"container": "module:scripts/tool.js",
             "declared": "function:scripts/tool.js#add",
             "declarationKind": "function"}, anchors))

    all_paths = sorted(inv)
    scopes, covs = [], []
    s_file, h_file = A.add_scope("file", "enumerated", uni_hex, uni_hex, prov_cid,
                                 all_paths)
    scopes.append(s_file)
    covs.append(A.add_coverage(s_file, h_file, coverage_entry(
        "file", "enumerated", "sha256:" + h_file, len(all_paths), "complete")))

    if shape == "mixed":
        s_dec, h_dec = A.add_scope("declares", "syntactic", uni_hex, uni_hex,
                                   prov_cid, ["module:scripts/tool.js"])
        scopes.append(s_dec)
        covs.append(A.add_coverage(s_dec, h_dec, coverage_entry(
            "declares", "syntactic", "sha256:" + h_dec, 1, "complete")))
        s_cl, h_cl = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                                 prov_cid, ["scripts/tool.js"])
        scopes.append(s_cl)
        covs.append(A.add_coverage(s_cl, h_cl, coverage_entry(
            "clones", "normalized-body-hash", "sha256:" + h_cl, 1, "complete")))
        # a clones scope over a DATA-DOCUMENT path: no body identity, and the
        # suffix backstop refuses a determinate answer
        s_md, h_md = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                                 prov_cid, ["docs/notes.md"], label="markdown")
        md_entry = coverage_entry("clones", "normalized-body-hash", "sha256:" + h_md,
                                  1, "unknown",
                                  deficiency="language-tier-unsupported",
                                  cause="capability-missing")
        if m.get("false_complete_data_clone"):
            md_entry = coverage_entry("clones", "normalized-body-hash",
                                      "sha256:" + h_md, 1, "complete")
        scopes.append(s_md)
        covs.append(A.add_coverage(s_md, h_md, md_entry))
    else:
        # DATA-ONLY: declares and clones are unavailable; a complete EMPTY result
        # would conceal unsupported analysis and must refuse.
        s_dec, h_dec = A.add_scope("declares", "syntactic", uni_hex, uni_hex,
                                   prov_cid, ["module:data/config.json"])
        dec_entry = coverage_entry("declares", "syntactic", "sha256:" + h_dec, 1,
                                   "unknown", deficiency="language-tier-unsupported",
                                   cause="capability-missing")
        if m.get("false_complete_empty_declares"):
            dec_entry = coverage_entry("declares", "syntactic", "sha256:" + h_dec, 1,
                                       "complete")
        scopes.append(s_dec)
        covs.append(A.add_coverage(s_dec, h_dec, dec_entry))
        s_cl, h_cl = A.add_scope("clones", "normalized-body-hash", uni_hex, uni_hex,
                                 prov_cid, ["docs/notes.md"])
        scopes.append(s_cl)
        covs.append(A.add_coverage(s_cl, h_cl, coverage_entry(
            "clones", "normalized-body-hash", "sha256:" + h_cl, 1, "unknown",
            deficiency="language-tier-unsupported", cause="capability-missing")))

    # a SEMANTIC capability under a grammar-only universe: correctly unavailable
    s_ref, h_ref = A.add_scope("references", "resolved-binding", uni_hex, uni_hex,
                               prov_cid, ["symbol:anything"])
    ref_entry = coverage_entry(
        "references", "resolved-binding", "sha256:" + h_ref, 1, "unknown",
        deficiency="language-tier-unsupported", cause="capability-missing",
        rc={"state": "not-attempted", "attempted": False, "examinedExhaustive": True,
            "stageTerminal": None, "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": []})
    if m.get("false_complete_references"):
        ref_entry = coverage_entry(
            "references", "resolved-binding", "sha256:" + h_ref, 1, "complete")
    scopes.append(s_ref)
    covs.append(A.add_coverage(s_ref, h_ref, ref_entry))

    view = A.seal_view(prov_cid, scopes, file_facts + code_facts, covs,
                       [build.RELATION_DOC_DIGEST, build.NATIVE_DOC_DIGEST])
    run_id = A.seal_run(eval_cid, prov_cid, [view])
    A.extra = {"bodyIdentity": body_id, "bodyLanguageVersion": blv,
               "contextHex": ctx_hex, "universeHex": uni_hex,
               "selectedGrammarIds": uni["selectedGrammarIds"],
               "bundledLanguages": sorted(BUNDLED)}
    return fx, A, run_id
