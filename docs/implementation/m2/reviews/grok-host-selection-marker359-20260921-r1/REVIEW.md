# Independent review — host selection/marker bundle 359

**Standing:** bounded **host composition** review of frozen `host-selection-marker-checkpoint-359`. `ProvisionalInstallationRecords` privately owns an actual 356 `ProvisionalSelection` and 358 `ProvisionalStoreMarker` that both borrow **one** opaque `InstallationReadFence`. Requested marker S is taken from retained selection syntax; storage compares an independently captured marker. This is **not** full `(S,G,K)`, `StoreGenerationBindingV1`, namespace/handle/registry, selected I, core/profile, active-slot, or current authority. Product remains `fa72e50`. Prior 358 REVIEW `cdbad99c…c2d3` (7380 B, no ADDENDUM), 357 `c36e96cf…a710`, 356 `d620c9af…e74d`, store-binding advisory `cf1903f4…17ff` and ADDENDUM `84da081d…9a8b` were read and are **unchanged**. Distinct from 360 (separately labelled synthetic-home harness; **not** this freeze and **not** approved here).

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir **not** overwritten. **This review reproduced:** `installation_records::` **2**, crate `opensip-host` **68** (actually run), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **2** compiled sequencing controls + two-test baseline. Security **375**, storage **96**, and lifecycle **20** **not rerun**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 358 archive **545 / 6874352 B / `296b07c1…81cb`** / 505 product pins rehashed before 359 extract. Independent rehash of 359 tar, 549 members, and extract: 0 mismatches.

Frozen archive: **6870648 B, 549 members, SHA256 `387a488115c4f6095c34cc3bd449cbacd5fbd3ec648a9f3ec4bf4af9a23b6cf2`**. 506 product pins.

Product vs 358: **502** unchanged, **3** changed, **1** added (host + lock only):

| Path | SHA256 / bytes |
|---|---|
| `Cargo.lock` | `426c89e6…b2d2` / 12954 (was `fb42b30e…fba3` / 12934) |
| `crates/host/Cargo.toml` | `c5108dec…fa34` / 550 (was `46ee3eea…71f3` / 507) |
| `crates/host/src/lib.rs` | `022e77c5…a8f7` / 481 (was `bcf2fe7e…8d1d` / 422) |
| `crates/host/src/installation_records.rs` **added** | `74ec64c9…5071` / 4337 |

`lib.rs` only adds `#[cfg(target_os = "macos")] pub mod installation_records`. Cargo.lock: **61** packages, ordered name/version identical to 358; the **only** body diff is `opensip-host` gaining path dep `opensip-storage` (inventory v32 SHA `105a260d…b72e` already listed that host edge). **No** external crate/feature. **No** security, storage, or lifecycle source deltas (`installation_observation.rs`, `native_marker.rs`, `selection.rs`, 356 `installation_selection.rs` byte-identical to 358). 126 security fixtures unchanged.

---

## Same fence / ownership / postcheck

The only constructor is `read_existing(fence: &'fence InstallationReadFence)`. Fields `selection` and `marker` are private and share `'fence`. There is **no** constructor that accepts independently supplied captures, a second fence, a path, or raw bytes.

`ProvisionalSelection::read_existing(fence)` then `observe_then_recheck`: read marker with `record.store_instance()` from the **retained** decoded pair, then **always** `selection.recheck()` including when the marker attempt fails. The completed bundle `recheck()` is selection, then marker, then selection again. Getters (`selection`, `marker_raw`, `contributing_filesystems`) recheck before exposing syntax/raw/samples. Combined samples are marker I/fence/all relative pairs/File **plus** the selection File (selection sits at I; no extra below-I pairs). Copies are observations, not custody, profile admission, or atomic proof.

Private `observe_then_recheck`: run observe, then recheck, then return observe **only if** recheck succeeded. Failed final custody never returns a partial bundle. Tests use **synthetic** callbacks only; they are not a live same-fence `read_existing` fixture. Native File/prefix/lifetime remain 357; marker codec remains 358.

Decoded G/K on the pair remain **claims** despite marker S equality. This freeze does **not** compare 344 `C.store` or construct `StoreGenerationBindingV1`. The store-binding ADDENDUM still applies: three-member current comparison is only a necessary provisional check, not a replacement for admitted namespace/handle/registry.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `installation_records::` | **2 passed** |
| `cargo test -p opensip-host` | **68 passed** (actually run) |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Security 375 / storage 96 / lifecycle 20 | **not rerun** |

---

## Mutants

Two compiled sequencing controls + two-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`1fa403432aece74ed952bdf3915479e262ef3e7c54a293d156a0900f26a495af`**, **byte-identical** to frozen **r1**. All **3** compiled.

| Control | First failure |
|---|---|
| `skip-postcheck-on-second-owner-error` | failed marker observe skips selection recheck (`calls == ["observe"]`) |
| `ignore-failed-postcheck` | successful observe returned despite failed custody |
| baseline | 2 `installation_records::` |

---

## Findings

359 is the host-owned **same-fence join** of 356 pair + 358 S-only marker. Same-fence is enforced by constructor signature, field privacy, and shared `'fence` — not by a live native fixture in these two tests.

**Actionable defects in this freeze:** none that make “one fence only,” “selection recheck after failed marker,” “final custody wins over partial observe,” or “G/K remain claims” self-contradictory with the 2 tests, 68 host tests, and 2 compiled controls.

**Coverage, not a freeze contradiction:** no live `read_existing` against a native fence. 360’s planned synthetic-home cross-crate harness is **out of scope** and is not an approval of this freeze or of full binding.

**Must not be counted closed:** full `(S,G,K)` / `StoreGenerationBindingV1`; admitted namespace/handle/registry; 344 `expected_store` as authority; core/profile allowlist; active-slot; `--trust-group`; 5s scheduler; create/init; current authority; writers; M2–M6. Do **not** infer full store admission from marker S equality with the pair.

---

## Remaining (do not count closed)

Independent security current `StoreBinding` as **provisional comparison only** (358 ADDENDUM). 323/229 closure, 350 profile FS-name law on the **same** held Files, active-slot, invocation groups, writers. 360 if requested later is a labelled harness, not this report.

---

## Verdicts

- [x] **359 as frozen private host selection/marker bundle:** archive verified against parent 358; host+lock only; host→storage already in inventory v32; one fence; S from retained selection vs independent marker; G/K remain claims; live 2+68; Clippy/fmt30; 2 compiled controls frozen-r1-equal. Matches the join request, not full binding or selected-I.
- [ ] **Not** full `(S,G,K)`, `StoreGenerationBindingV1`, selected-I/current authority, 360 harness approval, writers, or product installation.
