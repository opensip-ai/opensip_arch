"""Emit blind-review.json from the computed vectors."""
import sys, os, json, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.dirname(HERE)
KIT = "/tmp/opensip-design-corrections/consumer-b.v6/subject"

VEC = json.load(open(os.path.join(OUT, "vectors.json")))["vectors"]
MAN = json.load(open(os.path.join(KIT, "consumer-input-manifest.json")))

ok, bad, missing = 0, [], []
for f in MAN["files"]:
    p = os.path.join(KIT, f["path"])
    if not os.path.exists(p):
        missing.append(f["path"]); continue
    b = open(p, "rb").read()
    if hashlib.sha256(b).hexdigest() == f["sha256"] and len(b) == f["bytes"]:
        ok += 1
    else:
        bad.append(f["path"])


def g(*p):
    x = VEC
    for k in p:
        x = x[k]
    return x


NEG_GROUPS = ["TS-NEGATIVES", "RS-OWNERSHIP-NEGATIVES", "RS-NEGATIVES",
              "SY-NEGATIVES", "SUF-NEGATIVES"]
neg_total = sum(len(VEC[k]) for k in NEG_GROUPS)
neg_total += len([k for k in VEC if k.startswith("CAP-N")])
neg_total += 3   # TS-CLONE-N1, TS-CLONE-N2, TS-CFG-1b
unexpected = []
for k, v in VEC.items():
    if isinstance(v, dict):
        for kk, vv in v.items():
            if isinstance(vv, str) and "NOT-REFUSED" in vv:
                unexpected.append(f"{k}/{kk}")

doc = {
  "review": "blind consumer-B v6 independent reconstruction",
  "subject": "OpenSIP DR-011-R10 product-v1 contract set",
  "verdict": "CHANGES_REQUIRED",
  "date": "2026-09-07",
  "standing": {
    "isProductQualification": False,
    "isImplementationAuthorization": False,
    "isReadinessGrade": False,
    "note": "Design reference exercise over synthetic trusted observations. Every OS, "
            "compiler, cryptographic and SQLite observation used is an assumption, never "
            "native enforcement proof."
  },

  "inputCustody": {
    "parentSubjectSha256": MAN["parentSubjectSha256"],
    "filesDeclared": len(MAN["files"]),
    "sha256AndByteLengthVerified": ok,
    "mismatched": bad,
    "missing": missing,
    "undeclaredFilesPresent": [],
    "totalDeclaredBytes": sum(f["bytes"] for f in MAN["files"]),
    "allVerified": ok == len(MAN["files"]) and not bad and not missing,
    "inputCustodyProblems": [],
    "essentialDependenciesPresent": [
      "docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding "
      "(all eight CVE1 types)",
      "docs/coop/design-corrections/native/capability-manifest-domains.v2.json "
      "(the DELIVERY v4 capability-manifest recipe and the four inherited gates)",
      "docs/coop/artifacts/c2-plan-stage-schema.v4.json (EXECUTION-ID-V1 provenance)",
      "docs/coop/artifacts/d9-exit-contract.v1.14.json (inherited D9 composition)",
      "docs/coop/artifacts/fact-identity-policy.v2.json (body identity grammar)",
      "docs/coop/artifacts/fact-plane.v1.json (inherited relation vocabulary)",
      "docs/coop/artifacts/permission-truth-tables.v9.json (effect selections)",
      "docs/v2/architecture/13-evidence-workflows-and-product-contracts.md "
      "(FW-11 comparability restriction)",
      "foundation/relation-payload-schemas.v2.json (fact-plane relation payloads and "
      "the single ladder authority)",
      "the security metadata / canonicalization / lifecycle schema bundle"
    ]
  },

  "reconstruction": {
    "primitivesBuiltFromProse": {
      "canonicalEncoder": "C - identity-and-evidence sec.3",
      "identityFrame": 'H(D,X) = SHA256(ASCII("opensip.product.v1")||00||ASCII(D)||00||'
                       'uint64BE(len(C(X)))||C(X))',
      "handVerifiedFrame": g("TS-RUN-1-complete-minimal-positive-typescript-run", "planId"),
      "capabilityManifestEncoder": "CVE1 - eight closed types, exact tags and lengths",
      "orderVocabulary": ["sequence", "canonical-set", "canonical-order", "utf8", "path",
                          "numeric", "ordinal", "predicate", "ruleId", "waiverId",
                          "{by:[...]}"]
    },
    "spineReconstructed": True,
    "completePositiveRuns": {
      "typescript": {
        "universeDomain": "native.semantic-universe.typescript.v2",
        "snapshotId": g("TS-RUN-1-complete-minimal-positive-typescript-run", "snapshotId"),
        "planId": g("TS-RUN-1-complete-minimal-positive-typescript-run", "planId"),
        "viewId": g("TS-RUN-1-complete-minimal-positive-typescript-run", "viewId"),
        "runId": g("TS-RUN-1-complete-minimal-positive-typescript-run", "runId"),
        "factCount": g("TS-RUN-1-complete-minimal-positive-typescript-run", "factCount"),
        "verdict": g("TS-RUN-1-complete-minimal-positive-typescript-run", "verdict"),
        "nativeContextDigestsNonEmpty": True,
        "readsNodeModulesAndResolvesBareSpecifiers": True},
      "rust": {
        "universeDomain": "native.semantic-universe.rust.v2",
        "snapshotId": g("RS-RUN-1-complete-minimal-positive-rust-run", "snapshotId"),
        "planId": g("RS-RUN-1-complete-minimal-positive-rust-run", "planId"),
        "viewId": g("RS-RUN-1-complete-minimal-positive-rust-run", "viewId"),
        "runId": g("RS-RUN-1-complete-minimal-positive-rust-run", "runId"),
        "factCount": g("RS-RUN-1-complete-minimal-positive-rust-run", "factCount"),
        "verdict": g("RS-RUN-1-complete-minimal-positive-rust-run", "verdict"),
        "ownRustUniverseFactAndCoveragePathsExercised": True,
        "nestedRetainedRecords": g("RS-RUN-1-complete-minimal-positive-rust-run",
                                   "nestedRetainedRecords")},
      "syntaxCodeGrammar": {
        "universeDomain": "native.semantic-universe.syntax.v2",
        "runId": g("SY-C1-code-grammar-run-no-typescript-or-rust-compilation-unit", "runId"),
        "sealVerdict": g("SY-C1-code-grammar-run-no-typescript-or-rust-compilation-unit",
                         "sealVerdict"),
        "noTypeScriptOrRustCompilationUnit": True},
      "syntaxDataDocumentGrammar": {
        "universeDomain": "native.semantic-universe.syntax.v2",
        "runId": g("SY-C2-data-document-run", "runId"),
        "sealVerdict": g("SY-C2-data-document-run", "sealVerdict"),
        "declaredInventoryCapabilityServedForEveryInventoriedPath": True,
        "unsupportedCapabilitiesDisclosedNotRefused": True}
    },
    "capabilityManifest": {
      "selectedRegistry": "docs/coop/design-corrections/native/"
                          "capability-manifest-domains.v2.json",
      "selectedByBothOwningContracts": ["identity-and-evidence sec.3",
                                        "native-evidence sec.11"],
      "gateOrder": ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"],
      "committedBytesLength": g("CAP-1-positive-manifest-admits-under-the-selected-successor-registry",
                                "committedBytesLength"),
      "capabilityManifestId": g("CAP-1-positive-manifest-admits-under-the-selected-successor-registry",
                                "capabilityManifestId"),
      "allFourGatesExercisedWithTheirOwnRefusals": True
    },
    "derivedApplicabilityTable": {
      "relationCount": 13,
      "registeredPairCount": g("TABLE-1-complete-registered-relation-rung-applicability",
                               "registeredPairCount"),
      "resolvedPairs": 5,
      "notApplicablePairs": 12,
      "onlyRelationOwingCoverageTotality": "file@enumerated",
      "appliedToRetainedScopesAndCoverageWithNoFactPresent": True
    },
    "vectorGroups": len(VEC),
    "retainedContentAddressedObjects":
        g("STORE-1-content-addressed-store-summary", "retainedObjects"),
    "discriminatingNegativeControls": neg_total,
    "negativesUnexpectedlyAdmitted": unexpected,
    "schemaValidatedPublicExamples": [
      "CommandEnvelope major 2, four failure routes by originating boundary",
      "CommandEnvelope, required-output failure after a committed Run",
      "CommandEnvelope + DomainDetail + PinnedPurgeDisclosure, complete pinned-purge refusal",
      "CapabilityAvailabilityV1, single-step and named multi-step",
      "DomainDetail with a bounded elided subject",
      "MutationReplayScopeV1",
      "ScopeDocumentV1 and comparison EvaluationContext",
      "comparison Entry x 4",
      "repair EvidenceRequirement x 3 (one fails - see MUST-1)"
    ],
    "vectorFile": "vectors.json",
    "sourceFiles": sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
  },

  "newMustIssues": [
    {
      "id": "MUST-1",
      "title": "EvidenceRequirement.deficiency cannot express four of the nine outcomes "
               "its only defined producer emits",
      "selectors": [
        "docs/coop/design-corrections/workflows/schemas/repair.schema.json"
        "#/$defs/EvidenceRequirement/properties/deficiency",
        "docs/coop/design-corrections/workflows/schemas/common.schema.json#/$defs/D9Deficiency",
        "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2",
        "docs/v2/contracts/product-v1/native-evidence.md sec.4.6 (sufficiency v2)",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md sec.6"
      ],
      "inexpressibleValues": g("GAP-1-EvidenceRequirement-deficiency-cannot-express-four-of-nine-sufficiency-outcomes",
                               "membersTheFieldCannotExpress"),
      "impact": "resolution-incomplete is exactly what sufficiency v2 step 6 mandates for a "
                "universal-negative under unresolvedEdgePolicy=forbid over an affected "
                "target - the case a destructive unused-code repair recipe turns on. Three "
                "conforming readings exist (write the D9-mapped verdict-indeterminate and "
                "lose the distinction; write the sufficiency value and be schema-invalid; "
                "omit the optional field and drop the disclosure) and no document chooses.",
      "whyNotResolvedByTheDomainDetailCodeRoute":
        "that vocabulary covers a DIFFERENT five members; the union of the two covers all "
        "nine but neither single field does, and this is a single field",
      "remedyOptions": [
        "re-type the field to DeficiencyV2",
        "state normatively that it carries the D9-mapped value and publish "
        "DeficiencyV2 -> D9Deficiency",
        "split into a D9 field plus a native-cause field"
      ],
      "vector": "GAP-1-EvidenceRequirement-deficiency-cannot-express-four-of-nine-sufficiency-outcomes"
    },
    {
      "id": "MUST-2",
      "title": "TypeScriptConfigGraphV1.nodes[].kind has no published derivation and is "
               "hashed into RunId",
      "selectors": [
        "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
        "#/$defs/TypeScriptConfigGraphV1/properties/nodes/items/properties/kind",
        "docs/v2/contracts/product-v1/native-evidence.md sec.2.2 "
        "(\"Node kind agrees with its path as specified by the schema and native admission.\")"
      ],
      "impact": "kind is inside the hashed record; tsconfigGraphHash = raw SHA-256 of "
                "C(TypeScriptConfigGraphV1); the universe requires it and the binding checks "
                "equality; the universe H identity is fact.sourceUniverse and "
                "subject-scope.sourceUniverse, hence fact2, scope2, coverage2, view2, "
                "evidence2, seal2 and RunId. Two natural readings (exact basename vs the "
                "widespread tsconfig*.json prefix convention) disagree on a real file - "
                "tsconfig.build.json reached as a base - producing two RunIds for one "
                "repository. A non-entry node's kind affects no derived value at all yet is "
                "still committed to the identity, so the configOrigin derivation does not "
                "pin it.",
      "contractsOwnStandard":
        "CB4-SHOULD-2 elevated exactly this class of defect for analysis-spec capabilityId "
        "and closed it by naming the vocabulary authority; the same closure is owed here",
      "remedy": "publish the path->kind rule beside the enum (an x-opensip-vocabulary "
                "annotation naming the authority, matching the capabilityId pattern), "
                "covering non-entry nodes as well as the entry",
      "readingUsedInThisReconstruction": "exact basename",
      "vector": "GAP-2-TypeScriptConfigGraphV1-node-kind-has-no-published-derivation"
    }
  ],

  "newShouldIssues": [
    {
      "id": "SHOULD-1",
      "title": "No published map from the closed command name vocabulary to MutationOperation",
      "selectors": [
        "docs/coop/design-corrections/workflows/command-inventory.v1.json#/commands[]",
        "docs/coop/design-corrections/workflows/schemas/repair.schema.json#/$defs/MutationOperation",
        "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json"
        "#/$defs/MutationReplayScopeV1",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md sec.1"
      ],
      "commandsWithNoSameNamedOperation": g("WF-11-command-name-to-mutationClass-mapping",
                                            "commandsWithNoSameNamedOperation"),
      "impact": "mutationClass is a public envelope field and MutationReplayScopeV1.operation "
                "equals it, so it enters the H(workflow.mutation-intent, scope) preimage of "
                "the published idempotencyKey; the Command record carries no mutationClass "
                "field",
      "boundedImpact": "requestId is host-minted and unique per invocation, so a spelling "
                       "difference cannot cause a false or missed dedupe across hosts and "
                       "the key grants no authority",
      "remedy": "add mutationClass to the Command record, or publish the map beside the "
                "MutationOperation enum",
      "vector": "GAP-3-command-name-to-mutationClass-mapping-unpublished"
    },
    {
      "id": "SHOULD-2",
      "title": "The Coverage-partition \"without omissions\" clause has no decidable "
               "referent for symbol relations",
      "selectors": [
        "docs/v2/contracts/product-v1/identity-and-evidence.md sec.3 "
        "(\"Coverage scopes partition the claimed universe without overlaps or omissions\")",
        "docs/v2/contracts/product-v1/native-evidence.md sec.1.2 "
        "(\"Which relations owe totality is stated in the relation registry "
        "(coverageTotality), where only `file` has a row, and never inferred.\")",
        "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry"
        "/relations/file/coverageTotality"
      ],
      "impact": "the overlap half is decidable; the omission half is not, for the nine "
                "symbol-kind relations, because native sec.1.2 itself states the "
                "enumerator's symbol-to-file attribution is trusted and not re-derivable "
                "from the retained Run and no symbol-universe enumeration is published",
      "remedy": "reconcile the two statements in text: say that the omission half is "
                "discharged by the coverageTotality registry and applies only to relations "
                "with a row there, and keep the overlap half as the general rule",
      "readingUsedInThisReconstruction": "the registry reading; overlap-freedom enforced "
                                         "separately",
      "vector": "GAP-4-coverage-partition-omission-clause-has-no-decidable-referent-for-symbol-relations"
    }
  ],

  "advisories": [
    {"id": "ADV-1",
     "title": "js-synthesized recognition (sec.1.2) vs the U-1 unit-marker rule (sec.1.4)",
     "selectors": ["docs/v2/contracts/product-v1/native-evidence.md sec.1.2 language-mode table",
                   "docs/v2/contracts/product-v1/native-evidence.md sec.1.4 U-1"],
     "summary": "under U-1 the 'or any .js file under the unit' disjunct is unreachable, so a "
                "directory of bare .js files is not a unit; an implementer reading sec.1.2 "
                "alone would mint one, changing membership and the Plan",
     "readingUsed": "U-1", "blocking": False,
     "vector": "GAP-5-js-synthesized-recognition-vs-U-1-unit-markers"},
    {"id": "ADV-2",
     "title": "The scope of native.confidence.v1's \"no value below 1000000\" clause",
     "selectors": ["docs/v2/contracts/product-v1/native-evidence.md sec.4.8",
                   "docs/v2/contracts/product-v1/native-evidence.md sec.4.6"],
     "summary": "the clause is unscoped but sec.4.6's own named regression case exercises a "
                "clones fact at 100000; it must be read as scoped to the types@checked "
                "method it defines",
     "readingUsed": "types-scoped", "blocking": False,
     "vector": "GAP-6-native-confidence-v1-scope"},
    {"id": "ADV-3",
     "title": "The successor D9 artifact is a live cross-unit obligation, correctly disclosed",
     "selectors": ["docs/v2/contracts/product-v1/native-evidence.md sec.10",
                   "docs/coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps/faultCauseToErrorCode"],
     "summary": "the inherited artifact keeps its bytes and omits the host-invariant cause, "
                "so a checker reading it alone would refuse a lawful host-invariant "
                "termination; the contract states this and attributes it",
     "blocking": False,
     "vector": "WF-8-selected-D9-extension-checked-against-the-inherited-contract"}
  ],

  "d9ExtensionCheck": {
    "againstInheritedContract": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
    "addedMember": "faultCause host-invariant -> SYSTEM.OUTCOME.ILLEGAL_STATE",
    "errorCodeAlreadyInTheInheritedClosedVocabulary": True,
    "hadNoCausePreimageInEitherInheritedMap": True,
    "successorMapStillInjective": True,
    "noNewClassExitReasonOrErrorCode": True,
    "declaredPrecedence": ["faultCause", "rejectionCause", "deficiency"],
    "precedenceRespected": True,
    "isAVocabularyExtension": True,
    "conclusion": "the selected extension is consistent with the inherited contract and its "
                  "declared precedence"
  },

  "requiredInvention": [
    {"item": "path -> TypeScriptConfigGraphV1 node kind", "grade": "MUST-2",
     "choiceMade": "exact basename", "movesIdentity": "RunId"},
    {"item": "the value for EvidenceRequirement.deficiency in the four inexpressible cases",
     "grade": "MUST-1", "choiceMade": "field left absent rather than write a refused or "
                                      "lossy value", "movesIdentity": "no"},
    {"item": "waive -> waiver-change (and two siblings)", "grade": "SHOULD-1",
     "choiceMade": "the obvious rename", "movesIdentity": "the operational idempotencyKey"},
    {"item": "the referent of \"the claimed universe\"", "grade": "SHOULD-2",
     "choiceMade": "the coverageTotality registry reading", "movesIdentity": "no"}
  ],

  "algorithmFreedomNotCountedAsAGap": [
    "clones near-v1 Jaccard shingling", "tsjs-erasure-v1 projection internals",
    "query planning (an optimization only, held to agree with a retained full scan)",
    "which spans a producer cites for a source-text fact (no cross-provider anchor "
    "identity is promised)",
    "the internal diagnostic key space behind the registered public keys",
    "the physical storage carrier"
  ],

  "limitations": [
    "Design reference exercise only: no product qualification, no implementation "
    "authorization, no readiness grade.",
    "Every OS, filesystem, compiler, Cargo, provider, cryptographic and SQLite observation "
    "is a synthetic trusted observation - an assumption, never native enforcement proof.",
    "No compiler, repository code, provider, renderer, ledger or filesystem was executed.",
    "Closures, trees, manifests and signatures are synthetic; no trust claim is made.",
    "Security S4/S5/S6/S7/S9 (time, root chain, revocation, leases, migration) were read "
    "only as far as the reconstruction's joins required; a separate pass is owed for them.",
    "Byte values depend on synthetic inputs; what is independently meaningful is the recipe, "
    "the refusals and the disagreements between two conforming readings.",
    "Only schemas present in the kit were validated against."
  ],

  "verdictRationale":
    "Every promised vector was constructible from these inputs alone except the one MUST-1 "
    "blocks, and the two identity-critical recipes most likely to be under-specified - the "
    "subjectScopeCommitment producing recipe and the Rust compilation-unit dialect selection "
    "- are closed, precise and reproduced exactly by an independent implementation. The two "
    "MUST issues are narrow, precisely located and independently fixable, and neither is "
    "architectural; both are the same class of defect this contract set has already "
    "corrected twice on its own initiative, and both would defeat the property it most "
    "insists on - independent replay across machines. That is why they block rather than "
    "advise."
}

p = os.path.join(OUT, "blind-review.json")
with open(p, "w") as f:
    json.dump(doc, f, indent=1, ensure_ascii=False)
print("wrote", p)
print("verdict", doc["verdict"], "| MUST", len(doc["newMustIssues"]),
      "| SHOULD", len(doc["newShouldIssues"]),
      "| ADV", len(doc["advisories"]))
print("hashes", ok, "/", len(MAN["files"]), "| negatives", neg_total,
      "| unexpected", unexpected)
