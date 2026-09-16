#!/usr/bin/env python3
"""Composed PS-01 control, revision 5.

Calls the frozen security_lifecycle_model_v1 admit_transition_intent,
transition_intent_digest, transition_journal_record and
recover_transition_journal directly. Every owner result reported here is that
model's own return value. The companion law is applied strictly afterwards, and
node shape is admitted through the companion's REAL closed schema using the
frozen foundation ExactValidator.

Sections:
  A  root v2 regressions (invalid rollback fixtures)
  B  the owner pair law, read off the owner
  C  seven owner-admitted operation cases x six journal states, with REAL
     lifecycle timing: a forward target does not exist at LEASED or PREPARING and
     may be reclaimed at ABORTED, so its marker is NOT synthesised there
  D  root v3 regressions (repeated generation, missing predecessor)
  E  composed migrate -> rollback -> second forward selection with a retained branch
  F  damaged predecessor, duplicate full key, unreadable markers, off-chain ancestor
  G  owner actions that decide nothing
  H  root v5 regression: phase-sensitive marker availability at an early abort
  I  root v5 regression: idempotent target path must validate ancestry
  J  multi-component lineages after an authorized restore

Input assumptions are labelled per section. Shape admission
(admit_transition_intent over the eleven-member record) is kept distinct from
current-state and footprint admission (recover_transition_journal over the
namespace registry, held fence, re-acquired leases and the durable footprint).

Design evidence only: no product code, no carrier behaviour, no native lifecycle
qualification.

Usage: check_lineage_recovery.py <work-tree> <candidate25-root>
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lineage_law as L                                            # noqa: E402
from node_schema import build_node_admission                       # noqa: E402

SEC = "docs/coop/design-corrections/security"
FAILURES = []

REGISTRY = ["ns-b", "ns-a", "ns-c"]
MARK_A = "a" * 32          # the store selected before a transition
MARK_B = "b" * 32          # an earlier retained store
MARK_NEW = "e" * 32        # a newly materialised store
MARK_F = "f" * 32          # a second newly materialised store

# Real lifecycle timing for a FORWARD selection's target store root.
# LEASED/PREPARING precede materialisation; ABORTED may already be reclaimed.
TARGET_PRESENT_STATES = ("PREPARED", "COMMITTED", "DONE")


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def load_owner(c25):
    path = c25 / SEC / "security_lifecycle_model_v1.py"
    spec = importlib.util.spec_from_file_location("s9owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rctx(journal, footprint=None):
    return {"namespaceRegistry": REGISTRY, "fenceHeld": True,
            "leasesReacquired": journal["leaseSet"], "storeFootprint": footprint}


FENCED_PREPARED = {"old": {"present": True, "unbootstrappedReason": "RESTORED"},
                   "new": {"dir": "migrating", "state": "PREPARED"}}
UNFENCED_PREPARED = {"old": {"present": True, "unbootstrappedReason": None},
                     "new": {"dir": "migrating", "state": "PREPARED"}}


def owner_intents(fixtures):
    retreat = dict(fixtures["intentCoreRollback"])
    retreat.update({"fromStateSchema": 2, "toStateSchema": 1,
                    "fromStoreGeneration": 4, "toStoreGeneration": 3})
    return [
        ("core-repair (same store)", fixtures["intentRepair"], L.SAME_STORE),
        ("core-update same schema (same store)", fixtures["intentUpdateSameSchema"],
         L.SAME_STORE),
        ("core-rollback same schema (same store)", fixtures["intentCoreRollback"],
         L.SAME_STORE),
        ("core-rollback schema retreat (ancestor reselect)", retreat, L.ANCESTOR_RESELECT),
        ("store-rollback schema retreat (ancestor reselect)",
         fixtures["intentStoreRollback"], L.ANCESTOR_RESELECT),
        ("core-update schema raise (forward selection)",
         fixtures["intentUpdateSchemaChange"], L.FORWARD_SELECTION),
        ("store-migrate (forward selection)", fixtures["intentStoreMigrate"],
         L.FORWARD_SELECTION),
    ]


def lineage_and_markers(intent):
    """A lawful starting lineage plus the markers of the SETTLED phase."""
    case = L.selection_case(intent)
    frm = (intent["fromStoreGeneration"], intent["fromStateSchema"])
    to = (intent["toStoreGeneration"], intent["toStateSchema"])
    if case is L.SAME_STORE:
        current = L.node(MARK_A, frm[0], frm[1], None, None)
        return [current], L.node_triple(current), \
            {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_A}
    if case is L.ANCESTOR_RESELECT:
        ancestor = L.node(MARK_B, to[0], to[1], None, None)
        current = L.node(MARK_A, frm[0], frm[1], L.node_triple(ancestor), "1" * 64)
        return [ancestor, current], L.node_triple(current), \
            {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_B}
    current = L.node(MARK_A, frm[0], frm[1], None, None)
    return [current], L.node_triple(current), \
        {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}


def markers_for_state(case, settled_markers, state):
    """Phase-accurate markers. A forward target is absent before materialisation."""
    if case is not L.FORWARD_SELECTION or state in TARGET_PRESENT_STATES:
        return dict(settled_markers), "target root present"
    return ({"predecessorStoreRoot": settled_markers["predecessorStoreRoot"],
             "selectedStoreRoot": L.TARGET_ABSENT},
            "target root not materialised yet, or reclaimed after abort")


def section_a(M, fixtures):
    rows = []
    for label, base in (("core-rollback", "intentCoreRollback"),
                        ("store-rollback", "intentStoreRollback")):
        bad = dict(fixtures[base])
        bad.update({"fromStoreGeneration": 5, "fromStateSchema": 1,
                    "toStoreGeneration": 4, "toStateSchema": 1})
        rows.append({"v2Label": label + " (5,1)->(4,1) mislabelled schema retreat",
                     "ownerShapeRefusals": M.admit_transition_intent(bad)})
    check(rows[0]["ownerShapeRefusals"] == ["TRANSITION.SAME_SCHEMA_KEEPS_STORE"],
          "core-rollback v2 counterexample refusal changed")
    check(rows[1]["ownerShapeRefusals"] ==
          ["TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT"],
          "store-rollback v2 counterexample refusal changed")
    return rows


def section_b(M, fixtures):
    rows = []
    for op in ("core-update", "core-rollback"):
        base = fixtures["intentUpdateSameSchema" if op == "core-update"
                        else "intentCoreRollback"]
        a = dict(base, fromStateSchema=2, toStateSchema=2,
                 fromStoreGeneration=4, toStoreGeneration=5)
        b = dict(base, fromStateSchema=1, toStateSchema=2,
                 fromStoreGeneration=4, toStoreGeneration=4)
        ra, rb = M.admit_transition_intent(a), M.admit_transition_intent(b)
        rows.append({"operation": op, "sameSchemaDifferentStore": ra,
                     "schemaChangeSameStore": rb})
        check("TRANSITION.SAME_SCHEMA_KEEPS_STORE" in ra,
              op + ": same schema must keep the store")
        check("TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE" in rb,
              op + ": a schema change must select a new store")
    return rows


def section_c(M, fixtures, admit):
    matrix = []
    for label, intent, expected_case in owner_intents(fixtures):
        shape = M.admit_transition_intent(intent)
        check(shape == [], label + ": owner shape-refused an admitted intent: " + str(shape))
        if shape:
            continue
        digest = M.transition_intent_digest(intent)
        journal = M.transition_journal_record(intent, REGISTRY)
        nodes, current, settled_markers = lineage_and_markers(intent)
        case = L.selection_case(intent)
        check(case == expected_case,
              label + ": expected " + expected_case + ", got " + case)

        pub_case, pub_refusal, pub_nodes, published, _d = L.publish(
            intent, digest, nodes, current, settled_markers, admit)
        check(pub_refusal is None, label + ": publication refused: " + str(pub_refusal))
        check((published is not None) == (case is L.FORWARD_SELECTION),
              label + ": only a forward selection may publish a node")
        check(not L.invariants(pub_nodes, admit, expected_components=1),
              label + ": publication broke invariants")

        per_state = []
        for state in M.TRANSITION_STATES:
            footprint = FENCED_PREPARED if state == "PREPARED" else None
            owner = M.recover_transition_journal(dict(journal, state=state),
                                                 rctx(journal, footprint))
            markers, timing = markers_for_state(case, settled_markers, state)
            rec = L.recover_nodes(owner, intent, digest, nodes, current, markers, admit)
            problems = L.invariants(rec["nodes"], admit, expected_components=1)
            check(not problems, label + "/" + state + ": invariants broken " + str(problems))
            check(rec["refusal"] is None,
                  label + "/" + state + ": unexpected refusal " + str(rec["refusal"])
                  + " (" + str(rec.get("rationale")) + ")")
            if case is not L.FORWARD_SELECTION and rec.get("node") is not None:
                original, _dup = L.find_at_triple(nodes, L.node_triple(rec["node"]))
                check(rec["node"]["predecessor"] == original["predecessor"]
                      and rec["node"]["selectedByIntentDigest"]
                      == original["selectedByIntentDigest"],
                      label + "/" + state + ": recovery rewrote an existing origin")
                check(rec["nodeAction"] == "validated-existing",
                      label + "/" + state + ": non-forward must only validate")
            check(not (case is not L.FORWARD_SELECTION
                       and rec["nodeAction"] == "reconstructed-and-written"),
                  label + "/" + state + ": a non-forward case reconstructed")
            per_state.append({"journalState": state, "ownerAction": owner["action"],
                              "ownerJournalStateAfter": owner["journalStateAfter"],
                              "targetRootTiming": timing,
                              "targetObservation": rec["targetObservation"],
                              "companionNodeAction": rec["nodeAction"],
                              "companionRefusal": rec["refusal"],
                              "nodeCountAfter": len(rec["nodes"])})

        missing = None
        if case is not L.FORWARD_SELECTION:
            stripped = [n for n in nodes
                        if L._key(L.node_triple(n)) != L._key(
                            L.selected_triple(intent, settled_markers))]
            owner = M.recover_transition_journal(dict(journal, state="COMMITTED"),
                                                 rctx(journal))
            rec = L.recover_nodes(owner, intent, digest, stripped, current,
                                  settled_markers, admit)
            check(rec["refusal"] == L.QUARANTINE,
                  label + ": missing selected node must quarantine")
            missing = {"refusal": rec["refusal"], "rationale": rec["rationale"]}

        matrix.append({"case": label, "operation": intent["operation"],
                       "from": [intent["fromStoreGeneration"], intent["fromStateSchema"]],
                       "to": [intent["toStoreGeneration"], intent["toStateSchema"]],
                       "selectionCase": case, "publishesNode": published is not None,
                       "states": per_state, "missingSelectedNode": missing})
    return matrix


def section_d(M, fixtures, admit):
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    root = L.node(MARK_A, 3, 1, None, None)
    retained = L.node(MARK_B, 4, 2, L.node_triple(root), "1" * 64)
    nodes = [root, retained]
    check(not L.invariants(nodes, admit, expected_components=1),
          "the retained-branch lineage must start clean")
    repeated = []
    for state, markers in (("LEASED", {"predecessorStoreRoot": MARK_A,
                                       "selectedStoreRoot": L.TARGET_ABSENT}),
                           ("COMMITTED", {"predecessorStoreRoot": MARK_A,
                                          "selectedStoreRoot": MARK_NEW})):
        owner = M.recover_transition_journal(dict(journal, state=state), rctx(journal))
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root),
                              markers, admit)
        repeated.append({"state": state, "ownerAction": owner["action"],
                         "targetObservation": rec["targetObservation"],
                         "companionNodeAction": rec["nodeAction"],
                         "companionRefusal": rec["refusal"],
                         "nodeCountAfter": len(rec["nodes"]),
                         "invariantProblems": L.invariants(rec["nodes"], admit,
                                                           expected_components=1)})
        check(rec["refusal"] is None,
              "retained branch at the same numeric pair must not refuse at " + state)
    check(repeated[0]["nodeCountAfter"] == 2, "ABORT must write no node")
    check(repeated[1]["nodeCountAfter"] == 3,
          "a settled forward selection must write its own node beside the retained branch")

    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    missing = L.recover_nodes(owner, intent, digest, [], L.node_triple(root),
                              {"predecessorStoreRoot": MARK_A,
                               "selectedStoreRoot": MARK_NEW}, admit)
    check(missing["refusal"] == L.QUARANTINE,
          "a forward reconstruction with an absent predecessor must refuse")
    check(len(missing["nodes"]) == 0, "a refused reconstruction must write nothing")
    return {"retainedBranchRepeatedGeneration": repeated,
            "absentPredecessor": {"refusal": missing["refusal"],
                                  "rationale": missing["rationale"],
                                  "nodesWritten": len(missing["nodes"])}}


def section_e(M, fixtures, admit):
    steps = []
    migrate = fixtures["intentStoreMigrate"]
    rollback = dict(fixtures["intentStoreRollback"],
                    fromStoreGeneration=4, toStoreGeneration=3,
                    fromStateSchema=2, toStateSchema=1)
    second = dict(fixtures["intentStoreMigrate"],
                  fromStoreGeneration=3, toStoreGeneration=5, preconditionGeneration=9)
    for name, intent in (("migrate", migrate), ("rollback", rollback),
                         ("second-migrate", second)):
        check(M.admit_transition_intent(intent) == [],
              name + " must be owner shape-admitted")

    nodes = [L.node(MARK_A, 3, 1, None, None)]
    current = L.node_triple(nodes[0])
    for name, intent, markers, expect in (
            ("migrate (3,1)->(4,2)", migrate,
             {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW},
             "reconstructed-and-written"),
            ("store-rollback (4,2)->(3,1)", rollback,
             {"predecessorStoreRoot": MARK_NEW, "selectedStoreRoot": MARK_A},
             "validated-existing"),
            ("second migrate (3,1)->(5,2)", second,
             {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_F},
             "reconstructed-and-written")):
        digest = M.transition_intent_digest(intent)
        journal = M.transition_journal_record(intent, REGISTRY)
        owner = M.recover_transition_journal(dict(journal, state="COMMITTED"),
                                             rctx(journal))
        rec = L.recover_nodes(owner, intent, digest, nodes, current, markers, admit)
        check(rec["refusal"] is None and rec["nodeAction"] == expect,
              name + ": expected " + expect + ", got " + str(rec["nodeAction"])
              + " / " + str(rec["refusal"]))
        nodes = rec["nodes"]
        current = L.selected_triple(intent, markers)
        steps.append({"step": name, "ownerAction": owner["action"],
                      "companion": rec["nodeAction"], "nodes": len(nodes),
                      "originPreserved": rec.get("originPreserved")})
    problems = L.invariants(nodes, admit, expected_components=1)
    check(not problems, "the branched lineage must stay clean: " + str(problems))
    return {"steps": steps, "finalLineage": nodes, "invariantProblems": problems}


def section_f(M, fixtures, admit):
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    root = L.node(MARK_A, 3, 1, None, None)
    good = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    rows = []

    def case(name, nodes, markers, expect_refusal, expect_written):
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root),
                              markers, admit)
        ok = ((rec["refusal"] == L.QUARANTINE) == expect_refusal) and \
             ((rec["nodeAction"] == "reconstructed-and-written") == expect_written)
        rows.append({"case": name, "refusal": rec["refusal"],
                     "nodeAction": rec["nodeAction"],
                     "nodesWritten": len(rec["nodes"]) - len(nodes),
                     "rationale": rec.get("rationale"), "ok": ok})
        check(ok, "section F case " + name + ": refusal=" + str(rec["refusal"])
              + " action=" + str(rec["nodeAction"]))
        if expect_refusal:
            check(len(rec["nodes"]) == len(nodes),
                  "section F case " + name + " must write nothing on refusal")

    case("absent predecessor", [], good, True, False)
    damaged = L.node(MARK_A, 3, 1, L.triple(MARK_B, 2, 1), "9" * 64)
    case("predecessor names a node that does not exist", [damaged], good, True, False)
    dup_pred_same = [L.node(MARK_A, 3, 1, None, None), L.node(MARK_A, 3, 1, None, None)]
    case("duplicate predecessor key, identical contents", dup_pred_same, good, False, True)
    dup_pred_diff = [L.node(MARK_A, 3, 1, None, None),
                     L.node(MARK_A, 3, 1, L.triple(MARK_B, 2, 1), "7" * 64)]
    case("duplicate predecessor key, disagreeing contents", dup_pred_diff, good,
         True, False)
    target = L.node(MARK_NEW, 4, 2, L.triple(MARK_A, 3, 1), "8" * 64)
    case("duplicate target key, disagreeing contents",
         [root, target, dict(target, selectedByIntentDigest="9" * 64)], good, True, False)
    case("target key exists with a different origin", [root, target], good, True, False)
    case("target marker not observed at all", [root],
         {"predecessorStoreRoot": MARK_A}, True, False)
    case("target marker unreadable", [root],
         {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": "zz"}, True, False)
    case("forward markers name the same store", [root],
         {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_A}, True, False)
    case("settled forward selection whose target root is absent", [root],
         {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": L.TARGET_ABSENT},
         True, False)
    bad_node = dict(L.node(MARK_A, 3, 1, None, None), stateSchema=True)
    case("node set member fails real schema admission", [bad_node], good, True, False)

    rollback = fixtures["intentStoreRollback"]
    rdigest = M.transition_intent_digest(rollback)
    rjournal = M.transition_journal_record(rollback, REGISTRY)
    rowner = M.recover_transition_journal(dict(rjournal, state="COMMITTED"), rctx(rjournal))
    chain_root = L.node(MARK_B, 3, 1, None, None)
    cur = L.node(MARK_A, 4, 2, L.node_triple(chain_root), "1" * 64)
    off_chain = L.node(MARK_F, 3, 1, L.node_triple(cur), "2" * 64)
    rec = L.recover_nodes(rowner, rollback, rdigest, [chain_root, cur, off_chain],
                          L.node_triple(cur),
                          {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_F},
                          admit)
    rows.append({"case": "ancestor reselect naming an off-chain store at the same pair",
                 "refusal": rec["refusal"], "nodeAction": rec["nodeAction"],
                 "rationale": rec.get("rationale"),
                 "ok": rec["refusal"] == L.QUARANTINE})
    check(rec["refusal"] == L.QUARANTINE,
          "an off-chain store at the same numeric pair must not qualify as an ancestor")
    rec_ok = L.recover_nodes(rowner, rollback, rdigest, [chain_root, cur],
                             L.node_triple(cur),
                             {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_B},
                             admit)
    rows.append({"case": "ancestor reselect naming the verified chain member",
                 "refusal": rec_ok["refusal"], "nodeAction": rec_ok["nodeAction"],
                 "ok": rec_ok["refusal"] is None
                 and rec_ok["nodeAction"] == "validated-existing"})
    check(rec_ok["refusal"] is None and rec_ok["nodeAction"] == "validated-existing",
          "an on-chain ancestor must validate")
    return rows


def section_g(M, fixtures, admit):
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    root = L.node(MARK_A, 3, 1, None, None)
    conflicting = L.node(MARK_NEW, 4, 2, L.node_triple(root), "8" * 64)
    nodes = [root, conflicting]
    markers = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    rows = []
    for name, ctx, state in (
            ("fence not held", {"namespaceRegistry": REGISTRY, "fenceHeld": False,
                                "leasesReacquired": journal["leaseSet"],
                                "storeFootprint": None}, "COMMITTED"),
            ("lease set not re-acquired", {"namespaceRegistry": REGISTRY,
                                           "fenceHeld": True,
                                           "leasesReacquired": ["ns-a"],
                                           "storeFootprint": None}, "COMMITTED"),
            ("registry differs", {"namespaceRegistry": ["ns-a"], "fenceHeld": True,
                                  "leasesReacquired": journal["leaseSet"],
                                  "storeFootprint": None}, "COMMITTED"),
            ("PREPARED store operation without a footprint", rctx(journal), "PREPARED")):
        owner = M.recover_transition_journal(dict(journal, state=state), ctx)
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root),
                              markers, admit)
        ok = (rec["nodeAction"] == "no-decision" and rec["refusal"] is None
              and rec["case"] is None and len(rec["nodes"]) == len(nodes))
        rows.append({"context": name, "ownerAction": owner["action"],
                     "ownerRefusal": owner["refusal"],
                     "companionNodeAction": rec["nodeAction"],
                     "companionInspectedNodes": rec["case"] is not None, "ok": ok})
        check(ok, "section G " + name + ": companion must make no decision")
    owner = M.recover_transition_journal(dict(journal, state="PREPARED"),
                                         rctx(journal, UNFENCED_PREPARED))
    rec = L.recover_nodes(owner, intent, digest, [root], L.node_triple(root),
                          markers, admit)
    rows.append({"context": "PREPARED store operation, old store not fenced",
                 "ownerAction": owner["action"],
                 "companionNodeAction": rec["nodeAction"],
                 "companionRefusal": rec["refusal"],
                 "ok": owner["action"] == "ABORT" and rec["refusal"] is None})
    check(owner["action"] == "ABORT" and rec["refusal"] is None,
          "an unfenced PREPARED store operation must abort with no companion refusal")
    return rows


def section_h(M, fixtures, admit):
    """Root v5 regression: phase-sensitive marker availability."""
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    root = L.node(MARK_A, 3, 1, None, None)
    rows = []

    for state, markers, label, expect_refusal in (
            ("LEASED", {"predecessorStoreRoot": MARK_A,
                        "selectedStoreRoot": L.TARGET_ABSENT},
             "early abort, target not materialised", False),
            ("PREPARING", {"predecessorStoreRoot": MARK_A,
                           "selectedStoreRoot": L.TARGET_ABSENT},
             "abort during prepare, target not materialised", False),
            ("ABORTED", {"predecessorStoreRoot": MARK_A,
                         "selectedStoreRoot": L.TARGET_ABSENT},
             "unpublished target already reclaimed", False),
            ("LEASED", {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW},
             "target observable, no node for this attempt", False),
            ("LEASED", {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": "nothex"},
             "target observed but unreadable", True)):
        owner = M.recover_transition_journal(dict(journal, state=state), rctx(journal))
        rec = L.recover_nodes(owner, intent, digest, [root], L.node_triple(root),
                              markers, admit)
        ok = ((rec["refusal"] == L.QUARANTINE) == expect_refusal) and \
            len(rec["nodes"]) == 1
        rows.append({"journalState": state, "scenario": label,
                     "ownerAction": owner["action"],
                     "targetObservation": rec["targetObservation"],
                     "companionNodeAction": rec["nodeAction"],
                     "companionRefusal": rec["refusal"],
                     "rationale": rec.get("rationale"), "ok": ok})
        check(ok, "section H " + state + "/" + label + ": refusal="
              + str(rec["refusal"]) + " expected refusal=" + str(expect_refusal))

    # A genuinely premature node at the attempt's own FULL triple still refuses.
    premature = L.node(MARK_NEW, 4, 2, L.node_triple(root), digest)
    owner = M.recover_transition_journal(dict(journal, state="LEASED"), rctx(journal))
    rec = L.recover_nodes(owner, intent, digest, [root, premature], L.node_triple(root),
                          {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW},
                          admit)
    rows.append({"journalState": "LEASED", "scenario": "premature node at the FULL triple",
                 "ownerAction": owner["action"], "targetObservation": rec["targetObservation"],
                 "companionRefusal": rec["refusal"],
                 "ok": rec["refusal"] == L.QUARANTINE})
    check(rec["refusal"] == L.QUARANTINE,
          "a premature node at the attempt's own full triple must still refuse")

    # A retained branch at the same numeric pair is NOT premature.
    retained = L.node(MARK_B, 4, 2, L.node_triple(root), "1" * 64)
    rec = L.recover_nodes(owner, intent, digest, [root, retained], L.node_triple(root),
                          {"predecessorStoreRoot": MARK_A,
                           "selectedStoreRoot": L.TARGET_ABSENT}, admit)
    rows.append({"journalState": "LEASED",
                 "scenario": "retained branch at the same numeric pair, target absent",
                 "ownerAction": owner["action"], "targetObservation": rec["targetObservation"],
                 "companionRefusal": rec["refusal"], "ok": rec["refusal"] is None})
    check(rec["refusal"] is None,
          "a retained branch must not make an early abort a quarantine")
    return rows


def section_i(M, fixtures, admit):
    """Root v5 regression: the idempotent target path must validate ancestry."""
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    markers = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    rows = []

    # Negative: exact existing target, immediate predecessor present, chain broken.
    broken_pred = L.node(MARK_A, 3, 1, L.triple(MARK_F, 2, 1), "2" * 64)
    broken_target = L.node(MARK_NEW, 4, 2, L.node_triple(broken_pred), digest)
    rec = L.recover_nodes(owner, intent, digest, [broken_pred, broken_target],
                          L.node_triple(broken_pred), markers, admit)
    rows.append({"case": "existing exact target whose predecessor chain is broken",
                 "refusal": rec["refusal"], "nodeAction": rec["nodeAction"],
                 "rationale": rec.get("rationale"),
                 "nodesWritten": len(rec["nodes"]) - 2,
                 "ok": rec["refusal"] == L.QUARANTINE})
    check(rec["refusal"] == L.QUARANTINE,
          "an idempotent match with a broken chain must refuse")
    check(len(rec["nodes"]) == 2, "an idempotent refusal must write nothing")

    # Positive: exact existing target on a clean chain validates without writing.
    good_root = L.node(MARK_A, 3, 1, None, None)
    good_target = L.node(MARK_NEW, 4, 2, L.node_triple(good_root), digest)
    rec_ok = L.recover_nodes(owner, intent, digest, [good_root, good_target],
                             L.node_triple(good_root), markers, admit)
    rows.append({"case": "existing exact target on a clean chain",
                 "refusal": rec_ok["refusal"], "nodeAction": rec_ok["nodeAction"],
                 "nodesWritten": len(rec_ok["nodes"]) - 2,
                 "originPreserved": rec_ok["node"] == good_target,
                 "ok": rec_ok["refusal"] is None and rec_ok["nodeAction"] == "validated"})
    check(rec_ok["refusal"] is None and rec_ok["nodeAction"] == "validated",
          "a clean idempotent match must validate")
    check(len(rec_ok["nodes"]) == 2, "an idempotent match must write nothing")
    check(rec_ok["node"] == good_target, "an idempotent match must not rewrite the origin")

    # Negative: a cycle on the existing chain.
    cyc_a = L.node(MARK_A, 3, 1, L.triple(MARK_NEW, 4, 2), "3" * 64)
    cyc_b = L.node(MARK_NEW, 4, 2, L.triple(MARK_A, 3, 1), digest)
    rec_cyc = L.recover_nodes(owner, intent, digest, [cyc_a, cyc_b],
                              L.node_triple(cyc_a), markers, admit)
    rows.append({"case": "existing target on a cyclic chain",
                 "refusal": rec_cyc["refusal"], "nodeAction": rec_cyc["nodeAction"],
                 "ok": rec_cyc["refusal"] == L.QUARANTINE})
    check(rec_cyc["refusal"] == L.QUARANTINE, "a cyclic chain must refuse")

    # The same discipline on the non-forward validation path.
    rollback = fixtures["intentStoreRollback"]
    rdig = M.transition_intent_digest(rollback)
    rjour = M.transition_journal_record(rollback, REGISTRY)
    rown = M.recover_transition_journal(dict(rjour, state="COMMITTED"), rctx(rjour))
    anc = L.node(MARK_B, 3, 1, L.triple(MARK_F, 1, 1), "4" * 64)   # dangling root
    cur = L.node(MARK_A, 4, 2, L.node_triple(anc), "5" * 64)
    rec_nf = L.recover_nodes(rown, rollback, rdig, [anc, cur], L.node_triple(cur),
                             {"predecessorStoreRoot": MARK_A,
                              "selectedStoreRoot": MARK_B}, admit)
    rows.append({"case": "ancestor reselect onto a node with a dangling chain",
                 "refusal": rec_nf["refusal"], "nodeAction": rec_nf["nodeAction"],
                 "ok": rec_nf["refusal"] == L.QUARANTINE})
    check(rec_nf["refusal"] == L.QUARANTINE,
          "a non-forward validation onto a dangling chain must refuse")
    return rows


def section_j(M, fixtures, admit):
    """Component scoping: a restored lineage is a second component, not corruption."""
    original = [L.node(MARK_A, 3, 1, None, None),
                L.node(MARK_NEW, 4, 2, L.triple(MARK_A, 3, 1), "1" * 64)]
    restored_root = L.node(MARK_F, 7, 2, None, None)
    both = original + [restored_root]
    single = L.invariants(original, admit, expected_components=1)
    two = L.invariants(both, admit, expected_components=2)
    wrong = L.invariants(both, admit, expected_components=1)
    check(not single, "the original lineage alone must be clean")
    check(not two, "two lineage components must be clean when declared: " + str(two))
    check(wrong, "declaring one component over two must be reported")

    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    rec = L.recover_nodes(owner, intent, digest, both, L.triple(MARK_A, 3, 1),
                          {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_B},
                          admit)
    check(rec["refusal"] is None,
          "an unrelated restored lineage must not block a lawful forward selection: "
          + str(rec.get("rationale")))
    return {"originalOnlyProblems": single, "twoComponentsDeclaredProblems": two,
            "oneComponentDeclaredOverTwo": wrong,
            "forwardSelectionBesideARestoredLineage": {
                "refusal": rec["refusal"], "nodeAction": rec["nodeAction"],
                "nodeCountAfter": len(rec["nodes"])}}


def main():
    work = Path(sys.argv[1])
    c25 = Path(sys.argv[2])
    M = load_owner(c25)
    admit, admission_description = build_node_admission(work, c25)
    fixtures = json.loads(
        (c25 / SEC / "transition-journal-cases.v1.json").read_text())["records"]
    result = {
        "control": "check_lineage_recovery",
        "ownerModel": {
            "path": SEC + "/security_lifecycle_model_v1.py",
            "shapeAdmission": "admit_transition_intent over the eleven-member record",
            "stateAndFootprintAdmission":
                "recover_transition_journal over namespaceRegistry, fenceHeld, "
                "leasesReacquired and the durable storeFootprint",
            "otherFunctions": ["transition_intent_digest", "transition_journal_record"]},
        "nodeAdmission": admission_description,
        "inputAssumptions": {
            "ownerResults": "actual returns of the frozen owner model; nothing synthesised",
            "intents": "owner shape-admitted eleven-member records; one composed "
                       "schema-retreating core-rollback is admitted before use",
            "nodes": "every node is admitted by the companion's real closed schema "
                     "through the frozen ExactValidator; no member or type is assumed",
            "markers": "store-root observations, phase-accurate: a forward target is "
                       "stated absent at LEASED, PREPARING and ABORTED rather than "
                       "synthesised",
            "notClaimed": "no filesystem, carrier, crash or native lifecycle behaviour"},
        "A_rootV2Regressions": section_a(M, fixtures),
        "B_ownerPairLaw": section_b(M, fixtures),
        "C_operationStateMatrix": section_c(M, fixtures, admit),
        "D_rootV3Regressions": section_d(M, fixtures, admit),
        "E_migrateRollbackSecondForward": section_e(M, fixtures, admit),
        "F_damagedAndDuplicate": section_f(M, fixtures, admit),
        "G_ownerActionsThatDecideNothing": section_g(M, fixtures, admit),
        "H_phaseSensitiveMarkers": section_h(M, fixtures, admit),
        "I_idempotentPathValidation": section_i(M, fixtures, admit),
        "J_lineageComponents": section_j(M, fixtures, admit),
        "failures": FAILURES,
    }
    result["status"] = "PASS" if not FAILURES else "FAIL"
    result["limits"] = ("Owner results are the frozen model's own returns. The companion "
                        "law is a design reference: no product code, no carrier behaviour, "
                        "no native lifecycle qualification.")
    print(json.dumps(result, indent=1))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
