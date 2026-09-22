# Independent source + formal review — native runtime40 / source work-reader-430

Reviewer: actual Claude Opus 5 (model identity, not a task label), 2026-09-21.
Bounded and independent. No repository edits, no selection, no commits or push, no delegation. I
owned the serial native lane and used it. All outputs are under
`/tmp/opensip-implementation/reviews/claude-opus5-runtime40-source430-r1`. Prior frozen bytes and
review evidence are untouched; no compiled binaries are archived.

**Layout acceptance at inventory62 was not source approval. This is the independent assessment of the
actual reader.**

## Verdict

**ACCEPT-DESIGN-UNIT.** `requiredFindings: []`. Five non-blocking observations follow.

## Frozen inputs

| Input | Bytes | SHA-256 | Result |
| --- | --- | --- | --- |
| `native-runtime-selection-v40-subject.json` | 2453 | `b4046feb…f1b1d168` | matches pin |
| `trials/work-reader-430/subject.tar.xz` | 6958340 | `874c6ae3…3caa3b3c` | matches pin |
| `trials/work-reader-430/subject.json` | 115477 | `cafaa7cc…f4f5100a6` | matches pin |

Product clean at `6dddbfe`, lock at **37 inventory / 61 contract** successors with
`repository-file-inventory.v62.json` selected and all **five** inherited meanings intact.

## Formal, archive and staging

All 12 members verify byte-for-byte. Replaying the current `contract_successor` rules: the record is
a subject member with a matching pin; the **11** candidates are exactly the subject minus the record
with pin-identical rows; the **3** parents are sorted, unique and all in the accepted set (15604
paths) — initial-owner-406, runtime-39 and inventory-62 — none overwritten; no path reuse;
`passageOverrides` empty; unit not yet in the lock. `stage.py` is byte-identical to the accepted v39
helper.

All **614** archive members streamed and hashed in memory: regular files only, no unsafe or duplicate
names, membership equal to the manifest. The split reproduces exactly — **596** product − 1 lock =
**595** non-lock = **592** unchanged + **3** mapped — and the three mapped paths are precisely the
existing `crates/platform/src/lib.rs` plus **two genuinely new** files, `work_reader.rs` and
`tests/work_reader_tests.rs`, which are exactly candidate-minus-baseline. The archive's
`design-lock.json` is the **historical 36/61** lock, excluded from materialization by exact path,
while the live **37/61** lock with inventory62 is preserved — `stage.py` asserts the staged lock
equals the live one. Map `before`/`after`, the 592 unchanged rows, the 594-row baseline and the
recorded stage stdout all verify.

One continuity fact worth recording: the frozen 430 `work_reader.rs` is **byte-identical** to the
unfrozen 428 draft I read while writing the 429 advice, so that analysis applies directly to this
frozen source rather than by analogy.

## The reader

`lib.rs` adds `mod work_reader;` and one `pub use` of `WorkReadFailure`, `read_bounded_accounted` and
`read_bounded_reserved`. Unlike the `account` exports it is ungated, correctly — the reader is pure
`std::io`, with no platform-specific code, matching `work_ledger`. `read_charged` and its charge
closure are **not** exported, so there is no public arbitrary charger and no way to bypass the guard.

I verified every claimed property by reading, then confirmed the numeric ones by execution.

**Bounds and validation.** `max == 0 || max > MAX_RECORD` refuses `InvalidLimit`, so the admitted
range is 1..=4 MiB. `ceiling = max + 1` cannot overflow at that bound.

**Charge ordering.** One object is charged before any allocation; each growth charges
`{edges: 1, bytes: next}` **before** `try_reserve_exact`, and non-growth turns charge `{edges: 1}`.
So every read attempt costs at least one edge and every requested buffer is paid for before it
exists.

**Growth.** `next = (empty ? 4096 : len*2).min(ceiling)`. I checked the subtraction cannot underflow:
reaching the growth branch implies `used == bytes.len()` and `used != ceiling`, hence
`bytes.len() < ceiling`, hence `next > bytes.len()`.

**Termination and prefixes.** `Ok(0)` truncates to `used` and returns — a complete result, including
the empty one. `used == ceiling` refuses `Bound`. Every error path returns `Err` and drops the
accumulated buffer, so the module's "No incomplete prefix is returned" holds on every branch; the
only `Ok` exit is the EOF path.

**Hostile readers.** `Ok(n)` with `n > bytes.len() - used` is rejected as
`io::ErrorKind::InvalidData`. That is a real defensive check, since `Read` is a safe trait whose
contract a buggy or malicious implementation can violate, and it prevents `used` from running past
the buffer.

**Failures.** `try_reserve_exact` gives typed `Reserve` rather than an allocation abort. An ordinary
IO error is returned as `Io(e)` with the original `io::Error` preserved by value. `Interrupted` loops
without returning, and the next turn charges again.

**Guards.** Both entry points wrap in `work.scope(...)` / `post.scope(...)` — the guards accepted at
runtime37 and runtime39 — so any `Err`, including an ordinary IO error, latches the original owner.

### Executed edge-case probes

Nine probe groups against the staged rlib, public API only, all passing. The numbers confirm the
charge formula independently of the shipped tests:

| Probe | Result |
| --- | --- |
| P1 exact 100 B / max 4096 | `objects 1, edges 2, bytes 4096` — 1 object, one growth (edge + 4096), one more edge for the EOF turn |
| P2 empty / max 16 | `objects 1, edges 1, bytes 17` — growth clamps to `min(4096, max+1)`; complete empty result |
| P3 nine bytes / max 8 | `Bound`, **no prefix**, owner latched |
| P4 Interrupted ×0/1/5 | edges **1 / 2 / 6** — every Interrupted retry is precharged exactly one edge, so retries are finite and budget-bounded |
| P5 reader returning `n > buf.len()` | `InvalidData` |
| P6 partial read then IO error | `PermissionDenied` preserved verbatim, no prefix, **owner latched** |
| P7 max = 0 and 4 MiB+1 | `InvalidLimit`, charges **nothing**, but the owner is latched |
| P8 reserved read vs exact allowance | `used` equals the effect reservation **exactly** — the reserved path adds nothing to `used` |
| P9 reserved read, short allowance | Budget refusal **before any read**; owner latched |

P8 is the decisive one for the "reserved path must not double charge" requirement: I set the
reservation to exactly `{1, 2, 4096}`, ran a reserved read that consumes precisely that, and `used`
came back equal to the reservation and nothing more. P4 is the decisive one for "every subsequent
read including Interrupted precharged" — the edge count moves 1 → 2 → 6 for 0, 1 and 5 interruptions.

### Native replay

Staged with the frozen helper to my own directory, reproducing the recorded counts exactly
(614 / 595 / 3 / 592, `liveProductUnchanged: true`), live product still clean at `6dddbfe`. Then with
pinned Rust 1.95.0, `--locked --offline`, fresh target dir, `RUST_TEST_THREADS=1`: **8** work_reader
integration tests, **7** work_ledger integration tests, **6** ledger unit tests and **2** rustdoc
compile-fail cases all pass, and `check --workspace --all-targets` is clean with **zero** warnings.
No security suite was needed and none is claimed.

## Scope limits, held

The counters bound **requested caller-owned buffers and read attempts only**. They do not bound
arbitrary `Read` implementation internals, allocator overhead or RSS, opaque OS allocation, network
activity or latency, and they confer no native custody. As the request states and the source
confirms, the **allocation edge also serves as that turn's read-attempt edge** — the unit does not
claim a separately counted allocator-API edge.

Most importantly: **this component alone is not native postcheck composition.** P6 demonstrates the
mechanism concretely — an ordinary IO error latches the owner *before* returning, so substituting
this reader into `directory_record_capture::read_one` would leave that function's mandatory
after-read file, directory and name checks either skipped or unaccounted. That is correct standalone
behavior and the unit says so; it is also exactly the boundary audit 429 identified and that my 429
advice and its correction analysed. Nothing here amends selected law, qualifies any native
composition, or approves the private 432 protected-callback partition, 433 typed cache errors or
combined 434 — none of which is in source430 and none of which I assessed.

No actor, core, profile, home base, creator, permit, P0 or current authority is conferred; no full M2
or M2–M6 completion; no Linux or release qualification. Root substantive assent and guarded
private/live verification remain required before selection.

## Evidence and attribution

- **Mine:** independent staging, five cargo runs, nine executed probe groups, and read-only Python
  checks over the formal subject, the whole archive and the map/baseline. Exact commands, environment
  and raw logs preserved; the probe binary was deleted after the run and only its source and output
  are archived.
- **Root evidence, attributed, not replayed:** the original 428 eight public reader tests plus
  workspace pass. Frozen 430 makes no fresh native claim and records the exact non-lock equality. I
  reproduced the eight reader tests independently rather than accepting that result.

## Non-blocking observations

1. **`InvalidLimit` latches while charging nothing** (P7). A caller passing `max = 0` or an
   over-large `max` is a programming error, not an observed operational failure, yet it permanently
   closes the shared operation ledger. Fail-closed is the safe direction and it is consistent with
   "any observed failure latches", but validating `max` *before* entering the guarded scope would let
   a misuse be a plain error without poisoning an otherwise healthy operation. Worth considering when
   callers are written.
2. **The `bytes` dimension is cumulative requested growth, not peak residency.** Charging the
   complete new buffer on every growth means a 4 MiB read charges roughly 12.6 MB cumulative while
   peak live is about 4 MiB. Deliberate, documented ("Never refund old buffers") and the right
   direction for a work ledger — but limits should be set knowing that, exactly as with the 427
   account precharge.
3. **One edge covers both the allocation and the read attempt on a growth turn.** The unit correctly
   declines to claim a separate allocator-API edge. The consequence for anyone later wanting to bill
   allocations separately is that today's edge count cannot be decomposed into the two.
4. **`WorkReadFailure` derives only `Debug`**, where `WorkBudgetError` and `WorkFailure` derive
   `PartialEq, Eq`. This is *forced* rather than sloppy — the variant holds `io::Error`, which is not
   `PartialEq` — but downstream tests must use `matches!` instead of `assert_eq!`. My own probe
   harness hit this and I adjusted it; a short doc note would save the next caller the same detour.
5. **The latch-before-return property is the composition hazard, not a defect.** It is worth keeping
   visible in the source header rather than only in the unit README, since the reader is now publicly
   exported and a future caller may reach for it inside an existing native bracket.
