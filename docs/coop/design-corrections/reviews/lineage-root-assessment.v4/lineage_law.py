"""PS-01 lineage publication and recovery law, revision 4.

One module so publication and recovery cannot drift. Revision 4 corrects the
identity-selection boundary root demonstrated against revision 3:

  * A node is identified by its FULL TRIPLE, and the instance component comes
    from the store-root MARKER of the store the transition actually selects.
    Revision 3 searched by the numeric (storeGeneration, stateSchema) pair, so a
    retained old branch at (b,4,2) blocked a fresh target at (e,4,2) and produced
    two wrong quarantines against owner ABORT and RESUME-COMMIT.
  * intentDigest is never a global search key. The record's own schema says it
    may repeat, so it is validated ON the selected node, never scanned for.
  * One admission law, admit_node(), is applied by BOTH publish and recover.
    Revision 3 reconstructed a forward node without checking that its predecessor
    existed, writing broken ancestry with no refusal; the whole-set invariants()
    helper caught it but was never on the decision path.
  * Markers are validated before any dereference.
  * BUSY, REFUSE and QUARANTINE mean no companion decision at all: the node set
    is not inspected, matching the prose.

Design reference only. Not product code, not a carrier implementation.
"""

SAME_STORE = "same-store"
ANCESTOR_RESELECT = "ancestor-reselect"
FORWARD_SELECTION = "forward-selection"
UNADMITTED = "unadmitted-intent-shape"

QUARANTINE = "QUARANTINE/MIGRATION.CORRUPT"

NODE_MEMBERS = {"schemaVersion", "storeInstanceId", "storeGeneration",
                "stateSchema", "predecessor", "selectedByIntentDigest"}

# Owner actions that settle a transition as committed, and those that decide nothing.
SETTLING = (("RESUME-COMMIT", "DONE"), ("RELEASE-ONLY", "DONE"))
NO_DECISION_ACTIONS = ("BUSY", "REFUSE", "QUARANTINE")


def triple(instance_id, generation, state_schema):
    return {"storeInstanceId": instance_id, "storeGeneration": generation,
            "stateSchema": state_schema}


def node(instance_id, generation, state_schema, predecessor, intent_digest):
    return {"schemaVersion": 1, "storeInstanceId": instance_id,
            "storeGeneration": generation, "stateSchema": state_schema,
            "predecessor": predecessor, "selectedByIntentDigest": intent_digest}


def node_triple(n):
    return triple(n["storeInstanceId"], n["storeGeneration"], n["stateSchema"])


def _key(t):
    return (t["storeInstanceId"], t["storeGeneration"], t["stateSchema"])


def find_at_triple(nodes, t):
    """Exact full-triple lookup. Returns (node|None, refusal|None).

    A duplicate primary key whose contents disagree refuses; it never picks one.
    """
    hits = [n for n in nodes if _key(node_triple(n)) == _key(t)]
    if not hits:
        return None, None
    first = hits[0]
    if any(h != first for h in hits[1:]):
        return None, QUARANTINE
    return first, None


def ancestry(nodes, start):
    """Walk predecessor links from a full triple. Returns (chain, clean)."""
    chain, seen, cursor = [], set(), start
    while cursor is not None:
        if _key(cursor) in seen:
            return chain, False
        seen.add(_key(cursor))
        found, dup = find_at_triple(nodes, cursor)
        if dup is not None or found is None:
            return chain, False
        chain.append(found)
        cursor = found["predecessor"]
    return chain, True


def selection_case(intent):
    """A pure function of the ADMITTED intent. It never reads the node set.

    The owner's admit_transition_intent fixes the schema/store pair, so over the
    admitted space: same store and same schema is SAME_STORE, an advancing schema
    is FORWARD_SELECTION, a retreating schema is ANCESTOR_RESELECT, and no
    admitted intent changes the store with an unchanged schema.
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


# --- markers ----------------------------------------------------------------

HEX32 = "0123456789abcdef"


def _marker_ok(value):
    return (isinstance(value, str) and len(value) == 32
            and all(c in HEX32 for c in value))


def markers_refusal(markers, case):
    """Validate markers BEFORE any dereference. Returns a refusal or None.

    selectedStoreRoot is the storeInstanceId read from the root of the store this
    transition selects: the new store for a forward selection, the retained
    ancestor for a re-selection, the unchanged store for a same-store operation.
    predecessorStoreRoot is the root of the store it comes from.
    """
    if not isinstance(markers, dict):
        return QUARANTINE
    needed = ["selectedStoreRoot", "predecessorStoreRoot"]
    for name in needed:
        if name not in markers or not _marker_ok(markers.get(name)):
            return QUARANTINE
    if case is SAME_STORE and markers["selectedStoreRoot"] != markers["predecessorStoreRoot"]:
        return QUARANTINE
    if case is FORWARD_SELECTION and \
            markers["selectedStoreRoot"] == markers["predecessorStoreRoot"]:
        return QUARANTINE
    return None


def selected_triple(intent, markers):
    return triple(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                  intent["toStateSchema"])


def outgoing_triple(intent, markers):
    return triple(markers["predecessorStoreRoot"], intent["fromStoreGeneration"],
                  intent["fromStateSchema"])


# --- the one admission law --------------------------------------------------

def admit_node(candidate, nodes):
    """The single node admission law. Publication and recovery both call it.

    Returns (refusal|None, resulting_nodes, disposition).
    """
    if not isinstance(candidate, dict) or set(candidate) != NODE_MEMBERS:
        return QUARANTINE, list(nodes), "shape"
    if candidate["schemaVersion"] != 1:
        return QUARANTINE, list(nodes), "schema-version"
    pred, digest = candidate["predecessor"], candidate["selectedByIntentDigest"]
    if (pred is None) != (digest is None):
        return QUARANTINE, list(nodes), "unpaired-nulls"
    if pred is not None:
        if not isinstance(pred, dict) or set(pred) != {"storeInstanceId",
                                                       "storeGeneration", "stateSchema"}:
            return QUARANTINE, list(nodes), "predecessor-shape"
        if _key(pred) == _key(node_triple(candidate)):
            return QUARANTINE, list(nodes), "self-predecessor"
        # Predecessor presence is checked HERE, on the decision path.
        found, dup = find_at_triple(nodes, pred)
        if dup is not None:
            return QUARANTINE, list(nodes), "duplicate-predecessor-key"
        if found is None:
            return QUARANTINE, list(nodes), "predecessor-absent"

    existing, dup = find_at_triple(nodes, node_triple(candidate))
    if dup is not None:
        return QUARANTINE, list(nodes), "duplicate-primary-key-disagrees"
    if existing is not None:
        if existing != candidate:
            return QUARANTINE, list(nodes), "primary-key-contents-disagree"
        return None, list(nodes), "idempotent"

    result = list(nodes) + [candidate]
    _chain, clean = ancestry(result, node_triple(candidate))
    if not clean:
        return QUARANTINE, list(nodes), "broken-or-cyclic-ancestry"
    roots = [n for n in result if n["predecessor"] is None]
    if len(roots) != 1:
        return QUARANTINE, list(nodes), "expected-exactly-one-lineage-root"
    return None, result, "written"


# --- publication ------------------------------------------------------------

def publish(intent, intent_digest, nodes, current_triple, markers):
    """Publication after the journal record is durably COMMITTED.

    Returns (case, refusal|None, resulting_nodes, node|None).
    Only a forward selection writes, and it writes through admit_node.
    """
    case = selection_case(intent)
    refusal = markers_refusal(markers, case)
    if refusal is not None:
        return case, refusal, list(nodes), None
    if case is not FORWARD_SELECTION:
        return case, None, list(nodes), None
    candidate = node(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                     intent["toStateSchema"], outgoing_triple(intent, markers),
                     intent_digest)
    refusal, result, _disposition = admit_node(candidate, nodes)
    if refusal is not None:
        return case, refusal, list(nodes), None
    return case, None, result, candidate


# --- recovery ---------------------------------------------------------------

def _classify(owner_result):
    action = owner_result.get("action")
    after = owner_result.get("journalStateAfter")
    if action in NO_DECISION_ACTIONS:
        return "no-decision"
    if (action, after) in SETTLING:
        return "settled"
    if action in ("ABORT", "RELEASE-ONLY"):
        return "not-settled"
    return "no-decision"


def recover_nodes(owner_result, intent, intent_digest, nodes, current_triple, markers):
    """Companion recovery, applied strictly after the owner's own decision."""
    action = owner_result.get("action")
    after = owner_result.get("journalStateAfter")
    out = {"ownerAction": action, "ownerJournalStateAfter": after,
           "case": None, "nodeAction": None, "refusal": None, "nodes": list(nodes)}
    disposition = _classify(owner_result)

    if disposition == "no-decision":
        # BUSY, REFUSE, QUARANTINE: the node set is not inspected at all.
        out["nodeAction"] = "no-decision"
        out["rationale"] = ("owner action " + str(action) + " makes no transition "
                            "decision; the companion inspects nothing and changes nothing")
        return out

    case = selection_case(intent)
    out["case"] = case
    refusal = markers_refusal(markers, case)
    if refusal is not None:
        out["nodeAction"] = "none"
        out["refusal"] = refusal
        out["rationale"] = ("a store-root marker is missing or unreadable; nothing is "
                            "read, dereferenced or written")
        return out

    selected = selected_triple(intent, markers)

    if disposition == "not-settled":
        # ABORT, or RELEASE-ONLY reaching ABORTED. Pre-existing ancestry is
        # expected and untouched. What must not exist is a NEW node for THIS
        # attempt, identified by ITS OWN FULL TRIPLE, never by a numeric pair and
        # never by scanning for an intentDigest that may lawfully repeat.
        out["nodeAction"] = "none"
        existing, dup = find_at_triple(nodes, selected)
        if dup is not None:
            out["refusal"] = QUARANTINE
            out["rationale"] = "duplicate primary key with disagreeing contents"
            return out
        if case is FORWARD_SELECTION and existing is not None:
            out["refusal"] = QUARANTINE
            out["rationale"] = ("premature new node: a node already occupies THIS "
                                "attempt's own target triple before the owner settled it")
            return out
        if existing is not None and existing["selectedByIntentDigest"] == intent_digest:
            out["refusal"] = QUARANTINE
            out["rationale"] = ("a node at the selected triple already claims this "
                                "unsettled transition as its origin")
            return out
        out["rationale"] = ("owner action " + str(action) + "; a retained branch at the "
                            "same numeric generation is a different store and is neither "
                            "read as this attempt's node nor disturbed")
        return out

    # settled: RESUME-COMMIT or RELEASE-ONLY reaching DONE.
    if case is FORWARD_SELECTION:
        candidate = node(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                         intent["toStateSchema"], outgoing_triple(intent, markers),
                         intent_digest)
        refusal, result, dispo = admit_node(candidate, nodes)
        if refusal is not None:
            out["refusal"] = refusal
            out["rationale"] = "node admission refused: " + dispo
            return out
        out["nodes"] = result
        out["node"] = candidate
        out["nodeAction"] = ("validated" if dispo == "idempotent"
                             else "reconstructed-and-written")
        out["rationale"] = ("this transition created the node at its own full triple, so "
                            "its origin is derivable from this committed intent plus the "
                            "markers; the same admission law as publication applied")
        return out

    # SAME_STORE and ANCESTOR_RESELECT: the selected node was created by an
    # EARLIER, unrelated act. This intent cannot reconstruct an origin it never
    # created, so absence is a quarantine and presence is validated, never rewritten.
    if case is SAME_STORE and _key(selected) != _key(current_triple):
        out["refusal"] = QUARANTINE
        out["rationale"] = ("same-store case whose selected marker and to pair are not "
                            "the current triple")
        return out

    found, dup = find_at_triple(nodes, selected)
    if dup is not None:
        out["refusal"] = QUARANTINE
        out["rationale"] = "duplicate primary key with disagreeing contents"
        return out
    if found is None:
        out["refusal"] = QUARANTINE
        out["rationale"] = ("the selected store's node is missing at its own full triple; "
                            "this transition never created it, so no repair can "
                            "reconstruct its origin from this unrelated intent")
        return out
    if found["selectedByIntentDigest"] == intent_digest:
        out["refusal"] = QUARANTINE
        out["rationale"] = "an existing node claims this transition as its origin"
        return out

    chain, clean = ancestry(nodes, current_triple)
    if not clean:
        out["refusal"] = QUARANTINE
        out["rationale"] = "the chain from the current node is broken or cyclic"
        return out
    if case is ANCESTOR_RESELECT and \
            _key(selected) not in [_key(node_triple(n)) for n in chain]:
        out["refusal"] = QUARANTINE
        out["rationale"] = ("the re-selected store is not on the verified chain from the "
                            "current node; a matching numeric generation elsewhere is a "
                            "different store and never qualifies")
        return out

    out["nodeAction"] = "validated-existing"
    out["node"] = found
    out["originPreserved"] = {"predecessor": found["predecessor"],
                              "selectedByIntentDigest": found["selectedByIntentDigest"]}
    out["rationale"] = ("the retained node keeps its original predecessor and origin "
                        "digest; recovery validates at the full triple and never rewrites")
    return out


def invariants(nodes):
    """Whole-set auditor for controls. admit_node is the decision boundary."""
    problems = []
    for n in nodes:
        if set(n) != NODE_MEMBERS:
            problems.append("member set: " + str(n.get("storeInstanceId")))
        if n["predecessor"] is not None and _key(n["predecessor"]) == _key(node_triple(n)):
            problems.append("self-predecessor: " + n["storeInstanceId"])
        if (n["predecessor"] is None) != (n["selectedByIntentDigest"] is None):
            problems.append("unpaired nulls: " + n["storeInstanceId"])
        _chain, clean = ancestry(nodes, node_triple(n))
        if not clean:
            problems.append("broken or cyclic ancestry from: " + n["storeInstanceId"])
    roots = [n for n in nodes if n["predecessor"] is None]
    if len(roots) != 1:
        problems.append("expected exactly one lineage root, found " + str(len(roots)))
    keys = [_key(node_triple(n)) for n in nodes]
    if len(set(keys)) != len(keys):
        problems.append("duplicate primary key")
    return problems
