# Proposed C2a-3 export and feature map

Unaccepted design selection. Names below are proposed Rust items, not current
exports or compiler evidence. Current owners and gates are pinned in INPUTS.json.

| Owner/source | Proposed public or private surface | Gate |
|---|---|---|
| security/component_closure.rs and security/lib.rs | `pub fn verify_retained_tree` plus root re-export; unchanged concrete inputs and kernel; `ClosureCandidate::blob_count` read-only method | same unconditional pure module as existing candidate/kernel |
| security/trust/initial_core.rs | public opaque `AuthenticatedCoreRoles`, closed `CoreRole`, borrowed `AuthenticatedCoreRole` view and read-only role/id accessors; private fields and constructor | macOS, inherited InitialCore module gate |
| security/trust/root_payload.rs, trust.rs, lib.rs | public re-export chain for those three core types; keep InitialCore itself crate-private | `target_os = "macos"` at every gated edge |
| security/custody/read_premise.rs | `PlatformReceipt<P>::take_core_evidence` and private taken state, existing attempt carrier | crate-private; existing macOS owner module |
| security/custody/ordinary_writer.rs, installation_read.rs | forward owned core handoff before receipt/trust branch, no escaping guard | crate-private; existing macOS owner modules |
| lifecycle/lib.rs and new component_admission.rs | private module, root public re-exports `AdmittedComponent`, `AdmittedClosure`, `AdmittedSet`, `ComponentAdmissionFailure`, `admit_component` | `target_os = "macos"`; no fixture feature required for ordinary API |
| lifecycle/component_admission.rs internals | collector, representation, fee calculators and constructors | private; no public sink trait/fault injector/raw authority constructor |

`AdmittedClosure` is a borrowed enum view of the admitted set's owners, not a
second owning clone. Core variant carries only the authenticated closed-role
view. Any public failure type must expose a closed opaque invariant category,
not leak the private CollectorFault type or a path/error string. Exact safe
lifetime parameters and Rust signature spelling remain implementation preflight
and compiler controls; changing the selected ownership design requires review.

## Existing fixture gates and selected extension

The security candidate module is unconditional, but its existing
`AnalyzerSubprotocol::selected_for_tests` is **only cfg(test)** and crate-private.
Dependent-crate tests do not make that cfg true. Keep that existing method/gate.
Add a separate fixture factory, named `fixture_analyzer_subprotocol`, behind
`any(test, feature = "crash-matrix", feature = "scenario-fixtures")` at both its
definition and root re-export. Its only operation constructs the same bounded
selected protocol from an explicit major for synthetic authenticated-component
fixtures. It accepts no installed path, root, key, receipt or production selector.
This is an explicit new fixture-gate site requiring inventory/feature review,
not a claim that the present cfg(test) method is already cross-crate callable.
The production analyzer-selection owner remains unimplemented by this plan.

Lifecycle tests use the existing dev-dependency forwarding of scenario-fixtures
to security. No new Cargo feature, default feature, normal dependency feature or
root/key is added. Keep existing debug-assertion refusal guards. New lifecycle
fixture tests and their private injector use
`all(test, target_os = "macos")`; any cross-crate fixture factory must use exactly
the owning joint predicate above, not test-only cfg at just one re-export edge.
Core fixtures must originate in the existing InitialCore authenticated receipt
fixture path under its existing macOS plus joint predicate. No public direct
core bundle fixture constructor is introduced.

## Required export checks

Source review enumerates all added items and every re-export edge. Native checks
cover default library, ordinary release without fixture features, each allowed
fixture-feature debug configuration and existing rejected release combinations.
Compile-fail callers must be unable to construct admitted/core payloads from
raw fields, candidates or ids, or access the fixture factory from default or
ordinary release builds. No native result is claimed by this source plan.

## Production handoff remains separate

This library unit exports evidence types but adds no public native admission
entrypoint or production caller. C2a-4/J3d/J2c must bind the actual receipt-owned
bundle to their actual component admission context before draws/reservations.
The same-core and field-use association controls remain with their owners.
