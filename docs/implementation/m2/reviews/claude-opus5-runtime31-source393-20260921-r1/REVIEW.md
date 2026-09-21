# Independent review — source 393 (retained directory barrier receipt) and formal runtime31

Reviewer: Claude Opus 5 (1M context), model id `claude-opus-5[1m]`. Capacity available; a substantive
review was performed — nothing here is a quota report.

**Top verdict: ACCEPT-DESIGN-UNIT**, bounded to the platform primitive and its formal unit
`native-runtime-selection-v31`. Three required findings are recorded, all non-blocking: they concern
the precision of the shipped evidence and documentation, not the correctness of the source. Section
10 states what this acceptance is not.

---

## 1. Context HEADs — sampled at the END

Per the request, both HEADs were sampled after all verification, replay and probe work had finished,
not at the start. Recorded in `evidence/head-context.json`.

| Repository | HEAD at end of review | Subject | Committed |
|---|---|---|---|
| architecture | `613d3c7a85b8726e4d27cbea9805c29484dd70dd` (`613d3c7a8`) | "Resolve initial creation review gaps and freeze directory barrier candidate" | 2026-09-21T14:53:01-07:00 |
| product | `cd5af4dbf524b81ac98876029798d569ccdc0052` (`cd5af4d`) | "Capture native project paths without relaxing internal name rules" | 2026-09-21T14:25:22-07:00 |

The architecture repository **did** advance during this review: it was at `cd753cc02` when the review
started, and root committed `613d3c7a8` at 14:53:01 while this review was in progress. That is exactly the
case the request anticipated, and the end-sampling policy is what makes the label correct rather than
stale. The two earlier stale-HEAD errors (runtime30, owner390) came from sampling early or carrying a
label forward; neither happened here.

The advance does not touch the subject. Every subject byte I verified is what is committed at
`613d3c7a8`, checked by blob id rather than by `git show | shasum`, because `subject.tar.xz` is
Git‑LFS tracked and `git show` would return the pointer:

| Path | committed blob | worktree blob | status |
|---|---|---|---|
| `…/native-runtime-selection-v31-subject.json` | `592076fcd87db429d7259a4a258760a1aab1a043` | identical | clean |
| `…/native-runtime-selection-v31/successor.json` | `4e9e17c1b7fa429065e9a3d83d22bf53c3334f6b` | identical | clean |
| `…/trials/directory-barrier-checkpoint-393/subject.json` | `8baa7dcb8772ef72c1b6e22fcf6ffb034b532a76` | identical | clean |
| `…/trials/directory-barrier-checkpoint-393/subject.tar.xz` | `551694937fb4349ab0f26a22a7e1ee8fc401b59d` (LFS pointer) | identical | clean |

The product repository did not move during the review and its working tree is clean.

---

## 2. Formal unit — `native-runtime-selection-v31`

Subject manifest `docs/implementation/m2/native-runtime-selection-v31-subject.json`, **2521 bytes**,
sha256 `4cb93ab368e30773a6c0c837e636959973a28c06126466149b7fec06a8a38c3d`. Full record in
`evidence/verification.json`.

| Check | Result |
|---|---|
| Declared members | 12 |
| Members verified against live bytes + sha256 | **12 / 12**, 0 failures |
| Member list sorted, unique | yes, yes |
| Successor candidates | 11, sorted, unique |
| `candidates + successor == subject` | yes |
| `passageOverrides` | `[]` |
| Candidate ∩ parents | empty |
| Any candidate already in `design-lock.json` | none |
| Successor itself in the lock | no — correct, it is unselected |
| Standing | "PROPOSED retained directory barrier receipt; independent source/formal review required" |

### Parents

All three declared parents match live bytes exactly **and** are genuinely selected — that is, each has
a `design-lock.json` entry *and* a per-item assent unit, which is the selection test, not the
document's own `standing` header. My first pass reported these as absent from the lock; that was a
defect in my extraction (lock entries nest the pin under `record` / `candidate` / `parent`, never at
the top level). Re-checked by a recursive walk over every object carrying a `path` key.

| Parent | Live match | Lock site(s) | Assent unit | Status |
|---|---|---|---|---|
| `…/native-runtime-selection-v30/successor.json` | yes | `/contractSuccessors/51/record` | `native-runtime-selection-v30-unit.json` | `ACCEPTED-DESIGN-UNIT`, `rootSubstantiveAssent: true`, no required findings |
| `…/project-registry-owner-selection-v2/successor.json` | yes | `/contractSuccessors/48/record` | `project-registry-owner-selection-v2-unit.json` | `ACCEPTED-DESIGN-UNIT`, `rootSubstantiveAssent: true`, none |
| `…/repository-file-inventory.v58.json` | yes | `/inventorySuccessors/33/candidate` + 4 × `/inventoryPassageInheritance/*/parent` | `shared-store-codecs-inventory-v58-unit.json` | `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`, none |

None of the three was re-reviewed on its merits here; only that they are current, pinned and selected.

### Stage helper

`native-runtime-selection-v31/stage.py` is **byte-identical** to the v30 helper
(`3a71d80af89babf7059a3ebe71c127a7dcc43a896f35b7cb6ce1de4cee03b1c4`), so no staging behaviour changed
between the two units. I ran it myself into a review-local output directory and reproduced the
author's record exactly apart from that path:

```
{"archiveMembersVerified": 606, "nonLockSourceFilesVerified": 590, "mapped": 2,
 "unchangedNonLock": 588, "liveProductUnchanged": true, "runtimeAcceptance": false}
```

The historical source lock is excluded by **exact relative path** `design-lock.json`, not by basename,
so `tools/typescript-boundary/tests/fixtures/product/design-lock.json` is still verified. I did not
run any root select script.

---

## 3. Source unit — 393 archive

| Artefact | Bytes | sha256 |
|---|---|---|
| `…/trials/directory-barrier-checkpoint-393/subject.tar.xz` | 6 888 848 | `ea32681e683dd3f18e9d3c3f44e8bd585623228d4faed9f1b038d3b44d0cda2b` |
| `…/trials/directory-barrier-checkpoint-393/subject.json` | 113 891 | `46a1f258d3100033c0d863cd15f71a28681109a9d8f082e8277299b4e31b18bd` |

Both pins were verified **before** extraction, and extraction went only into the review directory.

- **606 / 606** members match the manifest byte-for-byte and by sha256.
- 0 missing, 0 extra, 0 mismatched.
- 0 unsafe members: no symlink, no hard link, no absolute path, no `..` component.
- Composition: **591 product + 14 evidence + 1 README**.

### Delta against live product

Independently derived from `git ls-files` in the live product repository, not from the author's
`source-delta.json`:

- 591 live tracked files; **589 identical**, **2 differing**, 0 live-only, 0 archive-only.
- `crates/platform/src/filesystem.rs` 73 907 → 80 615 bytes
  (`9a02dcbb…` → `d90d6bf2…`).
- `crates/platform/src/lib.rs` 3 792 → 3 817 bytes (`d13e441f…` → `8cbed576…`).
- 0 new files, 0 package-graph changes, no new crate edge or inventory entry.

**The `filesystem.rs` diff is purely additive: 166 added lines, 0 removed and 0 modified.** The
`lib.rs` diff touches only the `pub use filesystem::{…}` list — `DirectoryBarrierReceipt` inserted and
the list reflowed; no item removed, and the existing
`#[cfg(any(target_os = "macos", target_os = "linux"))]` gate is unchanged, so the new type is exported
on exactly the same targets as its neighbours. Nothing in the selected source was edited.

An independent count corroborates this: the **live** platform crate lists **110** unit tests, the
staged crate lists **115**. Exactly five tests were added; none was removed or renamed.

---

## 4. What the change actually is

Two additions to `crates/platform/src/filesystem.rs` plus one export.

```rust
pub struct DirectoryBarrierReceipt<'directory> {
    directory: &'directory RetainedDirectory,
    barrier: DirectoryBarrier,
}
impl DirectoryBarrierReceipt<'_> {
    pub fn barrier(&self) -> DirectoryBarrier { self.barrier }
    pub fn is_for(&self, directory: &RetainedDirectory) -> bool {
        std::ptr::eq(self.directory, directory)
    }
}
```

```rust
pub fn confirm_directory_barrier(&self) -> io::Result<DirectoryBarrierReceipt<'_>> {
    self.confirm_directory_with(|directory| NATIVE_PUBLICATION.sync_directory(directory))
}
fn confirm_directory_with(&self, flush: impl FnOnce(&File) -> io::Result<DirectoryBarrier>)
    -> io::Result<DirectoryBarrierReceipt<'_>>
{
    let before = self.0.metadata()?;
    if !before.is_dir() || before.nlink() == 0 { /* InvalidData, before any flush */ }
    let attempted = flush(&self.0);
    let after = self.0.metadata()?;                 // sampled even after a failed barrier
    if !after.is_dir() || after.nlink() == 0
        || before.dev() != after.dev() || before.ino() != after.ino() { /* InvalidData */ }
    Ok(DirectoryBarrierReceipt { directory: self, barrier: attempted? })
}
```

Structural points I checked rather than assumed:

- `barrier()` returns by value; this needed **no** change to the enum, which already derived
  `Debug, Clone, Copy, PartialEq, Eq`. That is the same fact the author's preparation note records.
- The production path hard-codes the `NATIVE_PUBLICATION` constant, which is the same constant the
  file-publication path uses. `sync_directory` is **unchanged**: macOS tries `F_FULLFSYNC` once, and
  only `EINVAL` / `ENOTSUP` / `ENOTTY` — the existing named set — permit the `fsync` fallback; Linux
  calls `fsync`. `confirm_directory_with` is private and exists only as a test seam.
- `flush` is invoked exactly once. There is no retry, no loop, and no `EINTR` special case.
- Receipt fields are private and there is no public constructor, so the type is unforgeable outside
  the crate.
- **Zero callers.** A repository-wide search of the staged tree finds `confirm_directory_barrier` and
  `DirectoryBarrierReceipt` only in their own definition, the five new tests and the export list. No
  production caller switched; no initialization or write path was wired.

`is_for` is sound. The receipt holds a shared borrow of the handle, so borrow checking prevents the
handle from being moved or dropped while the receipt lives; two distinct live `RetainedDirectory`
values cannot share an address, and `RetainedDirectory(File)` is not zero-sized. There is no
false-positive path.

---

## 5. Independent replay

Run against **my own** staged tree, with a fresh review-local `CARGO_TARGET_DIR`. No author binary,
author target directory or author script was reused. Environment exactly as pinned — `HOME=/Users/sb`
preserved, `PATH=/usr/bin:/bin`, the shared offline `CARGO_HOME`, pinned `RUSTC`/`RUSTDOC`,
`LC_ALL=C LANG=C TZ=UTC`, `CARGO_INCREMENTAL=0`, `RUST_TEST_THREADS=1`, and the pinned `TMPDIR` (no
host `/tmp` default, no `HOME` override). Commands, stdout and stderr in `evidence/replay-*`.

| Check | Command | Result |
|---|---|---|
| New receipt tests | `cargo test --locked --offline -p opensip-platform directory_barrier` | **5 passed, 0 failed, 110 filtered out** |
| Existing fallback test | `cargo test --locked --offline -p opensip-platform directory_fallback_accepts_only_named_unsupported_errors` | **1 passed, 0 failed, 114 filtered out** |
| Workspace | `cargo check --locked --offline --workspace --all-targets` | **clean, 15.86 s** (author: 17.60 s) |

Every figure the author reported reproduces exactly. All five new test names pass, including the
rename/inode test and the kind-guard test.

---

## 6. Reviewer probes — the adversarial part

The replay above establishes reproducibility, not independence: it runs the author's own assertions.
So I wrote my own probe against a **private copy** of the staged tree, as a `tests/` integration file
using the **public API only**. No subject byte was modified — the copied `filesystem.rs` hashes
identical to the staged one. Output in `evidence/reviewer-probe.stdout`.

| Probe | Question | Measured result |
|---|---|---|
| **R1** | Is `is_for` directory identity or handle identity? | **Handle identity.** A second `RetainedDirectory` opened on the *same inode* is rejected. |
| **R2** | Is a receipt exclusive or one-shot? | **Neither.** Two receipts for one handle are alive simultaneously, both `is_for == true`, neither invalidated. Nothing is consumed. |
| **R3** | Can a receipt be obtained after the opened name was taken over? | **Yes.** Renamed the directory away, created a different directory at the original path, then confirmed: receipt granted for the original inode while the name resolves elsewhere. Reachable publicly, so it is not an artefact of the private seam. |
| **R4** | What happens for a directory that is unlinked from the namespace? | **nlink after `rmdir` = 2** (not 0); `is_reachable()` = `Ok(false)`; `confirm_directory_barrier()` = **`Ok(FullFlush)`**. |
| **R5** | Which primitive actually completes on this lane? | **`FullFlush`** on the pinned APFS `TMPDIR`. |
| **R6** | Is the confirm-time kind guard publicly reachable? | **No.** `from_retained_handle` refuses a regular file first (`InvalidInput`, "retained root is not a directory"). |
| **R7** | Does the receipt satisfy the `T: Debug` bound ordinary error assertions need? | **No.** `confirm_directory_barrier().unwrap_err()` fails to compile: `` `DirectoryBarrierReceipt<'_>` doesn't implement `Debug` ``. Compiler output retained in `evidence/reviewer-probe-r7.stderr`; the probe file was removed afterwards. |

**R4 is the load-bearing one.** It converts the author's caveat — "a positive link count does not
establish attachment, especially on macOS" — from an assertion into a measurement: on this lane the
`nlink() == 0` guard is *inert* for the unlink case, and a receipt is issued for a directory with no
name anywhere in the filesystem. The disclaimer is therefore accurate, not conservative boilerplate.

---

## 7. Do the documented claims match actual behaviour?

| Claim (doc comment / README) | Verdict | Basis |
|---|---|---|
| "Records the barrier primitive completed on one exact retained directory" | **matches** | code + R5 |
| "The borrow keeps that handle alive" | **matches** | shared borrow; borrow checking prevents move/drop |
| "Exact borrowed owner identity, not equality of caller-supplied pathnames" | **matches, and is narrower than it reads** | R1: also not directory identity — see O‑1 |
| "It proves neither a parent/name binding, recursive child/file durability, custody, profile qualification nor authority" | **matches** | no path handling exists in the added code; R3, R4 |
| "F_FULLFSYNC is tried once; only named unsupported errors allow the existing fsync fallback" | **matches** | reuses the unchanged `NATIVE_PUBLICATION.sync_directory`; existing fallback test still passes |
| "The receipt exposes which completed" | **matches in the source; under-asserted in the shipped tests** | see RF‑1 |
| "does not flush file contents, confirm this directory's name in its parent, recurse, re-resolve a path or create installation authority" | **matches** | R3, R4, no callers |
| "A failure returns no receipt and is never retried here" | **matches** | one `flush` call; author test 2 pins `calls == 1` for EIO/EINTR/EACCES |
| "No unsupported profile is upgraded by a successful syscall" | **matches** | disclaimer only; nothing in the code records a profile |
| "The caller owes original name/custody/filesystem checks before and after, including on error, and exclusion through consumption" | **matches, and is load-bearing** | R2 shows the receipt supplies no exclusion at all |
| Descriptor samples "bracket attempt even error" | **matches, with undocumented error precedence** | see RF‑3 |
| "No production caller switched" | **matches** | repository-wide search: zero callers |
| "588 non-lock unchanged, 2 writes" | **matches** | my own stage run and my own `git ls-files` delta |

No claim was found to overstate what the code does. Every gap below is a gap in precision or in the
shipped evidence.

---

## 8. Required findings — three, all non-blocking

These do not block acceptance of the source unit. They should be carried into any assent and fixed,
in keeping with the project's zero-deferral standard.

### RF‑1 — the macOS primitive assertion is vacuous, and the test name over-claims

`directory_barrier_receipt_binds_original_owner_and_reports_actual_primitive` asserts, on macOS:

```rust
assert!(matches!(receipt.barrier(), DirectoryBarrier::Fsync | DirectoryBarrier::FullFlush));
```

`DirectoryBarrier` has exactly two variants and is not `#[non_exhaustive]`, so this pattern is
irrefutable: **the assertion cannot fail.** Only the Linux arm (`assert_eq!(…, Fsync)`) discriminates,
and Linux is not run. On the only lane that executes, the test backs its "binds original owner" half
and nothing of its "reports actual primitive" half — while the test name asserts both, and the name
travels into the frozen evidence as a claim.

*Required:* assert the value actually expected on the macOS lane (my R5 measures `FullFlush`), or
remove the claim from the test name. A test whose name promises more than its body checks is precisely
the kind of evidence debt that should not enter a selected unit.

### RF‑2 — the `nlink() == 0` guard is inert on macOS, and the doc does not name the remedy

R4 measures `nlink == 2` for a directory held open after `rmdir`, so on this platform the guard never
fires for the case it reads as addressing, and a receipt is granted for an unlinked directory. The
inline comment predicts this; the **public** documentation on `confirm_directory_barrier` does not, and
it tells the caller it "owes original name/custody/filesystem checks" without naming what is available.

The crate already carries a stronger, selected, public observation — `RetainedDirectory::is_reachable`,
whose own doc records the same macOS behaviour and which answered `Ok(false)` in exactly the case the
barrier accepted.

*Required:* state on the public method that the link-count guard is best-effort and platform-asymmetric
(it catches the Linux-style case, not the macOS one), and name `is_reachable()` as the existing
observation a semantic owner must call itself if it wants reachability. This is a disclosure change
only; do **not** wire `is_reachable` into the barrier, which would silently widen a primitive.

### RF‑3 — error precedence after a failed barrier is undocumented

`attempted` is held while `after` is sampled, and `attempted?` is applied last. Two consequences that
the documentation does not state:

1. If the flush fails **and** the post-sample condition fails, the caller receives
   `InvalidData: "retained directory changed"` and the barrier's own `io::Error` is dropped.
2. If the flush fails **and** the post `metadata()` call itself errors, the caller receives the
   metadata error and the barrier error is dropped.

Both fail closed, so neither is unsafe, and preferring the stronger signal is defensible. But the same
doc says "semantic owners must stop the act", and an owner that must *classify* the failure — transient
versus durable, medium error versus descriptor invalidity — cannot do so when the underlying error has
been replaced without notice.

*Required:* document which error wins and why, or surface both.

---

## 9. Observations — recorded, not required

- **O‑1.** `is_for` is handle-object identity, not directory identity (R1). An owner holding two
  handles on one directory gets `false`. The failure direction is safe, and it is narrower than
  "not equality of caller-supplied pathnames" suggests. Worth one sentence in the doc.
- **O‑2.** Receipts are neither exclusive nor one-shot (R2): `&self` permits any number of live
  receipts per handle, and they are indistinguishable. A receipt cannot serve as a capability token.
  The doc correctly places exclusion on the caller; the property is just not obvious from the type.
- **O‑3.** The receipt has no `Debug`, so `…unwrap_err()` on the result does not compile (R7). The
  cause is legitimate — `RetainedDirectory` itself has no `Debug`, so a derive is impossible — but
  `NewFileReceipt` and `ExistingFileReceipt` both derive it, so downstream test code will hit an
  inconsistency. A manual `impl Debug` printing only the barrier variant would remove it.
- **O‑4.** The confirm-time kind guard is unreachable through the public API (R6); the author's fifth
  test covers defence in depth behind the private seam, which is worth having but is not a public
  failure mode.
- **O‑5.** The post-check is thinner than it reads. For an owned descriptor, `dev`/`ino` cannot
  change and `is_dir` cannot change, so those three arms are unfalsifiable; only the `nlink` arm can
  differ between the two samples, and per RF‑2 only on Linux. The bracket costs two `fstat` calls per
  barrier and, on macOS, detects nothing today.
- **O‑6.** No new test drives `confirm_directory_barrier` through the **fsync fallback** arm. Fallback
  coverage is inherited from two pre-existing tests that reach the private helper directly or use a
  socket descriptor. R5 confirms `FullFlush` is what actually runs on the lane, so the new API's
  fallback claim rests entirely on the unchanged helper.
- **O‑7.** Fixtures use `std::env::temp_dir()`, i.e. the pinned `TMPDIR` volume — not a prospective
  installation-root volume. Whatever the barrier does on another filesystem is unmeasured here.
- **O‑8.** The receipt is unforgeable outside the crate, but private fields are visible to descendant
  modules of `filesystem` (`path_binding`, `directory_binding`, `directory_volume`, …), any of which
  could construct one directly. None does today. Worth knowing before the type is treated as a
  witness in a security argument.

---

## 10. The narrower limitation, stated explicitly

The request asked me to critique any narrower limitation rather than let it pass. Three:

**It is the barrier half only.** My owner390 review recorded that "the product today has exclusive
no-replace publication for regular files only (`publish_new_regular`), with no directory-publication
primitive and no directory-barrier receipt type, so two native capabilities remain unimplemented."
393 supplies the **second** of those two. The first does not exist: I searched the staged tree and the
exclusive no-replace rename (`renameatx_np RENAME_EXCL` / `renameat2 RENAME_NOREPLACE`) is wired only
through `NativeNewPublication` for regular files, and no production code path creates a directory at
all — `create_dir` appears exclusively in tests. Root should not read 393 as closing the 390 TCB gap;
it closes one named half of it.

**It does not touch RF‑2 of owner390.** The undefined base case in the directory-publication durability
recursion — "…continue up to the already admitted durable ancestor" with nothing naming what first
establishes one — is a law-level hole. A primitive that flushes one already-open directory cannot
supply a base case, and nothing here should be read as progress on it.

**A receipt is weaker than the sentence a caller will want to write.** After R2, R3 and R4, what a
receipt licenses is: *this exact in-memory handle had the named barrier primitive applied to its inode,
and the inode was still a directory with a non-zero link count immediately afterwards on a platform
where that is not evidence of attachment.* It does not say the directory is named, reachable,
contained by the parent the caller meant, exclusively held, or durable as a namespace entry. That is
what the documentation says too — the risk is not misrepresentation, it is a later caller reading
"directory barrier receipt" as "the directory is durably published". RF‑2 exists to make that harder.

I record, without endorsing, that the README's framing is correct on this point: exposing this
platform primitive adopts none of the unselected 390/392 initialization law.

---

## 11. Limits

- **Level:** source reading, formal-pin verification, native test replay and public-API probing on
  macOS arm64 development only.
- **Not qualified:** Linux execution, power-loss and crash durability, filesystems other than the
  pinned APFS `TMPDIR` volume, custody, actor identity, native profiles, GC, release.
- **Not re-reviewed on their merits:** runtime30, registry-v2, inventory58 — only their currency,
  pins and selection status.
- **Unselected references remain unselected:** S9.3, `docs/v2/architecture/store-instance-lineage.v1.json`,
  the 390 atomic-root-publication proposal, the 392 audit's policy choices, and
  `host-foundation-completion.v2.md` / `reference-architecture.v2.md`.
- **Replay caveat:** the three replayed checks are the author's own tests, so they establish
  reproducibility and internal consistency. The independent part is §3 (delta derived from
  `git ls-files`, not from the author's manifest), the 110→115 test count, and the R1–R7 probes.
- The author's retained preparation-failure note was read and corroborated: the initial preparation's
  final textual assertion expected a different derive order and the enum already derived `Copy`. That
  is a preparation-script assertion, not a native compile or test failure, and no enum change was made
  — the staged enum still reads `#[derive(Debug, Clone, Copy, PartialEq, Eq)]`.

---

## 12. Attestation

Read-only against live, frozen, history, product and lock. No architecture, product, frozen, history
or lock byte was edited. No commit, no push. All writing went into this review directory; extraction
and both build trees are review-local. No root select script was run. The author's binary and target
directory were not reused. Running `cargo` inside the product repository to list its tests left that
repository clean (`git status --porcelain` empty, verified after).

This grants no root assent, no formal selection, no native installation, no current authority, no
S9.3 adoption, no M2 completion and no release qualification. Integration of runtime31 requires this
review, root's assent and prospective validation. The runtime30 / source389 acceptance and the
owner390 NEEDS-CHANGES verdict are untouched, and no earlier report was rewritten.

Reviewer: Claude Opus 5 (1M context).
