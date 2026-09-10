# Independent review — candidate-subject.v3 (post-reset, corrected mixed subject)

Reviewer: fresh actual Claude session. Authored none of the subject bytes.
**Model continuation.** This session began on `claude-fable-5-1` and was interrupted by an
API 429 (`"You've reached your Fable limit"`, `terminal_reason: api_error`, `is_error: true`)
after 64 turns with **no verdict**; that response is retained verbatim in `response.json` and
is not acceptance of anything. The same session was resumed with `--model opus` and completed
on `claude-opus-5` (`process.opus-resume.v1.json`). No prior model agreed to anything; every
verdict below is this session's own. Do not infer agreement from the interrupted run.

Standing: independent substantive design/reference review of a FROZEN mixed-author subject.
Not implementation qualification, and **not** the blind consumer-B litmus (DR-011-R10), which
remains a later distinct act. Signatures, OS/custody observations, evaluator callbacks, fence
and lease observations, trust instants and pivot presences are expressly synthetic TCB inputs
and were treated as such; no product qualification is claimed.

## Verdict: CHANGES_REQUIRED

All five prior new findings (N-1..N-5), all five advisories (A-1..A-5), every original MUST
and SHOULD, and CX-01..CX-07 are independently verified as corrected or lawfully disposed in
the frozen bytes. Two issues block acceptance:

- **MUST-A** — the two owning contracts disagree about a closed consent enum, and the reference
  host composition implements the wrong side, so no `opensip test run` can be admitted in CI.
  This is the MUST-2 class of defect (two vocabularies for one identity) reintroduced by the
  A-2 correction, and the A-2 disposition claiming it is delivered is false.
- **SHOULD-A** — first-party unit populations between 1025 and 4096 admit discovery and then
  die at scope admission with an untyped schema error: no D9 class, exit or registered public
  detail exists for the band the contracts themselves call the effective limit.

Three advisories are recorded. All counterexamples are executable and retained in
`probes/independent-probes.py` / `probes/independent-probes.json` (28 probes: 25 OK, 1
counterexample, 2 gaps).

## Subject and verification

| Item | Value |
|---|---|
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v3.json`, sha256 `e3365d6e64cb5b0260ec7261af5c3e554504c9ab9515456f680aeb01b31b76fd` (required value matched) |
| Predecessor manifest | `5bd9cde140ce48a69c57092c09b5d2cc67cec69aa86fb9725a81b9c8f15af18a` |
| Snapshot | `/tmp/opensip-design-corrections/candidate-subject.v3` |
| Pinned files verified | **1317 of 1317** (0 mismatched, 0 missing, 0 extra; 10 170 342 bytes as declared) before review (`probes/verify-manifest.before.json`) and again after every suite run and all 28 probes (`probes/verify-manifest.after.json`) |
| Environment | `/tmp/opensip-architecture-review-env/bin/python -I -B`, Python 3.12.13, jsonschema 4.25.1 |
| Scratch copy | `scratch/docs/**` (the four unit checkers and the integration checker write beside their sources and ran there; neither the snapshot nor the repository was written) |

## Executed checks

| Check | Result | Where |
|---|---|---|
| Foundation launcher (check-foundation 231, check-identity 124, product-quality 24, product-configuration 18) | **397/397**, source pins valid (1091 files) | `reports/foundation-launcher.json`, `reports/foundation-reports/` |
| Security lifecycle checker | **444/444** cases across fifteen fixtures, **9/9** invariant sweeps, pins valid, 38 output schemas validated | `reports/security-lifecycle-report.rerun.json` |
| Native evidence checker | **100/100** (35 positive, 65 negative), 60 matrix cells, 0 qualified, 86 closed defs, 0 open objects, no uncovered feedback | `reports/native-evidence-report.rerun.json` |
| Workflows launcher | **1206/1206** checks, 13 schemas, 57 pins valid | `reports/workflows-launcher.json`, `reports/workflows-report.rerun.json` |
| Integration checker | **201/201** | `reports/integration-report.rerun.json` |
| Report reproducibility | all eight regenerated reports byte-identical to the retained ones | `reports/report-diff.json` |
| Counts versus `validation-summary.v1.json` | every claimed count equals the count I reproduced | probe P19 |
| Independent probes P1–P28 | 25 OK, 1 counterexample, 2 gaps | `probes/independent-probes.py`, `probes/independent-probes.json` |

Exit codes for all five suites are 0 (`reports/exit-codes.txt`). Counts are evidence that cases
ran; they are not acceptance, and none of them qualifies a platform.

Read in full: the design-corrections README, the D-372 act, the current source map, inherited
residuals, evaluation-residual dispositions, qualification gates, the correction crosswalk,
both post-reset disposition files, JOINT-INTERFACES, integration issues, NEXT-REVIEW, all five
product contracts and their index, both prior independent reviews with their probes, the
actual-Claude author v1/v2 handoffs, both Codex technical reviews and both codex-findings
files, the public detail registry, `discovery-defaults.py`, the integration host model, the
integration fixture builder and the integration checker, and the relevant definitions in all
four units (security discovery/boundary-inventory/grant/projection/repair-apply/repair-recovery/
transition-intent/journal/recovery/lease/storage; native discover_units/assign_membership/
unit_scope_descriptor/sufficiency/D9 map; workflow compare/classify/evaluate/repair apply and
recover/test admission/import build and staleness; foundation `close_run`, identity schemas,
the new `import-source-context.schema.json`, Config2 resolver). Historical completion and
artifact files were read only where pinned and consumed.

## Dispositions of the prior independent review (post-reset-review.v2)

| Finding | Disposition | Independent basis |
|---|---|---|
| N-1 nested boundaries not carried into native discovery | **CORRECTED** | P3: one security discovery produces `AdmittedBoundaryInventoryV1`; over the v2 P3 fixture the security and native unit-root sets are equal, `apps/site`, `apps/site/sub` and `vendor/lib` are excluded with reasons `nested-project`/`nested-repository`, their files are `outside-project-boundary`, both anchors enter `excludedPathPrefixes`, and none of their paths is a source-capture candidate. The same marker inventory through the standalone instrument still yields the four-unit set, so the inventory is doing the work. A substituted marker set and a caller-authored ignore list are refused. Launch inside the nested config selects it as the whole project with no boundaries. |
| N-2 several public spellings for one condition | **CORRECTED** | P4/P27: the registry is 270 records with a separate four-entry internal alias map; registry and `DomainDetailCode` are at exact parity; the cap projects to `PROJECT.WORKSPACE_UNIT_LIMIT` and malformed roots to `PROJECT.EXPLICIT_PATH_INVALID` from all three internal spellings; aliases and the dead `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED`, uppercase storage alias and table-key entry are refused by the public schema; every record is well-formed, unique, owner-attributed and admitted by the envelope. Residue in ADV-ii. |
| N-3 identity closure blind to import source correspondence | **CORRECTED** | P5: a Plan import whose retained `SourceCorrespondence` names another snapshot refuses; a `vcs-revision` import closes only through an admitted `SourceMappingV1` whose every `sourceSha256` joins the snapshot inventory; digest mismatch, dirty worktree and absent mapping refuse. The closure reuses the workflow admission functions, so the source law has one implementation. |
| N-4 repair recovery mutation had no owning record | **CORRECTED** | P6: `RepairRecoveryAuthorizationV1` is closed and owned by security; `repair_recover` refuses any mutating action without an admitted projection bound to the exact journal identity, observed state digest, action, project, plan and base snapshot; the caller dictionary is refused; the journal reference takes the closed grammar. Expiry, moved journal state, foreign project, CI-with-interactive-consent, reused original execution, un-re-admitted custody and a policy that does not admit repair all refuse. Safe rollback proceeds under a revoked recipe while commit refuses first. The security and workflow action tables and the two journal preimages are byte-identical, and the journal identity is noncircular (adding `recoveryAuthorizationRef` does not move it). |
| N-5 core transition intent could not express store operations | **CORRECTED** | P7: one closed eleven-field intent covers all five operations; the workflow `CoreTransitionIntentV1` admits the same record; `InstallationTransitionJournalV1` binds the frozen registry and the exact derived lease set; a caller-narrowed (or widened) lease set refuses `TRANSITION.SCOPE_MISMATCH`; a journal written without the full lock set refuses `LEASE_SET_NOT_HELD`; crash at LEASED aborts, at COMMITTED resumes, a changed registry quarantines and a partially re-acquired set is `PROJECT.BUSY`. `admit_transition_intent` is total over all 80 operation × schema × store × deadline combinations I enumerated (every one returns a closed refusal list). |
| A-1 `analysisOperations` versus prepared resolution | **CORRECTED** | P12: `close_run` enforces `prepare-code` exactly when a trusted-repository-code principal is projected, and `read-import` whenever the Plan selects imports; both negatives refuse. |
| A-2 test consent mode not carried in the projection | **NOT CORRECTED** | P8/P28. The projection now carries a consent mode, but it can only ever be `interactive-consent`. See MUST-A. |
| A-3 explicit Cargo root lost member folding | **CORRECTED** | P10: naming the workspace root explicitly reproduces the automatic unit rows, keeps `memberPackageRoots`, keeps member `target` pruned and keeps a member's `src/target` a program member; naming a member alone selects it as its own `cargo-package`. |
| A-4 documentation residue | **CORRECTED** | P19: no duplicate headings in any contract, zero `/tmp` citations, the empty `native-fix-handoff.v3.md` is no longer pinned, and every count claimed in the contracts and in `validation-summary.v1.json` equals the count I reproduced. |
| A-5 pruned trees versus dependency read-set custody | **CORRECTED** | P13/P3: security S3 carries the read-set paragraph; pruned-tree bytes remain source-capture candidates subject to per-file snapshot custody while boundary paths are removed, which is exactly the stated split. |
| CX-01 repair authorization recipe/admission join | **CORRECTED** | P6 first half; foreign recipe, unadmitted recipe, foreign reference and unhashed plan all refuse through real security admission. |
| CX-02 empty comparison with missing pivots | **CORRECTED** | P14: I rebuilt the baseline and re-executed the three comparisons myself. With zero entries on both sides a missing policy pivot yields `indeterminate` with `COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE`, a missing detector pivot yields `indeterminate` with `BASELINE.PIVOT_DETECTOR_UNAVAILABLE`, and no missing pivot remains `pass`. |
| CX-03 duplicate S12/S13 headings | **CORRECTED** | P19. |
| CX-04 end-of-input assertions | **CORRECTED** | P15: 337 closed patterns scanned across 19 schema documents, zero `$`-anchored patterns remain and 336 carry the explicit `(?![\s\S])` end-of-input assertion; newline, CRLF and space suffixes refuse on `Hash` and `ProjectId` while ordinary newline text round-trips. |
| CX-05 confidence operator typing | **CORRECTED** | P16: only integer `gte`/`lte` on `confidenceMillionths`; string operators, floats and numeric operators on string fields refuse. |
| CX-06 recovery could trust a self-consistent journal | **CORRECTED** | P7: `recover_installation_transition` re-validates the full reference, reconstructs the closed intent, rehashes `intentDigest` and re-derives the lease set over the frozen registry before the state table; a forged digest, a state-mismatched reference and a narrowed scope all refuse. History admission preserves the immutable fields and the exact durable state order. |
| CX-07 declared build context during replay | **CORRECTED** | P5: the expected build labels are an analysis-spec parameter keyed by the raw digest of a closed schema; more than one row refuses; a declared build label with no expected context, and one outside the expected set, both refuse, while a label inside it closes. The importer cannot nominate its own labels. |

Prior-prior findings (MUST-1..3, SHOULD-1..10, ADV-1..4 of post-reset-review.v1) were
re-verified rather than assumed: MUST-1 by P4/P26/P27 (the three goldens v1 named now carry
`RECOVERY.REFUSED`, `MIGRATION.CORRUPT` and `evidence.purged`, all registered, and every
golden's class and exit agree with the fixed table), MUST-2 by P1 (six independent consumers
carry the identical four machine ids; a display alias refuses; the G13 v5 schema stays a
scoped historical harness label), MUST-3 by P2 (4200 installed manifests are one pruned tree
and one unit; 4200 first-party directories refuse typed with exit 2; exactly 4096 admit),
SHOULD-1 by P22, SHOULD-2 by P12, SHOULD-3 by P13, SHOULD-4 by P11 (with the `declares`
dependency present, confidence 100 000 under floor 900 000 is `confidence-floor-unmet` in both
v2 and the retained v1 oracle, and 1 000 000 is satisfied), SHOULD-7/8 by P19/P18, SHOULD-9 by
P17, SHOULD-10 and ADV-4 by P23, and ADV-1/ADV-2 remain the explicit dispositions stated in
workflows §12.

## MUST issues

### MUST-A — the security and workflow contracts disagree about the closed consent enum, and the host composition implements the non-existent value, so authorized test execution cannot be admitted in CI (AR-07, AR-08, AR-13, FW-13; the A-2 disposition)

Evidence (P8, P28). The security `Consent.mode` enum is closed as
`["interactive-explicit", "policy-record"]`. Security S10 states the mapping correctly: the
workflow's `consentSource` (`pre-existing-policy` | `interactive-consent`) "maps to
`policy-record` | `interactive-explicit`". Workflows §12 states it wrongly, naming a
security-side value that no security record can carry:

> requires consentSource to equal the actual admitted security grant projection
> (`interactive-explicit` -> `interactive-consent`, pre-existing-policy -> pre-existing-policy)

`integration-host-model.py:103` implements the workflow spelling:

```
'consentSource': 'pre-existing-policy' if grant['authorization']['mode'] == 'pre-existing-policy' else 'interactive-consent',
```

The left-hand comparison can never hold, so the projection is **always** `interactive-consent`.
I built a lawful CI grant (`executionClass: test-runner`, `authorization.mode: policy-record`
with a policy record id, `ci: true`), which security admits (`result: ADMIT`). The host
projects `consentSource: interactive-consent`. `admit_test_execution` with `ci: true` then
refuses both lanes: `pre-existing-policy` params refuse because the projection disagrees, and
`interactive-consent` params refuse `TEST.INTERACTIVE_CONSENT_IN_CI`. Substituting only the
corrected mapping into the same projection admits the step. No `opensip test run` invocation
can be admitted in CI through the host composition.

Why it blocks: this is MUST-2's defect class — two owning contracts carrying different
vocabularies for one closed identity — reintroduced by the A-2 correction, and it disables a
selected product capability. CI is the only context in which `policy-record` consent is
lawful, so the failure is exactly on the lane the contract says must work. Both matching unit
tests pass and hide it: the workflow fixture `testExecution.ctx.grant` is a hand-authored
projection that already carries `pre-existing-policy`, and `check-integration.py` exercises
only the non-CI interactive lane plus a relabelling negative. `post-reset-dispositions.v3`
records A-2 as "CORRECTED-PENDING-REVIEW … exact consentSource projects from actual security
consent and binds to params"; that claim is not delivered.

Owning selectors: `workflows-and-surfaces.md` §12 "Test-step admission validates the complete
closed TestExecutionStepParams …" sentence; `security-and-lifecycle.md` S10 "the workflow
contract's `consentSource` … maps to `policy-record` | `interactive-explicit`";
`integration-host-model.py` `test_grant_projection` (the `consentSource` line);
`security-lifecycle.schemas.v1.json#/$defs/Consent/properties/mode`;
`workflows/schemas/test-execution.schema.json#/$defs/TestExecutionStepParams/properties/consentSource`;
`workflows_model.v1.py` `admit_test_execution` (the `g.get('consentSource') == params['consentSource']` conjunct);
`check-integration.py` `security-to-test.*` and `test-consent-cannot-be-relabeled.*`.

Return: correct the workflows §12 sentence to the security S10 mapping, fix the projection to
compare against `policy-record`, and add the CI lane to the integration checker on all four
platforms (a `policy-record` grant with `ci: true` admits with `consentSource:
pre-existing-policy`; an `interactive-explicit` grant with `ci: true` refuses at security
admission). While there, decide the third spelling named in ADV-i.

## SHOULD issues

### SHOULD-A — the 1025..4096 first-party unit band admits discovery and then fails scope admission with no class, exit or registered detail (AR-03, AR-13, FW-01, FW-06)

Evidence (P9). Discovery's first-party cap is 4096 unit directories and the foundation scope
descriptor admits at most 1024 `workspaceRoots`. With 1025 first-party marker directories
`discover_units` admits (`refused: null`, 1025 units) and `unit_scope_descriptor` then raises a
bare jsonschema `ValidationError`. Nothing types that outcome: `d9_map` has no row for a
scope-root bound (it refuses an unknown detail, correctly saying "silent exit 0 is forbidden"),
and the registry contains no code naming the condition — `PROJECT.WORKSPACE_UNIT_LIMIT` is
defined as the 4096 cap with detail `WORKSPACE_UNIT_LIMIT:<n>><cap>`, and native §10's only
unit-population row is "more than 4096 first-party workspace unit directories".

Why it blocks: the contracts state the consequence but not the outcome. Native §1.4 says "a
project with more than 1024 unit roots refuses at scope admission without truncation and asks
for a narrower explicit scope", and §14 repeats "the effective scope limit is 1024". A blind
implementer must invent the class, exit and public detail for an ordinary large monorepo, and
the two instruments' bounds (4096 and 1024) meet at a band that no reference case exercises.
This is the same shape as MUST-3's untested refusal branch, one bound lower.

Owning selectors: `native-evidence.md` §1.4 "Unit scopes feed the shared scope descriptor"
paragraph and §14 "The discovery instrument can enumerate 4096 first-party units …";
`native_evidence_model.v2.py` `unit_scope_descriptor` and `D9_MAP`;
`foundation/identity-schemas.v2.json#/$defs/scope-descriptor` (`workspaceRoots` `maxItems`
1024); `discovery-defaults.py` `MAX_WORKSPACE_UNITS`; `public-detail-registry.v1.json`;
`security-and-lifecycle.md` S3 cap paragraph and S12 row.

Return: register one public detail for the scope-root bound, map it to an existing D9 code
(`REQUEST.UNSATISFIABLE` matches the cap row), state it in native §10 and security S12, and add
a 1025-root case to the native unit and to the integration checker. Alternatively lower the
discovery cap to 1024 and say so once in the shared rule.

## Advisory

- **ADV-i (AR-07, AR-08)** Three spellings of one concept survive: security
  `interactive-explicit | policy-record`, test-execution `pre-existing-policy |
  interactive-consent`, and `RepairApplyParams.consentSource` `policy | interactive` (P25).
  Only the test mapping is stated, and the repair projection returned by
  `repair_authorization_projection` carries no consent mode at all, so `repair_apply` compares
  its own caller-supplied `consent` argument against its own caller-supplied `ci` argument
  rather than against the admitted record. Security refuses interactive consent under a CI
  context, so no authority hole follows, but the join is asserted by neither side. State one
  mapping table for all three records and carry the admitted mode in the repair projection.
- **ADV-ii (AR-16, FW-13)** `native.explicit-root-crosses-boundary` and
  `native.boundary-inventory-mismatch` are registered *public* codes that the operational host
  composition cannot emit: security refuses an explicit root crossing a nested boundary first,
  as `PROJECT.EXPLICIT_PATH_INVALID` / `JOIN_CROSSES_NESTED_PROJECT`, and
  `admit_repository_discovery` never reaches native (P24). They are reachable only from the
  standalone instrument, which native §1.4 U-8 says is "not an operational host composition".
  Fail-closed redundancy is good design; publishing a second public code for a condition the
  product always reports under the first is the residue N-2 asked to retire. Either mark them
  internal aliases of the security spelling or state which surface emits them.
- **ADV-iii (AR-14)** `core_transition_affected_namespaces` still reads
  `intent.get('reselectsStore', False)`, a key the closed `InstallationTransitionIntentV1`
  cannot carry and that `core_transition_scope` refuses at schema admission (P28). The
  parameter is dead; leaving it invites an implementer to treat store re-selection as
  caller-supplied, which §12 explicitly forbids.
- **ADV-iv (AR-09, DR-011-R11)** `close_run` raises a bare `KeyError` when a retained blob is
  absent, rather than a typed `AdmissionError` (P28). Identity §5 distinguishes retention loss
  (`HOST.IO_FAILURE`, evidence detail, exit 4) from admission rejection (exit 2), and §4 says
  "missing witness bytes is retention loss, not a false predicate"; the reference closure
  checker cannot express that difference. Reference-only, but it is the function an implementer
  will copy.
- **ADV-v (AR-08, AR-14)** Installation revisions written by crash recovery have no lawful
  holder (P20). Workflows §12 says a `RESUME-COMMIT` recovery "first retains COMMITTED if
  needed, then DONE", while `installation_journal_history` refuses any history that does not
  begin at `LEASED` — so those revisions can be attached to no `Attempt.installationJournalRefs`
  (the original attempt's history ended before the crash, and recovery is not an attempt). The
  durable journal remains the record, so nothing is unsound; state where the recovery-written
  revisions are referenced, or say explicitly that they are referenced by nothing.
- **ADV-vi (AR-15, D-372 application)** Every crosswalk `review` field still names
  `post-reset-review.v1/review.json` and the v1 manifest with verdict `CHANGES_REQUIRED`, and
  all sixteen rows read `AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW` (P23). That is correct
  pre-application standing, not a defect; the application must repoint these fields at this
  review and, later, at the consumer-B record, and must not present a superseded review as
  acceptance of the current bytes.

## AR obligation dispositions

| AR | Disposition | Basis |
|---|---|---|
| AR-01 exact admission | ACCEPT | P21; foundation 397 reproduced |
| AR-02 authenticated qualification | ACCEPT | P1, P15; product-quality 24 and G13 v5 reproduced |
| AR-03 discovery/custody | CHANGES_REQUIRED | SHOULD-A; N-1/A-5 corrected (P2, P3, P13) |
| AR-04 trust clock/recovery | ACCEPT | sweeps reproduced; P18 |
| AR-05 expired root/live revocation | ACCEPT | sweeps reproduced |
| AR-06 platform population | ACCEPT | P1 |
| AR-07 sealed inputs/execution boundary | CHANGES_REQUIRED | MUST-A; ADV-i; otherwise P12 |
| AR-08 invocation/repair lifecycle | CHANGES_REQUIRED | MUST-A; N-4/N-5 corrected (P6, P7); ADV-i, ADV-v |
| AR-09 identity/retention closure | ACCEPT with advisory | P5, P12, P22; ADV-iv; identity 124 reproduced |
| AR-10 runnable prior detector/baseline | ACCEPT | P14 |
| AR-11 typed comparison/imports | ACCEPT | P5, P14, P16 |
| AR-12 resolution completeness | ACCEPT | P11; RC rows and closed-world cases reproduced |
| AR-13 cells/discovery/parity | CHANGES_REQUIRED | SHOULD-A, MUST-A (test surface); N-1/A-3 corrected (P3, P10) |
| AR-14 stage transition/concurrency | ACCEPT with advisories | P7; ADV-iii, ADV-v |
| AR-15 current narrative | ACCEPT with advisory | P19, P23; ADV-vi |
| AR-16 provenance-specific remedies | ACCEPT with advisory | P4, P26, P27; ADV-ii |

## Fallow constraint dispositions

FW-01 CHANGES_REQUIRED (SHOULD-A). FW-02 ACCEPT. FW-03 ACCEPT. FW-04 ACCEPT. FW-05 ACCEPT.
FW-06 ACCEPT. FW-07 ACCEPT. FW-08 ACCEPT. FW-09 ACCEPT. FW-10 ACCEPT (N-4 corrected).
FW-11 ACCEPT. FW-12 ACCEPT. FW-13 CHANGES_REQUIRED (MUST-A; ADV-ii). FW-14 ACCEPT as a stated
harness obligation. FW-15 ACCEPT.

## Inherited residuals, D-372 and readiness obligations

The sixteen DR-011 residual dispositions and the parent DR-001..011 rows remain lawful
prospective dispositions and none is contradicted by the frozen bytes. MUST-A touches R09
(one-shot operational authority: the consent mode is part of the operational grant an
implementer must bind) and R15 (trusted request context). SHOULD-A touches R01 (declared
view/subject-set joins) and R16 (the bounded first-party composition must name its own
boundary outcome). ADV-v touches R04/R11 (stage delivery and G19 recovery custody). R10
correctly remains open for the blind consumer B, which this review does not perform and does
not prejudge.

The thirty evaluation-proof residual dispositions are history-preserving and make no
containment claim. The 32 qualification-gate rows honestly record `qualified=false`,
`demonstrated=false`, `implementationHarnessAuthored=false` over the four machine ids, and
`historical-preservation-report.v3.json` records 31 of 31 historical files unchanged. The
D-372 DR-003 timing disposition is a scoped condition-1 disposition with explicit release-gate
retention and no SATISFIED or DEMONSTRATED claim; it is acceptable as proposed and grants no
condition-5 authorization, which remains NOT MET. The current source map's rows are consistent
with the contracts, and its G13 alias sentence is confirmed by P1. `validation-summary.v1.json`
still records `claudeFinalReview: PENDING-FROZEN-V3` and `readinessChanged: false`, and the
central and navigation documents remain pre-application, as intended.

## Limitations

Reference code ran only over synthetic fixtures. No OS custody, cryptography, SQLite
durability, fsync, process death, compiler, Cargo, provider, renderer or repository code was
executed and none is claimed; every signature, OS observation, evaluator callback, fence/lease
observation and pivot presence is a declared TCB assumption. The workflow and native models
accept host projections as trusted inputs by design, so `repair_recover` and
`admit_test_execution` cannot themselves prove that a well-formed projection came from a real
admission; the integration checker composes the real admissions, and I re-composed them myself
in P6 and P8, but a forged projection at that seam is outside what any of these models can
detect and is correctly declared. Unit expectations are same-author; this review is the
independent oracle for the mixed bytes, not the blind implementer litmus. Severity is my
judgement against the contracts' own statements; each finding names a claim the subject makes
that its bytes do not deliver.

## What the authors should do

1. Fix MUST-A and SHOULD-A in new bytes, consider ADV-i..ADV-vi, re-pin, regenerate all five
   reports and freeze a new exact subject with a new manifest. Do not overwrite
   `candidate-subject.v3.json`.
2. Do not reuse this review for changed bytes; request a fresh independent re-review of the
   newly frozen subject. This review is CHANGES_REQUIRED and accepts nothing.
3. Only after an ACCEPT run the separate blind consumer-B review, then the per-row application
   review, then apply D-372, the current source map and the central register.

Paths: this file, `review.json`, `probes/independent-probes.py`, `probes/independent-probes.json`,
`probes/verify-manifest.before.json`, `probes/verify-manifest.after.json`, `reports/` (launchers,
reruns, `report-diff.json`, `exit-codes.txt`, per-suite stdout), `scratch/` (run-in-place copy),
`run-suites.sh`, and the retained interrupted-run evidence `response.json` / `process.json`.
