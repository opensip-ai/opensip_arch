# Independent review — native record reader 271

**Standing:** bounded native-Rust review of frozen `native-record-reader-checkpoint-271`. Source-bound typed edges after 270 shape admission. **Not** a shared operation Budget, complete graph walk, current/historical population, non-key subjects, other-root contexts, private-policy adoption/merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 270 (`0f32e9ec…1fd0`) and 269 were not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5247812 B, 502 members, SHA256 `60312d344afa7f4467676fc70f892d5a89a2d45e4e6c5d68445693124eb98fc1`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **502/502**. Product-inputs **398/398** live-equal.

Nested parent 270 pin `7198e69b…337e` (5673276 B / 506 / 392 files) equals the reviewed 270 freeze; live trial tar still matches; `trust-before.rs` equals that 270 `trust.rs` (`5fb3ceae…88bb`). Nested 265 `73c3b3f5…86df` and reader 232 r4 `26bf1187…e2e9` match reviewed archives. Schema `1328ba16…4208`. `trust_record_reference.py` `00ad3a34…e6df`. `canonical.py` `d47f25db…b442`. `Cargo.lock` unchanged vs 270.

Product vs 270: **398** files, **389** unchanged, **3** changed (`trust.rs` module declaration; `trust_record_shapes.rs` private `fragment_matches` bridge; `trust_record_shape_nodes.rs` drops `#[cfg(test)]` on `fragment()`), **6** added (`trust_record_reader.rs` `72762575…3229`; `trust_record_visit_nodes.rs` `e8853cab…3103`; `trust_record_reader_tests.rs`; `reader271-{extract,decode,targets}.ndjson`). Inherited 270 fixtures unchanged. Exact generator→rustfmt regeneration matches those reader SHAs.

---

## What 271 adds

Static 385 useful visitors from 929 schema locations and all **134** owner/schema-pointer registry sites. Closed internal `RecordKind` (27 roots). Generated walkers select fragment ids only; there is no caller schema/type/collection API. `lib.rs` does not name the module.

`Record::parse` runs full 270 product canonical+shape (`4MiB` / 32 containers / `[-2^63, 2^64-1]` / non-NFC) then LIFO extraction (`reversed` schema steps; array items `enumerate().rev()`). Overlapping constraints keep the **first** row. Dedup key is `(instance pointer, collection, expected kind)`; returned rows are BTree-sorted. RFC6901 pointer spelling (`~0`/`~1`). Edge limit `0..=131072`; `131073` is `Profile`. Source raw is `Arc<[u8]>`.

`decode_at(instance_pointer, actual_bytes)` uniquely selects that pointer on the immutable source. It joins SHA-256 and declared `bytes` of the **actual** target, then decodes the **source-derived** `RecordKind`. `EventRef` also joins `store`/`storeInstanceId` and `sequence`. `PublicationRef` joins `previousCapsule`. `BlobRef` (`expected=None`) returns opaque `Decoded::Blob` with no JSON/shape admission. Callers cannot supply a schema pointer, relabel a row, or forge a target type. Mutating the caller buffer after success leaves owned source/target bytes unchanged.

No shared Budget. No graph. Unrepresentable Python inputs (unknown enum, non-string pointer, forged edge rows) are listed as non-native, not claimed as Rust checks.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **205/205** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 10 compiled controls + baseline | **11/11**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | independent Rust decode/locator probes | **pass** (review-local extra test; frozen product unmodified) |
| Exact live | Python source/fixture probes | **35/35** |
| Inspected | 352 extract / 234 positive | all 27 roots and 134 sites; exact rows/order/pointers; 0 duplicate instance pointers on positives; exact and one-short limits |
| Inspected | 37 decode + 481 targets = 518 / 140 positive | every 134 site: valid target, byte tamper, and (129 typed sites) coherent hash+length wrong record type; 80 event store/sequence; 4 publication predecessor; 5 BlobRef sites stay opaque |
| Inspected | Clippy 134 leaf + 25 transitive `ptr_arg` | generator signatures only (slices on non-mutating walks); beforeimages retained |
| Inspected | 268 workspace 493+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): skip source shape (`record-shape` target admits); skip digest; skip length; skip event store; skip event sequence; skip publication predecessor; skip edge budget (`limit=0` extract admits); widen clock edge to event union (`/clock/by` ClockWriteEventV1 → TrustEventV1, `record-shape` admits).

First fail **other** assertions (not exploit proofs):

- `schema-pointer-as-instance`: overlap count 2 vs 1, then `/prior` `SourcePointer`; extract `sourcePointer` becomes the schema path `/$defs/OperationInputV1/...` instead of `/input/ref`.
- `collapse-distinct-instance-pointers`: distinct `/a` and `/b` collapse to 1; later missing `/list/body` and `/evaluation` rows that share reference bytes.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | module/`Record`/`decode_at`/`Error` not exported from `lib.rs` |
| Schema pointer as decode key | `SourcePointer`; instance pointer remains required |
| Empty / oversize / unmatched target | `ReferenceBytes`; Blob unmatched bytes never become JSON |
| `edge_limit=131073` | `Profile` before parse |
| Clock `/clock/by` | expected `ClockWriteEventV1`, not `TrustEventV1` |
| Caller buffer fill(0) | owned `raw` unchanged |
| Dedup | same `(pointer,collection,expected)` keeps first schema pointer; distinct instance pointers stay two rows |

---

## Remaining (do not count closed)

Complete shared-budget graph (never a caller old-T skip list); current/historical population and non-key subjects; other-root contexts; private-policy adoption/merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. Typed decode mints none of those proofs. 271 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 398 product files: 389 unchanged vs 270. Nested 270/265/232 pins match reviewed archives.
- [x] **205** security tests, Clippy, and fmt reproduced. Ten controls behave as documented (eight wrong admissions; two other-first on edge identity).
- [x] 270 shape precedes extract; 134 sites are source-bound; instance pointer + actual SHA/length + source-derived type + Event/Publication locators; BlobRef opaque; no public schema/type API.
- [ ] **Not** shared Budget, complete graph, current authority, native custody, or product installation.
