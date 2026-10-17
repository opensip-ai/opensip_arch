Codex review: the D1a implementation plan r1 (M3-D r5 items 1 to 8: the spawn primitive, `crates/platform/src/process.rs`). A **plan review**, round 2. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-d1a-plan-r2.

**Rules:** read-only; no repository edits, commits, pushes or delegation; no product build, test or generator run (reading, hashing and `git show` / `git diff` are fine). Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store or T2 cache. No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/supervisor-d/d1a-plan-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), SHA-256 `bbce5e52603ecfabae4f1d186e4f0e08901de3abe6ce6aeef0c3bacf45384234`. It pins `d1a/PLAN-r2.md` and, unchanged, `d1a/PLAN-r1.md`.
- **Bases:** product `808ad6476fb848f84e732ee233a47229370081f4` (clean), architecture `92eaf1d5abc575511becd012e8cdf1b3a24d1083`.

## Authority

- **Law M3-D r5,** `supervisor-d/PROPOSAL.md`: section A, items 1 to 8, with controls D1-T1 to T9, T7b and T9b; the units table row D1a and its gates; and section F (O7) for what D1a does not include.
- **The contracts the law cites:** BBC (`docs/coop/completion/broker-bootstrap.contract.v2.md`) and DRJ2 (`docs/coop/artifacts/delivery-rust-provider-join.v2.json`).
- **The macOS SDK 27 headers:** `/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`.
- **The pinned libc:** `crates/platform/Cargo.toml:15`, libc 0.2.189.
- **The operability source census,** `tools/check_operability.py`.

## Round 2

Your round 1 (`/tmp/opensip-implementation/reviews/codex-d1a-plan-r1/`) returned D1APLAN-R1-RF-1 to RF-3. `PLAN-r2.md`'s "r2 changes" table maps each finding to its resolution:
- **RF-1:** `dlsym` resolution of both `addchdir` forms, with a typed refusal and a fallback control;
- **RF-2:** the fixture's runtime effects accounted for (SIGPIPE, SIGSEGV and SIGBUS reported unrepaired), the SIGUSR1/SIGUSR2 witnesses, the direct `F_GETNOSIGPIPE` probe, and their mutants;
- **RF-3:** the closed TS2 and Rust3 constructors building their own argv and environment; the tool constructor crate-internal until C3b; and the exact-profile controls.

A candidate implementation exists in `/Users/sb/code/opensip-ai/opensip-d1a`, as context only; this round reviews the plan. Check each resolution first.

## Decide

1. **Fidelity.**
   - Does the plan implement items 1 to 8 and the macOS controls without adding or dropping a rule?
   - Is the API's division of duties right? D1 holds no policy; D3 holds supervision; D4 holds the session factory and the closure recheck.
2. **LD-D1A-1 (Q1).**
   - Is the macOS half now, with the Linux half as D1a-L on a Linux lane, a faithful reading of item 8 ("run and claim only this host's macOS family. The Linux code is built and exercised only on Linux lanes")?
   - Is the explicit unsupported build on other targets acceptable meanwhile?
3. **LD-D1A-2.** Are the four local SDK declarations and their citations right? Is selecting `addchdir` over the `_np` form at run time sound?
4. **LD-D1A-3 (Q2).** Is `VerifiedLaunch::from_recheck` as the only constructor, enforced structurally until D4 and D5, acceptable?
5. **LD-D1A-4 and 5.** Is the `TestFixture` child being the test binary itself sound? Is the operability census accounting right?
6. **Tests, checks and mutations.** Are they adequate for the macOS rows? Is any risk unaddressed?
7. **Anything else** that blocks acceptance.

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D1APLAN-R2-RF-n` / `D1APLAN-R2-NBO-n`.
