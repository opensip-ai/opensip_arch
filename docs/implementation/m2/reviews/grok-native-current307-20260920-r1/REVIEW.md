# Independent review — actual-current OS source to S4 307

**Standing:** bounded native-Rust review of frozen `native-current-s4-checkpoint-307`. Private `evaluate_current_ordinary` captures a 305 OS sample **after** a 301 `OrdinaryClockInput` is already prepared, then feeds `sample.recording()` through unchanged `RecordedObservation::admit` and `evaluate_retained_ordinary`. This does **not** admit platform/namespace, prove current head, compose 306's raw capsule image, select 1 s, publish, or grant effects. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–306 reports were not edited (306 fully read and left archived).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/host/mutant directories were not overwritten. No workspace rerun. No load/suspend/proof-prep/namespace qualification.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8889760 B, 954 members, SHA256 `98aa4727905a090664d9f73959b49a93d0b0d97c008f266bd82887e55e48dd1d`**. Standing: private unselected307 actual OS-source S4 composition; no namespace/current authority or publication qualification. Extract rehashed **954/954**. Product-inputs **460/460**. Nested 306 pin `f2850285…ad26` (live tar match), 305 `87d4cd14…933d`, 297 `f0d7c35d…45df`. Included `kernel201.py` `df45c9c5…2299`. `trust_time.rs` (S4 kernel included) is **byte-identical** to 306 (`b76c829f…1dc4f`). `captured_capsule_clock.rs` byte-identical to 306. `lib.rs` byte-identical to 305/306; **no** public re-export of `evaluate_current_ordinary` / `CurrentOrdinaryProposal` / `UseSite`. Product vs 306: **460** files, **457** unchanged. Changed: `clock_observation.rs` `f025b4ea…b820`, `trust/ordinary_targets.rs` `a02db6d0…b253`. Added: `current-s4307.ndjson` (4 freshly signed TEST-ONLY fixtures, SHA256 `48715273…8d52`). `clock-observation-before.rs` equals 305. Production `ordinary_targets.rs` is 306's file with only the ignored host consumer appended (306 bytes are the prefix through the 301 test closer).

---

## What the composition does

`evaluate_current_ordinary(inputs: OrdinaryClockInput, site: UseSite)` takes **no** caller clock, serialized recording, or timeout. `UseSite` is `pub(crate)` (`ClockPublication` / `CurrentReport`) so the TEST-ONLY host consumer can name it; `ObservedSample::capture` stays private.

Order: consume already-prepared opaque 301 input → `ObservedSample::capture()` → `RecordedObservation::admit(sample.recording())` → unchanged `evaluate_retained_ordinary(..., report = site == CurrentReport)`. Historical `evaluate_retained_ordinary` with a supplied `RecordedObservation` remains a separate path; this constructor will not take one.

`CurrentOrdinaryProposal` **owns** the exact `ObservedSample`, the `OrdinaryClockProposal`, and the declared `site`. Accessors borrow (`proposal()`, `raw_sample()`, `site()`). Private `observe_age()` binds that sample and purpose; it is not a cached publication permit and is not called by any installed host. After the host test drops fixture JSON, callback store, roots, and Budget, the owned proposal still matches raw W / midpoint-floor M / boot to the **exact** recording document used for S4.

`CurrentError` preserves `Sample` / `Recording` / `Evaluation`. `sampling_failure_projection()` emits 302's `{operational-failed, HOST.IO_FAILURE, host-io}` exit 4 **only** for `Sample`. Recording invariant and kernel errors return `None` (not relabeled as host-io). An S4 no-write assessment is still `Ok(CurrentOrdinaryProposal)`, not `CurrentError`.

The ignored host consumer prepares 301 inputs with `capsule_clock` on fixture JSON plus `prepare_clock_input` (sources checked against the fixture **before** sampling). It does **not** call 306 `capture` of a raw retained image. That 306→301 composition remains root-planning 308.

Four signed fixtures × two purposes = eight OS samples: `advance`, `keep-original-T`, `poisoned-floor`, `payload-future`. Report mode never proposes writes; payload-future withholds; poisoned floor Keep is preserved on publication.

**Executed:** `cargo clean -p opensip-security` then **252 passed / 0 failed / 2 ignored** with `Compiling opensip-security` (305 host pilot + 307 host composition). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **ten** include files. Mapping test `current_sampling_mapping_does_not_reclassify_recording_or_kernel_errors` is in the 252.

**Host samples (separate from frozen `host-r1`):**

- Historical replay of frozen `host-r1/observed.ndjson` through pinned 201/265 `clock_decision`: **8/8** matched; 1 NewRequired / 2 Keep / 5 NoWrite; walls `2026-09-21T00:30:04Z`. Frozen stdout SHA256 `a8ddf531…87dd` unchanged.
- Live review-local `grok-out/io/host-live/`: new samples, 1 passed / 253 filtered, **8/8** primary-matched; same 1/2/5 split this wall (`2026-09-21T00:41:53Z`–`00:41:54Z`). Frozen `host-r1` not overwritten. These counts are **this wall**, not a clock-independent guarantee. 305's 1 s bounds remain unqualified.

**Seven compiled controls (r2; r1 matcher setup-failure preserved):**

| Control | Rust | Independent primary | Class |
|---|---|---|---|
| `force-report-mode` | exit **0** | **rejected** (`advance`) | Rust-success / oracle-reject |
| `force-publication-mode` | exit **0** | **rejected** (`advance`) | Rust-success / oracle-reject |
| `substitute-retained-purpose` | exit 101 | not run | host-path Rust fail |
| `substitute-signed-time-for-os-wall` | exit 101 | not run | host-path Rust fail |
| `substitute-monotonic` | exit 101 | not run | host-path Rust fail |
| `substitute-boot` | exit 101 | not run | host-path Rust fail |
| `kernel-error-as-host-io` | exit 101 | n/a (deterministic mapping) | causal mapping |

The two mode controls do **not** fail cargo: the ignored host test does not assert S4 output against the primary. Forcing `report=true` or `report=false` while telemetry still carries the loop `site` is caught only when Python `clock_decision` uses that declared `reportOnly`. Live replay reproduced both as Rust 0 + `primaryRejected`. Six host-path controls execute real `observe_clock`. Frozen `mutation-check-r2/report.json` SHA256 `c52edc66…4ac0` unchanged; live core-equal.

No production or test compile correction in this freeze.

---

## Findings

### 1. Ownership / causal mapping — hold

The OS object stays owned through evaluation. Replacing wall/mono/boot in the recording, or the stored purpose, is caught against the raw sample. Kernel/recording errors are not mapped to HOST.IO_FAILURE. Sampling failures are. S4 no-write stays an evaluated proposal.

### 2. Policy / 1 s — not selected

Capture is process-global `observe_clock` with no namespace token and no installed final guard. Collection and use-age 1 s remain unqualified. This quiet-host run does not measure load, suspend, or 222 proof prep.

### 3. 306 image is not this input

`evaluate_current_ordinary` consumes 301's parsed `OrdinaryClockInput`. The host fixture still builds that via 298 `capsule_clock` on JSON values. 306's raw SHA/len image capture is **not** composed here.

**Actionable defects in this freeze:** none that make the private current-source wrapper self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 307 pins before extract | match |
| Nested 306 / 305 / 297 / kernel201 | match |
| `trust_time.rs` / 306 `captured_capsule_clock.rs` | byte-identical |
| Live `cargo test -p opensip-security` | **252 passed / 2 ignored** after force rebuild |
| Clippy / fmt / rustfmt 10 includes | pass |
| Frozen host-r1 primary replay | 8/8; 1/2/5 |
| Live host-live samples | 8/8; 1/2/5; **separate files** |
| Mode mutants | Rust 0 + primary reject |
| Other 5 mutants | Rust 101 |
| 1 s / namespace / publication | **not qualified** |

---

## Remaining (do not count closed)

306 raw retained image is not yet 301 parsed-clock input (308). Current wrapper does not prove raw/current head. OLD/R/history/T provenance, current revocation population, bootstrap/batch, namespace/custody, same-control-flow guard, 222 durable publication, post-S4 minima/completeness/role effects, writers, source selection, and M3–M6 remain open. 305 1 s is still an unqualified candidate. No operational consumer calls `evaluate_current_ordinary` outside the ignored test.

---

## Verdicts

- [x] **307 as private current-source wrapper:** archive verified; capture-after-301-input; owned sample+proposal; mapping only on sampling; 8/8 frozen and live host recordings match 201/265 using each actual observation; two mode controls distinguished as Rust-success/oracle-reject; 252/2 ignored, Clippy, fmt10, 7/7 r2.
- [ ] **Not** current-head proof, 306 image composition, qualified OS policy, publication, completeness, grant, or product installation.
