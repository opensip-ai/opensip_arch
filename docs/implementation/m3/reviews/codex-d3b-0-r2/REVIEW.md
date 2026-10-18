# D3b-0 r2 review

**Verdict: ACCEPT-UNIT.** No required findings or non-blocking observations. D3B0-R1-RF-1 and D3B0-R1-NBO-1 are resolved.

## Subject and provenance

Verified the 7,915-byte subject manifest, SHA-256 `c1fd5c30f6fafc05d2b1fc5cb75633f436fa3f72d0def4c4279df9388fd517f4`, and all 35 members against their sizes and hashes. Authority/history pins match, and the archived round-1 request and review files are byte-identical to the originals. All three product-map candidate and archive pins match the worktree; parent pins match Git at the declared base `f16f50d4022c013055027072fcc7972afeb0c96b`. Exactly lib.rs, process.rs and process_tests.rs are edited; there are no new paths.

## RF-1 — resolved

`native_listing` clears this thread's errno immediately before invoking its native closure and captures it immediately afterward. A negative result, or zero with errno set, returns LaunchError::Io with the call name and error. Zero with errno clear remains a legitimate empty listing. No intervening operation in the native closures can replace the call's errno.

This applies to child_processes, group_members_bounded and the retained group_members API. Child listings still interpret the return as a pid count; group listings interpret bytes divided by pid size. The bounded APIs retain checked capacity-plus-one arithmetic and a single buffer, returning Exceeded rather than truncating an over-capacity result.

`process_identity` independently clears errno before proc_pidinfo. Exact-size success constructs an identity; ESRCH with a nonpositive result alone gives None. Other native errors retain their call/errno. A zero or short result without errno becomes Io/InvalidData, not a missing process. The descendant kill path propagates identity failures before signalling; its own kill failure preserves fresh errno, except ESRCH's explicit Exited outcome. resident_bytes retains its existing -1/error convention.

The controls use real native calls: LISTING_BYTES changes only the supplied byte count to one, and IDENTITY_BYTES changes only the supplied size to ten. The functions do not inject return values or errno. Recorded controls require ENOMEM for all three listing paths and proc_pidinfo, preserve successful empty child/group listings despite stale EPERM, and prevent stale ESRCH from misclassifying identity failure. The listing-error-read-as-empty, listing-errno-not-cleared and identity-error-read-as-gone mutations all fail tests.

## NBO-1 and rebases — resolved

The round-1 attempt-2 move is now archived and pinned at evidence/r1-lane-attempt2/rebased.json. Git confirms its exact 274dccc-to-2ead5cf changed-path set, disjoint from this unit. SCOPE correctly distinguishes that attempt from the already-aligned final round-1 lane.

The hand reapplication preserves CI-2's component_tree declaration and this unit's export block. process.rs and process_tests.rs base bytes are unchanged across the relevant move onto 6fab8fc; comparison of the round packages shows the intended errno changes without unrelated edits. The lane-of-record rebase from 6fab8fc to f16f50d lists exactly the six components paths Git reports, all disjoint from the three platform candidate paths. Its record is included and hashed.

## Regression, prior rulings and self-review

The protected-target refusals still precede identity reads and signalling: root, pid <= 1, host and after-reap. Identity comparison remains pid/start-time equality only; pgid and relative start-time ordering do not decide eligibility. The older-than-root control and order-filter mutation retain RF-4's protection. Zombie ESRCH remains Exited without a signal. Sent still means kill returned success, not confirmed death; ancestry and the identity/send race remain caller policy and best effort.

Q1 remains ACCEPT: group_members may remain until D3b-1 moves the sampler/confirm callers to the bounded API and removes it. Its errno fix does not remove that obligation. Q2 remains ACCEPT: LaunchError::Io carries failed-call evidence instead of a KillOutcome::Failed variant, with D3b-1 responsible for its per-pid projection.

The self-review's ledger/feasibility, duration and schema-source exclusions are appropriate for these mechanisms. No persistent failure latch is needed: native failures return immediately, and a failed identity lookup prevents the subsequent kill. The disclosure accurately separates untested negative wrapper returns, short/zero proc_pidinfo returns without errno, non-ESRCH kill failures and other-target stubs. In particular, the forced ENOMEM identity control cannot prove the defensive errno-clear behavior for an unproducible no-errno short return; that limitation is stated rather than claimed covered.

## Validation and limits

Independently ran the permitted operability source command: passed, 114 rows, no findings. No native probe, compiler, Cargo, build, test or lane was run during this review.

The pinned lane records empty failure sets at base/candidate, platform 343/352 passing tests and nine new controls. All rows pass, including formatting of all three base-clean files, warning-denied all-targets Clippy, workspace all-targets check, nine focused tests, environment checks, unchanged census closure and verify_design (52 admission sources; no qualification). Each of the eleven mutation logs contains failing tests, not a compilation failure.

This accepts the macOS library mechanisms. D3b-1's walk, bounds, eligibility, confirm/report composition and error projection, D3b-2 cancellation, other-target implementation and production qualification remain outside this unit.

Only REVIEW.md and review.json were written. Neither repository, worktree nor control files were edited. No network, other panes or delegation was used. No forbidden fixture, installation, signing key, held tree, T2 store or cache was read.
