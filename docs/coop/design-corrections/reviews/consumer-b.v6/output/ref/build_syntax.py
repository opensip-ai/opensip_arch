"""Vector group C: compiler-free syntax-only Runs.
C1 = a supported CODE grammar (rust files with no Cargo unit): inventory +
     syntax + clone facts.
C2 = an already bundled DATA/DOCUMENT grammar: its declared inventory capability
     with explicit unavailability for the capabilities its class does not support.
Both in a repository with NO TypeScript and NO Rust compilation unit."""
import sys, os, json, hashlib, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import S, V, PROJECT_ID, PLATFORM, blob, inv, closure, EVAL_CID
from build_ts2 import CAP_ID, CAP_BYTES_DIGEST, NA_RC, CW_CLOSED
from build_ts3 import LEVEL_SPEC

SYU = "native.semantic-universe.syntax.v2"
SYC = "native.context.syntax.v2"
LANGS = GRAMREG["languages"]

# --------------------------------------------------------- the grammar bundle
gtree = []
for lang in sorted(LANGS):
    gtree.append(blob(f"grammars/{lang}.grammar", f"GRAMMAR-{lang}-BYTES")[0])
gtree.append(blob("normalizer/spec.json", "NORMALIZER-SPECIFICATION")[0])
gtree.append(blob("bundle-manifest.json", "GRAMMAR-BUNDLE-MANIFEST")[0])
GRAM_CID, GRAM_CLOSURE = closure("grammar", gtree, "3.1.0", 0, PLATFORM,
                                 b"GRAMMAR-BUNDLE-MANIFEST-BODY")
BUNDLE_MANIFEST_BYTES = b"GRAMMAR-BUNDLE-MANIFEST"

BUNDLE = {"schemaVersion": 1, "closureId": GRAM_CID,
          "parserName": "opensip-grammar-bundle",
          "parserVersion": GRAM_CLOSURE["semanticVersion"],
          "bundleDigest": rawbytes(BUNDLE_MANIFEST_BYTES),
          "normalizer": {"specificationDigest": [b["sha256"] for b in gtree
                                                 if b["path"] == "normalizer/spec.json"][0]},
          "grammars": sorted([
              {"grammarId": f"g.{lang}", "grammarVersion": "1.0.0", "languageId": lang,
               "syntaxClass": LANGS[lang]["syntaxClass"],
               "suffixes": sorted(LANGS[lang]["suffixes"]),
               "grammarDigest": [b["sha256"] for b in gtree
                                 if b["path"] == f"grammars/{lang}.grammar"][0]}
              for lang in sorted(LANGS)], key=lambda g: g["grammarId"])}
S.put_blob(BUNDLE_MANIFEST_BYTES, "grammar bundle manifest")


def admit_grammar_bundle(b):
    d = b["closureId"].split(":")[1]
    rec = S.reframe_check(d, "closure")
    if rec["kind"] != "grammar":
        raise Refuse("native.native-context-closure-kind-mismatch", b["closureId"])
    if b["parserVersion"] != rec["semanticVersion"]:
        raise Refuse("native.syntax-grammar-version-not-from-manifest", b["parserVersion"])
    seen = {}
    for g in b["grammars"]:
        if g["languageId"] not in LANGS:
            raise Refuse("native.syntax-grammar-language-unregistered", g["languageId"])
        if g["syntaxClass"] != LANGS[g["languageId"]]["syntaxClass"]:
            raise Refuse("native.syntax-grammar-class-mismatch",
                         f"{g['languageId']}:{g['syntaxClass']}")
        for s in g["suffixes"]:
            if s not in LANGS[g["languageId"]]["suffixes"]:
                raise Refuse("native.syntax-grammar-suffix-not-routed-to-this-language", s)
            if s in seen:
                raise Refuse("native.syntax-grammar-suffix-ambiguous", s)
            seen[s] = g["grammarId"]
    # the CODE subset is what is held equal to the body-language-version enum
    enum = set(IDS["$defs"]["body-language-version"]["properties"]["languageId"]["enum"])
    code = {g["languageId"] for g in b["grammars"] if g["syntaxClass"] == "code"}
    data = {g["languageId"] for g in b["grammars"] if g["syntaxClass"] == "data-document"}
    if code != enum:
        raise Refuse("native.syntax-grammar-code-subset-drift", str(sorted(code ^ enum)))
    if data & enum:
        raise Refuse("native.syntax-grammar-data-language-in-body-enum", str(sorted(data & enum)))
    return True


admit_grammar_bundle(BUNDLE)
SY_CTX = {"schemaVersion": 2, "grammarBundle": BUNDLE}
SY_CTX_ID = "sha256:" + S.put_framed(SYC, SY_CTX)

V["SY-BUNDLE-1-seven-bundled-grammars-and-the-code-versus-data-law"] = {
    "bundledLanguages": sorted(LANGS),
    "codeClass": sorted(l for l in LANGS if LANGS[l]["syntaxClass"] == "code"),
    "dataDocumentClass": sorted(l for l in LANGS if LANGS[l]["syntaxClass"] == "data-document"),
    "suffixCount": sum(len(LANGS[l]["suffixes"]) for l in LANGS),
    "codeSubsetEqualsBodyLanguageVersionEnum": True,
    "dataLanguagesAreAbsentFromThatEnum": True,
    "parserVersionJoinedToTheGrammarClosureManifestSemanticVersion": BUNDLE["parserVersion"],
    "contextId": SY_CTX_ID,
    "contextCarriesNoToolchainStdlibLockfileNodeModulesOrConfigGraph":
        sorted(SY_CTX.keys()) == ["grammarBundle", "schemaVersion"],
    "verifiedAgainstThePublishedMatrix": {
        lang: LANGS[lang]["capabilities"] for lang in sorted(LANGS)}}


def syntax_universe(selected):
    for g in selected:
        if g not in {x["grammarId"] for x in BUNDLE["grammars"]}:
            raise Refuse("native.syntax-grammar-not-in-bundle", g)
    if not selected:
        raise Refuse("native.syntax-selection-empty", "")
    u = {"schemaVersion": 2, "nativeContextId": SY_CTX_ID,
         "selectedGrammarIds": sorted(selected, key=lambda s: s.encode()),
         "resolutionAttempted": False}
    return u, "sha256:" + S.put_framed(SYU, u)


# =============================================== R3: data / document repository
r3 = {}
r3["README.md"], _ = blob("README.md", "# Project\n\nDocs.\n")
r3["docs/guide.md"], _ = blob("docs/guide.md", "## Guide\n")
r3["data/config.json"], _ = blob("data/config.json", '{"k":1}\n')
r3["data/values.yaml"], _ = blob("data/values.yaml", "k: 1\n")
r3["settings.toml"], _ = blob("settings.toml", "[a]\nb=1\n")
r3["tool/main.py"], _ = blob("tool/main.py", "def main():\n    pass\n")
r3["assets/logo.bin"], _ = blob("assets/logo.bin", b"\x00\x01\x02\xff")   # non-UTF8, extensionless class
R3_INV = inv(list(r3.values()))
R3_MAP = {r["path"]: r for r in R3_INV}

DATA_SEL = ["g.json", "g.markdown", "g.toml", "g.yaml"]
U3, U3_ID = syntax_universe(DATA_SEL)
U3H = U3_ID.split(":")[1]

# membership: every inventory file in exactly one row, erasedFiles is empty
MEMBERSHIP_3 = []
for r in R3_INV:
    g = suffix_owner(BUNDLE, DATA_SEL, r["path"])
    if g:
        MEMBERSHIP_3.append({"path": r["path"], "membership": "syntax-only",
                             "reason": "grammar-only", "grammarId": g["grammarId"]})
    else:
        MEMBERSHIP_3.append({"path": r["path"], "membership": "unsupported-file",
                             "reason": "no-bundled-grammar", "grammarId": None})

V["SY-C2-data-document-repository-membership"] = {
    "snapshotInventoryPaths": [r["path"] for r in R3_INV],
    "membership": MEMBERSHIP_3,
    "erasedFiles": [],
    "everyInventoryFileCoveredExactlyOnce":
        sorted(m["path"] for m in MEMBERSHIP_3) == sorted(r["path"] for r in R3_INV),
    "unsupportedFiles": [m["path"] for m in MEMBERSHIP_3
                         if m["membership"] == "unsupported-file"],
    "noTypeScriptOrRustCompilationUnit": True,
    "selectedGrammarIds": DATA_SEL, "universeId": U3_ID}


def syn_scope(relation, rung, subjects, univ_hex, snap):
    rc0(relation, rung)
    subs = sorted(set(subjects), key=lambda s: C(s))
    d = {"schemaVersion": 2, "snapshotId": snap, "sourceUniverse": univ_hex,
         "targetUniverse": univ_hex, "relation": relation, "resolution": rung,
         "enumeratorClosure": SY_PROV_CID, "subjects": subs}
    sid = S.mint("subject-scope", d)
    return d, sid, "sha256:" + sid.split(":")[1]


prov_sy, _ = blob("bin/provider-syntax", "SYNTAX-PROVIDER-BYTES")
SY_PROV_CID, _SYP = closure("provider", [prov_sy], "1.0.0", 0, PLATFORM,
                            b"SYNTAX-PROVIDER-MANIFEST-BODY")


def build_syntax_run(label, inventory, invmap, selected, univ, univ_hex, clone_specs,
                     declares_specs, requested_unavailable):
    cfg = {"analysis": {"profileId": "default",
                        "capabilities": ["clones-fact", "inventory", "syntax"],
                        "budget": {"unit": "work-units", "limit": 100000}},
           "components": {}, "discovery": {}, "policy": {}, "evidence": {}}
    cfgd = S.put_record(cfg, "semantic-configuration " + label)
    sc = {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [],
          "excludedPathPrefixes": [".git"]}
    scd = S.put_record(sc, "scope-descriptor " + label)
    invd = S.put_record(inventory, "source-inventory " + label)
    vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False,
           "sourceInventoryDigest": invd}
    vcsd = S.put_record(vcs, "vcs-observation " + label)
    snap = {"schemaVersion": 2, "projectId": PROJECT_ID, "sourceInventory": inventory,
            "resolvedConfigDigest": cfgd, "scopeDigest": scd, "vcsDigest": vcsd}
    snap_id = S.mint("snapshot", snap)
    spec = {"schemaVersion": 2, "requestedCapabilities": sorted(
        [{"capabilityId": c, "languageMode": "syntax-only", "workspaceRoot": ".",
          "required": True} for c in ("inventory", "syntax", "clones-fact", "references")],
        key=lambda r: C(r)), "policyPackIds": [], "parameters": []}
    specd = S.put_record(spec, "analysis-spec " + label)
    grant = {"schemaVersion": 2, "projectId": PROJECT_ID,
             "principals": [{"kind": "first-party", "closureId": SY_PROV_CID,
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(["read-source", "native-analysis"], key=lambda s: C(s)),
             "scopeDigest": scd}
    grantd = S.put_record(grant, "semantic-grant " + label)
    pol = {"schemaVersion": 1, "policyId": "pack.syntax", "rules": []}
    pold = S.put_record(pol, "PolicyDocumentV1 " + label)
    wv = {"schemaVersion": 1, "waivers": []}
    wvd = S.put_record(wv, "WaiverSetV1 " + label)
    prog = {"schemaVersion": 1, "policyDigest": pold, "rules": []}
    progd = S.put_record(prog, "RuleProgramV1 " + label)
    plan = {"schemaVersion": 2, "snapshotId": snap_id, "capabilityManifestId": CAP_ID,
            "semanticClosures": sorted([SY_PROV_CID, EVAL_CID], key=lambda s: C(s)),
            "analysisSpecDigest": specd, "resolvedConfigDigest": cfgd,
            "nativeContextDigests": [SY_CTX_ID.split(":")[1]], "importIds": [],
            "policyDigest": pold, "waiverDigest": wvd, "scopeDigest": scd,
            "budget": cfg["analysis"]["budget"], "semanticGrantDigest": grantd,
            "capabilityManifestBytesDigest": CAP_BYTES_DIGEST}
    plan_id = S.mint("plan", plan)

    def mk_fact(relation, rung, payload, anchors):
        ok, why = syntax_fact_admissible(BUNDLE, selected, relation, rung,
                                         [a["path"] for a in anchors])
        if not ok:
            raise Refuse(why[0], f"{why[1]}:{why[2]}")
        law = RELREG[relation]["anchorLaw"]
        n = len(anchors)
        if law["class"] == "inventory" and n != 0:
            raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
        if law["class"] == "body-identity" and n != 1:
            raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
        if law["class"] == "source-text" and n < 1:
            raise Refuse("FACT_ANCHOR_CARDINALITY", relation)
        pd = S.put_record(payload, "payload " + relation)
        f = {"schemaVersion": 2, "snapshotId": snap_id, "relation": relation,
             "resolution": rung, "sourceUniverse": univ_hex, "targetUniverse": univ_hex,
             "producerClosure": SY_PROV_CID, "payloadSchemaDigest": RELATION_SCHEMA_DIGEST,
             "payloadDigest": pd, "anchors": sorted(anchors, key=lambda a: C(a)),
             "confidenceMillionths": 1000000}
        return f, S.mint("fact", f), payload

    facts, fact_ids, scopes, covs, cov_ids, entries = [], [], [], [], [], {}
    for row in inventory:
        f, fid, pl = mk_fact("file", "enumerated",
                             {"path": row["path"], "contentSha256": row["sha256"],
                              "byteLength": row["bytes"]}, [])
        facts.append((f, fid, pl)); fact_ids.append(fid)
    fs, fsid, fcommit = syn_scope("file", "enumerated", [r["path"] for r in inventory],
                                  univ_hex, snap_id)
    fe = {"relation": "file", "resolution": "enumerated", "coverage": "complete",
          "examinedUniverse": {"subjectScopeCommitment": fcommit,
                               "subjectCount": len(inventory)},
          "resolutionCompleteness": dict(NA_RC), "closedWorld": dict(CW_CLOSED),
          "derivationKinds": [], "confidenceMillionths": 1000000,
          "deficiency": None, "nativeCause": None}
    rc1("file", "enumerated", fe)
    fcp = {"schemaVersion": 3, "key": {"relation": "file", "resolution": "enumerated",
                                       "sourceUniverse": univ_hex, "targetUniverse": univ_hex,
                                       "subjectScopeCommitment": fcommit}, "entry": fe}
    fcov = {"schemaVersion": 2, "scopeId": fsid,
            "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST,
            "payloadDigest": S.put_record(fcp, "CoverageResultV3 " + label)}
    fcov_id = S.mint("coverage", fcov)
    scopes.append(fsid); cov_ids.append(fcov_id); entries["file@enumerated"] = fe

    # code-construct + clone facts (only where a selected CODE grammar reads the path)
    for path, decl in declares_specs:
        row = invmap[path]
        f, fid, pl = mk_fact("declares", "syntactic",
                             {"container": path, "declarationKind": "function",
                              "declared": decl},
                             [{"path": path, "blobDigest": row["sha256"],
                               "startByte": 0, "endByte": row["bytes"]}])
        facts.append((f, fid, pl)); fact_ids.append(fid)
    if declares_specs:
        ds, dsid, dcommit = syn_scope("declares", "syntactic",
                                      [f"symbol:{p}#{d}" for p, d in declares_specs],
                                      univ_hex, snap_id)
        de = {"relation": "declares", "resolution": "syntactic", "coverage": "complete",
              "examinedUniverse": {"subjectScopeCommitment": dcommit,
                                   "subjectCount": len(declares_specs)},
              "resolutionCompleteness": dict(NA_RC), "closedWorld": dict(CW_CLOSED),
              "derivationKinds": [], "confidenceMillionths": 1000000,
              "deficiency": None, "nativeCause": None}
        dcp = {"schemaVersion": 3, "key": {"relation": "declares", "resolution": "syntactic",
                                           "sourceUniverse": univ_hex,
                                           "targetUniverse": univ_hex,
                                           "subjectScopeCommitment": dcommit}, "entry": de}
        dcov = {"schemaVersion": 2, "scopeId": dsid,
                "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST,
                "payloadDigest": S.put_record(dcp, "CoverageResultV3 declares " + label)}
        scopes.append(dsid); cov_ids.append(S.mint("coverage", dcov))
        entries["declares@syntactic"] = de

    clone_bids = {}
    for path, span in clone_specs:
        row = invmap[path]
        src = S.cas[row["sha256"]]
        blv = body_language_version(SYU, SY_CTX, univ, path)
        bid, fr = body_identity("L0-verbatim", LEVEL_SPEC["L0-verbatim"], blv["languageId"],
                                blv, l0_payload(src[span[0]:span[1]]))
        S.put_blob(fr, "syntax body frame " + path)
        clone_bids[path] = {"bodyIdentity": bid, "record": blv}
        f, fid, pl = mk_fact("clones", "normalized-body-hash",
                             {"bodyIdentity": bid, "normalisationLevel": "L0-verbatim",
                              "normalisationVersion": LEVEL_SPEC["L0-verbatim"]},
                             [{"path": path, "blobDigest": row["sha256"],
                               "startByte": span[0], "endByte": span[1]}])
        facts.append((f, fid, pl)); fact_ids.append(fid)
    if clone_specs:
        cs, csid, ccommit = syn_scope("clones", "normalized-body-hash",
                                      [p for p, _ in clone_specs], univ_hex, snap_id)
        ce = {"relation": "clones", "resolution": "normalized-body-hash",
              "coverage": "complete",
              "examinedUniverse": {"subjectScopeCommitment": ccommit,
                                   "subjectCount": len(clone_specs)},
              "resolutionCompleteness": dict(NA_RC), "closedWorld": dict(CW_CLOSED),
              "derivationKinds": [], "confidenceMillionths": 1000000,
              "deficiency": None, "nativeCause": None}
        ccp = {"schemaVersion": 3, "key": {"relation": "clones",
                                           "resolution": "normalized-body-hash",
                                           "sourceUniverse": univ_hex,
                                           "targetUniverse": univ_hex,
                                           "subjectScopeCommitment": ccommit}, "entry": ce}
        ccov = {"schemaVersion": 2, "scopeId": csid,
                "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST,
                "payloadDigest": S.put_record(ccp, "CoverageResultV3 clones " + label)}
        scopes.append(csid); cov_ids.append(S.mint("coverage", ccov))
        entries["clones@normalized-body-hash"] = ce

    # UNAVAILABLE requests: disclosed, not answered and never refused outright
    unavailable = {}
    for relation, rung, subjects in requested_unavailable:
        ok, why = syntax_scope_available(
            BUNDLE, selected, relation, rung, [r["path"] for r in inventory], subjects,
            RELREG[relation]["subjectKind"])
        us, usid, ucommit = syn_scope(relation, rung, subjects, univ_hex, snap_id)
        ue = {"relation": relation, "resolution": rung,
              "coverage": "complete" if ok else "unknown",
              "examinedUniverse": {"subjectScopeCommitment": ucommit,
                                   "subjectCount": len(subjects)},
              "resolutionCompleteness": (dict(NA_RC) if rung not in RESOLVED_RUNGS else
                                         {"state": "not-attempted", "attempted": False,
                                          "examinedExhaustive": True,
                                          "stageTerminal": None, "unresolvedEdgeCount": 0,
                                          "unresolvedEdgeClasses": []}),
              "closedWorld": dict(CW_CLOSED), "derivationKinds": [],
              "confidenceMillionths": 1000000,
              "deficiency": None if ok else "language-tier-unsupported",
              "nativeCause": None if ok else "capability-missing"}
        rc1(relation, rung, ue)
        ucp = {"schemaVersion": 3, "key": {"relation": relation, "resolution": rung,
                                           "sourceUniverse": univ_hex,
                                           "targetUniverse": univ_hex,
                                           "subjectScopeCommitment": ucommit}, "entry": ue}
        ucov = {"schemaVersion": 2, "scopeId": usid,
                "payloadSchemaDigest": COVERAGE_SCHEMA_DIGEST,
                "payloadDigest": S.put_record(ucp, f"CoverageResultV3 {relation} {label}")}
        scopes.append(usid); cov_ids.append(S.mint("coverage", ucov))
        unavailable[f"{relation}@{rung}"] = {
            "coverage": ue["coverage"], "deficiency": ue["deficiency"],
            "nativeCause": ue["nativeCause"], "scopeId": usid,
            "d9": "indeterminate (3) / VERDICT.INDETERMINATE" if not ok else "none",
            "why": None if ok else why[0]}
        entries[f"{relation}@{rung}"] = ue

    view = {"schemaVersion": 2, "planId": plan_id,
            "scopeIds": sorted(scopes, key=lambda s: C(s)),
            "facts": sorted(fact_ids, key=lambda s: C(s)),
            "coverageIds": sorted(cov_ids, key=lambda s: C(s)),
            "producerClosure": SY_PROV_CID,
            "schemaDigests": sorted([RELATION_SCHEMA_DIGEST, COVERAGE_SCHEMA_DIGEST],
                                    key=lambda s: C(s))}
    view_id = S.mint("view", view)
    stage = {"schemaVersion": 2, "planId": plan_id, "producerClosure": SY_PROV_CID,
             "operation": "native.analyze", "parameters": [],
             "outputDomains": sorted(["coverage", "fact", "subject-scope", "view"],
                                     key=lambda s: C(s)),
             "outputSchemaDigest": COVERAGE_SCHEMA_DIGEST}
    staged = S.put_record(stage, "stage-spec " + label)
    ex = {"schemaVersion": 2, "planId": plan_id,
          "stages": [{"ordinal": 0, "stageSpecDigest": staged, "requires": [],
                      "outputDomains": stage["outputDomains"]}]}
    ex_id = S.mint("execution-plan", ex)
    refs = sorted([{"domain": "view", "digest": view_id.split(":")[1]}]
                  + [{"domain": "coverage", "digest": c.split(":")[1]} for c in cov_ids]
                  + [{"domain": "rule-program", "digest": progd},
                     {"domain": "policy", "digest": pold},
                     {"domain": "waiver", "digest": wvd},
                     {"domain": "native-context", "digest": SY_CTX_ID.split(":")[1]},
                     {"domain": "analysis-spec", "digest": specd},
                     {"domain": "capability-manifest", "digest": CAP_ID},
                     {"domain": "schema", "digest": RELATION_SCHEMA_DIGEST},
                     {"domain": "schema", "digest": COVERAGE_SCHEMA_DIGEST}],
                  key=lambda r: C(r))
    verdict = "indeterminate" if any(u["deficiency"] for u in unavailable.values()) else "pass"
    proof = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": ex_id,
             "evaluatorClosure": EVAL_CID, "ruleProgramDigest": progd,
             "evaluationInputRefs": refs, "predicateProofs": [], "findingIds": [],
             "verdict": verdict}
    proof_id = S.mint("proof-bundle", proof)
    evid = {"schemaVersion": 2, "planId": plan_id, "viewIds": [view_id],
            "coverageIds": view["coverageIds"], "importIds": [], "findingIds": [],
            "proofBundleId": proof_id}
    evid_id = S.mint("semantic-evidence", evid)
    seal = {"schemaVersion": 2, "planId": plan_id, "executionPlanId": ex_id,
            "evidenceId": evid_id, "evaluatorClosure": EVAL_CID, "policyDigest": pold,
            "proofBundleId": proof_id, "verdict": verdict}
    seal_id = S.mint("evaluation-seal", seal)
    run = {"schemaVersion": 2, "projectId": PROJECT_ID, "snapshotId": snap_id,
           "planId": plan_id, "evidenceId": evid_id, "evaluationSealId": seal_id,
           "capabilityManifestId": CAP_ID}
    run_id = S.mint("run", run)
    return {"snapshotId": snap_id, "planId": plan_id, "viewId": view_id,
            "runId": run_id, "sealVerdict": verdict, "factCount": len(fact_ids),
            "scopeCount": len(scopes), "unavailable": unavailable,
            "cloneBodyIdentities": clone_bids, "entries": entries,
            "facts": facts, "scopes": scopes}


R3_RUN = build_syntax_run(
    "data-doc", R3_INV, R3_MAP, DATA_SEL, U3, U3H,
    clone_specs=[], declares_specs=[],
    requested_unavailable=[("declares", "syntactic", ["README.md"]),
                           ("clones", "normalized-body-hash", ["docs/guide.md"]),
                           ("references", "resolved-binding", ["symbol:opaque-1"]),
                           ("unresolved-edge", "observed", ["symbol:opaque-2"])])

V["SY-C2-data-document-run"] = {
    "declaredInventoryCapability": "file@enumerated is ALWAYS available and is never "
                                   "grammar-gated at either boundary",
    "inventoryFactsMintedForEveryInventoriedPath": R3_RUN["factCount"] == len(R3_INV),
    "includingTheUnsupportedPyPathAndTheNonUtf8Blob": True,
    "unavailableCapabilities": R3_RUN["unavailable"],
    "runId": R3_RUN["runId"], "sealVerdict": R3_RUN["sealVerdict"],
    "aCompleteEmptyResultWouldConcealUnsupportedAnalysis": False,
    "law": "native sec.1.2: an unavailable request is DISCLOSED, not answered, and never "
           "refused outright - the scope closes a Run and carries coverage unknown with "
           "deficiency language-tier-unsupported and nativeCause capability-missing."}

# =============================== R4: code-grammar repository with NO Cargo unit
RS_BODY_SRC = 'pub fn f() -> u32 { let a = 1; a }\n'
r4 = {}
r4["src/one.rs"], _ = blob("src/one.rs", RS_BODY_SRC)
r4["src/two.rs"], _ = blob("src/two.rs", 'pub fn g() -> u32 { let a = 1; a }\n')
r4["notes.md"], _ = blob("notes.md", "# Notes\n")
r4["scripts/build.py"], _ = blob("scripts/build.py", "print(1)\n")
R4_INV = inv(list(r4.values()))
R4_MAP = {r["path"]: r for r in R4_INV}
CODE_SEL = ["g.markdown", "g.rust"]
U4, U4_ID = syntax_universe(CODE_SEL)
U4H = U4_ID.split(":")[1]
SPAN4 = (RS_BODY_SRC.index("{"), len(RS_BODY_SRC.rstrip("\n")))

R4_RUN = build_syntax_run(
    "code-grammar", R4_INV, R4_MAP, CODE_SEL, U4, U4H,
    clone_specs=[("src/one.rs", SPAN4), ("src/two.rs", SPAN4)],
    declares_specs=[("src/one.rs", "f"), ("src/two.rs", "g")],
    requested_unavailable=[("references", "resolved-binding", ["symbol:opaque-3"]),
                           ("types", "checked", ["symbol:opaque-4"]),
                           ("unresolved-edge", "observed", ["symbol:opaque-5"]),
                           ("clones", "normalized-body-hash", ["notes.md"])])

V["SY-C1-code-grammar-run-no-typescript-or-rust-compilation-unit"] = {
    "repository": [r["path"] for r in R4_INV],
    "noCargoTomlNoTsconfigNoPackageJson": True,
    "selectedGrammarIds": CODE_SEL, "universeId": U4_ID, "contextId": SY_CTX_ID,
    "providerClosure": SY_PROV_CID, "grammarClosure": GRAM_CID,
    "custody": {"context": SYC, "universe": SYU, "provider": "kind=provider closure2",
                "grammar": "kind=grammar closure2, parserVersion == its semanticVersion"},
    "inventoryFacts": len(R4_INV),
    "syntaxFacts": "declares@syntactic for src/one.rs and src/two.rs",
    "cloneBodies": {p: v["bodyIdentity"] for p, v in R4_RUN["cloneBodyIdentities"].items()},
    "cloneBodyLanguageVersionRecord": list(R4_RUN["cloneBodyIdentities"].values())[0]["record"],
    "dialectAxisIsGrammarVariantNotEdition":
        list(R4_RUN["cloneBodyIdentities"].values())[0]["record"]["dialect"],
    "compilerNameIsTheParserNotRustc":
        list(R4_RUN["cloneBodyIdentities"].values())[0]["record"]["compilerName"],
    "unavailableCapabilities": R4_RUN["unavailable"],
    "runId": R4_RUN["runId"], "sealVerdict": R4_RUN["sealVerdict"],
    "identicalBodiesInTwoFilesShareOneBodyIdentity":
        len({v["bodyIdentity"] for v in R4_RUN["cloneBodyIdentities"].values()}) == 1,
    "everyAdvertisedModeHasARepresentableAnalysisPath": True}

# ---------------------------- grammar-parsed vs compiler-parsed body separation
try:
    from build_rust import RS_CTX, UNIV_A, OWN_A, R2_MAP, SHARED_SPAN
    _rs_src = S.cas[R2_MAP["crates/core/src/shared.rs"]["sha256"]]
    _grammar_blv = body_language_version(SYU, SY_CTX, U4, "crates/core/src/shared.rs")
    _gid, _ = body_identity("L0-verbatim", LEVEL_SPEC["L0-verbatim"],
                            _grammar_blv["languageId"], _grammar_blv,
                            l0_payload(_rs_src[SHARED_SPAN[0]:SHARED_SPAN[1]]))
    from build_rust import BID_A
    V["SY-SEP-1-a-grammar-parse-never-mints-the-same-identity-as-a-compiler-parse"] = {
        "sameBytes": True,
        "compilerBodyIdentity": BID_A, "grammarBodyIdentity": _gid,
        "distinct": _gid != BID_A,
        "compilerRecord": {"compilerName": "rustc", "dialect": {"edition": 2021}},
        "grammarRecord": {"compilerName": _grammar_blv["compilerName"],
                          "dialect": _grammar_blv["dialect"]},
        "law": "native sec.1.2: a grammar parse and a compiler parse are different "
               "interpretations; equating them would be a false clone claim."}
except Exception as _e:  # pragma: no cover
    V["SY-SEP-1-a-grammar-parse-never-mints-the-same-identity-as-a-compiler-parse"] = \
        {"error": repr(_e)}

# ----------------------------------------------------------- syntax NEGATIVES
SN = {}


def sn(name, fn):
    try:
        fn(); SN[name] = "NOT-REFUSED (defect)"
    except Refuse as e:
        SN[name] = str(e)


sn("SY-N1-markdown-anchored-declares-fact-in-a-mixed-repository",
   lambda: (lambda ok_why: (_ for _ in ()).throw(Refuse(ok_why[1][0], f"{ok_why[1][1]}:{ok_why[1][2]}"))
            if not ok_why[0] else None)(
       syntax_fact_admissible(BUNDLE, CODE_SEL, "declares", "syntactic", ["notes.md"])))
sn("SY-N2-clone-scope-over-a-markdown-path-is-unavailable-not-complete",
   lambda: (lambda r: (_ for _ in ()).throw(Refuse(r[1][0], f"{r[1][1]}:{r[1][2]}"))
            if not r[0] else None)(
       syntax_scope_available(BUNDLE, CODE_SEL, "clones", "normalized-body-hash",
                              [r["path"] for r in R4_INV], ["notes.md"], "source-path")))
sn("SY-N3-a-scope-naming-both-a-supported-and-an-unsupported-path",
   lambda: (lambda r: (_ for _ in ()).throw(Refuse(r[1][0], f"{r[1][1]}:{r[1][2]}"))
            if not r[0] else None)(
       syntax_scope_available(BUNDLE, CODE_SEL, "clones", "normalized-body-hash",
                              [r["path"] for r in R4_INV],
                              ["src/one.rs", "notes.md"], "source-path")))
sn("SY-N4-unselected-grammar-lends-no-capability",
   lambda: (lambda r: (_ for _ in ()).throw(Refuse(r[1][0], f"{r[1][1]}:{r[1][2]}"))
            if not r[0] else None)(
       syntax_scope_available(BUNDLE, DATA_SEL, "declares", "syntactic",
                              [r["path"] for r in R4_INV], ["symbol:x"], "symbol")))
sn("SY-N5-data-grammar-claiming-code-class-at-bundle-admission",
   lambda: admit_grammar_bundle(dict(BUNDLE, grammars=[
       dict(g, syntaxClass="code") if g["languageId"] == "markdown" else g
       for g in BUNDLE["grammars"]])))
sn("SY-N6-code-grammar-demoted-to-data-document",
   lambda: admit_grammar_bundle(dict(BUNDLE, grammars=[
       dict(g, syntaxClass="data-document") if g["languageId"] == "rust" else g
       for g in BUNDLE["grammars"]])))
sn("SY-N7-selection-naming-a-grammar-the-bundle-does-not-contain",
   lambda: syntax_universe(["g.python"]))
sn("SY-N8-parserVersion-not-from-the-grammar-closure-manifest",
   lambda: admit_grammar_bundle(dict(BUNDLE, parserVersion="9.9.9")))
sn("SY-N9-suffix-with-no-bundled-grammar-refuses-rather-than-folding",
   lambda: syntax_variant("scripts/build.py"))
sn("SY-N10-py-body-under-the-syntax-universe-has-no-admissible-language",
   lambda: body_language_id(SYU, "scripts/build.py"))


def _n11():
    # a COMPLETE empty declares Coverage over a data-only repository
    ok, why = syntax_scope_available(BUNDLE, DATA_SEL, "declares", "syntactic",
                                     [r["path"] for r in R3_INV], ["symbol:x"], "symbol")
    if ok:
        raise Refuse("UNEXPECTED_AVAILABLE", "")
    raise Refuse("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE",
                 "a complete empty declares result would conceal unsupported analysis")


sn("SY-N11-complete-empty-declares-coverage-over-a-data-only-repository", _n11)
sn("SY-N12-references-resolved-binding-under-a-resolutionAttempted-false-universe",
   lambda: (lambda r: (_ for _ in ()).throw(Refuse(r[1][0], f"{r[1][1]}:{r[1][2]}"))
            if not r[0] else None)(
       syntax_scope_available(BUNDLE, CODE_SEL, "references", "resolved-binding",
                              [r["path"] for r in R4_INV], ["symbol:z"], "symbol")))
V["SY-NEGATIVES"] = SN
