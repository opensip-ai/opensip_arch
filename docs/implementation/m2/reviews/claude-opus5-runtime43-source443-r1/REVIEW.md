# Independent source + formal review — native runtime43 / source accounted-cache-read-443

Actual Claude Opus 5, 2026-09-21. Bounded, independent. No repo edits, selection, commits, push or
delegation. I owned the serial native lane. Commands, logs and hashes are in `evidence/` and
`hashes.txt`; no compiled binaries, no native UUID or account capture in any report.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Four non-blocking observations.

## Formal, archive, staging

All three pins match (subject `6b25f2b3…` 2488 B, archive `07aac1f7…`, manifest `4047fca2…`).
12 members verify; 11 candidates = subject minus record, pin-identical; 3 sorted parents (owner-406,
runtime-42, inventory-62), all accepted, none overwritten; no overrides; unit not in the lock;
`stage.py` byte-identical to the accepted v42 helper.

All **634** members hashed in memory — regular files only, none unsafe or duplicated, membership
equals manifest. **596** product − 1 lock = **595** non-lock = **589** unchanged + **6** mapped, all
six **existing** declared paths, zero new files, no dependency or layout change, and the archive
product set equals the live 596-file tracked set. The archive lock is the accepted **37/64** baseline
rebased onto accepted 42, equals live, retains all five inherited meanings, and is excluded from
materialization by exact path. Map, baseline and recorded stage stdout verify; my staging reproduced
634 / 595 / 6 / 589 with the live product untouched.

## `read_bounded_cost` — a calculator that is exactly tight

The design decision that makes this sound is that price derivation and the real read share one
private helper, `next_buffer(current, ceiling)`. The calculator walks the same ladder the reader
walks, so conformance is structural rather than asserted.

I checked it anyway, and more widely than the shipped tests do. My probe swept **36** `max` values —
every growth boundary plus its ±1 neighbours, plus small and assorted values — running an actual
worst-case read at each and comparing `used` against the calculation. **The calculator never
under-charged, and the minimum slack was 0 bytes.** So the bound is not merely conservative; it is
*exactly* the worst case at the boundaries. At `max = 4 MiB` it yields `objects 1, bytes 12578817`,
matching the advertised ceiling and the figure I derived independently when reviewing the reader at
runtime40.

Off-by-one and overflow hold up. Validation is parity with the reader (`max == 0`,
`max > MAX_RECORD`, `attempts == 0` all give `InvalidLimit`), `ceiling = max + 1` matches, and the
loop terminates because `next_buffer` strictly increases to the clamp. At the declared maximum the
running sum is 12578817, well inside a 32-bit `usize`; the source comment hedges "on supported
widths", which is the right hedge.

The `edges: attempts` term is honestly described. My probe confirmed a one-byte-at-a-time reader
needs 8193 attempts at `max = 8192` against a 2-attempt reservation, so `attempts` is a caller's
limit and not a completion promise; reserving too few refuses **through the ledger** and latches
rather than silently truncating, and an `attempts` value above the global cap is likewise refused by
the ledger before any callback. `WorkCost::checked_add` becoming public is pure arithmetic —
`usize::MAX` attempts compose to `None` rather than wrapping.

The doc is careful in the way that matters: a pure calculation reserves nothing, closes nothing and
grants no authority, and an active owner still owes guarded propagation of its refusal.

## `capture_accounted` and the generic `capture_in`

`capture_accounted` checks `shared.is_none()` and refuses `Error::Profile` **before** reaching
`capture_in`, so a legacy owned budget is refused even on the cached shortcut — which is the right
call, since an owned budget would otherwise let some captures skip shared accounting entirely. The
typed `E` flows through the generic `work` accepted at runtime41. Ordering inside `capture_in` is
unchanged where it matters: `available` → cache shortcut only when `!presence` → callback →
non-empty/cap → digest → `retain`, and `retain` still charges object and bytes **before** `Arc::from`,
once per key. Presence semantics are preserved by construction: `presence = true` bypasses the cache,
so a hit can never masquerade as fresh presence.

One change is a real improvement rather than a refactor. The old legacy path did
`capture(cap).map(Arc::from)` and then `retain` allocated a *second* `Arc` from the same bytes — an
intermediate allocation that was never charged. Making `capture_in` generic over `R: AsRef<[u8]>`
lets the `Vec` pass through borrowed, so the charged allocation is now the only allocation. That
makes the accounting match reality, not just tidier code.

`self.guard(…)` became `self.scope(…)` for the same necessary reason as runtime41 — `guard` fixes
`E = Error` and cannot serve a generic `E`, while `scope` already carries the `E: From<Error>` bound,
so the RAII guard and `closed()` entry check are preserved rather than weakened. Nested guards
(`capture_in` → `work` → platform `scope`) all latch the one ledger, so a caught nested failure still
yields `Closed` and releases nothing.

## Replay

**24** reader integration, **13** ledger integration, **5** new accounted-capture, **4** existing
retained-cache and **3** existing typed-work tests all pass, and `check --workspace --all-targets` is
clean with **zero** warnings. I did not repeat the full security suite: root ran it at 442 (404
passed, 2 pre-existing ignored) and no finding of mine justified a repeat.

## Limits

This remains composition foundation. No native capture adapter is rewired, and no ACL or descriptor
cost qualification follows — this review runs no ACL experiment. The callback owes its own read and
postcheck costs; arbitrary callback internals are not automatically bounded, and a pure calculator is
not a reservation. No creator, P0 or current authority; no Linux, release, power-loss, full M2 or
M2–M6 completion; existing law unchanged. As the request notes, the runtime42 claim is the specific
API one — new bytes and the pending outcome stay private until checks — not a general no-output
authority over an arbitrary callback, which can still mutate captures or do external I/O. Root
substantive assent and guarded private/live integration remain required.

## Acknowledging root's ACL444 qualifications

Read separately, and I accept all five. The 413 draft does **not** erase the NOACL distinction —
`Acl` stores `explicit_no_acl`, derives `PartialEq`/`Eq`, and an existing test distinguishes all
three cases; everything is module-private, so in-module consumers can read the field. My "concrete
defect" was **overstated**; an accessor is merely sensible if the adapter later crosses a module
boundary. I also should not have carried the SDK comment's Windows "deny-all" gloss into a macOS
semantic. My selected-code claim about `descriptor_acl` was stronger than my evidence: I did not
inspect filesec or kernel behaviour, and fgetattrlist omission is not the same observation as filesec
property absence, so it is an investigation target, not a demonstrated defect. `ATTR_CMN_ACCESSMASK`
file-type bits and the directory links/size mapping need source verification — a missing mapping is
not proof no route exists, so "not reconstructible" should have read "not obviously reconstructible".
And "all fixed-buffer blockers are resolvable in-repo" was too strong while absence and directory
metadata remain open; root's point that refusing every ordinary no-ACL directory could make creation
unusable is well taken — refusal is honest but is not the required product behaviour. The original
advice stands as written; these are corrections to it, not edits of it.

## Observations (non-blocking)

1. **Zero slack is by design but leaves no headroom.** Because the calculation is exactly tight at
   growth boundaries, a caller reserving precisely `read_bounded_cost(max, attempts)` has nothing
   spare for anything else on that allowance. The docs point at `checked_add` for composition; worth
   knowing before sizing helpers are written.
2. **`attempts` is unvalidated against the global cap**, so a caller can compute a cost that can never
   be charged. My probe confirms the ledger refuses it before any callback, which is the honest
   behaviour, but there is no early diagnostic separating "impossible reservation" from "exhausted
   budget".
3. **`capture_accounted` latches on the legacy-owned refusal.** Consistent with the `InvalidLimit`
   pattern, but as at runtime40 and 42 it means a caller or configuration error closes the shared
   operation rather than reporting a distinguishable misuse.
4. **The removed intermediate `Arc` is worth recording as a correctness gain, not just cleanup** — it
   was an allocation that happened without being charged, so the change brings the ledger into line
   with what actually executes.
