# B2-D1-r1 review

**Verdict: ACCEPT-UNIT.** No required findings or nonblocking observations.

## Subject verification

Verified the 12,897-byte manifest, SHA-256 `5d8578545c72be76b480d2f96160c99624e364620850354f64af852fa444eb3b`, and rehashed every one of its 55 members. All recorded byte counts and hashes match.

All six product-map entries match the candidate worktree and archived product bytes. The two existing-file parent pins match Git HEAD; the four new paths are absent from HEAD. All eight source authority pins and the product-lock pin match. Product main and detached candidate HEAD are `c4f8eddd718bf6ef9e37bda6d54bc55fcdcdfb8c`; main is clean. Candidate changes are exactly the six mapped paths. Architecture HEAD is `11bd0d3899ec6fb9c6aff83d3987d4b183bf2c34`.

## Equivalence assessment

The Rust reader implements the bound B2-d0 YAML reader rule for rule:

- The byte bound precedes UTF-8 decoding. BOM/tab checks, CRLF-only normalization, residual-CR refusal and the narrowed character ranges match, including comment text and EOF CR.
- comment_tail implements the optional separated comment without admitting spaces alone. spaces_or_comment implements the empty-flow tail's distinct spaces-only allowance. The key stays at column zero; empty flow requires separation, then permits no further content other than blank/comment lines.
- Block items require indentation and separation after the dash, preserve consistent indentation and require at least one item. Trimming the separating spaces matches the regex's greedy space match; empty item text reaches scalar refusal.
- Single-quote indices remain UTF-8 boundaries, doubled quotes produce one quote, and the closing tail has the reference's exact separation rule. Double quotes use character indices and admit only quote/backslash escapes. Quoted empty strings remain valid.
- Plain comment splitting and trailing-space handling match the reference. Reserved-word comparison, optional-sign numeric matching and the two numeric alternatives match its ASCII character classes. Date matching uses ASCII bytes and the same year/month/day widths and optional T/t/space suffix. Greedy digit matching has no omitted successful backtracking case: a shorter month would leave a digit where a dash is required, and a shorter day would leave a digit where only end/T/t/space is allowed.

Twenty additional constructed cases were evaluated against the pinned reference, covering key/tail separation, quoted versus plain comment tails, near-number/date spellings, signs, doubled quotes, multibyte quoted text, CRLF and EOF CR. Their expected dispositions agree with inspection of the Rust branches. No Rust/reference divergence was demonstrated. Rust was not executed during this review.

## Vectors and tests

The committed vector file contains **1,540 cases: 103 grammar cases (24 accepted, 79 refused), two bound cases and 1,435 substitution cases**. The grammar table covers the plan's productions/exclusions and the defects from the B2-d0 review rounds, including null values, invalid characters, unseparated empty flow and EOF CR. Exact and one-past 64 KiB are separate vectors.

Generation checks the reference's exact byte count/hash before import and requires agreement on every handwritten expectation. The three sweep seeds cover plain/block, escaped single/double quotes with comments, and empty flow. The 19-byte alphabet covers punctuation, separation, quotes, controls and invalid/non-ASCII byte substitutions. This is suitable additional equivalence evidence alongside the grammar table; it is not exhaustive input equivalence.

The Rust tests replay all vectors and verify the bound, exercise every refusal category, and apply every byte value at every position of every accepted grammar document, twice, checking both no panic and deterministic results. The full-byte sweep is a robustness check; only the committed oracle vectors establish cross-implementation expected results.

## Live checks permitted by the request

Executed in the candidate worktree:

- The required Python 3.14 vector generator in --check mode: passed, reproducing the committed vector bytes from the grammar table and pinned reference.
- `python3 -I -B tools/tests/test_discovery_fw01.py`: all eight tests passed, including planted negative controls on temporary copies.

No Cargo, rustc, build, lane, mutation run or additional product test was executed.

## Archived lane evidence

Read and cross-checked the hashed logs and summaries, rather than treating the summary booleans alone as proof.

The final lane shows base **358 passed / 8 failed**, candidate **361 passed / 8 failed**, with the identical eight named synthetic failures and equal suite counts. Unit-test passes rise from 348 to 351; the three new YAML tests pass, including the full-byte sweep. The host suite remains subject to those baseline failures; acceptance here uses the requested equality criterion.

Formatting classification covers lib.rs and both new Rust files; all candidate files are clean and none is excluded as base-dirty. The all-targets host Clippy command includes `-D warnings` and finishes successfully. All seven mutation logs show actual YAML test failures rather than compilation failure, consistent with controls.json. Vector checks, FW-01, environment-exception checks, operability source inspection and verify_design pass in the archived lane. The verify_design JSON reports passed true and productQualification false.

Attempt 1 is retained and honestly marked failed: its only nonzero check is Clippy's type_complexity warning for the test-case tuple. The candidate factors that tuple into the Case alias. Its other archived checks and all seven mutations passed; the subsequent lane passes Clippy too. No failed attempt is presented as the final successful lane.

## FW-01, mint and environment rules

The reader is added to both COVERED and PURE; its test module is explicitly outside production. The production implementation operates on supplied bytes and ordinary strings/vectors only. It has no filesystem, environment, process, socket or publication operation, no forbidden authority-minting constructor and no unsafe block. lib.rs adds only the library module and test-gated tests; no caller or public API is introduced. The structural negative controls cover the new reader, including planted reads and environment access. Existing environment policy is not widened.

## Scope and boundaries

Acceptance covers this exact library-reader unit and evidence. B2-d2 recognition/caller integration, subsequent inventory binding and qualification remain separate. No B2-d, B2 or M3-B completion is claimed.

Neither repository, the candidate worktree nor control files were edited. No prohibited private fixture, installation directory, signing key, held tree or T2 store was accessed. No network, other pane or delegation was used. Only REVIEW.md and review.json were written in the requested review directory; permitted FW-01 controls used their own temporary copies.
