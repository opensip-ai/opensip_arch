"""Vector group E: relation-specific minimum-resolution predicates at the
syntactic, resolved and type levels, sufficiency v2 as published, the matching
repair EvidenceRequirements, the imported-observation boundary, and the
baseline-audit comparison (missing / evidence-changed / empty-result)."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import *
from model import *
from build_ts import S, V, PROJECT_ID
from build_workflow import validate, envelope, CLASS_EXIT, REQ_ID

POLDOC = loadj("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
IMPEV = loadj("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
FLAT_RUNGS = POLDOC["$defs"]["Rung"]["enum"]
EVIDREG = IMPEV.get("x-opensip-evidence-relation-registry", {})

# ---------------- the flat rung vocabulary is exactly the union of the ladders
LADDER_UNION = sorted({r for row in RELREG.values() for r in row["ladder"]})
V["SUF-0-rung-vocabulary-drift-check"] = {
    "flatRungEnum": sorted(FLAT_RUNGS),
    "unionOfTheThirteenLadders": LADDER_UNION,
    "equal": sorted(FLAT_RUNGS) == LADDER_UNION,
    "necessaryNotSufficient": "the enum is a NECESSARY condition only; membership of THIS "
                              "atom's relation's ladder is the SUFFICIENT condition and is "
                              "enforced at admission (policy resolver AND Run closure, over "
                              "both PolicyDocumentV1 and the compiled RuleProgramV1)",
    "withdrawnAbstractTierVocabulary": ["syntax", "resolved", "type", "external"],
    "withdrawnGlobalRankTable": "{syntax:0, resolved:1, type:2, external:1}",
    "whyWithdrawn": "the abstract tiers shared ZERO members with the fifteen rung names, and a "
                    "per-relation mapping is a partial lossy renaming that cannot survive the "
                    "inherited C-1 per-relation ordering law",
    "evidenceRelations": sorted(EVIDREG.get("relations", {})) if EVIDREG else
                         ["runtime-observation", "history-change"],
    "evidenceRelationLadder": "[observed] - one rung, no NEW rung token"}


def admit_atom(relation, min_resolution):
    """Vocabulary admission: the rung must be on THIS relation's own ladder."""
    if relation in RELREG:
        ladder = RELREG[relation]["ladder"]
        kind = "native-fact-relation"
    elif relation in ("runtime-observation", "history-change"):
        ladder = ["observed"]
        kind = "imported-evidence-relation"
    else:
        raise Refuse("ATOM_RELATION_UNREGISTERED", relation)
    if min_resolution not in FLAT_RUNGS:
        raise Refuse("ATOM_RUNG_OUTSIDE_FLAT_VOCABULARY", min_resolution)
    if min_resolution not in ladder:
        raise Refuse("ATOM_RUNG_NOT_ON_THIS_RELATIONS_LADDER",
                     f"{relation}@{min_resolution}")
    return {"kind": kind, "ladder": ladder, "index": ladder.index(min_resolution)}


def rung_satisfies(relation, fact_rung, min_resolution):
    """Ladder-INDEX comparison inside ONE relation. Nothing orders a rung of one
    relation against a rung of another: that is a refusal, never true or false."""
    a = admit_atom(relation, min_resolution)
    if fact_rung not in a["ladder"]:
        raise Refuse("CROSS_RELATION_RUNG_COMPARISON", f"{relation}:{fact_rung}")
    return a["ladder"].index(fact_rung) >= a["index"]


PRED = {}
# --- SYNTACTIC level -------------------------------------------------------
PRED["E1-syntactic-qualifying"] = {
    "atom": {"op": "exists", "relation": "declares", "minResolution": "syntactic"},
    "admittedFactRung": "syntactic",
    "ladder": RELREG["declares"]["ladder"],
    "rungIndexComparisonSatisfied": rung_satisfies("declares", "syntactic", "syntactic"),
    "coverage": "complete", "verdict": "predicate TRUE on a matching fact"}
PRED["E2-syntactic-insufficient-imports-at-the-WEAKER-rung"] = {
    "atom": {"op": "exists", "relation": "imports", "minResolution": "resolved-target"},
    "admittedFactRung": "syntactic-specifier",
    "ladder": RELREG["imports"]["ladder"],
    "rungIndexComparisonSatisfied": rung_satisfies("imports", "syntactic-specifier", "resolved-target"),
    "sufficiencyStep": "2 - rung below minResolution -> the rung-unavailable cause "
                       "(language-tier-unsupported / provider-unavailable / "
                       "input-closure-incomplete / budget-exhausted) else required-relation-missing"}
# --- RESOLVED level --------------------------------------------------------
PRED["E3-resolved-qualifying"] = {
    "atom": {"op": "none", "relation": "references", "minResolution": "resolved-binding"},
    "admittedFactRung": "resolved-binding",
    "ladder": RELREG["references"]["ladder"],
    "rungIndexComparisonSatisfied": rung_satisfies("references", "resolved-binding", "resolved-binding"),
    "requirementV2": {"quantifier": "universal-negative", "completeness": "complete",
                      "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid"},
    "resolutionCompleteness": {"state": "complete", "attempted": True,
                               "examinedExhaustive": True, "stageTerminal": "complete",
                               "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
    "closedWorld": {"exportsClosed": "closed", "entryPointsRecognized": "all",
                    "nonliteralLoading": "none", "externalConsumers": "none-declared"},
    "verdict": "satisfied=true with NO deficiency - the ONLY shape under which an "
               "authoritative no-consumer claim is eligible (native sec.4.7)"}
PRED["E4-resolved-insufficient-one-dynamic-edge"] = {
    "atom": {"op": "none", "relation": "references", "minResolution": "resolved-binding"},
    "admittedFactRung": "resolved-binding",
    "rungIndexComparisonSatisfied": rung_satisfies("references", "resolved-binding", "resolved-binding"),
    "coverage": "complete",
    "resolutionCompleteness": {"state": "incomplete", "attempted": True,
                               "examinedExhaustive": True, "stageTerminal": "complete",
                               "unresolvedEdgeCount": 1,
                               "unresolvedEdgeClasses": ["computed-member-access"]},
    "sufficiencyStep": "6 - universal-negative, state incomplete, unresolvedEdgePolicy forbid "
                       "-> resolution-incomplete",
    "deficiency": "resolution-incomplete", "nativeCause": None,
    "causeCarrier": "entry.resolutionCompleteness (state + unresolvedEdgeClasses); "
                    "nativeCause is null BY DESIGN and admission refuses unless the named "
                    "field actually carries the cause",
    "note": "RC-3: coverage complete WITH state incomplete is a valid honest entry that owes "
            "no deficiency; the deficiency here is the SUFFICIENCY evaluation's against a "
            "RequirementV2, not something re-derived from the entry alone",
    "verdict": "predicate INDETERMINATE (strong Kleene); the seal is indeterminate, "
               "never an authoritative no-match"}
PRED["E5-resolved-insufficient-partial-stage"] = {
    "atom": {"op": "none", "relation": "calls", "minResolution": "resolved-callee"},
    "admittedFactRung": "resolved-callee",
    "rungIndexComparisonSatisfied": rung_satisfies("calls", "resolved-callee", "resolved-callee"),
    "resolutionCompleteness": {"state": "partial", "attempted": True,
                               "examinedExhaustive": True, "stageTerminal": "budget-exhausted",
                               "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
    "sufficiencyStep": "6 - state partial -> resolution-incomplete REGARDLESS of policy",
    "zeroEdgeCountNeverImpliesComplete": True,
    "budgetCarrier": "entry.resolutionCompleteness.stageTerminal = budget-exhausted",
    "d9": "indeterminate (3) / COVERAGE.BUDGET_EXHAUSTED"}
# --- TYPE level ------------------------------------------------------------
PRED["E6-type-qualifying-declared"] = {
    "atom": {"op": "exists", "relation": "types", "minResolution": "checked"},
    "admittedFactRung": "checked", "ladder": RELREG["types"]["ladder"],
    "rungIndexComparisonSatisfied": rung_satisfies("types", "checked", "checked"),
    "derivationKinds": ["annotated"],
    "requirementV2": {"derivationPolicy": "declared-only"},
    "verdict": "satisfied - no compiler-inferred derivation in the view"}
PRED["E7-type-insufficient-declared-only-vs-compiler-inferred"] = {
    "atom": {"op": "exists", "relation": "types", "minResolution": "checked"},
    "admittedFactRung": "checked",
    "rungIndexComparisonSatisfied": rung_satisfies("types", "checked", "checked"),
    "derivationKinds": ["compiler-inferred"],
    "requirementV2": {"derivationPolicy": "declared-only"},
    "sufficiencyStep": "4 - relation types with declared-only and a compiler-inferred "
                       "derivation in the view -> derivation-policy-unmet",
    "deficiency": "derivation-policy-unmet", "nativeCause": None,
    "causeCarrier": "relation MUST be `types` AND entry.derivationKinds must contain "
                    "compiler-inferred; a `references` entry carrying the same array value "
                    "is refused by the registry row's owning `relations` list",
    "notAProbability": "TypeDerivationV1 is confidenceMillionths 1000000 under "
                       "native.confidence.v1; the withdrawn 900000 cap had no evidence rationale"}
PRED["E8-type-insufficient-below-the-rung"] = {
    "atom": {"op": "exists", "relation": "types", "minResolution": "checked"},
    "admittedFactRung": "annotated",
    "rungIndexComparisonSatisfied": rung_satisfies("types", "annotated", "checked"),
    "ladderIndices": {"annotated": 0, "checked": 1}}
V["SUF-1-relation-specific-minimum-resolution-predicates"] = PRED

# --- cross-relation comparison is a REFUSAL, never a truth value ------------
SN = {}


def sn(name, fn):
    try:
        r = fn()
        SN[name] = f"NOT-REFUSED (defect): returned {r!r}"
    except Refuse as e:
        SN[name] = str(e)


sn("SUF-N1-declares-atom-naming-a-rung-of-calls",
   lambda: admit_atom("declares", "resolved-callee"))
sn("SUF-N2-file-atom-naming-the-syntactic-rung",
   lambda: admit_atom("file", "syntactic"))
sn("SUF-N3-comparing-a-calls-fact-rung-under-a-references-atom",
   lambda: rung_satisfies("references", "resolved-callee", "resolved-binding"))
sn("SUF-N4-atom-over-an-unregistered-relation",
   lambda: admit_atom("python-imports", "syntactic"))
sn("SUF-N5-atom-rung-outside-the-flat-vocabulary",
   lambda: admit_atom("references", "resolved"))
sn("SUF-N6-evidence-relation-atom-naming-a-native-rung",
   lambda: admit_atom("runtime-observation", "resolved-binding"))
V["SUF-NEGATIVES"] = SN

# --- confidence floor precedes the one-rung existential shortcut ------------
def sufficiency_v2(req, view_entry, view_has_relation=True, affected=False,
                   exported=False):
    """The published order, with NO early exit."""
    causes = []
    if not view_has_relation:
        return {"satisfied": False, "deficiency": "required-relation-missing", "step": 1}
    if not rung_satisfies(req["relation"], view_entry["resolution"], req["minResolution"]):
        return {"satisfied": False,
                "deficiency": view_entry.get("deficiency") or "required-relation-missing",
                "step": 2}
    if view_entry["confidenceMillionths"] < req.get("minConfidenceMillionths", 0):
        causes.append(("confidence-floor-unmet", 3))
    if (req["relation"] == "types" and req.get("derivationPolicy") == "declared-only"
            and "compiler-inferred" in view_entry.get("derivationKinds", [])):
        causes.append(("derivation-policy-unmet", 4))
    if req["completeness"] == "complete" and view_entry["coverage"] != "complete":
        causes.append((view_entry.get("deficiency"), 5))
    if req["quantifier"] == "universal-negative":
        st = view_entry["resolutionCompleteness"]["state"]
        if st in ("partial", "not-attempted"):
            causes.append(("resolution-incomplete", 6))
        elif st == "incomplete" or affected:
            if req["unresolvedEdgePolicy"] == "forbid":
                causes.append(("resolution-incomplete", 6))
        if exported and view_entry["closedWorld"]["exportsClosed"] != "closed":
            if req["externalConsumerPolicy"] == "forbid":
                causes.append(("external-consumers-unknown", 7))
    if not causes:
        return {"satisfied": True, "deficiency": None, "step": None}
    PREC = ["language-tier-unsupported", "provider-unavailable", "input-closure-incomplete",
            "budget-exhausted", "confidence-floor-unmet", "derivation-policy-unmet",
            "resolution-incomplete", "external-consumers-unknown", "required-relation-missing"]
    causes = [c for c in causes if c[0]]
    best = min(causes, key=lambda c: PREC.index(c[0]))
    return {"satisfied": False, "deficiency": best[0], "step": best[1],
            "allApplicable": [c[0] for c in causes]}


_ONE_RUNG = {"relation": "clones", "minResolution": "normalized-body-hash",
             "completeness": "partial-ok", "quantifier": "existential",
             "minConfidenceMillionths": 900000, "unresolvedEdgePolicy": "disclose",
             "externalConsumerPolicy": "assume-closed"}
_E_LOW = {"relation": "clones", "resolution": "normalized-body-hash", "coverage": "complete",
          "confidenceMillionths": 100000, "derivationKinds": [],
          "resolutionCompleteness": {"state": "not-applicable"},
          "closedWorld": {"exportsClosed": "closed"}, "deficiency": None}
_E_HIGH = dict(_E_LOW, confidenceMillionths=1000000)
V["SUF-2-no-early-exit-the-confidence-floor-precedes-the-one-rung-shortcut"] = {
    "requirement": _ONE_RUNG,
    "atConfidence100000": sufficiency_v2(_ONE_RUNG, _E_LOW),
    "atConfidence1000000": sufficiency_v2(_ONE_RUNG, _E_HIGH),
    "law": "the former step-9 'satisfied outright' shortcut returned BEFORE the confidence "
           "floor and let 100000 pass a floor of 900000; it was removed (post-reset SHOULD-4)"}

V["SUF-3-advisory-postures-refuse-in-an-authoritative-control-rule"] = {
    "authoritativeNoConsumerRequirement": {"quantifier": "universal-negative",
                                           "completeness": "complete",
                                           "unresolvedEdgePolicy": "forbid",
                                           "externalConsumerPolicy": "forbid"},
    "advisoryPostures": ["disclose", "assume-closed"],
    "refusalAtPackAdmission": "advisory-posture-in-control-rule",
    "universalNegativeRequiresCompleteness": "quantifier=universal-negative requires "
                                             "completeness=complete",
    "whichPredicatesMustUseIt": ["a repair prerequisite", "no-consumer", "cold-code",
                                 "unreachable", "any predicate whose truth is a negative "
                                 "over consumers"]}

# --------------------------- repair evidence requirements + imported boundary
REQS = [
    {"relation": "references", "minResolution": "resolved-binding",
     "completeness": "complete", "satisfied": True},
    {"relation": "reachability", "minResolution": "from-resolved-calls",
     "completeness": "complete", "satisfied": False,
     "deficiency": "resolution-incomplete"},
    {"relation": "types", "minResolution": "checked",
     "completeness": "partial-acceptable", "satisfied": True}]
V["SUF-4-repair-evidence-requirements-and-the-imported-observation-boundary"] = {
    "requirements": REQS,
    "eachAdmittedAgainstItsOwnRelationsLadder": {
        f'{r["relation"]}@{r["minResolution"]}': admit_atom(r["relation"], r["minResolution"])["index"]
        for r in REQS},
    "schemaErrors": {f'{r["relation"]}@{r["minResolution"]}':
                     validate("urn:opensip:product-v1:workflows:repair",
                              "#/$defs/EvidenceRequirement", r) for r in REQS},
    "planApplicable": all(r["satisfied"] for r in REQS),
    "unsafeActionSet": ["delete", "replace"],
    "gate": "REPAIR.CLOSED_WORLD_NOT_ESTABLISHED when deadCodeRepairEligible is false, with "
            "the evidence record's own `reasons` in the remedy",
    "authorityBoundary": "preview ADMITS the requirement's relation/minResolution (vocabulary "
                         "admission) and CONSUMES its own `satisfied` value; the semantic "
                         "sufficiency behind it is native sufficiency_v2's and the sec.4.5 "
                         "affected-target evidence, PER REQUIREMENT, never collapsed into "
                         "one flag",
    "importedObservationBoundary": {
        "runtimeSubjectStates": ["observed-hit", "observable-unhit", "unobservable", "unmapped"],
        "observableUnhitIsNotUnused": True,
        "unobservableAndUnmappedNeverBecomeUnhitSignals": True,
        "oneWindowIsNeverUniversalNonUse": True,
        "runtimeCoverageIsNeverOpenSIPCoverage": True,
        "anImportedPreparedDeclaredOriginCannotAuthorizeAnUnsafeRepair": True,
        "anAdvisorySimilarityOrRuntimeColdSignalAloneNeverAuthorizesDeletion": True,
        "correspondenceIsMandatory": "exact-snapshot naming an admitted snapshot2, or "
                                     "vcs-revision through an admitted SourceMappingV1 whose "
                                     "EVERY sourceSha256 equals the snapshot inventory digest; "
                                     "a clean commit name alone or a declared build string "
                                     "alone is UNMAPPED (IMPORT.SOURCE_MAPPING_REQUIRED) and "
                                     "never feeds a predicate"}}

# ============================================ comparison: the three audit shapes
def cmp_entry(fp, rule, cls, live, gates, reason=None, subseq=None):
    e = {"fingerprint": fp, "ruleId": rule, "detectorId": "det.core",
         "presence": {"B": True, "E0": True, "E1": True, "E2": True, "E3": True, "E4": True},
         "classification": cls, "subsequentDeltas": subseq or [],
         "liveInCurrent": live, "gates": gates}
    if reason:
        e["indeterminateReason"] = reason
    if gates:
        e["gateReason"] = ("code-net-new" if cls == "CODE-NET-NEW"
                           else "indeterminate-gating-rule")
    return e


PP = loadj("docs/coop/design-corrections/workflows/schemas/comparison-result.schema.json")
PIVOT_KEYS = sorted(PP["$defs"]["PivotPresence"]["properties"])
AUD = {}
AUD["A1-missing-required-detector-pivot"] = {
    "situation": "the baseline detector closure is not installed and is not declared "
                 "compatible, so E0 cannot be computed",
    "entry": cmp_entry("fp-1", "r.dead-code", "INDETERMINATE", True, True,
                       "pivot-detector-unavailable"),
    "verdict": "indeterminate", "d9": "indeterminate (3) / BASELINE.RECIPE_UNSUPPORTED",
    "detail": "BASELINE.PIVOT_DETECTOR_UNAVAILABLE",
    "law": "E0 must NEVER be substituted with B; a revoked closure is never executed whatever "
           "bytes are present"}
AUD["A2-evidence-changed-on-a-gating-rule"] = {
    "situation": "the bound import2 identity for the required runtime evidence differs "
                 "between sides and the rule gates on either side",
    "entry": cmp_entry("fp-2", "r.cold-code", "INDETERMINATE", True, True,
                       "evidence-availability-changed"),
    "verdict": "indeterminate",
    "law": "only for a NON-gating rule may a presence change be EVIDENCE-DELTA; required "
           "evidence loss can never disappear as a non-gating delta. Replacing an artifact "
           "with another of the same kind is still an evidence change "
           "(evidence-content-changed): the axis compares exact bound import2 IDENTITIES, "
           "not kind presence.",
    "conservativeByDesign": "there is NO counterfactual pivot that replays old source under a "
                            "new runtime/test observation, so a changed import identity can "
                            "make an evidence-dependent comparison indeterminate even under "
                            "full-current"}
AUD["A3-empty-result-on-both-sides-still-indeterminate"] = {
    "situation": "both observed finding sets are EMPTY, but a required E1-E3 re-evaluation "
                 "was not bound and an enabled rule gates under the selected profile",
    "entryCount": 0,
    "verdict": "indeterminate",
    "law": "workflows sec.12: missing evaluation can hide a finding that appears in NEITHER "
           "set, so entry counts cannot prove its absence. Rule deficiencies are enumerated "
           "INDEPENDENTLY of findings and zero emitted findings never establish complete "
           "analysis.",
    "hostObligation": "the host MUST compute and bind every E1-E3 re-evaluation a changed axis "
                      "requires; those are required workflow steps, not caller options, and a "
                      "host failure to execute a computable step is an OPERATIONAL failure, "
                      "not typed comparison indeterminacy",
    "typedIndeterminacyIsReservedFor": "unavailable required inputs or unsupported admitted "
                                       "recipes, with the missing input named"}
AUD["A4-code-net-new-hidden-by-a-same-change-policy-edit"] = {
    "entry": cmp_entry("fp-3", "r.new-bug", "CODE-NET-NEW", False, True, None, ["policy"]),
    "gateReasonUnderBaselineOrCurrent": "code-net-new-policy-hidden",
    "law": "a new bug introduced and simultaneously hidden by disabling the rule is "
           "CODE-NET-NEW with subsequentDeltas [policy] and STILL gates"}
AUD["A5-detector-removed"] = {
    "law": "removed detectors require the actual current-trusted prior detector pivot and set "
           "E1-E4 false; a new bug hidden by REMOVING its detector remains CODE-NET-NEW and "
           "can gate. Missing prior execution is indeterminate, including detector removal."}
V["CMP-1-baseline-audit-shapes"] = AUD
# the schema-VALIDATED entry objects live in CMP-4 (build_final); these rows carry
# the situation and the law, and name the validated entry there.
for _k in list(AUD):
    AUD[_k].pop("entry", None)
    AUD[_k]["validatedEntryVector"] = "CMP-4-schema-validated-comparison-entries"
V["CMP-2-audit-profiles"] = {
    "profiles": PP["$defs"]["AuditProfileName"]["enum"]
    if "AuditProfileName" in PP["$defs"] else None,
    "defaultForAudit": "code-regression",
    "verdictRule": "fail if ANY entry gates; else indeterminate if any INDETERMINATE entry "
                   "belongs to a gating rule OR a current gating rule has unsatisfied/unknown "
                   "required Coverage or evidence; else pass",
    "enumPrecedenceNeverDecidesAGate": True,
    "wholeComparisonIndeterminacy": "unmapped project, unsupported schema/recipe major or a "
                                    "context-document mismatch performs NO comparison and "
                                    "emits ZERO entries with a typed remedy",
    "fw11": "a numeric comparison needs the same metric definition, supplied diff scope and "
            "comparison base; redistribution is not behavioural improvement"}

# ------------------------------------------- purge / replay / availability
V["CMP-3-purge-replay-and-current-availability"] = {
    "sealedAssuranceIsImmutable": ["verified", "verifiable", "replayable"],
    "defaultAuthoritativeProfileRequires": "replayable retention AT SEAL",
    "currentAvailabilityIsASeparateMonotonicGenerationRecord":
        ["retained", "partial", "expired", "purged", "corrupt", "unavailable"],
    "aQueryReportsBOTH": True,
    "purgeRetains": "the minimal sealed manifest, provenance and tombstone; unshared evidence "
                    "bytes are deleted by reachability GC and shared bytes survive until the "
                    "final reference is removed. Purged is NOT deleted-history.",
    "aRetentionDecisionNeverChanges": ["fact identity", "Coverage identity", "finding identity",
                                       "Run identity", "the historical verdict"],
    "itNeverTurnsExpiredEvidenceIntoNoMatch": True,
    "queryOfARetainedManifestAfterPurge": "allowed; states evidence unavailable",
    "queryRequiringActualProofBaselineOrRepairInput": {
        "class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "exit": 2,
        "details": ["evidence.expired", "evidence.purged", "evidence.missing",
                    "evidence.corrupt"],
        "position": "BEFORE evaluation"},
    "inabilityDuringASelectedOperation": {
        "class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "exit": 4,
        "faultCause": "host-io"},
    "admittedPartialNativeInputs": {"class": "indeterminate", "exit": 3},
    "theseAreDifferentEVENTPOSITIONSNotInterchangeableSpellings": True,
    "regenerationMismatch": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
                             "faultCause": "host-io", "exit": 4,
                             "detail": "evidence.regeneration-mismatch",
                             "law": "it cannot replace the sealed Run; an expired or revoked "
                                    "permission cannot be resurrected by a matching hash"},
    "cacheKeyVsCacheHit": {
        "keyConstruction": "PURE and deterministic - exact schema admission and canonical order "
                           "over the cache-key record. It reads NO bytes and resolves NO "
                           "reference, so a host may compute it before loading anything.",
        "hitAdmission": "an entry may be consumed only against EXACTLY the closure the Run "
                        "itself requires: stage spec retained and Plan-joined, producing closure "
                        "retained and Plan-selected, every scopeIds member a retained "
                        "subject-scope of this snapshot, the output schema document retained, "
                        "and every inputRefs entry resolved through the same digest-domain "
                        "registry the Run uses",
        "aBareCoverageImportOrFactPayloadRefIsRefusedAsAnAuthoritativeRoot": True,
        "aHitIsReusableProducerOutputNeverEvidenceAuthority": True},
    "durabilityUndetermined": {"class": "operational-failed", "exit": 4,
                               "law": "a crash after ledger commit but before acknowledgement "
                                      "returns durability-undetermined with an ExecutionId for "
                                      "READ-ONLY recovery; recovery returns committed or failed "
                                      "and never repeats a repository mutation"}}
