Grok review: X3d-0, the work ledger's settlement reserve (law X3d r6 items 8 and 13), with inventory v112 (parent v110). Claude Opus 5.5 leads, and you are the single reviewer. Make no repository edits, commits or pushes, and do not delegate. Write only under /tmp/opensip-implementation/reviews/grok-settlement-reserve-x3d0-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git read-only, and only against the worktree below. Do not touch the real home.

**Law.** `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, r6, accepted at arch 21a7eaba7:
- item 8's "r6: the settlement reserve (lead decision)", in particular "What the platform provides (unit X3d-0)";
- item 13's X3d-0 unit and its tests;
- the r6 forbidden substitutes.

Read it together with:
- `journal-x3b/PROPOSAL.md` r10: item 5's r10 note under "A post-failure allowance", item 9's end-path bullet, and its forbidden substitutes;
- your joint review `reviews/grok-journal-x3b-r10-commit-session-x3d-r6/REVIEW.md`, which restates the exact semantics ("The latch holds outside `settle`" lists the four points X3d-0 implements).

X3d-1 (security) is the next unit and is not built. It owns:
- the end-path step and wrapper type;
- the exact cost;
- the forfeit;
- `finish`'s single `settle`;
- the source pin admitting exactly one production caller for each method.

The platform `WorkLedger` at 9d51f33 is byte-identical to the 6dd7363 file the law cites.

## Subject

Pins are in hashes.txt.

**Product.** The worktree is `/Users/sb/code/opensip-ai/opensip-x3d0`, detached at 9d51f33 (main: X2d integrated, inventory v110 selected).
- Save `git -C <worktree> diff` as product.diff and report its sha256. The new file is intent-to-add.
- Lead's value: `9c8e18c83502df6cf38dd26ef463940210af86ac02311d622b77e5484e82a3a1`, 30721 bytes. It covers 3 files, with 672 insertions and 9 deletions.
- Files: `crates/platform/src/work_ledger.rs`, `crates/platform/src/lib.rs` and the new `crates/platform/tests/settlement_reserve_tests.rs`.

**Arch.** These files are untracked in arch until acceptance:
- `repository-file-inventory.v112.json`;
- `settlement-reserve-x3d0-inventory-v112-subject.json`;
- `settlement-reserve-x3d0-inventory-v112/`.

The parent is `repository-file-inventory.v110.json`: 364396 bytes, sha256 `4d11a9d9578efa4dc0f6f963ff1d7a6cdc60c571087fadde8faed3438ecad6bc`, selected by the lock at 9d51f33. v106, v108 and v111 are other units' candidate numbers and are not part of this subject.

## What it does

### `WorkLedger` gains one private field

`settlement` is a private enum with four states: `Untaken`, `Reserved(issue)`, `Active { latched }` and `Spent`. It starts `Untaken` in both `new` and `with_limits`.

### `reserve_settlement(&mut self, cost) -> Result<SettlementReserve, BudgetFailure>`

It is on `WorkLedger` only. `WorkScope` and `ReservedPostchecks` have no such method.
- **Not `Untaken`.** Refused `Closed`, and it sets `failed`. That covers a second reservation, whether the first is outstanding or already spent.
- **Ledger failed.** Refused `Closed`.
- **Otherwise.** It draws a process-wide issue number from a checked `AtomicU64`; exhaustion refuses `Arithmetic` and latches. It then charges `cost` through the existing `charge`, which refuses `Objects`, `Edges`, `Bytes` or `Arithmetic`, takes nothing and latches, exactly as any charge does. On success the cost is in `used` at once, the state becomes `Reserved(issue)`, and the reserve is returned.

No `BudgetFailure` variant is added.

### `SettlementReserve { issuer: u64, allowance: Cost }`

Its fields are private. It has no derives and no impls, so it is not `Clone`, `Copy`, `Default`, `Debug` or serializable (the platform has no serde). `reserve_settlement` is its only constructor. It is re-exported from `opensip_platform` beside `WorkLedger`, `WorkScope` and `ReservedPostchecks`.

### `settle(&mut self, reserve, action) -> Result<T, Failure<E>>`

It consumes the reserve.
- **A foreign reserve.** If the state is not `Reserved(reserve.issuer)`, `settle` sets `failed` and returns `Closed` before `action` runs. That covers another instance's reserve, and a ledger that is `Untaken` or `Spent`.
- **Otherwise:**
  1. A `Settling` drop guard saves `prepaid` and installs `prepaid = Some(allowance)`. This is 467's existing credit slot.
  2. The state is set to `Active { latched: false }`.
  3. `action` runs through the ordinary `scope`.
  4. However `settle` ends (`Ok`, `Err` or unwind), the guard restores the saved credit (`None` at the owner) and sets the state to `Spent`.

### The only changes to existing paths

- **Scope admission.** `WorkLedger::scope` and `ReservedPostchecks::scope` admit and complete against `closed()`. That is the settlement's latch while `Active`, and `failed` otherwise.
- **Latching.** `LedgerScope` and `ReservedScope` drop through `latch()`. It sets `failed` and, while `Active`, the settlement's latch.

The state is `Active` only inside `settle`, so outside it `closed() == failed` and `latch()` only sets `failed`. Every existing path is byte-for-byte equivalent there.

### Consequences

- **Inside `settle`,** every charge, including nested `run`, `retained_record`, `effect`, `ReservedPostchecks` and `prepaid`, draws from the allowance through the existing prepaid mechanism. `used` does not move.
- **An overrun** is `ReservedPostcheck` before the work it covers.
- **Any `Err`, swallowed failure or unwind** latches both. Later steps in the same `settle` are refused `Closed`: there is no `CLN` after a failed `REV`.
- **A successful settlement** on an open ledger leaves it open.
- **Unused allowance** is never refunded.

## Judgment calls

1. **Instance binding.** A reserve carries an issue number drawn from a process-wide checked `AtomicU64` at reservation, and the ledger records it in `Reserved(issue)`. Numbers are never reused, and exhaustion refuses `Arithmetic` before charging. Rejected alternatives:
   - **Pointer identity:** a ledger can move.
   - **A lifetime-bound reserve:** it could not move into X3d-1's `StoppedSession` while the ledger is in use.
   - **An id drawn for every ledger at construction:** that changes every ledger's state, while the lazy draw touches only ledgers that reserve.
2. **Return type.** `reserve_settlement` returns `Result<_, BudgetFailure>`, not `Failure<E>`. It runs no operation, so there is no `E`, and the law allows only budget failures.
3. **What a foreign reserve latches.** It latches the instance it was offered to (the law's "and latches"). If that instance holds its own outstanding reserve, that reserve stays spendable, because a settlement is admitted after the latch by design. The tests pin both cases. The issuer's reserve is consumed by the move. Nothing else changes on the issuer, which cannot be reached from the refused call.
4. **A second reservation.** It is refused `Closed` and latches, while a first reserve is outstanding or after it was spent. An outstanding first reserve stays spendable, for the same reason as call 3. A refusal on a closed ledger or over the limits leaves the state `Untaken`, but the latch already refuses every later reservation `Closed`.
5. **A settlement that succeeds on an open ledger leaves it open.** The law latches only on `Err`, overrun or unwind. The reserve is then `Spent`, and no second one can be taken.
6. **`is_failed()` keeps its meaning.** On both `WorkLedger` and `WorkScope`, it still reports the ledger's permanent `failed` flag, including inside `settle`. The law moves scope admission to the settlement's latch, but `is_failed` is a report, not a scope check. Changing it would alter a public answer outside the law. No journal append-path code reads `is_failed` at 9d51f33. X3d-1's end path must not gate on it inside `settle`.
7. **The allowance reuses the `prepaid` credit slot.** So "exactly as `prepaid` draws today" holds by construction, not by a parallel mechanism.
8. **The source pin is on names, not on `settle`.** The zero-callers pin, in the new test file, walks every `.rs` file under `crates/` and `apps/`, except the `tests/`, `target` and `node_modules` directories. It requires that no file except work_ledger.rs and lib.rs names `reserve_settlement` or `SettlementReserve`, and that lib.rs names `SettlementReserve` exactly once (the re-export). It does not search for `.settle(`, because ordinary_writer.rs already has an unrelated private `settle` on the write gate. A `WorkLedger::settle` call needs a `SettlementReserve`, which only `reserve_settlement` constructs, so the pin excludes both methods.
   - **What X3d-1 does with it.** X3d-1 replaces this pin with its one-caller-each pin. The API supports that pin: both methods live only on the owner's `WorkLedger`, the reserve is a distinct type, and its only constructor is a distinctly named method.
   - **Is the law content?** I read the law as allowing an interim zero-caller pin. Item 13 assigns the one-caller pin to X3d-1, and a zero-caller pin before X3d-1 is the same property with zero admitted callers.
9. **No `Debug`, `PartialEq` or `#[must_use]`.** None is required. A capability token has nothing to compare, and the law allows dropping a reserve unspent ("dropped unspent. It is never refunded"). A zero-cost reserve is admitted, because the law sets no minimum.
10. **Inventory.** Law item 13 says X3d-0 "comes with an inventory successor for the platform crate". The precedent (460, 461a and 464) is that a unit adding no file owes no successor while every changed description stays true. Item 13's public-API tests go in a new integration test file beside `work_ledger_tests.rs`, so v112 adds exactly that row.
    - **work_ledger.rs's description stays true:** "Non-authority bounded ... accounting ... with permanent failure, unwind closure and precharged effect/postcheck reservations". `failed` is never cleared, every call outside `settle` still refuses, and the settlement is a precharged reservation. That description never named 467's `prepaid` either.
    - **lib.rs's description stays true:** "Expose the intentionally public API".
    - **Rejected:** a v112 with no row change, which would carry nothing. Also rejected: putting the tests only in work_ledger.rs's private module, which would leave the law's successor with no row to carry.

## Tests

**New tests.** There are 19:
- 9 integration tests in `settlement_reserve_tests.rs`;
- 1 private-state unit test in work_ledger.rs: after `Ok`, `Err` and unwind, the state is `Spent` and the credit is restored;
- 9 doctests on `SettlementReserve`: 1 positive and 8 `compile_fail`.

**Item 13's X3d-0 cases.**
- **Spendable after a closed ledger.** `settlement_is_spendable_after_each_way_the_ledger_closes` closes the ledger by a nested failure, an unwind, a swallowed failure, a budget overrun and a postcheck overrun. In each case the ledger refuses `scope`, `charge`, `run`, `retained_record` and `effect` before and after the settlement.
- **Drawing only from the allowance.** `charges_inside_settle_draw_only_from_the_allowance`: the limits are exhausted and the ledger has failed, and nested `run`, `retained_record`, `effect`, `ReservedPostchecks::spend`, `prepaid`, and `effect` and `prepaid` inside `prepaid` all leave `used` unchanged.
- **Overruns.** `overrun_inside_settle_is_refused_before_the_work_and_latches_both`: a direct overrun, a swallowed overrun that then refuses further charges `Closed`, and an effect larger than the allowance.
- **`Err` and unwind.** `err_or_unwind_inside_settle_latches_both`: a returned `Err`; a swallowed nested `Err`, where a second step does not run; and an unwind, on both a failed and an open ledger.
- **One per instance.** `one_reservation_per_instance_and_none_on_a_closed_ledger`: a second reservation (outstanding, or after the spend), a closed ledger, and `Objects`, `Edges` and `Bytes` overruns. Each takes nothing and latches.
- **Foreign reserve.** `a_reserve_from_another_instance_is_refused_before_its_action`, to a ledger with no reserve and to one with its own.
- **Other ledgers.** `ledgers_without_a_settlement_are_unchanged`, plus every existing test unchanged.
- **No refund.** `a_successful_settlement_on_an_open_ledger_leaves_it_open_and_refunds_nothing`, including a reserve forfeited by drop.
- **The pin.** `no_production_source_reserves_or_settles_yet`.
- **The `compile_fail` doctests:** clone; a second `settle` of a moved reserve (not `Copy`); `Default`; a struct literal (private fields); and `reserve_settlement` and `settle` on `WorkScope` and on `ReservedPostchecks`. I compiled each snippet separately. Each fails with exactly its intended error (E0599 no method, E0382 use after move, E0599 no `default`, E0451 private fields) and no other error. The positive doctest compiles and runs.

**Runs.**
- `cargo test --workspace` ran twice: 1419 passed, 0 failed and 3 ignored both times. The base 9d51f33 has 1400; the 19 above are the difference.
- `cargo clippy --workspace --all-targets -- -D warnings` and `cargo fmt --all --check` are clean.
- `check_package_edges.py --lane host` passes against both v112 and v110, with fresh `cargo metadata --locked --offline`.
- `verify_scratch.py` passes: v112 appended over the real lock at 9d51f33 with a synthetic review and assent, run with the worktree's real `verify_design`. It reports 73 inventory successors, 72 contract successors, 16 inheritance rows, and v112 selected.
- `verify_projection.py` against the real lock: 16 rows, 83 corruptions refused.
- `build_v112.py` reruns produce identical bytes. It refuses tracked paths and a lock that selects v112.

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`, python3.14.

## Decide

- **Item 8 and the X3d-0 unit.** Does X3d-0 implement item 8's platform part and item 13's X3d-0 unit exactly? In particular:
  - the reserve is owner-only, charged at once and never refunded;
  - one per instance, with the second refused `Closed` and latched;
  - existing variants only;
  - the opaque, non-Clone, non-Default, non-serializable value with one constructor;
  - `settle` consumes the reserve and is admitted after the latch;
  - the allowance-only draw with `used` unchanged, including nested `effect` and `prepaid`;
  - an `Err`, overrun or unwind latching both;
  - a foreign reserve refused `Closed` before its action;
  - no refill.
- **Outside `settle`.** Is behaviour truly unchanged, for every ledger, including ledgers that never settle and the attempt ledger's ordinary calls?
- **The judgment calls.** Rule on each, in particular 1, 3, 6, 8 and 10.
- **v112.** Is v112 right on v110?
- **Anything else wrong?**

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `settlement-reserve-x3d0-inventory-v112-subject.json`. The lead's value is `bf7cb37c6d830656bef4f638250a7fba7db5c7b336cbf3e21fddcb838c727fd7` (2171 bytes);
- "inventoryCandidateAssessment", with these fields:
  - verdict;
  - requiredFindings;
  - path `docs/implementation/m2/repository-file-inventory.v112.json`, bytes 365881, sha256 `acfc4bc9cc896bab1f916d4a06eb6adc87bab89b2a1c809696dba09b13c7473a`;
  - parent: the v110 pin above;
  - successorRecord: the pin of `docs/implementation/m2/settlement-reserve-x3d0-inventory-v112/successor.json`, 20159 bytes, sha256 `69f08204e81970ed7b293685e8ae58bb759ed768de63ff2abe943066d00a1612`.

Write REVIEW.md and review.json. Do not commit.
