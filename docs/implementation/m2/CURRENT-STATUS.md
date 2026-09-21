# Current implementation status — September 21

The project is not fully implemented. M2–M6 remain open. Product `opensip` is clean at `fa72e50`; candidates remain private and uninstalled. The user pushes; no push has been performed.

- **357:** [Native descendant capture](trials/native-descendant-capture-checkpoint-357/README.md) is frozen and independently reviewed by actual Grok. Twelve focused tests, two lifetime compile-fail checks and eight fault controls reproduced; no bounded defect found. Full375 security tests are author evidence.
- **358:** [Storage marker](trials/native-store-marker-checkpoint-358/README.md) is frozen and independently reviewed by actual Grok with no bounded defect.96 storage tests and three fault controls reproduced.
- **359:** [Host selection/marker bundle](trials/host-selection-marker-checkpoint-359/README.md) is frozen and independently reviewed by actual Grok;68 host tests and two fault controls reproduced, no bounded defect. Both retained records share one fence; this establishes only provisional S consistency.
- **360:** [Cross-crate fixture](trials/provisional-host-integration-checkpoint-360/README.md) is frozen and independently replayed by actual Grok. All12 cases pass, two deliberate faults are caught, and the restored baseline passes. The account home is explicitly synthetic; all506 production files remain unchanged359. This tests public composition, not native account-home provenance or platform qualification.

**361:** [Native trust read session](trials/native-trust-read-session-checkpoint-361/README.md) is frozen and currently under Grok review.382 security tests, four lifetime checks and eight fault controls pass. It retains every original current file across repeated reads under one cumulative, failure-latching budget.

**362:** [Shared current/census session](trials/native-trust-census-session-checkpoint-362/README.md) is frozen, awaiting review.388 security tests and14 fault controls pass. All current/dependency/candidate evidence remains owned under the same budget and fence.

**363:** Host composition of selection, marker and trust session is in integration testing. It does not establish the full five-member store binding or current authority.

The [store-binding advisory](reviews/grok-store-binding358-20260921-r1/REVIEW.md) has a corrective ADDENDUM preserved in its archive. Independent current-record S/G/K comparison is necessary provisional consistency, not a replacement for the full namespace/registry/lineage/admitted-handle binding.

Claude's latest attempt at05:33 was refused by its Fable quota. No Claude agreement is claimed; Grok is the active fallback reviewer. Current work joins that session with the host records and tests changes across owner boundaries. Full authority, writers, installation and later milestones remain open.

Detailed append-only history and exact pins: [resume guide](REVIEW-RESUME.md).
