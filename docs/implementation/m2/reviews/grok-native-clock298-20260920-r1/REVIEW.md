# Independent review — capsule clock phase view 298

**Standing:** bounded native-Rust review of frozen `native-capsule-clock-checkpoint-298`. Private `admitted_trust_records::capsule_clock` runs 279 `capsule_consistency` on the same Budget, then materializes an explicit-phase six-field view. This is not authenticated historical time provenance, current-head selection, S4 write-ahead, OS clock authority, host admission, grant, or product installation. Installed product remains `fa72e50`. Archived 294–296 reports were not edited. 297 REVIEW read-order wording was corrected separately (beforeimage preserved).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8661836 B, 922 members, SHA256 `23a84b2305b3a14eb4caade34a3701aedd55607b0ed4828957da0acc937ff835`**. Standing: unselected private298 structural capsule clock view; original time provenance and operational authority pending. Extract rehashed **922/922**. Product-inputs **451/451**. Nested parent 297 pin `f0d7c35d…45df` equals reviewed 297; live 297 trial tar matches. Nested 279 `8b081b4f…4e9d` live-matches. Nested 215 r14 `cd338af6…dd9c` / OWNER `d8165f14…19fa`. Nested 265 `73c3b3f5…86df`. 227 r9 `shape_join_model227.py` SHA256 `781061b6…cdf2`. Schema `private-trust-state.schemas.v1.json` SHA256 `1328ba16…4208`. Product vs 297: **451** files, **449** unchanged. Changed only `trust.rs` `789a1211…18f3`. Added: `capsule-clock298.ndjson`. `capsule_clock` / `CapsuleClock` are not in `lib.rs`.

---

## What `capsule_clock` does

Same Budget: 279 `capsule_consistency` first (full capsule/descriptor/optional BEFORE). Then `clock.phase`:

- `unevaluated` (explicit only): six null CLOCK_FIELDS. Missing/malformed capsule never becomes this phase.
- `evaluated`: copy the exact six-member P1 projection; calendar-validate `evalHighWater`/`lastAccepted`; nullable calendar-valid `anchor` via `recovery_observation`. No eleven-field record and no fabricated positive counters. Retain `timeEvidence` as an unauthenticated NodeRef (ClockPhase schema; it points at the time proof node).
- `retained`: existing full eleven-member `admit` (pending-challenge semantics included) then six-field projection. Retain `timeEvidence`.

Owned `CapsuleClock` keeps `CapsuleBound`, phase, six-field `ClockProjection`, and optional T ref. No T lookup, history read, provenance, current selection, or custody. A structurally valid unavailable T ref is still a view. Poisoned/ahead floors stay recorded; S4 arithmetic is not this owner. Repeat projection on a seeded budget stays **1 object / 2 edges / 5 B** with no further I/O. Values survive input drop.

741 differential cases, **150** valid (26 P0 / 38 P1 / 86 P2): 649 inherited 279 plus calendar boundaries, leap/year1/year9999, invalid days/LF, nullable anchors, mono i64, Unicode boot length, absent/malformed/altered T refs, invalid P0 lookalikes, P2 pending semantics. Oracle: exact 227 r9 shape join (full 125 schema as in 279), 265 primary clock/trust record shape, explicit 215 r14 D phase law (six nulls only from admitted `unevaluated`).

**Preserved authoring (production logic unchanged after initial author):**

1. Clippy-r1 `items-after-test-module`: moved **only** the nested test module after existing `admit`. `trust-before-test-module-order-fix.rs` SHA256 `1bd5825c…16ab`; `test-order-fix.json` records exact non-test comparison. Final Clippy-r2 passes.
2. Mutant r1 latch (`clock-calendar-failure-not-latched`) did not compile (inner `Ok` rewritten). Retained. r2 anchors the outer `budget.scope` closure on final source plus 245-test baseline. Do not count the r1 compile-fail as a detection.

**Executed:** `cargo clean -p opensip-security` then **245/245** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. r1 11 variants + r2 latch/baseline core-equal frozen `mutation-check-r1` / `mutation-check-r2` (live baseline cargo skipped). Frozen mutant dirs not overwritten (`report.json` SHA256 `614cd18e…97c8` / `982e27af…5993`).

**11 compiled controls: 4 wrong conditional admissions** — `p1-omits-floor-calendar`; `p1-omits-last-calendar`; `p1-omits-anchor-calendar`; `p2-skips-full-record-semantic-admission`. **7 other-first** — `p0-materializes-string-instead-of-null`; `p1-labels-retained`; `p1-overwrites-floor-with-last`; `p2-leaks-full-eleven-field-record`; `p1-discards-time-reference`; `p2-discards-time-reference`; r2 `clock-calendar-failure-not-latched`. r1 latch remains compile-fail, not counted.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 298 pins before extract | match |
| Nested 297 / 279 / 265 / 215 r14 / 227 r9 model | match |
| Live `cargo test -p opensip-security` | **245/245** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 298 r1+r2 mutants | 11 compiled frozen-equal; 4 wrong / 7 other; 1 r1 compile-fail preserved |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

S4 composition, OS observation, durable write-ahead; original time-evidence codecs; qualified current/BEGIN/OLD/history/population; post-S4 minima/completeness/role effects; bootstrap; active-batch head barrier; full host admission; custody/fence/census/writers; source selection; M3–M6. Observation-latency/rounding/midpoint for `observe_clock` is **missing** from pinned S4 sources (see `CLOCK-OBSERVATION.md`). 298 is a structural phase view, not complete ordinary import or cumulative approval.

---

## Verdicts

- [x] **298:** archive/pins verified; 279 first; P0 six-null only from explicit unevaluated; P1 calendar/anchor without eleven-field manufacture; P2 full `admit` then six-field projection; T ref unauthenticated; 4/7 mutant classification with r1 latch compile-fail preserved; 245/245, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** S4 write-ahead, current-head/BEGIN proof, host installation, completeness, grant, or product installation.
