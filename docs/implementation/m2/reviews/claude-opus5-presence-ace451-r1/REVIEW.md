# Review: presence ACE 451

The actual model is Claude Opus 5.5 (model ID `claude-opus-5-5[1m]`), serving as the assigned Claude Opus 5 reviewer on wF:p1. Single reviewer, 2026-09-22. Grok leads. No repository edits, commits, pushes or delegation. All writes are under this directory.

Every git call against the product ran with `GIT_OPTIONAL_LOCKS=0`, and the product index is byte-unchanged. I owned the serial native lane and ran every native job serially, 22:15–22:19Z. The lane is released with this report. I did not access the private 413 UUID fixture.

## Verdict: REQUIRED-FINDINGS (not accepted)

| Subject | Verdict | Required findings |
|---|---|---|
| Uncommitted `crates/platform/src/macos.rs` (`edcbaed9…`, 13601 B) and `crates/platform/src/filesystem/descriptor_acl_capture.rs` (`7238923b…`, 33031 B) on product a11f267 | **REQUIRED-FINDINGS** | RF-1, RF-2, RF-3 |

**Direct answer to the question asked.** Replacing the whole ACL with one group deny of delete is **not** an acceptable presence marker. It fails for two independent reasons, each a required finding:

- **RF-1.** The chosen deny binds the owner whenever the owner is in the file's group, which is the default case. It then blocks the owner's own unlink, atomic rename-over, rename and rmdir.
- **RF-2.** The replacement itself discards every existing ACE, inherited ones included. That makes the helper an ACL-rewriting policy action rather than a marker, and without a precondition it can widen effective access.

The replay itself is clean: rustfmt 0, 12 tests pass. The capture decodes the marker exactly as the test claims. The findings are about what the marker *does*, not about the capture.

## Subject

- **Product state.** HEAD is a11f267. `git status`/`git diff` show only the two modified paths (`evidence/subject-diff-vs-a11f267.patch`), and both pins match.
- **Base.** The capture file's base is the committed 449 bytes `eab5c0a8…`.
- **Context.** a11f267 adopts my 450 O1 recommended tests (other-kind exact permissions and file exactness).
- **`macos.rs`.**
  - The former test-only `set_probe_acl` body becomes the production `pub(crate) install_single_ace(file, group, id, tag, mask)`. It is `acl_init(1)` + one entry + `acl_set_fd_np(fd, acl, ACL_TYPE_EXTENDED)`, which **replaces** the extended ACL.
  - New production `pub(crate) install_non_granting_presence_ace(file)` calls it with (group, file gid, tag 2 deny, mask 1<<4 DELETE).
  - `set_probe_acl` becomes a `cfg(all(test, macos))` wrapper.
- **Capture test.** `acl_capture_sees_one_non_granting_presence_ace` installs the marker on a fresh 0600 file and asserts `Entries(1)`, kind 2, rights exactly 0x10, and a `Group` principal.

## Replay

Environment: `env -i`, with an isolated `CARGO_HOME` copy, a fresh `CARGO_TARGET_DIR`, and `TMPDIR` all under this directory.

| # | Command (cwd product) | Exit |
|---|---|---|
| 01 | `rustfmt --edition 2024 --check` on both paths | **0** |
| 02 | `cargo test --locked --offline -p opensip-platform --lib acl_capture_` | **0** — 12 passed, 144 filtered; no warnings in the test build |
| 03 | extra: `cargo check --locked --offline --workspace --all-targets` | 0 — but **`opensip-platform` (lib) generated 10 warnings** (RF-3) |
| 04 | extra: reviewer native probe of the marker (copy only) | 0 — `evidence/probe-results.json` |
| 06 | extra: reviewer probe of two alternative markers (copy only) | 0 — `evidence/alternative-results.json` |

The snapshots before and after the runs are identical. Product HEAD, status and index, both subject files, the lock, the product `target/`, and the shared `~/.cargo/.global-cache` are all unchanged, and the architecture repo is clean. About 240 MB of scratch was deleted.

## Native probe of the candidate marker (`evidence/presence_probe.rs`)

I ran the candidate's own `install_non_granting_presence_ace` on a copy, on scratch objects under my TMPDIR. Parent A keeps the `/tmp` default group. Parent B is `chown`ed to my primary group, which is the normal situation under a home directory or `/var/folders/…/T`.

| Case | A: owner **not** in the file's group | B: owner **in** the file's group |
|---|---|---|
| marker installed; capture | `Entries(1)` kind 2 rights 0x10 `Group` | same |
| owner writes via fd | Ok | Ok |
| owner unlinks the marked file | Ok | **EACCES (13)** |
| owner renames a new file over it (atomic replace) | — | **EACCES (13)** |
| owner renames the marked file away | — | **EACCES (13)** |
| owner rmdirs a marked directory | Ok | **EACCES (13)** |
| owner renames a marked directory | — | **EACCES (13)** |
| after owner `chmod -N`: unlink / rmdir | — | Ok / Ok |

Replacement semantics (parent A):

| Case | Before the marker | After the marker |
|---|---|---|
| C pre-existing `user:nobody allow read` + `group:everyone deny write` | `Entries(2)` | `Entries(1)` deny-delete only: **both discarded** |
| D child inheriting `group:everyone allow read,file_inherit` | `Entries(1)` kind 1, inherited | `Entries(1)` deny-delete only: **inherited foreign allow erased** |
| E file mode 0644 + `group:everyone deny read` | deny read present | deny read **discarded**, so 0644 mode bits again give group/other read: **effective access widened** |

**Already observed in the owner's own environment.** The owner's default TMPDIR `/var/folders/zg/kvnts3md1tndqtbpbhjh3zwh0000gn/T` is `sb:staff`. It holds two scratch directories from 15:12 today, each containing `record` with `0: group:staff deny delete` (`evidence/owner-tmpdir-leaked-scratch.txt`, listed read-only and not touched).

These are the new test's `Scratch` directories: its `Drop` `remove_dir_all` was denied by the marker. My replay did not leak, only because my TMPDIR's group (wheel) excludes me.

## Required findings

### RF-1 — the marker ACE restricts the owner

`group:<file gid> deny delete` applies to every member of the file's group. On macOS an explicit file-ACL DELETE deny is not overridden by the owner's POSIX permissions. So whenever the owner belongs to the file's group — the default for objects created under a home directory, whose group is the owner's primary group — the owner can no longer unlink, atomically replace by rename, rename or rmdir the marked object (probe B, EACCES). The unit's own test already leaks state this way.

A presence marker must be behaviour-neutral for the owner. This one would break later publication by rename, staging cleanup and removal, or force a `chmod -N` before each.

**Fix (measured under parent B, `evidence/alternative-results.json`).**
- ALT1, a **zero-rights allow for the owner** (tag 1, mask 0), is stored and captured as `Entries(1)` kind 1 rights 0x0. It grants nothing and denies nothing. The owner's rename-over and unlink succeed. `private_access` accepts PERMIT with zero rights; that is pinned by the 448 P13 kill.
- ALT2, `user:nobody deny delete`, also works and leaves the owner unaffected.
- ALT1 is the most neutral.

### RF-2 — whole-ACL replacement is policy, not a marker, and can widen access

`acl_set_fd_np(…, ACL_TYPE_EXTENDED)` with a one-entry ACL discards every existing ACE:
- explicit allows and denies (C)
- inherited foreign allows (D)

That is an ACL-rewriting policy decision, contrary to "presence marker … not creator policy". With no precondition on mode or ownership, discarding a deny can widen effective access: in E, on a 0644 file, group/other read comes back. That contradicts the doc claim "does not grant access". The ACE grants nothing, but the operation can.

**Fix.** Make the marker additive. Read the descriptor's ACL, append the marker ACE, and write it back on the same descriptor, so existing and inherited ACEs stay visible to the capture and the predicate. `private_access` then refuses an inherited foreign allow, as it should. If clearing inherited ACEs on objects the creator just made is wanted, that is creator policy: it belongs in a separately reviewed unit with explicit preconditions (a fresh object created in this operation, exact private mode, invoking-user owner), not in a function named and documented as a neutral marker.

### RF-3 — production helpers without a production caller add 10 warnings

`install_non_granting_presence_ace` and the generic `install_single_ace` are production `pub(crate)` with no non-test caller. The platform lib build now reports 10 `dead_code` warnings: the two functions plus the eight FFI declarations inside the writer. The workspace check was warning-free at every accepted state from 447 through 450.

The generic writer can install any ACE, including allows, and it moved from test-only to production scope.

**Fix.**
- Keep `install_single_ace` private to `macos.rs`.
- Either land the marker together with its reviewed caller, or keep it `cfg(test)` until the creator unit wires it.
- Do not paper over this with `allow(dead_code)`.

## Observations (non-blocking)

- **O1.** After the fix, add a regression test with the probe-B shape: install the marker under a parent `chown`ed to the owner's primary group, then assert that owner unlink and rename-over succeed and that the capture still returns `Entries`. The current test cannot see RF-1 in a TMPDIR whose group excludes the owner.
- **O2 — cleanup for the owner (outside my write scope).** For each leaked directory in the owner's TMPDIR:
  1. Run `chmod -RN` on it, to drop the deny.
  2. Remove it.

  The two paths are listed in `evidence/owner-tmpdir-leaked-scratch.txt`.
- **O3.** Unchanged and correct:
  - the capture itself, including exact marker decoding;
  - `set_probe_acl` staying test-only;
  - the fd-based write, with no path lookup;
  - the updated SAFETY comment.

## Limits

- Evidence covers this macOS development host only. Linux was not replayed.
- Delete/rename semantics were measured, not taken from pinned XNU source. Superuser behaviour is outside scope.
- There is no creator policy, absence authority, per-vnode profile qualification, private-access wiring, commit or selection.
