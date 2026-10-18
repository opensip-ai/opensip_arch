# D3b-1 r2 independent unit review

**Verdict: REQUIRED-FINDINGS**

**Subject manifest SHA-256:** `d5c6cac6a64b6210f84828106cfe2ffff153108a66062b3844ceffff05dedbb2`

The manifest and all 134 members rehash exactly. All fifteen parent rows match product commit `d154eb002fc536855b9c831d0d6484bfaf5335d3`; all archived candidate bytes match the product map and final evidence pins. The eight authority files match architecture commit `853d3f08edc90f22abfb11c635eec8b4168094fc`, and the product lock matches the product base. This review is limited to D3b-1 and does not accept D3b-2, Linux/D3b-L, codec qualification, CF/production wiring, D4, or project completion.

## Required finding

### D3B1-R2-RF-1 — The alive-root control still lacks the lifecycle proof and cleanup claimed by the frozen package

The request and `SCOPE.md:34-36` say the preflight alive-root finding was corrected by checking `ExitClass::Unreaped`, absence of `ExitObserved`, and out-of-band cleanup of the surviving root. The frozen test does not contain those checks.

In `a_failed_listing_or_group_kill_leaves_the_tree_incomplete`, the fixture deliberately ignores `SIGTERM` and every group `SIGKILL` is replaced by an injected failure. The test obtains the root PID and proves it was not a by-pid request, but it never asserts the settlement's exit class, never rejects `ExitObserved`, and never proves the root is alive at settlement (`supervisor_tests.rs:4117-4159`). Its cleanup loop covers only `pids` read from the fixture file, which contains the descendant and excludes `root` (`supervisor_tests.rs:4160-4164`). The root therefore remains until the fixture's independent 60-second self-exit (`supervisor_fixture.rs:255-259`), contrary to both the test comment and the scope disclosure.

The held-zombie half is directly controlled: `no_group_signal_follows_the_reap_ceiling` asserts `Unreaped`, `ExitObserved`, and `RootAlone`. The alive half still does not prove the required distinction, so the 193-pass component result cannot close preflight RF-3.

Add direct assertions that the injected group-failure case settles `ExitClass::Unreaped`, has no `ExitObserved`, retains the alive-root confirm state rather than `RootAlone`, and still has a live root identity at settlement. Then kill that root out of band and verify it is gone. Re-run the corrected affected control and the final component suite, and update the summary so `allRequiredComparisonsAndControlsPassed` is supported by the frozen bytes.

## Non-blocking observations

### D3B1-R2-NBO-1 — The other preflight corrections are present and meaningfully controlled

The snapshot now counts and inspects the root, retains its identity or exited observation, and never adds it to the by-pid target set. Root-only, provider 4/5, and tool 64/65 controls exercise the actual bound selection. The provider-bound and root-count mutations fail runtime tests.

### D3B1-R2-NBO-2 — Source behavior and evidence otherwise match the accepted D3b-1 plan

The frozen source uses bounded listings, preserves original `LaunchError` values with call and errno, retains failed and exceeded observations, counts only by-pid `Sent` outcomes in the sweep fact, deduplicates late joiners, and keeps reap-last ordering. The real fork-after-snapshot and same-pid group-change fixtures are present. All eight recorded mutations compile and are caught by runtime test failures.

### D3B1-R2-NBO-3 — Validation supersessions are explicit and coherent

The final component suite records 193 passes, platform records 292 passes and one inherited ignore, and operability records 95 passes against the exact generated JSON/Markdown references. The corrected-CARGO refusal supplement records three passes on both sides. Final Clippy, source check, design verification, formatting, census closure, product pins, and the conservative no-cgroup scan are coherent. The stopped nested-lock catalog attempt is superseded by the standalone five-pass run.

### D3B1-R2-NBO-4 — The inherited enforcement failure and remaining gates are properly limited

The owner-label expectation fails under the same named test on baseline and candidate and is expressly not reported as a whole-check pass. `LadderUnavailable` and `needs_d3b_ladders` remain, no package edge or new product path is introduced, and the carried obligations preserve D3b-2, D3b-L, D5 codec reruns, and the operability owner-label issue. The package correctly makes no qualification claim.

No builds, tests, cargo commands, or lanes were run during this review.
