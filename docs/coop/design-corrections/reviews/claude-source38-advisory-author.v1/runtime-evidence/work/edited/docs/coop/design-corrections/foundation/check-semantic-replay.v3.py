"""Native-admitted TypeScript/package graphs through identity-model.v3.close_run.

Synthetic compiler data admitted by the actual native owner and full public replay.
Does not claim real compiler extraction qualification. Seed seal is owner-closure
input only; final proof is R.derive + public close_run.

The execution manifest is captured before seeding and independently admitted
during full replay. These are reference controls, not compiler qualification.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, file):
    s = importlib.util.spec_from_file_location(name, HERE / file)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


S = load("semantic_fixture3", "evaluator_semantic_fixture.v3.py")
R = load("semantic_replay3", "evaluator_replay_model.v3.py")
E = R.E
M = R.M
C = M.C


def canonical_sets(value):
    if type(value) is dict:
        for k, v in value.items():
            canonical_sets(v)
            if k in ("findingIds", "waivedFindingIds", "evidenceRefs", "inputRefs",
                     "evaluationInputRefs", "scopeIds", "coverageIds", "matchingFactIds",
                     "uncertainFactIds", "matchingImportRows", "uncertainImportRows",
                     "deficiencies"):
                value[k] = E.cset(v)
            if k == "predicateProofs":
                value[k] = sorted(v, key=lambda x: tuple(x[t].encode() for t in ("ruleId", "subjectId", "predicateId")))
    elif type(value) is list:
        for x in value:
            canonical_sets(x)
    return value


def remint_finding(run, objects, blobs, change):
    run = copy.deepcopy(run)
    objects = copy.deepcopy(objects)
    blobs = copy.deepcopy(blobs)
    evidence = objects[run["evidenceId"]][1]
    seal = objects[run["evaluationSealId"]][1]
    proof = objects[seal["proofBundleId"]][1]
    fid = proof["findingIds"][0]
    finding = copy.deepcopy(objects[fid][1])
    change(finding, blobs)
    newfid = M.identifier("finding", finding)
    objects[newfid] = ("finding", finding)

    def replace(value):
        if type(value) is str:
            return newfid if value == fid else value
        if type(value) is list:
            return [replace(x) for x in value]
        if type(value) is dict:
            return {k: replace(v) for k, v in value.items()}
        return value

    proof = canonical_sets(replace(copy.deepcopy(proof)))
    pid = M.identifier("proof-bundle", proof)
    objects[pid] = ("proof-bundle", proof)
    evidence = canonical_sets(replace(copy.deepcopy(evidence)))
    evidence["proofBundleId"] = pid
    eid = M.identifier("semantic-evidence", evidence)
    objects[eid] = ("semantic-evidence", evidence)
    seal = copy.deepcopy(seal)
    seal["proofBundleId"] = pid
    seal["evidenceId"] = eid
    sid = M.identifier("evaluation-seal", seal)
    objects[sid] = ("evaluation-seal", seal)
    run["evidenceId"] = eid
    run["evaluationSealId"] = sid
    return run, objects, blobs


def close_positive(graph):
    """Seed owner-closure only, then actual Atom/global admission and public close_run."""
    seed, objects, blobs, _ = S.seed_seal(graph)
    _, owner = M.open_run_closure(seed, objects, blobs)
    i = graph["inputs"]
    result = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                      i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(graph, result, objects, blobs)
    actual = R.replay(run, objects, blobs)
    run_id = M.close_run(run, objects, blobs)
    if run_id != actual["runId"]:
        raise AssertionError("close_run runId != replay runId")
    return run, objects, blobs, actual


def proof_of(run, objects):
    return objects[objects[run["evaluationSealId"]][1]["proofBundleId"]][1]


def findings_of(run, objects):
    return [objects[fid][1] for fid in proof_of(run, objects)["findingIds"]]


def predicates_of(run, objects):
    return proof_of(run, objects)["predicateProofs"]


def subject_values(run, objects):
    out = {}
    for p in predicates_of(run, objects):
        if p["predicateId"] == "p":
            out[p["subjectId"]] = p["value"]
    return out


def package_items(graph):
    return [item for item in graph["inputs"]["population"].values() if item["kind"] == "package"]


def symbol_items(graph, universe=None):
    items = [item for item in graph["inputs"]["population"].values() if item["kind"] == "symbol"]
    if universe is not None:
        items = [item for item in items if item["universe"] == universe]
    return items


def by_native(items, nid, path=None):
    hits = [i for i in items if i["row"]["nativeSubjectId"] == nid
            and (path is None or i["row"]["path"] == path)]
    if len(hits) != 1:
        raise AssertionError("subject lookup %s path=%s count=%d" % (nid, path, len(hits)))
    return hits[0]


DECLARES = {"op": "exists", "relation": "declares", "minResolution": "syntactic", "filters": []}
REFS_EXISTS_SRC = {"op": "exists", "relation": "references", "minResolution": "resolved-binding",
                   "endpoint": "source", "filters": []}
REFS_NONE_SRC = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
                 "endpoint": "source", "filters": []}
REFS_EXISTS_TGT = {"op": "exists", "relation": "references", "minResolution": "resolved-binding",
                   "endpoint": "target", "filters": []}
REFS_NONE_TGT = {"op": "none", "relation": "references", "minResolution": "resolved-binding",
                 "endpoint": "target", "filters": []}
PKG_EXISTS = {"op": "exists", "relation": "package", "minResolution": "manifest-declared", "filters": []}
IMPORTS_EXISTS_TGT = {"op": "exists", "relation": "imports", "minResolution": "resolved-target",
                      "endpoint": "target", "filters": []}
IMPORTS_NONE_TGT = {"op": "none", "relation": "imports", "minResolution": "resolved-target",
                    "endpoint": "target", "filters": []}


def file_items(graph, universe=None):
    items = [item for item in graph["inputs"]["population"].values() if item["kind"] == "file"]
    if universe is not None:
        items = [item for item in items if item["universe"] == universe]
    return items


def case_imports_file_first_party_exists():
    g = S.build_ts_semantic_graph(atom=IMPORTS_EXISTS_TGT, subject_kind="file", has_declares=False,
                                  has_references_fact=False, second_partition=False)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    a_ts = by_native(file_items(g, g["u1"]), "a.ts")
    assert vals[a_ts["subjectId"]] == "true", vals
    others = [item for item in file_items(g, g["u1"]) if item["row"]["nativeSubjectId"] != "a.ts"]
    for item in others:
        assert vals[item["subjectId"]] != "true", (item["row"]["nativeSubjectId"], vals[item["subjectId"]])
    assert actual["verdict"] == "fail" and actual["findingCount"] >= 1, actual
    return g, (run, objects, blobs), actual


def case_imports_file_none_false_on_mapped_target():
    g = S.build_ts_semantic_graph(atom=IMPORTS_NONE_TGT, subject_kind="file", has_declares=False,
                                  has_references_fact=False, second_partition=False)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    a_ts = by_native(file_items(g, g["u1"]), "a.ts")
    assert vals[a_ts["subjectId"]] == "false", vals
    return g, (run, objects, blobs), actual


def case_declares_exists():
    g = S.build_ts_semantic_graph(atom=DECLARES, has_declares=True, has_references_fact=False,
                                  second_partition=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[foo["subjectId"]] == "true" and vals[bar["subjectId"]] == "true", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 2, actual
    return g, (run, objects, blobs), actual


def case_references_exists_source():
    g = S.build_ts_semantic_graph(atom=REFS_EXISTS_SRC, has_declares=False, has_references_fact=True,
                                  second_partition=True, references_resolved=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[foo["subjectId"]] == "true", vals
    assert vals[bar["subjectId"]] == "false", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 1, actual
    return g, (run, objects, blobs), actual


def case_references_none_outgoing_complete():
    g = S.build_ts_semantic_graph(atom=REFS_NONE_SRC, has_declares=False, has_references_fact=True,
                                  second_partition=True, references_resolved=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[foo["subjectId"]] == "false", vals
    assert vals[bar["subjectId"]] == "true", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 1, actual
    return g, (run, objects, blobs), actual


def case_incoming_known_hit():
    g = S.build_ts_semantic_graph(atom=REFS_EXISTS_TGT, has_declares=False, has_references_fact=True,
                                  second_partition=True, references_resolved=True,
                                  incoming_search=True, incoming_complete=True, target_sidecar=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[bar["subjectId"]] == "true", vals
    assert vals[foo["subjectId"]] == "false", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 1, actual
    return g, (run, objects, blobs), actual


def case_incoming_incomplete_unknown():
    g = S.build_ts_semantic_graph(atom=REFS_NONE_TGT, has_declares=False, has_references_fact=True,
                                  second_partition=True, references_resolved=False,
                                  incoming_search=True, incoming_complete=False, target_sidecar=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[bar["subjectId"]] == "false", vals
    assert vals[foo["subjectId"]] == "indeterminate", vals
    assert actual["verdict"] == "indeterminate" and actual["findingCount"] == 0, actual
    return g, (run, objects, blobs), actual


def case_no_false_cross_u():
    g = S.build_ts_semantic_graph(atom=REFS_EXISTS_TGT, has_declares=False, has_references_fact=True,
                                  second_partition=True, second_universe=True, references_resolved=True,
                                  incoming_search=True, incoming_complete=True, target_sidecar=True,
                                  cross_u_binding="foo")
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    baz = by_native(symbol_items(g, g["u2"]), g["baz"])
    assert vals[bar["subjectId"]] == "true", vals
    assert vals[foo["subjectId"]] == "false", vals
    assert vals[baz["subjectId"]] == "false", vals
    assert actual["findingCount"] == 1, actual
    return g, (run, objects, blobs), actual


def case_incoming_partition_s_to_v_unknown():
    """Full graph: complete S->U on foo and complete S->V on bar. Incoming none of foo is unknown."""
    g = S.build_ts_semantic_graph(
        atom=REFS_NONE_TGT, has_declares=False, has_references_fact=False,
        second_partition=True, second_universe=False, partition_b_target="u2",
        references_resolved=True, incoming_search=False)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[foo["subjectId"]] == "indeterminate", vals
    assert vals[bar["subjectId"]] == "indeterminate", vals
    assert actual["verdict"] == "indeterminate" and actual["findingCount"] == 0, actual
    return g, (run, objects, blobs), actual


def case_incoming_attestation_covers_other_partition():
    """Whole-source U1->U1 attestation covers the S->V partition; incoming none of foo is true."""
    g = S.build_ts_semantic_graph(
        atom=REFS_NONE_TGT, has_declares=False, has_references_fact=False,
        second_partition=True, second_universe=False, partition_b_target="u2",
        references_resolved=True, incoming_search=True, incoming_complete=True)
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    foo = by_native(symbol_items(g, g["u1"]), g["foo"])
    bar = by_native(symbol_items(g, g["u1"]), g["bar"])
    assert vals[foo["subjectId"]] == "true", vals
    assert vals[bar["subjectId"]] == "true", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 2, actual
    return g, (run, objects, blobs), actual


def case_package_two_manifests():
    g = S.build_package_graph()
    pkgs = package_items(g)
    left = by_native(pkgs, "dup", "packages/left/package.json")
    right = by_native(pkgs, "dup", "packages/right/package.json")
    root = by_native(pkgs, "fixture-workspace", "package.json")
    assert left["subjectId"] != right["subjectId"]
    assert left["row"]["path"] != right["row"]["path"]
    assert "packageManifestPath" not in left["row"]
    run, objects, blobs, actual = close_positive(g)
    vals = subject_values(run, objects)
    assert vals[left["subjectId"]] == "true", vals
    assert vals[right["subjectId"]] == "true", vals
    assert vals[root["subjectId"]] == "true", vals
    assert actual["verdict"] == "fail" and actual["findingCount"] == 3, actual
    return g, (run, objects, blobs), actual


def case_package_manifest_path_join():
    """Remint the graph omitting the left dup fact. Name-only join would still hit left."""
    full = S.build_package_graph()
    dropped = S.build_package_graph(drop_package_paths=["packages/left/package.json"])
    run, objects, blobs, actual = close_positive(dropped)
    pkgs = package_items(dropped)
    left = by_native(pkgs, "dup", "packages/left/package.json")
    right = by_native(pkgs, "dup", "packages/right/package.json")
    root = by_native(pkgs, "fixture-workspace", "package.json")
    vals = subject_values(run, objects)
    assert vals[left["subjectId"]] == "false", vals
    assert vals[right["subjectId"]] == "true", vals
    assert vals[root["subjectId"]] == "true", vals
    assert actual["findingCount"] == 2, actual
    full_ids = {i["subjectId"] for i in package_items(full) if i["row"]["nativeSubjectId"] == "dup"}
    drop_ids = {left["subjectId"], right["subjectId"]}
    assert full_ids == drop_ids
    return dropped, (run, objects, blobs), actual


def case_complete_empty_reference_execution():
    g = S.build_ts_semantic_graph(atom=REFS_EXISTS_SRC, has_declares=False,
                                 has_references_fact=False, second_partition=True)
    run, objects, blobs, actual = close_positive(g)
    assert (actual["verdict"], actual["findingCount"]) == ("pass", 0), actual
    assert proof_of(run, objects)["executionDeficiencies"] == []
    return g, (run, objects, blobs), actual


def case_missing_inventory_execution():
    g = S.build_ts_semantic_graph(atom=REFS_EXISTS_SRC, has_declares=False,
                                 has_references_fact=False, second_partition=True,
                                 complete_required_inventory=False)
    run, objects, blobs, actual = close_positive(g)
    assert (actual["verdict"], actual["findingCount"]) == ("indeterminate", 0), actual
    assert proof_of(run, objects)["executionDeficiencies"]
    return g, (run, objects, blobs), actual


POSITIVES = [
    ("complete-empty-reference-execution", case_complete_empty_reference_execution),
    ("missing-required-inventory-execution", case_missing_inventory_execution),
    ("declares-exists-source-positive", case_declares_exists),
    ("references-exists-source-positive", case_references_exists_source),
    ("references-none-outgoing-complete", case_references_none_outgoing_complete),
    ("references-exists-incoming-known-hit", case_incoming_known_hit),
    ("references-incoming-incomplete-unknown", case_incoming_incomplete_unknown),
    ("references-no-false-cross-u", case_no_false_cross_u),
    ("incoming-partition-s-to-v-unknown", case_incoming_partition_s_to_v_unknown),
    ("incoming-attestation-covers-other-partition", case_incoming_attestation_covers_other_partition),
    ("package-two-manifest-distinct-subject3", case_package_two_manifests),
    ("package-manifest-path-source-join", case_package_manifest_path_join),
    ("imports-file-first-party-exists", case_imports_file_first_party_exists),
    ("imports-file-none-false-on-mapped-target", case_imports_file_none_false_on_mapped_target),
]


def run_finding_mutants(base):
    rows = []
    run, objects, blobs = base

    def parameter_change(finding, blobs_):
        p = C.parse(blobs_[finding["parameterDigest"]])
        p["parameters"]["matchingFactCount"] += 1
        raw = C.canonical(p)
        d = hashlib.sha256(raw).hexdigest()
        blobs_[d] = raw
        finding["parameterDigest"] = d

    def message_change(finding, blobs_):
        p = C.parse(blobs_[finding["parameterDigest"]])
        p["messageCode"] = "different-message"
        raw = C.canonical(p)
        d = hashlib.sha256(raw).hexdigest()
        blobs_[d] = raw
        finding["parameterDigest"] = d
        finding["messageCode"] = "different-message"

    changes = {
        "same-count-severity": lambda f, b: f.update(severity="warning"),
        "same-count-message": message_change,
        "same-count-parameter": parameter_change,
        "same-count-missing-citation": lambda f, b: f.update(evidenceRefs=[]),
    }
    for name, change in changes.items():
        mutant = remint_finding(run, objects, blobs, change)
        rid = M.open_run_closure(*mutant)[0]
        try:
            R.replay(*mutant)
        except Exception as exc:
            if "EVALUATOR_COMPLETE_PROOF_REPLAY" not in str(exc):
                raise
            rows.append({"case": name, "ownerAdmission": "ADMIT", "remintedRunId": rid,
                         "replay": "REFUSE", "reason": str(exc)})
        else:
            raise AssertionError("semantic mutant accepted:" + name)
    return rows


def run_termination_composition(g, doc, T, Q, built, atoms, validate_shape, schema_valid):
    """Section 7 host composition controls over actually closed Runs (run-termination-contract.v1.md).

    Each case composes one candidate StepTermination against an admitted Run (a golden Run, a fixture Run, or none
    for operational and ephemeral candidates) and a host attempt observation built from existing records: the
    invocation-record Attempt and a commit receipt whose inventoryDigest is the retained commit inventory. For an
    analysis candidate the pure check_projection standing is recorded beside the composition outcome, so a
    composition refusal is never mistaken for a projection refusal.
    """
    faults, out = [], []
    ids = {tag: "exec1_" + ch * 32 for tag, ch in g["executionIdHex"].items()}
    other_run = "run3:" + "1" * 64
    attempt_ref = "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/Attempt"
    receipt_schema = copy.deepcopy(M.SCHEMA)
    receipt_schema["$ref"] = "#/$defs/commit-receipt"

    def validate_attempt(attempt):
        Q.validate_schema(attempt_ref, attempt)

    def validate_receipt(receipt):
        C.validate(receipt_schema, receipt)

    def placeholders(value):
        text = json.dumps(value)
        for tag, eid in ids.items():
            text = text.replace("$" + tag.upper(), eid)
        return json.loads(text.replace("$OTHER_RUN", other_run))

    for case in g["cases"]:
        try:
            run = objects = blobs = derived = None
            if "of" in case:
                run, objects, blobs = built[case["of"]]
            elif "build" in case:
                fixture = doc["fixtures"][case["build"]["fixture"]]
                params = dict(fixture["params"], **case["build"]["params"], atom=atoms[fixture["atom"]])
                run, objects, blobs, _ = close_positive(S.build_ts_semantic_graph(**params))
            if run is not None:
                derived = T.finalize(run, objects, blobs)["termination"]
            candidate = dict(case["termination"]) if "termination" in case else dict(derived)
            for key in case.get("remove", []):
                candidate.pop(key, None)
            candidate.update(case.get("set", {}))
            candidate = placeholders(candidate)
            observation = None
            spec = case.get("observation")
            if spec is not None:
                own_plan = run["planId"] if run is not None else "plan2:" + "2" * 64
                plan = "plan2:" + "0" * 64 if spec.get("plan") == "other" else own_plan
                attempts = []
                for tag in spec["attempts"]:
                    if tag == "busy":
                        attempts.append({"executionId": ids["busy"], "outcome": "failed", "faultCause": "ledger-busy",
                                         "retried": True})
                    elif tag == "done":
                        attempts.append({"executionId": ids["done"], "outcome": "completed",
                                         "derivation": {"planId": plan, "executionPlanId": "exec-plan2:" + "e" * 64,
                                                        "stageCount": 1, "stagesCompleted": 1}})
                    else:
                        attempts.append({"executionId": ids["done"], "outcome": "failed", "faultCause": "host-io"})
                receipt = None
                if spec.get("receipt") is not None:
                    who, which = spec["receipt"]
                    _, inventory_digest = M.commit_inventory(derived["runId"], objects, blobs)
                    receipt = {"schemaVersion": 2, "runId": derived["runId"] if which == "run" else other_run,
                               "executionId": ids[who], "namespaceId": "reference-private-namespace",
                               "commitSequence": 1, "inventoryDigest": inventory_digest,
                               "sealedAssurance": "replayable", "signerKeyId": "reference-host-signer"}
                observation = {"stepId": 0, "durability": spec.get("durability", "authoritative"),
                               "attempts": attempts, "commitReceipt": receipt,
                               "requiredClosureNotInstalled": spec.get("closureNotInstalled", False)}
            validity = schema_valid(candidate)
            try:
                got = T.admit_analysis_step_termination(candidate, run, objects, blobs, observation, validate_shape,
                                                        validate_attempt, validate_receipt)
                outcome = {"composed-analysis-termination-admitted": "ADMIT:" + str(got.get("domainDetailCode") or "none"),
                           "outside-analysis-projection": "OUTSIDE",
                           "ephemeral-attribution-admitted": "EPHEMERAL"}[got["standing"]]
            except T.RunTerminationError as exc:
                outcome = str(exc).split(":", 1)[0]
            pure = None
            if derived is not None:
                try:
                    pure = (T.check_projection(candidate, derived, validate_shape)["delegatedStanding"]
                            or "admitted-without-delegated-member")
                except T.RunTerminationError as exc:
                    pure = str(exc).split(":", 1)[0]
            if outcome != case["expect"]:
                faults.append(f"{case['label']}: composition {outcome}, expected {case['expect']}")
            if case.get("schemaValid", True) and validity is not True:
                faults.append(f"{case['label']}: candidate is not a schema-valid StepTermination, so it proves nothing: {validity}")
            if "pureProjection" in case and pure != case["pureProjection"]:
                faults.append(f"{case['label']}: pure projection {pure}, expected {case['pureProjection']}")
            out.append({"label": case["label"], "composition": outcome, "pureProjection": pure, "schemaValid": validity})
        except Exception as exc:
            faults.append(f"{case['label']}: error {type(exc).__name__}: {str(exc)[:200]}")
            out.append({"label": case["label"], "error": type(exc).__name__ + ": " + str(exc)[:300],
                        "traceback": traceback.format_exc()[-1500:]})
    return {"case": "run-termination:" + g["id"], "ownerAdmission": "ADMIT", "composition": out, "faults": faults}


def run_termination_goldens(exports):
    """Whole-Run indeterminate termination goldens (run-termination-contract.v1.md) over actually closed Runs.

    Each golden Run is either an exported positive above or a fixture graph closed by close_positive. The
    derived termination must equal the retained golden; every retained alternative must be a schema-valid
    StepTermination AND be refused by derivation (schema validity grants nothing).
    """
    T = load("run_termination1", "run_termination_model.v1.py")
    Q = load("run_termination_step_schema3", "../workflows/query_projection_model.v3.py")
    doc = json.loads((HERE / "run-termination-goldens.v1.json").read_text())
    atoms = {"REFS_NONE_TGT": REFS_NONE_TGT, "DECLARES": DECLARES}
    d9 = json.loads((HERE.parents[1] / "artifacts" / "d9-exit-contract.v1.14.json").read_text())
    d9_goldens = {g["id"]: g for g in d9["goldenCases"]}
    rows, built = [], {}

    def validate_shape(term):
        Q.validate_schema(Q.COMMON_ID + "#/$defs/StepTermination", term)

    def schema_valid(term):
        try:
            validate_shape(term)
            return True
        except Exception as exc:  # recorded, never read as refusal of the law
            return "INVALID:" + str(exc).split("\n")[0][:160]

    derived_by = {}

    drift = T.route_drift()
    rows.append({"case": "run-termination:route-drift", "ownerAdmission": "ADMIT", "drift": drift,
                 "faults": [] if drift == doc["routeDrift"] else ["route drift " + json.dumps(drift)]})
    for g in doc["goldens"]:
        faults = []
        try:
            if g["kind"] == "permutation":
                run, objects, blobs = built[g["of"]]
                _, _, population, ctx = T.retained_population(run, objects, blobs)
                got = T.permutation_invariance(T.conditions(population, objects, blobs, ctx["xi"]))
                if got != g["expect"]:
                    faults.append("permutation " + json.dumps(got, sort_keys=True))
                rows.append({"case": "run-termination:" + g["id"], "ownerAdmission": "ADMIT", "permutation": got,
                             "faults": faults})
                continue
            if g["kind"] == "projection":
                derived = derived_by[g["of"]]
                admitted, refused = [], []
                for case in g["admitDelegated"]:
                    candidate = dict(derived, **case["add"])
                    try:
                        got = T.check_projection(candidate, derived, validate_shape)
                    except T.RunTerminationError as exc:
                        faults.append("delegated member refused: " + case["label"] + " " + str(exc)[:200])
                        continue
                    if (got["projection"] != derived or sorted(got["delegated"]) != case["delegated"]
                            or got["delegatedStanding"] != "owner-validation-required"):
                        faults.append("delegated projection " + case["label"] + " " + json.dumps(got, sort_keys=True))
                    admitted.append({"label": case["label"], "delegated": sorted(got["delegated"]),
                                     "standing": got["delegatedStanding"]})
                for case in g["refuse"]:
                    candidate = {k: v for k, v in derived.items() if k not in case.get("remove", [])}
                    candidate.update(case.get("set", {}))
                    try:
                        T.check_projection(candidate, derived, None if case.get("noShapeValidator") else validate_shape)
                        faults.append("candidate admitted: " + case["label"])
                    except T.RunTerminationError as exc:
                        code = str(exc).split(":", 1)[0]
                        if code != case["expect"]:
                            faults.append(f"{case['label']} refused as {code}, expected {case['expect']}")
                        refused.append({"label": case["label"], "refusal": code})
                rows.append({"case": "run-termination:" + g["id"], "ownerAdmission": "ADMIT",
                             "admittedProjectionWithDelegatedMembers": admitted, "refused": refused, "faults": faults})
                continue
            if g["kind"] == "composition":
                rows.append(run_termination_composition(g, doc, T, Q, built, atoms, validate_shape, schema_valid))
                continue
            spec = g["build"]
            if "export" in spec:
                run, objects, blobs = exports[spec["export"]]
            else:
                fixture = doc["fixtures"][spec["fixture"]]
                params = dict(fixture["params"], **spec["params"], atom=atoms[fixture["atom"]])
                run, objects, blobs, _ = close_positive(S.build_ts_semantic_graph(**params))
            built[g["id"]] = (run, objects, blobs)
            fin = T.finalize(run, objects, blobs)
            derived, reduction = fin["termination"], fin["reduction"]
            derived_by[g["id"]] = derived
            want = g["expect"]
            if derived != want["termination"]:
                faults.append("termination " + json.dumps(derived, sort_keys=True))
            for key in ("deficiency", "secondaryDeficiencies", "primaryCause", "carrierKind"):
                if reduction[key] != want[key]:
                    faults.append(f"{key} {reduction[key]!r} != {want[key]!r}")
            if schema_valid(derived) is not True:
                faults.append("derived termination not a StepTermination")
            if "carrierEntry" in want:
                entry = C.parse(blobs[objects[derived["coverageId"]][1]["payloadDigest"]])["entry"]
                got_entry = {"deficiency": entry["deficiency"],
                             "stageTerminal": entry["resolutionCompleteness"]["stageTerminal"],
                             "state": entry["resolutionCompleteness"]["state"]}
                if got_entry != want["carrierEntry"]:
                    faults.append("carrierEntry " + json.dumps(got_entry, sort_keys=True))
            if "d9Golden" in g:
                expected = dict(d9_goldens[g["d9Golden"]]["expectedTermination"], runId=derived["runId"])
                if expected != derived:
                    faults.append("D9 golden " + g["d9Golden"] + " expects " + json.dumps(expected, sort_keys=True))
            refused = []
            for alt in g["refuse"]:
                validity = schema_valid(alt["termination"])
                if validity is not True:
                    faults.append("alternative " + alt["label"] + " is not schema-valid, so it proves nothing: " + str(validity))
                try:
                    T.check_projection(alt["termination"], derived, validate_shape)
                    faults.append("alternative admitted: " + alt["label"])
                except T.RunTerminationError:
                    refused.append(alt["label"])
            rows.append({"case": "run-termination:" + g["id"], "ownerAdmission": "ADMIT", "close_run": "ADMIT",
                         "termination": derived, "refusedSchemaValidAlternatives": refused, "faults": faults})
        except Exception as exc:
            rows.append({"case": "run-termination:" + g["id"], "ownerAdmission": "BLOCKED",
                         "error": type(exc).__name__ + ": " + str(exc), "traceback": traceback.format_exc(),
                         "faults": ["error"]})
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(description="Native-admitted TS/package full replay. Not compiler qualification.")
    parser.add_argument("--export-dir", default=None,
                        help="NEW_DIRECTORY for actual run/objects/base64 blob exports of positives.")
    parser.add_argument("--output", default=None,
                        help="Directory for grok-native-replay.v1.json. Default: stdout only.")
    args = parser.parse_args(argv)
    rows = []
    exports = {}
    failures = []
    for name, fn in POSITIVES:
        try:
            graph, packed, actual = fn()
            exports[name] = packed
            extra = {"verdict": actual["verdict"], "findingCount": actual["findingCount"],
                     "runId": actual["runId"]}
            if name.startswith("package-two"):
                pkgs = [i for i in package_items(graph) if i["row"]["nativeSubjectId"] == "dup"]
                extra["distinctDupSubjects"] = len({p["subjectId"] for p in pkgs})
                extra["dupManifests"] = sorted(p["row"]["path"] for p in pkgs)
            rows.append({"case": name, "ownerAdmission": "ADMIT", "close_run": "ADMIT",
                         "replay": extra})
        except Exception as exc:
            failures.append(name)
            rows.append({"case": name, "ownerAdmission": "BLOCKED",
                         "error": type(exc).__name__ + ": " + str(exc),
                         "traceback": traceback.format_exc()})
    if "declares-exists-source-positive" in exports:
        try:
            rows.extend(run_finding_mutants(exports["declares-exists-source-positive"]))
        except Exception as exc:
            failures.append("finding-mutants")
            rows.append({"case": "finding-mutants", "ownerAdmission": "BLOCKED",
                         "error": type(exc).__name__ + ": " + str(exc),
                         "traceback": traceback.format_exc()})
    try:
        termination_rows = run_termination_goldens(exports)
        rows.extend(termination_rows)
        failures.extend(r["case"] for r in termination_rows if r["faults"])
    except Exception as exc:
        failures.append("run-termination-goldens")
        rows.append({"case": "run-termination-goldens", "ownerAdmission": "BLOCKED",
                     "error": type(exc).__name__ + ": " + str(exc),
                     "traceback": traceback.format_exc()})
    passed = all(r.get("ownerAdmission") == "ADMIT" and r.get("close_run", "ADMIT") == "ADMIT"
                 for r in rows if "error" not in r) and not failures
    report = {
        "standing": ("synthetic native-admitted TypeScript/package graphs through actual "
                     "identity-model.v3.close_run; not compiler extraction qualification; "
                     "execution manifest bound and fully replayed"),
        "passed": passed and not failures,
        "count": len(rows),
        "blocked": failures,
        "checks": rows,
    }
    if args.export_dir is not None:
        directory = Path(args.export_dir)
        directory.mkdir(parents=True, exist_ok=False)
        for name, (run, objects, blobs) in exports.items():
            artifact = {
                "run": run,
                "objects": {k: {"domain": d, "descriptor": v} for k, (d, v) in sorted(objects.items())},
                "blobs": {k: base64.b64encode(v).decode("ascii") for k, v in sorted(blobs.items())},
            }
            (directory / (name + ".json")).write_text(json.dumps(artifact, indent=2) + "\n")
        report["exportCount"] = len(exports)
    text = json.dumps(report, indent=2)
    print(text)
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "grok-native-replay.v1.json").write_text(text + "\n")
    if failures:
        raise SystemExit(1)
    return report


if __name__ == "__main__":
    main()
