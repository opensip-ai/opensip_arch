# Proposed C2a-3 interfaces, owner amendments and validation boundary

Unaccepted plan annex. No product interface below exists because of this file.

## Security pure surface

- Re-export the existing concrete `verify_retained_tree` kernel for lifecycle.
  Keep its body/behavior and borrowed map/body/scope inputs. It returns only
  verification, never admitted authority. No public caller-selected custody trait.
- Add O(1) read-only `ClosureCandidate::blob_count()` for funded fee computation.
  Preserve all existing private construction and candidate/Blob semantics.
- Add opaque `AuthenticatedCoreRoles` and closed role views in the InitialCore
  owner. Private construction uses only authenticated native receipt projections.
  Export getters and the opaque type, not raw-id construction or InitialCore.

## Receipt-owned core handoff: X-C2A3-CORE

PlatformReceipt exposes one crate-private, checked `take_core_evidence` owner
operation. It prepares the five-id bundle on the existing attempt scope only
when the analysis handoff requests it, marks a private taken flag on success,
and returns owned values. No RefCell borrow escapes; InitialCore remains
available to later rechecks. No eager receipt-capture allocation or caller in
unrelated command paths is added.

The proposed fee `(5,128,5863)` is separately derived in M-BOUND-r1.md. It is not
M(c), a trust-body re-read, R10a work, a new ledger or a new cap. Its source/category
proof and the handoff, failure, single-take and no-I paths require owner controls.
The read ledger and admission ledger must be visibly distinct in those tests.

The durable OrdinaryWriteAdmission and ephemeral receipt/ReadSession handoff
are crate-private owner seams, called before analysis setup discards a no-I
receipt and before the separate admission ledger starts. C2a-4/J3d/J2c later expose only their intended
bounded admission context, with this bundle from the actual receipt. No public
native gate or production wiring is enabled in the library unit.

## Lifecycle operational surface

- Add an opaque admitted-component payload holding the candidate borrow and
  actual pinned `RetainedTree`; constructor private, no Clone/Default/Deserialize.
- One component-admission function takes ordinary authenticated component,
  matching candidate, selected platform, store, pin request and borrowed scope.
  It executes the full CI open/verified-transfer/map/kernel chain.
- The owning admitted set stores payloads and the owned core bundle. Its
  `AdmittedClosure` views borrow one of those opaque owners. Native contexts,
  Plans and selection must never accept a candidate in their place.
- Keep sink, buffer representation, fee calculator and CollectorFault private.
  No operational custody or verified-byte boolean interface is exported.

The exact safe Rust generics/exports are source-preflight obligations. Candidate
slots remain stable in an outer operation frame. Their initial allocation is
funded once; disjoint mutable-slot iteration preserves serial refusal order.
No unsafe code, leak, hidden clone or self-referential owning return is permitted.

## Existing carrier basis: X-C2A3-SINK

Collector protocol invariants use D4's existing SpecInconsistent/J1 row-2 route:
operational-failed 4, SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant, no public detail,
closed bounded operational-record key. Add the named basis at owning J2/C2a-4
wiring; add no public code or serialized field. Genuine Tree/Closure causes
and Budget remain distinct and take precedence over cleanup observations.

## Representation price: X-C2A3-M

Adopt the proposed concrete M formula only after plan/source review. Implement
funded fixed/metadata/remainder stages and source guards for the allowed shape.
Native ABI, allocation, mutation and charge evidence must establish the actual
implementation; the arithmetic model alone closes neither X-SD9-2 nor fit.
Preserve the whole in-memory map and all existing kernel checks.

## Fixtures and exports

Use the accepted C2a-2 synthetic builders and CI fixture store through their
ordinary authentication/retention path. Preserve the owners' exact existing
joint feature predicates. A dependent-crate analyzer fixture may need a security
fixture-only wrapper around its crate-private synthetic protocol selection;
that wrapper must not become a production constructor or accept a new root/key.

Prove default and ordinary release exports lack every fixture-only constructor,
fault injector and synthetic protocol selector. Explicit feature combinations
retain their owning law's predicate; do not infer a new predicate from a filename.
The implementation preflight must provide the exact export diff and feature map
before any fixture/compiler lane is authorized.

## Source, receipt and integration gates

Before implementation validation, classify every changed file and new callable
against inventory, current owner sources and discovery/snapshot receipt closures.
Any affected receipt follows its required fresh baseline, pre-run review, frozen
blind refresh and post-run review. Historical receipts are not silently current.

Plan acceptance is not source, native, unit or qualification acceptance. Product
changes start only in a new isolated checkout after the plan review. Native
actions require their own reviewed exact recipe/assent and the global lane.
Only independently accepted exact bytes integrate and receive inventory bindings.
Existing C2b/C1c/install/D5 drafts and queued images remain untouched.

The first library unit claims no production R10a/ER10a, C2a-4/J3d/J2c path,
actual pre-attempt envelope, census coverage, first-party release qualification
or completed C2b context admission. The full project retains all those goals.
