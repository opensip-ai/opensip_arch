# D5-0a release-waits implementation review

**Verdict: ACCEPT-UNIT**

**Subject manifest:** `e85379d04ba93e9e4c11505a1b0d1e32665a1af3715b754147c510a948e4341a`

The subject manifest and all 74 members rehash exactly. The product and architecture bases remain the pinned commits, all authority hashes match, and the current product base's `supervisor_tests.rs` is the mapped parent. The final worktree source, archived product source, product map, and archived diff agree at `098fe2c0aefca32cbf3276f0b62ad29e34508c4bcbbf7c67e690c5761b804dce`. The only tracked product change is `crates/components/src/supervisor_tests.rs`; the two disclosed untracked helper drafts are outside the subject.

## Prior findings

### D5-WAITS-PRE-R1-RF-1 — closed

`control_cap` now adds `term_to_kill`, drain, and reap after the largest trigger-side wait. For release provider and tool waits, the structural control checks the exact law-derived sums and separately proves that the cap is strictly greater than wall + TERM + reap by the positive drain margin. Direct, threaded, and tool drivers all use this corrected helper. The focused `missing-term-budget` mutation removes the sequential TERM term, compiles, fails the exact runtime control with `1811s != 1812s`, and the restored exact source passes.

### D5-WAITS-PRE-R1-RF-2 — closed

The final source adds exact `WaitExpired(WallClock)` evidence and preserves `Deadline` as first cause for each previously unproved path: all three incomplete-sample runs, both manual cancel controls, and both provider-snapshot-bound iterations. The shared tool-deadline helper continues to assert the same event for its callers. The corrected source passes all three complete candidate runs.

## Source and control assessment

`quick()` is exactly `Waits::RELEASE`. Each named exception changes one pre-existing wait and its control exercises the corresponding expiry, report, or ordering; TERM is never shortened. Ordinary tool controls use `Waits::TOOL`, while deadline-driven tool/tree controls select the named wall exception and assert wall expiry. The old universal short handshake is caught at runtime by the structural control, and exact restoration is recorded.

The inherited native correction is narrow and evidence-preserving. Any retained failure must be `TreeCall::GroupKill`, `killpg`, and `EPERM`; the failure count must equal the evidence vector; at least one native group signal must succeed; `RootAlone`, root-inclusive counts, descendant removal, and the platform-limited fact remain required; and the settlement is incomplete exactly when a native group send failed. This matches the frozen baseline's one `killpg` EPERM rather than erasing or reclassifying it.

## Evidence

- The baseline build is pinned to the unchanged base sources and its recorded binary hashes. Its complete default-parallel run reports 192 passed and the one disclosed native EPERM assertion failure, with no `HandshakeDeadline`.
- Candidate-r3 is the final-source evidence. Its build artifacts and binary hashes are linked to the final source, and all three default-parallel runs report 194 passed, zero failed, zero ignored, and no `HandshakeDeadline`.
- Mutation-r2 is pinned to the final source. Both `universal-handshake` and `missing-term-budget` compile and fail the focused control at runtime; the exact restored source passes.
- Owning-r2 is pinned to the final source. Components all-target Clippy with warnings denied, doctests, rustfmt, environment controls, operability source and lock checks, and design verification all pass.
- Candidate-r2, owning-r1, mutation-r1, and the cancelled development attempt remain historical context only and supply no final-source acceptance evidence.

## Boundary

This accepts only the corrected waits-only D5-0a slice under the previously permitted LD-D5-0-SPLIT-1 sequencing. It does not complete D5-0, satisfy D5-1's dependency, or establish a full-repository suite, product qualification, or any production behavior. D5-0b retains the structural root, graph, proof, census, owner-integration, mutation, inventory, and final combined D5-0 obligations; D5-1 onward, D3b-2, Linux, CF/J, and qualification remain open.

## Non-blocking observations

- The existing operability enforcement owner-label expectation remains outside this test-only slice and is not resolved or claimed here.
- No inventory successor is needed for this package because it adds no path; later D5-0b inventory and final binding remain outstanding.
