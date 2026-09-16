# Source38 advisories ADV38-01, ADV38-02, ADV38-03 and review of root's A5 correction

**Standing.** This is the same actual Claude coauthor (origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`) doing an architecture/design/reference correction.

- **Not acceptance.** No source-level, full-design or readiness acceptance, and no product qualification.
- **Where the work lives.** All work is in this runtime. The correction is a regular-copy working tree (`work/edited`) over frozen source38; `work/baseline` is the untouched copy.
- **Not done.** No live, frozen, history, global pin, planning or grade edits; no subagents, web, commit or push. Root's A5 patch was not copied into this tree.
- **Recovery cases.** All 54 product recovery cases (F00–F53) remain not executed.

## Custody (p00, p04)

- **Parent.** Manifest `2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5`, verified once. 12904 members and 737100757 bytes match, with no unlisted file.
- **Working copies.** `work/baseline` and `work/edited` hold 1359 files each: `docs/` minus `design-corrections/reviews`. Every copied file has its own inode with `st_nlink == 1`, and equals the manifest.
- **At the end (p04):**
  - the 10 touched files and 33 dependency files are unchanged in source38;
  - every dependency in the edited tree still equals source38;
  - no file was added or removed;
  - the completed independent review and root's A5 inputs are unchanged.

## Dispositions

| Item | Decision | Files |
|---|---|---|
| ADV38-01 | **CORRECTED.** A published host composition law at the finalizer boundary, with a closed analysis detail allowlist, attempt/Run binding and the committed-versus-ephemeral authority rule; executed controls and discrimination | run-termination contract, model, goldens and checker; one shared sentence in workflows-and-surfaces §9 |
| ADV38-02 | **CORRECTED.** A carrier observed unmigrated maps explicitly to F46 `unknown-carrier-incompatible`, with stated precedence; SQLite controls for format 1 and 2 | dispatch JSON, carrier-format §8.1/§9, S12 row, read-only §1/§3, carrier checker |
| ADV38-03 | **CORRECTED.** F00–F53 current scope and the writer/maintenance scope of `MIGRATION.CORRUPT`, with a control | read-only §1 (same file as ADV38-02) |
| A5 review | **CORRECTIONS REQUIRED.** Two substantive and one editorial correction, with a separate proposed amendment | `a5-review/` only |

## ADV38-01: delegated members of an analysis termination

**Problem confirmed.** `check_projection` admitted a shape-valid unrelated registered detail, such as `HOST.INVARIANT_VIOLATED` or `QUERY.*`, as `owner-validation-required`. No owner closed the law. The implementation-coverage method only said "separately validate … under their host owners".

**Correction.** The pure analysis projection is unchanged: `check_projection` has the same refusals and the same scoped standing. New `run-termination-contract.v1.md` §7 is the admission law that the host finalizer applies to the whole `StepTermination` (`admit_analysis_step_termination`).

**Scope (§7.1).**
- Composed: a `success`, `policy-failed` or `indeterminate` termination decided by the sealed verdict.
- Not composed here: `operational-failed`, `request-rejected` and `interrupted`. The composition returns their owner (D9 `causeModel`, workflows §1/§9, S12, native §10 route registry) **without reading a Run**, so operational carriers such as `HOST.INVARIANT_VIOLATED` on `host-invariant` are never passed through verdict derivation.

**Two kinds of input (§7.2).**
- Retained semantic content: the Run admitted by `close_run`, its population and the record named by `coverageId`.
- Host-supplied operational inputs, trusted but not authenticated:
  - the step's existing `invocation-record` `Attempt` records;
  - `AnalysisParams.durability`;
  - the identity `commit-receipt`;
  - one installation observation.

  No new public field is added.

**`executionId` (§7.3).**
- The terminating attempt is the last one: `completed`, with no earlier `completed` attempt and no repeated id.
- The receipt's `runId` is the derived one, and the receipt's `executionId` is the terminating attempt's. The reference commit path issues one receipt per committing attempt.
- The attempt's `derivation.planId` is the Run's `planId`.
- When present, `executionId` must be that attempt's: an earlier retried or foreign id refuses.

**`authority` (§7.4).**
- Committed Run: `runId`, and `authority` omitted. Every retained golden and workflow case uses that spelling.
- Ephemeral attempt: `authority=ephemeral` on every verdict class, never `runId`, no receipt, no detail. Its reasons are not derived by this contract.

**Closed `domainDetail` allowlist (§7.5).** The first row whose prerequisites hold is **required**, and no detail is lawful when none holds. The detail is meaning-bearing: the `kind=failure` envelope's `errors` is that detail (workflows §8), and the aggregate keeps the first termination with a detail (§1). So the selection is deterministic.

| # | Code | Retained prerequisite | Host prerequisite | Authorizing owners |
|---|---|---|---|---|
| 1 | `EVALUATION.WORK_BUDGET_EXHAUSTED` | a `work-budget-exhausted` population record, **and** the primary D9 deficiency is `budget-exhausted` | — | composition §8, §9.6; workflow-projection Appendix; registry (workflows) |
| 2 | `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | `reasonCodes[0] = COVERAGE.PROVIDER_UNAVAILABLE` | required provider closure observed not installed | workflows §9 golden; command-inventory.v3 `default-missing-required-closure`; workflow-cases `indeterminate-provider-unavailable`; registry (workflows) |
| 3 | the named record's `entry.deficiency` ∈ {`budget-exhausted`, `derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete`, `resolution-incomplete`} | `coverageId` names that `coverage2` record | — | native §10 "Retained and public routes…"; registry (native) |

- **Excluded:** every other code, including `QUERY.*`, `DOCTOR.*`, `HOST.INVARIANT_VIOLATED`, `native.*` refusals, `COMPARISON.*`, `BASELINE.*`, `PROJECT.BUSY`, `MIGRATION.CORRUPT`, `RECOVERY.REFUSED` and `evidence.*`. `success` and `policy-failed` carry none.
- **Shape of the detail:** `{code, remedy}` only. `remedy` is presentation text and is not compared.
- **Nothing new is invented.** No blessing flag (a `valid` member refuses as an unknown field), no public field, no D9 code and no registry member. The new `RUN_TERMINATION_*` refusal keys are internal reference diagnostics, the same family as the existing ones.

**Controls.** Golden `host-composition-boundary` has 37 cases over actually closed Runs (p01 edited.r2); semantic replay 31/31 rows pass. All candidates except the blessing member are schema-valid StepTerminations.

| Group | Cases | Outcome |
|---|---|---|
| admitted | work budget with a stage carrier; the D9 golden Run; a retried terminating attempt; row 3 with a declared carrier and with a stage carrier; closure not installed; provider-unavailable with no installation observation (row 3); lawful omission; a verdict Run | the expected `ADMIT:<code/none>` |
| refused: detail | `HOST.INVARIANT_VIOLATED`, `QUERY.PARAMS_MALFORMED`, `DOCTOR.DEFECTS_FOUND`; work budget with no retained budget; work budget as a secondary; closure detail with no observation; closure detail over a budget primary; detail on a verdict; detail `subject` | `DETAIL_NOT_ADMITTED` / `DETAIL_MEMBER_NOT_ADMITTED`. The **pure projection still reports `owner-validation-required`** for the same candidates |
| refused: omission | selected detail omitted | `DETAIL_REQUIRED` |
| refused: attribution | earlier retried attempt; foreign id; Run committed by another attempt; receipt for another Run; attempt bound to another plan; terminating attempt not completed; committed Run with no receipt | `EXECUTION_ID_NOT_ATTEMPT`, `RECEIPT_ATTEMPT_MISMATCH`, `RECEIPT_RUN_MISMATCH`, `ATTEMPT_PLAN_MISMATCH`, `ATTEMPT_NOT_TERMINATING`, `OBSERVATION_SHAPE` |
| refused: other | `authority=authoritative` beside `runId`; a blessing member; an allowlisted detail over a wrong projection | `AUTHORITY_NOT_COMPOSED`, `UNKNOWN_FIELD`, `NOT_DERIVED` |
| ephemeral | `policy-failed` admitted; `success` without authority, with a `runId`, or with a work-budget detail refused | as stated |
| outside | required delivery after commit; host invariant; interrupted; request-rejected | `OUTSIDE`, with no Run supplied |

**Discrimination (p03).** Each variant is a hybrid regular copy, and exactly the expected controls fail:

| Variant | What changed | Failing controls |
|---|---|---|
| model-baseline | baseline model restored | only the composition row |
| detail-law-disabled | detail equality check removed | exactly the 8 detail refusals |
| attempt-join-disabled | receipt/attempt join removed | exactly `run-committed-by-another-attempt` |
| execution-id-law-disabled | `executionId` binding removed | exactly the earlier-retried and foreign attributions |
| outside-forced-through-derivation | early return removed | exactly the 4 operational/interrupted/rejected cases |

**Shared selectors for root and the workflow coauthor.**
- **Changed:** `workflows-and-surfaces.md` §9, last paragraph. It now says the owner derives the projection, that its §7 is the composition law, and that fault, rejection and interruption stay outside.
- **Cited, unchanged:**
  - workflows §1 (attempts, retry, ephemeral, aggregate tie), §8 (failure `errors`) and the §9 golden row;
  - `command-inventory.v3.json` and `workflow-cases.v1.json` ids;
  - `public-detail-registry.v1.json` records;
  - `invocation-record.schema.json#/$defs/Attempt` and `AnalysisParams.durability`;
  - `identity-schemas.v3.json#/$defs/commit-receipt`;
  - native §10.

  If the workflow coauthor changes the registry, the failure-envelope rule or those goldens, §7.5 must be rechecked.
- **Suggested for root, not edited:** the inventory `outcomes.rs` description and the implementation-coverage `workflows-and-surfaces:10` method can now cite contract §7.

**Design choices root should weigh.**
- Row selection is *required*, not merely permitted. This is new host behavior. For example, the stage-unavailable golden Run must carry `resolution-incomplete` when no installation observation exists. A permit-only rule would make `errors` and the aggregate tie host-dependent.
- `authority` is omitted on a committed Run.
- Row 1 requires the work budget at the primary rank.

I found no retained golden or case that contradicts these; independent review should still judge them.

## ADV38-02: association naming a carrier observed unmigrated

**Decision.** Keep the existing prose route and make it machine-explicit: **F46 `unknown-carrier-incompatible`** (operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, detail omitted) for dispatch results `carrierFormat1` and `carrierFormat2`.

Quarantine was not chosen. The observation is made from object names before the SEAL join, like the existing below-`first_generation` F46. It names no corruption of the observed carrier's own footprint, and an association (written only with a committed carrierFormat 3 SEAL) contradicts two retained owners, which is the `unknown-custody` family. Both candidate routes fail closed at exit 4.

**Precedence (read-only §1; carrier-format §8.1; dispatch `phaseLaws`).** All inside one journal snapshot, before the SEAL join:
1. `binding-unusable`, before any carrier read.
2. With any carrierFormat 3 object present:
   - footprint, project binding (row or witness), F51 and row-boundary conditions → quarantine row with Step 4 stable observations, otherwise `unavailable-busy`;
   - an unpublished lawful prefix → `unavailable-busy`;
   - then an association generation below `first_generation` → F46.
3. With no carrierFormat 3 object and an inherited `grant_journal` → F46, whatever generation the association or a surviving witness names. It is decided from object names and needs no witness comparison, so the Step 3 witness and anchor rows are not reported. Step 4 does not gate it, because it is not a quarantine report.

No read-only migration, publication or write happens on any path.

**Edits.**
- `carrier-dispatch.v3.json`:
  - `readOnlyStandingOfDispatchResult` gains `carrierFormat1`/`carrierFormat2` → `unknown-carrier-incompatible`;
  - the F46 observations and `readerLaws` name the unmigrated carrier;
  - `phaseLaws` gains the precedence;
  - the standing note is updated.
- `carrier-format.v3.md`: the §8.1 F46 row, a new paragraph, and the §9 reader law.
- S12 F46 row: "or of a carrier observed unmigrated … decided before the SEAL join, after the binding row and any carrierFormat 3 footprint row".
- Read-only §1 paragraph plus a precedence list, and the §3 carrier sentence.

**Controls.** SQLite 3.50.4 in memory, through the retained `_s37_open` owner dispatch. Carrier validator 384/0 (baseline 362/0).
- Real `ddl1` (security-completion v1) and `ddl2` (security-schemas v2) carriers with a row:
  - each opens as its format at a writer open;
  - associations naming generations 1, 2 and 7 give F46;
  - an association naming another carrier gives `binding-unusable` first;
  - a witness naming another project does not displace F46;
  - dispatch writes nothing and creates no carrierFormat 3 object;
  - adding one carrierFormat 3 object gives footprint corruption (quarantine row), not F46.
- The migrated below-`first_generation` association is still F46.
- A `grant_journal_v3` row below `first_generation` is decided before it.
- Map, law and prose checks.

**Discrimination.**
- Baseline dispatch JSON restored: 374/10, exactly the ADV38-02 map, law and 8 unmigrated scenario checks.
- Baseline prose restored: 382/2, exactly the ADV38-02 and ADV38-03 prose checks.

**Checker robustness.** A read-only result with no standing is now a failed check instead of a `KeyError` that aborted the whole checker; the dispatch-baseline variant exercises this.

## ADV38-03: stale scope phrases

- **Line 39.** Now reads: the plan "was F00–F37 when this document was authored; the current `commit-recovery-plan.v1.json` holds F00–F53, and all 54 cases remain not executed". The history is kept as history.
- **`MIGRATION.CORRUPT`.** Not reused on any read-only path. S12 scopes it to a store transition footprint and, at a writer or maintenance carrier open only, to a carrierFormat 3 migration footprint (including F51). The read-only distinction is preserved.
- **Standing note.** Names the source38 advisory corrections.
- **Unchanged.** `store-instance-lineage.v1.json` already carries a correct current-standing note and is not edited.
- **Control.** A prose check, with discrimination above.

## A5 review (separate: `a5-review/assessment.md`)

**Accepted:**
- effective `allowJs=true` for a tsconfig with `checkJs=true` and no `allowJs`;
- both flag formulas, consistent with `typescript_mode`, `universe_context_field_faults` and the boolean-only `TypeScriptHonoredOptionsV1` and resolved-input schemas;
- zero JS roots;
- explicit `false` with `checkJs=true` (5052) left unrewritten.

**Corrections:**
- **A5-C1 (substantive).** "Apply configuration inheritance before these defaults" contradicts TypeScript 5.6.3, which applies the jsconfig default per file beneath that file's options and then merges `extends` (`typescript.js:42796-42802`, `:42581`).
  - A jsconfig entry extending a base that writes `allowJs:false` is effective `true`.
  - A tsconfig extending `shared/jsconfig.json` inherits `true`.
  - Over 52 retained compiler rows (root's 32 plus 20 new offline cases with the custody-verified compiler), root's law disagrees on 8 and the amended law on 0.
- **A5-C2 (substantive).** Retained native case `ts-tsconfig-without-allowjs-excludes-js` still expects the old default, and root's corrected model now fails it.
- **A5-C3 (editorial).** The `ts-tsconfig` row omits jsconfig entries with explicit `false` (`configOrigin=jsconfig`).

**Proposed amendment.** `a5-review/proposed-amendment.r2.diff` (`e86be974…`, 184 lines). Amended `native-evidence.md` `68184d04…`; amended `native-cases.v2.json` `f382d81a…`, a byte-preserving splice. All amended `typescript_mode` cases agree with root's model, and both `checkJs`-only cases fail on source38's model.

**Observation.** No owner I found routes option diagnostic 5052 into admission.

## Touched files (source38 → edited)

| File | Before | After |
|---|---|---|
| `docs/coop/design-corrections/foundation/run-termination-contract.v1.md` | `7fdaae67ae6f4439e6e2de9b19946b188169474f9e32a6289cb671a81b4f3436` | `155fa57b66539056e866a9e08dc9a7d7daadde00f54f88a4d254593a6015252d` |
| `docs/coop/design-corrections/foundation/run_termination_model.v1.py` | `2b9dd91782147182d55b50f52527641868ab01b1cc985109bddd1084bef7cf49` | `6196be9ba9cd07badeba42b85e7849153ae0c2b2a080a67dd0d3488b5c6ad101` |
| `docs/coop/design-corrections/foundation/run-termination-goldens.v1.json` | `9bdde8236ce24b299b36100325df4a6874bbba4e86d4abf308b653da457f4fcc` | `85ed0bf71071699f9f6264c3a0d764cb142f84b4e1f1209d654e82ad97ee8c17` |
| `docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` | `bc8a82e08bc3bebcc157c4e9adbf4f822c2d4ba5aeb323e8108679f346e03bb4` | `a18122933de03e3846f179bd65e8663d78105ab1001071a41e51e30e33c7c450` |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `857d6bbed265a51cf0df68cf072863f4eeb28726b6b1ed8c04272dc663f951ec` | `167c73bf17d3143b2080f12bb4a87b8e85994ddfbf71a71022621cafd14d3bc5` |
| `docs/coop/design-corrections/security/carrier-dispatch.v3.json` | `62b1958e7e2832bab77215078334b8821a252ed27c6e7a976de7d0ae79c82600` | `6d9eb28d4c13f9a88d480b16823339df592ec282b3dbacf8db91bdd91b84e2e1` |
| `docs/coop/design-corrections/security/carrier-format.v3.md` | `10608c16c510a4eb4a65a01ffedae267c625e4d999ebc5946349659bc8f1be3e` | `42b118903f6e429202f62e2469b61ddccae33aa4ce999e262eb080b50afeb97d` |
| `docs/coop/design-corrections/security/check-carrier-v3.py` | `4948301df3752c52e4eabae0b529063bbfceed905ba4395d5ff970b639838747` | `7e397699370270fc8f1204a91ca4552b04563970b0bd61a567df6af632968da2` |
| `docs/v2/architecture/commit-recovery-readonly.v3.md` | `3b32d24a3c6e71954bee620dc0add29f72aa35cfb643cac86a7d7d719238e85a` | `a6d0ce729cf33efa4410f9e7746e541969b730da2a93a832c0d7a4296456732f` |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | `9ca85de10f4f364b7dceb015799189796f12094fe506e1f172aa809c746ece32` | `60e67e7dc5b941fe1e0bfe00f9abfc1e5980b56563504ce516b1faa6666a7371` |

- **Full correction diff:** `proposed-edits.diff` (`ac36485a0c785e8c49b34d8aafac16406716a7091ab310273a956d742e4e70df`, 1032 lines).
- **Dependency hashes:** listed in `receipts/p04-summary.final.json`.

## Bindings awaiting root rebind (computed, not edited)

- **Before-hash pins.** Five source-pin ledgers pin all 10 touched files: foundation `evaluator3-source-pins.v1`, foundation `source-pins.v1`, native `source-pins.v2`, security `source-pins.v1` and workflows `source-pins.v1`. `implementation-coverage.v1.json`, `implementation-normative-inputs.v6.json` and `implementation-planning-sources.v1.json` also pin 6 of them: run-termination contract, carrier-dispatch, carrier-format, read-only v3, security-and-lifecycle and workflows-and-surfaces.
- **Planning section selectors:**
  - `security-and-lifecycle:12` (S12 text);
  - `workflows-and-surfaces:10` (§9 text; lines 1135–1189 → 1135–1193);
  - `workflows-and-surfaces:11`–`13` (line ranges shift by +4; text unchanged).
- **Candidate manifest pins** by construction. The planning checker and global groups were not run.

## Failed attempts preserved

- `receipts/a5_amendment.*` (exit 1) re-serialized `native-cases.v2.json`, which does not round-trip. Its outputs `a5-review/amended/` and `proposed-amendment.diff` are kept and superseded by `a5_amendment_b` (exit 0).
- No other probe failed. The first `p01` edited report (before the checker robustness and docstring edits) is kept as `receipts/p01-edited`; `p01-edited.r2` covers the final bytes.

## Limits

- **Reference evidence only.** In-memory SQLite and synthetic native-admitted Runs; F00–F53 are not executed; no product host, ledger, installation probe or authentication.
- **§7 limits:**
  - host inputs are trusted, not authenticated;
  - §7.5 row 2 rests on a host installation observation that no retained record carries;
  - row 3 is exercised only with `resolution-incomplete`;
  - ephemeral reasons are not derived.
- **ADV38-02 limits:**
  - the Step 4 two-capture stability is covered by the route law check, not simulated with two snapshots;
  - `fresh-install` (no journal table at all) with an association has no read-only standing in the map. That is outside the advisory and noted for root.
- **A5 limits.**
  - The 20 `extends` shapes are bounded.
  - TypeScript 5.6.3 is supporting evidence, not a pin.
  - The native checker was not run.
- **Only the two focused owner validators were run.** No global six groups and no planning checker.
- All foreground and background subprocesses have completed.
