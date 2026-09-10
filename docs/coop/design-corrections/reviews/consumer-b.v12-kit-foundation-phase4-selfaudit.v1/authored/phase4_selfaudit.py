#!/usr/bin/env python3
"""Phase 4 self-audit of this origin's five executed-pass grades.

Compares original charter/requirement clauses to exact fields present in the
raw foundation artifacts and to current kit law. Does not remint consumer
records. Frozen stores are membership observations only, not Run admission.
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

PREV = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1")
KIT = PREV / "subject"
DATA = PREV / "data"
OUT = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"

RESOLVED_RUNGS = {
    "checked",
    "from-resolved-calls",
    "resolved-binding",
    "resolved-callee",
    "resolved-target",
}

CHARTER_P4 = (
    "Derive the complete registered relation/rung applicability table. "
    "Derive state-dependent count/class/attempt rules and apply them to retained "
    "scopes and Coverage even when no fact is present. Verify code-versus-data "
    "capability distinction against the published matrix and body/normalizer laws. "
    "Enumeration completeness is distinct from resolution completeness; do not "
    "invent a resolved rung for file facts. Every advertised mode must have a "
    "representable analysis path; document the chosen grammar."
)


def load(p: Path):
    return json.loads(p.read_text())


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_h_frame(raw: bytes) -> tuple[str, dict]:
    pfx = b"opensip.product.v1\x00"
    if not raw.startswith(pfx):
        raise ValueError("not an H frame")
    rest = raw[len(pfx) :]
    i = rest.index(b"\x00")
    domain = rest[:i].decode("ascii")
    rest = rest[i + 1 :]
    ln = int.from_bytes(rest[:8], "big")
    c = rest[8 : 8 + ln]
    return domain, json.loads(c.decode("utf-8"))


def store_facts(store: dict) -> list[dict]:
    out = []
    blobs = store.get("blobs") or {}
    for digest, blob in blobs.items():
        if not isinstance(blob, str):
            continue
        try:
            raw = base64.b64decode(blob)
        except Exception:
            continue
        if not raw.startswith(b"opensip.product.v1\x00"):
            continue
        try:
            domain, rec = parse_h_frame(raw)
        except Exception:
            continue
        if domain != "fact":
            continue
        out.append(
            {
                "digest": digest,
                "typedId": f"fact2:{digest}",
                "relation": rec.get("relation"),
                "resolution": rec.get("resolution"),
            }
        )
    return out


def rc1_class(resolution: str) -> str:
    return "resolved-rung" if resolution in RESOLVED_RUNGS else "not-applicable-rung"


def rc_derive(inp: dict, ladders: dict) -> dict:
    rel = inp.get("relation")
    res = inp.get("resolution")
    if rel not in ladders or res not in ladders[rel]:
        return {"refused": True, "reason": "RC-0 unregistered pair"}
    if res not in RESOLVED_RUNGS:
        return {
            "state": "not-applicable",
            "attempted": False,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }
    exhaustive = bool(inp.get("examinedExhaustive"))
    terminal = inp.get("stageTerminal")
    n_unres = int(inp.get("unresolvedEdgeCount") or 0)
    if inp.get("attempted") is False:
        return {"state": "not-attempted", "attempted": False, "unresolvedEdgeCount": 0}
    if terminal in {"unavailable", "budget-exhausted", "provider-fault", "cancelled", "crash"} or not exhaustive:
        return {"state": "partial", "attempted": True}
    if terminal == "complete" and exhaustive and n_unres == 0:
        return {"state": "complete", "attempted": True, "examinedExhaustive": True}
    if terminal == "complete" and exhaustive and n_unres >= 1:
        return {"state": "incomplete", "attempted": True, "unresolvedEdgeCount": n_unres}
    return {"state": "partial", "attempted": True}


def walk_keys(obj, prefix="$"):
    found = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.add(f"{prefix}.{k}" if prefix != "$" else f"$.{k}")
            found |= walk_keys(v, f"{prefix}.{k}" if prefix != "$" else f"$.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:8]):
            found |= walk_keys(v, f"{prefix}[{i}]")
    return found


def main() -> int:
    rel_schema = load(KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
    grammar = load(KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    grammar_reg = grammar["x-opensip-grammar-capability-registry"]
    matrix = load(KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json")
    identity = load(KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    prior = load(PREV / "output/foundation-data-review.json")

    reg = rel_schema["x-opensip-relation-registry"]
    relations = reg["relations"]
    anchor_class = {}
    for cls_name, cls in reg["anchorLaw"]["classes"].items():
        for rel in cls["members"]:
            anchor_class[rel] = {
                "class": cls_name,
                "cardinality": cls.get("cardinality"),
                "minimum": cls.get("cardinality") if "cardinality" in cls else None,
            }
            if cls_name == "source-text":
                anchor_class[rel]["cardinalityNote"] = "minimum 1"
            elif cls_name == "body-identity":
                anchor_class[rel]["cardinalityNote"] = "exactly 1"
            elif cls_name == "inventory":
                anchor_class[rel]["cardinalityNote"] = "exactly 0"

    # ---- R-RELATION-RUNG-TABLE ---------------------------------------------
    ex_rel = load(DATA / "foundation/relation-rung-table.json")
    derived_rows = []
    pair_rows = []
    for name, row in relations.items():
        derived_rows.append(
            {
                "relation": name,
                "ladder": row["ladder"],
                "subjectKind": row["subjectKind"],
                "universeRule": row["universeRule"],
                "anchorClass": anchor_class[name]["class"],
                "hasCoverageTotality": "coverageTotality" in row,
                "snapshotJoinCount": len(row.get("snapshotJoins") or []),
            }
        )
        for rung in row["ladder"]:
            pair_rows.append(
                {
                    "relation": name,
                    "rung": rung,
                    "rc1Class": rc1_class(rung),
                }
            )
    claimed = {r["relation"]: r for r in ex_rel["rows"]}
    field_cmp = []
    for d in derived_rows:
        c = claimed.get(d["relation"], {})
        field_cmp.append(
            {
                "relation": d["relation"],
                "testedFields": {
                    "ladder": {"kit": d["ladder"], "exhibit": c.get("ladder"), "match": c.get("ladder") == d["ladder"]},
                    "subjectKind": {
                        "kit": d["subjectKind"],
                        "exhibit": c.get("subjectKind"),
                        "match": c.get("subjectKind") == d["subjectKind"],
                    },
                    "universeRule": {
                        "kit": d["universeRule"],
                        "exhibit": c.get("universeRule"),
                        "match": c.get("universeRule") == d["universeRule"],
                    },
                    "anchorClass": {
                        "kit": d["anchorClass"],
                        "exhibit": c.get("anchorClass"),
                        "match": c.get("anchorClass") == d["anchorClass"],
                    },
                },
                "notInExhibit": {
                    "coverageTotality": d["hasCoverageTotality"],
                    "snapshotJoinCount": d["snapshotJoinCount"],
                    "note": "Not required as extra original-clause columns; recorded so completeness is not inferred from the 13 names alone.",
                },
            }
        )
    exhibit_keys = sorted(walk_keys(ex_rel))
    rel_current_law = all(
        all(v["match"] for v in row["testedFields"].values()) for row in field_cmp
    ) and set(claimed) == set(relations) and ex_rel.get("nRelations") == 13
    rel_file_ok = ex_rel.get("fileLadder") == ["enumerated"] and "resolved" not in (ex_rel.get("fileLadder") or [])
    rel_id = {
        "priorGrade": "executed-pass",
        "kind": "standaloneCanonicalVector",
        "originalClause": "Derive the complete registered relation/rung applicability table.",
        "observable": "vectors/relation-rung-table.json",
        "artifact": "data/foundation/relation-rung-table.json",
        "artifactKeys": exhibit_keys,
        "exactInputsTested": [
            "kit x-opensip-relation-registry.relations[name].ladder|subjectKind|universeRule",
            "kit anchorLaw.classes members → class name",
            "exhibit rows[] those four fields",
        ],
        "currentLawMatchOnTestedFields": rel_current_law and rel_file_ok,
        "pairCountFromKit": len(pair_rows),
        "resolvedPairs": [p for p in pair_rows if p["rc1Class"] == "resolved-rung"],
        "notApplicablePairs": [p for p in pair_rows if p["rc1Class"] == "not-applicable-rung"],
        "unexecutedOriginalClause": None,
        "disposition": "prior-grade-stands" if rel_current_law and rel_file_ok else "withdraw",
        "note": "Complete 13-relation table with ladder/subjectKind/universeRule/anchorClass. Pair-level RC-1 class is derived here from the same ladders; the exhibit stores ladders not exploded pairs. Not treated as a missing original observable.",
    }
    if not (rel_current_law and rel_file_ok):
        rel_id["unexecutedOriginalClause"] = "complete registered relation/rung applicability table does not match kit on tested fields"
        rel_id["disposition"] = "withdraw"

    # ---- R-COUNT-CLASS-ATTEMPT ---------------------------------------------
    ex_cca = load(DATA / "foundation/count-class-attempt.json")
    ladders = {n: r["ladder"] for n, r in relations.items()}
    cca_keys = sorted(walk_keys(ex_cca))
    coverage_record_keys = [
        k
        for k in cca_keys
        if any(
            tok in k.lower()
            for tok in (
                "schemaversion",
                "subjectscope",
                "coverage2",
                "resolutioncompleteness",
                "examineduniverse",
                "closedworld",
                "viewentry",
                "coverageresult",
            )
        )
    ]
    scope_like = [k for k in cca_keys if "scope" in k.lower()]
    coverage_like = [k for k in cca_keys if "coverage" in k.lower()]
    cca_rows = []
    for vec in ex_cca.get("vectors") or []:
        inp = vec.get("input") or {}
        independent = rc_derive(inp, ladders)
        cca_rows.append(
            {
                "name": vec.get("name"),
                "inputKeys": sorted(inp.keys()),
                "input": inp,
                "hasScopeRecord": False,
                "hasCoverageRecord": False,
                "factsPresentIsBoolean": isinstance(vec.get("factsPresent"), bool),
                "independentFromInputScalars": independent,
                "claimedDerived": vec.get("derived"),
                "claimedObserved": vec.get("observed"),
                "claimedExpected": vec.get("expected"),
                "scalarLawMatch": (
                    independent.get("state") == (vec.get("derived") or {}).get("state")
                    == (vec.get("expected") or {}).get("state")
                    == (vec.get("observed") or {}).get("state")
                    and independent.get("attempted")
                    == (vec.get("derived") or {}).get("attempted")
                    == (vec.get("expected") or {}).get("attempted")
                ),
            }
        )
    ViewEntry_required = grammar["$defs"]["ViewEntryV3"]["required"]
    subject_scope_required = identity["$defs"]["subject-scope"]["required"]
    cca_scalar_ok = all(r["scalarLawMatch"] for r in cca_rows) and set(ex_cca.get("resolvedRungs") or []) == RESOLVED_RUNGS
    cca_applied_to_records = False  # no Coverage/scope records in artifact
    cca_id = {
        "priorGrade": "executed-pass",
        "kind": "standaloneCanonicalVector",
        "originalClause": "Derive state-dependent count/class/attempt rules and apply them to retained scopes and Coverage even when no fact is present.",
        "observable": "vectors applying the rules to scopes/Coverage with and without facts",
        "artifact": "data/foundation/count-class-attempt.json",
        "artifactKeys": cca_keys,
        "exactInputsTested": [
            "exhibit vectors[].input {relation, resolution, factsPresent, unresolvedEdgeCount, stageTerminal, examinedExhaustive}",
            "kit RC-0 pair membership and RC-1/RC-2 state/attempted from those scalars",
        ],
        "currentLawMatchOnTestedScalars": cca_scalar_ok,
        "appliedToRetainedScopeRecords": cca_applied_to_records,
        "appliedToRetainedCoverageRecords": cca_applied_to_records,
        "coverageLikeKeysInArtifact": coverage_like,
        "scopeLikeKeysInArtifact": scope_like,
        "coverageRecordShapedKeys": coverage_record_keys,
        "kitCoverageEntryRequiredFields": ViewEntry_required,
        "kitSubjectScopeRequiredFields": subject_scope_required,
        "factAbsentCasePresentAsBoolean": any(v.get("factsPresent") is False for v in ex_cca.get("vectors") or []),
        "unexecutedOriginalClause": (
            "apply them to retained scopes and Coverage even when no fact is present "
            "(observable: vectors applying the rules to scopes/Coverage with and without facts). "
            "The artifact retains scalar tuples and a factsPresent boolean; it does not retain a "
            "subject-scope record or a CoverageResultV3/ViewEntryV3. A standaloneCanonicalVector "
            "could retain those records without becoming a complete Run; this one does not."
        ),
        "disposition": "withdraw",
        "withdrawReason": "Prior executed-pass inferred sufficiency from scalar RC-1/RC-2 equality and factsPresent=false. Original clause requires application to retained scopes and Coverage.",
        "notInvented": [
            "Not requiring every registered (relation,rung) pair",
            "Not requiring RC-6 coverage/examinedExhaustive implication as a new case",
            "Not requiring a sealed Run",
        ],
    }

    # ---- R-CODE-VS-DATA-MATRIX ---------------------------------------------
    ex_cvd = load(DATA / "foundation/code-vs-data-matrix.json")
    langs = grammar_reg["languages"]
    code_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "code")
    data_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "data-document")
    body_enum = identity["$defs"]["body-language-version"]["properties"]["languageId"]["enum"]
    cvd_keys = sorted(walk_keys(ex_cvd))
    grammar_table_match = (
        ex_cvd.get("classLaw") == grammar_reg["classLaw"]
        and sorted(ex_cvd.get("codeLanguages") or []) == code_langs
        and sorted(ex_cvd.get("dataLanguages") or []) == data_langs
    )
    json_caps = langs["json"]["capabilities"]
    ts_caps = langs["typescript"]["capabilities"]
    boolean_vs_caps = {
        "jsonHasNoBodyIdentity_boolean": ex_cvd.get("jsonHasNoBodyIdentity"),
        "jsonCapabilitiesContainClones": "clones@normalized-body-hash" in json_caps,
        "typescriptHasClones_boolean": ex_cvd.get("typescriptHasClones"),
        "tsCapabilitiesContainClones": "clones@normalized-body-hash" in ts_caps,
        "bodyLanguageVersionEnum": body_enum,
        "jsonInBodyLanguageEnum": "json" in body_enum,
        "typescriptInBodyLanguageEnum": "typescript" in body_enum,
    }
    matrix_caps = [c["id"] for c in matrix["capabilities"]]
    syntax_only_clones = [
        c
        for c in matrix["cells"]
        if c["capability"] == "clones-fact" and c["mode"] == "syntax-only"
    ]
    syntax_only_syntax = [
        c
        for c in matrix["cells"]
        if c["capability"] == "syntax" and c["mode"] == "syntax-only"
    ]
    exhibit_mentions_matrix = "native-capability-matrix" in json.dumps(ex_cvd)
    exhibit_mentions_body_enum = "body-language-version" in json.dumps(ex_cvd)
    run_citation = ex_cvd.get("frozenSyntaxRunsCitedReadOnly") or {}
    run_measured_fields = [
        k
        for k in cvd_keys
        if any(tok in k.lower() for tok in ("relation", "resolution", "clones", "deficiency", "nativecause", "payload"))
        and "frozen" not in k.lower()
        and "classlaw" not in k.lower()
    ]
    cvd_id = {
        "priorGrade": "executed-pass",
        "kind": "standaloneCanonicalVector",
        "originalClause": "Verify code-versus-data capability distinction against the published matrix and body/normalizer laws.",
        "observable": "matrix application cited on syntax Runs and a table vector",
        "artifact": "data/foundation/code-vs-data-matrix.json",
        "artifactKeys": cvd_keys,
        "exactInputsTestedNow": {
            "grammarRegistryClassLaw": grammar_table_match,
            "codeLanguages": code_langs,
            "dataLanguages": data_langs,
            "booleanVsCapabilityLists": boolean_vs_caps,
            "exhibitSelector": ex_cvd.get("selector"),
            "publishedMatrixArtifact": "native-capability-matrix.v2.json",
            "exhibitCitesPublishedMatrix": exhibit_mentions_matrix,
            "exhibitCitesBodyLanguageVersion": exhibit_mentions_body_enum,
            "matrixCapabilityIds": matrix_caps,
            "syntaxOnlyClonesFactCell": syntax_only_clones,
            "syntaxOnlySyntaxCell": syntax_only_syntax,
            "runPathCitation": run_citation,
            "runMeasuredFieldsInVector": run_measured_fields,
        },
        "currentLawMatchGrammarTable": grammar_table_match
        and boolean_vs_caps["jsonHasNoBodyIdentity_boolean"] is True
        and boolean_vs_caps["jsonCapabilitiesContainClones"] is False
        and boolean_vs_caps["typescriptHasClones_boolean"] is True
        and boolean_vs_caps["tsCapabilitiesContainClones"] is True,
        "unexecutedOriginalClause": (
            "against the published matrix and body/normalizer laws; observable "
            "'matrix application cited on syntax Runs and a table vector'. "
            "The table matches the grammar-capability-registry classLaw and language lists. "
            "It does not retain native-capability-matrix.v2.json cells, body-language-version.languageId "
            "application, or any measured relation/deficiency/nativeCause fields from the cited syntax Run stores. "
            "jsonHasNoBodyIdentity/typescriptHasClones are booleans; prior grade treated those plus capability-list membership as the matrix and body/normalizer verification."
        ),
        "disposition": "withdraw",
        "withdrawReason": "Prior executed-pass used grammar-registry string equality and two booleans. Original clause names the published matrix and body/normalizer laws, and the observable requires matrix application on syntax Runs plus a table vector.",
        "notInvented": [
            "Not requiring a new language mode",
            "Not requiring full Run admission of the cited syntax stores",
            "Not inventing data-format syntax facts the kit says do not exist",
        ],
    }

    # ---- R-ENUM-VS-RESOLUTION ----------------------------------------------
    ex_enum = load(DATA / "foundation/enum-vs-resolution.json")
    store_map = {
        "syntax-code": DATA / "runs/syntax-code.store.json",
        "ts": DATA / "runs/ts.store.json",
        "rust": DATA / "runs/rust.store.json",
        "syntax-data": DATA / "runs/syntax-data.store.json",
        "rust-partial-clones": DATA / "runs/rust-partial-clones.store.json",
    }
    cited_rows = []
    for obs in ex_enum.get("observedFileFacts") or []:
        store = load(store_map[obs["store"]])
        digest = obs["id"].split(":", 1)[-1]
        blob = (store.get("blobs") or {}).get(digest)
        if not isinstance(blob, str):
            cited_rows.append({"store": obs["store"], "id": obs["id"], "ok": False, "reason": "not in blobs"})
            continue
        domain, rec = parse_h_frame(base64.b64decode(blob))
        cited_rows.append(
            {
                "store": obs["store"],
                "id": obs["id"],
                "testedFields": {
                    "domain": domain,
                    "relation": rec.get("relation"),
                    "resolution": rec.get("resolution"),
                },
                "ok": domain == "fact"
                and rec.get("relation") == "file"
                and rec.get("resolution") == "enumerated"
                and rec.get("resolution") == obs.get("resolution"),
            }
        )
    store_census = []
    for name, path in store_map.items():
        facts = store_facts(load(path))
        file_facts = [f for f in facts if f["relation"] == "file"]
        non_enum = [f for f in file_facts if f["resolution"] != "enumerated"]
        store_census.append(
            {
                "store": name,
                "nFactFrames": len(facts),
                "nFileFacts": len(file_facts),
                "nFileNonEnumerated": len(non_enum),
                "fileResolutions": sorted({f["resolution"] for f in file_facts}),
                "admission": "unverified-frozen-membership-only",
            }
        )
    enum_cited_ok = all(r.get("ok") for r in cited_rows) and ex_enum.get("fileRung") == "enumerated"
    enum_census_ok = all(s["nFileNonEnumerated"] == 0 and s["nFileFacts"] >= 1 for s in store_census)
    enum_id = {
        "priorGrade": "executed-pass",
        "kind": "standingRule",
        "originalClause": "Enumeration completeness is distinct from resolution completeness; do not invent a resolved rung for file facts.",
        "observable": "file facts remain on the registered enumerated rung in every claimed graph",
        "artifact": "data/foundation/enum-vs-resolution.json",
        "exactInputsTested": [
            "kit file.ladder == [enumerated]",
            "five cited fact H-frames: relation and resolution fields",
            "membership census of all fact H-frames with relation=file in the five cited frozen stores (not Run admission)",
        ],
        "citedFactRows": cited_rows,
        "storeCensusMembershipOnly": store_census,
        "currentLawMatch": enum_cited_ok and enum_census_ok and rel_file_ok,
        "unexecutedOriginalClause": None,
        "disposition": "prior-grade-stands",
        "limitation": "Frozen stores remain unverified for full Run admission/replay. Membership of relation/resolution only.",
        "note": "Standing rule is a prohibition plus membership on claimed graphs. Cited facts and all file-relation frames in those stores are enumerated. Not upgraded to Coverage totality or Run closure.",
    }
    if not (enum_cited_ok and enum_census_ok and rel_file_ok):
        enum_id["disposition"] = "withdraw"
        enum_id["unexecutedOriginalClause"] = "file facts remain on the registered enumerated rung in every claimed graph"

    # ---- R-ADVERTISED-MODE-PATHS -------------------------------------------
    ex_modes = load(DATA / "foundation/advertised-mode-paths.json")
    kit_modes = list(matrix["languageModes"])
    ctx_set = identity["x-opensip-digest-domains"]["domainSets"]["native-context"]
    uni_set = identity["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"]
    lang_map = identity["x-opensip-digest-domains"]["languageModes"]["map"]
    native_defs = grammar["$defs"]
    mode_rows = []
    for m in ex_modes.get("modes") or []:
        mode = m.get("mode")
        path = m.get("analysisPath") or ""
        expected_ctx = {
            "ts-tsconfig": "native.context.typescript.v2",
            "js-allowjs": "native.context.typescript.v2",
            "js-synthesized": "native.context.typescript.v2",
            "rust-cargo": "native.context.rust.v2",
            "rust-cargo-prepared": "native.context.rust.v2",
            "syntax-only": "native.context.syntax.v2",
        }.get(mode)
        expected_uni = {
            "ts-tsconfig": "native.semantic-universe.typescript.v2",
            "js-allowjs": "native.semantic-universe.typescript.v2",
            "js-synthesized": "native.semantic-universe.typescript.v2",
            "rust-cargo": "native.semantic-universe.rust.v2",
            "rust-cargo-prepared": "native.semantic-universe.rust.v2",
            "syntax-only": "native.semantic-universe.syntax.v2",
        }.get(mode)
        mode_rows.append(
            {
                "mode": mode,
                "inMatrixLanguageModes": mode in kit_modes,
                "languageModeMapTarget": lang_map.get(mode),
                "claimedAnalysisPath": path,
                "claimedRepresentableBoolean": m.get("representable"),
                "namedContextRegistered": expected_ctx in ctx_set if expected_ctx else False,
                "namedUniverseRegistered": expected_uni in uni_set if expected_uni else False,
                "pathContainsRegisteredContext": bool(expected_ctx and expected_ctx in path),
                "pathContainsRegisteredUniverse": bool(expected_uni and expected_uni in path),
                "contextSelector": (ctx_set.get(expected_ctx) or {}).get("selector") if expected_ctx else None,
                "universePresent": expected_uni,
            }
        )
    grammar_doc = ex_modes.get("chosenGrammar") or ""
    grammar_names = {
        "SyntaxGrammarBundleV1": "SyntaxGrammarBundleV1" in native_defs and "SyntaxGrammarBundleV1" in grammar_doc,
        "TypeScriptNativeContextV2": "TypeScriptNativeContextV2" in native_defs and "TypeScriptNativeContextV2" in grammar_doc,
        "NativeContextV2": "NativeContextV2" in native_defs and "NativeContextV2" in grammar_doc,
    }
    modes_cover = [m["mode"] for m in ex_modes.get("modes") or []] == kit_modes
    modes_paths_registered = all(
        r["inMatrixLanguageModes"]
        and r["namedContextRegistered"]
        and r["namedUniverseRegistered"]
        and r["pathContainsRegisteredContext"]
        and r["pathContainsRegisteredUniverse"]
        for r in mode_rows
    )
    modes_id = {
        "priorGrade": "executed-pass",
        "kind": "standingRule",
        "originalClause": "Every advertised mode must have a representable analysis path; document the chosen grammar.",
        "observable": "mode-path table covering advertised modes; missing path is unexecuted, not ACCEPT",
        "artifact": "data/foundation/advertised-mode-paths.json",
        "exactInputsTested": [
            "matrix.languageModes",
            "identity-schemas x-opensip-digest-domains domainSets native-context and native-semantic-universe keys",
            "native-evidence.schemas.v2.json $defs TypeScriptNativeContextV2, NativeContextV2, SyntaxGrammarBundleV1",
            "exhibit modes[].mode and analysisPath strings; chosenGrammar names",
        ],
        "modeRows": mode_rows,
        "chosenGrammar": grammar_doc,
        "chosenGrammarNamesRegistered": grammar_names,
        "representableBooleanNotUsedAsProof": True,
        "currentLawMatch": modes_cover and modes_paths_registered and all(grammar_names.values()),
        "unexecutedOriginalClause": None,
        "disposition": "prior-grade-stands",
        "note": "Representable is shown by registered context/universe domain names in the path string and registered grammar/context defs, not by the representable:true boolean. No new language mode invented.",
    }
    if not modes_id["currentLawMatch"]:
        modes_id["disposition"] = "withdraw"
        modes_id["unexecutedOriginalClause"] = "Every advertised mode must have a representable analysis path; document the chosen grammar."

    # ---- prior checker what it actually tested -----------------------------
    prior_status = {row["id"]: row["status"] for row in prior.get("requirementStatus") or []}
    prior_what_tested = {
        "R-RELATION-RUNG-TABLE": "compared exhibit rows to kit ladder/subjectKind/universeRule/anchorClass; nRelations==13; fileLadder==[enumerated]",
        "R-COUNT-CLASS-ATTEMPT": "compared RC-1/RC-2 derivation of exhibit input scalars to claimed derived/expected/observed; resolvedRungs set equality. Did not require subject-scope or CoverageResultV3 records.",
        "R-CODE-VS-DATA-MATRIX": "grammar-registry classLaw string equality, code/data language lists, json/ts capability-list membership vs two booleans. Did not load matrix cells or body-language-version, did not measure syntax Run fields.",
        "R-ENUM-VS-RESOLUTION": "decoded five cited fact H-frames; relation/resolution membership only.",
        "R-ADVERTISED-MODE-PATHS": "mode list equals matrix.languageModes; analysisPath string equality to a hardcoded map; representable boolean must be true.",
    }

    grades = {
        "R-RELATION-RUNG-TABLE": rel_id,
        "R-COUNT-CLASS-ATTEMPT": cca_id,
        "R-CODE-VS-DATA-MATRIX": cvd_id,
        "R-ENUM-VS-RESOLUTION": enum_id,
        "R-ADVERTISED-MODE-PATHS": modes_id,
    }
    withdrawn = [i for i, g in grades.items() if g["disposition"] == "withdraw"]
    stands = [i for i, g in grades.items() if g["disposition"] == "prior-grade-stands"]
    contradictions = []
    if not rel_current_law:
        contradictions.append("R-RELATION-RUNG-TABLE tested fields mismatch kit")
    if not cca_scalar_ok:
        contradictions.append("R-COUNT-CLASS-ATTEMPT scalar RC derivation mismatches exhibit claims")
    if enum_id["disposition"] == "withdraw":
        contradictions.append("R-ENUM-VS-RESOLUTION membership failed")
    if not modes_id["currentLawMatch"] and modes_id["disposition"] == "withdraw":
        contradictions.append("R-ADVERTISED-MODE-PATHS registered-path check failed")

    if contradictions:
        verdict = "PHASE4_DATA_REFUSED"
    elif withdrawn:
        verdict = "PHASE4_DATA_INCOMPLETE"
    else:
        verdict = "PHASE4_DATA_ADMITS"

    results = {
        "checker": "phase4_selfaudit.py",
        "command": f"{PY} -I -B {OUT / 'phase4_selfaudit.py'}",
        "verdict": verdict,
        "charterParagraph": CHARTER_P4,
        "scope": "Focused follow-through on this origin's five Phase 4 grades. StandaloneCanonicalVector / standingRule observables only. Not a complete Run demand, not whole-foundation or 123-requirement ACCEPT, not product qualification.",
        "priorDisposition": {
            "priorReview": "consumer-b.v12-fresh-foundation-data-review.v1 FOUNDATION_DATA_ADMITS",
            "priorTraceRecheck": "consumer-b.v12-kit-foundation-trace-recheck.v1 TRACE_DATA_ADMITS remains historical",
            "priorPhase4Grades": {i: prior_status.get(i, "executed-pass") for i in grades},
            "priorWhatWasActuallyTested": prior_what_tested,
            "withdrawnNow": withdrawn,
            "standsNow": stands,
        },
        "grades": grades,
        "sourceMap": {
            "charter": "original-consumer-charter.txt Phase 4 paragraph",
            "requirements": {
                "R-RELATION-RUNG-TABLE": "standaloneCanonicalVector; observable vectors/relation-rung-table.json",
                "R-COUNT-CLASS-ATTEMPT": "standaloneCanonicalVector; observable vectors applying the rules to scopes/Coverage with and without facts",
                "R-CODE-VS-DATA-MATRIX": "standaloneCanonicalVector; observable matrix application cited on syntax Runs and a table vector",
                "R-ENUM-VS-RESOLUTION": "standingRule; observable file facts remain on enumerated rung in every claimed graph",
                "R-ADVERTISED-MODE-PATHS": "standingRule; observable mode-path table covering advertised modes",
            },
            "kit": {
                "relationRegistry": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry",
                "rcLaws": "docs/v2/contracts/product-v1/native-evidence.md §4.3 RC-0/RC-1/RC-2",
                "grammarRegistry": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/x-opensip-grammar-capability-registry",
                "publishedMatrix": "docs/coop/design-corrections/native/native-capability-matrix.v2.json",
                "bodyLanguageVersion": "identity-schemas.v3.json#/$defs/body-language-version",
                "coverageEntry": "native-evidence.schemas.v2.json#/$defs/ViewEntryV3 and CoverageResultV3",
                "subjectScope": "identity-schemas.v3.json#/$defs/subject-scope",
                "languageModes": "native-capability-matrix.v2.json languageModes; identity-schemas domainSets",
            },
            "artifacts": {
                "R-RELATION-RUNG-TABLE": "data/foundation/relation-rung-table.json",
                "R-COUNT-CLASS-ATTEMPT": "data/foundation/count-class-attempt.json",
                "R-CODE-VS-DATA-MATRIX": "data/foundation/code-vs-data-matrix.json",
                "R-ENUM-VS-RESOLUTION": "data/foundation/enum-vs-resolution.json plus five frozen stores for membership",
                "R-ADVERTISED-MODE-PATHS": "data/foundation/advertised-mode-paths.json",
            },
            "priorChecker": "consumer-b.v12-fresh-foundation-data-review.v1/output/independent-checker.py relation/count/matrix/enum/mode blocks",
        },
        "existingLawMisses": [],
        "missingOrContradictoryNorm": [],
        "notInvented": [
            "No complete Run requirement",
            "No new language mode",
            "No demand to test every (relation,rung) pair or every RC-2 fixture name",
            "No remint of consumer records",
        ],
        "limitations": [
            "Frozen Run stores remain unverified for admission/replay.",
            "S-* author-process custody remains external from the prior review.",
            "This audit does not re-open phases 0-3 or the trace successor recheck.",
        ],
    }
    (OUT / "phase4-selfaudit-results.json").write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(
        json.dumps(
            {
                "verdict": verdict,
                "withdrawn": withdrawn,
                "stands": stands,
                "enumCensus": store_census,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
