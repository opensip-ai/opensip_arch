# Independent review — proposed clock sampling policy 300

**Standing:** policy critique of frozen `clock-observation-proposal-wip-300-r1`. This is a **new, unselected** producer rule for turning `opensip_platform::ClockObservation` into S4's integer `(W, M, B)`. It is not native implementation, OS qualification, current authority, or cumulative approval. Work 301 is stated to compose **recorded** observations only and **does not adopt** this policy. Installed product remains `fa72e50`. Prior 298 `CLOCK-OBSERVATION.md` and 299 REVIEW were not edited.

Python 3.12.13 `-I -B`. Review-local copies only. Frozen `cases.json` / `mutation-report.json` were not overwritten.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **140092 B, 20 members, SHA256 `ec72cd974ff18ca7892ab605e70d6133561d73e88e920796270f595b0df654e0`**. Standing: proposed observation projection owner; unselected and not native qualification. Extract rehashed **20/20**. Nested 299 pin `4ab31d19…e36e` matches reviewed 299. Copied 298 `CLOCK-OBSERVATION.md` SHA256 `acfa7c71…5c56` matches the independent note. Included `kernel201.py` SHA256 `df45c9c5…2299`. Platform `clock.rs` SHA256 `610fd433…fd62`.

Independent live: model `cases()` **132 rows / 55 accepted**, byte-equal to frozen `cases.json`. 12/12 compiled controls core-equal frozen `mutation-report.json` (SHA256 `9a10c389…cafb`). Frozen cases/mutants not overwritten.

---

## What is proposed

Security consumes a **fresh** `observe_clock()` sample (platform already rejects boot change and reversed monotonic brackets) and applies a **fixed**, non-flag policy:

1. Inclusive sleep-inclusive span ≤ **1_000_000_000 ns**. Wider → unavailable. No wall-only fallback.
2. **W** = `wall_unix_seconds` (nanos validated in `[0,1e9)` then discarded). Year 0001–9999 unix range `[-62135596800, 253402300799]`, matching `timestamp_seconds`.
3. Convert before/after to wide nanoseconds; **midpoint** = `before + floor(span/2)`; **M** = `floor(midpoint/1e9)` fitting nonnegative signed i64.
4. **B** = platform-normalized lowercase UUID. No substitute sample after failure. Historical replay uses **stored** W/M/B, not a new OS read.
5. Sample formation only. S4 order, 24 h future, 90 d horizon, in-session continuity, and S6 remain separate owners. No new public diagnostic.

The model is a pure projector. Passing it does not prove suspend, scheduling, boot identity, namespace, or trusted-kernel facts.

---

## Kernel boundary

**No silent change to S4/S4.5 arithmetic or closed Anchor shape.** Kernel `clock_decision` still takes `{wall: ISO, mono: i64 seconds, bootId: str}` and still uses `FUTURE_TOLERANCE_S = 1 d`, `UNATTESTED_FORWARD_HORIZON_S = 90 d`, `SESSION_DEVIATION_TOLERANCE_S = 1 d`, and `expected = anchorWall + (M − anchorMono)`. The proposal does not alter those constants or add raw-sample fields to the 125 schemas.

What **is** new is the **producer mapping** into those integer inputs (the three gaps named in 298 `CLOCK-OBSERVATION.md`). Historical stored integers replay as-is. A later adapter that used a different M derivation would only affect **new** samples; in-session `M` is still required nondecreasing because `observe_clock` orders `after ≥ before` and successive reads have `before_new ≥ after_old`.

The model returns integer `W`, not ISO. An adapter **must** format W with the same codec as `timestamp_seconds` (every day 86400 s, years 0001–9999). That is adapter law, not a kernel change.

---

## Findings

### 1. One-second bound — unselected number, weak stated rationale

The bound is an explicit **new design choice**. It is **not** derived from S6's 10 s stall (`REVOCATION_OBSERVATION_BOUND_S`, elapsed **between** samples) and must not be confused with it.

The stated rationale — “matching the retained clock's whole-second precision” — does **not** entail 1 s. Whole-second **outputs** are compatible with a 10 ms or 100 ms collection bound; they do not require allowing a full second of placement uncertainty. Worst-case error under this policy is about **0.5 s** (half-span) **plus <1 s** (floor of midpoint) on M, and <1 s of discarded wall nanos on W. Relative to S4's 24 h / 90 d constants that is negligible, so **1 s is not an S4-safety defect**. It **is** an availability/qualification number sold with the wrong derivation.

Sleep-inclusive monotonic plus a 1 s ceiling means **preemption or suspend during the four syscalls** makes the sample unavailable. That is the correct uncertainty bound and a real availability cost. The proposal correctly defers measurement to platform qualification; until that measurement exists, **1 s is not freeze-ready as a derived constant**. It is a reasonable unselected candidate only if restated as “comfortably below S4 thresholds, pending load/suspend measurement,” not as a consequence of one-second fields.

Inclusive `span <= 1e9` (vs exclusive) is the right tie for “one second”; the exclusive mutant over-refuses `bracket/*/1000000000`. Keep inclusive if 1 s is kept.

### 2. Floor-second W and midpoint M — defensible shape

Floor-second W matches POSIX `timespec.tv_sec` and `clock.rs` `wall_unix_seconds` (including `wall_parts(-1, 999_999_999) → (-1, 999999999)`). Do not round-to-nearest (mutant `round-wall-to-nearest` caught) and do not reconstruct a float. Calendar bounds equal `timestamp_seconds` for `0001-01-01T00:00:00Z` and `9999-12-31T23:59:59Z` (independently computed).

Midpoint-then-floor is the right **minimizer of worst-case monotonic placement error** inside the bracket. Averaging already-truncated endpoint seconds is wrong (`before=0.9s, after=1.1s` → truncated average 0, nanosecond midpoint 1.0). Endpoint selection is a different policy and is caught. Integer `before + span//2` then `// 1e9` is well-defined for nonnegative Duration. Native adapters **must** use checked wide (u128) nanoseconds; Python ints hide overflow that `Duration::as_nanos` would not.

B as platform-normalized lowercase UUID matches `clock.rs` `boot_id()`, which already lowercases mixed-case OS bytes. The model's rejection of uppercase is correct **if and only if** the adapter reads `ClockObservation.boot_id()`, not raw sysctl/proc bytes.

### 3. Sample freshness versus S6 — still a missing decision

S6 `observer_tick` / private `revocation.rs` `OBSERVATION_BOUND = 10s` is stall **between** freshness-monitor samples. This 1 s rule is stall **inside** one `observe_clock()` bracket. Different owners; do not merge them.

What remains unspecified: how long a **formed** sample may be held before S4 write (“owned through projection and **immediate** evaluation” is not a bound). A long evaluation that samples at start and writes later feeds S4 a stale W as part of `tEval = max(F, W, A)`. That is **not** S6's job and **not** closed by the 1 s span. Policy is still missing an evaluation/effect freshness decision.

“New sample per current evaluation; historical replay does not re-sample” is the right split.

### 4. Failure mapping — installation blocker, correctly not invented

Private `Unavailable` reasons (`sample-latency`, `wall-calendar`, `platform-boot-uuid`, …) are **not** a public diagnostic. The proposal is right not to mint one. It is also explicit that sampling unavailability must not become `PAYLOAD-NOT-ADMISSIBLE`, a fabricated P0, a lowered floor, an unowned busy retry, or a persisted refused role event.

Until host causal mapping is named against the **existing** vocabulary, this policy **cannot be installed**. That is an open requirement, not a model-test gap.

### 5. Platform / suspend / namespace — model cannot qualify

`observe_clock` does not admit mount-namespace, SIP, or current platform. Proposal leaves that to existing platform/namespace admission. Still required: the sample used for S4 must be taken **in** the admitted namespace/platform context, or W/M/B are a confused-deputy observation. Suspend/VM restore/scheduler stall are explicitly out of the pure model; qualification must include them if 1 s is frozen.

---

## Classification

**Actionable defects**

- The 1 s ceiling is **not entailed** by whole-second retained fields. Freeze text must not treat it as derived. Either qualify it as an availability bound or pick a measured number.
- “Immediate evaluation” does not specify sample-to-write freshness. That decision is still missing.

**Open integration requirements (block installation, not model bugs)**

- Public causal mapping of sampling unavailability.
- Adapter: `ClockObservation` getters only; u128 ns; ISO wall via `timestamp_seconds` inverse; no schema extras; no S4-refuse retry.
- Sample taken under admitted platform/namespace.
- Ordinary, recovery staging/BEGIN/COMMIT, S4.5, and report-only share the producer; report-only still needs a **usable** sample and still writes nothing.
- Load/suspend availability measurement if 1 s is kept.

**Reasonable unselected choices**

- Inclusive 1 s vs a tighter bound (e.g. 100 ms).
- Midpoint vs before-endpoint (midpoint is the better default if a bound exists).
- Floor-second W vs round-nearest (floor matches POSIX and `clock.rs`).
- Lowercase UUID via platform normalize vs case-insensitive compare.

**Not found**

- Silent change to S4 constants, Anchor schema, or original-proof replay of stored W/M/B.
- Confusion of this bound with S6 10 s, if the proposal's separation is kept in the adapter.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 300 pins before extract | match |
| Nested 299 / 298 note / kernel201 | match |
| Live `cases()` | 132 / 55, equal frozen |
| 12 projection controls | frozen-equal |
| S4 kernel arithmetic | unchanged |
| Public mapping / sample lifetime / 1 s freeze | **not decided** |
| OS qualification | not claimed; not proven |

---

## Verdicts

- [x] **300 as proposal:** archive/pins verified; projector 132/55 and 12/12 controls reproduce; closes the three 298 gaps **as a producer policy**; does not silently retune S4/S6 constants or schemas.
- [ ] **Not selected, not installed, not OS-qualified.** 1 s is an unselected availability bound with a weak stated derivation. Public failure mapping and sample-to-write freshness are still missing. Work 301 composing recorded observations does not adopt this policy. No implementation or qualification approval follows from the model.
