# Source38 advisory follow-up v2: execution-plan and receipt-inventory joins, and the absent-carrier read-only route

**Standing.** This is the same actual Claude coauthor (origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`) doing an architecture/design/reference correction only.
- **Not acceptance.** No acceptance of integrated bytes, readiness or product qualification.
- **Where the work lives.** This new runtime only. `work/edited` is a regular copy of v1's `work/edited`.
- **Untouched.** v1, frozen source38, LIVE, root's A5 and root's assessment are unchanged.
- **Not done.** No A5 redo, no global pins, planning, grades, subagents, web, commit or push.
- **Recovery cases.** All 54 product recovery cases (F00–F53) remain not executed.

## Inputs and custody (p00, p07)

- **Frozen source38.** Manifest `2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5` re-verified by hash; the whole manifest was not rescanned. The 10 touched files' source38 bytes and v1's 33 dependency files equal the manifest.
- **v1.** `review.json` is `1f69efb90f57f8d45905a4d398331e000bdde6bd28647d5859b0f3d7c29274b9` (root's recorded value). Its `work/edited` tree (1359 files) was copied as regular files: every copy has its own inode, `st_nlink == 1` and equal bytes. The v1 tree and review are unchanged at the end.
- **Root's assessment** (`probe-joins.py`, `probes.json`, `assessment.json`, attempt-1 files) is unchanged at the end. Root's first harness failure is theirs and was not touched.
- **Root's findings reproduced (p01).** Against the unchanged v1 model, `baseline`, `wrong-execution-plan` and `wrong-inventory-digest` all return `composed-analysis-termination-admitted`.

## 1. Attempt derivation binding to the Run's admitted execution plan

**Finding confirmed.** The v1 composition joined only `derivation.planId`, so an arbitrary `executionPlanId` was admitted. The v1 fixture used an invented `exec-plan2:e…` with `stageCount 1`.

**Owner facts** (p01, measured on actually closed Runs):
- The Run record has no `executionPlanId`. The Run's execution plan is `objects[run.evaluationSealId].executionPlanId`.
- `close_run` joins it to the proof bundle (`EVALUATOR_JOIN`) and to the Run's `planId` (`PLAN_JOIN`).
- Fixture plans have one stage, ordinal 0.
- `DerivationBinding` says one attempt owns exactly one execution plan. Workflows §1 records the attempt's derivation DAG in that binding.
- `stagesCompleted` is runtime progress: the native protocol increments it when a stage's Coverage arrives (`protocol3-transitions.v1.json` P3-24).

**Correction** (contract §7.3, §7.6; `admit_analysis_step_termination`):

| Join | Refusal |
|---|---|
| `derivation.executionPlanId` = the seal's `executionPlanId` | `RUN_TERMINATION_ATTEMPT_EXECUTION_PLAN_MISMATCH` |
| `derivation.stageCount` = the number of that plan's `stages` | `RUN_TERMINATION_ATTEMPT_STAGE_COUNT_MISMATCH` |
| `stagesCompleted ≤ stageCount`, and a present `firstFailedStage` is an `ordinal` of that plan | `RUN_TERMINATION_ATTEMPT_STAGE_PROGRESS_MISMATCH` |

The existing `planId` join and the receipt joins are preserved and ordered first.

**Stage semantics assessed; nothing invented.** No retained record re-derives `stagesCompleted` or `firstFailedStage`, and a scheduled stage is not a completed one. So the composition does **not** require `stagesCompleted = stageCount` and does not decide whether a completed attempt may carry `firstFailedStage`. Both stay with the host attempt owner (workflows §1). Only the bounds the retained plan decides are checked.

**Controls.** Every committed case now binds its Run's actual seal plan and stage count; the fixture assumes full progress as a host observation.

| Case | Outcome |
|---|---|
| `wrong-execution-plan-otherwise-admitted` (the same candidate is admitted with the actual plan in `work-budget-detail-on-d9-golden-run`) | `ATTEMPT_EXECUTION_PLAN_MISMATCH` |
| `stage-count-not-the-execution-plans` | `ATTEMPT_STAGE_COUNT_MISMATCH` |
| `stages-completed-beyond-stage-count` | `ATTEMPT_STAGE_PROGRESS_MISMATCH` |
| `first-failed-stage-outside-the-execution-plan` (ordinal 1023) | `ATTEMPT_STAGE_PROGRESS_MISMATCH` |
| `partial-stage-progress-is-not-invented-or-refused` | admitted |

## 2. Receipt inventory join

**Finding confirmed.** An arbitrary `inventoryDigest` (`f*64`) was admitted, because receipt schema admission does not relate the digest to the Run.

**Assessment: no existing invoked owner discharges it.**
- `identity-model.v3` `EvidenceStore.commit` *mints* the digest on the commit path, and `check-identity.py` controls that minting.
- Read-only recovery joins `inventoryDigest` only between receipt and association (`attempt-custody.schema.v1.json` `joins.toReceipt`).

None of these runs on the composition path, and none compares the receipt with the Run content composed. The identity contract defines `commit-inventory` as "the exact set of typed object identities and retained raw blob digests the commit published for that Run".

**Correction.** After the receipt `runId` and `executionId` joins, `receipt.inventoryDigest` must equal `M.commit_inventory(runId, objects, blobs)` over the composed Run content: `RUN_TERMINATION_RECEIPT_INVENTORY_MISMATCH`.
- The contract states that the composed `objects`/`blobs` are the Run's published retained content, not a wider shared store.
- `namespaceId`, `commitSequence`, `sealedAssurance` and `signerKeyId` stay with receipt admission and its signer/custody checks.
- §7.7 now says these joins catch accidental disagreement between the host's attempt, its receipt and the Run. They do not authenticate the receipt.

**Controls.** Every committed-case receipt is minted by the actual reference commit path: `EvidenceStore.prepare` with a trusted replay adapter over `evaluator_replay_model.v3.derive`, then `commit`. p01 measured that this receipt digest equals `commit_inventory` on two Runs.

| Case | Outcome |
|---|---|
| `receipt-minted-by-reference-commit-path` (a retried attempt) | admitted |
| `wrong-inventory-otherwise-admitted` (`f*64`) | `RECEIPT_INVENTORY_MISMATCH` |
| `receipt-inventory-missing-a-published-object` | `RECEIPT_INVENTORY_MISMATCH` |

## 3. Read-only association naming a bound carrier observed absent

**Finding confirmed.** An empty SQLite carrier dispatches `fresh-install`, and the v1 read-only map had no standing for it. That was the gap disclosed in v1.

**Selected route.** The existing **`unknown-custody`**: operational-failed / 4 / `HOST.IO_FAILURE` / `host-io`, detail omitted. It already exists in read-only §1 and is the S12 "unreadable ledger or carrier" row.
- **Why:** the association names this carrier, so its absence is lost, emptied or fallback custody. Step 1 already refuses to read an empty fallback database as absence, and the carrier stage now does the same.
- **Never** absence, `terminal-not-committed` or success; never created, initialized or migrated.
- No new D9 code, detail, class or F-case.

**Precedence** (read-only §1 rows 1–4; carrier-format §8.1; dispatch `phaseLaws`):
1. `binding-unusable` first.
2. carrierFormat 3 footprint and stability precedence unchanged; an interrupted fresh `{B}` stays `unavailable-busy`.
3. Unmigrated format 1/2 stays F46.
4. The absent carrier → `unknown-custody`, whatever generation the association or a surviving witness names. It is decided from object names; witness and anchor rows are not reported, and Step 4 does not gate it.

**Totality.** The carrier stage is now total: every `_s37_open` result except `carrierFormat3`, which continues to the SEAL join, has exactly one published read-only standing. A writer or maintenance fresh-install stays its separate existing owner.

**Edits.**
- **Dispatch JSON:** a `readOnlyRecovery.unknown-custody` route; `fresh-install → unknown-custody`; a reader law; a totality phase law; the standing note.
- **carrier-format:** a §8.1 row and a paragraph.
- **S12:** the unreadable-carrier row names the bound carrier observed absent and states `domainDetail` omitted.
- **Read-only doc:** precedence row 4, the totality statement and a Step 3 sentence.

**Controls** (real SQLite, the unchanged `_s37_open` owner dispatch):
- An empty in-memory carrier:
  - it is still `fresh-install` at a writer open;
  - associations at generations 1, 2 and 7 give `unknown-custody`;
  - a surviving witness naming another project, or the admitted project, does not displace it;
  - an association naming another carrier gives `binding-unusable` first;
  - nothing is created or written.
- A fallback database with only an unrelated table → `unknown-custody`.
- `mode=ro` open of a missing carrier file refuses and creates no file.
- An existing empty carrier file opened `mode=ro` → `unknown-custody`, with its bytes unchanged.
- An interrupted fresh `{B}` with an association keeps `incomplete-footprint`.
- An AST totality check over `_s37_open`'s result positions.
- Law and prose checks, plus the existing route loop for `unknown-custody`: schema-valid, D9 pair, exactly one S12 row, the read-only §1 row.

## Results

| Validator | v1 | v2 edited (`receipts/p04-edited.r2`) |
|---|---|---|
| semantic replay | 31/31 rows; 37 composition cases | **31/31 rows pass; 44 composition cases, 0 faults** |
| carrier (`check-integrated-carrier.v1.py`) | 384/0 | **406/0** |

**Discrimination** (p05, hybrid regular copies; each met its exact expectation):

| Variant | Effect |
|---|---|
| `v1-model` (v1 model under v2 goldens: root's finding) | only the composition row fails, exactly the 6 new join cases |
| `inventory-join-disabled` | exactly `wrong-inventory-otherwise-admitted`, `receipt-inventory-missing-a-published-object` |
| `execution-plan-join-disabled` | exactly `wrong-execution-plan-otherwise-admitted` |
| `stage-count-join-disabled` | exactly `stage-count-not-the-execution-plans` |
| `stage-progress-join-disabled` | exactly `stages-completed-beyond-stage-count`, `first-failed-stage-outside-the-execution-plan` |
| `v1-dispatch` | 391/9: exactly the 7 absent-carrier read-only scenarios, totality and law |
| `v1-prose` | 404/2: exactly the `unknown-custody` S12-row check and the absent-carrier prose check |

## Failed attempts preserved

- **`p04_owner_checks.edited` (exit 1).** Carrier 405/1. My totality check's AST walk took every string constant inside `_s37_open`'s return expressions, so the condition operand `'gj_seq_contiguous'` of `return 'carrierFormat2' if 'gj_seq_contiguous' in names else 'carrierFormat1'` counted as a dispatch result. This was a harness defect; law and map were right. `p06_fix_totality_extraction` now reads only result positions, and `p04_owner_checks.edited.r2` (exit 0) covers the final bytes.
- **Denied launches.** Two compound background shell loops that would have started the p05 variants were denied by the environment before running; no receipt exists. Each variant then ran individually through the receipt runner.

## Diffs and hash maps

- **Total, frozen source38 → v2:** `total-edits-vs-source38.diff` (sha256 `beaa92e4b9b6e86c43ca088a91f008aa58e54f40b4ba49834576836214cefb4a`, 1257 lines). The same 10 files as v1.
- **Incremental, v1 → v2:** `incremental-v1-to-v2.diff` (sha256 `870bc958db978852570cd3b25faedb8c854ad754931ce01047e86cd9d0c4c3d4`, 534 lines). 9 files; `workflows-and-surfaces.md` is unchanged from v1.

| File | source38 | v1 | v2 |
|---|---|---|---|
| `foundation/run-termination-contract.v1.md` | `7fdaae67ae6f4439e6e2de9b19946b188169474f9e32a6289cb671a81b4f3436` | `155fa57b66539056e866a9e08dc9a7d7daadde00f54f88a4d254593a6015252d` | `f9eb575219cd4815929166bb9e536d973639aab7250a3f993d5050f6f30d139c` |
| `foundation/run_termination_model.v1.py` | `2b9dd91782147182d55b50f52527641868ab01b1cc985109bddd1084bef7cf49` | `6196be9ba9cd07badeba42b85e7849153ae0c2b2a080a67dd0d3488b5c6ad101` | `cedf74a4ced223e94edece76564edc92e60514f6351bb6eb391566cb3f6533bb` |
| `foundation/run-termination-goldens.v1.json` | `9bdde8236ce24b299b36100325df4a6874bbba4e86d4abf308b653da457f4fcc` | `85ed0bf71071699f9f6264c3a0d764cb142f84b4e1f1209d654e82ad97ee8c17` | `2f205d1adc67985d81e75e8a8e7c2247302eaf64fc13cb44a4f858e5f98607c2` |
| `foundation/check-semantic-replay.v3.py` | `bc8a82e08bc3bebcc157c4e9adbf4f822c2d4ba5aeb323e8108679f346e03bb4` | `a18122933de03e3846f179bd65e8663d78105ab1001071a41e51e30e33c7c450` | `2bef052db5dacf5399822cbd44a6d241c6ff6369b6d308b613aedb02088fbabf` |
| `security/carrier-dispatch.v3.json` | `62b1958e7e2832bab77215078334b8821a252ed27c6e7a976de7d0ae79c82600` | `6d9eb28d4c13f9a88d480b16823339df592ec282b3dbacf8db91bdd91b84e2e1` | `f5c4ce7779f71bbb80c43a41de90f95c074cb83aaab2d47b1661e06e70886997` |
| `security/carrier-format.v3.md` | `10608c16c510a4eb4a65a01ffedae267c625e4d999ebc5946349659bc8f1be3e` | `42b118903f6e429202f62e2469b61ddccae33aa4ce999e262eb080b50afeb97d` | `2c3e465d90140228225790fec5eeac00c767d7f0ed06842be5e855fdb6145a7f` |
| `security/check-carrier-v3.py` | `4948301df3752c52e4eabae0b529063bbfceed905ba4395d5ff970b639838747` | `7e397699370270fc8f1204a91ca4552b04563970b0bd61a567df6af632968da2` | `834e337a18b1f6320463b3cd6d3132b7e809d5c32acc976c12a8f6238872b977` |
| `v2/architecture/commit-recovery-readonly.v3.md` | `3b32d24a3c6e71954bee620dc0add29f72aa35cfb643cac86a7d7d719238e85a` | `a6d0ce729cf33efa4410f9e7746e541969b730da2a93a832c0d7a4296456732f` | `7bcc8f8e23da91e87d36e7c1a1c913f05a634be058e4a4c5c0c73ac4faec1d80` |
| `v2/contracts/product-v1/security-and-lifecycle.md` | `9ca85de10f4f364b7dceb015799189796f12094fe506e1f172aa809c746ece32` | `60e67e7dc5b941fe1e0bfe00f9abfc1e5980b56563504ce516b1faa6666a7371` | `f580d0e6012ab4f9479f494031acf7f70fa18e10485e62ae486371aa1ec43e21` |
| `v2/contracts/product-v1/workflows-and-surfaces.md` | `857d6bbed265a51cf0df68cf072863f4eeb28726b6b1ed8c04272dc663f951ec` | `167c73bf17d3143b2080f12bb4a87b8e85994ddfbf71a71022621cafd14d3bc5` | `167c73bf17d3143b2080f12bb4a87b8e85994ddfbf71a71022621cafd14d3bc5` |

The first seven rows are under `docs/coop/design-corrections/`, the last three under `docs/`. Dependency hashes (25 files, all unchanged and untouched) are in `receipts/p07-summary.final.json`.

## Bindings awaiting root rebind (computed, not edited)

These are unchanged in kind from v1.
- **Before-hash pins.** Five source-pin ledgers pin all 10 touched source38 hashes: foundation `evaluator3-source-pins.v1`, foundation `source-pins.v1`, native `source-pins.v2`, security `source-pins.v1` and workflows `source-pins.v1`. `implementation-coverage.v1.json`, `implementation-normative-inputs.v6.json` and `implementation-planning-sources.v1.json` also pin 6 of them: contract, dispatch, carrier-format, read-only, security-and-lifecycle and workflows-and-surfaces.
- **Planning section selectors:**
  - `security-and-lifecycle:12` (S12 text; lines unchanged);
  - `workflows-and-surfaces:10` (text; 1135–1189 → 1135–1193);
  - `workflows-and-surfaces:11`–`13` (+4 line shift).
- **Shared selectors for root's merge:**
  - contract §6 goldens row, §7.2, §7.3, §7.6, §7.7 and §8;
  - S12 unreadable-carrier row and F46 row;
  - read-only §1 precedence and §3 Step 3 sentence;
  - `carrier-dispatch.v3.json` `readDispatch.readerLaws`, `publicProjectionByPhase.phaseLaws`, `readOnlyRecovery.unknown-custody` and `readOnlyStandingOfDispatchResult`.
  - The workflows §9 sentence is unchanged from v1.

## Limits

- **Reference evidence only.** In-memory and temporary-file SQLite; synthetic native-admitted Runs; F00–F53 not executed.
- **Fixture plans have one stage.** Stage-count and ordinal joins are exercised only there.
- **Stage progress** is bounded, not derived. Whether a completed verdict attempt may carry `firstFailedStage` is left to the host attempt owner.
- **The inventory join** assumes the composed `objects`/`blobs` are the Run's published content. A host composing from a wider shared store would be refused, which fails closed. Receipt authenticity, namespace, sequence, signer and assurance are not checked here.
- **Trusted host.** All three corrections fix accidental cross-record disagreement within the trusted-host TCB. No adversarial-host defence is claimed.
- **Only the two affected focused validators and their seven discrimination variants** were run. No global six groups, planning checker or whole-manifest rescan.
- All foreground and background commands have completed.
