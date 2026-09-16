"""Corrected PS-01 lineage publication and recovery law, revision 3.

One module so publication and recovery cannot drift: both derive the selection
case from the SAME admitted intent members, which is exactly the defect root
demonstrated in v2 (an unconditional reconstruction produced a self-predecessor
node on an owner-admitted same-store core-repair).

Design reference only. Not product code, not a carrier implementation.
"""

SAME_STORE = "same-store"
ANCESTOR_RESELECT = "ancestor-reselect"
FORWARD_SELECTION = "forward-selection"

QUARANTINE = "QUARANTINE/MIGRATION.CORRUPT"
UNADMITTED = "unadmitted-intent-shape"


def triple(instance_id, generation, state_schema):
    return {"storeInstanceId": instance_id, "storeGeneration": generation,
            "stateSchema": state_schema}


def node(instance_id, generation, state_schema, predecessor, intent_digest):
    """A lineage node. predecessor and intent digest are null together (root)."""
    return {"schemaVersion": 1, "storeInstanceId": instance_id,
            "storeGeneration": generation, "stateSchema": state_schema,
            "predecessor": predecessor, "selectedByIntentDigest": intent_digest}


def node_triple(n):
    return triple(n["storeInstanceId"], n["storeGeneration"], n["stateSchema"])


def ancestry(nodes, start):
    """Walk predecessor links from `start`. Returns (chain, terminated_cleanly)."""
    chain, seen, cursor = [], set(), start
    while cursor is not None:
        key = (cursor["storeInstanceId"], cursor["storeGeneration"], cursor["stateSchema"])
        if key in seen:
            return chain, False                      # cycle; never lawful
        seen.add(key)
        found = next((n for n in nodes if node_triple(n) == cursor), None)
        if found is None:
            return chain, False                      # broken ancestry
        chain.append(found)
        cursor = found["predecessor"]
    return chain, True


def selection_case(intent):
    """A pure function of the ADMITTED intent. It never reads the node set.

    The owner's admit_transition_intent already fixes the pair for every
    operation: a core operation keeps the store exactly when the schema is
    unchanged (TRANSITION.SAME_SCHEMA_KEEPS_STORE and
    TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE), core-update never lowers the
    schema, core-rollback never raises it, store-migrate requires an advance and
    store-rollback a retreat, and both store operations require a different
    generation. So over the admitted space:

        same store and same schema  -> SAME_STORE
        schema advances             -> FORWARD_SELECTION
        schema retreats             -> ANCESTOR_RESELECT

    and no admitted intent changes the store with an unchanged schema.

    Deriving the case from the intent alone is deliberate. An earlier revision
    asked whether the `to` pair appeared in the stored ancestry, which let a
    DAMAGED lineage silently reclassify a rollback as a forward selection and
    fabricate a node. The case must be decidable without trusting the very
    records recovery is about to check.
    """
    same_store = intent["fromStoreGeneration"] == intent["toStoreGeneration"]
    same_schema = intent["fromStateSchema"] == intent["toStateSchema"]
    if same_store and same_schema:
        return SAME_STORE
    if intent["toStateSchema"] > intent["fromStateSchema"]:
        return FORWARD_SELECTION
    if intent["toStateSchema"] < intent["fromStateSchema"]:
        return ANCESTOR_RESELECT
    return UNADMITTED


def publish(intent, intent_digest, nodes, current_triple, markers):
    """Normal publication after the journal record is durably COMMITTED.

    Only a forward selection writes a node. Returns (case, node_or_None).
    """
    case = selection_case(intent)
    if case is not FORWARD_SELECTION:
        return case, None
    return case, node(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                      intent["toStateSchema"],
                      triple(markers["predecessorStoreRoot"],
                             intent["fromStoreGeneration"], intent["fromStateSchema"]),
                      intent_digest)


def expected_node_for(intent, intent_digest, case, nodes, current_triple, markers):
    """What recovery expects to find, per case. Only FORWARD is reconstructible."""
    if case is FORWARD_SELECTION:
        _case, rebuilt = publish(intent, intent_digest, nodes, current_triple, markers)
        return {"kind": "reconstructible", "node": rebuilt}
    if case is SAME_STORE:
        return {"kind": "pre-existing", "triple": current_triple}
    selected = triple(None, intent["toStoreGeneration"], intent["toStateSchema"])
    return {"kind": "pre-existing-ancestor", "triple": selected}


def _find_by_generation_schema(nodes, generation, state_schema):
    return [n for n in nodes
            if (n["storeGeneration"], n["stateSchema"]) == (generation, state_schema)]


def recover_nodes(owner_result, intent, intent_digest, nodes, current_triple, markers):
    """Companion recovery, applied strictly after the owner's own decision.

    `owner_result` is the dict returned by the frozen
    recover_transition_journal. The companion never overrides it; it acts only
    where the owner's action settles the transition as committed.
    """
    action = owner_result.get("action")
    after = owner_result.get("journalStateAfter")
    out = {"ownerAction": action, "ownerJournalStateAfter": after,
           "case": None, "nodeAction": None, "refusal": None, "nodes": list(nodes)}

    carries_this_intent = [n for n in nodes
                           if n["selectedByIntentDigest"] == intent_digest]

    settled_committed = (action in ("RESUME-COMMIT", "RELEASE-ONLY") and after == "DONE")
    if not settled_committed:
        # Pre-COMMITTED or aborted. Pre-existing ancestry is expected and
        # untouched; what must not exist is a NEW node for THIS transition.
        out["nodeAction"] = "none"
        if carries_this_intent:
            out["refusal"] = QUARANTINE
            out["rationale"] = ("premature new node: a node carries this transition's "
                                "intentDigest while the owner has not settled it as committed")
            return out
        case = selection_case(intent)
        out["case"] = case
        if case is FORWARD_SELECTION and _find_by_generation_schema(
                nodes, intent["toStoreGeneration"], intent["toStateSchema"]):
            out["refusal"] = QUARANTINE
            out["rationale"] = ("premature new node: a node already occupies the "
                                "forward selection target before commit")
            return out
        out["rationale"] = ("owner action " + str(action) + "; pre-existing ancestry is "
                            "expected and is neither written nor rewritten")
        return out

    case = selection_case(intent)
    out["case"] = case

    if case is FORWARD_SELECTION:
        _c, rebuilt = publish(intent, intent_digest, nodes, current_triple, markers)
        if not markers.get("selectedStoreRoot") or not markers.get("predecessorStoreRoot"):
            out["refusal"] = QUARANTINE
            out["rationale"] = "a store-root marker is unreadable; nothing is reconstructed"
            return out
        if rebuilt["predecessor"] == node_triple(rebuilt):
            out["refusal"] = QUARANTINE
            out["rationale"] = ("reconstruction would name itself as predecessor; "
                                "refused rather than written")
            return out
        existing = _find_by_generation_schema(nodes, intent["toStoreGeneration"],
                                              intent["toStateSchema"])
        if not existing:
            out["nodeAction"] = "reconstructed-and-written"
            out["nodes"] = list(nodes) + [rebuilt]
            out["node"] = rebuilt
            out["rationale"] = ("this transition created the node, so its origin is "
                                "derivable from this committed intent plus the markers")
            return out
        if existing[0] != rebuilt:
            out["refusal"] = QUARANTINE
            out["rationale"] = "stored node disagrees with the reconstruction"
            return out
        out["nodeAction"] = "validated"
        out["node"] = existing[0]
        out["rationale"] = "stored node equals the reconstruction"
        return out

    # SAME_STORE and ANCESTOR_RESELECT: the selected node was created by an
    # EARLIER, unrelated act. This intent cannot reconstruct an origin it never
    # created, so absence is a quarantine and presence is validated, never rewritten.
    if case is SAME_STORE:
        selected = current_triple
        check_same = (intent["toStoreGeneration"], intent["toStateSchema"]) == \
            (current_triple["storeGeneration"], current_triple["stateSchema"])
        if not check_same:
            out["refusal"] = QUARANTINE
            out["rationale"] = "same-store case whose to pair is not the current triple"
            return out
    else:
        candidates = _find_by_generation_schema(nodes, intent["toStoreGeneration"],
                                                intent["toStateSchema"])
        if len(candidates) != 1:
            out["refusal"] = QUARANTINE
            out["rationale"] = ("re-selected ancestor is missing or ambiguous; the current "
                                "intent names a different origin and cannot repair it")
            return out
        selected = node_triple(candidates[0])
        # The owner has no lineage knowledge, so it cannot check that a rollback
        # target really is an ancestor. The companion must.
        chain, clean = ancestry(nodes, current_triple)
        if not clean or selected not in [node_triple(n) for n in chain]:
            out["refusal"] = QUARANTINE
            out["rationale"] = ("the re-selected generation is not an ancestor of the "
                                "current node, or the chain to it is broken")
            return out

    found = next((n for n in nodes if node_triple(n) == selected), None)
    if found is None:
        out["refusal"] = QUARANTINE
        out["rationale"] = ("the selected store's node is missing; this transition never "
                            "created it, so no repair can reconstruct its origin from this "
                            "unrelated intent")
        return out
    if found["selectedByIntentDigest"] == intent_digest:
        out["refusal"] = QUARANTINE
        out["rationale"] = "an existing node claims this transition as its origin"
        return out
    chain, clean = ancestry(nodes, selected)
    if not clean:
        out["refusal"] = QUARANTINE
        out["rationale"] = "the selected node's ancestry is broken or cyclic"
        return out
    out["nodeAction"] = "validated-existing"
    out["node"] = found
    out["originPreserved"] = {"predecessor": found["predecessor"],
                              "selectedByIntentDigest": found["selectedByIntentDigest"]}
    out["rationale"] = ("the retained node keeps its original predecessor and origin "
                        "digest; recovery validates and never rewrites it")
    return out


def invariants(nodes):
    """Structural invariants every lineage must satisfy."""
    problems = []
    roots = [n for n in nodes if n["predecessor"] is None]
    for n in nodes:
        if n["predecessor"] == node_triple(n):
            problems.append("self-predecessor: " + n["storeInstanceId"])
        if (n["predecessor"] is None) != (n["selectedByIntentDigest"] is None):
            problems.append("unpaired nulls: " + n["storeInstanceId"])
    for n in nodes:
        _chain, clean = ancestry(nodes, node_triple(n))
        if not clean:
            problems.append("broken or cyclic ancestry from: " + n["storeInstanceId"])
    if len(roots) != 1:
        problems.append("expected exactly one lineage root, found " + str(len(roots)))
    keys = [(n["storeInstanceId"], n["storeGeneration"], n["stateSchema"]) for n in nodes]
    if len(set(keys)) != len(keys):
        problems.append("duplicate primary key")
    return problems
