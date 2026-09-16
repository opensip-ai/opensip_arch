#!/usr/bin/env python3
"""Composed PS-01 control: actual frozen owner functions x all operation cases
x all six journal states.

Calls the frozen security_lifecycle_model_v1 admit_transition_intent,
transition_intent_digest, transition_journal_record and
recover_transition_journal directly. Every owner result printed here is that
model's own return value, not a stand-in. The companion's corrected
publication/recovery law is applied strictly after the owner's decision.

Reproduces root's two v2 counterexamples as regressions.

Design evidence only: no product code, no carrier behaviour, no qualification.

Usage: check_lineage_recovery.py <candidate25-root> [--json]
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lineage_law as L                                            # noqa: E402

SEC = "docs/coop/design-corrections/security"
FAILURES = []


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


REGISTRY = ["ns-b", "ns-a", "ns-c"]
MARK_A = "a" * 32          # the store selected before the transition
MARK_B = "b" * 32          # the ancestor at an earlier generation
MARK_NEW = "e" * 32        # a newly materialized store


def owner_intents(fixtures):
    """Six owner-admitted intents: five from the frozen fixtures, one composed.

    The frozen fixture set has no schema-retreating core-rollback, so one is
    composed and then ADMITTED BY THE OWNER before use.
    """
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


def lineage_for(intent):
    """A lawful starting lineage whose current node matches the intent's `from`.

    Root asked for different lawful starting states per case; the state schema
    enum is {1, 2}, so an ancestor at the retreat target is materialised when the
    intent's `to` pair names one.
    """
    root = L.node(MARK_B, intent["toStoreGeneration"], intent["toStateSchema"],
                  None, None)
    current = L.node(MARK_A, intent["fromStoreGeneration"], intent["fromStateSchema"],
                     L.node_triple(root), "1" * 64)
    if (intent["fromStoreGeneration"], intent["fromStateSchema"]) == \
            (intent["toStoreGeneration"], intent["toStateSchema"]):
        # same-store: the current node IS the selected node, and it is a root here
        return [L.node(MARK_A, intent["fromStoreGeneration"], intent["fromStateSchema"],
                       None, None)]
    ancestor_named = (intent["toStoreGeneration"], intent["toStateSchema"])
    if ancestor_named[0] < intent["fromStoreGeneration"]:
        return [root, current]                       # the `to` pair is a real ancestor
    return [L.node(MARK_A, intent["fromStoreGeneration"], intent["fromStateSchema"],
                   None, None)]                      # forward: nothing beyond the current


def main():
    c25 = Path(sys.argv[1])
    M = load_owner(c25)
    fixtures = json.loads((c25 / SEC / "transition-journal-cases.v1.json").read_text())["records"]

    # --- regression of root's two v2 counterexamples -------------------------
    regressions = []
    for label, base in (("core-rollback", "intentCoreRollback"),
                        ("store-rollback", "intentStoreRollback")):
        bad = dict(fixtures[base])
        bad.update({"fromStoreGeneration": 5, "fromStateSchema": 1,
                    "toStoreGeneration": 4, "toStateSchema": 1})
        refusals = M.admit_transition_intent(bad)
        regressions.append({"v2Label": label + " (5,1)->(4,1) mislabelled schema retreat",
                            "ownerRefusals": refusals})
        check(bool(refusals),
              "root counterexample no longer refuses for " + label)
    check(regressions[0]["ownerRefusals"] == ["TRANSITION.SAME_SCHEMA_KEEPS_STORE"],
          "core-rollback counterexample refusal changed")
    check(regressions[1]["ownerRefusals"] == ["TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT"],
          "store-rollback counterexample refusal changed")

    # --- the owner's pair law, read off the owner itself ---------------------
    pair_law = []
    for op in ("core-update", "core-rollback"):
        base = fixtures["intentUpdateSameSchema" if op == "core-update"
                        else "intentCoreRollback"]
        mismatch_a = dict(base)
        mismatch_a.update({"fromStateSchema": 2, "toStateSchema": 2,
                           "fromStoreGeneration": 4, "toStoreGeneration": 5})
        mismatch_b = dict(base)
        mismatch_b.update({"fromStateSchema": 1, "toStateSchema": 2,
                           "fromStoreGeneration": 4, "toStoreGeneration": 4})
        a = M.admit_transition_intent(mismatch_a)
        b = M.admit_transition_intent(mismatch_b)
        pair_law.append({"operation": op,
                         "sameSchemaDifferentStore": a,
                         "schemaChangeSameStore": b})
        check("TRANSITION.SAME_SCHEMA_KEEPS_STORE" in a,
              op + ": same schema must keep the store")
        check("TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE" in b,
              op + ": a schema change must select a new store")

    # --- all operation cases x all six journal states ------------------------
    matrix = []
    for label, intent, expected_case in owner_intents(fixtures):
        refusals = M.admit_transition_intent(intent)
        check(refusals == [], label + ": owner refused a supposedly admitted intent: "
              + str(refusals))
        if refusals:
            continue
        digest = M.transition_intent_digest(intent)
        journal = M.transition_journal_record(intent, REGISTRY)
        nodes = lineage_for(intent)
        current = L.node_triple(
            next(n for n in nodes
                 if (n["storeGeneration"], n["stateSchema"])
                 == (intent["fromStoreGeneration"], intent["fromStateSchema"])))
        markers = {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": MARK_NEW}

        case = L.selection_case(intent)
        check(case == expected_case,
              label + ": expected case " + expected_case + ", got " + case)

        pub_case, published = L.publish(intent, digest, nodes, current, markers)
        writes = published is not None
        check(writes == (case is L.FORWARD_SELECTION),
              label + ": only a forward selection may publish a node")
        if published is not None:
            check(published["predecessor"] != L.node_triple(published),
                  label + ": published node names itself as predecessor")

        per_state = []
        for state in M.TRANSITION_STATES:
            j = dict(journal, state=state)
            rctx = {"namespaceRegistry": REGISTRY, "fenceHeld": True,
                    "leasesReacquired": journal["leaseSet"],
                    "storeFootprint": ({"old": {"present": True,
                                                "unbootstrappedReason": "RESTORED"},
                                        "new": {"dir": "migrating", "state": "PREPARED"}}
                                       if state == "PREPARED" else None)}
            owner_result = M.recover_transition_journal(j, rctx)
            after_nodes = list(nodes)
            if owner_result["action"] in ("RESUME-COMMIT", "RELEASE-ONLY") and \
                    owner_result["journalStateAfter"] == "DONE" and \
                    case is L.FORWARD_SELECTION:
                pass                                  # recovery must reconstruct
            rec = L.recover_nodes(owner_result, intent, digest, after_nodes,
                                  current, markers)
            problems = L.invariants(rec["nodes"])
            check(not any("self-predecessor" in p for p in problems),
                  label + "/" + state + ": self-predecessor node produced")
            check(not any("cyclic" in p for p in problems),
                  label + "/" + state + ": cyclic ancestry produced")

            # Origins must be stable for the non-forward cases.
            if case is not L.FORWARD_SELECTION and rec.get("node") is not None:
                original = next(n for n in nodes
                                if L.node_triple(n) == L.node_triple(rec["node"]))
                check(rec["node"]["predecessor"] == original["predecessor"]
                      and rec["node"]["selectedByIntentDigest"]
                      == original["selectedByIntentDigest"],
                      label + "/" + state + ": recovery rewrote an existing origin")
                check(rec["nodeAction"] == "validated-existing",
                      label + "/" + state + ": non-forward case must only validate")
            if case is not L.FORWARD_SELECTION:
                check(rec["nodeAction"] != "reconstructed-and-written",
                      label + "/" + state + ": a non-forward case must never reconstruct")

            per_state.append({"journalState": state,
                              "ownerAction": owner_result["action"],
                              "ownerJournalStateAfter": owner_result["journalStateAfter"],
                              "ownerRefusal": owner_result["refusal"],
                              "companionNodeAction": rec["nodeAction"],
                              "companionRefusal": rec["refusal"],
                              "nodeCountAfter": len(rec["nodes"]),
                              "invariantProblems": problems})

        # Missing ancestry for a non-forward case must quarantine, never fabricate.
        missing_note = None
        if case is not L.FORWARD_SELECTION:
            stripped = [n for n in nodes
                        if (n["storeGeneration"], n["stateSchema"])
                        != (intent["toStoreGeneration"], intent["toStateSchema"])]
            owner_done = M.recover_transition_journal(dict(journal, state="COMMITTED"),
                                                      {"namespaceRegistry": REGISTRY,
                                                       "fenceHeld": True,
                                                       "leasesReacquired": journal["leaseSet"],
                                                       "storeFootprint": None})
            rec = L.recover_nodes(owner_done, intent, digest, stripped, current, markers)
            check(rec["refusal"] == L.QUARANTINE,
                  label + ": missing selected node must quarantine, not fabricate")
            check(rec.get("nodeAction") != "reconstructed-and-written",
                  label + ": missing selected node must not be reconstructed")
            missing_note = {"refusal": rec["refusal"], "rationale": rec["rationale"]}

        matrix.append({"case": label, "operation": intent["operation"],
                       "from": [intent["fromStoreGeneration"], intent["fromStateSchema"]],
                       "to": [intent["toStoreGeneration"], intent["toStateSchema"]],
                       "ownerAdmitted": refusals == [], "selectionCase": case,
                       "publishesNode": writes, "states": per_state,
                       "missingSelectedNode": missing_note})

    # --- root's exact same-store scenario, now correct ------------------------
    repair = fixtures["intentRepair"]
    digest = M.transition_intent_digest(repair)
    nodes = lineage_for(repair)
    current = L.node_triple(nodes[0])
    journal = M.transition_journal_record(repair, REGISTRY)
    owner_done = M.recover_transition_journal(
        dict(journal, state="COMMITTED"),
        {"namespaceRegistry": REGISTRY, "fenceHeld": True,
         "leasesReacquired": journal["leaseSet"], "storeFootprint": None})
    rec = L.recover_nodes(owner_done, repair, digest, nodes,
                          current, {"predecessorStoreRoot": MARK_A,
                                    "selectedStoreRoot": MARK_A})
    check(rec["nodeAction"] == "validated-existing",
          "same-store repair must validate the existing node")
    check(len(rec["nodes"]) == len(nodes), "same-store repair must write no node")
    check(not L.invariants(rec["nodes"]), "same-store repair must leave invariants clean")
    root_case = {"ownerAdmitted": M.admit_transition_intent(repair) == [],
                 "ownerAction": owner_done["action"],
                 "companionNodeAction": rec["nodeAction"],
                 "selfPredecessorProduced": any(
                     n["predecessor"] == L.node_triple(n) for n in rec["nodes"]),
                 "originPreserved": rec.get("originPreserved"),
                 "v2Defect": "unconditional reconstruction produced predecessor == self"}
    check(root_case["selfPredecessorProduced"] is False,
          "the v2 self-predecessor defect must not reproduce")

    # --- retry after abort, and replay after commit --------------------------
    migrate = fixtures["intentStoreMigrate"]
    mdigest = M.transition_intent_digest(migrate)
    mnodes = lineage_for(migrate)
    mcurrent = L.node_triple(mnodes[0])
    mjournal = M.transition_journal_record(migrate, REGISTRY)
    aborted = M.recover_transition_journal(
        dict(mjournal, state="PREPARED"),
        {"namespaceRegistry": REGISTRY, "fenceHeld": True,
         "leasesReacquired": mjournal["leaseSet"],
         "storeFootprint": {"old": {"present": True, "unbootstrappedReason": None},
                            "new": {"dir": "migrating", "state": "PREPARED"}}})
    rec_abort = L.recover_nodes(aborted, migrate, mdigest, mnodes, mcurrent,
                                {"predecessorStoreRoot": MARK_A,
                                 "selectedStoreRoot": MARK_NEW})
    check(aborted["action"] == "ABORT", "unfenced PREPARED store op must abort")
    check(len(rec_abort["nodes"]) == len(mnodes), "an aborted attempt must write no node")
    _case, retried = L.publish(migrate, mdigest, mnodes, mcurrent,
                               {"predecessorStoreRoot": MARK_A, "selectedStoreRoot": "f" * 32})
    after_retry = mnodes + [retried]
    check(not L.invariants(after_retry), "a lawful retry must keep invariants clean")
    retry = {"ownerAbortAction": aborted["action"],
             "nodesAfterAbort": len(rec_abort["nodes"]),
             "retryNodeKey": [retried["storeInstanceId"], retried["storeGeneration"],
                              retried["stateSchema"]],
             "retryPredecessorIsSelf": retried["predecessor"] == L.node_triple(retried),
             "invariantsAfterRetry": L.invariants(after_retry)}

    result = {"control": "check_lineage_recovery",
              "ownerModel": {"path": SEC + "/security_lifecycle_model_v1.py",
                             "functionsCalled": ["admit_transition_intent",
                                                 "transition_intent_digest",
                                                 "transition_journal_record",
                                                 "recover_transition_journal"]},
              "rootCounterexampleRegressions": regressions,
              "ownerPairLaw": pair_law,
              "sameStoreRepairFixed": root_case,
              "operationStateMatrix": matrix,
              "retryTrace": retry,
              "failures": FAILURES,
              "status": "PASS" if not FAILURES else "FAIL",
              "limits": ("Owner results are the frozen model's own returns. The companion "
                         "law is a design reference: no product code, no carrier behaviour, "
                         "no qualification.")}
    print(json.dumps(result, indent=1))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
