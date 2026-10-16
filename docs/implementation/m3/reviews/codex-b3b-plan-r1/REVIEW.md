# B3-b plan r1 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 449 bytes, SHA-256 `5d6f3374eff19d739bf6e01e700af101197610efb8679a7cec207846bb9a2908`. Its sole member, `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r1.md`, matches the manifest: 14,606 bytes, SHA-256 `2570f8e4f665a5dbdbec4226fe2f3002e6b67edfa174d0fda1764896374e65c9`.

Architecture HEAD matches `2cd0bb7712b2c7d4663a2301ed70eaea27934001`; clean product main matches `15a8ac0a82bd81bd04d24190ba90539e2a5bd582`.

## Required findings

### B3BPLAN-R1-RF-1: The synthetic Git reconstruction cannot silently replace the vcs:none law control

Location: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r1.md:99`.

Item 20 explicitly requires the four T2 workspaces in vcs:none mode to give their overlay link maps, while item 19 and B-S1 require a conventional .git directory for actual membership. LD-B3B-6 recognizes the conflict but resolves it by adding synthetic conventional Git evidence and treating that different input as the specified control. That is a useful integration fixture, but it does not demonstrate the control on the stated vcs:none assembly. The plan also expressly leaves the optional git-conventional assembly successor S8 to B3-c.

Required change: Resolve the control interpretation at the law level before using this fixture as its discharge: obtain an accepted clarification/amendment of the item-20 control naming the synthetic reconstruction and its limits, or specify a separate declaration/link-only vcs:none control with supplied member evidence plus a distinct conventional-Git integration control. Do not claim that unchanged vcs:none product discovery admitted members, or that S8 has been implemented. Preserve exact pinned carrier/provider bytes and overlay-map comparison.

### B3BPLAN-R1-RF-2: Define the census equality projection and validate the new member cost paths

Location: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r1.md:120`.

The plan requires byte-identical census records after re-pinning a changed closure, but the census record itself carries the closure pins, so the complete record cannot remain byte-identical. It also says every non-workspace project’s charges remain unchanged even though new declaration-reader work can occur with zero admitted members. No-member equality alone cannot establish an upper bound for the new member-aware traversal. Section 3’s record-equality tests do not test ledger usage against the extended cost model.

Required change: Name the exact unchanged comparison, such as repository-entry walker cost/population rows with an explicit allowlist for changed closure/reference metadata, rather than whole-record byte identity. Separate unchanged walker costs from added reader/member costs, including reader work at n=0. Require the revised native walk/member producer’s measured objects, edges and bytes to be bounded by the new model/bound on synthetic member, shared-path, exact-root, excluded/nested-member and boundary cases, including worst read growth/retries and root length. Retain the existing actual-versus-predicted cost checks and appropriate under-count mutations before using new workspace margins to close the gate.

### B3BPLAN-R1-RF-3: Keep the owner-required pre-run and post-run reviews as separate gates

Location: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r1.md:124`.

LD-B3B-5 calls for rerunning the previously reviewed mode with a new closure, but B3-b3 groups the changed cost model/tool, blind refresh and resulting evidence into one reviewable step. The owner’s authorization explicitly requires review before and after the run. The original mode’s acceptance does not review newly changed cost/population/reference logic or its renewed receipt bindings. The plan does not identify a pre-run acceptance gate before opening held-out stores.

Required change: Within B3-b3, explicitly gate the mechanical run on acceptance of the exact updated tool, transitive cost/reference closure, receipt handling and synthetic confidentiality/lifecycle controls. Only then run the blind mode, followed by an independent review of the receipt and composed census. Preserve the closed output allowlist and no-inspection boundary. A fresh owner decision is not needed for this same authorized method and population; changing access or disclosure beyond that method would require separate authorization.

## Rulings on the requested questions

**Coverage and ownership.** The main scope is appropriate: item 6b, both readers and both branches, root-in-repository disclosures, cap-before-Git-read ordering, V3 membership/provenance, typed link declarations, item 24 and the full-ledger bound. It retains explicit/config refusal versus automatic-reader exclusion, exact named roots and member Git custody without the project-owner waiver. C1/S4 snapshot/VCS bytes, S5/S6 consumption, B3-c harness assembly, recognition and production composition are correctly left to their owners. The joint walker/native sweep, memberConfigs not consulted, placement/decoder fixtures and cap controls are useful commitments. The law's controls and B-S1's additional control list remain binding on the eventual reference/product reviews, including the member config digest invariant, member anchors and U-9's single fallback.

**Decomposition and supplied verdicts.** A separately accepted B3-b0 wrapper is sound; contract 168 is the next available successor at the pinned base. Supplying item 6b verdicts is acceptable for a reference of placement, declaration and routing, provided supplied verdicts do not bypass candidate placement/cap/branch rules. B3-b1's actual custody/config/index fixtures own those verdicts and must establish agreement. Reusing the reviewed decoder avoids an unnecessary second Git parser. The sequence reference/6b producer/readers/full-ledger evidence/status is reasonable, subject to RF-3's additional pre-run gate. Reference no-member equality must preserve the old comparable semantics rather than require an unchanged partial output shape: B2-b0 explicitly emits pendingFields for workspaceDeclarations, whereas this unit completes that field.

**Census closure.** Re-pinning is the correct approach. discovery_scan.rs currently records every observed VCS directory as a nested repository, while member_repositories is empty; the reference similarly stops at VCS boundaries. Admitted members require real traversal/classification changes. A parallel walk that fabricates or erases VCS observations would not preserve the owning law. No lawful pin-avoidance shortcut is established by this plan. But no-member equality alone is insufficient assurance for the new cost-bearing paths, and complete record identity is incompatible with changed closure pins (RF-2). The reviewed bound must cover every charged step and its fixed cost, not only a multiple of member count; caps return to the law if the full-ledger margin fails.

**Blind authorization.** The existing owner's recorded decision authorizes the mechanical blind method, not merely one immutable historical receipt. The accepted B2-b4 plan r6 expressly anticipates stale bindings and a new reviewed run, so a fresh owner choice is unnecessary for a refresh with the same access and disclosure limits. It does not waive the owner's before-and-after review requirement. The updated exact inputs and any modified model must be accepted before the run, and the resulting receipt afterward (RF-3). No current held-out content was inspected to make this ruling.

**T2 link-map control.** Synthetic conventional-Git reconstruction is useful evidence for the production path and need not implement the general S8 harness assembly. Nevertheless it changes the input mode explicitly named by item 20. It cannot, by a plan-only lead decision, be the sole discharge of the unchanged vcs:none control. Resolve that narrow law/control inconsistency as RF-1 requires; do not relax production member custody to make the corpus control pass.

**Link rows.** LD-B3B-3 is sound. Item 22 gives the logical link-set shape, while B-S1's registry explicitly calls its outputs the declaration half and leaves Plan binding to S5/S6. Typed rows must preserve the registry's full fields, including cargoPatchSource and declaredBy, and unresolved dispositions. B3-b need not invent published canonical bytes or consumer-satisfaction behavior. This is a scoped implementation of the unit-row obligation, not removal of WorkspaceLinkSetV1 from later work.

## Non-blocking observation

B3BPLAN-R1-NBO-1: The blind receipt is already stale at the pinned product base, independently of any proposed B3-b edit. Its reference binding for tools/contracts/generator-closure.json is fe4bb4f4580706a556bb047c5a62ffc0a481b43dbc77984169a8fe8d2ea6fbd2, while the current file hashes to 796701ea87e7ff7db1b029c8c0eea043e550e9cd5f0daf234637fae927291acb (both 68,468 bytes). Correct the statement that B3-b1 leaves the receipt current: it can avoid additional drift, but cannot restore current validity. The planned reviewed refresh can address this existing drift as well.

## Verification limits

Reviewed the pinned plan against M3-B r9 items 12 and 19–24, B-S1's reader registry/passages/control list, the accepted B2-b0/B2-c0 reference interfaces, current Git observation and discovery source, the census closure/receipt implementation and public receipt bindings, and the recorded owner decision/B2-b4 plan r6. The receipt-drift finding comes from hashing public product control files, not opening any held-out store or overlay.

No product build, test, generator, census or network operation was run. Neither repository nor control files were edited. No installation, private fixture, signing key or T2 held-out store/overlay was accessed. No delegation or other panes were used. Only REVIEW.md and review.json were written in the requested directory. This is a plan review, with no implementation acceptance, new owner assent or qualification claim.
