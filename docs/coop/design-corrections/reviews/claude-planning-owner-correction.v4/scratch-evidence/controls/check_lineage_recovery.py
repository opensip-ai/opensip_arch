#!/usr/bin/env python3
"""Composed PS-01 control, revision 4.

Calls the frozen security_lifecycle_model_v1 admit_transition_intent,
transition_intent_digest, transition_journal_record and
recover_transition_journal directly. Every owner result reported here is that
model's own return value. The companion law is applied strictly afterwards.

Sections:
  A  root v2 counterexample regressions (invalid rollback fixtures)
  B  the owner pair law, read off the owner
  C  seven owner-admitted operation cases x six journal states
  D  root v3 counterexample regressions (repeated generation, missing predecessor)
  E  composed migrate -> rollback -> second forward selection with a retained branch
  F  damaged predecessor, duplicate full key, unreadable markers
  G  owner actions that decide nothing

Shape admission (admit_transition_intent, an eleven-member record check) is kept
distinct from current-state and footprint admission (recover_transition_journal
with a namespace registry, held fence, re-acquired leases and, for a PREPARED
store operation, the durable migrating-root footprint).

Design evidence only: no product code, no carrier behaviour, no native lifecycle
qualification.

Usage: check_lineage_recovery.py <candidate25-root>
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lineage_law as L                                            # noqa: E402

SEC = "docs/coop/design-corrections/security"
FAILURES = []

REGISTRY = ["ns-b", "ns-a", "ns-c"]
MARK_A = "a" * 32          # the store selected before a transition
MARK_B = "b" * 32          # an earlier retained store
MARK_NEW = "e" * 32        # a newly materialised store
MARK_F = "f" * 32          # a second newly materialised store


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
    """Current-state and footprint admission context, distinct from shape admission."""
    return {"namespaceRegistry": REGISTRY, "fenceHeld": True,
            "leasesReacquired": journal["leaseSet"], "storeFootprint": footprint}


FENCED_PREPARED = {"old": {"present": True, "unbootstrappedReason": "RESTORED"},
                   "new": {"dir": "migrating", "state": "PREPARED"}}
UNFENCED_PREPARED = {"old": {"present": True, "unbootstrappedReason": None},
                     "new": {"dir": "migrating", "state": "PREPARED"}}


def owner_intents(fixtures):
    """Seven owner-admitted intents: six frozen fixtures plus one composed."""
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
    """A lawful starting lineage plus the markers the selected stores would carry."""
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


def section_c(M, fixtures):
    matrix = []
    for label, intent, expected_case in owner_intents(fixtures):
        shape = M.admit_transition_intent(intent)
        check(shape == [], label + ": owner shape-refused an admitted intent: " + str(shape))
        if shape:
            continue
        digest = M.transition_intent_digest(intent)
        journal = M.transition_journal_record(intent, REGISTRY)
        nodes, current, markers = lineage_and_markers(intent)
        case = L.selection_case(intent)
        check(case == expected_case,
              label + ": expected " + expected_case + ", got " + case)

        pub_case, pub_refusal, pub_nodes, published = L.publish(
            intent, digest, nodes, current, markers)
        check(pub_refusal is None, label + ": publication refused: " + str(pub_refusal))
        check((published is not None) == (case is L.FORWARD_SELECTION),
              label + ": only a forward selection may publish a node")
        check(not L.invariants(pub_nodes), label + ": publication broke invariants")

        per_state = []
        for state in M.TRANSITION_STATES:
            footprint = FENCED_PREPARED if state == "PREPARED" else None
            owner = M.recover_transition_journal(dict(journal, state=state),
                                                 rctx(journal, footprint))
            rec = L.recover_nodes(owner, intent, digest, nodes, current, markers)
            problems = L.invariants(rec["nodes"])
            check(not problems, label + "/" + state + ": invariants broken " + str(problems))
            check(rec["refusal"] is None,
                  label + "/" + state + ": unexpected refusal " + str(rec["refusal"]))
            if case is not L.FORWARD_SELECTION and rec.get("node") is not None:
                original, _d = L.find_at_triple(nodes, L.node_triple(rec["node"]))
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
                              "companionNodeAction": rec["nodeAction"],
                              "companionRefusal": rec["refusal"],
                              "nodeCountAfter": len(rec["nodes"])})

        # Missing selected node in a non-forward case must quarantine, not fabricate.
        missing = None
        if case is not L.FORWARD_SELECTION:
            stripped = [n for n in nodes
                        if L._key(L.node_triple(n)) != L._key(
                            L.selected_triple(intent, markers))]
            owner = M.recover_transition_journal(dict(journal, state="COMMITTED"),
                                                 rctx(journal))
            rec = L.recover_nodes(owner, intent, digest, stripped, current, markers)
            check(rec["refusal"] == L.QUARANTINE,
                  label + ": missing selected node must quarantine")
            check(rec["nodeAction"] != "reconstructed-and-written",
                  label + ": missing selected node must not be reconstructed")
            missing = {"refusal": rec["refusal"], "rationale": rec["rationale"]}

        matrix.append({"case": label, "operation": intent["operation"],
                       "from": [intent["fromStoreGeneration"], intent["fromStateSchema"]],
                       "to": [intent["toStoreGeneration"], intent["toStateSchema"]],
                       "ownerShapeAdmitted": True, "selectionCase": case,
                       "publishesNode": published is not None,
                       "states": per_state, "missingSelectedNode": missing})
    return matrix


def section_d(M, fixtures):
    """Root's v3 counterexamples, now expected to behave."""
    intent = fixtures["intentStoreMigrate"]
    check(M.admit_transition_intent(intent) == [], "intentStoreMigrate must be admitted")
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    root = L.node(MARK_A, 3, 1, None, None)
    retained = L.node(MARK_B, 4, 2, L.node_triple(root), "1" * 64)
    nodes = [root, retained]
    check(not L.invariants(nodes), "the retained-branch lineage must start clean")
    markers = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}

    repeated = []
    for state in ("LEASED", "COMMITTED"):
        owner = M.recover_transition_journal(dict(journal, state=state), rctx(journal))
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root), markers)
        repeated.append({"state": state, "ownerAction": owner["action"],
                         "ownerJournalStateAfter": owner["journalStateAfter"],
                         "companionNodeAction": rec["nodeAction"],
                         "companionRefusal": rec["refusal"],
                         "nodeCountAfter": len(rec["nodes"]),
                         "rationale": rec["rationale"],
                         "invariantProblems": L.invariants(rec["nodes"])})
        check(rec["refusal"] is None,
              "retained branch at the same numeric pair must not refuse at " + state)
        check(not L.invariants(rec["nodes"]),
              "retained branch handling broke invariants at " + state)
    check(repeated[0]["nodeCountAfter"] == 2, "ABORT must write no node")
    check(repeated[1]["nodeCountAfter"] == 3,
          "a settled forward selection must write its own node beside the retained branch")

    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    missing = L.recover_nodes(owner, intent, digest, [], L.node_triple(root), markers)
    check(missing["refusal"] == L.QUARANTINE,
          "a forward reconstruction with an absent predecessor must refuse")
    check(len(missing["nodes"]) == 0, "a refused reconstruction must write nothing")
    check(not any("broken" in p for p in L.invariants(missing["nodes"]) if p.startswith("broken")),
          "a refused reconstruction must not leave broken ancestry")
    return {"retainedBranchRepeatedGeneration": repeated,
            "absentPredecessor": {"refusal": missing["refusal"],
                                  "rationale": missing["rationale"],
                                  "nodesWritten": len(missing["nodes"])}}


def section_e(M, fixtures):
    """Composed migrate -> rollback -> second forward selection, retained branch kept."""
    steps = []
    migrate = fixtures["intentStoreMigrate"]                       # (3,1) -> (4,2)
    rollback = dict(fixtures["intentStoreRollback"],
                    fromStoreGeneration=4, toStoreGeneration=3,
                    fromStateSchema=2, toStateSchema=1)            # (4,2) -> (3,1)
    second = dict(fixtures["intentStoreMigrate"],
                  fromStoreGeneration=3, toStoreGeneration=5,
                  preconditionGeneration=9)                        # (3,1) -> (5,2)
    for name, intent in (("migrate", migrate), ("rollback", rollback),
                         ("second-migrate", second)):
        check(M.admit_transition_intent(intent) == [],
              name + " must be owner shape-admitted: "
              + str(M.admit_transition_intent(intent)))

    nodes = [L.node(MARK_A, 3, 1, None, None)]
    current = L.node_triple(nodes[0])

    # 1. migrate (3,1) -> (4,2), new store MARK_NEW
    d1 = M.transition_intent_digest(migrate)
    j1 = M.transition_journal_record(migrate, REGISTRY)
    m1 = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    own1 = M.recover_transition_journal(dict(j1, state="COMMITTED"), rctx(j1))
    r1 = L.recover_nodes(own1, migrate, d1, nodes, current, m1)
    check(r1["refusal"] is None and r1["nodeAction"] == "reconstructed-and-written",
          "step 1 migrate must write its node")
    nodes = r1["nodes"]
    current = L.selected_triple(migrate, m1)
    steps.append({"step": "migrate (3,1)->(4,2)", "ownerAction": own1["action"],
                  "companion": r1["nodeAction"], "nodes": len(nodes),
                  "current": current})

    # 2. store-rollback (4,2) -> (3,1), re-selecting the retained root
    d2 = M.transition_intent_digest(rollback)
    j2 = M.transition_journal_record(rollback, REGISTRY)
    m2 = {"predecessorStoreRoot": MARK_NEW, "selectedStoreRoot": MARK_A}
    own2 = M.recover_transition_journal(dict(j2, state="COMMITTED"), rctx(j2))
    r2 = L.recover_nodes(own2, rollback, d2, nodes, current, m2)
    check(r2["refusal"] is None and r2["nodeAction"] == "validated-existing",
          "step 2 rollback must validate the retained root, not write: " + str(r2["refusal"]))
    check(r2["originPreserved"] == {"predecessor": None, "selectedByIntentDigest": None},
          "step 2 must preserve the retained root's origin")
    check(len(r2["nodes"]) == len(nodes), "step 2 must write no node")
    current = L.selected_triple(rollback, m2)
    steps.append({"step": "store-rollback (4,2)->(3,1)", "ownerAction": own2["action"],
                  "companion": r2["nodeAction"], "nodes": len(r2["nodes"]),
                  "originPreserved": r2["originPreserved"], "current": current})

    # 3. second forward selection (3,1) -> (5,2) while (4,2) is a retained branch
    d3 = M.transition_intent_digest(second)
    j3 = M.transition_journal_record(second, REGISTRY)
    m3 = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_F}
    own3 = M.recover_transition_journal(dict(j3, state="COMMITTED"), rctx(j3))
    r3 = L.recover_nodes(own3, second, d3, r2["nodes"], current, m3)
    check(r3["refusal"] is None and r3["nodeAction"] == "reconstructed-and-written",
          "step 3 must write a second forward node: " + str(r3["refusal"]))
    check(len(r3["nodes"]) == 3, "step 3 must leave three nodes")
    problems = L.invariants(r3["nodes"])
    check(not problems, "the branched lineage must stay clean: " + str(problems))
    retained = [n for n in r3["nodes"] if n["storeInstanceId"] == MARK_NEW]
    check(retained and retained[0]["selectedByIntentDigest"] == d1,
          "the retained branch must keep its original origin digest")
    steps.append({"step": "second migrate (3,1)->(5,2)", "ownerAction": own3["action"],
                  "companion": r3["nodeAction"], "nodes": len(r3["nodes"]),
                  "retainedBranchOriginUnchanged": bool(retained)
                  and retained[0]["selectedByIntentDigest"] == d1,
                  "invariantProblems": problems})
    return {"steps": steps, "finalLineage": r3["nodes"]}


def section_f(M, fixtures):
    """Damaged predecessor, duplicate full key, unreadable markers."""
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    owner = M.recover_transition_journal(dict(journal, state="COMMITTED"), rctx(journal))
    root = L.node(MARK_A, 3, 1, None, None)
    good = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    rows = []

    def case(name, nodes, markers, expect_refusal, expect_written):
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root), markers)
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
    # Duplicates are exercised where the decision path actually dereferences a
    # key: the predecessor lookup and the target lookup.
    dup_pred_same = [L.node(MARK_A, 3, 1, None, None), L.node(MARK_A, 3, 1, None, None)]
    case("duplicate predecessor key, identical contents", dup_pred_same, good,
         True, False)
    dup_pred_diff = [L.node(MARK_A, 3, 1, None, None),
                     L.node(MARK_A, 3, 1, L.triple(MARK_B, 2, 1), "7" * 64)]
    case("duplicate predecessor key, disagreeing contents", dup_pred_diff, good,
         True, False)
    target = L.node(MARK_NEW, 4, 2, L.triple(MARK_A, 3, 1), "8" * 64)
    dup_target_diff = [root, target, dict(target, selectedByIntentDigest="9" * 64)]
    case("duplicate target key, disagreeing contents", dup_target_diff, good,
         True, False)
    benign = L.node(MARK_B, 9, 2, L.triple(MARK_A, 3, 1), "5" * 64)
    case("duplicate key on an unrelated branch, identical contents",
         [root, benign, dict(benign)], good, False, True)
    existing_target = L.node(MARK_NEW, 4, 2, L.triple(MARK_A, 3, 1), "8" * 64)
    case("target key exists with a different origin", [root, existing_target],
         good, True, False)
    case("selected marker missing", [root],
         {"predecessorStoreRoot": MARK_A}, True, False)
    case("selected marker malformed", [root],
         {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": "zz"}, True, False)
    case("forward markers name the same store", [root],
         {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_A}, True, False)

    # An ancestor re-selection must not accept a same-numeric store off the chain.
    rollback = fixtures["intentStoreRollback"]                      # (4,2) -> (3,1)
    rdigest = M.transition_intent_digest(rollback)
    rjournal = M.transition_journal_record(rollback, REGISTRY)
    rowner = M.recover_transition_journal(dict(rjournal, state="COMMITTED"),
                                          rctx(rjournal))
    chain_root = L.node(MARK_B, 3, 1, None, None)
    cur = L.node(MARK_A, 4, 2, L.node_triple(chain_root), "1" * 64)
    off_chain = L.node(MARK_F, 3, 1, L.node_triple(cur), "2" * 64)
    rec = L.recover_nodes(rowner, rollback, rdigest, [chain_root, cur, off_chain],
                          L.node_triple(cur),
                          {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_F})
    rows.append({"case": "ancestor reselect naming an off-chain store at the same pair",
                 "refusal": rec["refusal"], "nodeAction": rec["nodeAction"],
                 "rationale": rec.get("rationale"),
                 "ok": rec["refusal"] == L.QUARANTINE})
    check(rec["refusal"] == L.QUARANTINE,
          "an off-chain store at the same numeric pair must not qualify as an ancestor")

    rec_ok = L.recover_nodes(rowner, rollback, rdigest, [chain_root, cur],
                             L.node_triple(cur),
                             {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_B})
    rows.append({"case": "ancestor reselect naming the verified chain member",
                 "refusal": rec_ok["refusal"], "nodeAction": rec_ok["nodeAction"],
                 "ok": rec_ok["refusal"] is None
                 and rec_ok["nodeAction"] == "validated-existing"})
    check(rec_ok["refusal"] is None and rec_ok["nodeAction"] == "validated-existing",
          "an on-chain ancestor must validate")
    return rows


def section_g(M, fixtures):
    """Owner actions that decide nothing must leave the companion silent."""
    intent = fixtures["intentStoreMigrate"]
    digest = M.transition_intent_digest(intent)
    journal = M.transition_journal_record(intent, REGISTRY)
    root = L.node(MARK_A, 3, 1, None, None)
    conflicting = L.node(MARK_NEW, 4, 2, L.node_triple(root), "8" * 64)
    nodes = [root, conflicting]
    markers = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}
    rows = []
    contexts = [
        ("fence not held", {"namespaceRegistry": REGISTRY, "fenceHeld": False,
                            "leasesReacquired": journal["leaseSet"],
                            "storeFootprint": None}),
        ("lease set not re-acquired", {"namespaceRegistry": REGISTRY, "fenceHeld": True,
                                       "leasesReacquired": ["ns-a"],
                                       "storeFootprint": None}),
        ("registry differs", {"namespaceRegistry": ["ns-a"], "fenceHeld": True,
                              "leasesReacquired": journal["leaseSet"],
                              "storeFootprint": None}),
        ("PREPARED store operation without a footprint",
         {"namespaceRegistry": REGISTRY, "fenceHeld": True,
          "leasesReacquired": journal["leaseSet"], "storeFootprint": None}),
    ]
    for name, ctx in contexts:
        state = "PREPARED" if name.startswith("PREPARED") else "COMMITTED"
        owner = M.recover_transition_journal(dict(journal, state=state), ctx)
        rec = L.recover_nodes(owner, intent, digest, nodes, L.node_triple(root), markers)
        ok = (rec["nodeAction"] == "no-decision" and rec["refusal"] is None
              and rec["case"] is None and len(rec["nodes"]) == len(nodes))
        rows.append({"context": name, "ownerAction": owner["action"],
                     "ownerRefusal": owner["refusal"],
                     "companionNodeAction": rec["nodeAction"],
                     "companionRefusal": rec["refusal"],
                     "companionInspectedNodes": rec["case"] is not None, "ok": ok})
        check(ok, "section G " + name + ": companion must make no decision, got "
              + str(rec["nodeAction"]) + "/" + str(rec["refusal"]))

    # Unfenced PREPARED store operation is an owner ABORT, not a no-decision.
    owner = M.recover_transition_journal(dict(journal, state="PREPARED"),
                                         rctx(journal, UNFENCED_PREPARED))
    rec = L.recover_nodes(owner, intent, digest, [root], L.node_triple(root), markers)
    rows.append({"context": "PREPARED store operation, old store not fenced",
                 "ownerAction": owner["action"],
                 "companionNodeAction": rec["nodeAction"],
                 "companionRefusal": rec["refusal"],
                 "ok": owner["action"] == "ABORT" and rec["refusal"] is None})
    check(owner["action"] == "ABORT" and rec["refusal"] is None,
          "an unfenced PREPARED store operation must abort with no companion refusal")
    return rows


def main():
    c25 = Path(sys.argv[1])
    M = load_owner(c25)
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
        "A_rootV2Regressions": section_a(M, fixtures),
        "B_ownerPairLaw": section_b(M, fixtures),
        "C_operationStateMatrix": section_c(M, fixtures),
        "D_rootV3Regressions": section_d(M, fixtures),
        "E_migrateRollbackSecondForward": section_e(M, fixtures),
        "F_damagedAndDuplicate": section_f(M, fixtures),
        "G_ownerActionsThatDecideNothing": section_g(M, fixtures),
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
