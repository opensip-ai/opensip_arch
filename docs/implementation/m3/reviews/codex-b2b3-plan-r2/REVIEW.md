# B2B3-PLAN-r2 review

Verdict: **ACCEPT**. No required findings remain.

The subject manifest independently hashes to `e2a4d3d57b91c131ce8ed8b71ecce456685539e0d9db2b0967fff5249990f4b0` (452 bytes). Its sole member, `docs/implementation/m3/config-discovery-b/b2-b3/PLAN-r2.md`, hashes to `023033372e5373a830ddf0249f6402571a1f9341c82a3afe17580ee383f01ecc` (21,772 bytes). Both match the request and manifest. Product HEAD is `3b3ab6e0e354c8f81e4ac030ed3102757be43085`, with clean porcelain status; architecture HEAD is `47bee3b55292a973e90bbff6e81e3c509b28f3c0`.

## Round 1 disposition

| Finding | Independently checked resolution |
|---|---|
| B2B3PLAN-1 | Resolved in LD-2, section 3 and controls. Every OS name is charged; exactly dot and dot-dot are discarded before validation/observation. Whole root-relative LogicalPath validation includes 255-scalar segments and the 4096-scalar total bound. The refusal detail and boundary controls are specified. Using the validator directly for an unmaterializable 256-scalar segment is appropriate. This agrees with LogicalPath::parse, MC:274 and the listing primitive's explicit dot-entry behavior. |
| B2B3PLAN-2 | Resolved in LD-3/6 and section 3. Metadata-only kind/owner/mode rejection precedes ACL-dependent judgment in reference order. Nonregular markers retain honest NotObserved state and are never opened; the invariant fault occurs only if an ACL-dependent check actually needs uncaptured evidence. FIFO/socket/symlink cases alone and alongside a valid marker have oracle and no-open controls. The existing core must be updated as this plan requires. |
| B2B3PLAN-3 | Resolved in LD-12 and its failure control. Phase 1 precedes carrier-based resolution and pack admission; phase 2 follows those, then release and downward walking. This agrees with installation_read.rs:245-253. Resolution/admission failures do not reach phase 2 or downward observations. |
| B2B3PLAN-4 | Resolved in LD-11. Existing host configuration.rs and production-reachable includes are covered now, with planted spawn/socket/write negatives. Only nonexistent discovery.rs waits for B2-c. This meets MB item 15's current-module requirement. |
| B2B3PLAN-5 | Resolved in section 3. The common tree descriptions drive reference and native capture. Comparison covers population, VCS evidence, relevant custody inputs, partial provenance, complete boundary inventory and refusal/detail. The ACL projection explicitly excludes uncaptured ACLs rather than inventing them. Pruned and depth-257 hidden-VCS cases exercise the bound adapter's evidence stripping. workspaceDeclarations remains pending. |

Prior NBO-1 is addressed by separating retained ancestors and temporary descriptors, with code/census verification promised; see the implementation note below. Prior NBO-2 is addressed explicitly in LD-7: budget exhaustion and identity changes remain whole-operation refusals even when an unavailable gitdir target would otherwise be null.

## Scope and decisions

The plan refines accepted parent plan r4 section 1.3 and MB items 12/13/15. Section 0's factual baseline remains accurate at the pinned product base. The split into selection/lending, walker, and host seam/flag controls is sound; all three require their own review and binding before B2-b3 is complete.

All thirteen lead decisions are sound as a plan. DiscoveryRoot borrows the retained root and receipt qualification without lending the attempt ledger. The read equivalent release preserves the receipt while releasing the fence, as MB item 12 requires; a failed release cannot authorize walking. The walker uses one discovery ledger, bounded charged listing, parent-relative no-follow observation/open and identity comparison, pruning before entry, and lazy unit-chain custody. Depth-first traversal is compatible with the order-free population, subject to the descriptor implementation note. The upward evidence and waiver plumbing preserve the legacy selection path and charges; the waiver remains confined to the explicit selection root and its required recheck. No downward mount rule is invented. The FW-01 pin and test-only trace fit the existing structural-check and lookup-log patterns.

Section 3 and its strengthened controls are sufficient for this implementation plan: restricted explicit/config observation, no automatic fall-through, Cargo pruning/crossing order, no-open pruning and nonregular markers, same-kind swaps, name limits, read-only/canary/structural checks, exhaustion, and oracle comparisons are retained. Implementation review must verify these controls against actual primitive calls, including absence probes. B2-c's native instrument, B3-b's readers/members, J1's production caller, M4's joins flag, B2-b4's census and product qualification remain separate.

## Non-blocking implementation note

Treat LD-4's 259 as walker descriptor accounting to verify in implementation, rather than a process-wide bound. Close listing streams before recursive descent; account for marker-file temporaries and separately retained admission/installation handles when measuring the actual peak. Explicit source chains also need their own accounting. EMFILE remains a whole-operation refusal.

## Verification limits

Reviewed the complete r2 subject and its diff against r1, the prior review artifacts, parent r4 section 1.3, MB r5 items 12/13/15, MC walk/name rules, the bound walker_population/evidence projection, and the relevant product admission, receipt-release, custody, identity and listing primitives. All work was read-only inspection, hashing, JSON parsing or Git queries until writing these two review artifacts. No reference imports/execution, Cargo, tests, builds, lane or network were used. No private fixture, installation directory, signing keys, held trees or T2 held-outs were read. No code, law, binding or product qualification is claimed. Neither repository nor the stage was edited.
