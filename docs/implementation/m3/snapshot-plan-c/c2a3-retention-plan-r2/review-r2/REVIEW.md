# Independent review — C2a-3 retained admission plan r2

**Verdict: `ACCEPT-PLAN`**

The supplied `subject.json` has SHA-256 `109757bcea029cb018604b1ba7b848a7e5136fdf8058c5fb13c50ebfb408e62c`. All 49 declared members match their recorded byte lengths and SHA-256 values.

## Finding closure

`C2A3-PLAN-R1-RF-1` is closed. `FAILURE-CONVERSIONS-r2.md:6-29` selects a payload-free public `Invariant` variant, keeps `CollectorFault` private, and assigns every collector case one fixed operational-record key. The amended decisions and export/interface annexes consistently use that shape.

`FAILURE-CONVERSIONS-r2.md:31-64` also selects one exhaustive normalization boundary inside the original borrowed scope. Direct `WorkFailure::Budget` and nested `TreeReadFailure::Budget` both become the sole top-level `Budget`; Closure operation failures preserve their exact `ClosureRefusal`; every listed non-Budget tree variant preserves its cause and payload; representation arithmetic becomes `Budget(Arithmetic)`; and collector faults become the unit `Invariant`. `FAILURE-CONVERSIONS-r2.md:66-103` fixes transfer-error precedence and requires conversion, privacy, routing, and mutation controls. A transfer error, including Budget, I/O, or digest failure, wins over any cleanup observation. No wildcard conversion or post-scope normalization may bypass the original ledger latch.

## Plan assessment

The complete selected plan is implementable as written at design level. It preserves CI open, verified transfer, private full-buffer retention, explicit borrowed-map construction, and the unchanged C2a-3k verification kernel in the required order. A candidate remains unadmitted until whole retention succeeds, completed capabilities and pins remain private on failure, and no partial admitted set escapes.

The stable outer candidate slots, disjoint slot iteration, retained capability ownership, and admitted-set borrow relationships describe a safe Rust design with explicit compiler controls and a stop-for-review condition if the selected lifetimes cannot be expressed. The plan does not authorize unsafe lifetime extension or an alternate ownership model.

The proposed M(c) model separates CI open/transfer and kernel costs from the new retained representation. It includes staged fee computation, private payload storage and copy work, explicit BTreeMap insertion/search/node/drop categories, conservative shared-slot accounting, checked overflow handling, and a rootless zero-node case. The 2F node and 11FH comparison bounds are source-derived proposals with appropriately required implementation source, ABI, allocation, charge, and mutation evidence rather than claims already proved by arithmetic equality.

The core branch remains receipt-derived and single-use: five existing authenticated role/base ids plus lineage are copied under the existing attempt ledger before the I/trust branch can discard the receipt and before the separate admission ledger begins. The bundle has no raw-id constructor, clone, default, or deserialization path; the no-component-trust case retains core evidence without opening a component store or charging M(c). Same-core and field-use joins remain with their later owners.

The export and fixture map keeps production and synthetic authority separated. The analyzer fixture extension uses the joint fixture predicate, accepts no root, key, receipt, path, or production selector, and remains subject to source/export and release controls. X-C2A3-M, X-C2A3-CORE, and X-C2A3-SINK are correctly presented as proposed amendments and later owner obligations, not existing standing.

## Evidence limits

This is plan acceptance only. I did not execute the arithmetic scripts, compiler, native code, builds, tests, fixtures, or receipt lanes. The frozen arithmetic reports support internal formula consistency but do not establish source completeness, native ABI/layout, allocation behavior, exact charge conformance, safe lifetime compilation, carrier behavior, feature/export closure, or mutation effectiveness. Those checks, the substantive owner amendments, complete census and production-fit work, C2a-4/J3d/J2c wiring, independent exact-byte unit review, integration, binding, root assent, and qualification remain open. This verdict grants no native launch, unit acceptance, integration, root assent, or product qualification.
