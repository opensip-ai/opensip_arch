# C2a-3 retained closure admission: working implementation plan

Draft, not accepted or implemented. This file does not enable production admission.
Exact starting authorities and source snapshots are in `INPUTS.json`.

## Authority and intended result

C2a plan r4 requires an unforgeable `AdmittedClosure` sum type. Its component
branch is constructed only after delivery custody, whole retention and C2a-3k
verification; its core branch comes only from authenticated InitialCore role
projections. Neither a candidate nor a digest-only assertion grants admission.
CI r5 and accepted CI-3/CI-3L supply the retained tree and verified transfer.

SD-9 r2 is **accepted**, despite the preserved draft heading in its README:
the accepted unit record, independent review, manifest and all manifest members
were rehashed during preparation. Its Q5 selection is the existing bounded
`snapshot_profile()` interim. X-SD9-1 and X-SD9-2 remain mandatory; no complete
census or production-fit claim follows. SD-9 expressly assigns the retained-byte
representation and M(c) price to this plan.

The selected first implementation preserves the complete existing transfer and
in-memory re-hash shape. CI-3 verifies on open; every Blob is transferred through
its retained capability; C2a-3k verifies all retained slices and the authenticated
manifest body. This plan removes no check and proposes no streaming replacement.

## Ownership and crate placement

Add the operational component admission wrapper in lifecycle, which already
depends on security and owns CI-3. Security must not depend on lifecycle.

Expose the existing pure `verify_retained_tree` kernel through a narrow security
export. It continues to accept concrete borrowed map/slice inputs, charge the
borrowed scope and return only a verification result. It mints no operational
custody or admission token. Existing kernel behavior and charge controls remain.

Lifecycle owns an opaque admitted-component payload containing the borrowed
candidate and its real `RetainedTree`. Its fields and constructor are private;
the public admission function is the sole component constructor. Do not derive
Clone, Default or Deserialize. Do not export a constructor from raw ids, paths,
schema values, booleans, arbitrary byte maps or a user-supplied custody trait.

The public `AdmittedClosure` enum has `Component(opaque admitted component)` and
`Core(opaque authenticated core projection)` branches. Security supplies the core
evidence through a trust-owned bridge: only the authenticated InitialCore owner
constructs that bounded opaque evidence from the existing four role ids, without
re-hashing or accepting caller ids. The receipt/read owner explicitly prices
the bounded single-use handoff before the separate admission ledger starts; no RefCell borrow
escapes. See DESIGN-DECISIONS-r1.md for the proposed handoff and cohort join. The bridge must work when there is no
component trust view. It grants none of C3/C4/H/E/X12d's field-use permissions.
The proposed owner entrypoints and visibility are pinned in EXPORT-MAP-r1.md;
their concrete Rust implementation remains subject to source/native review.

## Candidate lifetime and refusal order

CI-3's evidence and returned tree currently borrow the candidate id. Do not make
a self-referential admitted-set object and do not introduce unsafe lifetime
extension or change CI-3's borrowed-name representation to hide this constraint.

The operation owns stable candidate slots outside the lexical R10a result. After
the admitted component count is known, it reserves exactly that many
`Option<ClosureCandidate>` slots on R10a's single ledger. It does not push,
reserve or resize that storage after capabilities begin borrowing it.

Process the slots with a disjoint mutable-slot iterator. For each component in
the established owning order, construct its candidate in its slot and then
perform its retention/admission before proceeding to the next component. This
preserves the first component's retention refusal ahead of a later component's
candidate refusal. Eagerly building every candidate first is not substituted.

The resulting admitted set borrows the operation's slots and holds the retained
capabilities. The outer operation keeps both through selection and supervisor
settlement; the admitted set drops before candidate storage. On any admission
failure, every completed private capability and pin drops, and no partial set
escapes. C2a-4 must provide the owning operation frame; this library does not
invent a production caller, draw or reservation.

A compile-pass borrowing control and compile-fail controls for moving slots,
growing storage after borrowing, returning a set beyond storage lifetime and
using a capability after its owner drops are required. If the exact public
lifetimes cannot express this pattern safely, stop for a reviewed interface
correction before implementing an alternate ownership scheme.

## Per-component algorithm

1. Accept an ordinary-reader `AuthenticatedComponent`, its matching candidate,
   selected platform, component store, pin request and caller's borrowed scope.
   Do not construct or reset a ledger here.
2. Open through `open_retained_tree`. Preserve its association, custody, pin,
   installed-mode, structure, link, length, digest, I/O and Budget partitions.
   A missing installation is distinguished from every promised-tree failure.
3. Fund the fixed and metadata-scan stages in M-BOUND-r1.md, determine F, B, P
   and E, then charge the checked complete remainder before any buffer or map
   allocation. Candidate order and paths are borrowed, not copied.
4. For each Blob, use its already-funded bounded sink allocation and callback/copy
   allowance before creating the buffer and before calling `transfer` for that
   exact path. Keep the entire unverified buffer private. No byte is committed
   to a map or admitted value before successful verified completion.
5. The sink never holds a `WorkScope`: transfer already borrows the same scope.
   Its callbacks allocate nothing beyond the pre-reserved maximum, append no
   more than the expected length, and record sticky state. Overflow, a length
   mismatch, repeated/invalid begin or completion, or unverified completion
   cannot become an accepted prefix. Inspect sink state after transfer even
   when transfer returned success. A transfer failure retains its own cause.
6. Once all buffers are verified, use the already-funded map allocation/search/
   insertion allowance to construct `BTreeMap<&str, &[u8]>` by explicit
   inserts. Do not use a bulk `collect` implementation with unpriced temporary
   allocations. Paths and slices borrow the candidate and owned buffer vector.
7. Invoke the same C2a-3k kernel over that map and the ordinary reader's body.
   Missing, length, digest and body-digest controls all remain required. No
   manifest body is reconstructed, canonicalized or signed again.
8. Only on success construct the opaque admitted component. Drop the temporary
   map and byte buffers, retain the pinned CI-3 capability and candidate borrow.
   Ledger consumption is not refunded when temporary allocations drop.

FAILURE-CONVERSIONS-r2.md fixes the exported failure sum, payload-free Invariant
and exhaustive normalization of every Budget source to the top-level Budget.
No sink error invents a public route. Proposed internal sink invariant failures
need an explicit existing owner projection before source implementation; they
must not be casually relabelled as not-installed or as a native digest failure.

## M(c) representation and price work

M(c) is separate from C2a-1, B_open, transfer T and kernel K. It includes only the
new retained representation and its copying, dispatch, allocation, insertion and
comparison work. The same work is never charged in both M and a CI owner price.

Let F be the Blob count, b_i its byte lengths, P the maximum borrowed path byte
length, and H = 1 + bit_length(F). Use checked sums/products throughout. On any
unrepresentable length or allowance, refuse through the existing latched Budget
path before allocation, never by truncation or as a blob length mismatch.

The proposed categories are:

| Category | Bound to derive and pin before acceptance of the implementation |
|---|---|
| Buffer index | one published owned-record allowance for `F * size_of::<Vec<u8>>()` |
| Payload storage | sum of the published owned-record allowance for every b_i |
| Sink copy | sum of b_i byte copies, plus bounded begin/chunk/finish dispatch; chunk calls bounded by CI's exact `env(b_i) = 2*ceil(b_i/65536)+2` |
| Borrowed map nodes | a sourced maximum live/transient node count, with pinned Rust 1.95 node layouts for `(&str, &[u8])`; no key or payload string is owned here |
| Map search and insertion | per insert at most `11*H` key comparisons, each reserving both path byte streams; node movement and parent-link repairs priced separately from comparisons |
| Representation verification | every local length/state/association check not already charged by CI or K |
| Admission-set storage | operation-private candidate slots and retained-capability result slots, charged once for the set and conservatively represented in the aggregate owner bound |

The complete proposed formulas and source-category table are now in
`M-BOUND-r1.md`. `M-STORAGE-PROOF-r1.md` gives the conditional node/layout
sub-proof; `check_m_bound.py` checks staged fee arithmetic, shared slot
accounting, overflow and the receipt fee. These are draft design evidence, not
an implemented price or a native ABI result. The node/copy/control allowances
must survive independent source review and concrete implementation checks.
No X-SD9-2 completion or production fit follows from the formulas alone.

The plan preserves SD-9's distinction between exact charged calls and conservative
bounds. Tests independently enumerate charges actually made and compare them to
the owner bound; they do not assume equality to the bound. Shared set allocations
must have one explicit aggregate accounting location, not disappear between the
per-component M rows.

## Required controls and evidence

- Every supported role through the existing synthetic ordinary trust path,
  candidate, installed fixture store, CI-3 open/transfer and unchanged kernel.
  Analyzer tests use only the existing fixture selection predicate; they mint
  no production analyzer protocol selection and add no root/key/feature.
- Whole-tree and authenticated-body success, zero-length Blob, multiple Blobs,
  nested paths, borrowed path ordering and exact id/descriptor preservation.
- Not-installed versus promised corrupt/missing/type/mode/link/pin/custody
  causes, interrupted/short reads and I/O, plus transfer failure latching.
- Sink overflow, invalid callback order, incomplete/unverified completion and
  a late digest failure: no accepted prefix or externally visible partial bytes.
- Independent kernel controls for wrong/missing bytes, length, raw digest and
  body digest. Mutants removing any check must be detected for its own reason.
- Explicit WorkFailure::Budget and TreeReadFailure::Budget normalization to
  top-level Budget, preservation of every non-Budget tree cause, and public
  collector-fault privacy controls (FAILURE-CONVERSIONS-r2.md).
- Budget exhaustion at buffer reservation, payload reservation, map work, CI
  open, transfer and K; keep Budget latched, drop earlier pins, return no partial
  admitted set and never start another ledger.
- Two components on one scope, with a failure in the second releasing the first.
  Preserve per-component refusal order and avoid hidden preflight admission.
- Opaque-type construction and lifetime compile controls; no raw-id/candidate
  conversion into admitted authority; no production use of fixture constructors.
- Authenticated core-role provenance and CRC-1 values, including no component
  trust view. Manifest/catalog/store availability is not a core prerequisite.
- Independent source/ABI/allocation proof for M, exact actual charge records,
  model/bound conformance, and source guard against unpriced operations.
- Owning-lane tests, relevant feature/default/release exports, format and denied
  warnings lint, adversarial controls, and separate independent unit review.
- Inventory, exact accepted-byte integration, effective contract/descriptions,
  and source/census impact classification before any receipt claims.

C2a-4/J3d/J2c retain actual pre-draw row-11 projection and reservation controls
SD9-T1 through T5. This library plan does not claim those path controls.

## Proposed work order

1. Freeze the working plan, proposed M formulas, source proof, failure/core
   decisions and exact export/feature map. Obtain independent plan acceptance
   before product changes; close any source/accounting findings first.
2. Implement the narrow security kernel export/core evidence bridge and lifecycle
   admitted wrapper, private bounded sink and explicit retained representation
   in an isolated checkout. Preserve all other drafts and queued jobs.
3. Obtain source/recipe preflight, then separate bounded native validation assent.
   Every compiler, build, physical fixture, format and lint action uses the
   existing global native lane. Pure models are clearly labelled.
4. Close findings and independently accept the exact library bytes. Integrate
   and bind inventories only under the existing project workflow.
5. Materialize C2a-4 under SD-9, preserving X-SD9-1/X-SD9-2. A complete aggregate
   census needs final M plus accepted CI and D4 bounds. No production admission,
   qualified first-party release or end-to-end fit is inferred from library tests.

## Draft completion gates still open

Independent acceptance of the proposed source-category bounds, export/feature
map and complete plan remain open. Native ABI/lifetime, actual carrier and every
implementation result remain open. No C2b/C1c protected draft is edited. The D5
and C2b running/queued validations remain authoritative and unchanged.
