# Independent review — captured source through current S4 308

**Standing:** bounded native-Rust review of frozen `native-captured-s4-checkpoint-308`. This composes 306 raw image capture, 301 authentication on the **same** Budget, and 307 current evaluation that now **requires** `CapturedOrdinaryInput`. It does **not** admit live `state.v1`, prove current head/history/T, qualify by-prev publication filesystem, select 1 s, publish, or grant effects. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–307 reports were not edited (307 fully read and left archived).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/host/mutant directories were not overwritten. No workspace rerun. No load/suspend/VM/proof-prep/namespace qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9154148 B, 956 members, SHA256 `ac8d73b9f2e0a8fd03fd96dda1b064a9118b225a1020ffcd9616bf37b8916c25`**. Standing: private unselected308 captured source and OS-source S4 composition; no namespace/current authority or publication qualification. Extract rehashed **956/956**. Product-inputs **461/461**. Nested 307 pin `98aa4727…dd1d` (live tar match), 306 `f2850285…ad26`, 305 `87d4cd14…933d`, 297 `f0d7c35d…45df`. `kernel201.py` `df45c9c5…2299`. Whole `trust_time.rs` is **byte-identical** to 307 (`b76c829f…1dc4f`). `lib.rs` byte-identical to 305–307; **no** public re-export. Product vs 307: **461** files, **456** unchanged. Changed: `trust.rs` `a54bfe57…b88d` (private crate re-exports of `CapturedImage` / `CapturedOrdinaryInput` / `OrdinaryClockInput`), `captured_capsule_clock.rs` `00e36fda…68f0`, `ordinary_targets.rs` `e2d3f745…b93e`, `clock_observation.rs` `c937cd00…acd6`. Added: `captured-s4308.ndjson` (10254700 B, SHA256 `4c5682b1…e86c`). Beforeimages: `clock-observation-before.rs` = 307; `ordinary-targets-before.rs` = 307; `captured-capsule-before.rs` = 306; `trust-before.rs` = 307. Production `ordinary_targets` prefix is unchanged vs the predecessor-coverage expansion (tests/counts only). First **109** fixture rows are byte-identical to that beforeimage.

---

## What the composition does

`CapturedClock` now owns `CapturedImage` plus the paired `CapsuleClock`. `into_parts` moves both. `CapturedImage` has private fields and **no** JSON constructor: NodeRef, raw capsule `Record`, raw descriptor `Record`, optional `(before NodeRef, Record)`. Borrowed getters only. 306 `capture` I/O, SHA/len, `/publication` edge, predecessor SHA-join, and 279/298 `capsule_clock` are unchanged except the owned split. Existing 306 tests remain.

`prepare_captured_clock_input` is the only producer of `CapturedOrdinaryInput`: `capture` then `prepare_clock_input` on the **same** `Budget::scope`. Distinct from parsed `OrdinaryClockInput`. Roles/OLD/R/revocation remain **premises**.

`evaluate_current_ordinary` now takes `CapturedOrdinaryInput`, not parsed-only input (type boundary). It `into_parts`s the wrapper, captures the actual OS sample **after** authentication, then retains the image, exact sample, and unchanged 301 proposal together. Historical `evaluate_retained_ordinary(OrdinaryClockInput, RecordedObservation)` is untouched. S4 math is not retuned.

The ignored host consumer still uses the four signed 307 fixtures × two purposes, but now `put`s canonical capsule/descriptor/before into the store, runs `prepare_captured_clock_input`, checks 301 sources **before** sampling, and after JSON/store/root/Budget drop asserts retained source JSON **and** raw bytes plus raw W/M/B against the S4 recording. Telemetry prefix is `CURRENT308`.

**113** differential cases: 99 signed 301 contexts + 10 raw/ref/combined-budget + 4 explicit predecessor (`empty-head-publication-with-before` plus missing/length/unknown-field). **56/56** accepted. Baseline **13 objects / 34 edges / 27373 B** → repeat **13 / 68 / 27373** with **13** captures. Initial 109-case log retained; expansion did not change production source.

**Executed:** `cargo clean -p opensip-security` then **253 passed / 0 failed / 2 ignored** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **ten** include files.

**Host samples (separate from frozen `host-r1`):**

- Historical replay of frozen `host-r1/observed.ndjson` through pinned 201/265 `clock_decision`: **8/8**; 1 NewRequired / 2 Keep / 5 NoWrite; walls `2026-09-21T00:44:21Z`. Frozen stdout SHA256 `50ff4fc9…de08` unchanged.
- Live `grok-out/io/host-live/`: new samples, **8/8** this wall, same 1/2/5 split. Frozen `host-r1` not overwritten. Counts are **this wall**, not a clock-independent guarantee. 302 1 s remains unqualified.

**Nine compiled controls — classified by first frozen failure, not a single heuristic:**

Wrong **refusal**: `omit-explicit-predecessor` (`empty-head-publication-with-before` needs exact before); `substitute-capsule-ref-for-payload-closure` (auth `Shape` on capsule NodeRef as closure).

**Counters / budget**: `detached-authentication-budget` (outer Budget 2/2/8534 vs 13/34/27373); `duplicate-capsule-edge` (13/35 vs 13/34).

**Facts / retained identity**: `return-descriptor-as-capsule` (view is descriptor object); `substitute-capsule-raw` / `substitute-descriptor-raw` / `substitute-before-raw` (raw bytes swapped); `drop-retained-predecessor-view` (before missing on the explicit-predecessor positive).

None of these first failures is a `left: true` faulty **acceptance**. Live 9/9 core-equal frozen `mutation-check-r1` (`report.json` SHA256 `f764ac93…d86d`). No compile correction.

---

## Findings

### 1. Pairing / type boundary — hold

Current evaluation cannot be given a parsed-only `OrdinaryClockInput`. The owned image travels with the 301 proposal and the OS sample. Substituting views/raws is caught after temps drop.

### 2. Same-Budget capture then auth — hold

Detaching auth onto a new Budget is caught on counters. An extra Records load is caught as an extra edge. Failure latch remains the existing `scope`.

### 3. Still not current authority

The raw image may be historical/unselected. Supplied roles/OLD/R/revocation are premises. The store callback is still `(Collection, digest, cap)`, not a qualified by-prev publication locator. 306 remainders on absence-of-predecessor and filesystem layout still apply.

**Actionable defects in this freeze:** none that make the private pairing self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 308 pins before extract | match |
| Nested 307 / 306 / 305 / 297 | match |
| `trust_time.rs` vs 307 | byte-identical |
| Fixtures | 113; 56/56; 13/34/27373 → 13/68/27373 |
| Live `cargo test -p opensip-security` | **253 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 10 includes | pass |
| Frozen host-r1 primary replay | 8/8; 1/2/5 |
| Live host-live samples | 8/8; 1/2/5; **separate files** |
| 9 r1 mutants | frozen-equal; classified refusal/counter/fact |
| 1 s / namespace / publication | **not qualified** |

---

## Remaining (do not count closed)

Original T/history/current-head admission, actual OLD/R/revocation population, bootstrap/batch, namespace/custody/fences, same-control-flow age guard, 222 durability, post-S4 minima/completeness/role effects, writers, source selection, qualified by-prev publication filesystem, and M3–M6 remain open. 305 1 s is still unqualified. No operational consumer outside tests.

---

## Verdicts

- [x] **308 as private captured-source wrapper:** archive verified; 306 image owned and moved; 301 auth on the same Budget; 307 current eval requires `CapturedOrdinaryInput` and retains image+OS sample+proposal; 113/56/56; 9/9 mutants classified; frozen and live host 8/8; 253/2 ignored, Clippy, fmt10.
- [ ] **Not** live-state admission, current authority, qualified filesystem publication, OS policy selection, completeness, grant, or product installation.
