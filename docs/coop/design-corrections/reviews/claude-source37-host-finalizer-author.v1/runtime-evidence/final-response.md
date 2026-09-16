I closed S37-01 in my own copy of source37: a new host finalizer contract now alone decides the ordered `reasonCodes`, the cause mapping and `coverageId` for an indeterminate evaluator3 analysis Run. It adds no code, class, exit, schema field or identity. This is coauthor work only, not acceptance, and nothing was committed, pushed, frozen or activated. Frozen37 and a second clean copy were both still byte-exact after all my check runs.

**The law** (`foundation/run-termination-contract.v1.md`, reference model `run_termination_model.v1.py`):
- **Class precedence is unchanged.** Faults, rejections, interruption and durability are still decided first, from host observations. Then the sealed verdict gives success, policy-failed or indeterminate. A native stage never changes the Run's class.
- **Inputs are sealed facts only.** The Run must pass `close_run` with complete replay. Discovery order, stage scheduling and stage terminals the host saw but no record kept are not inputs.
- **Conditions.** All `executionDeficiencies`, plus, for each indeterminate gating rule, its rule-level records and the deficiencies that actually blocked each indeterminate root. The blocking set is recomputed from the retained witness tree. An indeterminate rule with nothing to explain it is treated as a host invariant violation.
- **Cause mapping and order.**
  - A `DeficiencyV2` cause is ranked by native §10 precedence and follows the native route.
  - `work-budget-exhausted` must map to `budget-exhausted`, which replaces "may reuse"; D9's `analysis-budget-exhausted` golden is exactly this case.
  - Every other registered cause ranks last and maps to `VERDICT.INDETERMINATE`.
  - Distinct D9 deficiencies are ordered by their best rank, so the order is total and discovery order cannot change it.
- **Stage/entry disagreement.** When a Coverage record's `stageTerminal` is `budget-exhausted` or `unavailable`, it adds that stage's cause without rewriting the entry. So `coverageId` can name a record whose own `entry.deficiency` differs from `reasonCodes[0]`; the contract says so explicitly.
- **`coverageId`.** The least record that declares the primary cause, otherwise the least record whose stage terminal implies it, otherwise omitted.

**Checks:**
- **Goldens:** 8 new rows in the maintained `check-semantic-replay.v3.py`, all built from Runs that actually pass `close_run`. The checker passes 26/26 (frozen37: 18/18). The rows cover the five cases you asked for, plus a stage `unavailable` variant and a route-drift check.
  - The reviewer's A, B and C cases are reproduced and resolved.
  - Every refused alternative is a schema-valid `StepTermination`, refused because it isn't the derived termination.
  - Over 16 orders the derivation gives one termination, while D9's reducer used as written gives two different primaries.
- **The checks catch wrong laws.** The reference model passes. Five swapped-in wrong versions each fail at least two golden rows: least deficient Coverage anywhere, stage terminals ignored, work budget not mapped, first-discovered primary, carrier always omitted.
- **No regressions against frozen37 or the clean copy:**
  - identity 1596/0, integration 412, query projection 138, `check_workflows` 1803/1803 and native cases 377/377 all match;
  - workflow projection passes 459 and differs only in its recorded hash of the edited projection contract;
  - the other checkers that load the fixture give identical output, except `check-execution-inputs`, where only file-path strings differ.

**Edits:**
- **New files:** the contract, the model and `run-termination-goldens.v1.json`.
- **Existing files:**
  - `check-semantic-replay.v3.py`: +94.
  - The semantic fixture: +19/−5, two new options whose defaults leave existing output unchanged.
  - Native §10: +5/−2, a pointer replacing its "does not define" sentence.
  - workflows-and-surfaces §9: one added paragraph, +11/−0.
  - The work-budget row in the projection contract: +1/−1.
- No root-owned file was edited; the new checker rows only read `query_projection_model.v3.py` for schema validation.

**For root:**
- 25 stale pin rows (5 in each of the five ledgers), plus the frozen37 hashes in `implementation-normative-inputs.v5` (2), `planning-sources` (4) and `implementation-coverage` (2); the older v4/v3 inputs hold 1 each.
- Pin additions for the three new files.
- I did not run the pin-gated launchers, the native checker's `main` (it writes into the tree), the six groups or the planning checks.

**Limits:**
- No retained golden mixes several `COVERAGE.*` causes from different owners (the reviewer's three-owner case). That order rests on the contract's table and the route-drift check only.
- The contract, model and goldens have one author, with no blind reconstruction.
- The goldens are synthetic Runs, not compiler or provider qualification.
- The TCB-SCOPE-01 assumption (13 dependent accounts), 32 product gates and 54 recovery cases remain unperformed.

Everything is in `/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1`; per-file diffs, before/after images and all 36 command receipts (including failed attempts) are alongside:
- review.md
- review.json (SHA-256 `b1374449…a492`)
- proposed-edits.diff (SHA-256 `19298c16…82ae`)
- after-manifest.json
