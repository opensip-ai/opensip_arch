# Independent review — native payload path preflight 262

**Standing:** bounded native-Rust review of frozen `native-payload-paths-checkpoint-262`. Pure payload2 declaration preflight (logical NFC + Unicode 15 casefold alias, reserved exact frames, cross-slot aliases, file-parents, RA envelope listed once) plus 261-bridge requiring **that signed manifest’s** preflight. **Not** listed-envelope index pairing/ambiguity/presence/preimage, extra RA envelope rules, member I/O/capture order, catalog/list/component/policy/repair/artifact, aggregate Operation, current+incoming revocations, or native publication. Archived 261 `REVIEW.md` (`988feaec…3492`) and `CORRECTION.md` (`0f559fdd…0acd`) were not edited. 259 workspace 472+2 was **not** rerun. Installed product remains `fa72e50`.

Rust 1.95.0. Review-local `product/` copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **4328076 B, 473 members, SHA256 `f78a584de4f8e926673cc20b2b99457dd163d36df936cddb9dca0e7f157a03cd`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 473/473.

Parent 261 pin `4eff98e1…61bc` matches the reviewed 261 archive. Nested 258 pin `b36518ef…f622` matches reviewed 258. Reviewed Index `trust_metadata_index_reference.py` SHA `be87c4c3…f1b7` is byte-identical to that 258 candidate file.

Product: **367** files vs 261. **360** byte-identical, **2** changed (`trust.rs`, `lib.rs`), **5** new (`metadata_casefold15.rs`, `casefold15-mappings.json`, `payload-paths262-{logical.json,cases.ndjson,signed.ndjson}`). Inherited 261 fixtures byte-identical. `trust.rs-before` equals 261 `trust.rs`. Product-input hashes match 367/367.

`lib.rs` vs `lib.rs-before` adds `metadata_casefold15`; vs `lib-before-format-order.rs` is declaration-order only (`mod metadata_casefold15` moved). `trust.rs` after r1 gained the 6-case signed-bridge test; algorithm bytes match the compiled controls (`1d5ac4d1…1fde`).

---

## What 262 adds

Private `admitted_payload_paths`. `logical()`: 1–1024 characters, Unicode 15 NFC, no ASCII `letter:` drive prefix, no `\` or **NUL anywhere** (closes 261 first-character NUL syntax allowance), no empty/`.`/`..` segments. Alias = NFC(Unicode 15 full casefold). `admit()`: payload2 `payload_shape`; count all slot rows (max **131072** before allocating the row list); derive kinds from slots; refuse exact aliases `payload.json` / `payload.sig.json`; refuse duplicate aliases and file-parent prefixes; require the RA **envelope** object exactly once in `members.envelopes`. Returns owned immutable path/digest/kind map. **No member I/O.**

261 `verify_recovery_bundle_document` now calls `admit` on **its own** parsed signed payload. An unrelated valid preflight must not substitute.

Unicode 15 full casefold: 1530 mapped scalars from pinned Python 3.12.13; identity elsewhere. Exhaustive nonsurrogate-scalar fingerprint `b6b067c3…e891`. Existing Unicode 15 NFC adapter reused. Conformance to that selected reference, not whole-toolchain authentication.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **183/183** (38 logical, 28 preflight/5 positive, 6 signed integration 5+1, exhaustive casefold) |
| Exact live | workspace Clippy `-D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 6 compiled wrong-admission controls + baseline | **7/7**, SHA equal frozen `mutation-check-r1` |
| Inspected | 258 Index oracle | unmodified; TESTONLY capture sentinel; not full Index admission |
| Inspected | r1 fixture harness notes | invalid Unicode escape; then report-name shadow; driver-only, production unchanged |

Controls (all **wrong admission** of a signed case): ASCII-only fold; skip alias insert; skip reserved frames; skip file-parent; skip RA envelope membership; substitute an unrelated valid preflight manifest.

---

## Bounded edge: `payload.json/child`

Pure preflight **admits** `reserved-frame-descendant-is-only-preflight` because reservation is **exact** alias `payload.json` / `payload.sig.json`, not descendants. Native case records that inherited Index allowance. It does **not** prove a realizable delivery filesystem, writes, or capture. No new owner is invented here; remaining listed-envelope/index pairing stays pending.

---

## Independent probes

| Probe | Result |
|---|---|
| First-char NUL | logical refuses `\0a` and `a\0b` |
| Exact reserved frames | `payload.json` / `PAYLOAD.SIG.JSON` refuse; `payload.json/child` allowed at this stage only |
| No `std::fs` in preflight | absent |
| 261 own-manifest bridge | `unrelated-valid-preflight` admits wrongly when substituted |
| 261 REVIEW + CORRECTION | hashes unchanged |

Successful preflight is not complete Index admission, custody, or listed-path reads.

---

## Remaining (do not count closed)

Listed-envelope index pairing/ambiguity/limited capture/presence/preimage/extra RA envelope rules; full catalog/list/component/policy/repair/artifact; aggregate Operation; complete current+incoming revocations/held selection/ancestry/floors/S4; batch/effects/fence/slot/census/durability/writers; source selection; M3–M6. Payload1 path preflight is not in this recovery-only stage. 262 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 367 product files: 360 unchanged vs 261. Index byte-equal 258.
- [x] **183** security tests, Clippy, and fmt reproduced. Six wrong-admission controls caught; baseline passes.
- [x] Logical NFC/casefold/NUL-anywhere; exact reserved frames; own-manifest 261 bridge; no preflight I/O. 261 first-NUL syntax gap is closed here.
- [ ] **Not** full index pairing, member capture, current authority, filesystem realization of `payload.json/child`, or native publication.
