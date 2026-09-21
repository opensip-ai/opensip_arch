# Independent review — native Store integration 343

**Standing:** bounded native-**security integration** review of frozen `native-store-integration-checkpoint-343`. A budget-aware `Store` + opaque `ReadRequest` replace 66 flat collection/digest/cap callback bounds across 17 files. `NativeStore` **borrows** a 341 fence and **owns** 342 `Captured` Files/prefix handles. Default `refresh_cached` is true (native always revisits the requested path); digest closures set it false and remain supplied-byte fixtures with **no** native custody. Structural evidence values (`CapturedClock`, graph `Evidence`, traces) can **move out** with no fence lifetime; the caller **must** keep Store/fence alive through consumption. This is **not** selected I, native current, census, original T/action, writers, FS qualification, or an authority token. Installed product remains `fa72e50`. 342 REVIEW `759f16e8…b0ae` and 341 REVIEW `0731e5b1…beb9` were read and are **unchanged**.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **Final (this review reproduced):** security **318 / 2 ignored**, platform **73** serial, Clippy `-D warnings`, fmt of 25 included modules. Frozen workspace-r2 **640 / 0 / 2** serial is recorded; **this review did not re-run the full workspace** (cost). No new `unsafe` or dependency. Fixture **bytes/names/verdicts/counters** are byte-identical to 342 (126 files). libc `=0.2.189`. `installation_fence.rs` SHA `e3547afc…302a` identical to 342.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of the live tar, all 602 tar members, and the extract: 0 mismatches.

Frozen archive: **6977700 B, 602 members, SHA256 `b9e7e4125a138809aa1564bcea92823b1e78da01da972ec2ff2cb6b84f575e57`**. Extract 602/602. Parent 342 live tar SHA `5b1ccb9b…a755` (6849716 / 619 / 490).

Product vs 342: **470** unchanged, **20** changed, 0 added/removed. The 20 are 19 security files plus **TEST-only** `locks.rs` `println!("\nLOCKED")`. `store-interface-sites.json` is authoritative: **66** sites / **17** files (sum verified). The other two security deltas are `native_record_capture.rs` (NativeStore + factored `reference_parts`) and `trust_record_reader.rs` (`initial_publication_store`).

---

## Store, ReadRequest, cache flags

`Budget::load_at` charges one **logical edge first**, then `reference_parts` (exact 127 member set, SHA/length, Event store+seq, Publication previous/Null, StoreId only when Publications+Null), then constructs `ReadRequest` and calls `store.read(same Budget, request)`. SHA and declared length are checked after the adapter returns. `load()` is the NodeRef/BlobRef convenience and always passes `initial_store: None`. Native Event/Publication location requires the full typed reference on `load_at`.

`Store::refresh_cached` defaults **true**. `NativeStore` does not override it. Digest closures implement `Store` with `refresh_cached=false` and ignore everything on the request except `(collection, digest, length)` — they make no path, presence, or custody claim. On a cache hit with `refresh_cached=false`, `load_at` returns the held `Arc` **without** `store.read`. That is the fixture layer, not a native skip.

On a NativeStore cache hit, objects/bytes are **not** recharged (`retain` returns the existing `Arc`; tests assert `ptr_eq`). Prefix/directory/file **edges** are charged again because `store.read` still runs `capture(..., presence=true)`. Example: objects first `(3,6,3)` then second `(3,12,3)` with `captures.len()==2`. 342 capture-only objects were `(3,5,3)`; the extra edge is the new logical `load_at` charge.

`NativeStore::read` maps every native capture error to `M::Error::Capture`. Fence/Changed/Length/Reference distinctions remain on `capture`/`recheck`, not on the Store trait. Failures still latch the Budget.

---

## NativeStore lifetime and Files

```text
NativeStore<'f> { fence: &'f SuppliedInstallationFence, captures: Vec<Captured<'f>> }
```

`read` always calls 342 `capture` with the request's collection/reference/initial S, pushes the owned `Captured`, and returns a clone of the charged raw `Arc`. `recheck` is fence + every owned capture + fence. Dropping captures (`drop-retained-files`) leaves structural JSON/Arc values while `captures.len()` is 0 — owned Files are gone. Caller-retained evidence is **not** a grant and does not keep the fence or Files alive.

Directory identity is still charged **after** retained handles exist (same 342 disclosure). Full-reference preflight is factored as `reference_parts` and keeps 342 shape/path rules; Locator still requires initial S for `initial/S/H`.

---

## Initial S provenance (r1 production join)

342 capsule capture stripped publication to `{sha256,bytes}` and loaded Publications through the old digest callback. 343 passes the **full** `publication` PublicationRef:

- `captured_capsule_clock`: `initial_store = store.storeInstanceId` **only** when `publication.previousCapsule == Null`. Not the full store object (r1 defect: 305/7).
- Graph `Record::initial_publication_store(pointer)` returns that ID only for schema pointer `/$defs/TrustCapsuleV1/properties/publication`. Other initial publication edges return `Ok(None)` and stay unresolved. Nested capsules are walked from the immutable source record, not the nearest store field.
- Explicit `walk_at` / prepared-outcome `walk_at` take caller initial S at the root. `walk()` is `walk_at(..., None)`. Missing S on an initial Publication refuses in `Locator` before file IO (`captures` empty; counters `(0,1,0)` from the logical edge). Cached raw does **not** supply missing S while `refresh_cached` is true (mutant that defaults it false makes `graph::walk` after a prior hit succeed).

Restore-declaration `examinedOrphans` are **not** Store-loaded. The owner only requires `previousCapsule == beforeImage.sha256` (order + bucket). Schema-null orphan refs cannot gain a guessed S. Restore-proof publication loads use `PublicationRef` + `load_at(..., None)` because chain/terminal refs have non-null predecessors.

Successor bind: full `PublicationRef` pre-IO, `load_at(Publications, ref, None)` — correct `by-predecessor` route. Event replay (`current_event_trace`, `bind_events`) keeps EventRef + `Collection::Events` (the r1 generic Event→NodeRef miss).

TEST `write_rows343` derives native paths from fixture **record content** (event.store string vs capsule `store.storeInstanceId`; `raw`/`rawHex`). That is not Locator and not a production hash search. outcome273 input-mode completes a PublicationRef `previousCapsule` from **already supplied fixture bytes** in the in-memory map; fixtures/verdicts/counters unchanged.

---

## Failure history (must not be hidden)

| Run | Result | Cause | Production? |
|---|---|---|---|
| security-r1 | **305 pass / 7 fail / 2 ignored** | initial S = full store object; generic Event load still NodeRef | **yes, then corrected** |
| security-r2 | **compile fail** | test called `CapturedClock` accessors on `Record` (`image().capsule()` / `.descriptor()`) | test-only |
| native-store-r1 | **4 pass / 2 fail** (`native_store_` filter) | fixture writer `no entry found for key` (`raw` vs `rawHex` / event.store) | TEST writer |
| security-r3 | **315 pass / 2 fail / 2 ignored** | event-trace writer + outcome273 input-mode bare PubRef | **TEST adapter** from already-supplied fixture bytes; **no native hash search** |
| mutation-r1 | 9 compiled controls + 6-test baseline **passed** | before platform newline | — |
| workspace-r1 | **HUNG**; SIGTERM only own child **PID 72108**; **72 pass / 1 fail** (`kernel_releases_lock_after_holder_process_is_killed`) | serial libtest prefixes `LOCKED`; parent waited exact marker | **TEST-only** leading newline; **FileLock production unchanged** (existing `flock` `unsafe`) |
| security-r4 / Clippy-r3 / workspace-r2 | 318/2 ignored; Clippy; **640/0/2** recorded | — | — |

security-r1 failed tests (not originally-green production runs): `captured_capsule_matches_primary_raw_binding_and_budget`; `current_candidate_binds_operation_outcome_and_trace_without_minting_native_standing`; `captured_sources_and_authentication_share_budget_and_remain_owned`; `current_operation_graph_and_typed_inputs_bind_outcomes_on_the_same_budget`; `full_structural_graph_matches_current_guarded_shared_budget`; `absence_and_continuity_descriptors_share_exact_prior_budget_and_owned_inputs`; `creation_declaration_and_admission_input_joins_match_current_reference`.

---

## Live cargo (this review)

Review-local copy, `RUST_TEST_THREADS=1`, `cargo clean -p opensip-platform -p opensip-security`, `--offline --locked`:

| Kind | Result |
|---|---|
| `cargo test -p opensip-platform` | **73 passed / 0 failed / 0 ignored** |
| `cargo test -p opensip-security` | **318 passed / 0 failed / 2 ignored**; 113.47s; all 6 `native_store_*` ok |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **25** included modules (23 `trust.rs` + 2 `custody.rs`) | exit 0 |
| Full workspace 640 | **not re-run**; frozen `workspace-counts.json` records 640/0/2 |

Six integration tests cover the five routes (objects/records `(3,6,3)`; events/by-predecessor/initial `(5,10,3)`), cache `ptr_eq` + second File, unlink then fail, malformed Event/Pub as Records **pre-callback** (`calls==0`, `(0,1,0)`), missing initial S (`captures` empty), exact/one-short/shared object budget, 306 initial C-D **`(7,16,3234)`** vs legacy digest-closure **`(2,2,3234)`**, three 325 event traces, 272 Event/Publication/Capsule graphs plus prepared-outcome `walk_at` with explicit root S.

---

## Mutants

Nine compiled controls + **six-test** `native_store_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`0668181eb38a3a185b9775b175e0bd61f02f8b5c23c365af4926c6a576d50b2b`**, **byte-identical** to frozen r1. All **10** compiled. Five mutated source pins match final product (`trust.rs` `997ab0f1…34b4`, `native_record_capture.rs` `1ab180e6…eb91`, `captured_capsule_clock.rs` `33ce69b5…e27e`, `current_event_trace.rs` `5b9e5f16…2258`, `trust_record_reader.rs` `ceb87d32…02d0`).

Actual first failures (live stdout, not the summary-parser mix of later asserts):

| Control | First failure |
|---|---|
| `native-cache-skips-presence` (`refresh_cached` default false) | capsule recapture **after unlink succeeds** from cached raw; all-routes second load `(3,7,3)` vs `(3,12,3)`; `graph::walk` without S succeeds on cache |
| `drop-retained-files` | `captures.len()` 0 vs 2 (event-trace `!captures.is_empty()`; capsule 0 vs 2) |
| `fresh-native-budget` (hidden `Budget::new(65536,…)`) | capsule **`(2,2,3234)` vs `(7,16,3234)`** — operation budget sees only legacy digest-closure work |
| `skip-store-recheck-files` | `store.recheck().is_err()` after unlink |
| `drop-capsule-initial-context` | initial C-D `unwrap` |
| `strip-event-location` | event-trace `unwrap` |
| `drop-source-capsule-context` | graph `unwrap` (schema-owned S) |
| `drop-root-initial-context` | graph `unwrap` (explicit root S) |
| `skip-logical-load-edge` | capsule `(7,14,3234)` vs `(7,16,3234)`; malformed pre-IO `(0,0,0)` vs `(0,1,0)` |
| baseline | 6 `native_store_` tests, 1.24s |

---

## Findings

The Store join is the required migration of 66 bounds onto 342 locators + 341 fence. 342 remaining (“callbacks still cannot use these locators”) is addressed **for those 17 files**. Initial S is now the closed capsule `storeInstanceId` / schema-owned source, which is what r1 lacked.

**Reproduction of the r1 production defect:** passing the full store object as initial S is refused by StoreId/127 shape; NativeStore then cannot locate `initial/S/H`. Corrected source uses `object(&c["store"])["storeInstanceId"]` and `capsule.store.storeInstanceId` at the schema-owned publication pointer only.

**Reproduction of cache/ownership:** `drop(captured)` still returns bytes; `captures` is empty and unlink/recheck tests fail. `refresh_cached=false` makes a second `load_at` skip native presence so unlink does not fail recapture and missing S is not observed on a cache hit. A hidden NativeStore Budget reproduces the **legacy** `(2,2,3234)` pair on the caller Budget.

**Not defects vs stated standing:** evidence types have no `'f`; Store collapses native errors to `Capture`; restore orphans are predecessor-keyed and unread; `HostCapture` path reads remain a separate nested-metadata adapter; digest closures may load Publications without S because they never build a path.

**Actionable defects in this freeze:** none that make Store/`NativeStore`/locator provenance self-contradictory with those bounds on the reproduced 318+73 tests and nine compiled controls.

**Must not be counted closed:** selected I; native current; `state.v1` reader; separate current-path budget; P2 local joins; original T/action; writers; FS profile; Linux; M2–M6.

---

## Remaining (do not count closed)

Root-next: actual `state.v1` reader, separate current-path budget, P2 local joins — **not** in 343. Fence-through-consumption is a caller obligation, not a type-system grant. 337 profile; M2–M6.

---

## Verdicts

- [x] **343 as frozen private Store integration:** archive verified; 342/341 preserved; 66/17 Store migration; NativeStore borrows fence/owns Files; initial S from closed capsule ID; live 318/73; Clippy/fmt25; 9 compiled controls + 6-test baseline frozen-r1-equal; r1–r3/workspace hang **not** hidden.
- [ ] **Not** selected-I/current authority, census, original T, writers, or product installation.
