# C1B-PLAN-r5 review

**Verdict: REQUIRED-FINDINGS — one required finding, no non-blocking observations.**

R4-RF-1's canonical-record correction is sound. The reissued complete derivation retains a separate scalar-versus-byte error in member reach, so its quantitative term and residual margin still need correction. This does not establish a cap failure or require a new product bound.

## Subject and verification

Manifest: `docs/implementation/m3/snapshot-plan-c/c1b-plan-r5-subject.json`, 3,276 bytes, SHA-256 `02575ae6857e4172e911de083d06b78493b77bf659161ae977c6d653187111ec`.

Rehashed all 15 members successfully. All eight historical r4 subject members retain exactly their r4 manifest pins. Live bases match product `813d559efccbfc30b81b7530833c8427bb4f7dfd` and architecture `fa875bfd5c2bc1627742c5363ebc2787b7db46ed`. Git confirms identity is unchanged between caa71e2 and 813d559, and the scratch dependency worktree's identity files match 813d559. Verified all 19 discovery cost-closure pins against current source bytes.

Read the r4 review and r4/r5 plan diff, both derivation sources and recorded outputs, scratch source/manifests/log, canonical encoder and sealing string helpers, LogicalPath implementation/schema, VCS schemas, member reach and native open pricing, r9's guarantee/refusal text, accepted C1c-0 retention evidence and C2a's size method. No evidence script or scratch program was executed. Independent read-only arithmetic reproduces every r5 output vector from the unchanged r4 pricing definitions plus the exact record correction and accepted retention increment.

## Required finding

### C1BPLAN-R5-RF-1 — Price member reach names in UTF-8 bytes rather than Unicode scalars

**P2.** `c1b/r5-evidence/vcs_term_r5.py:111`, with the shared scalar constant at line 46 and LD-C1B-6's complete-term claim.

The member reach charges MAX_DEPTH directory-open base costs and then adds only `LOGICAL_PATH_MAX = 4096` bytes for the names. The identity implementation explicitly bounds **Unicode scalars**, while `open_child_directory_cost` charges `name.as_bytes().len()` (`crates/platform/src/filesystem/directory_open.rs:32`). Item 6b actually spends that cost for each segment (`custody/git_tracking.rs:1492`). There is no 4,096-byte admission bound established here.

A concrete admissible spelling has 256 segments: 255 segments of 15 U+10000 scalars and a final segment of 16 U+10000 scalars. It has 3,841 nonseparator scalars plus 255 slashes, exactly 4,096 scalars. No component is empty, dot, dot-dot, NUL or backslash; every component is at most 16 scalars and 64 UTF-8 bytes. Its directory names total **15,364 UTF-8 bytes**, exceeding the 4,096-byte reach allowance by **11,268 bytes**, even with the segment count exactly at the priced maximum.

This is inherited from r4; it is not a regression introduced by the corrected record formula. Nevertheless, r5 reissues the complete quantitative term and margin using this unsound component bound. The scratch record-encoding check does not exercise member-directory reach.

**Required change:** use separate scalar and UTF-8 byte bounds, correct this component and regenerate the evidence, totals, search/boundary outputs and residual-margin claims. Add a multibyte member-reach control to C1b-1's pricing gate. Do not narrow the admitted path language to preserve the old figure.

A straightforward conservative reach allowance is 4 × 4,096 bytes. Across 64 members it adds **786,432 bytes**. Holding every other published assumption fixed, at the current coordinates this gives a VCS byte term of **1,645,988,966**, cumulative byte total **4,185,918,120**, doubled byte total **8,371,836,240**, and residual byte margin **4,404,016,472**. That remains below 2^33 after doubling; objects and edges are unaffected. These are arithmetic consequences of that conservative repair, not a substitute for the corrected bound/search evidence. Other conservative overcounts do not document or justify treating scalars as bytes in this component.

## Requested assessments

1. **Canonical record length — resolved.** Schema 3 has fixed overhead 167, per-member overhead 91 plus escaped payload, and n−1 commas for n≥1. Schema 2 is 190 bytes for git and 154 for none. Escape costs agree with Encoder::string and C1a3's helpers, including raw UTF-8 for DEL/C1/non-ASCII. Exhaustively checking separator counts independently gives maximum e(P)=24,496 at 16 separators. The maximum is attainable by 4,080 six-byte-escaped controls, and the 64 distinct sorted paths in the scratch source attain the resulting **1,573,798-byte** record. The archived log reports exact formula matches, registry admission of that maximum and refusal of a 4,097-scalar path. Nothing was rerun.
2. **Ownership and controls — sound plan requirements.** The plan now specifies exact preallocation after charging, borrowed member paths/retained commits, stack hex output and no temporary string/integer allocation in the hand encoder. C1b-1 owns the complete model/vectors/derivation and retained commit charges; C1b-2 owns exact sealing/charge-site equality. Escape-class, maximum-record, one-byte-short Budget-before-allocation and allocation-pin controls are explicit implementation gates. Plan acceptance would not establish their implementation.
3. **Published arithmetic — reproducible, subject to RF-1.** The record payload increment over r4 is 1,303,462 bytes. C1c-0 adds 64 objects and 1,056,768 bytes to the subtotal. These exactly reproduce all four published r5 term/total/twice/holds vectors and the residual margin. The existing definitions other than total are unchanged between the r4/r5 scripts. D*=226 and H*=1,048,575 retain the reported edge and read-buffer-growth boundaries under those assumptions. RF-1 concerns the reach-byte premise, not a mismatch between the script's formulas and its output.
4. **Q6/Q7 and member projection — adopted correctly.** D*/H* remain evidence-envelope coordinates rather than runtime thresholds. HEAD's 4 MiB refusal bound is acknowledged and distinguished from a guaranteed 2x fit. All non-row work shares r9's conditional remaining margin. Exhaustion can precede classification and returns typed WORK.BUDGET_EXHAUSTED with no partial observation or unborn-head substitution. A broader unconditional guarantee or cap change still needs reviewed law revision. INDEX_CAP and exact-cap/one-over controls remain. ENAMETOOLONG retains the member-vcs-unsupported:ref-name projection.
5. **Earlier sound decisions — preserved.** The plan diff retains proof lending and same-root composition, per-read no-follow custody and evidence recheck, innermost selection, the closed ref grammar and one-level symbolic policy, loose-ref precedence, constant dirty meaning, schema-2 byte preservation, typed J2 routing, and the combined census batch. Output checks remain separate from freshness; the batch's final reviewed refresh remains after C1b-2. No code, caller or product qualification is accepted here.

## Boundaries

No repository, worktree or control file was edited. No Cargo, rustc, build, lane, evidence script, scratch program, network, private fixture, installation directory, key, held tree, T2 store or cache was accessed or run. No other pane or delegation was used. Only REVIEW.md and review.json were written in the requested directory.
