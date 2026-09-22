# Independent source + formal review — native runtime41 / source native-accounting-437

Actual Claude Opus 5, 2026-09-21. Bounded, independent. No repo edits, selection, commits, push or
delegation. I owned the serial native lane. Outputs under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime41-source437-r1`; exact commands, logs and
hashes are in `evidence/` and `hashes.txt`. No compiled binaries archived, no native account details
printed.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Four non-blocking observations.

## Formal, archive, staging

All three frozen pins match (subject `dac61d4c…` at 2476 B, archive `5e47ec3a…` at 6959636 B,
manifest `e7238f60…` at 136532 B). 12 members verify; 11 candidates = subject minus record with pin-identical rows;
3 sorted parents (owner-406, runtime-40, inventory-62) all accepted, none overwritten; no path reuse;
`passageOverrides` empty; unit not in the lock. `stage.py` byte-identical to the accepted v40 helper.

All **731** archive members hashed in memory — regular files only, no unsafe or duplicate names,
membership equals manifest. Split reproduces exactly: **596** product − 1 lock = **595** non-lock =
**587** unchanged + **8** mapped, all eight **existing** paths (zero new files), and the archive
product set equals the live 596-file tracked set. The archive lock equals the live 37/62 lock with
inventory62 and all five inherited meanings, and is excluded from materialization by exact path. Map
`before`/`after`, the 587 unchanged rows, the 596-row baseline and the recorded stage stdout all
verify. My own staging reproduced 731 / 595 / 8 / 587 with `liveProductUnchanged: true`.

## Change 1 — `ReservedPostchecks::with_allowance`

This is option A from my 429 correction, in callback form. The ordering is the point:
`parent.spend(cost)?` runs **before** the child exists, so the parent's remainder is reduced first and
the child receives exactly `cost` on the **same** ledger (`ledger: parent.ledger`, a reborrow, not a
move — `ReservedPostchecks` has no `Drop`, and you cannot move out of `*parent`). Three nested guards
(`self.scope` → `spend`'s scope → `child.scope`) all latch the one ledger.

I verified the boundary by compilation rather than by reading, with a positive control so the
negatives cannot pass on a broken harness:

| Probe | Result |
| --- | --- |
| positive control | **compiles and executes**: `used` stays 10 however it is subdivided; after a 4-edge child the parent remainder is exactly 6 and spendable; a nested grandchild works; a child asking 5 from a 4-edge share refuses and latches while `used` stays 10 |
| cross-owner child swap | **E0521** |
| child escape through `T` | lifetime error |
| parent used while child borrowed | **E0500/E0501** |

So the child cannot reach the parent's share, cannot escape, cannot be swapped across owners, and the
parent is exclusively reborrowed for the child's lifetime. No double charge, no refund, no reset, no
second ledger. The callback form is sounder than my returnable-split sketch: there is no window in
which a caller holds both a live parent handle and a child.

## Change 2 — generic `Budget::work`

`work<T, E: From<Error>>` now passes `Operation(E)` through unchanged and maps a platform budget
failure via the existing `work_error` and then `.into()`. This is exactly the fix I recommended in
the 429 correction (C3), and it lands as a generalisation of `work` in place rather than a second
`work_in` — cleaner, no duplicate API. `self.guard(...)` necessarily became `self.scope(...)` because
`guard` fixes `E = Error`; `scope` already carries the `E: From<Error>` bound, so the RAII guard and
the `closed()` entry check are preserved, not weakened. `guard` remains used seven times elsewhere,
so nothing went dead — consistent with the zero-warning workspace check. The legacy owned budget
still refuses with `Profile` in the `None` arm before the callback is ever invoked. Three typed tests
pin the original `PermissionDenied` against a budget `EdgeLimit` and the legacy refusal, and all
three pass.

## Change 3 — native descriptor-name precharge

`observation_cost() = { objects: 1, edges: 1, bytes: BUFFER_BYTES }` with
`BUFFER_BYTES = 32 + 1024 = 1056` — exactly the claimed 1 object / 1 `fgetattrlist` edge / 1056
requested attribute-buffer bytes, derived from the constant the observer actually uses.
`matches_accounted` uses `work.run(cost, …)` so the charge precedes the callback;
`matches_reserved` uses `post.scope(|p| { p.spend(cost)?; observe() })` with no outer recharge. The
existing `matches` implementations are untouched and both `#[cfg]` gates are intact — the single
removed line in that diff is positional, not a gate removal. The shipped test asserts
`owner.used() == descriptor_name_observation_cost()` on the accounted path and the same equality on
the reserved path, so exactness and no-double-charge are pinned rather than asserted in prose. A name
mismatch returns `false` with the owner **not** failed — mismatch is data, and the test comment says
the consuming policy must refuse it, which matches the request's framing.

On the buffer question the request asked me to inspect: the attribute buffer is a **stack** array
`[0u8; BUFFER_BYTES]`, not a heap allocation, and the doc comment says plainly that stack frame,
allocator and OS internals are not measured. So `objects: 1` here means "one caller-owned buffer",
not "one heap object". Honest and documented; see observation 1.

## Replay (mine)

Pinned Rust 1.95.0, `--locked --offline`, fresh target dir, `RUST_TEST_THREADS=1`: **6** ledger unit,
**13** ledger integration, **8** reader integration, **5 new** name tests, **4** cache, **3** typed =
**39**, matching the claimed count, plus **2** rustdoc compile-fail cases, and
`check --workspace --all-targets` clean with **zero** warnings. (My `directory_names::` filter
reported 10 because it also matches five pre-existing name tests; the five new ones are the four
`work_tests` plus the public-wrapper test.) No full security suite was needed; the historical 433 run
is not a fresh 437 claim and I did not treat it as one.

The requested source-header warning is present in `work_reader.rs` and is accurately scoped: it states
that both entry points close the ledger on **any** returned error including ordinary I/O and invalid
limits, and that they are not drop-in inside native brackets needing accounted postchecks. It is in
this new source, not retroactively in 430, which is correct. My runtime38 note about `borrowed()`'s
hardcoded caps also picked up a doc line pointing at `WorkLedger::with_limits`.

## Limits

Counters cover requested buffers and outer API calls only — not opaque OS, allocator or service
costs, and not latency. This reviews the actual 432/433 implementation plus the name wrapper; it is
**not** whole native postcheck composition. The standalone 430 reader still latches ordinary I/O
before returning, so a native owner must keep an ordinary read outcome provisional until its required
checks finish while a terminal work failure stops immediately — audit 429, my corrected advice and
root's qualifications stand unchanged, and no law is amended. No native capture, ACL or postcheck-cost
qualification; no actor, core, profile, custody, home base, creator, permit, P0 or current authority;
no Linux, release, power-loss, full M2 or M2–M6 completion. Root substantive assent and guarded
integration remain required.

## Observations (non-blocking)

1. **`objects` now spans two notions.** The reader counts a heap `Vec`; the name observer counts a
   stack array. Both are "caller-owned buffers" and both are documented, but anyone setting an
   operation-wide object limit should know the dimension mixes heap and stack buffers.
2. **Linux charges for an operation that cannot succeed.** The wrappers precharge, then `matches`
   returns `Unsupported`. Conservative and disclosed, but a Linux caller pays 1056 bytes and an edge
   for a guaranteed failure; worth a note wherever Linux support is eventually added.
3. **Unused child allowance is silently lost.** Documented and consistent with the no-refund model,
   but a caller that over-sizes a child quietly burns the parent's share; sizing helpers will matter
   once real postcheck costs exist.
4. **Cost derivations still lack the drift-pinning test that 427 established.** `observation_cost`
   reads `BUFFER_BYTES` directly, so the byte term cannot drift — good — but the `edges: 1` and
   `objects: 1` terms are literals with no test asserting the observer makes exactly one syscall and
   holds exactly one buffer, unlike `account_full_retry_and_owned_home_fit_exact_precharge`. A
   counting assertion would close that gap cheaply.
