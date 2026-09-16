#!/usr/bin/env python3
"""Structural and join control for the PS-01 correction.

Checks the authored store-instance lineage companion against the frozen S9 owner
and the working planning inputs, and executes the rollback digest-continuity
property the correction claims. This validates design bookkeeping and one
modelled property; it is not product code, a carrier test or qualification.

Usage: check_store_instance_lineage.py <work-tree> <candidate25-root>
"""
import hashlib
import json
import sys
from pathlib import Path

OWNER = "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json"
FAILURES = []


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def load(path):
    return json.loads(Path(path).read_text())


def canonical_bytes(obj):
    """Stand-in for the one foundation product-profile canonicalizer.

    The real canonicalizer is owned by identity section 3. This model only needs
    determinism and no normalization to exercise the digest-continuity property.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def store_generation_digest(namespace_id, instance_id, generation, state_schema):
    return hashlib.sha256(canonical_bytes({
        "schemaVersion": 1,
        "namespaceId": namespace_id,
        "storeInstanceId": instance_id,
        "storeGeneration": generation,
        "stateSchema": state_schema,
    })).hexdigest()


def check_closed_schema(schema, label):
    check(schema.get("additionalProperties") is False,
          label + ": not closed")
    check(set(schema.get("required", [])) == set(schema.get("properties", {})),
          label + ": required does not equal properties")
    check(len(schema.get("required", [])) == len(set(schema.get("required", []))),
          label + ": duplicate required member")


def structural_checks(companion, owner, inventory, recovery):
    lineage = companion["privateCompanionSchema"]["schema"]
    check_closed_schema(lineage, "StoreInstanceLineageV1")

    defs = owner["$defs"]
    props = lineage["properties"]

    expected_members = {
        "schemaVersion", "intentDigest", "operation",
        "fromStoreInstanceId", "toStoreInstanceId",
        "fromStoreGeneration", "toStoreGeneration",
        "fromStateSchema", "toStateSchema",
        "instanceDisposition", "predecessorIntentDigest",
    }
    if not check(set(props) == expected_members,
                 "StoreInstanceLineageV1 member set changed: missing "
                 + str(sorted(expected_members - set(props)))
                 + ", extra " + str(sorted(set(props) - expected_members))):
        return

    # Owner enums are held equal, never widened.
    check(props["operation"]["enum"] == defs["TransitionOperation"]["enum"],
          "operation enum drifted from owner TransitionOperation")
    for member in ("fromStateSchema", "toStateSchema"):
        check(props[member]["enum"] == defs["StateSchema"]["enum"],
              member + " enum drifted from owner StateSchema")
        check(props[member].get("type") == "integer",
              member + " must narrow to integer, never widen")
    for member in ("fromStoreGeneration", "toStoreGeneration"):
        actual = {k: v for k, v in props[member].items() if k != "description"}
        check(actual == defs["I64NonNegative"],
              member + " drifted from owner I64NonNegative")
    for member in ("intentDigest",):
        check(props[member]["pattern"] == defs["Hex64"]["pattern"],
              member + " pattern drifted from owner Hex64")

    # The successor adds nothing to the closed public records it names.
    owner_text = json.dumps(owner)
    check("storeInstance" not in owner_text,
          "owner bundle unexpectedly already carries a store instance member")
    for name in companion["ownerSuccessorDelta"]["closedPublicRecordsUnchanged"]:
        if name in owner.get("schemas", {}) or name in defs:
            record = owner["schemas"].get(name) or defs.get(name)
            if isinstance(record, dict) and "properties" in record:
                check("storeInstanceId" not in record["properties"],
                      name + " must not gain a storeInstanceId member")
    for name in ("InstallationTransitionIntentV1", "InstallationTransitionJournalV1"):
        record = owner["schemas"][name]
        check(record["additionalProperties"] is False, name + " must stay closed")
        check("storeInstanceId" not in record["properties"],
              name + " must not gain a storeInstanceId member")
    check(defs["NamespaceList"]["items"]["type"] == "string",
          "NamespaceList must remain an array of strings")

    # intentDigest is the join key and must exist on the public journal already.
    journal = owner["schemas"]["InstallationTransitionJournalV1"]
    check("intentDigest" in journal["properties"],
          "join key intentDigest absent from the public journal")

    # The binding is referenced, not duplicated, and is unchanged.
    binding = recovery["storeGenerationBindingSchema"]
    check(set(binding["required"]) == {"schemaVersion", "namespaceId",
                                       "storeInstanceId", "storeGeneration",
                                       "stateSchema"},
          "StoreGenerationBindingV1 members changed by this correction")
    check("StoreGenerationBindingV1" not in companion.get("privateSchemas", {}),
          "binding must be referenced, not duplicated, to prevent drift")
    check("commit-recovery-plan.v1.json" in companion["canonicalDigestRecipe"]["subject"],
          "digest recipe must name the binding's owning file")

    # Every named owning module exists in the planning inventory.
    paths = {row["path"] for row in inventory["files"]}
    for role, module in companion["privateCompanionSchema"]["owningModules"].items():
        for candidate in module.replace(" with ", " ").replace(" behind ", " ").split():
            if candidate.startswith(("crates/", "apps/", "providers/")):
                check(candidate in paths,
                      "owning module not in inventory (" + role + "): " + candidate)

    # Operation rules are total over the owner's five operations.
    covered = " ".join(rule["operation"] for rule in companion["operationRules"])
    for operation in defs["TransitionOperation"]["enum"]:
        check(operation in covered, "operation rule missing for " + operation)

    # No D9 code is minted.
    check(companion["ownerSuccessorDelta"]["d9Impact"].startswith("None"),
          "successor must mint no D9 code")


def rollback_continuity_property():
    """Execute the claimed join behaviour over the S9.2 operation sequence."""
    namespace = "acme.reports"
    old_instance = "a3f10c9d5b27e4084c6d1f9b02e7a851"
    new_instance = "77c4e0b119ad3f625e8802fd4a6c31be"

    before = store_generation_digest(namespace, old_instance, 5, 1)

    # store-migrate: advances the schema and selects a new store generation, so
    # the S9 footprint materializes a new physical store instance.
    migrated = store_generation_digest(namespace, new_instance, 6, 2)
    check(migrated != before, "migration must change the binding digest")

    # store-rollback: re-selects the retained old store, which keeps its original
    # instance identity, so the tuple and therefore the digest are restored.
    rolled_back = store_generation_digest(namespace, old_instance, 5, 1)
    check(rolled_back == before,
          "rollback to the same retained physical store must restore the digest")

    # A restored/new physical store never reproduces the old digest, even at the
    # same numeric generation and state schema.
    restored_instance = "0e5b8c2143a7f96d8b31c0da47e25f6c"
    restored = store_generation_digest(namespace, restored_instance, 5, 1)
    check(restored != before,
          "a new physical store instance must not reproduce a predecessor digest")

    # A different namespace never collides at the same installation-scoped tuple.
    other = store_generation_digest("acme.other", old_instance, 5, 1)
    check(other != before, "namespace must participate in the digest")

    return {
        "beforeMigration": before,
        "afterMigration": migrated,
        "afterRollback": rolled_back,
        "afterRestoreNewInstance": restored,
        "otherNamespace": other,
        "rollbackRestoresDigest": rolled_back == before,
        "restoreDoesNotImpersonate": restored != before,
    }


MUTATIONS = {
    "widen-operation-enum":
        lambda c, o: c["privateCompanionSchema"]["schema"]["properties"]
        ["operation"]["enum"].append("store-adopt"),
    "widen-state-schema":
        lambda c, o: c["privateCompanionSchema"]["schema"]["properties"]
        ["fromStateSchema"].__setitem__("enum", [1, 2, 3]),
    "open-the-record":
        lambda c, o: c["privateCompanionSchema"]["schema"]
        .__setitem__("additionalProperties", True),
    "unbound-generation":
        lambda c, o: c["privateCompanionSchema"]["schema"]["properties"]
        ["toStoreGeneration"].__setitem__("maximum", 18446744073709551615),
    "drop-join-key":
        lambda c, o: (c["privateCompanionSchema"]["schema"]["required"]
                      .remove("intentDigest"),
                      c["privateCompanionSchema"]["schema"]["properties"]
                      .pop("intentDigest")),
    "duplicate-the-binding":
        lambda c, o: c.setdefault("privateSchemas", {})
        .__setitem__("StoreGenerationBindingV1", {}),
    "unknown-owning-module":
        lambda c, o: c["privateCompanionSchema"]["owningModules"]
        .__setitem__("stateMachine", "crates/lifecycle/src/store_lineage.rs"),
    "drop-an-operation-rule":
        lambda c, o: c["operationRules"].pop(0),
    "mint-a-d9-code":
        lambda c, o: c["ownerSuccessorDelta"]
        .__setitem__("d9Impact", "Adds LIFECYCLE.STORE_INSTANCE_MISMATCH."),
    "widen-the-public-intent":
        lambda c, o: o["schemas"]["InstallationTransitionIntentV1"]["properties"]
        .__setitem__("storeInstanceId", {"type": "string"}),
    "namespace-list-to-objects":
        lambda c, o: o["$defs"]["NamespaceList"]["items"]
        .__setitem__("type", "object"),
}


def negative_controls(arch, c25):
    fired = {}
    for name, mutate in MUTATIONS.items():
        global FAILURES
        FAILURES = []
        companion = load(arch / "store-instance-lineage.v1.json")
        owner = load(c25 / OWNER)
        inventory = load(arch / "repository-file-inventory.v1.json")
        recovery = load(arch / "commit-recovery-plan.v1.json")
        try:
            mutate(companion, owner)
            structural_checks(companion, owner, inventory, recovery)
            fired[name] = FAILURES or None
        except Exception as exc:                      # a mutation may break a lookup
            fired[name] = ["raised " + type(exc).__name__ + ": " + str(exc)[:80]]
    undetected = [name for name, result in fired.items() if not result]
    return fired, undetected


def main():
    work = Path(sys.argv[1])
    c25 = Path(sys.argv[2])
    arch = work / "docs/v2/architecture"
    companion = load(arch / "store-instance-lineage.v1.json")
    owner = load(c25 / OWNER)
    inventory = load(arch / "repository-file-inventory.v1.json")
    recovery = load(arch / "commit-recovery-plan.v1.json")

    structural_checks(companion, owner, inventory, recovery)
    baseline = list(FAILURES)
    property_result = rollback_continuity_property()
    baseline_with_property = list(FAILURES)

    fired, undetected = negative_controls(arch, c25)

    result = {
        "control": "check_store_instance_lineage",
        "structuralFailures": baseline_with_property,
        "digestContinuityProperty": property_result,
        "negativeControls": {
            "count": len(MUTATIONS),
            "detected": len(MUTATIONS) - len(undetected),
            "undetected": undetected,
            "firstFailureByMutation": {k: (v[0] if v else None)
                                       for k, v in fired.items()},
        },
        "status": "PASS" if not baseline_with_property and not undetected else "FAIL",
        "limits": "Models the digest-continuity property with a stand-in canonicalizer. "
                  "Proves no product behaviour, no carrier behaviour and no qualification.",
    }
    print(json.dumps(result, indent=1))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
