# Independent review — native store marker 358

**Standing:** bounded **storage** review of frozen `native-store-marker-checkpoint-358`. `ProvisionalStoreMarker` borrows an opaque 357 `InstallationReadFence`, parses requested **S** before IO, captures fixed `[stores, S]` / `store-instance.v1` / 128, and reuses the existing **private** two-member `DecodedMarker` codec. A match identifies **S only**. This is **not** full `(S,G,K)`, `StoreGenerationBindingV1`, namespace/handle/registry admission, selected I, or current authority. Product remains `fa72e50`. Prior 357 REVIEW `c36e96cf…a710` (8116 B, no ADDENDUM), 356 `d620c9af…e74d`, store-binding advisory `cf1903f4…17ff` (8261 B) and ADDENDUM `84da081d…9a8b` were read and are **unchanged**. Distinct from that source/ownership advisory.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir **not** overwritten. **This review reproduced:** `native_marker::` **2**, crate `opensip-storage` **96**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **3** compiled controls + two-test baseline. Security **375** and host **66** **not rerun**. Frozen author record: native-marker-r1 **2**; storage-r1 **96**; clippy-r1 `Finished dev`.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 357 archive **564 / 6904012 B / `f2d9cdd9…474e`** / 504 product pins rehashed before 358 extract. Independent rehash of 358 tar, 545 members, and extract: 0 mismatches.

Frozen archive: **6874352 B, 545 members, SHA256 `296b07c1f4bfdb2c6f4c4748e883c154fd3f687ddc9fd41c8d74455b152081cb`**. 505 product pins.

Product vs 357: **502** unchanged, **2** changed, **1** added (storage only):

| Path | SHA256 / bytes |
|---|---|
| `crates/storage/src/lib.rs` | `5bebc3e7…b9f5` / 457 (was `41dc3295…bcb2` / 329) |
| `crates/storage/src/store_root.rs` | `e00c0c0e…466d` / 26797 (was `11f04d2c…36c3` / 26738) |
| `crates/storage/src/store_root/native_marker.rs` **added** | `3f415c9e…2769` / 5393 |

`store_root.rs` is the 357 file plus `#[cfg(target_os = "macos")] pub(crate) mod native_marker;`. `lib.rs` only reexports `ProvisionalStoreMarker` and `StoreMarkerObservationError` on macOS. `Cargo.lock` and `crates/storage/Cargo.toml` byte-identical to 357. Security `installation_observation.rs` byte-identical to 357 (`966a415f…bf82`). 126 security fixtures unchanged. **No** new crate/feature, **no** security→storage, **no** storage→lifecycle. `StoreInstance`, `DecodedMarker`, `MARKER_NAME`, and `MARKER_LIMIT` stay module-private; codec visibility is **not** widened. Existing `observe_marker` / test `observe_unchecked_marker` still take a supplied `RetainedDirectoryPath` and were **not** rewritten onto the native fence.

---

## Ownership / retention / postcheck

`ProvisionalStoreMarker<'fence>` privately holds `ProvisionalHeldFile<'fence>` (357 original File + **all** relative parents under the borrowed fence) and `DecodedMarker`. `read_existing` takes `&InstallationReadFence` and a requested instance string. `StoreInstance::parse` (32 lowercase hex) runs **before** any open. Capture uses storage’s fixed `MARKER_NAME` / `MARKER_LIMIT` and prefixes `["stores", S]`. No caller path, bytes, root, or `File` injection/escape. Missing/malformed never creates I.

Private `decode_then_recheck`: always run the observation callback **after** `DecodedMarker::decode` (and the extra `> 128` Bound gate), then return decode error only if that check succeeded. Production passes `|| capture.recheck()`. `store_instance()` / `raw()` recheck the original capture first; `contributing_filesystems()` forwards to the 357 capture (which rechecks). Tests use **synthetic** callbacks only; they are not native I/fence/marker-file proof (357 remains that evidence).

A matched marker is **S only**. It does not carry `namespaceId`, `storeGeneration`, or `stateSchema`. Marker + pair, or marker + 344 `C.store` equality, is still only the advisory’s **provisional comparison**, not `StoreGenerationBindingV1`.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `native_marker::` | **2 passed** |
| `cargo test -p opensip-storage` | **96 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Security 375 / host 66 | **not rerun** |

No historical 358 source failures (native-marker-r1 is the freeze image).

---

## Mutants

Three compiled controls + two-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`0fc7ffe9a460cfa87b8d135a10375417af6bc02273f1cd51f96a5f2c211eb775`**, **byte-identical** to frozen **r1**. All **4** compiled. Request name `skip-reused-marker-instance-binding` is this freeze’s `skip-marker-instance-binding`.

| Control | First failure |
|---|---|
| `skip-postcheck-on-marker-error` | mismatch/malformed/oversize skips recheck (`calls != 1`) |
| `ignore-failed-postcheck` | decode outcome wins over observation failure |
| `skip-marker-instance-binding` | reused `DecodedMarker` S-equality not `Binding` |
| baseline | 2 `native_marker::` |

---

## Findings

358 is the planned **storage-owned S-only marker** under the same native fence: parse S before IO, 357 descendant capture with owner-fixed leaf/cap, existing private codec, recheck even on decode failure, opaque retained capture. It does **not** close G/K, namespace, handle/registry, core, profile, or current.

**Actionable defects in this freeze:** none that make parse-before-IO, decode-then-recheck order (“observation wins after decode failure”), reused marker instance binding, or “no File/root/`into_parts`” self-contradictory with the 2 tests, 96 storage tests, and 3 compiled controls.

**Coverage, not a freeze contradiction:** 358 does not call `read_existing` against a live native fence; native File/prefix/lifetime tests remain 357. Synthetic tests are labeled as such. Supplied-root `observe_marker` remains a separate conditional API.

**Must not be counted closed:** full `(S,G,K)` / `StoreGenerationBindingV1`; admitted namespace from registry; 344 `expected_store` as authority; core/profile allowlist on these Files; active-slot; `--trust-group`; 5s scheduler; create/init; current authority; writers; M2–M6. Do **not** infer full store admission from marker + pair or marker + current `StoreBinding`.

---

## Remaining (do not count closed)

Host join of 356 pair S to this marker S, then security current `StoreBinding` as **provisional comparison only** (358 ADDENDUM). 323/229 closure, 350 profile FS-name law on the **same** held Files, active-slot, invocation groups, writers. No native SQLite `File` escape.

---

## Verdicts

- [x] **358 as frozen private storage-owned S-only marker:** archive verified against parent 357; three storage-only deltas; parse S before IO; 357 capture with fixed `stores/S/store-instance.v1` cap 128; private `DecodedMarker` reused, not widened; recheck even on decode error; no `root`/`into_parts`; live 2+96; Clippy/fmt30; 3 compiled controls frozen-r1-equal. Matches the marker request, not full G/K or selected-I.
- [ ] **Not** full `(S,G,K)`, `StoreGenerationBindingV1`, selected-I/current authority, writers, or product installation.
