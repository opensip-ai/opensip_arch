# Proposed complete C2a-3 representation price

Draft policy and source derivation for plan review. These are not implemented
prices, native measurements, accepted bounds or complete admission A(Σ).
The conditional node-storage proof and pinned sources are in the sibling files.

## Inputs and conventions

F is Blob count, b_i each checked byte length, B their checked sum, P the maximum
borrowed path **byte** length, H = 1 + bit_length(F), and
E = Σ[2*ceil(b_i/65536)+2]. All arithmetic is checked in the borrowed scope.
The published storage price is R(n) = (1,0,n+128). Supported-target assumptions
are LP64, 24-byte Vec headers, 16-byte fat references and node allowance 512;
native ABI checks remain required. No cap follows from this price.

The implementation uses one pre-reserved payload-header vector, F private
payload buffers, then explicit unique BTreeMap inserts. No bulk collect, owned
path key, extra payload clone, callback allocation beyond reservation or map
deletion during construction is allowed by this shape.

## Map work decomposition

Let N ≤ 2F be the conservative node-allocation bound. Let q ≤ 11FH bound string
key comparisons. Search descents visit at most FH nodes. Each split allocates
one sibling; root growth also allocates a node. Bound leaf/internal splits and
root growth individually by N, and internal insertion by 2N. Rootless F=0
allocates no node. The bounds are deliberately conservative and not exact counts.

The selected source paths are entry.rs insert_entry, node.rs insert_fit/insert,
insert_recursing, split, correct_parent_link and root growth, plus search.rs.
Existing left nodes are reused. Allocations remain in the resulting unique-key
tree; nonempty completed nodes own keys. The source proof and native controls
must validate the N bound, not assume an allocator trace was already executed.

| Operation group | Count bound | Logical edges per occurrence | Bulk bytes per occurrence |
|---|---:|---:|---:|
| Node initialization | N | 2 | scalar category |
| Ordinary leaf insertion | F | 6 | 768 |
| Leaf split | N | 8 | 704 |
| Internal insertion/root push | 2N | 22 | 1024 |
| Internal split | N | 20 | 1024 |
| Root growth | N | 8 | 1024 |
| Key/reference drop walk and node release | F+N | 1 | scalar category |
| Search descent | FH | 1 | scalar category |
| String comparison | q | 1 | 2P |
| Probe-loop metadata | q | 1 | scalar category |

This gives at most `7F + 83N + FH + 2q` map edges. Node-array bulk operations
total at most `768F + 4800N` bytes. The bulk allowances count both read and write
streams; node metadata and parent repairs belong to the scalar category, not
again to bulk copies. A scalar visit reserves 64 bytes, covering the bounded
metadata operands, including parent pointer/index repairs. It is not a count of
machine instructions or a claim about allocator internals/RSS.

The table must be source-audited against the concrete implementation and pinned
standard-library paths before the price is accepted. Any uncovered operation
changes the proposed bound and requires re-review; the table is no license to
add arbitrary work to a fee block.

## Complete per-component representation bound

In addition to map work, reserve 64 scalar visits per Blob for local metadata,
header/collector state and buffer-drop bookkeeping, 8 scalar visits per allowed
chunk callback, and 128 fixed visits for price arithmetic and empty-case work.
The callback allowance includes begin/finish within the per-Blob reserve.

With N=2F, q=11FH:

```
M_edges = 128 + F*(237 + 23H) + 8E
scalar_edges = M_edges - q

M_objects = (1 if F>0 else 0) + F + 2F

M_bytes = (24F + 128 if F>0 else 0)
        + Σ(b_i + 128)
        + 2F*(512 + 128)
        + 2B                       # sink read/write copy streams
        + 48F                      # payload-vector header moves
        + 2P*q                     # path comparison streams
        + 64*scalar_edges
        + 10368F                   # map bulk operations
```

Storage, bulk copying and metadata visits are distinct categories. CI's shared
buffer acquisition/hash is still B_open/T; kernel re-hashing is still K. Neither
is repeated in M. The map borrows keys and values; no key ownership price is
invented. Drop work is prepaid before allocation and does not charge a latched
ledger afterward. Existing CI capability/pin drop remains its owner's rule.

## Fund computing the fee

Expose a read-only O(1) `ClosureCandidate::blob_count()` accessor. It authorizes
nothing. After successful CI-3 open, charge the fixed 128 scalar visits before
querying the count or computing a variable allowance.

Then charge a metadata scan allowance `(0,12F,64*12F)` before iterating Blobs to
derive B, P and E with checked arithmetic. No payload or path bytes are copied
during that scan. It inspects borrowed lengths and fixed metadata only.

Compute the complete bound, subtract those already-charged fixed and scan
allowances by checked componentwise arithmetic, and charge the remainder before
any retained buffer/map allocation or callback copying. M's work is one bounded
composite operation; the sink holds no WorkScope and cannot allocate beyond its
already-funded capacity. The same M operations are not charged again inside it.
T and K continue charging their own scopes normally.

This is not a request-class pre-admission A(Σ) test. CI-3 has already performed
its read/pin work, failures remain operational Budget, and no install-budget
route, new ledger or per-component reset appears. The source guard must prove
the planned operation stays within the funded block.

## Operation-owned slot storage

Let n be admitted component count, S_c the native size of an optional candidate
slot, and S_r the native size of an opaque admitted-component result slot.
The owning operation allocates the two stable arrays once, before borrowing
slots. For n=0 it allocates neither.

For n>0 its actual shared fee is:

```
R(n*S_c) + R(n*S_r) + (0,8n,4n*S_c+2n*S_r)
```

Each component's conservative M bound may include:

```
M_slot(c) = R(S_c) + R(S_r) + (0,8,4*S_c+2*S_r)
```

Summing these dominates the single shared allocation for n≥1. The execution
charges the shared allocation **once**, not each per-component bound. Every
record must distinguish that actual charged sum from the conservative ΣM_slot.
Both native sizes must be published by the exact candidate build, not guessed
from private fields. An empty/no-trust component set charges nothing here.

The admitted set owns component payloads and the separately owned core evidence.
Consumers may receive borrowed `AdmittedClosure::{Component,Core}` views. Such
views duplicate no capability and cannot outlive the owning set/candidate frame.

## Pre-admission core evidence fee

The single-use receipt-owner handoff, on its existing InitialInstallationAttempt
ledger, prepares an
owned opaque bundle containing the four existing role ids, the base core id and
the 16-byte lineage/cohort. Each id is the existing fixed 73-byte closure id.
It makes no new digest, signature or role projection. PlatformReceipt retains a
private taken flag; the handoff constructs the bundle only after charging, marks
the flag on success and returns owned values. No RefCell reference escapes and
the InitialCore itself is not moved or changed. Receipt capture and unrelated
command paths gain no eager allocation.

The proposed fixed fee is five R(73) records, both streams of five id copies,
both streams of the cohort copy, and 128 bounded metadata visits at 32 bytes:

```
objects = 5
edges = 128
bytes = 5*(73+128) + 2*5*73 + 2*16 + 128*32 = 5863
```

Native ABI/source checks and the exact capture/handoff control flow must validate
that fee. The owner scope checks latch state before any handoff; taking twice
is an internal invariant, never a fresh allocation/retry. No partial bundle
escapes on failure. The receipt owner's typed Budget/invariant carrier is preserved.

This is a separately named receipt-owner accounting amendment, not M(c), and
not a charge to R10a's component ledger. The owning analysis setup performs this handoff before its I/trust-view branch
can discard the receipt; core roles remain available in every lawful
no-component-trust case. X-SD9's zero component-admission charge
rule is unchanged. C4 and later consumers retain their same-core/field joins.

## Standing and remaining proof

These formulas select a concrete draft shape for review. Native ABI/lifetime,
allocation/move/source guard, carrier, feature and mutation controls remain
implementation obligations. The full plan must be independently accepted before
product changes. X-SD9-2 needs accepted implemented M and final CI/D4 bounds;
X-SD9-1 still needs the complete aggregate census and its E/V/N outcome. No full
A(Σ), admission coverage, production fit, cap change or qualification is claimed.
