# Independent review — native diagnostics 353 (350 follow-ups)

**Standing:** bounded native-**security** review of frozen `native-diagnostics-checkpoint-353`. Two 350 follow-ups: (1) preserve **generic** `retained_metadata_index::Error::Capture` while an **owned** `NativeStore::complete` adapter can return the first native cause; (2) `ProfiledCensus` constructor refuses ExactMeasured **with** identity refusals before census I/O. **`complete` is not on the `Store` trait.** A generic `Store::read` caller is **not** type-forced to call it. This is **not** selected S/core/profile, current authority, writers, or product install. Product remains `fa72e50`. Prior 352 REVIEW `9a2fbd3f…f18e`, 351 `ca61ae4c…534f`, and 350 `a2815d6b…d084` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir not overwritten. **This review reproduced:** `native_diagnostics_` **4**, `native_store_` **6**, `native_current_` **6**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** includes, **6** compiled controls + four-test baseline. Full security **363** **not rerun**. Frozen author record: security-r1 363/0/2.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 352 archive **561 / 6887244 B / `0d319b84…485f`** rehashed before 353 extract. Independent rehash of 353 tar, 556 members, and extract: 0 mismatches.

Frozen archive: **6880856 B, 556 members, SHA256 `14c04924f877797d0492e828f555a5b45b776b75a1906087a862ed7f671ea4d3`**.

Product vs 352: **498** unchanged, **3** changed, 0 added/removed:

| Path | SHA256 / bytes | Production vs 352 |
|---|---|---|
| `trust/native_record_capture.rs` | `d0cf5772…9965` / 44200 | `complete` + `read_failure` |
| `trust/native_current.rs` | `dbdeae4e…f384` / 25177 | `capture_p2` wraps both loads |
| `trust/native_census.rs` | `b23cde12…8f19` / 38492 | **tests only** (production byte-identical) |

126 security + 2 dyld fixtures unchanged (128). No dependency change. Generic index `Error` still `#[derive(PartialEq, Eq)]` with unit `Capture` (no native IO).

---

## Generic Capture vs owned native completion

`Store::read` still returns `M::Error::Capture` on native failure and stores **at most the first** `native_record_capture::Error` in `read_failure`. `complete(result)` is a `NativeStore` method: pending native **wins even over `Ok`**; else `Logical(caller error)`. No extra IO, retry, error list, or Budget charge. `take()` consumes the pending cause (one first failure).

`capture_p2` is the **only non-test** `NativeStore` factory and the only production `complete` call site: after D/`load_at` **and** after nested `current_record_bindings::bind`, mapping `Native(source)` → `Error::Immutable(source)` before drop. Later 350 `store.recheck().map_err(Error::Immutable)` is unchanged.

**Not a type-enforced completion claim.** `trait Store` has only `read`. A caller that uses `NativeStore` solely as `impl Store` still sees category `Capture` unless it also calls `complete`. Dropping the store without `complete` drops the owned cause. That boundary is explicit, not a generic-enum redesign or a capability.

Preserved nested source for missing file: `ReadCompletionError::Native(Error::Capture(Open(NotFound)))` — the **native** `Error` tree, not flattened `io::Error` and not only generic `Capture`.

---

## Exact-tier constructor refusal

Fresh **correctly signed SYNTHETIC** profile: clone unverified payload from a verified fixture, set measured `build`/`kernUuid` from actual host, **wrong** `dyldCdhash`, sign with deterministic quorum-62 test seeds whose public keys **match** fixture `publicKey` bytes (`ed25519_dalek` `SigningKey`/`Signer`; TEST ONLY). Normal `verify_profile_set` (envelope/corePin/root role/empty revocations). No frozen fixture mutation. `native_platform::capture` → `ExactMeasured` + `NT-TCB-IDENTITY:dyldCdhash`. `native_profile_census::capture` → `ProfileRefused` **after `state.v1` is removed**, `foreign_calls==0`, counters `(0,0,0)`, Budget `Closed`. Tier alone does not admit.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-r1 | **2 pass / 1 fail** (3 tests) | TEST expected outer `Native(NotFound)`; actual `Native(Capture(Open(NotFound)))`; **TEST-only** fix; production unchanged; beforeimage/assessment kept |
| native-r2 | **4 pass** | added missing-prefix D / nested operation `Immutable(Native(NotFound))` |
| Clippy-r1 / security-r1 | Clippy; **363**/0/2 | this review did not rerun 363 |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `native_diagnostics_` | **4 passed** |
| `native_store_` | **6 passed** |
| `native_current_` | **6 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Full 363 | **not rerun** |

---

## Mutants

Six compiled controls + four-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`86e5b801ff8a5f644aadb57f4fff482e914833ed67f5fc62f6a5210f6829b228`**, **byte-identical** to frozen **r1**. All **7** compiled.

| Control | First failure |
|---|---|
| `discard-native-source` | pending cause not stored |
| `accept-swallowed-failure` | `Ok` wins over pending native |
| `flatten-native-source` | `Error::Changed` instead of original `Capture(Open(NotFound))` |
| `publication-load-bypasses-completion` | D load not `Immutable(native)` |
| `nested-bindings-bypass-completion` | nested records load not `Immutable(native)` |
| `tier-bypasses-constructor-refusals` | ExactMeasured + refusals not `ProfileRefused` |
| baseline | 4 `native_diagnostics_` |

---

## Findings

353 answers the 350 diagnostics **without** making generic `Store` carry native IO or forcing `complete` in the type system. `capture_p2` is the owned completion path. ExactMeasured with identity refusal cannot construct `ProfiledCensus`.

**Actionable defects in this freeze:** none that make `read`/`complete`/`capture_p2`/`ProfileRefused` self-contradictory with the 4+6+6 tests and 6 compiled controls.

**Must not be counted closed:** selected S/core/profile; `--trust-group`/privilege; current authority; original T; writers; durability; M2–M6. Direct generic `Store` callers still see `Capture` unless they use native `complete`.

---

## Remaining (do not count closed)

Selected S/core/profile-root, admitted groups, 5s scheduler, original T, writers, current authority, Linux/Intel, M3–M6. Generic-`Store` category-only errors remain for non-completing callers by design.

---

## Verdicts

- [x] **353 as frozen private native diagnostics:** archive verified against parent 352; three deltas (`native_census` tests-only); generic `Capture` preserved; `complete` owned not trait-enforced; `capture_p2` both sites; ExactMeasured+refusals `ProfileRefused` before census; live 4+6+6; Clippy/fmt30; 6 compiled controls frozen-r1-equal; r1 TEST nested-cause mismatch **not** a production pass.
- [ ] **Not** selected-S/current authority, type-enforced completion for every `Store` caller, writers, or product installation.
