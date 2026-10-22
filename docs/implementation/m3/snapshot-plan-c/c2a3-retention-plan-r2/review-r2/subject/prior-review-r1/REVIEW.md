# Independent review — C2a-3 retained admission plan r1

**Verdict: `REQUIRED-FINDINGS`**

The supplied `subject.json` has SHA-256 `7df3f5d5595bb3ff9d0a88d0ed03ba62f831fe173cb9d3cec8d8259815c3b7bb`. All 45 declared members match their recorded byte lengths and SHA-256 values.

The selected retention chain, candidate/capability ownership, staged representation accounting, receipt-owned core handoff, and sink failure precedence are coherent at plan level. The plan cannot yet be implemented as written because its exported admission-failure contract is contradictory and leaves a route-significant conversion undecided.

## Required findings

### C2A3-PLAN-R1-RF-1 — High — the public admission-failure shape is contradictory and does not define one Budget route

**References:** `DESIGN-DECISIONS-r1.md:7-10,27-31`; `EXPORT-MAP-r1.md:13,16-21`; `AMENDMENTS-AND-SURFACES-r1.md:38-47`; `WORKING-PLAN-r1.md:85-90,115-117`; `inputs/product/crates/lifecycle/src/retained_tree.rs:83-120,390-404`; `inputs/product/crates/security/src/component_closure.rs:62-82,492-535`.

`EXPORT-MAP-r1.md` selects a root-public `ComponentAdmissionFailure` and `admit_component`. The provisional selected sum in `DESIGN-DECISIONS-r1.md` gives that failure an `Invariant(CollectorFault)` variant, while the other annexes require `CollectorFault` to remain private and forbid the public failure from exposing it. Those requirements do not describe one implementable public contract. Deferring the exact Rust spelling does not resolve whether the public variant carries a private value, an opaque public category, or no value.

The same sum has both `Tree(TreeReadFailure)` and `Budget(WorkBudgetError)`, but the frozen `TreeReadFailure` already contains `Budget(WorkBudgetError)` and `open_retained_tree` returns it on ledger exhaustion. The plan does not state an exhaustive conversion that lifts this nested value to the sole top-level Budget route. By contrast, the closure kernel returns `WorkFailure<ClosureRefusal>`, so that path also requires an explicit split between operation and Budget. A scope exhausted during retained-tree open can therefore be returned as `Tree(TreeReadFailure::Budget(_))` rather than `Budget(_)`; a later owner matching the selected top-level Budget variant for J row 11 can misroute a genuine ledger failure as a tree refusal.

**Required correction:** select and document one exact semantic public failure shape. Keep `CollectorFault` private and project it to a public closed invariant category that does not carry the private fault or native/path text, or select another concrete non-leaking representation. Specify the exhaustive conversions from `ClosureFailure`, `TreeReadFailure`, representation arithmetic, transfer, and collector outcomes, including `WorkFailure::Budget(_) -> Budget(_)` and `TreeReadFailure::Budget(_) -> Budget(_)`, with every non-Budget tree cause remaining under Tree. Update the export/interface annexes consistently and require source controls that prove the two Budget-producing input forms reach only the top-level Budget route and collector details remain private.

## Evidence limits

This is plan review only. I did not execute the arithmetic scripts, compiler, native code, builds, tests, fixtures, or receipt lanes. The frozen arithmetic reports support internal formula consistency but do not prove source completeness, native ABI/layout, allocation behavior, or implementation conformance. Safe lifetime expressibility, exact carrier behavior, feature/export closure, source-category guards, owner controls, and all named native and receipt gates remain later evidence. This verdict grants no unit acceptance, native launch, integration, root assent, or product qualification.
