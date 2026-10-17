# REQUIRED-FINDINGS — D1a implementation plan r1

Subject manifest SHA-256: `efda51a374b5f29e6e32203fba121745cf8c9911232495e211c691dafefc6bf2`. The sole member matches 10,601 bytes and SHA-256 `9ca30c54c80af04555915ae8cac14e7c42dbf4b04e1514ff012c4926fd79f98a`. Product HEAD is clean at `808ad6476fb848f84e732ee233a47229370081f4`; architecture HEAD is `92eaf1d5abc575511becd012e8cdf1b3a24d1083`.

## Required findings

### D1APLAN-R1-RF-1 — Runtime OS selection alone does not make the new addchdir symbol optional

`docs/implementation/m3/supervisor-d/d1a/PLAN-r1.md:65`. The SDK declares posix_spawn_file_actions_addchdir available from macOS 26, and the plan declares it locally in Rust while promising an _np fallback before 26. A normal direct Rust extern reference does not acquire the C header's availability/weak-import semantics. An OS-version branch alone can therefore leave a required loader symbol unavailable before the branch executes. The constants and header citations are correct; the missing piece is linkage and symbol availability.

Required change: Specify availability-safe resolution, such as a typed dlsym lookup with a checked _np fallback, or an explicitly supported weak-link mechanism and deployment-target contract. Add a symbol-unavailable fallback control and keep lookup/spawn errors typed. If instead requiring macOS 26+, explicitly change the compatibility claim through the owning authority rather than promise an unimplemented older-host fallback.

### D1APLAN-R1-RF-2 — The ordinary Rust test binary cannot directly witness untouched exec startup state

`docs/implementation/m3/supervisor-d/d1a/PLAN-r1.md:74`. LD-D1A-4 observes signal dispositions only after Rust runtime and libtest initialization. The installed pinned Rust 1.95 source, library/std/src/sys/pal/unix/mod.rs:25-41 and :165-183, explicitly resets SIGPIPE to SIG_IGN by default before user code and initializes other runtime facilities. Consequently D1-T9 cannot observe the intended default SIGPIPE at that test function. Resetting it inside the fixture would hide a missing spawn reset. The proposed closed-pipe host write also does not demonstrate F_SETNOSIGPIPE while Rust already ignores SIGPIPE: it returns EPIPE without killing the process even when the per-fd option is missing.

Required change: Define an observation path before Rust/libtest modifies the measured startup state, or a minimal controlled first-party fixture/startup arrangement with its runtime effects explicitly accounted for. Do not repair the measured dispositions before observing them. Probe F_SETNOSIGPIPE directly with F_GETNOSIGPIPE or use an isolated default-SIGPIPE observer. Add mutants omitting SETSIGDEF, SETSIGMASK and the per-fd SIGPIPE option, and ensure each is caught. Other post-runtime observations may still use the test binary where valid.

### D1APLAN-R1-RF-3 — Construction does not yet specify the exact protocol-specific launch profiles

`docs/implementation/m3/supervisor-d/d1a/PLAN-r1.md:22`. The plan states a generic Provider class and construction checks for absolute argv[0] and an environment-key allowlist, while promising to reject an extra argv element. TS2 and Rust3 share that class but have different ordered argv, required environment keys and fixed values. An allowlist alone admits missing keys and wrong values, such as LANG=other; a union provider allowlist also admits TS2-only keys for Rust3. The plan does not identify the profile discriminator or closed constructors that make its exactness promise enforceable.

Required change: Specify closed protocol-specific LaunchSpec construction within Provider, without adding a repository-code class, with exact BBC TS2 and DRJ2 Rust3 argv shapes, required environment sets and fixed values, and validated host-supplied placeholders. Keep Tool argv/environment under its C3b owner, explicitly gated where that contract is pending. Add negative controls for extra/reordered argv, missing required keys, wrong fixed values and cross-protocol keys; retain the no-inheritance controls.

## Requested decisions

**Fidelity / division of duties:** The plan correctly keeps primitive mechanisms in D1, policy and teardown in D3, and closure rechecking/session construction in D4. Its macOS sessions, exact pipe topology, close-on-exec handling, wait-without-reap, final wait4, reap-last group signalling, membership enumeration, fresh private scratch and stale sweep correspond to items 1–8. Section F confinement remains D1b's, with no confinement claim. Exact launch construction and test observation need the findings above before acceptance.

**Q1 / LD-D1A-1:** A disclosed macOS milestone followed by D1a-L on an actual Linux lane is acceptable under item 8's platform-scope restriction. It must remain partial with respect to the units table's both-family D1a row. Explicit unsupported constructors on other targets are preferable to silently launching with reduced guarantees; their API/build compatibility still needs verification on those targets. Linux rows remain not run, and no Linux or full D1 completion follows from macOS acceptance.

**LD-D1A-2:** The four pinned-libc gaps are real in its Apple surface. SDK 27 confirms SETSID `0x0400`, F_SETNOSIGPIPE `73`, PROC_PGRP_ONLY `2`, and addchdir's signature and macOS-26 availability; the older _np signature remains declared and deprecated from 26. Local, narrowly scoped declarations avoid a dependency upgrade. RF-1 addresses the missing availability-safe call mechanism; declaration evidence alone does not prove loader compatibility.

**Q2 / LD-D1A-3:** Structural enforcement is acceptable for this trusted workspace boundary at a no-production-caller stage, provided the promised call-site check lands with D1a and rejects unauthorized construction. D4 must later become the sole production constructor and perform the same-session closure-owner recheck before spawn. The observed member/descriptor/digest data must correspond to the launch spec; a public constructor name is not itself proof of rechecking. D1 should not introduce a competing digest-verification recipe. D4/D5 integration remains owed.

**LD-D1A-4:** The locks test demonstrates that the test binary can be relaunched for a fixture function. It does not establish that late fixture code sees raw exec state. Environment, descriptors, mask and signal checks need an explicit runtime-effect analysis; RF-2 establishes a concrete SIGPIPE failure in the proposed observer. Session/cwd/core observations can use self-exec where initialization is shown not to alter them.

**LD-D1A-5:** The current operability process patterns do not include posix_spawn, so adding that call does not itself increment that class. Adding the patterns and owner in D5 is correctly disclosed as future work. However, unchanged total counts remain something to check on the actual diff, including stdio/environment/swallowed patterns; absence of Command::new alone proves no whole-census result. The VerifiedLaunch construction census is a separate promised check, not something the present process patterns already enforce.

**Checks and mutations:** The planned platform comparisons, formatting, warning-denied all-targets Clippy, FW-01/environment checks, design verification and mutation suite are appropriate gates. The listed session, fd leak, scratch reuse, core-limit, reap-last, symlink-sweep and search-spawn mutants address important rules. RF-2 and RF-3 supply missing startup and exact-profile controls. New module files are outside the discovery cost closure, so no blind-receipt refresh is implied merely by adding them; the implementation must still verify its actual changed-file set.

No non-blocking observations. This is a plan review, not implementation acceptance, Linux completion or qualification. Review used only file reading, hashing, JSON parsing and Git queries, including local SDK, pinned libc and installed pinned Rust source. No compiler, build, test, generator, network, delegation or prohibited private-data access occurred. Only this directory's `REVIEW.md` and `review.json` were written; neither repository was edited.
