# Independent review — native directory visit 330

**Standing:** bounded native-**platform** FFI review of frozen `native-directory-visit-checkpoint-330`. `RetainedDirectory::visit_entry_names` streams **OS-returned** names under an already-retained directory handle. It is **not** a security JSON owner, successor census, custody, native current, canonical 64-cap, or durable authority. Installed product remains `fa72e50`. 329 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. platform-r1 compile-fail and r2/r3 logs are historical; **final is platform-r4 / 57 / mutation-r1**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6808096 B, 550 members, SHA256 `70565367518761781b5b53ad4d340689ce5610022d2960e394941222ad842c75`**, `allMembersRehashed: true`, **480** product pins. Extract rehashed **550/550**. Parent 329 live tar SHA `2d8b3de8…ca89` (9689148 / 1199 / 479). 329 REVIEW `ddbcb191…1a70` unchanged.

Product vs 329: **477** unchanged, **2** changed (`filesystem.rs` adds `mod directory_entries` + re-export; `lib.rs` adds `DirectoryVisitError` / `DirectoryVisitSummary` to the existing filesystem `pub use`), **1** added (`filesystem/directory_entries.rs` SHA256 `4e599caf…7915` 22041 B). 329 `successor_record_bindings.rs` remains `c29e126f…1d2f`. `visit_entry_names` has **no** security-crate caller. libc remains **`=0.2.189`**. Crate `#![deny(unsafe_code)]`; FFI stays under `#[allow(unsafe_code)] mod filesystem`.

r1 did not compile: `statfs.f_flags` is `u32`, `libc::MNT_UNION` is `i32` (`before-flag-conversion330.rs`). Production uses `libc::MNT_UNION as u32`. That compile-fail is **not** a test result and **not** a mutation kill. r2=56 (before fault seams); r3=57 (before union-guard factoring); **r4=57**.

---

## FFI ownership (source)

`NativeEntries::open` uses `openat(retained, ".", O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK)` — a **new** description, not `dup`/`try_clone`. Mutant `share-directory-offset` (`dup`) is caught.

On macOS, `fstatfs` + `check_mount_flags` runs **before** `fdopendir` (Apple may preload a union directory). `MNT_UNION` and `MNT_UNION|MNT_LOCAL` refuse `Unsupported`. Linux has no equivalent guard.

`fdopendir` takes the fd **only on success**; failure leaves `File` to close it. Success `mem::forget`s the `File` so `DIR` uniquely owns the descriptor. `close_with` `take()`s the pointer and never retries. `Drop` calls `close` (error swallowed on unwind, which is RAII, not a completed summary). Explicit success path **refuses** if `closedir` fails. Mutant `close-error-as-success` is caught. Double-close is a no-op after `take`. Visitor panic still leaves the parent `RetainedDirectory` usable (tested).

`next_with` zeros **this thread’s** errno immediately before `readdir`. Null + errno 0 is EOF; null + nonzero is error. Mutant `keep-stale-errno` turns leftover EIO into a false native error; `native-error-as-eof` turns EIO into `Ok(None)` (would emit a completed `Summary`). Private `read_error`/`close_error` seams inject EIO; production always passes `libc::readdir` / `closedir`.

Name borrow: read `d_reclen` and `d_name` offset only — **no** reference to the full variable-size `dirent`. Span is `min(reclen-offset, 1024 mac / 256 Linux)`. Require NUL, nonempty, no `/`; Darwin `d_namlen ==` NUL index. Slice lives only until the next `readdir`/close; `visit` calls the visitor while that borrow is live, then continues. No clone/open of the entry inside this component.

Limits (0 allowed, caps 131072 / 256MiB) are checked **before** the visitor. Zero entry limit may `readdir` one borrowed record then `EntryLimit` with **zero** callbacks. Exact OS count + exact name-byte cap can EOF-succeed. One extra native entry may be read to detect overflow; that extra is not dispatched. Mutants `ignore-entry-limit` / `ignore-name-byte-limit` / `visitor-before-limits` / `ignore-limit-profile` are caught.

This wrapper does **not** skip `.` / `..` / non-UTF8. Mutants `drop-dot-entries` and `drop-non-utf8-entries` are caught (the latter on the fake `0xff,0xfe` name). Native macOS tests cover regular file, subdirectory, dangling symlink, FIFO, 512 long names, `.`/`..` → **518**, plus nested/repeat streams with independent offsets. **Not** all possible `d_type`s. Linux `directory_visit_native_linux_preserves_non_utf8_names` is `cfg(target_os = "linux")` and was **not executed** on this macOS review.

Union refusal is a **predicate** on `f_flags` (`0` ok, UNION / UNION|LOCAL refuse). No actual union mount was created. Mutant `ignore-union-flags` is caught by that predicate test only.

`NativeEntries` is a private stack type. `NonNull<DIR>` is auto-`Send`/`Sync`; the API never stores the stream across threads. Concurrent `visit_entry_names` on `&RetainedDirectory` each `openat` independently.

---

## Library-scope limitations (do not promote to census)

`DirectoryVisitSummary` is **only** completed-stream entry and visible-name-byte counts after EOF **and** successful close. It has no standing, no canonical names, no 64-cap, no foreign-name report, no security `Budget`. The visitor **must** charge the same operation Budget **before** cloning or materializing; this crate does not.

Apple `readdir` (cited Libc `main`, **not** an installed-binary pin) skips **whiteouts and zero-inode** slots and may return **null without errno** on malformed internal dirent alignment/length. That path is **indistinguishable from EOF** in this wrapper (`errno==0` → `Ok(None)` → `Summary`). “All names” here means all names **the supported OS stream returned**, not proof that every raw on-disk slot was exposed.

POSIX directory mutation during iteration has **unspecified** visibility. A renamed retained handle still names the original object (tested vs a decoy at the old path); that is **not** proof the selected pathname still names it. Libc prefetch/buffering is **not** charged as retained bytes. No kernel-cache, RSS, or bounded-deadline claim. Selected FS/kernel/libc qualification, native fence/exclusion, and a future enumerator that charges **every** candidate (including foreign names) **before** materialization remain **mandatory** before any authority owner treats EOF as a complete physical census.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **57 passed / 0 failed / 0 ignored**; `Compiling opensip-platform`; 0.16s |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **18** unchanged security includes + `directory_entries.rs` | exit 0 |

---

## Mutants

Twelve compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`38e19d07…e7ce`**, **byte-identical** to frozen r1. All **13** compiled.

| Control | First failure (class) |
|---|---|
| `ignore-entry-limit` | fake stream still dispatches past max |
| `ignore-name-byte-limit` | name-byte overflow not `NameByteLimit` |
| `visitor-before-limits` | extra `valid` callback before native error |
| `drop-dot-entries` | `.`/`..` omitted from fake stream |
| `drop-non-utf8-entries` | `0xff,0xfe` omitted |
| `share-directory-offset` | `dup` vs independent `openat` |
| `keep-stale-errno` | leftover EIO not EOF |
| `native-error-as-eof` | EIO `read_error` becomes `Ok(None)` |
| `swallow-visitor-error` | visitor `Err` not `DirectoryVisitError::Visitor` |
| `ignore-limit-profile` | `MAX_ENTRIES+1` accepted |
| `ignore-union-flags` | `MNT_UNION` predicate returns `Ok` |
| `close-error-as-success` | failing `closedir` treated as success |
| baseline | 57 passed |

---

## Findings

The FFI ownership, errno/EOF split, borrowed-name bounds, independent `openat`, close-once, and “no completed summary on failure” rules are consistent with the disclosed POSIX/`fdopendir` contract **for names the OS actually returns**. Tests do not, and cannot, close the Apple skip/null-without-errno hole, Linux ABI, actual union mounts, concurrent mutation, or a security census owner.

**Actionable defects in this freeze:** none that make `visit_entry_names` self-contradictory with its stated stream contract on the macOS 57 tests and 12 controls.

**Must not be counted closed:** physical/qualified census, custody, native current, canonical 64-cap, whiteout/raw-slot completeness, Linux execution, actual union streaming, writers, M2–M6.

---

## Remaining (do not count closed)

Selected-FS/kernel/libc qualification and native fence; enumerator that charges every candidate including foreign names before materialization; security Budget join; Linux ABI/non-UTF8 native execution; union-mount behavior; corrupted-dirent vs EOF; full native entry-kind set; 329 successor composition is a different owner.

---

## Verdicts

- [x] **330 as frozen private OS directory-name stream:** archive verified; 329 report preserved; independent `openat`+RAII `DIR`; errno-0 EOF vs error; borrowed names; limits before visitor; close failure not success; live 57/0 ignored; Clippy/fmt; 12 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** a qualified physical census, custody, native current, security Budget owner, or product installation.
