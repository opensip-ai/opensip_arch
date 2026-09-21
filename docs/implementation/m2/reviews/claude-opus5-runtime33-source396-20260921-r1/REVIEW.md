# Independent review — native source 396 and formal runtime33

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed.

**Top verdict: ACCEPT-DESIGN-UNIT**, with **three non-blocking required findings**.

The module is correct, honestly documented and well tested. I measured each of its disclaimers rather
than reading them: every limit the README claims is real, and several are sharper than the prose
suggests. The three findings are about what the documentation does not yet say — one of them a seam
between this unit and the runtime32 receipt it will be used with.

---

## 1. Verification

### Declared pins — checked before extraction

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/native-runtime-selection-v33-subject.json` | 2 493 B, `77cd0a6d32047f9d3e764ccfbee69eb5cad0fe535bd78c9259e6f75145068c3c` | identical | ✓ |
| `…/trials/directory-publication-396/subject.tar.xz` | 6 894 260 B, `ca744ec6b00fe33a559eda166a1eff9d9c58e144a4f464fddb574c6ac6d6dcee` | identical | ✓ |
| `…/trials/directory-publication-396/subject.json` | 113 947 B, `da720bdb767b5254cb8cc00f729d37ccceaa23a6dba33b4ade4f563d54155a4e` | identical | ✓ |

### Formal unit — runtime33

**12 / 12** members verified byte-for-byte and by sha256; sorted; unique. Successor
`…/native-runtime-selection-v33/successor.json`, 3 076 B, `18714151…`, standing "PROPOSED retained
private directory staging and exclusive publication; independent source/formal review required".
11 candidates, sorted and unique; `candidates + successor == subject`; `passageOverrides: []`; no
candidate/parent collision; no candidate already locked; the successor itself is not locked.

**Three parents, all current, pinned and genuinely selected** (lock entry *and* assent unit):

| Parent | Live match | Lock site(s) | Assent unit | Status |
|---|---|---|---|---|
| `…/native-runtime-selection-v32/successor.json` | ✓ | `/contractSuccessors/52/record` | `native-runtime-selection-v32-unit.json` | `ACCEPTED-DESIGN-UNIT`, `rootSubstantiveAssent: true`, 0 findings |
| `…/project-registry-owner-selection-v2/successor.json` | ✓ | `/contractSuccessors/48/record` | `project-registry-owner-selection-v2-unit.json` | `ACCEPTED-DESIGN-UNIT`, true, 0 |
| `…/repository-file-inventory.v59.json` | ✓ | `/inventorySuccessors/34/candidate` + 4 × `/inventoryPassageInheritance/*/parent` | **`directory-publication-inventory-v59-r2-unit.json`** | `ACCEPTED-UNIT`, true, 0 |

The inventory parent's assent names the **r2** unit, confirming independently that selection went
through r2 and not the unselected r1 record. Live lock reads 46 inputs, **35** inventory successors,
**53** contract successors — the stated baseline.

### Source archive

**606 / 606** members match the manifest byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched,
0 unsafe (no symlink, hard link, absolute path, `..` component, non-regular member). Composition:
**592 product + 13 evidence + 1 README**.

### Archive lock provenance — the disclosed historical lock, checked

The archive carries `product/design-lock.json` at **98 926 B / `63081729715a81a9ef64dd0a5fb0f41f46c916c6169a774296e08bcab9153b2a`**,
which is **not** the live lock (`48a8f67b…`, 101 003 B). That is the runtime30-era lock retained from
the source395 preparation, exactly as disclosed in the README and in the author's `source-delta.json`.
I verified the exclusion works both ways in my own stage:

- `staged/product/design-lock.json` = **`48a8f67b…`**, byte-identical to the **live** lock — so the
  historical lock was excluded and the current one separately composed.
- `staged/product/tools/typescript-boundary/tests/fixtures/product/design-lock.json` = `ac65d09c…`,
  byte-identical to live — so the exclusion is by **exact relative path**, not basename, and the
  fixture lock remains verified.

### Stage

`native-runtime-selection-v33/stage.py` is **byte-identical** to the v30/v31/v32 helpers
(`3a71d80a…`); four units now share one staging behaviour. My own run reproduced the author's record
exactly apart from the output path:

```
{"archiveMembersVerified": 606, "nonLockSourceFilesVerified": 591, "mapped": 3,
 "unchangedNonLock": 588, "liveProductUnchanged": true, "runtimeAcceptance": false}
```

The `before: null` row for the new file is handled without a helper change.

### Delta — derived independently from `git ls-files`

591 live tracked files, 592 staged: **589 identical, 2 modified, 1 new, 0 absent, 0 archive-only.**

| Path | Before | After |
|---|---|---|
| `crates/platform/src/filesystem/directory_publication.rs` | *(new)* | 25 152 B, `1ad6793cf6a07bdcdc6b8626c3d17cfc9d302ea26ca2e607a2b57e48a9597c06` |
| `crates/platform/src/filesystem.rs` | 81 671 B, `87636b86…` | 81 813 B, `11ab4ced006edd88d154f02f1b75cbf478ab8d557f8012889ed5de368dd912ee` |
| `crates/platform/src/lib.rs` | 3 817 B, `8cbed576…` | 3 895 B, `938ed9827b56dac5f61b1db8090ef71050b62973efac290fbb3be426cbb1287c` |

All three match the declared pins. 588 unchanged non-lock + the lock = 589. 0 package/dependency
changes.

**Both edited files are declaration/export-only, and purely additive.** `filesystem.rs` gains five
lines — `mod directory_publication;` and a three-name `pub use`; `lib.rs` inserts
`DirectoryRenameFailure`, `NamedDirectoryPublication` and `PrivateDirectoryStage` into the existing
re-export list under its unchanged `cfg(any(macos, linux))` gate. No existing line was modified or
removed in either.

---

## 2. The mechanism, read rather than summarised

`PrivateDirectoryStage` and `NamedDirectoryPublication` both wrap one private `Binding { parent,
directory, name }`. The whole unit rests on two operations:

**Staging.** `create_private_directory_stage` dups the caller's parent
(`RetainedDirectory::from_retained_handle(self.0.try_clone()?)`), then loops at most `ATTEMPTS = 8`:
128-bit OS entropy → 32 lowercase hex → `.opensip-stage-install-<nonce>` → `mkdirat(parent, name,
0o700)`. `AlreadyExists` **continues without reading or adopting**; any other errno aborts. On success
it opens the child with `O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK` and requires a
`recheck()` before returning. Exhaustion is `AlreadyExists "private directory stage candidates
exhausted"`.

**Publication.** `publish_exclusive` consumes `self` and calls, through a private fault seam that
production fills with exactly one closure:

```rust
let to = target(name)?;                       // pre-effect grammar → Unchanged on refusal
match self.binding.recheck() { … }            // pre-effect binding check → Unchanged on refusal
let renamed = rename(&parent.0, &self.binding.name, &to);   // NATIVE_NEW_PUBLICATION.rename
if renamed.is_ok() { self.binding.name = to; }
let checked = self.binding.recheck();
if let Err(error) = renamed {
    let visibility = if error.kind() == AlreadyExists && matches!(checked, Ok(true))
        { Unchanged } else { Indeterminate };
    return Err(failure(error, visibility));   // primary syscall error retained
}
match checked { Ok(true) => Ok(publication), Ok(false) => Err(changed(), Indeterminate),
                Err(e) => Err(e, Indeterminate) }
```

Points I checked rather than assumed:

- The rename is the **existing** `NATIVE_NEW_PUBLICATION.rename` — `renameatx_np RENAME_EXCL` on macOS,
  `renameat2 RENAME_NOREPLACE` on Linux, with the pre-existing rule that *no* overwrite fallback is used
  on `ENOTSUP`/`EINVAL`/`ENOSYS` or any other failure. No new syscall wrapper was added.
- `target()` refuses empty, `>1023` bytes, `.`/`..`, NUL, `/`, `\\`, and **any name beginning with the
  reserved `STAGING_PREFIX`** — so a caller cannot publish into the staging namespace.
- `recheck()` compares `dev`/`ino` between the retained handle and a fresh `openat` of the bound name
  under the retained parent; `exact()` brackets a macOS leaf-name comparison between two rechecks.
- No `Drop`, no cleanup, no retry, no flush, no delete, no merge. `publish_exclusive(self)` consumes
  the handle, so a failed attempt cannot be resumed.
- **Zero production callers.** `PrivateDirectoryStage`, `NamedDirectoryPublication` and
  `DirectoryRenameFailure` appear only in their own module, the twelve tests and the two export lines.

---

## 3. Independent replay

My own staged tree, fresh review-local `CARGO_TARGET_DIR`, serial, pinned environment
(`HOME=/Users/sb` unchanged, `PATH=/usr/bin:/bin`, shared offline `CARGO_HOME`, pinned
`RUSTC`/`RUSTDOC`, `LC_ALL=C LANG=C TZ=UTC`, `CARGO_INCREMENTAL=0`, `RUST_TEST_THREADS=1`, pinned
`TMPDIR`). **No author binary, target directory or script reused.**

| Check | Result |
|---|---|
| `cargo test … -p opensip-platform directory_publication` | **12 passed, 0 failed, 115 filtered out** |
| `cargo check … --workspace --all-targets` | **clean, 17.13 s** |
| `cargo test … --lib -- --list` | **127 tests** |
| `cargo doc --no-deps` with `-D rustdoc::broken_intra_doc_links` *(reviewer addition)* | **clean** |

The live pre-396 crate lists **115** tests and the staged crate **127** — exactly 12 added, none
removed or renamed. All twelve author test names pass, including the two-contender race, the
parent-relocation boundary, the after-effect EIO seam and the EEXIST-with-changed-stage case.

The retained preparation note is accurate: the first freeze script's module-only assertion expected a
one-line `pub use` while the tested `filesystem.rs` uses multiline formatting, and it **stopped before
creating any frozen directory or archive**. I confirmed the shape it was asserting about — five
inserted lines in `filesystem.rs`, three re-exports in `lib.rs`, nothing else — so this was a
preparation-verification failure, not a compile or test failure, and the original script is retained in
the archive.

---

## 4. Reviewer probes — public API only

Six probes against a private copy of the staged tree whose `directory_publication.rs` hashes identically
to the staged one. No subject byte modified. Output in `evidence/reviewer-probe.stdout`.

| Probe | Measured result |
|---|---|
| **P1** barrier-receipt identity across the stage's parent handle | `is_for(caller_parent)=true`; **`is_for(stage.parent_directory())=false`** — same underlying directory |
| **P2** 300-byte final name (passes the 1023-byte grammar, exceeds NAME_MAX) | `File name too long (os error 63)`, `InvalidFilename`, **visibility `Indeterminate`**, target absent, stage still on disk |
| **P3** parent renamed away after publication | **`recheck_binding()=true` and `recheck_exact_name()=true`** while the original path no longer exists |
| **P4** arbitrary contents | `["not-a-p0-tree", "random-subdir"]` published unvalidated |
| **P5** target inside the reserved staging prefix | `InvalidInput`, **`Unchanged`**, original stage intact |
| **P6** EEXIST loser | `AlreadyExists`, **`Unchanged`**, handle consumed, **stage directory still present** |

P3 is worth emphasising: *both* recheck methods answer true after the parent moves, so the macOS
exact-name observation does not narrow this boundary either — it checks the leaf spelling, not the
ancestry. The README says exactly that; now it is measured.

P5 and P6 confirm the two `Unchanged` paths are real and correctly separated from `Indeterminate`.

---

## 5. Required findings — three, all non-blocking

### RF-1 — the runtime32 receipt cannot be tied to the handle this unit uses

`create_private_directory_stage` dups the caller's parent into its own `RetainedDirectory`, so
`stage.parent_directory()` (and the publication's) is a **different handle object** wrapping a dup of
the same fd. `DirectoryBarrierReceipt::is_for` — which runtime32 deliberately defines as handle-object
identity, not directory identity — therefore answers `false` across the two (probe P1).

The consequence is concrete. This module's own doc says the caller "must keep its original fence
through the required parent barrier". A semantic owner performing that barrier on its own parent handle
obtains a receipt that **cannot be shown, through the public API, to concern the parent this
publication used** — there is no public directory-identity comparison between two `RetainedDirectory`
values. Two correct implementations could apply the barrier to different handles and neither could prove
the association.

*Required:* document the relationship in this module (the parent is a dup; a runtime32 receipt taken on
the caller's handle will not `is_for` the publication's), or expose a way to compare the publication's
parent with a caller-held handle. Documentation is sufficient; a new comparison would need its own
review.

### RF-2 — the error-retention rule is stated for one direction only

The doc says: *"The original syscall error is retained when both rename and post-check fail."* It does
not say what the caller receives when the **rename succeeds and the post-check fails** — which is the
`Ok(false) => changed()` / `Err(e) => e` arm, returning the post-check's error with `Indeterminate` and
no indication that the rename itself succeeded.

The behaviour is right: a successful rename whose binding no longer verifies is genuinely
indeterminate. But this is the same class of undocumented precedence I raised as RF-3 against source393,
which root closed in source395 by stating both directions explicitly. The symmetric sentence is missing
here.

*Required:* state that when the rename succeeds and the post-check fails, the post-check's error is
returned and the successful rename is not reported.

### RF-3 — definitionally pre-effect syscall refusals are also `Indeterminate`

`Unchanged` is reachable only from a pre-syscall refusal (`target()` or the pre-rename `recheck`) or
from `AlreadyExists` with the original stage still bound. Every other rename errno — including ones
that are *definitionally* pre-effect, such as `ENAMETOOLONG` (probe P2, measured: nothing published,
stage intact, yet `Indeterminate`) — is reported uncertain.

Conservative is the right default and I am not asking to enumerate errnos. But the cost is not stated:
under the creation law this primitive is built for, `Indeterminate` latches the invocation, so a caller
that passes a final name longer than `NAME_MAX` burns the whole attempt instead of receiving a clean
request rejection. Callers need to know to validate the final component against the platform's limits
themselves — the module's 1023-byte grammar deliberately is not a `NAME_MAX` oracle, consistent with the
grammar-versus-kernel separation established in source389.

*Required:* say that `Indeterminate` covers refusals that could in principle be known pre-effect, and
that the caller owes its own platform name-length admission.

---

## 6. Observations — recorded, not required

- **O-1.** Failure consumes the stage, there is no `Drop` cleanup, and the type "cannot be reconstructed
  from a name, parsed nonce or existing directory". The compound consequence, measured in P6: every
  failed publish deterministically leaves one directory that **the same process can no longer address
  through this API**, so a retry loop leaks one stage per attempt. Each part is disclosed; the
  combination is not, and owner397 §6 already anticipates a separately specified cleanup mechanism.
- **O-2.** `mkdirat` mode `0o700` is subject to umask and inherited ACLs — stated in the doc, and worth
  keeping visible because the owner law requires 0700 exactly. The unit observes the resulting mode in
  its own test but cannot enforce it.
- **O-3.** The parent `nlink() == 0` arm in `recheck()` carries the same macOS caveat runtime32
  documented: a positive link count is not attachment. Consistent with P3.
- **O-4.** `O_NONBLOCK` on the directory open is harmless and belt-and-braces alongside `O_DIRECTORY`;
  noted only so it is not mistaken for a behavioural requirement.
- **O-5.** The fault seam `publish_with` is private and production passes exactly one closure, so no
  public caller can substitute the syscall — the same discipline as `confirm_directory_with` in
  runtime32.
- **O-6.** Tests run on the pinned `TMPDIR` volume (APFS), not a prospective installation-root volume,
  and the twelve tests are macOS-only in effect. No Linux, crash, power-loss or profile qualification is
  claimed or checked.

---

## 7. Limits

- **Level:** source reading, formal-pin verification, native test replay, a reviewer-added rustdoc pass,
  and public-API probing.
- **Platform:** macOS arm64 development lane only.
- **Not qualified:** Linux execution, crash and power-loss durability, filesystems other than the pinned
  APFS `TMPDIR` volume, custody, actor identity, native profiles, shared budgets, GC, release.
- **Not re-reviewed on their merits:** runtime32/source395, inventory59, registry-v2 — only currency,
  pins, lock presence and assent status.
- **Unselected references remain unselected:** owner397 and the in-progress 399, owner392, S9.3, 215.
  This unit adopts none of them, and accepting it grants no creator permission.
- **Replay caveat:** the author's two checks run the author's tests. The independent parts are the
  `git ls-files` delta, the lock-provenance verification in both directions, the 115→127 test count, the
  rustdoc pass, and probes P1–P6.

---

## 8. Context HEADs — as of 2026-09-21T16:07:14-07:00

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `6f3136e83d3288ddba17d06d4a4a894adb8b1436` | "Correct diagnostic count semantics and freeze explicit inventory inheritance" | 2026-09-21T15:57:23-07:00 |
| product | `4b298dae44e553e8317cf68350f5201cd3fc6771` | "Select directory publication module layout with explicit inherited descriptions" | 2026-09-21T16:00:33-07:00 |

Product tree clean; runtime33 is **not** integrated. At this sample the 396 trial archive and manifest
are committed with matching blob ids, while the v33 formal subject and its successor are present and
byte-verified on disk but not yet tracked. The verified pins, not these labels, are the authority.

---

## 9. Attestation

Read-only against live, frozen, history, product and lock. No architecture, product, frozen, history or
lock byte was edited; no pin edited; no select script run; no commits, no pushes. All writing went into
this review directory; extraction and both build trees are review-local. The author's binary and target
directory were not reused. Running `cargo` inside the product repository to count its tests left that
repository clean, verified after.

This grants no root assent, no formal selection, no native creator permission, no owner397 or owner399
acceptance, no current authority, no S9.3 or 215 adoption, no M2 completion and no release
qualification. Every earlier report is untouched and keeps its own standing.

Reviewer: Claude Opus 5 (1M context).
