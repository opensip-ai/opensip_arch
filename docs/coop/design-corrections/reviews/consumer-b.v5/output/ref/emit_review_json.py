"""Emit blind-review.json from the retained vector outputs."""

from __future__ import annotations

import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_ref as R  # noqa: E402

OUT = "/tmp/opensip-design-corrections/consumer-b.v5/output"


def load(name):
    with open(os.path.join(OUT, "vectors", name + ".json")) as fh:
        return json.load(fh)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    inputv = load("input-verification")
    summary = load("_summary")
    audits = load("registry-audits")

    new_must = [
        {
            "id": "CB5-MUST-1",
            "title": "The capability-manifest value-domain successor is not selected by "
                     "any contract selector, so the contract text directs ADM-DOMAIN at "
                     "the superseded registry",
            "severity": "MUST",
            "selectors": [
                "docs/v2/contracts/product-v1/identity-and-evidence.md#section-3 "
                "(\"The host validates the committed CVE1 artifact under the effective "
                "delivery.v4.json schema and recomputes capabilityManifestId as ...\")",
                "docs/coop/design-corrections/native/capability-manifest-domains.v2.json#/standing",
                "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
                "#/registries/RELATION-DOMAIN-V2",
                "docs/v2/contracts/product-v1/native-evidence.md#section-11",
                "docs/coop/artifacts/delivery.v4.json"
                "#/derivedFrom/operations/17/value/admission/ADM-DOMAIN",
            ],
            "evidence": {
                "successorStandingClaim": "Normative CURRENT successor of delivery.v4 "
                                          "capabilityManifestIdentity valueDomains, named "
                                          "by native-evidence section 11 and "
                                          "identity-and-evidence section 3",
                "identityAndEvidenceMentionsOfTheSuccessor": 1,
                "identityAndEvidenceMentionContext":
                    "section 3 ladder paragraph only, as a DECLARED MIRROR of "
                    "RELATION-LADDER-DOMAIN-V2.ladders; not as the ADM-DOMAIN successor",
                "nativeEvidenceMentionsOfTheSuccessor": 0,
                "delivery4RelationDomainMembers":
                    audits["capabilityManifestDomainConflict"][
                        "capabilityManifestRelationDomain"],
                "successorRelationDomainMemberCount": 13,
                "productRelationRegistryMembers":
                    audits["capabilityManifestDomainConflict"]["productRelations"],
                "relationUnexpressibleUnderTheSelectedRegistry":
                    audits["capabilityManifestDomainConflict"]["relationsUnexpressible"],
                "matrixCellsForTheUnexpressibleCapability":
                    {m: R.CELLS[("unresolved-edge", m)]["state"]
                     for m in R.MATRIX["languageModes"]},
            },
            "impact": "A release capability manifest declaring unresolved-edge - a "
                      "capability the matrix advertises as SUPPORTED-DESIGN in five of six "
                      "language modes and the matrix-fixed default profile requests for "
                      "every non-syntax unit - is refused at ADM-DOMAIN under DL-DOM-1's "
                      "no-third-state rule. The implementer must either refuse the "
                      "product's own thirteenth relation or invent the selection of a "
                      "document no contract selector names.",
            "requiredInvention": True,
            "proposedFix": "identity-and-evidence section 3 names "
                           "native/capability-manifest-domains.v2.json as the effective "
                           "value-domain / ADM-DOMAIN registry for the committed CVE1 "
                           "artifact within its declared scope, superseding "
                           "delivery.v4.json's valueDomains; native section 11 lists it, "
                           "as the successor's own standing claims.",
        },
        {
            "id": "CB5-MUST-2",
            "title": "libSelection -> standardLibraryComponentDigests is an enforced "
                     "admission join with no published name mapping",
            "severity": "MUST",
            "selectors": [
                "docs/v2/contracts/product-v1/native-evidence.md#section-2.4 "
                "(toolchain.libSelection row: \"each must be covered by a retained "
                "component\"; and \"libSelection ... selects the same case-insensitive "
                "name set as the honored lib list\")",
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
                "#/$defs/TypeScriptToolchainIdentityV1/properties/libSelection",
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
                "#/$defs/TypeScriptLibComponentV1/properties/component",
                "docs/v2/contracts/product-v1/native-evidence.md#section-10 "
                "(native.native-context-lib-not-retained route)",
            ],
            "evidence": {
                "libSelectionHolds": "the effective TypeScript compilerOptions lib NAMES, "
                                     "forced by the equality rule against "
                                     "configProjection.honoredOptions.lib",
                "componentHolds": "declaration FILE names inside the admitted stdlib "
                                  "closure tree, e.g. lib.es2022.d.ts",
                "mappingPublishedInTheKit": False,
                "joinIsEnforced": True,
                "typedRefusal": "native.native-context-lib-not-retained",
                "d9Route": "request-rejected (2) / REQUEST.PRECONDITION_FAILED, "
                           "before PlanId, no worker spawned",
                "inventedMapping": "component == \"lib.\" + lowercase(name) + \".d.ts\"",
                "whereInvented": "output/ref/closure.py admit_native_context, marked at "
                                 "the point of use",
            },
            "impact": "Two conforming hosts that invent different mappings admit and refuse "
                      "the SAME retained context bytes differently. This is a public "
                      "admission divergence, not algorithm freedom left to implementation.",
            "requiredInvention": True,
            "proposedFix": "Publish the mapping in section 2.4, or make libSelection carry "
                           "component names and drop the honoredOptions.lib equality rule "
                           "- but not both readings.",
        },
    ]

    new_should = [
        {
            "id": "CB5-SHOULD-1",
            "title": "RC-1 does not determine resolutionCompleteness.state for "
                     "unresolved-edge@observed",
            "severity": "SHOULD",
            "selectors": [
                "docs/v2/contracts/product-v1/native-evidence.md#section-4.3 RC-1",
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
                "#/$defs/ResolutionCompletenessState",
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
                "#/$defs/ViewEntryV3 (resolutionCompleteness is REQUIRED)",
                "docs/coop/design-corrections/native/native-capability-matrix.v2.json"
                "#/capabilities (unresolved-edge)",
            ],
            "evidence": load("rc1-unresolved-edge-state-gap"),
            "impact": "Two conforming producers mint DIFFERENT coverage2 payload digests, "
                      "and therefore different coverage2 identities, for the same "
                      "observation of the same universe.",
            "requiredInvention": True,
            "proposedFix": "Add unresolved-edge to RC-1's not-applicable list, or state the "
                           "required state for the observed rung explicitly.",
        },
        {
            "id": "CB5-SHOULD-2",
            "title": "RepairPlanDescriptor.closedWorld is described as \"Copied from\" "
                     "ClosedWorldV2 but is a closed five-field record where ClosedWorldV2 "
                     "is a closed seven-field record",
            "severity": "SHOULD",
            "selectors": [
                "docs/coop/design-corrections/workflows/schemas/repair.schema.json"
                "#/$defs/RepairPlanDescriptor/properties/closedWorld",
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
                "#/$defs/ClosedWorldV2",
                "docs/v2/contracts/product-v1/workflows-and-surfaces.md#section-12",
                "docs/v2/contracts/product-v1/native-evidence.md#section-4.5",
            ],
            "evidence": {
                "repairClosedWorldRequired": ["deadCodeRepairEligible", "exportsClosed",
                                              "entryPointsRecognized", "nonliteralLoading",
                                              "externalConsumers"],
                "nativeClosedWorldV2Required": sorted(
                    R.NATIVE["$defs"]["ClosedWorldV2"]["required"]),
                "literalCopyRefusal":
                    "repair#/$defs/RepairPlanDescriptor @ /closedWorld: Additional "
                    "properties are not allowed ('dynamicDispatch', 'reasons' were "
                    "unexpected)",
                "projectionPublished": False,
                "determinateByElimination": True,
            },
            "impact": "A literal copy refuses. The projection (drop dynamicDispatch and "
                      "reasons) is determinate by elimination, so no semantic invention is "
                      "forced, but it is published nowhere and dynamicDispatch is a genuine "
                      "closed-world ingredient a destructive-repair prerequisite discards.",
            "requiredInvention": True,
            "proposedFix": "Replace \"Copied from\" with the explicit projection, or widen "
                           "the repair record to the seven ClosedWorldV2 members.",
        },
    ]

    advisories = [
        {
            "id": "CB5-ADV-1",
            "title": "The \"four closed representations\" are five tokens in practice",
            "selectors": [
                "docs/v2/contracts/product-v1/identity-and-evidence.md#section-3 "
                "(\"The four representations are closed\")",
                "docs/coop/design-corrections/foundation/identity-schemas.v2.json"
                "#/$defs/Ref/properties/digest",
                "#/$defs/ProofInputRef/properties/digest",
                "#/$defs/FindingEvidenceRef/properties/digest",
            ],
            "observation": "Those three fields carry representation \"by-domain\", a fifth "
                           "token that indirects into the four through "
                           "x-opensip-digest-domains.byDomain. The adjacent paragraph "
                           "explains the indirection, so a careful reader recovers; a "
                           "strict implementer enforcing the four-member vocabulary refuses "
                           "three real fields.",
            "representationsObservedInUse": load("digest-law")["representationsInUse"],
        },
        {
            "id": "CB5-ADV-2",
            "title": "The LogicalPath description overstates its adoption",
            "selectors": [
                "docs/coop/design-corrections/foundation/identity-schemas.v2.json"
                "#/$defs/LogicalPath (\"every identity-bearing path field now carries it "
                "in the schema\")",
            ],
            "observation": "Only Blob.path and import-blob.path reference it. "
                           "fact.anchors[].path and "
                           "finding-fingerprint.subjectKey.logicalPath are plain bounded "
                           "strings; the three scope-descriptor arrays legitimately cannot "
                           "use it because `.` is the project-root sentinel and LogicalPath "
                           "forbids a dot segment. No invention is forced - an anchor path "
                           "must be an inventoried snapshot path and inventory rows ARE "
                           "Blob - but the sentence is not true as written.",
            "measured": audits["logicalPathUsageInIdentitySchemas"],
        },
        {
            "id": "CB5-ADV-3",
            "title": "The L0 body payload carries two length prefixes",
            "selectors": [
                "docs/coop/artifacts/fact-identity-policy.v2.json"
                "#/canonicalisationSchema/byteGrammar/payloadEncodingByLevel/L0-verbatim",
                "docs/coop/artifacts/fact-identity-policy.v2.json"
                "#/canonicalisationSchema/byteGrammar/domainSeparatedPreimage",
                "docs/v2/contracts/product-v1/identity-and-evidence.md#section-3 "
                "(clones body recipe)",
            ],
            "observation": "Read together the L0 payload is length-prefixed twice "
                           "(payload_len == raw_byte_len + 4). The reading is decided by "
                           "symmetry with streamFraming for L1-L3 (u32be token_count || "
                           "token* under the same outer u32be payload_len), and this review "
                           "implemented it that way, but the alternative reading is "
                           "grammatically available and yields a different bodyIdentity.",
            "resolution": "one explicit byte vector or one sentence closes it",
        },
        {
            "id": "CB5-ADV-4",
            "title": "PLATFORM-ID-DOMAIN-V1 admits platforms the selected product does not "
                     "promise",
            "selectors": [
                "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
                "#/registries/PLATFORM-ID-DOMAIN-V1",
                "docs/coop/artifacts/delivery.v4.json"
                "#/derivedFrom/operations/17/value/valueDomains/registries/"
                "PLATFORM-ID-DOMAIN-V1",
                "docs/v2/contracts/product-v1/security-and-lifecycle.md#S8",
                "docs/v2/contracts/product-v1/admission-and-qualification.md#section-5 "
                "item 1 (\"Windows is not selected\")",
            ],
            "observation": "ProviderCapability.platformIds[] admits windows-x86_64-msvc, "
                           "windows-aarch64-msvc and linux-x86_64-musl while security S8 "
                           "and the native matrix select exactly four machine ids. "
                           "delivery.v4 discloses this as DUD-V4-9, so it is an accounted "
                           "open item rather than a hidden inconsistency, but the product "
                           "contracts do not repeat the accounting.",
            "measured": {
                "manifestDomain": audits["capabilityManifestDomainConflict"][
                    "platformDomainMembers"],
                "selectedPlatformIds": audits["capabilityManifestDomainConflict"][
                    "securitySelectedPlatformIds"],
                "outsideTheSelectedProduct": audits["capabilityManifestDomainConflict"][
                    "platformIdsInTheManifestDomainOutsideTheSelectedProduct"],
            },
        },
    ]

    checked_and_cleared = [
        {
            "id": "CB5-CLEARED-1",
            "title": "capability-manifest DEFICIENCY-DOMAIN-V1 stays at the inherited five "
                     "while DeficiencyV2 has nine",
            "consideredSeverity": "SHOULD",
            "withdrawnBecause": "The four added members (input-closure-incomplete, "
                                "resolution-incomplete, external-consumers-unknown, "
                                "derivation-policy-unmet) are per-Run or "
                                "requirement-relative conditions, whereas "
                                "AbsentCapability.deficiency is a RELEASE-LEVEL "
                                "capability-absence declaration for which "
                                "provider-unavailable and language-tier-unsupported "
                                "suffice. The rule is closed and implementable; only the "
                                "rationale is unpublished.",
            "measured": {
                "manifestDeficiencyDomain": audits["capabilityManifestDomainConflict"][
                    "capabilityManifestDeficiencyDomain"],
                "productDeficiencies": audits["capabilityManifestDomainConflict"][
                    "productDeficiencies"],
                "unexpressible": audits["capabilityManifestDomainConflict"][
                    "deficienciesUnexpressible"],
            },
        },
    ]

    verified_claims = {
        "everyArrayInEveryKitSchemaDeclaresAnOrder":
            all(not v for v in audits["arraysWithoutDeclaredOrder"].values()),
        "arraysWithoutDeclaredOrderByDocument": audits["arraysWithoutDeclaredOrder"],
        "no64HexFieldLacksAnAnnotation": {
            "identity": audits["unannotated64HexFields"]["identity"],
            "native": audits["unannotated64HexFields"]["native"],
            "note": "the two hits are the terminal scalar DEFINITIONS Hash and DigestHex, "
                    "which the relation document's law explicitly says must not carry a "
                    "blanket default; every reference site is annotated",
        },
        "rungVocabularyIsExactlyTheLadderUnion": audits["rungVocabularyUnion"],
        "relationDigestLawIsConsumedNotMerelyDeclared":
            audits["relationDigestLawConsumption"] == [],
        "publicDetailRegistryEqualsTheCommonEnum":
            audits["publicDetailRegistryParity"]["identical"],
        "everyContextFreeRouteKeyWithAPublicDetailHasAnAlias":
            audits["publicDetailRegistryParity"]["contextFreeKeysMissingAnAlias"] == [],
        "scopeLimitArithmetic": audits["scopeLimitArithmetic"],
        "d9ExtensionCheck": load("public-terminations")["d9ExtensionCheck"],
        "cve1ReadingAgreesWithTheEmbeddedIllustration": {
            "note": "consistency check of MY encoder against the embedded delivery.v4 "
                    "DCM-1 committed byte string; the embedded example is NOT used as an "
                    "oracle for any designed vector",
            "agrees": True,
        },
    }

    ref_files = sorted(glob.glob(os.path.join(OUT, "ref", "*.py")))
    vector_files = sorted(glob.glob(os.path.join(OUT, "vectors", "*.json")))

    review = {
        "review": "OpenSIP DR-011-R10 blind consumer-B reconstruction",
        "reviewer": "actual Claude, fresh blind consumer-B session",
        "verdict": "CHANGES_REQUIRED",
        "verdictBasis": "2 unresolved MUST issues and 2 unresolved SHOULD issues; any "
                        "remaining MUST/SHOULD design gap requires CHANGES_REQUIRED",
        "notAClaimOf": ["product qualification", "implementation authorization",
                        "readiness grade", "acceptance of any governance record"],
        "inputVerification": {
            "parentSubjectSha256": inputv["parentSubjectSha256"],
            "declaredFileCount": inputv["declaredFileCount"],
            "verifiedOk": inputv["verifiedOk"],
            "failed": inputv["failed"],
            "extraFilesOnDisk": inputv["extraFilesOnDisk"],
            "manifestEntriesMissingOnDisk": inputv["manifestEntriesMissingOnDisk"],
            "allVerified": inputv["allVerified"],
            "perFileDigests": "output/vectors/input-verification.json",
        },
        "inputCustody": {
            "readOnlyTheKit": True,
            "originalRepositoryAccessed": False,
            "authorReferenceModelsRead": False,
            "fixturesCasesGoldensReportsRead": False,
            "priorReviewsRead": False,
            "otherDesignCorrectionDirectoriesRead": False,
            "historicalOrReviewLinksFollowed": False,
            "embeddedExamplesUsedAsAnOracle": False,
        },
        "newMustIssues": new_must,
        "newShouldIssues": new_should,
        "nonblockingAdvisories": advisories,
        "checkedAndCleared": checked_and_cleared,
        "verifiedClaims": verified_claims,
        "reconstruction": {
            "scenarioCount": summary["scenarioCount"],
            "scenarios": summary["scenarios"],
            "scenarioErrors": summary["errors"],
            "closedRunDescriptorGraphs": {
                "typescript": ["ts-ordinary", "ts-synthesized",
                               "ts-custom-named-multi-base", "ts-jsconfig-shared-base",
                               "ts-two-contexts-one-plan"],
                "rust": ["rust-mixed-edition"],
                "syntaxOnly": ["syntax-code-grammar", "syntax-data-only-repository"],
                "total": 8,
            },
            "additionalConstructedUniverses": {
                "rust-two-selections": 3,
                "rust-ownership-deficiencies": 3,
            },
            "negativeProbeCount": 58,
            "runIds": {
                "ts-ordinary": load("ts-ordinary")["runId"],
                "ts-synthesized": load("ts-synthesized")["runId"],
                "ts-custom-named-multi-base": load("ts-custom-named-multi-base")["runId"],
                "ts-jsconfig-shared-base": load("ts-jsconfig-shared-base")["runId"],
                "ts-two-contexts-one-plan": load("ts-two-contexts-one-plan")["runId"],
                "rust-mixed-edition": load("rust-mixed-edition")["runId"],
                "syntax-code-grammar": load("syntax-code-grammar")["runId"],
                "syntax-data-only-repository": load("syntax-data-only-repository")["runId"],
            },
        },
        "requiredInvention": [
            {"item": "the lib name -> stdlib component file-name mapping",
             "blocking": True, "issue": "CB5-MUST-2"},
            {"item": "which value-domain registry admits the committed CVE1 artifact",
             "blocking": True, "issue": "CB5-MUST-1"},
            {"item": "resolutionCompleteness.state for unresolved-edge@observed",
             "blocking": True, "issue": "CB5-SHOULD-1"},
            {"item": "the 7->5 projection of ClosedWorldV2 into the repair descriptor",
             "blocking": True, "issue": "CB5-SHOULD-2"},
            {"item": "the L0 double-length-prefix reading (decided by L1-L3 symmetry)",
             "blocking": False, "issue": "CB5-ADV-3"},
            {"item": "synthetic repository contents, closure trees, tool digests, level "
                     "specification bytes, grammar bundle bytes, ProjectId, "
                     "RequestId/ExecutionId values",
             "blocking": False,
             "issue": None,
             "note": "these are inputs a blind consumer is supposed to choose, not "
                     "design gaps"},
        ],
        "limitations": [
            "Nothing executed: no compiler, cargo, provider, repository, filesystem, "
            "ledger, renderer or cryptographic primitive. Real OS/compiler/crypto/SQLite "
            "measurements are future qualification.",
            "Every provider/OS/security observation in these vectors is a SYNTHETIC "
            "TRUSTED INPUT - an assumption, never native enforcement proof.",
            "The reconstructed close_run implements the joins the contracts name that are "
            "decidable over retained descriptors; it does not implement the evaluator, the "
            "ledger, retention GC, lease mechanics, trust time, root-chain admission, "
            "migration, the protocol-3 state machine or renderer conformance.",
            "x-opensip-order is not a JSON-Schema keyword; a stock validator ignores it. "
            "Mirror-agreement statements hold only with the separately implemented order "
            "enforcement in place.",
            "Reference-fixture and checker claims inside the contracts were deliberately "
            "not read and are outside what this kit can confirm.",
            "Governance standing (correction record, readiness register) is excluded from "
            "the kit by construction; nothing here grants readiness, acceptance or "
            "implementation permission.",
            "agent serve, HTML/SARIF renderers, policy test suites, baseline export/adopt "
            "round trips, trust recovery, store migration and the installation transition "
            "journal were read but not exercised as vectors.",
        ],
        "retainedOutputs": {
            "reviewMarkdown": "output/blind-review.md",
            "reviewJson": "output/blind-review.json",
            "referenceSources": [
                {"path": os.path.relpath(p, OUT), "sha256": sha(p)} for p in ref_files],
            "vectorOutputs": [
                {"path": os.path.relpath(p, OUT), "sha256": sha(p)} for p in vector_files],
        },
    }

    with open(os.path.join(OUT, "blind-review.json"), "w") as fh:
        json.dump(review, fh, indent=1, sort_keys=False, ensure_ascii=False)
    print(json.dumps({"verdict": review["verdict"],
                      "newMustIssues": [i["id"] for i in new_must],
                      "newShouldIssues": [i["id"] for i in new_should],
                      "advisories": [a["id"] for a in advisories],
                      "scenarios": summary["scenarioCount"],
                      "closedRuns": 8,
                      "negativeProbes": 58,
                      "inputsVerified": inputv["allVerified"]}, indent=1))


if __name__ == "__main__":
    main()
