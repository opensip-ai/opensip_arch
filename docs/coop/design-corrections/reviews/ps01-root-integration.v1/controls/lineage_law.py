"""PS-01 lineage publication and recovery law, revision 5.

One module so publication and recovery cannot drift. Revision 5 corrects the two
final-boundary defects root demonstrated against revision 4:

  * PHASE-SENSITIVE MARKERS. A forward selection's target store does not exist at
    LEASED or PREPARING, and an unpublished target may already be reclaimed at
    ABORTED. Revision 4 required selectedStoreRoot in every branch, turning the
    owner's lawful early ABORT into a quarantine. The requirement is now bound to
    the owner's own decision: only a settled transition needs the target marker.
    Before materialisation an absent target is expected and the owner's abort
    stands; an observed-but-unreadable target still refuses.
  * IDEMPOTENT PATH VALIDATION. admit_node returned "idempotent" on an exact key
    match BEFORE checking ancestry, so an existing target whose chain was broken
    validated with no refusal. Ancestry and uniqueness are now checked on the
    idempotent path too, still writing nothing and never rewriting an origin.

Two scoping corrections follow directly:

  * The single-lineage-root rule is a COMPONENT invariant, not a global one. An
    authorized restore or adoption starts a separate lineage with its own root, so
    several roots may coexist across unrelated stores. What must hold is that the
    chain from the node under consideration terminates cleanly at exactly one root.
  * Node shape is admitted through a REAL schema validator supplied by the caller,
    not by ad hoc member and type guesses here. A caller that supplies none must
    say so explicitly with ASSUME_SCHEMA_ADMITTED, which controls record as a
    labelled input assumption; otherwise the law refuses rather than assuming.

Design reference only. Not product code, not a carrier implementation, and not a
product parser.
"""

SAME_STORE = "same-store"
ANCESTOR_RESELECT = "ancestor-reselect"
FORWARD_SELECTION = "forward-selection"
UNADMITTED = "unadmitted-intent-shape"

QUARANTINE = "QUARANTINE/MIGRATION.CORRUPT"

# A caller that has already schema-admitted its nodes says so explicitly.
ASSUME_SCHEMA_ADMITTED = "assume-schema-admitted"

# Owner actions that settle a transition as committed, and those that decide nothing.
SETTLING = (("RESUME-COMMIT", "DONE"), ("RELEASE-ONLY", "DONE"))
NO_DECISION_ACTIONS = ("BUSY", "REFUSE", "QUARANTINE")

# Target-store observation outcomes, distinct on purpose.
TARGET_ABSENT = None            # store root not materialised yet, or already reclaimed

HEX32 = "0123456789abcdef"


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
    """Walk predecessor links from a full triple. Returns (chain, clean).

    clean means every hop was found at its exact triple, no cycle was met, and the
    walk terminated at a lineage root. It is the component-scoped form of the
    one-root rule: this chain reaches exactly one root.
    """
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
    return chain, bool(chain)


def selection_case(intent):
    """A pure function of the ADMITTED intent. It never reads the node set."""
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

def _marker_readable(value):
    return (isinstance(value, str) and len(value) == 32
            and all(c in HEX32 for c in value))


def target_observation(markers):
    """Classify the selected-store marker. Three outcomes, deliberately distinct.

      "readable"   a 32-lowercase-hex identity was read from the target store root
      "absent"     selectedStoreRoot is explicitly None: no target store root is
                   present. Before materialisation, and after an unpublished
                   target is reclaimed, this is the expected observation.
      "unreadable" a target was observed but its marker is missing or malformed.
                   This is NOT absence and never becomes one.
      "not-observed" the caller supplied no observation at all.
    """
    if "selectedStoreRoot" not in markers:
        return "not-observed"
    value = markers["selectedStoreRoot"]
    if value is TARGET_ABSENT:
        return "absent"
    if _marker_readable(value):
        return "readable"
    return "unreadable"


def markers_refusal(markers, case, settled):
    """Validate markers BEFORE any dereference, bound to the owner's phase.

    settled is True only when the owner's own action settled the transition as
    committed. A settled transition's selected store exists by construction, so
    its marker is required. An unsettled transition may precede materialisation.
    """
    if not isinstance(markers, dict):
        return QUARANTINE, "markers were not supplied"
    if not _marker_readable(markers.get("predecessorStoreRoot")):
        return QUARANTINE, ("the predecessor store root marker is missing or "
                            "unreadable; the store a transition comes from always exists")
    observation = target_observation(markers)
    if observation == "unreadable":
        return QUARANTINE, ("a target store root was observed but its marker is "
                            "unreadable; an unreadable target is never treated as absent")
    if settled:
        if observation != "readable":
            return QUARANTINE, ("a settled transition's selected store must have a "
                                "readable marker; observation was " + observation)
        if case is SAME_STORE and \
                markers["selectedStoreRoot"] != markers["predecessorStoreRoot"]:
            return QUARANTINE, "a same-store selection must name one store"
        if case is FORWARD_SELECTION and \
                markers["selectedStoreRoot"] == markers["predecessorStoreRoot"]:
            return QUARANTINE, "a forward selection must name a different store"
        return None, None
    # Unsettled: the target may lawfully not exist yet or have been reclaimed.
    if observation == "not-observed":
        return QUARANTINE, ("no target observation was supplied; absence must be "
                            "stated explicitly, never inferred from a missing key")
    if observation == "readable" and case is SAME_STORE and \
            markers["selectedStoreRoot"] != markers["predecessorStoreRoot"]:
        return QUARANTINE, "a same-store selection must name one store"
    return None, None


def selected_triple(intent, markers):
    return triple(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                  intent["toStateSchema"])


def outgoing_triple(intent, markers):
    return triple(markers["predecessorStoreRoot"], intent["fromStoreGeneration"],
                  intent["fromStateSchema"])


# --- schema admission boundary ----------------------------------------------

def schema_admission(candidate, node_admission):
    """Admit a node's shape through a REAL validator, or an explicit assumption.

    node_admission is either a callable returning a refusal string or None, or the
    ASSUME_SCHEMA_ADMITTED sentinel by which a caller states that its inputs were
    already admitted elsewhere. Anything else refuses: this law does not guess
    member sets, integer-versus-boolean types or version constants for itself.
    """
    if node_admission is ASSUME_SCHEMA_ADMITTED:
        return None
    if not callable(node_admission):
        return QUARANTINE
    return node_admission(candidate)


# --- the one admission law --------------------------------------------------

def admit_node(candidate, nodes, node_admission):
    """The single node admission law. Publication and recovery both call it.

    Returns (refusal|None, resulting_nodes, disposition).
    """
    refusal = schema_admission(candidate, node_admission)
    if refusal is not None:
        return QUARANTINE, list(nodes), "schema-admission"
    pred, digest = candidate["predecessor"], candidate["selectedByIntentDigest"]
    if (pred is None) != (digest is None):
        return QUARANTINE, list(nodes), "unpaired-nulls"
    if pred is not None:
        if _key(pred) == _key(node_triple(candidate)):
            return QUARANTINE, list(nodes), "self-predecessor"
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
        # Revision 5: the idempotent path validates the SAME chain and uniqueness
        # rules as a write. It still writes nothing.
        refusal, why = _chain_and_uniqueness(nodes, node_triple(candidate),
                                             node_admission)
        if refusal is not None:
            return refusal, list(nodes), why
        return None, list(nodes), "idempotent"

    result = list(nodes) + [candidate]
    refusal, why = _chain_and_uniqueness(result, node_triple(candidate),
                                         node_admission)
    if refusal is not None:
        return refusal, list(nodes), why
    return None, result, "written"


def _chain_and_uniqueness(nodes, start, node_admission):
    """Component-scoped chain and key checks over the set that will stand."""
    keys = [_key(node_triple(n)) for n in nodes]
    for k in set(keys):
        same = [n for n in nodes if _key(node_triple(n)) == k]
        if any(n != same[0] for n in same[1:]):
            return QUARANTINE, "duplicate-primary-key-disagrees"
    chain, clean = ancestry(nodes, start)
    if not clean:
        return QUARANTINE, "broken-or-cyclic-ancestry"
    for member in chain:
        refusal = schema_admission(member, node_admission)
        if refusal is not None:
            return QUARANTINE, "chain-member-schema-admission"
    roots = [n for n in chain if n["predecessor"] is None]
    if len(roots) != 1:
        return QUARANTINE, "chain-does-not-reach-exactly-one-lineage-root"
    return None, None


# --- publication ------------------------------------------------------------

def publish(intent, intent_digest, nodes, current_triple, markers, node_admission):
    """Publication after the journal record is durably COMMITTED.

    Returns (case, refusal|None, resulting_nodes, node|None, rationale|None).
    """
    case = selection_case(intent)
    refusal, why = markers_refusal(markers, case, settled=True)
    if refusal is not None:
        return case, refusal, list(nodes), None, why
    if case is not FORWARD_SELECTION:
        return case, None, list(nodes), None, None
    candidate = node(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                     intent["toStateSchema"], outgoing_triple(intent, markers),
                     intent_digest)
    refusal, result, disposition = admit_node(candidate, nodes, node_admission)
    if refusal is not None:
        return case, refusal, list(nodes), None, disposition
    return case, None, result, candidate, disposition


# --- recovery ---------------------------------------------------------------

def classify_owner(owner_result):
    action = owner_result.get("action")
    after = owner_result.get("journalStateAfter")
    if action in NO_DECISION_ACTIONS:
        return "no-decision"
    if (action, after) in SETTLING:
        return "settled"
    if action in ("ABORT", "RELEASE-ONLY"):
        return "not-settled"
    return "no-decision"


def recover_nodes(owner_result, intent, intent_digest, nodes, current_triple,
                  markers, node_admission):
    """Companion recovery, applied strictly after the owner's own decision."""
    action = owner_result.get("action")
    after = owner_result.get("journalStateAfter")
    out = {"ownerAction": action, "ownerJournalStateAfter": after,
           "case": None, "nodeAction": None, "refusal": None, "nodes": list(nodes),
           "targetObservation": None}
    disposition = classify_owner(owner_result)

    if disposition == "no-decision":
        out["nodeAction"] = "no-decision"
        out["rationale"] = ("owner action " + str(action) + " makes no transition "
                            "decision; the companion inspects nothing and changes nothing")
        return out

    case = selection_case(intent)
    out["case"] = case
    settled = disposition == "settled"
    refusal, why = markers_refusal(markers, case, settled)
    out["targetObservation"] = target_observation(markers) \
        if isinstance(markers, dict) else "not-observed"
    if refusal is not None:
        out["nodeAction"] = "none"
        out["refusal"] = refusal
        out["rationale"] = why
        return out

    if not settled:
        # ABORT, or RELEASE-ONLY reaching ABORTED. Pre-existing ancestry is
        # expected and untouched. Only a NEW node for THIS attempt, at ITS OWN
        # FULL TRIPLE, is a contradiction. No numeric pair or digest is scanned.
        out["nodeAction"] = "none"
        if out["targetObservation"] == "absent":
            out["rationale"] = ("owner action " + str(action) + " before the target "
                                "store exists, or after an unpublished target was "
                                "reclaimed; no target triple can be formed, so no "
                                "premature node is possible and the abort stands")
            return out
        selected = selected_triple(intent, markers)
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
        out["rationale"] = ("owner action " + str(action) + "; the observed target "
                            "carries no node for this attempt, and a retained branch at "
                            "the same numeric generation is a different store that is "
                            "neither read as this attempt's node nor disturbed")
        return out

    if case is FORWARD_SELECTION:
        candidate = node(markers["selectedStoreRoot"], intent["toStoreGeneration"],
                         intent["toStateSchema"], outgoing_triple(intent, markers),
                         intent_digest)
        refusal, result, dispo = admit_node(candidate, nodes, node_admission)
        if refusal is not None:
            out["refusal"] = refusal
            out["rationale"] = "node admission refused: " + dispo
            return out
        out["nodes"] = result
        out["node"] = candidate
        out["nodeAction"] = ("validated" if dispo == "idempotent"
                             else "reconstructed-and-written")
        out["rationale"] = ("this transition created the node at its own full triple; "
                            "the same admission law as publication applied, including "
                            "chain and uniqueness validation on the idempotent path")
        return out

    # SAME_STORE and ANCESTOR_RESELECT: the selected node was created by an
    # EARLIER, unrelated act. This intent cannot reconstruct an origin it never
    # created, so absence is a quarantine and presence is validated, never rewritten.
    selected = selected_triple(intent, markers)
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

    refusal, why = _chain_and_uniqueness(nodes, selected, node_admission)
    if refusal is not None:
        out["refusal"] = refusal
        out["rationale"] = "the selected node fails chain or uniqueness validation: " + why
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
                        "digest; recovery validates at the full triple, checks its chain "
                        "and uniqueness, and never rewrites")
    return out


def invariants(nodes, node_admission=ASSUME_SCHEMA_ADMITTED, expected_components=None):
    """Whole-set auditor for controls. admit_node is the decision boundary.

    Roots are COMPONENT-scoped: several lineages may coexist, for example after an
    authorized restore or adoption starts its own lineage. Each node's chain must
    terminate cleanly at exactly one root. expected_components, when given, asserts
    how many distinct lineages the caller believes it supplied.
    """
    problems = []
    for n in nodes:
        refusal = schema_admission(n, node_admission)
        if refusal is not None:
            problems.append("schema admission: " + str(n.get("storeInstanceId")))
            continue
        if n["predecessor"] is not None and _key(n["predecessor"]) == _key(node_triple(n)):
            problems.append("self-predecessor: " + n["storeInstanceId"])
        if (n["predecessor"] is None) != (n["selectedByIntentDigest"] is None):
            problems.append("unpaired nulls: " + n["storeInstanceId"])
        chain, clean = ancestry(nodes, node_triple(n))
        if not clean:
            problems.append("broken or cyclic ancestry from: " + n["storeInstanceId"])
        elif len([m for m in chain if m["predecessor"] is None]) != 1:
            problems.append("chain does not reach exactly one root from: "
                            + n["storeInstanceId"])
    roots = [n for n in nodes if n["predecessor"] is None]
    if expected_components is not None and len(roots) != expected_components:
        problems.append("expected " + str(expected_components) + " lineage components, "
                        "found " + str(len(roots)))
    keys = [_key(node_triple(n)) for n in nodes]
    for k in set(keys):
        same = [n for n in nodes if _key(node_triple(n)) == k]
        if any(n != same[0] for n in same[1:]):
            problems.append("duplicate primary key with disagreeing contents")
    return problems
