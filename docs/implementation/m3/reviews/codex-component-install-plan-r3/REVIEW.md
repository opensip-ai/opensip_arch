# CI-PLAN-r3 review

**Verdict: ACCEPT.** No required findings or non-blocking observations. This accepts the pinned implementation plan **and its narrow law amendment CI-A1 (CI-A1-a, CI-A1-b and CI-A1-c)**. It accepts no code, production enablement or qualification.

## Subject and scope

The subject manifest is 754 bytes, SHA-256 `bbb2fc46317d3625d0158c7a7b2afdae3a6e46219ecfc08f486e0bb009696842`. All three members match:

- PLAN-r3.md: 35,877 bytes, `b1db1e4d72634fb32eb5421893f3af1300c53cd7ae85d333c53b0e1bbed1b3fe`.
- PLAN-r2.md: 27,655 bytes, `a16873cd02e5ec132bed857d01a5acfd793de64ae140e6a463969479c6ba27e4`.
- PLAN-r1.md: 18,233 bytes, `320feee0f8f4f784021ab88af7895ed1cdb9bf7f7a7dbb9fd7f45305e58cc223`.

The historical plans remain unchanged from their earlier reviews. Live product HEAD `72e078799b201709b2545ba58cdce3fcd62a933e` and architecture HEAD `0b84657f6ecc1ba5445fdcaac4bdb9bd61087c0c` match the new manifest bases. Read the plan and r2/r3 diff, earlier review context, the amendment’s current law passages, C2a’s sort recipe, LD-D3A-17 and its acceptance, and the binding-source definitions.

Only permitted reading, hashing, JSON parsing and Git queries were used. No Cargo, rustc, builds, tests, lanes or lane lock, network, private fixture, installation directory, signing/private test key, held tree, T2 store/cache or held-out material was accessed. No other pane or delegation was used. Neither repository, worktree nor control file was edited. Only REVIEW.md and review.json were written in the requested directory.

## CIPLAN-R2-RF-1: resolved

LD-CIP-4 now specifies the actual two-buffer bottom-up merge mechanism. Each u32 buffer is charged at one object and `n*size_of::<u32>()` bytes immediately before allocation. Both buffers are included in B_install’s pre-acquisition admission bound: two objects and `2*n*size_of::<u32>()` bytes, using checked products and sums. The 100,000-entry limit makes u32 indices sufficient.

Each comparison charges one edge before execution through a fallible comparator; Budget propagates. The published worst-case bound `n*ceil(log2(n))` is valid for the selected merge passes. Integer computation and the n=1 zero-comparison case are explicit. The traversal reads the final output buffer without allocating another representation. The retained directory stack remains covered by the existing descent recipe.

CI-T22 and CI-PT-7 independently enumerate both allocations and every comparison. The specified cases cover n=1, powers of two, a value immediately above one, and the entry limit. Focused short scopes prove refusal before an unfunded scratch allocation and before an unfunded comparison. Missing/late scratch charges, a one-buffer admission price, missing/late comparison charges, omitted bound rows and unchecked arithmetic all have targeted mutations. These are appropriate future implementation obligations; no such tests were run for this plan review.

## CI-A1: accepted

**CI-A1-a** correctly replaces LAW P-3’s FileBarrierReceipt return phrase with an opaque witness of one successful barrier on the exact handle, with no byte claim. The quoted current phrase is verbatim. It reconciles the law with the constructible StandaloneBarrierReceipt while leaving the existing stronger read-back receipt and V1’s byte verification unchanged. The rest of P-3, including its native barrier semantics, remains unchanged.

**CI-A1-b** quotes the current step-4 traversal row verbatim. Its two inserted ordering rows fund both u32 buffers and the complete comparison bound, with charge-before-execution and checked arithmetic. The revised traversal row preserves its descent count and price while requiring one entry per directory and branch-local post-order. B_install is computed before acquisition, so the added executed work is also admitted before acquisition. Existing pre-acquisition and in-operation budget routes stay distinct.

**CI-A1-c** correctly identifies the current prose at lines 239 and 243 and the current row prefix at line 174. The latter is explicitly elided with the rest of the row unchanged; its quoted prefix matches the law. The replacements consistently require descendants before their parent, including tree/ last, without a global depth sort. That permits one retained branch stack and once-per-directory descent while preserving mode-before-barrier durability. No sibling’s finalization depends on globally sorting directories by depth.

The amendment is narrow and follows the accepted LD-D3A-17 pattern: named current text, explicit replacements, aligned plan/control changes, and acceptance with this plan. It changes the P-3 witness and step-4 ordering/accounting interpretation; P-6, native-call prices elsewhere, handle discipline, failure routes, funded suffix, V1/V2 and all other rules remain in force. No other unresolved law conflict was identified. The macOS-first implementation ruling does not alter the law’s S8 platform table or qualify Linux.

## Rebase and regressions

Git confirms exactly two commits since product 3742822e: the blind run record at `0772eb7f383cdbff1c3d0869486094a95ef7693a`, changing its four census/receipt files, followed by D3a-1 at 72e07879, changing its component files, the three named platform files and Cargo.lock. The lib.rs change adds process readiness exports. No tools/security file changes.

Static parsing of the binding definitions, including their named constants, derives 36 product source/tool paths across discovery’s bindings and the companion’s complete bindings. None intersects the 16 changed product paths since 3742822e. The companion snapshotSources set includes all 13 model/session/anchored source paths, including all four ANCHORED sources. The architecture-side manifest/reference inputs likewise have no changes between the old and new architecture bases. Thus the source sets and their bound inputs remain unchanged; the previously accepted C1a4-blind post-run baseline remains applicable. This conclusion uses public Git/source evidence and the archived ACCEPT-UNIT review, without reopening receipts or held-out material or running a census.

No accepted earlier conclusion regresses. P-6 remains one funded nonblocking flock over the admitted close-on-exec opened-file type, with no repeated checks, duplication, retry or LOCK_UN; close releases ownership under the existing uncounted-close convention. P-3 retains private construction, exact File-object identity and barrier-failure controls outside the bound sources. Branch-contiguous traversal, no readdir/re-entry, and the full per-receipt stop-and-re-plan rule remain explicit. Output checks and byte-equal receipts remain distinct from freshness.

Q1’s joint CI-2/CI-3 package/lane/review after CI-1 and Q2’s typed fail-closed unsupported-target route are unchanged. The single trust bridge, fixture-feature restrictions, exact record encoder, build-time access mode and X-CI-1-a’s separate production/qualification gate remain intact. Implementation acceptance still requires the planned controls, mutation evidence and checks at its actual integration base.
