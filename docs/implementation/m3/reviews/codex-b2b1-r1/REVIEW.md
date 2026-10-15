# B2-B1-r1 review

**Verdict: ACCEPT-UNIT.** No required findings. Two nonblocking scope-metadata observations below.

## Subject and scope verification

Rehashed the 6,429-byte subject manifest, SHA-256 `85da7c59ebce7b0b05edd20bbdc64af4c2b69f5d23fe37fcd134c6ee7a1f15f7`, and all 29 members. All sizes and hashes match. Verified the five candidate files against both their archived bytes and the candidate worktree, and every parent pin against product-base Git bytes. The worktree diff contains exactly the five mapped existing paths and no new paths.

Product and candidate HEADs are `7d0ac1b59df9a099a4d8edc05d8600f46dd63923`; architecture HEAD is `4fbc0c65011af58948f01986c79061443598a798`. Product main is clean, and architecture tracked state is clean. The existing untracked E2s directory was left uninspected and untouched. Source authority pins and the product-lock pin match. Inventory v191 and contract successor count 164 are unchanged.

## Implementation assessment

`WorkLedger::discovery_profile()` supplies exactly 2^20 objects, 2^21 edges and 2^30 bytes. The ordinary cap constants and existing constructors retain their behavior. Independently compared the complete `with_limits` method against base: byte-identical. The new constructor initializes the same failure/prepayment/settlement state as an ordinary fresh ledger; charge/latch behavior is unchanged. Only this new constructor permits limits above the ordinary caps. Creating the ledger once after handoff and retaining it across failures remains B2-b3's owner obligation; absence of Clone/Default alone cannot enforce it.

`observe_child` uses the existing bounded component grammar, one `fstatat` with `AT_SYMLINK_NOFOLLOW`, and no open/create/follow operation. It treats only ENOENT as absence and returns every other error. It initializes and reads stat storage only after syscall success. Child kind is derived from S_IFMT. `from_stat` maps the same device, inode, mode, uid/gid, link count, size, modified/changed timestamps and flags as the existing macOS `from_metadata` conversion.

`ChildObservation::matches` requires device, inode and kind equality; Absent always fails. This supplies the planned observation/open identity comparison, without claiming custody, stability or admission. B2-b3 must still open no-follow and apply the comparison before use. The accounted method reserves the unchanged single-status-read cost before the syscall through the existing work scope.

The filesystem types, methods, conversion and exports are macOS-only. The discovery ledger constructor and tests are portable: see NBO-1. No production caller, walker, custody judgment or environment read is added. The added public Rust items expose platform data/operations rather than operational authority.

LD-B2B1-1 is sound: no path is added and all five paths are already inventoried. Their existing adapter, service, public-api and test roles cover these changes; an additive inventory successor is unnecessary.

## Tests and evidence

Inspected the four observation tests and two profile tests. They cover directory/file/symlink/FIFO kinds, absence, invalid names, unchanged parent/child timestamps, unchanged positive matches, same-kind directory and atomic-file replacements, kind mismatch, Absent mismatch and exact accounted charge. Profile controls exercise exact caps, one beyond, latch persistence and rejection of raised limits through with_limits. The timestamp and identity tests are ordinary scratch-fixture evidence, not custody qualification.

Ran only the explicitly permitted operability source census against the candidate worktree: **passed, 114 rows, no findings**.

Reviewed the remaining evidence without running its driver, compiler or tests:

- Platform tests run serially for base and candidate alike, as declared. Raw archived logs reconcile with six suites and 287 → 293 passing tests, zero failures.
- Security has the same 14 named failures and 1078 passing tests on both trees. Host has the same eight named failures and 336 passing tests on both. Suite counts agree. Equal failure sets do not mean these suites are fully green.
- The driver and checks record locked/offline all-targets Clippy for platform, security and host with warnings denied; the archived log ends successfully.
- All five edited Rust files are classified base-clean and candidate-clean, with no formatting exclusions.
- Environment-exception and configuration-table checks are recorded passing; they were not rerun during this review.
- Parsed design-verification evidence is passing, selecting inventory v191 and 164 successors without qualification.
- All eight mutation logs contain the exact named failing tests reported by controls.json. Each reached test failures rather than compilation failure. The profile-cap, inode, absence, kind, no-follow and accounting mutations were all caught.

## Nonblocking observations

**NBO-1:** SCOPE.md's blanket macOS-only claim is too broad. Only the filesystem additions are gated; the ledger constructor, its constants and tests are portable. Consequently `macosOnlyLinuxUnchanged` is false as literally requested. This is a scope-description correction, not a functional blocker: existing Linux behavior is preserved while the portable ledger API is extended.

**NBO-2:** source.json marks publicApiAdded/newPublicCode false although public Rust platform methods and types are added. Correct those flags or explicitly define them as referring only to user-facing operational APIs. The new Rust surface is already part of the reviewed code; no operational caller or new custody authority is implied.

## Boundaries and remaining work

Acceptance is for this exact platform sub-unit. Lead assent, architecture publication and the product code commit remain subsequent steps. B2-b2/B2-b3 still own the core, walker, custody and invocation-ledger ownership; B2-b4 owns the T2 census and all-entry margin gate. Neither qualification nor the entire plan is complete.

Used permitted read-only inspection, hashing, JSON parsing, Git queries and the source census. Ran no Cargo, rustc, tests, builds or lane; used no network, other panes or delegation; accessed no private fixture, installation directory, signing keys, held trees or T2 held-out entry. Neither repository, worktree, stage nor control files were edited. Wrote only `REVIEW.md` and `review.json` in this directory.
