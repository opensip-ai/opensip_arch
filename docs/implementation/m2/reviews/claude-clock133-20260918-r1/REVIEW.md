# Independent bounded review — derived clock range reference 133

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-18.
Request: `clock133-20260918-REQUEST.md`. Scope: the delta of frozen `clock-range-reference-checkpoint-133` over frozen
131 — the reference form of my clock-range adjudications r1 (K-1..K-5) and r2 (F-1, P-1..P-4), plus record127 T-1.
**Pure reference**: asserted inputs, no clock read, signature, storage or OS effect; Rust 134 is a separate subject.
131's findings remain tracked independently and are not re-examined. No frozen/selected edit; scratch copies only
(`-I -B`, 0 stray `.pyc`); no commit, push or delegation; no cumulative acceptance.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,192,936 bytes, SHA-256 `ef3620e4886a14e290c8f9e8ed9695e7a1ac715a4e5cc11de35e48b14e50ccd3` = request and `archive-pin.json` |
| Members | 1,375/1,375 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,287/1,287 equal; none unpinned |
| Parent | `parent-inputs.json` (1,286) equals **my own** verified 131 extraction and its `frozen-candidate.json` |
| Changed | **14 changed + 1 new = 15**: model, lifecycle checker, lifecycle schemas, registry, both workflow `common` schemas, `check-integration.py`, contract, six pin files; new `security/clock_range_checks.v1.py` |

## 2. Owner checks, fresh scratch, required order
envelope → integration 423/0 → security 581/581 + **24 sweeps**, the new one present and mandatory
(`calendar-derived-time-range-and-honest-refusal-order`, 186 checked) → carrier 435/0 → workflows 2,117/2,117 →
foundation 231/231. All exit 0.

## 3. What changed (complete diffs read)
`calendar_representable(t)` on exact-type ints in `[−62,135,596,800, 253,402,300,799]`; `iso()` formats four digits
by hand and raises typed `TIME_RANGE` as a backstop; after both payload-future refusals and before the fresh/ordinary
split, an unrepresentable `A + 90 d` refuses `TRUST.TIME_RANGE_UNREPRESENTABLE` with tag `retained-last-accepted`
**iff `lastAccepted`'s own limit is unrepresentable**, else `presented-signed-time`; an unrepresentable continuity sum
refuses with `continuity-expected-wall`; recovery refuses `TIME_RANGE` after the three signed-time refusals and before
`writes`. Registry, both `DomainDetailCode` enums, the model's D9 row and vocabulary move together.

## 4. Evidence (`claude-out/probes/`)

**4.1 Randomised oracle, 120,000 evaluations** (`range_probe.py`). My own integer calendar (days-from-civil, no
`datetime`) reproduces both constants exactly. States drawn from 12 boundary instants (incl. `9999-10-02T23:59:59Z`,
`…10-03T00:00:00Z`, `…00:00:01Z`, year 0001), 9 mono values up to 2^63−1, optional anchor/payload/report-only:
- **the 48,627 range refusals are exactly the 48,627 evaluations on which reference 127 raised a foreign exception**,
  and every other evaluation is unchanged from 127 (0 behaviour changes outside the range cases);
- 0 foreign exceptions; 0 input mutations; every range refusal has `writes == []` and a withheld floor; no output
  string carries a five-digit year;
- the tag equals my oracle in every case **and equals its counterfactual**: `retained-last-accepted` ⇔ dropping the
  presented document still refuses; `presented-signed-time` ⇔ it then evaluates. r2 F-1 is implemented correctly,
  including the `presentedRootIssuedAt` variant.

**4.2 Edges and priorities** (all as decided): `9999-10-02T23:59:59Z` proceeds / `9999-10-03T00:00:00Z` refuses, same
under report-only; never-expires idiom proceeds; year 1 prints `0001-…` for the derived limit too; payload-future
before range; range before the horizon excursion; double fault → plausibility; `RECORD_SHAPE` and
`RECORD_LAST_ACCEPTED_REQUIRED` before range; continuity at exactly the last second is an ordinary
`CLOCK-EXCURSION-FORWARD`, one second beyond is the range refusal; calendar overflow with an i64-fine elapsed and
true i64 overflow give the **same** tag; a reboot clears it; fresh install with a presented time in the edge refuses
with `presented-signed-time`.

**4.3 Recovery guard (K-1/K-2)** (`route_probe.py`): signed `issuedAt = 9999-10-02T23:59:59Z` with equal wall →
`APPLIED` and the next clock evaluation proceeds; one second later → `REFUSE/TIME_RANGE`, `writes == []`,
`floorLowered false`, input unchanged, public `RECOVERY.REFUSED`. A year-9999 epoch under a 2026 wall stays
`ISSUED_IN_FUTURE`; authority and shape refusals keep priority. Retained `lastAccepted` in the edge →
`TIME_BEFORE_LAST_ACCEPTED` (restoration class, as the contract now says); poisoned floor alone and same-boot anchor
→ `APPLIED`, and **after every applied recovery the clock evaluates**.

**4.4 Public route (P-1..P-3).** Detail present in the registry and both enums; `enums == registry` (321 = 321 = 321);
D9 row `request-rejected / 2 / REQUEST.PRECONDITION_FAILED`; subject is the tag, never a timestamp or path; a tag
outside the closed set raises `CLOCK_RANGE_SUBJECT`; the three remedies say restoration / obtain another document /
check clock-reboot-recovery respectively, and all say nothing was written.

**4.5 Mutants.** Owner's six: script read; in-memory, no pin gate; includes the r2 wrong-max rule. Mine,
complementary (14 + 1 re-run whose anchor I first got wrong — kept as `HARNESS-ERROR` in `mutation.json`, result in
`survivors.json`): **10 killed** — range check before the payload-future refusals; after continuity; a hybrid
r1+r2 tag rule; always-presented tag; exclusive calendar minimum; maximum one day too generous; unpadded year;
recovery guard before the signed-time refusals; 89-day recovery horizon; report-only exempted. (Five of these are
kills because the mutant *raised* inside the checker — behaviour of the mutant, not a load failure.)
**4 survived**, each with a counterexample — T-1 below.

## 5. Closure of my adjudications

| Item | Status |
|---|---|
| r1 **K-1** recovery result guard | **Closed** in the reference (exact edge, no writes, priority kept) — see T-1(a) for one unpinned variant |
| r1 **K-2** no recovery promise for a retained `lastAccepted` | **Closed** — contract and remedy say restoration |
| r1 **K-3** / r2 **P-1..P-3** explicit route, closed subject, vocabulary closure | **Closed**, except N-1 |
| r2 **P-4** order inside the kernel | **Closed** — stated and executed |
| r1 **K-4** cross-language cases | reference half present (39 materialised cases); Rust half is 134 |
| r1 **K-5** compared-only cut-offs | **Closed** — expiry/grace/skew named; idiom case present |
| r2 **F-1** own-horizon tag rule | **Closed** — oracle and counterfactual agree on every refusal |
| record127 **F-1** foreign exceptions | **Closed** in the reference — 48,627/48,627 now typed |
| record127 **T-1** record-before-root | covered (owner case present; not re-mutated here) |
| record127 N-1 calendar range stated; N-2 37/32 | done by text/addendum, old bytes untouched |

## 6. Findings

- **T-1 (low–medium as a set) — four properties the mandatory checker does not pin** (`survivors.json`):
  (a) **the recovery guard tests `issuedAt`, not the wall.** With `wall + 90 d` substituted, a signed epoch issued one
  second after a wall of `9999-10-02T23:59:59Z` (inside the issue skew) is `APPLIED` and the next clock evaluation is
  a permanent range refusal — precisely the state K-1 exists to prevent. One case with wall and `issuedAt` on opposite
  sides of the edge pins it.
  (b) **per-tag remedies.** Giving the retained tag the continuity remedy — so that restoration is never named —
  passes all 186 checks (my oracle sees 5,469/20,000 differing answers). The remedy is the whole point of the tag.
  (c) **the closed-subject check in `public_details`.** Removed, a timestamp-and-path subject is published.
  (d) **`iso()`'s no-clamp backstop.** A clamping `iso()` is invisible because no model path reaches it out of range;
  a direct `iso(MAX+1)` assertion is the only way to keep "no clamping" executable.
- **N-1 (low) — the public subject set is one wider than the clock can produce.** `CLOCK_RANGE_SUBJECTS` includes
  `recovery-result`, which the clock never emits, recovery never routes through this detail, and the lifecycle output
  schema does not list (the other three are there). `public_details` accepts it on a clock outcome — and pairs it with
  whatever remedy the outcome carries. Keep `recovery-result` as the Rust-internal operand name and make the public
  set the three clock tags, or state where it can lawfully appear.
- **N-2 (note)** `public_details` does not check that the remedy belongs to the tag; with (b) pinned in the kernel
  this is harmless, but the projection is the last place to enforce "closed subject ⇒ fixed remedy".

No defect found in the range logic itself.

## 7. Unresolved limits
Pure model over asserted inputs. Whether a real adapter preserves the typed refusal and the no-write property,
whether renderers show it, and whether Rust agrees case-for-case are outside this subject (134). The early-year
formatting defect is a glibc property I cannot reproduce on this macOS host; the explicit formatter removes the
dependence and the checker now asserts the string.

## 8. Bounded verdict
**133: reviewed, no blocking finding. On 120,000 randomised evaluations the new typed refusal fires exactly where
reference 127 raised a foreign exception and nowhere else, never writes, and its operand tag agrees with an
independent oracle and with its own counterfactual on every refusal; the exact edge, the priorities, the recovery
guard, the restoration caveat and the public route are as adjudicated. T-1 lists four unpinned properties — (a) the
recovery guard's operand is the one that matters — and N-1 a one-value mismatch in the closed subject set.** Not
approval of Rust, adapters, renderers, storage, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{range_probe.py,range-probe.json,range-probe.log,route_probe.py,route-probe.json,route-probe.log,mutation.py,mutation.json,mutation.log,survivors.py,survivors.json}`, `hashes.txt`.
