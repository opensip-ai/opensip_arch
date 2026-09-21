# Independent review — native exact directory-name observations 339

**Standing:** bounded native-**platform + security** review of frozen `native-directory-names-checkpoint-339`. macOS `fgetattrlist` on the **retained child descriptor** samples `ATTR_CMN_NAME` and compares **exact raw bytes** to the saved component. `RetainedChildDirectory::recheck_exact_name` brackets that sample with 332 relative inode checks. Security 333 `inspect` uses it **pre- and post-observation**, so same-inode **case aliases refuse**. 331/332 opening and relative-inode `recheck` are unchanged. This is **not** ancestor admission, a held fence, lifetime-root enumeration, case-sensitive-only policy, qualified census, or current authority. Installed product remains `fa72e50`. 338 and 337 REVIEW were read and are **unchanged**.

337’s in-scope **case-alias** gap is what this addresses, without requiring a case-sensitive-only volume or a hostile-kernel/raw-slot theorem. Parent names, file aliases, fence, and release profile remain owed (340 named, not done).

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. Initial security-r1=294 / platform-r1=70 with the new security test **misplaced** on the Linux stub; moved to macOS + fifth platform test; **no production correction**. **Final:** platform 71 / security 295+2 ignored; workspace-r2 615; Clippy-r1; fmt23. Linux observer unsupported, not run.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6872732 B, 552 members, SHA256 `5d695d0f4f9d9cbb8a1e5ac659c5cbb6329c10b1434de75504acf7229aaaa8f1`**. Extract 552/552. Parent 338 live tar SHA `1970c46c…fbdc` (6833460 / 587 / 487). 338 REVIEW `666c97ec…954d` and 337 REVIEW `3d58a154…c97e` unchanged.

Product vs 338: **484** unchanged, **3** changed (`filesystem.rs` `mod directory_names`; `directory_binding.rs` `recheck_exact_name`; `directory_policy.rs` pre/post `recheck_exact_name()`), **1** added (`directory_names.rs` SHA256 `df9bf8b7…2696` 8772 B). 338 `directory_provers.rs` remains `d1561f2a…dead`. libc `=0.2.189`.

`native-api-source-pins.json` independently rehashed equal: SDK `getattrlist.2` `866c79ab…e34b`, `attr.h` `5118b924…eefe`, cached `libc-0.2.189` apple `mod.rs` `30b07c66…47de`. Historical web `getattrlist` is **not** installed-TCB qualification. `fgetattrlist` declaration: `fd, *mut c_void attrList, *mut c_void buf, size_t, u32 options`; `FSOPT_REPORT_FULLSIZE = 0x4`; `ATTR_CMN_NAME = 1`.

---

## FFI, bounds, name vs inode

macOS `matches`: `attrlist` requests **only** `ATTR_CMN_RETURNED_ATTRS | ATTR_CMN_NAME`, `FSOPT_REPORT_FULLSIZE`, **1056-byte** zeroed stack buffer (32-byte header + 1024 name+NUL). `unsafe fgetattrlist` on the **owned fd**; kernel error → `last_os_error`. Decoder uses **native-endian `u32`/`i32` copies**, not an alignment-dependent struct:

- `total` in `32..=buffer.len()` (truncation / REPORT_FULLSIZE overflow refuse)
- common has NAME, no extra common bits, vol/dir/file/fork words **zero**
- `attrreference` offset `>= 8`, `% 4 == 0`; `start = 24 + offset` checked
- length `2..=1024`; `end` checked against `total`
- terminal NUL, no embedded NUL, no `/`

Exact `== expected.as_bytes()` — **no** fold/normalization. Non-macOS: `Unsupported`.

`recheck_exact_name`: 332 `recheck` → native name match on **child** fd → `recheck` again. Equal leaf under another parent still fails inode binding. Case-only rename: inode `recheck` may still pass; exact name fails. Alias `openat("canonical")` of `"Canonical"`: `recheck` true, `recheck_exact_name` false (or `NotFound` on case-sensitive volumes — **not** dual-profile qualification).

333 `inspect` both name checks are `recheck_exact_name`. Alias cannot pass precheck; case-only rename during postcheck is `NameChanged`. Same-inode **chmod** still not prevented by name recheck (historical samples). 331 `open_child_directory` unchanged.

No private `__getdirentries64`, no `scandir`, no lifetime collection walk.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform -p opensip-security` then targeted crates (request: full 615 acceptable as frozen workspace-r2; targeted allowed):

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **71 passed / 0 failed / 0 ignored**; `Compiling opensip-platform`; 5 new `directory_names_*` ok |
| `cargo test --offline --locked -p opensip-security` | **295 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; `directory_policy_native_case_*` ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **23** security includes + `directory_names.rs` | exit 0 |

Mutant **baseline `--workspace`** also passed (includes 71 platform + remaining workspace crates; frozen workspace-r2 is the 615-count record).

---

## Mutants

Ten compiled controls + workspace baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`90c44afe…3c91`**, **byte-identical** to frozen r1. All **11** compiled.

| Control | First failure |
|---|---|
| `native-always-matches` | alias/`case-only` still “exact” |
| `casefold-name-comparison` | ASCII fold accepts alias |
| `ignore-returned-name-bit` | omitted NAME bit accepted |
| `accept-unterminated-name` | missing NUL accepted |
| `accept-embedded-nul` | `a\0b` accepted |
| `accept-slash` | `a/b` accepted |
| `skip-native-name-check` | case-only rename still exact |
| `name-without-inode-binding` | decoy/symlink without 332 recheck |
| `old-policy-precheck` | alias passed precheck panic |
| `old-policy-postcheck` | case rename after sample `Ok` |
| baseline | workspace pass |

---

## Findings

The decoder and `recheck_exact_name` close 337’s **case-alias** hole for **this** retained child without folding names or scanning the collection. They do not freeze names, exclude writers, or admit ancestors. Case-sensitive `NotFound` vs case-insensitive alias is a **conditional** test branch, not dual-class qualification.

**Actionable defects in this freeze:** none that make `matches` / `recheck_exact_name` / 333 pre/post self-contradictory with those bounds on the macOS 71+295 tests and ten controls.

**Must not be counted closed:** parent/higher names; file locator aliases; fence/profile; 340 full retained paths; current producer; Linux; M2–M6.

---

## Remaining (do not count closed)

340 captured-file / full-path name checks (named, not done); 337 planted-name/fence/FS qualification; selected installation; original T/TCB; writers; M2–M6.

---

## Verdicts

- [x] **339 as frozen private exact-name sample:** archive verified; 337/338 preserved; bounded `fgetattrlist` NAME decode; exact bytes vs saved component; 332 inode still required; 333 both checks refuse aliases; live 71 platform / 295 security; Clippy/fmt; 10 compiled controls + workspace baseline frozen-r1-equal.
- [ ] **Not** fence, ancestor admission, case-sensitive-only policy, qualified census, current authority, or product installation.
