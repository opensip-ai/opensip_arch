"""Compiler-free syntax-only Runs.

Two advertised grammar classes are exercised:
  * a supported CODE grammar (rust, via the bundled grammar, WITHOUT Cargo) with
    inventory and syntax/clone facts;
  * an already-bundled DATA/DOCUMENT grammar (markdown/json/toml/yaml) with its
    declared inventory capability and explicit unavailability for the capabilities
    its class does not support.
The repository deliberately contains NO TypeScript and NO Rust compilation unit,
so no compiler universe exists and the semantic capabilities are correctly
unavailable.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402

SX_SPEC = b"level-specification L1-lexical: grammar-bundle normalizer v1"
BODY = b"{\n    a + b\n}"

REG = kit.doc("native")["x-opensip-grammar-capability-registry"]["languages"]


def _files(kind):
    if kind == "data-only":
        return {"README.md": b"# docs only\n",
                "docs/guide.md": b"## guide\n",
                "config/app.yaml": b"key: value\n",
                "config/pins.toml": b'pin = "1"\n',
                "data/seed.json": b'{"a":1}\n'}
    if kind == "unsupported":
        return {"tool/main.py": b"def add(a, b):\n    return a + b\n",
                "README.md": b"# python only\n"}
    # code-grammar repository with a .rs file but NO Cargo.toml at all
    return {"README.md": b"# scripts\n",
            "scripts/util.rs": b"pub fn add(a: i32, b: i32) -> i32 " + BODY,
            "scripts/other.rs": b"pub fn mix(a: i32, b: i32) -> i32 " + BODY,
            "config/pins.toml": b'pin = "1"\n'}


def build(store, kind="code-grammar", selected=None, request=(),
          inventory_anchor="whole-file"):
    """kind: code-grammar | data-only | unsupported"""
    out = {"kind": kind, "assumptions": [
        "grammar bundle tree, source bytes and the enumeration are SYNTHETIC "
        "trusted observations; no compiler, Cargo or provider was executed"]}
    gclosure = F.grammar_bundle_closure(store)
    prov = F.provider_closure(store, "syntax-all")
    ev = F.evaluator_closure(store)
    rc = F.rule_closure(store)
    closures = {c["hex"]: c for c in (gclosure, prov, ev, rc)}

    files = _files(kind)
    cfg = F.config(["clones", "declares", "file"])
    scope = F.scope(["."], excluded=[".git"])
    snap = G.make_snapshot(store, files, scope, cfg, "git", "e" * 40, False)

    ctx = F.syntax_context(store, gclosure)
    G.admit_native_context(store, ctx, closures, snap, {})

    if selected is None:
        selected = {"code-grammar": ["g.rust", "g.toml", "g.markdown"],
                    "data-only": ["g.json", "g.markdown", "g.toml", "g.yaml"],
                    "unsupported": ["g.markdown"]}[kind]
    uni = F.syntax_universe(store, ctx, selected)
    G.bind_universe(store, uni, ctx, None, snap, {})
    rows = G.syntax_selected_rows(uni, ctx)

    out["selectedGrammars"] = sorted(selected)
    out["grammarCustody"] = {
        "context": ctx["sha256text"], "universe": uni["sha256text"],
        "grammarClosureId": gclosure["id"],
        "parserVersion": ctx["descriptor"]["grammarBundle"]["parserVersion"],
        "resolutionAttempted": uni["descriptor"]["resolutionAttempted"],
        "provider": prov["id"],
        "note": "the provider closure is the operational producer; the GRAMMAR is "
                "what interprets a body span, and the universe commits the selection"}

    facts, scopes, coverages = [], [], []

    # inventory facts are ALWAYS available and never grammar-gated
    for p in sorted(files):
        inv = snap["inventory"][p]
        readable = G.syntax_path_capability(rows, p, "file@enumerated")
        if inventory_anchor == "none" or (inventory_anchor == "whole-file"
                                          and not readable):
            anchors = []            # reading B: an unanchored inventory fact
        else:
            anchors = [{"path": p, "blobDigest": inv["sha256"],
                        "startByte": 0, "endByte": inv["bytes"]}]
        out.setdefault("inventoryAnchorChoice", {})[p] = \
            "anchored" if anchors else "unanchored"
        try:
            facts.append(G.make_fact(store, snap, "file", "enumerated", uni["hex"],
                                     uni["hex"], prov["id"],
                                     {"path": p, "contentSha256": inv["sha256"],
                                      "byteLength": inv["bytes"]}, anchors))
        except G.Refusal as exc:
            out.setdefault("inventoryRefusals", {})[p] = exc.cause

    # code-construct + clone facts, only where a SELECTED code grammar reads the path
    body_ids, refusals = {}, {}
    for p in sorted(files):
        if not G.syntax_path_capability(rows, p, "clones@normalized-body-hash"):
            refusals[p] = "capability-missing (no selected code grammar reads it)"
            continue
        src = files[p]
        if b"{" not in src:
            continue
        start = src.index(b"{")
        anchor = [{"path": p, "blobDigest": snap["inventory"][p]["sha256"],
                   "startByte": start, "endByte": len(src)}]
        payload, ident, blv = G.clone_body_fact_parts(store, uni, ctx, p, src[start:],
                                                      "L0-verbatim", SX_SPEC)
        body_ids[p] = {"bodyIdentity": ident, "dialect": blv["dialect"],
                       "languageId": blv["languageId"],
                       "compilerName": blv["compilerName"]}
        facts.append(G.make_fact(store, snap, "clones", "normalized-body-hash",
                                 uni["hex"], uni["hex"], prov["id"], payload, anchor))
        facts.append(G.make_fact(store, snap, "declares", "syntactic", uni["hex"],
                                 uni["hex"], prov["id"],
                                 {"container": "mod:" + p, "declared": "fn:add",
                                  "declarationKind": "function"}, anchor))
    out["bodyIdentities"] = body_ids
    out["cloneRefusals"] = refusals

    # scopes and Coverage: inventory always available; code capability disclosed
    file_scope = G.make_subject_scope(store, snap, "file", "enumerated", uni["hex"],
                                      uni["hex"], prov["id"], sorted(files))
    scopes.append(file_scope)
    coverages.append(G.make_coverage(store, file_scope,
                                     F.na_entry("file", "enumerated", file_scope)))

    disclosures = {}
    for relation, rung, subjects in [
            ("clones", "normalized-body-hash", sorted(body_ids) or sorted(files)),
            ("declares", "syntactic", ["sym:one"])]:
        sc = G.make_subject_scope(store, snap, relation, rung, uni["hex"], uni["hex"],
                                  prov["id"], subjects)
        scopes.append(sc)
        capname = "%s@%s" % (relation, rung)
        available = G._syntax_scope_capability(rows, capname, sc, snap, relation)
        if available:
            e = F.na_entry(relation, rung, sc)
        else:
            e = F.na_entry(relation, rung, sc, "unknown",
                           "language-tier-unsupported", "capability-missing")
        disclosures[capname] = {"available": available,
                                "coverage": e["coverage"],
                                "deficiency": e["deficiency"],
                                "nativeCause": e["nativeCause"]}
        coverages.append(G.make_coverage(store, sc, e))

    # a SEMANTIC rung must be unavailable under a syntax universe
    ref_scope = G.make_subject_scope(store, snap, "references", "resolved-binding",
                                     uni["hex"], uni["hex"], prov["id"], ["sym:one"])
    scopes.append(ref_scope)
    e = F.na_entry("references", "resolved-binding", ref_scope, "unknown",
                   "language-tier-unsupported", "capability-missing")
    # RC-1: a resolved rung must never claim not-applicable
    e["resolutionCompleteness"] = {"state": "not-attempted", "attempted": False,
                                   "examinedExhaustive": False, "stageTerminal": None,
                                   "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    coverages.append(G.make_coverage(store, ref_scope, e))
    disclosures["references@resolved-binding"] = {
        "available": False, "coverage": "unknown",
        "deficiency": "language-tier-unsupported", "nativeCause": "capability-missing"}
    out["capabilityDisclosures"] = disclosures

    declared = {"file": "enumerated", "package": "manifest-declared",
                "vcs-change": "vcs-reported"}
    if any(REG[g["languageId"]]["syntaxClass"] == "code" for g in rows):
        declared.update({"clones": "normalized-body-hash", "declares": "syntactic",
                         "literal": "syntactic", "control-flow": "syntactic"})

    return dict(out, store=store, snapshot=snap, closures=closures, context=ctx,
                universe=uni, retained={}, facts=facts, scopes=scopes,
                coverages=coverages, provider=prov, evaluator=ev, rule=rc,
                files=files, language="syntax", languageMode="syntax-only",
                declaredRelations=declared)
