import json
O = "/tmp/opensip-design-corrections/post-reset-review.v14"
r = json.load(open(O + "/review.partial.json"))

r["priorFindingDispositions"] = {
 "CB4-MUST-1": {
  "severity": "MUST", "disposition": "RESOLVED", "resolvedInThisCandidate": True,
  "finding": "Anchor cardinality for inventory (and symbol) facts was decided nowhere; under a syntax "
             "universe the two lawful readings differ in ADMISSIBILITY.",
  "whatTheCandidateDid":
    "A closed `anchorLaw` is added to the relation registry on EVERY one of the 13 relations, in three "
    "classes: source-text (9 code relations, minimum 1), body-identity (clones, exactly 1) and "
    "inventory (file/package/vcs-change, exactly 0). It is applied in identity-model "
    "relation_payload_rules BEFORE the relation's snapshot joins, so the cardinality fault reports as "
    "itself. `coverageTotality` is added for file@enumerated only, matched on the four CoverageKeyV2 "
    "coordinates plus the owning snapshot.",
  "howIVerifiedIt":
    "48 of my own probe cases (p1: 35, p1b: 13) driven through complete Run admission, not schema "
    "fields. Positive controls each carry their own fact: zero-anchor file/package/vcs-change facts "
    "close a Run; anchored declares/references/imports/calls/types/reachability/unresolved-edge close; "
    "a single-anchor clones fact closes. Negatives: every inventory relation refuses a borrowed anchor "
    "AND a self-consistent anchor into its own path (FACT_ANCHOR_CARDINALITY:<rel>:inventory:"
    "expected=0:declared=1); every constructible source-text relation refuses unanchored under "
    "TypeScript, and separately under Rust and under syntax "
    "(FACT_ANCHOR_CARDINALITY:<rel>:source-text:minimum=1:declared=0), which is the cross-universe hole "
    "the finding implied; clones refuses at 0 and at 2. A drifted bodyIdentityJoin.anchorCardinality "
    "refuses with RELATION_ANCHOR_LAW_DRIFT and a relation with the law removed refuses with "
    "RELATION_ANCHOR_LAW_MISSING rather than defaulting.",
  "closedMinMax":
    "Closed on both ends. The minimum is per class in the registry; the MAXIMUM for source-text is the "
    "SHARED schema bound - fact.anchors maxItems 100000 with uniqueItems - which I checked is still "
    "present and which the class text explicitly declines to override with a per-relation ceiling. The "
    "registry also corrects an earlier revision that had claimed 'no upper bound at all'.",
  "rawByteRepresentability":
    "Verified by complete Runs, not by prose: an EMPTY file and arbitrary NON-UTF8 binary bytes are "
    "ordinary inventory, including at an extensionless path, with no invented UTF-8 decoding - at zero "
    "anchors the ANCHOR_SOURCE/ANCHOR_RANGE/ANCHOR_UTF8 loop never runs. The SAME non-UTF8 bytes still "
    "refuse as a code span (ANCHOR_UTF8), so the code-span laws kept their scope. Raw digest, byte "
    "length, path and snapshot ownership all still refuse a wrong claim (my S7/S8/S9).",
  "perUniverseTotality":
    "Confirmed, and this is the joined case the finding required. In one view carrying two COMPLETE "
    "file@enumerated scopes for a.ts in a TypeScript and a syntax universe, the TypeScript fact does "
    "NOT discharge the syntax scope (COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts); the "
    "two-universe Run in which each scope carries its own fact closes, and is retained as the positive "
    "control. package and vcs-change are correctly NOT total, so their empty complete results still "
    "close.",
  "locationRequirementsPreserved":
    "Finding/proof/repair locations are untouched: nothing reads fact.anchors as a finding location, "
    "and finding, finding-fingerprint, proof-bundle and predicate-witness carry no anchor field at all, "
    "so removing inventory anchors removes no route and invents none.",
  "limits": [
    "control-flow and literal are covered at registry level only. The candidate's own relation_fixture "
    "has no payload shape for them, so no complete Run can be built for those two by this harness "
    "(FIXTURE_RELATION_UNKNOWN). I did not score them either way. The enforcement is relation-generic - "
    "a single anchor_law(row, fact) call inside relation_payload_rules that runs for every fact - so "
    "there is no per-relation branch that could skip them, but that is an argument from the code path, "
    "not an exhibited Run.",
    "The two universe coordinates in coverageTotality.matchOn are verified JOINTLY load-bearing, not "
    "individually: `file` carries universeRule same-only, so a half-matching fact is refused by that "
    "prior law and the independence question is unreachable for this relation."],
  "evidence": ["evidence/probe-cb4-must-1.json", "evidence/probe-cb4-must-1-totality.json",
               "evidence/diffs/identity-and-evidence.md.diff", "evidence/diffs/native-evidence.md.diff"]},

 "CB4-MUST-2": {
  "severity": "MUST", "disposition": "RESOLVED", "resolvedInThisCandidate": True,
  "finding": "Section 10's Cause column named causes for three deficiencies the CLOSED NativeCause enum "
             "cannot express, so the only representable value was null - which that enum's own "
             "description defines as a disclosure owed and not made.",
  "whatTheCandidateDid":
    "A closed x-opensip-deficiency-cause-registry names, for every DeficiencyV2 member, WHICH existing "
    "structured carrier holds its cause: resolutionCompleteness (state + the set-valued "
    "unresolvedEdgeClasses), closedWorld.exportsClosed, derivationKinds, "
    "resolutionCompleteness.stageTerminal, or entry.nativeCause with a closed allowedCauses list. "
    "Where a row says nativeCause must be null, admission refuses unless the NAMED field actually "
    "carries the cause.",
  "namesCarriersNotAClosedEnum":
    "Confirmed as required, and confirmed NOT to be a new invented format: NativeCause is still 14 "
    "members, DeficiencyV2 still 9, UnresolvedEdgeKindV1 still 16 - byte-compared against v13, "
    "IDENTICAL. Nothing was widened to make the fix work.",
  "registryTotality": "Total over DeficiencyV2: 9 rows for 9 members, no uncovered member and no "
                      "extra row. A deficiency with no row is declared a registry defect and refuses.",
  "joinsProducerHostWireAdmission":
    "Verified at BOTH boundaries with my own cases. At the native producer boundary "
    "(admit_coverage_result_v3): a cause without a deficiency, a borrowed scalar cause, a relabelled "
    "cause, a wrong or null cause for language-tier-unsupported, derivation-policy-unmet on a "
    "references entry, an empty derivationKinds carrier, and external-consumers-unknown over a CLOSED "
    "world each refuse - and each with its OWN distinct key (native.coverage-cause-without-deficiency, "
    "-carrier-unsupported, -not-for-deficiency, -required, -relation-not-in-scope), not one generic "
    "fault. At RETAINED RUN CLOSURE, the same faults refuse again after I mutated the committed "
    "coverage payload and re-closed the Run, which is the verifier's path.",
  "derivationPolicyUnmetScoping":
    "Correct and enforced: the registry row carries relations: [types] and it is the ONLY row with a "
    "relations restriction. A references entry declaring derivation-policy-unmet while carrying "
    "compiler-inferred refuses with native.coverage-cause-relation-not-in-scope, at the producer "
    "boundary and again at Run closure. References and other relations cannot be qualified by it.",
  "rc3AndRequirementRelativeSufficiencyPreserved":
    "RC-3 survives and I exhibited it natively rather than forging it: a Run built with a real admitted "
    "unresolved-edge fact yields coverage complete, resolutionCompleteness.state incomplete and "
    "deficiency null, and closes. The registry states explicitly that the deficiency is NOT re-derived "
    "from the entry alone because several conditions are requirement-relative and RC-3 would otherwise "
    "refuse lawful Runs; only the decidable direction - a DECLARED deficiency must be supported by the "
    "entry's own committed evidence - is enforced. I also confirmed the set-valued carrier really is a "
    "set by closing a Run carrying two distinct unresolved-edge classes at once.",
  "selectedScalarLimitationIsExplicitAndNotOverclaimed":
    "Correct, and the candidate does not overclaim. The registry states per carrier what is retained: "
    "unresolvedEdgeClasses is a genuine set and loses nothing; closedWorld and derivationKinds are "
    "independent; but input-closure-incomplete's carrier is a SINGLE SCALAR NativeCause and a Run can "
    "genuinely be missing several inputs at once, so the retained cause is a SELECTED one, not the full "
    "set. It explicitly retracts an earlier revision that generalised 'loses nothing' to all carriers, "
    "and it introduces no multi-cause format to paper over the limit. This is exactly the honesty the "
    "finding needed and I did not find a place where a cross-relation scalar is claimed to encode every "
    "simultaneous deficiency.",
  "noHelperInventedFormat":
    "No new cause spelling appears anywhere: the carriers are pre-existing fields and the refusal keys "
    "are internal decision keys routed through the published public-route registry, not new cause "
    "values.",
  "evidence": ["evidence/probe-cb4-must-2.json", "evidence/probe-cb4-must-2-closure.json"]},

 "CB4-SHOULD-1": {
  "severity": "SHOULD", "disposition": "RESOLVED", "resolvedInThisCandidate": True,
  "finding": "The clones registry derived the body languageId from the fact sourceUniverse domain row's "
             "`language`, which yields typescript for a .js body and `syntax` - not in the closed enum - "
             "for any body under the syntax universe.",
  "whatTheCandidateDid":
    "bodyIdentityJoin.languageIdSource now reads bodyLanguageByVariant[<variant the closed suffix table "
    "selects from this anchor's path, longest match>] where dialect.form is closed-suffix-table, and "
    "bodyLanguage for any other dialect form, with a companion key stating it is emphatically NOT the "
    "domain row's `language` field. identity-and-evidence section 3 now spells the same rule.",
  "sameSelectedLanguageForPayloadAndIdentity":
    "Yes, and I checked the COMMITTED bytes rather than the sentence: for a .js body under "
    "native.semantic-universe.typescript.v2 the frame the Run actually committed contains `javascript` "
    "and does not contain `typescript`; under the grammar-only syntax universe a .rs body's committed "
    "frame contains `rust` and never `syntax`. Complete Runs close for clones under the TypeScript, "
    "Rust and syntax universes, and for a .js body under the TS engine universe.",
  "jsThroughTsEngineAndRustSelectedTarget":
    "Both covered. The TS row's table maps js/jsx/mjs/cjs to javascript and ts/tsx/mts/cts/d.ts to "
    "typescript; the syntax row additionally maps .rs to rust; the Rust row uses form "
    "selected-compilation-target-edition with bodyLanguage rust and a single-member bodyLanguages, so "
    "the selected target dialect - not the engine - decides. Every derived value is a member of the "
    "closed {javascript, rust, typescript} enum, which is unchanged.",
  "notInferredFromEnclosingUniverse":
    "Confirmed negatively too: an unlisted suffix REFUSES rather than being folded into a neighbouring "
    "variant (BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN under syntax, "
    "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN under TypeScript), driven through the model's own selector.",
  "framingAndOwnershipLimitsPreserved":
    "level/source/specification/compiler/normalizer framing is untouched: recomputableAt remains "
    "L0-verbatim only, the L1-L3 statement remains retained-preimage custody plus framed-identity "
    "rather than a normalizer qualification, and the raw-32-byte language-version component is "
    "unchanged. A clones SCOPE still closes where no body identity is admissible, so the honest "
    "indeterminate result is preserved.",
  "evidence": ["evidence/probe-cb4-should-1.json"]},

 "CB4-SHOULD-2": {
  "severity": "SHOULD", "disposition": "RESOLVED", "resolvedInThisCandidate": True,
  "finding": "requestedCapabilities[].capabilityId was free Text entering PlanId through "
             "analysisSpecDigest with no named vocabulary authority.",
  "whatTheCandidateDid":
    "native-capability-matrix.v2.json#/capabilities[].id is published as THE closed authority (11 "
    "members) with a capabilityIdLaw beside it; the analysis-spec field gains a shape pattern and an "
    "x-opensip-vocabulary authority pointer; membership is closed again at Plan/Run closure over the "
    "RETAINED spec; and a ReleaseCapabilityRegistryV1 schema is added for the authenticated release "
    "declaration.",
  "closedAuthority":
    "Verified: cells are exactly the complete product of 11 capabilities x 6 modes = 66, no id contains "
    "'@', and the law names the matrix selector. A relation@rung spelling is refused BY SHAPE before "
    "membership is consulted - both in the helper and over the retained spec at Run closure - and an "
    "unregistered id refuses with ANALYSIS_SPEC_CAPABILITY at closure.",
  "defaultFixedByMatrixNotByRelease":
    "This is the substantive half and it holds. The default request set is IDENTICAL under a full "
    "release registry and a starved one-row registry: the same capabilities are requested either way. "
    "UNSUPPORTED-TYPED cells are requested deliberately (references under syntax-only is requested), "
    "and only NOT-SELECTED cells are excluded (clones-cross-tsjs under syntax-only). An "
    "UNSUPPORTED-TYPED request is ADMISSIBLE and answered; a NOT-SELECTED request is refused as "
    "unsatisfiable. Explicit configuration overrides the request with its own provenance and the "
    "defaulted path records DEFAULTED.",
  "releaseDeclarationsCannotRedefinePromises":
    "Enforced: a row naming an unregistered capability, an unregistered mode, a NOT-SELECTED cell, or a "
    "duplicate capabilityId each refuses with its own key, and the registry text explicitly retracts an "
    "earlier 'a release need not ship everything' sentence that had let the default shrink silently.",
  "candidateOnlyCapabilities":
    "No fabrication. clones-near and clones-cross-tsjs have EMPTY matrix relations, carry "
    "projection: selection-account-only and an empty relations list, and mint no fact, no relation@rung "
    "and no Coverage entry; fact-producing capabilities carry projection: coverage-entry and name their "
    "exact coordinates. The disclosure is stated advisory - it terminates nothing, mints no Coverage, "
    "creates no Control verdict and fabricates no clone Candidate.",
  "disclosedInTheOriginalInvocation":
    "Yes, and with the complete ownership tuple in TYPED fields rather than a concatenated subject: "
    "each notice carries capabilityId, languageMode and the unit's own workspaceRoot, plus the single "
    "const code native.capability-unavailable and a remedy. Two workspaces requesting the same "
    "capability stay distinguishable (this is the case the earlier concatenated subject collapsed). "
    "Composition is per step: release_absence_notices yields the {noticeCount, notices} leaf, stepId is "
    "added to form the step, and invocation_availability composes {stepCount, totalNoticeCount, steps} "
    "on CommandEnvelope.availability.",
  "boundsAndHonestCounts":
    "A step's notices are bounded at 1024 - exactly the analysis-spec requestedCapabilities bound, so "
    "one absence per requested row makes overflow UNREACHABLE - and steps at 64, which is the "
    "invocation's own StepId 0-63 range rather than a new limit. Two steps of 1023 compose 2046 "
    "notices, the case one flat 1024 array would have refused. noticeCount equals each array's length "
    "and totalNoticeCount is their sum, exact at the edge. The helpers do not truncate, and a forced "
    "oversized step, a 65-step invocation and a stepId of 64 are each refused by the schema. A "
    "4000-character workspaceRoot survives intact because it is a UserInputPath (4096), never folded "
    "into a BoundedText (1024) subject.",
  "allSurfaceParity":
    "capability-availability is a DECLARED parityField of all five requestClass: analysis commands "
    "(default, analyze, fit, audit, repair-verify), so it reaches human, SARIF and HTML and not only "
    "JSON/agent. The render path's parity access is now strict, so a missing declared field fails as a "
    "required-delivery fault instead of silently rendering a partial result.",
  "compilerFreeReferencesPrecedence":
    "Preserved. references under syntax-only is an UNSUPPORTED-TYPED cell whose named deficiency is "
    "language-tier-unsupported, whose only lawful cause is capability-missing, and which OUTRANKS "
    "provider-unavailable in PRECEDENCE_V2. It is answered, never rejected merely because a provider is "
    "missing, and the release-absence account cannot override the more specific deficiency.",
  "unsupportedGrammarCannotClaimCompleteEmptyResults":
    "Verified by forging the false claim rather than assuming it: the honest answer "
    "(unknown / language-tier-unsupported / capability-missing) closes a Run and is retained as the "
    "positive control, while a forged coverage: complete with deficiency null refuses with "
    "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE and a relabelling to a weaker deficiency refuses with "
    "SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH.",
  "evidence": ["evidence/probe-cb4-should-2.json", "evidence/probe-cb4-should-2b.json",
               "evidence/probe-capability-bounds.json"]},

 "CB4-ADV-1": {"severity": "advisory", "disposition": "ADDRESSED-AT-ORIGINAL-SEVERITY",
   "basis": "The stale literal '60 cells' is gone; the prose now says the cells array is the complete "
            "product of the two arrays and the reference checks hold it to that product rather than to "
            "a hand-maintained number, which removes the class of defect rather than the instance. I "
            "measured 66 cells and the native check reports 'matrix cells 66'. "
            "validation-summary.v1.json now also carries 66. Original advisory severity preserved; the "
            "frozen v13 stale-60 record is retained as history."},
 "CB4-ADV-2": {"severity": "advisory", "disposition": "ADDRESSED-AT-ORIGINAL-SEVERITY",
   "basis": "Both prose enumerations now list the syntax universe and context domains: "
            "identity-and-evidence section 3 says 'All three universe domains' and names "
            "native.semantic-universe.syntax.v2, and native section 11 lists both "
            "native.semantic-universe.syntax.v2 and native.context.syntax.v2. The machine-readable "
            "domainSets registry remains the dispatch authority and is unchanged in that role."},
 "CB4-ADV-3": {"severity": "advisory", "disposition": "ADDRESSED-AT-ORIGINAL-SEVERITY",
   "basis": "The four effect-name to permission-token mappings are now published as a table "
            "(subprocess/PT-PROC-EXEC-DECLARED, filesystemWrite/PT-FS-WRITE-HOST-STATE, "
            "network/PT-NET-EGRESS, environment/PT-ENV-READ) against the pinned seven-token v9 table, "
            "with three scope facts that must travel with it: the values are per execution mode, "
            "PT-FS-WRITE-HOST-STATE is not repository filesystem authority, and PT-HOST-EFFECT-BROKERED "
            "plus the two read-only tokens are deliberately unprojected. Confinement is explicitly not "
            "claimed, so the mapping grants no enforcement and no qualification - the advisory's limit "
            "is preserved, not upgraded."},
 "CB4-ADV-4": {"severity": "advisory", "disposition": "ACCOUNTED-NOT-LIFTED-AT-ORIGINAL-SEVERITY",
   "basis": "identity-and-evidence now states the limitation is accounted rather than lifted: today's "
            "two parameter rows are distinguishable, the same policy-document bytes named by "
            "plan.policyDigest/waiverDigest sit in a different payload class outside this key space, "
            "and a FUTURE second parameter row selecting another $def out of an already-cited document "
            "is a refusal (PAYLOAD_PARAMETER_AMBIGUOUS_ROW) rather than a defect. Re-keying by "
            "(document, selector) is explicitly declined as widening a closed key space for a "
            "requirement that does not exist. The advisory's limit is preserved and nothing is "
            "silently widened."},
}

r["newAdvisories"] = [
 {"id": "V14-ADV-1", "severity": "advisory",
  "title": "native-evidence section 10 ends with the unqualified sentence \"No new public code is added "
           "and none is needed\", while section 13 of the same document adds four DomainDetailCode "
           "members. Both are true under their own scopes; the section 10 sentence is not scoped in its "
           "own text.",
  "selectors": ["docs/v2/contracts/product-v1/native-evidence.md:2267",
                "docs/v2/contracts/product-v1/native-evidence.md:2376-2385",
                "docs/coop/design-corrections/public-detail-registry.v1.json#/newInThisCorrection"],
  "why": "Section 10's paragraph is about how a lawful entry's DEFICIENCY and CAUSE reach the public "
         "surface, and for that route no new code is indeed added. The four added members "
         "(native.capability-spec-invalid, native.release-declaration-invalid, "
         "native.coverage-cause-unsupported, HOST.INVARIANT_VIOLATED) serve REFUSAL branches, and one of "
         "them is named for the Coverage-cause route section 10 is discussing, so the two sentences read "
         "as contradictory ~110 lines apart.",
  "whyNotAMustOrShould": "Nothing is unrepresentable or ambiguous. The machine-readable registry is "
         "unambiguous, records the four additions with their reasons under an explicit "
         "newInThisCorrection key, and section 13 discloses them prominently; an implementer builds from "
         "the registry and reaches the same result either way. No admission, identity or D9 outcome "
         "differs. This is the same class of prose-versus-registry staleness Bv4 itself raised as "
         "ADV-1 and ADV-2.",
  "suggestedRepair": "Scope the sentence, e.g. 'No new public code is added for this projection route'; "
                     "or cross-reference section 13.",
  "evidence": "Measured: public-detail-registry codes went 283 -> 287 with 0 removed."},
 {"id": "V14-ADV-2", "severity": "advisory",
  "title": "The anchorLaw's enforcedAt claims the producer boundary AND retained Run closure, but the "
           "reference model exposes only the Run-closure call site.",
  "selectors": ["docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
                "#/x-opensip-relation-registry/anchorLaw/enforcedAt",
                "docs/coop/design-corrections/foundation/identity-model.py:939"],
  "why": "anchor_law is reachable only through relation_payload_rules, which is nested inside "
         "open_run_closure; every path to it (including admit_cache_entry) goes through that closure. "
         "So the reference evidence demonstrates enforcement at retained Run closure only. By contrast "
         "the deficiency-cause registry's enforcedAt names admit_coverage_result_v3 AND close_run, and I "
         "independently exercised BOTH - so the asymmetry is visible within this same correction.",
  "whyNotAMustOrShould": "The safety-relevant direction is fully demonstrated: retained Run closure is "
         "the verifier's path, and a fact that would violate the law cannot be committed. The native "
         "producer is outside this reference model's scope and its conformance is already future "
         "qualification work, so this is a scope-of-evidence precision issue in a registry sentence, not "
         "a gap in the law or in what is representable.",
  "suggestedRepair": "Either narrow enforcedAt to what the reference model exhibits, or name the "
                     "producer-boundary call site the way the cause registry names "
                     "admit_coverage_result_v3."},
]

r["carriedAdvisoryAccount"] = {
 "path": "docs/coop/design-corrections/reviews/codex-post-reset.v1/advisory-application-account.v14.proposed.json",
 "count": 43, "v13Count": 37, "added": 6, "removed": 0, "changed": 0,
 "addedIds": ["CLAUDE-V13-ADV-1", "CLAUDE-V13-ADV-2", "CB4-ADV-1", "CB4-ADV-2", "CB4-ADV-3", "CB4-ADV-4"],
 "basis": "I diffed the v13 and v14 accounts item by item. All 43 are individually carried with their own "
          "id, disposition and subsequentReviewEvidence; no prior disposition text was altered and none "
          "was removed. Each preserves its own limit - the effect/token mapping disposition still says it "
          "grants no permission, enforcement claim or qualification, and the parameter-key disposition "
          "still says a future second selector requires a separately designed change. Nothing was "
          "silently upgraded or erased.",
 "note": "My two new advisories above are NOT added to that account; they are this review's output and "
         "the account is the candidate's own record."}

r["productQualificationGates"] = {
 "count": 32, "demonstrated": 0, "qualified": 0, "implementationHarnessAuthored": 0,
 "platformFamilies": ["linux-x86_64-gnu", "linux-aarch64-gnu", "macos-aarch64", "macos-x86_64"],
 "basis": "Independently enumerated from qualification-gates.proposed.json in the frozen v14 bytes: 32 "
          "items, every one demonstrated=false and qualified=false, over exactly the four D-371 machine "
          "ids (two macOS, two Linux). The file is byte-identical to v13. Nothing in this delta "
          "demonstrates or qualifies a gate, and this review does not."}
r["evaluationSubresiduals"] = {
 "count": 30, "disposition": "CARRIED-UNCHANGED",
 "source": "docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json",
 "basis": "30 items, and the file is byte-identical between v13 and v14 (cmp). Preservation only."}

r["preservationOfPreviouslyConfirmedBehaviour"] = {
 "method": "Targeted probes where the delta's changed paths can reach a safeguard; otherwise carried on "
           "the reproduced suite rather than restated. The candidate's own identity suite (1282 checks) "
           "runs green inside my harness on every probe module.",
 "probed": {
   "canonicalTypedAnnotationEqualityAndBoolIntDistinction": "HOLDS - bool is not equal to int under "
     "equal_typed and canonical encoding distinguishes them; '1' is not 1 and None is not False.",
   "arrayOrderLaws": "HOLDS - a mis-ordered canonical set refuses, the correctly ordered one admits; the "
     "same law refused two of my own malformed release-registry fixtures before I sorted them.",
   "thirteenRelationSelectorsAndRungs": "HOLDS - 13 relations each with a non-empty ladder, the registry "
     "is the single ladder authority, and a rung borrowed from another relation's ladder refuses.",
   "snapshotOwnedFileClaims": "HOLDS - wrong content digest, wrong byte length and a path outside the "
     "snapshot each refuse.",
   "fullTsJsRustAndSyntaxClosure": "HOLDS - complete Runs close under the TypeScript, Rust and "
     "grammar-only syntax universes, and for a .js body under the TS engine universe.",
   "raw32CompilerDialectCloneVersionAndRustTargetEdition": "HOLDS - the language-version component is "
     "raw 32 bytes; Rust selects its dialect from the compilation target edition with five separately "
     "named ownership faults.",
   "unavailablePartialOwnershipEmptyControls": "HOLDS - a clones scope still closes where no body "
     "identity is admissible, so the honest indeterminate result survives.",
   "syntaxOnlyCodeAndDataGrammarRepresentability": "HOLDS - inventory facts close for tool/main.py, "
     "LICENSE and docs/extra.md under a grammar-only repository.",
   "scopeDocumentParameterBinding": "HOLDS - the parameter payload class stays keyed and closed and an "
     "unregistered parameter document refuses.",
   "requiredOutputFailureAfterCommittedRun": "STRENGTHENED by this delta - render's parity access is now "
     "strict, so a missing declared parity field fails as a required-delivery fault "
     "(DELIVERY.REQUIRED_FAILED, faultCause delivery-required) instead of silently vanishing from all "
     "five formats. An earlier `if k in envelope['parity']` guard had weakened this for EVERY declared "
     "parity field.",
   "d9FaultCauseMappings": "HOLDS - 0 inherited mappings changed, exactly 1 added."},
 "carriedOnReproducedSuiteNotReprobed": [
   "local cycles and missingness laws", "retained ordered/repeated config and node_modules layout",
   "imported observation evidenceUse at retained Run admission", "cache validated-hit boundary",
   "mutation/repair replay", "purge public disclosure and leased pin ledger"],
 "basisForCarrying": "These families' owning files are outside the 12 normative modified paths, and the "
   "reference suites that exercise them reproduce byte-identically. Refer to the full v13 independent "
   "review for the inherited exact evidence and its limitations; I did not regrade unchanged paths by "
   "restating them."}

r["normativeProseAssessment"] = {
 "verdict": "SUBSTANTIVELY IMPROVED, with one scoping wrinkle raised as V14-ADV-1",
 "notes": [
   "The corrections argue from the defect rather than asserting a rule: each names the exact frozen-v13 "
   "graph that closed and should not have (both spellings of one file@enumerated claim with different "
   "fact2 identities; a package fact anchored into an unrelated file; an unanchored code fact under a "
   "compiler universe; a complete file@enumerated scope with zero facts; a TypeScript fact paying a "
   "syntax scope's obligation). I verified several of these are genuinely refused now.",
   "Retractions are explicit rather than quiet: the 'no upper bound at all' anchor claim, the 'a release "
   "need not ship everything' scope sentence, the 'loses nothing' multi-cause generalisation, the claim "
   "that all 14 keys belonged in the context-free alias map, and the claim that the D9 maps were "
   "non-total are each named as wrong and corrected. That is the right behaviour for a normative "
   "document and it made my job easier, not harder.",
   "Limits are stated instead of engineered around: the selected-scalar cause, the requirement-relative "
   "sufficiency conditions, the SHA-256 collision-resistance assumption being ordinary rather than an "
   "impossibility claim, and the absence of any promised retained store for an elided subject."]}

r["limitations"] = [
 "This is a DESIGN and REFERENCE review. Every native, compiler, OS, cryptographic, storage, grammar and "
 "provider observation in the reference model is a SYNTHETIC TRUSTED ASSUMPTION, not measured "
 "enforcement. No compiler, cargo, parser, toolchain or repository code was executed and no platform was "
 "qualified.",
 "control-flow and literal are not constructible by the candidate's own relation fixture, so those two "
 "relations are covered at registry level only and not through a complete Run.",
 "The two universe coordinates of coverageTotality.matchOn are verified jointly, not individually, "
 "because universeRule same-only makes divergence unreachable for `file`.",
 "The anchor law's producer-boundary enforcement is asserted but not exhibited by a second call site in "
 "the reference model (V14-ADV-2); only retained Run closure is demonstrated.",
 "I read the full Bv4 blind report and its companion Markdown, the v14 dispositions, the coauthor v3 "
 "handoff and root assessments and the preserved v1/v2 handoffs, but I did not re-derive the blind "
 "reconstruction itself; this review makes no statement about blind reconstructability.",
 "Application and readiness records were not graded. Five owner routing assessments do not grant final "
 "application outcomes.",
 "Passing my probes shows a lawful graph is constructible and that the named refusals actually fire; it "
 "does not show any implementation is correct."]

r["claimsExplicitlyNotMade"] = [
 "product qualification", "platform qualification", "implementation authorization",
 "application acceptance or readiness change", "blind reconstructability",
 "a substitute for the separate new blind review on the accepted normative bytes",
 "a substitute for the separate full application review"]

r["requiredNextActs"] = [
 "NEW fresh blind review on these accepted normative bytes - a separate gate, and not a reason to reject "
 "this otherwise coherent pending design.",
 "Separate full application review to grade the proposed readiness and evaluation records.",
 "Optionally, the two advisory repairs above; neither blocks."]

r["readinessChanged"] = False
r["implementationAuthorized"] = False
r["productQualification"] = False
r["applicationAccepted"] = False
r["blindAccepted"] = False

json.dump(r, open("/tmp/opensip-design-corrections/post-reset-review.v14/review.json", "w"), indent=1)
print("verdict:", r["overallVerdict"],
      "| MUST:", len(r["newMustIssues"]), "| SHOULD:", len(r["newShouldIssues"]),
      "| advisories:", len(r["newAdvisories"]),
      "| priorFindings:", len(r["priorFindingDispositions"]),
      "| probes:", r["independentProbeCaseTotal"])
