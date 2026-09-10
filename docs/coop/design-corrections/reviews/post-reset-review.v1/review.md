# Independent integration/foundation review — candidate-subject.v1 (post-reset)

Reviewer: fresh actual Claude session (claude-fable-5-1). Authored none of the subject bytes.
Standing: independent substantive review of a FROZEN mixed-author subject. This is design/reference review, not implementation qualification, and it is not the blind consumer-B review (DR-011-R10), which remains a separate later act.

## Verdict: CHANGES_REQUIRED

Three MUST issues and ten SHOULD issues remain. The central architecture and most of the AR corrections are determinate and were independently reproduced (exact admission, authenticated qualification oracles, trust clock and poisoned-floor recovery, expired-root chains, live revocation, lease model, resolution completeness, sealed dependency inputs, portable baseline and pivot chain, repair journal and recovery, proof closure and replay). What blocks acceptance is that three cross-unit joins are not yet determinate: the public envelope cannot carry the typed details the other three contracts define; the security unit uses two disjoint platform-identity vocabularies; and the zero-config unit discovery path is not determinate on an ordinary repository with installed dependencies, and its refusal branch is untested and crashes in the reference. All counterexamples are executable and retained in `probes/independent-probes.json`.

## Subject and verification

| Item | Value |
|---|---|
| Manifest | `docs/coop/design-corrections/reviews/candidate-subject.v1.json`, sha256 `e7403b702d419f381be1cdbee7b886303fb43106b86985bc2f8ec63f5687a0ac` |
| Snapshot | `/tmp/opensip-design-corrections/candidate-subject.v1` |
| Pinned files verified | 1192 of 1192 (0 bad, 0 missing, 0 extra) before review; 1192 of 1192 again after all probes (`probes/independent-probes.json` P15, `hash-verify-after.json`) |
| Environment | Python 3.12.13, jsonschema 4.25.1, `-I -B` |
| Scratch copy | `scratch/docs/**` (checkers that write into their own directory were run there) |

## Executed checks

| Check | Result | Where |
|---|---|---|
| Foundation launcher (check-foundation 231, check-identity 113, product-quality 24, product-configuration 15) | 383/383, pins valid (1060) | `probes/foundation-launcher.json`, `probes/foundation-reports/` |
| Security lifecycle checker | 318/318 cases, 6/6 sweeps, pins valid | `probes/security-lifecycle-report.rerun.json` |
| Native evidence checker | 89/89 cases, 60 matrix cells, 0 open objects, F1–F12 and R1–R7 covered | `scratch/.../native/native-evidence-report.v2.json` |
| Workflows launcher | 1165/1165 checks, 13 schemas, 33 pins valid | `probes/workflows-launcher.json` |
| Integration checker | 43/43 | `probes/integration-report.rerun.json` |
| Report reproducibility | all nine regenerated reports byte-identical to the retained ones | `probes/report-diff.json` |
| Independent probes P1–P15 | 8 counterexamples, 2 inconsistencies, 2 gaps, 3 OK | `probes/independent-probes.py`, `probes/independent-probes.json` |

Read in full: REVIEW.md, D-372 act, crosswalk, source map, inherited residuals, qualification gates, integration issues, JOINT-INTERFACES, all five product contracts and README, all four unit READMEs, all reference models (`canonical.py`, `identity-model.py`, `host-foundation-model.v2.py`, `product-configuration-model.py`, `g13-validator.v5.py`, `product-quality-validator.py`, `security_lifecycle_model_v1.py`, `native_evidence_model.v2.py`, `workflows_model.v1.py`), the checkers, the integration host model and fixtures, the identity schemas, all thirteen workflow schemas, the command inventory, the security schema definitions for profile set / grant / discovery, the evaluation-residual dispositions, the prior foundation review and its disposition, the Codex feedback and handoff files, and the D9 v1.14 code table. Not re-read: the 1050 historical completion/artifact files except those pinned and consumed by the checkers (v8 root schema, d9 contract, delivery v4).

## MUST issues

### MUST-1 — The public envelope's closed detail vocabulary cannot carry the details defined by the other three contracts (AR-08, AR-13 surfaces, AR-16, FW-13)

Evidence (P1): `StepTermination.domainDetail.code` is the closed enum `DomainDetailCode` in `workflows/schemas/common.schema.json`. Validation refuses every detail the other units say they emit as request-rejection detail: `native.execution-not-authorized`, `native.stale-prepared-output`, `native.explicit-root-without-marker` (native §10), `storage.backup-choice-required` (identity §5, security S3.1, inventory flag joins), `GRANT.*`, `AUTHZ.*`, `RECOVERY.REFUSED`, `CLOCK-EXCURSION-FORWARD`, `ROOT.SCHEMA_UNSUPPORTED`, `MIGRATION.CORRUPT` (security S12), and `evidence.{expired,purged}` (identity §5). The only storage detail the envelope admits is `STORAGE.BACKUP_CHOICE_REQUIRED`, a second spelling of the same detail. The inventory goldens for `trust-recovery-import-refused` and `store-migrate-corrupt-footprint` therefore carry no `domainDetail`, and `query-evidence-purged` carries none either.

Why it blocks: workflows §9 and the inventory make the JSON envelope the parity reference for every renderer, and AR-16 requires provenance-specific remedies on that surface. Native §10 (H-3) and security S12 discharge their D9 obligations by saying the typed detail travels "as request rejection detail"; the schema that defines that detail refuses it. The product surface is therefore not determinate for any security, native or identity refusal.

Owning selectors: `workflows/schemas/common.schema.json#/$defs/DomainDetailCode`; `workflows-and-surfaces.md` §9 and §12; `native-evidence.md` §10 table and H-3/H-4; `security-and-lifecycle.md` S12 (first) table; `identity-and-evidence.md` §5 (`evidence.*` details); `workflows/command-inventory.v1.json` goldens.

Return to Codex: one detail-code registry (or namespaced open enum with per-owner registration) that every unit's typed details join, one spelling for the storage detail, and goldens that carry the security/native/identity details; add negative cases that an unregistered detail is refused and positive cases for each cross-unit detail.

### MUST-2 — Two disjoint platform-identity vocabularies inside the security unit; no mapping to the delivery/native identities (AR-06, AR-07, AR-13, FW-03)

Evidence (P2): `PlatformProfileSetV1.platforms` keys and `SUPPORTED_POPULATION` are `macos-arm64`, `macos-x86_64`, `linux-x86_64`, `linux-arm64`; `RepoExecutionGrantV2.platformId`, `PLATFORM_TRUTH_TABLE`, the native matrix `platformFamilies`, the test-execution schema and `qualification-gates.proposed.json` are `macos-aarch64`, `macos-x86_64`, `linux-x86_64-gnu`, `linux-aarch64-gnu`. `platform_admit` with `platform=macos-aarch64` refuses `NT-TCB-PROFILE-UNQUALIFIED:platform-not-in-population`; a grant with `platformId=macos-arm64` is schema-invalid. Only `macos-x86_64` coincides. The S8 table in the contract itself uses the first vocabulary while S10 says "one of the four delivery platforms". Integration issue 3 claims the four machine IDs are shared; that is true only between security S10, native and workflows, not for the profile set that decides admission.

Why it blocks: the admitted platform identity is the join between platform admission (AR-06), grant admission (AR-07), matrix cells (AR-13) and the qualification lanes; without a stated equivalence the product cannot say which admitted profile authorizes which grant or qualifies which cell.

Owning selectors: `security-lifecycle.schemas.v1.json#/schemas/PlatformProfileSetV1/properties/platforms`, `security_lifecycle_model_v1.py` `SUPPORTED_POPULATION` vs `PLATFORM_TRUTH_TABLE`, `security-and-lifecycle.md` S8 table vs S10, `platform-admission-cases.v1.json`, `native-capability-matrix.v2.json#/platformFamilies`, `qualification-gates.proposed.json#/platformFamilies`.

Return to Codex: select one machine vocabulary (the delivery four) for the profile set, admission output, grant, matrix and gates, with display aliases only in an explicit table; re-pin fixtures; add a case that a profile-set platform key outside the delivery set is refused.

### MUST-3 — Zero-config unit discovery is not determinate on an ordinary repository with installed dependencies, and the cap refusal is untested and crashes (AR-03, AR-13, FW-01)

Evidence (P3, P4, P5):
- Security S3 automatic marker scan (`discovery.finish`) makes every `node_modules/<pkg>/package.json` a workspace unit; on the fixture root with two installed packages the provenance lists three units. With 4200 installed packages the reference raises `KeyError('REQUEST.UNSATISFIABLE')` inside its own `WORKSPACE_UNIT_LIMIT` refusal because that code is absent from the security D9 table; no fixture exercises the cap (`grep WORKSPACE_UNIT_LIMIT` finds none). A typical JavaScript checkout exceeds 4096 package manifests.
- Native `discover_units` likewise creates a unit for `node_modules/left-pad/package.json`; native U-4 names `node_modules/` only as a file-membership ignore convention, and `assign_membership` applies it as a path substring, so `packages/target/index.ts` and `src/target/x.ts` are erased from the program as "host-ignore-convention".
- Config2 `discovery.workspaceRoots: ["."]` is `ACCEPT` in security (S12: "." names the admitted root; identity §3 defines the sentinel) and `CONFIG.INVALID` / `native.explicit-root-without-marker` in native `discover_units`.

Why it blocks: FW-01 zero-config is a selected product constraint; the default `opensip` invocation's unit set is the input to scope, Plan identity and every capability selection. Two reference instruments disagree, neither states an ignore rule for dependency trees, the effective bound (1024 scope roots per native §11) is reached by dependency manifests, and the refusal path has never run.

Owning selectors: `security-and-lifecycle.md` S3 (marker scan, 4096 cap, `unitSource: automatic`), `security_lifecycle_model_v1.py` `discovery.finish` and the `D9` table; `native-evidence.md` §1.4 U-1/U-4/Config2 join and §11 (1024 effective bound); `native_evidence_model.v2.py` `discover_units`, `assign_membership` (`HOST_IGNORE`), `_LOGICAL_RE`; `identity-and-evidence.md` §3 scope sentinel.

Return to Codex: one discovery rule that excludes dependency, VCS and build-output trees from unit enumeration by anchored path segment (not substring), stated once and consumed by both instruments; native must accept the "." sentinel exactly as security/foundation do; add the cap refusal to the security D9 table and fixtures; add a monorepo-with-node_modules case to both units and to the integration checker.

## SHOULD issues

- **SHOULD-1 (AR-09, AR-11, FW-06)** Identity closure accepts a finding whose `evidenceRefs` names an `import2` that is in neither `plan.importIds` nor `proof.evaluationInputRefs` (P8: `close_run` returned `ACCEPTED`). Identity §4 forbids hidden lookups and §3 rejects extra authoritative roots, but `identity-model.py close_run` constrains only predicate `inputRefs`. Require finding evidence refs of domain `import` to be members of `plan.importIds` and add a negative case.
- **SHOULD-2 (AR-07, AR-08)** Security S10 refuses any `RepoExecutionGrantV2` whose principal is not projected in "the Plan's semantic-grant" (P11: `GRANT.SEMANTIC_PRINCIPAL_NOT_PROJECTED` without a projection). A test-runner grant belongs to a `test-execution` step, which workflows §1/§7 define as an operational step with no Plan; identity §3 says the projection carries only operations the analysis needs. No contract states which Plan projects the test-code principal. `check-integration.py bind()` fabricates the projection from the grant itself, so the passing integration check does not establish the join. Also the `ownerSourceDigest` for a test-runner is the digest of an empty owner array, which binds nothing. Decide: either exempt test-runner from the projection rule and bind the runner member instead, or name the consuming Plan.
- **SHOULD-3 (AR-03, AR-09)** Security S3.1 prose says a root classified "backup-managed or UNKNOWN" needs an explicit choice; its own model, fixture `unknown-backup-status-is-not-not-backed-up`, the S13 addendum, identity §5 and the inventory flag joins all admit UNKNOWN with disclosure (P6). Correct S3.1.
- **SHOULD-4 (AR-12, FW-08)** Native §4.6 lists nine sufficiency steps "evaluated in this order"; `sufficiency_v2` applies step 9 (one-rung/existential/partial-ok satisfied outright) before step 3 (confidence floor). P7: a `clones` requirement with floor 900000 over an entry at 100000 is `satisfied` in v2 and `confidence-floor-unmet` in the retained v1 oracle. Align model to prose and add the case.
- **SHOULD-5 (AR-08, FW-07, FW-10)** The repair-apply authorization join is not exercised across units: `workflows_model.repair_apply` accepts a synthetic `{repairPlanId, snapshotId, projectId, live}` dict, `RepairApplyParams.authorizationRef` and `RepairApplyJournalV1.authorizationRef` are free text (minLength 1) rather than the `security.repair-apply-authorization.v1:` grammar the test-execution schema uses for its grant, and `check-integration.py` contains no repair join although security S10.1 defines `admit_repair_authorization`. Pin the grammar and add the composed admission to the integration checker.
- **SHOULD-6 (AR-14)** Lease scope of core lifecycle commands is unspecified (P14). S7 lists `update` as fence-only with no project lock; S13 says `core update|repair|rollback` "use EXCLUSIVE admission", but EXCLUSIVE is a per-namespace project lease and a core transition is install-level state. State whether core transitions take the fence only, EXCLUSIVE on every namespace, or a new install-level mode, and add cases.
- **SHOULD-7 (AR-15)** Documentation accuracy defects of the kind AR-15 names: `security-and-lifecycle.md` has two `## S12` and two `## S13` headings and `native-evidence.md` has two `## 11` headings, the exact selector hazard the source map warns about; native §7.4 and §13 "recorded conflicts" describe a workflow conflict that the current workflow bytes have already resolved (raw-SHA auxiliary digests, single payload domains) and cite `AuthorizedExecutionV1` on the security side (the model comment at line 1510 still says V1); `reviews/native-fix-handoff.v3.md`, cited by the native contract and README, is an empty file; security S13 says 312 cases (actual 318). Refresh the prose and retire stale conflict text.
- **SHOULD-8 (AR-04, AR-15)** The inventory labels `trust-recovery-import` with `authorizationClass: root-quorum`, whose schema description reads "a root-signed artifact (S4.5)"; S4.5 says root keys never count and the authority is `recoveryAuthority` at its threshold. Rename the class (for example `recovery-authority-quorum`) and correct the description.
- **SHOULD-9 (AR-08, FW-15)** `workflows_model.evaluate` makes the whole verdict indeterminate when a non-gating rule's required evidence is absent, but not when the same non-gating rule is indeterminate under incomplete coverage (P9: `indeterminate` vs `pass`). Workflows §5 says only an indeterminate gating rule is a typed deficiency. State the intended rule and align the model.
- **SHOULD-10 (AR-15, D-372 review provenance)** The snapshot retains no Codex review record for the final native and workflows bytes; only intermediate feedback files exist, and the native contract cites a "Codex independent review v2 (R1–R7)" whose record is absent. The crosswalk `review` fields are all null. This fresh review covers the mixed bytes substantively, but the D-372 application must name the actual review artifacts per unit and must not cite a review that is not retained.

## Advisory

- **ADV-1 (AR-11)** As written, any change of a gating rule's bound import identity yields `INDETERMINATE` for every entry of that rule (P10: `evidence-content-changed`). Freshly collected runtime or test artifacts differ on every CI run, so gating rules that declare evidence can never yield a determinate changed-code verdict. This is contract-consistent; confirm it is the intended product behaviour or add an evidence pivot that re-evaluates the baseline side under current evidence.
- **ADV-2 (AR-10, AR-11)** Unbound E1–E3 re-evaluations make every entry `INDETERMINATE`, including pure code regressions. Since E1–E3 are host-computable from retained facts, state that the host must bind them whenever the corresponding axis changed, so the "unavailable" branch is an operational fault rather than a lawful host choice.
- **ADV-3 (AR-03)** S3 selects the nearest ancestor with an `opensip.json` before reaching the VCS root, so a nested config re-roots the project to that subdirectory and scope again varies with launch directory, which the VCS-root rule was introduced to prevent. Confirm intended and add a case.
- **ADV-4 (AR-15)** Crosswalk AR-15 lists `integration-report.v1.json` twice; every `review` field is null and must be filled from actual review artifacts at application.
- **ADV-5 (AR-01)** No defects found; the depth rule (root container counts 1, 33 refused), `-0`, exponent, bool-versus-integer and duplicate-key refusals, the domain frame and the G13/product validators all behave as specified in the rerun.

## AR obligation dispositions

| AR | Disposition | Basis |
|---|---|---|
| AR-01 exact admission | ACCEPT | foundation canonical/config v2/G13 v5/product v3 reproduced; no gap found |
| AR-02 authenticated qualification | ACCEPT | independent context, oracle atoms, signature, baseline pair rules reproduced |
| AR-03 discovery/custody | CHANGES_REQUIRED | MUST-3, SHOULD-3, ADV-3 |
| AR-04 trust clock/recovery | ACCEPT (SHOULD-8 label) | refusal-before-write, single-boot challenge, exact counters, recovery authority reproduced by sweeps |
| AR-05 expired root/live revocation | ACCEPT | chain thresholds, final freshness, schema-2 typed refusal, linearization and postimage rollback reproduced |
| AR-06 platform population | CHANGES_REQUIRED | MUST-2 |
| AR-07 sealed inputs/execution boundary | CHANGES_REQUIRED (SHOULD) | SHOULD-2; DS-1..6, prepared inert rows, carrier rules and grant admission otherwise determinate |
| AR-08 invocation/repair lifecycle | CHANGES_REQUIRED | MUST-1, SHOULD-5, SHOULD-6, SHOULD-9 |
| AR-09 identity/retention closure | CHANGES_REQUIRED (SHOULD) | SHOULD-1, SHOULD-3; closure, replay, receipts, availability, purge otherwise reproduced |
| AR-10 runnable prior detector/baseline | ACCEPT | pivot closure, fresh-CI admission, detector union and removal semantics reproduced; ADV-2 |
| AR-11 typed comparison/imports | ACCEPT (ADV-1) | single import2 wrapper, registry, mapping law, staleness table reproduced |
| AR-12 resolution completeness | ACCEPT (SHOULD-4) | RC-1..5, closed world, propagation and the m[k] counterexample reproduced |
| AR-13 cells/discovery/parity | CHANGES_REQUIRED | MUST-2, MUST-3; inventory of 45 commands and five renderers otherwise complete |
| AR-14 stage transition/concurrency | ACCEPT (SHOULD-6) | schema bridge, migration recovery table, floor continuity, lease matrix reproduced |
| AR-15 current narrative | CHANGES_REQUIRED | SHOULD-7, SHOULD-8, SHOULD-10, ADV-4 |
| AR-16 provenance-specific remedies | CHANGES_REQUIRED | MUST-1 |

## Fallow constraint dispositions

FW-01 CHANGES_REQUIRED (MUST-3). FW-02 ACCEPT (clone modes, candidate-only cross-TS/JS, review suppression by stable key). FW-03 ACCEPT subject to MUST-2 vocabulary. FW-04 ACCEPT (no-hits is not non-use; unmapped never feeds a predicate). FW-05 ACCEPT (ADV-1/2). FW-06 ACCEPT subject to SHOULD-1. FW-07 ACCEPT subject to SHOULD-5. FW-08 ACCEPT subject to SHOULD-4. FW-09 ACCEPT (advisory records admit no Control field). FW-10 ACCEPT subject to SHOULD-5. FW-11 ACCEPT (profiles, code-net-new-policy-hidden). FW-12 ACCEPT. FW-13 CHANGES_REQUIRED (MUST-1). FW-14 ACCEPT as a stated harness obligation. FW-15 ACCEPT subject to SHOULD-9.

## Inherited residuals and readiness obligations

The sixteen DR-011 residual dispositions and the parent DR-001..011 rows are lawful prospective dispositions; none is contradicted by this review except where SHOULD-1/SHOULD-2 touch R09/R15 (hidden evidence input; trusted request context for the test principal) and MUST-1 touches R08 (D9 detail carrier). R10 correctly stays open for the blind consumer B. The 30 evaluation-proof residual dispositions (19 RES, 7 NB, 4 measured escapes) each state the product boundary without a containment claim and are acceptable as history-preserving dispositions. The 32 qualification-gate mappings are consistent with the contracts and honestly record `qualified=false`, `demonstrated=false`, `implementationHarnessAuthored=false`; the `platformFamilies` list must follow MUST-2. Synthetic signatures, evaluator callbacks, OS observations and detector pivot presences are stated assumptions throughout and were treated as such.

## Limitations

Reference code was executed only over synthetic fixtures; no OS custody, cryptography, SQLite durability, compiler, provider or repository code was run and none is claimed. The historical completion corpus was read only where pinned and consumed. Expectations in the units are same-author; this review is the independent oracle for the mixed bytes but not the blind implementer litmus. Severity assignments are the reviewer's judgement against the contracts' own statements.

## What Codex should do

1. Fix MUST-1..3 and SHOULD-1..10 in new bytes, re-pin, and freeze a new exact subject.
2. Do not reuse this review for the changed bytes; request a fresh independent re-review of the new frozen subject.
3. Only after that acceptance, run the separate blind consumer B review.

Paths: this file, `review.json`, `probes/independent-probes.py`, `probes/independent-probes.json`, `probes/report-diff.json`, `probes/*-launcher.json`, `probes/*.rerun.json`, `hash-verify-before.json`, `hash-verify-after.json`.
