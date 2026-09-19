# Independent bounded review — linked capture 124 (Rust)

Reviewer: Claude (actual independent reviewer; Codex remains implementation owner). 2026-09-18.
Request: `REQUEST.md`. Scope: the delta of frozen `linked-capture-checkpoint-124` over frozen 123 —
`platform/src/filesystem.rs` (`RetainedDirectory::is_reachable`, including its `unsafe` `F_GETPATH` call)
and `security/src/journal_store.rs` (capture ordering, open/read seam) — as correction of my capture121
F-1, F-2, F-3. Not 118 I-2 closure, not custody, not OS qualification, not cumulative approval. No
frozen/selected/product edit; scratch builds with dedicated target directories; no commit, push or
delegation.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 4,105,928 bytes, SHA-256 `9e07e6349cfebfd32becf91f457baeb455a1f12f130869e91f4024be235a62c3` = request and `archive-pin.json` |
| Members | 396/396 regular, each length + SHA-256 equal to the manifest from the tar; 0 unsafe/extra; re-verified clean afterwards |
| Product pins | 330/330 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 123 extraction; 328 unchanged |
| Changed | `crates/platform/src/filesystem.rs` `eb86230f…`, `crates/security/src/journal_store.rs` `7d28aa64…` |

## 2. What changed (read in full)
`is_reachable()`: `fstat` the retained descriptor (`nlink == 0` ⇒ false); on macOS `fcntl(F_GETPATH)` into a
`PATH_MAX` buffer, require a NUL-terminated absolute path, reopen it with
`O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`, `NotFound` ⇒ false, any other error ⇒ `Err`, otherwise compare
`(st_dev, st_ino)` with the retained descriptor; on Linux `Ok(true)` after the link-count test (declared
pending target qualification). The `unsafe` block has a SAFETY comment and is sound: a live descriptor and
a buffer of exactly the size `F_GETPATH` may write. Capture: reachability is checked **before the open,
after the open — even a failed one, before its result is interpreted — and after the read**; unreachable ⇒
`Unreadable(Context)`, reachability error ⇒ `Unreadable(Io)`; the bounded read is now
`read_bounded_operational(impl Read, …)` behind a private open seam.

This is a different and better design than the link-count idea I proposed and then withdrew: it does not
trust the stale path `F_GETPATH` returns — it **re-resolves it and compares identity**, so a stale path to a
vanished or re-created directory yields `NotFound` or a different inode.

## 3. Evidence
Scratch build: platform **29**, security **75** passed, 0 failed.

**Real-filesystem probe** (`probes/reachability.txt`, APFS, non-root; `floor` never existed in any case):

| Retained directory is then… | `is_reachable` | capture `witness` | capture `floor` |
|---|---|---|---|
| untouched | true | Present | Absent |
| removed | **false** | `Unreadable(Context)` | `Unreadable(Context)` |
| removed, new directory with a witness at the path (121 F-1) | **false** | `Unreadable(Context)` | `Unreadable(Context)` |
| removed, a regular file at the path | `Err(ENOTDIR)` | `Unreadable(Io)` | `Unreadable(Io)` |
| renamed (still linked) | true | Present | Absent |
| renamed away, symlink to it left at the old path | true | Present | Absent |
| **renamed away, a different directory with a witness at the old path** | **true** | Present (the *moved* directory's bytes) | **Absent** |
| moved under a directory that becomes mode 000 | `Err(EACCES)` | `Unreadable(Io)` | `Unreadable(Io)` |
| an ancestor replaced by a symlink to its new location | true | Present | Absent |
| absolute path ≈ 1,551 bytes (> `PATH_MAX`) | `Err(ENOSPC)` | `Unreadable(Io)` | — |

**Mutation** (12, all compiled, baseline green): **9 killed** — inode not compared; `NotFound` treated as
reachable; every reopen error flattened to "unreachable"; reachability ignored; only the first check kept;
recheck after open removed; recheck after read removed; partial bytes returned as `Present` after a read
error (121 F-2); `PermissionDenied` mapped to `Absent` (121 F-2). **3 survived** (§4 F-2).

## 4. Findings

- **F-1 (limit, confirmed and correctly disclosed) — reachable is not "still at the custody path".**
  Row 7: the retained directory was renamed away and a *different* directory now sits at the path the
  caller believes it is reading; `is_reachable` is true (the inode is linked, somewhere), the capture
  returns the moved directory's witness, and `floor` is **`Absent`**. 124 says exactly this ("conditional
  caller custody, not permanent name binding"), and it is the right boundary for a leaf capture. But it
  means **121 F-1 is closed for unlinked parents and remains a caller obligation for relocated ones**:
  whoever consumes `Absent` — the `witnesslessRestore` marker path in particular — must hold an
  ancestor-anchored identity for the custody directory (the `(dev, ino)` re-resolution from my 121
  addendum), because this API cannot supply it. Put that sentence where `Absent` is consumed, not only
  here.
- **F-2 (low–medium, tests) — a reachability *error* treated as reachable survives.** With
  `Err(_) => Ok(())` in `linked_operational_parent`, every test passes. My rows 4, 8 and 10 are real
  instances (`ENOTDIR`, `EACCES`, over-long path): under that mutant they would return `Present`/`Absent`
  from a directory whose linkage could not be established. The owner's permission test pins the platform
  side, not this mapping. One case through the existing open seam with a parent whose reachability errors
  closes it. The other two survivors are equivalent in practice: *device not compared* needs an inode
  collision across volumes, and *`O_NOFOLLOW` dropped* is never exercised because `F_GETPATH` returns the
  directory's real path, not the symlink (row 6).
- **F-3 (note) — availability limits of the macOS method**, both fail-safe: a custody directory whose
  absolute path exceeds `PATH_MAX` makes every capture `Unreadable(Io ENOSPC)` (the error kind reads as
  "storage full", which will mislead an operator — map it to a context error), and a directory the process
  cannot re-traverse by path (row 8) is unreadable even though `openat` through the retained descriptor
  would work. State both next to the local-filesystem precondition.
- **F-4 (note)** — Linux returns `Ok(true)` after the link-count test. On Linux an unlinked directory does
  report `nlink == 0`, so that branch is plausible, but it is unexecuted here and, like row 7, says nothing
  about relocation. The README is candid about this.

## 5. Closure of 121
| 121 finding | Status |
|---|---|
| **F-1** unlinked retained parent reads as `Absent` | **Closed for removal and removal-plus-recreation** (both now `Unreadable(Context)`, checked before and after the open and after the read). Relocation remains a disclosed caller obligation (F-1 above). |
| **F-2** two surviving mutants | **Closed** — both killed; the read seam exists and partial reads never become `Present`. |
| **F-3** case-insensitive leaf | Documented beside the leaf rules. |

## 6. Bounded verdict
**124: reviewed, no blocking finding. 121 F-1 is closed for unlinked parents and honestly bounded for
relocated ones; 121 F-2 and F-3 are closed; F-2 above is a one-case test follow-up and F-3 two operator
notes.** Not 118 I-2 closure, not custody or OS qualification, not cumulative approval.

Evidence: `claude-out/pin-verification.json`, `product-pins.json`, `filesystem.diff`, `journal_store.diff`,
`probes/rust_probe.rs.txt`, `reachability.txt`, `mutation.{py,json,log}`, `hashes.txt`.
