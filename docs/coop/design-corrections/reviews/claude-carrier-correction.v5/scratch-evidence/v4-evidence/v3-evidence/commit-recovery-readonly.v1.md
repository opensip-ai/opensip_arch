# Bounded read-only commit recovery, and the commit-admission gate (PROPOSED)

**Standing.** Proposed design/reference correction for the CR-08 prefix-anchor question and the
CR-23 observer-latch gap. Companion to
`docs/coop/design-corrections/security/carrier-format.v3.md`. Authored against frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`. No acceptance, readiness,
application or implementation authorization, and no self-acceptance. The algorithm and gate below
were executed as reference models (`scratch/controls/c3.py`, `scratch/out/c3.json`); no real
carrier, syscall, lock or crash was exercised. Root has not accepted the prior followup algorithm
and this is not that algorithm; §4 states where it differs.

## 1. Standing of the conclusion vocabulary

The ordered failure matrix in the build plan uses `indeterminate` as an internal scenario
expectation. That spelling collides with the **public D9 class** `indeterminate`, which is exit 3.
A reader who sees `indeterminate` in a recovery result and maps it to exit 3 would be wrong. This
correction therefore renames the internal standings so they cannot be read as a D9 class, and
states the public projection for each.

| Internal standing | Meaning | Public D9 projection |
|---|---|---|
| `committed-historically` | receipt + association present and joined, prefix anchored | success, exit 0, RunId observable |
| `committed-availability-degraded` | as above, current availability is partial/expired/purged/corrupt/unavailable | success for history; availability reported separately (identity §5) |
| `not-committed-verified-absent` | readable exact lookup, matching store binding, no receipt and no association, no active attempt | identity §5 "failed" answer for the durability-undetermined recovery path |
| `unknown-custody` | cannot answer: unreadable ledger, absent/malformed/foreign witness, floor contradiction, carrier incompatible, joins differ, prefix not anchored | `operational-failed` exit 4 with `LEDGER.CORRUPT` or `HOST.IO_FAILURE` |
| `unknown-quarantine-condition` | an owner quarantine condition is present (F20/F21/F22) | `operational-failed` exit 4, owner diagnosis reported |
| `unavailable-busy` | single reopen did not reconcile, or a writer demonstrably holds the resource | `operational-failed` exit 4 with `LEDGER.BUSY_TIMEOUT` |
| `in-progress` | the requested ExecutionId is an actively running attempt | in-progress; never a final failure from an older snapshot |

**No new public D9 class or code is introduced.** Every non-answer projects onto the existing
`operational-failed` vocabulary, never onto exit 3. This preserves identity §5's binary
"returns committed or failed" exactly where the ledger and objects are readable, and it stops the
algorithm from inventing a third public outcome where they are not.

## 2. The algorithm

Read-only throughout. Executed as `recover()` in `scratch/controls/c3.py`; the model records any
attempted mutation and all 21 cases completed with an empty mutation list.

### Step 0 — admission

Obtain the `SHARED-READ` project lease per S7 and the custody-admitted store binding through an
admitted handle and the registry, never from request fields. Compute `storeGenerationDigest`. An
unregistered namespace is a refusal, never `unknown`.

Prohibited for the whole algorithm: the install fence; the writer lease; `EXCLUSIVE`; any
`BEGIN IMMEDIATE`; any `INSERT`/`UPDATE`/`DELETE`; witness `INIT`, `REVERT` or `ADVANCE`; any
witness write; any SC-TRUST high-water raise or copy; any quarantine-marker write; any new
execution grant; any store-binding allocation; any wait on any lock; more than one journal
reopen; any repair.

### Step 1 — evidence ledger snapshot FIRST, exactly once

Open one consistent committed reader snapshot (level 3, WAL read snapshot). Inside that single
snapshot read: the receipt for `(storeGenerationDigest, namespaceId, executionId)`; the private
`CommitRecoveryAssociationV1` row for the same primary key; and the Run manifest, object
references, availability generation and pins.

- Ledger cannot be opened or read → **`unavailable`** (F24). Never `not-committed`. A failed read,
  a wrong generation or an empty fallback database is never absence.
- The requested ExecutionId is an actively running attempt → **`in-progress`** (F29).
- Receipt and association both absent, snapshot readable, store binding matches → 
  **`not-committed-verified-absent`** (F36). This is the orphan-SEAL answer: a durable SEAL with no
  committed ledger row is an uncommitted attempt, permanently, including after restart and after a
  later attempt commits the same semantic RunId.
- Exactly one of receipt/association present → **`unknown-custody`** (F23). Preserve the observed
  row; synthesize nothing.
- `storeGenerationDigest` or `namespaceId` in the association differs from the request →
  **`unknown-custody`** (F27).

Record the snapshot and **do not read the ledger again** for the rest of the algorithm. This single
read is what makes the mixed-snapshot contradiction impossible.

### Step 2 — journal snapshot SECOND, exactly once

Open the carrier read-only: no append lock, no write transaction, no witness mutation. Detect
`carrierFormat` per the open dispatch. Read once: the tail `(seq, body_sha256)` for
`A.grantGeneration` from the table that owns that generation; the witness `W`; and the SC-TRUST
high-water `H` for `(A.journalCarrierDigest, A.grantGeneration)`.

If `carrierFormat < 3` for the generation that holds the requested attempt, no `SEAL` row is
representable there at all → **`unknown-carrier-incompatible`** (F31/F46). Never `not-committed`.

### Step 3 — the ordering hazard, with exactly one bounded reopen

Because the ledger snapshot was taken first, `A.journalSeq <= t` is expected: the SEAL append
preceded the ledger commit. If `A.journalSeq > t`, the journal view is older than the ledger
snapshot, which no durable append can explain. This is root's hazard, and it is resolved without
a contradiction:

1. Close and reopen the journal read handle **once** and re-read `t`, `W`, `H`. Do **not** re-read
   the ledger. (A WAL reader can hold a stale snapshot; one reopen is the bounded remedy.)
2. If now `A.journalSeq <= t` → continue at Step 4, carrying the diagnosis
   `reconciled-after-single-reopen`.
3. If still `A.journalSeq > t`:
   - `H.lastSeq >= A.journalSeq` → the floor proves the prefix once existed and the current tail is
     below an observed floor. That is the F22 condition: **`unknown-quarantine-condition`**,
     `uncertainTailLoss`, reported to the carrier owner. No repair, no high-water raise.
   - otherwise → **`unavailable-busy`**, attributed to the **security carrier owner**, not to the
     requester and not to the ledger.

Never `uncommitted`, and never a conclusion drawn from two different snapshots.

### Step 4 — carrier naming and structural checks

All required; any failure yields `unknown-custody` or `unknown-quarantine-condition` as marked,
and all of them carry `notInvalidated = true`.

- `W` absent with a non-empty journal → `unknown-custody`, `witnesslessRestore` (F21).
- `W` fails the v8 closed shape, validated **before any comparison** → `unknown-custody`,
  `witnessMalformed` (F20). The shape is
  `{witnessSchema: 1, projectKeyDigest, grantGeneration, seq, state, bodySha256}`, `bodySha256`
  member present (absent is not null), `PENDING` requires `seq >= 1`, no other member.
- `W.projectKeyDigest != A.journalCarrierDigest` or `W.grantGeneration != A.grantGeneration` →
  `unknown-custody`, foreign carrier (F20).
- Sequence not contiguous 1..t → `unknown-custody`.
- `H` absent for this carrier → `unknown-custody`.
- `t < H.lastSeq` → `unknown-quarantine-condition` (F22). A lower tail is never a confirmation.
- Digest recomputation uses the **domain-framed** rule
  `body_sha256[j] == SHA256("opensip.metadata.journal.1" || 0x00 || C(body[j]))`. Not
  `SHA256(body[j])`.
- Chain recomputation under `carrier_format.chain_law` yields `chain-consistent` or
  `chain-unverifiable`. `chain-unverifiable` is a diagnostic, never tamper, never invalidation.

### Step 5 — record join at k = `A.journalSeq`

A row must exist at `(A.grantGeneration, k)` with `record_type = 'SEAL'`, `record_schema = 3`,
`body_sha256 == A.journalBodySha256` (the domain-framed digest), `operation_ref == A.operationRef`
and body `runId == A.runId` (`run3` only). Any mismatch → `unknown-custody` (F33). Hash presence
alone is insufficient; matching just RunId, a digest or a current row does not establish the join.

### Step 6 — prefix anchor selection

Let `t` be the tail seq and `floorOk` be `H.lastSeq == 0` or
`body_sha256[H.lastSeq] == H.tailSha256`.

| Case | Witness state | Anchor | Result |
|---|---|---|---|
| **A** COMMITTED at tail | `state = COMMITTED`, `seq = t`, `bodySha256 = body_sha256[t]` | `witness-committed-tail` | confirm for any `k <= t` |
| **B** PENDING at tail | `state = PENDING`, `seq = t`, `bodySha256 = body_sha256[t]` | `witness-pending-at-tail` | confirm for any `k <= t`; report `witnessWouldAdvance`; perform **no** ADVANCE |
| **C** PENDING at next slot | `state = PENDING`, `seq = t + 1` | `sc-trust-floor` if `k <= H.lastSeq` and `floorOk` | else if `k > H.lastSeq`: **`unknown-custody`**, explicitly **not invalidated** (F44); if not `floorOk`: `unknown-quarantine-condition` (F22) |
| any other | COMMITTED beyond tail, equal seq different hash, non-adjacent PENDING, foreign, malformed | none | `unknown-quarantine-condition` per the v8 §5.4 row; no repair |

Case C is the load-bearing one. In `PENDING t+1` the witness names a record that was never
appended, and the prior COMMITTED witness has been overwritten, so **the carrier has no live
witnessed anchor for its durable prefix**. The only retained custody-qualified anchor that
survives a later in-flight append is the SC-TRUST high-water, which v8 §5.4 writes under the
**fence** at operation start and end, never under a lease, and which is a record distinct from the
witness (§4.2).

In cases A and B the floor is still required: confirmation additionally needs `t >= H.lastSeq` and,
when `H.lastSeq >= 1`, `floorOk`. Otherwise the floor contradicts the tail and the answer is the
F22 condition.

### Step 7 — separate questions, separately answered

- **Historical commitment** comes from the receipt plus association plus the anchored join. It is
  immutable: sealed assurance and the historical verdict never change (identity §5).
- **Current availability** is the separate monotonic-generation record: retained, partial, expired,
  purged, corrupt or unavailable, with exact missing references and cause. A degraded availability
  yields `committed-availability-degraded` (F25) and never rewrites or reseals history.
- **Retained object state** is inspected separately from the ledger rows and from the carrier.
- The conclusion class is **`confirmed-under-retained-custody`**, never "cryptographically proven".
  Every confirming result carries the diagnosis `interior-bodies-not-authenticated`.

### Observer and active-writer races

- An `APPEND-WRITE` writer may advance `t` and `W` during the read. Each of `t`, `W`, `H` is read
  exactly once after the at-most-one reopen, and the decision is made on that single tuple. The
  algorithm never waits on the writer and never re-reads to obtain a better answer. A larger `t`
  can only help, since the predicate is `k <= t`.
- A concurrent writer holding a `PENDING` witness at `t+1` is exactly Case C. For `k <= H.lastSeq`
  the answer is confirm-by-floor; for `k > H.lastSeq` it is `unknown-custody`. **A valid later
  append's PENDING witness never invalidates an earlier committed receipt.**
- The observer fail-stop latch is writer-side attempt state. It is not durable carrier evidence and
  read-only recovery neither observes nor influences it.

### Executed case coverage (C3)

21 cases, all passing, zero mutations, ledger opened exactly once in every case, journal opened at
most twice in every case: A1 Case A; A2 Case B; A3 Case C confirm-by-floor; A4 Case C above floor →
`unknown-custody`; A5 Case C floor hash mismatch; A6 tail below floor; A7 COMMITTED beyond tail;
A8 witnessless; A9 malformed (PENDING 0); A10 foreign carrier; B1 hazard reconciled by one reopen;
B2 hazard unreconciled with floor at/above k; B3 hazard unreconciled with floor below k →
`unavailable-busy`; C1 ledger unreadable; C2 verified absent; C3 receipt without association;
C4 active attempt; D1 carrierFormat 2 generation; D2 availability purged; D3 join differs;
D4 binding swap.

## 3. The commit-admission gate and the post-gate latch (CR-23)

### 3.1 Assessment of root's ownership proposal

Root's proposal is sound as stated and this correction adopts it. Specifically:

- `begin_journal_txn` **consuming** `CommitSession` and returning a security-owned opaque
  `JournalWriteTxn` removes the followup sketch's borrowed-then-move problem, because no borrow of
  the session outlives the call that moves it.
- `JournalSealBinding` being privately constructed **in security**, not in the inert contracts
  crate, removes the cross-crate private-construction problem. Putting an authority-bearing
  constructor in `contracts` purely so another crate can build private fields would be the defect,
  not the fix.
- The staging/commit adapter **trait owned by security** with a **storage-private implementation**
  keeps the dependency direction correct (security does not depend on storage) without exporting
  any authority type.
- Storage owning the receipt, the remaining association values and all private SQL, while security
  owns the carrier-side values, is what makes the thirteen-field association a cross-owner check
  rather than a caller assertion.
- Security depending on the **pure** evaluator for `ReplayedRun` keeps the evaluator free of
  callbacks, ports and mutable store handles.
- Treating the trait as trusted-host collaboration rather than a sandbox for arbitrary
  implementations is the honest framing: the boundary that must hold against a hostile *caller* is
  the public facade, which accepts neither an external adapter nor an external `SealOutcome`.

One correction is required, and it is a correction to the **followup**, not to root:

> The followup's CR-23 remedy (i) says to record a `linearizationPoint` **at callback entry**, and
> that a latch at or after it can never yield `refused`. That is wrong. The staging callback runs
> *before* the gate and commits nothing. A latch arriving after staging entry but before admission
> **must** still refuse, because no durable ledger effect exists yet. The correct linearization
> point is the atomic `preparing -> commit-admitted` transition — which is precisely what root's
> design already specifies. Root's proposal fixes the followup here.

### 3.2 The gate

One atomic attempt state, transitioned by compare-and-set, arbitrates the latch against commit
admission. The observer latches **outside** the append mutex.

```
preparing --(latch wins)-------> latched          : refuse; no evidence commit is ever issued
preparing --(gate wins, staged)-> commit-admitted : latch can no longer refuse this commit
```

Ordered path: SEAL record durable → witness durable → security-owned staging callback validates the
`JournalSealBinding` joins and inserts the exact receipt and association in the already-open
evidence transaction, returning an owned prepared-commit adapter → security rechecks epoch,
freshness and cancellation → atomic `preparing -> commit-admitted` → consume the adapter's one
commit method (prepared commit and barriers only).

Laws:

- All payload admission, association construction and SQL staging precede the gate. The commit
  method performs only the prepared commit and its barriers.
- The gate **orders admission only. It is not the durability point.**
- A latch after admission blocks **subsequent effects** and cannot undo a syscall or rewrite its
  outcome. A confirmed durable commit stays committed.
- Neither raw transaction handles nor the append mutex escape. The callback cannot mint
  `PublishedCommit`; that constructor stays private to storage and is reachable only from storage's
  own commit after `SealOutcome::Committed`.
- Every journal writer, including the revocation observer, uses the same security-owned
  transaction-before-append API. No caller acquires a journal transaction from inside an
  append-lock callback.

### 3.3 Outcome mapping, preserving existing D9 behaviour

| Situation | Standing | D9 | RunId observable |
|---|---|---|---|
| latch won while `preparing` | `uncommitted` | no commit issued; SEAL stays an orphan attempt (F36) | no |
| admitted, commit confirmed | `committed` | success | **yes** |
| admitted, commit confirmed, required delivery then fails | `committed-delivery-failed` | `DELIVERY.REQUIRED_FAILED`, operational-failed, exit 4 | **yes** |
| admitted, commit syscall error or barrier unconfirmed | `durability-undetermined` | `DURABILITY.COMMIT_FAILED`, operational-failed, exit 4 | **no** |

Two existing D9 laws are preserved and must not be lost in implementation:

1. "RunId is externally observable only for a committed Run. A failed final authoritative commit
   omits `runId`, retains `executionId` for attempt correlation." So the
   `durability-undetermined` response **omits runId** even though a later read-only recovery may
   confirm the commit and then report the RunId. That asymmetry is intended.
2. "The settled ExecutionId is terminal." There is **no automatic write retry**. A later attempt
   after authority restoration receives a new ExecutionId.

The S6 observer bound bounds **admitting new effects**. It does not abort an in-flight syscall, and
this design does not infer OS cancellation bounds from Rust types.

### 3.4 Pending REV correlation — corrected

The followup's remedy (iv) requires the post-release REV to "record the SEAL `journalSeq` and its
evidence outcome". **That cannot be done in the journal.** The schema-3 `JournalRecord` is closed
(`additionalProperties: false`) and has no sequence-valued correlation member; adding one would
change a closed public schema, which the task forbids. The correct resolution has two parts:

1. **Correlation lives in lawful private operational metadata**: the storage-owned association row
   (which already carries `grantGeneration`, `journalSeq`, `journalBodySha256`, `operationRef`,
   `executionId`) plus the host's private `executionId <-> operationRef` map. Where no association
   was committed, the pending-REV correlation is recorded in the security-owned private carrier
   metadata for that operation, not appended to a journal body.
2. **A reader rule**, which is where the real fix belongs: *REV appearing after a SEAL in sequence
   order never implies the SEAL was refused.* The S6 linearization law says only that no `SEAL` is
   appended **after** `REV`; it says nothing in the other direction. Durable commitment is
   established solely by the evidence-ledger receipt and association.

Optionally, the REV body may carry the existing closed-schema `runId` member for correlation
without any schema change. This is *not* adopted here: `runId`'s own description says "SEAL records
that name a Run use run3", and whether a REV may lawfully name a Run is the security owner's call.
Flagged for root, not decided.

### 3.5 Cleanup and capacity ordering

On any end path security returns a **stopped session** that still owns the operation lease and
admits cleanup only, with no further analysis or effect APIs. Order (verified against S7):

1. Release the level-4 append mutex.
2. Abort or release the open evidence level-3 transaction and the journal level-3 transaction.
3. With the stopped operation lease **still held**, take a fresh lawful level-3 journal
   transaction and then level 4, and append REV/CLN.
4. Release the operation lease.
5. Perform the ordinary S7 end handoff: fence, non-blocking re-lease, SC-TRUST high-water copy,
   release.

This satisfies both S7 laws that constrain it: no level 3 is ever acquired under level 4, and the
fence is never awaited while a lease is held, because step 4 precedes step 5.

**Drop is best-effort only.** `mem::forget`, process abort and a stalled syscall do not guarantee
destructor execution. Those paths must leave recovery evidence and return an honest
unavailable/busy result — never a claimed cleanup success (F42).

**Capacity.** `seal_under_append_lock` reads the tail under the already-open journal level-3
transaction **before** taking level 4. If `tail + 1 == 9007199254740991` it appends nothing, writes
the `carrier_capacity_pause` row in the journal transaction it already holds, and returns typed
`CarrierCapacityExhausted {grantGeneration, provenTailSeq}`. Storage maps it to a typed storage
error; host maps it to the D9 refusal and, **after cleanup and operation-lease release**, routes the
lifecycle rollover under the fence. Storage never calls lifecycle backwards. The `TERMINAL` row
appended by that rollover carries the **lifecycle rollover operation's own** `op-` token, never the
released analysis operation's ref.

## 4. Where this differs from the prior followup algorithm

Root has not accepted the followup algorithm. The differences are substantive, not cosmetic.

1. **Ordering.** The followup gives a predicate over a single joint observation. This algorithm
   fixes the order — ledger snapshot first, journal second — and defines the resulting hazard and
   its single bounded reopen (§2.3). The followup does not address the hazard at all.
2. **Digest rule refuted by execution.** The followup requires
   `body_sha256[j] == SHA256(body[j])`. The frozen implementation computes the **domain-framed**
   digest; a validator implementing the followup literally rejects every lawful record. Evidence:
   `scratch/out/c1.json`, `body_sha256_is_raw_sha256_of_body = false`.
3. **The anchor claim is narrowed.** The followup concludes that Cases A and B let the witness
   "anchor the tail" and confirm any `k <= t`. That is right about *presence and non-rollback* and
   wrong if read as prefix authentication: executed measurement shows the v8 witness field
   `bodySha256` detects **no** interior substitution under either chain law (`carrier-format.v3.md`
   §11). The followup's own honest bound is directionally right but its mechanism is misattributed.
4. **A citation conflation, corrected without changing the conclusion.** The followup calls the
   SC-TRUST high-water `{project, grantGeneration, lastSeq, tailSha256}` "the witness", citing
   carrierFormat 1 §5.4, which does use one name for both. v8 §5.4 separates them: the witness is
   the PENDING/COMMITTED record with a strict closed shape, and the high-water copy is a distinct
   durability boundary (`security_unit_lib_v8.DURABILITY_BOUNDARIES` lists `witness-write` and
   `sc-trust-high-water-copy` separately). The followup's *conclusion* — that the floor is not
   overwritten by a PENDING witness — survives and is correct, but only under the v8 separation.
5. **The high-water has no closed shape.** The followup's floor case depends on `H.lastSeq` and
   `H.tailSha256`, but no frozen artifact gives the high-water a validated shape, unlike the
   witness beside it. `CarrierHighWaterV1` closes that gap.
6. **Conclusion vocabulary.** The followup reuses `unknown`/`indeterminate` loosely. §1 separates
   the internal standings from the public D9 `indeterminate` (exit 3) and pins each projection.
7. **CR-23 linearization point corrected** (§3.1): callback entry is the wrong point; the atomic
   `preparing -> commit-admitted` transition is the right one.
8. **CR-23 remedy (iv) is not implementable as written** (§3.4): the closed schema-3 body cannot
   carry the SEAL `journalSeq`, so correlation moves to private metadata plus a reader rule.
