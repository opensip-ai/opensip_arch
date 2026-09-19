# Independent bounded review — revocation reference 116 and monotone corrections 117

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-18. Request: `REQUEST.md`.
Two subjects, two verdicts. Scope: the corrections to my monotone-security113 findings only. 116
inherits reference 111, which has its own review (F-1 to F-4 there remain open); nothing here accepts
111, callers, integration, Linux, R-1/R-2/R-3, OS, dependencies or release. No frozen/selected/product
edit; scratch copies only; no commit, push or delegation.

## 1. Subject verification (both, before extraction)

| | 116 `revocation-reference-checkpoint-116` | 117 `monotone-corrections-checkpoint-117` |
|---|---|---|
| Archive | 2,034,652 B, `1007f7943dc96aa874af64482a08500324c86015bc548907e3ef55cb642efa4a` | 4,108,448 B, `b0501a24280f839c23e7e86ffc1a59cf74f8eabf8f18c9c562ebb33c3e56a2cc` |
| Members | 1,356/1,356 equal to manifest from the tar; 0 unsafe/extra | 456/456; 0 unsafe/extra |
| Pins | 1,284/1,284 candidate pins | 330/330 product pins |
| Parent | equals **my** verified 111 extraction (1,284 files) | equals **my** verified 114 extraction; 326 unchanged |
| Delta | model (1 condition), checker (+1 sweep), envelope binding and five pin inventories | `revocation.rs` +96/−0, `trust.rs` +4 (comment), `trust_time.rs` two count literals, `trust-clock-cases.ndjson` |

Both re-verified after the work (`mode: re-verified`), this time with bytecode writing disabled.

---

## 2. Reference 116

**Delta read in full.** `revocation_observe`: the `catalogSnapshot` arm now requires
`type(closure.get('catalogSnapshotVersion')) is int` before comparing with its decimal text. New
mandatory sweep `catalog-revocation-requires-present-integer-version` (24 checks). No clock change.

**Owner checks reproduced, required order, fresh output**: envelope receipt 168 / 145 / 1,803 / 6,000
passed → integration **423 / 0** with that receipt → security **581 / 0, 19 sweeps**, new sweep 24.

**My 60,000 cases re-executed against 116**: exactly **335** outcomes change relative to 107 — the
M-1 set — and against my retained 113 Rust outputs there are **0** differences in action, reason or
match count. I then went further than the owner could: a **new Rust execution** on 117 (whose
`observe_revocation` is unchanged) with 116-derived expectations and **full match-list comparison**:
**60,000 / 60,000 equal**.

**Value types** (`probes/observe116.json`): absent, `None`, `"7"`, `True`, `False`, `7.0`, `[7]` match
nothing; `7` matches only `"7"`; `0`, `-7`, 2⁶³−1 match their decimal text. **Precedence**: a lower
counter never revokes even with a matching entry and a lost grant; at a higher counter
`trust-revoked` precedes `policy`; at an equal counter entries are ignored and `policy` decides;
`required = None` suppresses the policy arm.

**Signed-entry reachability.** Unchanged by 116: `subject` is any 1–256-scalar string in the schema and
in Rust `revocation_shape`, so a genuinely signed `{catalogSnapshot, "None"}` entry is admissible —
which is why M-1 mattered and why the fix belongs in the predicate rather than in the entry grammar.

**Mutation** (owner sweep called directly; no pin gate in the path): old stringification,
`isinstance(int)` (admits `bool`), `is not None`, and "never matches" are all **killed**;
numeric comparison (`"07"` would match 7) **survives**.

### Findings — 116
- **N-1 (low)** — add one non-canonical decimal negative (`"07"`, `"+7"`, `"7 "`) to the sweep; Rust
  compares text and already refuses these (in my corpus), so the reference is right and merely unpinned.
- **N-2 (note)** — 2⁶³ and above match in the reference and cannot be represented by Rust's `i64`
  closure field; negative and zero versions match in both. Whether a catalog snapshot version may be
  ≤ 0 or exceed i64 is closure admission, which the sweep's own note leaves to the caller. Say which
  owner bounds it.

### Verdict — 116
**Reviewed; monotone113 M-1 is closed.** The reference now agrees with Rust on all 60,000 of my cases
including full match lists. N-1/N-2 are small. This is not acceptance of inherited 111.

---

## 3. Rust 117

**Delta read in full.** `StopOnUnwind(StopObserver)` latches in `Drop` when `thread::panicking()`;
`read_with` installs it after the already-stopped early return. Tests: interval bounds, the two-read
0–3 s / 9–11 s sequence, a three-position unwind test. `trust.rs`: a four-line caller obligation above
`EpochAtStart`. Exact counts 1,856 and 57,524. No production change to `assess`, `bounded_read`,
`timestamp_seconds` or `observe_revocation`.

**Scratch build**: security **67 passed / 0 failed**; strict clippy clean.

**Fixture**: the 114 file is an exact byte prefix; the 23 appended inputs are all from my corpus; all
**1,856** expectations recompute from the 116 model with my own projection (0 mismatches).

**All four corpora re-run on 117**: clock 120,000, timestamps 49,932, revocation observation 60,000,
monitor 40,000 — **every line equal**.

**Mutation** (`probes/mutation117.py`, dedicated target directory, baseline green, all compiled):
my **45 mutants from the 113 review plus 4 guard mutants = 49, all killed.** Each of the 17 that
survived on 113 is now killed — the 12 clock ones by the appended fixture cases, the 5 monitor ones by
the two new tests. Guard mutants: never latches / not installed / dropped immediately (`let _ =`) /
latches on every return — all killed.

**Adversarial panic and latch order** (`claude117_panic_order_probe`, scratch only):
1. a non-string panic payload (`4242u32`) propagates unchanged and the session is latched;
2. a callback panic **after** admission gives `AdmittedThenLatched` and the already-issued permit is
   still consumable — the same "late stop preserves permit" rule as an external stop;
3. a successful `read_with` executed **while another panic is unwinding** (from a `Drop`) returns
   `Ok` **and latches**, because `thread::panicking()` is true on the normal return path too;
4. the ordinary success path leaves the state `Preparing`.

### Findings — 117
- **N-1 (note, fail-safe)** — behaviour 3 above: reads made during unrelated unwinding latch the
  session although they succeed. It errs in the safe direction and only arises if a caller reads the
  monitor from a destructor; worth one sentence beside the guard so nobody "fixes" it into the unsafe
  direction. With `panic = "abort"` the guard is moot, as the comment says.
- **N-2 (note)** — the `EpochAtStart` obligation is documentation only, as stated; there is still no
  caller, so nothing enforces "same monitor, first read, before any effect". Carry it to the
  integration review.

### Closure — 117
| 113 finding | Status |
|---|---|
| T-1 twelve unpinned clock rules | **Closed** — all 12 mutants killed by the 23 appended cases |
| T-2 interval semantics | **Closed** — 5 of 5 killed, including the stored-sample mutant |
| N-1 panic in a callback | **Closed** — guard present, 4 guard mutants killed, order probed |
| N-2 first-read obligation | Documented; enforcement deferred to the caller (open by design) |
| N-4 inexact counts | **Closed** |

### Verdict — 117
**Reviewed, no blocking finding; T-1, T-2, N-1 and N-4 are closed.** Not approval of the signed-security
group, of any caller, or any target, dependency or current-authority qualification.

---

## 4. Harness incidents, preserved
- First probe run on 117 used a target directory shared with the unmodified build; cargo reused that
  binary and none of my probes ran ("67 filtered out", no output files). Detected from the missing
  files and rerun with a dedicated target directory (`probes/probe-run.FAILED-r1.txt`).
- `mutation117` r1 had a splice error (SyntaxError before any mutant ran); r2 is the run reported. One
  113 mutant's anchor no longer matched because 117 inserted the guard line beside it; re-anchored and
  run separately (`probes/mutation117_fix.py`) — killed.
- My panic probe first named a non-existent enum variant (compile error); corrected.
None of these touched a frozen or selected byte, and no compile failure or pin refusal is counted as a kill.

Evidence: `claude-out/pin-verification.json`, `pins.json`, `model116.diff`, `check116.diff`,
`*.117.diff`, `checks116/*`, `probes/*`, `hashes.txt`.
