# Independent review — private OS observation mechanism 305

**Standing:** bounded native-Rust review of frozen `native-clock-observation-checkpoint-305`. Private `ObservedSample::capture` / `observe_age` implement the **reviewed 302 policy shape** as numeric/source evidence over actual `opensip_platform::observe_clock`. This does **not** select the 1 s bounds, admit platform/namespace, persist a write-ahead, authenticate provenance, or publish. Host-collector 304 and this freeze's one ignored host check **cannot qualify** those constants. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Prior 298–304 reports were not edited (302/303 fully read and left archived).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8867620 B, 984 members, SHA256 `87d4cd14bbe1cb36027f8975a6db80b54cb70c08e0aecf77f81eea4c0300933d`**. Standing: unselected private305 actual OS sample formation and age evidence; no host/platform qualification or publication authority. Extract rehashed **984/984**. Product-inputs **457/457**. Nested 303 pin `30913a83…5337`, 302 pin `f690bba8…953c9`, live 301 `b6db23ad…906b`, 265 `73c3b3f5…86df` all match. Included `kernel201.py` SHA256 `df45c9c5…2299`. `trust_time.rs` is byte-identical to 303 (`b76c829f…1dc4f`). Platform `clock.rs` is byte-identical to 303. Product vs 303: **457** files, **453** unchanged. Changed: `lib.rs` `28977259…3469` (private `mod clock_observation` plus `#[allow(dead_code)]`). Added: `clock_observation.rs` `7e1a4ad0…e42e`, `clock-formation305.ndjson`, `clock-age305.ndjson`. `lib-before.rs` equals 303 `lib.rs`. `ObservedSample` / `AgeObservation` / `failure_projection` are **not** in `lib.rs` (no `pub use`).

Production text of `clock_observation.rs` before `#[cfg(test)]` is **byte-identical** to `before-fixture-framing/clock_observation.rs`. The fixture-framing correction changed only fixture selection and test counts.

---

## What the mechanism does

`ObservedSample::capture()` takes **no** caller clock, context, timeout, or JSON. It calls `observe_clock()`, retains that exact opaque `ClockObservation`, and projects via private `Parts` filled **only from getters** (`wall_unix_seconds`, `wall_nanoseconds`, `monotonic_before`/`after` as secs+subsec nanos, `boot_id`). There is no production path that accepts a serialized 301 `RecordedObservation` as an OS sample.

`project`: refuse nanos ≥ 1 s; wall calendar via **303** `format_timestamp` (year 0001..9999 ISO); boot 36-byte lowercase hex UUID with dashes at 8/13/18/23; checked `u128` monotonic endpoints; `after.checked_sub(before)` (regressed); **inclusive** collection span `span > 1e9` refuses so `1e9` is accepted; midpoint `before + span/2` then floor-second `i64` (overflow → `MonotonicRange`). Recording is closed `{wall: ISO string, mono: Integer, bootId}` — the same document 301 `RecordedObservation::admit` already parses (ISO wall through `timestamp_seconds`, Unicode boot 1..=256). 305's producer is **stricter** on boot (UUID) than 301's historical admit.

`observe_age(site)` captures a **new** actual sample, then `age`: same boot; `guard.before >= original.after`; inclusive total age `guard.after − original.before` (`> 1e9` refuses). `AgeObservation` **borrows** the original and **owns** the guard; `UseSite` has only `ClockPublication` / `CurrentReport`. Fields are measurement facts. Nothing in host/security/storage consumes this type. `observe_age` does not branch on `site`; both purposes share the same numeric predicate, matching 302.

`Failure` preserves `ClockError` / `ProjectionError` / `AgeError`. Private `failure_projection` **ignores** the variant and always emits `{termination: {class: operational-failed, errorCode: HOST.IO_FAILURE, faultCause: host-io}, exitCode: 4}` with **no** `domainDetail`. It does not call storage, mark corruption, or retry. It is **not** wired to workflow termination; it is a demonstrated mapping, not an installed host arm. Earlier NT-TCB / cancel / observer / historical-decode / S4 / publication owners are not this enum.

Reference: frozen 300 formation **132 / 55** and 302 age **237 / 89**. Native executes only Rust-representable rows: formation **80** (55 positive / 25 typed refuse) and age **183** (89 / 94). Excluded **52 / 54** (JSON type/range/field-set, plus 302's `historical-replay` and `effect-grant`) stay outside the typed API and are **not** claimed as native runtime rejections. Original corpora remain in `verified-policy302`. Native fixtures contain only representable lines (formation 80, age 183: 107 `publish-clock` + 76 `report-current`).

Initial integrated log is retained: **248 passed / 2 failed / 1 ignored** because product JSON refused Python `u64+1` (`IntegerRange`) **before** projection. Fix selected already-computed representable rows and updated counts `[52,55,25]→[0,55,25]` and `[… ]→[0,89,94]`. Production prefix unchanged.

**Executed:** `cargo clean -p opensip-security` then **250 passed / 0 failed / 1 ignored** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 14/14 r2 compiled controls core-equal frozen `mutation-check-r2` (`report.json` SHA256 `da371230…e2cf`). Frozen `mutation-check-r1` is the matcher setup failure only (rustfmt split `guard.after.checked_sub`); r2 matcher-only. Frozen mutant/host dirs not overwritten.

**14 compiled controls (all caught):** `span-too-wide`; `span-exclusive`; `before-instead-of-midpoint`; `after-instead-of-midpoint`; `round-wall-nearest`; `truncate-endpoint-seconds`; `monotonic-overflow-wrap`; `use-age-too-wide`; `use-age-exclusive`; `age-from-original-after`; `age-to-guard-before`; `omit-same-boot`; `omit-guard-order`; `failure-as-busy` (`LEDGER.BUSY_TIMEOUT`).

**Ignored host check (separate invocation, frozen `host-pilot-r1` untouched):** source SHA256 `7e1a4ad0…e42e` (matches module). Frozen: span **20333 ns**, age **142208 ns**, 1 passed / 250 filtered. Live this review: span **18833 ns**, age **141500 ns**, exit 0, 1/250 filtered. Checks raw W/B/M against the retained platform object and age against raw endpoints. **Not** portable profile, load, suspend, VM, namespace, or publication qualification.

---

## Findings

### 1. Getter / ownership / type boundaries — hold

`capture` cannot be fed a clock or a 301 recording. `ClockObservation` stays owned, not rebuilt from `{wall,mono,bootId}`. JSON `input()` exists only in tests and only after product JSON already decoded. `AgeObservation` borrows the source (`ptr::eq` in the host check) and is not a permit type. No public export; `#[allow(dead_code)]` is honest — no operational consumer.

### 2. Policy numeric fidelity — shape matches 302; 1 s still unqualified

Inclusive 1 s collection, inclusive 1 s use-age from original.before to guard.after, same-boot and guard order, floor-second wall via 303 codec, checked u128 midpoint-then-floor M, lowercase UUID, existing HOST.IO_FAILURE arm, no CLOCK.* mint, no wall-only fallback. Mutants cover the endpoints 302 cared about.

**1 s remains an unqualified candidate.** `MAX_SPAN` and `MAX_USE_AGE` are the same `1e9` envelope. This quiet-host check (~20 µs span / ~140 µs age) and 304 do **not** measure load, suspend, or long 222 proof prep. Do not select 1 s from this archive.

### 3. Host ordering / context — correctly not implemented (must stay remainder)

`capture()` is a process-global `observe_clock()` with **no** admitted platform/namespace/custody argument. `observe_age` recaptures immediately; nothing enforces “no work between guard and dispatch.” `AgeObservation` can be held for the borrow lifetime. `failure_projection` is not a host terminator. Pre-existing `observe_clock` callers (`revocation.rs`, `lifecycle/leases.rs`) are **unchanged vs 303** and do not use this module. Required same-control-flow guard, 222 orphan vs clock fields, and namespace admission remain **open**. The freeze does not pretend otherwise.

### 4. Mapping — existing arm, still operationally coarse

Witnessed JSON matches 302. `failure-as-busy` is caught. Coarseness from 302 stands: host-io recovery must not treat sample-age as storage corruption. This function cannot cause that; a future consumer could.

### 5. No S4 / role / effect in this module

Formation positives are `RecordedObservation::admit`-checked as document shape only. `evaluate_retained_ordinary` / write-ahead / publication are not called.

**Actionable defects in this freeze:** none that make the private numeric mechanism self-contradictory.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 305 pins before extract | match |
| Nested 303 / 302 / 301 / 265 / kernel201 | match |
| `trust_time.rs` / platform `clock.rs` vs 303 | byte-identical |
| Production `clock_observation` prefix vs before-fixture | byte-identical |
| Representable native cases | 80 = 55/25; 183 = 89/94 |
| Live `cargo test -p opensip-security` | **250 passed / 1 ignored** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 305 r2 mutants | 14/14 frozen-equal |
| Host check | live 18833 / 141500 ns; frozen 20333 / 142208 ns; **not qualification** |
| 1 s freeze / OS / product | **not decided by this archive** |

---

## Remaining (do not count closed)

Numeric 1 s collection **and** use-age still need profile/load/suspend/proof-prep measurement. Observed samples do not admit current platform/namespace/history/provenance or authorize filesystem action. Complete observed-source-to-301 S4 ownership, storage-owned publication gate, 222 durability, post-S4 minima/role effects, custody/fence/census/writers, source selection, and M3–M6 remain open. 304 is not this review and does not qualify 302.

---

## Verdicts

- [x] **305 as private mechanism:** archive verified; actual `observe_clock` owned with getter-only scalars; 303 codec; 302 numeric/age/mapping shape; typed API excludes 52/54 non-representable rows honestly; 14/14 mutants; 250/1 ignored; one actual-host check recorded separately.
- [ ] **Not selected, not qualified, not installed.** 1 s is still an unqualified candidate. No publication, current authority, or product installation follows.
