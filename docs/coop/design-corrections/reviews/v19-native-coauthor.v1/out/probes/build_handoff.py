import hashlib, json, pathlib

ROOT = pathlib.Path('/private/tmp/opensip-design-corrections/v19-native-coauthor.v1')
W = ROOT / 'work'
FROZEN = json.loads((ROOT / 'out/evidence/before-hashes.json').read_text())


def sha(rel):
    return hashlib.sha256((W / rel).read_bytes()).hexdigest()


CHANGED = [
    ("docs/coop/design-corrections/native/native_evidence_model.v2.py", "source",
     "CB7-MUST-1 source_variant_of_path / source_variant_capability_support / SCOPE_CAPABILITY_LAW read + producer-boundary hook in admit_coverage_result_v3; CB7-SHOULD-2 PLAN_SELECTION_FIELDS / plan_selection_bound / admit_plan_selection_cardinality, three new SCOPE_LIMIT_REMEDY rows, accounting inside plan_native_context_digests; CB7-ADV-4 PROTOCOL3_PHASES/RULES now read from the published artifact and protocol3_run gains an optional `rules` argument."),
    ("docs/coop/design-corrections/foundation/identity-model.py", "source",
     "CB7-MUST-1 coverage_source_variant_prerequisite plus its close_run call site (ordered after the two more specific guards), and close_run now hands the owning universe dialect to the producer boundary."),
    ("docs/coop/design-corrections/foundation/identity-schemas.v2.json", "source",
     "CB7-MUST-1 x-opensip-digest-domains/scopeCapabilityLaw: the published scope-capability law for closed-suffix-table universes."),
    ("docs/coop/design-corrections/integration-fixtures.py", "source",
     "CB7-MUST-1 producer construction branch for closed-suffix-table universes; CB7-SHOULD-2 pre-Plan boundary on the real Plan construction path."),
    ("docs/coop/design-corrections/foundation/check-identity.py", "source (reference controls)",
     "Mirrored producer helper (proved byte-identical before the change), the pre-Plan boundary on its Plan construction path, two new optional build() parameters, and 85 net new controls for MUST-1, SHOULD-2 and ADV-4. Two existing controls updated: one refusal boundary that legitimately moved, and the two bounded-field counting controls."),
    ("docs/v2/contracts/product-v1/native-evidence.md", "normative prose",
     "S1.2 scope-guard claim corrected and the source-variant law introduced; S10 states the source-variant scope law and why it is not the OWNER_NOT_COMPILED treatment; S9.2 publishes the transition artifact; S14 bounded-selection paragraph widened from four fields/two families to seven/three."),
]
NEW = [("docs/coop/design-corrections/native/protocol3-transitions.v1.json", "source (new artifact)",
        "CB7-ADV-4 the 34 transition rows, phases, wildcard vocabulary, match/guard/terminal law, state updates, the stage-dependent transition and the explicit prose-owned list. Generated from the exact existing rows; the model now reads it.")]

changed_files = []
for rel, kind, why in CHANGED:
    changed_files.append({"path": rel, "kind": kind, "frozen18Sha256": FROZEN[rel],
                          "v19Sha256": sha(rel), "changedThisTurn": True, "why": why})
for rel, kind, why in NEW:
    changed_files.append({"path": rel, "kind": kind, "frozen18Sha256": None,
                          "v19Sha256": sha(rel), "changedThisTurn": True, "newFile": True, "why": why})

doc = {
  "handoff": "opensip.design-corrections.v19-native-coauthor.v1",
  "role": "actual Claude SOURCE COAUTHOR, working with Codex; NOT the independent reviewer of these changes",
  "standing": "PROPOSED source delta. No grade is minted, no independent acceptance is claimed, and a fresh successor freeze, independent source review and NEW blind review remain required.",
  "inputCustody": {
    "beforeCopy": "/tmp/opensip-design-corrections/v19-native-coauthor.v1/work",
    "manifest": "docs/coop/design-corrections/reviews/candidate-subject.v18.json",
    "manifestSha256": "cd6e828c22c6bc0ecf07ab8fe1f4bd5d1a5a8726708e0deffac99960bdc25a44",
    "declaredFiles": 7864, "declaredBytes": 544831302,
    "verified": {"missing": 0, "mismatched": 0, "undeclared": 0},
    "filesAfter": 7865,
    "note": "The only difference between `work` and the frozen18 subject is the seven entries below. docs/coop/design-corrections/reviews/NEXT-REVIEW.md differs from the CURRENT live repository but is byte-identical to the frozen subject; the live repository has moved since the freeze and was read, never written."
  },
  "technicalAssent": {
    "value": True,
    "scope": "I assent to the exact proposed bytes in `changedFiles` as a correct and minimal closure of CB7-MUST-1, CB7-SHOULD-2 and CB7-ADV-4 on existing law, under the stated limitations. This is an author's assent to his own delta; it is not review, acceptance or qualification.",
    "notAssentedTo": [
      "CB7-SHOULD-1: source untouched pending root's clarification with the original blind reviewer. An initial disposition is given and is explicitly not a change proposal.",
      "Any claim of host, compiler, grammar, OS or platform enforcement. Every guard here is a reference-model admission boundary over synthetic trusted observations.",
      "Source pins, records, lineage or freeze, which root owns."
    ]
  },
  "changesRequired": [
    {"id": "V19-ROOT-1", "owner": "root", "statement": "docs/coop/design-corrections/native/protocol3-transitions.v1.json is a NEW file and has no row in native/source-pins.v2.json. Root owns the pin ledgers; the native checker verifies only listed pins, so its absence does not fail any check today, but the artifact is now a real input of native_evidence_model.v2.py and should be pinned when the six canonical checks are resealed."},
    {"id": "V19-ROOT-2", "owner": "root", "statement": "The same artifact is the subject of CB7-ADV-4 and needs adding to the NEXT blind kit selector, which is root's orchestration and was not touched here."},
    {"id": "V19-ROOT-3", "owner": "root", "statement": "All five pin ledgers now disagree with the changed sources, by construction. Every local result below was obtained either without the pin gate (check-identity, check-integration, check-foundation, check-array-orders, check-product-configuration, check-product-quality) or in a DISPOSABLE repinned copy outside `work` (check_native_evidence.v2, check-security-lifecycle.v1). No pin in `work` was edited and no pin match is claimed."}
  ],
  "findings": [
    {
      "id": "CB7-MUST-1", "disposition": "agreed and closed", "sourceChanged": True,
      "rootPreferredSemantics": "examined critically and adopted, with one refinement",
      "assessment": "The gap reproduces exactly as the blind measured it. `coverage_dialect_prerequisite` returns early unless the universe dialect carries an `ownership` key, which only Rust does, so a `clones` scope over `package.json` under the TypeScript universe reached no classification and closed a Run with coverage `complete`, deficiency null and zero facts. `body_language_version` does refuse an unlisted suffix with BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN, but only while a body is being derived, and a scope with no facts derives none.",
      "whyRootsReadingIsSound": "The alternative reading - treat an unlisted suffix like BODY_LANGUAGE_OWNER_NOT_COMPILED and leave `complete` lawful - is unsound here and the difference is substantive. OWNER_NOT_COMPILED describes a path that IS a Rust source file which no selected target compiles: the universe examined a known-language file and correctly produced no fact, so a determinate answer is honest. A suffix outside the closed table is not a body of that universe in any dialect, so `complete` would assert a negative from an absent capability - exactly what the syntax universe's grammar-capability law already refuses. Existing vocabulary suffices: language-tier-unsupported / capability-missing, no new deficiency, NativeCause or DomainDetailCode, and no schema enum changed.",
      "refinementProposed": "The law is NOT TypeScript-specific and must not be written as if it were. The syntax universe's dialect form is ALSO `closed-suffix-table`, so the correct gate is the dialect FORM, not a universe id. For the syntax universe the new condition is strictly implied by its own grammar registry, because the published grammar-capability classLaw states that no data-document suffix appears in the syntax dialect table; the grammar guard therefore runs FIRST at retained closure and keeps its own refusal names, and the source-variant guard is the backstop that makes the set of published universes total.",
      "totalityOfTheThreeUniverses": {
        "rust": "unchanged: selected-compilation-target-edition, clone_ownership_disclosure and the four COVERAGE_DIALECT_* refusals. Enumeration/selection distinctions and body identities for known variants are untouched.",
        "typescript": "the new coverage_source_variant_prerequisite is its ONLY scope-capability owner; its onUnknown remains the per-body refusal and is unchanged.",
        "syntax": "syntax_capability_prerequisite still owns every symbol relation and the selection case where a suffix IS in the dialect table but no selected grammar row owns it. Its dialect onUnknown (BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN) stays DEFENSIVE-ONLY: the scope guard refuses before a body is created, and no new authority over grammars or compilers is asserted anywhere."
      },
      "boundaries": {
        "producerAdmission": "admit_coverage_result_v3 gains an optional `universe_dialect` supplied by the caller that holds the retained universe record - the reference producer and close_run both do. Refusals native.coverage-source-variant-{unsupported-complete,deficiency-mismatch,cause-mismatch} under PROVIDER.PROTOCOL_VIOLATION. HONEST LIMIT: this boundary judges one record and never sees the snapshot, so it applies the law only where the scope carries its own paths (a source-path subject kind under a body-dialect relation), and a caller that supplies no dialect gets today's behaviour here.",
        "retainedRunClosure": "coverage_source_variant_prerequisite is UNCONDITIONAL in close_run and does not depend on any caller passing anything. Refusals COVERAGE_SOURCE_VARIANT_{UNSUPPORTED_SCOPE,DEFICIENCY_MISMATCH,CAUSE_MISMATCH}.",
        "factBoundary": "already total before this change and deliberately not duplicated: body_language_version refuses the unlisted suffix at the point a body is derived."
      },
      "subjectLaw": "Gated on the relation registry's bodyIdentityJoin, which today is `clones` alone, so nothing here claims a suffix table decides symbol capability. `clones` is a source-path relation, so ALL of the scope's own subjects must have a registered variant: a mixed src/a.ts + package.json scope discloses instead of hiding its unsupported half, and an empty subject list is unsupported rather than vacuously complete. INVENTORY_CAPABILITIES are exempt both by that gate and inside the derivation, so file/package/vcs-change remain lawful on every inventoried path. The symbol branch mirrors the syntax guard for a future row and is NOT reachable under today's registry - stated rather than claimed as live.",
      "derivedNotAsserted": "The classification is computed from the owning universe record's published table and the scope's subjects. Nothing is read from the payload; a control feeds the identical payload and scope under a dialect whose table registers the suffix and shows it then admits.",
      "measuredBeforeAndAfter": {
        "package.json clones scope under TypeScript, no facts": {"before": "run2 sealed, coverage complete, deficiency null", "after": "run2 sealed, coverage unknown, language-tier-unsupported / capability-missing"},
        "a.py clones scope under TypeScript": {"before": "complete", "after": "unknown / capability-missing"},
        "a.ts, a.d.ts, a.tsx clones scopes with NO clone body": {"before": "complete", "after": "complete (unchanged - the positive control)"},
        "src/plain.rs under Rust": {"before": "complete", "after": "complete (unchanged)"},
        "README.md clones scope under syntax": {"before": "unknown / capability-missing", "after": "unknown / capability-missing (unchanged)"}
      },
      "existingControlThatMoved": {
        "id": "injected-false-complete-for-a-markdown-scoped-clone-refuses",
        "was": "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE at retained closure",
        "now": "COVERAGE_PRODUCER_ADMISSION:native.coverage-source-variant-unsupported-complete at the producer boundary, one layer earlier",
        "why": "The syntax dialect table does not contain .md, so the general law sees the same defect at the earlier boundary. The claim still dies and the coverage entry content is identical; only the diagnostic name changed. The control was NOT weakened: it now asserts the exact earlier refusal, a companion asserts the producer boundary is the one that refused, and two NEW controls prove the syntax grammar guard still solely owns the case the dialect table provably cannot see (.tsx in the table, its grammar row dropped from the bundle).",
        "disclosedRisk": "A reviewer may reasonably prefer the more specific syntax refusal to survive at the producer boundary. I judged that the earliest boundary able to see a provider's false claim should refuse it, and that the source-variant reason is the more fundamental one. If root or the independent reviewer disagrees, the narrow alternative is to condition the producer hook so it makes no claim for a universe owned by a more specific capability law; that is a small, contained change and I do not object to it."
      },
      "controlsAdded": ["the-published-scope-capability-law-and-the-model-do-not-drift", "the-published-inventory-exemption-is-the-one-the-model-applies", "the-source-variant-law-reads-the-supplied-registry-table-and-not-a-private-copy", "the-typescript-body-axis-is-a-closed-suffix-table-with-no-ownership-key", "every-published-universe-now-has-an-owning-scope-law", "a-registered-suffix-selects-its-variant-and-longest-match-wins", "a-supported-code-scope-is-not-made-unavailable", "an-unregistered-suffix-scope-is-unavailable-with-the-published-pair", "a-mixed-source-variant-scope-cannot-hide-its-unsupported-part", "an-empty-source-variant-scope-is-not-vacuously-supported", "inventory-capability-is-never-source-variant-gated", "a-universe-with-no-suffix-table-is-not-owned-by-this-law", "a-package-json-scoped-typescript-clone-request-closes-as-disclosed", "an-unlisted-suffix-scoped-typescript-clone-request-closes-as-disclosed", "a-supported-typescript-clone-scope-with-no-body-still-closes-complete.{ts,declaration,tsx}", "a-rust-clone-scope-is-unaffected-by-the-source-variant-law", "the-disclosed-typescript-clone-scope-really-has-no-facts", "injected-false-complete-for-a-package-json-clone-scope-refuses", "injected-wrong-cause-for-an-unsupported-source-variant-refuses", "injected-wrong-deficiency-for-an-unsupported-source-variant-refuses", "the-producer-boundary-admits-the-disclosed-unsupported-scope", "the-producer-boundary-refuses-a-false-complete-for-an-unsupported-scope", "the-producer-boundary-refuses-an-undisclosed-unsupported-scope", "the-producer-boundary-makes-no-capability-claim-without-the-owning-dialect", "the-producer-boundary-derivation-ignores-a-payload-asserted-derivation-kind", "the-producer-boundary-answer-follows-the-registered-table-not-the-claim", "an-unsupported-source-variant-scope-projects-an-indeterminate-run", "a-supported-source-variant-scope-still-projects-a-successful-run", "a-dropped-grammar-row-is-still-inside-the-syntax-dialect-table", "an-unselected-grammar-row-still-makes-a-clone-scope-unavailable", "injected-false-complete-for-a-markdown-scoped-clone-refuses-at-the-producer-boundary"],
      "outputProjection": "run_termination over the new disclosed entry yields indeterminate exit 3 with typedDetail deficiency language-tier-unsupported and nativeCauses ['capability-missing']; the supported control still yields exit 0. Before the change the same request projected a silent exit 0."
    },
    {
      "id": "CB7-SHOULD-2", "disposition": "agreed and closed", "sourceChanged": True,
      "assessment": "Confirmed reachable by ordinary valid selections that every earlier bound admits. nativeContextDigests (128) carries one member per DISTINCT admitted native context and units collapse only when compiler closure, stdlib and effective options are identical, while scope-descriptor.workspaceRoots admits 1024 and a narrow capability selection keeps requestedCapabilities far under its own 1024 - so 129 such units pass every earlier gate. importIds (256) is selected by semantic-configuration.evidence.importIds, which admits 1024. semanticClosures (128) is reached by policy selections whose 128 admitted packs need not share closures. The only prior outcome was a generic jsonschema maxItems ValidationError naming no field, count, limit or public route.",
      "design": "admit_plan_selection_cardinality is a PRE-PLAN boundary on the PROSPECTIVE Plan, raising the existing field-generic ScopeRefusal: PROJECT.SCOPE_LIMIT, subject `field:count>limit`, request-rejected exit 2 REQUEST.UNSATISFIABLE, and a field-specific narrowing remedy. No bound is widened, nothing is truncated and no analysis is silently reduced.",
      "wiring": "Called on the real Plan construction path in BOTH reference producers (integration-fixtures.py and check-identity.py, immediately before add('plan',...) - `add` builds the identical value from the same fields, so no Plan identity moves) and inside plan_native_context_digests, which is where that field's deduplicated count first exists. It is not an orphan helper.",
      "prospectiveVersusRetained": "Deliberately NOT added to admit_run or close_run. A retained Plan over its bound is a corrupt or malformed retained record and keeps its schema-first refusal and section 10's origin-dependent routing; re-deriving a caller's remedy from already-committed bytes would misreport a corrupt store as an oversized request. Two controls assert the retained path still refuses and that the refusal is not a ScopeRefusal.",
      "shapeDiscipline": "Only an ACTUAL JSON array over its bound refuses. Missing, null, true, false, number, string, object, a nested list, an in-bound array of wrong-typed members, and a non-object prospective Plan all pass through untouched to the schema. A 300-character string is never reported as 300 members, which is the misclassification the analysis-spec boundary already had to fix.",
      "order": "PLAN_SELECTION_FIELDS is the published $defs/plan declaration order - semanticClosures, nativeContextDigests, importIds - drift-checked against the document, so one request always yields one first subject and narrowing makes deterministic progress.",
      "adjacentBoundsAudit": {
        "scope-descriptor.workspaceRoots/pathPrefixes/excludedPathPrefixes": "already accounted by unit_scope_descriptor; excludedPathPrefixes can exceed because it unions ignorePaths with conventional, observed and boundary prefixes, and that overflow was already guarded.",
        "analysis-spec.requestedCapabilities": "already accounted (the existing law).",
        "analysis-spec.policyPackIds 128 vs semantic-configuration.policy.packIds 128": "equal, no admitted-then-unrepresentable band.",
        "semantic-configuration.analysis.capabilities 128 vs analysis-spec.requestedCapabilities 1024": "the selecting field is the SMALLER one, so no gap.",
        "semantic-configuration.discovery.workspaceRoots 1024 vs scope-descriptor.workspaceRoots 1024": "equal and already accounted.",
        "policy.waiverIds 1024": "projects to a single waiverDigest, not an array.",
        "analysis-spec.parameters 128": "inspected and NOT an unaccounted selection: parameters carry one row per schema kind (the import-source-context row holds a declaredBuildIds list), not one per import. Recorded as an observation, not widened into a resource-policy redesign.",
        "view.scopeIds/facts/coverageIds 100000, view.schemaDigests 128": "not request selections; left alone."
      },
      "controlsAdded": ["the-plan-bounds-are-read-from-the-published-schema-not-restated", "the-plan-selection-order-is-the-published-declaration-order", "a-plan-selection-exactly-at-its-bound-is-admitted.{semanticClosures,nativeContextDigests,importIds}", "a-plan-selection-one-over-its-bound-refuses-typed.{semanticClosures,nativeContextDigests,importIds}", "the-plan-selection-refusal-carries-field-count-limit-and-its-own-remedy", "an-oversized-plan-selection-projects-the-existing-public-route", "the-oversized-plan-selection-route-adds-no-public-code", "two-oversized-plan-selections-refuse-on-the-first-published-field", "the-second-published-field-is-reported-once-the-first-is-narrowed", "a-malformed-plan-selection-shape-raises-no-scope-refusal.{null,true,false,number,string,object,nested-list}", "a-missing-plan-selection-field-raises-no-scope-refusal", "a-non-object-prospective-plan-raises-no-scope-refusal", "an-oversized-string-is-never-reported-as-a-member-count", "an-in-bound-but-malformed-plan-selection-passes-through-to-the-schema", "a-narrow-capability-workspace-reaches-the-plan-context-bound-through-admitted-bounds", "the-native-context-digest-producer-accounts-for-its-own-field", "the-native-context-digest-producer-still-returns-a-lawful-deduplicated-set", "the-configuration-import-selection-outranges-the-plan-import-array", "an-oversized-plan-import-selection-on-the-construction-path-mints-no-plan", "an-oversized-plan-closure-selection-on-the-construction-path-mints-no-plan", "an-in-bound-plan-import-selection-on-the-construction-path-still-closes-a-run", "a-plan-import-selection-exactly-at-its-bound-is-still-minted", "a-retained-plan-over-its-bound-refuses-at-retained-closure", "a-retained-plan-over-its-bound-is-not-reclassified-as-a-request-scope-refusal", "one-law-serves-seven-bounded-fields-across-three-record-families", "every-bounded-field-carries-its-own-narrowing-remedy", "the-published-law-states-the-widened-meaning-over-seven-fields"],
      "publishedProse": "native-evidence S14's bounded-selection paragraph is widened from four fields / two record families to seven / three, states the reachability arithmetic for each new field, the prospective-versus-retained distinction, the shape rule and the deterministic order."
    },
    {
      "id": "CB7-ADV-1", "title": "The D9 successor artifact obligation is live and disclosed",
      "disposition": "accounted, no source change", "sourceChanged": False,
      "account": "The blind's own assessment is that native S10 discloses it precisely with a named owner and nothing is left to invent: the successor adds exactly one fault cause (host-invariant) over the ten inherited, maps it to SYSTEM.OUTCOME.ILLEGAL_STATE, and leaves class-to-exit and reasonCodes unchanged. The limitation preserved here is that host-invariant has no inherited mapping, which is a deliberate successor extension and not a gap. Ownership: the artifact obligation is an IMPLEMENTATION and APPLICATION-record item, not a design-reference one; it belongs to whoever publishes the D9 successor artifact and to root's application record, and this coauthor turn asserts nothing about its completion."
    },
    {
      "id": "CB7-ADV-2", "title": "The matrix-fixed default cannot express 94..1024-unit TypeScript repositories",
      "disposition": "accounted, no source change", "sourceChanged": False,
      "account": "Already disclosed with a typed refusal and an explicit remedy, and the arithmetic is stated in the very S14 paragraph this turn widened: 11 capabilities per TypeScript unit, 93 units at 1023 rows (one under the bound, not exactly at it), 94 at 1034 against a 1024 bound. The limit is PRESERVED, not widened, and CB7-SHOULD-2 deliberately did not touch it. It is a real product limitation whose resolution - a narrower default, or a larger bound - is an implementation and product decision, not a reference-model correction. Ownership: implementation plus root's product-limit record."
    },
    {
      "id": "CB7-ADV-3", "title": "PLATFORM-ID-DOMAIN-V1 is broader than the four-platform product promise",
      "disposition": "accounted, no source change", "sourceChanged": False,
      "account": "Already disclosed by the successor registry with its reason: the encoding domain has 8 members, the selected machine platforms are 4, and the grant platformId enum is exactly those 4. Encoding breadth is not a support claim, and the blind measured that no product surface reads it as one. The limit is preserved unchanged. Ownership: implementation must not widen the supported set by widening the encoding domain, and platform support remains qualification work that this design exercise does not perform."
    },
    {
      "id": "CB7-ADV-4", "title": "PROTOCOL3_RULES is named, not published",
      "disposition": "agreed and closed", "sourceChanged": True,
      "assessment": "Substantiated as a real publication gap rather than dismissed. Existing normative inputs do NOT determine the 34 rows: S9.2 published the 22 phases, the frame table and three sentences of behaviour, but not the rows, their guards, the wildcard vocabulary, the terminal law or - decisively - the stage-dependent ANALYZING_OR_READY_COMPLETE transition, without which a multi-stage exchange cannot be interpreted at all. A consumer could not have reconstructed the state machine from the contract alone.",
      "artifact": "docs/coop/design-corrections/native/protocol3-transitions.v1.json, GENERATED from the exact existing rows rather than transcribed. It carries the 34 rows in order, the phase list, the wildcard definitions (*ANY, *PRE_COMPLETE with its explicit phases and its derivation, the * frame, the out-of-band *PROCESS_FAULT set), the match law, the guard law, the pre-match and no-match laws, per-frame state updates, the terminal law, the stage-dependent transition and an explicit ownedByProse list.",
      "consumption": "The reference now READS the artifact: PROTOCOL3_PHASES, PROTOCOL3_RULES, _PRE_COMPLETE, _PROCESS_FAULTS and _SOURCE_FRAMES all derive from it, so there is one authority and no transcription that could drift. The same idiom this file already uses for LADDERS.",
      "correctionOfMyOwnFirstDraft": "My first artifact text and control asserted that the declared ORDER is load-bearing and that reordering P3-08..P3-10 changes the transition. That is FALSE of this table: the rows are pairwise disjoint on (phase, frame, guard), so first-match-wins currently resolves no ambiguity and a reversed table reproduces the same trace. The competing rows are separated by MUTUALLY EXCLUSIVE guards, not by position. Both the artifact's matchLaw and the controls now assert the true, stronger property, plus a control proving the disjointness check would actually catch an overlapping row.",
      "proseOwnedActionLogic": ["frame payloads and their validation", "the identity token set behind identityNegotiated", "the terminalKind to D9 class and exit-code mapping in S10", "the custody and digest obligations of S3 and S5", "the stage COUNT itself, an invocation property the table cannot derive"],
      "controlsAdded": ["the-published-protocol-table-is-the-table-the-reference-runs", "the-published-pre-complete-wildcard-agrees-with-its-published-derivation", "the-published-out-of-band-and-source-frame-sets-are-the-ones-applied", "every-published-transition-names-a-published-successor", "every-published-row-names-a-published-phase-or-wildcard", "the-published-table-states-what-remains-prose-owned", "the-published-rows-are-pairwise-disjoint-so-position-resolves-no-ambiguity", "rows-sharing-a-phase-and-frame-really-exist-and-are-guard-separated", "the-published-guards-select-the-dependency-mode-transition", "a-reordered-published-table-reproduces-the-same-transition", "an-injected-overlapping-row-is-detected-by-the-disjointness-control", "an-unknown-frame-takes-the-published-fallback-row", "an-out-of-band-process-fault-takes-the-published-any-phase-row", "a-post-terminal-frame-is-refused-by-the-published-pre-match-law", "the-published-stage-dependent-transition-completes-a-two-stage-run", "a-two-stage-run-cannot-complete-after-one-coverage"],
      "existingTracesPreserved": "The four existing native protocol3 cases (open-universe-without-identity-faults, happy-path-dependency-and-prepared, crash-mid-stage-is-not-complete, budget-exhausted-terminal) now run off the published table and pass unchanged, which is the strongest available evidence that the artifact is the same table.",
      "notDone": "Orchestration tools were not modified; the blind kit selector is root's (V19-ROOT-2), as is the pin row (V19-ROOT-1)."
    },
    {
      "id": "CB7-ADV-5", "title": "UNICODE_CASE_DATA_VERSION is a prose constant",
      "disposition": "accounted, no source change", "sourceChanged": False,
      "account": "Already pinned: the reference declares UNICODE_CASE_DATA_VERSION = '15.0.0' and the contract states the portability limitation itself. Byte-exact semantics are preserved and nothing here changes the fold. The blind's own limitation is preserved and NOT converted into a guarantee: its vectors do not discriminate U+0130, Final_Sigma or U+00DF because every current lib name is ASCII, where the three candidate operations coincide. So the ASCII vector set demonstrates agreement on ASCII only; it establishes nothing about non-ASCII behaviour, and no such claim is made or added. Ownership: an implementation that folds non-ASCII lib names must bind to the same UCD version, and a discriminating non-ASCII vector set would be new work outside this turn's scope."
    },
    {
      "id": "CB7-SHOULD-1", "title": "The mandated per-requirement cause carrier cannot express 11 of 16 producible outcomes",
      "disposition": "INITIAL DISPOSITION ONLY - source deliberately untouched", "sourceChanged": False,
      "instructionHonoured": "Root is challenging the code==cause assumption with the original blind reviewer in a separate active directory, which was not read and not interfered with. No per-requirement deficiency vocabulary was changed and no DomainDetail code was invented.",
      "initialDisposition": "I lean to root's reading, and it is directly supported by the shipped bytes rather than only by argument. Workflows S6 says 'the exact cause is carried into that requirement's unmet precondition so two different causes are two different remedies'. That mandates remedy DISTINCTNESS, not code equality. workflows_model.v1.py already emits, for every unsatisfied evidence requirement, {'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'remedy': 'evidence requirement unsatisfied: <relation>@<minResolution> (<plane>: <deficiency>)'} - the exact plane and deficiency, derived by admit_evidence_requirement, in the remedy. Two different causes therefore produce two different unmetPreconditions entries, and since unmetPreconditions is in the repairPlanId preimage that distinction is identity-bearing, which is the property the blind's own whyShouldNotMust turns on. On that reading the finding's premise - that expressibility requires a distinct DomainDetailCode - does not follow from S6, and registering 11 new codes would be forbidden by workflows S12 anyway.",
      "whatWouldChangeMyMind": "If the original blind reviewer maintains that a consumer is contractually entitled to BRANCH on the code rather than to READ the remedy, then a shared code genuinely under-determines a machine consumer even though the human remedy differs, and the right fix is neither 11 codes nor silence but an explicit statement of which field is the machine-readable carrier.",
      "narrowlyExplicitSentenceIfBothAgree": "If root and the blind reviewer agree, ONE sentence in workflows S6 would close it without vocabulary change, along the lines of: 'The carrier of the exact cause is the unmet precondition's remedy, which names the plane and the deficiency; the code identifies the precondition class and is deliberately shared, so consumers distinguish causes by the remedy and by evidenceRequirements[].deficiency, not by the code.' I am NOT proposing this as a change now, have not written it to any source file, and it must not be auto-accepted without the blind reviewer's substantive reassessment."
    }
  ],
  "executedResults": {
    "environment": "/tmp/opensip-architecture-review-env/bin/python -I -B",
    "pinGateNote": "No source pin was edited in `work`. check_native_evidence.v2 and check-security-lifecycle.v1 refuse before running when pins differ, so they were executed in a DISPOSABLE repinned copy at out/disposable/final, outside `work`. No pin match is claimed for the delivered bytes.",
    "checks": [
      {"check": "foundation/check-identity.py", "before": "1346 passed / 0 failed", "after": "1431 passed / 0 failed", "delta": "+85 controls", "pinGate": "none"},
      {"check": "check-integration.py", "before": "392 passed / 0 failed", "after": "392 passed / 0 failed", "pinGate": "none"},
      {"check": "foundation/check-foundation.py", "after": "231/231 PASS", "pinGate": "none"},
      {"check": "foundation/check-array-orders.py", "after": "65/65", "pinGate": "none"},
      {"check": "foundation/check-product-configuration.py", "after": "28 passed / 0 failed", "pinGate": "none"},
      {"check": "foundation/check-product-quality.py", "after": "24 passed / 0 failed", "pinGate": "none"},
      {"check": "native/check_native_evidence.v2.py", "after": "PASS 355/355 cases; matrix cells 66; open objects 0; uncovered feedback []", "pinGate": "run in the disposable repinned copy"},
      {"check": "security/check-security-lifecycle.v1.py", "after": "456/456 pass", "pinGate": "run in the disposable repinned copy"}
    ],
    "failuresEncountered": [
      "First run after the MUST-1 guards: check-identity 1345/1, the single failure being injected-false-complete-for-a-markdown-scoped-clone-refuses. Diagnosed as the intended boundary move (the syntax dialect is also a closed suffix table), not a regression; control updated and two new discriminating controls added.",
      "A producer-boundary control used derivationKinds ['ts'], which is outside that field's closed enum and raised a schema ValidationError. Replaced with a valid member plus a stronger control that the answer follows the registered table rather than the claim.",
      "My S14 prose replacement silently did nothing because the document reads '**two record families**', not '**two** record families', while my assertion covered only the sentence prefix. Caught by the prose control failing (1413/1) and fixed with an assertion on the exact replacement string.",
      "My first CB7-ADV-4 control asserted that the table's ORDER is load-bearing. It failed, correctly: the rows are pairwise disjoint and a reversed table reproduces the trace. Both the artifact text and the controls were corrected to the true property."
    ],
    "limitations": [
      "Everything here is a reference-model admission boundary over synthetic trusted observations. No compiler, parser, grammar, provider, OS or filesystem is executed, ranked or qualified, and nothing here is evidence of host, compiler or OS enforcement.",
      "The producer-boundary source-variant guard is total only for callers that supply the owning universe dialect and only for source-path subject kinds; unconditional totality lives at retained Run closure.",
      "The symbol branch of source_variant_capability_support is unreachable under today's relation registry and is stated as future-facing parity, not as a live guard.",
      "coverage_result is duplicated between integration-fixtures.py and foundation/check-identity.py. That duplication is pre-existing; it was MIRRORED, with the mirror's soundness proved by asserting the patched copies are byte-equal, rather than unified, because unifying two fixture producers would move unrelated fixture identities and was not asked for. It remains a real maintenance hazard worth a separate scoped change.",
      "No native case was added to native-cases.v2.json: the existing syntax capability law has none either, and the discriminating ADV-4 controls need to drive the interpreter with a permuted table, which the JSON case DSL cannot express. They live in check-identity.py with a comment saying so.",
      "No grade is minted and no independent acceptance is claimed. I am not the independent reviewer of these changes."
    ]
  },
  "changedFiles": changed_files,
  "disposableProbes": {
    "note": "Everything below is DISPOSABLE and is not proposed for application. Failed and superseded intermediate attempts are preserved rather than deleted.",
    "editScripts": "out/probes/*.py - the exact edit scripts that produced the delta, including the ones whose first form was wrong (edit_should2_controls.py's prose anchor, edit_adv4_controls.py's order claim).",
    "disposableTrees": "out/disposable/{run1..run14,exp1,before,final,repinned} - copies of `work` used to run checks without writing generated reports into `work`; `before` restores the four frozen files for the baseline measurement; `final` and `repinned` carry LOCALLY REPINNED ledgers that exist only to run the two pin-gated checks.",
    "evidence": "out/evidence/{before-hashes.json,changed-files.json,final-reports/}"
  }
}

(ROOT / 'handoff.json').write_text(json.dumps(doc, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print('wrote handoff.json', len(json.dumps(doc)))
