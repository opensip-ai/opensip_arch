#!/usr/bin/env python3
"""Structural control for the PS-01 correction, revision 3.

Checks the authored companion and the owner patch against the frozen S9 owner,
and executes the digest properties with the ACTUAL frozen foundation
canonicalizer. The operation/state behaviour is executed separately by
check_lineage_recovery.py against the frozen owner model.

Usage: check_store_instance_lineage.py <work-tree> <candidate25-root>
"""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

OWNER_SCHEMAS = "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json"
CANONICAL = "docs/coop/design-corrections/foundation/canonical.py"
PATCH = "security-and-lifecycle.md.S9-pair-law-and-S9.3.patch"
FAILURES = []

NODE_MEMBERS = {"schemaVersion", "storeInstanceId", "storeGeneration",
                "stateSchema", "predecessor", "selectedByIntentDigest"}


def check(condition, message):
    if not condition:
        FAILURES.append(message)
    return bool(condition)


def load(path):
    return json.loads(Path(path).read_text())


def load_frozen_canonicalizer(c25):
    path = c25 / CANONICAL
    spec = importlib.util.spec_from_file_location("frozen_canonical", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, hashlib.sha256(path.read_bytes()).hexdigest()


def structural_checks(companion, owner, inventory, recovery, patch_text):
    node = companion["privateCompanionSchema"]["schema"]
    check(node.get("additionalProperties") is False, "node schema not closed")
    check(set(node.get("required", [])) == set(node.get("properties", {})),
          "node required does not equal properties")
    props = node["properties"]
    if not check(set(props) == NODE_MEMBERS,
                 "node member set changed: " + str(sorted(set(props) ^ NODE_MEMBERS))):
        return

    defs = owner["$defs"]
    actual = {k: v for k, v in props["storeGeneration"].items() if k != "description"}
    check(actual == defs["I64NonNegative"],
          "storeGeneration drifted from owner I64NonNegative")
    check(props["stateSchema"]["enum"] == defs["StateSchema"]["enum"],
          "stateSchema enum drifted from owner StateSchema")

    check("storeInstance" not in json.dumps(owner),
          "owner bundle unexpectedly already carries a store instance member")
    for name in ("InstallationTransitionIntentV1", "InstallationTransitionJournalV1"):
        record = owner["schemas"][name]
        check(record["additionalProperties"] is False, name + " must stay closed")
        check("storeInstanceId" not in record["properties"],
              name + " must not gain a storeInstanceId member")
    check(defs["NamespaceList"]["items"]["type"] == "string",
          "NamespaceList must remain an array of strings")

    key = companion["privateCompanionSchema"]["keyModel"]["primaryKey"]
    check(key == ["storeInstanceId", "storeGeneration", "stateSchema"],
          "primary key must be the binding triple")
    check("selectedByIntentDigest" not in key,
          "intentDigest must not be part of the primary key")

    binding = recovery["storeGenerationBindingSchema"]
    check(set(binding["required"]) == {"schemaVersion", "namespaceId",
                                       "storeInstanceId", "storeGeneration",
                                       "stateSchema"},
          "StoreGenerationBindingV1 members changed by this correction")

    paths = {row["path"] for row in inventory["files"]}
    for role, module in companion["privateCompanionSchema"]["owningModules"].items():
        for token in module.replace(" with ", " ").replace(" behind ", " ").split():
            if token.startswith(("crates/", "apps/", "providers/")):
                check(token in paths,
                      "owning module not in inventory (" + role + "): " + token)

    # --- the v2 defects must be gone -----------------------------------------
    # The claim may only survive inside an explicit withdrawal or revision note.
    def asserted_anywhere(obj, path=""):
        hits = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("withdrawn", "v2ToV3Changes", "v1ToV2Changes", "rootCause",
                         "what", "fix", "note"):
                    continue
                hits += asserted_anywhere(v, path + "/" + k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                hits += asserted_anywhere(v, path + "/" + str(i))
        elif isinstance(obj, str):
            for phrase in ("publishes no store-generation rule for core-rollback",
                           "does not publish a store rule",
                           "S9.2 does not publish"):
                if phrase in obj:
                    hits.append(path)
        return hits

    stale = asserted_anywhere(companion)
    check(not stale,
          "the withdrawn core-rollback overstatement is still asserted at " + str(stale))
    check(any(a["id"] == "A4b" for a in companion["frozenSourceAnchors"]),
          "the owner pair-law anchor A4b must be cited")
    a4b = [a for a in companion["frozenSourceAnchors"] if a["id"] == "A4b"][0]
    for refusal in ("TRANSITION.SAME_SCHEMA_KEEPS_STORE",
                    "TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE"):
        check(refusal in a4b["fact"], "A4b must name " + refusal)

    rc = companion.get("rootCounterexamples")
    check(rc is not None and rc.get("accepted") is True,
          "root's counterexamples must be recorded as accepted")
    ids = [f["id"] for f in rc.get("findings", [])]
    check(set(ids) >= {"RC-1", "RC-2", "RC-3", "RC-4", "RC-5"},
          "all five root findings must be recorded, got " + str(ids))

    # --- revision 4: full-triple identity and one admission law --------------
    ident = companion.get("identityAndMarkers")
    check(ident is not None, "the identity and marker contract must be stated")
    if ident:
        check("FULL TRIPLE" in ident["principle"],
              "identity must be the full triple")
        mc = ident["markerContract"]
        for name in ("selectedStoreRoot", "predecessorStoreRoot",
                     "validatedBeforeDereference", "caseConsistency"):
            check(name in mc, "marker contract missing " + name)
        check("before any dereference" in mc["validatedBeforeDereference"],
              "markers must be validated before dereference")
        check("never a search key" in ident["intentDigestIsNotAKey"],
              "intentDigest must be excluded as a search key")
        check("No global uniqueness" in ident["noInventedUniqueness"],
              "no global generation uniqueness may be invented")

    law = companion.get("admissionLaw")
    check(law is not None, "the single admission law must be stated")
    if law:
        check("admit_node" in law["oneLawBothPaths"],
              "publication and recovery must name one admission law")
        checks = json.dumps(law["checks"]).lower()
        for needed, label in (("already exist", "predecessor presence"),
                              ("acyclic", "acyclicity"),
                              ("disagree", "duplicate primary key"),
                              ("one lineage root", "single root")):
            check(needed in checks, "admission law missing " + label)
        check("nothing is written" in law["onRefusal"].lower(),
              "a refusal must write nothing")

    rt = companion["recoveryTotality"]
    check("markersFirst" in companion["durabilityAndReconciliation"],
          "markers must be validated before any dereference")
    check("noDecisionActions" in rt,
          "the no-decision action class must be stated")
    if "noDecisionActions" in rt:
        nd = rt["noDecisionActions"]
        check("inspects no node" in nd, "no-decision must inspect no node")
    for row in rt["byOwnerAction"]:
        if "REFUSE" in row["ownerAction"] or "BUSY" in row["ownerAction"]:
            check(row["companionAction"].startswith("no-decision"),
                  "BUSY/REFUSE/QUARANTINE must be a no-decision row")
    check("full triple" in rt["preCommittedInvariant"].lower(),
          "the premature-node check must use the full triple")
    check("retained branch" in rt["preCommittedInvariant"].lower(),
          "a retained branch at an equal numeric pair must be excluded explicitly")
    join = companion["associationJoinRules"]
    check("ancestorSelection" in join, "the ancestor selection join must be stated")
    if "ancestorSelection" in join:
        check("verified chain" in join["ancestorSelection"],
              "an ancestor must be resolved on the verified chain")
        check("never guesses globally" in join["ancestorSelection"]
              or "never guess" in join["ancestorSelection"],
              "an ancestor must not be guessed by numeric pair")

    # correctionOf metadata must describe the CURRENT patch, not a stale one.
    remedy = companion["correctionOf"]["remedy"]
    check("S9-pair-law-and-S9.3.patch" in remedy,
          "correctionOf must name the current patch filename")
    check("TWO hunks" in remedy or "two hunks" in remedy,
          "correctionOf must say the patch is two hunks")
    check("S9.3.patch\"" not in json.dumps(companion).replace(
        "S9-pair-law-and-S9.3.patch", ""),
        "a stale one-hunk patch path is still referenced")

    # --- node-writing is case-derived and only forward writes ----------------
    cases = {c["id"]: c for c in companion["nodeWritingRule"]["cases"]}
    check(set(cases) == {"same-store", "ancestor-reselect", "forward-selection",
                         "unreachable-by-admission"},
          "node-writing cases changed: " + str(sorted(cases)))
    check(cases["same-store"]["nodeWritten"] is False,
          "same-store must write no node")
    check(cases["ancestor-reselect"]["nodeWritten"] is False,
          "ancestor-reselect must write no node")
    check(cases["forward-selection"]["nodeWritten"] is True,
          "forward-selection must write a node")
    for cid in ("same-store", "ancestor-reselect"):
        check("never rewrite" in cases[cid]["recoveryExpectation"].lower()
              or "never rewrites" in cases[cid]["recoveryExpectation"].lower(),
              cid + " recovery must state it never rewrites the retained node")
    check("pure function" in companion["nodeWritingRule"]["principle"].lower(),
          "the case must be a pure function of the admitted intent")

    # --- recovery is conditional, composed, and never expects a bare absence --
    rt = companion["recoveryTotality"]
    check("RESUME-COMMIT" in rt["composition"] and "RELEASE-ONLY" in rt["composition"],
          "recovery must compose with the owner's own returned action")
    pre = rt["preCommittedInvariant"]
    check("wrong to say no node exists" in pre or "It is wrong to say" in pre,
          "the pre-COMMITTED invariant must correct the v2 absence claim")
    check("premature" in pre.lower(), "the premature new-node contradiction must be named")
    check("core operation at `PREPARED`" in rt["ownerPrecedenceAtPrepared"]
          or "core operation" in rt["ownerPrecedenceAtPrepared"],
          "PREPARED must record the owner's core-operation ABORT precedence")
    check("never replaces the owner ABORT" in rt["ownerPrecedenceAtPrepared"]
          or "never a quarantine" in rt["ownerPrecedenceAtPrepared"],
          "a missing node at PREPARED must not become a quarantine")
    dur = companion["durabilityAndReconciliation"]
    check("nonForwardIsNotReconstructible" in dur,
          "the non-forward non-reconstructibility rule must be stated")
    check("case-bound" in json.dumps(dur).lower() or "caseBound" in json.dumps(dur)
          or "derivabilityIsCaseBound" in dur,
          "derivability must be case-bound, not unconditional")
    check("does NOT claim" in dur["noAtomicityClaimed"],
          "the companion must not claim cross-file atomicity")

    # --- digest recipe: domain separation, not impossibility ------------------
    recipe = companion["canonicalDigestRecipe"]
    joined = json.dumps(recipe).lower()
    check("cannot collide" not in joined and "can never collide" not in joined,
          "the recipe must not claim collision is impossible")
    check("collision-resistance assumption" in joined,
          "the recipe must state the collision-resistance assumption")
    check("domainSeparation" in recipe, "the recipe must state domain separation")
    check("sort_keys=True" in recipe["canonicalizer"],
          "the recipe must name the frozen canonicalizer's sort_keys behaviour")
    check(any("order" in item.lower() for item in recipe["whatDoesNotChangeTheDigest"]),
          "the recipe must state that input key order does not change the digest")

    # --- lineage root covers restore/adoption --------------------------------
    root = companion.get("lineageRoot")
    check(root is not None, "the lineage-root law must be stated")
    if root:
        acts = json.dumps(root["creatingActs"]).lower()
        check("installation" in acts and ("restore" in acts or "adoption" in acts),
              "the lineage root must cover installation and restore/adoption")
        obligations = json.dumps(root["obligations"]).lower()
        check("replaces" in obligations and "impersonate" in obligations,
              "a copied marker must be replaced so a restore cannot impersonate its source")
        check("no node is imported" in obligations,
              "no source node may be imported")
        check("no transition is invented" in obligations
              or "no transition is invented" in json.dumps(root).lower(),
              "no public transition may be invented for a root")
    rules = json.dumps(companion["privateCompanionSchema"]["extraAdmissionRules"]).lower()
    check("lineage root" in rules, "the admission rules must name the lineage root")
    check("never names its own triple" in rules,
          "the admission rules must forbid a self predecessor")

    # --- floors --------------------------------------------------------------
    floors = companion["floorsAndAuthority"]
    check("floors forward" in floors["authorizedTransition"]["floors"].lower(),
          "the authorized migration floor carry-forward must be preserved")
    check("MAXIMUM" in floors["authorizedTransition"]["floors"].upper(),
          "the rollback maximum-of-both-stores rule must be preserved")

    # --- the owner patch is two pure insertions ------------------------------
    lines = patch_text.splitlines()
    hunks = [l for l in lines if l.startswith("@@")]
    check(len(hunks) == 2, "the owner patch must be two hunks, got " + str(len(hunks)))
    removed = [l for l in lines if l.startswith("-") and not l.startswith("---")]
    check(not removed, "the owner patch must remove no line, got " + str(len(removed)))
    added = "\n".join(l for l in lines if l.startswith("+") and not l.startswith("+++"))
    check("### S9.3" in added, "the owner patch must insert S9.3")
    check("TRANSITION.SAME_SCHEMA_KEEPS_STORE" in added
          and "TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE" in added,
          "the owner patch must insert the explicit pair law into S9.2")
    check("never rewrites its predecessor" in added
          or "never rewrites" in added,
          "S9.3 must say a retained node's origin is never rewritten")
    check("not name its own triple" in added or "never names its own triple" in added,
          "S9.3 must forbid a self-naming node")
    check("full triple" in added, "S9.3 must state full-triple identity")
    check("marker" in added, "S9.3 must state the store-root marker contract")
    check("never a search key" in added,
          "S9.3 must state that intentDigest is never a search key")
    check("no global uniqueness" in added.lower() or "asserts no global" in added.lower(),
          "S9.3 must not invent global generation uniqueness")
    # Phrases may wrap across diff lines, so normalise whitespace before matching.
    flat = " ".join(added.replace("+", " ").split())
    check("no decision at all" in flat and "inspects nothing" in flat,
          "S9.3 must state that a refusing/busy/quarantining owner leaves no decision")
    check("premature-node contradiction" in flat,
          "S9.3 must name the premature-node contradiction")
    check("retained branch at the same numeric generation" in flat,
          "S9.3 must state a retained branch is expected and untouched")


def digest_properties(C):
    def digest(ns, inst, gen, schema):
        return hashlib.sha256(C.canonical({
            "schemaVersion": 1, "namespaceId": ns, "storeInstanceId": inst,
            "storeGeneration": gen, "stateSchema": schema})).hexdigest()

    ns, old, new = "acme.reports", "a" * 32, "b" * 32
    before = digest(ns, old, 5, 1)
    migrated = digest(ns, new, 6, 2)
    rolled_back = digest(ns, old, 5, 1)
    restored = digest(ns, "c" * 32, 5, 1)
    other_ns = digest("acme.other", old, 5, 1)
    check(migrated != before, "migration must change the digest")
    check(rolled_back == before, "rollback to the retained store must restore the digest")
    check(restored != before, "a new instance must not reproduce a predecessor digest")
    check(other_ns != before, "namespace must participate in the digest")

    a = {"schemaVersion": 1, "namespaceId": ns, "storeInstanceId": old,
         "storeGeneration": 5, "stateSchema": 1}
    b = {"stateSchema": 1, "storeGeneration": 5, "storeInstanceId": old,
         "namespaceId": ns, "schemaVersion": 1}
    reorder_same = (hashlib.sha256(C.canonical(a)).hexdigest()
                    == hashlib.sha256(C.canonical(b)).hexdigest())
    check(reorder_same, "input key order must not change the digest")

    added_member = dict(a, carrierFormat=3)
    removed_member = {k: v for k, v in a.items() if k != "stateSchema"}
    renamed = {("storeGen" if k == "storeGeneration" else k): v for k, v in a.items()}
    changed = all(hashlib.sha256(C.canonical(x)).hexdigest() != before
                  for x in (added_member, removed_member, renamed))
    check(changed, "adding, removing or renaming a member must change the digest")

    framed = C.identity("opensip.design.store-generation-binding", a)
    check(framed != before, "the framed identity must differ on this input")

    refusals = {}
    for name, raw in (("duplicate-key", b'{"a":1,"a":2}'), ("float", b'{"a":1.5}'),
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
            "addRemoveRenameChangesDigest": changed,
            "framedIdentityDiffersOnThisInput": framed != before,
            "framedIdentitySample": framed,
            "separationBasis": "distinct construction and preimage framing, plus the "
                               "standard SHA-256 collision-resistance assumption; not an "
                               "impossibility claim",
            "parseRefusals": refusals}


def main():
    work = Path(sys.argv[1])
    c25 = Path(sys.argv[2])
    arch = work / "docs/v2/architecture"
    companion = load(arch / "store-instance-lineage.v1.json")
    owner = load(c25 / OWNER_SCHEMAS)
    inventory = load(arch / "repository-file-inventory.v1.json")
    recovery = load(arch / "commit-recovery-plan.v1.json")
    patch = (work.parent / "patches" / PATCH).read_text()
    C, canonical_sha = load_frozen_canonicalizer(c25)

    structural_checks(companion, owner, inventory, recovery, patch)
    result = {
        "control": "check_store_instance_lineage",
        "frozenCanonicalizer": {"path": CANONICAL, "sha256": canonical_sha},
        "digestProperties": digest_properties(C),
        "structuralFailures": list(FAILURES),
        "status": "PASS" if not FAILURES else "FAIL",
        "limits": ("Structural and digest checks only. The operation/state behaviour is "
                   "executed by check_lineage_recovery.py against the frozen owner model. "
                   "No product behaviour, no carrier behaviour, no qualification."),
    }
    print(json.dumps(result, indent=1))
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    sys.exit(main())
