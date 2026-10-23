# C2a-3 draft decisions: ownership, core evidence and internal failures

Unaccepted design decisions for the working plan; no product implementation.

## Existing error owners remain distinct

The component constructor returns a local sum, provisionally
`ComponentAdmissionFailure::{Closure(ClosureRefusal), Tree(TreeReadFailure),
Budget(WorkBudgetError), Invariant(CollectorFault)}`. This is an internal Rust
interface, not a public code, serialized envelope or free-form subject.

`CollectorFault` is a closed enum for impossible collector protocol states:
unexpected/repeated begin, a chunk outside the active state, capacity overrun,
and inconsistent completion after a nominally successful transfer. Each maps
to a fixed operational-record key; no byte, path or native error string is put
into that key. A failed transfer's own failure takes precedence over collector
state, so I/O, Budget or the promised-tree cause is never overwritten by a
subsequent `finish(false)` observation.

Projection follows D4 plan r2's `SpecInconsistent` precedent (LD-D4-11): J1 row 2,
operational-failed / 4, `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant, no public
detail, with the bounded key in the operational record. C2a-4/J2 must record this
explicit basis and test the actual pre-attempt carrier before production use.
This does not extend row 11: row 11 is reserved for genuine Budget failures.
Nor does an invariant prove corrupt installed bytes or not-installed standing.

The whole constructor runs inside one nested **borrowed** `work.scope`. Checked
arithmetic or `u64`-to-`usize` failure returns
`WorkFailure::Budget(WorkBudgetError::Arithmetic)` inside that scope. The existing
scope owner latches the original ledger. No fabricated over-cap charge, fresh
ledger, integer truncation or `Retention::Length` substitute is used.

## Concrete component lifetime sketch

The planned opaque payload is `AdmittedComponent<'store, 'borrow, 'manifest>`:

```rust
struct AdmittedComponent<'store, 'borrow, 'manifest: 'borrow> {
    candidate: &'borrow ClosureCandidate<'manifest>,
    retained: RetainedTree<'store, 'borrow>,
}
```

Fields and construction remain private. Its only public constructor operation
accepts a store borrow, an ordinary-reader `AuthenticatedComponent<'manifest>`,
the candidate borrow, the selected platform, the declared pin request and the
caller's borrowed scope. It performs CI-3 open, bounded verified transfers, map
construction and the unchanged kernel before returning the payload.

This is a proposed signature, **not a compiler result**. The exact covariance
and lifetime constraints must be compiled in the owning native lane before the
interface is accepted as implemented. Candidate slots remain in the outer
operation frame, stable and separate from the returned admitted set. A disjoint
slot iterator preserves serial candidate/retention refusal order. No pointer
cast, unsafe self-reference or lifetime extension is an alternative.

## Core branch comes from the pre-draw receipt

Add an opaque owned `AuthenticatedCoreRoles` bundle in the InitialCore owner
module. Its private fields contain the existing four role ids, the base core id
and selected InitialCore lineage. Only the authenticated owner constructs it.
There is no public raw-id constructor, Clone, Default or deserialization path.
Read-only closed-role views borrow this bundle, never a RefCell guard.

`ReadSession` holds its receipt in `RefCell<State>`. A naked borrowed role view
cannot escape a temporary guard, and retaining that guard would block rechecks
or release. The selected API therefore constructs and returns an owned bundle
inside a checked **single-use receipt-owner handoff**, releases the RefCell guard,
and stores no escaping borrow or pointer into that state.

`PlatformReceipt<P>::take_core_evidence` uses the receipt's already-existing
InitialInstallationAttempt scope. It charges the fixed fee, copies the five
existing ids and lineage, then marks the handoff taken and returns the bundle.
It adds no second ledger or automatic work to receipt capture. Failed scopes
remain latched; a second take is an internal invariant, not a new allocation or
retry. InitialCore and its existing getters remain available for later rechecks.

The durable fenced OrdinaryWriteAdmission and ephemeral receipt/ReadSession
owners forward that method. Their future analysis setup invokes it before the
I/trust-view branch can discard its receipt and before R10a's separate ledger
starts. Thus the I-absent/no-component-trust path retains the same authenticated
core evidence. No caller is added to existing non-analysis paths by this library
plan. The exact proposed fee is in M-BOUND-r1.md and is read-owner work, not M(c).

The public lifecycle core view accepts only the opaque evidence. The owning
admitted set retains the bundle and exposes role views borrowing it. The base
core id and lineage retain provenance for the same-core joins; a free caller id
never supplies that proof. C4's owning composition must use the bundle taken
from its actual receipt, and retains its field-use/current-core association
controls. No post-fence ProjectOperation accessor is used to perform R10a.

This is explicit **pre-admission receipt-owner work**, not M(c). SD9's zero
component-admission charge rule for no component trust view is unchanged.
Core evidence opens no component store and creates no ordinary-reader component
view with an absent catalog. It grants no C3/C4/E/H/X12d field-use permission.
The owner handoff/accounting addition requires the named plan amendment before
implementation, and actual carrier/ABI/lifetime controls remain native evidence.

## Remaining before plan freeze

EXPORT-MAP-r1.md records the proposed exact export/feature map. Independent
source-category proof review remains required.
M-BOUND-r1.md and check_m_bound.py supply the proposed complete representation
fee, staged computation charges and bounded receipt-handoff fee. These prices
and ownership choices still require independent plan acceptance. Native
API, carrier, ABI and lifetime controls remain implementation evidence to obtain
under separate reviewed lane authorization.
