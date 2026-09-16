"""Phase 4/5 observables derived from the ADMITTED exported Runs (never from builders' claims):

  vectors/relation-rung-table.json            R-RELATION-RUNG-TABLE (from phase4 tables)
  vectors/code-vs-data-matrix.json            R-CODE-VS-DATA-MATRIX (table + application cited on syntax Runs)
  vectors/enum-vs-resolution.json             R-ENUM-VS-RESOLUTION (every file fact of every positive store on enumerated)
  vectors/rust-body-identity-pairs.json       R-RUN-RUST-STABLE-BODY / SAME-FILE-TWO-EDITIONS / VERSION-COMPONENT / LARGE-EDITION-MAP
  vectors/unsupported-grammar.json            R-RUN-UNSUPPORTED-GRAMMAR (+ syntax disclosure refusals)
  vectors/hidden-mismatch-per-language.json   R-HIDDEN-MISMATCH-PER-LANGUAGE (first refusal + masked later, per language)
Every vector carries classification valid|invalid|explanatory, firstRefusal and masksLater where negative.
Usage: python3 tools/runref.py tools/phase5_vectors.py
"""
import copy
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output/preserved/pre-s41"
sys.path.insert(0, OUT + "/ref")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import native_ctx as NC  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
REL = "foundation/relation-payload-schemas.v2.json"
NE = "native/native-evidence.schemas.v2.json"
POSITIVES = ["syntax-code", "syntax-data", "syntax-mixed-disclosed", "syntax-mixed-omitted", "ts-pass", "ts-fail", "ts-clones-required",
             "rust-mixed", "rust-mixed-clones-required", "rust-extra-unit", "rust-same-file-2021", "rust-ambiguous", "rust-partial"]
failures = []


def dump(rel, obj):
    with open(f"{OUT}/{rel}", "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def check(name, cond, detail):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def admitted(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    replay = json.load(open(f"{OUT}/runs/{name}.replay.json"))
    return store, C, g, replay, exported


def relation_and_matrix():
    t = json.load(open(f"{OUT}/vectors/phase4-tables.json"))
    dump("vectors/relation-rung-table.json", {"classification": "explanatory", "source": "vectors/phase4-tables.json (tools/phase4_tables.py)",
                                              "selectors": ["foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry",
                                                            "foundation/evaluator-projection-registry.v1.json#/relations", "coop/artifacts/fact-plane.v1.json#/relationRegistry/dependsOn"],
                                              "rows": t["tables"]["relationRung"], "stateRuleVectors": t["countClassAttemptVectors"],
                                              "assertionFailures": t["assertionFailures"]})
    applications = {}
    for name in ("syntax-code", "syntax-data", "syntax-mixed-disclosed"):
        store, C, g, replay, _ = admitted(name)
        per_lang = {}
        for fid, f in g["facts"].items():
            for a in f["anchors"]:
                gr, caps = NF.syntax_path_capabilities(next(iter(g["bound"].values())), a["path"])
                per_lang.setdefault(gr["languageId"] if gr else "no-bundled-grammar", set()).add(f"{f['relation']}@{f['resolution']}")
        disclosed = sorted({(g["scopes"][cov["scopeId"]]["relation"], p["entry"]["deficiency"], p["entry"]["nativeCause"])
                            for cov, p in g["coverages"].values() if p["entry"]["deficiency"]})
        applications[name] = {"closure": replay["result"], "anchoredFactCapabilitiesByLanguage": {k: sorted(v) for k, v in per_lang.items()},
                              "disclosedCoverage": disclosed}
        check(f"matrix-{name}-admitted", replay["result"] == "ADMIT", replay["result"])
    for lang, caps in applications["syntax-code"]["anchoredFactCapabilitiesByLanguage"].items():
        check("code-grammar-facts-within-registry", set(caps) <= set(NF.GRAMMARS.get(lang, {}).get("capabilities", [])), (lang, caps))
    check("data-run-discloses-declares-and-clones",
          {r for r, _, _ in applications["syntax-data"]["disclosedCoverage"]} >= {"declares", "clones"}, applications["syntax-data"]["disclosedCoverage"])
    dump("vectors/code-vs-data-matrix.json", {"classification": "valid", "table": t["tables"]["codeVsData"], "appliedOnAdmittedSyntaxRuns": applications,
                                              "selectors": ["native/native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
                                                            "native-evidence.md s1.2 (lines 436-445)"]})


def enum_vs_resolution():
    rows = []
    for name in POSITIVES:
        exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
        store = Store.load(exported)
        file_facts = []
        for row in exported["objectTable"]:
            if row["domain"] == "fact":
                f = store.get_frame(row["frameSha256"], {"fact"})[1]
                if f["relation"] == "file":
                    file_facts.append(f["resolution"])
        ok = bool(file_facts) and set(file_facts) == {"enumerated"}
        check(f"file-facts-enumerated-{name}", ok, sorted(set(file_facts)))
        rows.append({"run": name, "fileFacts": len(file_facts), "resolutions": sorted(set(file_facts)), "onlyEnumerated": ok})
    dump("vectors/enum-vs-resolution.json", {"classification": "valid", "law": "file ladder is [enumerated]; no resolved rung is invented for file facts",
                                             "selector": "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/file/ladder",
                                             "runs": rows})


def rust_pairs():
    out = {"classification": "valid", "pairs": []}
    info = {}
    for name in ("rust-mixed", "rust-extra-unit", "rust-same-file-2021"):
        store, C, g, replay, exported = admitted(name)
        U, bound = next(iter(g["bound"].items()))
        ctx = bound["contextAdmission"]["context"]
        bodies = {}
        for fid, f in g["facts"].items():
            if f["relation"] != "clones":
                continue
            p = g["payloads"][fid]
            path = f["anchors"][0]["path"]
            frame = store.get_bytes(p["bodyIdentity"][7:])
            parts = NF.body_frame_parse(frame)
            rec, lang, refusal = NC.body_language_version(bound, path)
            bodies[path] = {"bodyIdentity": p["bodyIdentity"], "levelId": parts["level"].decode(), "languageId": parts["languageId"].decode(),
                            "languageVersionHex": parts["languageVersion"].hex(), "derivedBodyLanguageVersion": rec,
                            "derivedLanguageVersionHex": hashlib.sha256(K.C(rec)).hexdigest() if rec else None,
                            "frameLanguageVersionMatchesDerivation": rec is not None and parts["languageVersion"] == hashlib.sha256(K.C(rec)).digest()}
            check(f"version-component-derived-{name}-{path}", bodies[path]["frameLanguageVersionMatchesDerivation"], refusal)
        own = bound["sourceUnitOwnership"]
        info[name] = {"closure": replay["result"], "universe": U, "bodies": bodies, "editionMapEntries": len(bound["universe"]["edition"]),
                      "compilerContext": {"rustcVersion": ctx["toolchain"]["rustcVersion"], "rustCommitHash": ctx["toolchain"]["rustCommitHash"]},
                      "selectedUnits": [(u["crateName"], u["targetKind"], u["targetName"], u["targetEdition"]) for u in own["units"] if u["unitId"] in set(own["selectedUnitIds"])],
                      "packageEditions": {k: v for k, v in bound["universe"]["edition"].items() if not k.startswith("dep_")}}
        check(f"rust-pair-run-admitted-{name}", replay["result"] == "ADMIT", replay["result"])
    m, x, t = info["rust-mixed"], info["rust-extra-unit"], info["rust-same-file-2021"]
    lib = "crates/a/src/lib.rs"
    common = "crates/a/src/common.rs"
    stable = m["bodies"][lib]["bodyIdentity"] == x["bodies"][lib]["bodyIdentity"] and m["universe"] != x["universe"]
    check("stable-body-on-ownership-change", stable, (m["bodies"][lib]["bodyIdentity"], x["bodies"][lib]["bodyIdentity"]))
    out["pairs"].append({"property": "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE", "runs": ["rust-mixed", "rust-extra-unit"],
                         "change": "extra unselected bench unit 'perf' owning crates/a/src/lib.rs added to SourceUnitOwnershipV1 (universe identity changes)",
                         "universes": [m["universe"], x["universe"]], "bodyIdentities": [m["bodies"][lib]["bodyIdentity"], x["bodies"][lib]["bodyIdentity"]],
                         "effectiveDialect": [m["bodies"][lib]["derivedBodyLanguageVersion"]["dialect"], x["bodies"][lib]["derivedBodyLanguageVersion"]["dialect"]],
                         "measured": stable})
    two = m["bodies"][common]["derivedBodyLanguageVersion"]["dialect"] != t["bodies"][common]["derivedBodyLanguageVersion"]["dialect"] and \
        m["bodies"][common]["bodyIdentity"] != t["bodies"][common]["bodyIdentity"]
    check("same-file-two-editions", two, (m["bodies"][common], t["bodies"][common]))
    out["pairs"].append({"property": "R-RUN-RUST-SAME-FILE-TWO-EDITIONS", "path": common, "runs": ["rust-mixed", "rust-same-file-2021"],
                         "selections": [m["selectedUnits"], t["selectedUnits"]],
                         "dialects": [m["bodies"][common]["derivedBodyLanguageVersion"]["dialect"], t["bodies"][common]["derivedBodyLanguageVersion"]["dialect"]],
                         "bodyIdentities": [m["bodies"][common]["bodyIdentity"], t["bodies"][common]["bodyIdentity"]], "measured": two})
    target_edition = next(u for u in m["selectedUnits"] if u[2] == "tool")
    check("target-edition-differs-from-package-default", target_edition[3] is not None and target_edition[3] != m["packageEditions"]["a"], target_edition)
    out["pairs"].append({"property": "R-RUN-RUST-TARGET-EDITION / MIXED-EDITION / HASH-MARKER", "run": "rust-mixed",
                         "packageEditions": m["packageEditions"], "binTarget": target_edition,
                         "bodyDialects": {p: b["derivedBodyLanguageVersion"]["dialect"] for p, b in m["bodies"].items()},
                         "hashMarkerPaths": sorted(p for p in m["bodies"] if "#" in p)})
    same_bytes = m["bodies"][lib]["bodyIdentity"] != m["bodies"]["crates/#b/src/lib.rs"]["bodyIdentity"]
    check("identical-bytes-different-edition-identity", same_bytes, None)
    out["pairs"].append({"property": "R-RUN-RUST-VERSION-COMPONENT / LARGE-EDITION-MAP", "run": "rust-mixed", "editionMapEntries": m["editionMapEntries"],
                         "compilerContext": m["compilerContext"],
                         "versionComponents": {p: {"dialect": b["derivedBodyLanguageVersion"]["dialect"], "languageVersionHex": b["languageVersionHex"],
                                                   "derivedFromContextAndOwnership": b["frameLanguageVersionMatchesDerivation"]} for p, b in m["bodies"].items()},
                         "identicalBodyBytesDifferentEditionGiveDifferentIdentity": same_bytes})
    out["runs"] = info
    dump("vectors/rust-body-identity-pairs.json", out)


def unsupported_grammar():
    store, C, g, replay, exported = admitted("syntax-mixed-disclosed")
    U, bound = next(iter(g["bound"].items()))
    inv_rows = g["snapshot"]["sourceInventory"]
    membership = store.get_record(g["enum"]["membershipDigest"])
    vectors = []

    def vec(name, classification, faults, expect_first, note):
        first = faults[0] if faults else None
        ok = (first is None and expect_first is None) or (first is not None and expect_first is not None and first.startswith(expect_first))
        check(name, ok, faults)
        vectors.append({"vector": name, "classification": classification, "firstRefusal": first, "masksLater": faults[1:], "expected": expect_first,
                        "pass": ok, "note": note})

    row = next(r for r in membership["rows"] if r["path"] == "LICENSE")
    vec("membership-no-bundled-grammar", "explanatory", [] if (row["membership"], row["reason"]) == ("unsupported-file", "no-bundled-grammar") else ["membership-mismatch"],
        None, f"LICENSE membership {row['membership']}/{row['reason']}")
    for path in ("LICENSE", "README.md", "data/config.json"):
        rec, lang, refusal = NC.body_language_version(bound, path)
        vec(f"body-language-version-{path}", "invalid", [refusal] if refusal else [], "BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN",
            "no bundled code grammar variant selects this suffix; no body identity can be minted")
    # a declares fact anchored in a data-document grammar file
    s2 = Store.load(exported)
    blob = next(r for r in inv_rows if r["path"] == "data/config.json")
    payload = {"container": "file:data/config.json", "declared": "sym:data/config.json#k", "declarationKind": "field"}
    fact = {"schemaVersion": 2, "snapshotId": g["plan"]["snapshotId"], "relation": "declares", "resolution": "syntactic", "sourceUniverse": U,
            "targetUniverse": U, "producerClosure": next(iter(g["views"].values()))["producerClosure"], "payloadSchemaDigest": KIT.digest(REL),
            "payloadDigest": s2.put_record(payload), "anchors": [{"path": "data/config.json", "blobDigest": blob["sha256"], "startByte": 1, "endByte": 4}],
            "confidenceMillionths": 1000000}
    faults, _ = NF.fact_faults(s2, fact, g["plan"]["snapshotId"], inv_rows, g["bound"])
    vec("declares-fact-on-data-grammar", "invalid", faults, "SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "json is data-document: no code-construct syntax facts")
    # clones Coverage over no-bundled-grammar/data paths: complete, disclosed, wrong cause, wrong deficiency, undisclosed
    sid, sc = next((s, x) for s, x in g["scopes"].items() if x["relation"] == "clones" and "LICENSE" in x["subjects"])
    cid = next(c for c, (cd, p) in g["coverages"].items() if cd["scopeId"] == sid)
    for label, patch, expect in (("disclosed", {}, None),
                                 ("false-complete", {"coverage": "complete", "deficiency": None, "nativeCause": None,
                                                     "resolutionCompleteness": {"examinedExhaustive": True, "stageTerminal": "complete"}}, "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE"),
                                 ("wrong-deficiency", {"deficiency": "provider-unavailable", "nativeCause": "linker-unavailable"}, "cb24.SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH"),
                                 ("wrong-cause", {"deficiency": "language-tier-unsupported", "nativeCause": None}, "native.coverage-cause-required"),
                                 ("undisclosed-unknown", {"deficiency": None, "nativeCause": None}, "cb24.SYNTAX_CAPABILITY_UNDISCLOSED")):
        cd, p = copy.deepcopy(g["coverages"][cid])
        for k, v in patch.items():
            if isinstance(v, dict):
                p["entry"][k].update(v)
            else:
                p["entry"][k] = v
        cd["payloadDigest"] = s2.put_record(p)
        faults, _ = NF.coverage_faults(s2, cd, sc, sid, [], bound, inv_rows)
        vec(f"clones-coverage-{label}", "valid" if expect is None else "invalid", faults, expect, f"scope subjects {sc['subjects']}")
    # an unselected grammar lends no capability
    ctx_hex = g["plan"]["nativeContextDigests"][0]
    uni = copy.deepcopy(bound["universe"])
    uni["selectedGrammarIds"] = [x for x in uni["selectedGrammarIds"] if x != "cb24-rust"]
    uhex = s2.put_frame("native.semantic-universe.syntax.v2", uni)
    adm = NC.admit_native_context(s2, ctx_hex, inv_rows)
    b2 = NC.bind_universe(s2, uhex, {ctx_hex: adm}, inv_rows)
    gr, caps = NF.syntax_path_capabilities(b2, "tools/run.rs")
    vec("unselected-grammar-lends-no-capability", "invalid", [] if caps else ["SYNTAX_CAPABILITY_UNSUPPORTED_FACT:no-selected-grammar-for-.rs"],
        "SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "universe selecting every bundled grammar except rust; .rs path has no capability")
    dump("vectors/unsupported-grammar.json", {"baseRun": "syntax-mixed-disclosed", "baseClosure": replay["result"], "vectors": vectors,
                                              "selectors": ["native/native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
                                                            "foundation/identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.syntax.v2/languageVersionBinding",
                                                            "native-evidence.md s1.2 lines 432-445"]})


def hidden_mismatch():
    rows = []
    for path in sorted(glob.glob(f"{OUT}/runs/*~*.replay.json")):
        name = os.path.basename(path)[:-len(".replay.json")]
        rep = json.load(open(path))
        faults = rep.get("faultsInStageOrder") or (rep["graphAdmission"]["faults"] + rep["semanticReplay"].get("faults", []))
        lang = name.split("-")[0]
        rows.append({"run": name, "language": {"ts": "typescript", "rust": "rust", "syntax": "syntax"}.get(lang, lang), "result": rep["result"],
                     "classification": "invalid" if rep["result"] == "REFUSE" else "valid-measurement",
                     "firstRefusal": faults[0] if faults else None, "masksLater": faults[1:],
                     "boundary": (rep.get("firstRefusal") or {}).get("stage") or ("graph-admission" if rep["graphAdmission"]["faults"] else
                                                                                  ("semantic-replay" if rep["semanticReplay"].get("faults") else None)),
                     "retainedClosureFirstRefusal": rep.get("retainedClosure", {}).get("firstRefusal"),
                     "publishedKey": bool(faults) and not faults[0].startswith("cb24.")})
    for lang in ("typescript", "rust"):
        check(f"hidden-mismatch-{lang}", any(r["language"] == lang and r["result"] == "REFUSE" for r in rows), lang)
    dump("vectors/hidden-mismatch-per-language.json", {"rows": rows, "note": "each row is a fully re-framed and re-keyed Run built around one mutated input; "
                                                        "firstRefusal is the first fault of fresh-process close_run; publishedKey=false marks this reconstruction's own cb24.* key"})


def main():
    relation_and_matrix()
    enum_vs_resolution()
    rust_pairs()
    unsupported_grammar()
    hidden_mismatch()
    print("failures", json.dumps(failures)[:3000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
