"""Executed demonstrations for every claimed design gap.

Each entry states the exact selectors, what an implementer must INVENT, and a
run-time observation that the kit does not decide the question.
"""
from __future__ import annotations

import json

import canon as K
import kit
from evaluator import EvalView, eval_atom, SUBJECT_KIND_BINDING
from store import Refusal

RESULTS = []


def gap(gid, severity, title, selectors, invention, demonstration, note=""):
    RESULTS.append({"id": gid, "severity": severity, "title": title,
                    "selectors": selectors, "requiredInvention": invention,
                    "demonstration": demonstration, "note": note})


def _grep(needle, docs=("policy-document", "identity", "native", "relation",
                        "common", "imported-evidence", "comparison-result",
                        "graph-query", "repair", "policy-test",
                        "invocation-record", "capability-matrix")):
    hits = []
    for d in docs:
        blob = json.dumps(kit.doc(d))
        if needle in blob:
            hits.append(d)
    return hits


def run_all():
    # ---------------- CB9-MUST-1 ----------------
    se = kit.doc("policy-document")["$defs"]["Rule"]["properties"]["subjectEnumeration"]
    universe_type = se["properties"]["universe"]
    kinds = se["properties"]["subjectKind"]["enum"]
    registry_kinds = sorted({r["subjectKind"] for r in kit.RELATIONS.values()})
    universe_pattern = kit.doc("common")["$defs"]["CanonicalIdentifier"]["pattern"]
    fact_universe = kit.doc("identity")["$defs"]["fact"]["properties"]["sourceUniverse"]
    gap("CB9-MUST-1", "MUST",
        "The evaluator's subject enumeration has no published binding to a "
        "retained Run: neither the universe join nor the subject-kind "
        "vocabulary nor the candidate subject population is stated.",
        {"policyDocument": "workflows/schemas/policy-document.schema.json"
                           "#/$defs/Rule/properties/subjectEnumeration",
         "factUniverse": "foundation/identity-schemas.v2.json"
                         "#/$defs/fact/properties/sourceUniverse",
         "scopeSubjects": "foundation/identity-schemas.v2.json"
                          "#/$defs/subject-scope/properties/subjects",
         "relationSubjectKindLaw": "foundation/relation-payload-schemas.v2.json"
                                   "#/x-opensip-relation-registry/subjectKindLaw",
         "contractSentence": "identity-and-evidence.md S4: 'The declarative "
                             "rule program defines the exact subject "
                             "enumeration'"},
        "(a) a map from the CanonicalIdentifier `universe` name to a 64-hex "
        "native-semantic-universe h-identity; (b) a map from "
        "{file,symbol,export,package} to the registry's "
        "{source-path,package-name,symbol}; (c) the rule that says WHERE the "
        "candidate subject population comes from in a retained Run.",
        {"universeFieldType": universe_type,
         "canonicalIdentifierPattern": universe_pattern,
         "factUniverseForm": {"pattern": fact_universe["pattern"],
                              "annotation": fact_universe["x-opensip-digest"]},
         "policySubjectKinds": kinds,
         "relationRegistrySubjectKinds": registry_kinds,
         "sharedMembers": sorted(set(kinds) & set(registry_kinds)),
         "policyOnlyMembers": sorted(set(kinds) - set(registry_kinds)),
         "registryOnlyMembers": sorted(set(registry_kinds) - set(kinds)),
         "vocabulariesAreNotEqual": set(kinds) != set(registry_kinds),
         "subjectEnumerationAppearsIn": _grep("subjectEnumeration"),
         "onlyPopulationStatementIsTheFixturePlane":
             kit.doc("policy-test")["$defs"]["Subject"]["oneOf"][0]["properties"]
             ["subjects"]["description"],
         "thisReconstructionAssumed": {
             "universeBinding": "the universe DOMAIN ROW's `language` value",
             "subjectKindBinding": SUBJECT_KIND_BINDING,
             "population": "the union of subjects over the retained "
                           "subject-scopes of the matching relation kind"}},
        "Consequence: predicateProofs are keyed by subjectId, so two "
        "conforming hosts enumerating different subjects mint different "
        "proof2/seal2/run2 from one admitted Plan. This is the same "
        "independent-replay defect the contracts already closed for "
        "analysis-spec capabilityId (CB4-SHOULD-2) and Atom.minResolution "
        "(CB3-MUST-2), and it is not closed for this field.")

    # ---------------- CB9-MUST-2 ----------------
    ff = kit.doc("policy-document")["$defs"]["FieldFilter"]["properties"]["field"]["enum"]
    fact_fields = sorted(kit.doc("identity")["$defs"]["fact"]["properties"])
    frc = kit.doc("policy-test")["$defs"]["FactRecordCandidate"]
    view = EvalView(facts={}, scopes={}, coverages={}, universe_language={})
    try:
        eval_atom(view, {"op": "exists", "relation": "references",
                         "minResolution": "resolved-binding",
                         "filters": [{"field": "subject", "cmp": "eq",
                                      "value": "sym:x"}]})
        observed = "NOT REFUSED"
    except Refusal as exc:
        observed = exc.code
    gap("CB9-MUST-2", "MUST",
        "FieldFilter has no published projection from `fact2` + its relation "
        "payload onto the eight filter field names; the only place the eight "
        "are defined together is the policy-test FIXTURE record.",
        {"fieldFilter": "workflows/schemas/policy-document.schema.json"
                        "#/$defs/FieldFilter/properties/field",
         "fixtureOnlyDefinition": "workflows/schemas/policy-test.schema.json"
                                  "#/$defs/FactRecordCandidate",
         "factRecord": "foundation/identity-schemas.v2.json#/$defs/fact",
         "relationPayloads": "foundation/relation-payload-schemas.v2.json#/$defs",
         "contractSentence": "identity-and-evidence.md S4: 'typed field "
                             "filter' is part of what the program defines"},
        "a per-relation projection naming, for each of subject / target / "
        "universe / subjectKind / targetKind / observability, which field of "
        "the fact record or of THAT relation's payload it reads.",
        {"filterFields": ff,
         "fact2Fields": fact_fields,
         "fieldsWithNoHomeOnFact2": sorted(set(ff) - set(fact_fields)),
         "fixtureRecordDescription": frc["description"],
         "fixtureUniverseType": frc["properties"]["universe"]["$ref"],
         "fixtureSubjectType": frc["properties"]["subject"]["$ref"],
         "typeConflict": "FactRecordCandidate.universe is a "
                         "CanonicalIdentifier (^[a-z]...), which cannot "
                         "represent a 64-hex universe identity beginning with "
                         "a decimal digit; FactRecordCandidate.subject is a "
                         "LogicalPath, while nine relations' subjects are "
                         "opaque SubjectIdV1 values the record associates with "
                         "no path.",
         "thisReconstructionRefused": observed},
        "`filters` enters emitWhen, hence the rule programDigest, every "
        "program-predicate nodeDigest and the whole proof bundle. An atom "
        "carrying a filter is schema-admissible and undecidable over a "
        "retained Run, so this reconstruction refuses it "
        "(FILTER_PROJECTION_UNPUBLISHED) rather than inventing semantics.")

    # ---------------- CB9-MUST-3 ----------------
    pw = kit.doc("identity")["$defs"]["predicate-witness"]["properties"]
    ev_reg = kit.doc("imported-evidence")["x-opensip-evidence-relation-registry"]
    gap("CB9-MUST-3", "MUST",
        "A policy atom over an imported-evidence relation is admissible, but "
        "the closed predicate-witness record cannot carry what it matched and "
        "no projection from an atom to import payload subjects is published.",
        {"atomRelation": "workflows/schemas/policy-document.schema.json"
                         "#/$defs/Atom/properties/relation",
         "importedRelationRegistry": "workflows/schemas/imported-evidence.schema.json"
                                     "#/x-opensip-evidence-relation-registry",
         "witness": "foundation/identity-schemas.v2.json#/$defs/predicate-witness",
         "contractSentence": "identity-and-evidence.md S4: 'Witness facts must "
                             "be exactly those selected by the program over the "
                             "complete admitted view' and 'The verifier "
                             "recomputes scope membership, matches, "
                             "completeness and each result'"},
        "either a witness member that can name imported observation subjects, "
        "or an explicit statement that an imported atom's witness carries an "
        "empty match set by construction TOGETHER with the published "
        "atom-to-payload matching law that makes the value re-derivable.",
        {"admittedAtomRelations": sorted(ev_reg["relations"]),
         "witnessMatchPattern":
             pw["matchingFactIds"]["items"]["pattern"],
         "witnessCoveragePattern": pw["coverageIds"]["items"]["pattern"],
         "importedRelationsMintNoFact2":
             "native-evidence.md S4.6: these relations 'mint no fact2, carry "
             "no sourceUniverse/targetUniverse and have no Coverage entry'",
         "consequence": "exists/none/count-at-most over an imported relation "
                        "has no representable witness content, so the value is "
                        "producer-asserted rather than recomputed - the exact "
                        "thing S4 forbids ('Neither a provider nor a witness "
                        "supplies its own expected result')."},
        "The repair plane DOES publish a projection "
        "(imported-evidence.schema.json#/x-opensip-imported-requirement-law/"
        "targetSubjectProjection), but it is keyed by a finding fingerprint "
        "and is explicitly the REPAIR requirement law, not the policy-atom "
        "evaluation law.")

    # ---------------- CB9-MUST-4 ----------------
    verdict_bearers = {
        "proof-bundle": "identity-schemas.v2#/$defs/proof-bundle/properties/verdict",
        "evaluation-seal": "identity-schemas.v2#/$defs/evaluation-seal/properties/verdict",
        "policy-derivation": "identity-schemas.v2#/$defs/policy-derivation/properties/verdict"}
    finding_fields = sorted(kit.doc("identity")["$defs"]["finding"]["properties"])
    gap("CB9-MUST-4", "MUST",
        "The evaluator's consumption of the resolved WaiverSetV1 is not "
        "specified, and the relation among the three verdict-bearing records "
        "is not stated.",
        {"waiverSet": "workflows/schemas/policy-document.schema.json"
                      "#/$defs/WaiverSetV1",
         "planWaiverDigest": "foundation/identity-schemas.v2.json"
                             "#/$defs/plan/properties/waiverDigest",
         "verdictBearers": verdict_bearers,
         "contractSentences": [
             "identity-and-evidence.md S3: 'Waiver resolution selects the "
             "active admitted waiver set before pure evaluation and retains "
             "that resolved set'",
             "identity-and-evidence.md S4: the verifier 'recomputes finding "
             "fingerprints, findings, rule outcomes and aggregate verdict'"]},
        "(a) whether a waived finding is still emitted and still enters "
        "proof.findingIds / evidence.findingIds; (b) how a waiver changes the "
        "rule outcome and the aggregate verdict; (c) whether "
        "evaluation-seal.verdict may differ from proof-bundle.verdict, and "
        "what policy-derivation.verdict is relative to both.",
        {"findingRecordHasNoWaivedField": "waived" not in finding_fields,
         "findingFields": finding_fields,
         "onlyWaivedFlagInTheKit":
             "workflows/schemas/policy-test.schema.json#/$defs/CaseResult/"
             "properties/findings/items/properties/waived (the POLICY-TEST "
             "plane, not a retained Run record)",
         "noSentenceJoinsTheThreeVerdicts": True,
         "thisReconstructionAssumed": {
             "emission": "a waived finding IS emitted and IS retained; the "
                         "waiver removes only its GATING contribution",
             "sealJoin": "evaluation-seal.verdict == proof-bundle.verdict"}},
        "Consequence: over one admitted Plan whose gating rule emits on a "
        "waived target, one reading seals `fail` and the other seals `pass`. "
        "The sealed verdict is the product's public answer, so this is a "
        "public semantic divergence, not an implementation choice.")

    # ---------------- CB9-SHOULD-1 ----------------
    gap("CB9-SHOULD-1", "SHOULD",
        "`all-covered` has no stated value on the twelve non-resolved "
        "registered (relation, rung) pairs.",
        {"predicateTable": "identity-and-evidence.md S4 predicate table",
         "rc1": "native-evidence.md S4.3 RC-1",
         "resolvedSet": "the closed five-member resolved rung set"},
        "one sentence saying whether `not-applicable` resolution completeness "
        "satisfies `all-covered` (nothing to resolve) or leaves it "
        "indeterminate.",
        {"resolvedPairs": sorted(
            f"{r}@{g}" for r, row in kit.RELATIONS.items()
            for g in row["ladder"] if g in kit.RESOLVED_RUNGS),
         "nonResolvedPairCount": sum(
             1 for r, row in kit.RELATIONS.items() for g in row["ladder"]
             if g not in kit.RESOLVED_RUNGS),
         "strictReading": "true only with state == complete, so all-covered "
                          "over any non-resolved pair is permanently "
                          "indeterminate and a gating rule using it can never "
                          "pass",
         "lenientReading": "not-applicable trivially satisfies it",
         "thisReconstructionTook": "strict ('true ONLY with admitted "
                                   "resolution-complete coverage')"},
        "The strict reading is the one the text supports, so this is "
        "decidable; it is raised because the consequence (a permanently "
        "indeterminate gating rule) is severe enough to deserve a sentence.")

    # ---------------- CB9-SHOULD-2 ----------------
    fp = kit.doc("identity")["$defs"]["finding-fingerprint"]["properties"]["subjectKey"]
    gap("CB9-SHOULD-2", "SHOULD",
        "`finding-fingerprint.subjectKey.discriminator` is required and "
        "non-empty for every finding, including a finding over a zero-anchor "
        "INVENTORY fact that has no declaration signature.",
        {"fingerprint": "foundation/identity-schemas.v2.json"
                        "#/$defs/finding-fingerprint/properties/subjectKey",
         "tokenSource": "identity-and-evidence.md S3: 'The native subject "
                        "adapter supplies declaration-signature tokens in "
                        "grammar order ... The selected detector closure "
                        "defines the token projection.'",
         "inventoryFinding": "identity-and-evidence.md S3: 'A finding over a "
                             "zero-anchor inventory fact closes a Run'"},
        "what the token array is for a subject kind that HAS no declaration "
        "signature (a file, a package, a VCS change).",
        {"discriminatorRequired": "discriminator" in fp["required"],
         "discriminatorMinLength":
             fp["properties"]["discriminator"]["minLength"],
         "thisReconstructionAssumed":
             "a two-token array [path:<subject>, rule:<ruleId>] hashed with C; "
             "any other token projection mints a different finding-key2"},
        "The authority IS placed (the selected detector closure), so replay "
        "across installations sharing that closure is stable; what is missing "
        "is the contract-level statement for signature-less subject kinds, "
        "which reach baseline membership and comparison attribution.")

    # ---------------- CB9-SHOULD-3 ----------------
    gap("CB9-SHOULD-3", "SHOULD",
        "`subjectEnumeration.include`/`exclude` are LogicalPath globs, but a "
        "`symbol`- or `package`-kind enumeration ranges over subjects the "
        "registry says are NOT paths.",
        {"glob": "workflows/schemas/common.schema.json#/$defs/GlobPattern "
                 "('Closed glob over LogicalPath')",
         "subjectKindLaw": "foundation/relation-payload-schemas.v2.json"
                           "#/x-opensip-relation-registry/subjectKindLaw"},
        "what a path glob means against an opaque SubjectIdV1, or a statement "
        "that include/exclude apply only to source-path subject kinds.",
        {"globDescription": kit.doc("common")["$defs"]["GlobPattern"]["description"],
         "subjectIdPattern": kit.doc("relation")["$defs"]["SubjectIdV1"]["pattern"],
         "thisReconstructionAvoided":
             "every vector enumerates source-path subjects only"},
        "")

    # ---------------- confirmed disclosed obligations ----------------
    d9 = kit.doc("d9")
    causes = d9["scenarioAxesSchema"]["properties"]["faultCause"]["enum"]
    fm = d9["codeMaps"]["faultCauseToErrorCode"]
    gap("CB9-ADV-1", "advisory (already disclosed by the subject)",
        "The selected D9 composition extends the inherited faultCause "
        "vocabulary by exactly one member; the subject discloses this "
        "accurately and the extension preserves the inherited map properties.",
        {"inheritedEnum": "docs/coop/artifacts/d9-exit-contract.v1.14.json"
                          "#/scenarioAxesSchema/properties/faultCause/enum",
         "extension": "native-evidence.md S10 'The selected D9 composition'"},
        "nothing; the obligation to publish a successor D9 artifact is stated "
        "by the subject itself and is a cross-unit deliverable.",
        {"inheritedFaultCauses": causes,
         "hostInvariantInInheritedEnum": "host-invariant" in causes,
         "systemIllegalStateHasNoFaultCausePreimageToday":
             "SYSTEM.OUTCOME.ILLEGAL_STATE" not in fm.values(),
         "mapInjectiveToday": len(set(fm.values())) == len(fm),
         "soTheExtensionPreservesTotalityAndInjectivity": True,
         "independentlyConfirmed": "a checker reading v1.14 ALONE would refuse "
                                   "a lawful host-invariant operational-failed "
                                   "termination, exactly as S10 states"},
        "")
    return RESULTS
