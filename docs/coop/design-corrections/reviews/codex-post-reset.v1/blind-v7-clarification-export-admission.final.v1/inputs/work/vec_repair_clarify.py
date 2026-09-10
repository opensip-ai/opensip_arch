"""CLARIFICATION v1 item 2: reassessment of CB7-SHOULD-1.

The ORIGINAL finding imposed an extra equation the kit never states -
`unmetPreconditions[].code == the deficiency token` - and concluded that 11 of
16 producible per-requirement outcomes "cannot be expressed".  This module
tests that equation against the kit and demonstrates the alternative.
"""
import json

import oslib as O
import graph as G
from oslib import C, H, sha256hex, raw_digest

PROJECT = "prj1-" + "a1" * 32
DDC = set(O.doc("common")["$defs"]["DomainDetailCode"]["enum"])
NATIVE_DEF = O.doc("common")["$defs"]["NativeSufficiencyDeficiency"]["enum"]
IMPORTED_DEF = O.doc("common")["$defs"]["ImportedRequirementDeficiency"]["enum"]
IMPORTED_LAW = O.doc("imported-evidence")["x-opensip-imported-requirement-law"]
CONSUMER_BOUNDARY = (O.doc("native")["x-opensip-deficiency-cause-registry"]
                     ["perRequirementConsumerBoundary"])


def where_the_law_puts_the_outcome():
    """Read, do not assume, which field the kit names as the carrier."""
    consumers = CONSUMER_BOUNDARY["consumers"]
    return {
        "namedConsumerRecord": [c["record"] for c in consumers],
        "namedConsumerField": [c["field"] for c in consumers],
        "presenceLaw": [c.get("presenceLaw") for c in consumers],
        "blockAddsNoPublicDetailCode":
            "adds no D9 class, code, exit or public detail code"
            in CONSUMER_BOUNDARY["standing"],
        "standingVerbatim": CONSUMER_BOUNDARY["standing"],
        "conclusion": "The per-requirement outcome's named carrier is "
                      "repair.schema.json#/$defs/EvidenceRequirement.deficiency, "
                      "which admits BOTH closed vocabularies and is REQUIRED "
                      "exactly when satisfied is false. The kit explicitly says "
                      "this boundary adds no public detail code."}


def outcome_expressibility():
    """Both vocabularies, in the field the law actually names."""
    rows = {}
    for v, plane in [(NATIVE_DEF, "native"), (IMPORTED_DEF, "imported")]:
        for token in v:
            req = {"relation": "references" if plane == "native"
                               else "runtime-observation",
                   "minResolution": "resolved-binding" if plane == "native"
                                    else "observed",
                   "completeness": "complete", "satisfied": False,
                   "deficiency": token}
            rows[plane + "/" + token] = {
                "expressibleInEvidenceRequirementDeficiency":
                    O.validate("repair", "#/$defs/EvidenceRequirement", req) == [],
                "isAlsoADomainDetailCodeMember": token in DDC}
    return {"perOutcome": rows,
            "expressibleInTheNamedCarrier":
                sum(1 for r in rows.values()
                    if r["expressibleInEvidenceRequirementDeficiency"]),
            "total": len(rows),
            "alsoDomainDetailCodeMembers":
                sum(1 for r in rows.values() if r["isAlsoADomainDetailCodeMember"])}


def assess_repair_evidence_run_unavailable():
    """Root asked specifically about this registered code's applicability."""
    return {
        "code": "REPAIR.EVIDENCE_RUN_UNAVAILABLE",
        "isRegistered": "REPAIR.EVIDENCE_RUN_UNAVAILABLE" in DDC,
        "boundConditionInTheKit":
            "workflows-and-surfaces.md S6: the evidence Run 'whose availability "
            "is retained and whose sealed assurance is replayable (else the plan "
            "is not applicable with REPAIR.EVIDENCE_RUN_UNAVAILABLE)'",
        "applicableToAnUnsatisfiedEvidenceRequirement": False,
        "why": "It names retained AVAILABILITY and replayable sealed ASSURANCE "
               "of the evidence Run. An unsatisfied evidence requirement is a "
               "different condition: the Run is available and replayable, and "
               "the evidence it carries is insufficient at the demanded rung. "
               "Borrowing it would misname the condition, which is the same "
               "objection this review raised against borrowing "
               "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED.",
        "conclusion": "Not applicable - and NOT needed, because the outcome's "
                      "named carrier is EvidenceRequirement.deficiency, not an "
                      "unmetPreconditions code."}


def _descriptor(requirements, unmet, edits, label):
    proj = {"deadCodeRepairEligible": True, "exportsClosed": "closed",
            "entryPointsRecognized": "all", "nonliteralLoading": "none",
            "externalConsumers": "none-declared"}
    applicable = all(r["satisfied"] for r in requirements) and not unmet
    d = {"schemaFamily": "opensip.product.repair-plan", "schemaMajor": 1,
         "projectId": PROJECT, "snapshotId": "snapshot2:" + "3d" * 32,
         "evidenceRunId": "run2:" + "4e" * 32, "planId": "plan2:" + "5f" * 32,
         "recipe": {"contributionId": "opensip.first-party",
                    "recipeId": "remove-unused-export",
                    "recipeVersion": "1.0.0",
                    "closureId": "closure2:" + "6a" * 32},
         "recipeTrust": "admitted", "evidenceOrigin": "native-analysis",
         "closedWorld": proj, "targets": ["finding-key2:" + "7b" * 32],
         "edits": edits, "totalPostimageBytes": 0,
         "evidenceRequirements": requirements,
         "permittedEditScope": ["src/**"], "applicable": applicable,
         "unmetPreconditions": unmet,
         "limitations": ["a candidate is never a deletion prerequisite"]}
    rid = "repairplan2:" + H("workflow.repair-plan", d)
    plan = {"repairPlanId": rid, "descriptor": d}
    return {"label": label, "repairPlanId": rid, "descriptor": d,
            "schemaErrors": O.validate("repair", "#/$defs/RepairPlanV1", plan),
            "orderFaults": O.admit_ordered("repair", "#/$defs/RepairPlanV1", plan),
            "applicable": applicable,
            "retainedDeficiencies": [r.get("deficiency") for r in requirements],
            "remedies": [u["remedy"] for u in unmet],
            "codes": [u["code"] for u in unmet]}


def two_causes_two_remedies():
    """The demonstration root asked for: two DIFFERENT causes, one of them
    IMPORTED, in schema-admitted COMPLETE repair descriptors, distinguished by
    REMEDY with NO new DomainDetailCode."""
    edits = [{"path": "src/dead.ts", "action": "delete",
              "preimageDigest": sha256hex(b"dead\n"),
              "postimageDigest": None, "postimageBytes": 0}]

    # (a) NATIVE cause whose token is NOT a DomainDetailCode member
    req_a = [{"relation": "references", "minResolution": "resolved-binding",
              "completeness": "complete", "satisfied": False,
              "deficiency": "required-relation-missing"}]
    unmet_a = [{"code": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED",
                "subject": "references@resolved-binding",
                "remedy": "native plane, relation references at rung "
                          "resolved-binding: required-relation-missing - the "
                          "evidence Run carries no view entry for this "
                          "relation; re-analyse with the references capability "
                          "requested for this unit"}]

    # (b) IMPORTED cause, grounded by the imported law in an EXISTING condition
    req_b = [{"relation": "history-change", "minResolution": "observed",
              "completeness": "complete", "satisfied": False,
              "deficiency": "history-range-insufficient"}]
    unmet_b = [{"code": "IMPORT.ABSENT_FOR_PREDICATE",
                "subject": "history-change@observed",
                "remedy": "imported plane, relation history-change at rung "
                          "observed: history-range-insufficient - the mapped "
                          "history import's revisionRange does not meet the "
                          "recipe's declared demand; widen the collected "
                          "revision range and re-import"}]

    a = _descriptor(req_a, unmet_a, edits, "native/required-relation-missing")
    b = _descriptor(req_b, unmet_b, edits, "imported/history-range-insufficient")

    # a THIRD control: the same two causes with the SAME remedy string would
    # NOT satisfy the law's purpose clause; this is the discriminating check.
    same_remedy = [{"code": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED",
                    "subject": "x", "remedy": "the plan is not applicable"}]
    c1 = _descriptor(req_a, same_remedy, edits, "control/collapsed-remedy-a")
    c2 = _descriptor(req_b, same_remedy, edits, "control/collapsed-remedy-b")

    return {
        "nativeCause": a, "importedCause": b,
        "bothSchemaAdmitted": not a["schemaErrors"] and not b["schemaErrors"],
        "bothOrderAdmitted": not a["orderFaults"] and not b["orderFaults"],
        "remediesDiffer": a["remedies"] != b["remedies"],
        "exactPlaneRelationRungDeficiencyInEachRemedy": all(
            all(t in r for t in toks) for r, toks in
            [(a["remedies"][0], ["native", "references", "resolved-binding",
                                 "required-relation-missing"]),
             (b["remedies"][0], ["imported", "history-change", "observed",
                                 "history-range-insufficient"])]),
        "deficiencyRetainedInEvidenceRequirements": {
            "native": a["retainedDeficiencies"],
            "imported": b["retainedDeficiencies"]},
        "applicableFalseInBoth": a["applicable"] is False and b["applicable"] is False,
        "newDomainDetailCodesRequired": 0,
        "codesUsedAreRegistered": all(u in DDC for u in a["codes"] + b["codes"]),
        "discriminatingControl": {
            "note": "collapsing both causes onto one remedy string is what the "
                    "purpose clause forbids; the two descriptors then differ "
                    "only in evidenceRequirements, and the REMEDY no longer "
                    "distinguishes them",
            "remediesDifferUnderCollapse": c1["remedies"] != c2["remedies"],
            "collapsedRemedyA": c1["remedies"], "collapsedRemedyB": c2["remedies"]},
        "emptyUnmetPreconditionsIsAlsoLawful": {
            "applicableDescription": O.doc("repair")["$defs"]
                ["RepairPlanDescriptor"]["properties"]["applicable"]["description"],
            "reading": "'true only when every evidenceRequirement is satisfied "
                       "AND unmetPreconditions is empty' is a conjunction: "
                       "applicable:false follows from the first conjunct alone, "
                       "so an unsatisfied requirement with an EMPTY "
                       "unmetPreconditions is consistent with the published "
                       "description.",
            "measured": _descriptor(req_a, [], edits, "empty-unmet")},
    }


def expressible_versus_authorized():
    """A schema-admitted descriptor is NOT a fully authorized repair."""
    d = two_causes_two_remedies()
    rid_a = d["nativeCause"]["repairPlanId"]
    rid_b = d["importedCause"]["repairPlanId"]
    authz = {"authorizationSchema": 1, "kind": "repair-apply",
             "projectId": PROJECT, "repairPlanId": rid_a,
             "baseSnapshotId": "snapshot2:" + "3d" * 32,
             "recipeClosureId": "closure2:" + "6a" * 32,
             "consent": {"mode": "interactive-explicit", "policyRecordId": None,
                         "ci": False},
             "expiry": "operation-end", "leaseMode": "EXCLUSIVE",
             "repositoryExecution": False}
    return {
        "descriptorIsSchemaAdmitted": not d["nativeCause"]["schemaErrors"],
        "descriptorApplicable": d["nativeCause"]["applicable"],
        "authorizationSchemaErrors":
            O.validate("security", "#/schemas/RepairApplyAuthorizationV1", authz),
        "authorizationNamesPlan": rid_a,
        "authorizationDoesNotNameTheOtherPlan": rid_a != rid_b,
        "applyRequires": [
            "applicable == true (workflows S6: applicable is false whenever any "
            "requirement is unsatisfied)",
            "a security RepairApplyAuthorizationV1 bound to the EXACT "
            "repairPlanId, base snapshot and project",
            "current recipe trust and live authorization re-checked immediately "
            "before apply"],
        "conclusion": "An expressible, schema-admitted RepairPlanV1 carrying an "
                      "unsatisfied requirement is a DISCLOSURE. It is not an "
                      "authorized repair: applicable is false, and any edit to "
                      "the descriptor mints a different repairPlanId that no "
                      "authorization names."}


def build():
    return {"whereTheLawPutsTheOutcome": where_the_law_puts_the_outcome(),
            "outcomeExpressibility": outcome_expressibility(),
            "repairEvidenceRunUnavailableAssessment":
                assess_repair_evidence_run_unavailable(),
            "importedLawGroundsOutcomesInExistingConditions": {
                "outcomes": {k: {"meaning": v["meaning"],
                                 "groundedIn": v.get("groundedIn", "")}
                             for k, v in IMPORTED_LAW["outcomes"].items()},
                "precedence": IMPORTED_LAW["precedence"],
                "theKitItselfDistinguishesByRemedy":
                    "because the remedies differ"
                    in IMPORTED_LAW["outcomes"]["import-absent-for-requirement"]
                    ["groundedIn"]},
            "twoCausesTwoRemedies": two_causes_two_remedies(),
            "expressibleVersusAuthorized": expressible_versus_authorized()}
