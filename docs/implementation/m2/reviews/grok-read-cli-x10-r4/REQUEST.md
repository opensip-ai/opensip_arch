Grok review: law X10 r4, a narrow amendment. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-read-cli-x10-r4.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/read-cli-x10/PROPOSAL.md`, r4, sha256 33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a. r3, accepted by Codex, is preserved as PROPOSAL-r3.md; see hashes.txt. Codex reviewed r1 to r3 (`reviews/codex-read-cli-x10-r*`). You reviewed X10a's code.

Why: X9-1, the crash-matrix test-support surface, found that accepted law X10 r3 conflicts with accepted laws X9 r1 and X8 r3.
- X10 r3 item 5 rejects "a cross-crate test-support bridge, such as a pub test-only module or feature in opensip-security", and pins "No new cross-crate test bridge exists".
- X10a's test `apps/cli/tests/doctor_tests.rs` (`no_home_profile_or_release_selector_reaches_the_binary_or_the_ingress`) enforces that pin as "no [features] table in apps/cli, crates/host, crates/security or crates/reporting".
- X9 r1 items 1, 2 and 6 require a `crash-matrix` feature in security, storage and host, and a doc-hidden `pub mod crash_matrix_support`.
- X8 r3 item 4 requires `scenario-fixtures` in security and storage.
- Each of those features has its own release guards: X9 item 2 (no manifest dependency names it; a release build with it fails at compile_error) and X8 item 4f (dev-dependencies only, pinned out of release manifests).

Change (lead decision): item 5's rejection now says it governs doctor's own test arrangement, and that the later X9/X8 test-only features are not doctor bridges. The pin bullet now reads:
- no cross-crate test bridge reaches the binary, the doctor ingress, or any default or release build;
- apps/cli and reporting have no [features] table;
- host, security and storage may declare only crash-matrix and scenario-fixtures, each under its own law's release guards.

The rejected alternatives are recorded. The header gains the r4 note. Diff r3 to r4 and confirm nothing else changed. X9-1 will narrow the doctor test to match.

Decide:
- Is the narrowing lawful, and does it keep what r3 protected: no home, profile or release selector and no test seam reaching the binary, the ingress or a release build?
- Does anything else in X10, X9 or X8 conflict?

review.json: "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings", "subjectSha256". Write REVIEW.md and review.json. Do not commit.
