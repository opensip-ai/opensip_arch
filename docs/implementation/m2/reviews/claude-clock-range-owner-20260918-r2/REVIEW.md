# Independent adjudication — clock-range owner decisions r2

Reviewer: Claude (independent; Codex remains decision owner). 2026-09-18. Decisions:
`clock-range-owner-decisions-r2-20260918.md` (SHA-256 `53e7011b49aad2ba30baecb1d4532ee980bc1f48a5389385a738c69cd59cd466`,
2,757 B). Owner bytes: frozen reference 127 model (my verified extraction; hash in `claude-out/cases.json`) and the
127 registry/schemas; Rust 129 source read for the recovery refusal vocabulary. My r1 adjudication and its evidence
are preserved unchanged. No frozen/selected edit, commit, push or delegation; nothing here approves unauthored
schema, vocabulary or code.

## 1. Do the decisions settle K-1..K-5?

| r1 condition | r2 | Status |
|---|---|---|
| **K-1** recovery result range guard | guard on `issuedAt + 90 d` after authority/freshness/serial/binding and before writes; `REFUSE`, internal `TIME_RANGE`, no floor/last/anchor/pending/audit proposal | **Settled.** I checked the placement against the 127 kernel: the three signed-time refusals (`TIME_BEFORE_LAST_ACCEPTED`, `ISSUED_IN_FUTURE`, `ISSUED_TOO_OLD_FOR_WALL`) are the last checks before `writes` is built, so a year-9999 epoch under a 2026 wall stays `ISSUED_IN_FUTURE` and is never mis-reported as a range problem. `issuedAt + 90 d` is also the *complete* guard: recovery writes `anchor: None`, so the only derived instant the next evaluation must print from the recovered state is that plausibility limit. |
| **K-2** no recovery promise for a persisted `lastAccepted` in the edge | withdrawn; floor-only poisoning recoverable, anchor clearable "only if lastAccepted permits", transient mono retried | **Settled**, and the anchor caveat is exactly right (recovery clears the anchor but still needs `issuedAt ≥ lastAccepted`). |
| **K-3** explicit route + operand tag | `TRUST.TIME_RANGE_UNREPRESENTABLE`, request-rejected / `REQUEST.PRECONDITION_FAILED` / exit 2; four internal tags | **Settled in route; one tag rule is wrong — F-1 below.** |
| **K-4** cross-language no-write cases | listed for the successor | accepted as a commitment; nothing to adjudicate until authored |
| **K-5** which cut-offs are "compared only" | "expiry/grace integer arithmetic" | **Settled.** Confirmed against the kernel: the serialized derived instants are exactly `plausibilityLimit` and `continuity.expectedWall`; `admittedTimeReference`, `evaluationTime`, `floorWrite`, `lastAcceptedWrite` are maxima of in-calendar inputs and cannot leave it; `revocationIssuedAt + fresh days`, `wall + tolerance` and `wall ± skew` are compared, never printed. So the four tags cover every printable derived field, and the never-expires idiom stays lawful. |

## 2. The public detail — agreed
One narrowly defined, security-owned `TRUST.TIME_RANGE_UNREPRESENTABLE` on the existing clock row closes the gap
honestly: no registered detail names it (`TRUST.FLOOR_AHEAD_OF_WALL` is a non-refusing finding and does not
describe the continuity family), a `kind=failure` envelope needs one, and the row is the one every other clock
refusal already uses. Conditions, mostly mechanical:
- **P-1 closure.** Registry, both `DomainDetailCode` enums (workflows and `evaluator3/`), the model's `D9` table and
  its refusal-code inventory move together, or `sweep_public_detail_closure` fails — keep that as the guard.
- **P-2 subject is a closed set, not free text.** "Bounded subject naming the derived field/operand source" should
  be one of a fixed list (the four tags, or field names) so consumers can key on it and so no timestamp, path or
  raw operand can leak into it. r2's "no raw unrepresentable timestamp is formatted or echoed" then becomes
  checkable: assert the subject ∈ list and that no output string matches the timestamp grammar's shape with a
  five-digit year.
- **P-3 recovery.** Public detail stays `RECOVERY.REFUSED`; `TIME_RANGE` is an internal refusal detail. I checked
  that those details are **not** enumerated in the lifecycle schema, the registry or the common schema (0
  occurrences of e.g. `ISSUED_TOO_OLD_FOR_WALL` in all three), so no public enum changes for recovery — but Rust's
  `Refused(&'static str)` corpus and the reference case files gain one spelling that must match exactly.
- **P-4 order inside the clock kernel.** State where the range refusal sits: at the point of derivation — after the
  two payload-future refusals, **before** continuity and the horizon check — and, when both printable fields are
  unrepresentable, which is reported (plausibility first, as derived). Otherwise the two languages will pick
  different winners on double-fault inputs.

## 3. Finding

- **F-1 (medium for the stated purpose) — "if `lastAccepted` equals the maximal admitted time, classify retained;
  otherwise presented" gives a false diagnosis whenever a *later* document is presented to a record that is
  already in the edge.** The purpose of the tag is the remedy: *presented* means "rejecting the new document would
  fix the context". That is a counterfactual, and it can be executed on the 127 model (`claude-out/cases.py`;
  today's foreign exception stands in for tomorrow's `TIME_RANGE`):

  | Case | with document | without document | r2 rule says | honest tag |
  |---|---|---|---|---|
  | 1 only the presented time is in the last 90 days | range | **proceeds** | presented | presented ✔ |
  | 2 retained `9999-11-01`, presented newer `9999-12-01` | range | **range** | **presented** | retained ✘ |
  | 3 tie | range | range | retained | retained ✔ |
  | 4 retained in the edge, presented older (not a witness) | range | range | retained | retained ✔ |
  | 5 as 2, via `presentedRootIssuedAt` | range | **range** | **presented** | retained ✘ |

  In 2 and 5 the user would be told to drop a document when the installation in fact needs restoration — the
  exact misdiagnosis r2 set out to avoid, in the opposite direction. **Correct rule:** classify
  `retained-last-accepted` iff `lastAccepted + 90 d` is *itself* unrepresentable, regardless of which candidate is
  the maximum; `presented-signed-time` only when `lastAccepted` is null or its own limit is representable. It is
  one comparison, needs no counterfactual evaluation, and makes all five rows honest. Cases 2 and 5 belong in the
  successor's cross-language set.

## 4. Notes
- **N-1** `presented-signed-time` merges two sources (`newestIssuedAt`, `presentedRootIssuedAt`). The remedy is
  the same, so one tag is defensible; if the subject list (P-2) uses field names instead of tags the distinction
  comes for free.
- **N-2** Continuity: agreed not to guess between anchor and elapsed mono. Remedy text should say what is true in
  both cases — nothing was written, so a reboot (new boot id ⇒ no continuity sum) always clears it.
- **N-3** Rust: agreed that `Error::Arithmetic` must not erase the operand; a typed range variant carrying the tag
  is the smallest honest change. Pure i64 overflow (elapsed near 2^63) and calendar overflow (elapsed large but
  i64-fine — where Rust and the reference differ today) should produce the *same* variant and tag, since the user
  cannot act differently on them.
- **N-4** Report-only: same refusal, and `writes == []` was already true; the doctor surface therefore shows the
  range refusal rather than an evaluation. Say so, or a reader will expect doctor to "work anyway".

## 5. Answer
**r2 settles K-1, K-2, K-4 (as a commitment) and K-5, and the public-detail gap: one security-owned
`TRUST.TIME_RANGE_UNREPRESENTABLE` on the existing clock row, recovery via `RECOVERY.REFUSED` with an internal
`TIME_RANGE` placed after the signed-time refusals and before any write. K-3 is settled except for the
retained-versus-presented rule, which misdiagnoses two executable cases; replace "A equals lastAccepted" with
"lastAccepted's own limit is unrepresentable" (F-1). P-1..P-4 are the conditions for authoring.** As the owner
says, this is a proposed vocabulary extension; schema enums, registry, inventories and implementation need review
together before selection, and nothing here approves them.

Evidence: `claude-out/cases.py`, `claude-out/cases.json`, `claude-out/hashes.txt`.
