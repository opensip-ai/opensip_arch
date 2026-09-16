# OpenSIP blind consumer design review -- consumer-b.v22

**Verdict: ACCEPT-RECONSTRUCTABLE**

| | |
|---|---|
| sessionId | `79569ae1-10f4-4181-972b-334f7ed2f07a` |
| same-origin ancestry | consumer-b.v14 -> consumer-b.v15 -> consumer-b.v16 -> consumer-b.v17 -> consumer-b.v18 -> consumer-b.v19 -> consumer-b.v20 -> consumer-b.v22 (generation 21 prepared, never launched) |
| subject manifest SHA-256 | `f98d3eb0b7570470cdc85b7033e4558e67d3f66135293aa99897ca7a29951526` |
| parent digest declared in that manifest | `bd00c07d910e1fa7769b0aab5b180a96e984a255df849b5a96dc563ccbf8f3c6` (PASS) |
| kit files verified | 102 / 102 (PASS) |
| measured normative delta | 101 unchanged, 1 changed, 0 added |
| changed owner | `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` |
| requirement status | executed 131, futureQualification 3 |
| claimed-positive audit | {'PASS': 126, 'DEFERRED': 5} |
| new MUST / SHOULD / advisories | 0 / 0 / 1 |

> This is NOT a parent whole-candidate verification: only the parent digest declared inside
> the held manifest was compared. No root admission, agreement, expected result, author
> model or checker was supplied, read or inferred; the root outcome over these exact bytes
> is unobserved by this origin. Nothing here qualifies any product, compiler, provider or
> host; every toolchain and host observation is a synthetic trusted input.

## Why this verdict

ACCEPT-RECONSTRUCTABLE requires: every acceptBlocking requirement executed with evidence sufficient for its kind (claimed-positive audit, not presence or counts), no claimed-positive audit failure, no unresolved MUST or SHOULD, no open helper failure on a claimed positive, every complete Run closed, replayed, controlled and admitted by the independent atom law, every preceding stage of this command exited zero, and the measured read graph of this command passes. MEASURED: 0 acceptBlocking not executed, 0 audit failures, 0 MUST, 0 SHOULD, 0 open helper failures, Runs ok = True, preceding stages ok = True, read graph ok = True.

- acceptBlockingRequirementsNotExecuted: **none**
- phase11RowsFailed: **none**
- claimedPositiveAuditFailures: **none**
- newMustIssueCount: **0**
- newShouldIssueCount: **0**
- openHelperFailuresOnAClaimedPositive: **none**
- everyCompleteRunClosedReplayedControlledAndAtomLawAdmitted: **True**
- everyPrecedingStageOfThisCommandExitedZero: **True**
- measuredReadGraphOfThisCommandPasses: **True**
- thisIsTheFinalReconciliationStage: **True**

## What changed in the input

- kind: NORMATIVE SUCCESSOR; MEASURED per path against this origin's own retained generation-20 per-file map (notes/v20-input-custody.json); the supplied normative-delta.json hash inventory was then VERIFIED against both sides rather than adopted (notes/v22-input-custody.json claim 5).
- what the changed owner decides: foundation/atom-evaluation-contract.v1.md section 4 now publishes: a completeness result {complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies} that is independent of truth (a known match decides exists/none/count-at-most); the selection order of scopes and Coverage; the AtomCauseV1 representation; the shared prelude P1 (unavailable owed bindings, foreign-family edges not owed) and P2 (no owed binding); outgoing cause derivation steps 1-4 (selector-unbound, uncovered-expected-source-subject for the CURRENT subject only, scope-without-coverage per unpaired scope, coverage-unknown per paired Coverage); the deterministic DEPENDS_ON dependency view with its fold and coverage-unknown carrier; the incoming search-accounting table; and the section-5 quantifier split.
- consequence: every retained Run was re-evaluated under the new clauses (V22-D2), which also exposed an imported-polarity defect present since generation 14 (V22-D3); all five Runs were rebuilt, re-exported, re-closed, re-replayed and re-controlled, and an independent atom-law instrument that does not import the evaluator admits all five and refuses all five generation-20 predecessors.

## Complete positive Runs

| Run | runId | verdict | objects | blobs | closure | replay | controls | atom law |
|---|---|---|---|---|---|---|---|---|
| syntax-code | `run3:00b039cc63d8db342...` | indeterminate | 51 | 135 | 877 passed / 25 n-a / 0 refused | REPLAY_MATCH (2 findings, 6 witnesses) | 14, all refused: True | 6 atoms, 61 checks, 0 refused |
| typescript | `run3:7df13bbed9374cb5e...` | indeterminate | 58 | 177 | 1056 passed / 18 n-a / 0 refused | REPLAY_MATCH (3 findings, 18 witnesses) | 14, all refused: True | 12 atoms, 108 checks, 0 refused |
| rust | `run3:deae01b209903b6e7...` | indeterminate | 82 | 201 | 1192 passed / 27 n-a / 0 refused | REPLAY_MATCH (8 findings, 19 witnesses) | 14, all refused: True | 19 atoms, 190 checks, 0 refused |
| rust-partial | `run3:b4500bf8f0750a754...` | indeterminate | 88 | 192 | 747 passed / 16 n-a / 0 refused | REPLAY_MATCH (3 findings, 7 witnesses) | 14, all refused: True | 7 atoms, 84 checks, 0 refused |
| syntax-data | `run3:47fa680d35d319939...` | indeterminate | 53 | 136 | 804 passed / 28 n-a / 0 refused | REPLAY_MATCH (6 findings, 12 witnesses) | 14, all refused: True | 12 atoms, 139 checks, 0 refused |

- `runs/syntax-code.store.json` sha256 77eae9b95d39f95ea00a6c5ac404685897818105a607e83eb583d42cf9f51d87
- `runs/typescript.store.json` sha256 41702998335ae97dfd168db1458921c7dda03ffc62ea08e8dfb445de9b0567e3
- `runs/rust.store.json` sha256 ffe8d851e754dce760ddfbbd7cd14b1b8f8db68ea0bf057a0edbfdf2cad6ecef
- `runs/rust-partial.store.json` sha256 e9abe46f8dc087bd8e1a25e5d7a3286046212819d779755aebcffbfe1759d8d5
- `runs/syntax-data.store.json` sha256 53f4b9074968194aa971f32bff02a4761b410d0c30110fb8adfeff1d45a11428

## Claimed-positive audit (every requirement, from its final bytes)

Counts: {'PASS': 126, 'DEFERRED': 5}. Evidence classes: {'reconstructed-behavior': 72, 'measured-control': 13, 'cited-kit-distinction': 3, 'standing-record-verified': 16, 'schema-admitted-record': 27}.

each requirement was re-checked from its FINAL bytes in a fresh process. The evidence class says what the re-check actually is; a static comparison, a shape-only check or a helper assumption never makes a requirement executed. The five phase-11 rows are decided by the requirement-status stage after this deliverable is written.

| id | kind | evidence class | result | checks passed | first refusal |
|---|---|---|---|---|---|
| R-ACYCLIC-JOINS | standaloneCanonicalVector | reconstructed-behavior | PASS | 2 |  |
| R-ADVERTISED-MODE-PATHS | standingRule | standing-record-verified | PASS | 2 |  |
| R-BASELINE-AUDIT | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
| R-BLOCKER-NOT-ADJUST | standingRule | standing-record-verified | PASS | 2 |  |
| R-CANDIDATE-ONLY-CLONES | standaloneConfigVector | schema-admitted-record | PASS | 5 |  |
| R-CAP-ADMISSION | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-CAP-NAMED-GATES | standaloneCanonicalVector | measured-control | PASS | 53 |  |
| R-CHAIN-ZERO-CONFIG-TO-RECEIPT | standingRule | standing-record-verified | PASS | 7 |  |
| R-CLONE-DEFICIENCY-PAIRING | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-CLONES-NEGATIVE-VECTORS | standaloneCanonicalVector | measured-control | PASS | 1 |  |
| R-CMP-EMPTY-RESULT | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
| R-CMP-EVIDENCE-CHANGED | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
| R-CMP-MISSING | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
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
| R-E0-VS-E1-E3 | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
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
| R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR | standaloneCanonicalVector | schema-admitted-record | PASS | 59 |  |
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
| R-MULTI-STEP-DIFFERENT-SELECTIONS | schemaEnvelope | schema-admitted-record | PASS | 4 |  |
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
| R-PIVOT-ONLY-FINGERPRINTS | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
| R-PROMISE-VS-AVAILABILITY | standingRule | standing-record-verified | PASS | 2 |  |
| R-PUBLIC-FROM-INTERNAL-REFUSAL | schemaEnvelope | schema-admitted-record | PASS | 6 |  |
| R-PUBLIC-TERMINATION-EXAMPLES | schemaEnvelope | schema-admitted-record | PASS | 20 |  |
| R-PURGE-REPLAY-OUTPUT-FAILURE | schemaEnvelope | schema-admitted-record | PASS | 20 |  |
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
| R-SCOPE-POLICY-ONLY-COMPARISON | standaloneCanonicalVector | schema-admitted-record | PASS | 4 |  |
| R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC | completeRunProperty | reconstructed-behavior | PASS | 9 |  |
| R-SELECTED-PROVIDER-CONTEXT | standingRule | reconstructed-behavior | PASS | 40 |  |
| R-SEMANTIC-VS-OPERATIONAL | standaloneCanonicalVector | reconstructed-behavior | PASS | 3 |  |
| R-SEMANTIC-VS-OPERATIONAL-AUTHORITY | standingRule | reconstructed-behavior | PASS | 3 |  |
| R-SINGLE-STEP | schemaEnvelope | schema-admitted-record | PASS | 3 |  |
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
- typescript: {'atoms': 12, 'checks': 108, 'passed': 108, 'refusals': 0}
- rust: {'atoms': 19, 'checks': 190, 'passed': 190, 'refusals': 0}
- rust-partial: {'atoms': 7, 'checks': 84, 'passed': 84, 'refusals': 0}
- syntax-data: {'atoms': 12, 'checks': 139, 'passed': 139, 'refusals': 0}
- predecessor `predecessors.v20/runs/syntax-code.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (10 refusals)
- predecessor `predecessors.v20/runs/typescript.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (9 refusals)
- predecessor `predecessors.v20/runs/rust.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (37 refusals)
- predecessor `predecessors.v20/runs/rust-partial.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (12 refusals)
- predecessor `predecessors.v20/runs/syntax-data.store.json`: refused True at `WITNESS_RECORD_EQUALS_DERIVED` (18 refusals)
- tamper syntax-code / a rule-level uncovered-expected-source-subject copied into the atom (A7): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- tamper syntax-code / selector-unbound carrying the subject universe (A6/A3): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- tamper typescript / an observable-unhit runtime row counted as an observed hit (A16): refused True at `PREDICATE_VALUE_EQUALS_DERIVED`
- tamper rust-partial / coverage-unknown with its typed nativeCause carrier dropped (A12): refused True at `WITNESS_RECORD_EQUALS_DERIVED`
- law vectors: 11, passed 11
- min-resolution atom-level cases: 34, refused 0
- claim limit: no retained Run has an endpoint=target atom: A17 is measured on typed synthetic models only and is labelled so
- claim limit: no retained Run has a non-empty atom filter, an imported count-at-most/all-covered atom, or a vcs-revision staleness correspondence: each raises NotExercised if met
- claim limit: subject SELECTION (composition s2) is not re-derived here; every subject checked is recomputed from its retained record and joined to a retained inventory row
- claim limit: the product evaluator is not imported; agreement is measured only by comparing the retained witness bytes with this derivation

## Query, mutation and authorization surfaces

- **wholePublishedQuerySurface**: {"instrument": "lib/indep_query_surface.py", "artifact": "query/indep-query-surface.json", "runUnderQuery": "run3:7df13bbed9374cb5ed0185a390ea33d4e56e6ec8b2aec273018d0b1166eba93f", "operationsWithActualRecords": 20, "checks": 110, "refusals": 0, "negativeControls": 8, "originalQueryArtifact": "query/graph-query-reconstruction.json (re-admitted by the audit)"}
- **wholePublishedMutationSurface**: {"instrument": "lib/indep_mutation_surface.py", "artifact": "vectors/indep-mutation-surface.json", "checks": 29, "refusals": 0, "negativeControls": 7, "measuredKeys": {"genericMutationIntent": "f0ccf0a61cbadbd4e88021ad5720e0c44da84309f61aab11ac82451065ad0e70", "repairApply": "07b803d488cc99ce81b8144cdcf7c774400a09e6bfe2f944cd4695ce49f43a66", "importStep": "fa366fd3edfc96613f34e31ec2f3df69ae0d8acc8f3db4ecd7856f0c249f828f", "nativePreparationStep": "e7090515a7670cc356b44776c9e73199605ff0cda7d3ccd06888432d265957b8"}}
- **authorizationRecords**: {"artifact": "vectors/test-prep-repair-authorization.json", "recordsAdmitted": 4, "controlsRefused": 7, "syntheticHelperOnlyFields": {"repair-apply": ["authorization.consent.policyRecordId (the policy record is not constructed)"], "test-execution": ["authorizationRef (the RepoExecutionGrantV2 grant is not constructed)", "argv0Source.path (no test runner is inventoried by this origin's Runs)"], "native-preparation": ["authorizationDescriptorDigest (AuthorizedExecutionV2 is not constructed)", "securityGrantSetRef"]}, "standing": "authorization RECORDS constructed and admitted against their owning schemas. NOTHING was executed: no test ran, no preparation ran, no repair was applied. Every field listed under syntheticHelperOnly names a record this reconstruction does not construct and is not evidence-bound."}

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v22/output/lib/verify_all.py
```

The command declares **53** stages; **52** preceding stages of this same command were recorded when this reconciliation ran; failed stages: **[]**. this deliverable is written by the FINAL stage of that command. verify-all.json is rewritten after every stage, so the row count above is every preceding stage of the SAME command; the only row it cannot contain is this stage's own exit, which the command appends after it returns.

- earlier command A (`notes/v22-stage-io/20260912T123018`): failed stages 6
  - phase 0 input custody -- AssertionError hashVerification: the current-kit pins still held the generation-20 manifest and parent digests (edited while the command was already running)
  - phase 8 baseline audit and comparisons -- jsonschema PointerToNowhere '/$defs/RepairApplyAuthorizationV1': the record lives under the security document's `schemas` member
  - MEASURED read graph (both runs) -- reads of retained before-images and of Run stores written by child processes were unclassified, and phase 0 read requirement-status.json/checkpoints before writing them
  - CLAIMED-POSITIVE AUDIT -- 9 FAIL: R-CAP-NAMED-GATES, R-CVE1-EIGHT-TYPES, R-D9-EXTENSION-PRECEDENCE, R-DETECTOR-COMPAT-FILE, R-FIVE-CONTRACTS-INDEX, R-MEASURED-NOT-COUNTS, R-NEGATIVE-FIRST-REFUSAL, R-TEST-PREP-REPAIR-AUTH, R-VALID-VS-INVALID-VS-EXPLANATORY
  - checkpoints for every phase -- phases 0, 1, 2, 7, 8, 9 had failed or unexecuted ids
- earlier command B (`notes/v22-stage-io/20260912T124314`): failed stages 6
  - phase 8 baseline audit and comparisons -- KeyError 'EnforcementValue' inside opensip_schema._resolve_local2 (V22-D13)
  - MEASURED read graph (both runs) -- the analyzer parsed only the literal READS assignment, not the effective table the command guarded with; phase-8 artifacts unknown because phase 8 failed
  - CLAIMED-POSITIVE AUDIT -- 6 FAIL: R-CAP-NAMED-GATES (ADM-ORDER list row retained no submitted manifest), R-D9-EXTENSION-PRECEDENCE (AnalysisResult is a oneOf; auditor error), R-DETECTOR-COMPAT-FILE and R-TEST-PREP-REPAIR-AUTH (stale: phase 8 failed), R-FROM-SCRATCH-COMMAND and R-MEASURED-NOT-COUNTS (failed stages, read graph REFUSE)
  - checkpoints for every phase (pre-deliverable and final) -- failed ids above, and the pre-deliverable run did not yet tolerate the five phase-11 ids
- earlier command C (`notes/v22-stage-io/20260912T124516`): failed stages 0
  - edits followed it: the V22-D8 correction text was made accurate (it was edited while C was running, so C's helper-corrections.json is not a clean record), the launcher now records each stage's outcome, and the command now writes a per-command receipt. The final report is written by the command that ran after those edits.
- earlier command D (`notes/v22-stage-io/20260912T124739`): failed stages 0
  - its report rendered the failed-stage count of A and B as the number of grouped lines (5 and 4) instead of the six failed stages each had; this record and the renderer were corrected and the command was run again

Measured read graph (`notes/v22-read-graph.json`): **PASS**; 51 stages logged, 116 edges, order violations 0, undeclared edges 0, unknown reads 0. Child-process reads are not measured.

## New MUST issues

None. newMustIssues is EMPTY because every observable this origin was required to produce had a published derivation that it could execute: the C/H recipes, the closing digest law and its four representations and retention modes, the capability-manifest gates, the relation/rung registry with its anchor, snapshot, totality and partition laws, the grammar-capability registry and its three enforcement boundaries, the section 1.2 mode table, the config node-kind law, the Rust context projection, the execution-inputs cell and account derivation, the composition section 9 proof/evidence/seal/Run joins, the repair descriptor and its two idempotency recipes, the comparison and baseline identities, the D9 class/exit table, and the graph-query operations with their bounds and mandatory disclosure. Where a value could not be recomputed (L1-L3 normalisation, symbol-to-path attribution, provider occupancy) the kit SAYS so and substitutes custody, which this origin executed rather than worked around.

## New SHOULD issues

None open. Earlier SHOULD items resolved by a normative successor:

- **V16-S1** -- the repair descriptor's closedWorld projection names "that same Run's ClosedWorldV2" without saying which Coverage entry owns it when a Run carries several that differ (RESOLVED BY THE NORMATIVE SUCCESSOR, at generation 19)
- **V16-S2** -- GlobPattern publishes a whole-segment `**` and one example, which does not decide whether a TRAILING `**` matches the files of that directory (RESOLVED BY THE NORMATIVE SUCCESSOR, at generation 19)

Blocker statement: no blocker on this origin's side from the design: newMustIssues and newShouldIssues are both empty, and every earlier SHOULD item is recorded as resolved by a normative successor. Whether this origin's OWN work is complete is decided separately, from the claimed-positive audit, the requirement status and the from-scratch command, never from this statement.

## Advisories

- **V16-A3** (wording) `traversalCoverage` and native CoverageResult share the word "coverage" while being different obligations
  - observation: the schema already says "Not native CoverageResult" in both places, which is why this is only advisory. The shared noun still invites a consumer to report a COMPLETE traversal over an INCOMPLETE evidence base as evidence completeness.
  - handled here by: the two are carried in different required fields and reported separately, with an explicit statement of why: see query/graph-query-reconstruction.json evidenceLimitationsVersusStoredEdgeCompletion.

## What the generation-22 successor decided about this origin's own readings

- **standing**: not design gaps: the generation-22 kit changes ONE file, the atom evaluation contract, and its new section-4 text decides questions this origin's atom evaluator had answered differently (helper-corrections V22-D2). The imported polarity defect (V22-D3) was found while re-reading section 6 and is not a change of text.
- **completenessIsIndependentOfTruth**: this origin let any cause block a negative answer; the contract gives a completeness result of its own and a known match decides exists/none/count-at-most regardless of it
- **enumerationUncertaintyIsRootNotAtom**: this origin censused every expected subject inside the atom; the contract restricts uncovered-expected-source-subject to the CURRENT subject
- **unavailableOwedBinding**: this origin emitted missing-relation-coverage with the subject universe; the prelude gives selector-unbound with a null universe, and a foreign family is a non-blocking cross-family-edge-not-owed disclosure
- **coverageUnknownCarrier**: this origin had no dependency view, fold or carrier; the contract publishes a deterministic DEPENDS_ON view, a fold and a first-non-null carrier

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
  - measured where: `notes/v22-read-graph.json + notes/v22-stage-io/`
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

### V22-D1

- original failure: the generation-20 rebind ran a blanket bare-label pass and rewrote the second label of the V19-D2 sentence -- a quote of a rebind from `consumer-b.v18` to `consumer-b.v19` -- so the historical record came to name generation 20. The generation-20 provenance audit did not see it: it classified any line with two labels within 40 characters as an ancestry row and never drift-checked ancestry rows, and it keyed before-images by masked text without multiplicity. Its verdict NO HISTORICAL LABEL DRIFT was therefore wrong for that sentence. Found at generation 22 by the corrected audit before any copied code ran (exactly one drift).
- kit selector: not a kit defect: the charter requires historical V17/V18/V19/V20 findings to retain their true provenance
- correction: the sentence is restored byte-for-byte from lib.before-image.v19, where it was authored; the audit now treats a two-label sentence as narrative, compares label MULTISETS per masked sentence, recognises split-literal list lines and current-declaration KEYS, and checks every helper row generation against its id; the generation-22 rebind rewrites joined labels only in an expected list of read modules and asserts the restored sentence equals its before-image

### V22-D2

- original failure: the atom evaluator of every retained Run did not follow atom contract section 4 as now frozen: (a) it ran an inventory-wide expected-subject census INSIDE the atom and emitted uncovered-expected-source-subject for subjects that were not the current one ("Rule-level enumeration uncertainty is root, not this atom"), so every clones witness carried a spurious cause; (b) with an owed but unavailable binding it emitted missing-relation-coverage with the subject universe plus required-relation-missing instead of outgoing step 1 selector-unbound with a null universe; (c) with no containing scope it emitted missing-relation-coverage instead of step 2; (d) on an unpaired sibling it still cited the paired sibling Coverage and named only paired scopes; (e) it never emitted coverage-unknown and had no dependency view, fold or carrier; (f) any cause, including a non-blocking disclosure, blocked the negative answer. Measured: syntax-code 4 of 6 predicate proofs, typescript 3, rust 16 of 19 (five count-at-most atoms indeterminate -> true, findings 3 -> 8), rust-partial 4 of 7, syntax-data 6 of 12.
- kit selector: foundation/atom-evaluation-contract.v1.md section 4 "Completeness result and its independence from truth", "Selection order", "Cause representation", "Shared prelude" P1/P2, "Outgoing cause derivation" 1-4, "Deterministic dependency view, and the coverage-unknown carrier"; section 5; evaluator-composition-contract.v3.md section 9.5 rules 1-3
- correction: the evaluator implements each named rule; composition rule 3 reads the atom's own coverageIds and rule 1 refuses an unregistered cause. All five Runs were rebuilt, closed, replayed and controlled; lib/indep_atom_law.py re-derives every atomic witness WITHOUT importing the evaluator, admits all five Runs, and REFUSES all five generation-20 predecessors (predecessors.v20/runs) at the complete-witness comparison. The generation-20 function is kept as evaluate_native_atom_v20_reading for that control only.

### V22-D3

- original failure: present in every retained library since generation 14: a consumable runtime row whose observability was neither unobservable nor unmapped was counted as a KNOWN HIT, so an `observable-unhit` row (observable and NOT hit) made `exists` true. The TypeScript Run retained a finding for src/util.ts saying it was runtime-observed when its own payload says it was not; the Run still closed and replayed because replay shared the reading.
- kit selector: workflows/schemas/imported-evidence.schema.json RuntimeSubject.observability {observed-hit, observable-unhit, unobservable, unmapped} + atom contract section 6 "an exact consumable mapped polarity row at current grain (observed-hit or observable-unhit)"
- correction: only observed-hit is a match; observable-unhit is the other polarity row; completeness requires a polarity row for every owed wrapper and reads the owner window/population for every polarity row. Measured: typescript findings 4 -> 3; the independent instrument refuses a tamper that re-counts the row as a hit at PREDICATE_VALUE_EQUALS_DERIVED.

### V22-D4

- original failure: requirement status graded rows that its evidence did not measure: the eight standing rules and three phase-0 rows from notes/v16-input-custody.json, a GENERATION-16 custody note for a different kit; R-VALID-VS-INVALID-VS-EXPLANATORY and R-NEGATIVE-FIRST-REFUSAL from a literal True; phase 1, phase 2, the seven trace rows and the phase-7 standing rules from the mere presence of an artifact or key; several phase-8 rows from counts; and R-GRAPH-QUERY / R-MUTATION-REPLAY-SCOPE from the older artifacts only, never checking that they were bound to the CURRENT Runs or that their preimages were admissible. A command inventory was being reported as execution.
- kit selector: requirements.json stopCondition.acceptForbiddenIf "Helper self-consistency (... verdict/count equality, subset schema checks, inserted true) is offered as admission"
- correction: a claimed-positive audit stage re-checks every requirement from its final bytes in a fresh process and records its evidence class; status is derived from that audit, executed only when every check passes AND the evidence class is sufficient for the original kind

### V22-D5

- original failure: the single-relation sufficiency helper used by the min-resolution vector returned ANY entry deficiency at step 2 (only the four rung-unavailable causes are lawful there) and fell back to `coverage-unknown` at step 5, which is an atom cause and not a DeficiencyV2 member; and occupancy handled no `subject` (types), `owner` (literal) or `origin` (reachability) source field. No retained Run reached these branches, which is why they stood.
- kit selector: native-evidence.md section 4.6 steps 2 and 5; native-evidence.schemas.v2.json #/$defs/DeficiencyV2; evaluator-projection-registry relations.*.sourceField
- correction: step 2 carries only the four causes, step 5 refuses an entry with no own deficiency, and the three source fields are read; the min-resolution vector is now evaluated at ATOM level on all three levels (34 cases) and re-derived independently

### V22-D6

- original failure: present since generation 16: the generic, import and native-preparation replay-scope preimages used requestId 'req-7f3a1c' and stepId 'step-2', which the owning schema (invocation-record #/$defs/MutationReplayScopeV1: requestId ^req1_[0-9a-f]{32}, integer stepId) refuses, so the claimed-positive keys were H values over records that could never be admitted. The generation-20 mutation-surface instrument used valid identities but did not correct this artifact, which the report still claimed.
- kit selector: workflows/schemas/evaluator3/invocation-record.schema.json #/$defs/MutationReplayScopeV1; repair.schema.json x-opensip-mutation-operation-map receiptIdempotencyKeyByStepKind
- correction: typed identities; every preimage is admitted before its key is derived, the generation-20 preimage is kept as a measured refused control, and the audit re-admits all five preimages and joins the keys to the mutation surface

### V22-D7

- original failure: three claimed-positive artifacts could not be re-checked by any process other than the one that wrote them: traces kept frame NAMES but not the payloads that drive the state updates, config vectors kept an admission flag and an identity but not the admitted instances, and phase-1 raw negatives kept only the first 48 raw bytes (truncating the depth-33 case below its own fault).
- kit selector: requirements.json R-VALIDATE-OWNING-SCHEMA observable "per-record validation log" + charter "expose every positive graph for root validation"
- correction: payloads, stage count and identity token set are retained with each trace and the audit REPLAYS every trace against the kit table; config vectors retain every submitted instance with its document and selector and the audit re-admits them; raw negatives retain their full bytes and the audit re-runs raw admission

### V22-D8

- original failure: the from-scratch command ran the mutation-surface instrument before the repair-descriptor stage it reads, the query-surface instrument before the availability vector it reads, and phase 7 before the baseline audit it reads, so each consumed the PREVIOUS command's bytes. It went unseen while the Runs were stable; at generation 22 the rebuilt TypeScript Run changed identity and those artifacts would have stayed bound to a Run no longer in the export.
- kit selector: requirements.json R-FROM-SCRATCH-COMMAND "An executable from-scratch command recomputes identities and validates those complete graphs from the export"
- correction: stages reordered; the command carries a static READS table built from a grep of the stage modules and refuses to start if a reader precedes its producer (that table was itself incomplete -- see V22-D11 for the audit-hook measurement that replaced it as the authority); the audit checks every Run reference of the query, comparison, baseline, repair and envelope artifacts against the CURRENT exports

### V22-D9

- original failure: S-MISSING-DEP-IS-CUSTODY requires "custodyGaps[] with exact path/selector, or empty"; no generation produced that array and the rule was graded from a manifest hash check
- kit selector: requirements.json standing S-MISSING-DEP-IS-CUSTODY observable
- correction: every kit document opened by an active module is found by its opening construct and resolved against the verified manifest; the array is produced and audited

### V22-D10

- original failure: the claimed-positive audit re-checked every final artifact against its own request, schemas and clauses and refused claimed positives that were not what they said: (a) two "quotes" were not kit text (phase 0 capitalised "only within its declared scope"; phase 7 dropped "(currentStep)"); (b) count-class-attempt factsAtThisPair read 0 for clones rows of Runs that retain clone facts; (c) the pinned-purge truncation negative recorded admitted=true with no first refusal; (d) the query-surface negative controls and the phase-1 descriptor byte-cap row carried no classification, and the phase-1 float and byte-cap rows no masking record; (e) every configuration negative lacked a masking record; (f) a capability row flagged refused=true was classified explanatory with no refusal recorded, the gate negatives and CVE1 negatives retained no submitted value, and the CVE1 duplicate-key row wrote its first refusal as a literal; (g) the detector-compatibility vector labelled the closure DESCRIPTOR keys as the component manifest body keys; (h) R-TEST-PREP-REPAIR-AUTH was a table of definition names and code strings, not records; (i) the phase-10 blockerStatement still said two SHOULD items were pending source-author work although both were resolved at generation 19 and newShouldIssues was empty.
- kit selector: requirements.json R-NEGATIVE-FIRST-REFUSAL, R-VALID-VS-INVALID-VS-EXPLANATORY and R-TEST-PREP-REPAIR-AUTH observables; docs/v2/contracts/product-v1/README.md; security/security-lifecycle.schemas.v1.json schemas.RepairApplyAuthorizationV1; workflows/schemas/evaluator3/invocation-record.schema.json RepairApplyParams, TestExecutionParams, NativePreparationParams
- correction: each producer is corrected in place with its generation-20 bytes kept; quotes are verbatim; negatives retain the submitted value and record their first refusal and masking; the authorization, test-execution and native-preparation records are constructed and admitted against their owning schemas (helper-only references labelled) with seven refused controls; the audit re-runs admission or the encoder on every retained input rather than comparing recorded strings

### V22-D11

- original failure: phase4.py and phase4_modes.py open runs/*.store.json and were ordered BEFORE the stage that rebuilds the Runs in generations 16, 17, 18, 19 and 20 (lib.before-image.v16..v20 verify_all.py), so R-COUNT-CLASS-ATTEMPT, R-CODE-VS-DATA-MATRIX, R-ENUM-VS-RESOLUTION and R-ADVERTISED-MODE-PATHS measured the PREVIOUS command's Run bytes; phase 0 marked its ids executed through checkpoint.py after reading the previous command's requirement-status.json and checkpoints; and the draft deliverable digested checkpoints that were only written after it. The V22-D8 correction had not caught these because its READS table was hand-written from a grep.
- kit selector: requirements.json R-FROM-SCRATCH-COMMAND "An executable from-scratch command recomputes identities and validates those complete graphs from the export"
- correction: the phase-4 stages follow the Run stage; phase 0 writes no status; checkpoints precede the draft deliverable; every stage runs under an audit-hook launcher that logs its opens under output/ (child-process writes by a post-stage snapshot, child-process reads not measured and disclosed); read_graph_v22.py refuses a read of an artifact no earlier stage of the same command wrote, an undeclared edge, or a read of an unknown artifact; the static guard checks the last occurrence of a reader

### V22-D12

- original failure: both cite diagnostics/json_variance.py and diagnostics/current_declaration_audit.py, which were outside output/ in the generation-20 runtime and were never exported. The reproducibility claim (three commands, nine clock leaves) and the V20-D6 zero count therefore cannot be re-checked from this origin's own copies, and this generation holds only output/.
- kit selector: charter: "State measured results with full admitted retained joins" and "The complete report must distinguish actual reconstructed behavior from a command inventory"
- correction: the generation-22 report does not repeat the cross-command reproducibility claim and states that it was not re-measured; every diagnostic this generation cites is under output/lib

### V22-D13

- original failure: the published-keyword walker resolved a selector through _resolve_local, which drops the effective document root, and then walked the target against the SELECTING document. For a selector that is itself a cross-document alias whose target uses local references (invocation-record #/$defs/TestExecutionParams -> test-execution TestExecutionStepParams -> #/$defs/EnforcementValue) admission crashed with KeyError instead of admitting or refusing. It is the V16-D1 defect at the selector entry rather than inside the recursion; no earlier positive used such a selector, so it stood until generation 22 constructed actual test-execution records.
- kit selector: workflows/schemas/evaluator3/invocation-record.schema.json #/$defs/TestExecutionParams; workflows/schemas/test-execution.schema.json #/$defs/EnforcementValue; Draft 2020-12 base-URI resolution
- correction: the selector is resolved with _resolve_local2 and the walk starts in the target document; the test-execution record and its controls are admitted and refused through it

Open helper failures on a claimed positive: **0**.

## Limitations and scope

- Every compiler, provider, toolchain, OS and runtime observation in these Runs is a SYNTHETIC TRUSTED INPUT authored by this origin. Nothing here qualifies a compiler, provider, host or operating system, and no such qualification is claimed.
- No product code was written, no repository was modified, no commit or push was made, and no product was executed. Every byte produced lives under this origin's own generation-22 output directory.
- The parent subject was never held. Only the disclosed kit and the parent digest declared inside its manifest were verified.
- The repair, comparison, baseline, invocation, authorization and query records are RECORD reconstructions with their identities recomputed and their admission laws executed. No repair was previewed, applied or authorized; no test or preparation ran; no baseline was adopted; no query engine was run by a product. Fields that name records this origin did not construct are labelled helper-only.
- L1-L3 normalised body identities, symbol-to-path attribution and provider occupancy are not recomputable by a consumer; the kit says so and substitutes retained custody, which is what was executed.
- 3 of the 6 advertised language modes (js-synthesized, rust-cargo-prepared, ts-tsconfig) have an admitted representable path at the record level but were NOT exercised end-to-end on a sealed Run (vectors/advertised-mode-paths.json).
- Coverage limitations that are not design gaps are listed with the artifact that measures each in coverageLimitationsDisclosedNotDesignGaps; none is merged into the complete-positive claim.
- No root admission, agreement, expected result, author model, checker or golden was supplied, read or inferred. The root outcome over these exact bytes is UNOBSERVED by this origin.

Artifact digests: the sha256 of every exported artifact AS READ by this reconciliation stage, 134 rows, re-derived by each command from the bytes on disk. Artifacts written AFTER this stage by the command (none are declared) would not be in it.

Reproducibility: NOT re-measured in generation 22. The generation-20 report claimed a three-command leaf comparison through diagnostics outside output/ that were never exported (helper-corrections V22-D12), so that claim is not repeated here.

## Standing

- **noRootAdmissionClaim**: this origin reports ONLY its own independently executed admission, closure, replay, audit and controls. It does not claim that any root, author or successor admitted, agreed with or validated these bytes.
- **noProductQualificationClaim**: nothing here authorizes a product implementation or qualifies any product, component, compiler, provider or host.
- **kitOnly**: every citation names a path and selector inside the frozen kit. The disclosed PRIOR-OWN inputs are named in notes/v22-input-custody.json disclosedPriorInputs and are, verbatim from that artifact: output/ -- an exact copy of this origin's OWN generation-20 work, READ and being continued; previous-turn-response.md -- this origin's OWN generation-20 closing response, READ; requirements.before22.json -- the generation-20 requirement metadata, preserved; only inputKit was updated (measured above)
- **nothingElseClaimedAsAnInput**: no author implementation, control, expected output, golden, root replay/refusal report, root verdict or source-author diagnosis was supplied or read
- **runtimeFilesNotNamedAsInputs**: {"files": ["dispatch.json", "launch.py", "process.json", "prompt.md", "public-events.jsonl"], "standing": "present in the runtime, listed by name only, NOT opened or used"}
- **pathCensus**: CLEAN
- **priorGenerationsUnmodified**: {"method": "os.walk over directory metadata only, comparing each tree's newest modification time with a FIXED anchor write this session made inside generation 22. No file content of any earlier generation was opened.", "anchor": "notes/v22-rebind.json (written once, by the single rebind run)", "anchorWriteUtc": "2026-09-12T18:19:41Z", "anchorStanding": "generation 20 anchored on the path census, which every command rewrites, so its timestamp moved each run and was the one non-substantive difference between consecutive reports. The rebind record is written once, so the anchor is stable.", "trees": [{"generation": "consumer-b.v14", "present": true, "fileCount": 227, "newestMtimeUtc": "2026-09-12T09:15:20Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v15", "present": true, "fileCount": 301, "newestMtimeUtc": "2026-09-12T09:39:10Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v16", "present": true, "fileCount": 461, "newestMtimeUtc": "2026-09-12T11:54:34Z", "newerThanThisSessionsAnchorWrite": false}, {"generation": "consumer-b.v17", "present": true, "fileCount": 575, "newestMtimeUtc": "2026-09-12T11:52:40Z", "newerThanThisSessionsA
- **writeConfinement**: {"foreignWriteOrRootAssignmentsInActiveCode": 0, "foreignSplitLiteralRootAssignmentsInActiveCode": 0, "liveProbeResolvedBeneathThisRuntime": true, "noActiveModuleImportsAnArchivedOrQuarantinedTree": true, "badImports": [], "result": "CONFINED"}
- **historyStanding**: CONFINED-WITH-DISCLOSED-HISTORICAL-DAMAGE
- **generationLabelProvenance**: {'verdict': 'NO HISTORICAL LABEL DRIFT', 'method': "the earliest before-image containing the SAME sentence (with the label masked) carries that sentence's true generation; a later copy that disagrees was rewritten by a mechanical rebind. Helper rows are also checked directly against their own id.", 'standing': 'audited against the retained before-images before any copied code ran and again after every stage; the one drift found (a generation-19 sentence rewritten by the generation-20 rebind) was restored from its before-image (V22-D1)'}
- **writesMadeUnderAPriorGeneration**: generations modified during this session, measured in notes/v22-history-standing.json measuredC: []
  - still open from generation 17: the GENERATION-17 session overwrote TWO files under the generation-16 output before its own control caught the defect: helper-corrections.json and notes/siblings-untouched.json. The prior bytes were not retained by this origin and are NOT claimed to be restorable. The item stays OPEN and is carried forward rather than marked clean (helper-corrections V17-D8).

