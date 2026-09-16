# S37-01 correction — one host owner for whole-Run indeterminate reasons and `coverageId`

**Standing: coauthor correction only.** Origin `823bf66b-e92a-4789-ab81-63a1a9dc371d`.

This is **not**:
- independent acceptance or blind reconstruction;
- successor, application or readiness agreement;
- product qualification;
- a commit, push, freeze or activation.

**Custody.**
- **Read-only:** frozen37 and manifest `245ef613…6680`. I edited only my verified copy (`source/`).
- **Verified:** the copy was exact (12,900 files, 736,891,310 bytes). After all baseline runs, frozen37 and a second pristine copy both re-verified exact.
- **Records:** `review.json` (SHA-256 `b13744491bbb15847e01997d3944d5a4c747bad2d097c98e7dcf9514fcd5a492`) is built from 36 finished receipts under `receipts/`, including failed attempts. Before-images are in `before/`, after-images and per-file diffs in `after/` and `diffs/`, and the combined diff in `proposed-edits.diff` (SHA-256 `19298c1699f5bc6567465c88411d8d8873d34ceb33be8c2711e3937e3d4c82ae`).

## 1. The finding

**It is real.**
- Native §10 disclaimed ordering, and no other owner fixed it.
- D9's reducer takes the primary as `deficiencies[0]` in host input order.
- The proof keeps deficiencies as canonical sets, and `StepTermination.coverageId` has no selection law.

So one sealed Run could lawfully terminate several ways:
- **A:** a different or absent `coverageId`;
- **B:** a stage-implied primary whose named record declares another member;
- **C:** a different primary depending on discovery order.

## 2. The correction

**New owner:** `foundation/run-termination-contract.v1.md`. Its reference derivation is `run_termination_model.v1.py`. workflows-and-surfaces §9 and native §10 now point to it.

- **Scope.**
  - Class precedence is unchanged: fault, then rejection, then interruption, durability and delivery, all decided first from trusted host observations.
  - The sealed verdict then decides `success`, `policy-failed` or `indeterminate`.
  - A native stage never reclassifies the Run.
- **Inputs are sealed facts only.**
  - The Run must be admitted by `close_run` with complete replay. Its proof, witnesses, Plan policy and originating `coverage2` records are the inputs.
  - Discovery order, stage scheduling and host-seen but unretained stage terminals are not inputs.
- **Population.** All `proof.executionDeficiencies`, plus, for each sealed-`indeterminate` gating rule:
  - its rule-level records: enumeration, required import and work budget;
  - the verdict-blocking deficiencies of each indeterminate root, recomputed from the retained witness tree under composition §3/§5.
  - An empty population for an indeterminate rule or Run is a host invariant violation.
- **Cause bridge, total over the evaluator registry.**
  - A `DeficiencyV2` cause ranks at its native §10 precedence index and follows the native route.
  - `work-budget-exhausted` ranks as `budget-exhausted` and routes there. This replaces "may reuse" with a MUST, grounded in D9's `analysis-budget-exhausted` golden.
  - Every other registered cause ranks 9 and routes to `verdict-indeterminate`. That includes `required-cell-unsatisfied`, the enumeration, import and correspondence causes, and native diagnostics such as `coverage-unknown`. No cause is promoted by name resemblance.
- **Stage terminals.** An originating `coverage2` with `stageTerminal` `budget-exhausted` or `unavailable` adds a stage-implied `budget-exhausted` or `provider-unavailable` condition. That record is its stage carrier. The entry is never rewritten.
- **Total order.** Distinct D9 deficiencies are ordered by least rank; each rank maps to exactly one D9 deficiency, so the order is total. `reasonCodes` come from D9 `codeMaps`. Fed this sequence, D9's reducer agrees for every discovery order.
- **`coverageId`.** Among conditions at the primary rank:
  1. the least declared carrier (`entry.deficiency` equals the primary cause);
  2. else the least stage carrier;
  3. else omitted. This covers evaluator-only causes, work budget, and requirement-relative causes without an entry carrier.
- **Unchanged:** the D9 v1.14 artifact, the common schemas, registered payload schema bytes, identities, the public code vocabulary, the native `run_termination` helper, pin ledgers, planning layers and generated reports.

## 3. Changed files

| File | frozen37 SHA-256 | after SHA-256 | lines |
|---|---|---|---|
| `foundation/run-termination-contract.v1.md` | new | `93850961…5e025a26` | +164 |
| `foundation/run_termination_model.v1.py` | new | `e8dd6025…18e17e6` | +260 |
| `foundation/run-termination-goldens.v1.json` | new | `ed5c3ede…31ac7dd025` | +165 |
| `foundation/check-semantic-replay.v3.py` | `e1ff5ee2…ca8aca` | `4007f159…87580f7e` | +94/−0 |
| `foundation/evaluator_semantic_fixture.v3.py` | `87aed741…a76ae5e` | `2f51675e…4d57b72c` | +19/−5 |
| `v2/contracts/product-v1/native-evidence.md` | `ffa5b569…567bc33` | `cfe69627…ce54869` | +5/−2 (§10 pointer) |
| `v2/contracts/product-v1/workflows-and-surfaces.md` | `b2530a31…801615d0` | `22464fd3…d20d88ba4` | +11/−0 (§9 paragraph) |
| `workflows/workflow-projection-contract.v3.md` | `e890bcda…ccb19a` | `1f8128bb…c54bba13` | +1/−1 (row 138) |

Full hashes are in `after-manifest.json`. Nothing changed outside these targets.

**The fixture gained two knobs**, `budget_limit` and `references_stage_terminals`. Defaults are byte-preserving. Coverage stays minted by the native owner's `completeness_from_stage` and admission, then by `close_run`.

## 4. Retained goldens over actually closed Runs

These are integrated into the maintained `check-semantic-replay.v3.py`, which runs in the evaluator3 group. On my copy it passes 26/26; frozen37 passes 18/18. The 8 new rows:

| Golden | Derived termination | Refused schema-valid alternatives |
|---|---|---|
| same Run, two Coverage carriers (reviewer A, run `f9b48563…`) | `VERDICT.INDETERMINATE`, coverageId `11659545…` | other carrier; omitted |
| stage/entry disagreement (reviewer B) | `COVERAGE.BUDGET_EXHAUSTED`, `VERDICT.INDETERMINATE`; coverageId `1691d700…` (entry stays `resolution-incomplete`, stage `budget-exhausted`, `partial`) | least deficient record; entry-only reading; generic reason first; omitted |
| stage `unavailable` | `COVERAGE.PROVIDER_UNAVAILABLE`, `VERDICT.INDETERMINATE`; coverageId `fa6bea5f…` | least deficient record; entry-only reading |
| permuted discovery (reviewer C) | 16 orders give 1 derived termination; the raw D9 reducer gives 2 primaries | — |
| evaluator-only cause (`required-cell-unsatisfied`) | `VERDICT.INDETERMINATE`, no coverageId | `COVERAGE.REQUIRED_RELATION_MISSING` |
| no-Coverage primary over deficient Coverage (work budget) | `COVERAGE.BUDGET_EXHAUSTED`, `VERDICT.INDETERMINATE`, no coverageId | a deficient record named; work budget not reused; generic reason first |
| work budget equals the D9 `analysis-budget-exhausted` golden | `COVERAGE.BUDGET_EXHAUSTED`, no coverageId | `VERDICT.INDETERMINATE` |

Route drift is empty. Every alternative is a schema-valid `StepTermination` and is refused by derivation, not by shape.

## 5. Does it discriminate, and did anything regress?

**Discrimination (`p2-termination-mutants`).** The unchanged checker, goldens and Runs were run with the reference model and with five mutated laws. The reference passes. Every mutant fails at least two golden rows:
- least deficient Coverage anywhere;
- stage terminals ignored;
- work budget not reused;
- discovery-order primary;
- carrier always omitted.

**Regression checks.** Frozen37 or pristine baselines ran under the same interpreter.

| Check | Edited copy | Baseline |
|---|---|---|
| `check-identity.py` (reads native-evidence.md) | 1596/0 | 1596/0, identical stdout |
| `check-integration.py` | 412 | 412, identical stdout |
| `check-query-projection.v3.py` (imports the semantic replay checker) | 138 | 138, identical stdout |
| `check-workflow-projection.v3.py` | 459 passed | 459; only the recorded hash of the edited projection contract differs |
| `check_workflows.v1.py` (external report) | 1803/1803 | identical stdout |
| execution replay, candidate replay, provider attribution (fixture consumers) | pass | identical stdout |
| `check-execution-inputs.v1.py` | pass | only the owned-hash path strings differ |
| native cases via `run_case` | 377/377 | 377/377 |

## 6. For root

- **Stale frozen37 hashes.**
  - 25 pin rows: 5 per ledger, in `foundation/evaluator3-source-pins.v1.json`, `foundation/source-pins.v1.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json` and `workflows/source-pins.v1.json`.
  - Planning layers: `implementation-normative-inputs.v5.json` (2), `implementation-planning-sources.v1.json` (4) and `implementation-coverage.v1.json` (2).
  - Older `implementation-normative-inputs.v4/v3.json` (1 each).
  - Counts are in `review.json#/forRoot`.
- **Pin additions:** the three new foundation files.
- **workflows-and-surfaces.md delta:** exactly one §9 paragraph, +11/−0, bytes in `diffs/`.
- **Root-owned files:** none edited. The new checker rows only read `workflows/query_projection_model.v3.py` for `StepTermination` validation.
- **Not run by me:**
  - the pin-gated launchers (`run-evaluator3-checks.py`, workflows `run-reference-checks.py`);
  - the native checker `main` (it writes into the tree);
  - the six integrated groups and the planning checks.
- **Optional follow-ups:**
  - a root schema successor could cite this owner in the `StepTermination.coverageId` and `D9Deficiency` descriptions;
  - a D9 successor could restate the pre-reduction order.

## 7. Limits

- **Evidence strength:** the Runs are synthetic native-admitted graphs, not compiler or provider qualification.
- **No mixed-owner golden:** no retained Run combines several `COVERAGE.*` causes from different owners, which is the reviewer's three-owner mix. That order rests on the §4 table and route drift, not on a golden.
- **Same author:** contract, derivation and goldens share one author; there is no blind reconstruction.
- **By design:** a host-observed stage terminal that no retained record carries contributes nothing. The comparison step's `d9Deficiency` stays with its own owner.
- **Carried:** one TCB-SCOPE-01 assumption with 13 dependent accounts; 32 product gates and 54 planned recovery cases remain unperformed. Nothing is granted here.
