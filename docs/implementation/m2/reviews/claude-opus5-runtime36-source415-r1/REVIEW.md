# Independent source + formal review — native runtime36 / source trust-budget-scope-415

Reviewer: actual Claude Opus 5 (model identity, not a task label), session of 2026-09-21.
Bounded, read-only. No product or architecture edits, no commits, no delegation, no selection.
No native build or test was executed in this review: the optional focused replay was withdrawn
mid-review by the requester, and ROOT owns the native lane. All artifacts are written only under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime36-source415-r1`.

## Verdict

**ACCEPT-DESIGN-UNIT.** No required findings. Three non-blocking observations are recorded below.

## Frozen inputs verified

| Input | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `docs/implementation/m2/native-runtime-selection-v36-subject.json` | 2480 | `43e059a6…0f582d` | matches pin |
| `…/trials/trust-budget-scope-415/subject.tar.xz` | 6908356 | `8b9fa526…0fedc3625f` | matches pin |
| `…/trials/trust-budget-scope-415/subject.json` | 115594 | `225a23a8…71349d41e` | matches pin |

All 12 formal members exist with exactly their pinned bytes and digests; the member list is sorted
and unique. Product checkout is clean at `f7f50d6`.

## Formal structure (current `tools/verify_design.py` rules)

I ran the current product verifier against the live architecture (`passed: true`, 46 inputs,
57 contract successors, selected inventory `repository-file-inventory.v59.json`), then replayed
`contract_successor`'s rules against the *proposed* v36 record, which is correctly not yet in the
lock. Every rule holds:

- The record `native-runtime-selection-v36/successor.json` is itself a subject member and its pin
  matches its bytes.
- The 11 candidates are exactly the subject minus the record, with pin-identical rows — the
  "candidates cover the reviewed subject" rule.
- The three parents are sorted, unique, and each is an accepted base or selected artifact in the
  current accepted set (15554 paths): `initial-root-binding-owner-selection-v1/successor.json`,
  `native-runtime-selection-v35/successor.json`, `repository-file-inventory.v59.json`. No parent
  appears among the members, so the unit cannot overwrite a parent.
- No candidate reuses an accepted path; `passageOverrides` is empty; there is no
  `previousCandidate`; the record carries only the expected five fields.

`stage.py` is byte-identical to the already-selected v35 helper, so the staging semantics under
review are the ones already accepted at 35.

## Archive membership and coverage

I streamed and hashed every archive member in memory without extracting to disk. 615 members, all
regular files (`type '0'`), no absolute, traversal, backslash or non-canonical names, no duplicates,
no symlinks, devices or hardlinks. Archive membership equals manifest membership exactly and every
member matches its manifest bytes and digest. Layout is 1 `README.md` + 22 `evidence/` + 592
`product/` members.

Against the live product at `f7f50d6`, exactly two members differ:
`crates/security/src/trust/retained_metadata_index.rs` and its sibling
`retained_metadata_index_tests.rs`. This independently reproduces the claimed
**592 product / 2 mapped / 589 unchanged non-lock** split: 592 product members, minus
`design-lock.json` gives 591 non-lock, minus 2 mapped gives 589 unchanged. The archive's
`design-lock.json` is byte-identical to the live selected lock and is excluded from source
materialization by exact path, so the source unit cannot smuggle a lock change.

The materialization map's `before` rows equal the live bytes and its `after` rows equal the archive
bytes for both mapped files; each mapped `before != after`. The 589 unchanged rows are identical in
both the live product and the archive. `mapped ∪ unchanged ∪ {design-lock.json}` equals the 592-row
baseline, which in turn equals the live tracked file set, with all 592 digests matching. Both the
map and the baseline pin `baseProductHead` to `f7f50d6`.

Reading `stage.py`: full verification precedes any extraction or output creation, it refuses a
pre-existing output directory, re-pins every staged non-lock file after writing, asserts the staged
lock equals the live lock, and re-pins the whole live baseline at the end — so its
`liveProductUnchanged: true` is an actual post-condition, not a claim.

## The actual source change

The change is confined to `Budget::scope` plus a new private guard. The public shape is untouched:
`pub(super) fn scope<T, E: From<Error>>` keeps its signature and `E: From<Error>` bound; no new
error variant, constructor, public API, import or `unsafe` appears; no counter, limit, cache or
handle algorithm is altered.

```rust
struct BudgetScope<'a> { budget: &'a mut Budget, completed: bool }
impl Drop for BudgetScope<'_> {
    fn drop(&mut self) { if !self.completed { self.budget.failed = true; } }
}
```

and `scope` now matches `Ok(value) if !scope.budget.failed => { completed = true; Ok(value) }`,
`Ok(_) => Err(Error::Closed.into())`, `Err(error) => Err(error)`.

**Nested success.** The early `if self.failed` return happens before the guard is constructed, and
`failed` is never set before the callback, so legitimate nested charges still work. `failed` is
assigned `true` in exactly one place (the `Drop`) and `false` in exactly one place (`new`). There is
no reset, refund or retry anywhere in the diff.

**Explicit error preservation.** The `Err(error) => Err(error)` arm returns the caller's original
error type and value unchanged, even when a nested operation has already latched. That preserves the
existing precedence in which a specific native failure outranks a generic budget error — the pattern
`Err(e) => return Err(failure.unwrap_or(Error::Budget(e)))` in `directory_record_capture.rs`,
`native_current.rs` and `native_record_capture.rs` continues to report the specific cause.

**Swallowed nested failure.** This is the fix: a callback that catches an inner error and returns
`Ok` now yields `Err(Error::Closed)`. I scanned all 63 `.scope(` call sites in the security crate for
error-catching constructs. Fifteen contain such tokens; on inspection every one is `Option` handling
(`ok_or`, `unwrap_or_else(|| fence.root()…)`, `map_or`) or a path that still returns `Err`. The only
`M::Store` implementation, `NativeStore::read`, records the source and returns `Err(M::Error::Capture)`
— it never returns `Ok` after a failure. All internal `guard` closures propagate with `?`. I found no
caller that relied on the old "success wins over a latched budget" behavior, so no caller regression.

**Panic unwind.** `BudgetScope` is a local of `scope`, so it is dropped exactly on unwind through that
frame and latches the same budget before any catcher can reuse it. It cannot misfire during unrelated
unwinding, because its lifetime is the scope call. Nested guards latch idempotently. The workspace
sets no `[profile]` and has no `.cargo/config.toml`, so the default `panic = "unwind"` applies and the
regression is meaningful. This mirrors the established in-repo idiom `StopOnUnwind` in
`revocation.rs:64` and its test `callback_unwind_latches_before_a_catcher_can_reuse_the_monitor`;
`BudgetScope`'s explicit `completed` flag is the stricter form, since it does not depend on
`thread::panicking()`.

**Borrow and drop semantics.** `f(scope.budget)` is an implicit reborrow, not a move, because the
callee's parameter type `&mut Budget` is known. This matters: `BudgetScope` implements `Drop`, so a
real move out of the field would be rejected (E0509). The author's two exit-0 `cargo check
--workspace --all-targets` runs are consistent with the reborrow reading; I did not compile.

**Regressions.** Three added tests, no existing test touched (4 → 7 in the module). Reading them
against the *original* code: `Budget::new(1,1,1)` then `edge(2)` latches and the swallowing callback
returns `Ok(())`, so the old `scope` returned `Ok(())` — the first negative test must fail. In the
second, the old code never latched on unwind, so the post-catch `edge(1)` succeeded — it must fail.
The positive control charges 1 + 1 edges within a limit of 2 and must pass. The archived
`original414/before.stdout` shows exactly that: 1 passed, 2 failed, with `left: Ok(())` /
`right: Err(Closed)` at lines 316 and 331.

## Evidence attribution and limits

- **Author evidence, historical 414, not mine and not fresh:** the failing pre-fix run, the fixed
  focused run, and the full `opensip-security --lib` suite at 392 passed / 0 failed / 2 ignored in
  226.16s. The two ignored tests are pre-existing real-host clock pilots; I confirmed both still
  carry their `#[ignore]` attributes with the same reasons in the live product, so nothing was
  enabled or relabeled.
- **Author evidence, fresh 415:** one combined-workspace `cargo check --locked --offline --workspace
  --all-targets`, exit 0. The author's `baseline-reconciliation.json` states
  `fresh415FullSecuritySuiteClaimed: false` and `wholeWorkspaceNativeSourceUnchanged: false` — honest
  scoping, and I verified its rebase claim directly: `git diff e60ce01..f7f50d6` touches exactly
  `crates/host/src/installation_lineage.rs` and `design-lock.json`, neither a security test
  dependency.
- **My own evidence:** read-only Python structural checks only (formal, archive, map/baseline), plus
  file reads. No staging, no build, no test, no native job.
- **Limits:** I did not compile or execute any Rust. The historical 392-test result is corroborating,
  not fresh, evidence. As the source README states, this is a boundary guard: an error hidden
  entirely inside a callback that never enters a nested budget scope remains undetectable, and
  `capture`'s reader callback deliberately receives no `&mut Budget`. macOS-only development
  evidence. Nothing here qualifies a creator, shared ledger, native custody, current authority, P0,
  or any whole-M2/project completion.

## Non-blocking observations

1. `Ok(_) => Err(Error::Closed.into())` necessarily discards both the successful value and the
   original nested error; `Closed` is the only honest signal left, but diagnostics for a swallowing
   adapter will be coarse. Worth a note wherever adapters are audited.
2. `stage.py`'s closing re-pin covers the tracked baseline files, so an *untracked* file added to the
   product during staging would not be noticed. Staging never writes there, so this is cosmetic.
3. The guard latches on every unsuccessful exit, which is broader than `StopOnUnwind`'s
   `thread::panicking()` test. That is correct here only because the old explicit `if r.is_err()`
   latch is subsumed; the two idioms should not be assumed interchangeable elsewhere.
