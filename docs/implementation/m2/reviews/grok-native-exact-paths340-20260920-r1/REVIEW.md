# Independent review — native exact ancestor and file-name checks 340

**Standing:** bounded native-**platform + security** review of frozen `native-exact-paths-checkpoint-340`. Public `descriptor_name_matches` is a thin 339 wrapper on a `File`. `RetainedDirectoryPath::recheck_exact_names` requires the **full relative inode chain**, then **every non-root** edge’s native name vs saved component, then the inode chain again. Operational full-path policy uses that method **pre- and post-observation**. 335 `check_name` also matches the **original File** native name to the lowercase canonical leaf, alongside existing regular/single-link/dev/ino/fresh-leaf checks, at both pre- and post-read. Samples are **not** a fence, profile, current authority, or typed-dependent custody. Installed product remains `fa72e50`. 339 and 338 REVIEW were read and are **unchanged**.

337 TCB narrowing stands: cooperative fence / selected root / FS profile still owed; no hostile-kernel theorem. 341 lock carrier is **not** in this freeze.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **Final:** security-r1 **299 / 2 ignored**, platform-r1 **73**, Clippy-r1, fmt23. No setup/production failure. No new `unsafe`, module, or dependency. 339 FFI/decoder **byte-identical**. Linux not run.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6832428 B, 537 members, SHA256 `263fcd08de31fff3400bb3b4769178951b14d661a86da6fb1d93ae38005aa2ec`**. Extract 537/537. Parent 339 live tar SHA `5d695d0f…a8f1` (6872732 / 552 / 488). 339 REVIEW `a978f744…8ac8` and 338 REVIEW `666c97ec…954d` unchanged.

Product vs 339: **483** unchanged, **5** changed (`filesystem.rs` public wrapper; `lib.rs` re-export; `path_binding.rs` `recheck_exact_names`; `custody.rs` path-policy pre/post; `directory_record_capture.rs` `check_name`). `directory_names.rs` remains `df9bf8b7…2696`. libc `=0.2.189`.

---

## Whole path vs basename, inode, foreign names

`descriptor_name_matches`: sampled name **only** — no kind, parent, or inode. Root has **no** child component; zero-edge paths do **no** name query.

`recheck_exact_names`: `recheck()` (full chain) → `matches` on **each** `edges[]` descriptor vs saved bytes → `recheck()`. Skipping all names or **only the leaf** fails ancestor case-change. Dropping inode bracketing fails equal-basename relocation (name still `"child"`, inode does not). ABA restored spelling is observed as matching again — **not** claimed impossible.

`inspect_directory_path`: both name checks are `recheck_exact_names`. Alias can pass old `recheck()` precheck; post-observation case change is `NameChanged`.

335 `check_name`: reopen leaf for type/nlink/dev/ino **and** `descriptor_name_matches(original_file, leaf)`. Case-rename of the retained file after scan latches. Foreign **uppercase** names still 222: charged/reported/unread/untouched; they do **not** by themselves make the census unavailable. Path open/`recheck` unchanged. Typed dependents still need their own exact-name producers.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform -p opensip-security` (targeted; 339 workspace 615 not repeated):

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **73 passed / 0 failed / 0 ignored**; 2 new `exact_path_names_*` ok |
| `cargo test --offline --locked -p opensip-security` | **299 passed / 0 failed / 2 ignored**; path-policy + 3 capture name tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **23** security includes + `directory_names.rs` + `path_binding.rs` | exit 0 |

Case-sensitive volumes may `NotFound` on alias; this APFS run exercises same-inode alias. Not dual-profile qualification.

---

## Mutants

Six compiled controls + platform/security baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`bb5f07f7…87b8`**, **byte-identical** to frozen r1. All **7** compiled.

| Control | First failure |
|---|---|
| `skip-all-exact-names` | ancestor case change still “exact” |
| `only-leaf-exact-name` | ancestor case change still “exact” |
| `names-without-path-inodes` | relocated equal basename accepted |
| `old-path-policy-precheck` | alias passed precheck panic |
| `old-path-policy-postcheck` | case change after sample `Ok` |
| `skip-file-exact-name` | original-file case rename accepted |
| baseline | 73 platform + 299 security |

---

## Findings

340 extends 339 from one child edge to **every non-root path component** and to the **captured File** spelling, without changing the decoder or 331/332 open contracts. Whole-path ≠ leaf-only. Inode binding remains mandatory. Foreign uppercase remains 222. Samples are not a lock (341 is separate).

**Actionable defects in this freeze:** none that make `recheck_exact_names` / path-policy / 335 `check_name` self-contradictory with those bounds on the macOS 73+299 tests and six controls.

**Must not be counted closed:** fence; selected root/current; FS/case profile; typed dependent locators; 341 lock; census/authority; Linux; M2–M6.

---

## Remaining (do not count closed)

341 held lock under a **supplied** retained path (named, not in 340); 337 planted-name/profile qualification; writers; original T/TCB; M2–M6.

---

## Verdicts

- [x] **340 as frozen private exact path/file-name samples:** archive verified; 339 decoder unchanged; every non-root component + original File spelling; inode still required; 222 foreign uppercase; live 73/299; Clippy/fmt; 6 compiled controls + baseline frozen-r1-equal; 339/338 reports preserved.
- [ ] **Not** fence, profile, qualified census, current authority, 341 lock, or product installation.
