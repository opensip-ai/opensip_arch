"""Discriminating atom-model checks. Not full Run replay. Not product execution."""
from __future__ import annotations

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
            producer=C_PROV, universe=U1):
    return {
        "schemaVersion": 1, "planId": PLAN, "sourceFactId": fid, "producerClosure": producer,
        "targetUniverse": universe, "targetNativeId": native,
        "kind": kind, "occupancy": occupancy, "exported": exported, "logicalPath": logical,
        "packageManifestPath": manifest,
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
        "closures": {C_PROV: {"kind": "provider"}, C_EVAL: {"kind": "evaluator"}},
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
                        "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        inventories=[inv_symbol(), inv_file()],
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
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
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
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "src/a.ts", kind="symbol", occupancy="first-party", exported="exported")},
    )
    subj = {"universe": U1, "kind": "file", "nativeSubjectId": "src/a.ts"}
    atom = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
            "endpoint": "target", "filters": []}

    def go():
        AM.evaluate_atom(atom, subj, inputs)
    expect_admit(go, "TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT", "sidecar-kind")

    inputs2 = dict(inputs)
    inputs2["targetAttributions"] = {fid: sidecar(fid, "src/a.ts", kind="file", occupancy="external")}
    def go2():
        AM.evaluate_atom(atom, subj, inputs2)
    expect_admit(go2, "TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY", "sidecar-external")

    inputs3 = dict(inputs)
    facts3 = dict(inputs["facts"])
    f3 = dict(facts3[fid])
    f3["producerClosure"] = C_EVAL
    facts3[fid] = f3
    inputs3["facts"] = facts3
    inputs3["targetAttributions"] = {fid: sidecar(fid, "src/a.ts", kind="unknown", occupancy="unknown", producer=C_EVAL)}
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
    sr, scr, cr, covr = paired("reachability", "from-resolved-calls", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    cc, covc = coverage("calls", "resolved-callee", U1, U1, state="complete", cid="2")
    inputs = base_inputs(enumerationPlan=plan_one(cap="reachability"))
    install_pair(inputs, sr, scr, cr, covr)
    inputs["coverages"][cc] = covc
    atom = {"op": "all-covered", "relation": "reachability", "minResolution": "from-resolved-calls", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    if "required-relation-missing" in r["nativeDeficiencies"]:
        fail("calls dependency coverage should populate sufficiency view")
    expect_value(r, "true", "reachability-with-calls-dep")


def test_unknown_export_owes_closed_world():
    inv = inv_symbol()
    inv["rows"][0]["exported"] = "unknown"
    sid, sc, cid, cov = paired("references", "resolved-binding", U1, U1, ["ts-symbol:src/a.ts#f"], tag="1")
    cov["entry"]["closedWorld"]["exportsClosed"] = "open"
    inputs = base_inputs(inventories=[inv])
    install_pair(inputs, sid, sc, cid, cov)
    atom = {"op": "none", "relation": "references", "minResolution": "resolved-binding", "filters": []}
    r = AM.evaluate_atom(atom, {"universe": U1, "kind": "symbol", "nativeSubjectId": "ts-symbol:src/a.ts#f"}, inputs)
    expect_value(r, "indeterminate", "unknown-export")
    if "external-consumers-unknown" not in r["nativeDeficiencies"] and "target-export-unknown" not in {c["code"] for c in r["causes"]}:
        fail(f"unknown-export defs={r['nativeDeficiencies']} causes={r['causes']}")


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
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "ext", "resolvedTarget": "left-pad"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "left-pad", kind="package", occupancy="first-party",
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
            "payload": {"importer": "ts-symbol:src/a.ts#f", "specifier": "./a", "resolvedTarget": "src/a.ts"},
            "anchors": [{"path": "src/a.ts", "blobDigest": H("0"), "startByte": 0, "endByte": 1}],
        }},
        targetAttributions={fid: sidecar(fid, "src/a.ts", kind="unknown", occupancy="unknown", producer=C_EVAL)},
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
    out_dir = Path("/tmp/opensip-design-corrections/grok-atom-contract.v6")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "check-atoms.report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
