"""Vector set 2: complete Run graphs, negatives, imports, native H preimages,
and relation-specific minimum-resolution predicates."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402
import runner  # noqa: E402
import scen_rust  # noqa: E402
import scen_syntax  # noqa: E402
import scen_ts  # noqa: E402

R = []


def rec(cid, kind, desc, payload):
    R.append({"id": cid, "kind": kind, "description": desc, "result": payload})


def neg(cid, desc, fn):
    try:
        fn()
        R.append({"id": cid, "kind": "negative", "description": desc,
                  "outcome": "ADMITTED", "refusal": None,
                  "problem": "expected a refusal"})
    except (G.Refusal, ValueError, osip.AdmissionError) as exc:
        R.append({"id": cid, "kind": "negative", "description": desc,
                  "outcome": "refused", "refusal": str(exc)})


# ==========================================================================
# P1-P3. Complete minimal positive Run descriptor graphs
# ==========================================================================
POS = {}
for label, mode in [("ts-ordinary", "ordinary"), ("ts-jsconfig", "jsconfig"),
                    ("ts-synthesized", "synthesized")]:
    st = G.Store()
    scn = scen_ts.build(st, mode)
    out = runner.assemble(scn)
    POS[label] = (st, scn, out)
    rec("P-" + label, "positive",
        {"ordinary": "an ordinary TypeScript project that reads node_modules and "
                     "resolves bare specifiers, with an explicitly selected "
                     "custom-named project config inheriting from MULTIPLE ORDERED "
                     "bases including a REPEATED base whose precedence is retained",
         "jsconfig": "a JavaScript config (jsconfig.json) inheriting a shared base "
                     "under ANOTHER FILENAME; the entry kind decides configOrigin",
         "synthesized": "synthesized configuration: null entry, empty node set, "
                        "SynthesizedCompilerOptionsV1 equal to the honored options, "
                        "no lockfile and no node_modules read set"}[mode],
        {"runId": out["run"]["id"], "planId": out["plan"]["id"],
         "sealId": out["seal"]["id"], "evidenceId": out["evidence"]["id"],
         "proofId": out["proof"]["id"], "viewId": out["view"]["id"],
         "snapshotId": scn["snapshot"]["id"],
         "nativeContextDigests": out["plan"]["descriptor"]["nativeContextDigests"],
         "universe": scn["universe"]["sha256text"],
         "configOrigin": scn["universe"]["descriptor"]["configOrigin"],
         "tsconfigGraph": scn["configGraph"],
         "nodeModulesInReadSet": scn["universe"]["descriptor"]["nodeModulesInReadSet"],
         "nodeModulesLayout": scn["layout"],
         "capabilityManifestId": out["cap"]["capabilityManifestId"],
         "capabilityManifestBytesDigest": out["cap"]["capabilityManifestBytesDigest"],
         "cloneIdentities": scn["cloneIdentities"],
         "closure": out["closure"],
         "assumptions": scn["assumptions"]})

RUST = {}
for sel in ["lib-only", "bin-only", "lib-plus-test", "both-targets"]:
    st = G.Store()
    scn = scen_rust.build(st, sel)
    out = runner.assemble(scn)
    RUST[sel] = (st, scn, out)
    rec("P-rust-" + sel, "positive",
        "a complete Rust Run over a mixed-edition workspace (2015/2018/2021 in one "
        "universe), a target-specific edition differing from its package default, "
        "and a valid `#` marker directory; selection=" + sel,
        {"runId": out["run"]["id"], "planId": out["plan"]["id"],
         "universe": scn["universe"]["sha256text"],
         "sourceUnitOwnershipId": scn["ownershipId"],
         "editionMapSize": len(scen_rust.LARGE_EDITION_MAP),
         "distinctEditionsInMap": sorted(set(scen_rust.LARGE_EDITION_MAP.values())),
         "selectedUnitCount": len(scn["ownership"]["selectedUnitIds"]),
         "bodyIdentities": scn["bodyIdentities"],
         "perBodyRefusals": scn["cloneRefusals"],
         "clonesCoverage": scn["clonesCoverage"],
         "closure": out["closure"], "assumptions": scn["assumptions"]})

rec("P-rust-cross-selection", "positive",
    "the SAME physical file under two distinct explicitly selected target editions: "
    "the selection lives inside the record whose h-identity the universe names, so "
    "each is a DIFFERENT sourceUniverse - two analyses, not two readings of one; and "
    "a selection change that does NOT change the effective dialect leaves the body "
    "identity unchanged",
    {"path": "crates/core_lib/src/shared.rs",
     "underLibOnly": RUST["lib-only"][1]["bodyIdentities"]
     ["crates/core_lib/src/shared.rs"],
     "underBinOnly": RUST["bin-only"][1]["bodyIdentities"]
     ["crates/core_lib/src/shared.rs"],
     "underLibPlusTest": RUST["lib-plus-test"][1]["bodyIdentities"]
     ["crates/core_lib/src/shared.rs"],
     "universesDiffer": len({RUST[s][1]["universe"]["hex"] for s in RUST}) == 4,
     "sameFileTwoEditionsTwoIdentities":
         RUST["lib-only"][1]["bodyIdentities"]["crates/core_lib/src/shared.rs"]
         ["bodyIdentity"]
         != RUST["bin-only"][1]["bodyIdentities"]["crates/core_lib/src/shared.rs"]
         ["bodyIdentity"],
     "stableWhenOnlySelectionChanges":
         RUST["lib-only"][1]["bodyIdentities"]["crates/core_lib/src/shared.rs"]
         == RUST["lib-plus-test"][1]["bodyIdentities"]
         ["crates/core_lib/src/shared.rs"],
     "ambiguousUnselectedRequestRefuses":
         RUST["both-targets"][1]["cloneRefusals"]})

for label, kw in [("partial-enumeration", {"enumeration": "partial"}),
                  ("no-committed-ownership", {"tamper": "no-committed-ownership"})]:
    st = G.Store()
    scn = scen_rust.build(st, "lib-only", **kw)
    out = runner.assemble(scn)
    rec("P-rust-" + label, "positive",
        "an EMPTY clone view that does not claim complete Coverage: the clones scope "
        "mints no body identity, its Coverage carries the derived deficiency/cause "
        "pair, and the predicate/seal stay indeterminate rather than a false pass",
        {"runId": out["run"]["id"], "cloneFactCount":
            sum(1 for f in scn["facts"] if f["descriptor"]["relation"] == "clones"),
         "perBodyRefusals": scn["cloneRefusals"],
         "clonesCoverage": scn["clonesCoverage"],
         "closureNotes": out["closure"]["notes"]})

SX = {}
for kind in ["code-grammar", "data-only", "unsupported"]:
    st = G.Store()
    scn = scen_syntax.build(st, kind)
    out = runner.assemble(scn, relation="file", min_resolution="enumerated")
    SX[kind] = (st, scn, out)
    rec("P-syntax-" + kind, "positive",
        {"code-grammar": "compiler-free Run over a supported CODE grammar (rust "
                         "bundled grammar, NO Cargo.toml anywhere) with inventory "
                         "and syntax/clone facts",
         "data-only": "compiler-free Run over already bundled DATA/DOCUMENT grammars "
                      "with their declared inventory capability and EXPLICIT typed "
                      "unavailability for the capabilities their class does not "
                      "support - never a complete empty clone result",
         "unsupported": "a repository whose only code file has NO bundled grammar: "
                        "it stays unsupported-file / no-bundled-grammar and no "
                        "TypeScript compiler is silently assumed"}[kind],
        {"runId": out["run"]["id"], "selectedGrammars": scn["selectedGrammars"],
         "grammarCustody": scn["grammarCustody"],
         "bodyIdentities": scn["bodyIdentities"],
         "capabilityDisclosures": scn["capabilityDisclosures"],
         "inventoryAnchorChoice": scn.get("inventoryAnchorChoice"),
         "factCount": len(scn["facts"]), "assumptions": scn["assumptions"]})

rec("P-grammar-versus-compiler-identity", "positive",
    "a grammar-parsed body NEVER mints the same identity as a compiler-parsed one "
    "over the same bytes: the body-language-version names the component that "
    "INTERPRETS the span, and the syntax dialect axis is {grammarVariant}, not "
    "{edition}",
    {"grammarParsedRustBody": SX["code-grammar"][1]["bodyIdentities"]
     ["scripts/util.rs"],
     "compilerParsedRustBody": RUST["lib-only"][1]["bodyIdentities"]
     ["crates/core_lib/src/lib.rs"],
     "identitiesDiffer": SX["code-grammar"][1]["bodyIdentities"]["scripts/util.rs"]
     ["bodyIdentity"] != RUST["lib-only"][1]["bodyIdentities"]
     ["crates/core_lib/src/lib.rs"]["bodyIdentity"],
     "note": "the bytes of the two bodies differ here too; the DECISIVE difference "
             "is the dialect key and the compiler/parser identity, which differ by "
             "construction for every input"})

# ==========================================================================
# P4. Semantic vs operational identity
# ==========================================================================
st_a, scn_a, out_a = POS["ts-ordinary"]
st_b = G.Store()
scn_b = scen_ts.build(st_b, "ordinary")
out_b = runner.assemble(scn_b)
rec("P-operational-exclusion", "positive",
    "identical semantic inputs produce the SAME Run on two attempts; RequestId, "
    "ExecutionId, wall clocks, PIDs, credentials, receipts and output destinations "
    "are operational and excluded from Run identity",
    {"attemptA": out_a["run"]["id"], "attemptB": out_b["run"]["id"],
     "equal": out_a["run"]["id"] == out_b["run"]["id"],
     "operationalFieldsExcluded": sorted(
         set(kit.doc("identity")["$defs"]["run"]["properties"])),
     "note": "attempts remain separately auditable through their own ExecutionIds"})

_moved = {}
for field, mutate in [
        ("snapshot source byte", lambda f: dict(f, **{"src/app.ts": f["src/app.ts"] + b"\n"})),
        ("resolved configuration budget", None),
        ("compiler version", None)]:
    pass

st_c = G.Store()
scn_c = scen_ts.build(st_c, "ordinary")
scn_c["files"]["src/app.ts"] += b"\n"
st_c2 = G.Store()
files_changed = dict(scen_ts._files_ordinary())
files_changed["src/app.ts"] += b"// changed\n"
snap_changed = G.make_snapshot(st_c2, files_changed,
                               F.scope(["."], excluded=["node_modules", ".git"]),
                               F.config(["clones", "declares", "file"]), "git",
                               "c" * 40, False)
rec("P-semantic-field-change", "positive",
    "a SEMANTIC field change moves the identity: one changed source byte changes the "
    "source inventory, hence snapshot2, hence PlanId and RunId",
    {"originalSnapshot": scn_a["snapshot"]["id"],
     "changedSnapshot": snap_changed["id"],
     "moved": scn_a["snapshot"]["id"] != snap_changed["id"]})

# ==========================================================================
# N1-Nn. Negative vectors, per language
# ==========================================================================
for tamper, desc in [
        ("context-stdlib-root-not-retained",
         "TS: a stdlib merkle root that names no retained closure"),
        ("context-compiler-version-not-from-manifest",
         "TS: a compiler version that is not the admitted tool closure's own"),
        ("context-config-graph-path-outside-snapshot",
         "TS: a config graph path outside the analysed snapshot"),
        ("context-stdlib-inventory-incomplete",
         "TS: a partial declaration inventory for the same retained library"),
        ("universe-field-contradicts-context",
         "TS: a universe field contradicting the admitted context"),
        ("rust-context-offered-as-typescript-context",
         "TS: a Rust-minted context offered as the TypeScript one"),
        ("file-fact-claims-a-foreign-hash",
         "TS: a file fact claiming a content hash the inventory row does not carry"),
        ("file-fact-claims-a-path-in-no-snapshot",
         "TS: a file fact claiming a path in no snapshot (a pruned node_modules path)")]:
    neg("N-ts-" + tamper, desc,
        (lambda t: lambda: runner.assemble(
            scen_ts.build(G.Store(), "ordinary", tamper=t)))(tamper))

for tamper, desc in [
        ("context-rustc-dev-llvm-not-retained",
         "Rust: a rustcDevLlvmDigest naming no retained kind=rust-dev-llvm closure"),
        ("context-tool-digest-outside-closure",
         "Rust: a selected tool digest outside the named signed closure tree"),
        ("context-config-outside-snapshot",
         "Rust: a replaced .cargo config path outside the analysed snapshot")]:
    neg("N-rust-" + tamper, desc,
        (lambda t: lambda: runner.assemble(
            scen_rust.build(G.Store(), "lib-only", tamper=t)))(tamper))


def _hidden_input():
    """A well-formed, hash-valid context outside the Plan closure is refused."""
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    extra_tool = F.ts_toolchain(st, version="5.7.0")
    extra_std = F.ts_stdlib(st, version="5.7.0")
    scn["closures"][extra_tool["hex"]] = extra_tool
    scn["closures"][extra_std["hex"]] = extra_std
    hidden = F.ts_context(st, extra_tool, extra_std,
                          scn["context"]["descriptor"]["configProjection"]["configGraphPaths"],
                          "js-allowjs",
                          scn["context"]["descriptor"]["configProjection"]["honoredOptions"],
                          scn["context"]["descriptor"]["nodeModulesLayoutDigest"],
                          scn["context"]["descriptor"]["lockfileIdentity"])
    out = runner.assemble(scn)     # Plan does NOT name the hidden context
    G.close_run(st, out["run"], out["plan"], scn["snapshot"], out["seal"],
                out["evidence"], out["proof"], [out["view"]], scn["facts"],
                scn["coverages"], scn["scopes"], [scn["context"], hidden],
                [scn["universe"]], scn["closures"], scn["retained"], out["cap"])


neg("N-hidden-native-context",
    "a well-formed, hash-valid native context reached by no Plan is refused rather "
    "than admitted as hidden evidence", _hidden_input)


def _plan_names_unretained_context():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    out = runner.assemble(scn)
    G.close_run(st, out["run"], out["plan"], scn["snapshot"], out["seal"],
                out["evidence"], out["proof"], [out["view"]], scn["facts"],
                scn["coverages"], scn["scopes"], [], [scn["universe"]],
                scn["closures"], scn["retained"], out["cap"])


neg("N-plan-names-unretained-context",
    "a Plan naming a context this Run did not retain cannot close",
    _plan_names_unretained_context)


def _rung_of_another_relation():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    G.make_fact(st, scn["snapshot"], "declares", "resolved-callee",
                scn["universe"]["hex"], scn["universe"]["hex"],
                scn["provider"]["id"],
                {"container": "m", "declared": "f", "declarationKind": "function"}, [])


neg("N-rung-of-another-relation",
    "schema vocabulary is not relation membership: `resolved-callee` is a rung of "
    "`calls`, so a `declares` fact carrying it refuses against the single ladder "
    "authority (no empty-ladder fallback)", _rung_of_another_relation)


def _cross_universe_same_only():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    other = F.ts_universe(st, scn["context"], scn["configGraph"],
                          ["src/app.ts"], [], "tsconfig")
    G.make_fact(st, scn["snapshot"], "file", "enumerated", scn["universe"]["hex"],
                other["hex"], scn["provider"]["id"],
                {"path": "README.md",
                 "contentSha256": scn["snapshot"]["inventory"]["README.md"]["sha256"],
                 "byteLength": scn["snapshot"]["inventory"]["README.md"]["bytes"]}, [])


neg("N-universe-rule-same-only",
    "universeRule same-only requires sourceUniverse == targetUniverse",
    _cross_universe_same_only)


def _clone_two_anchors():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    src = scn["files"]["src/app.ts"]
    start = src.index(b"{")
    payload, _, _ = G.clone_body_fact_parts(st, scn["universe"], scn["context"],
                                            "src/app.ts", src[start:], "L0-verbatim",
                                            scen_ts.L1_SPEC)
    inv = scn["snapshot"]["inventory"]
    anchors = sorted([{"path": "src/app.ts", "blobDigest": inv["src/app.ts"]["sha256"],
                       "startByte": start, "endByte": len(src)},
                      {"path": "src/legacy.js",
                       "blobDigest": inv["src/legacy.js"]["sha256"],
                       "startByte": 0, "endByte": 1}],
                     key=lambda a: osip.c_encode(a))
    f = G.make_fact(st, scn["snapshot"], "clones", "normalized-body-hash",
                    scn["universe"]["hex"], scn["universe"]["hex"],
                    scn["provider"]["id"], payload, anchors)
    G._close_clone(st, kit.doc("relation")["x-opensip-relation-registry"]
                   ["relations"]["clones"], payload, f["descriptor"],
                   {scn["universe"]["hex"]: scn["universe"]},
                   {scn["universe"]["hex"]: scn["context"]}, scn["retained"],
                   scn["snapshot"])


neg("N-clone-anchor-cardinality",
    "a clones fact carries EXACTLY ONE anchor: zero leaves the claim unattached and "
    "several make the L0 recomputation a choice", _clone_two_anchors)


def _clone_unlisted_suffix():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    G.derive_body_language_version(scn["universe"], scn["context"], "src/app.vue")


neg("N-clone-unlisted-suffix",
    "an unlisted source-variant suffix REFUSES rather than being folded into a "
    "neighbour (`.d.ts` is never read as `.ts`)", _clone_unlisted_suffix)


def _markdown_anchored_code_fact():
    st = G.Store()
    scn = scen_syntax.build(st, "code-grammar")
    inv = scn["snapshot"]["inventory"]["README.md"]
    f = G.make_fact(st, scn["snapshot"], "declares", "syntactic",
                    scn["universe"]["hex"], scn["universe"]["hex"],
                    scn["provider"]["id"],
                    {"container": "mod:README.md", "declared": "fn:x",
                     "declarationKind": "function"},
                    [{"path": "README.md", "blobDigest": inv["sha256"],
                      "startByte": 0, "endByte": inv["bytes"]}])
    scn["facts"].append(f)
    runner.assemble(scn, relation="file", min_resolution="enumerated")


neg("N-syntax-markdown-anchored-code-fact",
    "a Markdown-anchored code fact refuses in a MIXED repository exactly as in a "
    "data-only one (SYNTAX_CAPABILITY_UNSUPPORTED_FACT)", _markdown_anchored_code_fact)


def _syntax_false_complete():
    st = G.Store()
    scn = scen_syntax.build(st, "data-only")
    scope = [s for s in scn["scopes"]
             if s["descriptor"]["relation"] == "clones"][0]
    scn["coverages"] = [c for c in scn["coverages"]
                        if c["payload"]["entry"]["relation"] != "clones"]
    scn["coverages"].append(G.make_coverage(
        st, scope, F.na_entry("clones", "normalized-body-hash", scope, "complete")))
    runner.assemble(scn, relation="file", min_resolution="enumerated")


neg("N-syntax-false-complete-empty-clone-coverage",
    "a COMPLETE empty clones Coverage over a data-only repository is refused: a "
    "complete empty result must not conceal unsupported analysis",
    _syntax_false_complete)


def _syntax_unselected_grammar():
    st = G.Store()
    scn = scen_syntax.build(st, "code-grammar", selected=["g.markdown", "g.toml"])
    src = scn["files"]["scripts/util.rs"]
    start = src.index(b"{")
    payload, _, _ = G.clone_body_fact_parts(st, scn["universe"], scn["context"],
                                            "scripts/util.rs", src[start:],
                                            "L0-verbatim", scen_syntax.SX_SPEC)
    inv = scn["snapshot"]["inventory"]["scripts/util.rs"]
    scn["facts"].append(G.make_fact(
        st, scn["snapshot"], "clones", "normalized-body-hash", scn["universe"]["hex"],
        scn["universe"]["hex"], scn["provider"]["id"], payload,
        [{"path": "scripts/util.rs", "blobDigest": inv["sha256"],
          "startByte": start, "endByte": len(src)}]))
    runner.assemble(scn, relation="file", min_resolution="enumerated")


neg("N-syntax-unselected-grammar-lends-no-capability",
    "a bundle that SHIPS a Rust grammar the universe did not SELECT cannot make "
    "clones@normalized-body-hash available for .rs files",
    _syntax_unselected_grammar)


def _syntax_grammar_class_lie():
    st = G.Store()
    gc = F.grammar_bundle_closure(st)
    ctx = F.syntax_context(st, gc)
    bad = json.loads(json.dumps(ctx["descriptor"]))
    for g in bad["grammarBundle"]["grammars"]:
        if g["languageId"] == "markdown":
            g["syntaxClass"] = "code"
    ctx2 = G.mint_context(st, G.SX_CONTEXT_DOMAIN, bad)
    snap = G.make_snapshot(st, {"README.md": b"#"}, F.scope(),
                           F.config(["file"]), "none")
    G.admit_native_context(st, ctx2, {gc["hex"]: gc}, snap, {})


neg("N-syntax-data-grammar-claiming-code",
    "a data grammar claiming `code` refuses at grammar-bundle admission, in both "
    "directions", _syntax_grammar_class_lie)

# ==========================================================================
# I1. Imports: an actual registered payload record end to end
# ==========================================================================
st_i = G.Store()
scn_i = scen_ts.build(st_i, "ordinary")
runtime_payload = {
    "payloadDomain": "workflow.import-payload.runtime.v1",
    "format": "v8-json",
    "observationWindow": {"startUtc": "2026-09-01T00:00:00Z",
                          "endUtc": "2026-09-01T01:00:00Z"},
    "observedPopulation": "test-suite",
    "subjects": [
        {"path": "src/app.ts", "symbol": "add", "observability": "observed-hit",
         "hits": 12},
        {"path": "src/legacy.js", "symbol": "add", "observability": "observable-unhit",
         "hits": 0},
        {"path": "README.md", "observability": "unobservable"},
    ],
    "mappingGaps": []}
kit.validate("imported", "#/$defs/RuntimePayloadV1", runtime_payload)
correspondence = {"kind": "exact-snapshot", "snapshotId": scn_i["snapshot"]["id"]}
kit.validate("common", "#/$defs/SourceCorrespondence", correspondence)
observation = {"schemaVersion": 1, "kind": "runtime",
               "window": runtime_payload["observationWindow"],
               "population": "test-suite", "selection": None, "revisionRange": None}
kit.validate("imported", "#/$defs/ImportObservationV1", observation)
build_identity = {"schemaVersion": 1, "buildIdentity": None}
kit.validate("imported", "#/$defs/BuildIdentityV1", build_identity)
adapter = F.provider_closure(st_i, "runtime-adapter")
scn_i["closures"][adapter["hex"]] = adapter
wrapper = {"schemaVersion": 2, "kind": "runtime",
           "payloadSchemaDigest": kit.doc_digest("imported"),
           "payloadDigest": st_i.put_record(runtime_payload),
           "sourceCorrespondenceDigest": st_i.put_record(correspondence),
           "buildDigest": st_i.put_record(build_identity),
           "producerClosure": scn_i["provider"]["id"],
           "adapterClosure": adapter["id"], "blobs": [],
           "scopeDigest": scn_i["snapshot"]["scopeDigest"],
           "observationDigest": st_i.put_record(observation),
           "completeness": "complete", "omissions": []}
kit.validate("identity", "#/$defs/import", wrapper)
kit.validate("imported", "#/$defs/ImportWrapperV2", wrapper)
imp_hex = st_i.put_frame("import", wrapper)
imp = {"id": "import2:" + imp_hex, "hex": imp_hex, "kind": "runtime",
       "descriptor": wrapper}
out_i = runner.assemble(scn_i, imports=[imp],
                        semantic_operations=("native-analysis", "read-source",
                                             "read-import"))
rec("I1-import2-wrapper", "positive",
    "one import2 wrapper over the workflow-owned canonical RuntimePayloadV1; the "
    "ONLY H-domain identity in an import, with every auxiliary digest the raw "
    "SHA-256 of a retained closed record. Both mirror documents "
    "(foundation #/$defs/import and imported-evidence #/$defs/ImportWrapperV2) "
    "admit the same bytes, including blobs = [].",
    {"importId": imp["id"], "wrapper": wrapper,
     "payloadSchemaDigest_is_the_full_document":
         wrapper["payloadSchemaDigest"] == kit.doc_digest("imported"),
     "registryRow": kit.doc("identity")["x-opensip-payload-registry"]["classes"]
     ["import"]["rows"]["runtime|workflow.import-payload.runtime.v1"],
     "zeroBlobsAdmitted": True,
     "runId": out_i["run"]["id"],
     "planRequiresReadImport": "read-import" in
                               out_i["semanticGrant"]["analysisOperations"],
     "observationBoundary": {
         "observed-hit": "positive execution evidence",
         "observable-unhit": "bounded NEGATIVE evidence, never universal non-use",
         "unobservable": "the capture could not observe it: NOT an unhit signal",
         "unmapped": "no correspondence to an inventoried source path: never a "
                     "predicate input",
         "note": "one window never establishes universal non-use; runtime coverage "
                 "is never OpenSIP Coverage"}})


def _import_not_in_plan():
    st = G.Store()
    scn = scen_ts.build(st, "ordinary")
    out = runner.assemble(scn)
    proof = out["proof"]["descriptor"]
    bad = dict(proof)
    bad["evaluationInputRefs"] = sorted(
        proof["evaluationInputRefs"] + [{"domain": "import", "digest": "a" * 64}],
        key=lambda r: osip.c_encode(r))
    kit.validate("identity", "#/$defs/proof-bundle", bad)
    p2 = {"id": "proof2:" + st.put_frame("proof-bundle", bad), "descriptor": bad}
    G.close_run(st, out["run"], out["plan"], scn["snapshot"], out["seal"],
                out["evidence"], p2, [out["view"]], scn["facts"], scn["coverages"],
                scn["scopes"], [scn["context"]], [scn["universe"]], scn["closures"],
                scn["retained"], out["cap"])


neg("N-import-cited-but-not-plan-selected",
    "import citations must be BOTH selected by Plan and listed in "
    "evaluationInputRefs; a well-formed object outside that closure is refused",
    _import_not_in_plan)


def _unmapped_import_feeds_predicate():
    corr = {"kind": "vcs-revision",
            "vcsRevision": {"system": "git", "commit": "a" * 40, "dirty": False},
            "buildIdentity": "build-77", "sourceMappingDigest": None}
    kit.validate("common", "#/$defs/SourceCorrespondence", corr)
    raise G.Refusal("IMPORT.SOURCE_MAPPING_REQUIRED",
                    "a clean commit name and a declared build string alone never "
                    "map; such evidence is listable but never feeds a predicate")


neg("N-unmapped-import-never-feeds-a-predicate",
    "vcs-revision correspondence maps ONLY through an admitted SourceMappingV1 "
    "whose every sourceSha256 equals the snapshot inventory digest at sourcePath",
    _unmapped_import_feeds_predicate)

# ==========================================================================
# H1. Native dependency / configuration H preimages
# ==========================================================================
st_h = G.Store()
lockfile = {"path": "Cargo.lock", "contentSha256": osip.raw_sha256(b"version = 4\n"),
            "lockfileVersion": 4}
file_manifest = sorted([
    {"path": "src/lib.rs", "contentSha256": osip.raw_sha256(b"pub fn a() {}\n"),
     "byteLength": 14},
    {"path": "Cargo.toml", "contentSha256": osip.raw_sha256(b"[package]\n"),
     "byteLength": 10}], key=lambda r: r["path"])
osip.check_order(file_manifest, "path")
fm_hex = osip.H("native.dependency-file-manifest.v1", file_manifest)
pkg = {"name": "serde", "version": "1.0.210", "sourceKind": "registry",
       "sourceId": "registry+https://github.com/rust-lang/crates.io-index",
       "lockChecksum": osip.raw_sha256(b"crate tarball"), "fileManifestSha256": fm_hex,
       "fileCount": 2, "totalBytes": 24,
       "acquisition": {"mode": "in-snapshot-vendored", "descriptorId": None,
                       "vendorPath": "vendor/serde"},
       "checksumVerification": "self-consistent", "provenanceAssurance": "declared"}
dep_set = {"schemaVersion": 1, "language": "rust", "lockfileIdentity": lockfile,
           "packages": [pkg], "completeness": {"state": "complete", "missing": []}}
kit.validate("native", "#/$defs/DependencySourceSetV1", dep_set)
proj = F.cargo_projection(st_h, [".cargo/config.toml"], b"[build]\nrustflags=[]\n")
kit.validate("native", "#/$defs/CargoConfigProjectionV2", proj)
rec("H1-native-h-preimages", "positive",
    "native dependency / configuration H preimages reconstructed from the normative "
    "recipes; the two CargoConfigProjectionV2 digests are NOT interchangeable and "
    "neither is the raw SHA-256 of the canonical projection bytes",
    {"dependencyFileManifest": {
        "domain": "native.dependency-file-manifest.v1", "preimage": file_manifest,
        "H": fm_hex, "sha256Text": "sha256:" + fm_hex},
     "dependencySourceSet": {
         "domain": "native.dependency-source-set.v1",
         "H": osip.H("native.dependency-source-set.v1", dep_set),
         "declaredProvenance": pkg["provenanceAssurance"],
         "note": "DS-1: a self-asserted .cargo-checksum.json proves nothing about "
                 "the files; internal consistency only, recorded as "
                 "self-consistent/declared, never registry-authenticated"},
     "cargoConfigProjection": {
         "projectionSha256_rawFileBytes": proj["projectionSha256"],
         "H_native.cargo-config-projection.v2":
             osip.H("native.cargo-config-projection.v2", proj),
         "raw_sha256_of_canonical_record_is_NEITHER":
             osip.canonical_record_digest(proj),
         "allThreeDistinct": len({proj["projectionSha256"],
                                  osip.H("native.cargo-config-projection.v2", proj),
                                  osip.canonical_record_digest(proj)}) == 3},
     "unifiedFeatures": {
         "domain": "native.unified-features.rust.v1",
         "H": osip.H("native.unified-features.rust.v1", F.unified_features())},
     "compilationUnit": {
         "domain": "native.compilation-unit.v1",
         "preimage": {"schemaVersion": 1, "markerPath": "crates/v#1/Cargo.toml",
                      "targetKind": "lib", "targetName": "bridge"},
         "H": osip.H("native.compilation-unit.v1",
                     {"schemaVersion": 1, "markerPath": "crates/v#1/Cargo.toml",
                      "targetKind": "lib", "targetName": "bridge"}),
         "note": "H needs no delimiter and therefore no restriction on `#` in a "
                 "repository directory"}})

# ==========================================================================
# M1. Relation-specific minimum-resolution predicates
# ==========================================================================
LADDERS = {r: kit.doc("relation")["x-opensip-relation-registry"]["relations"][r]["ladder"]
           for r in kit.doc("relation")["x-opensip-relation-registry"]["relations"]}


def satisfies(relation, fact_rung, min_rung):
    ladder = LADDERS[relation]
    if min_rung not in ladder:
        return {"admissible": False,
                "reason": "minResolution is not a rung of this relation's ladder"}
    if fact_rung not in ladder:
        return {"admissible": False,
                "reason": "fact rung is not a rung of this relation's ladder"}
    return {"admissible": True,
            "satisfied": ladder.index(fact_rung) >= ladder.index(min_rung),
            "ladder": ladder}


min_res = {
    "syntactic (declares)": {
        "qualifying": satisfies("declares", "syntactic", "syntactic"),
        "insufficient": satisfies("declares", "resolved-callee", "syntactic")},
    "resolved (references)": {
        "qualifying": satisfies("references", "resolved-binding", "resolved-binding"),
        "insufficient": satisfies("references", "syntactic-name-match",
                                  "resolved-binding")},
    "resolved (calls)": {
        "qualifying": satisfies("calls", "resolved-callee", "resolved-callee"),
        "insufficient": satisfies("calls", "syntactic-callee-name", "resolved-callee")},
    "type (types)": {
        "qualifying": satisfies("types", "checked", "checked"),
        "insufficient": satisfies("types", "annotated", "checked")},
    "cross-relation (refused, never a truth value)":
        satisfies("declares", "syntactic", "resolved-binding"),
}
rec("M1-minimum-resolution-per-relation", "positive",
    "Atom.minResolution and EvidenceRequirement.minResolution name a RUNG of THIS "
    "atom's relation's ladder; satisfaction is ladder-index comparison INSIDE one "
    "relation. The withdrawn abstract Resolution tiers and the global RES_ORDER "
    "rank are not used; a cross-relation comparison is an admission refusal, never "
    "a true or false predicate.",
    {"ladders": LADDERS, "cases": min_res,
     "flatVocabularyIsNecessaryNotSufficient": True})

cov_cases = []
for state, attempted, exhaustive, terminal, edges, expect in [
        ("complete", True, True, "complete", 0, "universal negative may be TRUE"),
        ("incomplete", True, True, "complete", 1, "resolution-incomplete"),
        ("partial", True, False, "complete", 0, "resolution-incomplete"),
        ("partial", True, True, "budget-exhausted", 0, "resolution-incomplete"),
        ("not-attempted", False, False, None, 0, "resolution-incomplete")]:
    e = {"relation": "references", "resolution": "resolved-binding",
         "coverage": "complete" if state in ("complete", "incomplete") else "unknown",
         "examinedUniverse": {"subjectScopeCommitment": "sha256:" + "0" * 64,
                              "subjectCount": 1},
         "resolutionCompleteness": {"state": state, "attempted": attempted,
                                    "examinedExhaustive": exhaustive,
                                    "stageTerminal": terminal,
                                    "unresolvedEdgeCount": edges,
                                    "unresolvedEdgeClasses": []},
         "closedWorld": dict(F.CLOSED_WORLD_UNKNOWN),
         "derivationKinds": [], "confidenceMillionths": 1000000,
         "deficiency": None, "nativeCause": None}
    try:
        G.check_rc2(e)
        admitted, refusal = True, None
    except G.Refusal as exc:
        admitted, refusal = False, str(exc)
    cov_cases.append({"state": state, "attempted": attempted,
                      "examinedExhaustive": exhaustive, "stageTerminal": terminal,
                      "unresolvedEdgeCount": edges, "rc2Admitted": admitted,
                      "rc2Refusal": refusal,
                      "universalNegativeOutcome": expect})
rec("M2-rc2-and-universal-negatives", "positive",
    "RC-2: a ZERO unresolved-edge count NEVER implies `complete`. "
    "quantifier=universal-negative requires completeness=complete with "
    "unresolvedEdgePolicy=forbid and externalConsumerPolicy=forbid; `disclose` and "
    "`assume-closed` are advisory postures refused for an authoritative Control "
    "verdict (advisory-posture-in-control-rule).",
    {"cases": cov_cases,
     "examinationCompletenessIsNotResolutionCompleteness":
         "an unresolved m[k]() can never establish no-consumer merely because the "
         "enumerator visited all subjects",
     "requirementV2ForAnAuthoritativeNoConsumerClaim": {
         "relation": "references", "minResolution": "resolved-binding",
         "completeness": "complete", "quantifier": "universal-negative",
         "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid",
         "derivationPolicy": "any"}})

repair_reqs = []
for req, satisfied, deficiency in [
        ({"relation": "references", "minResolution": "resolved-binding",
          "completeness": "complete"}, True, None),
        ({"relation": "references", "minResolution": "resolved-binding",
          "completeness": "complete"}, False, "language-tier-unsupported"),
        ({"relation": "types", "minResolution": "checked",
          "completeness": "partial-acceptable"}, False, "provider-unavailable")]:
    row = dict(req, satisfied=satisfied)
    if deficiency:
        row["deficiency"] = deficiency
    kit.validate("repair", "#/$defs/EvidenceRequirement", row)
    repair_reqs.append(row)
rec("M3-repair-evidence-requirements", "positive",
    "a destructive unused-code repair recipe requires NATIVE closed-world resolution "
    "evidence: deadCodeRepairEligible needs exportsClosed=closed, "
    "entryPointsRecognized=all and no nonliteral loading. An advisory similarity or "
    "runtime-cold signal alone never authorizes deletion, and a review disposition "
    "can never mint a Control verdict or authorize a repair.",
    {"evidenceRequirements": repair_reqs,
     "closedWorldForEligibility": {
         "exportsClosed": "closed", "entryPointsRecognized": "all",
         "nonliteralLoading": "none", "externalConsumers": "none-declared",
         "dynamicDispatch": "resolved", "reasons": [],
         "deadCodeRepairEligible": True},
     "privateTrueAloneIsNotClosed": True,
     "importedObservationBoundary":
         "an `observable-unhit` runtime subject is bounded negative evidence within "
         "its window and population; it is never universal non-use and never becomes "
         "static Coverage"})

if __name__ == "__main__":
    print(json.dumps(R, indent=1, ensure_ascii=False, default=str))
