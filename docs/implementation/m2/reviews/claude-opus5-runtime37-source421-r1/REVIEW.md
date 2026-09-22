# Independent source + formal review — native runtime37 / source shared-work-ledger-421

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Bounded, independent. No product or architecture edits, no selection, no commits or push, no
delegation. I owned the serial native lane for this review and used it. All artifacts, staging and
build outputs are under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime37-source421-r1`.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Five non-blocking observations are recorded at the
end.

This is the strongest-evidenced unit in this series so far, because the guarantees it claims are
type-system guarantees and I was able to test them by compilation rather than by reading alone.

## Frozen inputs

| Input | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `native-runtime-selection-v37-subject.json` | 2481 | `f5775cdd…5ea8ef4` | matches pin |
| `trials/shared-work-ledger-421/subject.tar.xz` | 6989276 | `fcbd99dc…20b2e5b` | matches pin |
| `trials/shared-work-ledger-421/subject.json` | 116137 | `bf281528…315ca45` | matches pin |

Product is clean at `597d6e6`, with the lock at 36 inventory / 58 contract successors and
`repository-file-inventory.v61.json` selected. `inventoryPassageInheritance` now carries **5** rows,
because selecting v61 projected the previously-direct initial-owner-406 row-104 override into the
inherited set — the mechanism I described at v60/v61, now visible in the lock.

## Formal structure

All 12 members verify byte-for-byte, sorted and unique. Replaying the current
`tools/verify_design.py` `contract_successor` rules against the proposed record: the record is a
subject member with a matching pin; the **11** candidates are exactly the subject minus the record
with pin-identical rows; the **3** parents are sorted, unique, all present in the accepted set
(15567 paths) — `initial-root-binding-owner-selection-v1`, `native-runtime-selection-v36` and
`repository-file-inventory.v61.json` — and none is overwritten; no candidate reuses an accepted path;
`passageOverrides` is empty; no `previousCandidate`; the record carries only the expected five
fields; and the unit is not yet in the lock. `stage.py` is byte-identical to the accepted v35/v36
helper (`3a71d80a…`).

## Archive, map and baseline

I streamed and hashed all **618** members in memory without extracting: all regular files
(type `'0'`), no absolute, traversal, backslash or non-canonical names, no duplicates, no symlinks or
devices, and membership equal to the manifest exactly. Layout is 1 `README.md` + 23 `evidence/` +
**594** `product/` members.

The claimed split reproduces exactly: 594 product − 1 lock = **593 non-lock**, of which **3 are
mapped** and **590 unchanged**. The three mapped paths are exactly one existing file,
`crates/platform/src/lib.rs`, plus two genuinely new files,
`crates/platform/src/work_ledger.rs` and `crates/platform/tests/work_ledger_tests.rs`. The corrected
test target name is present and the rejected `work_ledger.rs` name is absent — RF-1's correction is
carried into the source, as promised. The live tracked set is 592 files, and
candidate-minus-baseline is exactly those two new paths.

The lock handling differs from source415 and is worth stating precisely: the archive's
`design-lock.json` is **historical** here — it is the 35-inventory/58-contract lock
(`531734d9…`, the very lock I anchored at 117d0e3), not the live `e980499f…` 36/58 lock. That is
correct and required, and `stage.py` enforces it: the lock is excluded from materialization by exact
path, the live baseline is copied first, and staging asserts the staged lock still equals the live
one. So the historical lock in the archive cannot displace the accepted inventory61 selection.

Map `before` rows equal live bytes and `after` rows equal archive bytes; the two new rows correctly
declare `before: null` and their destinations are unoccupied live; the 590 unchanged rows are
identical in both trees; mapped ∪ unchanged ∪ {lock} equals all 594 product paths; the baseline is
the 592-file live tracked set with every digest matching.

## Independent staging and native replay

I staged to my own fresh directory with the frozen helper and reproduced the author's counts
exactly — `archiveMembersVerified: 618, nonLockSourceFilesVerified: 593, mapped: 3,
unchangedNonLock: 590, liveProductUnchanged: true`, exit 0 — and the live product stayed clean at
`597d6e6`. Then, with pinned Rust 1.95.0, `--locked --offline`, my own fresh `CARGO_TARGET_DIR` and
`RUST_TEST_THREADS=1`:

| Run | Result |
| --- | --- |
| `test -p opensip-platform --lib work_ledger::` | **6 passed**, 0 failed |
| `test -p opensip-platform --test work_ledger_tests` | **3 passed**, 0 failed |
| `test -p opensip-platform --doc work_ledger::` | **2 passed** (both compile-fail) |
| `check --workspace --all-targets` | exit 0, **zero** warnings or errors |

The 6 unit tests and 2 rustdoc boundaries were offered as *historical 418* evidence. I re-ran both at
421 from my own staging, so they are independently reproduced here rather than inherited. Commands,
environment and raw logs are preserved.

## The source

The public surface added to `crates/platform/src/lib.rs` is one private `mod work_ledger` plus one
`pub use` of `WorkBudgetError`, `WorkCost`, `WorkFailure`, `ReservedPostchecks`, `WorkLedger` and
`WorkScope`. The renaming of `BudgetFailure`/`Cost`/`Failure` to `Work*` follows platform's existing
domain-prefix convention (`ClockError`, `AccountObservationError`, `PublicationFailure`). Nothing
else in `lib.rs` changes.

**Caps, subtraction and overflow.** Fixed ceilings are 65536 objects, 131072 edges, 268435456
aggregate bytes and a 4 MiB per-record limit. `with_limits` refuses any zero dimension and any
dimension above the global cap, so it can only lower positive bounds — and the integration test
checks both refusals. The limit tests read `cost.d > limits.d - used.d`, a raw subtraction, which is
sound because `used` is assigned in **exactly one place** (inside `charge`, after all three
dimension checks), so `used <= limits` is an invariant with a single enforcement point. `limits` is
never mutated after construction. `Cost::checked_add`/`checked_sub` are used for the accumulate,
reservation-total and postcheck-decrement paths, each mapping overflow to `Arithmetic` or
`ReservedPostcheck`.

**Nested guard, failure latch and unwind.** `LedgerScope` is the same RAII idiom as the security
`Budget` guard accepted at runtime36, and the three-arm match is identical in shape:
`Ok` with a clean ledger completes, `Ok` with a latched ledger becomes `Closed`, and
`Err(error) => Err(error)` preserves the caller's original error type and value. `failed` is set
`true` in exactly one place — the `Drop` — and `false` only at construction. There is no reset,
refund or retry: `used()` is documented as including unused reservations and is never decremented.
The unit tests cover the swallowed-nested-failure and unwind paths directly, and
`failed_ledger_keeps_reservation_and_cannot_retry` asserts both that the original
`Failure::Operation("read failure")` survives and that the charged cost is retained.

**Retained record versus temporary cost.** `retained_record` charges `objects: 1` plus `bytes`
*before* the callback, after refusing anything above the 4 MiB record limit. The doc comment is
honest that identity deduplication belongs to the caller's cache and that temporary reads and
repeated observations need their own charges, and
`exact_limits_are_inclusive_and_repeated_work_is_not_free` proves two identical records charge twice.

**Reservation before effect, no refund.** `effect` adds effect and postcheck costs with
`checked_add`, charges the total before invoking the action, and hands the action a
`ReservedPostchecks` whose `spend` only decrements a local allowance — it never charges the ledger
again and never credits anything back. The test asserting `used.edges == 4` after spending 1 of 3
reserved edges pins the no-refund rule. Overspending underflows `checked_sub`, returns
`ReservedPostcheck`, and latches the ledger — and
`caught_postcheck_overrun_still_closes_the_ledger` shows that catching that overrun still closes the
ledger. The README's framing is right and worth repeating: this is allowance accounting, **not**
proof that any postcheck actually ran.

**Scope lifetimes and callback ability — verified by compilation.** This is where I spent the review
budget, because "non-constructible" and "cannot replace the owner" are claims a compiler can settle.
I built five probes against the staged rlib, including a **positive control** so a broken harness
could not masquerade as a passing boundary:

| Probe | Expectation | Result |
| --- | --- | --- |
| control: intended public use | must compile | **exit 0**, charges 2 edges across a nested scope |
| `*helper = WorkLedger::new()` | rejected | **E0308** — "expected `WorkScope<'_>`, found `WorkLedger`" |
| cross-owner `mem::swap` of two scopes | rejected | **E0521** — "borrowed data escapes outside of closure… mutable references are invariant over their type parameter" |
| return the scope through the success value `T` | rejected | "lifetime may not live long enough" (×2) |
| `owner.clone()` / `WorkLedger::default()` | rejected | **E0599**, **E0277** |
| struct literals for `WorkScope` / `ReservedPostchecks` | rejected | **E0451** — "field `ledger` … is private", "fields `ledger` and `remaining` … are private" |

So the 416/417 hole — a mutable callback handed the replaceable ledger, where
`*helper = WorkLedger::new()` erased charged work — is closed for the *right reason*, not
incidentally. `WorkScope` exposes no `Deref`/`DerefMut`, no accessor returning `&mut WorkLedger`, no
`Clone`, `Default` or `Debug`, and platform declares no serde dependency at all, so no derived
(de)serialization can reconstruct one. The escape-through-`T` result is the subtle one and it is
structural: `impl FnOnce(&mut WorkScope<'_>)` desugars to a higher-ranked bound, and `T` is fixed
before the call, so no callback can name the scope's lifetime in its return type.

The public integration test earns its place. It builds a sibling `HeldCache` holding
`&'cache mut WorkScope<'op>` plus its own buffers, and demonstrates three things through the real
public API: one ledger accumulates correctly across host → cache → platform reborrows
(objects 2, edges 6, bytes 32, with the held buffer's pointer stable across nested work); a nested
platform failure that the host *catches* still surfaces as `Closed` and survives the cache's drop;
and lowered policy limits refuse work *before* the callback runs, without resetting counters.

## Evidence and limits

- **My own evidence:** independent staging with the frozen helper, four cargo runs, six compile
  probes, and read-only Python structural checks (formal, archive, map/baseline). Commands,
  environment and raw logs preserved under `evidence/`.
- **Author evidence, attributed, not reinterpreted:** the original 416/417 mutable-callback reset
  demonstration and the 418 missing-reexport compile failure followed by its r2 success are
  preserved in the archive's embedded development history. Those are the author's records of how the
  hole was found and fixed; I did not rerun them, and the old source pathnames in them are
  historical, not the selected target.
- **Limits.** This is a source and formal review of three platform files. It approves no security
  work-420 cache bridge — I confirmed none is present, since only those three paths change. The
  conditional sibling-cache tests are accounting and lifetime demonstrations, not native
  evidence-capture fixtures. `ReservedPostchecks` is allowance accounting and is not a native
  success receipt; no cost derivation for real native producers exists yet. Public constructors are
  not authority, and the future host must still keep its owner private and tie receipts to one act —
  the type system prevents helper replacement, but it cannot make the host's ownership decision for
  it. macOS development evidence only; no Linux, crash, power-loss or release qualification. No
  claim of creator qualification, native custody, current authority, shared native
  capture-precharge, P0, or M2 qualification. Root substantive assent and guarded private/live
  verification remain required before selection.

## Non-blocking observations

1. Neither `compile_fail` doctest pins an expected error code, so in principle either could start
   passing for an unrelated reason after a refactor. My probes show they fail for the intended
   reasons **today** (E0308 and E0521, with a compiling control). I would pin `E0308` on the first
   and deliberately **not** pin the second: lifetime diagnostics like E0521 are among the least
   stable across compiler versions, so pinning it would trade a small robustness gain for spurious
   breakage. The guarantee does not depend on the doctests in any case — it is structural.
2. `ReservedPostchecks` is the only new export without the `Work` prefix used by `WorkCost`,
   `WorkFailure` and `WorkBudgetError`. No collision exists and no documented rule covers exported
   type names, so this is cosmetic, but `WorkReservedPostchecks` would read more consistently in a
   flat namespace.
3. The dimension checks use raw subtraction rather than `checked_sub`. It is sound, but the proof
   lives in the single-assignment invariant on `used` rather than in the expression. A
   `debug_assert!` that `used <= limits` at the top of `charge` would make the invariant local and
   survive future edits.
4. `retained_record` nests three guards (`scope` → `run` → `charge`) for one logical charge. Harmless,
   but worth knowing when reading traces: a caught failure at any depth latches the same ledger.
5. An `effect` action receives only `ReservedPostchecks` and therefore cannot charge newly discovered
   work — by design, since the reservation is meant to be complete. Real native producers will have
   to derive sufficient postcheck costs up front or fail; that obligation belongs to the future host
   integration and is already named in the source README.
