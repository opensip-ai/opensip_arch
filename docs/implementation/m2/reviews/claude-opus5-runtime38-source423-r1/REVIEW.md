# Independent source + formal review — native runtime38 / source shared-security-budget-423

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Bounded and independent. No product or architecture edits, no selection, no commits or push, no
delegation. I owned the serial native lane and used it. Everything I produced — reports, staging and
build outputs — is under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime38-source423-r1`. Previous review evidence
is untouched.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Five non-blocking observations follow.

This unit finally joins the private retained-security cache to the accepted platform ledger. The
join is narrow, and the claims it makes are ones a compiler can settle, so I settled them.

## Frozen inputs

| Input | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `native-runtime-selection-v38-subject.json` | 2496 | `2668e80f…5cb6ffa` | matches pin |
| `trials/shared-security-budget-423/subject.tar.xz` | 6914244 | `6a8456df…cfc17a3e` | matches pin |
| `trials/shared-security-budget-423/subject.json` | 117700 | `25dd43cc…1e3e86fa3` | matches pin |

Product is clean at `da02f64` with the lock at 36 inventory / 59 contract successors and
`repository-file-inventory.v61.json` selected — runtime37 is integrated as stated.

## Formal structure

All 12 members verify byte-for-byte, sorted and unique. Replaying the current
`tools/verify_design.py` `contract_successor` rules: the record is a subject member with a matching
pin; the **11** candidates are exactly the subject minus the record with pin-identical rows; the
**3** parents are sorted, unique and all in the accepted set (15579 paths) —
`initial-root-binding-owner-selection-v1`, `native-runtime-selection-v37` and
`repository-file-inventory.v61.json` — and none is overwritten; no candidate reuses an accepted path;
`passageOverrides` is empty; no `previousCandidate`; only the expected five record fields; and the
unit is not yet in the lock. `stage.py` is byte-identical to the accepted v37 helper.

## Archive, map and baseline

All **627** members streamed and hashed in memory without extraction: every one a regular file, no
absolute, traversal, backslash or non-canonical names, no duplicates, symlinks or devices, and
membership equal to the manifest exactly. Layout is 1 `README.md` + 32 `evidence/` + **594**
`product/`.

The claimed split reproduces exactly: 594 product − 1 lock = **593** non-lock = **583** unchanged +
**10** mapped. All ten mapped paths are **existing** files (no `before: null` rows anywhere) and all
ten are `crates/security/` files. The archive product set equals the live 594-file tracked set, so
the candidate adds and removes nothing. One difference from source421 worth stating plainly: here the
archive's `design-lock.json` is **byte-identical to the live 36/59 lock**, not historical. That is
equally sound, because `stage.py` excludes `design-lock.json` from materialization by exact path and
then asserts the staged lock still equals the live one; the accepted 36/59 selection is preserved
either way. My first check predicate assumed the source421 shape and I corrected it — the note is
recorded in `evidence/archive-checks.json` rather than quietly dropped.

Map `before` rows equal live bytes, `after` rows equal archive bytes, and every mapped file genuinely
differs; the 583 unchanged rows are identical in both trees; mapped ∪ unchanged ∪ {lock} covers all
594 paths; the baseline is the live tracked set with every digest matching.

## Independent staging and native replay

Staged with the frozen helper to my own fresh directory, reproducing the recorded counts exactly —
`archiveMembersVerified: 627, nonLockSourceFilesVerified: 593, mapped: 10, unchangedNonLock: 583,
liveProductUnchanged: true`, exit 0 — with the live product still clean at `da02f64`. Then with
pinned Rust 1.95.0, `--locked --offline`, my own fresh `CARGO_TARGET_DIR`, `RUST_TEST_THREADS=1`:

| Run | Result |
| --- | --- |
| `test -p opensip-security --lib retained_shared_ledger_` | **4 passed**, 0 failed (394 filtered out) |
| `check --workspace --all-targets` | exit 0, **zero** warnings or errors |
| focused tests re-run after probe restore | **4 passed** — tree returned to the tested state |

I did not run the full security suite; the request said it was unnecessary absent concerns, and none
of my findings needed it.

## The source

### The eight lifetime-only files

Exactly as claimed, and I checked each diff line by line: seven are test helpers changing
`fn budget() -> Budget` to `fn budget() -> Budget<'static, 'static>`, and the eighth,
`native_read_session.rs`, changes one private field to `budget: Budget<'static, 'static>`. That is
two changed lines per file and nothing else. The legacy `NativeTrustReadSession` therefore stays on
the owned/static path, gains no shared scope, and becomes no kind of producer.

### The core change

`Budget` becomes `Budget<'work, 'owner>` with one added field,
`shared: Option<&'work mut opensip_platform::WorkScope<'owner>>`. Three things make the ownership
story hold, and they interlock:

1. `impl Budget<'static, 'static>` carries `new()`, so the legacy owned constructor exists **only**
   at the fully static instantiation.
2. `borrowed(work: &'work mut WorkScope<'owner>)` is the only way to obtain a Budget with a
   non-static `'owner`, and it takes an actual borrow of the non-constructible platform scope.
3. `&'work mut WorkScope<'owner>` is covariant in `'work` but **invariant** in `'owner`, because
   `WorkScope` holds `&'owner mut WorkLedger`.

Together those mean a `Budget<'static,'static>` cannot stand in for a borrowed `Budget<'w,'o>`, so
there is no way to hand a helper a borrowed budget and have it swap in a fresh one — the reset hole
this whole line of work has been chasing. I verified this rather than reasoning about it alone; see
below.

**`work()`** lends the platform scope without exposing the owner: it takes the shared field by
`as_deref_mut()` — a reborrow, never a move — and passes it to
`impl FnOnce(&mut WorkScope<'_>) -> Result<T, WorkFailure<Error>>`. The elided lifetimes make that a
higher-ranked bound while `T` is fixed before the call, so the callback cannot name the scope's
lifetime in its return type and cannot smuggle the scope out. The whole call is wrapped in `guard`,
so a failure latches.

**`work_error`** maps platform failures onto **existing** security variants with a total match and no
wildcard: `Operation(e) => e` preserves the caller's original error, the four budget dimensions map
to `ObjectLimit`/`EdgeLimit`/`ByteLimit`/`Cap`, `Closed` maps to `Closed`, and
`Profile | Arithmetic | ReservedPostcheck` collapse to `Profile`. Because the match is exhaustive
without a catch-all, a future platform variant becomes a compile error rather than a silent
mis-mapping. That is the right call.

**`closed()`** is `self.failed || shared.is_some_and(|w| w.is_failed())`, and `scope()` now consults
it both on entry and after the callback. So a failure anywhere in the shared operation — including
one caused by a different participant — closes this Budget, and a callback that swallows a nested
platform error still yields `Err(Closed)`. The swallowed-failure guarantee now crosses the crate
boundary.

**The Drop guard** additionally closes the original operation on any unsuccessful exit:

```rust
if let Some(work) = self.budget.shared.as_deref_mut() {
    let _: Result<(), WorkFailure<()>> = work.scope(|_| Err(WorkFailure::Operation(())));
}
```

This closes the outer scope *through the platform's own guarded error path* rather than reaching into
private state, which I like. It is also panic-safe: `scope` and the platform's `LedgerScope::drop`
only flip a bool, so nothing can unwind out of this `Drop` during an unwind. Calling it on an
already-failed ledger returns `Closed` immediately, so it is idempotent.

**Charge placement.** `account()` is a no-op for an owned budget and charges the shared ledger
otherwise. I traced all five call sites and the ordering is consistent everywhere: local validation
first, then the shared charge, then the local mutation. For `edge` the order is limit check →
`account(0,count,0)` → `edges += count`; for `directory` it is object-limit check →
`account(1,0,0)` → insert, and only inside the `!contains_key` branch; for `entry` it is
`edge(1)` → byte check → `account(0,0,len)` → `bytes += len`; and for both `retain` and
`capture_current` the charge lands after the duplicate early-return and immediately **before** the
`Arc::from(raw)` allocation. So new unique retained records charge one object plus their bytes before
allocation, duplicates recharge nothing, and there is no path that charges the shared ledger and then
fails locally. Platform's `charge` validates all three dimensions before its single `used`
assignment, so a partial charge is impossible.

`current` and `raw` are distinct maps with distinct keys, so the same bytes reachable as both a
current-path entry and a content-addressed record charge twice — which mirrors the pre-existing local
object count (`raw.len() + directories.len() + current.len()`) exactly, so the shared ledger stays
consistent with local semantics rather than diverging from them.

**Visibility.** `borrowed` and `work` are `pub(super)`; `work_error`, `account` and `closed` are
private. No item in any of the ten files becomes `pub`. The `pub` surface in
`native_read_session.rs` is entirely pre-existing and its `budget` field stays private.

### Verified by compilation, not by reading

`Budget` is `pub(super)`, so an out-of-crate probe is impossible. I appended probes to **my own**
staged copy of the test module, compiled with `cargo check -p opensip-security --tests`, then
restored the file from a saved reference and re-verified its digest each time — the same discipline
the author used. After the probes I re-ran the focused tests to prove the tree was back to the exact
tested state.

| Probe | Expectation | Result |
| --- | --- | --- |
| intended borrowed use (`edge` then `work(charge)`) | must compile | **exit 0** |
| `*b = Budget::new(...)` on a borrowed `Budget<'_,'_>` | rejected | **E0521** — "argument requires that `'1` must outlive `'static`… which makes the generic argument `'_` **invariant**" |
| static helper shape assigned over a borrowed budget | rejected | "lifetime may not live long enough" |
| return the platform scope out of `work()` | rejected | "lifetime may not live long enough" ×2 |

The positive control matters: without it, "did not compile" proves nothing. With it, the three
rejections are specific. The compiler's own note names invariance as the mechanism, which is exactly
the argument the design rests on. My replacement probe was written independently — different function
name, different constructor arguments — and reproduced the same E0521 with the same invariance note
as the author's preserved 420 probe. One honest correction: my first owner-escape probe failed with
E0106 because of a missing lifetime in **my** signature, not because of the API; I fixed the
signature and re-ran, and the corrected probe is the one recorded.

### The four tests

All four are named `retained_shared_ledger_*` and each tests something real. Identity-through-reborrow
checks `Arc::ptr_eq` across a platform reborrow and that the duplicate retain recharges nothing
(host `used` = objects 1, edges 3, bytes 16; local counters `(1, 0, 2)`) — I re-derived that
arithmetic by hand and it is right. Recreated-cache is the sharpest one: a second `Budget::borrowed`
over the same host, with the ledger capped at one object, fails with `ObjectLimit` precisely because
the local cache reset but the shared ledger did not. Nested-failure and unwind both confirm the
original operation ends up latched and the outer scope returns `Closed`. Note that a dropped
`Budget` is harmless on its own — only the transient `BudgetScope` guard has a `Drop` — which is why
the first cache in that test can go out of scope without poisoning anything.

## Evidence, attribution and limits

- **Mine:** independent staging, three cargo runs, four compile probes, and read-only Python
  structural checks over the formal subject, the whole archive, and the map/baseline. Commands,
  environment and raw logs preserved under `evidence/`.
- **Author, historical 420, not rerun by me:** the full `opensip-security --lib` suite at
  396 passed / 0 failed / 2 ignored, and the original E0521 replacement probe with its restore. The
  two ignored tests are the pre-existing real-host clock pilots and are not relabeled.
- **Author, fresh 423:** the four focused tests and the combined workspace check, exit 0 each. I
  reproduced both independently, so they are not taken on trust here.
- **Not independently verifiable:** the claim that the 423 candidate equals the tested 420 candidate
  byte-for-byte under only the `work_ledger.rs` → `work_ledger_tests.rs` rename plus the lock. The
  420 trial retains an *evidence* archive only — no candidate archive — so there is nothing to
  compare against. Root states they checked all candidate contents; I record that as root's evidence,
  not mine. What I did verify instead is stronger for acceptance purposes: the candidate matches the
  **live** product at `da02f64` across all 583 unchanged non-lock files, the ten mapped files differ
  exactly as mapped, and the candidate introduces no path beyond the live tracked set.
- **Scope of acceptance.** Ten files, retained accounting only. This is explicitly **not** complete
  native precharge, and I am not treating it as such: existing capture callbacks may allocate and
  read before retention, native directory open and observation may precede the directory object
  charge, and names, ACLs, parsing, rechecks, temporary buffers and post-effect reservations remain
  unaccounted and need later native work. `HostCapture` is not qualified by this change. No host
  attempt, native creator, public ingress, permit, P0, custody or current authority is claimed, and
  no M2 or M2–M6 completion. The private 422 reader and 413 ACL prototypes are not included and are
  not approved. macOS development evidence only; no Linux, crash, power-loss or release
  qualification. Constructors remain accounting, not authority, and the obligation to keep the ledger
  owner private still sits with the future host. Root substantive assent and guarded private/live
  verification remain required before selection.

## Non-blocking observations

1. `work()` returns `Error::Profile` when there is no shared scope, overloading a variant that
   otherwise means "invalid budget profile parameters". Reusing existing variants was a constraint
   here, so this is a reasonable trade, but a caller cannot distinguish the two conditions. A short
   doc line on `work()` saying so would help, and a dedicated variant would be better whenever the
   error enum next opens for other reasons.
2. `borrowed()` hardcodes the global ceilings (65536 / 131072 / 268435456) and cannot fail, so it
   offers no way to tighten *local* caps the way `new()` does. Per-operation tightening has to come
   from the platform ledger's `with_limits`. That is a coherent choice — the shared ledger is the
   operation-wide authority — but it deserves a doc note, since the asymmetry with `new()` is easy to
   misread.
3. The Drop guard closes the shared scope with a synthetic `WorkFailure::Operation(())`. The platform
   ledger records only the latch, so nothing is lost today, but a post-mortem sees "closed" with no
   indication of which security operation closed it. If diagnostics ever matter there, the payload is
   the place to carry them.
4. `retained_record`-style nesting means one logical charge can traverse several guards
   (`scope` → `guard` → `account` → platform `charge` → platform `scope`). Harmless, but worth
   knowing when reading a trace: a caught failure at any depth latches both ledgers.
5. The accounting gap in observation 4 of the source README is real and I want it restated rather
   than buried: retention is charged, physical capture is not. Any later adapter that reads or
   allocates before retention is spending unaccounted work, and this acceptance does not cover it.
