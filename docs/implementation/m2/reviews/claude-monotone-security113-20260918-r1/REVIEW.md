# Independent bounded review — monotone-state security group in frozen 113

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Subject: frozen `first-flush-regression-checkpoint-113`. Scope, read in full:
`crates/security/src/trust_time.rs` (582 lines: clock kernel `assess`, `Assessment::finish`,
`timestamp_seconds`, tests), `crates/security/src/revocation.rs` (340 lines: `bounded_read`,
`FreshnessMonitor`, tests), and in `trust.rs` `observe_revocation` with the types it consumes plus
`RevocationEvidence`, `revocation_shape`, `verify_revocation` as supporting interfaces (l.4418–4800).
Expected semantics: frozen reference107. No frozen/selected/product edit; scratch builds and mutants
only; no commit, push or delegation.

## 1. Subject verification

Reused my firstflush113 extraction **after rehashing it against the tar**: archive
`c9261341996b619daf60628246aef8952b5e9763dc695f836e6c38723db9c253`, 346/346 members re-read from the
tar and compared byte-for-byte with the extraction (`mode: re-verified`, before and after this work);
330/330 product pins were verified in that review. Sources read:
`trust_time.rs` `86d5ea1c…12a6bd`, `revocation.rs` `27ab287b…b9b0`, `trust.rs` `f0d0f3a8…a3b8`
(unchanged since 112). Reference107 model `2f4bd78f…4037` from my own verified 107 extraction.

## 2. What these three pieces are, and their standing in the code

All three are **pure, private and have no production caller**: `assess` is called only by its tests,
`observe_revocation` only by its test, `FreshnessMonitor` only by its tests
(`timestamp_seconds` *is* used by root, chain and recovery code). They propose; none persists a
floor, reads a counter on its own, appends a journal record or grants anything. Inputs are typed
assertions: `Observation`/`Record`/`Payload` for the clock; `EpochAtStart`, `ClosureSubjects`,
`current_policy`, `allowed`, `required` for revocation. The one input that is *not* a caller assertion
is the revocation document: `observe_revocation` takes version and entries from a `RevocationEvidence`
that only `verify_revocation` constructs (shape-checked, root-version-bound, quorum `Met` after
filtering revoked keys) — so its `unwrap()`s on the payload are covered by `revocation_shape`.
The native clocks behind `FreshnessMonitor::read` are `mach_continuous_time` / `CLOCK_BOOTTIME`
(sleep-inclusive, as reference107's observer obligation names); I looked that up as context and did
**not** review `opensip-platform`.

## 3. Evidence

**Frozen fixtures recomputed from 107 with my own projection**: clock 1,833/1,833 equal; revocation
observation 1,920/1,920 equal.

**Differentials on my own cases** (probes inserted in a scratch copy, `catch_unwind` around calls):

| Kernel | Cases | Result |
|---|---|---|
| `assess` (boundary-biased: ±1 s around 1 d / 14 d / 90 d, boot change, malformed/negative mono, null and absent expiries, report-only, fresh install) | 120,000 | **120,000 identical projections** (refusal, evaluation, admitted, plausibility, witness, continuity, findings, all three write proposals, advance, states, freshness); 0 panics; 0 untyped reference exceptions |
| `timestamp_seconds` (every month/day class over 323 years incl. 1, 1582, 1900, 2000, 2100, 9999; 30,000 random fields; 1,500 single-character corruptions incl. Arabic-Indic/full-width digits, NUL, newline) | 49,932 | **0 differences**; the 38,942 accepted values also equal `calendar.timegm` |
| `observe_revocation` (version order incl. i64 max, 4 subject kinds, policy digests, duplicate/absent grants, `required = null`) | 60,000 | 59,665 identical; **335 differ, all one cause — M-1** |
| `bounded_read` with genuine intervals (`before ≠ after`), boot changes, empty boot, overlap | 40,000 | 40,000 equal to my restatement of the rule |

**Mutation** (`probes/mutation.py`; 45 mutants, all compiled, baseline green; then each survivor re-run
against my corpora — `probes/survivors.json` — so that "survived" is separated from "equivalent"):

| Area | Killed | Survived | Survivors that change behaviour on my corpus |
|---|---|---|---|
| clock kernel | 12 | **12** | **12 of 12** |
| `observe_revocation` | 8 | 0 | — |
| freshness monitor | 8 | **5** | 4 of 5 on `bounded_read`; the 5th needs `read_with` (pinned below) |

## 4. Findings

No defect found in the Rust semantics of this group. The findings are one reference mismatch and
test adequacy.

### M-1 (reference107 defect, unowned mismatch) — `str(None)` matches a revocation entry

`revocation_observe`: `k == 'catalogSnapshot' and s == str(closure.get('catalogSnapshotVersion'))`.
When the closure has **no** snapshot version this compares with the Python text `'None'`, so a signed
entry `{subjectKind: catalogSnapshot, subject: "None"}` REVOKEs every operation without a catalog
snapshot. The entry is reachable (`subject` is any 1–256-scalar string in both schema and Rust).
Rust uses `catalog_snapshot.is_some_and(...)` and does not match — Rust is right, the reference is
wrong, and the divergence is silent: the frozen fixture cannot contain it because its 1,920 cases all
reuse one fixed signed document (`mask:7:revoked:0`, version 2, four entries). 335 of my 60,000 cases
hit it; there is no other difference. Needs an owner disposition in the reference (compare only when
the version is an integer), not a Rust change.

### T-1 (medium) — the clock fixture does not pin twelve decisive rules, including fail-open ones

12 of 24 clock mutants survive `matches_proposed_reference_clock_projection`, and **every one** changes
results on my corpus. `probes/fixture-coverage.json` explains it exactly — the 1,833 frozen cases
contain **zero** instances of each situation:

| Surviving mutant | My cases changed | Fixture cases exercising it |
|---|---|---|
| evaluation ignores admitted time (`tEval = max(floor, wall)`) | 17,245 | 0 with admitted > max(floor, wall) |
| **absent root expiry ⇒ not expired** (fail-open) | 13,129 | 0 proceeding with no effective `rootExpiresAt` |
| negative `mono` admitted | 10,930 | 0 negative `mono` |
| **presented-root future check removed** | 3,336 | 0 with `presentedRootIssuedAt` > wall + 1 d |
| **payload's explicit null expiry ignored** (record value kept) | 1,862 | 0 proceeding with a null expiry member |
| older-witness boundary `<=` | 991 | 0 at `lastAccepted` / −1 |
| root expiry strict `>` | 900 | 0 with evaluation == expiry |
| payload-future boundary `>=` | 540 | 0 at wall + 1 d |
| floor-ahead `>=` | 420 | 0 at wall + 90 d |
| warning window strict | 382 | 0 at exactly 14 d |
| fresh horizon `>=` | 105 | 0 at admitted + 90 d |
| excuse requires witness `>` expected | 7 | 0 with witness == expected |

Because `assess` has no caller, the fixture is the *only* thing that ties this kernel to S4. Today a
regression that lets evaluated time ignore the newest signed time, treats a missing root expiry as
"not expired", or lets a payload fail to clear an expiry would pass the suite. My 120,000 cases carry
107-derived expectations in the fixture's own format (`probes/clock-mine.ndjson`); a few dozen chosen
from the twelve rows above would close this.

### T-2 (low) — freshness monitor: interval semantics are tested only with point samples

Every owner test uses `before == after`, so four mutants that matter only for real intervals survive:
elapsed measured from the previous read's **end** (560 of my cases change), elapsed measured to the
current read's **start** (364), a previous-boot change tolerated (516), an empty boot id tolerated
(54). The fifth — `read_with` storing the *end* of a read as the next baseline — needs a sequence; the
test in `probes/read_with_pin.py` (read 1 spans 0–3 s, read 2 spans 9–11 s ⇒ `Stalled(11 s)`) passes
on the frozen code and fails on that mutant. The rule itself is the right one: the previous counter
value may be as old as the earliest instant of its read and "now" as late as the latest instant of
this one, so `end.after − previous.before` is a sound upper bound and never under-reports a stall.

### Notes

- **N-1** `FreshnessMonitor` latches on every `Err`, but a **panic** in the counter callback unwinds
  past `self.stop.latch()`. Under `catch_unwind` upstream the session is left un-latched (the next
  read still stalls out after 10 s). Belongs with R-3; state the panic policy for callbacks.
- **N-2** The first `read` bounds only its own duration; nothing ties it to when `EpochAtStart` was
  captured. That is a caller obligation and should be written next to `EpochAtStart`.
- **N-3** Rust returns `Error::Arithmetic` where the reference cannot overflow at all (ISO years
  1–9999); correct and tested once. `HORIZON` serves both the 90-day forward horizon and revocation
  freshness; the reference also defines one from the other, so this is faithful, not a conflation.
- **N-4** `timestamp_tests` asserts `n > 7900` and the clock replay an exact 1,833; same remark as 112
  N-3.

## 5. Not examined

`opensip-platform` clock code (context lookup only); `commit_authority.rs` (`StopObserver`,
`PreparedAttempt`) beyond the four calls the monitor makes; `verify_envelope` / quorum filtering
behind `verify_revocation` (covered by my 106/112 reviews of other deltas, not re-read here); the
Linux half of `platform_decision`; R-1/R-2 carrier composition; journal, custody, final gate, native
groups. No Linux/x86_64 lane, no dependency or OS qualification. The 335-case mismatch was driven
through a scratch-only probe that replaces the entries of a genuinely verified evidence inside the
module; production code outside the module cannot do that.

## 6. Bounded verdict

**Monotone-state group in frozen 113 (`trust_time.rs`, `observe_revocation`, `revocation.rs`):
reviewed; no blocking finding and no Rust departure from reference107 except M-1, where reference107
is the defective side. T-1 should be closed before anything calls `assess`; T-2, N-1, N-2 are small.**
This is not approval of the signed-security group as a whole, of any caller that will persist these
proposals, or any cumulative, target, dependency or current-authority qualification.

Evidence: `claude-out/pin-reverification.json`, `source-hashes.txt`, `probes/*` (generators, corpora,
Rust results, `mutation.{py,json,log}`, `survivors.json`, `fixture-coverage.json`,
`observe-diff-analysis.json`, `read-with-pin.json`), `hashes.txt`.
