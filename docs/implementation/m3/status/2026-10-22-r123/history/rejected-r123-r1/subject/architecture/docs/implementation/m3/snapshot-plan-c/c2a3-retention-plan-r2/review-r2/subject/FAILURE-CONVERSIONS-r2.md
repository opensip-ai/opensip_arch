# C2a-3 selected failure contract and exhaustive conversions

Proposed correction for C2A3-PLAN-R1-RF-1. This selects semantic Rust types and
routes; it is not compiled source or accepted implementation evidence.

## Public shape and private diagnostics

```rust
pub enum ComponentAdmissionFailure {
    Closure(ClosureRefusal),
    Tree(TreeReadFailure),
    Budget(WorkBudgetError),
    Invariant,
}
```

`Invariant` is a **unit** variant. It carries no CollectorFault, opaque private
value, string, path, IO error or attacker-selected record key. CollectorFault
remains a private closed enum inside lifecycle's admission module. All its
cases project to Invariant and the single fixed operational-record key
`component-admission-collector`. No private per-case detail is required by the
carrier. Existing J1 row 2 / D4 SpecInconsistent precedent supplies operational
4, SYSTEM.OUTCOME.ILLEGAL_STATE, host-invariant, no public detail. The named
X-C2A3-SINK basis remains owed at its owning production wiring.

The public sum can describe a Tree value supplied by a caller, but **the
admission function never returns Tree(TreeReadFailure::Budget(_))**. The returned
normal form, not arbitrary caller-created error values, is the boundary contract.
No public route is selected from unchecked caller-constructed error values.

## Normalization inside the original borrowed scope

The wrapper uses one nested borrowed `work.scope`, not another ledger. A private
operation fault distinguishes Closure, non-Budget Tree and Collector. Normalize
all input failures **inside the scope closure, before it returns**. Thus any
Budget value is returned as WorkFailure::Budget to the existing scope owner,
which latches the original ledger. It cannot be disguised as an Operation fault.
The final public mapping simply projects that already-normalized scoped result.

| Source | Inside scoped operation | Public returned failure |
|---|---|---|
| ClosureFailure = WorkFailure::Budget(b), including unchanged kernel | WorkFailure::Budget(b) | Budget(b) |
| ClosureFailure = WorkFailure::Operation(c) | private Closure(c) operation fault | Closure(c), preserving exact refusal |
| CI open or transfer returns TreeReadFailure::Budget(b) | WorkFailure::Budget(b) | Budget(b) |
| CI open or transfer returns any non-Budget TreeReadFailure t | private non-Budget Tree(t) operation fault | Tree(t), preserving its cause/payload |
| Representation checked arithmetic, subtraction, cast or size calculation fails | WorkFailure::Budget(Arithmetic) | Budget(Arithmetic) |
| Representation scope charge returns WorkBudgetError b | WorkFailure::Budget(b) | Budget(b) |
| Successful transfer followed by sticky CollectorFault f | private Collector(f) operation fault | Invariant, without a payload |
| Successful open/transfer/kernel and valid collector | success | no failure |

The non-Budget Tree arm covers **all** current variants: NotInstalled, Absent,
Length, Digest, Type, Mode, LinkTarget, Extra, Association, Pin, Custody, Binding
and Io. Retain each exact field, including row/directory, custody cause and the
original IO call/error. No relabel to NotInstalled, generic corruption, Closure
or Invariant occurs. The implementation uses exhaustive enum matches so a new
owner variant requires a reviewed conversion decision, not a wildcard fallback.
A private helper may share the open/transfer conversion, but a blanket
`Tree(error)` map_err is forbidden because it would retain a nested Budget.

The final projection of WorkFailure::Budget(b) is only Budget(b). A normalized
Closure/Tree/Collector operation fault projects respectively to Closure/Tree/
Invariant. Source review must prove that no path constructs the private Tree
operation fault with a Budget value and no conversion occurs after the scoped
latching boundary that could evade the latch.

## Precedence and other owners

If transfer returns Err, normalize **that actual error first**. A collector's
finish(false) or other cleanup observation cannot replace it, including when
that error is Budget. Only after transfer Ok may sticky collector faults become
Invariant. Later kernel Closure or Budget causes retain their original partition.
Completed capabilities and pins drop on failure; drop adds no new charge to a
failed ledger and returns no partial admitted set. Ordinary CI failures, kernel
refusals and representation Budget remain distinct.

C2a-1 candidate computation is outside this constructor, whose input is already
a candidate. C2a-4 must apply the same WorkFailure split to candidate failures
on its original admission ledger; no candidate is silently admitted because a
shared failure type exists. The receipt-owned core handoff still uses its own
existing receipt carrier and ledger, never this component constructor or M fee.

## Required implementation controls (not executed here)

- Exercise both WorkFailure::Budget and TreeReadFailure::Budget input forms,
  with open and transfer exhaustion separately. All return only top-level
  Budget, preserve the exact WorkBudgetError and latch the same caller ledger.
- Exercise representation Arithmetic and ordinary charge exhaustion, with no
  allocation after failure and no fresh ledger/reset/retry.
- Source-control the exhaustive matches and prohibit private Tree(Budget).
  Exercise every non-Budget tree variant with its original fields unchanged;
  source guards and enum exhaustiveness cover variants hard to inject natively.
- Check every kernel ClosureRefusal remains Closure and every kernel Budget
  remains top-level Budget. No retention refusal becomes NotInstalled.
- Combine transfer Budget/IO/digest failure with finish(false) or sticky sink
  faults: the transfer error wins. Transfer Ok plus a sticky collector fault
  produces the payload-free Invariant and only its fixed bounded record key.
- External/default/release callers cannot name CollectorFault, construct its
  variants or retrieve it through the exported failure type. Existing public
  Tree and Closure owner types remain their own APIs; no serialization is added.
- Mutation controls must kill a blanket Tree(error) conversion, a conversion of
  WorkFailure::Budget into Operation, a leaking invariant payload and a cleanup
  fault that overwrites a transfer failure. Actual row-11/row-2 envelope controls
  remain owed to C2a-4/J2's production carrier, not claimed by library tests.
