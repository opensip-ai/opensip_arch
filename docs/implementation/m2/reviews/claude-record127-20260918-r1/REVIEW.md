# Independent bounded review — retained trust-record reference 127

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-18.
Request: `record127-20260918-REQUEST.md`. Scope: the delta of frozen `trust-record-reference-checkpoint-127` over
frozen 125 — reference model, checker, cases and contract text for the eleven-member `TrustClockRecordV1`
admission and the six-member clock projection (my recovery-record r1/r2 adjudications, C-1..C-3), plus the 125 B-1
negatives and the 124 F-1 obligation text. **Reference only**: no Rust decoder, storage, custody, current
authority, release or cumulative standing. No frozen/selected/product edit; scratch copies only
(`PYTHONDONTWRITEBYTECODE=1`, 0 stray `.pyc`); no commit, push or delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,147,340 bytes, SHA-256 `f1e9bbdee62fdf2822d9db162eb4a91f427f3b1a07d1e1ba6292a161f51651ba` = request and `archive-pin.json` |
| Members | 1,447/1,447 regular, each length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,284/1,284 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 125 extraction and its `frozen-candidate.json` (1,284/1,284); 125 archive `3d052ac4…` |
| Changed | **exactly 11**: model, lifecycle checker, envelope checker (1 line), `trust-recovery-cases.v1.json` (2 lines), contract, and six source-pin files. In the pin files only hash leaves change (`pin-file-deltas.json`), and the pin gates pass in my scratch run |

## 2. What changed (complete diffs read; `claude-out/diffs/`)
`clock_record_shape` (six consumed members present, closed per-member schema, **calendar** `ts()` on all five
timestamps, `_observation()` on a non-null anchor) gates `clock_decision` → `RECORD_SHAPE`.
`trust_record_shape` (closed eleven-member schema + the six-member check + `_pending_shape`) gates
`_recovery_apply` (after the present-pending shape, before root admission) and `_recovery_challenge` (after nonce,
observation, report-only and window-overflow; before digest, challenge construction and `pendingWrite`).
A non-dict record no longer reaches `.get`. Contract: one paragraph stating exactly this, the order, C-3
("malformed old pending ⇒ no recovery path; restoration is separate"), and the 124 F-1 consumer obligation.

## 3. Evidence

**Owner checks, fresh scratch, required order:** envelope 168+145+1,803+61+6,000 pass → integration 423/0 →
security 581/581 + all sweeps (new sweep included) → integrated carrier 435/0. All exit 0.

**Evidence-handling disclosure, checked:** `security-report-r1.json` really is a failed run (581 cases pass, sweep
`platform_host_float_types` fails — the old `CONTEXT_SHAPE` expectations), `-r2` passes; `envelope-r1` lacks a
qualification report, `-r2` has one. The `-final` logs are the passing rerun. I count the structured r1 reports as
preserved and the first-run stdout/stderr as **not** preserved, exactly as disclosed. It does not affect any
conclusion below, because I re-ran everything.

**A. Independent shape oracle** (`probes/record_probe.py`): written from the contract paragraph, using neither the
schema validator nor any model helper (own Gregorian arithmetic, exact-type integers, UTF-8 check).
120,000 one/two-member mutations over five admissible bases (fixture, no pending, with anchor, all-null, poisoned
floor without `lastAccepted`), 53-value pool incl. 25 timestamp spellings (leap days 2024/2026/2100/2000, month 0/13,
day 0, 24:00, :60, year 0000/0001/9999, lower-case `z`, trailing LF, fullwidth and Arabic-Indic digits, offsets),
bool-as-int, floats/NaN, 2^63, lone surrogate:
**eleven-member 120,000/120,000 agree (10,429 admit), six-member 120,000/120,000 agree (76,447 admit), 0 exceptions.**

**B. Operations** (40,000 mutated records through apply, challenge and clock, 125 alongside):
- apply: every oracle-inadmissible record → `REFUSE`, `writes == []`, input unmutated (36,829/36,829);
  **6,149 of them were `APPLIED` by 125.** Every `APPLIED` result yields a record that is again admissible and that
  the clock evaluates.
- challenge: `ISSUED` **iff** oracle-admissible (3,171 / 36,829); never a foreign exception.
- clock: `RECORD_SHAPE` **iff** the six-projection is bad (10,835) — except F-1 below.

**C. Precedence** — all 15 probes match the contract order: apply `SHAPE` > `CONTEXT_SHAPE` > `PENDING_SHAPE` >
`RECORD_SHAPE` > `ROOT_NOT_ADMITTED`; challenge `NONCE_GRAMMAR` > `OBSERVATION_SHAPE` > report-only > window
overflow > `RECORD_SHAPE`, and every refusal carries no `pendingWrite`. Malformed old pending blocks a replacement
(C-3); an *expired well-shaped* pending is replaced; a poisoned floor without `lastAccepted` is challengeable and
recoverable (owner sweep re-run and my case).

**D. My retained 280-label record mutations (123 probe inputs), 125 → 127:** 238 are record mutations;
**125 outcomes change, and all 125 are oracle-inadmissible records** — the 49 previously `APPLIED` now
`RECORD_SHAPE` (0 applied-though-inadmissible remain), 75 `RECORD_CHANGED_SINCE_CHALLENGE` → `RECORD_SHAPE`,
1 `NO_PENDING_CHALLENGE` → `RECORD_SHAPE`. All 23 admissible ones are unchanged. This reproduces the owner's
"125 changed incl. 49" independently.

**E. Recorded Rust fixture inputs on the pure model:** recovery 587 = 7 strict-metadata refusals before the kernel
+ **580 identical 125 ↔ 127** (result, detail, writes). Challenge 288: 264 agree; **24 rows are fixture `ISSUED`
with `recoveryEpochSerial: null` and 127 refuses them `RECORD_SHAPE`** — see §5.

**Materialised-clock audit, re-derived** (`probes/materialized_audit.py`): all 37 clock cases carry the six members
after `$from` resolution (0 missing); 32 carry the documentary `_plausibilityLimit`, which the six-member gate
ignores by construction. (The README says "all11 reference cases"; the owner's own audit file and my count say 37 —
wording only.)

**Mutants.** Owner's ten: killed, by sweeps without a pin gate — I read the script and agree they are behavioural.
Mine, complementary (16, all compiled; judged by the owner's new sweep, the clock and recovery sweeps and all 581
cases, called directly — no pin gate in the path; two harness slips of mine preserved as `mutation.FAILED-r1/r2.log`):
**14 killed** — 11 by assertion, 3 because the mutated model raised (`KeyError` / an unexpected `Reject`) inside the
owner sweep, which is behaviour of the mutant, not a load or pin failure (calendar check restricted to the floor members; `lastAccepted` skipped; six-member check dropped
from the full gate; 24 h window relaxed; record gate before pending; non-dict `.get`; challenge gate before
report-only / before observation; clock gate after the `lastAccepted` rule; clock using the eleven-member gate;
challenge or apply using only the six-member gate; both presence guards removed). **2 survived:**
projection `required` emptied — *equivalent* (the explicit presence test precedes it); and T-1.

## 4. Closure

| Item | Status |
|---|---|
| recovery-record r1 (owner schema unenforced; 49 inadmissible records applied) | **Closed** — 0 remain; 6,149/6,149 random ones refused |
| r2 six-vs-eleven | **Closed as decided** — kernel admits only its six members, present and calendar-valid; the eleven-member gate sits at both recovery operations; `_plausibilityLimit` ignored, not stripped |
| C-1 `$from` overlays | **Closed** — 37/37 materialised cases complete |
| C-2 `RECORD_SHAPE` vs `CONTEXT_SHAPE` | **Closed** — one class rule; the six changed expectations are all malformed-record inputs |
| C-3 malformed pending | **Closed** — `PENDING_SHAPE` at apply, no replacement at challenge, contract says restoration is separate |
| 125 B-1 tail-0 negatives | **Closed** — four added; owner mutants for both kill |
| 124 F-1 | text obligation only, correctly worded ("reachability after rename is not identity at its custody path"); nothing to execute |

## 5. On the two context notes (no disagreement)
- **24 `ISSUED` rows with `recoveryEpochSerial: null`:** confirmed exactly 24, and refusing them is right — the
  owner schema has `I64NonNegative`, not nullable, and a fresh install's serial is `0`. Re-deriving outputs and
  adding an integer-zero positive control is the correct handling; keep the 24 as negatives rather than deleting them.
- **Boundary class rule instead of per-label exceptions:** agreed in principle; where Rust reports its own earlier
  boundary (`Context`/`Input`) before the pure kernel's diagnostic and both refuse with no writes, a class mapping is
  the honest statement. I will check the concrete instances (as corrected: one root-context case and three
  observation-calendar mappings) against frozen 129, not here.

## 6. Findings

- **F-1 (low–medium, inherited from 125 but now inside 127's claim) — the admissible domain is larger than the
  clock kernel's arithmetic domain.** A six-projection that `clock_record_shape` admits makes `clock_decision` raise
  a **foreign** `ValueError`/`OverflowError` from `iso()` (`probes/clock_overflow.py`, identical on 125):
  `lastAccepted ≥ 9999-10-03T00:00:01Z` (A + 90 d crosses year 9999), an anchor wall near 9999 with later mono, or
  same-boot elapsed mono near 2^63. 32 of 40,000 random records hit it. `clock_decision` has no wrapper, so this
  is neither `RECORD_SHAPE` nor a typed refusal, and the new contract sentence "recovery must not … leave a clock
  state that cannot be evaluated" is not yet true at the edge. Such a record is *recoverable* (challenge issues,
  apply repairs the floor), so it is not a dead end — but the reference must choose: bound the admissible calendar
  (then it is `RECORD_SHAPE`), or make the kernel total with a typed refusal. Rust needs the same decision
  (its `saturating_add` survivor in 114 is the same edge); I will compare in 129.
- **T-1 (low) — record-before-root order is stated but unpinned.** Moving the apply gate *after*
  `ROOT_NOT_ADMITTED` passes all owner checks. One case with a malformed record **and** an unadmitted root pins it
  (my probe C shows the intended `RECORD_SHAPE`).
- **N-1 (note) — year 0000.** Refused by `ts()` only because Python's `datetime` starts at year 1; the contract
  says "calendar semantics" without naming the range. State the range (0001–9999, or narrower per F-1) so that Rust
  is bound by text rather than by a host-library property.
- **N-2 (note)** README "all11 reference cases" vs 37 in the audit file.

## 7. Unresolved limits
Pure reference only; no signature or Rust execution is claimed by the 125↔127 comparisons. The state decoder that
should own the eleven-member gate does not exist yet; "AdmittedTrustRecord" is a stated intention. Restoration for
C-3 is unspecified by design. I did not examine whether a *signed* epoch with an extreme `issuedAt` can make
recovery itself write an unevaluable floor (freshness rules probably prevent it; unverified).

## 8. Bounded verdict
**127: reviewed, no blocking finding. The eleven-member admission and six-member projection agree with an
independently written oracle on 240,000 shape decisions and 120,000 operation outcomes; all 49 formerly applied
malformed records — and 6,149 random ones — now refuse without writes; order, C-1..C-3 and 125 B-1 are closed.
F-1 (calendar extremes raise a foreign exception in the clock kernel) needs an owner decision before the Rust
record implementation is declared equivalent; T-1 is one missing case.** Not approval of Rust, storage, custody,
current authority, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `pin-file-deltas.json`, `diffs/`, `owner/`,
`probes/{record_probe.py,record-probe.json,record-probe.log,clock_overflow.py,clock-overflow.json,materialized_audit.py,materialized-audit.json,mutation.py,mutation.json,mutation.log,mutation.FAILED-r1.log,mutation.FAILED-r2.log}`, `hashes.txt`.
