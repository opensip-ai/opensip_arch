Grok review: X2b-2 r2, the Git tracking observation (law X2 r8 item 6a and item 1's Git premise scope), with inventory v99. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-git-tracking-x2b2-r2. If you build, use a CARGO_TARGET_DIR under that directory. Never run git against a real repository except read-only against the worktree below; the tests build their own scratch repositories.

**This supersedes r1.** The r1 request (`reviews/grok-git-tracking-x2b2-r1/`, v98 on v96 at fc7dce7 under X2 r7) was never reviewed. X3b-1b has since integrated, so this r2 is rebased onto 46b1d60 with inventory v99 on v97, and pins X2 r8. Review r2 only. **It waits on X2 r8's acceptance.**

Law: `docs/implementation/m2/project-root-x2/PROPOSAL.md` r8 (pinned in hashes.txt), queued for your review separately. r8 answers your r7 RF-1 and changes only item 1's wording: the system sources are outside the no-follow admission rule, with no premise or H-volume constraint, and are refused only as item 6a says. Item 6a is unchanged from r7, so the code needed no change for r8. The r7 change came from implementing this unit: under r5, item 1's custody rule for the system Git configuration sources refused every repository on a stock Mac (`/` is on the sealed system volume and omits its ACL, `/etc` is a link, `/opt/homebrew/etc` is user-owned and admin-writable).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2b2`, based on 46b1d60 (X3b-1b integrated, inventory v97 selected). Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
- **Arch:** v99 (parent v97), `git-tracking-inventory-v99-subject.json` and `git-tracking-inventory-v99/`. inventory98 (the r7 build on v96) and inventory95 (the r5 build on v93) are superseded and left unchanged. The product files are byte-identical to r1's; v99's two rows differ from v98's only in naming law X2 r8.

## What it does

The code is in `custody/git_tracking.rs`.
- **Pure parts.**
  - `parse_config` / `check_config`: the closed parse (sections, quoted subsections, `key = value` or a bare key, comments, quoted values with `\\ \" \n \t \b`), refusing continuations, CR, NUL, legacy `[a.b]` headers, a key before any section and anything over 64 KiB; then include/includeIf, `extensions.*`, `core.worktree`, a `core.bare` that is not false, a format version other than "0", and `core.precomposeunicode` false.
  - `check_environment`: any `GIT_*`, `XDG_CONFIG_HOME`, or a `HOME` other than H's spelling.
  - `decode_index`: versions 2, 3 and 4 exactly, with the trailing SHA-1 (a local implementation), extended flags, padding, v4 prefix compression, the name-length rule, extensions skipped by size, and `link`, `sdir` and unknown lowercase extensions refused.
  - `marker_path` (ASCII only) and `tracks` (ASCII case-insensitive; gitlinks never match).
- **`observe_tracking`.** In order: the environment; positive no-follow lookups of `.git`, `.hg`, `.svn` and `.jj` at every chain directory up to `/`; for every enclosing `.git` its volume and custody, positive absence of `commondir` and `config.worktree`, the required config and the index; the global sources under H with custody (owned by the invoking user); then the system sources.
- **System sources (item 6a, r7, unchanged in r8).** Each fixed path is opened with a plain `open` that follows links (`O_NONBLOCK`, so a FIFO cannot block), charged, and required to be regular. `ENOENT` anywhere on the path is absence. Otherwise the file is read capped at 64 KiB and goes through the same parse and refusals. No custody is judged. A non-regular file is `system-source-not-regular`; permission, I/O or a non-directory component is `system-source-unreadable`; over the cap is `config-oversized`. The evidence is the bytes read.
- **`recheck_tracking`.** A fresh pass whose evidence (metadata samples, absences, and the system sources' bytes) must equal the original; otherwise `evidence-changed`. For a system source this is the law's re-read: the same absence or the same bytes.
- **Rows.** `marker-tracked` and `vcs-unsupported` are root custody; host I/O is the I/O row.
- **`ReadSession::observe_project_tracking`.** Runs the observation and its recheck on the session ledger, then a full session recheck, and latches on any refusal. Production passes the process environment and `SYSTEM_SOURCES`; `observe_project_tracking_with` takes them as arguments.
- **Supporting edits.** Platform: `observe_descriptor_metadata`, `open_fixed_regular_following` and its cost, `RetainedDirectoryPath::directory_at`. Security: `ProjectChain::path` and `home_index`, `ProjectChainPolicy::home_filesystem`, and the module declaration.

## Judgment calls: please rule on each

1. **Extended flags on version 4.** Version 4 also carries the extended-flags field, as Git's documentation says for "version 3 or later". The law names only version 3.
2. **Custody failures are `vcs-unsupported`.** A custody failure of `.git`, config, index or a global source is `vcs-unsupported`, not a root-custody subject, because the law groups unreadable or unsupported VCS evidence that way.
3. **Every enclosing repository needs its config.** Its absence refuses at every level, not only the nearest.
4. **Index custody** is S3 config-file custody: owner the invoking user or root, no group or other write, one link, at most 4 MiB.
5. **Global sources** must be owned by the invoking user.
6. **The recheck** is a full re-observation compared for equality, not a per-object comparison.
7. **System-source I/O is `vcs-unsupported`, not host I/O.** Item 6a says a source that exists but cannot be read refuses as `vcs-unsupported`, so every non-`ENOENT` open or read failure maps there (a budget failure is still the budget). `ENOTDIR` (a regular file in the middle of the path) is treated as unreadable, not absent, because the law names only `ENOENT`. A dangling link yields `ENOENT` and is absence.
8. **Parse before recording.** A system source's bytes join the evidence only after they pass the parse; a refusal stops the pass anyway.
9. **Labels.** Evidence is labelled by path; global sources use `~/...`; system sources use their fixed path.
10. **The gitlink test.** Git will not hold a gitlink and a path below it in one index, so the "does not clear" case removes the gitlink before adding the outer marker entry. The "neither matches" rule is also tested directly through `tracks`.
11. **Environment injection.** `observe_project_tracking_with` lets a crate-internal caller pass the environment and source list. The real-layout test runs `observe_tracking` with the real `SYSTEM_SOURCES` and a clean environment, not the production entry, because the test process's own `HOME` is not the scratch H and the entry would refuse on the environment.
12. **The platform open.** `open_fixed_regular_following` is a new platform primitive that follows links by design. It proves no custody and its doc comment limits it to evidence that can only refuse.

## Tests

`custody/git_tracking_tests.rs`, 23 tests. Git runs with a cleared environment, a separate scratch `HOME` and `GIT_CONFIG_NOSYSTEM=1`. Real system paths are only probed read-only.
- The pure parts: FIPS SHA-1 vectors, config parse and every refusal, the environment, synthetic indexes of every version and refusal, the marker match.
- Real git indexes of versions 2, 3 and 4 decoded identically to `git ls-files -s`.
- Native, on scratch repositories: no repository, untracked, tracked in every version and after the file is deleted, a case variant, outer repositories and gitlinks, a subdirectory root, every layout refusal, global sources, the environment.
- **System sources (new since r5):** absence at the leaf, at an intermediate component and through a dangling link; a world-writable source still read (no custody); links followed at the leaf and on the path (an `etc -> private/etc` layout); exactly the cap read and one byte over refused; every config refusal through a system source; a directory and a FIFO refused as not regular; permission and a path through a file refused as unreadable; the recheck as a re-read (same absence, same bytes rewritten as a new file pass; new, changed or removed bytes refuse); the read charged and a short ledger refused.
- **This host's real layout:** an ordinary scratch clone is admitted (`Untracked { repositories: 1 }`) with the real `SYSTEM_SOURCES`; each real source is either absent or recorded with exactly the bytes a link-following read sees; the recheck agrees.

## Checks

- X2b-2 tests 23/23. Full workspace, one run at 46b1d60: 1326 passed, 0 failed, 3 ignored. Clippy `-D warnings` and fmt are clean.
- `check_package_edges --lane host` against v99 passes.
- verify_scratch (v99 appended over the real lock at 46b1d60) passes: 66 inventory successors, 71 contract successors, 16 inheritance rows, v99 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused. `build_v99.py` reruns produce the same bytes.

## Decide

- Does X2b-2 implement X2 r8 item 6a, and item 1's Git scope, exactly? In particular, are the system sources read as r8 says, with no custody and nothing they can admit?
- Rule on the judgment calls, in particular 2, 7 and 12.
- Is v99 right on v97?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256" (the sha256 of git-tracking-inventory-v99-subject.json);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v99, parent (the v97 pin), successorRecord}.

Write REVIEW.md and review.json. Do not commit.

Lead note on ordering: this r2 is rebuilt on v97 (X3b-1b, integrated at 46b1d60) and supersedes the unreviewed r1. Review waits on X2 r8's acceptance.
