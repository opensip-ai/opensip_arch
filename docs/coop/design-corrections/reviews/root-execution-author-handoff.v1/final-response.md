Bounded corrective source and controls are complete. Summary:

## What I changed

**9 files** in the successor copy (whole-tree hash comparison against frozen32: 12 898 files, **9 changed, 0 added, 0 removed**). Frozen32 untouched; no commit, no push, no product implementation.

| Decision | Implementation |
|---|---|
| **D1** account source-U | `want_u = binding universe` for every applicability; published in contract §5 as an explicit **external join** and on the schema as `x-opensip-external-joins` — the schema states that the comparand is another document rather than pretending to compare it. `targetUniverse` carries an explicit non-constraint, controlled by an admitting cross-universe case. |
| **D2** first-match precedence | VCS-none → matrix → **unselected** → null-U → supported, in code (`APPLICABILITY_PRECEDENCE`), contract table, and `x-opensip-applicability-precedence`, with a control asserting all three agree. |
| **D3** request vs enumerator | `enumeration-contract.v1.md` §1 clarification: `enumerator.status` is the *provider binding*; "answered by disclosure" is about the cell's answer and forces no provider. |
| **D4** unsupported Coverage | Contract §5 + a native-chapter paragraph: retained in view/selectedRefs, account names none of it, `derivedAccounts` + `requiredCellDeficiencies` carry the matrix pair (not "only the token"), complete outcome ≠ supported. |
| **D5** no fabricated carrier | `_primary_source_pair` replaces `or "provider-unavailable"`; per-record rows stop borrowing a sibling's carrier; composition §9.6's table — which literally specified the fabrication in two rows — corrected with it. |

## Evidence

- **71 checker cases** (was 52), 0 mismatches, 0 oracle failures.
- **21/21** current reference checks exit 0 (16 evaluator3 jobs + 5 reference children).
- **4 controls run as full retained Runs through actual `M.close_run`**: census and empty-partition paths now bridge `required-cell-unsatisfied` (was the fabricated `provider-unavailable`), the census one retaining its originating Coverage ref; required-unsupported bridges the matrix pair; optional-unselected + optional-unsupported close at `pass`.
- **Measured before/after delta**, not asserted: exactly 10 of 72 applicability combinations move (all lawful, all `unavailable-null-universe → unavailable-unselected`); 15 existing fixture caller shapes byte-identical.

## Three things worth your attention

1. **D1 has no reachable behavioural effect.** The replaced expression already yielded the binding U wherever one existed. It is a publication plus a uniformity fix — confirm that was the intent.
2. **`_binding_carrier` still defaults to `provider-unavailable`** for a binding declaring none. Left alone (binding-owner carrier, which D5 lists as *preserve*), flagged.
3. **`evaluator_input_model.v3.py:136-144`**: an optional unselected cell's own unavailable inventory can make an unrelated required rule's enumeration incomplete. Outside scope, not changed, raised.

**Not re-run:** blind19's five exports. They should still refuse on F1/F2/F3 with F4 gone, but that is reasoning from the corrected code, not a replay — it needs your export transport. I claim no admission for any of them.

Both pin ledgers are **stale for exactly those 9 files and unchanged**; the rebinding used to execute the suites is labelled `DISPOSABLE-` and lives only in this runtime. No acceptance is claimed.
