# Independent review — captured original time-input context 316

**Standing:** bounded native-Rust review of frozen `native-time-context-checkpoint-316`. Private unselected port of reviewed 312 **literal** `bind_context` into frozen 313: one existing operation `Budget` loads S4 evaluation → before capsule → authority node via typed edges. It does **not** authenticate the authority, run the 312 embedded-root resolver, implement 315 recovery-scope (`AcceptedRecoveryAuthorityForImage`), admit T/history/publication, or publish. Installed product remains `fa72e50`. Keys/fixtures are **TEST ONLY** / synthetic 312 zeros. 315 REVIEW was not edited (root disposition accepted 315 as source observations only; 316 remains exact 312 bindings).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/mutant directories were not overwritten. No extra host sampling. No workspace rerun.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **11199928 B, 1522 members, SHA256 `039392b98d6458d3cf41881f4cc27f734626313433b1ba43c6d2dbb6821ba788`**. Standing: private unselected316 literal context capture; not historical authority or native publication. Extract rehashed **1522/1522**. Product-inputs **465/465**. Nested 313 live tar SHA match `355396bd…ee39`. `proposed_time_input.rs` / `trust_time.rs` / `clock_observation.rs` / `lib.rs` **byte-identical** to 313. `lib.rs` has **no** public export; `include!("trust/captured_time_context.rs")` is private in `trust.rs`.

Product vs 313: **462** unchanged, **1** changed (`trust.rs` private include), **2** added (`trust/captured_time_context.rs` `a2c29f73…c444`, `tests/fixtures/time-context316.ndjson` SHA256 `994f1406…adae`).

Preserved unchanged: 315 REVIEW `87e3cd2d79b2f321a786247b9f26fc0c925ba7d3d5d380f96fdc5d8e8e9ee0e8` (12239 B). 313 REVIEW `f9d43c9f…ab76`; 313 ADDENDUM `8a0a2458…4b41`; 314 REVIEW/ADDENDUM `d54342fd…daca` / `02a3a0bc…c8ee`.

---

## What capture does (312 literal, not 315)

Caller supplies only a root **NodeRef** (shape-checked **before** I/O) and a collection capture adapter. Same `Budget.scope`:

1. Load records by the NodeRef; `Record::parse(S4EvaluationInput, …)` — V1/V2 aggregate.
2. Load `beforeImage` via typed `/beforeImage` edge; require `TrustCapsuleV1`.
3. `beforeClock` and `store` must equal the capsule; P0/P1 (`phase != retained`) require `heads`/`history` null; P2 requires them present.
4. **P0/P1:** require V2 `authority` (legacy P0/P1 → `legacy-original-core-unavailable`); load that NodeRef; require `kind: anchor`. No current-core/creator synthesis.
5. **P2:** derive expected locator from `before.heads.root.admission`; V2 must match; legacy P2 uses the before-head edge. Join authority `root` DocRef / `RootBinding` / `rootVersion` to the before head/clock.
6. Own `CapturedContext`: input/before/authority `Record`s, exact references, mode `EmbeddedCore` | `AcceptedBefore`. Private fields; one constructor.

Does **not** walk publication, history, old T, or `source.closure`. Fixtures omit those target bytes; that is **not** their admission. Ownership is checked after store/budget/fixture drop. 315’s skip of `context.time` **targets** for S4.5 is **not** implemented here: this path still **loads the authority record** and applies 312 literal joins.

Independent Python replay of frozen `time-context316.ndjson` through 312 `bind_context` + 265 `Budget` (not native expected JSON): **94** cases, **18** first-round / **11** second-round positives, **0** mismatches. Baseline **3 objects / 3 edges / 2963 B**, repeat **3/6/2963** (no recapture). Helper SHA256 `713ec94c…a9f2`.

---

## Reproduction

**Executed:** `cargo clean -p opensip-security` then **254 passed / 0 failed / 2 ignored** with `Compiling opensip-security` (`Finished` 10.69s; tests 12.13s). Ignored: 305 host observation pilot and 313 actual-host composition. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **twelve** include files (311 eleven plus `captured_time_context.rs`).

**Fourteen compiled controls plus baseline** (live 15/15 core-equal frozen `mutation-check-r1`, report SHA256 `d335a04f…0930`). All 14 **compiled** and **test FAILED**. None is a compile-fail counted as a kill.

| Control | Stage caught |
|---|---|
| `omit-before-clock`, `omit-store`, `omit-phase-heads`, `omit-phase-history`, `allow-preaccepted-ordinary`, `omit-head-document`, `omit-head-binding`, `omit-head-counter` | **False acceptance** (`is_ok` true vs fixture false; e.g. `P0-heads-phase round0: None`) |
| `wrong-context-mode` | Wrong mode (`AcceptedBefore` vs `EmbeddedCore`) |
| `wrong-authority-collection` | Wrong refusal of a **good** P0-v2 (`Budget(Capture)` vs expected ok) |
| `omit-before-authority`, `reject-supported-legacy`, `discard-shared-budget`, `suppress-failure-latch` | Still reject, **wrong stage/counters** (e.g. latch/shared-budget/legacy parse) |

Tests catch those before a final “binding diagnostic” success. Matcher uniqueness 1 for each replace-target. No compile/test correction.

No additional host sampling claimed.

---

## Findings

### 1. Literal 312 joins under one Budget — hold

Native capture matches 312 `bind_context` predicates (projection, phase heads/history, P0/P1 V2+anchor, P2 derived head, document/binding/counter). Typed `decode_at` is the 127 reader, not a second codec. 94-case primary replay is exact.

### 2. Not 315, not admission — hold

No recovery-scoped skip of historical `context.time`. No embedded-chain resolver, TCB, 222 durability, or publication. Missing unrequested history/publication/source bytes are not treated as verified.

### 3. Mutant stages — hold as requested

Guard deletions that still fail do so at `is_ok`, counters, capture trace, latch, or mode — not by failing to compile. `wrong-authority-collection` is a wrong-stage **refusal**, not false acceptance.

**Actionable defects in this freeze:** none that make the private capture self-contradictory with frozen 312 literal context.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 316 pins before extract | match |
| Nested 313 live tar / 313 producer/kernel | SHA / byte match |
| Independent 312+Budget fixture replay | 94 / 18 / 11; 0 mismatch; 3/3/2963 → 3/6/2963 |
| Live `cargo test -p opensip-security` | **254 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 12 includes | pass |
| 14 r1 mutants + baseline | all compiled; 14 test-FAILED; core-equal frozen |
| 315 recovery-scope / T proof / 222 | **not this freeze** |

---

## Remaining (do not count closed)

312 embedded-root resolver, original-authority authentication, 315 admitter (including disposition: ancestor equal-L designated target T; P2 `timeEvidence` field-present / target out of S4.5 scope), T consumption, P0/P1 live producer, OLD/R/revocation, custody/fence/census/capacity, final age, 222 durability, writers, source selection, M2–M6. 305 1 s unqualified. 313 host composition still ignored.

---

## Verdicts

- [x] **316 as private 312 literal-context capture:** archive verified; NodeRef-before-I/O; V1/V2 aggregate; P0/P1 V2+anchor; P2 derived head; one Budget 3/3/2963→3/6/2963; 94/18/11 primary-equal; 254/2 ignored; Clippy; fmt12; 14 controls distinguished by stage.
- [ ] **Not** 315 recovery-scope, historical admission, TCB, publication, OS qualification, or product installation.
