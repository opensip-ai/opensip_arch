# B-S10 round-2 design-unit review

Verdict: **ACCEPT-DESIGN-UNIT**

Required findings: none. Non-blocking observations: none.

Subject manifest: `96807b6d7852e00c57ba0022e94ea3677e38c61691266a8bb8fa4bbd3936317e` (28620 bytes; 125 members). Independently rehashed every member. All sizes and hashes match; the three successor parents and 124 candidate pins match too.

## Prior finding and observation resolved

**B-S10-R1-RF-01 is resolved.** The recipe's optionsSha256 is now `c3481af1bbc9f5c2ec90fff05d1a298452f8901dce5536dd399a1f5fce404af5`, matching the candidate options file and its generator-closure row. The recipe closure hash and complete source-digest set also match. The generation runner now calls the unchanged standard admission.registry before pipeline.run and asserts the admitted options pin. Its refreshed summary records standardRecipeAdmissionPassed true. The source rows are now sorted by sourcePath, as standard admission requires.

The retained failed attempt demonstrates that the new admission path catches unsorted source rows before pipeline execution. The rebuilt package preserves attempts 4 and 5 as well as earlier history. This review used the actual retained logs and corrected bytes rather than relying on the attempt numbering alone.

**B-S10-R1-NBO-01 is resolved.** The README explicitly limits scratch verification to verify_design.verify with synthetic selection. It reserves the actual report lane and standard generate_contracts.py check for integration with real acceptance/assent and the bound candidate lock. It claims neither has passed against an actual bound B-S10 lock yet.

## Materialization and generation

The admission registry is exactly the parent registry and aliases plus the two new rows, sorted by schema ID. All source IDs, lengths and hashes agree with the full selected documents. The preview JSON differs from its accepted parent only by removing the top-level $comment; its raw diff removes that member and the preceding comma. Every validating keyword is unchanged. The identity profile implementation remains byte-identical to base and does not admit $comment. No profile widening is selected.

All 14 product copies are byte-identical to the candidate worktree and exactly cover the changed/added Git file set. PCS is in generation and admission, owned by configuration.rs and generated as ProductConfiguration2 in invocation. Preview v1 is admission-only. All 50 identity pins match registry IDs, ordering, lengths and hashes; the host/storage source lists match that order exactly. The test/comments move only from 48 to 50. No configuration resolver implementation is added.

All 350 generator-closure pins match the candidate. The options/source-map re-pins and recipe provenance agree. All eight output hashes in the refreshed generation record match the actual worktree; only invocation.rs and report.ts differ from base. Compared with round 1, report.ts changes only its registry-provenance hash, now `a5cfa92296b4bc725c0562c5879b352a04cbe8d67a1543f74f994911ad4dd741`, matching the corrected registry. The Rust generated carrier is unchanged from the prior reviewed generation output. The runner, source and pin evidence support generation by the existing pinned pipeline; no generator was executed by this review.

## Checks and scratch evidence

Checked both retained r8 history and fresh r9 raw base/candidate logs against their comparison JSON. Host failure sets remain equal at eight and storage at 33. In each tree host records 310 passed across three suites and storage 137 passed across two suites. The comparisons use --no-fail-fast; equal failures demonstrate no observed regression, not full suite success.

The current r9 records retain passing identity/contracts suites, edited-file formatting and all-target warning-denied Clippy, with lane ownership, priority 10 and private TMPDIR. The pre-existing dependency-policy census failure and unrelated host/identity formatting conditions remain disclosed and unchanged. The actual report lane still stops at the unselected admission-registry preflight; allPassed remains false rather than concealing that boundary.

Verified that the scratch helper's work-directory architecture package matches every staged subject member. Independently reran the expressly permitted helper in report-only mode, suppressing its sole write_text expression in memory. It produced the supplied result without writing a file:

- Base lock with candidate tree refuses the unselected admission source.
- Synthetic B-S10 append passes: 162 contract successors, 124 candidates.
- Generation sources verified: 41. Admission sources verified: 50. Aliases verified: 15.
- No generator/runtime code execution and no product qualification.

This is structural selection evidence using synthetic review/assent, not a real binding or a report-lane pass. Fresh verification and the standard generator check with real acceptance/assent remain integration duties.

## Scope and boundaries

The product remains clean at `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; the candidate worktree remains based on that commit with its materialization uncommitted. Architecture HEAD is `54e336d81911a0e0eaeb815163e25ea992026e54`. This acceptance selects the exact design-unit bytes for the lead's subsequent assent/publication/bind process. It establishes no resolver semantics, law change, current binding or qualification.

Used permitted read-only file/source reading, hashing, JSON parsing and Git queries, plus the expressly permitted scratch helper with its file write suppressed. No Cargo, tests, builds, generators or lane were run. No network, panes or delegation were used. Private fixtures, installation, signing keys and held trees were not read. Neither repository, worktree, stage nor control files was edited. Only this directory's REVIEW.md and review.json were written; round-1 artifacts were not modified.
