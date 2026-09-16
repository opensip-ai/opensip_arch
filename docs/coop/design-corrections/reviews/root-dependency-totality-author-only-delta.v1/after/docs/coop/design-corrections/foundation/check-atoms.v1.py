"""Discriminating atom-model checks. Not full Run replay. Not product execution."""
from __future__ import annotations

import argparse
import copy
import hashlib
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
C_PROV2 = "closure2:" + "ee" * 32
C_EVAL = "closure2:" + "bb" * 32
PLAN = "plan2:" + "cc" * 32
SNAP = "snapshot2:" + "aa" * 32
IMPORT_SCOPE = {
    "schemaVersion": 2,
    "workspaceRoots": ["."],
    "pathPrefixes": ["src"],
    "excludedPathPrefixes": [],
}
WINDOW = {"startUtc": "2020-01-01T00:00:00Z", "endUtc": "2020-01-02T00:00:00Z"}


def rt_payload(subjects, window=None, pop="test-suite"):
    return {"subjects": subjects, "observationWindow": window or dict(WINDOW), "observedPopulation": pop}


def rt_obs(window=None, pop="test-suite"):
    return {"window": window or dict(WINDOW), "population": pop, "selection": None, "revisionRange": None}
CW_CLOSED = {
    "exportsClosed": "closed", "entryPointsRecognized": "all",
    "nonliteralLoading": "none", "externalConsumers": "none-declared",
    "dynamicDispatch": "not-applicable", "reasons": [],
    "deadCodeRepairEligible": True,
}
RESOLVED = {"resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"}


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


def rc_for(rung, state=None, cov="complete"):
    resolved = rung in RESOLVED
    if state is None:
        state = "complete" if resolved else "not-applicable"
    if not resolved:
        return {
            "state": "not-applicable", "attempted": False,
            "examinedExhaustive": cov == "complete",
            "stageTerminal": "complete", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
        }
    return {
        "state": state, "attempted": state not in ("not-applicable", "not-attempted"),
        "examinedExhaustive": cov == "complete",
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0 if state != "incomplete" else 1,
        "unresolvedEdgeClasses": [] if state != "incomplete" else ["computed-member-access"],
    }


def inv_c_digest(inv: dict) -> str:
    rec = {k: inv[k] for k in AM.INVENTORY_C_FIELDS if k in inv}
    return hashlib.sha256(AM.C.canonical(rec)).hexdigest()


def plan_one(universe=U1, cap="references", mode="ts-tsconfig", kinds=None):
    kinds = kinds or ["symbol"]
    return {
        "schemaVersion": 1,
        "snapshotId": SNAP,
        "scopeDigest": H("0"),
        "membershipDigest": H("0"),
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
                "nativeContextDigest": H("0"),
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
        "parameterDigest": H("0"),
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
        "parameterDigest": H("0"),
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


def inv_package(universe=U1, name="dup", path="pkg-a/package.json"):
    return {
        "schemaVersion": 1,
        "planId": PLAN,
        "parameterDigest": H("0"),
        "cellOrdinal": 0,
        "programOrdinal": 0,
        "kind": "package",
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": [path],
        "rows": [{
            "nativeSubjectId": name,
            "kind": "package",
            "path": path,
            "qualifiedName": name,
            "subjectLanguage": "json",
            "signatureTokens": [],
            "projections": [],
        }],
        "universe": universe,
    }


def coverage(rel, rung, src, tgt, state=None, cov="complete", cid="1"):
    if state is None:
        state = "complete" if rung in RESOLVED else "not-applicable"
    return cov2(cid), {
        "schemaVersion": 3,
        "key": {
            "relation": rel,
            "resolution": rung,
            "sourceUniverse": src,
            "targetUniverse": tgt,
            "subjectScopeCommitment": "sha256:" + H("0"),
        },
        "entry": {
            "relation": rel,
            "resolution": rung,
            "coverage": cov,
            "examinedUniverse": {"subjectScopeCommitment": "sha256:" + H("0"), "subjectCount": 1},
            "resolutionCompleteness": rc_for(rung, state, cov),
            "closedWorld": dict(CW_CLOSED),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": None,
            "nativeCause": None,
        },
    }


def scope(rel, rung, src, tgt, subjects, sid="1"):
    return scope2(sid), {
        "schemaVersion": 2,
        "snapshotId": SNAP,
        "sourceUniverse": src,
        "targetUniverse": tgt,
        "relation": rel,
        "resolution": rung,
        "enumeratorClosure": C_PROV,
        "subjects": sorted(subjects, key=AM.C.canonical),
    }


def paired(rel, rung, src, tgt, subjects, tag="1", state=None, cov="complete"):
    sid, sc = scope(rel, rung, src, tgt, subjects, sid=tag)
    cid, covr = coverage(rel, rung, src, tgt, state=state, cov=cov, cid=tag)
    return sid, sc, cid, covr


def wrap(kind, completeness="complete", **extra):
    w = {
        "kind": kind, "completeness": completeness, "consumable": True, "staleness": "current",
        "scope": dict(IMPORT_SCOPE), "scopeDigest": H("0"),
    }
    w.update(extra)
    return w


def sidecar(fid, native, kind="file", occupancy="first-party", exported=None, logical=None, manifest=None,
            producer=C_PROV, universe=U1, evaluation=None):
    if occupancy == "first-party" and evaluation is None:
        evaluation = native if kind == "symbol" else None
    if occupancy != "first-party":
        evaluation = None if evaluation is None else evaluation
    return {
        "schemaVersion": 2, "planId": PLAN, "sourceFactId": fid, "producerClosure": producer,
        "targetUniverse": universe, "targetNativeId": native,
        "kind": kind, "occupancy": occupancy, "exported": exported, "logicalPath": logical,
        "packageManifestPath": manifest, "evaluationNativeId": evaluation,
    }


def incoming_att(rel, rung, src, tgt, scope_ids, inventories, **over):
    att = {
        "schemaVersion": 1, "planId": PLAN, "providerClosure": C_PROV,
        "sourceUniverse": src, "targetUniverse": tgt, "relation": rel,
        "minResolution": rung, "scopeRefs": sorted(scope_ids),
        "expectedInventoryRefs": sorted({inv_c_digest(i) for i in inventories}),
        "completeSearch": True, "examinedExhaustive": True, "coverage": "complete",
        "resolutionCompleteness": rc_for(rung, cov="complete"),
        "closedWorld": dict(CW_CLOSED),
    }
    att.update(over)
    return att


def base_inputs(**extra):
    d = {
        "facts": {},
        "scopes": {},
        "coverages": {},
        "coverageScopes": {},
        "enumerationPlan": plan_one(),
        "inventories": [inv_symbol()],
        "targetAttributions": {},
        "closures": {C_PROV: {"kind": "provider"}, C_PROV2: {"kind": "provider"}, C_EVAL: {"kind": "evaluator"}},
        "universeDomains": {U1: TS, U2: TS, UR: RS},
        "imports": {},
        "importPayloads": {},
        "importObservations": {},
        "planSelectedImportIds": [],
        "evaluationInputRefs": [],
        "incomingSearchAttestations": [],
        "importScopeAdapter": "normalized-import-scope-descriptor",
        "planId": PLAN,
    }
    d.update(extra)
    return d


def install_pair(inputs, sid, sc, cid, covr):
    inputs.setdefault("scopes", {})[sid] = sc
    inputs.setdefault("coverages", {})[cid] = covr
    inputs.setdefault("coverageScopes", {})[cid] = sid


def test_known_hit_partial_none_false():
    iid = imp2("1")
    inputs = base_inputs(
        planSelectedImportIds=[iid, imp2("2")],
        evaluationInputRefs=[iid, imp2("2")],
        imports={
            iid: wrap("runtime"),
            imp2("2"): wrap("runtime", "partial"),
        },
        importPayloads={
            iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}]),
            imp2("2"): rt_payload([]),
        },
        importObservations={
            iid: rt_obs(),
            imp2("2"): rt_obs(),
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
    for c in r["causes"]:
        if c.get("evidenceKind") != "runtime" or c.get("nativeCause") is not None:
            fail(f"import cause typing {c}")


def test_missing_runtime_observable_unknown():
    iid = imp2("1")
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: wrap("runtime")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "unobservable"}])},
        importObservations={iid: rt_obs()},
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
    iid = imp2("3")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: wrap("history")},
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
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U2, ["ts-symbol:src/a.ts#g"], tag="1")
    fid = fact2("1")
    inputs = base_inputs(
        facts={fid: {
            "factId": fid, "relation": "references", "resolution": "resolved-binding",
            "sourceUniverse": U1, "targetUniverse": U2,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"referrer": "ts-symbol:src/a.ts#g", "name": "f",
                        "resolvedBinding": "ts-symbol:src/a.ts#f"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        inventories=[inv_symbol(), inv_symbol(nid="ts-symbol:src/a.ts#g", qn="g")],
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "incoming-no-cartesian")
    codes = {c["code"] for c in r["causes"]}
    if "source-target-search-unattested" not in codes:
        fail(f"incoming-no-cartesian causes {codes}")
    if r["knownFactIds"]:
        fail("incoming-no-cartesian: fact to V must not match U")


def test_source_kind_vs_incoming_target_kind():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a",
                        "resolvedTarget": "file:src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        inventories=[inv_symbol(), inv_file()],
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation="src/a.ts")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target",
            "filters": [{"field": "subjectKind", "cmp": "eq", "value": "symbol"}]}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "incoming-subjectKind-source")
    atom2 = dict(atom)
    atom2["filters"] = [{"field": "subjectKind", "cmp": "eq", "value": "file"}]
    r2 = AM.evaluate_atom(atom2, subj, inputs)
    if r2["value"] == "true":
        fail("incoming-subjectKind-file must not match source symbol")


def test_equal_native_id_different_universe():
    fid = fact2("1")
    inputs = base_inputs(
        facts={fid: {
            "factId": fid, "relation": "file", "resolution": "enumerated",
            "sourceUniverse": U2, "targetUniverse": U2,
            "producerClosure": C_PROV, "confidenceMillionths": 1000000,
            "payload": {"path": "src/a.ts", "contentSha256": H("0"), "byteLength": 1},
            "anchors": [],
        }},
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file(U1), inv_file(U2)],
    )
    inputs["enumerationPlan"]["cells"].append({
        "capabilityId": "inventory", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg",
        "required": True, "kinds": ["file"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV},
            "nativeContextDigest": H("0"), "universe": U2, "programEntry": "tsconfig.json",
            "extents": [{"kind": "file", "paths": ["src/a.ts"]}],
        }],
    })
    sid, sc, cid, cov = paired("file", "enumerated", U1, U1, ["src/a.ts"], tag="1")
    install_pair(inputs, sid, sc, cid, cov)
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
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan,
        inventories=[inv1, inv2, inv_file()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "file:src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation="src/a.ts")},
    )
    install_pair(inputs, sid, sc, cid, cov)
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
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a",
                        "resolvedTarget": "ts-symbol:src/a.ts#f"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "ts-symbol:src/a.ts#f", kind="file", occupancy="first-party",
                                         evaluation="src/a.ts")},
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target", "filters": []}

    def go():
        AM.evaluate_atom(atom, subj, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT", "sidecar-kind")

    inputs2 = dict(inputs)
    inputs2["targetAttributions"] = {fid: sidecar(fid, "ts-symbol:src/a.ts#f", kind="symbol", occupancy="external",
                                                  exported="exported")}
    def go2():
        AM.evaluate_atom(atom, subj, inputs2)
    expect_admit(go2, "TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY", "sidecar-external")

    inputs3 = dict(inputs)
    facts3 = dict(inputs["facts"])
    f3 = dict(facts3[fid])
    f3["producerClosure"] = C_EVAL
    facts3[fid] = f3
    inputs3["facts"] = facts3
    inputs3["targetAttributions"] = {fid: sidecar(fid, "ts-symbol:src/a.ts#f", kind="unknown", occupancy="unknown",
                                                  producer=C_EVAL)}
    def go3():
        AM.evaluate_atom(atom, subj, inputs3)
    expect_admit(go3, "TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER", "sidecar-evaluator")


def test_all_covered_na_and_resolved_partial():
    sid, sc, cid, cov = paired("file", "enumerated", U1, U1, ["src/a.ts"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "all-covered", "relation": "file", "minResolution": "enumerated", "filters": []}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "all-covered-na")

    sid2, sc2, cid2, cov2 = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"],
                                   tag="2", state="incomplete")
    inputs2 = base_inputs()
    install_pair(inputs2, sid2, sc2, cid2, cov2)
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
    sid, sc, cid, cov = paired("file", "enumerated", U1, U1, ["src/a.ts"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        facts={fact2("1"): {
            "factId": fact2("1"), "relation": "file", "resolution": "enumerated",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"path": "src/a.ts", "contentSha256": H("0"), "byteLength": 1},
            "anchors": [],
        }},
    )
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "exists", "relation": "file", "minResolution": "enumerated",
            "filters": [{"field": "universe", "cmp": "neq", "value": RS}]}
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "universe-neq-other-domain")


def test_tests_exit1_empty():
    iid = imp2("4")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: wrap("test")},
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
    for c in r["causes"]:
        if c.get("evidenceKind") != "runtime":
            fail(f"optional-unknown evidenceKind {c}")


def test_known_count_gt_n_partial():
    iid = imp2("1")
    qid = imp2("2")
    inputs = base_inputs(
        planSelectedImportIds=[iid, qid],
        evaluationInputRefs=[iid, qid],
        imports={
            iid: wrap("runtime"),
            qid: wrap("runtime", "partial"),
        },
        importPayloads={
            iid: rt_payload([
                {"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 3},
            ]),
            qid: rt_payload([]),
        },
        importObservations={
            iid: rt_obs(),
            qid: rt_obs(),
        },
    )
    wid = imp2("5")
    inputs["planSelectedImportIds"].append(wid)
    inputs["evaluationInputRefs"].append(wid)
    inputs["imports"][wid] = wrap("runtime")
    inputs["importPayloads"][wid] = rt_payload([
        {"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1},
    ])
    inputs["importObservations"][wid] = inputs["importObservations"][iid]
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "count-at-most", "n": 1, "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "false", "count-gt-n-partial")
    if len(r["knownObservationAddresses"]) < 2:
        fail("count-gt-n-partial: expected two known addresses")


def test_listed_paths_missing_not_vacuous():
    iid = imp2("3")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        evaluationInputRefs=[iid],
        imports={iid: wrap("history")},
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
    expect_admit(go, "ATOM_INPUT_KEY_UNKNOWN", "oracle")


def test_two_symbols_one_file_independent_partitions():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    sf, scf, cf, covf = paired("references", "resolved-binding", U1, U1, [f], tag="1", state="complete")
    sg, scg, cg, covg = paired("references", "resolved-binding", U1, U1, [g], tag="2", state="partial", cov="partial")
    inv_g = inv_symbol(nid=g, qn="g")
    inputs = base_inputs(inventories=[inv_symbol(), inv_g])
    install_pair(inputs, sf, scf, cf, covf)
    install_pair(inputs, sg, scg, cg, covg)
    atom = {"op": "all-covered", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "true", "two-sym-f-complete")
    r2 = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": g}, inputs)
    expect_value(r2, "indeterminate", "two-sym-g-partial")


def test_symbols_not_filepath_ids():
    plan = plan_one(cap="references", kinds=["symbol"])
    plan["cells"][0]["programBindings"][0]["extents"] = [
        {"kind": "symbol", "paths": ["src/a.ts"]},
        {"kind": "file", "paths": ["src/a.ts"]},
    ]
    inv = inv_symbol()
    inv["rows"] = []
    inv["state"] = "complete"
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, [], tag="1")
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    codes = {c["code"] for c in r["causes"]}
    if "uncovered-expected-source-subject" in codes and "src/a.ts" in str(r):
        fail("symbol expected ids must not include extent file paths as subject IDs")
    expect_value(r, "indeterminate", "symbol-empty-not-filepath")


def test_requested_rung_complete_higher_partial():
    s1, sc1, c1, cov1 = paired("imports", "syntactic-specifier", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    s2, sc2, c2, cov2 = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"],
                               tag="2", state="partial", cov="partial")
    inputs = base_inputs(enumerationPlan=plan_one(cap="imports"))
    install_pair(inputs, s1, sc1, c1, cov1)
    install_pair(inputs, s2, sc2, c2, cov2)
    atom = {"op": "all-covered", "relation": "imports", "minResolution": "syntactic-specifier", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "true", "requested-rung-not-higher")


def test_calls_with_dependency_coverage():
    f = "ts-symbol:src/a.ts#f"
    sr, scr, cr, covr = paired("reachability", "from-resolved-calls", U1, U1, [f], tag="1")
    sc, scc, cc, covc = paired("calls", "resolved-callee", U1, U1, [f], tag="2")
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    install_pair(inputs, sr, scr, cr, covr)
    install_pair(inputs, sc, scc, cc, covc)
    atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    if "required-relation-missing" in r["nativeDeficiencies"]:
        fail("calls dependency coverage should populate sufficiency view")
    expect_value(r, "true", "reachability-with-calls-dep")


def test_unknown_export_owes_closed_world():
    """Incoming target-direction closed-world. Outgoing counterpart is test_outgoing_exported_not_external_consumers."""
    inv = inv_symbol()
    inv["rows"][0]["exported"] = "unknown"
    g = "ts-symbol:src/a.ts#g"
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, [g], tag="1")
    cov["entry"]["closedWorld"]["exportsClosed"] = "open"
    inputs = base_inputs(inventories=[inv_symbol(nid=g, qn="g")])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "indeterminate", "unknown-export-incoming")
    if "external-consumers-unknown" not in r["nativeDeficiencies"] and "target-export-unknown" not in {c["code"] for c in r["causes"]}:
        fail(f"unknown-export-incoming defs={r['nativeDeficiencies']} causes={r['causes']}")


def test_portable_glob_contract():
    # Prescribed normative examples and boundary controls, not generated expected results.
    vectors = [
        ("**/*.ts", "a.ts", True), ("**/*.ts", "src/nested/a.ts", True),
        ("*.ts", "src/a.ts", False), ("src/**", "src", True),
        ("src/**", "src/legacy.js", True), ("src/**", "src/nested/legacy.js", True),
        ("src/**/*", "src", False), ("src/**/*", "src/legacy.js", True),
        ("a/**/b", "a/b", True), ("a/**/b", "a/x/y/b", True),
        ("a/*/b", "a/b", False), ("a**b", "a/x/b", False),
        ("a**b", "axxb", True), ("*", ".hidden", True),
        ("a.ts", "A.ts", False), ("a.ts", "a.ts.extra", False),
        ("?.ts", "é.ts", True), ("?.ts", "e\u0301.ts", False),
        ("[ab].ts", "a.ts", False), ("[ab].ts", "[ab].ts", True),
        ("{a,b}.ts", "a.ts", False), ("{a,b}.ts", "{a,b}.ts", True),
        ("src/", "src", False), ("src/*", "src/a/b", False),
        ("a*b", "ab", True), ("a?b", "ab", False),
        ("?.ts", "🙂.ts", True), ("é.ts", "e\u0301.ts", False),
        ("a/./b", "a/b", False), ("/a", "a", False),
    ]
    for pattern, candidate, expected in vectors:
        actual = AM.W.glob_match(pattern, candidate)
        if actual is not expected:
            fail(f"portable glob {pattern!r} / {candidate!r}: {actual!r} != {expected!r}")
    scope = {"include": ["**/*.ts"], "exclude": ["src/**"]}
    if not AM.W.in_scope(scope, "a.ts") or AM.W.in_scope(scope, "src/a.ts"):
        fail("ScopeDocument exclusion must win inclusion")


def test_glob_root():
    sid, sc, cid, cov = paired("file", "enumerated", U1, U1, ["a.ts"], tag="1")
    inv = inv_file(path="a.ts")
    inputs = base_inputs(enumerationPlan=plan_one(cap="inventory", kinds=["file"]), inventories=[inv],
                         facts={fact2("1"): {
                             "factId": fact2("1"), "relation": "file", "resolution": "enumerated",
                             "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
                             "confidenceMillionths": 1000000,
                             "payload": {"path": "a.ts", "contentSha256": H("0"), "byteLength": 1}, "anchors": [],
                         }})
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "exists", "relation": "file", "minResolution": "enumerated",
            "filters": [{"field": "subject", "cmp": "glob", "value": "**/*.ts"}]}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "file", "nativeSubjectId": "a.ts"}, inputs)
    expect_value(r, "true", "glob-root-a.ts")


def test_wrong_kind_none_admission():
    def go():
        AM.evaluate_atom(
            {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"},
            base_inputs(enumerationPlan=plan_one(cap="inventory", kinds=["file"]), inventories=[inv_file()]),
        )
    expect_admit(go, "ATOM_KIND_INCOMPATIBLE", "wrong-kind-none")


def test_runtime_complete_unhit_filter_hit_none_true():
    iid = imp2("1")
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        imports={iid: wrap("runtime")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observable-unhit", "hits": 0}])},
        importObservations={iid: rt_obs()},
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "none", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [{"field": "observability", "cmp": "eq", "value": "observed-hit"}], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "unhit-filter-hit-none")
    e = AM.evaluate_atom({**atom, "op": "exists"}, subj, inputs)
    expect_value(e, "false", "unhit-filter-hit-exists")


def test_runtime_partial_known_count_unknown():
    iid = imp2("1")
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        imports={iid: wrap("runtime", "partial")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}])},
        importObservations={iid: rt_obs()},
    )
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    atom = {"op": "count-at-most", "n": 5, "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "partial-count-le-n")
    ex = AM.evaluate_atom({**atom, "op": "exists", "filters": []}, subj, inputs)
    expect_value(ex, "true", "partial-exists-dominates")


def test_history_filtered_false_partial_known():
    iid = imp2("3")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        imports={iid: wrap("history", "partial")},
        importPayloads={iid: {"collectionScope": "all-paths",
                              "subjects": [{"path": "src/a.ts", "changeCount": 1, "lastChangedCommit": "a" * 40}],
                              "revisionRange": {"from": None, "to": "b" * 40, "commitCount": 1, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": None, "to": "b" * 40}}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "none", "relation": "history-change", "minResolution": "observed",
            "filters": [{"field": "subject", "cmp": "eq", "value": "src/other.ts"}], "evidence": "history"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "indeterminate", "history-filter-nomatch-partial")
    atom2 = {**atom, "filters": [{"field": "subject", "cmp": "eq", "value": "src/a.ts"}]}
    r2 = AM.evaluate_atom(atom2, subj, inputs)
    expect_value(r2, "false", "history-filter-match-partial-none")


def test_test_result_subject_kind_filter():
    iid = imp2("4")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        imports={iid: wrap("test")},
        importPayloads={iid: {
            "producer": "host-test-execution", "exitStatus": 0, "signal": None, "timedOut": False,
            "tests": [{"testId": "t1", "subjectPath": "src/a.ts", "outcome": "pass"}],
            "selection": {"mode": "full", "completenessEstablished": True},
        }},
        importObservations={iid: {"window": None, "population": None,
                                  "selection": {"mode": "full", "completenessEstablished": True},
                                  "revisionRange": None}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "test-result", "minResolution": "observed",
            "filters": [{"field": "subjectKind", "cmp": "eq", "value": "file"},
                        {"field": "testResult", "cmp": "eq", "value": "pass"}],
            "evidence": "test"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "true", "test-result-subjectKind")


def test_missing_wrapper_empty_refs():
    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
             "filters": [], "evidence": "runtime"},
            {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"},
            base_inputs(planSelectedImportIds=[imp2("6")], imports={}, evaluationInputRefs=[]),
        )
    expect_admit(go, "ATOM_IMPORT_WRAPPER_MISSING", "missing-wrapper")


def test_runtime_overload_ambiguous():
    iid = imp2("1")
    inv_a = inv_symbol(nid="ts-symbol:src/a.ts#f1", qn="f")
    inv_b = inv_symbol(nid="ts-symbol:src/a.ts#f2", qn="f")
    inputs = base_inputs(
        inventories=[inv_a, inv_b],
        planSelectedImportIds=[iid],
        imports={iid: wrap("runtime")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}])},
        importObservations={iid: rt_obs()},
    )
    atom = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f1"}, inputs)
    expect_value(r, "indeterminate", "overload-ambig")
    if not any(c["code"] == "overload-ambiguous" for c in r["causes"]):
        fail(f"overload causes {r['causes']}")
    if r["knownObservationAddresses"]:
        fail("overload must not be a positive match")


def test_incoming_attestation_malformed_duplicate_unselected():
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    sid, sc = scope("references", "resolved-binding", U1, U2, ["ts-symbol:src/a.ts#g"], sid="1")
    invs = [inv_symbol()]

    def go_mal():
        AM.evaluate_atom(atom, subj, base_inputs(incomingSearchAttestations=[{"schemaVersion": 1}]))
    expect_admit(go_mal, "INCOMING_SEARCH_SCHEMA", "att-malformed")

    good = incoming_att("references", "resolved-binding", U1, U1, [sid], invs)
    def go_dup():
        AM.evaluate_atom(atom, subj, base_inputs(scopes={sid: sc}, inventories=invs,
                                                 incomingSearchAttestations=[good, dict(good)]))
    expect_admit(go_dup, "INCOMING_SEARCH_DUPLICATE", "att-dup")

    badp = dict(good)
    badp["providerClosure"] = C_EVAL
    def go_unsel():
        AM.evaluate_atom(atom, subj, base_inputs(scopes={sid: sc}, inventories=invs,
                                                 incomingSearchAttestations=[badp]))
    expect_admit(go_unsel, "INCOMING_SEARCH_UNSELECTED_PROVIDER", "att-unselected")


def test_package_two_manifests_same_name():
    plan = plan_one(cap="inventory", kinds=["package"])
    a = inv_package(path="pkg-a/package.json")
    b = inv_package(path="pkg-b/package.json")
    b["cellOrdinal"] = 0
    fid_a = fact2("1")
    fid_b = fact2("2")
    sid, sc, cid, cov = paired("package", "manifest-declared", U1, U1, ["dup"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan,
        inventories=[a, b],
        facts={
            fid_a: {
                "factId": fid_a, "relation": "package", "resolution": "manifest-declared",
                "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
                "confidenceMillionths": 1000000,
                "payload": {"manifestPath": "pkg-a/package.json", "packageName": "dup", "packageVersion": "1.0.0"},
                "anchors": [],
            },
            fid_b: {
                "factId": fid_b, "relation": "package", "resolution": "manifest-declared",
                "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
                "confidenceMillionths": 1000000,
                "payload": {"manifestPath": "pkg-b/package.json", "packageName": "dup", "packageVersion": "2.0.0"},
                "anchors": [],
            },
        },
    )
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "exists", "relation": "package", "minResolution": "manifest-declared", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "package", "nativeSubjectId": "dup",
                                "packageManifestPath": "pkg-a/package.json"}, inputs)
    expect_value(r, "true", "pkg-a-hit")
    if fid_b in r["knownFactIds"]:
        fail("pkg-a subject must not occupy pkg-b fact")
    r2 = AM.evaluate_atom(atom, {"universe": U1, "kind": "package", "nativeSubjectId": "dup",
                                 "packageManifestPath": "pkg-b/package.json"}, inputs)
    expect_value(r2, "true", "pkg-b-hit")
    if fid_a in r2["knownFactIds"]:
        fail("pkg-b subject must not occupy pkg-a fact")
    def go_shape():
        AM.evaluate_atom(atom, {"universe": U1, "kind": "package", "nativeSubjectId": "dup"}, inputs)
    expect_admit(go_shape, "ATOM_SUBJECT_SHAPE", "package-requires-manifest")
    def go_file_extra():
        AM.evaluate_atom(
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts", "packageManifestPath": "x"},
            base_inputs(enumerationPlan=plan_one(cap="inventory", kinds=["file"]), inventories=[inv_file()]),
        )
    expect_admit(go_file_extra, "ATOM_SUBJECT_SHAPE", "file-forbids-manifest")


def test_incoming_mixed_atom_policy():
    sid, sc = scope("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], sid="1")
    invs = [inv_symbol()]
    att = incoming_att("references", "resolved-binding", U1, U1, [sid], invs)
    sid_f, sc_f, cid_f, cov_f = paired("file", "enumerated", U1, U1, ["src/a.ts"], tag="2")
    plan = plan_one(cap="inventory", kinds=["file"])
    plan["cells"].append(plan_one(cap="references")["cells"][0])
    inputs = base_inputs(
        enumerationPlan=plan,
        inventories=[inv_file(), inv_symbol()],
        scopes={sid: sc},
        incomingSearchAttestations=[att],
        facts={fact2("1"): {
            "factId": fact2("1"), "relation": "file", "resolution": "enumerated",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"path": "src/a.ts", "contentSha256": H("0"), "byteLength": 1}, "anchors": [],
        }},
    )
    install_pair(inputs, sid_f, sc_f, cid_f, cov_f)
    r = AM.evaluate_atom(
        {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
        {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
        inputs,
    )
    expect_value(r, "true", "mixed-atom-file-with-references-att")


def test_incoming_examined_exhaustive_false():
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    sid, sc = scope("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#g"], sid="1")
    invs = [inv_symbol()]
    att = incoming_att("references", "resolved-binding", U1, U1, [sid], invs,
                       completeSearch=True, examinedExhaustive=False, coverage="complete")
    def go():
        AM.evaluate_atom(atom, subj, base_inputs(scopes={sid: sc}, inventories=invs,
                                                 incomingSearchAttestations=[att]))
    expect_admit(go, "INCOMING_SEARCH_SCHEMA", "exhaustive-false-complete")


def test_unmatched_scope_beside_paired():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    sf, scf, cf, covf = paired("references", "resolved-binding", U1, U1, [f], tag="1")
    sg, scg = scope("references", "resolved-binding", U1, U1, [g], sid="2")
    inputs = base_inputs(inventories=[inv_symbol(), inv_symbol(nid=g, qn="g")])
    install_pair(inputs, sf, scf, cf, covf)
    inputs["scopes"][sg] = scg
    atom = {"op": "all-covered", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": g}, inputs)
    expect_value(r, "indeterminate", "unmatched-g")
    if "scope-without-coverage" not in {c["code"] for c in r["causes"]}:
        fail(f"unmatched-g causes {r['causes']}")
    r2 = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r2, "true", "paired-f-still-complete")


def test_first_party_not_in_inventory():
    fid = fact2("1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports"),
        inventories=[inv_symbol()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "ext", "resolvedTarget": "package:left-pad"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "package:left-pad", kind="package", occupancy="first-party",
                                         evaluation="left-pad",
                                         manifest="node_modules/left-pad/package.json")},
    )
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target", "filters": []}
    def go():
        AM.evaluate_atom(atom, {"universe": U1, "kind": "package", "nativeSubjectId": "left-pad",
                                "packageManifestPath": "node_modules/left-pad/package.json"}, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY", "fp-missing")


def test_unused_sidecar_still_admitted():
    fid = fact2("1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_EVAL,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "file:src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="unknown", occupancy="unknown", producer=C_EVAL)},
    )
    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []},
            {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
            inputs,
        )
    expect_admit(go, "TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER", "unused-sidecar")


def test_duplicate_inventory_observation_not_overload():
    iid = imp2("3")
    inv1 = inv_file()
    inv2 = inv_file()
    inv2["cellOrdinal"] = 1
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv1, inv2],
        planSelectedImportIds=[iid],
        imports={iid: wrap("history")},
        importPayloads={iid: {"collectionScope": "all-paths", "subjects": [],
                              "revisionRange": {"from": "a" * 40, "to": "b" * 40, "commitCount": 3, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": "a" * 40, "to": "b" * 40}}},
    )
    r = AM.evaluate_atom(
        {"op": "all-covered", "relation": "history-change", "minResolution": "observed",
         "filters": [], "evidence": "history"},
        {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"},
        inputs,
    )
    expect_value(r, "true", "dup-obs-not-overload")


def test_import_scope_roots_and_prefixes():
    iid = imp2("3")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file(path="a.ts")],
        planSelectedImportIds=[iid],
        imports={iid: wrap("history")},
        importPayloads={iid: {"collectionScope": "all-paths", "subjects": [],
                              "revisionRange": {"from": "a" * 40, "to": "b" * 40, "commitCount": 1, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": "a" * 40, "to": "b" * 40}}},
    )
    r = AM.evaluate_atom(
        {"op": "all-covered", "relation": "history-change", "minResolution": "observed",
         "filters": [], "evidence": "history"},
        {"universe": U1, "kind": "file", "nativeSubjectId": "a.ts"},
        inputs,
    )
    expect_value(r, "indeterminate", "root-file-outside-src-prefix")
    codes = {c["code"] for c in r["causes"]}
    if "zero-owed-wrappers" not in codes:
        fail(f"root-file-outside-src-prefix causes {codes}")


def test_incoming_caller_digest_is_not_authority():
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    sid, sc = scope("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#g"], sid="1")
    invs = [inv_symbol()]
    att = incoming_att("references", "resolved-binding", U1, U1, [sid], invs,
                       expectedInventoryRefs=[H("1")])
    def go():
        AM.evaluate_atom(atom, subj, base_inputs(scopes={sid: sc}, inventories=invs,
                                                 incomingSearchAttestations=[att]))
    expect_admit(go, "INCOMING_SEARCH_INVENTORY_MISJOIN", "caller-digest")


def test_dep_other_universe_does_not_heal():
    sr, scr, cr, covr = paired("reachability", "from-resolved-calls", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    cc, covc = coverage("calls", "resolved-callee", U1, U2, state="complete", cid="2")
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    install_pair(inputs, sr, scr, cr, covr)
    inputs["coverages"][cc] = covc
    atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    if r["value"] == "true":
        fail("S->V calls coverage must not heal missing S->U dependency")
    if "required-relation-missing" not in r["nativeDeficiencies"]:
        fail(f"dep-other-universe defs {r['nativeDeficiencies']}")


def test_history_duplicate_path_retains_all_ordinals():
    iid = imp2("3")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="inventory", kinds=["file"]),
        inventories=[inv_file()],
        planSelectedImportIds=[iid],
        imports={iid: wrap("history")},
        importPayloads={iid: {"collectionScope": "all-paths",
                              "subjects": [
                                  {"path": "src/a.ts", "changeCount": 1, "lastChangedCommit": "a" * 40},
                                  {"path": "src/other.ts", "changeCount": 1, "lastChangedCommit": "b" * 40},
                                  {"path": "src/a.ts", "changeCount": 2, "lastChangedCommit": "c" * 40},
                              ],
                              "revisionRange": {"from": None, "to": "b" * 40, "commitCount": 3, "truncated": False}}},
        importObservations={iid: {"window": None, "population": None, "selection": None,
                                  "revisionRange": {"from": None, "to": "b" * 40}}},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "count-at-most", "n": 1, "relation": "history-change", "minResolution": "observed",
            "filters": [], "evidence": "history"}
    r = AM.evaluate_atom(atom, subj, inputs)
    expect_value(r, "false", "history-dup-count")
    ords = [a["ordinal"] for a in r["knownObservationAddresses"]]
    if ords != [0, 2]:
        fail(f"history-dup ordinals {r['knownObservationAddresses']}")


def test_runtime_obs_payload_window_mismatch_refused():
    iid = imp2("1")
    other = {"startUtc": "2021-01-01T00:00:00Z", "endUtc": "2021-01-02T00:00:00Z"}
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        imports={iid: wrap("runtime")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}])},
        importObservations={iid: rt_obs(window=other)},
    )
    def go():
        AM.evaluate_atom(
            {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
             "filters": [], "evidence": "runtime"},
            {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"},
            inputs,
        )
    expect_admit(go, "ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN", "window-mismatch")


def test_admit_atom_inputs_missing_wrapper_no_atom():
    def go():
        AM.admit_atom_inputs(base_inputs(planSelectedImportIds=[imp2("1")], imports={}))
    expect_admit(go, "ATOM_IMPORT_WRAPPER_MISSING", "global-missing-wrapper")
    AM.admit_atom_inputs(base_inputs())


def test_import_flags_adapter_no_default():
    iid = imp2("1")
    w = wrap("runtime")
    del w["consumable"]
    del w["staleness"]
    inputs = base_inputs(
        planSelectedImportIds=[iid],
        imports={iid: w},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}])},
        importObservations={iid: rt_obs()},
    )
    atom = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    subj = {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}
    def go():
        AM.evaluate_atom(atom, subj, inputs)
    expect_admit(go, "ATOM_IMPORT_CONSUMABLE_UNSTATED", "no-default-flags")
    inputs2 = dict(inputs)
    inputs2["importFlagsAdapter"] = {iid: {"consumable": True, "staleness": "current"}}
    r = AM.evaluate_atom(atom, subj, inputs2)
    expect_value(r, "true", "adapter-flags")


def test_outgoing_exported_not_external_consumers():
    inv = inv_symbol()
    inv["rows"][0]["exported"] = "exported"
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    cov["entry"]["closedWorld"]["exportsClosed"] = "open"
    inputs = base_inputs(inventories=[inv])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "true", "outgoing-exported-cw-open")
    if "external-consumers-unknown" in r["nativeDeficiencies"]:
        fail("outgoing none must not inherit incoming closed-world")


def test_unrelated_dep_partition_does_not_poison_outgoing():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    sr, scr, cr, covr = paired("reachability", "from-resolved-calls", U1, U1, [f], tag="1")
    sa, sca, ca, cova = paired("calls", "resolved-callee", U1, U1, [f], tag="2")
    sb, scb, cb, covb = paired("calls", "resolved-callee", U1, U1, [g], tag="3", state="partial", cov="partial")
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"),
                         inventories=[inv_symbol(), inv_symbol(nid=g, qn="g")])
    install_pair(inputs, sr, scr, cr, covr)
    install_pair(inputs, sa, sca, ca, cova)
    install_pair(inputs, sb, scb, cb, covb)
    atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "true", "outgoing-A-not-poisoned-by-B")
    if "resolution-incomplete" in r["nativeDeficiencies"]:
        fail("unrelated B partial must not poison A outgoing")


def test_incoming_all_source_partitions_owed():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    sf, scf, cf, covf = paired("reachability", "from-resolved-calls", U1, U1, [f], tag="1")
    sg, scg, cg, covg = paired("reachability", "from-resolved-calls", U1, U1, [g], tag="2",
                               state="partial", cov="partial")
    sa, sca, ca, cova = paired("calls", "resolved-callee", U1, U1, [f], tag="3")
    sb, scb, cb, covb = paired("calls", "resolved-callee", U1, U1, [g], tag="4")
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"),
                         inventories=[inv_symbol(), inv_symbol(nid=g, qn="g")])
    install_pair(inputs, sf, scf, cf, covf)
    install_pair(inputs, sg, scg, cg, covg)
    install_pair(inputs, sa, sca, ca, cova)
    install_pair(inputs, sb, scb, cb, covb)
    atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "indeterminate", "incoming-B-partition-owed")


def test_two_providers_same_u_disjoint_scopes():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    plan = plan_one(cap="references")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg-b",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV2},
            "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/a.ts"]}],
        }],
    })
    inv_a = inv_symbol()
    inv_b = inv_symbol(nid=g, qn="g")
    inv_b["cellOrdinal"] = 1
    sa, sca = scope("references", "resolved-binding", U1, U1, [f], sid="1")
    sb, scb = scope("references", "resolved-binding", U1, U1, [g], sid="2")
    scb["enumeratorClosure"] = C_PROV2
    att_a = incoming_att("references", "resolved-binding", U1, U1, [sa], [inv_a])
    att_b = incoming_att("references", "resolved-binding", U1, U1, [sb], [inv_b], providerClosure=C_PROV2)
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv_a, inv_b],
                         scopes={sa: sca, sb: scb},
                         incomingSearchAttestations=[att_a, att_b])
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "true", "two-providers-same-u")
    if "source-target-search-unattested" in {c["code"] for c in r["causes"]}:
        fail("each provider attested its owned scopes")


def test_unavailable_foreign_family_does_not_poison():
    plan = plan_one(cap="references")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "rust-cargo", "workspaceRoot": "crate",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "default-unit",
            "enumerator": {"status": "selected", "closureId": C_PROV},
            "nativeContextDigest": H("0"), "universe": None, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/lib.rs"]}],
        }],
    })
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(enumerationPlan=plan)
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "true", "rust-unavailable-not-poison-ts")
    if "unavailable-program-binding" in {c["code"] for c in r["causes"]}:
        fail("foreign-family unavailable must not poison TS outgoing")
    if "cross-family-edge-not-owed" not in {c["code"] for c in r["causes"]}:
        fail("retain cross-family disclosure")


def test_incoming_partition_s_to_v_does_not_prove_u():
    """Same provider: complete S->U on A and complete S->V on B. Incoming none of U is unknown."""
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    subject = {"universe": U1, "kind": "symbol", "nativeSubjectId": f}
    inputs = base_inputs(inventories=[inv_symbol(), inv_symbol(nid=g, qn="g")])
    for args in [("references", "resolved-binding", U1, U1, [f], "1"),
                 ("references", "resolved-binding", U1, U2, [g], "2")]:
        rel, rung, su, tu, ids, tag = args
        install_pair(inputs, *paired(rel, rung, su, tu, ids, tag=tag))
    r = AM.evaluate_atom(atom, subject, inputs)
    expect_value(r, "indeterminate", "partition-A-U-not-B")
    if "source-target-search-unattested" not in {c["code"] for c in r["causes"]}:
        fail(f"partition-A-U-not-B causes {r['causes']}")


def test_optional_same_family_unavailable_does_not_poison_outgoing():
    f = "ts-symbol:src/a.ts#f"
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "source", "filters": []}
    subject = {"universe": U1, "kind": "symbol", "nativeSubjectId": f}
    inputs = base_inputs(inventories=[inv_symbol()])
    install_pair(inputs, *paired("references", "resolved-binding", U1, U1, [f], tag="1"))
    unavailable = copy.deepcopy(inputs["enumerationPlan"]["cells"][0])
    unavailable["workspaceRoot"] = "other"
    unavailable["required"] = False
    unavailable["programBindings"][0]["universe"] = None
    inputs["enumerationPlan"]["cells"].append(unavailable)
    r = AM.evaluate_atom(atom, subject, inputs)
    expect_value(r, "true", "optional-other-program-outgoing")
    if "unavailable-program-binding" in {c["code"] for c in r["causes"]}:
        fail("same-family optional unavailable must not poison current-U outgoing")


def test_incoming_search_other_provider_partial_does_not_invalidate_att():
    f, g = "ts-symbol:src/a.ts#f", "ts-symbol:src/a.ts#g"
    plan = plan_one(cap="references")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg-b",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV2},
            "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/a.ts"]}],
        }],
    })
    inv_a, inv_b = inv_symbol(), inv_symbol(nid=g, qn="g")
    inv_b["cellOrdinal"] = 1
    sa, sca = scope("references", "resolved-binding", U1, U1, [f], sid="1")
    sb, scb, cb, covb = paired("references", "resolved-binding", U1, U1, [g], tag="2",
                               state="partial", cov="partial")
    scb["enumeratorClosure"] = C_PROV2
    att_a = incoming_att("references", "resolved-binding", U1, U1, [sa], [inv_a])
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv_a, inv_b],
                         scopes={sa: sca, sb: scb},
                         incomingSearchAttestations=[att_a])
    install_pair(inputs, sb, scb, cb, covb)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "indeterminate", "other-provider-partial-att-a-admitted")
    if r["value"] == "true":
        fail("B partial still leaves incoming unknown")


def test_incoming_unattached_target_universe_refused():
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    invs = [inv_symbol()]
    att = incoming_att("references", "resolved-binding", U1, "00" * 32, [sid], invs)
    inputs = base_inputs(incomingSearchAttestations=[att])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "exists", "relation": "file", "minResolution": "enumerated", "filters": []}

    def go():
        AM.admit_atom_inputs(inputs)
    expect_admit(go, "INCOMING_SEARCH_JOIN", "unattached-target-universe")


def test_runtime_unrelated_overload_is_nomatch():
    iid = imp2("1")
    inv_a = inv_symbol(nid="ts-symbol:src/a.ts#f1", qn="f")
    inv_b = inv_symbol(nid="ts-symbol:src/a.ts#f2", qn="f")
    inv_g = inv_symbol(nid="ts-symbol:src/a.ts#g", qn="g")
    inputs = base_inputs(
        inventories=[inv_a, inv_b, inv_g],
        planSelectedImportIds=[iid],
        imports={iid: wrap("runtime")},
        importPayloads={iid: rt_payload([{"path": "src/a.ts", "symbol": "f", "observability": "observed-hit", "hits": 1}])},
        importObservations={iid: rt_obs()},
    )
    atom = {"op": "exists", "relation": "runtime-observation", "minResolution": "observed",
            "filters": [], "evidence": "runtime"}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#g"}, inputs)
    if r["value"] == "true":
        fail("unrelated overload must not match g")
    if any(c["code"] == "overload-ambiguous" for c in r["causes"]):
        fail("unrelated symbol must not inherit f's overload-ambiguous")
    if r["knownObservationAddresses"]:
        fail("unrelated overload is not a known hit on g")


def test_provider_with_no_scope_does_not_disappear():
    f = "ts-symbol:src/a.ts#f"
    plan = plan_one(cap="references")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg-b",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV2},
            "nativeContextDigest": H("0"), "universe": U1, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/a.ts"]}],
        }],
    })
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, [f], tag="1")
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv_symbol()])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
            "endpoint": "target", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": f}, inputs)
    expect_value(r, "indeterminate", "provider-no-scope-explicit")
    if "source-target-search-unattested" not in {c["code"] for c in r["causes"]}:
        fail(f"provider-no-scope causes {r['causes']}")


def _imports_file_fact(fid, resolved="file:src/a.ts"):
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": resolved},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def test_ordinary_first_party_file_import_target():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: _imports_file_fact(fid)},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation="src/a.ts")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []}, subj, inputs)
    expect_value(r, "true", "p-file-exists")
    if fid not in r["knownFactIds"]:
        fail("p-file-exists missing known fact")
    r2 = AM.evaluate_atom({"op": "none", "relation": "imports", "minResolution": "resolved-target",
                           "endpoint": "target", "filters": []}, subj, inputs)
    expect_value(r2, "false", "p-file-none-false")


def test_ordinary_first_party_package_import_target():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "package"]),
        inventories=[inv_symbol(), inv_package(name="demo-app", path="package.json")],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "demo-app",
                        "resolvedTarget": "package:demo-app"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "package:demo-app", kind="package", occupancy="first-party",
                                         evaluation="demo-app", manifest="package.json")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "package", "nativeSubjectId": "demo-app",
            "packageManifestPath": "package.json"}
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []}, subj, inputs)
    expect_value(r, "true", "p-package-exists")


def test_missing_sidecar_namespaced_file_is_unknown_not_nomatch():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    att = incoming_att("imports", "resolved-target", U1, U1, [sid], [inv_symbol()])
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: _imports_file_fact(fid)},
        incomingSearchAttestations=[att],
    )
    install_pair(inputs, sid, sc, cid, cov)
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    r = AM.evaluate_atom({"op": "none", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []}, subj, inputs)
    expect_value(r, "indeterminate", "c14-missing-sidecar-not-none")
    r2 = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                           "endpoint": "target", "filters": []}, subj, inputs)
    expect_value(r2, "indeterminate", "c14-missing-sidecar-exists-unknown")


def test_malformed_first_party_evaluation_id_refuses():
    fid = fact2("1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: _imports_file_fact(fid)},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation=None)},
    )
    def go():
        AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_SCHEMA", "malformed-null-eval-id")


def test_v1_sidecar_refused():
    fid = fact2("1")
    sc = sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts")
    sc["schemaVersion"] = 1
    del sc["evaluationNativeId"]
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: _imports_file_fact(fid)},
        targetAttributions={fid: sc},
    )
    def go():
        AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_SCHEMA_VERSION", "v1-sidecar")


def test_external_file_is_nomatch_on_inventory_subject():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: _imports_file_fact(fid, "file:node_modules/left-pad/index.js")},
        targetAttributions={fid: sidecar(fid, "file:node_modules/left-pad/index.js", kind="file",
                                         occupancy="external", logical="node_modules/left-pad/index.js")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    if r["value"] == "true":
        fail("external file must not occupy first-party inventory subject")
    if r["knownFactIds"]:
        fail("external file must not be a known hit on inventory file")


def test_symbol_exact_id_ephemeral_without_sidecar():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports"),
        inventories=[inv_symbol()],
        facts={fid: {
            "factId": fid, "relation": "imports", "resolution": "resolved-target",
            "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
            "confidenceMillionths": 1000000,
            "payload": {"importer": "ts-symbol:src/a.ts#g", "specifier": "./a",
                        "resolvedTarget": "ts-symbol:src/a.ts#f"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
    )
    install_pair(inputs, sid, sc, cid, cov)
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "true", "symbol-ephemeral-exact-id")


def test_provider_occupancy_conflict_same_producer():
    fid1, fid2 = fact2("1"), fact2("2")
    facts = {
        fid1: _imports_file_fact(fid1),
        fid2: _imports_file_fact(fid2),
    }
    facts[fid2]["payload"] = dict(facts[fid2]["payload"])
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file(), inv_file(path="src/b.ts")],
        facts=facts,
        targetAttributions={
            fid1: sidecar(fid1, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts"),
            fid2: sidecar(fid2, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/b.ts"),
        },
    )
    def go():
        AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT", "same-producer-conflict")


def test_different_providers_same_opaque_id_are_not_aliases():
    fid1, fid2 = fact2("1"), fact2("2")
    f2 = _imports_file_fact(fid2)
    f2["producerClosure"] = C_PROV2
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid1: _imports_file_fact(fid1), fid2: f2},
        targetAttributions={
            fid1: sidecar(fid1, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts"),
            fid2: sidecar(fid2, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts",
                          producer=C_PROV2),
        },
    )
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    expect_value(r, "true", "cross-provider-opaque-not-alias")


def test_c15_ephemeral_identity_conflict_refuses():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file(path="file:src/a.ts"), inv_file(path="src/b.ts")],
        facts={fid: _imports_file_fact(fid, "file:src/a.ts")},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation="src/b.ts")},
    )
    install_pair(inputs, sid, sc, cid, cov)

    def go():
        AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/b.ts"}, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT", "c15-overwrite")


def test_c15_agreement_same_identity_admits():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file(path="file:src/a.ts")],
        facts={fid: _imports_file_fact(fid, "file:src/a.ts")},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party",
                                         evaluation="file:src/a.ts")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "file:src/a.ts"}, inputs)
    expect_value(r, "true", "c15-agree-exists")


def test_c15_unknown_sidecar_keeps_ephemeral():
    fid = fact2("1")
    sid, sc, cid, cov = paired("imports", "resolved-target", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file(path="file:src/a.ts")],
        facts={fid: _imports_file_fact(fid, "file:src/a.ts")},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="unknown", occupancy="unknown")},
    )
    install_pair(inputs, sid, sc, cid, cov)
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "file:src/a.ts"}, inputs)
    expect_value(r, "true", "c15-unknown-keeps-ephemeral")


def test_wrong_universe_still_nomatch():
    fid = fact2("1")
    fact = _imports_file_fact(fid)
    fact["targetUniverse"] = U2
    inputs = base_inputs(
        enumerationPlan=plan_one(cap="imports", kinds=["symbol", "file"]),
        inventories=[inv_symbol(), inv_file()],
        facts={fid: fact},
        targetAttributions={fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="external",
                                         universe=U2, logical="src/a.ts")},
    )
    r = AM.evaluate_atom({"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                          "endpoint": "target", "filters": []},
                         {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}, inputs)
    if r["value"] == "true":
        fail("wrong universe must not match")
    if r["knownFactIds"]:
        fail("wrong universe known hit")


def test_invalid_native_carrier_refuses_not_unknown():
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    sc["snapshotId"] = "snapshot2:" + "g" * 64
    inputs = base_inputs(scopes={sid: sc}, coverages={cid: cov})
    atom = {"op": "all-covered", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    def go():
        AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_admit(go, "ATOM_NATIVE_CARRIER", "invalid-typed-scope")


F_SYM = "ts-symbol:src/a.ts#f"
G_SYM = "ts-symbol:src/a.ts#g"
IMPORTS_ATOM = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                "filters": []}
F_SUBJ = {"universe": U1, "kind": "symbol", "nativeSubjectId": F_SYM}


def outgoing_import_fact(fid):
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": F_SYM, "specifier": "./b", "resolvedTarget": "file:src/b.ts"},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def early_stops(fid=None):
    """The four outgoing early stops of contract section 4, as (label, inputs, cause, universe)."""
    facts = {fid: outgoing_import_fact(fid)} if fid else {}
    invs = [inv_symbol(), inv_symbol(nid=G_SYM, qn="g")]
    out = []

    out.append(("no-owed-binding",
                base_inputs(enumerationPlan=plan_one(cap="inventory"), facts=dict(facts)),
                "missing-relation-coverage", None))

    out.append(("bindings-none-at-u",
                base_inputs(enumerationPlan=plan_one(universe=U2, cap="imports"), facts=dict(facts)),
                "selector-unbound", None))

    i3 = base_inputs(enumerationPlan=plan_one(cap="imports"), facts=dict(facts), inventories=invs)
    install_pair(i3, *paired("imports", "resolved-target", U1, U1, [G_SYM], tag="2"))
    out.append(("no-containing-scope", i3, "uncovered-expected-source-subject", U1))

    i4 = base_inputs(enumerationPlan=plan_one(cap="imports"), facts=dict(facts), inventories=invs)
    install_pair(i4, *paired("imports", "resolved-target", U1, U1, [F_SYM], tag="1"))
    sb, scb = scope("imports", "resolved-target", U1, U1, [F_SYM, G_SYM], sid="2")
    i4["scopes"][sb] = scb
    out.append(("unmatched-scope", i4, "scope-without-coverage", U1))
    return out


def test_outgoing_early_stop_cause_and_universe():
    """Section 4 steps 2-5: which cause each stop emits, and the universe it carries."""
    for label, inputs, code, universe in early_stops():
        r = AM.evaluate_atom(dict(IMPORTS_ATOM), F_SUBJ, inputs)
        expect_value(r, "indeterminate", label)
        got = {c["code"]: c for c in r["causes"]}
        if code not in got:
            fail(f"{label}: causes {r['causes']}")
        if got[code].get("universe") != universe:
            fail(f"{label}: {code} universe {got[code].get('universe')!r} != {universe!r}")
        if r["coverageIds"]:
            fail(f"{label}: early stop cited coverage {r['coverageIds']}")
        if label != "unmatched-scope" and r["scopeIds"]:
            fail(f"{label}: early stop cited scopes {r['scopeIds']}")


def test_unmatched_scope_stop_cites_every_scope_and_no_coverage():
    """Section 4 step 5: scopeIds is every containing scope; coverageIds stays empty."""
    _label, inputs, _code, _u = early_stops()[3]
    r = AM.evaluate_atom(dict(IMPORTS_ATOM), F_SUBJ, inputs)
    if r["scopeIds"] != sorted([scope2("1"), scope2("2")]):
        fail(f"unmatched stop scopeIds {r['scopeIds']}")
    if r["coverageIds"]:
        fail(f"unmatched stop must not cite a paired sibling: {r['coverageIds']}")


def test_known_hit_dominates_every_outgoing_early_stop():
    """A completeness return ends completeness only: a known match still decides the value."""
    fid = fact2("1")
    for label, inputs, code, _u in early_stops(fid):
        e = AM.evaluate_atom({**IMPORTS_ATOM, "op": "exists"}, F_SUBJ, inputs)
        expect_value(e, "true", f"{label}-exists")
        if fid not in e["knownFactIds"]:
            fail(f"{label}: completeness return erased the known fact")
        if code not in {c["code"] for c in e["causes"]}:
            fail(f"{label}: dominance erased the completeness cause")
        n = AM.evaluate_atom({**IMPORTS_ATOM, "op": "none"}, F_SUBJ, inputs)
        expect_value(n, "false", f"{label}-none")
        c0 = AM.evaluate_atom({**IMPORTS_ATOM, "op": "count-at-most", "n": 0}, F_SUBJ, inputs)
        expect_value(c0, "false", f"{label}-count-at-most-0")


def test_cross_family_disclosure_survives_outgoing_selector_stop():
    """Section 4 step 1 runs before the returns, and outgoing carries the binding's null universe."""
    plan = plan_one(universe=U2, cap="imports")
    plan["cells"].append({
        "capabilityId": "imports", "languageMode": "rust-cargo", "workspaceRoot": "crate",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "default-unit",
            "enumerator": {"status": "selected", "closureId": C_PROV2},
            "nativeContextDigest": H("0"), "universe": None, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/lib.rs"]}],
        }],
    })
    r = AM.evaluate_atom(dict(IMPORTS_ATOM), F_SUBJ, base_inputs(enumerationPlan=plan))
    got = {c["code"]: c for c in r["causes"]}
    if "selector-unbound" not in got or "cross-family-edge-not-owed" not in got:
        fail(f"cross-family must survive the selector stop: {r['causes']}")
    if got["cross-family-edge-not-owed"].get("universe") is not None:
        fail(f"outgoing cross-family universe {got['cross-family-edge-not-owed']!r}")
    if "unavailable-program-binding" in got:
        fail("unavailable-program-binding is incoming only")


def dep_fold_inputs(low_cause, high_cause, reverse=False):
    sr, scr, cr, covr = paired("reachability", "from-resolved-calls", U1, U1, [F_SYM], tag="1")
    sa, sca, ca, cova = paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="2", cov="unknown")
    sb, scb, cb, covb = paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="3", cov="unknown")
    cova["entry"]["deficiency"] = covb["entry"]["deficiency"] = "input-closure-incomplete"
    cova["entry"]["nativeCause"], covb["entry"]["nativeCause"] = low_cause, high_cause
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    pairs = [(sr, scr, cr, covr), (sa, sca, ca, cova), (sb, scb, cb, covb)]
    for p in (reversed(pairs) if reverse else pairs):
        install_pair(inputs, *p)
    return inputs


def _expect_folded_carrier(r, label, cause):
    cu = [c for c in r["causes"] if c["code"] == "coverage-unknown"]
    if len(cu) != 1 or cu[0].get("nativeCause") != cause:
        fail(f"{label}: coverage-unknown {cu}")
    if cu[0].get("universe") != U1:
        fail(f"{label}: coverage-unknown universe {cu[0].get('universe')!r}")
    if not {cov2("2"), cov2("3")} <= set(r["coverageIds"]):
        fail(f"{label}: every folded partition must be cited, got {r['coverageIds']}")
    if r["nativeDeficiencies"] != ["input-closure-incomplete"]:
        fail(f"{label}: nativeDeficiencies {r['nativeDeficiencies']}")


def test_dep_fold_carrier_is_first_partition_in_selection_order():
    """The typed carrier follows the ascending coverage2 id, not the host map's insertion order."""
    for endpoint in ("source", "target"):
        atom = {"op": "all-covered", "relation": "reachability",
                "minResolution": "from-resolved-calls", "endpoint": endpoint, "filters": []}
        for low, high in (("lockfile-missing", "no-program-unit"),
                          ("no-program-unit", "lockfile-missing")):
            for reverse in (False, True):
                label = f"{endpoint}/{low}/reverse={reverse}"
                r = AM.evaluate_atom(atom, F_SUBJ, dep_fold_inputs(low, high, reverse))
                expect_value(r, "indeterminate", label)
                _expect_folded_carrier(r, label, low)


def test_incoming_reports_every_universe_without_early_stop():
    """After the shared prelude, incoming makes no further early return: a failing U1 partition
    cannot hide U2's own causes. The prelude's own return is checked separately."""
    g = "ts-symbol:src/b.ts#g"
    plan = plan_one(cap="references")
    plan["cells"].append({
        "capabilityId": "references", "languageMode": "ts-tsconfig", "workspaceRoot": "pkg-b",
        "required": True, "kinds": ["symbol"],
        "programBindings": [{
            "ordinal": 0, "provenance": "explicit-plan-selection",
            "enumerator": {"status": "selected", "closureId": C_PROV2},
            "nativeContextDigest": H("0"), "universe": U2, "programEntry": None,
            "extents": [{"kind": "symbol", "paths": ["src/b.ts"]}],
        }],
    })
    inv_b = inv_symbol(universe=U2, nid=g, path="src/b.ts", qn="g")
    inv_b["cellOrdinal"] = 1
    s1, sc1 = scope("references", "resolved-binding", U1, U1, [F_SYM], sid="1")
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv_symbol(), inv_b],
                         scopes={s1: sc1})
    r = AM.evaluate_atom({"op": "none", "relation": "references", "minResolution": "resolved-binding",
                          "endpoint": "target", "filters": []}, F_SUBJ, inputs)
    expect_value(r, "indeterminate", "incoming-two-universes")
    got = {(c["code"], c.get("universe")) for c in r["causes"]}
    for want in (("scope-without-coverage", U1),
                 ("uncovered-expected-source-subject", U2),
                 ("source-target-search-unattested", U2)):
        if want not in got:
            fail(f"incoming dropped {want}: {r['causes']}")


def ref_cell(cap, mode, universe, root, closure, paths, kinds=None):
    return {"capabilityId": cap, "languageMode": mode, "workspaceRoot": root, "required": True,
            "kinds": kinds or ["symbol"],
            "programBindings": [{
                "ordinal": 0, "provenance": "default-unit",
                "enumerator": {"status": "selected", "closureId": closure},
                "nativeContextDigest": H("0"), "universe": universe, "programEntry": None,
                "extents": [{"kind": k, "paths": paths} for k in (kinds or ["symbol"])],
            }]}


def test_no_owed_binding_return_is_shared_by_both_endpoints():
    """The missing-relation-coverage return sits in the shared prelude, before the endpoint split."""
    inputs = base_inputs(enumerationPlan=plan_one(cap="inventory"))
    for endpoint in ("source", "target"):
        r = AM.evaluate_atom({"op": "none", "relation": "references",
                              "minResolution": "resolved-binding", "endpoint": endpoint,
                              "filters": []}, F_SUBJ, inputs)
        expect_value(r, "indeterminate", f"no-owed-binding-{endpoint}")
        got = {c["code"]: c for c in r["causes"]}
        if "missing-relation-coverage" not in got:
            fail(f"no-owed-binding-{endpoint}: causes {r['causes']}")
        if got["missing-relation-coverage"].get("universe") is not None:
            fail(f"no-owed-binding-{endpoint}: universe must project to null")
        if r["scopeIds"] or r["coverageIds"]:
            fail(f"no-owed-binding-{endpoint}: shared return cites {r['scopeIds']} {r['coverageIds']}")


def test_incoming_keeps_both_cross_family_shapes():
    """Incoming carries the prelude's unavailable/null disclosure AND the available/S one."""
    plan = plan_one(cap="references")
    plan["cells"].append(ref_cell("references", "rust-cargo", None, "crate-a", C_PROV2,
                                  ["crate-a/src/lib.rs"]))
    plan["cells"].append(ref_cell("references", "rust-cargo", UR, "crate-b", C_PROV2,
                                  ["crate-b/src/lib.rs"]))
    inputs = base_inputs(enumerationPlan=plan)
    install_pair(inputs, *paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
    inputs["incomingSearchAttestations"] = [
        incoming_att("references", "resolved-binding", U1, U1, [scope2("1")], [inv_symbol()])]
    r = AM.evaluate_atom({"op": "none", "relation": "references",
                          "minResolution": "resolved-binding", "endpoint": "target",
                          "filters": []}, F_SUBJ, inputs)
    got = {(c["code"], c.get("universe")) for c in r["causes"]}
    for want in (("cross-family-edge-not-owed", None), ("cross-family-edge-not-owed", UR)):
        if want not in got:
            fail(f"incoming lost cross-family shape {want}: {r['causes']}")
    expect_value(r, "true", "cross-family-disclosures-are-not-blocking")


def test_same_family_unavailable_blocks_incoming_only():
    """A same-family unavailable binding is blocking incoming and leaves outgoing alone."""
    plan = plan_one(cap="references")
    plan["cells"].append(ref_cell("references", "ts-tsconfig", None, "pkg-b", C_PROV2,
                                  ["pkg-b/src/b.ts"]))
    inputs = base_inputs(enumerationPlan=plan)
    install_pair(inputs, *paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
    inputs["incomingSearchAttestations"] = [
        incoming_att("references", "resolved-binding", U1, U1, [scope2("1")], [inv_symbol()])]
    out = AM.evaluate_atom({"op": "none", "relation": "references",
                            "minResolution": "resolved-binding", "filters": []}, F_SUBJ, inputs)
    expect_value(out, "true", "same-family-unavailable-outgoing")
    if "unavailable-program-binding" in {c["code"] for c in out["causes"]}:
        fail("unavailable-program-binding is incoming only")
    inc = AM.evaluate_atom({"op": "none", "relation": "references",
                            "minResolution": "resolved-binding", "endpoint": "target",
                            "filters": []}, F_SUBJ, inputs)
    expect_value(inc, "indeterminate", "same-family-unavailable-incoming")
    if "unavailable-program-binding" not in {c["code"] for c in inc["causes"]}:
        fail(f"incoming must disclose the unavailable binding: {inc['causes']}")


def multi_scope_dep_inputs(reverse_mapping):
    """One reachability partition, and TWO same-kind `calls` scopes over the SAME subject.

    With reverse_mapping the lower scope id carries the HIGHER Coverage id, so a scope-ordered walk
    would hand the fold a descending Coverage list. Aligned tags conceal that branch.
    """
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    install_pair(inputs, *paired("reachability", "from-resolved-calls", U1, U1, [F_SYM], tag="1"))
    s_lo, sc_lo = scope("calls", "resolved-callee", U1, U1, [F_SYM], sid="5")
    s_hi, sc_hi = scope("calls", "resolved-callee", U1, U1, [F_SYM], sid="6")
    c_lo, cov_lo = coverage("calls", "resolved-callee", U1, U1, cov="unknown", cid="2")
    c_hi, cov_hi = coverage("calls", "resolved-callee", U1, U1, cov="unknown", cid="3")
    cov_lo["entry"]["deficiency"] = cov_hi["entry"]["deficiency"] = "input-closure-incomplete"
    cov_lo["entry"]["nativeCause"] = "lockfile-missing"
    cov_hi["entry"]["nativeCause"] = "no-program-unit"
    inputs["scopes"].update({s_lo: sc_lo, s_hi: sc_hi})
    inputs["coverages"].update({c_lo: cov_lo, c_hi: cov_hi})
    if reverse_mapping:
        inputs["coverageScopes"].update({c_hi: s_lo, c_lo: s_hi})
    else:
        inputs["coverageScopes"].update({c_lo: s_lo, c_hi: s_hi})
    return inputs


def test_same_kind_multi_scope_selection_is_ascending_coverage_id():
    """Combined selection is sorted after pairing, so scope order cannot flip the typed carrier."""
    for endpoint in ("source", "target"):
        atom = {"op": "all-covered", "relation": "reachability",
                "minResolution": "from-resolved-calls", "endpoint": endpoint, "filters": []}
        for reverse in (False, True):
            label = f"{endpoint}/reverse={reverse}"
            r = AM.evaluate_atom(atom, F_SUBJ, multi_scope_dep_inputs(reverse))
            expect_value(r, "indeterminate", label)
            _expect_folded_carrier(r, label, "lockfile-missing")


def test_dep_fold_replaces_whole_records_and_keeps_ties():
    """resolutionCompleteness/closedWorld replace WHOLE on strictly worse rank; ties keep the first."""
    c_lo, cov_lo = coverage("calls", "resolved-callee", U1, U1, cov="unknown", cid="2")
    c_hi, cov_hi = coverage("calls", "resolved-callee", U1, U1, cov="unknown", cid="3")
    cov_lo["entry"].update({
        "confidenceMillionths": 900000,
        "derivationKinds": ["declared"],
        "rungUnavailableBecause": "low-record",
        "resolutionCompleteness": {"state": "partial", "attempted": True,
                                   "examinedExhaustive": False, "stageTerminal": "budget-exhausted",
                                   "unresolvedEdgeCount": 7,
                                   "unresolvedEdgeClasses": ["computed-member-access",
                                                             "dynamic-import-nonliteral"]},
        "closedWorld": {**CW_CLOSED, "exportsClosed": "open", "entryPointsRecognized": "all"},
    })
    cov_hi["entry"].update({
        "confidenceMillionths": 800000,
        "derivationKinds": ["compiler-inferred"],
        "rungUnavailableBecause": "high-record",
        "resolutionCompleteness": {"state": "incomplete", "attempted": True,
                                   "examinedExhaustive": True, "stageTerminal": "complete",
                                   "unresolvedEdgeCount": 1,
                                   "unresolvedEdgeClasses": ["computed-member-access"]},
        "closedWorld": {**CW_CLOSED, "exportsClosed": "open", "entryPointsRecognized": "none"},
    })
    folded, cited = AM._conservative_entry("calls", [(c_lo, cov_lo), (c_hi, cov_hi)])
    rc, cw = folded["resolutionCompleteness"], folded["closedWorld"]
    if rc != cov_hi["entry"]["resolutionCompleteness"]:
        fail(f"resolutionCompleteness must be replaced WHOLE by the worse-state record: {rc}")
    if cw != cov_lo["entry"]["closedWorld"]:
        fail(f"closedWorld tie must retain the first record whole: {cw}")
    if folded["derivationKinds"] != ["declared", "compiler-inferred"]:
        fail(f"derivationKinds must be the ordered union: {folded['derivationKinds']}")
    if folded["rungUnavailableBecause"] != "low-record":
        fail(f"unfolded fields keep the first partition: {folded['rungUnavailableBecause']!r}")
    if folded["confidenceMillionths"] != 800000:
        fail(f"confidenceMillionths must be the minimum: {folded['confidenceMillionths']}")
    if (folded["deficiency"], folded["nativeCause"]) != (None, None):
        fail(f"no partition carried a deficiency, so the carrier stays empty: {folded}")
    if cited != [c_lo, c_hi]:
        fail(f"every folded partition is cited: {cited}")


C_PROV3 = "closure2:" + "dd" * 32
U2_G = "ts-symbol:pkg-b/src/b.ts#g"
U2_H = "ts-symbol:pkg-c/src/c.ts#h"
REF_IN = {"relation": "references", "minResolution": "resolved-binding", "endpoint": "target", "filters": []}


def _codes(r):
    return {(c["code"], c.get("universe")) for c in r["causes"]}


def cell_u1(cap="references", kinds=None):
    return ("u1", ref_cell(cap, "ts-tsconfig", U1, "pkg-a", C_PROV, ["src/a.ts"], kinds=kinds))


def cell_u1_unavailable():
    return ("u1-unavailable", ref_cell("references", "ts-tsconfig", None, "pkg-a", C_PROV, ["src/a.ts"]))


def cell_u2(cap="references", kinds=None):
    return ("u2", ref_cell(cap, "ts-tsconfig", U2, "pkg-b", C_PROV2, ["pkg-b/src/b.ts"], kinds=kinds))


def cell_u2b():
    return ("u2b", ref_cell("references", "ts-tsconfig", U2, "pkg-c", C_PROV3, ["pkg-c/src/c.ts"]))


def cell_rust():
    return ("rust", ref_cell("references", "rust-cargo", UR, "crate", C_PROV2, ["crate/src/lib.rs"]))


def cell_rust_unavailable():
    return ("rust-unavailable", ref_cell("references", "rust-cargo", None, "crate-u", C_PROV2,
                                         ["crate-u/src/lib.rs"]))


def cell_unknown_family_unavailable():
    """Synthetic atom-api shape: an unregistered languageMode, which the enumeration-plan schema refuses."""
    return ("unknown-family", ref_cell("references", "unregistered-mode", None, "odd", C_PROV2, ["odd/x"]))


def subject_program_inputs(rel, rung, cells, u1=False, u2=False, u3=False, facts=None, attributions=None):
    """Subject f is inventoried at U1 through a `calls` cell, so U1 can lack a binding for `rel`.

    u1: paired U1->U1 evidence. u2 / u3: provider C_PROV2 / C_PROV3 scopes at U2->U1 with complete
    Coverage. Cells are schema-sorted and inventories address them by cellOrdinal.
    """
    keyed = [("subject-calls", ref_cell("calls", "ts-tsconfig", U1, "pkg-a", C_PROV, ["src/a.ts"]))]
    keyed += list(cells)
    keyed.sort(key=lambda kc: (kc[1]["capabilityId"], kc[1]["languageMode"], kc[1]["workspaceRoot"]))
    plan = plan_one(cap="calls")
    plan["cells"] = [c for _, c in keyed]
    ordinal = {k: n for n, (k, _) in enumerate(keyed)}
    inv_f = inv_symbol()
    inv_f["cellOrdinal"] = ordinal["subject-calls"]
    invs = [inv_f]
    for key, sym, path in (("u2", U2_G, "pkg-b/src/b.ts"), ("u2b", U2_H, "pkg-c/src/c.ts")):
        if key in ordinal:
            inv = inv_symbol(universe=U2, nid=sym, path=path, qn=sym.rsplit("#", 1)[1])
            inv["cellOrdinal"] = ordinal[key]
            invs.append(inv)
    inputs = base_inputs(enumerationPlan=plan, inventories=invs, facts=dict(facts or {}),
                         targetAttributions=dict(attributions or {}))
    inputs["closures"][C_PROV3] = {"kind": "provider"}
    if u1:
        install_pair(inputs, *paired(rel, rung, U1, U1, [F_SYM], tag="1"))
    for flag, sym, tag, closure in ((u2, U2_G, "2", C_PROV2), (u3, U2_H, "3", C_PROV3)):
        if flag:
            sid, sc = scope(rel, rung, U2, U1, [sym], sid=tag)
            sc["enumeratorClosure"] = closure
            install_pair(inputs, sid, sc, *coverage(rel, rung, U2, U1, cid=tag))
    return inputs


def test_incoming_unbound_subject_universe_is_blocking():
    """MUST-34-01 / section 4 I1: U unbound while a same-family U2 is fully evidenced is unknown."""
    inputs = subject_program_inputs("references", "resolved-binding", [cell_u2()], u2=True)
    for op, extra in (("none", {}), ("exists", {}), ("count-at-most", {"n": 0}), ("all-covered", {})):
        r = AM.evaluate_atom({**REF_IN, "op": op, **extra}, F_SUBJ, inputs)
        expect_value(r, "indeterminate", f"unbound-U1/{op}")
        if {"code": "selector-unbound", "evidenceKind": None, "nativeCause": None} not in r["causes"]:
            fail(f"unbound-U1/{op}: I1 record must be selector-unbound with the universe key omitted: {r['causes']}")
        if cov2("2") not in r["coverageIds"] or scope2("2") not in r["scopeIds"]:
            fail(f"unbound-U1/{op}: U2's own account must still be cited: {r['coverageIds']} {r['scopeIds']}")
    out = AM.evaluate_atom({**REF_IN, "op": "none", "endpoint": "source"}, F_SUBJ, inputs)
    if _codes(out) != {("selector-unbound", None)}:
        fail(f"outgoing step 1 emits the same record: {out['causes']}")


def test_incoming_unbound_subject_universe_foreign_family_only():
    """Foreign-family-only owed bindings leave the subject's own program unsearched: unknown, disclosures kept."""
    for label, cells, disclosures in (
            ("available", [cell_rust()], {("cross-family-edge-not-owed", UR)}),
            ("unavailable", [cell_rust_unavailable()], {("cross-family-edge-not-owed", None)}),
            ("both", [cell_rust(), cell_rust_unavailable()],
             {("cross-family-edge-not-owed", UR), ("cross-family-edge-not-owed", None)})):
        inputs = subject_program_inputs("references", "resolved-binding", cells)
        for op in ("none", "exists"):
            r = AM.evaluate_atom({**REF_IN, "op": op}, F_SUBJ, inputs)
            expect_value(r, "indeterminate", f"foreign-only-{label}/{op}")
            if _codes(r) != disclosures | {("selector-unbound", None)}:
                fail(f"foreign-only-{label}/{op}: causes {r['causes']}")


def test_incoming_bound_subject_universe_and_p2_unchanged():
    """I1 fires only when U is unbound: a bound U keeps its own causes, and P2 still returns first."""
    rel, rung = "references", "resolved-binding"
    r = AM.evaluate_atom({**REF_IN, "op": "none"}, F_SUBJ,
                         subject_program_inputs(rel, rung, [cell_u1(), cell_u2()], u1=True, u2=True))
    expect_value(r, "true", "bound-evidenced")
    if r["causes"]:
        fail(f"bound-evidenced: {r['causes']}")
    r = AM.evaluate_atom({**REF_IN, "op": "none"}, F_SUBJ,
                         subject_program_inputs(rel, rung, [cell_u1(), cell_u2()], u2=True))
    expect_value(r, "indeterminate", "bound-unevidenced")
    if _codes(r) != {("source-target-search-unattested", U1), ("uncovered-expected-source-subject", U1)}:
        fail(f"bound-unevidenced keeps its own causes and no I1: {r['causes']}")
    r = AM.evaluate_atom({**REF_IN, "op": "none"}, F_SUBJ, subject_program_inputs(rel, rung, []))
    expect_value(r, "indeterminate", "no-binding-anywhere")
    if _codes(r) != {("missing-relation-coverage", None)}:
        fail(f"P2 returns before I1: {r['causes']}")


def test_incoming_unbound_subject_universe_with_unavailable_obligations():
    """An unavailable binding never satisfies I1; P1's unavailable-program-binding and I1 are both kept."""
    rel, rung = "references", "resolved-binding"
    for label, cells, kwargs, want in (
            ("U1-unavailable+U2", [cell_u1_unavailable(), cell_u2()], {"u2": True},
             {("unavailable-program-binding", None), ("selector-unbound", None)}),
            ("U1-bound+unknown-family-unavailable", [cell_u1(), cell_unknown_family_unavailable()], {"u1": True},
             {("unavailable-program-binding", None)}),
            ("U1-unbound+unknown-family-unavailable", [cell_unknown_family_unavailable()], {},
             {("unavailable-program-binding", None), ("selector-unbound", None)})):
        r = AM.evaluate_atom({**REF_IN, "op": "none"}, F_SUBJ, subject_program_inputs(rel, rung, cells, **kwargs))
        expect_value(r, "indeterminate", label)
        if _codes(r) != want:
            fail(f"{label}: causes {r['causes']}")


def incoming_import_fact(fid, importer):
    return {
        "factId": fid, "relation": "imports", "resolution": "resolved-target",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV,
        "confidenceMillionths": 1000000,
        "payload": {"importer": importer, "specifier": "./a", "resolvedTarget": "file:src/a.ts"},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def test_incoming_unbound_subject_universe_keeps_known_matches():
    """I1 retracts no evidence: known facts still decide exists/none and an exceeded count-at-most."""
    rel, rung = "imports", "resolved-target"
    f1, f2 = fact2("1"), fact2("2")
    facts = {f1: incoming_import_fact(f1, F_SYM), f2: incoming_import_fact(f2, "ts-symbol:src/a.ts#f2")}
    attrs = {fid: sidecar(fid, "file:src/a.ts", kind="file", occupancy="first-party", evaluation="src/a.ts")
             for fid in facts}
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    for bound in (False, True):
        cells = [cell_u2(cap="imports", kinds=["symbol", "file"])]
        if bound:
            cells.append(cell_u1(cap="imports", kinds=["symbol", "file"]))
        inputs = subject_program_inputs(rel, rung, cells, u1=bound, u2=True, facts=facts, attributions=attrs)
        inv = inv_file()
        inv["cellOrdinal"] = [n for n, c in enumerate(inputs["enumerationPlan"]["cells"])
                              if c["capabilityId"] == "calls"][0]
        inputs["inventories"].append(inv)
        want = {"none": "false", "exists": "true", "count-at-most-1": "false",
                "count-at-most-2": "true" if bound else "indeterminate",
                "all-covered": "true" if bound else "indeterminate"}
        for key, op, extra in (("none", "none", {}), ("exists", "exists", {}),
                               ("count-at-most-1", "count-at-most", {"n": 1}),
                               ("count-at-most-2", "count-at-most", {"n": 2}),
                               ("all-covered", "all-covered", {})):
            r = AM.evaluate_atom({"relation": rel, "minResolution": rung, "endpoint": "target",
                                  "filters": [], "op": op, **extra}, subj, inputs)
            expect_value(r, want[key], f"known/bound={bound}/{key}")
            if r["knownFactIds"] != sorted([f1, f2]):
                fail(f"known/bound={bound}/{key}: known facts must be retained: {r['knownFactIds']}")
            if (("selector-unbound", None) in _codes(r)) == bound:
                fail(f"known/bound={bound}/{key}: selector-unbound presence wrong: {r['causes']}")


def test_incoming_unbound_subject_universe_multi_provider_order_independent():
    """I1 sits beside each provider's own account, with one result for every insertion order."""
    from itertools import permutations
    rel, rung = "references", "resolved-binding"
    base = subject_program_inputs(rel, rung, [cell_u2(), cell_u2b(), cell_rust()], u2=True)
    atom = {**REF_IN, "op": "none"}
    results = set()
    for order in permutations(base["inventories"]):
        for reverse in (False, True):
            inputs = copy.deepcopy(base)
            inputs["inventories"] = copy.deepcopy(list(order))
            if reverse:
                for key in ("scopes", "coverages", "coverageScopes"):
                    inputs[key] = dict(reversed(list(inputs[key].items())))
            results.add(json.dumps(AM.evaluate_atom(atom, F_SUBJ, inputs), sort_keys=True))
    if len(results) != 1:
        fail(f"multi-provider result depends on insertion order: {len(results)} results")
    r = json.loads(results.pop())
    expect_value(r, "indeterminate", "multi-provider-one-unevidenced")
    if _codes(r) != {("selector-unbound", None), ("cross-family-edge-not-owed", UR),
                     ("source-target-search-unattested", U2), ("uncovered-expected-source-subject", U2)}:
        fail(f"multi-provider-one-unevidenced: causes {r['causes']}")
    r = AM.evaluate_atom(atom, F_SUBJ,
                         subject_program_inputs(rel, rung, [cell_u2(), cell_u2b(), cell_rust()], u2=True, u3=True))
    expect_value(r, "indeterminate", "multi-provider-both-evidenced")
    if _codes(r) != {("selector-unbound", None), ("cross-family-edge-not-owed", UR)}:
        fail(f"multi-provider-both-evidenced: causes {r['causes']}")
    r = AM.evaluate_atom(atom, F_SUBJ, subject_program_inputs(
        rel, rung, [cell_u1(), cell_u2(), cell_u2b(), cell_rust()], u1=True, u2=True, u3=True))
    expect_value(r, "true", "multi-provider-U1-bound")
    if _codes(r) != {("cross-family-edge-not-owed", UR)}:
        fail(f"multi-provider-U1-bound: causes {r['causes']}")


def test_scope_without_enumerator_closure_refuses_at_atom_api():
    """A-12: absent and null enumeratorClosure both fail the subject-scope carrier; no untagged fallback."""
    for mode in ("absent", "null"):
        for endpoint in ("target", "source"):
            for with_coverage in (False, True):
                inputs = base_inputs()
                sid, sc = scope("references", "resolved-binding", U1, U1, [F_SYM], sid="1")
                if mode == "absent":
                    del sc["enumeratorClosure"]
                else:
                    sc["enumeratorClosure"] = None
                inputs["scopes"][sid] = sc
                if with_coverage:
                    cid, cov = coverage("references", "resolved-binding", U1, U1, cid="1")
                    inputs["coverages"][cid] = cov
                    inputs["coverageScopes"][cid] = sid

                def go():
                    AM.evaluate_atom({**REF_IN, "op": "none", "endpoint": endpoint}, F_SUBJ, inputs)
                expect_admit(go, "ATOM_NATIVE_CARRIER", f"untagged/{mode}/{endpoint}/coverage={with_coverage}")
        # Global admission: an attestation naming such a scope refuses even when the evaluated atom's
        # own relation never pairs it, so the untagged join fallback admits nothing.
        plan = plan_one(cap="references")
        plan["cells"] = sorted(plan["cells"] + [ref_cell("calls", "ts-tsconfig", U1, ".", C_PROV, ["src/a.ts"])],
                               key=lambda c: (c["capabilityId"], c["languageMode"], c["workspaceRoot"]))
        inv = inv_symbol()
        inv["cellOrdinal"] = [n for n, c in enumerate(plan["cells"]) if c["capabilityId"] == "calls"][0]
        inputs = base_inputs(enumerationPlan=plan, inventories=[inv])
        install_pair(inputs, *paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
        sid, sc = scope("calls", "resolved-callee", U1, U1, [F_SYM], sid="9")
        if mode == "absent":
            del sc["enumeratorClosure"]
        else:
            sc["enumeratorClosure"] = None
        inputs["scopes"][sid] = sc
        inputs["incomingSearchAttestations"] = [incoming_att("calls", "resolved-callee", U1, U1, [sid], [inv])]
        expect_admit(lambda: AM.admit_atom_inputs(inputs), "ATOM_NATIVE_CARRIER", f"untagged/{mode}/named-by-attestation")


def empty_program_inputs(scope_mode, attest=False):
    """U1 fully evidenced, plus a second same-family selected program at U2 whose inventory is empty."""
    plan = plan_one(cap="references")
    plan["cells"].append(ref_cell("references", "ts-tsconfig", U2, "pkg-empty", C_PROV2, ["pkg-empty/src/index.ts"]))
    empty = inv_symbol(universe=U2, nid="ts-symbol:pkg-empty/src/index.ts#unused",
                       path="pkg-empty/src/index.ts", qn="unused")
    empty.update({"cellOrdinal": 1, "rows": [], "examinedPaths": ["pkg-empty/src/index.ts"]})
    inputs = base_inputs(enumerationPlan=plan, inventories=[inv_symbol(), empty])
    install_pair(inputs, *paired("references", "resolved-binding", U1, U1, [F_SYM], tag="1"))
    if scope_mode in ("empty-scope", "empty-scope-paired"):
        sid, sc = scope("references", "resolved-binding", U2, U1, [], sid="7")
        sc["enumeratorClosure"] = C_PROV2
        inputs["scopes"][sid] = sc
        if scope_mode == "empty-scope-paired":
            cid, cov = coverage("references", "resolved-binding", U2, U1, cid="7")
            inputs["coverages"][cid] = cov
            inputs["coverageScopes"][cid] = sid
    if attest:
        refs = [scope2("7")] if scope_mode.startswith("empty-scope") else []
        inputs["incomingSearchAttestations"] = [
            incoming_att("references", "resolved-binding", U2, U1, refs, [empty], providerClosure=C_PROV2)]
    return inputs


def test_scopeless_provider_group_admission_boundary():
    """A-12: a scope-less group has no admissible attestation; an explicit empty-subject scope closes it."""
    atom = {**REF_IN, "op": "none"}
    r = AM.evaluate_atom(atom, F_SUBJ, empty_program_inputs("none"))
    expect_value(r, "indeterminate", "no-scope")
    if _codes(r) != {("source-target-search-unattested", U2)}:
        fail(f"no-scope: causes {r['causes']}")

    def attest_without_scope():
        AM.evaluate_atom(atom, F_SUBJ, empty_program_inputs("none", attest=True))
    expect_admit(attest_without_scope, "INCOMING_SEARCH_SCHEMA", "no-scope-attestation-is-global-refusal")
    borrowed = empty_program_inputs("none", attest=True)
    borrowed["incomingSearchAttestations"][0]["scopeRefs"] = [scope2("1")]
    expect_admit(lambda: AM.admit_atom_inputs(borrowed), "INCOMING_SEARCH_SCOPE_MISJOIN",
                 "no-owned-scopes-borrowed-scope-is-global-refusal")
    r = AM.evaluate_atom(atom, F_SUBJ, empty_program_inputs("empty-scope"))
    expect_value(r, "indeterminate", "empty-scope-unpaired")
    if _codes(r) != {("scope-without-coverage", U2)}:
        fail(f"empty-scope-unpaired: causes {r['causes']}")
    r = AM.evaluate_atom(atom, F_SUBJ, empty_program_inputs("empty-scope-paired"))
    expect_value(r, "true", "empty-scope-with-complete-coverage")
    if r["causes"] or cov2("7") not in r["coverageIds"]:
        fail(f"empty-scope-with-complete-coverage: {r['causes']} {r['coverageIds']}")
    r = AM.evaluate_atom(atom, F_SUBJ, empty_program_inputs("empty-scope", attest=True))
    expect_value(r, "true", "empty-scope-with-qualifying-attestation")
    if r["causes"]:
        fail(f"empty-scope-with-qualifying-attestation: {r['causes']}")


REACH_ALL = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
DEP_SCOPE_MUTATIONS = (
    ("sourceUniverse", "absent", None), ("sourceUniverse", "null", None), ("sourceUniverse", "different", U2),
    ("relation", "absent", None), ("relation", "null", None), ("relation", "different", "references"),
    ("resolution", "absent", None), ("resolution", "null", None),
    ("resolution", "different", "resolved-binding"), ("resolution", "different", "syntactic-callee-name"),
)


def exact_dep_inputs():
    """reachability@from-resolved-calls for f, plus its calls@resolved-callee dependency scope 2 and Coverage 2."""
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    install_pair(inputs, *paired("reachability", "from-resolved-calls", U1, U1, [F_SYM], tag="1"))
    install_pair(inputs, *paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="2"))
    return inputs


def mutate_dep_scope(inputs, field, mode, other):
    sc = inputs["scopes"][scope2("2")]
    if mode == "absent":
        sc.pop(field)
    else:
        sc[field] = None if mode == "null" else other
    return inputs


def test_dependency_mapping_to_non_exact_scope_is_absent():
    """A coverageScopes mapping to a dependency scope outside the exact (relation, rung, S) pairs nothing."""
    for endpoint in ("source", "target"):
        atom = {**REACH_ALL, "endpoint": endpoint}
        absent = exact_dep_inputs()
        absent["scopes"].pop(scope2("2"))
        absent["coverageScopes"].pop(cov2("2"))
        want = AM.evaluate_atom(atom, F_SUBJ, absent)
        expect_value(want, "indeterminate", f"dependency-absent/{endpoint}")
        for field, mode, other in DEP_SCOPE_MUTATIONS:
            label = f"{endpoint}/{field}/{mode}" + (f"={other}" if other else "")
            r = AM.evaluate_atom(atom, F_SUBJ, mutate_dep_scope(exact_dep_inputs(), field, mode, other))
            expect_value(r, "indeterminate", label)
            if cov2("2") in r["coverageIds"]:
                fail(f"{label}: a non-exact dependency scope must not cite its Coverage: {r['coverageIds']}")
            if ("coverage-unknown", U1) not in _codes(r) or "required-relation-missing" not in r["nativeDeficiencies"]:
                fail(f"{label}: causes {r['causes']} nativeDeficiencies {r['nativeDeficiencies']}")
            if (r["causes"], r["nativeDeficiencies"], r["coverageIds"]) != (
                    want["causes"], want["nativeDeficiencies"], want["coverageIds"]):
                fail(f"{label}: must equal the dependency-absent result, not a refusal or a partial pairing")


def test_dependency_exact_scope_pairing_and_carrier_refusal():
    """Exact dependency scopes pair by mapping or commitment; the non-exact rule agrees with exact-unrelated scopes."""
    r = AM.evaluate_atom(REACH_ALL, F_SUBJ, exact_dep_inputs())
    expect_value(r, "true", "exact-mapped")
    if cov2("2") not in r["coverageIds"]:
        fail(f"exact-mapped must cite the dependency: {r['coverageIds']}")
    commit_only = exact_dep_inputs()
    commit_only["coverageScopes"].pop(cov2("2"))
    commit_only["coverages"][cov2("2")]["key"]["subjectScopeCommitment"] = AM._derive_scope_commitment(
        commit_only["scopes"][scope2("2")])
    r = AM.evaluate_atom(REACH_ALL, F_SUBJ, commit_only)
    expect_value(r, "true", "exact-commitment-only")
    if cov2("2") not in r["coverageIds"]:
        fail(f"exact-commitment-only must cite the dependency: {r['coverageIds']}")
    neither = exact_dep_inputs()
    neither["coverageScopes"].pop(cov2("2"))
    expect_value(AM.evaluate_atom(REACH_ALL, F_SUBJ, neither), "indeterminate", "exact-scope-unpaired")
    other_subject = exact_dep_inputs()
    other_subject["scopes"][scope2("2")]["subjects"] = [G_SYM]
    expect_value(AM.evaluate_atom(REACH_ALL, F_SUBJ, other_subject), "indeterminate", "exact-scope-other-subject")
    beside = mutate_dep_scope(exact_dep_inputs(), "sourceUniverse", "different", U2)
    s3, sc3 = scope("calls", "resolved-callee", U1, U1, [G_SYM], sid="3")
    beside["scopes"][s3] = sc3
    expect_value(AM.evaluate_atom(REACH_ALL, F_SUBJ, beside), "indeterminate", "non-exact-beside-exact-unrelated")
    missing = exact_dep_inputs()
    missing["scopes"][scope2("2")].pop("enumeratorClosure")
    expect_admit(lambda: AM.evaluate_atom(REACH_ALL, F_SUBJ, missing), "ATOM_NATIVE_CARRIER",
                 "exact-dependency-scope-missing-carrier-field-refuses")


def incoming_disjoint_dep_inputs():
    """Incoming primary scope over {f, g}; two DISJOINT exact calls scopes (one partition, no overlap)."""
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"),
                         inventories=[inv_symbol(), inv_symbol(nid=G_SYM, qn="g")])
    install_pair(inputs, *paired("reachability", "from-resolved-calls", U1, U1, [F_SYM, G_SYM], tag="1"))
    install_pair(inputs, *paired("calls", "resolved-callee", U1, U1, [F_SYM], tag="2"))
    sg, scg = scope("calls", "resolved-callee", U1, U1, [G_SYM], sid="4")
    cg, cvg = coverage("calls", "resolved-callee", U1, U1, cid="4")
    cvg["key"]["subjectScopeCommitment"] = AM._derive_scope_commitment(scg)
    inputs["scopes"][sg] = scg
    inputs["coverages"][cg] = cvg
    return inputs


def test_dependency_incoming_disjoint_scopes_order_independent():
    """Mapped and commitment-paired exact dependency scopes give one result for every insertion order."""
    from itertools import permutations
    atom = {**REACH_ALL, "endpoint": "target"}
    results = set()
    for order in permutations(("scopes", "coverages", "coverageScopes")):
        for reverse in (False, True):
            inputs = incoming_disjoint_dep_inputs()
            if reverse:
                for key in order:
                    inputs[key] = dict(reversed(list(inputs[key].items())))
            results.add(json.dumps(AM.evaluate_atom(atom, F_SUBJ, inputs), sort_keys=True))
    if len(results) != 1:
        fail(f"dependency pairing depends on insertion order: {len(results)} results")
    r = json.loads(results.pop())
    expect_value(r, "true", "incoming-disjoint-dependency-scopes")
    if r["coverageIds"] != [cov2("1"), cov2("2"), cov2("4")]:
        fail(f"both dependency partitions must be cited once, ascending: {r['coverageIds']}")


def reachability_fact(fid):
    return {
        "factId": fid, "relation": "reachability", "resolution": "from-resolved-calls",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV, "confidenceMillionths": 1000000,
        "payload": {"origin": F_SYM, "reachable": G_SYM},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def test_dependency_non_exact_scope_keeps_known_matches():
    """An absent dependency retracts no evidence: a known fact still decides exists/none/exceeded count-at-most."""
    fid = fact2("1")
    for exact in (True, False):
        inputs = exact_dep_inputs() if exact else mutate_dep_scope(exact_dep_inputs(), "sourceUniverse", "absent", None)
        inputs["facts"] = {fid: reachability_fact(fid)}
        want = {"exists": "true", "none": "false", "count-at-most-0": "false",
                "count-at-most-1": "true" if exact else "indeterminate",
                "all-covered": "true" if exact else "indeterminate"}
        for key, op, extra in (("exists", "exists", {}), ("none", "none", {}),
                               ("count-at-most-0", "count-at-most", {"n": 0}),
                               ("count-at-most-1", "count-at-most", {"n": 1}), ("all-covered", "all-covered", {})):
            r = AM.evaluate_atom({**REACH_ALL, "op": op, **extra}, F_SUBJ, inputs)
            expect_value(r, want[key], f"known/exact={exact}/{key}")
            if r["knownFactIds"] != [fid]:
                fail(f"known/exact={exact}/{key}: known fact must be retained: {r['knownFactIds']}")


def test_dependency_different_kind_whole_source_unchanged():
    """clones -> declares is a different kind: whole-source Coverage selection never consults dependency scopes."""
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "all-covered", "relation": "clones", "minResolution": "normalized-body-hash", "filters": []}

    def clones_inputs(mode):
        inputs = base_inputs(enumerationPlan=plan_one(cap="clones-fact", kinds=["file"]), inventories=[inv_file()])
        install_pair(inputs, *paired("clones", "normalized-body-hash", U1, U1, ["src/a.ts"], tag="1"))
        if mode != "no-declares":
            cid, cov = coverage("declares", "syntactic", U1, U1, cid="5")
            inputs["coverages"][cid] = cov
            if mode == "mapped-to-wrong-universe-scope":
                sid, sc = scope("declares", "syntactic", U2, U1, [F_SYM], sid="5")
                inputs["scopes"][sid] = sc
                inputs["coverageScopes"][cid] = sid
        return inputs

    expect_value(AM.evaluate_atom(atom, subj, clones_inputs("no-declares")), "indeterminate", "clones-no-declares")
    for mode in ("unscoped", "mapped-to-wrong-universe-scope"):
        r = AM.evaluate_atom(atom, subj, clones_inputs(mode))
        expect_value(r, "true", f"clones-{mode}")
        if cov2("5") not in r["coverageIds"]:
            fail(f"clones-{mode}: whole-source dependency must be cited: {r['coverageIds']}")


def test_dependency_rule_applies_at_every_depth_synthetic_graph():
    """Synthetic DEPENDS_ON extension calls -> declares@syntactic, restored afterwards (helper-graph evidence)."""
    saved = copy.deepcopy(AM.N.DEPENDS_ON)
    try:
        AM.N.DEPENDS_ON["calls"] = [{"relation": "declares", "minResolution": "syntactic"}]
        inputs = exact_dep_inputs()
        install_pair(inputs, *paired("declares", "syntactic", U1, U1, [F_SYM], tag="6"))
        r = AM.evaluate_atom(REACH_ALL, F_SUBJ, inputs)
        expect_value(r, "true", "depth-2-exact")
        if cov2("6") not in r["coverageIds"]:
            fail(f"depth-2-exact must cite the second-level dependency: {r['coverageIds']}")
        inputs["scopes"][scope2("6")]["sourceUniverse"] = U2
        r = AM.evaluate_atom(REACH_ALL, F_SUBJ, inputs)
        expect_value(r, "indeterminate", "depth-2-wrong-universe")
        if cov2("6") in r["coverageIds"]:
            fail(f"depth-2-wrong-universe must not cite the second-level dependency: {r['coverageIds']}")
    finally:
        AM.N.DEPENDS_ON.clear()
        AM.N.DEPENDS_ON.update(saved)


H_SYM = "ts-symbol:src/a.ts#h"
F_DEP = ([F_SYM], "2", "paired")
G_DEP = ([G_SYM], "4", "paired")


def totality_inputs(partitions, deps, attest=False):
    """Incoming reachability over primary partitions of {f, g} plus same-kind calls dependency partitions.

    partitions: subject lists, one primary scope each (tags 1, a, b); with attest=False each has complete
    S->U Coverage, with attest=True none has and one qualifying attestation names all of them.
    deps: (subjects, tag, variant), variant in paired | no-coverage | other-target | wrong-universe |
    unknown-carrier.
    """
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"),
                         inventories=[inv_symbol(), inv_symbol(nid=G_SYM, qn="g")])
    sids = []
    for n, subjects in enumerate(partitions):
        sid, sc = scope("reachability", "from-resolved-calls", U1, U1, subjects, sid="1ab"[n])
        sids.append(sid)
        if attest:
            inputs["scopes"][sid] = sc
        else:
            install_pair(inputs, sid, sc, *coverage("reachability", "from-resolved-calls", U1, U1, cid="1ab"[n]))
    if attest:
        inputs["incomingSearchAttestations"] = [incoming_att("reachability", "from-resolved-calls", U1, U1, sids,
                                                             inputs["inventories"])]
    for subjects, tag, variant in deps:
        target = U2 if variant == "other-target" else U1
        sid, sc = scope("calls", "resolved-callee", U1, target, subjects, sid=tag)
        if variant == "wrong-universe":
            sc["sourceUniverse"] = U2
        inputs["scopes"][sid] = sc
        if variant == "no-coverage":
            continue
        cid, cov = coverage("calls", "resolved-callee", U1, target, cid=tag,
                            cov="unknown" if variant == "unknown-carrier" else "complete")
        if variant == "unknown-carrier":
            cov["entry"]["deficiency"], cov["entry"]["nativeCause"] = "input-closure-incomplete", "lockfile-missing"
        inputs["coverages"][cid] = cov
        inputs["coverageScopes"][cid] = sid
    return inputs


def test_dependency_totality_regrouping_invariant():
    """Splitting incoming primary {f, g} into disjoint partitions cannot change the answer or its causes."""
    atom = {**REACH_ALL, "endpoint": "target"}
    for label, deps, want in (("f-only", [F_DEP], "indeterminate"), ("g-only", [G_DEP], "indeterminate"),
                              ("f-and-g", [F_DEP, G_DEP], "true")):
        merged = AM.evaluate_atom(atom, F_SUBJ, totality_inputs([[F_SYM, G_SYM]], deps))
        split = AM.evaluate_atom(atom, F_SUBJ, totality_inputs([[F_SYM], [G_SYM]], deps))
        expect_value(merged, want, f"{label}/merged")
        expect_value(split, want, f"{label}/split")
        if (merged["causes"], merged["nativeDeficiencies"]) != (split["causes"], split["nativeDeficiencies"]):
            fail(f"{label}: regrouping changed causes {merged['causes']} {merged['nativeDeficiencies']} "
                 f"vs {split['causes']} {split['nativeDeficiencies']}")
        if want == "indeterminate" and "required-relation-missing" not in merged["nativeDeficiencies"]:
            fail(f"{label}: an uncovered owed subject must answer required-relation-missing: {merged['nativeDeficiencies']}")


def test_dependency_totality_missing_subject_and_full_cover():
    """Every way g can lack a dependency leaves incoming unknown; f's actual evidence stays cited; full covers close."""
    atom_in = {**REACH_ALL, "endpoint": "target"}
    for variant, g_dep in (("absent", None), ("scope-without-coverage", ([G_SYM], "4", "no-coverage")),
                           ("coverage-at-other-target", ([G_SYM], "4", "other-target")),
                           ("wrong-universe-scope", ([G_SYM], "4", "wrong-universe")),
                           ("unrelated-subject-only", ([H_SYM], "5", "paired"))):
        inputs = totality_inputs([[F_SYM, G_SYM]], [F_DEP] + ([g_dep] if g_dep else []))
        r = AM.evaluate_atom(atom_in, F_SUBJ, inputs)
        expect_value(r, "indeterminate", f"missing-g/{variant}")
        if cov2("2") not in r["coverageIds"] or "required-relation-missing" not in r["nativeDeficiencies"]:
            fail(f"missing-g/{variant}: f's dependency must stay cited beside required-relation-missing: "
                 f"{r['coverageIds']} {r['nativeDeficiencies']}")
        expect_value(AM.evaluate_atom({**REACH_ALL, "endpoint": "source"}, F_SUBJ, inputs), "true",
                     f"outgoing-f-unchanged/{variant}")
    for label, deps in (("disjoint", [F_DEP, G_DEP]), ("one-spanning-scope", [([F_SYM, G_SYM], "2", "paired")]),
                        ("disjoint-plus-unrelated", [F_DEP, G_DEP, ([H_SYM], "5", "paired")])):
        r = AM.evaluate_atom(atom_in, F_SUBJ, totality_inputs([[F_SYM, G_SYM]], deps))
        expect_value(r, "true", f"full-cover/{label}")
        if cov2("5") in r["coverageIds"] or r["nativeDeficiencies"]:
            fail(f"full-cover/{label}: {r['coverageIds']} {r['nativeDeficiencies']}")


def test_dependency_totality_keeps_partial_carrier():
    """A gap never erases the actual partition's deficiency or typed carrier; it only adds the missing relation."""
    atom = {**REACH_ALL, "endpoint": "target"}
    f_unknown = ([F_SYM], "2", "unknown-carrier")
    for label, deps, want_defs in (("g-uncovered", [f_unknown], {"input-closure-incomplete", "required-relation-missing"}),
                                   ("g-covered", [f_unknown, G_DEP], {"input-closure-incomplete"})):
        r = AM.evaluate_atom(atom, F_SUBJ, totality_inputs([[F_SYM, G_SYM]], deps))
        expect_value(r, "indeterminate", f"carrier/{label}")
        if set(r["nativeDeficiencies"]) != want_defs:
            fail(f"carrier/{label}: nativeDeficiencies {r['nativeDeficiencies']}")
        cu = [c for c in r["causes"] if c["code"] == "coverage-unknown"]
        if len(cu) != 1 or cu[0].get("nativeCause") != "lockfile-missing" or cov2("2") not in r["coverageIds"]:
            fail(f"carrier/{label}: coverage-unknown {cu} coverageIds {r['coverageIds']}")


def incoming_reachability_fact(fid, origin):
    return {
        "factId": fid, "relation": "reachability", "resolution": "from-resolved-calls",
        "sourceUniverse": U1, "targetUniverse": U1, "producerClosure": C_PROV, "confidenceMillionths": 1000000,
        "payload": {"origin": origin, "reachable": F_SYM},
        "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
    }


def test_dependency_totality_known_matches_and_bounds():
    """A gap retracts no evidence: a known incoming fact still decides exists/none and an exceeded bound."""
    fid = fact2("1")
    for label, deps, needs_completeness in (("f-only", [F_DEP], "indeterminate"), ("f-and-g", [F_DEP, G_DEP], "true")):
        inputs = totality_inputs([[F_SYM, G_SYM]], deps)
        inputs["facts"] = {fid: incoming_reachability_fact(fid, G_SYM)}
        want = {"exists": "true", "none": "false", "count-at-most-0": "false",
                "count-at-most-1": needs_completeness, "all-covered": needs_completeness}
        for key, op, extra in (("exists", "exists", {}), ("none", "none", {}),
                               ("count-at-most-0", "count-at-most", {"n": 0}),
                               ("count-at-most-1", "count-at-most", {"n": 1}), ("all-covered", "all-covered", {})):
            r = AM.evaluate_atom({**REACH_ALL, "op": op, "endpoint": "target", **extra}, F_SUBJ, inputs)
            expect_value(r, want[key], f"known/{label}/{key}")
            if r["knownFactIds"] != [fid]:
                fail(f"known/{label}/{key}: known fact must be retained: {r['knownFactIds']}")


def test_dependency_totality_attestation_route_and_order():
    """The whole-source attestation view owes its owned scopes' subjects; one result for every insertion order."""
    from itertools import permutations
    atom = {**REACH_ALL, "endpoint": "target"}
    r = AM.evaluate_atom(atom, F_SUBJ, totality_inputs([[F_SYM, G_SYM]], [F_DEP], attest=True))
    expect_value(r, "indeterminate", "attested/f-only")
    if "required-relation-missing" not in r["nativeDeficiencies"] or cov2("2") not in r["coverageIds"]:
        fail(f"attested/f-only: {r['nativeDeficiencies']} {r['coverageIds']}")
    for label, deps in (("f-and-g", [F_DEP, G_DEP]), ("spanning", [([F_SYM, G_SYM], "2", "paired")])):
        expect_value(AM.evaluate_atom(atom, F_SUBJ, totality_inputs([[F_SYM, G_SYM]], deps, attest=True)),
                     "true", f"attested/{label}")
    results = set()
    for order in permutations(("scopes", "coverages", "coverageScopes", "inventories")):
        for reverse in (False, True):
            inputs = totality_inputs([[F_SYM, G_SYM]], [F_DEP, ([G_SYM], "4", "no-coverage")])
            if reverse:
                for key in order:
                    value = inputs[key]
                    inputs[key] = list(reversed(value)) if isinstance(value, list) else dict(reversed(list(value.items())))
            results.add(json.dumps(AM.evaluate_atom(atom, F_SUBJ, inputs), sort_keys=True))
    if len(results) != 1:
        fail(f"dependency totality depends on insertion order: {len(results)} results")
    expect_value(json.loads(results.pop()), "indeterminate", "ordering/g-scope-without-coverage")


def test_dependency_totality_every_depth_synthetic_graph():
    """Synthetic DEPENDS_ON extension calls -> declares@syntactic, restored afterwards (helper-graph evidence)."""
    saved = copy.deepcopy(AM.N.DEPENDS_ON)
    try:
        AM.N.DEPENDS_ON["calls"] = [{"relation": "declares", "minResolution": "syntactic"}]
        atom = {**REACH_ALL, "endpoint": "target"}
        inputs = totality_inputs([[F_SYM, G_SYM]], [F_DEP, G_DEP])
        install_pair(inputs, *paired("declares", "syntactic", U1, U1, [F_SYM], tag="6"))
        r = AM.evaluate_atom(atom, F_SUBJ, inputs)
        expect_value(r, "indeterminate", "depth-2/declares-f-only")
        if "required-relation-missing" not in r["nativeDeficiencies"] or cov2("6") not in r["coverageIds"]:
            fail(f"depth-2/declares-f-only: {r['nativeDeficiencies']} {r['coverageIds']}")
        install_pair(inputs, *paired("declares", "syntactic", U1, U1, [G_SYM], tag="8"))
        expect_value(AM.evaluate_atom(atom, F_SUBJ, inputs), "true", "depth-2/declares-f-and-g")
    finally:
        AM.N.DEPENDS_ON.clear()
        AM.N.DEPENDS_ON.update(saved)


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
    test_two_symbols_one_file_independent_partitions,
    test_symbols_not_filepath_ids,
    test_requested_rung_complete_higher_partial,
    test_calls_with_dependency_coverage,
    test_unknown_export_owes_closed_world,
    test_glob_root,
    test_portable_glob_contract,
    test_wrong_kind_none_admission,
    test_runtime_complete_unhit_filter_hit_none_true,
    test_runtime_partial_known_count_unknown,
    test_history_filtered_false_partial_known,
    test_test_result_subject_kind_filter,
    test_missing_wrapper_empty_refs,
    test_runtime_overload_ambiguous,
    test_incoming_attestation_malformed_duplicate_unselected,
    test_package_two_manifests_same_name,
    test_incoming_mixed_atom_policy,
    test_incoming_examined_exhaustive_false,
    test_unmatched_scope_beside_paired,
    test_first_party_not_in_inventory,
    test_unused_sidecar_still_admitted,
    test_duplicate_inventory_observation_not_overload,
    test_import_scope_roots_and_prefixes,
    test_incoming_caller_digest_is_not_authority,
    test_dep_other_universe_does_not_heal,
    test_history_duplicate_path_retains_all_ordinals,
    test_runtime_obs_payload_window_mismatch_refused,
    test_admit_atom_inputs_missing_wrapper_no_atom,
    test_import_flags_adapter_no_default,
    test_outgoing_exported_not_external_consumers,
    test_unrelated_dep_partition_does_not_poison_outgoing,
    test_incoming_all_source_partitions_owed,
    test_two_providers_same_u_disjoint_scopes,
    test_unavailable_foreign_family_does_not_poison,
    test_incoming_partition_s_to_v_does_not_prove_u,
    test_optional_same_family_unavailable_does_not_poison_outgoing,
    test_incoming_search_other_provider_partial_does_not_invalidate_att,
    test_incoming_unattached_target_universe_refused,
    test_runtime_unrelated_overload_is_nomatch,
    test_provider_with_no_scope_does_not_disappear,
    test_invalid_native_carrier_refuses_not_unknown,
    test_ordinary_first_party_file_import_target,
    test_ordinary_first_party_package_import_target,
    test_missing_sidecar_namespaced_file_is_unknown_not_nomatch,
    test_malformed_first_party_evaluation_id_refuses,
    test_v1_sidecar_refused,
    test_external_file_is_nomatch_on_inventory_subject,
    test_symbol_exact_id_ephemeral_without_sidecar,
    test_provider_occupancy_conflict_same_producer,
    test_different_providers_same_opaque_id_are_not_aliases,
    test_c15_ephemeral_identity_conflict_refuses,
    test_c15_agreement_same_identity_admits,
    test_c15_unknown_sidecar_keeps_ephemeral,
    test_wrong_universe_still_nomatch,
    test_outgoing_early_stop_cause_and_universe,
    test_unmatched_scope_stop_cites_every_scope_and_no_coverage,
    test_known_hit_dominates_every_outgoing_early_stop,
    test_cross_family_disclosure_survives_outgoing_selector_stop,
    test_dep_fold_carrier_is_first_partition_in_selection_order,
    test_incoming_reports_every_universe_without_early_stop,
    test_no_owed_binding_return_is_shared_by_both_endpoints,
    test_incoming_keeps_both_cross_family_shapes,
    test_same_family_unavailable_blocks_incoming_only,
    test_same_kind_multi_scope_selection_is_ascending_coverage_id,
    test_dep_fold_replaces_whole_records_and_keeps_ties,
    test_incoming_unbound_subject_universe_is_blocking,
    test_incoming_unbound_subject_universe_foreign_family_only,
    test_incoming_bound_subject_universe_and_p2_unchanged,
    test_incoming_unbound_subject_universe_with_unavailable_obligations,
    test_incoming_unbound_subject_universe_keeps_known_matches,
    test_incoming_unbound_subject_universe_multi_provider_order_independent,
    test_scope_without_enumerator_closure_refuses_at_atom_api,
    test_scopeless_provider_group_admission_boundary,
    test_dependency_mapping_to_non_exact_scope_is_absent,
    test_dependency_exact_scope_pairing_and_carrier_refusal,
    test_dependency_incoming_disjoint_scopes_order_independent,
    test_dependency_non_exact_scope_keeps_known_matches,
    test_dependency_different_kind_whole_source_unchanged,
    test_dependency_rule_applies_at_every_depth_synthetic_graph,
    test_dependency_totality_regrouping_invariant,
    test_dependency_totality_missing_subject_and_full_cover,
    test_dependency_totality_keeps_partial_carrier,
    test_dependency_totality_known_matches_and_bounds,
    test_dependency_totality_attestation_route_and_order,
    test_dependency_totality_every_depth_synthetic_graph,
]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Atom unit checks. Not full Run replay.")
    parser.add_argument("--output", default=None,
                        help="Directory for check-atoms.report.json. Default: stdout only; does not rewrite v6 receipts.")
    args = parser.parse_args(argv)
    results = []
    for fn in CASES:
        try:
            fn()
            results.append({"case": fn.__name__, "ok": True})
        except Exception as exc:  # noqa: BLE001 — collect
            results.append({"case": fn.__name__, "ok": False, "error": f"{type(exc).__name__}: {exc}"})
    ok = all(r["ok"] for r in results)
    report = {
        "standing": "atom unit checks of synthetic admitted maps; not full Run replay; not compiler qualification",
        "ok": ok,
        "passed": sum(1 for r in results if r["ok"]),
        "failed": sum(1 for r in results if not r["ok"]),
        "results": results,
    }
    print(json.dumps(report, indent=2))
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "check-atoms.report.json").write_text(json.dumps(report, indent=2) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
