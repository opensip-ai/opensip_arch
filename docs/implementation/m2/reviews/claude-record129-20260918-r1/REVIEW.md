# Independent bounded review — full retained trust record 129 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `record129-20260918-REQUEST.md`. Scope: the delta of frozen `trust-record-checkpoint-129` over frozen 128 —
`crates/security/src/trust.rs` and the two recovery corpora — i.e. the Rust `AdmittedTrustRecord` owner and its two
caller gates, against proposed reference 127 (reviewed separately, same day). Not wired to `trust_time` or a
physical decoder — I infer no state integration. No storage authority, OS, release or cumulative standing. No
frozen/selected/product edit; scratch builds, dedicated target directories; no commit, push or delegation.
Test-only keys have no authority.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,154,176 bytes, SHA-256 `d9a0107d50c4f955290003f2b9fc4270fd994674fde00e844c4a64bc0e3006ad` = request and `archive-pin.json` |
| Members | 438/438 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 128 extraction (330/330); `parent128/` copies equal the repository's 128 pin/manifest |
| Changed | exactly 3: `trust.rs`, `recovery-cases.ndjson`, `recovery-challenge-cases.ndjson`; 327 unchanged |
| Host pins | host79 receipt: 210 sources, all equal the product pins. host78 has no receipt — it is the retained failed run (76/1), as disclosed |
| Fixture continuity | recovery rows 1–587 byte-equal to 128's; challenge rows 1–288 have identical **inputs** (outputs re-derived); my 280 inputs from the 123 probe are present with identical `record/observation/revoked/epoch` (280/280) |

## 2. What changed (complete diff read; `claude-out/trust.diff`)
Child module `admitted_trust_records`: `admit(&V) -> AdmittedTrustRecord { record: Object, clock_projection: V }`,
private fields, accessors `fields() -> &Object` and `clock_projection() -> &V`. Admission = own 5 MB work bound →
object → closed eleven members → five nullable **calendar** timestamps → anchor via `recovery_observation` →
three counters ≥ 1 → serial ≥ 0 → pending via `admit_recovery_pending`. Callers: `propose_recovery` admits after
epoch, observation and the *present-pending* shape and before the supplied-root `Context` check and any signature
work; `issue_challenge_with_draw` admits after observation, report-only and window overflow and **before** the bound
digest and the entropy draw. This is the 127 order.

## 3. Evidence

**Owner checks, fresh scratch:** 77/77 security tests; strict workspace Clippy clean. Owner's four compile-fail
clients: one error each, in the inserted line (E0451/E0616/E0596/E0594) — privacy checks, as labelled.
Owner's nine mutants: report read; each names the failing test.

**A. My corpus — 11,225 distinct mutated records** (`probes/gen_records.py`; same generator family as my 127 probe:
five admissible bases, 52-value pool with 25 timestamp spellings, bool-as-int, ±2^63, 2^53, 256/257-unit and
non-BMP boot ids). Each row carries my contract-text oracle (independent of schema validator and model), the 127
`trust_record_shape`, the 127 challenge result and the 127 apply result on the good **genuinely signed** epoch.
Rust side (`probes/rust_probe.rs.txt`, `catch_unwind` on every call):

| Property | Result |
|---|---|
| `admit` ⇔ oracle ⇔ reference 127 | **11,225/11,225** (581 admit, 10,644 `Input("RECORD_SHAPE")`); 0 panics |
| owned value equals the input; projection has exactly six members, each equal to the owned member | 581/581 |
| challenge `ISSUED` ⇔ reference `ISSUED` | 11,225/11,225 |
| **entropy draws: exactly 1 when issued, exactly 0 on every refusal**, with a succeeding and with a failing source; entropy failure surfaces as `Entropy` | 11,225/11,225 |
| apply proposes ⇔ reference `APPLIED` (108) — no success on any unadmitted record | 11,225/11,225 |
| refusal details equal to the reference | all, except the `Context` class below |
| caller's value unchanged after every call | 11,225/11,225 |

**B. The `Context` class is a rule, not a label.** In my corpus Rust answers `Context` for **exactly** the admitted
records whose `rootVersion` ≠ the supplied root's (42/42; the other 539 admitted never do). The reference reaches
`RECORD_CHANGED_SINCE_CHALLENGE` (33) or `NO_PENDING_CHALLENGE` (9) for the same inputs. Both refuse, no writes.
I agree with the class statement in `projection-class-corrections-r2.json` (one root-context row, three
observation-calendar mappings — confirmed as corrected), and with recording it as *no equality of diagnostics
claimed*. For the model owner: the pure model never relates `record.rootVersion` to the accepted root at all; Rust's
earlier, cheaper refusal is the stricter behaviour. Whether the reference should state that binding is an owner
choice — see N-1.

**C. My 49.** All 49 formerly-applied malformed records are in the 129 corpus as `Input/RECORD_SHAPE` and pass as
such through real signed-epoch execution (`io/fixture-crosscheck.json`). The 24 old `ISSUED` rows that now refuse
all have `recoveryEpochSerial: null` (24/24), and the integer-zero control issues.

**D. Compile boundaries of my own** (10 must-fail, none overlapping the owner's four; each exactly one error inside
my line): literal forgery, destructuring move, parent-written `impl` forging `Self` or lending `&mut record`,
`Default`, `Clone`, `fields()` bound as `&mut`, `insert` through `fields()`, sibling child module reading the field,
assignment through `clock_projection()`. Three clients **compile** and mark where the seal ends — see F-1.

**E. Mutants** (12, all compiled, baseline green; stage 1 owner tests, stage 2 my corpus for survivors):
9 killed by owner tests — all five **order** mutants (admission before pending; after the root `Context` check;
before report-only; before window overflow; **entropy drawn before admission**), negative serial, zero counters,
non-string timestamps, calendar check limited to floor members. 3 survived owner tests:
- *projection anchor replaced by null* — **detected by my corpus (169 rows)**: T-1.
- *admit's own input bound removed* — no difference anywhere: T-2.
- *projection cloned from the caller's value instead of the owned one* — equivalent by construction (same bytes at
  that instant); listed for completeness only.

**F. Clock extremes (127 F-1), Rust side** (`io/clock-extremes.rust`): where reference 127 raises a foreign
`ValueError`/`OverflowError`, Rust's `assess` is **total** — `lastAccepted = 9999-12-31` evaluates (floor carried
to 9999, recoverable as designed); same-boot elapsed 2^63−1 returns typed `Err(Arithmetic)`. One case yields a
continuity instant of 253,402,306,798 s (> 9999-12-31) inside a finding — representable as i64, not as a
timestamp. That is input to the queued clock-range decision, not a 129 defect.

## 4. Findings

- **T-1 (low–medium, test gap) — the projection's `anchor` is unpinned.** `clock_projection` returning
  `anchor: null` for every record passes all 77 tests: the ownership test picks the *first* admitted fixture record,
  whose anchor is null, so its per-key equality is vacuous for the one structured member; the owner's projection
  mutant covers an expiry member only. The anchor is what same-boot continuity is computed from, so silently
  dropping it would disable that check in whatever consumes the projection. One positive test with a non-null anchor
  (and non-null expiries) closes it.
- **F-1 (low; same class as 128 F-1/F-2) — the projection leaves the seal as an untyped `V`.** A parent-module
  client can clone `clock_projection()`, alter it, and pass any `V` to the future clock adapter; likewise
  `RecoveryChallengeProposal` is a forgeable literal. Nothing consumes either yet. When the adapter is written, have
  it take `&AdmittedTrustRecord` (or a sealed six-member type built only inside the child module), not a `V`.
- **T-2 (low) — `admit`'s own 5 MB bound is unpinned.** Both current callers pre-bound their inputs, so removing it
  changes nothing today; the comment says it exists for a future direct caller. A direct `admit` test with an
  over-budget value (`Limit`) makes that promise executable.
- **N-1 (note, for the model owner)** — record `rootVersion` vs accepted root: Rust binds it (`Context`), the pure
  model does not mention it. Both refuse today; say which is the contract.
- **N-2 (note) — residual defensive code after the gate.** `serial: None | Null => 0`, the per-member re-checks in
  the challenge bound loop and `optional_time`'s error arms are unreachable once `admit` has succeeded. Harmless,
  but mutants there are equivalent and the `Null => 0` arm reads as if a null serial were still lawful. Remove or
  mark unreachable when convenient.

## 5. Unresolved limits
Six-member projection not wired to `trust_time`; no physical decoder; refusals "write nothing" is a property of
pure proposal functions — persistence does not exist yet. macOS host only; no Linux execution. Reference 127 is
itself proposed, with its own open F-1/T-1.

## 6. Bounded verdict
**129: reviewed, no blocking finding. Rust full-record admission equals an independently written oracle and
reference 127 on 11,225/11,225 records; challenge issues and apply proposes exactly when the reference does; entropy
is drawn exactly once on issue and never on refusal; all 49 formerly accepted malformed records refuse through real
signed execution; ownership holds against 10 further compile-time attacks; the `Context` difference is a verified
general class. T-1 (projection anchor unpinned) should be closed before the projection gains a consumer; F-1, T-2
and the notes are minor.** Not approval of storage, clock integration, custody, current authority, OS, release or
any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `trust.diff`, `owner/`,
`probes/{gen_records.py,rust_probe.rs.txt,rust_probe_clock.rs.txt,compare.py,compile_boundaries.py,compile-boundaries.json,compile-boundaries.log,compile-*.stderr,mutation.py,mutation.json,mutation.log}`,
`io/{records.ndjson,records.rust,context.json,generation-stats.json,comparison.json,context-class.json,fixture-crosscheck.json,clock-extremes.rust}`, `hashes.txt`.
