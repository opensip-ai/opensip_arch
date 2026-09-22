# Independent source + formal review — native runtime39 / source account-work-427

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Bounded and independent. No product or architecture edits, no selection, no commits or push, no
delegation. I owned the serial native lane and used it. All outputs are under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime39-source427-r1`. Prior review evidence is
untouched. No native account details are printed here or in my archived logs, and no compiled
binaries are archived.

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Five non-blocking observations follow.

## Frozen inputs

| Input | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `native-runtime-selection-v39-subject.json` | 2456 | `5cb991bb…d201d70` | matches pin |
| `trials/account-work-427/subject.tar.xz` | 6937256 | `60b171a3…bb0bf6e3` | matches pin |
| `trials/account-work-427/subject.json` | 127453 | `aaed2f7f…80c1a097` | matches pin |

Product is clean at `080bc8e` with the lock at 36 inventory / 60 contract successors — runtime38 is
integrated as stated.

## Formal and staging

All 12 members verify byte-for-byte, sorted and unique. Replaying the current
`tools/verify_design.py` `contract_successor` rules: the record is a subject member with a matching
pin; the **11** candidates are exactly the subject minus the record with pin-identical rows; the
**3** parents are sorted, unique and all in the accepted set (15591 paths) — owner-406, runtime-38
and inventory-61 — and none is overwritten; no candidate reuses an accepted path; `passageOverrides`
is empty; no `previousCandidate`; only the expected five record fields; unit not yet in the lock.
`stage.py` is byte-identical to the accepted v38 helper.

All **682** archive members streamed and hashed in memory: every one a regular file, no absolute,
traversal, backslash or non-canonical names, no duplicates, symlinks or devices, membership equal to
the manifest. Layout is 1 `README.md` + 87 `evidence/` + **594** `product/`. The split reproduces
exactly — 594 − 1 lock = **593** non-lock = **589** unchanged + **4** mapped — and the four mapped
paths are precisely the declared platform files, all **existing** (zero new files). The archive
product set equals the live 594-file tracked set, and the archive lock is the accepted 36/60 lock,
excluded from materialization by exact path. Map `before`/`after`, the 589 unchanged rows, the
594-row baseline and the recorded stage stdout all verify.

## The reserved-scope boundary

`ReservedPostchecks::scope` is a new public method that wraps a borrowed helper callback in a private
`ReservedScope` RAII guard. The shape is the same three-arm match already accepted twice in this
series: entry check on `ledger.failed`, `Ok` with a clean ledger completes, `Ok` with a latched
ledger becomes `Closed`, and `Err(error) => Err(error)` preserves the caller's original error. The
`Drop` sets `ledger.failed = true` on any unsuccessful exit, so an error or an unwind closes the
original ledger even when an outer callback catches it.

`spend` is refactored onto this boundary — previously `self.ledger.scope(|_| …)`, now
`self.scope(|s| …)`. The observable behavior is unchanged: both paths refuse on a failed ledger, both
latch on an overspend, and neither touches `used`. The refactor also removes the disjoint-field
capture the old form relied on, which reads better. No allowance is refunded, replaced or exposed.

I verified the claimed invariants from outside the crate, against the built rlib, without touching
the staged tree:

| Probe | Expectation | Result |
| --- | --- | --- |
| nested helper `scope` + `spend` | must compile **and** account correctly | **exit 0**; executed, `used().edges == 3` after effect(1)+postchecks(2) with a helper `spend(1)` — **no second charge** |
| cross-owner reserved-scope swap | rejected | **E0521** — borrowed data escapes outside of closure |
| return the reserved scope through `T` | rejected | lifetime may not live long enough |
| forge a `ReservedPostchecks` | rejected | **E0451** — both fields private |
| read `remaining` | rejected | **E0616** — field is private |

The last two are the ones that matter for the claim that the allowance stays private and
non-constructible, and the runtime execution of the control is what actually demonstrates "no double
charge" rather than merely asserting it.

The framing in the source README is accurate and worth preserving: the existing `effect` guard
already caught errors escaping the *whole* callback; this is the analogous **nested** boundary for
helper failures caught *inside* that callback. It does not claim the old API observed arbitrary
hidden failures, and failures outside any guarded boundary remain unobservable.

## The account reservation

`account.rs` is **purely additive** — zero removed lines — so `observe_account`, `observe_with`,
`lookup_home`, `credentials` and `os_lookup` are byte-for-byte unchanged. That alone disposes of most
regression risk.

I re-derived the constant from the algorithm rather than trusting the comment:

```rust
let calls = (MAX_BUFFER.ilog2() - INITIAL_BUFFER.ilog2() + 1) as usize;  // 16 - 10 + 1 = 7
objects: calls + 1,                                    // 8
edges:   calls + 4,                                    // 11
bytes:   2 * MAX_BUFFER - INITIAL_BUFFER + MAX_BUFFER - 1,  // 195583
```

`lookup_home` allocates a **fresh** `vec![0u8; size]` per attempt and doubles from
`INITIAL_BUFFER = 1024` while `size < MAX_BUFFER = 65536`, so the visited sizes are exactly
1024, 2048, 4096, 8192, 16384, 32768, 65536 — **seven** allocations totalling **130048** bytes, and
**seven** `lookup` calls. `home_from_buffer` makes one `to_vec()` of the NUL-terminated slice inside
that buffer, so the owned home is one object of at most `MAX_BUFFER - 1 = 65535` bytes.
`observe_with` samples credentials once before and once after the lookup, and `credentials()` is
`getuid` + `geteuid`, giving **four** credential API calls. So 7 + 1 = **8 objects**,
7 + 4 = **11 edges**, and 130048 + 65535 = **195583 bytes**. The bound is exactly tight for the
worst case and conservative for every shorter path.

What keeps that derivation from drifting is a test, not a comment:
`account_full_retry_and_owned_home_fit_exact_precharge` asserts both
`(objects, edges, bytes) == (8, 11, 195583)` **and** `(samples, calls, requested) == (2, 7, 130048)`,
with the observed home length pinned at 65535 and `owner.used() == full`. If `observe_with` ever
added a third credential sample or `lookup_home` changed its retry ladder, that test fails. This is
the right way to hold a hand-written bound to a real algorithm.

Ordering is correct in both wrappers. `observe_account_in` uses `WorkScope::run`, which charges
before invoking the action, and `observe_account_in_reserved` spends from the allowance before
calling `observe_with` — with **no second outer charge**. The refusal test panics from inside both
the sample and the lookup callbacks, so a refusal that reached the OS would fail the test; each
insufficient dimension refuses with `used() == default` and the owner latched. Original
`AccountObservationError` values are preserved inside `WorkFailure::Operation`, and unused
reservation is never refunded.

`lib.rs` adds three `cfg(macos|linux)`-gated exports — `account_observation_cost`,
`observe_account_accounted`, `observe_account_reserved` — alongside the existing account exports.
`observe_account` itself is untouched, and there is no environment-home fallback and no
supplied-observation public factory.

## Native replay (mine)

Staged with the frozen helper to my own fresh directory, reproducing the recorded counts exactly —
682 / 593 / 4 / 589, `liveProductUnchanged: true`, exit 0 — with the live product still clean at
`080bc8e`. Then with pinned Rust 1.95.0:

| Run | Result |
| --- | --- |
| `--lib account::` | **12 passed** |
| `--lib work_ledger::` | **6 passed** |
| `--test work_ledger_tests` | **7 passed** |
| `--doc work_ledger::` | **2 passed** |
| `-p opensip-security --lib retained_shared_ledger_` | **4 passed** |
| `check --workspace --all-targets` | exit 0, **zero** warnings |

Test counts move 6 → 12 in `account.rs` and 3 → 7 in `work_ledger_tests.rs`, matching the claimed
6 new account cases and 4 new integration cases. The 6 ledger unit tests and 2 doc cases were offered
as *historical* 424/426; I reproduced both fresh, and I wrote my own boundary probes rather than
replaying the author's. No full platform, filesystem or security suite was needed, and none is
claimed. My captured logs were scanned for account identifiers and home values before archiving;
none are present.

## Evidence, attribution and limits

- **Mine:** staging, six cargo runs, five external boundary probes (one executed at runtime), and
  read-only Python checks over the formal subject, the whole archive and the map/baseline. Exact
  commands, environment and raw logs preserved.
- **Author, historical 424/426, not replayed by me:** the 4 external negative compiler cases
  (E0308/E0521/lifetime/E0451) and the 426 platform-file runs. I reproduced the same *class* of
  guarantees with independently written probes.
- **Author, fresh 427:** 12 account, 7 integration, 4 shared-cache and workspace — all four
  reproduced independently here.
- **Evidence only, not reviewed or approved:** the 425 generic reader experiment. It is not selected
  source and I did not assess it.
- **Limits I am holding to.** The counters bound **requested caller-owned storage and API call
  counts only** — not allocator overhead or RSS, not opaque OS or name-service allocations, not
  latency, and not OS cache or network effects. Those remain separate qualified native profile and
  TCB premises. The raw observer queries the real UID and *reports* the effective UID; a creator must
  still require equality, recheck originals and admit home custody. A later 4096-byte creator path
  limit cannot retroactively reduce the 65535-byte home copy already charged here. These wrappers
  supply no InitialActor, core, profile, home-base, custody, permit, stage/P0, current authority,
  native creator or public ingress, and existing raw-observer error exits are not all
  creator-required postchecks. macOS development evidence only; no Linux, release, crash or
  power-loss qualification. No M2 or M2–M6 completion. Root substantive assent and guarded
  private/live verification remain required before selection.

## Non-blocking observations

1. The reservation charges **cumulative requested** bytes, not peak live bytes: 195583 is charged
   although at most ~131071 bytes are ever live at once, since each retry buffer is dropped before
   the next is allocated. That is the right direction for a work ledger, which accounts work done
   rather than residency — but it is worth stating plainly so nobody later reads 195583 as a memory
   high-water mark.
2. `observe_account_reserved` spends the full worst-case cost regardless of how few retries actually
   occur, and never refunds. A caller reserving for N observations must therefore reserve N × cost
   even if most succeed on the first buffer. Documented as "no refund", but the budgeting implication
   deserves a line wherever callers are eventually written.
3. Public API grows by three `cfg`-gated account items plus one method on the already-exported
   `ReservedPostchecks`. The README's "no public authority constructor" is accurate, but it does not
   mention the surface growth; a future reader comparing exports should not be surprised.
4. The `edges` dimension now carries two different notions on one shared ledger: native API call
   counts here, and traversal steps in the retained security cache accepted at runtime38. Both are
   legitimate "work units", but whoever sets operation-wide limits should know the edge budget is
   consumed by two unrelated things, or a generous traversal will starve the account reservation and
   vice versa. This is a limit-setting consideration, not a defect.
5. `account_observation_cost`'s `+4` edges and `+1` object are numeric literals rather than derived
   terms. That would normally worry me, but
   `account_full_retry_and_owned_home_fit_exact_precharge` pins `(samples, calls, requested)` against
   the real algorithm, so drift fails a test rather than silently under-charging. Keep that assertion
   if the test is ever refactored — it is what makes the constant trustworthy.
