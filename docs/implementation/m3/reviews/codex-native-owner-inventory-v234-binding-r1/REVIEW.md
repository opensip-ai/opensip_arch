# Review: inventory v234 binding-carry projection preflight

**Verdict: PREFLIGHT-CLEAR**

Subject manifest SHA-256: `fbcd483d2c38b27f64206d66769b6947355c79ca6a728d1344ccd981d64aab89`

No required findings.

## Independent assessment

- All five declared subject members rehash exactly. Product and architecture heads remain `a62fbd7cffef34b74896b474aef9262343427101` and `0c4161710471399dfa49453920690c115150f32a`; product is clean, neither head contains this binding, and the relevant accepted inventory publication remains untracked architecture material.
- The accepted v234 subject, three-member inventory manifest, 776,017-byte candidate, source census, successor record, 931-byte independent review, and current root assent rehash to their pins. The accepted inventory candidate remains SHA-256 `654e0ba18d3e16d4943cb12f329b4d4f6efc21e6940ae96b9d840e86a2af35bb`; this proposal changes none of those inventory, census, record, product-code, or review bytes.
- Contract successor 178 is the exact accepted CI3L description successor. Its record, subject, `ACCEPT-DESIGN-UNIT` review, and root substantive assent rehash. The record has exactly four direct v233 description overrides and no supersessions, for `retained_tree.rs`, `retained_tree_tests.rs`, `component_tree.rs`, and `component_tree_tests.rs`.
- The refused proposal appends inventory successor 194 and mechanically projects the current 113 inheritance entries from v233 to their byte-value-equal rows in v234. It preserves every existing `before` and effective `after` passage, but contains only those 113 entries. The unchanged verifier must reject that partial set because selecting v234 makes v233 an ancestor and therefore requires contract 178's four direct accepted passages to be inherited as well. The failed proposal was not committed.
- I independently reconstructed the corrected inheritance from the current lock rather than relying on the report. All 113 existing entries project to the same row path and exact `before`/`after` text under the v234 parent. The four contract-178 entries also project without reinterpretation: v233 indices 450, 451, 533, and 534 become v234 indices 464, 465, 547, and 548, and each v234 row is byte-value equal to its v233 row with the accepted `before` equal to the raw description.
- The corrected set is the canonical parent-path/lexicographic-selector ordering of those 117 unique entries. Relative to the refused lock, it adds exactly the four accepted projections, removes none, and changes only `inventoryPassageInheritance`. Relative to the current lock, the proposal appends the one accepted v234 inventory successor and replaces the 113-row v233 inheritance projection with the required 117-row v234 projection. The 181-entry contract chain and every other lock field remain exact.
- The permitted invocation of the existing, unmodified `tools/verify_design.py` against the corrected proposal exits successfully. Its result selects exact v234 and accepts 117 inheritance rows. This independently confirms the frozen verification summary without granting any execution or qualification authority.

## Boundary

This is projection-only preflight clearance. `design-lock.native-owner-v234.json` is an evidence object, not final commit bytes. After this assessment is recorded, the inventory successor's root-assent metadata pin must be refreshed; no other tuple, inventory byte, inheritance entry, contract entry, or lock field is authorized to change. Root must rerun the unchanged verifier over that final prepared lock before commit.

The 15 retained native `.current` descriptions still require their separate description-contract qualification after v234 binding. Those obligations are disjoint from the four already accepted CI3L meanings carried here. This review adds no inventory meaning, source selection, authority, blind invocation, receipt freshness, dependent-consumption permission, or product qualification.

`projectionOnly` is `true`. `inventoryCandidateChanged` and `productQualification` are `false`.
