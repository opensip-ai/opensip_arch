# OpenSIP blind consumer design review -- consumer-b.v23

**Verdict: CHANGES_REQUIRED**

| | |
|---|---|
| sessionId | `79569ae1-10f4-4181-972b-334f7ed2f07a` |
| same-origin ancestry | consumer-b.v14 -> consumer-b.v15 -> consumer-b.v16 -> consumer-b.v17 -> consumer-b.v18 -> consumer-b.v19 -> consumer-b.v20 -> consumer-b.v22 -> consumer-b.v23 (generation 21 prepared, never launched) |
| subject manifest SHA-256 | `e35dc60175ae9741435218614ca1d2aa81a1c69a105358af8af9ce537bde8ea9` |
| parent digest declared in that manifest | `a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235` (PASS) |
| kit files verified | 102 / 102 (PASS) |
| measured normative delta | 99 unchanged, 3 changed, 0 added |
| changed owner | `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md`, `docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json`, `docs/coop/design-corrections/foundation/incoming-search.schema.v1.json` |
| requirement status | executed 131, futureQualification 3 |
| claimed-positive audit | {'PASS': 126, 'DEFERRED': 5} |
| new MUST / SHOULD / advisories | 0 / 3 / 2 |

> This is NOT a parent whole-candidate verification: only the parent digest declared inside
> the held manifest was compared. No root admission, agreement, expected result, author
> model or checker was supplied, read or inferred; the root outcome over these exact bytes
> is unobserved by this origin. Nothing here qualifies any product, compiler, provider or
> host; every toolchain and host observation is a synthetic trusted input.

## Why this verdict

ACCEPT-RECONSTRUCTABLE requires: every acceptBlocking requirement executed with evidence sufficient for its kind (claimed-positive audit, not presence or counts), no claimed-positive audit failure, no unresolved MUST or SHOULD, no open helper failure on a claimed positive, every complete Run closed, replayed, controlled and admitted by the independent atom law, every preceding stage of this command exited zero, and the measured read graph of this command passes. MEASURED: 0 acceptBlocking not executed, 0 audit failures, 0 MUST, 3 SHOULD, 0 open helper failures, Runs ok = True, preceding stages ok = True, read graph ok = True.

- acceptBlockingRequirementsNotExecuted: **none**
- phase11RowsFailed: **none**
- claimedPositiveAuditFailures: **none**
- newMustIssueCount: **0**
- newShouldIssueCount: **3**
- openHelperFailuresOnAClaimedPositive: **none**
- everyCompleteRunClosedReplayedControlledAndAtomLawAdmitted: **True**
- everyPrecedingStageOfThisCommandExitedZero: **True**
- measuredReadGraphOfThisCommandPasses: **True**
- thisIsTheFinalReconciliationStage: **True**

## What changed in the input

- kind: NORMATIVE SUCCESSOR; MEASURED per path against this origin's own retained generation-22 per-file map (notes/v22-input-custody.json); the supplied normative-delta.json hash inventory was then VERIFIED against both sides rather than adopted (notes/v23-input-custody.json claim 5).
- what the changed owner decides: foundation/atom-evaluation-contract.v1.md now publishes: section 6 runtime polarity (an unfiltered exists is satisfied by observed-hit or observable-unhit; an observability filter restricts the polarity set); section 4 dependency totality for same-kind dependencies (a gap view is evaluated with and without its gap positions and a removed position answers required-relation-missing), no mapped-scope fallback, ATOM_NATIVE_CARRIER for an absent or null enumeratorClosure, the admitted-input refusals INCOMING_SEARCH_SCHEMA / INCOMING_SEARCH_SCOPE_MISJOIN, the explicit empty-subject scope that closes an empty program, and I1 (a subject universe with no available owed binding is blocking). The projection registry and the IncomingSearchV1 schema carry the matching registry and admission text.
- consequence: the atom evaluator was reconciled (V23-D1..V23-D3): the TypeScript and rust Runs changed identity (findings 3 -> 5 and 8 -> 7), all five Runs were rebuilt, re-exported, re-closed, re-replayed and re-controlled, and the independent atom-law instrument admits all five and refuses the generation-22 and generation-20 predecessors. The whole-charter recheck then found and corrected claimed positives whose semantic fields were not derived from their premises (V23-D6..V23-D11).

## Complete positive Runs

| Run | runId | verdict | objects | blobs | closure | replay | controls | atom law |
|---|---|---|---|---|---|---|---|---|
| syntax-code | `run3:00b039cc63d8db342...` | indeterminate | 51 | 135 | 877 passed / 25 n-a / 0 refused | REPLAY_MATCH (2 findings, 6 witnesses) | 14, all refused: True | 6 atoms, 61 checks, 0 refused |
| typescript | `run3:682fbbfe3ce84fe1b...` | indeterminate | 62 | 187 | 1106 passed / 18 n-a / 0 refused | REPLAY_MATCH (5 findings, 21 witnesses) | 14, all refused: True | 15 atoms, 134 checks, 0 refused |
| rust | `run3:ba7041773edb4dd2e...` | indeterminate | 81 | 200 | 1185 passed / 27 n-a / 0 refused | REPLAY_MATCH (7 findings, 19 witnesses) | 14, all refused: True | 19 atoms, 198 checks, 0 refused |
| rust-partial | `run3:b4500bf8f0750a754...` | indeterminate | 88 | 192 | 747 passed / 16 n-a / 0 refused | REPLAY_MATCH (3 findings, 7 witnesses) | 14, all refused: True | 7 atoms, 84 checks, 0 refused |
| syntax-data | `run3:47fa680d35d319939...` | indeterminate | 53 | 136 | 804 passed / 28 n-a / 0 refused | REPLAY_MATCH (6 findings, 12 witnesses) | 14, all refused: True | 12 atoms, 139 checks, 0 refused |

- `runs/syntax-code.store.json` sha256 6ed16aa8f0634b25405050d3405104a2a5b8bddb6598f96e637062ad1b78530d
- `runs/typescript.store.json` sha256 d6e33abdfaa6b7ce46b19f49027b70502a6269f5c1f7f59dc4da0f18862152c0
- `runs/rust.store.json` sha256 0729e0b2516a2145a682e952bc4858efb693dba32b5d6ab5d16bd5d52a298812
- `runs/rust-partial.store.json` sha256 057df271dbbbbdcc64fbaf4f739a67b83dbf8f96988371505fff163f0810a129
- `runs/syntax-data.store.json` sha256 8a15d29b8d26088ade131623d624c46aa2e7cd81e86cf4e009d44cf999b5a4ef

## Claimed-positive audit (every requirement, from its final bytes)

Counts: {'PASS': 126, 'DEFERRED': 5}. Evidence classes: {'reconstructed-behavior': 83, 'measured-control': 13, 'cited-kit-distinction': 3, 'standing-record-verified': 16, 'schema-admitted-record': 16}.

each requirement was re-checked from its FINAL bytes in a fresh process. The evidence class says what the re-check actually is; a static comparison, a shape-only check or a helper assumption never makes a requirement executed. The five phase-11 rows are decided by the requirement-status stage after this deliverable is written.

| id | kind | evidence class | result | checks passed | first refusal |
|---|---|---|---|---|---|
| R-ACYCLIC-JOINS | standaloneCanonicalVector | reconstructed-behavior | PASS | 2 |  |
| R-ADVERTISED-MODE-PATHS | standingRule | standing-record-verified | PASS | 2 |  |
| R-BASELINE-AUDIT | standaloneCanonicalVector | reconstructed-behavior | PASS | 10 |  |
| R-BLOCKER-NOT-ADJUST | standingRule | standing-record-verified | PASS | 2 |  |
| R-CANDIDATE-ONLY-CLONES | standaloneConfigVector | schema-admitted-record | PASS | 5 |  |
| R-CAP-ADMISSION | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-CAP-NAMED-GATES | standaloneCanonicalVector | measured-control | PASS | 53 |  |
| R-CHAIN-ZERO-CONFIG-TO-RECEIPT | standingRule | standing-record-verified | PASS | 7 |  |
| R-CLONE-DEFICIENCY-PAIRING | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-CLONES-NEGATIVE-VECTORS | standaloneCanonicalVector | measured-control | PASS | 1 |  |
| R-CMP-EMPTY-RESULT | standaloneCanonicalVector | reconstructed-behavior | PASS | 6 |  |
| R-CMP-EVIDENCE-CHANGED | standaloneCanonicalVector | reconstructed-behavior | PASS | 7 |  |
| R-CMP-MISSING | standaloneCanonicalVector | reconstructed-behavior | PASS | 6 |  |
| R-CODE-VS-DATA-MATRIX | standaloneCanonicalVector | reconstructed-behavior | PASS | 4 |  |
| R-CONFIG-CUSTOM-MULTI-BASE | standaloneConfigVector | schema-admitted-record | PASS | 6 |  |
| R-CONFIG-JS-SHARED-BASE | standaloneConfigVector | schema-admitted-record | PASS | 5 |  |
| R-CONFIG-SYNTHESIZED | standaloneConfigVector | schema-admitted-record | PASS | 7 |  |
| R-COUNT-CLASS-ATTEMPT | standaloneCanonicalVector | reconstructed-behavior | PASS | 40 |  |
| R-CVE1-EIGHT-TYPES | standaloneCanonicalVector | reconstructed-behavior | PASS | 17 |  |
| R-CVE1-TYPES-AVAILABLE | standingRule | reconstructed-behavior | PASS | 1 |  |
| R-D9-EXTENSION-PRECEDENCE | schemaEnvelope | reconstructed-behavior | PASS | 2 |  |
| R-DELIVER-MD-JSON | standingRule | standing-record-verified | DEFERRED | None |  |
| R-DETECTOR-COMPAT-FILE | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-DISTINGUISH-FOUR-BOUNDARIES | standingRule | standing-record-verified | PASS | 40 |  |
| R-DURABLE-RECEIPT-AVAILABILITY | schemaEnvelope | schema-admitted-record | PASS | 3 |  |
| R-E0-VS-E1-E3 | standaloneCanonicalVector | reconstructed-behavior | PASS | 6 |  |
| R-EMPTY-PARTIAL-UNAVAILABLE-MISSING | standingRule | reconstructed-behavior | PASS | 17 |  |
| R-ENUM-VS-RESOLUTION | standingRule | reconstructed-behavior | PASS | 1 |  |
| R-ENVELOPE-CONFIG-INPUT | schemaEnvelope | schema-admitted-record | PASS | 5 |  |
| R-ENVELOPE-EXTERNAL-INPUT | schemaEnvelope | schema-admitted-record | PASS | 5 |  |
| R-ENVELOPE-HOST-INVALID | schemaEnvelope | schema-admitted-record | PASS | 5 |  |
| R-ENVELOPE-PRODUCER-BOUNDARY | schemaEnvelope | schema-admitted-record | PASS | 5 |  |
| R-FAILURE-ENVELOPES-D9 | schemaEnvelope | reconstructed-behavior | PASS | 13 |  |
| R-FIVE-CONTRACTS-INDEX | standingRule | cited-kit-distinction | PASS | 2 |  |
| R-FREEDOM-VS-MISSING | standingRule | standing-record-verified | PASS | 1 |  |
| R-FROM-SCRATCH-COMMAND | standingRule | reconstructed-behavior | PASS | 3 |  |
| R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR | standaloneCanonicalVector | reconstructed-behavior | PASS | 185 |  |
| R-H-HELPER | standaloneCanonicalVector | reconstructed-behavior | PASS | 10 |  |
| R-HELPER-KIT-ONLY | standingRule | standing-record-verified | PASS | 2 |  |
| R-HIDDEN-MISMATCH-PER-LANGUAGE | standaloneCanonicalVector | measured-control | PASS | 1 |  |
| R-HOST-CAPTURED-VS-CANDIDATE | standaloneCanonicalVector | reconstructed-behavior | PASS | 8 |  |
| R-IDENTIFY-GAPS | standingRule | standing-record-verified | PASS | 2 |  |
| R-IMPORTED-OBSERVATION-BOUNDARY | standaloneCanonicalVector | reconstructed-behavior | PASS | 10 |  |
| R-IMPORTED-PAYLOAD-IN-GRAPH | completeRunProperty | reconstructed-behavior | PASS | 11 |  |
| R-INDEPENDENT-CLOSURE-JOINS | standingRule | reconstructed-behavior | PASS | 35 |  |
| R-INVOCATION-DISCLOSURE | schemaEnvelope | reconstructed-behavior | PASS | 5 |  |
| R-JS-CLONE-BODY-THROUGH-TS | standaloneCanonicalVector | reconstructed-behavior | PASS | 11 |  |
| R-LEXICAL-ADMISSION | standaloneCanonicalVector | measured-control | PASS | 22 |  |
| R-MEASURED-NOT-COUNTS | standingRule | measured-control | PASS | 2 |  |
| R-MIN-RESOLUTION-REPAIR-EVIDENCE | standaloneCanonicalVector | schema-admitted-record | PASS | 3 |  |
| R-MIN-RESOLUTION-THREE-LEVELS | standaloneCanonicalVector | reconstructed-behavior | PASS | 28 |  |
| R-MULTI-STEP-DIFFERENT-SELECTIONS | schemaEnvelope | reconstructed-behavior | PASS | 16 |  |
| R-MULTI-UNIT-MISSING-CAPS | standaloneConfigVector | schema-admitted-record | PASS | 5 |  |
| R-MUST-SHOULD-ADVISORY | standingRule | standing-record-verified | DEFERRED | None |  |
| R-MUTATION-REPLAY-SCOPE | standaloneCanonicalVector | schema-admitted-record | PASS | 9 |  |
| R-MUTATION-VS-ANALYSIS-STEPS | standingRule | cited-kit-distinction | PASS | 3 |  |
| R-NATIVE-PREIMAGE-JOINS | completeRunProperty | reconstructed-behavior | PASS | 24 |  |
| R-NEGATIVE-FIRST-REFUSAL | standingRule | measured-control | PASS | 1 |  |
| R-NO-ACCEPT-IF-INCOMPLETE | standingRule | standing-record-verified | DEFERRED | None |  |
| R-NO-QUALIFICATION-CLAIM | standingRule | standing-record-verified | DEFERRED | None |  |
| R-OBJECT-TABLE-FRAMES | standingRule | reconstructed-behavior | PASS | 35 |  |
| R-PINNED-PURGE | schemaEnvelope | schema-admitted-record | PASS | 9 |  |
| R-PIVOT-ONLY-FINGERPRINTS | standaloneCanonicalVector | reconstructed-behavior | PASS | 6 |  |
| R-PROMISE-VS-AVAILABILITY | standingRule | standing-record-verified | PASS | 2 |  |
| R-PUBLIC-FROM-INTERNAL-REFUSAL | schemaEnvelope | schema-admitted-record | PASS | 6 |  |
| R-PUBLIC-TERMINATION-EXAMPLES | schemaEnvelope | reconstructed-behavior | PASS | 51 |  |
| R-PURGE-REPLAY-OUTPUT-FAILURE | schemaEnvelope | reconstructed-behavior | PASS | 23 |  |
| R-RAW-VS-PARSED | standaloneCanonicalVector | measured-control | PASS | 2 |  |
| R-RELATION-RUNG-TABLE | standaloneCanonicalVector | reconstructed-behavior | PASS | 2 |  |
| R-REPAIR-APPLY-KEY | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-REPAIR-AUTHORITY-PER-TARGET | standaloneCanonicalVector | measured-control | PASS | 17 |  |
| R-REPAIR-DESCRIPTOR | standaloneCanonicalVector | schema-admitted-record | PASS | 10 |  |
| R-REPLAY-AFTER-ADMISSION | evaluatorReplay | reconstructed-behavior | PASS | 45 |  |
| R-REPLAY-COMPARE-BUNDLE | evaluatorReplay | reconstructed-behavior | PASS | 40 |  |
| R-REPLAY-ENUM-AND-IDS | evaluatorReplay | reconstructed-behavior | PASS | 40 |  |
| R-REPLAY-EXPORT | evaluatorReplay | reconstructed-behavior | PASS | 40 |  |
| R-REPLAY-NO-CALLER-TRUTH | standingRule | measured-control | PASS | 2 |  |
| R-REPLAY-PREDICATE-WITNESS-VERDICT | evaluatorReplay | reconstructed-behavior | PASS | 40 |  |
| R-REPLAY-TAMPER | evaluatorReplay | measured-control | PASS | 40 |  |
| R-REPLAY-THREE-VALUED | evaluatorReplay | reconstructed-behavior | PASS | 2 |  |
| R-RETAINED-ARTIFACTS-IN-CLOSURE | standingRule | reconstructed-behavior | PASS | 40 |  |
| R-ROOT-ADMISSION-EXPORT | standingRule | standing-record-verified | PASS | 5 |  |
| R-RUN-CLONES-CUSTODY | completeRunProperty | reconstructed-behavior | PASS | 17 |  |
| R-RUN-CLONES-L0-AND-NORMALIZED | completeRunProperty | reconstructed-behavior | PASS | 1 |  |
| R-RUN-FILE-FACT-INVENTORY | completeRun | reconstructed-behavior | PASS | 24 |  |
| R-RUN-NO-COMPILER-UNIT | completeRunProperty | reconstructed-behavior | PASS | 16 |  |
| R-RUN-NONCEMPTY-CONTEXT | completeRunProperty | reconstructed-behavior | PASS | 16 |  |
| R-RUN-RUST | completeRun | reconstructed-behavior | PASS | 8 |  |
| R-RUN-RUST-BODY-DIALECT | completeRunProperty | reconstructed-behavior | PASS | 8 |  |
| R-RUN-RUST-HASH-MARKER | completeRunProperty | reconstructed-behavior | PASS | 8 |  |
| R-RUN-RUST-LARGE-EDITION-MAP | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-RUST-MIXED-EDITION | completeRunProperty | reconstructed-behavior | PASS | 8 |  |
| R-RUN-RUST-PARTIAL-EMPTY-CLONES | completeRun | reconstructed-behavior | PASS | 9 |  |
| R-RUN-RUST-SAME-FILE-TWO-EDITIONS | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-RUST-TARGET-EDITION | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-RUST-VERSION-COMPONENT | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-SYNTAX-CODE | completeRun | reconstructed-behavior | PASS | 8 |  |
| R-RUN-SYNTAX-DATA | completeRun | reconstructed-behavior | PASS | 9 |  |
| R-RUN-TS | completeRun | reconstructed-behavior | PASS | 8 |  |
| R-RUN-TS-CONFIG-DEPS | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-RUN-TS-NODE-MODULES | completeRunProperty | reconstructed-behavior | PASS | 10 |  |
| R-RUN-UNAVAILABLE-SEMANTIC | completeRunProperty | reconstructed-behavior | PASS | 13 |  |
| R-RUN-UNSUPPORTED-GRAMMAR | standaloneCanonicalVector | reconstructed-behavior | PASS | 9 |  |
| R-SCOPE-POLICY-ONLY-COMPARISON | standaloneCanonicalVector | reconstructed-behavior | PASS | 8 |  |
| R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-SELECTED-PROVIDER-CONTEXT | standingRule | reconstructed-behavior | PASS | 40 |  |
| R-SEMANTIC-VS-OPERATIONAL | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-SEMANTIC-VS-OPERATIONAL-AUTHORITY | standingRule | reconstructed-behavior | PASS | 3 |  |
| R-SINGLE-STEP | schemaEnvelope | reconstructed-behavior | PASS | 8 |  |
| R-SOURCE-MAP-SCOPE | standingRule | cited-kit-distinction | PASS | 3 |  |
| R-SUBSYSTEM-OWNERS | standingRule | standing-record-verified | PASS | 13 |  |
| R-TEST-PREP-REPAIR-AUTH | standaloneCanonicalVector | schema-admitted-record | PASS | 18 |  |
| R-TRACE-CANCEL | standaloneTraceVector | reconstructed-behavior | PASS | 2 |  |
| R-TRACE-COMPLETE | standaloneTraceVector | reconstructed-behavior | PASS | 2 |  |
| R-TRACE-EXECUTED-VS-HOST | standingRule | standing-record-verified | PASS | 1 |  |
| R-TRACE-FAULT | standaloneTraceVector | reconstructed-behavior | PASS | 4 |  |
| R-TRACE-IDENTITY-BEFORE-SOURCE | standaloneTraceVector | reconstructed-behavior | PASS | 2 |  |
| R-TRACE-TERMINAL | standaloneTraceVector | reconstructed-behavior | PASS | 2 |  |
| R-TRACE-UNAVAILABLE | standaloneTraceVector | reconstructed-behavior | PASS | 2 |  |
| R-VALID-VS-INVALID-VS-EXPLANATORY | standingRule | measured-control | PASS | 1 |  |
| R-VALIDATE-OWNING-SCHEMA | standingRule | reconstructed-behavior | PASS | 40 |  |
| R-VERDICT-ENUM | standingRule | standing-record-verified | DEFERRED | None |  |
| S-CONTINUATION | standingRule | reconstructed-behavior | PASS | 3 |  |
| S-FRESH-ORIGIN | standingRule | reconstructed-behavior | PASS | 2 |  |
| S-KIT-ONLY | standingRule | measured-control | PASS | 2 |  |
| S-MANIFEST-VERIFY | standingRule | reconstructed-behavior | PASS | 1 |  |
| S-MISSING-DEP-IS-CUSTODY | standingRule | reconstructed-behavior | PASS | 2 |  |
| S-NO-ORACLE | standingRule | measured-control | PASS | 1 |  |
| S-NOT-PRODUCT | standingRule | reconstructed-behavior | PASS | 3 |  |
| S-PROFILE-CURRENT | standingRule | reconstructed-behavior | PASS | 15 |  |

## Atom contract reconciliation

- instrument: lib/indep_atom_law.py (imports no evaluator) -> `vectors/indep-atom-law.json`
- syntax-code: {'atoms': 6, 'checks': 61, 'passed': 61, 'refusals': 0}
- typescript: {'atoms': 15, 'checks': 134, 'passed': 134, 'refusals': 0}
- rust: {'atoms': 19, 'checks': 198, 'passed': 198, 'refusals': 0}
- rust-partial: {'atoms': 7, 'checks': 84, 'passed': 84, 'refusals': 0}
- syntax-data: {'atoms': 12, 'checks': 139, 'passed': 139, 'refusals': 0}
- predecessor `predecessors.v22/runs/syntax-code.store.json`: refused False at `None` (0 refusals)
- predecessor `predecessors.v22/runs/typescript.store.json`: refused True at `PREDICATE_VALUE_EQUALS_DERIVED` (3 refusals)
- predecessor `predecessors.v22/runs/rust.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (7 refusals)
- predecessor `predecessors.v22/runs/rust-partial.store.json`: refused False at `None` (0 refusals)
- predecessor `predecessors.v22/runs/syntax-data.store.json`: refused False at `None` (0 refusals)
- predecessor `predecessors.v20/runs/syntax-code.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (10 refusals)
- predecessor `predecessors.v20/runs/typescript.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (6 refusals)
- predecessor `predecessors.v20/runs/rust.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (38 refusals)
- predecessor `predecessors.v20/runs/rust-partial.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (12 refusals)
- predecessor `predecessors.v20/runs/syntax-data.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (18 refusals)
- tamper syntax-code / a rule-level uncovered-expected-source-subject copied into the atom (A7): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- tamper syntax-code / selector-unbound carrying the subject universe (A6/A3): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- tamper typescript / an observable-unhit runtime row counted as a hit under an observability=observed-hit filter (A16): refused True at `PREDICATE_VALUE_EQUALS_DERIVED`
- tamper typescript / an observable-unhit runtime row excluded from an UNFILTERED exists (the generation-22 V22-D3 reading) (A16): refused True at `PREDICATE_VALUE_EQUALS_DERIVED`
- tamper rust / an absent dependency answered with no required-relation-missing (the generation-22 I-A1 reading) (A13): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- tamper rust-partial / coverage-unknown with its typed nativeCause carrier dropped (A12): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- law vectors: 19, passed 19
- min-resolution atom-level cases: 40, refused 0
- claim limit: no retained Run has an endpoint=target atom: A17-A19 incoming rules and A21 dependency totality are measured on typed synthetic models only and are labelled so
- claim limit: the published DEPENDS_ON closure is one edge deep (reachability->calls, clones->declares), so "at every depth of the dependency closure" is measured at depth 1 only; no deeper edge is invented
- claim limit: the only atom filter any retained Run carries is observability=observed-hit on the TypeScript runtime atom; no retained Run has a NATIVE atom filter, an imported count-at-most/all-covered atom, or a vcs-revision staleness correspondence: each raises NotExercised if met
- claim limit: subject SELECTION (composition s2) is not re-derived here; every subject checked is recomputed from its retained record and joined to a retained inventory row
- claim limit: the product evaluator is not imported; agreement is measured only by comparing the retained witness bytes with this derivation

## Query, mutation and authorization surfaces

- **wholePublishedQuerySurface**: {"instrument": "lib/indep_query_surface.py", "artifact": "query/indep-query-surface.json", "runUnderQuery": "run3:682fbbfe3ce84fe1ba358c034047577a716c4a4369d90bdca26aa9f8b0f3cb06", "operationsWithActualRecords": 20, "checks": 153, "refusals": 0, "negativeControls": 9, "graphOutcomesRecomputed": 46, "graphOutcomesDisagreeing": 0, "reinjectedDefectsDetected": "10 of 10", "graphExecutorArtifact": "query/graph-query-reconstruction.json"}
- **wholePublishedMutationSurface**: {"instrument": "lib/indep_mutation_surface.py", "artifact": "vectors/indep-mutation-surface.json", "checks": 29, "refusals": 0, "negativeControls": 7, "measuredKeys": {"genericMutationIntent": "f0ccf0a61cbadbd4e88021ad5720e0c44da84309f61aab11ac82451065ad0e70", "repairApply": "203c47f11b081630911654728f90efbd5d704753549959f7a046474bc1ceaef1", "importStep": "fa366fd3edfc96613f34e31ec2f3df69ae0d8acc8f3db4ecd7856f0c249f828f", "nativePreparationStep": "e7090515a7670cc356b44776c9e73199605ff0cda7d3ccd06888432d265957b8"}}
- **authorizationRecords**: {"artifact": "vectors/test-prep-repair-authorization.json", "recordsAdmitted": 4, "controlsRefused": 7, "syntheticHelperOnlyFields": {"repair-apply": ["authorization.consent.policyRecordId (the policy record is not constructed)"], "test-execution": ["authorizationRef (the RepoExecutionGrantV2 grant is not constructed)", "argv0Source.path (no test runner is inventoried by this origin's Runs)"], "native-preparation": ["authorizationDescriptorDigest (AuthorizedExecutionV2 is not constructed)", "securityGrantSetRef"]}, "standing": "authorization RECORDS constructed and admitted against their owning schemas. NOTHING was executed: no test ran, no preparation ran, no repair was applied. Every field listed under syntheticHelperOnly names a record this reconstruction does not construct and is not evidence-bound."}

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v23/output/lib/verify_all.py
```

The command declares **54** stages; **53** preceding stages of this same command were recorded when this reconciliation ran; failed stages: **[]**. this deliverable is written by the FINAL stage of that command. verify-all.json is rewritten after every stage, so the row count above is every preceding stage of the SAME command; the only row it cannot contain is this stage's own exit, which the command appends after it returns.

- earlier command A (`notes/v23-stage-io/20260912T151859`): failed stages 0
  - edits followed it: a stage label of verify_all.py still said the atom contract was frozen for generation 22; the report's consequence text cited V23-D6..V23-D10 while the corrections run to V23-D11; and a limitation disclosing the measured layer of the 16 schema-admitted-record positives was added. The final report is written by the command that ran after those edits.

Measured read graph (`notes/v23-read-graph.json`): **PASS**; 52 stages logged, 121 edges, order violations 0, undeclared edges 0, unknown reads 0. Child-process reads are not measured.

## New MUST issues

None. newMustIssues is EMPTY because every observable this origin was required to produce had a published derivation that it could execute: the C/H recipes, the closing digest law and its four representations and retention modes, the capability-manifest gates, the relation/rung registry with its anchor, snapshot, totality and partition laws, the grammar-capability registry and its three enforcement boundaries, the section 1.2 mode table, the config node-kind law, the Rust context projection, the execution-inputs cell and account derivation, the composition section 9 proof/evidence/seal/Run joins, the repair descriptor and its two idempotency recipes, the comparison and baseline identities, the D9 class/exit table, and the graph-query operations with their bounds and mandatory disclosure. Where a value could not be recomputed (L1-L3 normalisation, symbol-to-path attribution, provider occupancy) the kit SAYS so and substitutes custody, which this origin executed rather than worked around.

## New SHOULD issues

- **V23-S1** a graph endpoint of kind=package without packageManifestPath: section 2 says QUERY.ENDPOINT_AMBIGUOUS, but the owning schema REQUIRES the coordinate and section 8 admits the request against that schema before endpoints
  - selectors: docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 2 "Fault precedence" step 2; docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 8 steps 1 and 5; docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 7 row "malformed graph params"; docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphEndpoint allOf (kind=package then required packageManifestPath)
  - whatTheKitSays: step 1 of section 2 lists the malformed shapes and does NOT include a missing package coordinate, which step 2 routes to ENDPOINT_AMBIGUOUS; the schema refuses the same request at section-8 step 1, whose section-7 row is PARAMS_MALFORMED
  - consequence: same request, different DomainDetail (and a different remedy)
  - readingApplied: I-Q4: the section-2 precedence decides; the executor re-admits the request with a placeholder coordinate and, if that is the only schema fault, emits ENDPOINT_AMBIGUOUS; both boundaries are retained (query/graph-query-reconstruction.json package-endpoint-without-manifest-path)
  - smallestFix: say in section 2 (or section 8 step 1) that a schema refusal whose only fault is the package coordinate maps to QUERY.ENDPOINT_AMBIGUOUS, or relax the request-side GraphEndpoint requirement
- **V23-S2** native-evidence section 10 names VERDICT.INDETERMINATE as the existing code for required-relation-missing, language-tier-unsupported and confidence-floor-unmet; the D9 exit contract terminates those Runs with COVERAGE.REQUIRED_RELATION_MISSING, COVERAGE.LANGUAGE_TIER_UNSUPPORTED and COVERAGE.CONFIDENCE_FLOOR_UNMET
  - selectors: docs/v2/contracts/product-v1/native-evidence.md section 10 table columns "D9 class (host-owned)" and "Existing code"; docs/coop/artifacts/d9-exit-contract.v1.14.json scenarios analysis-required-coverage-missing, analysis-language-tier-unsupported, analysis-confidence-floor-unmet expectedTermination; docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/D9Deficiency description ("per native-evidence.md section 10")
  - whatTheKitSays: both documents call the code the existing D9 code for the deficiency; neither says which surface its column governs
  - consequence: the same sealed Run yields different termination reasonCodes
  - readingApplied: the D9 exit contract governs whole-Run terminations (it is the D9 owner and its rows carry the host axes); lib/phase7.py d9_projection and the audit re-derivation use its scenario rows
  - smallestFix: state that the section-10 column is the per-requirement / DomainDetail route and the D9 scenarios are the whole-Run termination, or align the three codes
- **V23-S3** graph-query availability `unavailable` must refuse with HOST.IO_FAILURE / evidence.*, but no evidence.* DomainDetailCode names it
  - selectors: docs/coop/design-corrections/workflows/query-projection-contract.v3.md section 7 identity availability paragraph; docs/v2/contracts/product-v1/identity-and-evidence.md section 5 ("known purged, expired, corrupt or unavailable required evidence produces operational-failed / HOST.IO_FAILURE / exit 4"); docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json#/$defs/DomainDetailCode (evidence.corrupt, expired, missing, pinned, purged, regeneration-mismatch)
  - whatTheKitSays: purged, expired and corrupt have members; unavailable has none, and a kind=failure envelope requires a nonempty errors array of DomainDetail
  - consequence: a consumer must choose a detail (evidence.missing? another?) that the kit does not name
  - readingApplied: none invented: the executor exercises purged and corrupt only, and treats unavailable as unexercised
  - smallestFix: name the detail for `unavailable` (a registered member or an explicit mapping)

Blocker statement: 0 MUST and 3 SHOULD design issues are open (V23-S1, V23-S2, V23-S3); each is reported with its exact selectors and smallest fix rather than an adjusted meaning.

## Advisories

- **V16-A3** (wording) `traversalCoverage` and native CoverageResult share the word "coverage" while being different obligations
  - observation: the schema already says "Not native CoverageResult" in both places, which is why this is only advisory. The shared noun still invites a consumer to report a COMPLETE traversal over an INCOMPLETE evidence base as evidence completeness.
  - handled here by: the two are carried in different required fields and reported separately, with an explicit statement of why: see query/graph-query-reconstruction.json evidenceLimitationsVersusStoredEdgeCompletion.
- **V23-A1** (carrier choice not stated) an invocation interrupted before any Run commits has no single stated envelope kind: kind=run requires a run, kind=failure requires a DomainDetail and no registered code names an interruption
  - observation: the golden fixes class interrupted and exit 130; kind=invocation with a cancelled step carries that without inventing a detail, but nothing says a single-step builtin uses it
  - handled here by: envelopes/public-termination.json termination-interrupted-before-settle is kind=invocation and says why

## What the generation-23 successor decided about this origin's own readings

- **standing**: not design gaps: the generation-23 kit changes three files (the atom evaluation contract, the evaluator projection registry and the IncomingSearchV1 schema), and their text decides questions this origin had answered differently (helper-corrections V23-D1..V23-D3).
- **runtimePolarity**: generation 22 made observed-hit the only runtime match (V22-D3); section 6 now says an unfiltered exists is satisfied by observed-hit or observable-unhit and a filter restricts the polarity set
- **absentDependency**: generation 22 read an absent dependency as adding no cause (I-A1); section 4 now says the removed position answers required-relation-missing and a same-kind totality gap is evaluated with and without its gap positions
- **carrierAndFallback**: this origin paired untagged scopes and fell back to mapped scopes; section 4 refuses ATOM_NATIVE_CARRIER on pairing and publishes that there is no mapped-scope fallback
- **incomingI1**: a subject universe with no available owed binding is disclosed and blocking under I1, never silently skipped

## Withdrawn by this origin, or resolved in kit bytes

- **V16-A2 (WITHDRAWN by this origin as factually wrong about the kit)** -- WITHDRAWN -- the clauses do state it, and they state the opposite. three published clauses, read this generation: (1) enumeration-contract section 1, UNAVAILABLE binding -- "`extents` still populated from host membership so expected file/package paths are not lost", and the enumerator row requires "inventories empty `unavailable` matching that pair"; (2) enumeration-contract sections 3/4 -- EXACTLY ONE SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind) of cell.kinds, with the `unavailable` shape given explicitly (rows=[], examinedPaths=[], deficiency non-null) and ENUMERATION_INVENTORY_MISSING_RECORD named for a whole missing expected inventory; (3) execution-inputs section 6 -- "Inventory digests: exactly one per kind, kinds set-equal to the cell" with NO available-only qualifier, plus "Unselected or `universe=null` DOES NOT DISCARD same-cell inventory items." A MISSING record is not a retained `unavailable` record.
- **V15-S1 (withdrawn by this origin)** -- WITHDRAWN as over-broad. no annotated site of the native document uses `fragment`, so declining to declare it there is correct. Measured: retention counts are preimage-frame 31, preimage 21, owner-retained 11, closure-tree-member 10, derived 3, and ZERO fragment sites (notes/native-annotated-site-audit.json).
- **V15-A1 (resolved in the new kit bytes)** -- RESOLVED at the source. the v16 native schema replaces it with `siteCountLaw`: "Count syntactic x-opensip-digest annotation occurrences in this schema document; the reference checker reports the measured count. No second hand-maintained total is normative." This origin now MEASURES 76 occurrences and asserts the absence of the old key.
- **V15-observation on the `derived` retention recipe** -- RESOLVED at the source. the v16 native schema declares `derived` with the recipe this origin had already derived from the plan/run capabilityManifestId join; the closure now asserts the declared statement rather than this origin's inference (check_native_digest_law_vocabulary).

## Algorithm freedom that is NOT a gap

- **how a host ENUMERATES subjects**: pinned observable -- SubjectInventoryV1 rows, examinedPaths equal to the Plan census, and the locator identity (planId, parameterDigest, cellOrdinal, programOrdinal, kind); left open -- the traversal strategy, parallelism and caching. the retained record is fully specified, so any strategy is checkable
- **how a normalizer computes an L1-L3 body**: pinned observable -- the framed body identity, the retained level specification bytes, and bodyIdentityJoin.recomputableAt = [L0-verbatim] only; left open -- the normalisation algorithm itself. the kit states in terms that it is NOT recomputable above L0 and demands exact retained preimage custody instead -- a deliberate, published limit, not a missing recipe
- **which shortest path a graph.path returns when several tie**: pinned observable -- canonical fact2-id-sequence tie-break; left open -- the search algorithm. the tie-break makes the RESULT total, so the algorithm is free
- **how a host stores and indexes the evidence store**: pinned observable -- the exported object table plus every blob keyed by its digest; left open -- the storage engine, indexes and compaction. a host index is explicitly never authority; resolution goes through digests

## Coverage limitations (disclosed, not design gaps)

- section 6 CANDIDATE-ONLY custody (group bytes, sourceBodies id/path/universe/snapshot joins, complete examinedPaths, complete-empty envelope) is IMPLEMENTED in the retained closure and in the independent Area-3 instrument, but no positive Run declares a clones-near / clones-cross-tsjs cell, so no CandidateProducerResultV1 exists to exercise it
  - why not a gap: the kit publishes the law completely; this is a limit of this origin's own fixture set, recorded as an exercise gap. The equality law passes VACUOUSLY on all five Runs and is reported that way, and a cell whose capability is candidate-only is refused when it owes an envelope and has none
  - measured where: `vectors/indep-execution-inputs.json SECTION_6_CANDIDATE_CUSTODY_IS_UNEXERCISED_BY_THIS_RUN`
- a SELECTED-but-UNAVAILABLE enumerator binding (status selected, universe null) appears in no positive Run: the only unavailable binding is the optional-unselected shape, so the `unavailable-binding` typed null-stage reason and the `provider-unavailable` unavailable RECEIPT are reached by controls and by law-branch measurements rather than by a Run
  - why not a gap: both shapes are published and both are implemented and measured
  - measured where: `vectors/execution-inputs-negative-controls.json null-stage-reason-swapped; vectors/repair-closed-world-selection.json lawBranchControls`
- every positive Run declares exactly ONE execution-plan stage, so receipt totality over several stages is exercised by a control rather than by a positive
  - why not a gap: the totality law is implemented and measured
  - measured where: `vectors/execution-inputs-negative-controls.json execution-plan-stage-without-a-receipt`
- the required-UNSUPPORTED-TYPED case IS now exercised by a positive Run (syntax-data requests the imports cell as required), so the generation-19 limitation about it is withdrawn; what remains unexercised is a required cell whose row is UNAVAILABLE rather than complete
  - why not a gap: the bridge class for it is implemented and measured by the enumeration controls; no published law lacks a measurement
  - measured where: `runs/syntax-data.store.json proof executionDeficiencies: one required-execution deficiency carrying the MATRIX pair on a COMPLETE row`
- atom contract section 4 for the INCOMING endpoint (search-accounting table) and an endpoint=target atom are measured only on typed synthetic models: no retained Run has such an atom
  - why not a gap: the clauses are published; lib/indep_atom_law.py derives them from the text and labels the models synthetic
  - measured where: `vectors/indep-atom-law.json lawVectors + claimLimits`
- no retained Run has a non-empty atom filter, an imported count-at-most/all-covered atom or a vcs-revision staleness correspondence; the independent atom instrument raises NotExercised if it meets one
  - why not a gap: a limit of this origin's fixtures, not of the published law
  - measured where: `vectors/indep-atom-law.json claimLimits`
- the measured read graph hooks every stage process but not the child processes a stage spawns (Run builders, fresh-process replays): their writes are measured by a post-stage snapshot, their reads are not
  - why not a gap: a limit of this origin's own instrument, disclosed
  - measured where: `notes/v23-read-graph.json + notes/v23-stage-io/`
- the admitted TypeScript Run carries only imports@resolved-target as a graph-projectable relation, no IncomingSearchV1, no unresolved-edge fact and no weaker-rung fact inside a selected view, so the incoming-search-incomplete, unresolved-edge-present, unsupported-rung-omitted and resolution-* disclosure branches and the single-kind external/unknown vertex rule are implemented but not reached by a retained graph
  - why not a gap: the clauses are published; a limit of this origin's fixtures
  - measured where: `query/graph-query-reconstruction.json vertexDomain + indep-query-surface.json`
- candidate.list, inspection.show, review.brief and availability.show have actual schema-admitted records but no retained projection bound to the queried Run, so they are schema-only (I-Q9); the availability state `unavailable` is not exercised (V23-S3)
  - why not a gap: disclosed per operation in the artifact layersMeasured field
  - measured where: `query/indep-query-surface.json rawRequestAndResponseRecords`
- four comparison scenarios need a baseline or current side no retained Run provides (an alternative runtime payload, a narrower scope, a prior detector, an empty population); those sides are labelled synthetic helper-only and only the real side is bound to an export
  - why not a gap: the comparison law is executed over labelled premises and re-derived
  - measured where: `vectors/comparison-premises.json syntheticHelperOnly`
- every retained Run is sealed indeterminate, so the success and policy-failed public termination examples cannot be bound to a retained Run and carry labelled synthetic Run identities
  - why not a gap: the examples follow the command-inventory goldens they cite
  - measured where: `envelopes/public-termination.json`
- a js-synthesized CELL appears in no positive Run, so the SYNTHESIZED programEntry provenance is measured at the law level over synthetic parameters
  - why not a gap: the clause is published and all three provenances are measured
  - measured where: `vectors/program-entry-law.json`

## Helper corrections (helper bug != design gap)

| id | generation | status | where |
|---|---|---|---|
| V15-D1 | consumer-b.v15 | corrected | lib/rebind_v15.py, lib/verify_kit.py |
| V15-D2 | consumer-b.v15 | corrected | lib/run_ts.py language mode of record |
| V15-D3 | consumer-b.v15 | corrected | lib/opensip_schema.py _resolve_local |
| V15-D4 | consumer-b.v15 | corrected | lib/run_*.py VCS observation kind |
| V16-D1 | consumer-b.v16 | corrected | lib/opensip_schema.py walk_keywords / _resolve_local |
| V16-D2 | consumer-b.v16 | corrected | lib/opensip_build.py component-manifest description |
| V16-R1 | consumer-b.v16 | reconstruction-strengthening (NOT a helper bug and NOT a kit defect) | lib/run_ts.py, lib/run_ts_full.py -- the TypeScript subject and Run |
| V17-D1 | consumer-b.v17 | corrected | lib/phase0.py ANCESTRY table, after the v16->v17 path rebind |
| V17-D2 | consumer-b.v17 | corrected | lib/opensip_closure.py check_policy_admission filter admissibility |
| V17-D3 | consumer-b.v17 | corrected | lib/opensip_closure.py (no kind law at all) + run_syntax_code_full.py and run_rust_full.py disabled probe rules |
| V17-D4 | consumer-b.v17 | corrected | lib/opensip_closure.py (no enumeration checker) + all four non-data Run fixtures |
| V17-D5 | consumer-b.v17 | corrected (and withdraws the v16 advisory V16-A2) | lib/opensip_closure.py execution-inputs derivation + run_syntax_code.py unavailable binding |
| V17-D6 | consumer-b.v17 | corrected | lib/phase7.py multi-step invocation + lib/envelopes.py (no join checker) |
| V17-D7 | consumer-b.v17 | corrected | lib/phase6_repair.py FileEdit admission |
| V17-D8 | consumer-b.v17 | corrected, with an irreversible side effect reported in full | lib/rebind_v17.py SELF_EXCLUDE, lib/check_siblings_untouched.py, lib/helper_corrections.py |
| V16-A1 | consumer-b.v16 | self-correction | this origin's own v15 SHOULD about the native retention catalogue |
| V18-D1 | consumer-b.v18 | corrected | lib/rebind_v18.py + lib/phase0.py ANCESTRY table and its historical note |
| V18-D2 | consumer-b.v18 | corrected | lib/run_syntax_code.py and lib/run_syntax_data.py UnitMembershipV1 records, plus lib/opensip_closure.py (which had no U-1..U-4 law at all) |
| V18-D3 | consumer-b.v18 | corrected | lib/run_ts_full.py default-unit program binding + lib/opensip_closure.py check_enumeration_plan (no programEntry provenance law) |
| V18-D4 | consumer-b.v18 | corrected | lib/run_ts_full.py, lib/run_rust_full.py, lib/run_rust_partial.py membership rows |
| V18-D5 | consumer-b.v18 | corrected | lib/run_syntax_code.py unavailable binding AND its retained inventory, plus lib/opensip_closure.py check_enumeration_carrier_pair (new) |
| V18-D6 | consumer-b.v18 | corrected | lib/helper_corrections.py ROWS (the generation field of V17-D1..V17-D8) and the V17-D1 narrative sentence, plus the stale consumerId in main() |
| V18-D7 | consumer-b.v18 | corrected at generation 19 (identified at 18, measured and removed at 19) | lib/opensip_closure.py check_execution_inputs_derivation, the all-accounts-unsupported branch of the derived-state ladder |
| V18-D8 | consumer-b.v18 | corrected at generation 19 (PREDICTED at 18, MEASURED and repaired at 19) | lib/run_syntax_code.py / run_ts_full.py / run_rust_full.py / run_rust_partial.py clones-fact cell outcomes, and lib/opensip_closure.py (the clause is absent there entirely) |
| V19-D1 | consumer-b.v19 | corrected | lib/opensip_capmanifest.py, lib/opensip_schema.py (four helper-correction narratives) and lib/deliver.py sameOriginAncestry |
| V19-D2 | consumer-b.v19 | corrected | lib/rebind_v19.py own docstring |
| V19-D3 | consumer-b.v19 | corrected | lib/run_ts_full.py, lib/run_rust_full.py, lib/run_rust_partial.py, lib/run_syntax_data.py accounts + lib/opensip_closure.py (no matrix requirement) |
| V19-D5 | consumer-b.v19 | corrected | lib/phase7.py multi_unit_missing_caps (vectors/multi-unit-missing-caps.json) |
| V19-D4 | consumer-b.v19 | corrected | lib/phase6_repair.py schema_admit and four control inputs |
| V20-D1 | consumer-b.v20 | corrected (reconciliation to a newly frozen clause) | lib/opensip_build.py applicability, lib/opensip_closure.py and lib/indep_execution_inputs.py |
| V20-D2 | consumer-b.v20 | corrected (reconciliation to a newly frozen clause) | lib/opensip_build.py account construction + both checkers |
| V20-D3 | consumer-b.v20 | WITHDRAWN by this origin | lib/opensip_closure.py UNSUPPORTED_TYPED_CONTRADICTED_BY_A_RETURNED_PARTITION |
| V20-D4 | consumer-b.v20 | corrected (reconciliation to a newly frozen clause) | lib/opensip_build.py cross_source_items/primary_pair, lib/opensip_closure.py, lib/indep_execution_inputs.py |
| V20-D5 | consumer-b.v20 | corrected (reconciliation to a newly frozen clause) | lib/opensip_compose.py execution_deficiencies |
| V20-R1 | consumer-b.v20 | reconstruction-strengthening (NOT a helper bug and NOT a kit defect) | lib/indep_query_surface.py (new), lib/indep_mutation_surface.py (new), lib/run_syntax_data.py imports cell |
| V20-D6 | consumer-b.v20 | corrected | lib/helper_corrections.py, lib/phase6_repair.py, lib/deliver.py standing |
| V22-D1 | consumer-b.v22 | corrected | lib/helper_corrections.py V19-D2 sentence (damaged bytes kept in lib.before-image.v20), lib/label_history_v22.py, lib/rebind_v22.py |
| V22-D2 | consumer-b.v22 | corrected (reconciliation to the newly frozen atom contract, plus deviations it exposed) | lib/opensip_eval.py evaluate_native_atom, lib/opensip_compose.py eval_node |
| V22-D3 | consumer-b.v22 | corrected | lib/opensip_eval.py evaluate_imported_atom |
| V22-D4 | consumer-b.v22 | corrected | lib/status.py (generation-20 bytes in lib.before-image.v20), lib/audit_claimed_positives.py |
| V22-D5 | consumer-b.v22 | corrected | lib/opensip_eval.py sufficiency_v2 and subject_occupies |
| V22-D6 | consumer-b.v22 | corrected | lib/phase6_repair.py mutation keys (vectors/mutation-keys.json) |
| V22-D7 | consumer-b.v22 | corrected | lib/phase3_traces.py, lib/phase6_config.py, lib/phase1.py |
| V22-D8 | consumer-b.v22 | corrected | lib/verify_all.py stage order |
| V22-D9 | consumer-b.v22 | corrected | lib/verify_kit_v22.py custody |
| V22-D10 | consumer-b.v22 | corrected | lib/phase0.py, phase1.py, phase2.py, phase4.py, phase6_config.py, phase6_rest.py, phase7.py, phase8.py, phase10.py, indep_query_surface.py (generation-20 artifacts in predecessors.v20, generation-20 modules in lib.before-image.v20) |
| V22-D11 | consumer-b.v22 | corrected | lib/verify_all.py stage order and READS, lib/phase0.py, lib/stage_launcher_v22.py, lib/read_graph_v22.py |
| V22-D12 | consumer-b.v22 | disclosed -- the generation-20 claim is not repeated | generation-20 blind-review.json retainedArtifactDigestStanding.reproducibilityMeasured and helper row V20-D6 |
| V22-D13 | consumer-b.v22 | corrected | lib/opensip_schema.py walk_keywords (generation-20 bytes in lib.before-image.v20) |
| V23-D1 | consumer-b.v23 | corrected (the generation-22 V22-D3 reading is withdrawn; that row stays as written) | lib/opensip_eval.py evaluate_imported_atom (the generation-22 function is kept as evaluate_imported_atom_v22_reading for the control only), lib/run_ts_full.py |
| V23-D2 | consumer-b.v23 | corrected | lib/opensip_eval.py sufficiency_positions / dependency_view; lib/indep_atom_law.py (generation-22 interpretation I-A1 withdrawn) |
| V23-D3 | consumer-b.v23 | corrected | lib/opensip_eval.py require_scope_carrier / dependency_view, lib/phase6_clones.py |
| V23-D4 | consumer-b.v23 | corrected | lib/label_history_v23.py SELF_ATTRIBUTION |
| V23-D5 | consumer-b.v23 | extended (the clauses are new; not a defect of an earlier claim) | lib/indep_atom_law.py law vectors, predecessor controls, claimLimits |
| V23-D6 | consumer-b.v23 | corrected | lib/phase8.py (hand-written comparison helpers removed), lib/comparison_law.py, lib/indep_comparison_law.py; generation-22 records in predecessors.v22/vectors |
| V23-D7 | consumer-b.v23 | corrected | lib/graph_query.py (generation-22 artifact: predecessors.v22/query/graph-query-reconstruction.json) |
| V23-D8 | consumer-b.v23 | corrected | lib/indep_query_surface.py (generation-22 artifact: predecessors.v22/query/indep-query-surface.json) |
| V23-D9 | consumer-b.v23 | corrected | lib/phase8.py purge_replay_output (generation-22 bytes: predecessors.v22/vectors/phase8-all.json) |
| V23-D10 | consumer-b.v23 | corrected | lib/phase7.py analysis_result / single_step / multi_step (generation-22 bytes: predecessors.v22/envelopes) |
| V23-D11 | consumer-b.v23 | corrected | lib/phase8.py public_termination (generation-22 bytes: predecessors.v22/envelopes/public-termination.json) |

### V23-D1

- original failure: V22-D3 made observed-hit the ONLY match of every runtime `exists` atom. The newly frozen section 6 decides the unfiltered case the other way: "an unfiltered `exists` tests whether a consumable mapped runtime observation exists, so either `observed-hit` or `observable-unhit` can satisfy it. An `observability` filter restricts the matching polarity set before applying the quantifier". Under the generation-22 reading the TypeScript rule.c had carried its "observed" intent in the evaluator, not in its filter.
- kit selector: foundation/atom-evaluation-contract.v1.md section 6 "Runtime polarity"; foundation/evaluator-projection-registry.v1.json importQuantifiers
- correction: the matching set is the registry polarity set restricted by the atom filter; rule.c now declares observability=observed-hit and the unfiltered rule.e-runtime-mapped-observation measures the other branch. Measured: TypeScript findings 3 -> 5 (rule.e true on two subjects, indeterminate with unobservable-subject on the third); lib/indep_atom_law.py re-derives both branches and refuses a tamper that applies the V22-D3 reading to the unfiltered rule

### V23-D2

- original failure: I-A1 read "a dependency contributing no selected Coverage occupies no position" as: an absent dependency adds no cause. The frozen section 4 says the removed position "answers `required-relation-missing`, exactly as an absent relation does", and requires a view with a same-kind totality gap to be evaluated with AND without the gap positions. Measured on the rust Run: rule.a-no-clone-in-crates keeps value false but now retains coverage-unknown + required-relation-missing; rule.c-at-most-one-body true -> indeterminate; findings 8 -> 7.
- kit selector: foundation/atom-evaluation-contract.v1.md section 4 "Dependency totality (same kind)" items 1-4; docs/v2/contracts/product-v1/native-evidence.md section 4.6
- correction: an absent dependency answers required-relation-missing; both native answers of a gap view are retained in nativeDeficiencies; the independent instrument measures totality and refuses a tamper re-applying I-A1

### V23-D3

- original failure: a scope with an absent or null enumeratorClosure could be paired, dependency pairing could fall back to a mapped scope outside the exact (relation, rung, S) selection, and the synthetic min-resolution scopes of phase 6 carried no enumeratorClosure
- kit selector: foundation/atom-evaluation-contract.v1.md section 4 "Admitted inputs for these cases" items 1-2 ("refused `ATOM_NATIVE_CARRIER` wherever it is paired", `INCOMING_SEARCH_SCHEMA`, `INCOMING_SEARCH_SCOPE_MISJOIN`) and "There is **no mapped-scope fallback**"
- correction: pairing validates the carrier and selects exact scopes only; the synthetic scopes carry the TypeScript provider closure and absent/null carrier controls are refused; the atom-law vectors measure both IncomingSearchV1 refusals and the explicit empty-subject scope that closes an empty program

### V23-D4

- original failure: after the generation-23 rebind the label-provenance audit reported drift on a line that checks the CURRENT origin id, because its classifier had no current-origin keyword
- kit selector: not a kit question: charter "keep historical labels" and "Current consumerId ... become 23"
- correction: the classifier recognises CURRENT_ORIGIN; the audit reports no historical label drift and no historical sentence was touched

### V23-D5

- original failure: the instrument had no vector for I1 (subject universe with no available binding), dependency totality, runtime polarity, carrier/attestation admission or the explicit empty-subject scope
- kit selector: foundation/atom-evaluation-contract.v1.md sections 4 and 6 as frozen for generation 23
- correction: each clause has a law vector derived from the text; the generation-22 AND generation-20 exports are refused as predecessors

### V23-D6

- original failure: the generation-22 comparison and baseline records were emitted by helpers that did not apply the comparison verdict law to the current Run: baseline-audit, evidence-changed, scope-policy-only and pivot-only-fingerprints all said verdict=pass although the current TypeScript proof carries required-execution deficiencies; scope-policy-only reported E2 not-needed with the scope axis changed; pivot-only-fingerprints had no policy axis and no E1 pivot. The audit only re-admitted those records.
- kit selector: docs/v2/contracts/product-v1/workflows-and-surfaces.md sections 2-3; workflows/workflow-projection-contract.v3.md sections 9-12
- correction: every scenario is derived from retained premises by comparison_law.py and re-derived by a separate instrument (6/6 scenarios); measured verdicts are now indeterminate for the real current side, pass only for the labelled-synthetic empty result, not performed for the missing context document; the audit checks the independently derived fields

### V23-D7

- original failure: schema-admitted but not the contract: an external resolved target was dropped as unprojectable; neighbor rows were ordered by fact2 id only; a full page reported truncated=true; cursors were `ord:N`; graph.path counted the whole inventory as visited and was not the FIFO BFS; deficiencyCitations read a proof key that does not exist; unsupported-rung-omitted was emitted for a rung the Run merely lacks; fault codes were typed by hand per case
- kit selector: workflows/query-projection-contract.v3.md sections 1-8; workflows/schemas/evaluator3/graph-query.schema.json
- correction: a section-8 executor produces every outcome from the retained request and labelled host observations (22 answered cases, 24 failure envelopes, 1 reference-call precondition); lib/indep_query_surface.py recomputes all 46 with separately written code (0 disagreements) and detects all 10 re-injected defects

### V23-D8

- original failure: its own graph records set target := source and cited every Coverage; finding.list includeSuppressed=false listed the waived finding3:8f9e465...; baseline.show and receipt.show read keys the records do not have and so were empty; availability.show came from an unrelated scenario; coverage=complete was asserted for every operation
- kit selector: workflows/schemas/evaluator3/graph-query.schema.json Params, GraphQueryResponseContext
- correction: graph outcomes are recomputed, not re-authored; the seventeen other operations derive rows from the Run, both includeSuppressed values are measured and the audit re-derives them from the store; operations with no retained projection are schema-only and say so (I-Q9)

### V23-D9

- original failure: present since the envelope was first built: missing retained replay input was indeterminate exit 3 with a coverage reason code, and OUTPUT.FORMAT_NOT_APPLICABLE was paired with REQUEST.PRECONDITION_FAILED; the requirement's named observable envelopes/purge-replay-output-failure.json was never written; the audit only re-admitted the envelopes
- kit selector: docs/v2/contracts/product-v1/identity-and-evidence.md section 5 "Inability encountered during a selected operation remains HOST.IO_FAILURE with evidence detail (exit 4)"; workflow-projection-contract.v3.md section 0; command-inventory.v3.json golden sarif-not-applicable
- correction: HOST.IO_FAILURE / host-io / exit 4 and REQUEST.UNKNOWN_OPTION; each case names its event position and owner; the named file is written; the audit derives each route from the kit sentence or golden

### V23-D10

- original failure: every AnalysisResult said requiredCoverage=satisfied, deficiency=none, and every analysis step and the single-step envelope terminated SUCCESS exit 0, although every retained Run is sealed indeterminate with a required-execution deficiency; the comparison step hard-coded verdict=pass with 3 entries. Only schema shape and the invocation joins were checked.
- kit selector: docs/coop/artifacts/d9-exit-contract.v1.14.json scenarios analysis-required-coverage-missing and analysis-language-tier-unsupported; foundation/evaluator-composition-contract.v3.md section 9.6; native-evidence.md section 10 precedence; invocation-record ComparisonStepResult
- correction: the projection is derived from proof.executionDeficiencies and the sealed verdict: TypeScript and rust are requiredCoverage=unsatisfied, deficiency=required-relation-missing, termination indeterminate exit 3 with COVERAGE.REQUIRED_RELATION_MISSING and the cited coverageId; the comparison step projects the re-derived comparison (indeterminate, 5 entries); the audit re-derives each field from the store and the D9 scenario rows

### V23-D11

- original failure: the success and policy-failed examples bound verdicts pass and fail to the REAL TypeScript Run (sealed indeterminate); request-rejected paired REQUEST.UNKNOWN_OPTION with CONFIG.INVALID; indeterminate paired a coverage reason with evidence.missing; operational-failed paired LEDGER.BUSY_TIMEOUT / ledger-busy with storage.backup-choice-required; the interrupt carried an evidence.missing error. Only schema admission and the exit table were checked.
- kit selector: workflows/command-inventory.v3.json goldens default-first-use-durable, analyze-policy-failed, import-unmapped-artifact, audit-required-coverage-unknown-zero-findings, default-closure-bytes-corrupt, interrupted-before-settle; workflows-and-surfaces.md section 1 "Cancellation"
- correction: each example reproduces the golden it cites; Run identities no retained Run can supply are labelled synthetic helper-only; the interrupt is a cancelled invocation with no Run; the audit compares every field with the golden

Open helper failures on a claimed positive: **0**.

## Limitations and scope

- Every compiler, provider, toolchain, OS and runtime observation in these Runs is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a compiler, provider, host or operating system, and no such qualification is claimed.
- No product code was written, no repository was modified, no commit or push was made, and no product was executed. Every byte produced lives under this origin's own generation-23 output directory.
- The parent subject was never held. Only the disclosed kit and the parent digest declared inside its manifest were verified.
- 16 claimed positives are graded schema-admitted-record (R-CANDIDATE-ONLY-CLONES, R-CONFIG-CUSTOM-MULTI-BASE, R-CONFIG-JS-SHARED-BASE, R-CONFIG-SYNTHESIZED, R-DURABLE-RECEIPT-AVAILABILITY, R-ENVELOPE-CONFIG-INPUT, R-ENVELOPE-EXTERNAL-INPUT, R-ENVELOPE-HOST-INVALID, R-ENVELOPE-PRODUCER-BOUNDARY, R-MIN-RESOLUTION-REPAIR-EVIDENCE, R-MULTI-UNIT-MISSING-CAPS, R-MUTATION-REPLAY-SCOPE, R-PINNED-PURGE, R-PUBLIC-FROM-INTERNAL-REFUSAL, R-REPAIR-DESCRIPTOR, R-TEST-PREP-REPAIR-AUTH): each record is re-admitted against its owning schema and its identities and Run joins are recomputed, which is the evidence class accepted for its requirement kind. Their remaining semantic fields were SURVEYED against their owners in generation 23 rather than re-derived by a separate instrument; the survey found and corrected positives in other classes (V23-D6..V23-D11).
- The repair, comparison, baseline, invocation, authorization and query records are RECORD reconstructions with their identities recomputed and their admission laws executed. No repair was previewed, applied or authorized; no test or preparation ran; no baseline was adopted; no query engine was run by a product. Fields that name records this origin did not construct are labelled helper-only.
- L1-L3 normalised body identities, symbol-to-path attribution and provider occupancy are not recomputable by a consumer; the kit says so and substitutes retained custody, which is what was executed.
- 3 of the 6 advertised language modes (js-synthesized, rust-cargo-prepared, ts-tsconfig) have an admitted representable path at the record level but were NOT exercised end-to-end on a sealed Run (vectors/advertised-mode-paths.json).
- Coverage limitations that are not design gaps are listed with the artifact that measures each in coverageLimitationsDisclosedNotDesignGaps; none is merged into the complete-positive claim.
- No root admission, agreement, expected result, author model, checker or golden was supplied, read or inferred. The root outcome over these exact bytes is UNOBSERVED by this origin.

Artifact digests: the sha256 of every exported artifact AS READ by this reconciliation stage, 145 rows, re-derived by each command from the bytes on disk. Artifacts written AFTER this stage by the command (none are declared) would not be in it.

Reproducibility: NOT re-measured in generation 23. The generation-20 report claimed a three-command leaf comparison through diagnostics outside output/ that were never exported (helper-corrections V22-D12), so that claim is not repeated here.

## Standing

- **noRootAdmissionClaim**: this origin reports ONLY its own independently executed admission, closure, replay, audit and controls. It does not claim that any root, author or successor admitted, agreed with or validated these bytes.
- **noProductQualificationClaim**: nothing here authorizes a product implementation or qualifies any product, component, compiler, provider or host.
- **kitOnly**: every citation names a path and selector inside the frozen kit. The disclosed PRIOR-OWN inputs are named in notes/v23-input-custody.json disclosedPriorInputs and are, verbatim from that artifact: output/ -- an exact copy of this origin's OWN generation-22 work, READ and being continued; previous-turn-response.md -- this origin's OWN generation-22 closing response, READ; requirements.before23.json -- the generation-22 requirement metadata, preserved; only inputKit was updated (measured above)
- **nothingElseClaimedAsAnInput**: no author implementation, control, expected output, golden, root replay/refusal report, root verdict or source-author diagnosis was supplied or read
- **runtimeFilesNotNamedAsInputs**: {"files": ["dispatch.json", "launch.py", "process.json", "prompt.md", "public-events.jsonl"], "standing": "present in the runtime, listed by name only, NOT opened or used"}
- **pathCensus**: CLEAN
- **priorGenerationsUnmodified**: {"method": "os.walk over directory metadata only, comparing each tree's newest modification time with a FIXED anchor write this session made inside generation 23. No file content of any earlier generation was opened.", "anchor": "notes/v23-rebind.json (written once, by the single generation-23 rebind run)", "anchorWriteUtc": "2026-09-12T20:56:56Z", "trees": [{"generation": "consumer-b.v14", "present": true, "fileCount": 227, "newestMtimeUtc": "2026-09-12T09:15:20Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v15", "present": true, "fileCount": 301, "newestMtimeUtc": "2026-09-12T09:39:10Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v16", "present": true, "fileCount": 461, "newestMtimeUtc": "2026-09-12T11:54:34Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v17", "present": true, "fileCount": 575, "newestMtimeUtc": "2026-09-12T11:52:40Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v18", "present": true, "fileCount": 708, "newestMtimeUtc": "2026-09-12T12:47:41Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v19", "present": true, "fileCount": 841, "
- **writeConfinement**: {"foreignWriteOrRootAssignmentsInActiveCode": 0, "foreignSplitLiteralRootAssignmentsInActiveCode": 0, "liveProbeResolvedBeneathThisRuntime": true, "noActiveModuleImportsAnArchivedOrQuarantinedTree": true, "badImports": [], "result": "CONFINED"}
- **historyStanding**: CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
- **generationLabelProvenance**: {'verdict': 'NO HISTORICAL LABEL DRIFT', 'method': "the earliest before-image containing the SAME sentence (with the label masked) carries that sentence's true generation; a later copy that disagrees was rewritten by a mechanical rebind. Helper rows are also checked directly against their own id.", 'standing': 'audited against the retained before-images before any copied code ran and again after every stage; the one drift found at generation 22 (a generation-19 sentence rewritten by the generation-20 rebind) was restored from its before-image (V22-D1); at generation 23 the only report was a false positive on a current-origin check, corrected in the classifier (V23-D4)'}
- **writesMadeUnderAPriorGeneration**: generations modified during this session, measured in notes/v23-history-standing.json measuredC: []
  - still open from generation 17: the GENERATION-17 session overwrote TWO files under the generation-16 output before its own control caught the defect: helper-corrections.json and notes/siblings-untouched.json. The prior bytes were not retained by this origin and are NOT claimed to be restorable. The item stays OPEN and is carried forward rather than marked clean (helper-corrections V17-D8).

