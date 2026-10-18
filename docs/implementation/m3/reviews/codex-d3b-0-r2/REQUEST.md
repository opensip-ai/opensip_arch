# Review request: D3B-0-r2 (the macOS descendant mechanisms; M3-D r5 items 4, 8, 16 and 18, D3b sub-unit D3b-0), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3b-0-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing, diffing and Git queries;
  - read-only inspection of system library bytes, as in round 1;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3b-0-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7915 bytes, SHA-256 `c1fd5c30f6fafc05d2b1fc5cb75633f436fa3f72d0def4c4279df9388fd517f4`, 35 members. Rehash every member.
  - **Round 1's package stays as history, unchanged:** `../d3b-0-r1/` and `d3b-0-r1-subject.json` (`ae101c34…`).
  - **The round-1 review files** are copied byte-identical into `docs/implementation/m3/reviews/codex-d3b-0-r1/` and pinned by `source.json`.
- **The candidate base and lane base:** product main `f16f50d4022c013055027072fcc7972afeb0c96b`, as `source.json` and the lane's `checks.json` record.
  - **Before the lane:** the candidate was re-applied by hand onto `6fab8fc`. That was needed because CI-2 had appended to `crates/platform/src/lib.rs`, a candidate path; `process.rs` and `process_tests.rs` were byte-identical across it. SCOPE records the attempt that refused the automatic move.
  - **During the lane:** the runner moved the worktree inside the lock from `6fab8fc` to `f16f50d`. That move's changes are components files only (`evidence/d3b0-checks-r2/rebased.json`).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3b0`, detached at `f16f50d`. It holds the exact bytes `product-map.json` lists: 3 files in `crates/platform`, none new.
- **Main may move while you review.** Judge against `f16f50d`. The integrate script refuses if main changes a candidate path.

## Round 1

- **Review:** `/tmp/opensip-implementation/reviews/codex-d3b-0-r1/` (REVIEW.md and review.json): REQUIRED-FINDINGS, D3B0-R1-RF-1 and NBO-1. Q1 and Q2 were accepted.
- **The disposition** (SCOPE's "Round 2" table):

| Item | Round 1 | Disposition in r2 |
| --- | --- | --- |
| D3B0-R1-RF-1 | libproc listing failures read as `Complete(empty)` | **Fixed for every libproc and `kill` call.**<br>**The listings.** `native_listing` clears errno immediately before each listing call. Zero with errno set is `Io`, keeping the call name and errno; zero with errno clear is a real empty list; a negative return is `Io`. It covers `child_processes`, `group_members_bounded` and D1a's `group_members`.<br>**`proc_pidinfo`.** errno is cleared first. `None` is given only for `ESRCH`. A zero or short return with no errno is `Io`.<br>**`proc_pid_rusage` and `kill`** return -1 with errno and are unchanged (probed).<br>**Unchanged:** the single capacity-plus-one buffer and the count-against-bytes distinction.<br>**Controls:**<br>• real `ENOMEM` zero returns, forced by one-byte or ten-byte size seams, on all three listings and on `proc_pidinfo`;<br>• a stale `EPERM` before two real empty listings;<br>• a stale `ESRCH` before the forced identity failure.<br>**Mutations:** `listing-error-read-as-empty`, `listing-errno-not-cleared` and `identity-error-read-as-gone`. |
| D3B0-R1-NBO-1 | The rebase record was not archived under its attempt | **Fixed.** r1 attempt 2's record is archived at `d3b-0-r2/evidence/r1-lane-attempt2/rebased.json`, and SCOPE names attempt 2 as the attempt that moved the worktree. The r2 lane of record's own move is in its `rebased.json`. |
| Q1, Q2 | Accepted | Kept. Their D3b-1 obligations are recorded in SCOPE. |

## Also new in r2

SCOPE has a **"Self-review" section**: the lead's pre-submission checklist of Codex's recurring findings, item by item. It includes an explicit list of untested paths, each with its reason:
- a negative return from a listing wrapper;
- a zero or short `proc_pidinfo` return with no errno, so its errno clear has no catchable mutation;
- a non-`ESRCH` `kill` failure;
- the other targets.

## What to review

1. **RF-1 fixed as required, on every native call.**
   - Is the errno discipline correct and complete, with no stale errno ever read?
   - Is every failure kept as `Io` with its call and errno?
   - Are the seams real native failures?
   - Do the controls and the three new mutations prove it?
2. **NBO-1 fixed:** the archived record, and the corrected attempt history.
3. **No regression.**
   - Round 1's assessment still holds: the buffers, `kill_descendant`'s refusals and equality-only identity, the zombie case and RF-4.
   - The lane of record:
     - platform 343 to 352, with equal failure sets (none) and nine new tests;
     - all rows;
     - eleven mutations, each caught by a test.
4. **The rebases.** Is the hand re-application onto `6fab8fc` faithful, and the in-lock move to `f16f50d` disjoint?
5. **The self-review.** Are its "not applicable" entries and the untested-path disclosure accurate?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3B0-R2-RF-n` / `D3B0-R2-NBO-n`.
