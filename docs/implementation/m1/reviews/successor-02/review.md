# Correction review: design-lock v2 (m1-successor-subject-02)

**Verdict: ACCEPT-UNIT.** This approves the developer design-lock v2 unit only. It is not full M1, product qualification or release approval.

- Subject manifest SHA-256: `3aeddcf6c1a42def68ae74106e10c66ad5cb09ab29f628546a70738bbd7cb368`, verified before and after (13/13 rows, no extra files, no `__pycache__`).
- This is a nonblind review: it checks the correction for my own finding SUCC-R1-01 from review-01.

## Correction checked

- **Scope of change.** Only `tools/tests/test_design_binding.py` changed, and only by additions. `verify_design.py` and `design-lock.json` are byte-identical to subject01.
- **What was added.** `rebound()`, `refuse_with()` and four isolated tests were added to `InventorySuccessorTests`. The eight existing successor tests are unchanged, for 21 tests in total.
  - `rebound()` copies the full pin into `review.successorRecord` and `assent.actualClaudeReview`. The added `bytes` field is ignored by the verifier.
  - The parent-selection test restores the original `base_inputs`, so only the "selected base input" guard can refuse.
  - Each regex pattern matches only its intended diagnostic.
- **Tests.** All 21 tests pass.
- **Real verification.** The real command against the explicit arch checkout passes before and after: 46 inputs, v3 `63027fb6…`, 4 added files, `productQualification: false`. The canonical-04 lock1 still passes.

## Mutation confirmation

| Test variant | Mutants killed (of 35) | Survivors |
|---|---|---|
| Live subject02 tests | 28 | M02 plus N28–N32, N34 |
| Rebinding removed | 28 | same |
| Regex assertions downgraded to generic `DesignError` | 28 | same |
| Both removed | 18 | 17, back toward the pre-fix state |

- **Original 26 mutants:** 25 are killed, matching root's run. The sole survivor, M02, is equivalent.
- **Redundancy:** rebinding and message assertions each keep the full kill set on their own.

**SUCC-R1-01 is closed.**

## Advisories

- **Carried forward:** SUCC-A1-01 through SUCC-A1-06 remain unchanged and nonblocking, and are not claimed fixed. The reviewed real rows are strictly JSON-equal.
- **New, SUCC-A2-01 (nonblocking):** I added nine new mutants. Six survive:
  - **N34** (parent selected by path only) is equivalent. On the real lock, a same-path pin with a different sha or bytes fails the pin digest/length checks.
  - **N28/N29** (parent joins ignore bytes) could only admit inconsistent size metadata, because SHA-256 still binds the content.
  - **N30–N32** (truthy root assent, missing or falsy review `requiredFindings`, truthy record flag) are strictness regressions the tests would miss. The identical verifier refuses those inputs today, as shown by the review-01 probes. Three one-line isolated cases would lock this in.

## Limitations

- Rust and crypto checks were not rerun (bytes unchanged). The 59 verifier probes from review-01 apply because the verifier bytes are identical.
- Checks ran only on macOS with Python 3.14.6. The mutation set is my own selection and is not exhaustive.
- The arch checkout contains concurrent metadata-v1 work. I make no claim that any architecture directory is unchanged; only the pinned evidence was verified, through the real command.
- I did not read the pre-existing launcher and event files in the review directory.

Logs and scripts are in `probes/`.
