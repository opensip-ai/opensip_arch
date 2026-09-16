# Bounded carrier correction — coauthor report

**Standing.** Non-blind actual Claude coauthor output for a bounded design/reference carrier
correction. This is not an acceptance, not a readiness statement, not a blind-consumer
acceptance, not a final application acceptance and not a self-acceptance. It is not product
implementation. Root assesses and integrates; a fresh substantive review on the frozen successor
bytes remains pending and is not pre-empted here.

**Bindings, verified before work.** Four bound inputs, all four SHA-256 and byte lengths match
`input-manifest.json`. Frozen Source25 manifest
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`, with all **12869** members
swept and verified (0 missing, 0 mismatched, 735108187 bytes). Two files exist on disk outside the
manifest, both `__pycache__` byte-compiled artifacts from a prior session; disclosed, benign, not
manifest members. Comparison throughout is against the **Source25** contract mirrors, not any
current repository mirror.

## 1. Deliverables

Added, under `scratch/proposal/` (7 files, hashed in `scratch/output-manifest.json`):

| File | Role |
|---|---|
| `docs/coop/design-corrections/security/carrier-format.v3.md` | normative carrier correction: axes, defects, resolution, migration, dispatch, digest/chain pinning, anchor bound |
| `docs/coop/design-corrections/security/grant-journal.carrier.v3.sql` | the new physical DDL |
| `docs/coop/design-corrections/security/carrier-dispatch.v3.json` | machine-readable open/read/migration dispatch |
| `docs/coop/design-corrections/security/carrier-highwater.schema.v1.json` | closed shape for the SC-TRUST per-carrier floor |
| `docs/coop/design-corrections/security/check-carrier-v3.py` | reference validator (82 checks) |
| `docs/v2/architecture/commit-recovery-readonly.v1.md` | the bounded read-only recovery algorithm and the commit-admission gate |
| `carrier-fault-cases.v1.json` | the 12 added planned fault cases with model-probe citations |

Patched, minimally, in `scratch/patched/` with unified diffs in `scratch/patches/`:

| Bound input | Change | Before → after |
|---|---|---|
| `commit-recovery-plan.v1.json` | append F38–F48 (12 cases) in the existing closed case shape; extend `standing` | `9a5a8396…` → `a899c706…`, +110/−2 |
| `implementation-boundaries-and-build-plan.md` | two anchored prose edits plus the regenerated matrix rows | `cebf4406…` → `f60d4e85…`, +25/−2 |

F00–F37 conclusions are unchanged by the patch, and the validator asserts that against the
original bytes. The matrix rows sit inside the project's generated block; the project's own
generator must be re-run at integration so the block and the JSON stay byte-consistent.

## 2. Task 1 — the carrier (CR-04, CR-07, COV-03)

The defect is not a loose enum; it is a joint unsatisfiability, and I established it by execution
rather than by reading:

- **No physical DDL in Source25 admits `SEAL`.** All four carriers of the DDL text (v1 markdown,
  v2 `.sql`, `security_unit_lib_v2`, `security_unit_lib_v8`) carry the identical 14-member
  recordSchema-1 `record_type` set. Executed: a schema-3 `SEAL` insert aborts on the CHECK. The
  only schema-3 type the physical carrier rejects is `SEAL`.
- **The physical carrier requires `TERMINAL`** at the reserved slot 9007199254740991, and
  `TERMINAL` is not a member of the closed schema-3 `JournalRecord`.
- **The physical `platform` CHECK enumerates exactly the four S8 display aliases**, which S8
  MUST-2 refuses as a grant platform. Executed: `macos-aarch64` and `linux-x86_64-gnu` are refused
  by the frozen CHECK while the alias `macos-arm64` is admitted. Exactly one value,
  `macos-x86_64`, is lawfully shared.

**Resolution.** A new `carrierFormat` axis, explicitly distinct from `recordSchema` and from the
logical `stateSchema`, plus a new table `grant_journal_v3` whose single segregation CHECK carries
`TERMINAL` as **the already frozen recordSchema-1 TERMINAL body**. That is the move that avoids
both bad options: schema 3 is not widened, and `TERMINAL` is never admitted as a public
`JournalRecord`. No new H-domain, no new canonical profile, no public wire major change.

**Migration is expressible entirely within the frozen rules.** `TERMINAL` with the existing cause
`grantGenerationClosure` closes the inherited generation using constraints the frozen DDL already
enforces; then the additive script runs; then a single immutable `carrier_format` row fixes
`first_generation`. Executed: inherited rows byte-unchanged, inherited schema objects unchanged,
the legacy alias retained verbatim as `macos-arm64`, a second migration aborts, and a write below
`first_generation` is refused. Nothing is disabled and nothing is rewritten.

**Open dispatch is by schema introspection only**, because carrierFormat 1 has no version row.
Correct on all five databases tested. Two dispatch checks close real holes: the stored SQL text of
the two `IF NOT EXISTS` side tables must byte-equal the frozen definition, and the inherited
generation ceiling must sit strictly below `first_generation`.

Cross-contract additions, stated rather than smuggled: WA-13 gains a third generation-closure
cause (carrier-format migration, reusing the existing typed cause); S9 gains a carrierFormat
reader bridge on the existing dual-reader pattern; and `CarrierHighWaterV1` is a new private
closed shape.

## 3. Task 2 — the recovery algorithm and the anchor (CR-08)

The algorithm is in `commit-recovery-readonly.v1.md` and was executed as a model: 21 cases, all
passing, **zero** attempted mutations, the evidence ledger opened **exactly once** in every case,
and the journal opened **at most twice** in every case.

It does what root specified: ledger snapshot first, journal/witness/floor second, and the
resulting ordering hazard resolved by **exactly one** bounded journal reopen, then an honest
owner-attributed `unavailable-busy` or the F22 quarantine condition — never a conclusion drawn
from two different snapshots, and never `uncommitted`. No witness `INIT`/`REVERT`/`ADVANCE`, no
high-water raise, no new grant, no store-binding allocation, no fence, no waiting.

The three prefix-anchor cases are exact: `COMMITTED` at tail, `PENDING` at tail (confirm, report
`witnessWouldAdvance`, perform no ADVANCE), and `PENDING` at the next slot (fall back to the
SC-TRUST floor; above the floor the answer is **`unknown`**, explicitly not invalidation). The
observer and active-writer races are defined: each of tail, witness and floor is read once and
decided on that single tuple, and a valid later append's `PENDING` witness never invalidates an
earlier committed receipt.

**On the anchor, the honest answer is narrower than the followup's — and I found a defect neither
root nor the followup had named.** Executed measurement (C2):

- The v8 closed witness carries `bodySha256`, the *tail body* digest. Substituting any interior
  body leaves it unchanged. So **the witness detects no interior substitution at all, under either
  chain law.** Not weakly — zero interior authentication.
- carrierFormat 1 §5.4 states *"the chain head is in the witness."* It is not: the v8 closed
  witness shape has no chain-head member. Two frozen historical documents disagree about what the
  witness holds.
- The inherited chain binds only the immediately previous body digest and index, so even a
  chain-head-carrying witness would catch a substitution at seq t−1 and miss every earlier one.

So: protected custody plus a surviving witness and floor **can** confirm presence of the requested
`SEAL` row with its joined digest, `operationRef` and `runId`, sequence contiguity, and
non-rollback below the last *observed* boundary. They **cannot** authenticate the interior prefix.
The conclusion class is `confirmed-under-retained-custody`, never "cryptographically proven"; every
confirming result carries `interior-bodies-not-authenticated`. This does not block recovery,
because durable commitment is established by the receipt plus association, not by the journal
prefix.

I also corrected my own first instinct here. I had intended to propose a recursive chain as the
fix; the executed matrix shows that would add a law and buy nothing observable, because the witness
field is the binding constraint. Stronger authentication requires **both** a recursive chain and a
new `witnessSchema` 2 carrying the chain head — and even that does not defeat a coherent
whole-carrier rewrite. All four options are costed in `carrier-format.v3.md` §11 and **none is
adopted**; `carrier_format.chain_law` exists so the decision stays versioned rather than silent.

**A further honest limit I will not paper over:** the inherited `prev_sha256` formula is specified
by exactly one artifact, a DDL comment, with no reference implementation (`genesis_prev` has zero
call sites) and no retained fixture anywhere in Source25. Its byte encoding is therefore unpinned.
carrierFormat 3 pins it prospectively as `chain_law` 1. I cannot claim byte compatibility with any
real carrierFormat 1 or 2 instance, because no such instance exists in the reviewed corpus. A
historical chain that does not recompute reports `chain-unverifiable`, which is a diagnostic —
never tamper, never invalidation, and never a licence to rewrite a row.

## 4. Task 3 — the gate, the latch and cleanup (CR-23)

**Root's ownership proposal is sound and I adopt it.** Consuming `CommitSession` in
`begin_journal_txn` removes the followup sketch's borrowed-then-move problem; constructing
`JournalSealBinding` privately in security removes the cross-crate private-construction problem;
a security-owned trait with a storage-private implementation keeps the dependency direction right
without exporting an authority type; and the trusted-host framing is the honest one, with the
public facade — which accepts neither an external adapter nor an external `SealOutcome` — as the
boundary that must hold against a hostile caller. I did not find a reason to change any of it.

**One correction, and it lands on the followup rather than on root.** The followup's CR-23 remedy
(i) puts the linearization point at *callback entry*. That is wrong: the staging callback commits
nothing, so a latch arriving after staging but before admission **must** still be able to refuse.
The correct point is the atomic `preparing → commit-admitted` transition — exactly what root
already specified. Executed: 7 gate cases plus **15 exhaustive latch interleavings with zero
violations**; no schedule yields both a refusal and a durable commit, and none yields `uncommitted`
after a commit syscall was issued.

**A second correction: the followup's remedy (iv) is not implementable as written.** It requires
the post-release `REV` to record the SEAL `journalSeq`. The schema-3 `JournalRecord` is closed and
has no sequence-valued correlation member, so this would change a closed public schema. Correct
resolution: correlation lives in the lawful private association and the host's private
`executionId ↔ operationRef` map, plus a **reader rule** that `REV` after `SEAL` in sequence order
never implies the `SEAL` was refused. The S6 linearization law constrains only the other
direction. I flagged, and did **not** decide, the option of carrying the existing closed-schema
`runId` member on a `REV`: that is the security owner's call.

Existing D9 behaviour is preserved, including two laws easy to lose: a `durability-undetermined`
response **omits `runId`** while retaining `executionId` (RunId is observable only for a committed
Run), and the settled ExecutionId is **terminal** — no automatic write retry. Cleanup order
releases level 4 and both level-3 transactions, appends `REV`/`CLN` through a fresh lawful
level-3→level-4 under the still-held stopped operation lease, then releases the lease, then does
the S7 end handoff. That satisfies both binding S7 laws. `Drop` is best-effort only;
`mem::forget`, process abort and stalled syscalls guarantee nothing and must leave recovery
evidence rather than a claimed cleanup. Capacity is detected before level 4, writes the inherited
`carrier_capacity_pause` row in the transaction already held, and routes through host to lifecycle
**after** lease release; storage never calls lifecycle backwards.

## 5. Executed scope, stated exactly

Reference environment: CPython 3.12.13, SQLite 3.50.4, jsonschema 4.25.1, invoked as a `python3`
subprocess. Every SQLite database in every control is `:memory:`; no carrier file was created,
opened or migrated on disk.

| Control | Executed | Result |
|---|---|---|
| C1 | inherited carrier laws over 8 selected frozen members | 16 DDL probes; 14/14 `reconcile_witness` rows reproduced; digest semantics established |
| C2 | proposed DDL, migration, dispatch, anchor discrimination | 35 DDL probes; migration m1–m12; dispatch correct on 5 databases |
| C3 | recovery and gate models | 21/21 recovery, 0 mutations; 7/7 gate; 15 interleavings, 0 violations |
| C4a | patch application | +110/−2 and +25/−2 |
| C4b | reference validation | 82 passed, 0 failed |
| C5 | negative controls | 12 drifts, 12 rejected |

**The negative controls found four real gaps, which I then fixed.** Two were genuine holes in my
own validator: it checked trigger flags for carrierFormat 1 but not 2, and it matched the
segregation CHECK by text fragment rather than behaviour, so deleting the CHECK passed. The
validator now re-derives every asserted frozen flag for both inherited formats and carries 13
**behavioural** DDL probes that apply the DDL and observe admit/refuse rather than grepping. The
other two were badly chosen drifts of mine (a non-unique anchor, and a drift that left a second
standing marker intact); both are now precise. I am reporting this because a validator that cannot
fail proves nothing, and mine could not until the negative controls showed it.

## 6. What is not established

- **No OS durability**, `fsync`/`F_FULLFSYNC` behaviour, or real crash behaviour. Every added
  fault case is `not-executed`, and F00–F37 remain as they were.
- **No real lock contention, process isolation or process control.** F42 (`mem::forget`, abort,
  stalled syscall) has **no feasible model here** and is recorded as such rather than modelled.
- **No Rust.** No API sketch was compiled or borrow-checked. The E0505/E0451 reasoning is an
  ownership argument about root's design, not a compiler result.
- **No qualification gate**, no OS scheduling claim for the S6 5 s / 10 s bounds, and no
  application or implementation readiness.
- **A passing reference model establishes only internal consistency** of the model against the
  frozen bytes it reads.

## 7. Remaining defects and open decisions

Carried forward honestly rather than closed:

1. **The witness cannot authenticate any interior prefix** (§3). Real defect, newly named, not
   fixed here. Fixing it needs a new `witnessSchema` and touches a frozen security boundary;
   four costed options are recorded and none is adopted.
2. **carrierFormat 1 §5.4 contradicts the v8 witness shape** about the chain head. Two frozen
   documents disagree; the v8 closed shape governs, and the v1 sentence is inaccurate as a
   description of v8. Needs an owner disposition, not a silent edit.
3. **`prev_sha256` byte encoding is unpinned in the inherited corpus** (§3). Pinned prospectively
   for carrierFormat 3 only; historical verification is `chain-unverifiable`-capable by design.
4. **carrierFormat 1 cannot physically enforce TERMINAL closure** (no trigger). Handled by a
   reader rule marking such generations `closed-by-record, not-trigger-enforced`; a stronger fix
   would require touching carrierFormat 1, which is immutable.
5. **`indeterminate` is overloaded**: the build plan's internal conclusion spelling collides with
   the public D9 class at exit 3. I renamed the internal standings and pinned each public
   projection, but the original spelling still appears in F00–F37, which I deliberately did not
   touch. Root should decide whether to rename there too.
6. **The generated matrix block** now contains rows I produced in the generator's format. The
   project's own generator must be re-run at integration to guarantee byte consistency.
7. **`runId` on a `REV` record** is lawful under the closed schema but semantically the security
   owner's call (§4). Flagged, undecided.
8. **CR-04/CR-07 original texts are not in the bound input set.** They were stated in the prior
   review's pass 1, which is not among the four bound files. I reconstructed their scope from the
   followup's explicit citations, root's task statement, and direct inspection of the frozen
   carrier — and then established the underlying facts by execution rather than relying on either
   description. If pass 1 scoped either finding more broadly than the carrier, that extra scope is
   unaddressed here.
9. **Followup findings outside this bounded scope are untouched**: CR-01, CR-03, CR-05, CR-09,
   CR-12′, CR-15 through CR-22, and CR-24 through CR-27 are neither reviewed nor endorsed by this
   correction.
