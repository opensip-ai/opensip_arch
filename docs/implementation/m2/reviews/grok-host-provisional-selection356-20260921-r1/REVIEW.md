# Independent review — host provisional selection 356

**Standing:** bounded **host composition** review of frozen `host-provisional-selection-checkpoint-356`. Host `ProvisionalSelection` borrows an opaque 355 `InstallationReadFence`, captures lifecycle’s **fixed** `selection.pair` / 4096, decodes 354 syntax from the **original captured bytes**, and rechecks that capture **even when decode fails**. This is **not** selected I, marker/full `(S,G,K)`, core/profile, active-slot, current authority, or product install. Product remains `fa72e50`. Prior 355 REVIEW `84afca9a…286d`, 354 `01b3bbcf…06c3`, and selection-boundary advisory `a5947b69…8ba3` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir not overwritten. **This review reproduced:** host `installation_selection::` **2**, lifecycle **20**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **2** compiled sequencing controls + two-test baseline. Frozen author host-r1 **66** and security **370** **not rerun**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 355 archive **572 / 6902664 B / `8d762adb…f5c6`** rehashed before 356 extract. Independent rehash of 356 tar, 552 members, and extract: 0 mismatches.

Frozen archive: **6882012 B, 552 members, SHA256 `c8928f9828f19e8cb52975e2bb0fa6203a63db25677a4e3b4fe866cbfb59e0eb`**.

Product vs 355: **498** unchanged, **5** changed, **1** added:

| Path | SHA256 / bytes |
|---|---|
| `Cargo.lock` | `fb42b30e…fba3` / 12934 |
| `crates/host/Cargo.toml` | `46ee3eea…71f3` / 507 |
| `crates/host/src/lib.rs` | `bcf2fe7e…d1d` / 422 |
| `crates/lifecycle/src/lib.rs` | `3f86593d…50a6` / 441 |
| `crates/lifecycle/src/selection.rs` | `25725d9c…dece` / 10601 |
| `crates/host/src/installation_selection.rs` **added** | `8d7f6c3d…d5dc` / 4419 |

**Zero** security source deltas (`installation_observation.rs` byte-identical to 355). 126 security fixtures unchanged. Cargo.lock: 61 packages, ordered name/version identical; the **only** body diff is `opensip-host` gaining path deps `opensip-lifecycle` and `opensip-security` (inventory v32 SHA `105a260d…b72e` already listed those host edges). **No** lifecycle→security, **no** security→storage, **no** external crate/feature. Lifecycle Cargo.toml still identity+platform only. 354 decode algorithm unchanged except `pub` + `LEAF`/`CAP` constants; `Selection` fields and `StoreComponent` stay private.

---

## Ownership / retention / postcheck

`ProvisionalSelection<'fence>` privately holds `ProvisionalHeldFile<'fence>` and `DecodedSelectionV1`. `read_existing` takes **only** `&InstallationReadFence`; leaf/cap are `SELECTION_PAIR_LEAF` / `SELECTION_PAIR_CAP`. No caller path, bytes, UID, root, or `File` injection/escape. `record()` / `filesystem()` recheck the original capture first. Missing/malformed remains unavailable (355 missing is an error; 354 empty/invalid is decode error).

Private `decode_then_recheck`: always run the observation callback **after** `decode`, then return decode error only if that check succeeded. Production passes `|| capture.recheck()`. Tests use **synthetic** callbacks only; they are not native I/fence proof (355 remains that evidence).

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `cargo test -p opensip-host installation_selection::` | **2 passed** |
| `cargo test -p opensip-lifecycle` | **20 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Host 66 / security 370 | **not rerun** (frozen author 66/370) |

---

## Mutants

Two compiled controls + two-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`f69d91127e46239616601871b9c0ba80ec55f975dcf0aa7b045acdea67d2b1d0`**, **byte-identical** to frozen **r1**. All **3** compiled.

| Control | First failure |
|---|---|
| `skip-postcheck-on-decode-error` | invalid/oversize skips recheck (`calls != 1`) |
| `ignore-failed-postcheck` | decode error wins over observation failure |
| baseline | 2 `installation_selection::` |

---

## Findings

356 is the advisory’s **host-owned join of 355 capture + 354 decode**, still **provisional**. It does not bind marker/full `(S,G,K)`, core/profile, or promote to selected installation.

**Actionable defects in this freeze:** none that make fixed owner constants, fence-borrow lifetime, decode-then-recheck order, or “observation wins after decode failure” self-contradictory with the 2 tests, 20 lifecycle tests, and 2 compiled controls.

**Coverage, not a freeze contradiction:** 356 does not call `read_existing` against a live native fence; native File/lifetime tests remain 355. Public `DecodedSelectionV1::decode` is still **syntax-only** and can be invoked without a fence.

**Must not be counted closed:** storage marker/full; 357 prefix capture; core/profile qualification of this File; `--trust-group`; 5s scheduler; create/init; current authority; writers; M2–M6. Commit355 whitespace note in this subject is a **recorded precommit-guard miss** on four advisory hard-breaks, not a 356 production defect and not a rewrite of frozen 355/advisory bytes.

---

## Remaining (do not count closed)

357 planned bounded native prefix capture for storage-owned **marker** under the **same** fence (marker S, not full G/K). Marker/full store bind, 323/229 closure, 350 profile FS-name law, active-slot.

---

## Verdicts

- [x] **356 as frozen private host provisional selection:** archive verified against parent 355; six host/lifecycle/lock deltas; security 355 bytes unchanged; host→lifecycle/security only; `ProvisionalSelection` borrows 355 fence, uses fixed `selection.pair`/4096, keeps original capture, postchecks even on decode error; live 2+20; Clippy/fmt30; 2 compiled controls frozen-r1-equal. Matches advisory host join, not full selection authority.
- [ ] **Not** selected-I/current authority, marker/core/profile join, writers, or product installation.
