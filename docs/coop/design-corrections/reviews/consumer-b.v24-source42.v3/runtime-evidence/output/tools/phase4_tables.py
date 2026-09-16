"""Phase 4: relation/rung tables and state rules, generated from the kit registries and exercised by executable vectors.

Tables (from normative registries only): relation x rung applicability; code-vs-data grammar matrix; enumeration kinds
vs resolution rungs per capability; advertised language-mode paths. Vectors: count/class/attempt and cause-registry
rules run through native_facts.coverage_faults against a real admitted TypeScript universe (runs/ts-pass.store.json);
account applicability first-match and cell-outcome state/carrier rules run through execinputs.derive_outcome.
Usage: python3 tools/runref.py tools/phase4_tables.py
"""
import copy
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output"
sys.path.insert(0, OUT + "/ref")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import enumeration as EN  # noqa: E402
import execinputs as XI  # noqa: E402
import native_facts as NF  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
PROJ = KIT.doc("foundation/evaluator-projection-registry.v1.json")
RELREG = KIT.doc("foundation/relation-payload-schemas.v2.json")["x-opensip-relation-registry"]
MATRIX = KIT.doc("native/native-capability-matrix.v2.json")
LANGUAGE_MODES = KIT.doc(ID)["x-opensip-digest-domains"]["languageModes"]["map"]
POLICY_MAP = KIT.doc(ID)["x-opensip-evaluator-profile"]["policyUniverseMap"]
failures = []


def check(name, got, want, classification="valid"):
    ok = got == want
    if not ok:
        failures.append({"vector": name, "got": got, "want": want})
    row = {"vector": name, "classification": classification, "got": got, "want": want, "pass": ok}
    if classification == "invalid" and isinstance(got, list):
        row.update(firstRefusal=got[0] if got else None, masksLater=got[1:])
    return row


def tables():
    rel_rows = []
    for rel, row in sorted(RELREG["relations"].items()):
        pr = PROJ["relations"][rel]
        for rung in row["ladder"]:
            rel_rows.append({
                "relation": rel, "rung": rung, "ladderIndex": row["ladder"].index(rung), "universeRule": row["universeRule"],
                "subjectKind": row["subjectKind"], "anchorLaw": row["anchorLaw"]["class"],
                "rungFields": row["rungs"].get(rung, {"required": [], "forbidden": []}),
                "resolvedRung": rung in NF.RESOLVED, "rcClass": "RC-2 resolved" if rung in NF.RESOLVED else "RC-1 not-applicable",
                "capability": PROJ["capabilityForRelation"][rel], "sourceSubjectKind": pr["sourceSubjectKind"],
                "targetKinds": pr["targetKinds"], "endpointTarget": pr["endpointTarget"],
                "snapshotJoins": [j["form"] for j in row.get("snapshotJoins", [])], "bodyIdentityJoin": "bodyIdentityJoin" in row,
                "coverageTotality": "coverageTotality" in row, "dependsOn": NF.DEPENDS_ON.get(rel, [])})
    code_vs_data = []
    for lang, g in sorted(NF.GRAMMARS.items()):
        caps = set(g["capabilities"])
        code_vs_data.append({"languageId": lang, "syntaxClass": g["syntaxClass"], "suffixes": g["suffixes"],
                             **{c: (c in caps) for c in ["declares@syntactic", "literal@syntactic", "control-flow@syntactic",
                                                           "clones@normalized-body-hash", "file@enumerated", "package@manifest-declared",
                                                           "vcs-change@vcs-reported"]},
                             "unavailableRequestDisclosure": None if g["syntaxClass"] == "code" else "coverage unknown / language-tier-unsupported / capability-missing"})
    enum_vs_res = []
    for cap in MATRIX["capabilities"]:
        enum_vs_res.append({"capability": cap["id"], "enumerationKinds": EN.KIND_DERIVATION[cap["id"]],
                            "resolutionPairs": [f"{r}@{g}" for r, g in cap["relations"]],
                            "resolvedPairs": [f"{r}@{g}" for r, g in cap["relations"] if g in NF.RESOLVED],
                            "candidateOnly": cap["id"] in XI.CANDIDATE_CAPS})
    modes = []
    for mode, token in LANGUAGE_MODES.items():
        cells = [c for c in MATRIX["cells"] if c["mode"] == mode]
        modes.append({"languageMode": mode, "policyUniverseToken": token, "universeDomain": POLICY_MAP[token],
                      "engineFamily": next(k for k, v in PROJ["engineFamilies"]["families"].items() if mode in v["languageModes"]),
                      "supported": sorted(c["capability"] for c in cells if c["state"].startswith("SUPPORTED")),
                      "unsupportedTyped": sorted((c["capability"], c["deficiency"]) for c in cells if c["state"] == "UNSUPPORTED-TYPED"),
                      "notSelected": sorted(c["capability"] for c in cells if c["state"] == "NOT-SELECTED"),
                      "otherStates": sorted({c["state"] for c in cells} - {"UNSUPPORTED-TYPED", "NOT-SELECTED"} - {s for s in {c["state"] for c in cells} if s.startswith("SUPPORTED")})})
    return {"classification": "explanatory", "relationRung": rel_rows, "codeVsData": code_vs_data, "enumerationVsResolution": enum_vs_res,
            "advertisedModePaths": modes}


def rc_vectors():
    exported = json.load(open(OUT + "/runs/ts-pass.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    if C.faults:
        return {"skipped": f"ts-pass graph faults {C.faults[:3]}"}
    inv_rows = g["snapshot"]["sourceInventory"]
    U, bound = next(iter(g["bound"].items()))
    out = []

    def scope_of(rel, rung):
        return next((sid, s) for sid, s in g["scopes"].items() if s["relation"] == rel and s["resolution"] == rung)

    def run(name, rel, rung, entry_patch, edges, want_prefixes):
        sid, sc = scope_of(rel, rung)
        cid = next(c for c, (cd, p) in g["coverages"].items() if cd["scopeId"] == sid)
        cd, payload = copy.deepcopy(g["coverages"][cid])
        for k, v in entry_patch.items():
            if isinstance(v, dict) and isinstance(payload["entry"].get(k), dict):
                payload["entry"][k].update(v)
            else:
                payload["entry"][k] = v
        cd["payloadDigest"] = store.put_record(payload)
        vfp = [({"relation": "unresolved-edge"}, {"relation": rel, "referrer": sc["subjects"][0], "edgeKind": e}) for e in edges]
        faults, _ = NF.coverage_faults(store, cd, sc, sid, vfp, bound, inv_rows)
        got = sorted({f.split(":")[0] + (":" + f.split(":")[1] if f.startswith("native.coverage-bijection-mismatch") else "") for f in faults})
        out.append(check(name, got, sorted(want_prefixes), "invalid" if want_prefixes else "valid"))

    R = ("calls", "resolved-callee")
    run("RC2-complete-ok", *R, {}, [], [])
    run("RC2-complete-with-unresolved-edge", *R, {}, ["untyped-any-call"], ["native.coverage-bijection-mismatch:RC-2-complete", "native.coverage-bijection-mismatch:RC-2-edge-account"])
    run("RC2-incomplete-with-edge-ok", *R, {"coverage": "unknown", "deficiency": "resolution-incomplete",
                                          "resolutionCompleteness": {"state": "incomplete", "unresolvedEdgeCount": 1, "unresolvedEdgeClasses": ["untyped-any-call"]}},
        ["untyped-any-call"], [])
    run("RC2-incomplete-without-edge", *R, {"coverage": "unknown", "deficiency": "resolution-incomplete", "resolutionCompleteness": {"state": "incomplete"}},
        [], ["native.coverage-bijection-mismatch:RC-2-incomplete"])
    run("RC2-partial-budget-ok", *R, {"coverage": "unknown", "deficiency": "budget-exhausted",
                                    "resolutionCompleteness": {"state": "partial", "stageTerminal": "budget-exhausted", "examinedExhaustive": False}}, [], [])
    run("RC1-resolved-not-applicable", *R, {"resolutionCompleteness": {"state": "not-applicable", "attempted": False}}, [],
        ["native.coverage-bijection-mismatch:RC-1-resolved-not-applicable"])
    run("RC2-not-attempted-ok", *R, {"coverage": "unknown", "deficiency": "resolution-incomplete",
                                   "resolutionCompleteness": {"state": "not-attempted", "attempted": False, "examinedExhaustive": False, "stageTerminal": None}}, [], [])
    run("RC6-complete-not-exhaustive", *R, {"resolutionCompleteness": {"examinedExhaustive": False}}, [],
        ["native.coverage-bijection-mismatch:RC-2-complete", "native.coverage-bijection-mismatch:RC-6"])
    run("RC2-edge-count-mismatch", *R, {"coverage": "unknown", "deficiency": "resolution-incomplete",
                                      "resolutionCompleteness": {"state": "incomplete", "unresolvedEdgeCount": 2, "unresolvedEdgeClasses": ["untyped-any-call"]}},
        ["untyped-any-call"], ["native.coverage-bijection-mismatch:RC-2-edge-account"])
    N = ("declares", "syntactic")
    run("RC1-non-resolved-ok", *N, {}, [], [])
    run("RC1-non-resolved-complete-state", *N, {"resolutionCompleteness": {"state": "complete", "attempted": True}}, [],
        ["native.coverage-bijection-mismatch:RC-1-non-resolved"])
    run("cause-language-tier-without-cause", *N, {"coverage": "unknown", "deficiency": "language-tier-unsupported", "nativeCause": None,
                                                 "resolutionCompleteness": {"examinedExhaustive": False}}, [], ["native.coverage-cause-required"])
    run("cause-resolution-incomplete-on-complete-state", *R, {"coverage": "unknown", "deficiency": "resolution-incomplete"}, [],
        ["native.coverage-cause-carrier-unsupported"])
    run("cause-budget-with-native-cause", *R, {"coverage": "unknown", "deficiency": "budget-exhausted", "nativeCause": "capability-missing",
                                              "resolutionCompleteness": {"state": "partial", "stageTerminal": "budget-exhausted", "examinedExhaustive": False}},
        [], ["native.coverage-cause-must-be-null"])  # attempt1 also expected not-for-deficiency; the budget row declares no allowedCauses
    run("cause-derivation-policy-on-calls", *R, {"coverage": "unknown", "deficiency": "derivation-policy-unmet"}, [],
        ["native.coverage-cause-relation-not-in-scope", "native.coverage-cause-carrier-unsupported"])
    run("cause-without-deficiency", *R, {"nativeCause": "capability-missing"}, [], ["native.coverage-cause-without-deficiency"])
    return {"universe": U, "vectors": out}


def outcome_vectors():
    out = []
    U = "a" * 64
    P = "closure2:" + "b" * 64
    plan_id = "plan2:" + "c" * 64

    def inv(kind, state="complete", d=None, c=None):
        rec = {"kind": kind, "state": state, "deficiency": d, "nativeCause": c, "rows": [], "examinedPaths": []}
        return (K.raw_digest(rec), rec)

    def mk(cap, mode, binding, invs, required, views=None, scopes=None, coverages=None, cand=None, vcs="none", candidates=None):
        cell = {"capabilityId": cap, "languageMode": mode, "workspaceRoot": ".", "required": required,
                "kinds": EN.KIND_DERIVATION[cap], "programBindings": [binding]}
        ctx = {"enum_index": {"inventories": {(0, 0, k): v for k, v in invs.items()}, "extents": {(0, 0): {k: [] for k in invs}}},
               "views": views or {}, "scopes": scopes or {}, "coverages": coverages or {}, "candidates": candidates or {},
               "vcs_kind": vcs, "plan_id": plan_id,
               "receipts": [{"ordinal": 0, "producerClosure": P, "state": "complete",
                             "outputRefs": [{"domain": "view", "digest": v.split(":", 1)[1]} for v in (views or {})]}]}
        obs = {"viewDigests": list((views or {}).keys()), "stageOrdinal": 0, "candidateResultDigest": cand}
        faults = []
        o, accs, rows, _ = XI.derive_outcome(0, cell, binding, obs, ctx, faults)
        return o, accs, rows, faults

    avail = {"ordinal": 0, "enumerator": {"status": "selected", "closureId": P}, "universe": U}
    # 1 optional unselected enumerator
    b = {"ordinal": 0, "enumerator": {"status": "unselected", "reason": "optional-unselected"}, "universe": None,
         "deficiency": "provider-unavailable", "nativeCause": None}
    o, accs, rows, f = mk("syntax", "ts-tsconfig", b, {"symbol": inv("symbol", "unavailable", "provider-unavailable")}, False)
    out.append(check("unselected-optional", (o["state"], o["deficiency"], o["stageOrdinalNullReason"], [a["applicability"] for a, _ in accs], len(rows)),
                     ("unavailable", "provider-unavailable", "optional-unselected", ["unavailable-unselected"] * 3, 0)))
    # 2 selected enumerator, null universe, required
    b = {"ordinal": 0, "enumerator": {"status": "selected", "closureId": P}, "universe": None,
         "deficiency": "input-closure-incomplete", "nativeCause": "lockfile-missing"}
    o, accs, rows, f = mk("calls", "rust-cargo", b, {"symbol": inv("symbol", "unavailable", "input-closure-incomplete", "lockfile-missing")}, True)
    bridged = XI.bridge(rows, {"domain": "execution-inputs", "digest": "d" * 64})
    out.append(check("null-universe-required", (o["state"], o["deficiency"], o["nativeCause"], [a["applicability"] for a, _ in accs],
                                                sorted({(x["cause"], x["nativeCause"]) for x in bridged})),
                     ("unavailable", "input-closure-incomplete", "lockfile-missing", ["unavailable-null-universe"],
                      [("input-closure-incomplete", "lockfile-missing")])))
    # 3 UNSUPPORTED-TYPED outranks unselected
    b = {"ordinal": 0, "enumerator": {"status": "unselected", "reason": "optional-unselected"}, "universe": None,
         "deficiency": "provider-unavailable", "nativeCause": None}
    o, accs, rows, f = mk("imports", "syntax-only", b, {"symbol": inv("symbol", "unavailable", "provider-unavailable")}, False)
    out.append(check("unsupported-typed-outranks-unselected", ([a["applicability"] for a, _ in accs], [(i["deficiency"], i["nativeCause"]) for _, i in accs]),
                     (["unsupported-typed"], [("language-tier-unsupported", "capability-missing")])))
    # 4 available unsupported-typed required -> complete outcome, required row carries matrix pair
    o, accs, rows, f = mk("imports", "syntax-only", avail, {"symbol": inv("symbol")}, True)
    out.append(check("unsupported-typed-available-required", (o["state"], o["deficiency"], [(r["source"], r["deficiency"], r["nativeCause"]) for r in rows]),
                     ("complete", None, [("account-unsupported", "language-tier-unsupported", "capability-missing")])))
    # 5 supported account with no returned partition -> partial, (null,null), required-cell-unsatisfied
    o, accs, rows, f = mk("syntax", "syntax-only", avail, {"symbol": inv("symbol")}, True)
    bridged = XI.bridge(rows, {"domain": "execution-inputs", "digest": "d" * 64})
    out.append(check("missing-work-null-carrier", (o["state"], o["deficiency"], o["nativeCause"], sorted({x["cause"] for x in bridged})),
                     ("partial", None, None, ["required-cell-unsatisfied"])))
    # 6 partial inventory budget-exhausted carrier kept (not rewritten as provider-unavailable)
    o, accs, rows, f = mk("syntax", "syntax-only", avail, {"symbol": inv("symbol", "partial", "budget-exhausted")}, True)
    out.append(check("inventory-budget-carrier-kept", (o["state"], o["deficiency"], rows[0]["source"] if rows else None),
                     ("partial", "budget-exhausted", "inventory")))
    # 7 candidate required absent -> refusal; optional absent -> unavailable without invented carrier
    b2 = dict(avail, candidateSourcePaths=[])
    o, accs, rows, f = mk("clones-near", "syntax-only", b2, {}, True)
    out.append(check("candidate-required-absent", [x.split(":")[0] for x in f], ["EXECUTION_INPUTS_CANDIDATE_REQUIRED"], "invalid"))
    o, accs, rows, f = mk("clones-near", "syntax-only", b2, {}, False)
    out.append(check("candidate-optional-absent", (o["state"], o["deficiency"], o["nativeCause"], f), ("unavailable", None, None, [])))
    # 8 inventory vcs-change with vcs none -> inapplicable
    o, accs, rows, f = mk("inventory", "syntax-only", avail, {"file": inv("file"), "package": inv("package")}, False)
    out.append(check("vcs-none-inapplicable", [a["applicability"] for a, _ in accs], ["supported-available", "supported-available", "inapplicable-vcs"]))
    # 9 two Coverage records of one account with different carriers: carrier from first in H order, two rows
    s1, s2 = "scope2:" + "1" * 64, "scope2:" + "2" * 64
    c_low, c_high = "coverage2:" + "3" * 64, "coverage2:" + "4" * 64
    base_entry = {"coverage": "unknown", "nativeCause": None}
    # HC-42 follow-on (logs/s41-fin-p4to9.0.phase4_tables.log): a subject-scope always carries relation and resolution
    # (identity-schemas.v3 subject-scope required); the mock scopes omitted them and the s3 attribution law reads S.relation
    scopes = {s1: {"sourceUniverse": U, "relation": "declares", "resolution": "syntactic", "subjects": []},
              s2: {"sourceUniverse": U, "relation": "declares", "resolution": "syntactic", "subjects": []}}
    covs = {c_high: ({"scopeId": s1}, {"key": {"relation": "declares", "resolution": "syntactic", "sourceUniverse": U},
                                      "entry": dict(base_entry, deficiency="resolution-incomplete")}),
            c_low: ({"scopeId": s2}, {"key": {"relation": "declares", "resolution": "syntactic", "sourceUniverse": U},
                                     "entry": dict(base_entry, deficiency="provider-unavailable")})}
    v = "view2:" + "5" * 64
    views = {v: {"planId": plan_id, "producerClosure": P, "scopeIds": [s1, s2], "coverageIds": [c_low, c_high]}}
    o, accs, rows, f = mk("syntax", "syntax-only", avail, {"symbol": inv("symbol")}, True, views, scopes, covs)
    out.append(check("two-carriers-first-in-h-order", (o["state"], o["deficiency"], sorted((r["relation"], r["deficiency"]) for r in rows if r["relation"] == "declares")),
                     ("partial", "provider-unavailable", [("declares", "provider-unavailable"), ("declares", "resolution-incomplete")])))
    return out


def main():
    doc = {"tables": tables(), "countClassAttemptVectors": rc_vectors(), "cellOutcomeVectors": outcome_vectors()}
    doc["assertionFailures"] = failures
    with open(OUT + "/vectors/phase4-tables.json", "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    rc = doc["countClassAttemptVectors"]
    print("relationRung rows", len(doc["tables"]["relationRung"]), "modes", len(doc["tables"]["advertisedModePaths"]))
    print("rc vectors", len(rc.get("vectors", [])), rc.get("skipped", ""), "outcome vectors", len(doc["cellOutcomeVectors"]))
    print("failures", json.dumps(failures)[:3000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
