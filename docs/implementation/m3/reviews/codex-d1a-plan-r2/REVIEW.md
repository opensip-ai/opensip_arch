# ACCEPT — D1a implementation plan, round 2

Subject manifest SHA-256: `bbce5e52603ecfabae4f1d186e4f0e08901de3abe6ce6aeef0c3bacf45384234`. Both members match their declared byte counts and hashes. Archived r1 remains the reviewed 10,601 bytes (`9ca30c54c80af04555915ae8cac14e7c42dbf4b04e1514ff012c4926fd79f98a`). r2 is 15,295 bytes, SHA-256 `d0fc37ce8e8e259b7c4d5067bd7d127a44a664239df503ce502e7bf62f1c915c`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `92eaf1d5abc575511becd012e8cdf1b3a24d1083`.

## Prior findings resolved

- **D1APLAN-R1-RF-1:** Neither cwd function has a direct extern reference. Resolving addchdir and then its _np fallback through dlsym avoids requiring the newer symbol at load time. Both SDK declarations share the stated C signature. Missing both symbols yields a typed pre-spawn refusal, and the forced-first-lookup-null control exercises the fallback. Actual loader compatibility remains an implementation validation obligation; this plan does not establish an otherwise unrestricted minimum macOS version.
- **D1APLAN-R1-RF-2:** The fixture reports Rust's SIGPIPE/SIGSEGV/SIGBUS effects without repairing them. The inherited ignored SIGUSR1 and blocked SIGUSR2 are independent witnesses for the spawn's disposition and mask resets; their omission mutants are named. Full sigfillset/default-reset construction is also pinned structurally, without claiming the late Rust fixture directly observes pre-runtime SIGPIPE. The direct F_GETNOSIGPIPE probe and option-omission mutant replace the invalid EPIPE inference. These changes address the concrete observer contamination while preserving useful self-exec tests.
- **D1APLAN-R1-RF-3:** Closed TS2 and Rust3 constructors build their own argv and required environment, with fixed values and absolute/NUL validation for placeholders. Caller-supplied argv/environment cannot express missing, reordered, extra or cross-profile entries. Exact element/value assertions and invalid-placeholder controls support that construction. Tool remains crate-internal with no external launch path until C3b supplies its owning contract; no new launch class is introduced.

The complete r1-to-r2 diff stays within the declared fixes and supporting controls. No implementation build, test result or candidate-code acceptance is inferred; the contextual candidate worktree was not needed for this plan review.

## Requested decisions

**Fidelity:** The macOS plan retains items 1–8's mechanism/policy separation: D1 owns spawn, descriptors, sessions, exit observation, reaping, group signalling and scratch mechanisms; D3 owns supervision policy and teardown; D4 owns session construction and closure rechecking. No confinement or section-F enforcement is claimed. The listed macOS control families remain allocated to the unit, with corrected startup and profile controls.

**Q1:** A macOS milestone followed by D1a-L on a Linux lane is acceptable with the stated unsupported behavior elsewhere and Linux rows explicitly not run. It does not complete the units table's both-family D1a scope or D1 as a whole. Unsupported-target build compatibility still requires its own lane evidence; this host's plan acceptance supplies none.

**LD-D1A-2:** SDK 27 and pinned libc support the three local constants and the function-declaration gap. Dynamic symbol resolution addresses runtime availability rather than relying on an OS-version branch. Function-pointer typing, null handling, fallback and pre-spawn cleanup must be preserved in implementation.

**Q2:** Structural enforcement of the sole VerifiedLaunch constructor is acceptable for this trusted workspace at the explicitly no-production-caller stage. The D1a call-site check must exist before that scope is accepted. D4 later supplies the only production construction path and binds the same-session recheck to the spec; D5 strengthens the structural controls. D1 performs no competing digest verification.

**Fixture and operability:** Self-exec is sound for the described observations with the explicit runtime distinctions. Signal-state tests need isolated/serialized setup and restoration; they must not repair the child state before observing it. The current operability process patterns do not count posix_spawn, so that call alone does not raise the process count. Unchanged whole-census counts are still to be checked against the actual diff. Extending spawn/search patterns in D5 and checking VerifiedLaunch construction are separate future obligations.

The planned suite comparisons, formatting, warning-denied Clippy, FW-01/environment checks, design verification and positive/negative controls are adequate plan-level gates. Production callers, Linux, confinement, complete D1 and qualification remain unclaimed.

## D1APLAN-R2-NBO-1 — Superseded proof wording

LD-D1A-2 retains the r1 sentence claiming a SIGPIPE-free closed-pipe write proves F_SETNOSIGPIPE. The r2 table expressly withdraws it and requires the direct flag probe and mutant, so the effective control is clear. Remove or label the old sentence as superseded when publishing.

No required findings remain. Review used only file reading, hashing, JSON parsing and Git queries, including local SDK and installed pinned Rust sources. No build, compiler, test, generator, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
