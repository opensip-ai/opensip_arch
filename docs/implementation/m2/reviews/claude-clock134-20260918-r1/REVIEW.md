# Independent bounded review — Rust clock range 134

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `clock134-20260918-REQUEST.md`. Scope: the delta of frozen `clock-range-checkpoint-134` over frozen 132 —
`trust_time.rs`, `trust.rs` and three appended fixture corpora — as the Rust form of reference 133 (which I reviewed
separately today; this review depends on that one). No OS clock read, write, production admitted-record adapter or
public renderer exists or is claimed. Envelope/quorum privacy is 135, not this subject. 131 findings are separate.
No frozen/selected/product edit; scratch builds, dedicated target dirs; no commit, push or delegation. Test-only keys
have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,223,232 bytes, SHA-256 `0fa987cc62a5bc95427345a27e913bac0d64c9368480e569e9aaeb8a77562610` = request and `archive-pin.json` |
| Members | 390/390 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 132 extraction (330/330); 325 unchanged; 5 changed as stated |
| Fixtures | old bytes are **exact prefixes** of the new files: clock 1,856 → 1,892 (+36), recovery cases 867 → 871 (+4), recovery epochs 278 → 282 (+4) |
| Host pins | host82 receipt: 210 sources, all equal the product pins |

## 2. What changed (complete diffs read)
`representable_horizon(t)` = checked `t + 90 d` inside `[−62,135,596,800, 253,402,300,799]`; `Refusal::TimeRange(
RangeOperand)` with three operands; the plausibility check sits after both payload-future refusals and before the
fresh/ordinary split; retained iff `last`'s **own** horizon is unrepresentable; the continuity sum is
`checked_sub` → `checked_add` → calendar filter, so i64 overflow and calendar overflow share one operand; recovery
calls `representable_horizon(epoch.issued)` after the three signed-time refusals (which themselves follow serial and
counter checks, as in the reference) and before any write value is built.

## 3. Evidence

**Owner checks, fresh scratch:** 80/80 security tests; strict workspace Clippy clean. Owner's six mutants: report read.

**3.1 Owner's appended rows re-derived from reference 133** (`probes/owner_rows.py`): all **36/36** new clock rows
(refusal + operand, evaluation, plausibility, floor, last) and all **4/4** new recovery rows agree with my own run of
the reference; the four epochs verify at the carrier with 3 valid signers each — they are genuinely signed, and the
expectations are not projections of the Rust output.

**3.2 Cross-language corpus, 40,000 cases** (`gen_cases.py` → reference 133; `rust_probe.rs.txt`; `compare.py`):
15 boundary instants incl. both sides of `9999-10-03T00:00:00Z` and year 0001, 10 mono values to 2^63−1, optional
anchor / payload with optional expiry overrides / report-only. Every refusal class is populated (8,376 proceed;
13,236 range refusals across the three operands; 7,681 payload-future; 10,205 excursions; 306 fresh-no-context; 196
typed errors). Compared per case: refusal and operand, evaluation, plausibility, admitted time, floor write,
last-accepted write, anchor write, the three expiry **states**, advance:
**40,000/40,000 agree, 0 field differences, 0 panics; no returned instant lies outside the calendar; no range
refusal carries an evaluation or a write.** The `states` agreement over expiry members at 0001 and 9999 answers "no
accidental narrowing of expiry cut-offs". (My first comparison flagged 1,552 continuity refusals because I demanded
that the — valid, in-calendar — admitted time and limit be absent; the reference prints them too. That was my check,
not the subject; both outputs kept.)

**3.3 Recovery guard under real cryptographic input** (`gen_signed_recovery.py`: my retained R3 signing machinery
unchanged, public test-only seeds, real OpenSSL; expectations from reference 133's signed path): 11 genuinely signed
epochs — control; edge exact (`APPLIED`); edge + 1 s, maximum (`TIME_RANGE`); **wall and `issuedAt` on opposite
sides of the edge, both ways**; year-9999 epoch under a 2026 wall (`ISSUED_IN_FUTURE`); edge + 1 with every signature
corrupted (`SIGNATURE_THRESHOLD`), with a later `lastAccepted` (`TIME_BEFORE_LAST_ACCEPTED`), with a non-advancing
serial (`SERIAL_NOT_ADVANCING`); year 0001. **11/11 agree, including byte-equal proposed writes; refusals leave the
input unchanged.** Priority is preserved: a range refusal is reached only after authority, binding, serial and
signed-time checks have passed.

**3.4 Mutants** (10, all compiled, baseline green; stage 1 owner tests, stage 2 my two corpora): **6 killed** by owner
tests (guard before the signed-time refusals; 89-day horizon; hybrid retained rule; report-only exempted; range
before payload-future; continuity reported as presented). **4 survived owner tests:**
- *recovery guard tests the wall instead of `issuedAt`* — **detected by my two straddle cases**: T-1;
- *continuity maximum exclusive* — **detected by 32 rows of my corpus**: T-2;
- *horizon lower bound dropped*, *continuity lower bound dropped* — no difference on 40,000 + 11 cases either. With
  calendar-valid inputs a sum of a calendar instant and a non-negative duration cannot fall below year 0001, so the
  lower bounds are reachable only through raw out-of-calendar `i64` inputs, which the README places at the external
  input boundary. Equivalent for admitted inputs; reported as such, not as kills.

## 4. Findings

- **T-1 (low–medium) — the guard's operand is unpinned by the owner's signed rows.** All four appended epochs have
  `issuedAt == wall` or are a century apart, so substituting `observation.wall` for `epoch.issued` passes 80/80.
  With a wall of `9999-10-02T23:59:59Z` and a genuinely signed `issuedAt` one second later (inside the ±24 h skew)
  the mutant **proposes writes** whose next evaluation is a permanent range refusal with no recovery path. This is
  the same gap as reference 133 T-1(a); one signed straddle row in each direction closes both languages (mine are
  reusable: `io/signed-recovery.ndjson`).
- **T-2 (low) — continuity exactly at `9999-12-31T23:59:59Z` is unpinned.** An exclusive upper bound in the
  continuity filter passes all owner rows; 32 of my cases see it (an ordinary evaluation turns into a range refusal).
  The plausibility side *is* pinned at its inclusive edge; add the symmetric continuity row.
- **N-1 (note) — two error spellings for one overflow.** In recovery, `observation.wall ± 86,400` overflowing is
  `Input("TIME_RANGE")` while the horizon guard is `Refused("TIME_RANGE")`. The first is unreachable for a
  calendar-valid wall (the observation is shape-admitted before), so nothing is wrong today; it is worth a comment
  saying which one a caller can ever see, since the public route differs (`Input` vs `RECOVERY.REFUSED`).
- **N-2 (note, scope)** `Refusal::TimeRange` is returned as a typed value with `Withheld` advance; nothing maps it to
  `TRUST.TIME_RANGE_UNREPRESENTABLE`, a subject or a remedy yet, because no adapter or renderer exists. The 133
  notes about the closed public subject set and per-tag remedies therefore have no Rust counterpart to check. Say so
  when the adapter is written rather than assume the reference's projection carries over.

No defect found in the range logic.

## 5. Closure (Rust half)

| Item | Status |
|---|---|
| clock-range r1 K-1 / K-4 (Rust) | guard present, ordered and no-write under real signatures; cross-language agreement 40,000 + 11 + the owner's 40 rows |
| clock-range r2 F-1 own-horizon rule | **Closed** in Rust — agrees with the reference on all 11,684 plausibility refusals; hybrid rule killed |
| r2 N-3 (no erased operand; same operand for i64 and calendar overflow) | **Closed** — typed `RangeOperand`; both overflow kinds give `ContinuityExpectedWall` |
| my 129 note that Rust returned out-of-calendar instants | **Closed** — 0 of 40,000 |
| record114 `saturating_add` concern | not re-examined; the new code uses checked arithmetic throughout |

## 6. Unresolved limits
Typed kernel over supplied integers: no clock source, no persistence, no admitted-record adapter, no renderer. macOS
host only. Agreement is with reference 133, which is itself a proposal with open T-1/N-1.

## 7. Bounded verdict
**134: reviewed, no blocking finding. Rust equals reference 133 on 40,000/40,000 independently generated clock cases
(every refusal class, every printed instant, every write, the expiry states) and on 11/11 of my genuinely signed
recovery epochs including byte-equal writes; the owner's 36 + 4 appended rows re-derive from the reference; refusal
priority and the no-write property hold under real signatures. T-1 (guard operand unpinned — a signed straddle row is
needed) and T-2 (inclusive continuity maximum unpinned) are test gaps, not behavioural defects.** Not approval of an
adapter, renderer, storage, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.rs.diff`, `trust_time.rs.diff`, `owner/`,
`probes/{gen_cases.py,rust_probe.rs.txt,compare.py,gen_signed_recovery.py,rust_probe_recovery.rs.txt,owner_rows.py,mutation.py,mutation.json,mutation.log}`,
`io/{cases.ndjson,cases.rust,generation-stats.json,comparison.json,comparison.r1-overstrict-check.json,signed-recovery.ndjson,signed-recovery.rust,signed-recovery-comparison.json,owner-rows-rederived.json}`, `hashes.txt`.
