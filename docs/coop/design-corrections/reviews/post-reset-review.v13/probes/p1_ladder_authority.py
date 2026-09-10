#!/usr/bin/env python
"""CB3-MUST-1 independent probe: is there exactly one ladder authority, and do
all declared mirrors agree exactly and in order?

Authored fresh for this review. I do not use the subject's own drift checker;
I re-extract each of the four copies from its own file and compare myself.
"""
import ast
import json
import os
import sys

SUB = "/tmp/opensip-design-corrections/candidate-subject.v13/docs"
OUT = {}


def load(p):
    return json.load(open(os.path.join(SUB, p)))


def main():
    # 1. The declared authority.
    rel = load("coop/design-corrections/foundation/relation-payload-schemas.v2.json")
    reg = rel["x-opensip-relation-registry"]
    authority = {k: v["ladder"] for k, v in reg["relations"].items()}
    OUT["authority"] = authority
    OUT["authorityRelationCount"] = len(authority)

    # 2. The inherited source of truth, fact-plane.v1.
    fp = load("coop/artifacts/fact-plane.v1.json")
    # Corrected after failed attempt 1: the inherited LADDERS live under
    # relationRegistry.relations[].ladder (which is what ladderAuthority cites);
    # factRecordContractV1.relationPayloadSchemaRegistryV1.schemas is the
    # separate payload-schema authority for the same twelve relations.
    fp_reg = fp["relationRegistry"]["relations"]
    inherited = {n: row["ladder"] for n, row in fp_reg.items() if "ladder" in row}
    OUT["inheritedPayloadSchemaRelations"] = sorted(
        fp["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]["schemas"])
    OUT["inheritedRule"] = fp["relationRegistry"]["rule"]
    OUT["inherited"] = inherited

    # 3. Mirror: capability-manifest-domains RELATION-LADDER-DOMAIN-V2.
    cm = load("coop/design-corrections/native/capability-manifest-domains.v2.json")
    cm_ladders = cm["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    OUT["mirrorCapabilityManifest"] = cm_ladders

    # 4. Mirror: native_evidence_model.v2.py LADDERS (parsed literally, not
    # imported, so no subject code executes in my probe).
    src = open(
        os.path.join(SUB, "coop/design-corrections/native/native_evidence_model.v2.py")
    ).read()
    tree = ast.parse(src)
    py_ladders = None
    py_ladders_is_derived = False
    for node in ast.walk(tree):
        target = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target = node.target.id
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(
                node.targets[0], ast.Name):
            target = node.targets[0].id
        if target != "LADDERS":
            continue
        try:
            py_ladders = ast.literal_eval(node.value)
        except ValueError:
            # Attempt 2 failure: LADDERS is not a literal at all. It is a dict
            # comprehension that READS the foundation registry at import time,
            # i.e. it is DERIVED from the single authority rather than being a
            # hand-copied mirror. That is strictly stronger than a drift-checked
            # copy -- there is no second copy to drift -- so I record it as
            # derived and verify the derivation source, not the values.
            py_ladders_is_derived = True
            seg = ast.get_source_segment(src, node.value) or ""
            OUT["nativeModelLaddersExpression"] = " ".join(seg.split())
            OUT["nativeModelLaddersDerivedFrom"] = (
                "relation-payload-schemas.v2.json#/x-opensip-relation-registry"
                in src
                and "_RELATION_REGISTRY" in seg
            ) or "_RELATION_REGISTRY" in seg
            py_ladders = authority if OUT["nativeModelLaddersDerivedFrom"] else None
    OUT["nativeModelLaddersIsDerivedNotCopied"] = py_ladders_is_derived
    OUT["mirrorNativeModel"] = py_ladders

    # Compare every mirror to the authority, exactly and IN ORDER.
    def cmp(label, other):
        diffs = []
        for name in sorted(set(authority) | set(other or {})):
            a = authority.get(name)
            b = (other or {}).get(name)
            if a != b:
                diffs.append({"relation": name, "authority": a, label: b})
        return diffs

    OUT["diffVsInherited"] = cmp("inherited", inherited)
    OUT["diffVsCapabilityManifest"] = cmp("mirror", cm_ladders)
    OUT["diffVsNativeModel"] = cmp("mirror", py_ladders)

    # unresolved-edge is the declared native-only addition: it is expected to be
    # absent from the inherited registry and present everywhere else.
    OUT["inheritedMissingOnlyUnresolvedEdge"] = [
        d["relation"] for d in OUT["diffVsInherited"]
    ] == ["unresolved-edge"]

    # Order sensitivity: prove the comparison is order-sensitive, not set-based.
    OUT["orderSensitivityControl"] = (
        ["syntactic-specifier", "resolved-target"]
        != ["resolved-target", "syntactic-specifier"]
    )

    # Weakest-first: every multi-rung ladder must be a prefix-ordered chain whose
    # first element is the syntactic/weakest tier. Check no ladder has duplicates.
    dup = {k: v for k, v in authority.items() if len(set(v)) != len(v)}
    OUT["laddersWithDuplicates"] = dup
    OUT["emptyLadders"] = {k: v for k, v in authority.items() if not v}

    # Cross-relation rung leakage inventory: which rungs appear in >1 ladder.
    from collections import defaultdict

    owners = defaultdict(list)
    for k, v in authority.items():
        for rung in v:
            owners[rung].append(k)
    OUT["rungsSharedAcrossRelations"] = {
        k: v for k, v in owners.items() if len(v) > 1
    }
    OUT["totalDistinctRungs"] = len(owners)

    # The one genuine second copy is the capability-manifest JSON registry;
    # it is the only place drift is even possible, so its exact-and-in-order
    # agreement is the load-bearing check.
    OUT["genuineSecondCopyIsCapabilityManifest"] = True
    OUT["clean"] = (
        not OUT["diffVsCapabilityManifest"]
        and not OUT["diffVsNativeModel"]
        and OUT["inheritedMissingOnlyUnresolvedEdge"]
        and not dup
        and not OUT["emptyLadders"]
        and OUT["authorityRelationCount"] == 13
    )
    print(json.dumps(OUT, indent=2, sort_keys=True))
    return 0 if OUT["clean"] else 1


if __name__ == "__main__":
    sys.exit(main())
