# X2b-2 r2 — Git tracking observation

Implementation review of worktree `/Users/sb/code/opensip-ai/opensip-x2b2` at `46b1d60faef4ca004170ae3cbcff7c9b29ad3f7c`, with inventory v99 on v97. The OpenSIP support directory is absent. Product files match `hashes.txt`. `product.diff` is 91094 bytes, sha256 `b9000dcc153205ed15d89450a2cf283dbbd85e5906e17b528e005410337b1f11`, eight files, 2002 insertions. Law is the pinned X2 r8 text, `PROPOSAL-r8.md`, 39036 bytes, sha256 `c31d9a020f91650fb1c85f6697bffac1902bf3607d501e5821f48cd8c4b301b5`. The live `PROPOSAL.md` adds only the acceptance sentence.

Judged against X2 r8 items 1 and 6a and item 8. Replay: `opensip-security` lib tests filtered to `git_tracking`, 23 passed. `cargo clippy --locked --offline -p opensip-security -p opensip-platform --lib -- -D warnings` passed. `verify_projection.py` against the real lock: 16 rows, 83 corruptions refused. The workspace suite and `verify_scratch` were not replayed. The cargo target was removed.

## Law

Item 6a and item 1's Git scope are implemented. The walk is positive no-follow lookups of `.git`, `.hg`, `.svn` and `.jj` on every retained directory from the root up to `/`. Another VCS, a `.git` that is not a directory, and a `.git` at or above H or off H's volume refuse as `vcs-unsupported`. Every enclosing repository is examined: `commondir` and `config.worktree` must be absent, the repository `config` is required, and the index is read no-follow under custody, capped at 4 MiB, with the trailing SHA-1 checked. The marker path is the root relative to that `.git` parent plus `.opensip/project-id.v1`, ASCII only, matched ASCII-case-insensitively. A gitlink (mode 160000) is not a match. No marker on the chain is `NoRepository`.

System sources are the five fixed paths. `open_fixed_regular_following` opens each with `O_RDONLY|O_CLOEXEC|O_NONBLOCK` and no `O_NOFOLLOW`, then requires a regular file. `ENOENT` is absence, including a dangling link. Anything else that stops the read — permission, I/O, a non-regular file, `ENOTDIR`, or past 64 KiB — is `vcs-unsupported`. No custody, premise, or H-volume check runs. The bytes are recorded only after the closed parse accepts them. They never select a path or clear a marker. Global and repository sources stay no-follow, under the premise, on H's volume. Global objects must be owned by the invoking user.

`ReadSession::observe_project_tracking` passes the process environment and `SYSTEM_SOURCES`, runs the observation and the recheck on the session ledger, then the session recheck, and latches on refusal. `row()` is `marker-tracked` or `vcs-unsupported` on `PROJECT.ROOT_CUSTODY_REFUSED`, and host I/O for `TrackingRefusal::Io`. Budget stays the budget failure.

## Judgment calls

1. Version 4 carries the extended-flags field when bit 0x4000 is set. Item 6a says entries follow Git's index-format documentation, which defines that field for version 3 or later, and it names version 2 as the version that refuses the flag. Accept.
2. A custody failure of `.git`, `config`, the index, or a global source is `vcs-unsupported`. Item 8 gives item 6a those two subjects. Host I/O and budget stay their own failures. Accept.
3. A missing repository `config` refuses at every enclosing repository. Accept.
4. Index custody is S3 configuration-file custody: owner the invoking user or root, the existing group-write rule, one link, at most 4 MiB, on H's volume, under the premise. Accept.
5. Global files and the `.config` directories must be owned by the invoking user. Root ownership fails that check. Accept.
6. The recheck is a second full pass compared for equality, which includes the metadata samples, the absences, and the system sources' bytes. Accept.
7. System-source failures other than `ENOENT` are `vcs-unsupported`, including I/O. `ENOTDIR` is unreadable. A dangling link is `ENOENT` and is absence. Accept.
8. A system source's bytes join the evidence only after the parse accepts them. Accept.
9. Evidence labels are the chain spelling, `~/...` for global sources, and the fixed path for system sources. Accept.
10. The gitlink fixture removes the gitlink before adding the marker entry, and `tracks` tests the rule directly. Accept.
11. `observe_project_tracking_with` is the crate-internal seam. Production passes the process environment and `SYSTEM_SOURCES`. Accept.
12. `open_fixed_regular_following` follows links, proves no custody, and its comment limits it to evidence that can only refuse. The caller charges the open before it runs. Accept.

## Inventory v99

v99 is 343156 bytes, sha256 `990bed9a4f1413af7510b467aadf28cb6a7fa33319a3c592410ef8cc3431b5e3`. Parent v97 is 340214 bytes, sha256 `5e4269c50e07590c1cc8e56d1cf302f51f227e034f71fb3395f5467a174848a7`. All 772 inherited rows are equal by value. Packages and pending decisions are unchanged. The two added rows are `git_tracking.rs` and `git_tracking_tests.rs`, and their descriptions match the code and the tests. The subject manifest is `git-tracking-inventory-v99-subject.json`, sha256 `ccc666f8ab11607661897458b95dc1c7844d50fb5eea2a510eb17aaf37540f56`.

## Verdict

ACCEPT-UNIT. Inventory v99 ACCEPT.
