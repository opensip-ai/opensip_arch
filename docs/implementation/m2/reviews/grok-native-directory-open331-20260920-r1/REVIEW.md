# Independent review — native child-directory open 331

**Standing:** bounded native-**platform** FFI review of frozen `native-directory-open-checkpoint-331`. `RetainedDirectory::open_child_directory(&OsStr)` opens **one** existing child directory under an already-retained parent fd. It is **not** a qualified trust store, current capsule, complete successor census, custody/exclusion, or authorized absence. Installed product remains `fa72e50`. 330 REVIEW+ADDENDUM were read and are **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. **Final is platform-r1 / 61 / mutation-r1** (no 331 compile-fail).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6798428 B, 534 members, SHA256 `c11efa51bdf1f62c8abf73fae13c9aa51811cea3e8308fa5b5f710952ff21375`**, `allMembersRehashed: true`, **481** product pins. Extract rehashed **534/534**. Parent 330 live tar SHA `70565367…2c75` (6808096 / 550 / 480). 330 REVIEW `75b9b10e…468e` and ADDENDUM `7b783d22…62ff` unchanged.

Product vs 330: **479** unchanged, **1** changed (`filesystem.rs` adds private `mod directory_open;` — **no** new type export), **1** added (`filesystem/directory_open.rs` SHA256 `9c8eedaf…fcb2` 9575 B). 330 `directory_entries.rs` remains `4e599caf…7915`. `lib.rs` **byte-identical** to 330. `open_child_directory` has **no** security-crate caller. libc remains `=0.2.189`.

---

## FFI (source)

`component` runs **before** `CString` / `openat`: nonempty, ≤1023 raw bytes, not `.`/`..`, no `/` `\` NUL, no `.opensip-stage-` prefix. Same family as `path_binding` component policy, plus an explicit allocation cap. Raw `OsStr` bytes are kept; `from_utf8_lossy` is not used. Kernel `NAME_MAX` may be smaller; that refusal is a native error, not a bypass.

`openat(parent_fd, child, O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK)` — exact retained parent, one component, no `AT_FDCWD`, no create flags, no symlink fallback, no retry. Successful fd becomes `File`; `from_retained_handle` still requires directory metadata. Failed `openat` returns `last_os_error()`; it does **not** clone the parent. Mutant `failed-open-falls-back-to-parent` is caught (`absent` would otherwise `Ok(parent)`).

`NotFound` is an **observation**, not fenced absence. Directory symlink, dangling symlink, regular file, and FIFO refuse with a kind **other than** `NotFound`. Traversal / `.` / staging names are `InvalidInput` **before** the syscall. `O_DIRECTORY`/`O_NONBLOCK` stay even where a later metadata check would refuse; opening an unexpected device can have effects before that check (same existing filesystem primitive bound).

Returned `RetainedDirectory` is an owned fd (`File` is `Send`). After parent and child names are replaced, the handle still names the original inode (330 `visit_entry_names` sees `old` not `decoy`/`replacement`; `open_regular("old")` reads `retained`). That is **not** proof the selected parent/name path still names it, and not ownership/ACL/mount/exclusion/durability.

Linux-only native non-UTF8 directory create/open is `cfg(target_os = "linux")` and was **not executed**. The macOS unit test still checks that `component` preserves `[0xff, 0xfe, b'a']`.

---

## Inherited 330 boundaries

330 visitor source is unchanged. 331 tests **use** `visit_entry_names` after a child open; a completed 330 `Summary` is still **only** OS-stream counts. Apple whiteout/zero-inode skips and null-without-errno-as-EOF, union-flag-only testing, POSIX concurrent-mutation unspecified visibility, uncharged libc prefetch, and missing selected-FS/kernel/libc qualification **remain**. 330 ADDENDUM: `NonNull<DIR>` is `!Send`/`!Sync`; that does not apply to this owned `File` handle.

Neither a 331 child handle nor a 330 EOF may be promoted to census, custody, or current authority.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **61 passed / 0 failed / 0 ignored**; `Compiling opensip-platform`; 0.20s; 4 new `child_directory_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **18** unchanged security includes + 330 visitor + `directory_open.rs` | exit 0 |

---

## Mutants

Nine compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`b6c7df99…ce10`**, **byte-identical** to frozen r1. All **10** compiled.

| Control | First failure |
|---|---|
| `unbounded-component-copy` | 1024-byte name `Ok` |
| `allow-dot-parent` | `.` `Ok` |
| `allow-path-traversal` | `/` `Ok` |
| `allow-reserved-staging` | missing `.opensip-stage-*` becomes `NotFound` |
| `lossy-os-name` | `[0xff,0xfe,a]` → U+FFFD bytes |
| `follow-directory-symlink` | `link` opens as directory |
| `inherit-directory-handle` | `FD_CLOEXEC` bit 0 |
| `reselect-working-directory` | `AT_FDCWD` `NotFound` |
| `failed-open-falls-back-to-parent` | `absent` returns `Ok` |
| baseline | 61 passed |

---

## Findings

The opener is a handle-relative, single-component, no-follow directory capability consistent with existing `path_binding::child` flags, with an explicit 1023-byte copy cap and no parent fallback. It does not admit the child, re-check parent/name attachment, or close 330’s stream holes.

**Actionable defects in this freeze:** none that make `open_child_directory` self-contradictory with its stated component/`openat` contract on the macOS 61 tests and 9 controls.

**Must not be counted closed:** 330 library-scope limits; physical census; custody/fence; canonical 64-cap / shared Budget; ACL/mount observations; ABA-proof parent/name recheck; Linux native non-UTF8 dir open; writers; M2–M6.

---

## Remaining (do not count closed)

Exact-child metadata/ACL; enduring native exclusion; selected FS/libc qualification; directory/entry accounting before materialization; 64-canonical bucket cap and following buckets; 329 successor composition; original T/TCB/history; M2–M6.

---

## Verdicts

- [x] **331 as frozen private child-directory opener:** archive verified; 330 REVIEW+ADDENDUM preserved; visitor unchanged; component bounds before syscall; exact parent `openat` no-follow/CLOEXEC; `NotFound` not absence; wrong kinds not masquerading as missing; live 61/0 ignored; Clippy/fmt; 9 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** qualified custody, census, native current, authorized absence, or product installation.
