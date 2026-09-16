# Implementation boundaries and build plan

**Standing: author proposal, 2026-09-11; actual Claude review pending.** This
document owns the proposed admission/commit API, build rules and implementation
milestones. [Chapter 14](14-repository-and-module-layout.md) owns package paths,
filenames and naming. The [report inventory](prototype-report-inventory.md) owns
prototype feature dispositions. The [central register](08-decision-and-readiness-register.md#unified-product-design-readiness)
still owns readiness. No product implementation is authorized by these proposals.

The original semantic comparison used frozen candidate25; that provenance is
preserved in [planning sources](implementation-planning-sources.v1.json). Current
planning is bound by the `architecture.manifestPath` and `manifestSha256` in that
record, and the matching `subjectManifest` in [implementation coverage](implementation-coverage.v1.json).
They select the exact normative-input layer, including the integrated identity,
security, native and workflow owners. Historical candidate25 receipts do not
accept a successor, and unbound working mirrors cannot replace its selected bytes.
The selected internal API requires a security SEAL/witness phase before
evidence-ledger commitment. An orphan SEAL is a durable operational artifact,
never a committed Run. The corresponding current normative clauses and pending
implementation qualification govern; final design acceptance and readiness remain
with the central register. Public wire majors and lease modes are unchanged by
this private API selection.

## Admission and authoritative commit

### Decision: require independently minted prerequisites at the storage boundary

A private host wrapper alone cannot prevent another Rust caller of a public
storage crate from submitting unverified records. Select two opaque prerequisites:
the pure evaluator produces a **ReplayedRun**, and security produces a live
**CommitSession**. Storage can publish an authoritative commit only with both,
bound to the same exact target. Host finalization remains the application
coordinator; it does not manufacture either prerequisite from booleans or DTOs.

This changes the proposed source graph: `opensip-storage` depends directly on
`opensip-evaluator` and `opensip-security`, in addition to contracts, identity
and platform. Neither evaluator nor security depends on storage. Lifecycle may
continue to use storage without a reverse storage → lifecycle edge. Security also depends on the pure evaluator to accept its opaque `ReplayedRun`
at the SEAL boundary; a caller-authored RunId is insufficient. The evaluator
remains entirely pure; being called by effectful storage does not give it ports,
callbacks or access to live state. The dependency/footprint tradeoff is explicit
and requires Claude review. Do not create an extra admission crate merely to
hide this edge or weaken full replay to keep a diagram smaller.

These are proposed Rust API type names, not new serialized contracts:

| Type / operation | Constructor and visibility | Invariant |
|---|---|---|
| `RunCandidate` | Inert contract input; callers may construct/deserialize it | Makes no admission claim |
| `ReplayedRun` | Public opaque evaluator type; constructor private to complete replay in `replay.rs` | Contains exact admitted closure, recomputed RunId, retention inventory and selected profile after full semantic reconstruction; no `Default`, deserialization or unchecked constructor |
| `CommitSession` | Public opaque security type; created only by security admission over registered project/store custody, an owned live platform writer guard, actual grants and operation identity | Binds namespace, store generation, ExecutionId, admitted producer closure and permitted operation; acquisition never follows from a Run's semantic grant projection |
| `PreparedCommit` | Public opaque storage type; returned by `prepare_commit(ReplayedRun, CommitSession)` | Owns both prerequisites and the exact binding; checks equality and retention feasibility, then permits only the defined publication sequence |
| `PublishedCommit` | Public opaque storage result; constructor private to durable commit/recovery validation | Contains the exact committed receipt and Run reference after required barriers, not merely after writing blobs or appending SEAL |
| `RecoveredCommit` | Storage recovery result validated against current ledger and objects | Distinguishes confirmed commit, confirmed absence/failure and an inability to establish either; recovery does not repeat source mutation |

Owned guards and commit state are single-use and non-cloneable. Immutable byte
buffers may be shared read-only; the opaque wrapper exposes no mutable interior
or references that let a caller replace a validated object. An owned byte arena
or pinned read-only verified object set can avoid copying the entire closure;
filesystem paths alone cannot freeze it. Accessors provide identities and
read-only values, never a way to construct the prerequisite. Test helpers that
skip admission remain private to unit tests and unavailable in release builds.

`ReplayedRun` establishes semantic validity, not compiler truth, present custody
or current availability. `CommitSession` establishes operational admission, not
semantic validity. Storage compares their target identities, inventories and
producer selections, binds the current attempt and verifies all published bytes.
Changed Plan inputs require new replay. A new attempt using the same semantic
Run still requires a new session and its own ExecutionId/receipt.

The storage crate exports read APIs, cache/index APIs, authorized maintenance
APIs and the guarded commit facade. SQL connections, transaction handles,
ledger-row insertion and receipt constructors remain private modules. Host,
lifecycle and CLI cannot obtain raw writable ledger access through a convenience
method. Maintenance cannot insert an authoritative Run by using a restore or
migration helper: imported evidence is revalidated before local adoption, and
state transitions retain their separate authorization and recovery laws.

This is an API discipline inside the trusted host, not an OS sandbox or a
defense against arbitrary malicious native code running with store access.
Custody, exact-byte admission and actual platform qualification remain necessary.

### Security/storage ownership and the final commit gate

`begin_journal_txn(session: CommitSession)` consumes the session and returns an
opaque `JournalWriteTxn` owned by security. It owns the live session and its
operation lease, has no public SQL/write/checkpoint method and is non-cloneable.
It does not borrow a session that a later call must move. Storage holds this
opaque transaction while acquiring its own non-waiting level-3 ledger transaction.
Failure of that second acquisition calls the security-owned consuming abort path.

`JournalSealBinding` is also defined and privately constructed in security,
not in the inert contracts crate. It exposes read-only actual carrier/generation,
SEAL sequence/body digest, operationRef and replayed Run identity. It is evidence
of that append, never a reusable effect grant. Storage owns the remaining receipt
and inventory values and assembles the thirteen-field association by checking
both owners' exact joins; security does not manufacture storage's receipt counter
or receipt bytes. Neither raw transaction handles nor the append mutex escape.

The security-owned `seal_under_append_lock` consumes `JournalWriteTxn`, borrows
an evaluator-minted `ReplayedRun`, and owns the entire checkpoint/witness sequence.
It uses a two-phase storage adapter, whose concrete implementation and ledger
connection stay private to storage:

1. After the SEAL/witness is durable, an at-most-once staging callback receives
   the opaque `JournalSealBinding`, validates its joins and inserts the exact
   receipt/association in the already-open evidence transaction. It returns an
   owned prepared-ledger-commit adapter. This phase may fail without issuing an
   evidence commit; it must not commit or publish by itself.
2. Security rechecks epoch/freshness and atomically admits commitment only if the
   observer's fail-stop latch has not won. It then consumes the adapter's one
   commit method. All payload admission, association construction and SQL staging
   precede this gate; the method performs only the prepared commit and barriers.

The adapter trait is owned by security, which has no dependency on storage;
its implementation is storage-private. No authority-bearing type lives in
contracts merely to permit another crate to construct private fields. The trait
is an operational collaboration among trusted host modules, not a sandbox for
arbitrary downstream implementations. Storage's public facade accepts neither
an external adapter nor an external `SealOutcome`; callers cannot mint
`PublishedCommit` by returning a fabricated enum. The pure evaluator receives no
callback, port or mutable store handle.

The observer latches fail-stop outside the append mutex when a check fails or
staleness exceeds S6’s bound. Use one atomic bit state with `ADMITTED=1` and
`LATCHED=2`: 0 is preparing, 1 admitted, 2 latched before admission, and 3 admitted
then latched. Commit admission uses compare-exchange 0→1; the observer always
fetch-ORs 2, including 1→3, so a post-admission latch cannot be lost. No state
resets during the attempt. The successful gate mints one internal single-use
permit for the already prepared commit; it is not a reusable grant for later
effects. State 3 does not revoke that already admitted attempt or relabel its
outcome: it records the latch and forbids further effect admission or retries.
A latch winning at state 0 prevents the gate entirely. The observer cannot undo
an in-flight syscall or rewrite its outcome. A confirmed durable commit remains committed; an uncertain
commit/barrier remains durability-undetermined with ExecutionId and no automatic
write retry. This gate orders admission only and is not the durability point.

On any end path, security returns a stopped session that still owns the operation
lease and admits cleanup only, with no further analysis/effect APIs. After level 4
and any still-open ledger transaction are released, the host uses that stopped
session to record pending REV/cleanup through a fresh lawful level-3→level-4 append
while the operation lease still protects cleanup. It then releases the lease and
performs the ordinary S7 end handoff. Capacity exhaustion instead returns typed
`CarrierCapacityExhausted {grantGeneration, provenTailSeq}` through storage to
`host/finalization.rs`; after cleanup and lease release, host routes the required
lifecycle rollover under the fence. Storage never calls lifecycle backwards.

The outer PreparedCommit state has no Drop implementation that prevents moving its owned fields during publish; best-effort rollback/release belongs to the inner guards and ledger transaction. Drop is best-effort rollback/resource release if it runs; `mem::forget`, process
abort and stalled syscalls do not guarantee destructor execution. Those paths
must leave recovery evidence and an honest unavailable/busy result, not a claimed
cleanup success. This design does not infer OS cancellation bounds from Rust types. Because cross-crate adapter traits are public, another trusted security caller could use its own adapter and leave an orphan SEAL without an evidence receipt. Such a SEAL consumes journal capacity and participates in witness/recovery accounting exactly as F36 requires; it cannot manufacture PublishedCommit through storage’s facade.

### Publication sequence and lock discipline

1. Host obtains registered project/store admission and the required writer guard
   through lifecycle/security before source admission. The guard remains owned
   through evaluation and commit. Operational grants precede Plan construction;
   Plan grant descriptors never authorize effects.
2. Native/import admission and the pure evaluator reconstruct the complete Run.
   A failed reconstruction returns its typed failure without producing
   `ReplayedRun`. Explicit ephemeral analysis uses a separate non-authoritative
   result path and cannot call the durable commit facade.
3. Storage binds the two prerequisites and preflights exact replayable retention,
   pins and bounds. It writes verified immutable objects to private temporary
   files, satisfies file barriers, publishes digest-addressed objects and
   satisfies directory barriers. Failure leaves no acknowledged Run.
4. Prepare both carrier write transactions at level 3 in one fixed order:
   security grant-journal first, evidence ledger second, both non-waiting. If
   either acquisition fails, release the earlier transaction. Only then take
   the journal append checkpoint at level 4. It never holds level 4 while
   trying to acquire either level-3 transaction. No lease upgrade or new project/fence
   acquisition occurs inside this path. Existing S7 rules own earlier fence and
   lease acquisition/release and contention handling.
5. Under the journal checkpoint, security checks current custody, relevant trust
   epoch, observer freshness, grants and operation cancellation. The final
   SEAL/commit sequence must linearize with REV: no new SEAL or commit after REV.
   No slow replay, provider execution, network operation or discovery occurs
   while this final lock is held. A short-lived checkpoint is never serialized
   as a reusable authority token.
6. Publish the Run manifest, references, availability, authorized pins, exact
   receipt and private recovery association in one synchronous ledger
   transaction; satisfy all required durability barriers. Only then produce
   `PublishedCommit`. Required rendering/delivery follows commitment and cannot
   rewrite its Run.

**Proposed journal/ledger crash join for review:** persist the validated SEAL
record before ledger commit while holding the final journal lock through the
ledger commit/barrier. Include a private recovery association in that ledger
transaction linking namespace, ExecutionId, RunId, inventory digest, store
generation and the exact journal generation/sequence/record digest. Its values
come from the actual two owners, not caller assertions. The association is local
operational metadata, excluded from semantic hashes, and adds no field to the
closed public receipt or JournalRecord schemas. SEAL alone is not a durable
receipt. A surviving SEAL with no committed ledger row is an uncommitted attempt.
`admit_analysis_seal` validates a record and its Run; it does not establish that
attempt’s durable commitment. F36 requires the orphan attempt to remain
uncommitted after later operations. A later, properly receipted attempt may
commit the same semantic RunId; its new ExecutionId/receipt establishes that
commit and never retroactively confirms the earlier attempt.

This is a concrete proposed carrier join, not a claim that candidate25 already
specifies or implements that private table. Claude must check its compatibility
with the selected journal carrier, operationRef binding, recovery and bounded
revocation rules. The private record shape and ordered fault-injection plan below now make the
proposal concrete. Their carrier implementation/migration still requires review
and real execution before qualification.
If that review requires a normative amendment, freeze and review a successor;
do not silently edit the selected public schemas or weaken the existing laws.

### Failure and recovery account

| Interruption / refusal | Durable state and required behavior |
|---|---|
| Invalid closure or semantic mismatch | No replay prerequisite; no acknowledged Run or fabricated commit receipt |
| Wrong namespace/store generation, substituted Run/inventory or expired operational session | Refuse before authoritative publication; never repair the mismatch by rebinding an existing token |
| Object write/digest/barrier failure | No ledger commit; unreferenced blobs are reconciled under existing GC/custody rules |
| REV/cancellation/freshness failure before commit | Prevent subsequent SEAL/commit according to S6; disclose already completed effects under their own rules |
| Durable SEAL, ledger transaction not committed | No authoritative acknowledgement; recovery requires verified ledger absence before calling the attempt uncommitted; a read failure is not absence |
| Commit/barrier result uncertain, or acknowledgement lost | Return the existing durability-undetermined outcome with ExecutionId; read-only recovery checks the ledger, binding and objects; no automatic mutation retry |
| Receipt confirms commit, later object loss/corruption | Preserve historical sealed assurance and verdict; report current availability and missing references separately |
| Required report projection/rendering fails after commit | Preserve RunId; existing required-delivery operational failure/exit 4 applies |
| Optional browser launch/export fails | Disclose the optional delivery failure according to the selected surface; do not change the sealed result |

Recovery must not use a lone SEAL, a matching cache key or a syntactically valid
RunId as proof of commitment. Conversely, revocation after a confirmed commit
does not erase history. Corrupt or contradictory operational records require
an honest recovery/custody failure under the owning error contract; this design
does not invent a new public error code to conceal an unmapped case.

### Private recovery record and storage-generation binding

The machine-readable [recovery plan](commit-recovery-plan.v1.json) owns the closed
`CommitRecoveryAssociationV1` schema and F00–F53 checkpoint inventory. This is a
local operational record, never a public request, authority token or extension
to a Run/receipt/journal wire schema. All 13 fields are required, with no nulls,
unknown members, implicit defaults, duplicate JSON keys or lossy numeric parsing.
JSON Schema checks shape; the exact lexical and cross-owner checks below still
apply. Merely constructing a schema-valid association grants nothing.

Select a private `StoreGenerationBindingV1` with exactly `{schemaVersion: 1,
namespaceId, storeInstanceId, storeGeneration, stateSchema}`. `namespaceId` is the same exact
1–4096-character registered namespace used by the receipt; `storeInstanceId`
is 32 lowercase hexadecimal characters from 128 bits of OS randomness allocated
once at authorized store creation. `storeGeneration` is exactly the S9.2
admitted `currentStoreGeneration` (`I64NonNegative`), validated against the
transition intent’s `from/toStoreGeneration`; it is not a second counter and it
is not monotonic, because S9.2 `store-rollback`/`core-rollback` re-select a
retained earlier generation. `stateSchema` uses the owning security
`$defs/StateSchema` domain, currently
`{1, 2}`. It widens only through an explicit reviewed successor of that owner
and supported-reader admission, never because a generic integer can encode it.
The binding is custody-protected store metadata; `storeGenerationDigest` is raw
SHA-256 over the exact canonical bytes produced by the one foundation
product-profile canonicalizer of identity §3, selected by security S2 because
this record carries a `schemaVersion`. It is a raw-artifact digest used only for
local correlation, never `H(domain, descriptor)`: it is not a new
public H-domain, semantic identity or proof that a store is trusted. The active
security guard obtains this binding through an admitted handle and registry,
not from request fields. Randomness never enters the pure evaluator or Run hash.
Adding any member would change every historical digest, so this record is frozen
at version 1; a new member needs a V2 plus a reviewed bridge that preserves the
original digests, never a silent in-place edit.

The binding survives ordinary restart, a same-store core update that preserves
the admitted state schema/store generation, and index rebuild.
**Current S9 cannot express this validation, and this proposal does not pretend
otherwise.** `InstallationTransitionIntentV1` (11 members) and
`InstallationTransitionJournalV1` (20 members) are closed with
`additionalProperties: false` and carry no store instance identity, and S9.2's
`registry` is a `NamespaceList` of namespace strings. The minimal S9 owner
successor is therefore authored as an explicit normative insertion —
[two pure `+`-only hunks](store-instance-lineage.v1.json) that remove no line:
the explicit schema/store pair law into S9.2
itself, and a `### S9.3` section after it — and its
private lifecycle companion is specified in
[store-instance lineage](store-instance-lineage.v1.json): a private
`StoreLineageNodeV1` keyed by the admitted binding triple
`(storeInstanceId, storeGeneration, stateSchema)`, carrying its predecessor
triple and the creating `intentDigest` as evidence, written **after** the
transition journal record is durably `COMMITTED`, under the already-required
fence and exact `leaseSet`, adding no member to any closed public, signed or
namespace record and minting no D9 code. `intentDigest` is a semantic input
digest, not an attempt identifier, so it is evidence and never a key: a lawful
retry of a byte-identical intent after an abort writes a different triple or no
node at all. That successor must be frozen and
reviewed; it is not accepted here.

A store instance identity is allocated once per physical store and never
rewritten. Which transitions write a node is read from the admitted intent's own
`from`/`to` values, never from the operation name. The owner's pair law makes
that decidable without consulting any stored record: for `core-update` and
`core-rollback` alike an unchanged schema keeps the store
(`TRANSITION.SAME_SCHEMA_KEEPS_STORE`) and a changed schema selects a different
one (`TRANSITION.SCHEMA_CHANGE_SELECTS_NEW_STORE`), `core-repair` keeps all
three, and both store operations require a schema change *and* a different
generation. So equal `to`/`from` generation and schema keep the same physical
store and write nothing; a **retreating** schema re-selects a retained ancestor
and also writes nothing; only an **advancing** schema materializes a new store,
allocates a fresh identity and writes one node. Deriving the case from the intent
rather than from stored ancestry is deliberate: a case read out of the node set
would let a damaged lineage reclassify a rollback as a forward selection.

Every lookup identifies a node by its **full triple**, whose instance component is
read from the store-root **marker** of the store concerned — the newly
materialized store for a forward selection, the retained ancestor for a
re-selection, the unchanged store for a same-store operation. A numeric
generation pair never identifies a node, because a retained branch may lawfully
present the same pair as a fresh target; no global generation uniqueness is
asserted beyond the owner's own rules. `intentDigest` is evidence checked *on* the
selected node rather than a search key, since the record's own schema says it may
repeat.

Reading a store root yields exactly one of three outcomes — **readable**,
**absent** (no root present) or **unreadable** (a root observed whose marker is
malformed) — and an unreadable marker is never read as absence. The requirement is
**phase-bound**: the store a transition comes from always exists, so its marker is
always required, but the *selected* store's marker is required only where the
owner settles the transition as committed. At `LEASED` and `PREPARING` a forward
target may not yet have been materialized, and after an abort an unpublished target may
already have been reclaimed by the GC census, so an absent target there is expected
and must never be turned into corruption.

One admission law governs both publication and recovery: shape admitted by the
private record's **own closed schema**, paired nulls,
no self-reference, a predecessor that already exists at its exact triple, no
disagreeing duplicate primary key, and an acyclic chain reaching exactly one
lineage root — scoped to that chain, because an authorized restore or adoption
starts its own lineage and several may coexist. An exact byte-identical match at
the target key is idempotent but **not** a short circuit: it is validated the same
way and simply writes nothing. A
refusal writes nothing.

Recovery applies that **same** case and that same admission law, and only after
the owner's own `recover_transition_journal` decision settles the transition as
committed — a core operation at `PREPARED` still aborts, a store operation still
follows the S9 footprint, and where the owner refuses, reports the project busy
or quarantines, the companion makes **no decision, inspects nothing and reads no
marker**. No
atomicity is claimed between the journal record and a node. Only a
forward selection created a node, so only a forward selection is reconstructible,
from the journal's own from/to members plus the two store-root markers; because
the owner forbids a same store there, that reconstruction can never name itself.
A same-store or ancestor re-selection validates the retained node at its own full
triple and **never rewrites its predecessor or origin digest**, with an ancestor
additionally required to lie on the verified chain from the current node: that
node came from an earlier,
unrelated act whose origin the current intent does not carry, so a missing one
cannot be repaired from it and is a custody quarantine. Before the owner settles a
transition, pre-existing ancestry is expected and untouched — including a
retained branch at the same numeric generation — and an absent target is expected
as above. Where a target *is* observable, what must not exist
is a *new* node for that transition **at its own full triple**.

A rollback that re-selects the **same retained physical old store** keeps that
store's original `storeInstanceId`, so
the active `(namespaceId, storeInstanceId, storeGeneration, stateSchema)` tuple
is byte-identical to the pre-migration tuple and every association written
before the forward transition joins the active binding by plain binary equality,
with no lineage walk and no row rewrite. Associations written in the abandoned
forward store keep their own digest and are reached only through the lineage
chain or reported unavailable, which is F35 applied in the reverse direction.

Floors and authority stay with their existing owners, split three ways. An
**authorized S9 transition** keeps S9's rules exactly: a migration copies the
floors forward into the new store, a rollback inside the window sets them to the
maximum of both stores, and a poisoned floor is lowered only by S4.5 — the
instance identity records which store is selected and never lowers a floor. A
**fresh installation** has no predecessor and so inherits nothing. An
**evidence-bundle restore or portable adoption** allocates its own identity,
restores no trust floor and grants no local authority; that rule constrains
restore and adoption only and does not weaken the migration carry-forward above.
The random instance identity
distinguishes separately created/restored stores with coincident numeric
generations; it never replaces lifecycle generation checks or restores a
backup’s local authority. Old commit rows keep their original digest. Historical
lookup follows an admitted migration lineage or reports unavailability; it never
rewrites old rows to pretend they were committed by the new instance. Portable
adoption is a fresh locally authorized attempt, not recovery of local authority
from a backup. Exact lineage validation belongs to lifecycle transitions under
the proposed S9 successor. Logical `stateSchema`, the physical carrier format
owned by the separate versioned-carrier work, and this random instance identity
are three distinct axes; a carrier-format identifier joins the lineage by
`(storeInstanceId, storeGeneration)` and must never enter the binding. A byte
copy of an entire store root is not detected, the same stated bound S5 already
records for a coherent install-root rollback.

Storage owns an append-only association table, inserted **in the same evidence
ledger transaction** as its receipt, Run references, availability and pins.
Primary key: `(storeGenerationDigest, namespaceId, executionId)`. Unique keys:
`(storeGenerationDigest, namespaceId, commitSequence)` and
`(journalCarrierDigest, grantGeneration, journalSeq)`. Keep low-level row insertion
private to the guarded commit facade. No `INSERT OR REPLACE`, mutation-on-read,
unchecked restore constructor or convenience API may bypass these invariants.
Public schema versions are unaffected by this private record's version 1.

Map strings to binary-comparison SQL TEXT and counters within signed-i64 to SQL
INTEGER. `commitSequence` uses canonical decimal TEXT so uint64 receipt values
cannot overflow a signed SQLite integer; require an exact parse/range check and
compare numeric magnitude (length then bytes for canonical nonnegative decimals),
not lexical order alone or REAL conversion. The row's sequence value must equal
the selected receipt's numeric value. The public receipt remains numeric under
its own schema; this explicit private representation is not coercion at admission. The
SQL column also constrains text length to 1..20. One private ledger accessor
owns exact decoding and length-then-binary-byte ordering; raw SQL handles remain
private. No bare lexical `MAX`/`ORDER BY`, `CAST(... AS INTEGER)` or REAL conversion
may order or allocate commits. The association only copies a counter already
allocated by the guarded receipt writer. F37 exercises the 2/9/10/100 ordering
and uint64-maximum conversion counterexamples; source review checks that every
ordering call uses the one accessor.

The host's live session supplies the independent `executionId` ↔ `operationRef`
association. The latter retains security's `op-` plus 32 lowercase hex grammar;
it is not an ExecutionId with a different prefix. Validate the exact namespace,
store binding, Run, inventory, receipt bytes, security carrier, grant generation,
SEAL sequence/body hash and operation binding. Verify receipt schema and
signer/custody, the journal's owner hash chain and the retained replayable objects.
Matching just RunId, a digest or a current database row does not establish those
joins. Metadata canonicalization and product-data canonicalization stay separate.

### Witness-aware publication and read-only recovery

The inherited security v8 §5.4 witness protocol is part of the carrier boundary.
Final SEAL publication must complete its **PENDING witness → journal transaction
commit/barrier → COMMITTED witness** sequence before the evidence-ledger commit.
The broad journal record schema's i64 `seq` allowance does not override the
carrier's uint53 cap or reserved terminal slot: ordinary SEAL uses at most
`9007199254740990`; slot `9007199254740991` remains TERMINAL. Capacity handling
must finish through lifecycle outside the held operation lease, never by taking
its fence backwards inside commit.

The inherited `security-schemas.v2/grant-journal.sql` does not admit SEAL in its
record-type CHECK and still names historical platform aliases. It is historical
carrier evidence, not ready-to-use product DDL. **COV-03** requires an explicitly
versioned product carrier migration that admits current schema-3 SEAL/current
platform records while preserving historical row interpretation, append-only
hash chains, reserved capacity, witness/high-water checks and the S9 reader/core
bridge. Do not disable SQL checks or relabel old rows as current.
**COV-03 resolved (proposed, not accepted):** the versioned carrier is
`docs/coop/design-corrections/security/carrier-format.v3.md` with DDL
`grant-journal.carrier.v3.sql` and dispatch `carrier-dispatch.v3.json`, selected by security
§S1 and bridged by §S9. It adds `carrierFormat` as an axis distinct from `recordSchema` and
`stateSchema`, carries TERMINAL as the frozen recordSchema-1 body so schema 3 is not widened,
uses the four S8 machine ids, and migrates additively. The inherited carrier is incompatible
in exactly two ways, both measured: the `SEAL` record type, and the three alias-only machine
platform ids on a GRANT. Eight of the nine schema-3 operational record types insert cleanly. A journal's own
SQLite transaction is distinct from the evidence ledger transaction; holding
the prescribed lock order does not make the two databases atomically committed.
The proposal orders both level-3 write transactions before the level-4 append
lock: grant journal, then evidence ledger. Every journal writer, including the
revocation observer, must use the same security-owned transaction-before-append
API; no caller may acquire a new journal transaction from inside an append-lock
callback. A failed second acquisition rolls back/releases the first. Committing
the journal releases its DB transaction while the append lock stays held through
the witness and evidence commit; no journal transaction is reacquired there.
Claude must review this refinement against S7 and every inherited journal writer.

Read-only recovery may inspect a consistent ledger snapshot and the admitted
carrier/witness/floor state. It must not perform witness INIT, REVERT or ADVANCE,
raise trust high-water, allocate a store binding or obtain a new execution grant.
If reconciliation of the requested attempt's carrier prefix is needed, report
the owner diagnosis and inability to confirm current local custody; an
authorized lifecycle open performs the lawful mutation,
then a new read-only recovery can retry. The exact bounded algorithm is
`docs/v2/architecture/commit-recovery-readonly.v3.md`. Carrier observations are captured with
before/after stability brackets and at most one fresh journal retry; an owner quarantine
condition is reportable only from stable brackets plus two agreeing tail observations, so a
temporally skewed observation is attributed to busy rather than corruption. Terminality of an
attempt comes from the ledger-owned `AttemptCustodyV1` phase read in the same snapshot as the
receipt, never from an in-memory active set. A confirming result is
`confirmed-under-retained-custody`, never a cryptographic proof of the interior prefix. A mere absent or malformed witness never
licenses repair. The ordinary writer lifecycle's existing start/end high-water
handoff stays separate from a read-only request.

A journal tail ahead of the witness, a missing witness for nonempty history,
a lower-than-observed tail, an equal sequence with different hash, unknown schema
or contradictory receipt/association is a custody/recovery refusal. A verified
empty exact ledger lookup can establish that an attempt did not commit; an
unreadable ledger, another generation, the requested attempt still running or
an unresolved witness for its required prefix cannot. Active-attempt recovery
may report in-progress/undetermined and must not declare a final failure from an
older read snapshot. A valid later append's PENDING witness does not invalidate
an earlier committed receipt: snapshot readers verify its retained durable
prefix and never wait for the writer or repair the newer witness. Ordinary
historical queries do not reuse current execution grants or turn each read into
whole-carrier recovery.

Preserve the recovery association, exact receipt, store-generation lineage and
required journal verification material while their local commitment is retained.
They are operational custody state under G19, not disposable indexes. Removing
or compacting a journal generation requires an explicitly reviewed retained
verification bridge; absence of that bridge prevents deletion. This proposal
does not alter immutable assurance or claim that purge deletes exported copies.

Before the atomic commit-admission gate, recheck the observer latch and
freshness/cancellation after any blocking journal/witness or association-staging
operation. SEAL may already be durable; a failed final checkpoint
latches fail-stop and rolls back the still-uncommitted evidence transaction.
Release the append lock and remaining carrier transaction resources before a
fresh lawful journal append records REV/cleanup under the stopped operation
lease, then release that lease and perform the S7 end handoff; never
reacquire a level-3 journal transaction under level 4. No further effect is
admitted from the failed session. The old SEAL remains an uncommitted attempt. The journal lock
orders REV against commit; it cannot bound an OS syscall stalled indefinitely.
S6 scheduling assumptions and real platform measurements remain required.

<!-- BEGIN GENERATED COMMIT RECOVERY -->

| Private field | Representation | Exact binding |
|---|---|---|
| `recordSchema` | `integer` | Constant 1; reject unknown versions before joins. |
| `storeGenerationDigest` | `hex64` | SHA-256 of exact canonical private StoreGenerationBindingV1; compare with the custody-admitted active or explicitly selected historical store generation. |
| `namespaceId` | `text` | Exact receipt namespace and registered project namespace; binary equality, no path resolution. |
| `executionId` | `execution` | Exact host attempt ExecutionId and receipt executionId; never derived from operationRef. |
| `runId` | `run` | Byte-equal evaluator RunId, SEAL runId and receipt runId; current run3 only. |
| `inventoryDigest` | `hex64` | Exact admitted retention inventory and receipt inventoryDigest. |
| `commitSequence` | `decimal-u64` | Canonical decimal text for receipt commitSequence 0..18446744073709551615; parse as an exact integer, never SQL REAL or JavaScript Number. |
| `receiptBytesSha256` | `hex64` | Raw SHA-256 of the exact stored receipt bytes; verify its selected schema and signer/custody separately. |
| `journalCarrierDigest` | `hex64` | Existing journal projectKeyDigest from the security-owned carrier binding, not a hash of a caller-supplied path. |
| `grantGeneration` | `integer` | Exact positive i64 security generation; inherited metadata range. |
| `journalSeq` | `integer` | Exact ordinary-append sequence; inherited uint53 terminal slot 9007199254740991 stays reserved even though the broader product record shape permits i64. |
| `journalBodySha256` | `hex64` | Exact security carrier body hash of the validated SEAL; verify the owner hash chain and witness, not only this string. |
| `operationRef` | `operation` | Exact security-owned op- plus 32 lowercase hex token from the live session; map explicitly to executionId without changing either grammar. |

### Ordered failure matrix

Conclusions below are internal scenario expectations, not new public D9
codes. An unreadable or contradictory observation always prevents an
uncommitted/committed conclusion. A missing receipt alone is not terminal
absence: that requires settled+refused and both receipt and association
absent in one coherent snapshot. No crash case has been executed.

| Case / interruption | Possible stored state | Expected conclusion and action |
|---|---|---|
| F00 — Before project/store admission | No new source-derived state | refused: No live writer/session; no commit call; reads for diagnosis remain read-only. |
| F01 — Replay refuses or target/inventory is substituted | No authoritative receipt | refused: Neither structural-only validation nor a stale boolean/token can publish authority. |
| F02 — During temporary object write | Partial private temp files; no ledger receipt | unknown-attempt-open: Do not expose partial objects; later authorized reconciliation may remove orphans. |
| F03 — After temp write, before file barrier completes | Temporary bytes may or may not survive | unknown-attempt-open: Never infer durability from write return alone. |
| F04 — After object file barrier, during digest-addressed publication | Some immutable objects may be present | unknown-attempt-open: Verify existing collisions by exact digest/length; never overwrite unequal bytes. |
| F05 — After object publication, before directory barrier completes | Visible names may not survive restart | unknown-attempt-open: No receipt has committed; presence alone grants no authority. |
| F06 — After object barriers, journal/evidence transaction acquisition refused or busy | Durable orphan objects; no ledger receipt | unknown-attempt-open: Acquire journal then evidence level-3 transactions before append lock; if either acquisition fails release earlier resources, apply S7 non-waiting rules and preserve orphan status. |
| F07 — After witness PENDING persist, before SEAL journal transaction | Witness may lead journal tail by one | unknown-attempt-open: Read-only diagnosis reports would-REVERT; only authorized lifecycle open reconciles it. |
| F08 — During SEAL journal append before journal commit | Journal transaction may abort; witness PENDING | unknown-attempt-open: No evidence-ledger commit is permitted yet; validate actual journal tail before deciding REVERT/ADVANCE. |
| F09 — SEAL journal commit outcome unknown | SEAL may be durable, witness PENDING | unknown-attempt-open: Never proceed to evidence commit on an uncertain journal barrier. Read-only receipt absence alone is not a terminal negative; an admitted custody row remains unknown until the separately authorized settlement sweep establishes settled+refused with receipt and association absent in one coherent snapshot. An unreadable ledger remains unknown-custody. |
| F10 — SEAL durable, witness COMMITTED update interrupted | Journal at PENDING target or finalized witness | unknown-attempt-open: Read-only diagnosis reports would-ADVANCE where lawful; no evidence commit until witness finalization succeeds. |
| F11 — SEAL/witness durable, evidence ledger rows partially inserted inside transaction | SEAL exists; receipt/association not yet committed | unknown-attempt-open: Atomic transaction exposes all required rows or none; no commit from a lone SEAL. |
| F12 — Evidence ledger commit syscall returns error/connection lost | Transaction may have committed or aborted | durability-undetermined: Initial caller outcome durability-undetermined, operational-failed/exit4 with ExecutionId. A fresh read-only lookup may establish historical commitment; a terminal negative additionally requires settled+refused and both receipt and association absent in one snapshot. Leave unresolved custody admitted for the authorized sweep; no automatic write retry. |
| F13 — Evidence commit observed before all required carrier barriers confirmed | Durable result not yet established | durability-undetermined: Do not return PublishedCommit; recovery examines actual committed receipt and barrier/carrier state. |
| F14 — All commit barriers completed, acknowledgement lost | Exact receipt and association committed | committed: Fresh read-only lookup confirms historical commitment and separately inspects object availability. A valid joined receipt is committed-historically even while custody remains admitted; disclose pendingSettlement operationally and continue the carrier capture. Settlement is not a prerequisite for recognizing that historical commitment. |
| F15 — Acknowledgement delivered, later process crash | Acknowledged sealed history remains | committed: Do not re-run mutation or create a second receipt for the same attempt during recovery. |
| F16 — Required projection/HTML/output fails after commit | Committed Run remains intact | committed-delivery-failed: Preserve RunId and existing required-delivery operational failure/exit4. |
| F17 — Optional browser launch/export fails after required delivery | Committed Run and required artifact remain | committed: Optional effect failure is disclosed without rewriting result or treating export as required. |
| F18 — REV or observer fail-stop before final SEAL checkpoint | No later SEAL or evidence commit | refused: Disclose already completed external effects under S6; a prior semantic replay token grants no current authority. |
| F19 — Observer stall/freshness failure after SEAL but before evidence commit | SEAL may survive; evidence commit prevented if checkpoint fails | unknown-attempt-open: Recheck after blocking journal/witness work. On failure latch fail-stop, abort evidence transaction, release ordered locks, then record REV through a new lawful journal call; never reacquire level3 under level4. Actual syscall stall bounds require qualification. |
| F20 — Malformed, mismatched or hash-divergent witness | Carrier cannot be admitted | unknown-quarantine-condition: Report an owner quarantine condition only after the bounded stable carrier observations establish it; read-only never writes a quarantine marker, normalizes or repairs malformed bytes. Temporal skew without those observations remains unavailable-busy. |
| F21 — Missing witness with a nonempty journal | Witnessless restore condition | unknown-quarantine-condition: A witnessless restore condition requires stable bounded observations; report unknown-quarantine-condition without a marker write. A matching SEAL or receipt alone does not bypass custody. Temporal skew remains unavailable-busy. |
| F22 — Journal tail below trusted high-water / equal seq different hash | Rollback or uncertain tail loss | unknown-quarantine-condition: Preserve floors and historical bytes; only owner-authorized recovery can reconcile admitted cases. |
| F23 — Only receipt or only association appears committed | Impossible partial transaction or corruption | unknown-custody: Refuse local commitment confirmation; preserve observed rows for diagnosis, do not synthesize the missing partner. |
| F24 — Evidence ledger unreadable or wrong store selected | No reliable lookup conclusion | unknown-custody: Never interpret failed read, wrong generation or empty fallback DB as no commit. |
| F25 — Confirmed receipt, required evidence later missing/corrupt/purged | Historical commitment with changed availability | committed-degraded: Preserve assurance/verdict; disclose exact missing references and current availability, never reseal. |
| F26 — Revocation or expired grants observed after confirmed commit | Historical receipt remains | committed: Confirm history without reusing grants for new effects; current custody still gates reading. |
| F27 — Store-generation/namespace/operation/execution binding swap | Contradictory local association | binding-unusable: Refuse substituted recovery target; compare all independent owner joins, not just RunId. |
| F28 — Journal record pruned or unavailable after retained receipt | Historical record exists but required recovery custody cannot be reconstructed | unknown-custody: Never invent a journal proof or erase the historical receipt. Recovery metadata needs a retention root; lawful migrations preserve its verification lineage. |
| F29 — Reader observes transaction during publication | Committed snapshot excludes in-flight rows | unknown-attempt-open or committed-historically: Readers see old complete state or new complete state; no mixed receipt/association. A later valid PENDING journal append does not block confirmation of an earlier durable prefix. A snapshot missing an actively running requested attempt is not final absence. Apply the single-snapshot phase/outcome matrix; never infer terminal absence from an admitted attempt. The standing is selected from the one snapshot: admitted with neither row is unknown-attempt-open; a valid joined receipt is committed-historically (including pendingSettlement when admitted); a temporally skewed carrier capture that cannot reconcile within the bound is unavailable-busy. These are existing recovery standings, not a new snapshot-dependent public class. |
| F30 — Competing writer or EXCLUSIVE census while APPEND writer active | First admitted writer retains its guard | refused: Exercise actual process lock modes and S7 busy/retry behavior; no waiting/upgrades under the wrong lock. |
| F31 — Journal carrier cannot represent schema3 SEAL/current platform | Carrier incompatibility detected before commit work | refused: Explicit versioned migration required; never insert SEAL into the inherited SQL check set by disabling constraints. |
| F32 — Journal sequence reaches reserved terminal capacity | No ordinary SEAL in terminal slot | refused: Storage returns CarrierCapacityExhausted {grantGeneration, provenTailSeq} to host/finalization.rs. Host completes cleanup and releases the operation lease, then calls lifecycle under its fence to close/roll the generation. No storage-to-lifecycle reverse call, fence acquisition or rollover inside commit. |
| F33 — Receipt/inventory/signature or journal-body join differs | Observed record cannot confirm claimed local commit | unknown-custody: Hash presence alone is insufficient; validate closed schemas, owner digests, signatures/custody and full object inventory. |
| F34 — Duplicate commit request for the same ExecutionId | Existing exact attempt may already be committed | unknown-custody: Route to read-only recovery; compare requested binding exactly and refuse a different binding; do not INSERT OR REPLACE or auto-append a new SEAL. |
| F35 — Explicit store migration/restore with previous receipt associations | Old associations remain tied to old generation | unknown-custody: Use admitted migration lineage for historical lookup or explicit adoption with a new attempt; never rewrite old association IDs to imply new local authority. |
| F36 — Orphan SEAL followed by a later successful operation | An aborted attempt has a valid durable SEAL but no receipt/association; a later attempt commits successfully | unknown-attempt-open: Keep the earlier SEAL as operational history only. It must never become a committed Run in history, receipt, availability or query selection, including after restart or a later commit in the same journal generation. admit_analysis_seal establishes record and Run validity, not durable commitment; only the guarded evidence-ledger receipt/association establishes that attempt’s commit. A later attempt may lawfully commit the same semantic RunId: report that new ExecutionId/receipt as committed while the earlier ExecutionId remains uncommitted. Never globally blacklist a RunId because one attempt left an orphan SEAL. A terminal-not-committed recovery conclusion additionally requires settled+refused and absent receipt/association in the same snapshot; before authorized settlement the historical orphan attempt remains unknown to the reader. After a separately authorized sweep holds the fence and EXCLUSIVE, verifies both rows absent in one readable snapshot, and durably settles refused, a fresh reader reports terminal-not-committed. The earlier unknown standing is explicitly pre-sweep. |
| F37 — Decimal sequence ordering and uint64 conversion boundaries | Associations contain exact text values 0, 2, 9, 10, 100 and 18446744073709551615 | validate-private-accessor: The sole private ordering accessor returns numeric magnitude order and round-trips the full uint64 maximum. Reject leading zeroes, negatives, over-range values and lossy parsing. Exercise the bare lexical MAX/ORDER BY and CAST-to-i64 counterexamples to show why they are forbidden; no allocation decision may use the association column. |
| F38 — Observer latch wins before commit admission (atomic bit state reaches 2), after SEAL/witness durable and after association staging | Durable SEAL and COMMITTED witness; receipt/association staged but never committed | uncommitted: A latch winning at state 0 prevents the gate entirely, so the compare-exchange 0 to 1 fails and no commit permit is ever minted. Distinguish TWO different facts. First, the ACTUAL ABORTED ACTION is known to this attempt: no evidence commit was issued, the staged evidence transaction is aborted, level 4 and both level-3 transactions are released, and a fresh lawful level-3 to level-4 append records REV/CLN under the still-held stopped operation lease. Second, the OBSERVER standing before any sweep is unknown-attempt-open, because a later read-only reader sees no receipt and an attempt row still admitted; the stopped cleanup-only session may not settle it. Those are consistent with F36: the durable SEAL stays operational history and must never become a committed Run, and once the authorized sweep observes a free lease and a readable ledger with neither row present it settles refused, after which the same attempt reads terminal-not-committed. The aborted action is immediate and local; the terminal observer standing arrives only with the sweep. |
| F39 — Observer latch arrives after the atomic 0 to 1 admission (bit state becomes 3) and the commit is later confirmed | Exact receipt and association committed and durable | committed-delivery-failed: State 3 does not revoke the already admitted attempt or relabel its outcome. The commit stays committed and its RunId stays observable. The latch forbids further effect admission and retries, so no new required-delivery phase is started and required delivery is reported through the existing DELIVERY.REQUIRED_FAILED, operational-failed, exit 4 path. With no latch (state 1) the same commit proceeds to a normal successful required-delivery phase in SHARED-READ mode, drawing no authority from the returned stopped cleanup-only session. A failed or latching attempt cannot reacquire authority by opening a delivery phase. |
| F40 — Commit syscall returns an error or a required barrier is unconfirmed, with or without a concurrent latch | Transaction may have committed or aborted | durability-undetermined: Report DURABILITY.COMMIT_FAILED, operational-failed, exit 4. Retain ExecutionId for correlation and omit runId, because RunId is externally observable only for a committed Run. A latch does not convert this into uncommitted. TWO SENSES OF TERMINAL must not be conflated: the D9 law that a settled ExecutionId is terminal means no retry of that attempt is ever admitted and a later attempt receives a fresh ExecutionId; it does NOT mean the private attempt-custody phase is settled. This attempt is D9-terminal to its caller while its custody row remains admitted, and the authorized settlement sweep is what later resolves that row to committed or refused. A later read-only recovery may therefore establish committed or, after the sweep, terminal-not-committed. |
| F41 — Latch and commit admission race on the one atomic bit state, across every interleaving | Either no evidence commit was issued, or exactly one was | single-winner-invariant: States stay within 0..3 and never reset during the attempt. Commit admission is compare-exchange 0 to 1 and fails from state 2. The observer always fetch-ORs 2, including 1 to 3, so a post-admission latch is never lost and the fetch-OR is idempotent and never clears ADMITTED. The successful gate mints one single-use permit: a second consume, including any retry path, obtains no commit. No effect is admitted while latched. Exercise the real atomic primitive with deterministic synchronisation, not only a model. |
| F42 — mem::forget, process abort or an indefinitely stalled syscall on the commit path | Any state; no destructor is guaranteed to have run | unknown-custody: Drop is best-effort only, and the outer prepared-commit state has no Drop that prevents moving its owned fields during publish. These paths must leave recovery evidence and return an honest unavailable or busy result, never a claimed cleanup success. Recovery in a fresh process reads the actual stored bytes and returns a verified conclusion or unknown-custody. No OS cancellation bound may be inferred from Rust types. An attempt left in the admitted phase by such a path stays unknown until an authorized sweep settles it. |
| F43 — Read-only recovery ordering hazard: the association journalSeq exceeds the observed journal tail | Journal read snapshot older than the evidence ledger snapshot, or the tail was lost | unavailable-busy: Take exactly one fresh capture and re-read tail, witness and floor; never re-read the ledger. If reconciled, continue. If still ahead and the floor lastSeq is at or above the requested sequence with two agreeing tail observations, report the F22 quarantine condition. Otherwise return unavailable or busy attributed to the security carrier owner. Never conclude uncommitted, and never draw a conclusion from two different snapshots. |
| F44 — Prefix anchor with a PENDING witness at the next slot and the requested sequence above the SC-TRUST floor | Durable prefix exists but no live witnessed anchor names it; a newer append is in flight | unknown-custody: Report unknown, explicitly not invalidated. An earlier committed receipt is never invalidated by a newer PENDING append. Report the witnessWouldRevert diagnosis and perform no REVERT, no ADVANCE, no witness write and no high-water raise. Do not wait on the writer. |
| F45 — Prefix anchor with a PENDING witness at the tail carrying the tail body digest | The append became durable before the witness was advanced | committed-historically: The witness still names the durable tail, so it anchors it. Confirm for any requested sequence at or below the tail under anchor class witness-pending-at-tail, provided the witness bracket was byte-stable. Report witnessWouldAdvance as a diagnosis and perform no ADVANCE. The conclusion class is confirmed-under-retained-custody, never a cryptographic proof, and every confirming result carries the interior-bodies-not-authenticated diagnosis. |
| F46 — The generation holding the requested attempt is carrierFormat 1 or 2 | Historical generation in which no schema-3 SEAL row can exist | unknown-carrier-incompatible: Report carrier incompatibility, never not-committed and never uncommitted. Read historical bytes under recordSchema-1 semantics only; never relabel them as schema 3 and never present a historical platform alias as an S8 machine id. This is the read-side counterpart of F31. Note the measured scope: the inherited carrier refuses exactly the SEAL record type and the three alias-only machine platform ids, and admits the other eight schema-3 operational types. |
| F47 — Carrier-format migration from 1 or 2 to 3 | Inherited generation closed by TERMINAL; new carrierFormat 3 objects present | migrated: TERMINAL closes the inherited generation under the inherited constraints with no constraint or trigger disabled and no row rewritten. The TERMINAL row carries the migration operation own op- token, never a released analysis operation ref. Inherited rows and inherited schema objects stay byte-unchanged and legacy platform aliases are retained verbatim. A write to a generation below first_generation is refused. Run the whole transition under the install fence with non-blocking EXCLUSIVE on the affected project namespace. NO installation transition intent or journal is written: the closed 11-member intent and 20-member journal have no carrier field, reusing store-migrate is refused MIGRATE_REQUIRES_SCHEMA_ADVANCE and SCHEMA_CHANGE_SELECTS_NEW_STORE, and an invented carrier-migrate operation is refused by the closed operation enum. The footprint is self-describing from the three durable acts plus the operationRef already inside the frozen TERMINAL body. |
| F48 — Post-migration open and read dispatch, including a core that does not support carrierFormat 3 | carrierFormat 3 carrier present | refused: A carrierFormat-AWARE core that supports only formats 1 and 2 refuses a carrierFormat 3 carrier typed and keeps its prior generation until it expires, mirroring the S9 dual-reader staging. A FORMAT-UNAWARE core cannot be made to refuse at all, because it never looks for carrier_format; that limitation is selected and disclosed, detectable but not preventable, and its mitigation is the existing ordered-release discipline. A carrierFormat 1-2-3 core applies the selected dispatch in order: observe object NAMES only; refuse MIGRATION.CORRUPT on a partial name set; refuse MIGRATION.CORRUPT when all seven names are present but any definition is invalid; only then read the format row; then verify the frozen side-table SQL text, the carrier projectKeyDigest and the generation boundary; then read both historical and current generations without relabelling either. |
| F49 — Concurrency capture races during read-only recovery: a lawful concurrent APPEND-WRITE advances the witness, tail or floor between the reader's own observations, and a writer commits and exits after the reader's ledger snapshot | Carrier is entirely lawful; the reader's independently timed observations are mutually skewed, and its ledger snapshot may predate a commit that then completes | unavailable-busy: Two separate laws. First, an adverse witness or floor observation is a reportable owner quarantine condition only when both bracketing reads are byte-identical AND two journal snapshots agree on the tail sequence and tail digest; otherwise it is attributed to temporal skew and reported busy. A lawful later append must never produce a corruption diagnosis, and the reader must never invent one from independently timed observations. Second, terminality comes from the ledger-owned AttemptCustodyV1 phase read in the SAME snapshot as the receipt; no in-memory active set or separately timed liveness probe is consulted, so a stale snapshot plus later inactivity never yields a terminal not-committed conclusion. Bound the whole protocol to one ledger snapshot, at most two journal snapshots, at most four witness and four floor reads, no lock, no wait on the writer and no mutation. Exercise real concurrent processes, not only the model. |
| F50 — Carrier-format migration interrupted after any durable prefix of TERMINAL append, object creation and format-row publication | One-sided footprint: generation closed with no new objects; or objects present with no format row; or complete | resume-exact-prefix: Each of the three durable acts is atomic and the physical state is self-describing, so there is no torn state to repair. Act B is ONE explicit transaction on the same connection: BEGIN, every statement, COMMIT, ROLLBACK on failure. A bulk-script execution is NOT an acceptable act B, because it issues an implicit COMMIT and then runs statements one at a time, leaving earlier objects durable. Detection reads object NAMES first, refuses MIGRATION.CORRUPT on a partial set or on all-names-with-invalid-definitions, and reads the carrier_format ROW only after that, so objects without a published row still read as the inherited format. Prefix empty starts at A, or at B on a fresh install with no inherited table; prefix A resumes at B, recomputing the closed generation; prefix AB validates the existing definitions and resumes at C; prefix ABC is complete. first_generation is recomputed at C, never fixed earlier. COMMIT OR BARRIER UNCERTAINTY STOPS THE ATTEMPT: it performs cleanup only, releases EXCLUSIVE then the fence and writes nothing further; progress requires a separately admitted fresh maintenance attempt with its own migrationOpRef, re-acquiring fence and EXCLUSIVE, which resumes from the observed durable prefix. The same operation never retries an act or proceeds to the next. A TERMINAL naming a previous attempt operationRef is lawful history to resume past, never something to redo, and the inherited trigger independently refuses any append to a TERMINAL generation. Object existence is a resume signal, never the recovery mechanism. |
| F51 — A format-unaware core opens or writes a migrated carrier | A generation at or above first_generation appears in the INHERITED table | split-brain-custody-condition: Prevention is impossible within the inherited format, which has no mechanism to refuse, and claiming otherwise would be an overclaim. Detection is exact: any generation at or above first_generation in the inherited table is a custody condition, never valid history, and is never merged into the current generation sequence. The mitigation is the existing ordered-release pattern, shipping the format-aware core first and enabling migration only once the selected core generation is at or above that release. For carrierFormat 1 the limit is wider because that format has no TERMINAL-closure trigger, so rows after the TERMINAL are also a custody condition. |
| F52 — Read-only recovery over every AttemptCustodyV1 phase and outcome against receipt and association presence | Any of the eleven settlement-matrix combinations, including a purged historical receipt | negative-only-from-settled-refused: terminal-not-committed requires ALL of: phase settled, settledOutcome exactly refused, and both the receipt and the association confirmed absent, in ONE coherent ledger snapshot. A settled-committed row with no receipt is a contradiction and unavailable history, never a negative. A receipt present while the attempt row is still admitted is the LAWFUL pre-settle interval, because the settle write is ordered after the receipt write: it answers committed-historically with pendingSettlement disclosed operationally, revives no authority, and no writer may reopen a stopped session merely to settle it. A present receipt with NO attempt-custody row and no legacy custody record answers committed-historically for commitment and custody-unknown-legacy for settlement, never a negative. Exactly one matrix cell yields the negative. A purged historical receipt never becomes never-committed: a logical retained tombstone or manifest that still names the Run is committed with degraded availability, which is a different observation from a raw both-absent snapshot, and no receipt is ever forged from a tombstone. There is no undetermined custody outcome: a durability-uncertain attempt stays admitted, and durability-undetermined is the D9 response to the caller. |
| F53 — The authorized settlement sweep over live, crashed, one-sided, inaccessible and already-settled attempts | Attempts left admitted by crashed, latching or durability-uncertain writers | settle-only-on-proof: The sweep runs as a per-namespace step of the existing store-gc operation under the install fence with non-blocking EXCLUSIVE, which is what proves no writer for the namespace is live. It reads ONE coherent ledger snapshot and writes only committed or refused, never undetermined, and at most one transition per attempt. It writes nothing when the lease is busy (skip and retain), when the ledger is unreadable, when the ledger is one-sided, or when the row is already settled. It reuses none of the dead attempt authority, obtains no new execution grant and never retries the commit. Permissible cleanup is the existing reachability GC of unreferenced orphan objects only; it may never synthesize a receipt or association, append a SEAL, raise the high-water, write or repair the witness, roll a grant generation or revive a grant. A failed, latching or durability-uncertain attempt must never open another write transaction with its stopped session; it releases and leaves the row admitted for the sweep. |

<!-- END GENERATED COMMIT RECOVERY -->

### Required API and fault-injection checks

`crates/host/tests/admission_tests.rs` owns public-boundary scenarios;
`crates/storage/tests/commit_tests.rs` owns the real carrier crash matrix;
private evaluator/security unit tests own prerequisite construction. Verify:

- Raw DTOs, a boolean `verified`, structural-only validation and a serialized
  previous session cannot enter the commit facade. Include compile-fail API
  fixtures once the test harness is selected, plus behavioral rejection checks.
- Alter any admitted input, inventory, namespace, execution or generation at
  the handoff; no acknowledged authority results. Exercise live revocation and
  stale-guard behavior with deterministic synchronization.
- Interrupt before/after every object barrier, SEAL append/barrier, ledger
  transaction/barrier and acknowledgement. Recover in a fresh process using
  actual stored bytes; distinguish orphan attempts, historical commitment and unknown custody.
- Concurrent readers see a consistent committed snapshot; a competing writer
  or exclusive operation follows S7 contention rules without a reversed lock
  acquisition. Releasing an object drops guards in the specified order.
- An identity-valid but replay-invalid candidate never publishes authority.
  Loss of report assets after commitment does not change its evidence or verdict.

These are required future implementation checks, not tests run in this design
task. Reference-model success cannot establish OS durability or process isolation.

## Build, generation and dependency rules

### Independently selectable build lanes

| Lane | Source roots and prerequisites | Output / isolation requirement |
|---|---|---|
| Host libraries and CLI development | Root Cargo workspace: `apps/cli` and selected `crates/*`; root lockfile/toolchain | Native host and package tests; neither provider compiler integration nor Node/report build is an implicit Cargo build-script prerequisite |
| Rust provider | Separate `providers/rust` workspace, lockfile and toolchain; exact shared pure library sources | Provider executable plus its declared runtime/compiler/standard-library assets; host build does not compile rustc integration |
| TypeScript provider | Its own TS package and pinned compiler/runtime dependencies | Provider executable/launch payload and sealed runtime closure; no browser/report imports or frontend build requirement |
| Browser report | `apps/report` and generated projection binding | Self-contained asset bundle and compatibility descriptor; no provider or host runtime imports |
| Contract generation | Selected schema source registry and pinned generator closure | Rust/TS carriers, TS runtime shape validation and module indexes; deterministic drift check across every declared output |
| Product release assembly | Explicitly chosen native binaries, report assets, providers, storage and trust inputs | Signed exact offline closure and compatibility/TCB inventory; source directory adjacency does not establish compatibility |

The default product release remains authoritative-capable. A management-only
installation is explicit and refuses analysis until its required signed closure
is installed through the authorized lifecycle. Optional development build lanes
must not become a new preview product, silently omit required capabilities from
a release, or download missing tools at runtime.

**Rust workspace policy.** Shared pure packages must be usable from the pinned
provider workspace without accidentally inheriting the root workspace's compiler
or dependency settings. Their distributable manifests explicitly resolve package
metadata and dependencies; source-package assembly may materialize inherited
values, but the isolated provider build must prove they resolve without the host
workspace. Each workspace's lockfile is authoritative for that build. Shared
library/API compatibility, each wire major and toolchain support are separate
axes; a new host release does not force a provider release. Build inputs may
include immutable exported source packages from the one owner; never maintain
editable provider copies of shared contracts.

**TypeScript policy.** Root scripts may coordinate the provider and report, but
must expose independent build/test targets. Select one package manager and
lockfile strategy before scaffolding; do not check in competing lockfiles. A
shared lockfile is acceptable only if each lane can install/build its declared
closure without running the other's scripts or requiring its toolchain. Provider
Node and browser DOM environments have separate compiler settings. Runtime
imports, type-only imports and generated inputs all appear in dependency checks;
type-only imports cannot hide duplicate schema ownership.

**Generation policy.** Select checked-in generated bindings for the initial
implementation: ordinary builds can consume reviewed bindings without running a
generator or fetching schemas. Generated headers identify their owner and recipe;
the registry pins source digest/ID/profile, generator version/closure and options,
output target and semantic validator owner. The generation lane regenerates into
a clean temporary directory and compares bytes with the checked-in outputs.
Changes to a source/recipe must update every affected consumer in the same change.
Only explicit registry membership determines outputs; no glob over historical
schema versions. Generators must not resolve remote references implicitly.

**Asset policy.** Generated JS/CSS bundles and release binaries are build outputs,
not checked-in application source. Report assembly emits a manifest of exact
asset bytes, projection compatibility and license/notice inputs. The host consumes
that manifest through an explicit build/release input; a Cargo build script must
not invoke an ambient package manager or contact the network. A source build can
use locally built assets; a verified prebuilt bundle is another explicit input.
Development host tests may use labelled fixture assets. A product release must
fail assembly if its selected report asset bundle is missing or incompatible.
Rendering a required output fails honestly if the installed assets are unusable.

### Compiler-free syntax owner and retained grammar inputs

Select pure `crates/syntax`, depending only on contracts and identity, with an
explicit host → syntax dependency. It takes immutable admitted source and grammar
bytes and returns inert candidates. It performs no filesystem discovery, compiler
lookup, process execution, trust admission or authoritative Coverage construction.
`host/syntax.rs` dispatches; `host/fact_admission.rs` checks source/context,
occupancy, relation-at-rung and Coverage joins before ordinary evaluation. Parser
code linked into the host is part of the declared native host TCB, not evidence
that its candidate assertions are already admitted.

Static linking does not remove the retained `kind=grammar` closure obligation.
The admitted `SyntaxGrammarBundleV1.parserVersion` equals its signed closure
manifest’s semanticVersion. Retain its exact manifest, grammar definitions and
normalizer bytes; a compiled-in grammar with no retained closure is insufficient.
The syntax universe commits its context and selected grammar set. Refuse an
unbundled grammar; use the unique longest selected suffix and exact
`grammarVariant` for body identity. Compiler and grammar bodies retain distinct
identity dialects. The current closed registry covers seven language families
and fourteen suffixes: Rust/TS/JS are code; JSON/TOML/Markdown/YAML are data with
no code-body/clone output. Syntax-only analysis retains `resolutionAttempted=false`.
Only the selected inventory/syntactic/normalized-clone relations are supported;
semantic requests do not silently fall back. New grammars or relations require a
reviewed registry successor, not ambient plugin discovery.

### Provider release joins and shared contracts

Provider source isolation does not change installed admission. Each selected
provider/toolchain/stdlib/Rust-dev-LLVM/grammar artifact has the existing exact
`closure2` identity over kind, manifest digest, tree, semanticVersion,
protocolMajor and platform. Its component manifest, signature-envelope2
(`opensip.metadata.manifest.1`) and TR-INDEX-signed catalog bind the selected
platform tree and RJ-3 entrypoint. `DetectorManifestV1` is a compatibility listing,
not a component manifest. Identity Blob members project regular files only;
directory/symlink rows remain delivery metadata and are never followed into the
identity listing. Preserve exact bytes, lengths and mode-bearing delivery trees.

TS compilerVersion equals the admitted toolchain closure semanticVersion;
compilerPackageDigest identifies its exact member and the stdlib identifier is
the selected stdlib closure’s bare hash suffix with the complete retained `.d.ts`
inventory. Rust retains the analogous compiler/Rust-dev-LLVM joins. Source
releases may be independent, but every build/package must declare these exact
compatible inputs; neither PATH nor a system compiler supplies an implicit
fallback. Current worker protocols are TS2/Rust3. Reuse shared identity tokens,
HelloV3 framing and generated contract carriers. No additional provider SDK is
selected merely to hide their distinct protocol obligations.

### Closed generation registry and complete output coverage

Select `{schemaVersion: 1, sources, recipes}` as the closed registry. A source row
has exactly `{sourcePath, sourceSha256, schemaId, declaredMajor, profile,
semanticValidatorOwner}`. Its path names a canonical repository-relative regular
file; sourceSha256 is raw SHA-256 of the complete exact document, not a fragment
or reserialization. Schema ID, positive declared major and explicit profile match
the selected source owner. If the document has no such declaration, record the
explicit reviewed owner mapping rather than deriving it from a filename.
Source digests are unique keys; all source/recipe/path lists use explicit stable
ordering and reject duplicate JSON keys and unknown fields.

A recipe row has exactly `{recipeId, generatorClosureSha256, optionsPath,
optionsSha256, sourceSha256s, outputs}`. The nonempty unique recipe ID identifies
a hermetic generator closure and exact options-file bytes by lowercase SHA-256.
`sourceSha256s` is a sorted nonempty unique list of registered source keys, so a
single output may depend on several schema documents without duplicate output
ownership. All transitive schema references must resolve within the recipe’s
registered inputs; no implicit remote lookup or historical-version glob. The
registry bytes themselves are also an explicit generation input, enabling module
indexes without a self-referential source digest stored in the registry.

`outputs` is a nonempty path-sorted list of closed `{path, language, roles}` rows.
Language is `rust` or `typescript`; roles is a sorted nonempty unique subset of
`carrier`, `shape-validator`, `module-index`. Each output path is globally unique
and belongs to its declared consumer’s generated directory. The initial recipe
covers all eight generated inventory files. `generated/mod.rs` has module-index
role and lists exactly its recipe’s declared sibling Rust modules;
`apps/report/src/generated/report.ts` has both carrier and shape-validator roles.
The Rust generated files provide inert carriers; handwritten Rust admission
owners retain shape/canonical/cross-object checks. The build lane does not claim
unlisted generated Rust runtime validators. Additional recipes may share schema
sources, but never write the same output or read another recipe’s undeclared
outputs. Their exact inputs and own module-index populations remain explicit.

Every generated inventory path must occur exactly once in these output rows;
there are no exceptions for index modules or files combining roles. Regenerate
all recipes into one fresh temporary output tree and compare every declared byte
with the checked-in outputs. Schema/recipe changes update all affected consumers
together. SemanticValidatorOwner identifies handwritten exact admission separately;
generated shape checking never proves lexical canonicalization, content identity
or complete semantic replay. Actual generator/library selection and source/closure
pin population occur at M1 before creating generated product files, using this
accepted row contract and a drift trial that exercises all eight target files.

### Report assets bind to a host-embedded pin in the signed release

Report assets are build outputs shipped in the host release tree. They introduce
no producer `closure2.kind` or semantic Run dependency. Load-time integrity uses
a build-embedded `HostAssetPinV1` constant inside the trusted host binary, holding
the exact length and raw SHA-256 of its private asset manifest. The code validates
that pin before admitting the listed assets.

Install-time provenance has a separate existing owner: the TR-CORE signed file
inventory and release ceremony incorporated by security v1 §3.2/3.3 and retained
by security v8 §2.1. The successor restores the exact incorporated
`distribution-core-inventory-contract.v16.json` input omitted from candidate25.
Its `inventorySchema` covers the mandatory runtime/data file closure; release
assembly includes the selected report manifest and assets there explicitly.
It is distinct from the component-only DR-103 TreeCommitment and does not supply
a CORE-specific catalog-row schema. Architecture and release engineering own
that inventory/assembly through DR-101 and the product-release-assembly lane;
security owns trust admission and lifecycle owns installation. This work is
separate from the grant-journal carrier correction. The selected load-time pin
needs no new CORE manifest field or signature-envelope kind. The current
admission contract §5 item7 keeps the default release authoritative-capable;
restoring the older inventory input does not revert it to management-only.
[Report asset binding](report-asset-binding.v1.json) owns the closed private
schemas, the anchor comparison and the rejected alternatives. Use the selected
machine platform rows (`linux-x86_64-gnu`, `linux-aarch64-gnu`, `macos-aarch64`,
`macos-x86_64`); identical browser bytes may be shared across archives, but no
new `platform-independent` platform vocabulary is introduced.

The private report asset manifest has exactly `{schemaVersion: 1,
projectionSchemaSha256s, assets}`. The schema-digest list is nonempty, sorted and
unique, containing raw SHA-256 of complete supported report projection schemas.
`assets` is a nonempty canonical-path-sorted list of closed
`{path, sha256, bytes, role}` regular-file rows, with globally unique paths,
exact nonnegative integer byte lengths and lowercase SHA-256. Roles are
`script`, `style`, `font`, `image` or `notice`; license/notice files are exact
retained members too. Paths are relative to the release tree and cannot escape
it. Rows are regular files only; a directory or symlink at a listed path refuses
and no symlink is followed, matching the identity rule that `type=dir` and
`type=symlink` stay delivery rows. No URL fetch, duplicate JSON key or unknown
manifest field is permitted. The manifest **never lists itself**: a row whose
path equals the pinned `assetManifestPath` refuses, and completeness reads
"every regular file under the asset root except exactly that one pinned path".
The exclusion is by exact path equality, never a prefix or filename pattern, so
coverage stays total — every byte under the root is covered either by an asset
row's digest or by the manifest's own independent pin, and the self-referential
digest can never arise. Build assembly validates all joins, refuses when
the selected bundle is missing or incompatible, and compiles the manifest's
exact length and raw SHA-256 into the host binary as `HostAssetPinV1` with its
`buildChannel`. No second untrusted self-declaration is introduced, and no
catalog is consulted at render time.

At load, and only when an asset-consuming renderer has been selected,
`reporting/assets.rs` resolves the manifest under the pinned release-relative
root through safe handles, reads it length-bounded, requires byte equality with
the compiled-in digest, then checks projection-schema compatibility and each
selected member’s length and digest before use. No caller, request, environment
variable or configuration file supplies any of those paths. Trust/installation
belongs to lifecycle and security, not the renderer; `assets.rs` verifies no
signature and grants nothing.
The build never invokes an ambient package manager or contacts the network.
Missing/incompatible/corrupt required assets use the existing required-delivery
operational failure (`operational-failed`, exit 4, `faultCause=delivery-required`,
`DELIVERY.REQUIRED_FAILED`); after a committed Run the existing
`DELIVERY.RENDERER_FAILED_AFTER_COMMIT` detail applies and the RunId is
preserved, and otherwise no RunId is invented. No D9 code, class, exit or detail
is minted. Absent assets never affect a human/JSON/agent/SARIF invocation, and a
required HTML request is never silently downgraded to another format. When only
an **optional** surface cannot use the assets, the aggregate termination is
**unchanged**: §8's aggregate is computed over required steps only and an
optional step's failure never changes it, so a `policy-failed` 1 or
`indeterminate` 3 outcome stays exactly that and is not reset to `success` 0.
The optional failure is disclosed on its own surface and neither raises nor
lowers the class.
Development
fixtures are labelled and cannot masquerade as a signed product release. Asset
packaging is a delivery input; it neither changes native context nor creates an
additional semantic producer identity.

### Enforcement and verification

1. Compare actual direct Cargo normal/build/dev dependencies, target-conditioned
   edges and activated features with the inventory's permitted graph. Record
   dev-only exceptions explicitly; do not silently broaden a production edge.
   Inspect transitive effects/build scripts of pure-layer external libraries.
2. Check TS imports and package exports against provider/browser boundaries.
   Check scripts and generation/asset edges as well as import graphs. Detect
   reverse edges, undeclared sibling source imports and provider toolchains
   entering the host's build closure.
3. Build each lane from a clean input manifest with dependencies materialized
   beforehand; an offline rebuild must not fetch missing inputs. Record source,
   lockfile, compiler, generator, platform and asset identities. Do not claim
   bit-for-bit reproducibility until measured; deterministic findings and
   reproducible release binaries are different properties.
4. Assemble each advertised product profile from exact compatible artifacts and
   test installation/analysis with blocked egress. Record mandatory and incremental
   sizes, help/version startup, memory and actual loader dependencies under the
   existing qualification gates; importing a pure crate is not a size measurement.
5. Run independent schema/protocol/output conformance vectors, built-browser
   offline/accessibility checks and real process/storage failure scenarios.
   A root `tests/` README links executable owners; it is not an executable harness.

The pending tool choice list is finite: supported toolchain versions, TS package
manager/lock layout, frontend/bundler, schema generator/runtime-validator tool,
dependency checker, browser/compile-fail/OS harnesses, and release adapter.
Select them against these rules and existing qualification requirements before
the corresponding implementation milestone. This document does not adopt the
prototype's framework, dependency versions or lockstep release train by default.

## Implementation milestones after design acceptance

These are dependency-ordered work packages, not dates or separate product designs.
M0 is required before product implementation; later milestones establish partial
engineering results until the full selected product and its gates pass. Paths
refer to the [canonical file inventory](repository-file-inventory.v1.json).

| Milestone | Prerequisites and deliverable | Main files / boundaries | Demonstration of completion |
|---|---|---|---|
| M0 — accepted implementation contract | Resolve actual external review, successor/blind-consumer/application obligations and the public API/carrier join; choose tools needed for M1 | This document, chapter 14, report inventory, final source map and readiness register | Actual scoped acceptance and complete readiness reconciliation; no author-only replacement |
| M1 — isolated build and contracts | M0; implement independent workspaces, generation registry/drift checks, minimal CLI parsing and command-scoped bootstrap | Root/provider manifests; contracts generated modules; identity canonical/digest modules; CLI arguments/bootstrap, pure host outcomes, human and JSON renderers; schema registry | Each build lane selects only declared inputs; help/version human and JSON metadata share the pure envelope projection without project/provider/store/network effects; version closure IDs come from the build-embedded signed release descriptor, not loaded components; independent identity vectors pass |
| M2 — admission and durable publication | M1; pure replay plus live security guards, storage facade and selected carrier recovery join | Evaluator replay; security commit_authority; storage commit/ledger/blob/recovery; host fact_admission/finalization | Opaque API refusal tests and actual crash/lock/revocation matrix pass; synthetic fixtures remain labelled, not compiler qualification |
| M3 — native analysis core | M2 and provider build lanes; discovery/configuration, sealed snapshot/Plan, supervised TS/JS and Rust analysis and the guarded durable host pipeline | Host discovery/snapshot/plan/analysis; components protocols; both providers and evaluator | Selected native matrix/corpora, missing-role disclosures, cancellation, semantic admission and host-boundary durability checks; neither language silently dropped. Complete CLI analysis delivery follows at M4 with every advertised renderer |
| M4 — coherent report and historical exploration | M3; complete default/analyze/recommend delivery with all advertised formats, common projections, report assets, exact retained selections and disposable index behavior | Reporting projection/renderers; report views/data; host query/comparison; storage index_store | Complete M4 command/format pairs and common renderer behavior; later M5 commands exercise their pairs at M5. The full applicability sets remain HTML for default/analyze/fit/audit/candidates/inspect/review-brief/repair-preview and SARIF for default/analyze/audit/repair-verify. Include offline browser, report dispositions and exact historical availability scenarios |
| M5 — complete workflows and lifecycle | M3–M4; baseline/delta gating, evidence imports, policy/waivers, authorized execution/repair, agent and management surfaces | Host workflow modules; lifecycle/security; storage maintenance | Every selected command and outcome accounted; mutation/retry/recovery, independent releases, trust and pin handling tested |
| M6 — release qualification | All earlier milestones and every selected product requirement | Release tools and tests/qualification owners | Actual signed offline closure, exact-byte/loader, startup/size/memory, native quality, performance and all required gate evidence; no omitted gate inferred waived |

Report UI fixture work and provider extraction work may proceed independently
after their accepted interfaces exist; M2/M3 joins still gate authoritative claims.
The named files are main responsibility owners, not a complete task checklist.
The coverage owner fixes `milestoneOrder` and `moduleFirstMilestone` for delivery-bearing command/query/renderer/capability/golden rows. A row cannot move before its declared module prerequisite. Every command delivery also waits for all of its advertised renderer milestones; each workflow golden waits for its command. Intermediate milestones are development checkpoints, not releases with silently reduced format contracts. Section-routing and gate-preparation milestones are planning responsibilities; gate execution still belongs to M6. The checker enforces this declared schedule and test-versus-document ownership, not semantic completeness of a module or the correctness of an arbitrarily rewritten schedule.

Implementation planning must expand each selected command, native capability,
protocol, carrier and all 32 standing gate accounts into its executable work;
this table cannot silently redefine old preview gates or mark future gates passed.

## Implementation coverage account

[Implementation coverage](implementation-coverage.v1.json) owns the source-bound
mapping from selected commands, query operations, native cells, gates, contract
sections and Fallow/Hydra/report requirements to milestones, modules and planned
verification. It binds whole source records, including nested flags, format and
parity requirements, and preserves every capability/mode state, limitation,
deficiency, corpus case and platform family. The 66 cells expand over four
platform families and selected profile/fixture/grammar populations; 66 is not a
qualified-runner or performance-case count.

This is **ownership and test-plan coverage**. The 55 top-level contract sections
route all their descendants and incorporated owners, but this mapping is not a
complete enumeration or execution of every prose predicate. Per-predicate branch
coverage and independent consumer reconstruction remain separate obligations.
Qualification rows name the owning harness specification until executable harnesses
exist; a README path is not a test. All 32 gates remain unqualified. Their full
product expansions govern, including G26's applicability successor rather than
its historical blanket SARIF exclusion. D9 implementation and golden coverage
are required across M3–M5, not implicitly closed by an output table.

The review found and accounted for these concrete gaps:

| Finding | Proposed correction / remaining review |
|---|---|
| COV-01 — compiler-free analysis lacked a source owner | Add host `syntax.rs` and explicit TS syntax/reachability modules. Syntax mode works without a TS/Rust compilation unit; code/data grammars and typed unsupported rungs stay distinct. Review backend placement and signed grammar closure before implementation; no new provider protocol is silently selected |
| COV-02 — four current command example strings still say run2 | Correct baseline-adopt, repair-preview, test-run and purge examples to their selected Run3 surface in a reviewed successor. Preserve candidate25; no compatibility acceptance of run2 is inferred from stale text |
| COV-03 — inherited journal SQL cannot carry product SEAL | Version/migrate the actual carrier with current record/platform handling and witness/sequence preservation; add a security `journal_store.rs` owner, distinct from lifecycle's transition journal |
| XA-03 — purged-evidence golden shares the existing route overlap | Keep the exit2 source golden pinned as evidence, but do not freeze it as the graph-query expected result until the existing applicability correction settles exact selectors. The graph-specific owner currently returns exit4 |

<!-- BEGIN GENERATED IMPLEMENTATION COVERAGE -->

| Source population | Mapped entries | Standing |
|---|---:|---|
| `commands` | 45 | Ownership/verification routing; not executed |
| `queryOperations` | 20 | Ownership/verification routing; not executed |
| `capabilityCells` | 66 | Ownership/verification routing; not executed |
| `qualificationGates` | 32 | Ownership/verification routing; not executed |
| `sharedFlags` | 7 | Ownership/verification routing; not executed |
| `renderers` | 5 | Ownership/verification routing; not executed |
| `workflowGoldens` | 43 | Ownership/verification routing; not executed |
| `contractSections` | 55 | Ownership/verification routing; not executed |
| `fallowConstraints` | 15 | Ownership/verification routing; not executed |
| `hydraProposals` | 8 | Ownership/verification routing; not executed |
| `reportFeatures` | 24 | Ownership/verification routing; not executed |

### Command routing

| Command | Milestone | Main owner |
|---|---|---|
| `default` | M4 | `crates/host/src/analysis.rs` |
| `recommend` | M4 | `crates/host/src/discovery.rs` |
| `analyze` | M4 | `crates/host/src/analysis.rs` |
| `fit` | M4 | `crates/host/src/review.rs` |
| `audit` | M5 | `crates/host/src/comparison.rs` |
| `query` | M4 | `crates/host/src/query.rs` |
| `import` | M5 | `crates/host/src/imports.rs` |
| `baseline-adopt` | M5 | `crates/host/src/baselines.rs` |
| `baseline-export` | M5 | `crates/host/src/baselines.rs` |
| `baseline-show` | M5 | `crates/host/src/baselines.rs` |
| `baseline-upgrade` | M5 | `crates/host/src/baselines.rs` |
| `policy-show` | M5 | `crates/host/src/policy.rs` |
| `policy-init` | M5 | `crates/host/src/policy.rs` |
| `policy-test` | M5 | `crates/host/src/policy.rs` |
| `waive` | M5 | `crates/host/src/policy.rs` |
| `candidates` | M5 | `crates/host/src/review.rs` |
| `inspect` | M5 | `crates/host/src/review.rs` |
| `review-brief` | M5 | `crates/host/src/review.rs` |
| `review-join` | M5 | `crates/host/src/review.rs` |
| `repair-preview` | M5 | `crates/host/src/repair.rs` |
| `repair-apply` | M5 | `crates/host/src/repair.rs` |
| `repair-verify` | M5 | `crates/host/src/repair.rs` |
| `repair-recover` | M5 | `crates/host/src/repair.rs` |
| `test-run` | M5 | `crates/host/src/execution.rs` |
| `install` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `update` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `doctor` | M5 | `crates/lifecycle/src/doctor.rs`, `crates/security/src/trust_time.rs` |
| `purge` | M5 | `crates/host/src/maintenance.rs` |
| `agent-serve` | M5 | `crates/host/src/agent_server.rs` |
| `help` | M1 | `apps/cli/src/arguments.rs`, `apps/cli/src/bootstrap.rs`, `crates/host/src/outcomes.rs`, `crates/reporting/src/json_renderer.rs`, `crates/reporting/src/human_renderer.rs` |
| `version` | M1 | `apps/cli/src/arguments.rs`, `apps/cli/src/bootstrap.rs`, `crates/host/src/outcomes.rs`, `crates/reporting/src/json_renderer.rs`, `crates/reporting/src/human_renderer.rs` |
| `completion` | M1 | `apps/cli/src/arguments.rs`, `apps/cli/src/bootstrap.rs`, `crates/reporting/src/human_renderer.rs`, `crates/host/src/outcomes.rs` |
| `trust-recovery-challenge` | M5 | `crates/security/src/trust.rs`, `crates/security/src/trust_time.rs` |
| `trust-recovery-import` | M5 | `crates/security/src/trust.rs`, `crates/security/src/trust_time.rs` |
| `trust-refresh` | M5 | `crates/security/src/trust.rs`, `crates/security/src/trust_time.rs` |
| `trust-import` | M5 | `crates/security/src/trust.rs`, `crates/security/src/trust_time.rs` |
| `trust-doctor` | M5 | `crates/lifecycle/src/doctor.rs`, `crates/security/src/trust_time.rs` |
| `store-migrate` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `store-rollback` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `store-gc` | M5 | `crates/host/src/maintenance.rs` |
| `store-status` | M5 | `crates/host/src/maintenance.rs` |
| `native-prepare` | M5 | `crates/host/src/execution.rs` |
| `core-update` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `core-repair` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |
| `core-rollback` | M5 | `crates/lifecycle/src/transitions.rs`, `crates/lifecycle/src/installation.rs` |

### Qualification routing

Every gate still requires actual M6 qualification. Earlier milestones name
the implementation owner; source thresholds and full-product expansion stay
in the pinned gate account and the machine-readable mapping.

| Gate | Implementation milestone | Main owners |
|---|---|---|
| DR-G01 | M6 | `tools/README.md` |
| DR-G02 | M6 | `tools/README.md` |
| DR-G03 | M1 | `apps/cli/src/bootstrap.rs` |
| DR-G04 | M6 | `apps/cli/src/bootstrap.rs` |
| DR-G05 | M6 | `tools/README.md` |
| DR-G06 | M6 | `crates/lifecycle/src/installation.rs`, `crates/host/src/analysis.rs` |
| DR-G07 | M2 | `crates/platform/src/filesystem.rs`, `crates/security/src/custody.rs` |
| DR-G08 | M5 | `crates/security/src/trust.rs`, `crates/security/src/revocation.rs` |
| DR-G09 | M2 | `crates/security/src/grants.rs`, `crates/host/src/execution.rs` |
| DR-G10 | M3 | `crates/components/src/provider_protocol.rs`, `crates/components/src/control_protocol.rs` |
| DR-G11 | M2 | `crates/storage/src/commit.rs`, `crates/storage/src/recovery.rs` |
| DR-G12 | M5 | `crates/lifecycle/src/doctor.rs`, `crates/host/src/maintenance.rs` |
| DR-G13 | M3 | `providers/typescript/src/compiler-adapter.ts`, `providers/rust/src/compiler_adapter.rs`, `crates/host/src/syntax.rs`, `crates/syntax/src/grammar.rs`, `crates/syntax/src/candidates.rs` |
| DR-G14 | M3 | `crates/lifecycle/src/installation.rs`, `tools/README.md` |
| DR-G15 | M1 | `tools/README.md` |
| DR-G16 | M1 | `tools/README.md` |
| DR-G17 | M4 | `crates/reporting/src/projection.rs`, `crates/host/src/delivery.rs` |
| DR-G18 | M5 | `crates/lifecycle/src/journal_store.rs`, `crates/lifecycle/src/leases.rs`, `crates/lifecycle/src/transitions.rs`, `crates/security/src/journal_store.rs` |
| DR-G19 | M2 | `crates/lifecycle/src/journal_store.rs`, `crates/security/src/journal_store.rs`, `crates/storage/src/availability.rs`, `crates/storage/src/blob_store.rs`, `crates/storage/src/commit.rs`, `crates/storage/src/index_store.rs`, `crates/storage/src/ledger_store.rs`, `crates/storage/src/recovery.rs` |
| DR-G20 | M5 | `crates/host/src/configuration.rs`, `crates/host/src/invocation.rs`, `crates/host/src/outcomes.rs` |
| DR-G21 | M3 | `crates/components/src/supervisor.rs` |
| DR-G22 | M6 | `crates/platform/src/process.rs`, `tools/README.md` |
| DR-G23 | M3 | `crates/host/src/fact_admission.rs`, `crates/evaluator/src/replay.rs` |
| DR-G24 | M2 | `crates/evaluator/src/policy.rs`, `crates/host/src/configuration.rs` |
| DR-G25 | M3 | `crates/host/src/fact_admission.rs`, `crates/host/src/outcomes.rs` |
| DR-G26 | M4 | `apps/cli/src/arguments.rs`, `crates/host/src/query.rs`, `crates/host/src/request.rs`, `crates/reporting/src/renderer_factory.rs` |
| DR-G27 | M2 | `crates/host/src/finalization.rs`, `crates/storage/src/commit.rs` |
| DR-G28 | M5 | `crates/evaluator/src/composition.rs`, `crates/host/src/outcomes.rs` |
| DR-G29 | M3 | `crates/host/src/request.rs`, `crates/components/src/manifest.rs` |
| DR-G30 | M6 | `crates/lifecycle/src/installation.rs`, `crates/host/src/analysis.rs` |
| DR-G31 | M1 | `crates/identity/src/descriptors.rs`, `crates/host/src/request.rs` |
| DR-G32 | M5 | `crates/security/src/grants.rs`, `crates/host/src/request.rs` |

<!-- END GENERATED IMPLEMENTATION COVERAGE -->

The checker verifies source-set equality, exact selectors/value digests,
milestone/owner references, untouched native/gate metadata and generated tables:

```sh
python3 -I -B docs/operations/check_implementation_planning.py --source /path/to/frozen-candidate
```

Add `--write` only to regenerate the two marked sections from their JSON owners.
It verifies the selected source files against the exact normative-input manifest
named by `implementation-coverage.v1.json`; the final candidate manifest also
binds that input layer and the planning records. It does not rerun the original
architecture/reference suite or qualify behavior.
Future successor selection requires an explicit source rebind and review of the
delta, not copying new hashes over unresolved findings.

## Tooling decision matrix

These are candidates and acceptance criteria for review, not installed tools,
chosen versions or compatibility claims against OpenSIP's actual schemas. Public
capabilities below were checked against primary documentation on 2026-09-11;
our preferred trial order is an engineering judgment. Record exact versions and
license/dependency closures when a candidate is selected.

| Decision / candidates | Tradeoff and proposed trial | Required acceptance evidence / decision point |
|---|---|---|
| Rust schema bindings: Typify versus a narrowly scoped schema-to-Rust adapter | Start by testing a schema-first generator against the exact selected registry; keep semantic validators separate. Typify generates Rust types from schemas, but that is not proof it preserves every OpenSIP constraint ([Typify](https://docs.rs/typify/latest/typify/)) | At M1, exercise refs/combinators, closed records, optional versus null, exact integer limits and deterministic output. Refuse unsupported constructs rather than dropping them. A custom adapter must justify its maintenance cost |
| TS declarations: json-schema-to-typescript versus a shared custom generator | Test generated declarations from the same schema owners as Rust; avoid reversing schema ownership to handwritten TS/Rust models ([project documentation](https://github.com/bcherny/json-schema-to-typescript)) | At M1, pin each output to source/profile, check supported constructs and compile provider/browser consumers. Declarations are not runtime validation |
| Browser runtime shape validation: Ajv standalone versus a registry-specific generated validator | Trial build-time generated validation so the report need not compile schemas at startup. Ajv documents standalone output, draft-specific instances and strict handling of unknown/ambiguous schema constructs ([standalone](https://ajv.js.org/standalone.html), [draft support](https://ajv.js.org/json-schema.html), [strict mode](https://ajv.js.org/strict-mode.html)) | Before M4, test exact dialects, registered annotations and generated-runtime dependencies; no coercion/default insertion/removal. Establish lossless parsing for u64/duplicate-key/lexical laws before validation; native JSON Number parsing cannot serve as exact admission. Do not change a public numeric field to a string just to fit the tool |
| Rust dependencies: Cargo metadata plus explicit source/build rules | Use Cargo's machine-readable dependency graph as input to the declared-edge checker; supplement it with build-script/source import and feature/target analysis ([Cargo metadata](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html)) | At M1, prove rejection of a forbidden normal/build/dev/target/feature edge and provider compiler leakage. A dependency list alone does not prove evaluator purity |
| TS dependencies: dependency-cruiser versus a compiler-API rule checker | Trial established import-rule enforcement; a compiler-based custom checker is justified only for gaps in the declared boundaries ([dependency-cruiser](https://github.com/sverweij/dependency-cruiser)) | At M1, cover runtime/type-only/dynamic imports, aliases, exports, generated inputs and scripts. No unsupported resolution silently treated as no edge |
| Browser behavior: Playwright plus deterministic DOM unit tests | Use a real browser for offline assets, interaction, accessibility and download behavior; retain smaller pure tests for projections. Playwright documents network routing and the service-worker interception caveat ([network testing](https://playwright.dev/docs/network)) | Before M4, test file-based offline opening, block external egress and service workers, detect attempted fetches, hostile text, large/partial payloads, keyboard/focus and optional renderer loss. DOM-only tests do not establish browser/OS behavior |
| Rust opaque API misuse: trybuild versus isolated Cargo compile-fail fixtures | Trial compile-fail examples at the public crate boundary; trybuild provides that test style ([trybuild](https://docs.rs/trybuild/latest/trybuild/)) | At M2, raw DTO, forged receipt, cloned/reused session and private-constructor attempts must fail for the intended reason. Behavioral tests still check stale valid tokens and effects |
| Storage/process faults: real carrier harness versus an in-memory scheduling model | Use deterministic synchronization and crash barriers against actual storage/processes for qualification. Models can explore orderings while preserving reference-only standing | At M2/M6, execute F00–F53 plus native OS witness/restore/census cases. Record platform/filesystem/profile, actual state bytes and exact outcomes; inject before/after each durability step, without sleep-and-hope synchronization |
| TS package manager / lock topology | Compare one shared lock with isolated immutable lane installs against per-lane lockfiles. Select one coherent policy; no incidental prototype tool/version inheritance | At M1, prove provider-only/report-only builds exclude each other's scripts/toolchain, offline input materialization, drift and a usable contributor workflow; select actual manager/version after the trial |
| Frontend/bundler and graph renderer | Compare framework-free DOM plus a small bundler against a framework where report complexity warrants it; compare bundled graph assets with a simpler renderer | Before M4, use R01–R24 interaction/size/accessibility cases on the same data. No external asset fetch, browser analysis authority or duplicated schema owner; measure size/startup before declaring a winner |
| Release orchestration | Prefer thin adapters over the native build lanes and one common signed assembly contract; compare a larger task runner only against demonstrated orchestration needs | At M1/M6, exact inputs/outputs, compatibility, license/TCB inventory, reproducibility evidence and no hidden downloads. No new signing scheme, credential model or remote release service is selected |

For each trial retain the exact input set, candidate/tool version, configuration,
observed failures and accepted limitations. No candidate passes by popularity or
by producing compilable output while losing a contract constraint. These trials
belong to the corresponding authorized implementation work after M0, not this
document-only planning task. Claude should review the criteria and trial order
with the pending schema, carrier and frontend decisions.

## Historical author verification checkpoints

On 2026-09-11, the inventory checker passed for 186 unique paths and the generated
chapter. Four additional negative controls rejected duplicate paths, an effectful
pure-layer edge, a security/storage cycle and incorrect nested ownership. All 44
prototype file hashes matched both the clean pinned checkout and commit objects;
all six selected architectural file hashes matched candidate25's pinned manifest.
The 24 report feature IDs, 53 pinned prototype links, 60 local documentation links
and whitespace checks passed. This verifies source identity and planning
consistency, not full-source comprehension, prototype execution or product tests.

The same-day recovery/coverage follow-up passed both planning checkers with 190
inventory paths, 320 exact source-bound mapping rows, 13 private record fields
and 36 planned fault cases. Twenty negative controls rejected missing populations,
invalid owners, changed native/golden metadata, false execution claims and broken
recovery bookkeeping. All 44 prototype and 15 selected candidate25 source hashes
matched their original bytes; 62 local links and whitespace checks passed. The
prototype remains clean. These counts are planning validation, not crash tests,
per-predicate proof coverage or qualified native measurements.

## Current author verification after the fresh planning review

The current inventory has 198 proposed files in 20 groups, 320 source-bound
ownership mappings and 54 planned recovery cases. Earlier counts above are dated
historical checkpoints, not the current totals. All recovery cases remain
unexecuted product obligations. Actual Claude’s fresh planning review compiled
the API shape and confirmed the dependency/visibility design; its PS01–PS08
findings and the carrier/discovery/root corrections are integrated as author work
and require final source rebinding and fresh independent changed-byte review. No implementation readiness is claimed.

## Questions reserved for actual Claude

- Assess the two-prerequisite storage API and new storage → evaluator/security
  edges. Can any normal exported API or maintenance route bypass full replay or
  current authorization? Is each token's constructor and lifetime owned correctly?
- Check the 13-field recovery association, store-generation binding and F00–F53
  matrix; examine both level-3 transaction acquisitions before the level-4 append
  lock, witness mutation authority, observer stalls and nonblocking historical
  reads. Resolve COV-03 carrier migration against S6/S7 and the selected schemas.
- Check independent build lanes, checked-in binding/drift policy, release asset
  closure and shared-library/toolchain compatibility; challenge unnecessary crates.
- Review every prototype report disposition and the resulting module additions;
  confirm required projection parity and historical identity survive UI migration.
- Check all 320 mapping entries against the final accepted source populations
  and existing gate standing; address COV-01/02 and the corrected XA-03 graph/finding.show scope.
  Review tooling candidates/trial criteria and resolve decisions before M1/M2.

This is an additional nonblind author-review input. Bind final bytes at dispatch,
preserve the substantive Claude response and re-review material corrections.
