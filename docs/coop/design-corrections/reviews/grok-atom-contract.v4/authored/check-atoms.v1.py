"""Discriminating atom-model checks. Not full Run replay. Not product execution."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
import importlib.util

spec = importlib.util.spec_from_file_location("atom_model_v1", HERE / "atom_model.v1.py")
AM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(AM)

U1 = "11" * 32
U2 = "22" * 32
UR = "33" * 32
TS = "native.semantic-universe.typescript.v2"
RS = "native.semantic-universe.rust.v2"
C_PROV = "closure2:" + "aa" * 32
C_EVAL = "closure2:" + "bb" * 32
PLAN = "plan2:" + "cc" * 32


def H(ch: str) -> str:
    return ch * 64


def fact2(ch: str) -> str:
    return "fact2:" + H(ch)


def imp2(ch: str) -> str:
    return "import2:" + H(ch)


def cov2(ch: str) -> str:
    return "coverage2:" + H(ch)


def scope2(ch: str) -> str:
    return "scope2:" + H(ch)


def fail(msg: str) -> None:
    raise AssertionError(msg)


def expect_value(r, v, label):
    if r["value"] != v:
        fail(f"{label}: value {r['value']!r} != {v!r} causes={r.get('causes')}")


def expect_admit(fn, key, label):
    try:
        fn()
    except AM.AtomAdmissionError as e:
        if e.key != key:
            fail(f"{label}: key {e.key!r} != {key!r}")
        return
    fail(f"{label}: expected admission {key}")


def plan_one(universe=U1, cap="references", mode="ts-tsconfig", kinds=None):
    kinds = kinds or ["symbol"]
    return {
        "schemaVersion": 1,
        "snapshotId": "snapshot2:" + H("s"),
        "scopeDigest": H("o"),
        "membershipDigest": H("m"),
        "cells": [{
            "capabilityId": cap,
            "languageMode": mode,
            "workspaceRoot": ".",
            "required": True,
            "kinds": kinds,
            "programBindings": [{
                "ordinal": 0,
                "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": C_PROV},
                "nativeContextDigest": H("n"),
                "universe": universe,
                "programEntry": None,
                "extents": [{"kind": k, "paths": ["src/a.ts"]} for k in kinds],
            }],
        }],
    }


def inv_symbol(universe=U1, nid="ts-symbol:src/a.ts#f", path="src/a.ts", qn="f", exported="exported"):
    return {
        "schemaVersion": 1,
        "planId": PLAN,
        "parameterDigest": H("p"),
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "symbol",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": nid,
            "kind": "symbol",
            "path": path,
            "qualifiedName": qn,
            "subjectLanguage": "typescript",
            "exported": exported,
            "signatureTokens": ["f"],
            "projections": [],
        }],
        "universe": universe,
    }


def inv_file(universe=U1, path="src/a.ts"):
    return {
        "schemaVersion": 1,
        "planId": PLAN,
        "parameterDigest": H("p"),
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "file",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": path,
            "kind": "file",
            "path": path,
            "qualifiedName": path,
            "subjectLanguage": "typescript",
            "signatureTokens": [],
            "projections": [],
        }],
        "universe": universe,
    }


def coverage(rel, rung, src, tgt, state="not-applicable", cov="complete", cid="1"):
    return cov2(cid), {
        "schemaVersion": 3,
        "key": {
            "relation": rel,
            "resolution": rung,
            "sourceUniverse": src,
            "targetUniverse": tgt,
            "subjectScopeCommitment": "sha256:" + H("k"),
        },
        "entry": {
            "relation": rel,
            "resolution": rung,
            "coverage": cov,
            "examinedUniverse": {"subjectScopeCommitment": "sha256:" + H("k"), "subjectCount": 1},
            "resolutionCompleteness": {
                "state": state, "attempted": state not in ("not-applicable", "not-attempted"),
                "examinedExhaustive": cov == "complete",
                "stageTerminal": "complete",
                "unresolvedEdgeCount": 0 if state != "incomplete" else 1,
                "unresolvedEdgeClasses": [] if state != "incomplete" else ["computed-member-access"],
            },
            "closedWorld": {"exportsClosed": "closed", "entryPointsRecognized": "all",
                            "nonliteralLoading": "none", "externalConsumers": "none-declared",
                            "dynamicDispatch": "not-applicable", "reasons": [],
                            "deadCodeRepairEligible": True},
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": None,
            "nativeCause": None,
        },
    }


def scope(rel, rung, src, tgt, subjects, sid="1"):
    return scope2(sid), {
        "scopeId": scope2(sid),
        "relation": rel,
        "resolution": rung,
        "sourceUniverse": src,
        "targetUniverse": tgt,
        "subjects": subjects,
    }


def base_inputs(**extra):
    d = {
        "facts": {},
        "scopes": {},
        "coverages": {},
        "enumerationPlan": plan_one(),
        "inventories": [inv_symbol()],
        "targetAttributions": {},
        "closures": {C_PROV: {"kind": "provider"}, C_EVAL: {"kind": "evaluator"}},
        "universeDomains": {U1: TS, U2: TS, UR: RS},
        "imports": {},
        "importPayloads": {},
        "importObservations": {},
        "planSelectedImportIds": [],
        "evaluationInputRefs": [],
        "incomingSearchAttestations": [],
    }
    d.update(extra)
    return d


def test_known_hit_partial_none_false():
    iid = imp2("r")
    inputs = base_inputs(
        planSelectedImportIds=[iid, imp2("q")],
        evaluationInputRefs=[iid, imp2("q")],
        imports={
            iid: {"kind": "runtime", "completeness": "complete", "consumable": True, "staleness": "current",
                  "scope": {"pathPrefixes": ["src"]}},
            imp2("q"): {"kind": "runtime", "completeness": "partial", "consumable": True, "staleness": "current",
                        "scope": {"pathPrefixes": ["src"]}},
        },
        importPayloads={
            iid: {"subjects": [{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}]},
            imp2("q"): {"subjects": []},
        },
        importObservations={
            iid: {"window": {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"},
                  "population": "test-suite", "selection": None, "revisionRange": None},
            imp2("q"): {"window": {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"},
                        "population": "test-suite", "selection": None, "revisionRange": None},
        },
        inventories=[inv_symbol()],
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "none", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "false", "known-hit-partial-none")
    if not r["knownObservationAddresses"]:
        fail("known-hit-partial-none: missing known addresses")


def test_missing_runtime_observable_unknown():
    iid = imp2("r")
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: {"kind": "runtime", "completeness": "complete", "consumable": True, "staleness": "current",
                       "scope": {"pathPrefixes": ["src"]}}},
        importPayloads={iid: {"subjects": [{"path": "src/a.ts", "symbol": "f", "observability": "unobservable"}]}},
        importObservations={iid: {"window": {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"},
                                  "population": "test-suite", "selection": None, "revisionRange": None}},
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "none", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "unobservable-none")
    codes = {c["code"] for c in r["causes"]}
    if "unobservable-subject" not in codes:
        fail(f"unobservable-none causes {codes}")


def test_history_empty_complete_all_paths_covered():
    iid = imp2("h")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: {"kind": "history", "completeness": "complete", "consumable": True, "staleness": "current",
                       "scope": {"pathPrefixes": ["src"]}}},
        importPayloads={iid: {"collectionScope": "all-paths", "subjects": [],
                              "revisionRange": {"from": "a" * 40, "to": "b" * 40, "commitCount": 3, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": "a" * 40, "to": "b" * 40}}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "all-covered", "relation": "history-change", "minResolution": "observed",
            "filters": [], "evidence": "history"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "history-empty-all-paths")


def test_scope_s_to_v_does_not_omit_incoming_s_for_u():
    """S has a scope/coverage targeting V, not U. Incoming none for U must not invent (S,U);
    without attestation it is unknown (owed S still considered)."""
    cid, cov = coverage("references", "resolved-binding", U1, U2, state="complete", cid="c")
    sid, sc = scope("references", "resolved-binding", U1, U2, ["ts-symbol:src/a.ts#g"], sid="s")
    fid = fact2("1")
    inputs = base_inputs(
        facts={fid: {
            "factId": fid, "relation": "references", "resolution": "resolved-binding",
            "sourceUniverse": U1, "targetUniverse": U2,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"referrer": "ts-symbol:src/a.ts#g", "name": "f",
                        "resolvedBinding": "ts-symbol:src/a.ts#f"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("x"), "startByte": 0, "endByte": 1}],
        }},
        coverages={cid: cov},
        scopes={sid: sc},
        inventories=[inv_symbol(), inv_symbol(nid="ts-symbol:src/a.ts#g", qn="g")],
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "incoming-no-cartesian")
    codes = {c["code"] for c in r["causes"]}
    if "source-target-search-unattested" not in codes:
        fail(f"incoming-no-cartesian causes {codes}")
    # fact target is U2 not U1 so it is not a match for E in U1
    if r["knownFactIds"]:
        fail("incoming-no-cartesian: fact to V must not match U")


def test_source_kind_vs_incoming_target_kind():
    fid = fact2("1")
    cid, cov = coverage("imports", "resolved-target", U1, U1, state="complete", cid="c")
    sid, sc = scope("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], sid="s")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a",
                        "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("x"), "startByte": 0, "endByte": 1}],
        }},
        coverages={cid: cov},
        scopes={sid: sc},
        inventories=[inv_symbol(), inv_file()],
        incomingSearchAttestations=[{
            "schemaVersion": 1, "sourceUniverse": U1, "targetUniverse": U1,
            "relation": "imports", "minResolution": "resolved-target",
            "examinedExhaustive": True, "coverage": "complete",
            "resolutionCompleteness": {"state": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
            "closedWorld": {"exportsClosed": "closed"},
        }],
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target",
            "filters": [{"field": "subjectKind", "cmp": "eq", "value": "symbol"}]}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "incoming-subjectKind-source")
    atom2 = dict(atom)
    atom2["filters"] = [{"field": "subjectKind", "cmp": "eq", "value": "file"}]
    r2 = AM.evaluate_atom(atom2, subj, inputs)
    # source importer is symbol, not file; eq file is nomatch => exists false if complete, or unknown
    if r2["value"] == "true":
        fail("incoming-subjectKind-file must not match source symbol")


def test_equal_native_id_different_universe():
    fid = fact2("1")
    inputs = base_inputs(
        facts={fid: {
            "factId": fid, "relation": "file", "resolution": "enumerated",
            "sourceUniverse": U2, "targetUniverse": U2,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"path": "src/a.ts", "contentSha256": H("c"), "byteLength": 1},
            "anchors": [],
        }},
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file(U1), inv_file(U2)],
    )
    # add U2 binding
    inputs["enumerationPlan"]["cells"].append({
        "capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg",
        "required": True, "kinds": ["file"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV},
            "nativeContextDigest": H("n"), "universe": U2, "programEntry": "tsconfig.json",
            "extents": [{"kind": "file", "paths": ["src/a.ts"]}],
        }],
    })
    cid, cov = coverage("file", "enumerated", U1, U1, cid="a")
    sid, sc = scope("file", "enumerated", U1, U1, ["src/a.ts"], sid="a")
    inputs["coverages"][cid] = cov
    inputs["scopes"][sid] = sc
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "false", "cross-universe-id")
    if r["knownFactIds"]:
        fail("cross-universe-id matched U2 fact")


def test_two_cap_identical_inventory_lookup():
    fid = fact2("1")
    inv1 = inv_symbol()
    inv2 = inv_symbol()
    inv2["cellOrdinal"] = 1
    plan = plan_one(cap="imports")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": ".",
        "required": True, "kinds": ["symbol"],
        "programBindings": [plan["cells"][0]["programBindings"][0]],
    })
    cid, cov = coverage("imports", "resolved-target", U1, U1, state="complete", cid="c")
    inputs = base_inputs(
        enumerationPlan=plan,
        inventories=[inv1, inv2, inv_file()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("x"), "startByte": 0, "endByte": 1}],
        }},
        coverages={cid: cov},
        incomingSearchAttestations=[{
            "schemaVersion": 1, "sourceUniverse": U1, "targetUniverse": U1,
            "relation": "imports", "minResolution": "resolved-target",
            "examinedExhaustive": True, "coverage": "complete",
            "resolutionCompleteness": {"state": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
        }],
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "two-cap-lookup")


def test_conflict_sidecar():
    fid = fact2("1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports"),
        inventories=[inv_file(), inv_symbol()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("x"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: {
            "schemaVersion": 1, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_PROV,
            "targetUniverse": U1, "targetNativeId": "src/a.ts",
            "kind": "symbol", "occupancy": "first-party", "exported": "exported", "logicalPath": None,
        }},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target", "filters": []}

    def go():
        AM.evaluate_atom(atom, subj, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT", "sidecar-kind")

    inputs2 = dict(inputs)
    inputs2["targetAttributions"] = {fid: {
        "schemaVersion": 1, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_PROV,
        "targetUniverse": U1, "targetNativeId": "src/a.ts",
        "kind": "file", "occupancy": "external", "exported": None, "logicalPath": None,
    }}
    def go2():
        AM.evaluate_atom(atom, subj, inputs2)
    expect_admit(go2, "TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY", "sidecar-external")

    inputs3 = dict(inputs)
    facts3 = dict(inputs["facts"])
    f3 = dict(facts3[fid])
    f3["producerClosure"] = C_EVAL
    facts3[fid] = f3
    inputs3["facts"] = facts3
    inputs3["targetAttributions"] = {fid: {
        "schemaVersion": 1, "planId": PLAN, "sourceFactId": fid, "producerClosure": C_EVAL,
        "targetUniverse": U1, "targetNativeId": "src/a.ts",
        "kind": "unknown", "occupancy": "unknown", "exported": None, "logicalPath": None,
    }}
    def go3():
        AM.evaluate_atom(atom, subj, inputs3)
    expect_admit(go3, "TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER", "sidecar-evaluator")


def test_all_covered_na_and_resolved_partial():
    cid, cov = coverage("file", "enumerated", U1, U1, state="not-applicable", cid="f")
    sid, sc = scope("file", "enumerated", U1, U1, ["src/a.ts"], sid="f")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        coverages={cid: cov},
        scopes={sid: sc},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "all-covered", "relation": "file", "minResolution": "enumerated", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "all-covered-na")

    cid2, cov2 = coverage("references", "resolved-binding", U1, U1, state="incomplete", cid="r")
    sid2, sc2 = scope("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], sid="r")
    inputs2 = base_inputs(
        coverages={cid2: cov2},
        scopes={sid2: sc2},
        incomingSearchAttestations=[{
            "schemaVersion": 1, "sourceUniverse": U1, "targetUniverse": U1,
            "relation": "references", "minResolution": "resolved-binding",
            "examinedExhaustive": True, "coverage": "complete",
            "resolutionCompleteness": {"state": "incomplete", "unresolvedEdgeCount": 1,
                                       "unresolvedEdgeClasses": ["computed-member-access"]},
        }],
    )
    atom2 = {"op": "all-covered", "relation": "references", "minResolution": "resolved-binding",
             "endpoint": "source", "filters": []}
    subj2 = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    r2 = AM.evaluate_atom(atom2, subj2, inputs2)
    expect_value(r2, "indeterminate", "all-covered-resolved-partial")
    if "resolution-incomplete" not in r2["nativeDeficiencies"]:
        fail(f"all-covered-resolved-partial defs {r2['nativeDeficiencies']}")


def test_wrong_enum_neq():
    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "file", "minResolution": "enumerated",
             "filters": [{"field": "subjectKind", "cmp": "neq", "value": "export"}]},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
            base_inputs(enumerationPlan=plan_one(cap="inventory", kinds=["file"]), inventories=[inv_file()]),
        )
    expect_admit(go, "ATOM_FILTER_ENUM_LITERAL_UNKNOWN", "enum-neq-export")

    def go2():
        AM.evaluate_atom(
            {"op": "exists", "relation": "file", "minResolution": "enumerated",
             "filters": [{"field": "universe", "cmp": "eq", "value": U1}]},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
            base_inputs(enumerationPlan=plan_one(cap="inventory", kinds=["file"]), inventories=[inv_file()]),
        )
    expect_admit(go2, "ATOM_FILTER_ENUM_LITERAL_UNKNOWN", "universe-hex")


def test_universe_neq_different_valid_domain():
    cid, cov = coverage("file", "enumerated", U1, U1, cid="f")
    sid, sc = scope("file", "enumerated", U1, U1, ["src/a.ts"], sid="f")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        coverages={cid: cov},
        scopes={sid: sc},
        facts={fact2("1"): {
            "factId": fact2("1"), "relation": "file", "resolution": "enumerated",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"path": "src/a.ts", "contentSha256": H("c"), "byteLength": 1},
            "anchors": [],
        }},
    )
    atom = {"op": "exists", "relation": "file", "minResolution": "enumerated",
            "filters": [{"field": "universe", "cmp": "neq", "value": RS}]}
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "universe-neq-other-domain")


def test_tests_exit1_empty():
    iid = imp2("t")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: {"kind": "test", "completeness": "complete", "consumable": True, "staleness": "current",
                       "scope": {"pathPrefixes": ["src"]}}},
        importPayloads={iid: {
            "producer": "host-test-execution", "exitStatus": 1, "signal": None, "timedOut": False,
            "tests": [], "selection": {"mode": "full", "completenessEstablished": True},
        }},
        importObservations={iid: {"window": None, "population": None,
                                  "selection": {"mode": "full", "completenessEstablished": True},
                                  "revisionRange": None}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "test-execution", "minResolution": "observed",
            "filters": [{"field": "testResult", "cmp": "eq", "value": "failed"},
                        {"field": "exitStatus", "cmp": "eq", "value": 1}],
            "evidence": "test"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "test-exit1-empty")


def test_optional_unknown_disclosure():
    """Zero owed wrappers: unknown with evidence-kind-unavailable; gating is root, not atom-local."""
    inputs = base_inputs(planSelectedImportIds=[], evaluationInputRefs=[])
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "optional-unknown")
    codes = {c["code"] for c in r["causes"]}
    if "zero-owed-wrappers" not in codes and "evidence-kind-unavailable" not in codes:
        fail(f"optional-unknown causes {codes}")
    if "gating" in r:
        fail("atom must not decide gating")


def test_known_count_gt_n_partial():
    iid = imp2("r")
    qid = imp2("q")
    inputs = base_inputs(
        planSelectedImportIds=[iid, qid],
        evaluationInputRefs=[iid, qid],
        imports={
            iid: {"kind": "runtime", "completeness": "complete", "consumable": True, "staleness": "current",
                  "scope": {"pathPrefixes": ["src"]}},
            qid: {"kind": "runtime", "completeness": "partial", "consumable": True, "staleness": "current",
                  "scope": {"pathPrefixes": ["src"]}},
        },
        importPayloads={
            iid: {"subjects": [
                {"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 3},
            ]},
            qid: {"subjects": []},
        },
        importObservations={
            iid: {"window": {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"},
                  "population": "test-suite", "selection": None, "revisionRange": None},
            qid: {"window": {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"},
                  "population": "test-suite", "selection": None, "revisionRange": None},
        },
    )
    # two distinct addresses: add second complete wrapper with a hit
    wid = imp2("w")
    inputs["planSelectedImportIds"].append(wid)
    inputs["evaluationInputRefs"].append(wid)
    inputs["imports"][wid] = {"kind": "runtime", "completeness": "complete", "consumable": True,
                              "staleness": "current", "scope": {"pathPrefixes": ["src"]}}
    inputs["importPayloads"][wid] = {"subjects": [
        {"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1},
    ]}
    inputs["importObservations"][wid] = inputs["importObservations"][iid]
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "count-at-most", "n": 1, "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "false", "count-gt-n-partial")
    if len(r["knownObservationAddresses"]) < 2:
        fail("count-gt-n-partial: expected two known addresses")


def test_listed_paths_missing_not_vacuous():
    iid = imp2("h")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: {"kind": "history", "completeness": "complete", "consumable": True, "staleness": "current",
                       "scope": {"pathPrefixes": ["src"]}}},
        importPayloads={iid: {"collectionScope": "listed-paths", "subjects": [{"path": "src/other.ts",
                                                                              "changeCount": 1,
                                                                              "lastChangedCommit": "a" * 40}],
                              "revisionRange": {"from": None, "to": "b" * 40, "commitCount": 1, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": None, "to": "b" * 40}}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "none", "relation": "history-change", "minResolution": "observed",
            "filters": [], "evidence": "history"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "listed-paths-missing")
    codes = {c["code"] for c in r["causes"]}
    if "history-outside-collection-scope" not in codes:
        fail(f"listed-paths-missing causes {codes}")


def test_oracle_refused():
    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
            {**base_inputs(), "expectedValue": "true"},
        )
    expect_admit(go, "ATOM_ORACLE_FLAG_REFUSED", "oracle")


CASES = [
    test_known_hit_partial_none_false,
    test_missing_runtime_observable_unknown,
    test_history_empty_complete_all_paths_covered,
    test_scope_s_to_v_does_not_omit_incoming_s_for_u,
    test_source_kind_vs_incoming_target_kind,
    test_equal_native_id_different_universe,
    test_two_cap_identical_inventory_lookup,
    test_conflict_sidecar,
    test_all_covered_na_and_resolved_partial,
    test_wrong_enum_neq,
    test_universe_neq_different_valid_domain,
    test_tests_exit1_empty,
    test_optional_unknown_disclosure,
    test_known_count_gt_n_partial,
    test_listed_paths_missing_not_vacuous,
    test_oracle_refused,
]


def main() -> int:
    results = []
    for fn in CASES:
        try:
            fn()
            results.append({"case": fn.__name__, "ok": True})
        except Exception as exc:  # noqa: BLE001 — collect
            results.append({"case": fn.__name__, "ok": False, "error": f"{type(exc).__name__}: {exc}"})
    ok = all(r["ok"] for r in results)
    report = {
        "standing": "atom unit checks; not full Run replay",
        "ok": ok,
        "passed": sum(1 for r in results if r["ok"]),
        "failed": sum(1 for r in results if not r["ok"]),
        "results": results,
    }
    out_dir = Path("/tmp/opensip-design-corrections/grok-atom-contract.v4")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "check-atoms.report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
