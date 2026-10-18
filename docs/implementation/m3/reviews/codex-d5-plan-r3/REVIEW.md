# D5 plan r3 review

**Verdict: REQUIRED-FINDINGS.** Two required corrections remain in the new reachability specification.

Verified the 748-byte subject manifest, SHA-256 `c2a66656b043cdbd5d89e9e2d697d82e64df4cc86277e944d1121ae88f348283`, and all three member lengths and digests. PLAN-r3 is 56,565 bytes, SHA-256 `f9485a66706836a562bcbbe050130bf6db2f01e96aea8d63ab4e143ad7733ae6`. Both historical members match their previous reviews. All eleven opening authority hash prefixes match. Product inspection used the pinned `4e475c7` base.

## Round-two disposition

- RF-1 is resolved: process creation, PATH-search execution and the one D1b-owned launcher execve site are separate predicates, with narrow positive and negative controls.
- RF-2 is substantially addressed: external mod, path and include edges, ancestor gates and production-over-test precedence are now specified. The root and Boolean-condition gaps below must be corrected before calling the graph sound.
- RF-3 is resolved: provider setsid records the same POSIX EPERM in both session-leader contexts without confinement credit. The separately labelled non-leader sanity child and credit-misclassification mutation are appropriate. E-TREE enforcement credit remains platform-specific; macOS's documented escape limit is not enforcement.
- RF-4 is resolved at plan level: zero fit, automatic=1 and automatic>1 have distinct evidence states. The alternate single-thread interaction control is explicitly overlapping and never substituted for the resolver's actual value. Mutation credit requires genuine overlap.
- NBO-1 is adopted: strict requested-result fields remain strict; operationally variable fields require per-script synchronization or explicit allowed outcomes.

Q6's resolver dependency/not-run state, Q7's SCAN_SCOPE/CLIPPY_CRATES split and Q8's numeric-address validity exception are preserved. The unchanged seven-unit split, runtime fake smoke checks, codec re-run and qualification/CF/Linux gates retain their earlier standing. These are prospective obligations, not executed evidence.

## D5PLAN-R3-RF-1 (P2): Keep build-script code within the production policies

Location: d5/PLAN-r3.md:175-186 (LD-D5-6 roots/classification).

Build scripts are roots of a separate kind, but only paths from production roots make a file production; the final otherwise case makes remaining files test targets. Thus build.rs and its ordinary modules can receive a test exemption, including the platform build script whose exact environment reads the baseline deliberately records. Cargo also permits an explicit build path other than build.rs.

Required change: Treat build-script roots and their reachable ordinary code as production for both structural policies (or give them a separate non-exempt class subject to the same restrictions). Discover the effective manifest build target, including custom paths and build=false, as well as default build.rs. Keep the exact reviewed build-script environment baseline. Add a custom build-root/helper control with a planted forbidden spawn and an extra environment read, both refused.

## D5PLAN-R3-RF-2 (P2): Use Boolean reachability rather than gate-atom presence

Location: d5/PLAN-r3.md:177-186 (LD-D5-6 cfg propagation/classification).

The plan supports all/any/not but defines exemptions by a path containing cfg(test) or a test-only feature. Presence of an atom is not a test-only guard: cfg(not(test)) is production and cfg(any(test, not(feature = "crash-matrix"))) is reachable with both test and crash-matrix false. Unknown-cfg fallback does not repair these fully parsed expressions. The new graph must not reproduce filename exemptions as syntactic gate exemptions.

Required change: Define classification over the Boolean path condition: grant a test exemption only when reachability implies test, and a test-only-feature exemption only when every non-test reachable configuration requires an exact release-refused feature. A satisfiable path with test=false and no such feature is production; uncertain analysis remains non-exempt. Include the enclosing item and inline-module conditions. Add positive all(test, ...) controls and negative not(test), any(test, not(feature = ...)), and mixed test/production paths, for both owner tools with synchronized census data.

The pinned platform manifest explicitly selects build.rs; that script reads CARGO_CFG_GETRANDOM_BACKEND at line 11. The plan already names this as a production build-script exception. A classification that exempts the whole script would make that exact baseline ineffective.

## Q9 ruling

**ACCEPT.** An empty launcherExec row until D1b's accepted launcher supplies the exact path, function and pattern is the correct ownership. D5 may implement and test the row schema using temporary synthetic trees; it must not populate a production exception for an unaccepted launcher. D1b's eventual scope/review must include the row and the combined structural checks. Lack of a detailed D1b plan today does not justify a speculative exception or a crate-wide exemption.

## Limits

No checker, Cargo, rustc, build, lane or network operation was run for this review. No other pane or delegate was used for this review; no prohibited fixture, installation, key, held tree/entry, store, overlay or cache was inspected. Only REVIEW.md and review.json were written for this review; neither repository, any worktree, nor the control files were edited. Runtime soundness remains for D5-0 implementation and its mutation controls.
