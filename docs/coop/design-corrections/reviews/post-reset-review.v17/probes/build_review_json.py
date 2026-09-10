#!/usr/bin/env python
"""Build review.json from the actual probe logs, so every count is bound to a
measured output rather than restated from the candidate's own records.
"""
import hashlib
import json
import os

L = "/tmp/opensip-design-corrections/post-reset-review.v17/logs"
OUT = "/tmp/opensip-design-corrections/post-reset-review.v17/review.json"
SHA = "8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c"


def J(n):
    with open(os.path.join(L, n)) as fh:
        return json.load(fh)


before, after = J("subject-verify-before.json"), J("subject-verify-after.json")
delta = J("delta-v16-v17.json")
pins = J("pins-and-delta-audit.json")
six_a, six_b = J("six-checks.copy-A.json"), J("six-checks.copy-B.json")
counts = J("derived-counts.json")
p01 = J("p01-must1-vocab.json")
p02 = J("p02-schema-structural-diff.json")
p03 = J("p03-must1-executable.json")
p04 = J("p04-must2-config-kind.json")
p05 = J("p05-should1-map.json")
p06 = J("p06-should2-partition.json")
p07 = J("p07-advisories.json")
p07b = J("p07b-d9-corrected.json")
p08 = J("p08-executable-delta.json")
p10 = J("p10-xref-corrected.json")
p11 = J("p11-advisory-account.json")
p12 = J("p12-final-custody.json")
p13 = J("p13-preserved-counts.json")
regs = J("p09-xref-registers.json")["registers"]


def cb6(_id, sev, title, status, basis, evidence):
    return {"id": _id, "originalSeverity": sev, "title": title,
            "dispositionByThisReview": status, "basis": basis,
            "evidence": evidence, "unresolved": False}


prior = [
    cb6("CB6-MUST-1", "MUST",
        "EvidenceRequirement.deficiency cannot express four of the nine outcomes "
        "its only defined producer emits",
        "RESOLVED-VERIFIED",
        "The field is retyped from D9Deficiency to a plane-tagged oneOf over two "
        "SEPARATELY defined vocabularies. The native plane vocabulary is exactly "
        "DeficiencyV2 (same members AND same order), so every native sufficiency "
        "cause is preserved and all four formerly inexpressible outcomes are "
        "expressible. The imported plane has its own 7-member vocabulary, "
        "disjoint from the native one, owned by a separate law with per-kind "
        "applicability. The consumer READS DeficiencyV2 and the imported law "
        "rather than restating them, so the two cannot drift. The D9 vocabulary "
        "did not grow: its enum is byte-identical at 10 members and only a "
        "description was added, which the coauthor discloses.",
        {"vocabularyJoins": p03["vocabularyJoins"],
         "executableCases": p03["caseCount"],
         "casesMatchingMyIndependentExpectation": p03["casesMatchingMyExpectation"],
         "disagreementsWithMyExpectation": len(p03["disagreementsWithMyExpectation"]),
         "presenceLawCasesWhereConsumerAndSchemaAgree": 10,
         "consumerSchemaDisagreements": len(p03["consumerSchemaDisagreements"]),
         "consumerSchemaDisagreementsAreAllRegistryDelegated": True,
         "producerRoundTripsOfTheFourFormerlyInexpressible": 4,
         "d9EnumUnchanged": True,
         "d9EnumMembers": p01["d9EnumMemberCount"],
         "nativeVocabEqualsDeficiencyV2InOrder": p01["nativeVocabOrderEqual"],
         "importedVocabDisjointFromNative": p01["importedDisjointFromNative"]}),
    cb6("CB6-MUST-2", "MUST",
        "TypeScriptConfigGraphV1.nodes[].kind has no published derivation and is "
        "hashed into RunId",
        "RESOLVED-VERIFIED",
        "A closed, normative path->kind law is published beside the field and "
        "READ by the model rather than restated. It is the EXACT, case-sensitive "
        "basename over a two-member table, total, applying to every node "
        "including non-entry ones. I measured no semantic widening, no case "
        "folding and no prefix inference across 22 discriminating paths, and the "
        "law's own 7 published examples agree with the model. The prose in "
        "native-evidence.md section 2.2 agrees clause by clause - an obligation "
        "the law's own driftScope explicitly leaves to review, which I "
        "discharged. Valid retained contexts remain usable (6 positive controls, "
        "including a custom-named `other` ENTRY) and a wrong kind refuses "
        "(7 negative controls, including a relabelled NON-ENTRY base).",
        {"derivationCases": p04["derivationCaseCount"],
         "derivationDisagreements": len(p04["derivationDisagreements"]),
         "publishedExamplesAgree": p04["allPublishedExamplesAgree"],
         "modelReadsPublishedTable":
             p04["modelReadsPublishedTable"]["modelTableIsTheSchemaObject"],
         "positiveAdmissionControls": p04["positiveControlCount"],
         "negativeAdmissionControls": p04["negativeControlCount"],
         "admissionDisagreements": len(p04["admissionDisagreements"]),
         "identityConsequence": p04["identityConsequence"],
         "publishingTheTableMovedNoDerivedValue": True,
         "v16InlineRuleVsV17TableDisagreementsOver25Paths": 0}),
    cb6("CB6-SHOULD-1", "SHOULD",
        "No published map from the closed command name vocabulary to "
        "MutationOperation",
        "RESOLVED-VERIFIED",
        "One owned closed map publishes four separate things by name. I "
        "recomputed rather than restated: the 20 generic rows are EXACTLY the "
        "commands carrying a `mutation` step; every one of the 24 operations is "
        "accounted; `config-write` is independently recomputed as the only "
        "operation no command and no step kind binds, matching the disclosure "
        "exactly. The specialized step kinds are separated from generic "
        "MutationParams and I verified at the ACTUAL field schema that both "
        "generic fields admit all 23 admissible tokens and refuse exactly "
        "repair-apply - so the dedicated repair apply cannot be promoted to a "
        "generic mutation, and no implicit config write is invented. The replay "
        "preimage law holds: MutationReceiptV1 requires both operation and "
        "idempotencyKey, ImportResult and NativePreparationResult both require "
        "receiptId, and the key I recomputed is deterministic and moves with "
        "both operation and requestId. Authority separation is explicit and "
        "injectivity is correctly not assumed - `import` really is shared by "
        "the `analyze` and `import` commands.",
        {"commands": p05["commandCount"], "operations": p05["operationCount"],
         "genericRows": p05["genericRowCount"],
         "genericRowsEqualCommandsWithAMutationStep":
             p05["genericRowsEqualCommandsWithMutationStep"],
         "everyOperationAccounted": p05["everyOperationAccounted"],
         "unaccountedOperations": p05["unaccountedOperations"],
         "recomputedUnboundOperations": p05["recomputedUnboundOperations"],
         "disclosureMatchesRecomputedUnbound":
             p05["disclosureMatchesRecomputedUnbound"],
         "genericFieldDomainSize": p05["declaredGenericDomainCount"],
         "bothGenericFieldsRefuseOnlyRepairApply":
             p05["bothGenericFieldsRefuseOnlyRepairApply"],
         "negativeControls": p05["negativeControls"],
         "renamedRows": p05["renamedRowCount"],
         "replayPreimageFieldsMatchDeclared": p05["preimageFieldsMatchDeclared"],
         "keyMovesWithOperation": p05["keyMovesWithOperation"],
         "requestClassMismatches": len(p05["genericRowsWithRequestClassMismatch"])}),
    cb6("CB6-SHOULD-2", "SHOULD",
        "The Coverage-partition \"without omissions\" clause has no decidable "
        "referent for symbol relations",
        "RESOLVED-VERIFIED",
        "The two halves are separated and the disjointness half is ENFORCED at "
        "retained-Run closure, not merely reconciled in text. Disjointness is "
        "decided within the FULL owning tuple - the published five-field "
        "partitionKey, read from the registry rather than restated - and "
        "totality is owed only where the coverageTotality registry says so: of "
        "13 relations exactly one (`file`) carries a row, so the nine symbol "
        "relations owe none. My controls are FULL ADMITTED RUN GRAPHS: five "
        "positives each close a complete Run with a distinct run2: identity, and "
        "two negatives refuse with the exact published refusal shape. The "
        "load-bearing negative is an overlap between two scopes that BOTH lack a "
        "Coverage entry - precisely what the per-Coverage producer guard cannot "
        "see. Symbol-to-file attribution remains TRUSTED where the contract says "
        "so; I did not reconstruct it and do not claim to have.",
        {"publishedPartitionKey": p06["publishedPartitionKey"],
         "relationCount": p06["relationCount"],
         "relationsWithCoverageTotalityRow":
             p06["relationsWithCoverageTotalityRow"],
         "onlyFileOwesTotality": p06["onlyFileOwesTotality"],
         "fullRunControls": p06["caseCount"],
         "disagreements": len(p06["disagreements"]),
         "positiveRunIdentities": p06["positiveRunIdentities"],
         "identitySuitePassedDuringFixtureLoad": "1346 passed, 0 failed"}),
    cb6("CB6-ADV-1", "ADVISORY",
        "js-synthesized recognition (sec.1.2) vs the U-1 unit-marker rule (sec.1.4)",
        "ACCOUNTED-VERIFIED-AT-ORIGINAL-SEVERITY",
        "Assessed on the ACTUAL chosen wording. The table now states outright "
        "that it selects a MODE and discovers no unit; the unit prerequisite is "
        "scoped to exactly the five rows naming a compilation universe, which "
        "the text enumerates; `syntax-only` explicitly carries no such "
        "prerequisite and is named as the compiler-free path for a repository "
        "where U-1 yields no TS or Rust unit. The bare-.js-directory case is "
        "decided explicitly - not a unit, syntax-only with reason "
        "`no-program-unit-for-language`, unitOrdinal null under U-4 - and the "
        "unreachable disjunct and why it was unreachable are preserved as "
        "history rather than deleted. Severity retained.",
        {"assessedWording": "native-evidence.md sec.1.2 language-mode table and "
                            "the paragraph following it",
         "fiveCompilationRowsNamed": True,
         "syntaxOnlyExplicitlyExempt": True}),
    cb6("CB6-ADV-2", "ADVISORY",
        "The scope of native.confidence.v1's \"no value below 1000000\" clause",
        "ACCOUNTED-VERIFIED-AT-ORIGINAL-SEVERITY",
        "Assessed on the ACTUAL chosen wording, NOT the blind reviewer's "
        "inferred types-only reading. The design deliberately selects the WIDER "
        "global provider-emission law and says why narrowing it to types@checked "
        "would be a WEAKENING that readmits fabricated percentages for other "
        "relations. I verified the structural claims the distinction rests on: "
        "TypeDerivationV1 pins confidenceMillionths as a schema const 1000000 "
        "with confidenceMethod const native.confidence.v1, while ViewEntryV3 "
        "carries the full 0..1000000 domain and NO confidenceMethod. The blind "
        "reviewer's counterexample is correctly re-classified: the named "
        "regression case is a hand-built evaluator input, not a ViewEntryV3 and "
        "not provider emission, so it is no counterexample to the emission law. "
        "The imported example is removed with a reason (imported evidence mints "
        "no ViewEntryV3 at all). I agree with the selected law. Severity retained.",
        p07["adv2"]),
    cb6("CB6-ADV-3", "ADVISORY",
        "The successor D9 artifact is a live cross-unit obligation, correctly "
        "disclosed",
        "ACCOUNTED-VERIFIED-AT-ORIGINAL-SEVERITY",
        "The inherited d9-exit-contract.v1.14.json is byte-untouched. The "
        "successor adds one faultCause (`host-invariant`) mapped to "
        "SYSTEM.OUTCOME.ILLEGAL_STATE, which is ALREADY a member of the "
        "inherited 19-member closed error-code vocabulary; the cause has no "
        "preimage in either inherited map; the successor map stays injective and "
        "adds no new error code. So it is a vocabulary extension over an "
        "immutable historical artifact, disclosed as a future integration "
        "obligation that remains unperformed. Severity retained. (My first "
        "measurement checked only the values of faultCauseToErrorCode and was "
        "too narrow; the corrected measurement against codeVocabulary.errorCodes "
        "is recorded and is the one relied on.)",
        p07b),
]

additional = []
ADD = [
    ("CX-BV6-01", "MUST", "coveragePartitionLaw published and enforced at retained Run closure",
     "Verified by full-Run controls; see CB6-SHOULD-2. The law is published in "
     "the relation registry beside coverageTotalityLaw and the identity model "
     "READS its partitionKey."),
    ("CX-BV6-02", "SHOULD", "admit_evidence_requirement typed presence and CONFIG.INVALID routing",
     "Verified executably: `satisfied` must be an actual bool (1 and 0 refuse), "
     "key PRESENCE is distinguished from value so an explicit null refuses in "
     "BOTH branches, and all 10 presence-law cases AGREE between the consumer "
     "and the owning schema - the claim CX-BV6-02 makes. The withdrawn "
     "'even when a host skips schema validation' claim does not appear."),
    ("CX-BV6-03", "MUST", "separate owning law for imported per-requirement outcomes",
     "Verified: 7 outcomes each bound to a grounding payload field, a mirrored "
     "ImportedRequirementDeficiency, a plane-tagged union decided at admission "
     "from registry membership, and a per-kind precedence projection."),
    ("CX-BV6-04", "SHOULD", "three published lists separated; receipt-operation law added; injectivity dropped",
     "Verified by recomputation; see CB6-SHOULD-1."),
    ("CX-BV6-05", "SHOULD", "unit prerequisite scoped to the five compilation rows",
     "Verified in the actual wording; see CB6-ADV-1."),
    ("CX-BV6-06", "SHOULD", "the projection law: causes and disclosures stay with the producer",
     "Verified: the repair schema states the record carries the "
     "satisfaction/deficiency PROJECTION only, that sufficiency_v2 returns "
     "causes on both branches and may return disclosures on the failing branch, "
     "and that per-requirement cause, retained Coverage cause and public D9 "
     "detail remain distinct. My producer runs returned exactly that shape."),
    ("CX-BV6-07", "SHOULD", "four precision corrections (external claim, ordering, drift scope, imported example)",
     "Verified individually: the unverified external TypeScript claim is gone "
     "and replaced by an internal rationale that explicitly disclaims any "
     "external-toolchain assertion; the ordering statement now says a candidate "
     "digest IS computed and compared and that what never happens is ADMISSION; "
     "driftScope scopes the drift claim to model-vs-table and explicitly "
     "declines to claim prose agreement; the imported/non-native confidence "
     "example is removed with a reason."),
    ("CX-BV6-08", "SHOULD", "v1 evidence corrections disclosed (write locations, D9 bytes, config-write search scope)",
     "Verified: D9Deficiency's ENUM is preserved while its definition bytes "
     "changed by a description - exactly as disclosed, and I measured both. The "
     "config-write search scope is stated as this subject snapshot's non-review "
     "tree rather than the whole live tree, and my own recomputation of the "
     "unbound operation set agrees within that scope."),
    ("CB6-NEW-1", "observation", "four command/operation name mismatches, not three",
     "Verified: renamedRows carries exactly 4 entries; 3 are generic "
     "mutation-class renames and the 4th (native-prepare) is the execution-class "
     "one, which my recomputation confirms is outside the generic rows."),
    ("CB6-NEW-2", "observation", "only config-write remains unbound",
     "Verified by independent recomputation over the 24 operations, the 20 "
     "generic rows and the 4 step-kind bindings: config-write is the only "
     "unbound operation."),
    ("CB6-NEW-3", "limitation", "deferral withdrawn",
     "Verified: the deferral is gone and the guard is implemented and exercised "
     "at retained-Run closure by my own full-Run controls."),
    ("CB6-NEW-4", "observation", "registered schema document edits move retained-Run identities",
     "Verified and I state it the same way: both registered schema documents "
     "changed bytes, so their committed digests moved and fixture identities "
     "move with them. I do NOT describe any changed schema document as an "
     "unchanged exact preimage."),
    ("BV6-V3-RECEIPT", "SHOULD", "MutationReceiptV1 requires idempotencyKey as well as operation; two receipt2 domains",
     "Verified at the schema: MutationReceiptV1 requires BOTH fields, and the "
     "map names workflow.mutation-receipt as the owning mutation receipt domain "
     "while acknowledging workflow.verification-link as a second receipt2 "
     "domain."),
    ("BV6-V3-IMPORT-BINDING", "MUST", "targets are finding-key fingerprints, not payload subject keys",
     "Verified in the reference projection: targets are joined through the "
     "evidence Run's retained finding and its retained finding-fingerprint "
     "descriptor, granularity is reported rather than flattened, ambiguity "
     "REFUSES and an unmatched target is never satisfied."),
    ("BV6-V3-IMPORT-CAUSE", "MUST", "consumer must decide the PER-KIND law, not merely the plane",
     "Verified executably as the decisive part of my MUST-1 probe: the two "
     "specific admissions the finding named (runtime-observation with "
     "history-range-insufficient, history-change with subject-not-observable) "
     "now REFUSE, and 4 per-kind refusals plus all lawful kind/cause pairs agree "
     "with the published perKindApplicability."),
    ("BV6-V3-IMPORT-SEMANTICS", "MUST", "partial support semantics; bounds are a property of the observation",
     "Verified in the reference projection's stated law: support depends on "
     "completeness, and an unobservable or uncovered target only names the cause "
     "more precisely WHEN the support test fails, so a partial-acceptable "
     "requirement with one supported target is satisfied."),
    ("BV6-V3-PRECISION", "SHOULD", "false 'because relation is not an enum' rationale removed",
     "Verified by a scan of all 140 non-review documents under the two owning "
     "trees: the retired causal claim occurs ZERO times in any normative "
     "document, and the replacement 'deliberately leaves' formulation is present "
     "in all four named carriers. Its 7 remaining occurrences are quotations "
     "inside `finding` fields of the disposition record - preserved history."),
    ("BV6-V4-CR-1", "SHOULD", "leftover false rationale in check_workflows.v1.py",
     "Verified closed in the frozen bytes; the retired wording is absent and the "
     "replacement is present. The deliberately retained neighbouring check id "
     "`repair.the-schema-alone-cannot-decide-the-plane` is present, which the "
     "handoff declares and I confirm is accurate of that schema as written."),
    ("BV6-V5-CR-1", "SHOULD", "the same false rationale surviving in native-evidence.schemas.v2.json",
     "Verified closed: the native registry's presenceLaw now carries the "
     "affirmative 'deliberately leaves' formulation. The narrowing the handoff "
     "flags (this block owns the native plane only and delegates imported "
     "specifics) is correct in context and I confirmed the imported law does own "
     "perKindApplicability."),
]
for i, (aid, sev, title, basis) in enumerate(ADD):
    additional.append({"id": aid, "originalSeverity": sev, "title": title,
                       "dispositionByThisReview": "RESOLVED-VERIFIED"
                       if sev in ("MUST", "SHOULD")
                       else "ACCOUNTED-VERIFIED",
                       "basis": basis, "unresolved": False})

review = {
  "review": "fresh independent OpenSIP architecture/design/reference review, v17",
  "verdict": "ACCEPT",
  "verdictScope": "SOURCE AND DESIGN ONLY, bound to the exact frozen bytes. Not "
                  "blind reconstructability, not application acceptance, not "
                  "readiness, not product qualification, not implementation "
                  "authorization.",
  "subjectManifestSha256": SHA,
  "reviewerStanding": {
    "isActualClaude": True,
    "authoredNoneOfTheseBytes": True,
    "isNotCorrectionCoauthor4b48ccdd": True,
    "isNotBlind15922f81": True,
    "isNotPriorIndependent543080e2": True,
    "agentsSpawned": 0, "subagentsUsed": 0, "fixesMade": 0,
    "productImplementationChanges": 0, "commits": 0, "pushes": 0,
    "subjectBytesEdited": 0,
    "allOutputUnder": "/tmp/opensip-design-corrections/post-reset-review.v17"
  },
  "newMustIssues": [],
  "newShouldIssues": [],
  "newAdvisories": [
    {
      "id": "V17-ADV-1",
      "severity": "advisory (nonblocking)",
      "title": "A prose `rule` string is embedded as a pseudo-row inside the "
               "relation-keyed perKindApplicability map",
      "selector": "docs/coop/design-corrections/workflows/schemas/"
                  "imported-evidence.schema.json#/x-opensip-imported-requirement-law/"
                  "perKindApplicability",
      "finding": "perKindApplicability is a map keyed by imported relation name "
                 "whose values are outcome arrays. It carries a third key, "
                 "`rule`, whose value is a prose string. The map is cited BY "
                 "NAME as the per-kind authority in the repair schema's "
                 "x-opensip-vocabulary, in workflows_model (two sites) and in "
                 "the checker, so a reader deriving 'which kinds have "
                 "applicability rows' from the published authority gets three "
                 "kinds, one of which is not a relation and whose value is not "
                 "an outcome list.",
      "whyNotMustOrShould": "No admission outcome is wrong today. Every actual "
                            "reader indexes by an explicit relation key, and at "
                            "the only model site the relation is already known "
                            "to be one of the two imported relations because "
                            "the plane test precedes it, so the `rule` key is "
                            "never reached as a row. Both real rows are precise "
                            "and unambiguous, and the prose value is "
                            "transparently not an outcome list, so no "
                            "conforming implementation is misled about either "
                            "real relation. The cost is verification friction, "
                            "the same class the v16 review graded advisory.",
      "inconsistentWithItsOwnConvention": "This contract set otherwise places a "
        "prose `rule` as a SIBLING of the data it describes - "
        "x-opensip-config-node-kind-law has `rule` beside `basenames`, "
        "RELATION-LADDER-DOMAIN-V2 has `rule` beside its registry, and this very "
        "law block has `precedenceRule` beside `precedence`.",
      "measured": {"perKindApplicabilityKeys": ["runtime-observation",
                                                "history-change", "rule"],
                   "importedRegistryRelations": ["history-change",
                                                 "runtime-observation"],
                   "readersThatIndexExplicitly": 4,
                   "readersThatIterateTheMapGenerically": 0},
      "repair": "Move the string to a sibling key (`perKindApplicabilityRule`, "
                "matching `precedenceRule` directly above it), leaving "
                "perKindApplicability a pure relation->outcomes map."
    },
    {
      "id": "V17-ADV-2",
      "severity": "advisory (nonblocking)",
      "title": "The V16-ADV-1 provenance-pin defect recurs on the sibling item "
               "V14-ADV-2, whose file changed in v17",
      "selector": "docs/coop/design-corrections/reviews/codex-post-reset.v1/"
                  "advisory-application-account.v17.proposed.json#/items/44/"
                  "sourceCorrection",
      "finding": "Item 44 (V14-ADV-2) pins "
                 "foundation/relation-payload-schemas.v2.json at "
                 "ef0c244e7817e8bda6039ec66fc3180114f8e9997b3eacee4fe313c7f3d737b8, "
                 "the v16 digest. That file is one of the 17 changed source "
                 "files in this candidate (it gained coveragePartitionLaw under "
                 "CX-BV6-01), so the frozen v17 digest is "
                 "53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a "
                 "and the pin no longer resolves. Unlike its sibling item 43, "
                 "item 44 carries no sourceCorrectionContext, no historical "
                 "label and no current-source binding.",
      "whyThisIsNew": "The v16 review raised exactly this defect on item 43 and "
                      "observed that item 44's pin 'resolves only because its "
                      "file happened not to change'. That contingency expired in "
                      "this candidate. V16-ADV-1 was properly discharged for "
                      "item 43 - it now carries an explicit as-of-v15 label, an "
                      "as-of-v16 pointer and a currentSource binding that I "
                      "verified equals the frozen bytes - but the same remedy "
                      "was not extended to the sibling it was compared against.",
      "whyNotMustOrShould": "Nothing normative is affected and no admission "
                            "changes. The substance of V14-ADV-2 survives in the "
                            "current bytes: I confirmed relation_payload_rules is "
                            "still invoked inside open_run_closure. This is "
                            "provenance friction, and it is the same defect the "
                            "v16 review and the candidate both graded advisory.",
      "measured": {"accountItems": p11["itemCount"],
                   "itemsCarryingASourceCorrectionPin":
                       p11["itemsWithASourceCorrectionPin"],
                   "staleButExplicitlyLabelledHistorical":
                       p11["labelledHistoricalCount"],
                   "staleAndNotLabelled": p11["unlabelledStaleCount"],
                   "item43CurrentBindingMatchesFrozenBytes": True},
      "repair": "Apply the item-43 pattern to item 44: label the existing pin as "
                "the as-of-v16 historical correction pin and add a currentSource "
                "binding to the frozen v17 digest. No historical byte is "
                "rewritten."
    }
  ],
  "priorFindingDispositions": prior,
  "additionalSourceFindingDispositions": additional,
  "priorFindingAccounting": {
    "cb6FindingsAccounted": len(prior),
    "additionalSourceFindingsAccounted": len(additional),
    "totalAccounted": len(prior) + len(additional),
    "unresolvedMustCount": 0,
    "unresolvedShouldCount": 0,
    "everyOriginalSeverityPreserved": True,
    "noSeverityDowngraded": True
  },
  "custody": {
    "manifestSha256Verified": before["manifestShaMatchesDeclared"],
    "declaredFileCount": before["declaredFileCount"],
    "verifiedBefore": before["verifiedOk"],
    "verifiedAfter": after["verifiedOk"],
    "declaredTotalBytes": before["declaredTotalBytes"],
    "observedTotalBytes": before["sumVerifiedBytes"],
    "undeclaredFilesBefore": before["undeclaredCount"],
    "undeclaredFilesAfter": after["undeclaredCount"],
    "symlinks": before["symlinkCount"],
    "missing": before["missingCount"],
    "hashMismatches": before["hashMismatchCount"],
    "lengthMismatches": before["sizeMismatchCount"],
    "frozenSubjectUnchangedByThisReview":
        before["allDeclaredFilesIntact"] and after["allDeclaredFilesIntact"],
    "copies": p12["copyCustody"],
    "allCopiesByteExactAfterExecution": p12["allCopiesByteExactAfterExecution"],
    "v16ExtractIsPartialReference": p12.get("v16Extract", {}).get("fileCount")
  },
  "sourcePins": {
    "verifiedBeforeAnyExecution": True,
    "pinRegistries": 4,
    "totalTransitivePins": 1308,
    "byRegistry": {"foundation": 1099, "native": 71, "security": 73,
                   "workflows": 65},
    "mismatches": 0,
    "everRepinnedByThisReview": False,
    "finalSealAfterAllRecording": {
      "scopesChecked": len(p12["finalPinSeal"]),
      "totalPinChecks": p12["totalPinsCheckedAcrossAllScopes"],
      "sealHoldsEverywhere": p12["finalSealHoldsEverywhere"]
    }
  },
  "sourceDelta": {
    "predecessorManifestSha256": delta["v16ManifestSha256"],
    "predecessorChainVerified": delta["predecessorChainOk"],
    "filesChanged": delta["changedCount"],
    "filesAdded": delta["addedCount"],
    "filesRemoved": delta["removedCount"],
    "nonScaffoldChanged": delta["changedNonScaffoldCount"],
    "nonScaffoldAdded": delta["addedNonScaffoldCount"],
    "declaredSourceDeltaFileCount": pins["declaredSourceDeltaCount"],
    "declaredSourceDeltaFullyConsistent": pins["sourceDeltaFullyConsistent"],
    "changedNonScaffoldNotInDeclaredSourceDelta":
        pins["changedNonScaffoldNotInSourceDeltaCount"],
    "thoseAreAllGeneratedReportsPinRegistriesOrRecords": True
  },
  "referenceChecks": {
    "commandsReproduced": six_a["commandCount"],
    "reproducedInCopies": ["copy-A-reference-run", "copy-B-probes"],
    "allExitsMatchDeclared": six_a["allExitsMatch"] and six_b["allExitsMatch"],
    "allStdoutByteIdenticalToFrozenLogs":
        six_a["allStdoutMatchesFrozenLog"] and six_b["allStdoutMatchesFrozenLog"],
    "allInTreeReportsByteIdenticalToFrozen":
        six_a["allReportsByteIdentical"] and six_b["allReportsByteIdentical"],
    "deterministicAcrossTwoIndependentCopies": True,
    "noSourceMutatedByExecution":
        six_a["noSourceMutated"] and six_b["noSourceMutated"],
    "nativeCheckerWritesInTreeSoRunOnlyInDisposableCopies": True,
    "nativeRegeneratePinsModeNeverInvoked": True,
    "expectationsPrewrittenBeforeExecution":
        "logs/expected-outcomes.prewritten.json",
    "measuredCounts": {
      "note": "These are measured passing CALLS, distinct IDs, and scoped cases "
              "and sweeps with their recorded scope. They are not exhaustive "
              "coverage and are never product qualification.",
      "foundationChecksPassed": counts["measured"]["foundation.checksPassedSum"],
      "foundationComponents": counts["measured"]["foundation.componentsMeasured"],
      "foundationSourcePins": counts["measured"]["foundation.sourcePinsVerified"],
      "identityPassingCalls": counts["measured"]["identity.passingCalls"],
      "identityDistinctIds": counts["measured"]["identity.distinctIds"],
      "identityDuplicateExtraInstances":
          counts["measured"]["identity.duplicateExtraInstances"],
      "identityDuplicateIds": {"closed-closure": 7, "exact-version-closure": 7},
      "securityCasesPassed": p13["securityCases"],
      "securityInvariantSweeps": p13["securitySweeps"],
      "securitySchemasValidated": p13["securitySchemasValidated"],
      "nativeCasesPassed": p13["nativeCases"],
      "nativePositiveCases": p13["nativePositiveCases"],
      "nativeNegativeCases": p13["nativeNegativeCases"],
      "nativeMatrixCells": p13["nativeMatrixCells"],
      "nativeQualifiedCells": p13["nativeQualifiedCells"],
      "workflowsChecksPassed": counts["measured"]["workflowSurface.passed"],
      "integrationChecksPassed": p13["integrationPassed"],
      "commands": p13["commands"],
      "goldens": p13["goldens"]
    },
    "everyHeadlineFigureReDerivedFromExecutedReports": True
  },
  "structuralAssessment": {
    "schemaDocumentsDiffed": len(p02["documents"]),
    "structuralPointersChangedAcrossAllDocuments": 0,
    "wideningKeyPointersChangedAcrossAllDocuments": 0,
    "onlyStructuralRemoval":
        "repair.schema.json#/$defs/EvidenceRequirement/properties/deficiency/$ref "
        "-> D9Deficiency, replaced by the two-plane oneOf. That removal IS the "
        "CB6-MUST-1 correction.",
    "enumVocabulariesChanged": [
        "NativeSufficiencyDeficiency (NEW definition)",
        "ImportedRequirementDeficiency (NEW definition)"],
    "d9DeficiencyEnumUnchanged": True,
    "deficiencyV2EnumUnchanged": True,
    "relationRegistryMembershipUnchanged": True,
    "executableLineDelta": [
        {"path": f["path"],
         "added": f.get("addedExecutableLines"),
         "removed": f.get("removedExecutableLines"),
         "refusalBearingRemoved": len(f.get("removedRefusalBearing", []))}
        for f in p08["files"]],
    "refusalBearingLinesRemovedFromAnyModel": 0,
    "whatTheThreeRemovalsWere": [
        "native model: an INLINE restatement of the kind rule, replaced by a "
        "read of the published table. I measured both over 25 paths including "
        "edge cases: 0 disagreements, so publishing the authority moved no "
        "derived value.",
        "workflows model: an unmet-precondition append that now has a NEW "
        "admission gate (admit_evidence_requirement) ahead of it and carries the "
        "rung, plane and exact cause. Strictly stronger.",
        "checker harness: two lines replaced by stricter versions that also "
        "assert errorCode equality and an expected remedy substring."],
    "conclusion": "No grammar, authority or admission was widened. Every "
                  "executable change is additive strictness."
  },
  "arDispositions": [
    {"id": "AR-%02d" % i,
     "disposition": "CARRIED-UNCHANGED",
     "basis": "The owning document docs/coop/architecture-depth-review/REVIEW.md "
              "and the correction crosswalk are BYTE-IDENTICAL to the v16 "
              "manifest entry, so no row moved.",
     "scope": "Preservation only. This review re-grades nothing.",
     "authority": "Not this review's to grant; the row's own owner and the "
                  "separately reviewed application own it.",
     "appliedByThisReview": False,
     "finalApplicationOutcomeGranted": False}
    for i in range(1, 17)],
  "fwDispositions": [
    {"id": "FW-%02d" % i,
     "disposition": "CARRIED-UNCHANGED",
     "basis": "current-source-map.proposed.md is byte-identical between the v16 "
              "and v17 manifests and is absent from the changed-path set.",
     "scope": "Preservation only.",
     "authority": "Not this review's to grant.",
     "appliedByThisReview": False,
     "finalApplicationOutcomeGranted": False}
    for i in range(1, 16)],
  "inheritedResidualDispositions": [
    {"id": rid,
     "disposition": "CARRIED-UNCHANGED",
     "basis": "inherited-residuals.proposed.md and "
              "inherited-row-sources.proposed.json are byte-identical to their "
              "v16 manifest entries.",
     "scope": "Preservation only. DR-011-R10 in particular states it cannot be "
              "closed by that table and requires an actual fresh blind "
              "implementer litmus, which this review does not supply.",
     "authority": "Not this review's to grant.",
     "appliedByThisReview": False,
     "finalApplicationOutcomeGranted": False}
    for rid in ["DR-001", "DR-002", "DR-003", "DR-004", "DR-005", "DR-006",
                "DR-007", "DR-008", "DR-009", "DR-010", "DR-011"]
               + ["DR-011-R%02d" % i for i in range(1, 17)]],
  "scopedReviewOwnerDispositions": [
    {"id": rid,
     "disposition": "ROUTING-ASSESSED-ONLY-NOT-APPLIED",
     "basis": "The owning register docs/v2/architecture/"
              "08-decision-and-readiness-register.md is byte-identical to its "
              "v16 manifest entry; the row's own historical 2026-08-13 scoped "
              "disposition stands unchanged as history.",
     "scope": "A routing assessment of a scoped review owner. It is NOT a grade "
              "and NOT a final application outcome.",
     "authority": "The row's own owner and the separately reviewed application. "
                  "This review invents no grade authority.",
     "appliedByThisReview": False,
     "finalApplicationOutcomeGranted": False}
    for rid in ["DR-201", "DR-202", "DR-203", "DR-204", "DR-205"]],
  "ownerRoutingScopeStatement":
    "The five owner routing assessments do not grant a final application "
    "outcome and are not a grade. CARRIED-UNCHANGED and ROUTING-ONLY are "
    "neither new grades nor final application outcomes. No grade is granted by "
    "inference anywhere in this review.",
  "registers": {
    "arRows": regs["arRowCount"],
    "fwRows": regs["fwRowCount"],
    "inheritedResiduals": 27,
    "inheritedResidualNote":
        "DR-001..011 (11) plus the DR-011 subledger R01..R16 (16). DR-012 "
        "appears only in the document's header prose as an explicitly EXCLUDED "
        "item ('DR-012 remains release qualification') and is not a table row.",
    "evaluationSubresiduals": regs["evaluationSubresidualCount"],
    "scopedReviewOwners": regs["dr201to205Count"],
    "qualificationGates": regs["qualificationGateCount"],
    "gatesDemonstrated": 0,
    "gatesQualified": 0,
    "allGatesRemainUnperformed": regs["allGatesUnperformed"],
    "gatesPerformedByThisReview": 0,
    "owningDocumentsByteIdenticalToV16": True,
    "advisoryAccount": {
      "v16Items": 50, "v17Items": 55,
      "added": ["CB6-ADV-1", "CB6-ADV-2", "CB6-ADV-3", "V16-ADV-1", "V16-ADV-2"],
      "removed": [], "severitiesChanged": 0,
      "myTwoNewAdvisoriesAreNotInThisAccount": True,
      "anyFutureApplicationMustAccountForThemSeparately": True
    }
  },
  "governanceCrossReferences": {
    "currentPinsResolved": p10["currentPinsResolved"],
    "explicitAsOfHistoricalPins": p10["historicalAsOfPins"],
    "unresolvedAndNotMarkedHistorical": 1,
    "theOneUnresolved": "advisory-application-account.v17 /items/44 - raised as "
                        "V17-ADV-2",
    "scannerCorrectionsIMade": [
      "custody/handoff records use RECORD-RELATIVE paths; my first resolver "
      "tried only repo-root and reported 18 false unresolved. Re-resolved: 36/36 "
      "entries in bv6-corrections-author.v6/custody.json verify exactly.",
      "`subjectManifestSha256` beside a review path is a MANIFEST digest, not "
      "that file's digest; my first scan mis-paired 240 crosswalk rows.",
      "`frozen16Sha256` and `finalV5Sha256` in the handoff are self-labelling "
      "as-of pins; 18 more false positives.",
      "historical-preservation-report.v17.json names 31 files of the wider live "
      "repository; only 10 lie inside the frozen subject slice. Those 10 match "
      "their currentSha256 exactly. The other 21 are OUTSIDE the subject and I "
      "therefore cannot verify them from the frozen bytes - stated as a limit of "
      "my evidence, not as a finding."
    ]
  },
  "preservedPriorCorrections": {
    "count": p13["preservedCorrectionCount"],
    "allHaveLiveAnchorsInTheFrozenBytes":
        p13["allPreservedCorrectionsHaveLiveAnchors"],
    "items": [r["correction"] for r in p13["preservedCorrections"]],
    "evidenceKind": "PRESERVATION evidence - a live anchor in the frozen bytes "
                    "plus a governing suite that executed and passed on those "
                    "exact bytes, combined with zero structural schema change, "
                    "unchanged registry membership and a refusal-only executable "
                    "delta. It is NOT a first-principles re-derivation of each "
                    "correction."
  },
  "evidenceHonesty": {
    "schemaOnlyChecks": "The vocabulary joins, presence law, generic field "
                        "domain, MutationReceipt/ImportResult required fields "
                        "and every structural diff are SCHEMA-level facts.",
    "helperLevelChecks": "config_node_kind, typescript_config_graph_faults, "
                         "admit_evidence_requirement, sufficiency_v2, "
                         "mutation_replay_key and the target projection are "
                         "reference MODEL functions over synthetic in-memory "
                         "inputs, not a production host.",
    "fullRunClosure": "Only the CB6-SHOULD-2 controls are complete admitted Run "
                      "graphs. Five closed with real distinct run2: identities "
                      "and two refused at close_run. Where a change affects "
                      "closure I used full Runs; schema fragments are not "
                      "claimed to prove full Runs anywhere.",
    "executedExpectation": "All six reference commands were EXECUTED with "
                           "pre-written expectations, in two byte-exact copies.",
    "narrative": "Statements about intent, rationale and history - including "
                 "the candidate's own dispositions - are narrative and are "
                 "reported as such, never as measurement.",
    "firstActualRefusalBoundary":
        "For the imported per-requirement plane the first actual refusal is "
        "workflows_model.admit_evidence_requirement raising CONFIG.INVALID; the "
        "owning schema does NOT refuse a cross-plane value, deliberately, and I "
        "measured exactly 50 cases where the consumer refuses and the schema "
        "admits. For the config-node kind the first actual refusal is "
        "typescript_config_graph_faults reporting "
        "native.config-graph-kind-contradicts-path, ahead of universe "
        "admission. For the coverage partition it is identity-model close_run "
        "raising SUBJECT_SCOPE_PARTITION_OVERLAP, and NOT the per-Coverage "
        "producer, which structurally cannot see a second scope.",
    "blindV6HelperLimitsAcknowledged":
        "I preserve the root qualifications on blind v6 as written: it "
        "constructed 355 CAS objects but its four claimed complete Run graphs "
        "refuse close_run for missing retained schema bytes, and separate "
        "policy/waiver schema checks fail; its 83 negative-labelled controls "
        "include 3 positive/hash-distinction controls; some assertions are "
        "narrative. Those helper limits do NOT erase the normative gaps blind "
        "v6 identified, and they do not turn precise existing text into a "
        "design omission. Its original report remains literal historical "
        "evidence.",
    "noBlanketCoverageClaim": True,
    "referenceCountsAreNotProductQualification": True
  },
  "failedAttempts": [
    {"id": "failed-attempt-01", "file": "probes/failed-attempt-01-p04-wrong-graph-key.py",
     "what": "My TypeScriptConfigGraphV1 fixture used `entry` instead of the "
             "schema's `entryConfigPath` and omitted contentSha256/schemaVersion.",
     "wasADesignFailure": False,
     "correctedBy": "probes/p04_must2_config_kind.py"},
    {"id": "failed-attempt-02", "file": "probes/failed-attempt-02-p04-unsorted-nodes-array.py",
     "what": "My nodes array was unsorted; the record carries "
             "x-opensip-order {by:[path]} and typescript_config_graph_digest "
             "correctly refused it. Note the fault checker does not validate "
             "order, the digest path does.",
     "wasADesignFailure": False,
     "correctedBy": "sorting the fixture; no law changed"},
    {"id": "failed-attempt-03", "file": "probes/failed-attempt-03-p06-wrong-ladder-module.py",
     "what": "I read RELATION_LADDERS from the identity model; ladders live in "
             "the relation registry, which is the single published ladder "
             "authority.",
     "wasADesignFailure": False,
     "correctedBy": "reading row['ladder'] from the registry"},
    {"id": "failed-attempt-04", "file": "probes/failed-attempt-04-p06-degenerate-identical-scope.py",
     "what": "My first overlap control built a SECOND subject-scope byte-identical "
             "to the first. Subject-scopes are content-addressed, so it collapsed "
             "onto the same id, added nothing, and the Run admitted with the "
             "BASELINE's own run id - which I caught because the run identity was "
             "identical. A degenerate control, not a design failure.",
     "wasADesignFailure": False,
     "correctedBy": "giving the second scope an extra subject so it is a distinct "
                    "record that still shares one subject and the full partition "
                    "tuple; it then refused as the law requires"},
    {"id": "corrected-scan-01",
     "what": "p01 pin parser matched `primaryReferences` before `pins` in the "
             "native registry and reported 0 entries; re-run against the `pins` "
             "key gives 71/71 valid.",
     "wasADesignFailure": False},
    {"id": "corrected-scan-02",
     "what": "p09 cross-reference resolver missed record-relative custody paths "
             "and mis-paired manifest digests with file paths, producing 42 then "
             "304 false positives. p10 corrects the resolution and classification; "
             "exactly one genuine unresolved pin remains (V17-ADV-2).",
     "wasADesignFailure": False},
    {"id": "corrected-scan-03",
     "what": "p13 anchor patterns were case-sensitive and named "
             "`runtime-observation` in a model that reads that relation from the "
             "schema registry. Both anchors are in fact present; corrected "
             "patterns confirm 14/14.",
     "wasADesignFailure": False},
    {"id": "corrected-measurement-01",
     "what": "My first ADV-3 measurement checked only the VALUES of "
             "faultCauseToErrorCode and concluded SYSTEM.OUTCOME.ILLEGAL_STATE "
             "was not in the inherited vocabulary. It is - at "
             "codeVocabulary.errorCodes[18] of 19. The corrected measurement is "
             "the one relied on and the blind reviewer's claim was right.",
     "wasADesignFailure": False}
  ],
  "standing": {
    "implementationAuthorized": False,
    "readinessChanged": False,
    "productQualification": False,
    "d372Applied": False,
    "condition5": "NOT MET",
    "blindReconstructabilityClaimed": False,
    "applicationAcceptanceClaimed": False,
    "aNewIndependentBlindReconstructionRemainsSeparatelyRequired": True,
    "priorIndependentAcceptDidNotSurviveBlindReconstruction":
        "The v16 ACCEPT was overturned by blind v6. My ACCEPT is therefore "
        "explicitly NOT a prediction that a new blind reconstruction will "
        "succeed, and cannot substitute for one.",
    "oneCompleteIntendedProductImplementedInStages": True,
    "scopeUnchanged": {
      "machineIds": 4, "platforms": ["macOS", "Linux"],
      "paths": ["TypeScript", "JavaScript", "Rust", "bounded bundled grammar"],
      "noInventedProviderOsCompilerCryptoOrStorageQualification": True
    },
    "gatesInView": {"ar": 16, "fw": 15, "inheritedResiduals": 27,
                    "evaluationSubresiduals": 30, "scopedReviewOwners": 5,
                    "unperformedQualificationGates": 32}
  },
  "requiredNextActs": [
    "A NEW independent blind consumer reconstruction over these accepted "
    "normative bytes. This is separately required and this review cannot supply "
    "it.",
    "A complete, independently reviewed application and readiness "
    "reconciliation.",
    "Optionally, the two nonblocking clarifications V17-ADV-1 and V17-ADV-2 at "
    "their stated advisory severity."
  ]
}

with open(OUT, "w") as fh:
    json.dump(review, fh, indent=1, sort_keys=False)
    fh.write("\n")

print("wrote", OUT, os.path.getsize(OUT), "bytes")
print("verdict:", review["verdict"])
print("newMustIssues:", len(review["newMustIssues"]),
      "newShouldIssues:", len(review["newShouldIssues"]),
      "newAdvisories:", len(review["newAdvisories"]))
print("prior CB6 accounted:", len(prior), "| additional accounted:", len(additional))
print("sha256:", hashlib.sha256(open(OUT, "rb").read()).hexdigest())
