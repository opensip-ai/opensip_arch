# D3A-0-r2 review

**Verdict: ACCEPT-UNIT.** D3A0-R1-RF-1 is resolved. No required findings; one non-blocking observation concerning the strength of the root-open test trace.

Subject manifest SHA-256: `46094307b1a158df420a23cadbca9cea9237984fe8a9f8d97bbc92e2ea4c0656` (7,203 bytes). Rehashed all 32 members successfully. Verified all four candidate, archive and parent pins, authority and prior-round pins, and the package-base lock pin. The candidate is detached at `4ece8495b3a599dbd1f14009458c94b60d1836c8`, with exactly the four declared edited platform paths and no new paths.

## Round-one resolution

All four descent sites now defer acquisition: measure and remove_bounded each pass a closure for the root duplicate and each pass a closure for opening a child directory. Constructing those closures allocates no descriptor or name. The shared enter helper computes the borrowed name's length, charges the complete descend_cost once, records Descend, and only then invokes the opener. The name copy, stream duplicate, stream creation and stack growth also remain after the charge. A budget refusal therefore prevents acquisition, while a funded acquisition failure retains its I/O call and errno.

This directly resolves RF-1's effect-before-charge and error-precedence defect in both walks. The unchanged successful-walk charge accounting still prices one descent per level, with Open carrying zero additional cost.

The new control uses object budgets 2 and 5 against three objects per descent: the first cannot fund the root; the second funds the root and reaches an unreadable subdirectory before refusing the next descent as Budget. The supplied mutation moves open() before the shared charge. Its recorded run fails the new Budget assertion, without a compilation failure. The successful-walk Descend/Open checks also verify the expected pairing, subject to NBO-1 below.

## Non-blocking observation

**D3A0-R2-NBO-1 — Open is not a complete syscall trace** (`crates/platform/src/process.rs:1228`).

The Open log is emitted inside enter after the charge and after the opener returns. In the supplied late-charge mutant, the initial duplicate can succeed before a failed charge yet emit no Open. Therefore the unfunded-root zero-Open assertion and successful-run adjacency alone do not independently prove acquisition order. The unreadable nested-directory check catches this mutant, and inspection confirms all current sites defer their effects correctly; acceptance is not blocked.

For stronger root-specific coverage, observe the actual opener invocation independently, at its call site or through an injected counting opener, and assert it is never invoked on an unfunded root. The current trace should be described as successful charged acquisitions rather than every attempted syscall.

## Lane and base

Reviewed the runner and archived logs without executing them. The serial platform suite records 321 base and 328 candidate passes, zero failures, equal suite counts, seven new tests and no differing/flaky cases. The focused process suite passes 31 tests. All edited Rust files are base-clean and candidate-clean under rustfmt. Warning-denied all-targets platform Clippy, workspace all-targets check, debug feature check, expected release-feature rejection, ten environment-exception tests, operability, unchanged-closure check and verify_design pass as recorded.

All seven mutants are caught by test failures, not compilation errors: blocking reap, reaping Unreaped Drop, killing abandoned Child Drop, following links, omitting the status charge, opening before the descent charge and ignoring the measurement limit. The new mutation is caught by the new test specifically.

The lane ran at `2b24f319882d41fa4688a6a55bc1ed431fdfb78c`. Git confirms the package base differs by exactly one commit, inventory v219's lock binding, and only design-lock.json changes. The platform candidate is unchanged by that base move. Reusing the lane for this lock-only package rebase is sufficient; no fresh lane or package-base verify_design execution is inferred.

## No regression and limits

Compared the round-two product archive against round one. The only changes are deferred descent acquisition, its Open observation and the additional controls. Cargo.toml and lib.rs are byte-identical to round one's candidates. The accepted assessments of try_reap/settle_reap, abandon/Unreaped holds, no-follow iterative walks and removal passes, logical-size measurement, funded EMFILE treatment, resident-byte sampling and the debug-only fixture feature carry over. D1a's stale-root sweep remains outside this bounded ChildScratch replacement.

The permitted live operability source check passes with 114 rows and no findings. No new mint-census call, ambient environment read or `let _ =` is introduced. No census-closure file changes. This remains macOS library mechanism work: callers, supervision policy and timed ceiling, Linux work and qualification remain unclaimed.

Only reading, hashing, JSON parsing, Git queries and the permitted operability command were performed. No Cargo, rustc, builds or lanes ran. Neither repository, worktree nor control files was edited. Only the requested REVIEW.md and review.json were written.
