# Independent review — native OS-account installation root 351

**Standing:** bounded native-**custody** review of frozen `native-installation-root-checkpoint-351`. Production `NativeInstallationRoot::capture` takes **only supplied trust-group policy**. It derives the fixed macOS operational I from the actual account-database home after **real==effective** UID equality; HOME/XDG/PATH/argv/UID/project cannot select the root. Existing vs missing are distinct observations. Missing is **not** creation. Groups remain **SUPPLIED**; OS membership is not an invocation grant. Host orchestration and fence join are **352**, not this freeze. This is **not** selected S/core/profile-root provenance, current authority, writers, or product install. Product remains `fa72e50`. Prior 350 REVIEW `a2815d6b…d084` (12356 B) and filesystem advisory `3b2f3c67…934d` were read and are **unchanged**. Unfrozen 352 bytes were **not** reviewed.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; frozen mutant dir not overwritten. **This review reproduced:** `installation_root_` **9**, Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **30** security includes, **11** compiled controls + nine-test baseline. Full security **353** and prior 350 controls **not rerun** (request). Frozen author record: security-r3 353/0/2.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, 581 members, and extract: 0 mismatches.

Frozen archive: **6915620 B, 581 members, SHA256 `4cad22ee2c008ca246985057f6ed32f0bec49eff1f5216b3057fccac4356a581`**. Parent 350 tar SHA `216b29ee…4729` (6955400 / 721 / 500).

Product vs 350: **499** unchanged, **1** changed, **1** added, 0 removed:

| Path | SHA256 / bytes |
|---|---|
| `security/src/custody.rs` | `fb4d3d48…6880` / 39044 |
| `security/src/custody/installation_root.rs` **added** | `03be1bff…6f10` / 21471 |

`custody.rs` only adds `#[cfg(target_os = "macos")] pub(crate) mod installation_root`. 126 security fixtures + 2 dyld CD fixtures unchanged (128). No dependency or platform crate change. Linux layout is **not** implemented by this macOS module.

---

## Source / account sequencing

`observe_account` looks up **real** UID via `getpwuid_r` (no HOME/USER/SUDO_UID). Host-foundation v2 §1 asks for **effective**-UID home. 351 inserts `real == effective` **before** using that home, so mixed credentials cannot treat the real-UID home as the effective account. No UID-0 prohibition and no elevated-execution endorsement. Recheck compares **raw `OsStr`** home bytes (`/Users/person` ≠ `/Users//person`; Path normalization is not used).

Public-within-crate factory: `capture(&BTreeSet<u32>)` → `capture_observing(..., native_account)`. Private `capture_observing` / `recheck_observing` exist only so tests can inject **explicitly SYNTHETIC** account keys; fixture Files/paths/ACLs stay real OS. Production consumption (`recheck`, `observation`) always resamples `observe_account`.

Successful capture samples account **four** times: before FS, after FS, then recheck before and after path work. Failed FS capture still samples after the failed open (2). Failed later recheck still samples after custody error (2). `NativeInstallationRoot` does not `Debug` home or UIDs.

Isolated child (`HOME`/`XDG_STATE_HOME`/`USER`/`SUDO_UID` spoof, no process-global mutation) asserts the literal suffix `Library/Application Support/OpenSIP/preview-v1`, that account home ≠ spoofed `HOME`, and that any successful existing leaf matches native `(dev,ino)`. Unsafe/absent real I may refuse (`Custody`/`Native`); that is not relabeled as accepted absence. Fixture trees never create the user's operational I.

---

## Absence / custody

Fixed four macOS components. Each next `RetainedDirectoryPath::open` is a nofollow `openat` walk of the reconstructed absolute path (340 exact names, 256 **engineering** child-component cap including the four suffix parts — not S3 discovery depth). Prefix `inspect_directory_path` runs **before and after** even a failed open. **Only** `NotFound` under an unchanged admitted parent is `Missing`; file/symlink/dangling/mode/case-alias/unsafe ancestor are errors, never absence. Missing retains last existing prefix + remaining fixed suffix. Later appearance is `Appeared`. Existing replacement/mode/case/ancestor change refuses. Home itself must exist and pass custody; missing home is not a `MissingRoot`. No mkdir/chmod/fence/init/repair.

S3 replaced nearest-ancestor **project** discovery, not host-foundation §1 operational I. 351 does not walk `opensip.json` and does not override I.

---

## Failure history (must not be hidden)

| Run | Result | Notes |
|---|---|---|
| native-r1 / security-r1 | **8** focused; **352**/2 ignored | before ninth sequencing test |
| Clippy-r1 | **TEST** `needless_range_loop` | production unchanged; loop became `enumerate` |
| security-r2 | **352 pass / 1 fail / 2 ignored** | inherited 350 `native_profile_census_same_fence_...` `ChangedDuringRead` on ancestor ACL/metadata after step0/1; concurrent root fixtures + Grok 350; **not** a 351 production retry/weakening; logs kept |
| native-r2 / Clippy-r2 / security-r3 | **9** focused; Clippy; **353**/0/2 | final source; this review did not rerun 353 |

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `cargo test -p opensip-security installation_root_` | **9 passed** |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **30** includes | exit 0 |
| Full 353 / 350 controls | **not rerun** |

---

## Mutants

Eleven compiled controls + nine-test baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 **not** overwritten). Live `report.json` SHA256 **`c7c223b87b788260c969f66adbe6e7ceb20d0febc0fca906c04871ec9dcbd9ca`**, **byte-identical** to frozen **r1**. All **12** compiled.

| Control | First failure |
|---|---|
| `mixed-credentials` | real≠effective accepted |
| `normalized-home-equality` | `/Users//person` matches `/Users/person` |
| `environment-home` | spoofed `HOME` becomes account home |
| `wrong-fixed-suffix` | suffix `preview-v2` vs required `preview-v1` |
| `collapse-open-errors` | file/symlink/alias captured as missing |
| `accept-appeared-child` | created next component still `Ok` |
| `skip-existing-recheck` | replace/mode/case/ancestor accepted |
| `skip-all-later-path-checks` | missing recheck ignores wrong-kind/prefix change |
| `skip-post-capture-account` | post-FS account sample dropped |
| `skip-before-after-consumption-account` | consumption account brackets dropped |
| `skip-constructor-final-recheck` | constructor skips final account/path recheck |
| baseline | 9 `installation_root_` |

---

## Findings

351 is a **read-only** private macOS observation of host-foundation §1 operational I from OS-account home, with real==effective before home use, raw home equality, NotFound-only missing, and account snapshots around FS work including errors. It does not create I, admit groups, or join 350/341 fence.

**Reproduction:** live 9 tests include per-depth missing without creation, existing identity + later replacement, wrong-kind≠absence, parent/child inspect on failed/successful open, mixed UID and `//` home refuse, isolated-child environment ignore, and 4/2/2 account-sample counts.

**Actionable defects in this freeze:** none that make `capture` / `Missing` vs `Existing` / `Appeared` / credential/home equality / account bracketing self-contradictory with those 9 tests and 11 compiled controls.

**Must not be counted closed:** selected S/core/profile-root; `--trust-group` admission; privilege policy; 352 fence/host join; current authority; original T/action; durability; writers; Linux I; M2–M6. Sequential samples are not an atomic snapshot or ABA proof. `supplied_actor()` returns stored UID/groups without resampling (consumption goes through `recheck`/`observation`).

---

## Remaining (do not count closed)

352 host orchestration and fence join (unfrozen, not reviewed here). Admitted invocation/group provenance, selected S/core/profile, release qualification, original T, writers, current authority, Linux native custody, M3–M6.

---

## Verdicts

- [x] **351 as frozen private native account-root observation:** archive verified; 499 product pins unchanged vs 350; two security deltas only; groups-only factory; real==effective before home; raw OsStr home recheck; NotFound-only missing; account brackets even FS error; live 9; Clippy/fmt30; 11 compiled controls frozen-r1-equal; Clippy-r1 TEST loop / security-r2 concurrent `ChangedDuringRead` **not** counted as production passes.
- [ ] **Not** selected-S/current authority, 352 fence join, writers, or product installation.
