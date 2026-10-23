# Independent source audit — C2a3 initial library r1

**Verdict: `REQUIRED-FINDINGS`**

The supplied `subject.json` has SHA-256 `ccbcde324bb6d876f8a5c8e740cdd1a61a9b2aabc3b0e3b61cb89aaefe436826`. All 79 declared members under its frozen root match their recorded byte lengths and SHA-256 values.

Within this uncompiled source scope, the single-component path preserves the required CI open, verified transfer, private complete buffers, explicit borrowed map, and unchanged kernel order. Tree and kernel Budget values normalize inside the original borrowed scope; non-Budget tree causes remain exhaustive; transfer failures precede collector cleanup state. The core evidence type remains privately constructed from the actual `InitialCore`, and the receipt handoff charges and latches its existing attempt before marking the single take. The split candidate/result slot formula is algebraically the accepted aggregate fee. The issue is that the source does not bind the candidate half of that fee, or its new slot invariant, to the admission operation.

## Required findings

### C2A3-LIBSRC-R1-RF-1 — High — raw candidate slots bypass their mandatory fee and create an unowned invariant route

**References:** `product/crates/lifecycle/src/component_admission.rs:52-69,75-111,137-176`; `SCOPE.md:17-23`; `accepted-plan/WORKING-PLAN-r1.md:59-75`; `accepted-plan/M-BOUND-r1.md:113-136`; `accepted-plan/FAILURE-CONVERSIONS-r2.md:17-24,31-64`.

`prepare_slots` charges the candidate-array half of the accepted shared fee, but returns an ordinary public `Vec<Option<ClosureCandidate>>`. `AdmittedSet::admit` accepts any mutable slice of that shape and has no evidence that `prepare_slots` created or charged it. A caller can allocate a correct-length all-`None` vector directly, pass it to `admit`, and reach successful candidate construction and whole retention. Lines 91-97 charge only the result-array half, so the candidate-array `R(n*S_c) + (0,4n,4n*S_c)` work is absent from the caller's ledger. Length and emptiness checks cannot detect this case.

The raw carrier also creates `Fault::Slots` for a length mismatch or a pre-populated slot and maps it to the same public unit `Invariant` as `CollectorFault`. The accepted exhaustive conversion contract names only Closure, non-Budget Tree, and Collector private operation faults, and binds `Invariant` to the fixed `component-admission-collector` operational key. Once `Fault::Slots` is flattened, later J2/C2a-4 wiring cannot distinguish a slot/preparation defect from a collector-protocol defect. Recording it under the collector key silently broadens the accepted X-C2A3-SINK basis; choosing another route requires an owner decision.

**Required correction:** bind preparation to admission with an opaque, non-constructible prepared-slot carrier whose only constructor charges and allocates the exact candidate array, whose storage cannot be resized or pre-populated externally, and which `AdmittedSet::admit` consumes or uniquely borrows. Preserve the separately charged result-array half and the exact aggregate equality. Make slot length/emptiness inconsistency unreachable from the public safe API and remove the public-reachable `Fault::Slots` route, or obtain a reviewed plan/owner successor that selects its distinct invariant semantics and bounded operational key. Add source controls proving that admission cannot accept uncharged raw slots and that no slot fault is projected as a collector fault.

## Evidence limits

This is an early semantic source audit only. I performed ordinary source reads and hashing and did not execute scripts, imports, compilers, builds, tests, formatting, linting, native code, or fixtures. The source arithmetic is not proof of ABI/layout, allocation behavior, complete operation coverage, safe compilation, or runtime charge conformance. The scope's omitted ordinary-CI success and refusal cases, multi-component and pin-release controls, authenticated cross-crate core fixture seam, lifetime/opacity compile controls, map/source/ABI/allocation proof, mutation and charge controls, export matrix, impact classification, full source/recipe preflight, separately assented native validation, exact-byte unit acceptance, inventory/descriptions, production composition, census/fit, and qualification all remain open. This verdict grants no native launch, preflight clearance, unit acceptance, integration, inventory binding, or product qualification.
