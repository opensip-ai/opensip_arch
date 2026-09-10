"""Vector group F: closure-membership joins, the finding-fingerprint
discriminator, schema-valid comparison entries, and the two representability
gaps this reconstruction found."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import S, V, PROJECT_ID, TS_PROV_CID, EVAL_CID
from build_ts2 import PLAN, PLAN_ID, POLICY_DIGEST
from build_ts3 import (VIEW, FILE_SCOPE, DECL_SCOPE, CL_SCOPE, PROOF, SEAL,
                       DECL_F, RUN_ID)
from build_rust import RS_PROV_CID
from build_syntax import SY_PROV_CID
from build_workflow import validate

# ------------------------------------------- closure kind and Plan membership
KINDS = DIGDOM["closureKinds"]["byField"]


def closure_kind_of(cid):
    return S.reframe_check(cid.split(":")[1], "closure")["kind"]


CHECKS = {
    "subject-scope.enumeratorClosure": [FILE_SCOPE["enumeratorClosure"],
                                        DECL_SCOPE["enumeratorClosure"],
                                        CL_SCOPE["enumeratorClosure"]],
    "view.producerClosure": [VIEW["producerClosure"]],
    "fact.producerClosure": [DECL_F["producerClosure"]],
    "proof-bundle.evaluatorClosure": [PROOF["evaluatorClosure"]],
    "evaluation-seal.evaluatorClosure": [SEAL["evaluatorClosure"]],
}
V["JOIN-1-closure-kind-and-plan-membership"] = {
    "declaredKindByField": {k: KINDS[k] for k in CHECKS},
    "observed": {k: sorted({closure_kind_of(c) for c in v}) for k, v in CHECKS.items()},
    "allKindsAgree": all(closure_kind_of(c) == KINDS[k] for k, v in CHECKS.items() for c in v),
    "everyClosureIsAPlanSelectedSemanticClosure":
        all(c in PLAN["semanticClosures"] for v in CHECKS.values() for c in v),
    "planSemanticClosures": PLAN["semanticClosures"],
    "noEnumeratorClosureKindIsMinted": "enumeration, view production, fact production and "
                                       "stage production are all PROVIDER acts",
    "providersUsedAcrossTheThreeUniverses": {
        "typescript": TS_PROV_CID, "rust": RS_PROV_CID, "syntax": SY_PROV_CID}}

# ----------------------------------------- finding-fingerprint discriminator
TOKENS = ["ts", "function", "helper", "generic:0", "(x: number)", "=> number", "helper"]
# grammar order, REPEATED tokens retained, body and positions excluded
DISC = rawbytes(C(TOKENS))
_dedup = rawbytes(C(sorted(set(TOKENS))))
FP = {"schemaVersion": 2, "ruleStableId": "R-ORPHAN", "detectorSemanticsMajor": 2,
      "subjectKey": {"language": "typescript", "kind": "function",
                     "logicalPath": "src/util.ts", "qualifiedName": "helper",
                     "discriminator": DISC},
      "relatedSubjectKeys": []}
FP_ID = S.mint("finding-fingerprint", FP)
V["ID-3-finding-fingerprint-discriminator"] = {
    "declarationSignatureTokens": TOKENS,
    "orderLaw": "grammar order, REPEATED tokens retained; body and positions excluded",
    "recipe": "raw SHA-256 of the canonical JSON ORDERED string array",
    "canonicalArrayBytes": C(TOKENS).decode(),
    "discriminator": DISC,
    "sortingOrDeduplicatingChangesIt": DISC != _dedup,
    "fingerprintExcludes": ["line offsets", "messages", "timestamps", "concrete evidence"],
    "fingerprintId": FP_ID,
    "ambiguousKeysRefuseRatherThanBeingSuffixedByEncounterOrder": True,
    "aStableFingerprintIsNotProofOfUnchangedDetectorSemantics": True}

# ------------------------------------------- schema-valid comparison entries
def presence(b=True, e0=True, e1=True, e2=True, e3=True, e4=True, wb=False, wc=False):
    return {"B": b, "E0": e0, "E1": e1, "E2": e2, "E3": e3, "E4": e4,
            "waivedB": wb, "waivedC": wc}


FPX = "finding-key2:" + "5e" * 32
CMP_ENTRIES = {
    "A1-missing-required-detector-pivot": {
        "fingerprint": FPX, "ruleId": "r.dead-code", "detectorId": "det.core",
        "presence": presence(e0=False), "classification": "INDETERMINATE",
        "indeterminateReason": "pivot-detector-unavailable", "subsequentDeltas": [],
        "liveInCurrent": True, "gates": True, "gateReason": "indeterminate-gating-rule"},
    "A2-evidence-changed-on-a-gating-rule": {
        "fingerprint": "finding-key2:" + "6f" * 32, "ruleId": "r.cold-code",
        "detectorId": "det.core", "presence": presence(), "classification": "INDETERMINATE",
        "indeterminateReason": "evidence-availability-changed", "subsequentDeltas": [],
        "liveInCurrent": True, "gates": True, "gateReason": "indeterminate-gating-rule"},
    "A4-code-net-new-hidden-by-a-same-change-policy-edit": {
        "fingerprint": "finding-key2:" + "7a" * 32, "ruleId": "r.new-bug",
        "detectorId": "det.core",
        "presence": presence(b=False, e0=False, e1=True, e2=False, e3=False, e4=False),
        "classification": "CODE-NET-NEW", "direction": "appeared",
        "subsequentDeltas": ["policy"], "liveInCurrent": False, "gates": True,
        "gateReason": "code-net-new-policy-hidden"},
    "A6-scope-delta-from-the-ScopeDocumentV1-axis-alone": {
        "fingerprint": "finding-key2:" + "8b" * 32, "ruleId": "r.lint",
        "detectorId": "det.core",
        "presence": presence(b=False, e0=False, e1=False, e2=False, e3=True, e4=True),
        "classification": "SCOPE-DELTA", "direction": "appeared", "subsequentDeltas": [],
        "liveInCurrent": True, "gates": False},
}
V["CMP-4-schema-validated-comparison-entries"] = {
    "entries": CMP_ENTRIES,
    "schemaErrors": {k: validate("urn:opensip:product-v1:workflows:comparison-result",
                                 "#/$defs/Entry", e) for k, e in CMP_ENTRIES.items()},
    "pivotPresenceCarriesWaivedFlagsOnBothSides": True,
    "aClassifiedEntryDeclaresItsDirection": True}

# =========================================================== the found gaps
EVREQ_D9 = loadj("docs/coop/design-corrections/workflows/schemas/"
                 "common.schema.json")["$defs"]["D9Deficiency"]["enum"]
DEFV2 = NAT["$defs"]["DeficiencyV2"]["enum"]
DDC = set(loadj("docs/coop/design-corrections/workflows/schemas/"
                "common.schema.json")["$defs"]["DomainDetailCode"]["enum"])
V["GAP-1-EvidenceRequirement-deficiency-cannot-express-four-of-nine-sufficiency-outcomes"] = {
    "field": "workflows/schemas/repair.schema.json#/$defs/EvidenceRequirement/properties/deficiency",
    "declaredType": "urn:opensip:product-v1:workflows:common#/$defs/D9Deficiency",
    "d9DeficiencyEnum": sorted(EVREQ_D9),
    "itsOnlyDefinedProducer": "native-evidence sec.4.6 sufficiency_v2, whose outcome vocabulary "
                              "is DeficiencyV2 (native sec.10 precedence list)",
    "deficiencyV2Enum": sorted(DEFV2),
    "membersTheFieldCannotExpress": sorted(set(DEFV2) - set(EVREQ_D9)),
    "includingTheCanonicalRepairCase":
        "resolution-incomplete is exactly what sufficiency_v2 step 6 mandates for a "
        "universal-negative under unresolvedEdgePolicy=forbid over an affected target - "
        "the case a destructive unused-code recipe turns on",
    "noPublishedMappingEitherWay": True,
    "twoConformingReadings": [
        "write the D9-MAPPED value (verdict-indeterminate), which collapses all four "
        "successor members and destroys the per-requirement distinction native sec.10 "
        "went to length to preserve",
        "write the sufficiency_v2 value, which is schema-invalid for four of nine",
        "omit the optional field, which drops the disclosure entirely"],
    "whyThisIsNotResolvedByTheDomainDetailCodeRoute":
        "native sec.10's public route for a native deficiency is DomainDetailCode, and it "
        "covers a DIFFERENT five members: " + json.dumps(
            {m: (m in DDC) for m in sorted(DEFV2)}) +
        ". The union of the two vocabularies covers all nine, but NEITHER single field does, "
        "and EvidenceRequirement.deficiency is a single field.",
    "grade": "MUST"}

TSCFG = NAT["$defs"]["TypeScriptConfigGraphV1"]
V["GAP-2-TypeScriptConfigGraphV1-node-kind-has-no-published-derivation"] = {
    "field": "native/native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1"
             "/properties/nodes/items/properties/kind",
    "schemaSupplies": TSCFG["properties"]["nodes"]["items"]["properties"]["kind"],
    "proseSays": "native-evidence sec.2.2: 'Node kind agrees with its path as specified by the "
                 "schema and native admission.'",
    "butTheSchemaSuppliesOnlyTheEnum": True,
    "andNoNativeAdmissionRuleForItIsPublishedInThisKit": True,
    "whyItMatters": "kind is inside the hashed record. tsconfigGraphHash = raw SHA-256 of "
                    "C(TypeScriptConfigGraphV1); the universe REQUIRES it and the binding "
                    "checks equality, so the universe H identity moves with it - and that "
                    "identity is fact.sourceUniverse / subject-scope.sourceUniverse, hence "
                    "fact2, scope2, coverage2, view2, evidence2, seal2 and RunId.",
    "twoNaturalReadingsThatDisagreeOnRealFiles": {
        "basenameExactly": "'tsconfig.json' -> tsconfig, 'jsconfig.json' -> jsconfig, "
                           "everything else -> other  (what this reconstruction used)",
        "basenamePrefix": "any 'tsconfig*.json' -> tsconfig  (the widespread "
                          "tsconfig.build.json / tsconfig.base.json convention)"},
    "discriminatingFile": "tsconfig.build.json reached as a base of the entry: `other` under "
                          "the first reading, `tsconfig` under the second, two different "
                          "tsconfigGraphHash values, two different RunIds for one repository",
    "thisIsTheContractsOwnStandard":
        "CB4-SHOULD-2 elevated exactly this class of defect for analysis-spec capabilityId - "
        "'two conforming hosts requesting the same analysis of the same unit therefore mint "
        "different analysisSpecDigests, different PlanIds and different RunIds, which defeats "
        "independent replay across machines' - and closed it by naming the vocabulary "
        "authority. The same closure is owed here.",
    "notFixedByConfigOriginDerivation":
        "configOrigin is derived from the ENTRY node's kind only, and 'other' and 'tsconfig' "
        "both derive `tsconfig`, so the derivation law does not pin the field; it is the "
        "HASH, not configOrigin, that diverges - including for NON-entry nodes, whose kind "
        "affects no derived value at all yet is committed to the identity.",
    "grade": "MUST"}

V["GAP-3-command-name-to-mutationClass-mapping-unpublished"] = {
    "grade": "SHOULD",
    "seeVector": "WF-11-command-name-to-mutationClass-mapping"}

V["GAP-4-coverage-partition-omission-clause-has-no-decidable-referent-for-symbol-relations"] = {
    "grade": "SHOULD",
    "identityStatement": "identity-and-evidence sec.3: 'Coverage scopes partition the claimed "
                         "universe without overlaps or omissions'",
    "nativeStatement": "native-evidence sec.1.2: 'Which relations owe totality is stated in the "
                       "relation registry (coverageTotality), where only `file` has a row, and "
                       "never inferred.'",
    "overlapHalfIsDecidable": "pairwise disjointness of subjects within one (snapshotId, "
                              "relation, resolution, sourceUniverse, targetUniverse) key",
    "omissionHalfIsNotDecidableForSymbolRelations":
        "native sec.1.2 states that the enumerator's attribution of symbols to files is "
        "TRUSTED and not re-derivable from the retained Run, and no document publishes an "
        "enumeration of the symbol universe, so 'without omissions' has no referent a "
        "closure checker can evaluate for declares/literal/control-flow/imports/references/"
        "calls/types/reachability/unresolved-edge",
    "twoConformingReadings": [
        "'the claimed universe' is the union of the scopes' own committed subjects, making "
        "the omission clause vacuous and the sentence an overlap rule only",
        "'the claimed universe' is what exists, making the clause unenforceable for eight of "
        "the nine symbol relations and inconsistent with the coverageTotality registry"],
    "whyItIsSHOULDAndNotMUST": "the registry statement is the more specific successor and "
                               "resolves the conflict in practice; what is missing is the "
                               "reconciliation in text, which an implementer must supply",
    "notInventedHere": "this reconstruction used the registry reading (only `file@enumerated` "
                       "owes totality) and enforced overlap-freedom separately"}

V["GAP-5-js-synthesized-recognition-vs-U-1-unit-markers"] = {
    "grade": "ADVISORY",
    "recognitionRow": "native-evidence sec.1.2 js-synthesized: 'No tsconfig.json/jsconfig.json "
                      "at the unit root; package.json present OR ANY .js/.mjs/.cjs/.jsx file "
                      "under the unit'",
    "discoveryRule": "sec.1.4 U-1: a directory holding tsconfig.json, jsconfig.json or "
                     "package.json yields exactly one tsjs unit",
    "consequence": "under U-1 the 'or any .js file' disjunct is unreachable, because a unit "
                   "root must already carry one of the three markers and the first two are "
                   "excluded by the same row; a directory holding only .js files and no "
                   "manifest is NOT a unit and its files are grammar-only members",
    "whyAdvisory": "U-1 is the specific discovery model with the closed WorkspaceUnitV2 record "
                   "and the exactly-once FileMembershipRowV1 law, so it governs; but an "
                   "implementer reading sec.1.2 alone would mint units for bare .js "
                   "directories and change both membership and the Plan",
    "readingUsedHere": "U-1"}

V["GAP-6-native-confidence-v1-scope"] = {
    "grade": "ADVISORY",
    "statement": "native-evidence sec.4.8: native.confidence.v1 is 'declared-exact: every "
                 "admitted checked fact is 1000000 under its universe; NO VALUE BELOW 1000000 "
                 "IS PRODUCED BY A NATIVE PROVIDER'",
    "tension": "sec.4.6's own named regression case exercises a `clones` fact at "
               "confidenceMillionths 100000 against a floor of 900000, and "
               "fact.confidenceMillionths / ViewEntryV3.confidenceMillionths are per-relation "
               "fields with a 0..1000000 range that sufficiency step 3 compares for EVERY "
               "relation",
    "resolution": "the unscoped clause must be read as scoped to the types@checked method it "
                  "defines; otherwise sufficiency step 3 and its own regression case are "
                  "unreachable",
    "readingUsedHere": "types-scoped"}
