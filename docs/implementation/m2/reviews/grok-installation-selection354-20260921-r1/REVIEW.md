# Independent review — lifecycle selection.pair codec 354

**Standing:** bounded **lifecycle codec** review of frozen `installation-selection-checkpoint-354`. Private `Selection::decode` owns exact bytes of the five-member working `InstallationSelectionV1` after a 4096-byte cap and product-canonical JSON. This is **not** native File/root/fence/FS custody, marker/full `(S,G,K)` / core-closure binding, selected I, current authority, or product install. It matches the selection-boundary advisory’s **codec layer** (lifecycle + identity, no host join). Product remains `fa72e50`. Prior advisory `a5947b69…8ba3` (10464 B) and 353 REVIEW `5fb5ea84…9b5b` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir not overwritten. **This review reproduced:** `selection::` **5**, all lifecycle **20**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **7** compiled controls + five-test baseline. Full security **363** / workspace **681** **not rerun**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 353 archive **556 / 6880856 B / `14c04924…a4d3`** rehashed before 354 extract. Independent rehash of 354 tar, 567 members, and extract: 0 mismatches.

Frozen archive: **6902344 B, 567 members, SHA256 `e155b80152ecde1a008c9ad842fd1da4c21037763eb693cfde523c94a743f859`**.

Product vs 353: **497** unchanged, **4** changed, **1** added:

| Path | SHA256 / bytes |
|---|---|
| `Cargo.lock` | `f2a830c1…66c3` / 12891 |
| `crates/lifecycle/Cargo.toml` | `2f96c01f…f483` / 240 |
| `crates/lifecycle/src/lib.rs` | `ac0fe019…d683` / 209 |
| `crates/lifecycle/src/locations.rs` | `6f629eec…25aa` / 12889 |
| `crates/lifecycle/src/selection.rs` **added** | `c16a908a…32fd` / 10612 |

126 security + 2 dyld fixtures unchanged (128). **No** security or platform source change. Cargo.lock: 61 packages, ordered name/version identical to 353; the **only** body diff is `opensip-lifecycle` gaining path dep `opensip-identity` (no external crate/feature). Lifecycle still has **no** security or storage dependency.

Source-audit copies match pins (`physical-owner203.md` `292dbab3…e5ac`; 127 `a0431300…7928`; inventory v32 `105a260d…b72e`). Independent rehash: frozen 222-r6 **165 / `5b6df2a5…1d5c`**, 312 **559 / `f04b5b42…6e5b`**. Inventory v32 SHA is in product `design-lock.json`. 203 has **no** dedicated InstallationSelection JSON Schema; five fields compose 127 `ClosureId` + `StoreId` + `I64NonNegative` + `StateSchema` + `selectionSchema:1`.

---

## Codec (advisory layer A)

`pub(super) Selection::decode(&[u8])`: cap **before** `parse_json`; closed five names (`selectionSchema` int 1, `coreClosure` `closure2:`+64 lower-hex, `storeInstanceId` via existing `StoreComponent::parse`, `storeGeneration` 0..=i64::MAX, `stateSchema` 1|2); then `canonical_bytes == raw`. Duplicate keys/floats/invalid lexemes are identity `Decode`. Extra/missing/renamed members `Shape`. No I/O, path, fence, or environment. `StoreComponent` is `pub(super)` parse + `as_str` only (not crate-public). Module is `#[allow(dead_code)]` private; no public grant.

This is the advisory’s smallest codec: identity for product JSON, **not** lifecycle→security, **not** a native join.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| installation-selection-r1 | **TEST compile fail** | `b"[]"as` invalid suffix; library/lock already passed; TEST whitespace only; noncanonical case narrowed to `":"` → `": "` so closure contents stay intact; production unchanged; beforeimage kept |
| r2 / lifecycle-r1 / Clippy-r1 | **5** focused; **20** lifecycle; Clippy | this review did not rerun 363 |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `cargo test -p opensip-lifecycle selection::` | **5 passed** |
| `cargo test -p opensip-lifecycle` | **20 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** security includes | exit 0 |
| Full 363 / 681 | **not rerun** |

---

## Mutants

Seven compiled controls + five-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`7e30be184c8133de3ab50643452b5d8488f5f786b7533e6924725677de06e0eb`**, **byte-identical** to frozen **r1**. All **8** compiled.

| Control | First failure |
|---|---|
| `skip-preparse-cap` | 4097 bytes not `Bound` |
| `allow-extra-fields` | extra member not `Shape` |
| `allow-wrong-closure-length` | 65-hex `closure2:` accepted |
| `normalize-store-case` | uppercase S accepted |
| `allow-negative-generation` | `-1` accepted |
| `allow-unsupported-schema` | `stateSchema` 3 accepted |
| `skip-canonical-byte-equality` | trailing newline not `NonCanonical` |
| baseline | 5 `selection::` |

---

## Findings

354 implements the advisory’s **codec** and does **not** implement the native join (host fence, single-leaf capture, marker/full, profile). Missing pair is not in this API at all (bytes-in only).

**Actionable defects in this freeze:** none that make cap / closed members / identifier grammar / integer domains / canonical raw equality self-contradictory with the 5+20 tests and 7 compiled controls.

**Must not be counted closed:** native File/root/fence/FS; marker/full `(S,G,K)` / core-closure bind; active-slot; `--trust-group`; selected I/S/core; current authority; writers; M2–M6. Advisory native-join remaining is **unchanged**.

---

## Remaining (do not count closed)

Host-owned native composition from the selection-boundary advisory. Marker/full store, 323/229 closure, 350 profile FS qualification, 352 fence, create/init, writers.

---

## Verdicts

- [x] **354 as frozen private lifecycle selection codec:** archive verified against parent 353; five lifecycle/lock deltas only; identity path dep allowed by inventory v32; no security/storage reverse edge; no filesystem read; live 5+20; Clippy/fmt30; 7 compiled controls frozen-r1-equal; r1 TEST compile **not** a production pass. Matches advisory codec layer.
- [ ] **Not** native selection join, selected-I/current authority, writers, or product installation.
