All five bounded findings are addressed and every check is green. Final state:

## What changed in v2 — 6 files, no new file beyond v1's nine

**1. DRAFT-P1 — `items[0]` masking (root was right).** `_outcome_from_items` now takes the first source *actually carrying* a typed pair. Evidence at three levels:
- root's own probe inputs replayed: `[null,null]` → `["budget-exhausted",null]`, with sources, refs and causes all byte-unchanged
- an **admitted fixture** with the discriminating shape (untyped `file` account owed *before* a typed `package` account, in the authored matrix order)
- the same shape through **`M.close_run`**: `indeterminate`, and *both* originating Coverage refs reach proof

Measured extent: 4 of 11 enumerated source shapes change their row pair; **every state, every `inputRefs` list and every `nativeCauses` list is unchanged** — the conservative completeness law is untouched.

**2. DRAFT-P2 — cross-source order published,** after reading the real authorities rather than guessing. Two things worth your attention: the account leg is the **authored** matrix `relations` array (`syntax` is `declares, literal, control-flow` — *not* lexical, so nothing may re-sort it), and the host's `nativeCoverageAccounts` order is `sequence`, which the validator does not enforce and admission does not read. No deterministic behaviour changed.

**3. Checker reporting.** Every control declares a `controlStanding` (60 admission / 5 closed-run / 7 helper-unit / 3 schema-unit); non-admission controls report **null**, not an invented complete cell. `full_run_case` returns real rows — the three indeterminate Runs now report cell state `partial`. Rather than assert that those admission columns are the Run's, each case **tests** it: `bridgedCausesEqualProof` bridges them with §9.6 step 3 and requires equality with the proof's causes. It holds in all five.

**4. Independence claim corrected** to reference self-consistency, since the builder calls `M.derived_applicability` / `M._summarize_coverage_records` / `M.derive_outcome`.

**5. Control renamed** to `optional-unsupported-cell-owes-no-required-cell-row`, with the selected-U/synthetic-Coverage qualification recorded on the case row.

## The candidate path you asked me to assess narrowly

It **is** a reachable contradiction, on actual evidence: `AvailableProgramBindingV1` has no `deficiency` property at all, so the candidate branch manufactured `provider-unavailable` every time; an optional candidate cell with no envelope **ADMITs** with that invented pair on empty refs. Required still refuses, as you said. Minimal fix: `_declared_binding_carrier` (no default) — state and refs unchanged, typed envelope pairs preserved. **`_binding_carrier` itself is untouched**; I confirmed your guards at `enumeration_model.v1.py:679-683` and `:752-754` by reading them, and the two binding control shapes keep their real typed pairs.

F4 cross-owner qualification is now written into §9.6 itself. The optional-inventory/same-kind interaction is restated as existing conservative behaviour, unchanged.

**Checks:** 75 cases, 0 mismatches, 0 oracle failures; 9 focused current checks all exit 0 (the 12 untouched ones named and skipped, per your instruction). Whole tree: 12 898 files, 9 changed, 0 added, 0 removed. Both pin ledgers unedited. v1 runtime re-hashed and intact. No acceptance claimed.
