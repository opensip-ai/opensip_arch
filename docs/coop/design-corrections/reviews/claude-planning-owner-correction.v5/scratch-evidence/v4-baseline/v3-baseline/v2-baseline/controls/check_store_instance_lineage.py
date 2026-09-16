#!/usr/bin/env python3
"""Structural and join control for the PS-01 correction, revision 2.

Checks the authored store-instance lineage companion and the S9.3 owner patch
against the frozen S9 owner, and executes four properties using the ACTUAL
frozen foundation canonicalizer: digest continuity, node-writing derivation,
the lawful-retry trace, and recovery totality over the owner's six journal
states. This validates design bookkeeping and modelled properties; it is not
product code, a carrier test or qualification.

Usage: check_store_instance_lineage.py <work-tree> <candidate25-root>
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

OWNER_SCHEMAS = "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json"
OWNER_PROSE = "docs/v2/contracts/product-v1/security-and-lifecycle.md"
CANONICAL = "docs/coop/design-corrections/foundation/canonical.py"
FAILURES = []


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def load(path):
    return json.loads(Path(path).read_text())


def load_frozen_canonicalizer(c25):
    """Import the exact frozen foundation canonicalizer, read-only."""
    path = c25 / CANONICAL
    spec = importlib.util.spec_from_file_location("frozen_canonical", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, hashlib.sha256(path.read_bytes()).hexdigest()


def check_closed_schema(schema, label):
    check(schema.get("additionalProperties") is False, label + ": not closed")
    check(set(schema.get("required", [])) == set(schema.get("properties", {})),
          label + ": required does not equal properties")


# --- structural -------------------------------------------------------------

NODE_MEMBERS = {"schemaVersion", "storeInstanceId", "storeGeneration",
                "stateSchema", "predecessor", "selectedByIntentDigest"}


def structural_checks(companion, owner, inventory, recovery, patch_text):
    node = companion["privateCompanionSchema"]["schema"]
    check_closed_schema(node, "StoreLineageNodeV1")
    props = node["properties"]
    if not check(set(props) == NODE_MEMBERS,
                 "node member set changed: missing "
                 + str(sorted(NODE_MEMBERS - set(props)))
                 + ", extra " + str(sorted(set(props) - NODE_MEMBERS))):
        return

    defs = owner["$defs"]
    actual = {k: v for k, v in props["storeGeneration"].items() if k != "description"}
    check(actual == defs["I64NonNegative"],
          "storeGeneration drifted from owner I64NonNegative")
    check(props["stateSchema"]["enum"] == defs["StateSchema"]["enum"],
          "stateSchema enum drifted from owner StateSchema")
    check(props["stateSchema"].get("type") == "integer",
          "stateSchema must narrow to integer, never widen")

    # The successor adds nothing to the closed public records.
    check("storeInstance" not in json.dumps(owner),
          "owner bundle unexpectedly already carries a store instance member")
    for name in ("InstallationTransitionIntentV1", "InstallationTransitionJournalV1"):
        record = owner["schemas"][name]
        check(record["additionalProperties"] is False, name + " must stay closed")
        check("storeInstanceId" not in record["properties"],
              name + " must not gain a storeInstanceId member")
    check(defs["NamespaceList"]["items"]["type"] == "string",
          "NamespaceList must remain an array of strings")

    # intentDigest is evidence, never the key.
    key = companion["privateCompanionSchema"]["keyModel"]["primaryKey"]
    check(key == ["storeInstanceId", "storeGeneration", "stateSchema"],
          "primary key must be the binding triple")
    check("selectedByIntentDigest" not in key,
          "intentDigest must not be part of the primary key")

    # Binding referenced, not duplicated, and unchanged.
    binding = recovery["storeGenerationBindingSchema"]
    check(set(binding["required"]) == {"schemaVersion", "namespaceId",
                                       "storeInstanceId", "storeGeneration",
                                       "stateSchema"},
          "StoreGenerationBindingV1 members changed by this correction")

    # Owning modules exist in the planning inventory.
    paths = {row["path"] for row in inventory["files"]}
    for role, module in companion["privateCompanionSchema"]["owningModules"].items():
        for token in module.replace(" with ", " ").replace(" behind ", " ").split():
            if token.startswith(("crates/", "apps/", "providers/")):
                check(token in paths,
                      "owning module not in inventory (" + role + "): " + token)

    # Recovery is total over the owner's six journal states.
    owner_states = set(owner["schemas"]["InstallationTransitionJournalV1"]
                       ["properties"]["state"]["enum"])
    covered = {row["journalState"] for row in companion["recoveryTotality"]}
    check(covered == owner_states,
          "recovery not total: missing " + str(sorted(owner_states - covered))
          + ", extra " + str(sorted(covered - owner_states)))

    # PREPARED for a core operation must keep the owner's ABORT, not quarantine.
    prepared = [r for r in companion["recoveryTotality"]
                if r["journalState"] == "PREPARED"][0]
    check("ABORT" in prepared["ownerDecision"].upper(),
          "PREPARED row must record the owner's core-operation ABORT")
    check(prepared["companionAction"].lower().startswith("none"),
          "the companion must take no action at PREPARED")
    check("never replace" in prepared["companionAction"].lower(),
          "the PREPARED row must say a missing node never replaces the owner ABORT")
    check(prepared["expectedNode"] == "absent",
          "a node must not be expected at PREPARED")
    for state in ("LEASED", "PREPARING", "ABORTED"):
        row = [r for r in companion["recoveryTotality"]
               if r["journalState"] == state][0]
        check(row["expectedNode"] == "absent",
              "a node must not be expected at " + state)
        check(row["companionAction"].lower().startswith("none"),
              "the companion must take no action at " + state)

    # No atomicity claim; a one-sided footprint must reconcile.
    dur = companion["durabilityAndReconciliation"]
    check("NOT claim" in dur["noAtomicityClaimed"] or "does NOT" in dur["noAtomicityClaimed"],
          "the companion must not claim cross-file atomicity")
    check("reconstruct" in json.dumps(companion["recoveryTotality"]).lower(),
          "the one-sided footprint must reconcile by reconstruction")

    # No D9 code minted.
    check(companion["ownerSuccessorDelta"]["d9Impact"].startswith("None"),
          "successor must mint no D9 code")

    # The digest recipe must not repeat the withdrawn reordering claim.
    recipe = companion["canonicalDigestRecipe"]
    joined = json.dumps(recipe["whatChangesTheDigest"]).lower()
    check("reorder" not in joined and "order of object members" not in joined,
          "reordering must not be listed as changing the digest")
    check(any("order" in item.lower() for item in recipe["whatDoesNotChangeTheDigest"]),
          "the recipe must state that input key order does not change the digest")
    check("sort_keys=True" in recipe["canonicalizer"],
          "the recipe must name the frozen canonicalizer's sort_keys behaviour")

    # Floors: the migration carry-forward must not be invalidated by the restore rule.
    floors = companion["floorsAndAuthority"]
    check("COPIES THE FLOORS FORWARD" in floors["authorizedTransition"]["floors"].upper()
          or "copy" in floors["authorizedTransition"]["floors"].lower(),
          "the authorized migration floor carry-forward must be preserved")
    check("MAXIMUM" in floors["authorizedTransition"]["floors"].upper(),
          "the rollback maximum-of-both-stores rule must be preserved")
    check("does not touch" in floors["evidenceRestoreOrPortableAdoption"]["doesNotInvalidate"]
          or "not touch" in floors["evidenceRestoreOrPortableAdoption"]["doesNotInvalidate"],
          "the restore rule must state it does not override the migration rule")

    # The owner patch must be a pure insertion naming S9.3.
    lines = patch_text.splitlines()
    hunks = [l for l in lines if l.startswith("@@")]
    check(len(hunks) == 1, "the owner patch must be a single hunk, got " + str(len(hunks)))
    removed = [l for l in lines if l.startswith("-") and not l.startswith("---")]
    check(not removed, "the owner patch must remove no line")
    added = [l for l in lines if l.startswith("+") and not l.startswith("+++")]
    check(added, "the owner patch must add lines")
    check(any(l.startswith("+### S9.3") for l in added),
          "the owner patch must insert S9.3")
    for banned in ("storeInstanceId\": ", "InstallationTransitionIntentV1` gains"):
        check(banned not in patch_text, "the owner patch must not widen a closed record")


# --- executed properties ----------------------------------------------------

def store_generation_digest(C, namespace_id, instance_id, generation, state_schema):
    """Raw SHA-256 over the FROZEN canonicalizer's bytes. Not identity(domain, v)."""
    return hashlib.sha256(C.canonical({
        "schemaVersion": 1,
        "namespaceId": namespace_id,
        "storeInstanceId": instance_id,
        "storeGeneration": generation,
        "stateSchema": state_schema,
    })).hexdigest()


def digest_properties(C):
    ns, old, new = "acme.reports", "a3f10c9d5b27e4084c6d1f9b02e7a851", \
        "77c4e0b119ad3f625e8802fd4a6c31be"
    before = store_generation_digest(C, ns, old, 5, 1)
    migrated = store_generation_digest(C, ns, new, 6, 2)
    rolled_back = store_generation_digest(C, ns, old, 5, 1)
    restored = store_generation_digest(C, ns, "0e5b8c2143a7f96d8b31c0da47e25f6c", 5, 1)
    other_ns = store_generation_digest(C, "acme.other", old, 5, 1)

    check(migrated != before, "migration must change the digest")
    check(rolled_back == before, "rollback to the retained store must restore the digest")
    check(restored != before, "a new instance must not reproduce a predecessor digest")
    check(other_ns != before, "namespace must participate in the digest")

    # Issue 3: input member order must NOT change the digest, because canonical()
    # sorts keys. The v1 prose claimed otherwise.
    ordered_a = {"schemaVersion": 1, "namespaceId": ns, "storeInstanceId": old,
                 "storeGeneration": 5, "stateSchema": 1}
    ordered_b = {"stateSchema": 1, "storeGeneration": 5, "storeInstanceId": old,
                 "namespaceId": ns, "schemaVersion": 1}
    reorder_same = (hashlib.sha256(C.canonical(ordered_a)).hexdigest()
                    == hashlib.sha256(C.canonical(ordered_b)).hexdigest())
    check(reorder_same, "input key order must not change the digest")

    # Adding or removing a member DOES change it.
    added = dict(ordered_a); added["carrierFormat"] = 3
    add_changes = hashlib.sha256(C.canonical(added)).hexdigest() != before
    removed = {k: v for k, v in ordered_a.items() if k != "stateSchema"}
    remove_changes = hashlib.sha256(C.canonical(removed)).hexdigest() != before
    renamed = {("storeGen" if k == "storeGeneration" else k): v
               for k, v in ordered_a.items()}
    rename_changes = hashlib.sha256(C.canonical(renamed)).hexdigest() != before
    check(add_changes and remove_changes and rename_changes,
          "adding, removing or renaming a member must change the digest")

    # It is not the framed H(domain, descriptor).
    framed = C.identity("opensip.design.store-generation-binding", ordered_a)
    check(framed != before, "the raw digest must differ from the framed identity")

    # The canonicalizer refuses what the record forbids.
    refusals = {}
    for name, raw in (("duplicate-key", b'{"a":1,"a":2}'),
                      ("float", b'{"a":1.5}'),
                      ("negative-zero", b'{"a":-0}'),
                      ("over-range-integer", b'{"a":18446744073709551616}')):
        try:
            C.parse(raw)
            refusals[name] = None
        except Exception as exc:
            refusals[name] = type(exc).__name__
        check(refusals[name] is not None, "canonicalizer admitted " + name)

    return {"beforeMigration": before, "afterMigration": migrated,
            "afterRollback": rolled_back, "afterRestoreNewInstance": restored,
            "otherNamespace": other_ns,
            "rollbackRestoresDigest": rolled_back == before,
            "inputKeyOrderIrrelevant": reorder_same,
            "addRemoveRenameChangesDigest": add_changes and remove_changes and rename_changes,
            "rawDigestIsNotFramedIdentity": framed != before,
            "framedIdentitySample": framed,
            "parseRefusals": refusals}


def node_writing(current, ancestors, to_generation, to_state_schema):
    """Derived from the intent's own values, never the operation name (issue 6)."""
    if (to_generation, to_state_schema) == (current["storeGeneration"], current["stateSchema"]):
        return "unchanged"
    for node in ancestors:
        if (node["storeGeneration"], node["stateSchema"]) == (to_generation, to_state_schema):
            return "ancestor-reselect"
    return "forward-selection"


def node_writing_property():
    current = {"storeInstanceId": "a" * 32, "storeGeneration": 5, "stateSchema": 1}
    ancestors = [{"storeInstanceId": "b" * 32, "storeGeneration": 4, "stateSchema": 1}]
    cases = [
        ("core-repair, schema and generation unchanged", 5, 1, "unchanged", False),
        ("core-update, schema unchanged", 5, 1, "unchanged", False),
        ("core-rollback, schema unchanged (owner publishes no store rule)",
         5, 1, "unchanged", False),
        ("core-rollback, schema retreats to an ancestor", 4, 1, "ancestor-reselect", False),
        ("store-rollback, retained generation re-selected", 4, 1, "ancestor-reselect", False),
        ("store-migrate, schema advances to a new generation", 6, 2, "forward-selection", True),
        ("core-update, schema raised to a new generation", 6, 2, "forward-selection", True),
    ]
    rows = []
    for name, gen, schema, expected, writes in cases:
        actual = node_writing(current, ancestors, gen, schema)
        ok = actual == expected
        rows.append({"case": name, "to": [gen, schema], "expected": expected,
                     "actual": actual, "writesNode": writes, "ok": ok})
        check(ok, "node-writing case " + name + ": expected " + expected
              + ", got " + actual)
    check(not any(r["writesNode"] for r in rows if r["actual"] != "forward-selection"),
          "only a forward selection may write a node")
    check(all(r["actual"] != "forward-selection" or r["writesNode"] for r in rows),
          "every forward selection must write a node")
    return rows


def retry_trace_property():
    """Issue 7: a lawful retry of a byte-identical intent must not contradict."""
    nodes = {("x" * 32, 5, 1): {"predecessor": None, "intentDigest": None}}
    intent = {"fromStoreGeneration": 5, "fromStateSchema": 1,
              "toStoreGeneration": 6, "toStateSchema": 2}
    intent_digest = hashlib.sha256(
        json.dumps(intent, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    trace = []

    def admit(current_gen, current_schema):
        if intent["fromStoreGeneration"] != current_gen:
            return "TRANSITION.CURRENT_STORE_MISMATCH"
        if intent["fromStateSchema"] != current_schema:
            return "TRANSITION.CURRENT_SCHEMA_MISMATCH"
        return None

    current = ("x" * 32, 5, 1)
    trace.append({"step": "attempt-1 admission", "refusal": admit(current[1], current[2])})
    check(trace[-1]["refusal"] is None, "first attempt must be admitted")
    trace.append({"step": "attempt-1 materializes instance Y at (6,2), reaches PREPARED, crashes"})
    trace.append({"step": "recovery at PREPARED decides ABORT; no node written",
                  "nodesAfter": len(nodes)})
    check(len(nodes) == 1, "an aborted attempt must write no node")

    trace.append({"step": "attempt-2 admission with a byte-identical intent",
                  "intentDigestRepeats": True,
                  "refusal": admit(current[1], current[2])})
    check(trace[-1]["refusal"] is None, "a lawful retry must be admitted")
    new_key = ("z" * 32, 6, 2)
    collision = new_key in nodes
    nodes[new_key] = {"predecessor": current, "intentDigest": intent_digest}
    current = new_key
    trace.append({"step": "attempt-2 commits; one node written", "key": list(new_key),
                  "primaryKeyCollision": collision})
    check(not collision, "a lawful retry must not collide on the primary key")

    after = admit(current[1], current[2])
    trace.append({"step": "attempt-3 replays the same intent after the commit",
                  "refusal": after})
    check(after == "TRANSITION.CURRENT_STORE_MISMATCH",
          "a replay after commit must be refused by the owner's own check")

    repeated = [d for d in (n["intentDigest"] for n in nodes.values()) if d]
    return {"intentDigest": intent_digest, "trace": trace,
            "nodeCount": len(nodes), "intentDigestAppearsAsKey": False,
            "intentDigestOccurrencesAsEvidence": len(repeated)}


def reconstruction_property():
    """Issue 7: a one-sided footprint reconciles because the node is derivable."""
    journal = {"state": "COMMITTED", "fromStoreGeneration": 5, "fromStateSchema": 1,
               "toStoreGeneration": 6, "toStateSchema": 2,
               "intentDigest": "c" * 64}
    markers = {"predecessorStoreRoot": "x" * 32, "selectedStoreRoot": "z" * 32}

    def reconstruct(j, m):
        if j["state"] not in ("COMMITTED", "DONE"):
            return None
        if not m.get("selectedStoreRoot") or not m.get("predecessorStoreRoot"):
            return "QUARANTINE/MIGRATION.CORRUPT"
        return {"schemaVersion": 1, "storeInstanceId": m["selectedStoreRoot"],
                "storeGeneration": j["toStoreGeneration"],
                "stateSchema": j["toStateSchema"],
                "predecessor": {"storeInstanceId": m["predecessorStoreRoot"],
                                "storeGeneration": j["fromStoreGeneration"],
                                "stateSchema": j["fromStateSchema"]},
                "selectedByIntentDigest": j["intentDigest"]}

    rebuilt = reconstruct(journal, markers)
    check(isinstance(rebuilt, dict), "a COMMITTED journal must reconstruct its node")
    unreadable = reconstruct(journal, {"predecessorStoreRoot": "x" * 32})
    check(unreadable == "QUARANTINE/MIGRATION.CORRUPT",
          "an unreadable marker must quarantine")
    aborted = reconstruct({**journal, "state": "ABORTED"}, markers)
    check(aborted is None, "an ABORTED journal must reconstruct nothing")
    return {"reconstructedFromCommitted": rebuilt is not None,
            "unreadableMarkerQuarantines": unreadable == "QUARANTINE/MIGRATION.CORRUPT",
            "abortedReconstructsNothing": aborted is None,
            "sample": rebuilt}


def main():
    work = Path(sys.argv[1])
    c25 = Path(sys.argv[2])
    arch = work / "docs/v2/architecture"
    companion = load(arch / "store-instance-lineage.v1.json")
    owner = load(c25 / OWNER_SCHEMAS)
    inventory = load(arch / "repository-file-inventory.v1.json")
    recovery = load(arch / "commit-recovery-plan.v1.json")
    patch = (work.parent / "patches" / "security-and-lifecycle.md.S9.3.patch").read_text()
    C, canonical_sha = load_frozen_canonicalizer(c25)

    structural_checks(companion, owner, inventory, recovery, patch)
    result = {
        "control": "check_store_instance_lineage",
        "frozenCanonicalizer": {"path": CANONICAL, "sha256": canonical_sha,
                                "usedInsteadOfStandIn": True},
        "structuralFailures": list(FAILURES),
        "digestProperties": digest_properties(C),
        "nodeWritingDerivation": node_writing_property(),
        "retryTrace": retry_trace_property(),
        "oneSidedFootprintReconstruction": reconstruction_property(),
    }
    result["structuralFailures"] = list(FAILURES)
    result["status"] = "PASS" if not FAILURES else "FAIL"
    result["limits"] = ("Executes the digest property with the exact frozen canonicalizer "
                        "and models the node, retry and reconciliation rules. Proves no "
                        "product behaviour, no carrier behaviour and no qualification.")
    print(json.dumps(result, indent=1))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
