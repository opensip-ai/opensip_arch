# B2-A-REFERENCE-r2 review

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings or new nonblocking observations.

## Subject verification

Rehashed the 1,345-byte manifest, SHA-256 `9a3b413d5867297efa285e406a189c27b39415c95ec9f4d148e879fa938bce92`, and all six members. Every size and digest matches. The successor record is 3,057 bytes, SHA-256 `9451422baab8fc7d22566cea927113940d8be4d94a09208950998c69e3ebe3c5`. The candidate reference is 25,293 bytes, SHA-256 `4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8`.

Product HEAD matches `2191674d873ed7c0eb4459683dcc29cf7da42440`; architecture HEAD matches `ccb8b07cc43ba5debc77c600b1f77e06611cf47b`. Both tracked states are clean.

## Round 1 resolution

**B2AREF-1 is resolved.** `cargo_roots_from_markers`, `enumerate_units` and `pruned_anchors_from_directories` snapshot member roots into tuples before repeated forwarding. The directory helper also snapshots Cargo roots, addressing the inherited equivalent defect. The reference differs from r1 only by these materializations and their comments in those three functions.

Repeated the original single-pass iterator reproductions read-only. A member custody directory no longer becomes a Cargo root or unit, and its observed row is retained. Also checked Cargo-root iterator handling in directory observations. The four new equivalence controls cover all three entry points, multiple members and observed directories processed after marker classification. The supplied negative-control transcript shows the r2 checker rejecting the r1 candidate at the first iterator control; it was inspected, not independently rerun.

**Round 1 NBO-1 is applied.** The target-versus-member control now contains both competing anchors (`target/m/.opensip/x`), and `.opensip/.git/x` checks custody above VCS. Both cases also passed independent spot checks. **Plan NBO-1 remains applied:** `PRUNED_TREE_ROW_VERSION` is 3 and explicitly asserted.

## Reference and evidence assessment

Reconstructed the candidate entirely in memory from the accepted pruning copy using the 21 literal asserted replacements in `author.py`; it matches the staged candidate exactly. Did not execute the author script. The permitted checker confirms AST confinement to the same six changed functions, one added helper, seven changed constants, one added constant and the module docstring. Changes preserve the accepted pruning correction's parent-first Cargo derivation and outermost competition across reasons.

SX-1 classification uses exact segments and bytes at the selected root and admitted member roots only. Elsewhere `.opensip` remains ordinary source. The outermost anchor wins across custody, dependency, VCS and Cargo-output reasons. Member roots propagate through enumeration and observed-directory classification without iterator exhaustion; conventional custody prefixes are always present.

The V3 converter carries relative, UTF-8-sorted members separately from boundaries and excluded prefixes. Its outputs validate against the pinned SLS bundle merged with B-S1's additions. V1 and V2 conversion explicitly refuse; historical recognition remains separate from conversion. Current DD, provenance, boundary-inventory and pruned-row versions are correctly moved to 3. The converter operates on admitted provenance; membership admission retains responsibility for the 64-member bound.

Ran the exact permitted checker, writing only [checker-rerun.json](checker-rerun.json). All **83 controls** passed: 49 unchanged pruning controls, 23 SX-1 controls, four iterator controls and seven V3 controls. The rerun is byte-identical to staged `evidence/checks.json`: 603,588 bytes, SHA-256 `b467e14fd3a45b81c44950ae5e17548db2f1d4bf2ce29a2c3c698071ba2f9288`. These controls and the confined source changes are sufficient for this reference design unit.

## Record and scope

All eight sorted parent pins match their bytes and accepted source/application manifests, earlier successor candidates or selected inventory v190. The five candidate pins cover the reviewed subject exactly apart from its included successor record. DD and the pruning copy retain their accepted bytes. There are no passage overrides or supersessions, schema changes or product changes.

The product lock has 162 contract successors, so this unit correctly occupies the next position, 163. Inspected the product's binding requirements and supplied scratch support: it reports base and appended-lock verification passing with synthetic review/assent and identifies this exact manifest and record. That support was not executed during this review. Acceptance here does not make the binding: actual lead assent, architecture publication and the separate product-lock commit with fresh verification remain the lead's next steps.

This separate reference implements accepted plan section 1.1 and LD-B2A-1 and discharges BS1-F3/LD-14's reference-refresh obligation. It does not implement the product rule, walker or CI trace, membership admission, SLM/native-model refresh, or product qualification.

## Boundaries

Used permitted read-only inspection, hashing, JSON parsing, Git queries, the staged checker and reference imports. Ran no Cargo, tests, builds, lane or network operations; accessed no private fixture, installation directory, signing keys or held trees; used no other panes or delegation. Neither repository, stage nor control files were edited. Wrote only `REVIEW.md`, `review.json` and the permitted checker output in this review directory.
