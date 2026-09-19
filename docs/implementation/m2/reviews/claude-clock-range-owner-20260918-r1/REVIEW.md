# Independent adjudication — clock-range owner choice (127 F-1 / T-1 / N-1 / N-2)

Reviewer: Claude (independent; Codex remains decision owner). 2026-09-18. Proposal:
`clock-range-owner-20260918.md` (SHA-256 `f7c20f898a83c8b6b563aa4999981aa1a2180bc06edae3211c8a69a1b278f11b`, 2221 B). Owner bytes: frozen reference 127 model and
contract from **my verified extraction** (hashes in `claude-out/cases.json`); Rust behaviour from my 129 probe
(`claude-record129-…/claude-out/io/clock-extremes.rust`). Executable cases in `claude-out/`. No frozen/selected
edit, commit, push or delegation; no schema, code or cumulative approval follows.

## 1. Decision as I understand it
Keep the admitted calendar 0001–9999 (no narrowing, no clamping). A **derived** timestamp that the clock kernel must
return must itself be in that calendar; otherwise — or on i64 overflow — a typed internal `TIME_RANGE`
(Rust `Error::Arithmetic` class), with no decision, effect or write, report-only included. Not `RECORD_SHAPE`, not a
new D9 class/error. Cut-offs that are only compared may leave the calendar if checked arithmetic succeeds.

## 2. Adjudication

**2.1 Keeping the domain — agreed, and my 127 alternative is withdrawn.** In 127 F-1 I offered "bound the admissible
calendar" as one option. The cases show why that would be wrong: the *never-expires idiom* — all three expiry members
at `9999-12-31T23:59:59Z` — evaluates normally today (`PROCEED`, 2 writes), as do each expiry member and
`evalHighWater` alone at either extreme, and payload expiries at 9999. Narrowing the record domain would refuse lawful
signed state to cure an arithmetic edge elsewhere.

**2.2 Where `TIME_RANGE` can actually fire — exactly three operand families** (`cases.json` A/B; 26 extreme cases,
everything else is total today):

| Family | Trigger | Derived value | Persistence |
|---|---|---|---|
| (a) admitted time | `lastAccepted` (or a witness/root issue time that becomes A) ≥ `9999-10-03T00:00:00Z` — the edge is exact: `…10-02T23:59:59Z` proceeds | `plausibilityLimit = A + 90 d` | **persistent** |
| (b) same-boot anchor | `anchor.wall` + elapsed mono beyond 9999 | `continuity.expectedWall` | until reboot or an anchor rewrite |
| (c) observation | same-boot elapsed mono near 2^63 | same field, i64 overflow | transient (no write ⇒ next sane observation evaluates) |

Both derived values are **report fields**; every decision that uses them is an integer comparison. So the rule turns
"cannot print a field" into "refuse the evaluation". I agree with that choice over the alternative (null the field and
continue), for a reason worth writing into the decision: in family (a) continuing means `tEval = max(floor, wall, A)`
is ~9999 and the kernel **writes a year-9999 floor** — which is what Rust does today
(`evaluation: 253402300799, advance: Advance`). `TIME_RANGE` with no write is strictly better than silently
completing a poisoning.

**2.3 "Recovery still admits lawful poisoned floors" — true for floors, false for family (a).** New evidence
(`cases-recovery.json`, pure model, signers asserted as in the owner's cases):
- `lastAccepted = 9999-12-31` (with or without the floor): challenge issues, **apply refuses
  `TIME_BEFORE_LAST_ACCEPTED`** — a recovery epoch issued now can never be ≥ a year-9999 `lastAccepted`. Family (a) is
  therefore *unevaluable and unrecoverable*: the same class as C-3 (restoration, not recovery). That is acceptable —
  `lastAccepted` is signed time evidence, so reaching it needs storage corruption or a signer issuing year-9999
  documents under a year-9999 wall — but the decision text must not promise a recovery path for it.
- same-boot anchor at 9999: apply succeeds and the clock then proceeds. Family (b) *is* recoverable.
- **Recovery can itself manufacture family (a):** wall and signed `issuedAt` = `9999-10-03T00:00:01Z` → `APPLIED`,
  and the next clock evaluation raises (today) / would be `TIME_RANGE` on every evaluation (tomorrow). A later epoch
  cannot help: it must be issued at or after that `lastAccepted`, so it lands inside the same 90-day edge. So the
  representability rule must also bind **`recovery_apply`'s proposed state**: refuse (typed, no writes) when
  `issuedAt + 90 d` is not representable. This makes the contract sentence "recovery must not … leave a clock state that
  cannot be evaluated" true, and is the concrete form of the owner's "signed-recovery extreme issue times" test line.

**2.4 Must the public route be made explicit? — Yes.** "Caller routes through the existing owning refusal; no guessed
public detail" is the right *principle*, but the kernel is the only place that knows which family fired, and the
honest remedies differ: (a) restoration, (b) reboot or recovery, (c) retry / inspect the host monotonic source.
Left implicit, each caller will map `Error::Arithmetic` by itself, most likely to a generic operational failure
with no remedy. What I would fix now, without any new vocabulary:
- The D9 row: every existing clock refusal in the model (`CLOCK-EXCURSION-FORWARD`,
  `TRUST.NO_ADMITTED_TIME_CONTEXT`) is `request-rejected / exit 2 / REQUEST.PRECONDITION_FAILED`. `TIME_RANGE` is the
  same kind of fact — the retained/observed time context does not permit an evaluation — so it belongs on that row,
  **not** on `operational-failed/HOST.IO_FAILURE` (nothing failed to operate) and not on `LEDGER.CORRUPT` (the state
  is admissible by 2.1).
- The typed internal outcome should carry the operand family (`state` vs `observation`, or the field name). That is
  internal, mints nothing public, and lets the owning caller choose an honest remedy string.
- Whether a registered *detail* already names it: `TRUST.FLOOR_AHEAD_OF_WALL` is registered and is the closest for
  (a)/(b), but it is a non-refusing finding today and does not describe (c). I would not stretch it. If the owner
  wants zero new details, carrying no domain detail is lawful only where the envelope branch allows it; a
  `kind=failure` envelope requires one (same constraint as the purge131 question), so this needs an explicit owner
  line rather than "no guessed detail".

**2.5 Totality and formatting — agreed, one host note.** The reference must never leak `ValueError`/`OverflowError`;
explicit range checks plus fixed four-digit formatting are right. On *this* macOS host `strftime('%Y')` already pads
(`iso()` of year 1 → `0001-…`; `cases.json` C), so I cannot reproduce the early-year defect here — it is a glibc
behaviour. Keep the fix, but the regression test must assert the **string**, not rely on the host to misbehave.

**2.6 Rust.** Agreed that `assess` must apply the same representability check to admitted time, plausibility,
continuity, evaluation and write timestamps. Today it is total but returns out-of-calendar instants
(continuity `253402306798`, plausibility beyond 9999) — i.e. it needs a behaviour change, not only a mapping. "No
saturation" is consistent with my 114 note; the surviving `saturating_add` mutant there should become killable by
the new extreme cases.

**2.7 T-1, N-1, N-2 — accepted as proposed.** One malformed-record + invalid-root case pins record-before-root;
stating the calendar range 0001–9999 in the contract resolves N-1 (year 0000 refused by rule, not by host library);
37 cases / 32 documentary fields corrected by addendum with 127's README preserved.

## 3. Conditions
- **K-1** `recovery_apply` refuses, with no writes, a proposal whose resulting `lastAccepted + 90 d` (and any other
  serialized derived instant) is unrepresentable (2.3).
- **K-2** Decision text: family (a) has no clock-recovery path (restoration, as C-3); (b) recoverable; (c) transient.
- **K-3** Explicit D9 row and an internal operand-family tag for `TIME_RANGE`; an explicit statement about the
  domain detail on `kind=failure` (2.4).
- **K-4** Cross-language cases, each asserting *no write*: the exact edge pair (`9999-10-02T23:59:59Z` proceeds /
  `9999-10-03T00:00:00Z` refuses); never-expires idiom proceeds; same-boot anchor 9999; elapsed 2^63−1 and an
  elapsed that overflows the calendar but **not** i64 (the case where Rust and the reference differ today);
  report-only variants; year 0001 on all members; recovery at both extremes incl. K-1.
- **K-5** "Compared-only cut-offs may exceed the calendar" needs one positive case (wall vs `A + 90 d` decided while
  the limit is unprintable is *not* that case under this rule — it refuses — so name which cut-offs are meant, e.g.
  expiry + grace comparisons) or the sentence will be read as contradicting the rule.

## 4. Answer
**I agree with the owner's choice: keep 0001–9999, no clamping, typed no-write `TIME_RANGE` for unrepresentable
derived instants, in both languages. My 127 option of narrowing the record domain is withdrawn — the never-expires
idiom shows it would refuse lawful state. Two corrections to the proposal: recovery does *not* rescue a
`lastAccepted`-derived range failure and can currently *create* one (K-1, K-2); and the public route should be made
explicit now — the existing clock row `request-rejected / REQUEST.PRECONDITION_FAILED`, with an internal operand-family
tag so the remedy is honest (K-3).** No schema, vocabulary, code or cumulative approval is implied.

Evidence: `claude-out/cases.py`, `cases.json`, `cases_recovery.py`, `cases-recovery.json`, `hashes.txt`.
