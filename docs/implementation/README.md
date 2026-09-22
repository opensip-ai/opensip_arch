# OpenSIP implementation

Product code lives in the sibling `opensip` repository. This repository holds the accepted design, reference models and review evidence. Codex leads implementation; actual Claude Opus 5 is the preferred reviewer, with actual Grok as the authorized fallback. Local commits in both repositories are authorized. The user will push; no push is authorized here.

Implementation is **not complete**. The selected product is native runtime40 with inventory62, product `ef7d008` (37 inventory and 62 contract successors). The metadata CLI and substantial identity, contracts, evaluator, security, lifecycle, storage and platform foundations exist. Native initialization/current authority, compiler providers, complete analysis workflows, the full report and release qualification remain work. File counts and passing component tests are not a completion percentage.

- [Current status](m2/CURRENT-STATUS.md) gives the compact installed state and pending work.
- [Active work guide](ACTIVE-WORK.md) retains exact hashes, review subjects, test-lane ownership and durable resume instructions; use its latest entry.
- [Independent review queue](m2/PENDING-REVIEW.md) retains chronological evidence. Its current navigation supersedes historical queue entries.
- [Accepted design baseline](../coop/design-corrections/reviews/root-application46-delivery.v1/README.md) and [build plan](../v2/architecture/implementation-boundaries-and-build-plan.md) remain authoritative through their reviewed successors.

Recent accepted work includes [endpoint-only lineage](m2/native-runtime-selection-v35-unit.json), [trust-budget failure closure](m2/native-runtime-selection-v36-unit.json), and [the corrected shared-ledger layout](m2/shared-work-ledger-inventory-v61-unit.json). The [shared-ledger implementation](m2/native-runtime-selection-v37-unit.json) is accepted by actual Claude Opus5 and integrated after root verification. The [real security-cache budget bridge](m2/native-runtime-selection-v38-unit.json) is also reviewed and integrated. [Guarded reserved helpers and actual account precharge](m2/native-runtime-selection-v39-unit.json) are also integrated. Native capture/temporary-buffer and original-postcheck composition remain separate work.

The previous overview, including all earlier implementation and review references, is preserved [verbatim in this checkpoint](checkpoints/implementation-readme-before-runtime37.md). Historical claims about pending reviews or exhausted quotas describe their original checkpoints, not current availability or approval.
