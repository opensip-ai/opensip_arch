# B3-b plan amendment A3 review

Verdict: **ACCEPT**. No required findings or non-blocking observations.

Subject: `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A3.md`, 6,427 bytes, SHA-256 `3f5567a9ec75aea52cec2486c921e765c74abb22c2024ba45a9657002851980d`. Byte count and hash match. Architecture HEAD matches `e8f6023cb90847a8d859fadd31e62d9884518765`; clean product main matches `46c0ebb3e88e4cfaa8d5a1021b3fdcccee2e63a8`.

## Completeness

The split preserves A2-1's remaining obligations. B3-b2b2a owns retained-chain identity, handoff proof construction and the per-candidate 6b session. B3-b2b2b owns native observation/custody, composition over the accepted decision core and walker, complete V3 serialization and scenario integration. B3-b2b2c retains both T2 link-map controls and the joint sweep. Each step retains its review and inventory obligations; splitting them does not declare B3-b2b2 complete early.

Item 24's refusal behavior remains in the composition, including no-member baseline provenance for a member-rule refusal and PROJECT.SCOPE_LIMIT's request-rejected/exit-2/REQUEST.UNSATISFIABLE classification. The full-result comparison against B3-b0 supplements the already accepted separate core and walker vectors rather than replacing an integration control with those separate comparisons.

## Identity and recheck equality

The proposed identity satisfies the retained-root requirement at plan level. A private, process-wide, never-reused identity identifies the ProjectChain object that 6a actually observed. Recording it in TrackingObservation and requiring equality in NoRepository::retained binds the stored observation to the exact retained chain after moves into Eligible or RegisteredProject. OperationHandoff::member_precondition uses the subject's own pair, rather than independently selected chain and observation arguments. The existing borrowed RootObservation route remains valid.

The constructor must compare identity explicitly as well as requiring NoRepository; evidence equality is not a substitute. A separately retained root, including a replacement at the same spelling, must have a different identity. Non-Clone ownership supports this construction. The never-reused requirement entails a counter that cannot wrap or reset into reuse; implementation review must verify that behavior, move stability and the existing substitution controls. Neither pathname labels, raw descriptor numbers nor movable addresses can provide this identity.

Excluding the identity from the observation's evidence equality is sound for the stated separation. recheck_tracking continues to compare the tracking verdict and every existing evidence sample. The inspected recheck paths use the admission's retained chain, or the chain moved into RegisteredProject and subsequently lent through Current; they do not create a new chain per recheck. The additional subject-binding gate is NoRepository::retained, whose identity check remains mandatory even when two observations compare equal on evidence. Thus the proposal preserves 6a's existing evidence-recheck semantics without weakening the new member proof. “Unchanged” here concerns operations, charges and decisions; adding an identity field necessarily changes the internal representation.

The amendment does not introduce the rejected unfenced second 6a pass. It uses the already retained fenced observation at the handoff.

## Item-6b session

A begin/observe session is the appropriate replacement for repeatedly invoking the batch API. It pays environment/global/system checks once, then lets the accepted core request candidates in path order and stop branch A at the first refusal. Keeping observe_members as the compatibility wrapper preserves the accepted batch behavior and its charges.

The implementation must retain the existing distinction between an unsupported shared-source verdict and a pass failure: an ordinary shared-source refusal applies to each requested member without latching the ledger, while host I/O and exhaustion fail the pass. A session must preserve that outcome without rechecking sources for each member. Its integration must start source work at the corresponding 6b stage, preserving trial, placement and cap priority, rather than eagerly beginning before those decisions. The original empty/batch behavior remains the wrapper's compatibility obligation. These are consequences of the amendment's unchanged-verdict/charge commitment and the accepted core's short-circuit order, not additional gates.

## Native composition and controls

The proposed native discipline retains the relevant invariants: accounted by-name observations and no-follow opens from the lent root, ACL capture only when metadata judgment reaches it, omission-premise treatment matching the walker, bounded retained-descriptor reads, positive VCS probes, and identity consistency for repeated paths. Ordinary custody/placement verdicts are decided outside charged scopes; catching an already latched error is not an equivalent implementation. The prior non-latching controls remain applicable.

Comparing native access with the accepted core's access must retain metadata, byte and listing coverage, including forbidden anchors and boundaries. Real conventional-Git scratch controls cover the native custody/6b path; the complete reference-result comparison covers both branches, root-in-repository and V3 records. The planned closure re-pins for project_chain.rs, discovery_scan.rs and custody.rs where changed correctly follow A1-2's equality projection. Any other closure file changed during implementation remains subject to the same rule.

## T2 and later gates

B3-b2b2c preserves the two distinct controls: a vcs:none reconstruction with the supplied-member seam specifically at the link stage, and a separate conventional-Git reconstruction through discovery. The first does not claim production admission without Git; the second must exercise actual member admission, links and complete records as section 3 already requires. The joint P3 sweep keeps native.boundary-inventory-mismatch for a removed member. Only lead-readable reconstructions are in scope; held-out workspaces remain unread.

The B3-b3a/b/c sequence, exact-byte pre-run acceptance, single mechanical blind refresh and post-run review, full-ledger margins and failure-to-law obligation remain unchanged. Placement/listing costs at zero admitted members are explicitly carried forward. No current bound, restored held-out margin, full D15 completion or product qualification is claimed by accepting this amendment.

Review used read-only reading, hashing and Git queries, followed by writing the requested outputs. No Cargo, rustc, tests, builds, lane or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
