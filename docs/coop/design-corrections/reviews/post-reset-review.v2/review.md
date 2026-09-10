# Independent review — candidate-subject.v2 (post-reset, corrected mixed subject)

Reviewer: fresh actual Claude session (claude-fable-5-1). Authored none of the subject bytes.
Standing: independent substantive design/reference review of a FROZEN mixed-author subject. Not implementation qualification, not the blind consumer-B litmus (DR-011-R10), which remains a later distinct act. Signatures, OS observations, evaluator callbacks and pivot presences in the reference are synthetic TCB inputs and were treated as such.

## Verdict: CHANGES_REQUIRED

No MUST issue remains. All three prior MUST issues, all ten prior SHOULD issues, the four advisories and CX-01..05 are independently verified as corrected or lawfully disposed in the frozen bytes. Five new SHOULD issues block acceptance: they are cross-unit joins that the corrections introduced or exposed and that the matching unit tests do not cover (nested-tree exclusion not carried into native discovery, one condition with several registered public spellings, identity closure blind to import source correspondence, an un-owned repair-recovery authorization, and a core-transition intent that cannot carry what the security contract says it records). Five advisories are recorded. All counterexamples are executable and retained in `probes/independent-probes.py` and `probes/independent-probes.json`.

## Subject and verification

| Item | Value |
|---|---|
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v2.json`, sha256 `5bd9cde140ce48a69c57092c09b5d2cc67cec69aa86fb9725a81b9c8f15af18a` (required value matched) |
| Predecessor manifest | `e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac` |
| Snapshot | `/tmp/opensip-design-corrections/candidate-subject.v2` |
| Pinned files verified | 1250 of 1250 (0 bad, 0 missing, 0 extra; total bytes 8363577 as declared) before review (`hash-verify-before.json`) and again after every suite run and probe (`hash-verify-after.json`) |
| Environment | `/tmp/opensip-architecture-review-env/bin/python -I -B`, Python 3.12.13, jsonschema 4.25.1 |
| Scratch copy | `scratch/docs/**` (checkers that write beside their sources ran there; the snapshot and the repository were not written) |

## Executed checks

| Check | Result | Where |
|---|---|---|
| Foundation launcher (check-foundation 231, check-identity 113, product-quality 24, product-configuration 18) | 386/386, source pins valid (1060 files) | `reports/foundation-launcher.json`, `reports/foundation-reports/` |
| Security lifecycle checker | 361/361 cases, 8/8 sweeps, pins valid, 30 output schemas validated | `reports/security-lifecycle-report.rerun.json` |
| Native evidence checker | 93/93 (32 positive, 61 negative), 60 matrix cells, 0 open objects, F1–F12/R1–R7/PR-MUST-3/PR-SHOULD-4 covered | `reports/native-evidence-report.rerun.json` |
| Workflows launcher | 1204/1204 checks, 13 schemas, 34 pins valid | `reports/workflows-launcher.json` |
| Integration checker | 94/94 | `reports/integration-report.rerun.json` |
| Report reproducibility | all nine regenerated reports byte-identical to the retained ones | `reports/report-diff.json` |
| Independent probes P1–P25 | 5 counterexamples, 5 gaps, 15 OK | `probes/independent-probes.py`, `probes/independent-probes.json` |

Counts match the expected intermediate reference counts and are not treated as acceptance.

Read in full: design-corrections README, D-372 act, current source map, inherited residuals, evaluation-residual dispositions, qualification gates, correction crosswalk, post-reset dispositions, JOINT-INTERFACES, integration issues, all five product contracts and their index, the prior independent review (v1), the actual-Claude author handoff, the Codex technical review and codex-findings, the public detail registry, `discovery-defaults.py`, the integration host model and checker, the integration fixture builder, and the relevant model/schema definitions in all four units (security discovery/grant/projection/repair-authorization/lease/core-transition/recovery/storage; native discover/membership/scope/sufficiency/D9; workflow compare/classify/evaluate/repair/recover/test admission; identity `close_run`; Config2 resolver). Historical completion/artifact files were read only where pinned and consumed.

## Dispositions of prior findings (post-reset-review.v1)

| Finding | Disposition | Independent basis |
|---|---|---|
| MUST-1 public envelope cannot carry unit details | CORRECTED | P4/P25: one closed registry (210 records) equals the `DomainDetailCode` enum; unregistered and uppercase storage alias refused; native/security/identity details project into `StepTermination` with lawful class and exit; the three goldens named in v1 now carry `domainDetail`. Residual: N-2 (several registered spellings for one condition). |
| MUST-2 two platform vocabularies | CORRECTED | P1: profile-set keys, `SUPPORTED_POPULATION`, truth table, native matrix, workflow test schema, workflow model and gates are the same four machine IDs; alias in a grant refuses `GRANT.PLATFORM_DISPLAY_ALIAS_NOT_MACHINE_ID`; G13 v5 aliases remain historical corpus labels per the source map. |
| MUST-3 zero-config discovery indeterminate; cap crashes | CORRECTED | P2: 4200 installed manifests → one unit and one pruned tree in both instruments; 4200 first-party → typed `PROJECT.WORKSPACE_UNIT_LIMIT`/`native.too-many-units` (no KeyError); 4096 exactly admits; `packages/target/index.ts` retained; `.`/trailing slash/grammar/pruned-tree explicit roots agree across security and native. Residual: N-1 (nested repositories/projects are a further exclusion the shared rule does not carry). |
| SHOULD-1 hidden import evidence | CORRECTED | P5(c): a finding citing an import in Plan but not in `evaluationInputRefs` is `HIDDEN_FINDING_EVIDENCE`; citing the evaluated Plan import closes. New N-3 found beside it. |
| SHOULD-2 test-runner grant projection | CORRECTED | P6: grant admission is operational, a ctx projection is never consulted, test-runner admits with the canonical empty-owner digest and refuses an unsealed runner; Plan-time join refuses missing/extra principals, imported-inert principals and a consumed test-runner grant. |
| SHOULD-3 UNKNOWN backup prose | CORRECTED | P7: S3.1 now says UNKNOWN admits; security and identity instruments agree (UNKNOWN admit/disclosed, detected refuses in CI, flag admits). |
| SHOULD-4 sufficiency order | CORRECTED | P8: floor 900000 over 100000 → `confidence-floor-unmet` in v2 and v1 oracle; 1000000 satisfied (with `declares` dependency present); declared-only policy also not bypassed. |
| SHOULD-5 repair apply authorization join | CORRECTED (apply) | P9: `RepairAuthorizationRef` closed grammar; free text refused; integration composes real `admit_repair_authorization`. New N-4 on recovery. |
| SHOULD-6 core transition lease scope | CORRECTED (mechanism) | P10: all-or-nothing ordered EXCLUSIVE set under a held fence, busy releases in reverse, unordered/unregistered sets refused, schema-change and store re-selection affect all namespaces, same-schema update none. New N-5 on representability. |
| SHOULD-7 documentation defects | CORRECTED | P11: no duplicate heading numbers in any contract; counts 361/eight/93/82 match; V1 comment gone; workflow cross-reference now native §14/security S15. Advisory residue in A-4. |
| SHOULD-8 root-quorum label | CORRECTED | P12: inventory class `recovery-authority-quorum`; root keys as signers refuse `SIGNATURE_THRESHOLD`; higher counters and reboot refuse. |
| SHOULD-9 non-gating indeterminacy | CORRECTED | P13: absent required evidence and incomplete coverage are disclosed identically; only a gating rule turns the verdict indeterminate. |
| SHOULD-10 review provenance | CORRECTED | P24: verbatim v1 review with probes, author handoff and Codex delta review retained; crosswalk `review` fields populated with the predecessor review and honest standing; no duplicate evidence. |
| ADV-1 evidence pivot | DISPOSED (explicit) | Workflows §12 states the conservative attribution and the composed-invocation remedy; P19 reproduces `evidence-content-changed` → INDETERMINATE on a gating rule. Accepted as intended product behaviour. |
| ADV-2 unbound E1–E3 | DISPOSED (explicit) | Workflows §12: host must bind; P19 reproduces typed `pivot-reevaluation-unavailable`. |
| ADV-3 nested config | CORRECTED (decided) | P20: nearest config wins inside; enclosing project records `nestedProjects`, excludes units, refuses joins; S3 states the rejected alternative. |
| ADV-4 crosswalk | CORRECTED | P24. |

## Dispositions of Codex findings

| Finding | Disposition | Basis |
|---|---|---|
| CX-01 repair authorization recipe/admission join | CORRECTED | P9 first half; integration checks foreign recipe, unadmitted recipe, foreign ref, unhashed plan. |
| CX-02 empty comparison with missing pivots | CORRECTED | P14: missing policy pivot → indeterminate with `COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE`; bound or unneeded pivots → pass; detector pivot missing → indeterminate; `report-only` also indeterminate because current gating rules exist. |
| CX-03 duplicate S12/S13 | CORRECTED | P11. |
| CX-04 end-of-input assertions | CORRECTED | P15: zero `$`-anchored patterns remain in any of the 13 schema documents (312 patterns); newline/CRLF/space suffixes refused in workflow, native, foundation and security records; ordinary newline text preserved. |
| CX-05 confidence operator typing | CORRECTED | P16: only integer gte/lte on `confidenceMillionths`; string fields refuse numeric operators; float refused. Note A-4: CX-05 has no record in `codex-findings.json`. |

## New SHOULD issues

### N-1 — Nested repository and nested project exclusion is a security-only fact; the native unit instrument and the shared scope descriptor do not see it (AR-03, AR-13, FW-01, FW-06)

Evidence (P3): on one inventory with a nested repository (`vendor/lib`, has `.git` and `package.json`) and a nested project (`apps/site/opensip.json` with `package.json` and `apps/site/sub/Cargo.toml`), security discovery yields one unit and records `INSIDE_NESTED_REPOSITORY` / `INSIDE_NESTED_PROJECT` exclusions; native `discover_units` over the same marker inventory yields four units (`""`, `apps/site`, `apps/site/sub`, `vendor/lib`) and `unit_scope_descriptor` lists no anchor for either exclusion. The shared rule prunes only `node_modules`, VCS directories and Cargo `target`; a nested repository's own files carry no such segment. The integration check `security-native-shared-unit-roots` uses a fixture without nested trees and therefore passes.

Why it blocks: security S3 decides the authority boundary and says nested repositories are "never entered" and nested projects are "never entered by automatic discovery"; native §1.4/H-1 say the native instrument works "inside that boundary" and consumes the one shared rule. No contract states who removes nested-tree markers and files from the inventory native receives (identity §3 defines the snapshot inventory without mentioning nested trees), and the Plan-visible scope descriptor cannot show that a nested repository was excluded. Two instruments again disagree on the unit set of an ordinary monorepo with a vendored repository, which is the MUST-3 class of defect.

Owning selectors: `security-and-lifecycle.md` S3 "Authority roots versus workspace units" and "Nested config is a deliberate project boundary"; `security_lifecycle_model_v1.py` `discovery.finish` (`nestedRepositories`, `nestedProjects`, `_in_nested_repo`, `_in_nested_project`); `discovery-defaults.py` (`_segment_prune`, `classify_path`, `enumerate_units`); `native-evidence.md` §1.4 U-4a and §13 H-1; `native_evidence_model.v2.py` `discover_units`, `assign_membership`, `unit_scope_descriptor`; `identity-and-evidence.md` §3 snapshot row and scope-descriptor paragraph; `check-integration.py` `security-native-shared-unit-roots`.

Return: state once (in the shared rule) that nested repository roots and nested project roots are pruned anchors (`nested-repository`, `nested-project` reasons) supplied by the security boundary decision, consumed by `enumerate_units`/`classify_path`, entered into `excludedPathPrefixes`, and excluded from the snapshot source inventory; add a nested-repository plus nested-project fixture to both units and to the integration checker.

### N-2 — One condition has several registered public detail spellings, so the parity envelope is not determinate for the unit cap and for explicit-root grammar (AR-16, AR-08, FW-13)

Evidence (P4): the registry admits `PROJECT.WORKSPACE_UNIT_LIMIT`, `WORKSPACE_UNIT_LIMIT` and `native.too-many-units`; `public_termination` produces three lawful `request-rejected`/`REQUEST.UNSATISFIABLE`/exit-2 envelopes with three different `domainDetail.code` values for the same 4097-unit repository. Likewise a malformed explicit root is `PROJECT.EXPLICIT_PATH_INVALID` (security, subject `JOIN_PATH_GRAMMAR`) or `native.explicit-root-grammar` (native). The registry also carries `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED`, which no model emits since SHOULD-2, and the model-table key `provider-unavailable/capability-missing` as a public code.

Why it blocks: workflows §12 makes JSON the parity reference and requires "one spelling" (it retired the uppercase storage alias for exactly this reason); AR-16 requires exact goldens. The security S3/S12 and native §1.4 U-7/§10 rows each own a different code for the same shared-rule refusal, and neither contract says which instrument's spelling the default invocation emits.

Owning selectors: `public-detail-registry.v1.json` records `PROJECT.WORKSPACE_UNIT_LIMIT`, `WORKSPACE_UNIT_LIMIT`, `native.too-many-units`, `native.explicit-root-grammar`, `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED`, `provider-unavailable/capability-missing`; `workflows/schemas/common.schema.json#/$defs/DomainDetailCode`; `security-and-lifecycle.md` S3 cap paragraph and S12 table; `native-evidence.md` §1.4 U-7 and §10 table rows for `native.too-many-units` / `native.explicit-root-grammar`; `workflows-and-surfaces.md` §12 registry paragraph; `integration-host-model.py` `public_termination`.

Return: one registered code per shared-rule condition (the sub-detail travels in `subject`), retire the dead and table-key entries, and add a negative integration check that the same condition cannot project to two codes.

### N-3 — The identity closure does not parse import source correspondence, so a Run whose evaluated import belongs to another snapshot closes and replays as valid (AR-09, AR-11, FW-06)

Evidence (P5): a graph whose Plan/evidence/proof all list one `import2` whose retained `sourceCorrespondence` blob names `snapshot2:ffff…` (not the Run's snapshot) returns `run2:` from `close_run`; the same graph with the Run's own snapshot also closes. The staleness law lives only in workflow `classify_staleness` at Plan admission.

Why it blocks: identity §3 says the closure checker "rejects missing, extra authoritative roots, wrong-kind, cross-Plan/cross-source or unresolved references" and admission §1.1 says already-imported evidence "must belong to the admitted project/source/build context"; identity §4 promises an independent installation can replay "without trusting the original result flags". An import bound to the wrong source is exactly a cross-source reference that replay cannot detect, so the promise depends on trusting the original host's Plan admission.

Owning selectors: `identity-and-evidence.md` §3 "The closure checker parses and exactly validates scope, semantic configuration, analysis specification, semantic grant, VCS observation and predicate witnesses" and the "rejects … cross-source" sentence; `foundation/identity-model.py` `close_run` (`visit` performs no snapshot join for domain `import`; `payload` is never called on `sourceCorrespondenceDigest`); `admission-and-qualification.md` §1.1 line "Already-imported evidence IDs must belong…"; `workflows-and-surfaces.md` §4 staleness table; `identity-schemas.v2.json#/$defs/import`.

Return: have the closure checker parse each Plan import's retained `SourceCorrespondence` (and `SourceMappingV1` where `vcs-revision`) and require it to map to the Run's snapshot under the workflow §4 law; add positive/negative cases in check-identity and the integration checker.

### N-4 — Repair recovery mutation authorization has no owning record, grammar or security admission (AR-08, FW-10)

Evidence (P9): workflows §6 requires "an authorization bound to this repairPlanId and journal requestId" for every recovery mutation; the journal's `recoveryAuthorizationRef` is free text (`minLength 1`, no pattern); security defines only `RepairApplyAuthorizationV1` (S10.1) and no recovery function or schema exists; `repair_recover` accepts any caller dict carrying the two fields and mints `auth:<16 hex>`, a grammar no contract names; the inventory labels `repair recover` `policy-record-or-consent` and S7 gives it EXCLUSIVE, but nothing binds consent, CI, expiry or current trust to the recovery write.

Why it blocks: the correction for SHOULD-5/CX-01 closed apply; recovery writes to the same tree under the same lease and remains where apply was before the fix. A blind implementer must invent the record.

Owning selectors: `workflows-and-surfaces.md` §6 "Recover" paragraph; `workflows/schemas/repair.schema.json#/$defs/RepairApplyJournalV1/properties/recoveryAuthorizationRef` and `#/$defs/RecoveryAction` description; `workflows_model.v1.py` `repair_recover` (`recovery_authorization`, `'auth:' + …`); `security-and-lifecycle.md` S10.1 (apply only) and S7 command map row `repair recover`; `workflows/command-inventory.v1.json` `repair-recover`; registry `REPAIR.RECOVERY_NOT_AUTHORIZED`.

Return: either extend `RepairApplyAuthorizationV1` with a closed `kind: repair-recover` bound to `repairPlanId`, journal `requestId`, base snapshot, consent/ci/expiry and current trust, admitted by security and composed in the integration checker, or state that the apply authorization covers recovery for its journal and pin the journal ref to that grammar.

### N-5 — `CoreTransitionIntentV1` cannot express store migrate/rollback and no record carries the journaled lease set the security contract says the intent records (AR-14, AR-08, FW-07)

Evidence (P10): the intent `operation` enum is `core-update|core-repair|core-rollback`; a `store-migrate` intent is schema-invalid, while `MutationOperation` and the inventory class `core-transition-leases` name `store-migrate`/`store-rollback` and S7/S15/§12 say they use the same protocol; the intent has no lease-set or namespace field, although S7 item 4 says "The `CoreTransitionIntentV1` / migrating-root journal record (S9) names the exact lease set and is written only after every lease is held" and crash recovery "re-acquires exactly the journaled set"; the only security record with a namespace list is the decision output `CoreTransitionScopeV1`, which is not a journal record; `core_transition_scope` in the host model derives `reselectsStore` only from `core-rollback`, so the store operations are unreachable through the admitted intent.

Why it blocks: this is the mechanism SHOULD-6 introduced; the crash-recovery guarantee depends on a durable record that no schema defines, and two of the five commands the lock set covers cannot be admitted as intents.

Owning selectors: `workflows/schemas/invocation-record.schema.json#/$defs/CoreTransitionIntentV1` (`operation` enum, property set) and `#/$defs/MutationParams` `allOf`; `security-and-lifecycle.md` S7 "Core-transition lock set" item 4 and S15 third paragraph; `security-lifecycle.schemas.v1.json#/schemas/CoreTransitionScopeV1`, `MigrationRecoveryV1`; `workflows-and-surfaces.md` §12 core-transition paragraph; `integration-host-model.py` `core_transition_scope`; `workflows/command-inventory.v1.json` `store-migrate`, `store-rollback`.

Return: extend the intent enum (or define a sibling `StoreTransitionIntentV1`) for store migrate/rollback with `reselectsStore` host-observed; add a closed journaled `leaseNamespaces` record (S9 migrating root or a `CoreTransitionJournalV1`) written after acquisition and consumed by recovery; add cases for crash-before-journal and crash-after-journal.

## Advisory

- **A-1 (AR-07, AR-09)** `analysisOperations` is part of `semanticGrantDigest` and native §2.1/§5.1 fix the rule (`prepare-code` iff `host-prepared`, `read-import` for `imported-inert`), but neither the foundation `semantic-grant` schema, `close_run`, nor `admit_plan_execution_projection` (principals only) checks operations against `preparedResolution` (P6). State where the rule is enforced and add a case.
- **A-2 (AR-08)** The integration checker builds `TestExecutionStepParams` with `consentSource: interactive`, which the schema refuses (`pre-existing-policy|interactive-consent`), and never validates those params; S10 states the grant `authorization.mode` ↔ step `consentSource` mapping, but the projection carries no consent mode, so an `interactive-explicit` grant with a `pre-existing-policy` step admits outside CI (P21). Validate params in the integration join and carry the mode in the projection.
- **A-3 (AR-13)** Naming a Cargo workspace root as an explicit root drops member folding (`memberPackageRoots` empty) and stops pruning member `target` directories (P22); U-2 does not say explicit roots change folding.
- **A-4 (AR-15)** Documentation residue: security S3 and the fixture `config2-workspace-root-with-trailing-slash-…` say a Config2 `packages/web/` value is normalized, while the foundation resolver refuses it and workflows §12 says malformed Config2 is rejected before either instrument (P2); S14 says migration/rollback "require S7's EXCLUSIVE lease" (singular) where S7 defines the lock set; the security and native contracts cite the `/tmp/…` copies of the retained v1 review and author handoff instead of `reviews/post-reset-review.v1/` and `reviews/post-reset-author.v1/`; native pins the empty `native-fix-handoff.v3.md`; CX-05 appears in the dispositions and technical review but not in `codex-findings.json`; the registry retains a dead `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED` entry.
- **A-5 (AR-03, AR-07)** S3 says a pruned tree receives "no custody walk", while native §2.2/§9.4 put `node_modules` in the TypeScript snapshot read set. State whether read-set bytes from pruned trees are custody-checked or explicitly exempt; the analysis facts they feed are Plan-bound either way.

## AR obligation dispositions

| AR | Disposition | Basis |
|---|---|---|
| AR-01 exact admission | ACCEPT | P17; foundation 386 reproduced |
| AR-02 authenticated qualification | ACCEPT | unchanged since v1 except CX-04 patterns; product-quality 24 and G13 v5 reproduced |
| AR-03 discovery/custody | CHANGES_REQUIRED | N-1; A-4, A-5; MUST-3/SHOULD-3/ADV-3 corrected |
| AR-04 trust clock/recovery | ACCEPT | P12, P18, sweeps |
| AR-05 expired root/live revocation | ACCEPT | P18, sweeps |
| AR-06 platform population | ACCEPT | P1 |
| AR-07 sealed inputs/execution boundary | ACCEPT (A-1, A-5) | P6; DS-1..6, prepared inert rows and grant admission reproduced |
| AR-08 invocation/repair lifecycle | CHANGES_REQUIRED | N-4, N-5, N-2; A-2 |
| AR-09 identity/retention closure | CHANGES_REQUIRED | N-3; SHOULD-1 corrected; identity 113 reproduced |
| AR-10 runnable prior detector/baseline | ACCEPT | P14, P19 |
| AR-11 typed comparison/imports | ACCEPT subject to N-3 | P14, P16, P19 |
| AR-12 resolution completeness | ACCEPT | P8; RC-1..5 and closed-world cases reproduced |
| AR-13 cells/discovery/parity | CHANGES_REQUIRED | N-1 (native side), N-2; A-3; inventory 45 commands, five renderers |
| AR-14 stage transition/concurrency | CHANGES_REQUIRED | N-5; lease mechanism itself reproduced (P10) |
| AR-15 current narrative | ACCEPT with advisories | A-4; SHOULD-7/8/10 corrected |
| AR-16 provenance-specific remedies | CHANGES_REQUIRED | N-2; MUST-1 corrected |

## Fallow constraint dispositions

FW-01 CHANGES_REQUIRED (N-1). FW-02 ACCEPT. FW-03 ACCEPT. FW-04 ACCEPT. FW-05 ACCEPT. FW-06 ACCEPT subject to N-3. FW-07 ACCEPT subject to N-5. FW-08 ACCEPT. FW-09 ACCEPT. FW-10 CHANGES_REQUIRED (N-4). FW-11 ACCEPT. FW-12 ACCEPT. FW-13 CHANGES_REQUIRED (N-2). FW-14 ACCEPT as a stated harness obligation. FW-15 ACCEPT.

## Inherited residuals, D-372 and readiness obligations

The sixteen DR-011 residual dispositions and the parent DR-001..011 rows remain lawful prospective dispositions. N-3 touches R06 (evidence closure) and R15 (trusted request context: an import's source binding is part of that context); N-1 touches R01 (declared view/subject-set joins) and R16 (bounded first-party composition must name the boundary rule); N-5 touches R04/R11 (stage delivery and G19 recovery). R10 correctly remains open for the blind consumer B, which this review does not perform. The thirty evaluation-proof residual dispositions are history-preserving and make no containment claim. The 32 qualification-gate rows honestly record `qualified=false`, `demonstrated=false`, `implementationHarnessAuthored=false` over the four machine IDs. The D-372 DR-003 timing disposition is a scoped condition-1 disposition with explicit release-gate retention and no SATISFIED/DEMONSTRATED claim; it is acceptable as proposed and grants no condition-5 authorization. The current source map's rows are consistent with the contracts; its G13 alias sentence is confirmed by P1. The crosswalk's `review` fields point to the predecessor review and must be replaced at application by this review's path and, later, the consumer-B record. Central and navigation documents remain pre-application, as intended.

## Limitations

Reference code ran only over synthetic fixtures; no OS custody, cryptography, SQLite durability, compiler, provider, renderer or repository code was executed and none is claimed. Unit expectations are same-author; this review is the independent oracle for the mixed bytes but not the blind implementer litmus. The historical corpus was read only where pinned and consumed. Severity is the reviewer's judgement against the contracts' own statements; each new SHOULD names a claim the contract makes that the reference bytes do not deliver.

## What the authors should do

1. Fix N-1..N-5 in new bytes (security/native/foundation/workflow owners as named), consider A-1..A-5, re-pin, regenerate reports and freeze a new exact subject.
2. Do not reuse this review for changed bytes; request a fresh independent re-review of the new frozen subject.
3. Only after that acceptance run the separate blind consumer-B review, then apply D-372, the source map and the central register.

Paths: this file, `review.json`, `probes/independent-probes.py`, `probes/independent-probes.json`, `reports/*` (launchers, reruns, `report-diff.json`), `hash-verify-before.json`, `hash-verify-after.json`, `scratch/` (run-in-place copy).
