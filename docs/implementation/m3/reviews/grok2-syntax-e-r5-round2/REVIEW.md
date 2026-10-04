# E1 r5 round 2 — ACCEPT

M3-E1 r5 round 2 records the three round-1 findings and takes up E-R5-NB-1. Item 11 states the two P6 derivations, item 4 records the call 1 receipt and leaves its field list with E2b, and item 14 records LD-NS8's closed set, including `ref mut x`, with declares on the same forms. The diff is those rows, the round 2 table, and the header notes.

The subject is `docs/implementation/m3/syntax-e/PROPOSAL.md`, 165,418 bytes, sha256 `3b9eae379574d037bf879ff67605232803fcf1f97641b86c860ce93d5f5fb6f0`. The diff base is `PROPOSAL-r5-round1.md`, 161,442 bytes, sha256 `2c268a07193e1c32c7d7abad4b3573d70fe5ad597b90d4b0655b5cb60e9b3ae2`. Every `hashes.txt` pin matches, including the overnight log at arch `7fc02d0a6`. No product build, cargo, test, lane or verifier was run. `~/Library/Application Support/OpenSIP` was absent.

The name stays E1 r5. The pinned overnight entry says to fix the three findings as E1 r5 round 2 and keep the revision name, because the E2a records already cite it.

## E-R5-1

Item 11 and r5 changes row 2 derive each constant by E0's P6 rule from the native T2a run E2b measures. The sentence that gave both constants the base formula is gone.

E0R:264 derives `fuelBase` as 4 × the maximum fuel over the empty files, rounded up to two significant figures. E0R:265 derives `fuelPerByte` as the ceiling, over the non-empty files, of (4 × fuel − base) ÷ bytes, then rounds that ceiling up to two significant figures. Item 11 states the same two shapes. The measured quantity is the progress-callback count from that native run, so the formulas say `count` where E0 says `fuel`:

- `base`: 4 × the maximum count over the empty files, rounded up to two significant figures.
- `perByte`: the ceiling of the maximum over the non-empty files of (4 × count − `base`) ÷ bytes, rounded up to two significant figures.

Row 2 points at those two lines and at item 11. The limits object is unchanged: `{maxFileBytes: 4194304, maxNodes: 4194304, maxDepth: 4096, operationBudget: {base, perByte}}`. E0's measured values stay on the T-wasm reading rule.

## E-R5-2

Item 4 records the T-native receipt as call 1 states it. It records the crate archives and the compile models that build the linked code, with toolchain fields null. E2b writes it, and `buildReceiptSha256` is never null. The three-field compile-model definition is gone.

Ruling 1 leaves the T-native receipt's field list to E2b's proposal and E1's next revision, alongside A8's range. Item 4 says that. Item 20's E2b row adds the proposal, and the integration edge says E1's next revision fixes A8's range and the receipt's field list before E2b integrates. The law sets no receipt schema and no A8 number.

## E-R5-3 and E-R5-NB-1

Item 14's E-12 bullet matches LD-NS8. An identifier binds only as `ref x`, `mut x` (also `ref mut x`), `x @ p`, `let mut x`, or a `mut x: T` parameter. A shorthand field binds only as `S { mut a }` or `S { ref a }`. Any other identifier in a pattern binds nothing, and at L3 its name is not renamed. Declares extraction uses the same forms, so an ordinary unmodified local or parameter is neither renamed at L3 nor declared. That is LD-NS8's stated limit, and it is the declares half the SYN-NS review records at REVIEW.md:34. r5 changes row 14 adds the declares sentence.

LD-NS9 stays. A Rust body that contains a `macro_invocation`, an `attribute_item`, or an `inner_attribute_item` gets no L3 renaming at all.

E-R5-NB-1 is taken up in the same item. The level files carry `atomicKinds` and, from SYN-NS r2, `lineTerminators`, in L1, L2 and L3. That is LD-NS2's level-file bullet.

E-R5-NB-2 is unchanged. The questions closer still restates the review question in one `(r5)` sentence.

## Scope

Against `PROPOSAL-r5-round1.md` the diff is 25 insertions and 9 deletions. Each hunk is the draft line, the round 2 paragraph, the lead-decisions sentence, the round 2 table, r5 rows 2 and 14, item 4's receipt row, item 11's two constant bullets, item 14's E-12 bullet and level-file sentence, or item 20's E2b row and its integration edge.

## Required findings

None.
