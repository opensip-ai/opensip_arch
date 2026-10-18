# D3b-0 r3 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations.

## Subject and provenance

Verified the 7,693-byte subject manifest at SHA-256 `9596a0fafd07020707c6073606209bac69e924222af1e946d857a337d690444c` and independently rehashed all 34 members; every size and digest matches. The accepted r2 manifest remains the pinned 7,915-byte subject at `c1fd5c30f6fafc05d2b1fc5cb75633f436fa3f72d0def4c4279df9388fd517f4`; its three archived product files and accepted review match their pins. The r3 authority, prior-round and product-lock pins also match.

The candidate worktree is detached at `4e475c753002d21ed99e0d53e64218e55af0cb1f`, and product main is still at that commit. Exactly `crates/platform/src/lib.rs`, `process.rs` and `process_tests.rs` are edited. For every product-map row, the parent bytes match Git at the declared base, the candidate bytes match the worktree, and the archived bytes match the candidate.

## Q1 — ACCEPT

The rebase is faithful. Directly extracting the added and removed lines from the r2 diff against `f16f50d4022c013055027072fcc7972afeb0c96b` and the r3 diff against `4e475c753002d21ed99e0d53e64218e55af0cb1f` produces byte-identical sequences for both `process.rs` and `process_tests.rs`. Their independent numstats also remain identical: 323 additions/15 removals and 388 additions/2 removals, respectively.

The `lib.rs` re-export list is the exact union required by the rebase: it retains D3a-4's `TerminatingSignal` and adds only r2's seven names, `KillOutcome`, `Listing`, `ProcessIdentity`, `Protected`, `child_processes`, `group_members_bounded` and `process_identity`. D3a-4's `TerminatingSignal` implementation and `terminating_signals_map_by_their_libc_constants` test are preserved byte-for-byte from the new base. All three files have the same 4/3, 323/15 and 388/2 addition/removal counts as r2, and no fourth path is changed.

## Saved evidence and limits

The saved lane records 344 base passes and 353 candidate passes across the same seven suites, with zero failures, equal failure sets and nine new passing tests. Every listed row passed, including base-clean/candidate-clean formatting for all three files, warning-denied all-targets Clippy, workspace all-targets check, focused tests, environment exceptions, operability, unchanged census closure and verify-design. Each of the eleven mutation logs reaches the focused tests and records at least one test failure; none is merely a compilation failure. The r2 untested-path and scope disclosures remain applicable, and r3 accurately describes the conflict resolutions and takeover packaging.

No build, test, lane, network operation or fresh validation run was performed for this review. The saved lane evidence predates the takeover, as disclosed. Only `REVIEW.md` and `review.json` were written in the request directory.
