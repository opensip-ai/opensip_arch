# CODEX2 Review — CI-3L Source Preflight r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### CI3L-PRE-R1-RF-1 — Make the CI-T28 price oracle independent of production cost helpers

The accepted CI-T28 duty requires its enumerator to compute expected sizes independently, rather than taking them from module cost functions (`authorities/docs/implementation/m3/component-install/CI-A3-r4.md:179-183`). The frozen enumerator instead defines `descent` by calling production `crate::installation::descend_cost` and takes `st` and `fopen` directly from production `ct::status_read_cost` and `ct::open_regular_no_follow_cost` (`product/crates/lifecycle/src/retained_tree_tests.rs:830-832,858-864`). It then uses those values in both `E_launch` and `B_hat_launch` (`:878-927,987-1006`). A pricing defect shared by the implementation and one of those helpers therefore changes the expected result with the subject and can leave the equality and bounds green.

Reconstruct the descent, status-read, and regular-open prices in the reference code from their published primitive expressions and independently measured type sizes. Do not call the production cost functions under test. Keep the existing independently implemented component ordering, binary search, read-envelope calculation, and owned-record formulas.

### CI3L-PRE-R1-RF-2 — Update the exact-work oracle for the corrected last permitted lookup and exercise the cyclic refusal through it

Production `resolve` now correctly refuses when the last permitted lookup finds another link, before allocating an `(S + 1)`th hop temporary. The direct CI-T27 control catches the former three-temporary behavior for `S = 2` (`product/crates/lifecycle/src/retained_tree_tests.rs:1159-1175`). The supposedly independent `expected` state machine still implements the pre-fix order: after lookup `S + 1`, it unconditionally joins and records another owned hop for a link, and refuses only at the next loop head (`:954-973`). The cyclic case is never passed through `check_work`, so the oracle does not currently establish exact `E_launch`, `E <= B <= B_hat`, or equality with `launch_pre_bound` for the corrected refusal prefix. If that case were added unchanged, the oracle would expect three temporaries and contradict the production control.

Make the reference resolver refuse a link found on lookup `S + 1` before joining or recording a hop. Run the two-link cycle through the exact-work/bounds oracle and require three lookup traces, exactly two hop records, the precise refused-prefix charge, and both componentwise inequalities against the independently calculated pre-bound.

### CI3L-PRE-R1-RF-3 — Preserve the law's budget failure for hop-length arithmetic overflow

CI-A3 requires every sum and product to use checked arithmetic and makes overflow the same refusal as exceeding the allowance (`authorities/docs/implementation/m3/component-install/CI-A3-r4.md:127-138`). The launch-path calculation follows that rule by returning `TreeReadFailure::Budget(WorkBudgetError::Arithmetic)`, but lexical resolution maps a checked `joined_length` overflow to `TreeReadFailure::Association` (`product/crates/lifecycle/src/retained_tree.rs:626-632,775-782,920-925`). That loses the required budget cause and latches `Association` rather than `Budget`, so a later call would return the wrong latched cause as well.

Map hop-length overflow to `Budget(Arithmetic)` before any charge or allocation, and add a control or source-level arithmetic guard that fixes this partition. The accepted archive limits may make the branch unreachable for admitted manifests, but the implementation deliberately checks it and its typed outcome still has to match CI-A3.

## Scope and evidence review

The frozen subject manifest is 4,934 bytes with SHA-256 `cab1c334391e6117e1cf925660c151ab91d8d1e71d254ae6b8c144300f0868b9`. All 27 declared members match their recorded byte counts and SHA-256 values. All nine architecture authorities match both their staged pins and architecture commit `9e89627bef006ab33e1f1036898653e55c0d5fc1`. The product lock matches product base `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`, which is the current product head. The six product-map parent pins match that base; each candidate pin matches its archived product member. `product.diff` changes exactly the six declared paths and introduces no path or dependency.

The current scope correctly marks `original-SCOPE.md` as historical intent and identifies the four takeover corrections. The final retained-tree source differs from the original draft pin at the stated last-hop boundary, while the four unaffected product files retain their stated original-draft pins. The frozen before-fix report is tied to retained-tree SHA-256 `7cd5fe9bfa92376fcbfb9eaac5e402bb997713598ae8ebf2a66dbfb57511aa6c` and records the intended runtime failure: three hop temporaries for a two-link cycle. The final source and direct cycle control implement the two-temporary correction.

Apart from the findings, the inspected source applies the accepted CI-A3 mechanics coherently. It performs the kind check before lookup; charges each lookup, hop, descent, open, read, status observation, path buffer, and result before its work; uses at most `S + 1` lookups and `S` hop allocations; resolves only over the retained index; reopens and re-hashes files from retained no-follow handles; binds the single composed absolute path by final-component `lstat` and `(device,inode)`; preserves the disclosed same-principal residual window; latches launch and transfer failures across operations and scopes; and ties `LaunchMember` to the mutable capability borrow. The pin remains held by the capability, and the lifetime/GC controls exercise the intended continuity.

The store records an absolute, NUL-free path with its one owned-record charge before copying. `path_status_no_follow` and `directory_identity` check macOS support before charging, charge before their single native call, take `errno` immediately on failure, and use `lstat`/retained-handle `fstat` with no fallback. The unsupported path returns an `Unsupported` `io::Error` before charge. The source does not add spawn or D4 factory authority.

The frozen initial report records 95 lifecycle tests, 15 focused platform tests, and warning-denied all-target Clippy passing against the final six source pins. I did not rerun them. The complete owning, structural, release, and 19-mutation lane remains in progress and no result from it is inferred. This verdict is limited to source preflight and does not accept, integrate, or qualify CI-3L.
