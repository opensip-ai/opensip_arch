# Bounded read-only commit recovery, the commit-admission gate, and the settlement sweep (PROPOSED v3)

**Standing.** PROPOSED-NOT-SELF-ACCEPTED: no acceptance, no readiness, no application and no
implementation authorization. Private design/reference work, not OS qualification. Supersedes the
v2 draft, which is retained unchanged in `scratch/v4-evidence/`. Authored against frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.

**What changed from v2.** Three corrections root identified, plus one selected law:

1. Step 1 branched on `phase` alone, so a `settled` row whose outcome was `committed` or
   `undetermined` could yield `terminal-not-committed`. Fixed in §2 and §3; the negative conclusion
   now requires the `refused` outcome *and* a confirmed absent receipt in the same snapshot.
2. The authorized settlement sweep was named but unspecified. Specified in §4.
3. The carrier-quarantine public projection was left as a two-option open decision. Settled in §1
   against the actual schema: `LEDGER.CORRUPT` with a non-none `faultCause` and **no**
   `domainDetail`. No registry member is minted and `MIGRATION.CORRUPT` is not misused.
4. The state-3 delivery rule is now a **selected successor law**, not an owner choice (§6.2).

## 1. Conclusion vocabulary and its exact schema-valid projection

Internal recovery standings are **not** public D9 classes and are deliberately spelled so they
cannot be mistaken for one. This matters because the word `indeterminate` collides with the public
D9 class `indeterminate` at exit 3: no standing below is spelled that way, and every one projects
onto an existing class, `errorCode` and `faultCause`. Root owns the final generator and the
clarification of the older internal `indeterminate` spelling in F00–F37; that is not treated as a
blocker here.

The public shape is `workflows/schemas/common.schema.json#/$defs/StepTermination`. Its frozen
branch contract is decisive: `required: ["class"]` only; `domainDetail` is **optional**; and
"request-rejected and operational-failed require `errorCode` (operational-failed also a non-none
`faultCause`)". Every projection below is therefore expressible with **only existing members**, and
C12 validates each one against that actual schema.

| Internal standing | class | errorCode | faultCause | domainDetail |
|---|---|---|---|---|
| `committed-historically` | `success` | — | — | omitted |
| `committed-availability-degraded` | `success` for history; a required object unavailable during a selected operation is `operational-failed` / `HOST.IO_FAILURE` / `host-io` | | | `evidence.missing`, `evidence.corrupt`, `evidence.purged` or `evidence.expired` |
| `terminal-not-committed` | `success` | — | — | omitted (a successful observation, not a refusal) |
| `unknown-attempt-open` | `operational-failed` | `LEDGER.BUSY_TIMEOUT` | `ledger-busy` | `PROJECT.BUSY` |
| `unknown-attempt-unobserved` | `operational-failed` | `HOST.IO_FAILURE` | `host-io` | omitted |
| `unknown-custody` | `operational-failed` | `HOST.IO_FAILURE` | `host-io` | omitted |
| `unknown-quarantine-condition` | `operational-failed` | `LEDGER.CORRUPT` | `ledger-corrupt` | **omitted** |
| `unavailable-busy` | `operational-failed` | `LEDGER.BUSY_TIMEOUT` | `ledger-busy` | `PROJECT.BUSY` |
| `binding-unusable` | `request-rejected` | `EXTENSION.ADMISSION_REJECTED` | — | `RECOVERY.REFUSED` with typed subject |

**The carrier-quarantine decision is settled, not deferred.** `LEDGER.CORRUPT` with
`faultCause: "ledger-corrupt"` and an omitted `domainDetail` is schema-valid, so no new
`DomainDetailCode` is minted for aesthetics. `MIGRATION.CORRUPT` is **not** reused: it is the store
transition's detail, and borrowing it for ordinary journal corruption would put two remedies behind
one code, which the D9 contract names a defect. The typed reason (`uncertainTailLoss`,
`witnesslessRestore`, `witnessMalformed`) travels in the operational record and the owner
diagnosis, not in a public detail code.

A registered detail is used only where one already fits the event exactly: `PROJECT.BUSY` for busy,
`RECOVERY.REFUSED` for a refused recovery request, and the `evidence.*` family for availability.

## 2. The algorithm

Read-only throughout. Prohibited for the whole algorithm: the install fence; the writer lease;
`EXCLUSIVE`; any `BEGIN IMMEDIATE`; any `INSERT`/`UPDATE`/`DELETE`; witness `INIT`, `REVERT` or
`ADVANCE`; any witness write; any SC-TRUST high-water raise or copy; any quarantine-marker write;
any new execution grant; any store-binding allocation; any wait on any lock or on the writer; any
repair. Bounded to **exactly one** ledger snapshot, **at most two** journal snapshots, and **at
most four** witness and four floor reads.

### Step 0 — admission

Take the `SHARED-READ` project lease per S7 and obtain the custody-admitted store binding through
an admitted handle and the registry, never from request fields. Compute `storeGenerationDigest`
(PS-01 owns the binding tuple and digest shape; nothing is allocated here). An unregistered
namespace refuses. **No liveness probe of any kind is taken, and no in-memory active set is
consulted at any point.**

### Step 1 — one coherent ledger snapshot, read as a whole

Inside one consistent committed reader snapshot read: the receipt; the private
`CommitRecoveryAssociationV1` row; the Run manifest, object references, availability generation and
pins; **and the `AttemptCustodyV1` phase together with its `settledOutcome`**.

Ledger unreadable → `unknown-custody` (F24). Never absence: a failed read, a wrong generation or an
empty fallback database is never absence.

### Step 2 — the settlement matrix, decided entirely inside that snapshot

| receipt + association | phase | settledOutcome | conclusion |
|---|---|---|---|
| both present | `settled` | `committed` | continue to the carrier capture (§3) |
| both present | `settled` | `refused` | **contradiction** → `unknown-custody`; preserve rows, synthesize nothing |
| both present | `admitted` | null | **contradiction** (a receipt exists but the attempt was never settled) → `unknown-custody` |
| both absent | `settled` | **`refused`** | **`terminal-not-committed`** — the only negative |
| both absent | `settled` | `committed` | **contradiction** → `unknown-custody`, unavailable history. **Never a negative** |
| both absent | `admitted` | null | `unknown-attempt-open`. A durability-uncertain attempt lands here too |
| both absent | no row | — | `unknown-attempt-unobserved` |
| exactly one present | any | any | `unknown-custody` (F23) |

Store-binding or namespace mismatch in the association → `binding-unusable` (F27).

**Two rows in that table are conservative policy, not correctness requirements, and are labelled
as such.** C11 drift A8 shows that treating *receipt present with the attempt still `admitted`* as
a contradiction is not needed for safety: the receipt is the authority, so confirming would be
defensible. The rule is retained because a receipt whose attempt was never settled indicates a
broken write ordering worth surfacing — but these controls do not prove it necessary, and root may
drop it. The same standing applies to the second-tail observation in §4. Everything else in the
table is load-bearing: C11 drifts A3 and A9 both produce false negatives when removed.

**A purged historical receipt can never become never-committed.** The only negative requires
`settledOutcome == refused`, which a purge can never produce; and purge retains the minimal sealed
manifest, provenance and tombstone, so a `settled+committed` attempt whose receipt *bytes* are gone
is committed with degraded availability. Absence of receipt bytes is not absence of a receipt.

### Step 3 — bracketed capture of the carrier observations

Unchanged from v2 and re-verified by C6. Each capture takes witness-before, floor-before, journal
snapshot, witness-after, floor-after, and computes byte stability of each bracket. An anchor is
usable only if its own bracket was stable. Anchor classes and the single permitted retry are
unchanged: `witness-committed-tail`, `witness-pending-at-tail` (report `witnessWouldAdvance`,
perform no ADVANCE), `sc-trust-floor`, and `unknown-custody` above the floor under a PENDING next
slot.

### Step 4 — which stable observations an owner quarantine condition requires

Unchanged from v2: stable witness bracket, stable floor bracket, two journal snapshots agreeing on
tail sequence **and** tail digest, the closed witness shape validated before any comparison, and
matching carrier naming. Otherwise the mismatch is attributed to temporal skew and reported
`unavailable-busy`. Read-only never invents a corruption diagnosis from independently timed
observations.

**Standing of the second-tail observation.** It is retained as an explicit **conservative
diagnostic policy**, not as a correctness requirement. My controls (C11 drift A2) show that
dropping it produces no violation in any enumerated schedule, because in a lawful append the tail
moves only together with the witness. It is therefore **not proven independently necessary**, it is
not required for correctness, and it is no part of any cryptographic argument. No attack is
manufactured to justify it. Root may drop it.

## 3. Carrier anchor bound — a selected limit, not an open gap

Retained-custody-only confirmation is the **selected** position. Confirming establishes that the
sealing record is present with its joined digest, operation reference and Run identity, that the
sequence is contiguous, and that no rollback below the last *observed* operation boundary occurred.
It does not authenticate the interior record prefix. The conclusion class is
`confirmed-under-retained-custody`, and every confirming result carries
`interior-bodies-not-authenticated`. An unmet anchor is `unknown`, never invalidation.

No stronger prefix authentication is requested or proposed. `chain_law` is **1** only; the DDL
refuses any other value. Historical generations report `chain-unverifiable` where the prospective
encoding does not recompute, which is a diagnostic and never tamper. These are selected limits and
are **not** listed as remaining gaps.

## 4. The authorized settlement sweep

A writer that dies before settling leaves `phase = admitted` forever. Read-only recovery then
reports `unknown-attempt-open` indefinitely, and that is correct: unknown stays unknown until
proof. This section specifies the separately authorized act that obtains the proof.

### 4.1 Authorization and custody, traced to existing owners

| Question | Existing owner |
|---|---|
| Which command? | `store-gc` — `owner: "security"`, `requestClass: "lifecycle"`, `authorizationClass: "exclusive-lease"`, `writesTrackedIntent: false` |
| What custody? | S7 install fence at level 0, then `EXCLUSIVE` on the affected project namespace, `LOCK_EX|LOCK_NB` |
| Busy namespace? | Skipped and retained, never refused — S7's existing GC law |
| What authority does it get? | Only the exclusive-lease maintenance authority of that operation. **No reuse of the dead attempt's authority**, no new execution grant, no grant revival, and no retry of its commit |

The sweep is **not** read-only recovery and **not** something a stopped session may do. A failed,
latching or undetermined attempt must never open another write transaction with its stopped
session; it releases and leaves the row `admitted`.

### 4.2 What counts as proof, per case

The sweep holds the fence and `EXCLUSIVE`, so **no writer for this namespace can be live**. That is
the custody fact that makes proof possible, and it is why read-only recovery — which holds neither
— cannot produce it.

| Observed case | Proof available | Permitted write |
|---|---|---|
| **crashed**: `admitted`, no receipt, no association, exclusive lease acquired | The lease was free, so the attempt's writer is gone and can never commit. A later writer would be a different ExecutionId | settle `refused` |
| **crashed with an orphan SEAL**: as above, plus a durable `SEAL` for that `operationRef` and no receipt | Same. F36 already fixes that a lone SEAL is an uncommitted attempt | settle `refused`; the SEAL stays operational history and is never promoted |
| **committed but unsettled**: `admitted`, receipt and association both present and joined | The receipt is the authority | settle `committed` |
| **one-sided ledger**: exactly one of receipt/association present | None. This is the F23 contradiction | **no write**; leave `admitted`, report the contradiction |
| **durability uncertainty**: `admitted`, the attempt's own D9 response was `durability-undetermined`, no receipt | The same proof as "crashed": the lease is free, so its writer is gone, and a readable ledger with no receipt means it did not commit | settle `refused` |
| **live**: the namespace lease is busy | None — the attempt may still commit | **no write**; skip and retain, exactly as GC does |
| **inaccessible**: the ledger cannot be opened or read | None | **no write**; report `operational-failed` / `HOST.IO_FAILURE` / `host-io` |
| **already settled** | — | **no write**; the row is immutable once settled |

**The sweep writes only `committed` or `refused`, and that is deliberate.** C14 exposed a flaw in
the v5 draft of this section, which carried a third `undetermined` custody outcome: because the row
is immutable once settled, `settled+undetermined` would have been **unresolvable** — nothing could
ever move it to a real outcome, which is exactly the "cannot prove absence without actual durable
reconciliation" problem root named. The correct separation is:

- `durability-undetermined` is the **D9 response to the caller** at the moment the commit syscall or
  barrier failed: `operational-failed` / `DURABILITY.COMMIT_FAILED` / `durability-commit`, with the
  ExecutionId retained, the `runId` omitted and no automatic retry.
- The **custody row stays `admitted`**, because terminality is genuinely unknown then. `admitted`
  *is* the honest unknown.
- The sweep is the durable reconciliation. Holding the fence and `EXCLUSIVE` proves no writer for
  the namespace is live, so the attempt's writer is gone and can never commit; with a readable
  ledger, absence of both rows proves not-committed and presence proves committed. Absence observed
  under that custody cannot later become presence.

The default for not-knowing is therefore to **leave the row `admitted`** — which happens whenever
the lease is busy, the ledger is unreadable, or the ledger is one-sided.

### 4.3 Write ordering and cleanup

1. Acquire the fence; acquire `EXCLUSIVE` non-blocking on the namespace. Busy → skip.
2. Open **one** coherent ledger snapshot and read receipt, association and custody row together.
   The sweep honours the same one-snapshot rule as the reader; holding the lease does not license
   separately timed re-reads to assemble a conclusion.
3. Decide per §4.2. If no write is permitted, release and continue to the next namespace.
4. Write the single `admitted → settled` transition with its outcome, in one transaction, and
   satisfy the ledger's durability barriers. The monotone trigger refuses a second settle.
5. Permissible lifecycle cleanup, and only this: remove unreferenced orphan objects by the existing
   reachability GC; record nothing else. **Not permitted**: synthesizing a receipt or association,
   appending a `SEAL`, raising the SC-TRUST high-water, writing or repairing the witness, rolling a
   grant generation, or reviving any grant.
6. Release `EXCLUSIVE`, then the fence, in reverse order.
7. A crash anywhere leaves either the pre-state or the settled state; step 4 is a single atomic
   transition and steps 1–3 are read-only, so there is no torn state and the retry is the next
   sweep.

## 5. Race 2 — the ledger-owned attempt phase

Unchanged in mechanism from v2 and re-verified by C6: identity §2 already requires that RequestId
and ExecutionId are "reserved with uniqueness checked in the corresponding operational ledger
before use", so the durable reservation is existing law, and this design adds a monotone phase and
outcome to it rather than a second record. What v3 adds is the outcome coupling of §2 and the sweep
of §4.

## 6. The commit-admission gate (PS05 bit states)

Unchanged from v2 and re-verified by C7: one atomic bit state, `ADMITTED = 1`, `LATCHED = 2`; `0`
preparing, `1` admitted, `2` latched before admission, `3` admitted then latched; compare-exchange
`0 → 1`; the observer always fetch-ORs `2` including `1 → 3`; no state resets during the attempt;
one internal single-use permit; a latch at state `0` prevents the gate entirely; state `3` records
the latch and forbids further effect admission or retries without revoking or relabelling the
already admitted attempt.

### 6.1 Pending REV correlation

Unchanged: the private association plus the `executionId ↔ operationRef` mapping in
`AttemptCustodyV1`, plus the reader rule that `REV` after `SEAL` in sequence order never implies the
`SEAL` was refused. **No `runId` member is added to `REV`.**

### 6.2 Required delivery after the gate — selected successor law

**Selected, not an open owner choice.** After a latch (state `2` or `3`) the host starts **no new
required-delivery phase**. For state `3` the commit stays committed, the RunId stays observable, and
the required delivery is reported through the existing `DELIVERY.REQUIRED_FAILED` /
`operational-failed` / `delivery-required` route at exit 4. A failed or latching attempt cannot
reacquire authority by opening a delivery phase; a new effect needs a fresh attempt with a fresh
ExecutionId.

For an unlatched ordinary commit (state `1`), required rendering and delivery run as a separate
`SHARED-READ` phase over the committed snapshot, drawing no authority from the returned stopped
cleanup-only session. The handoff is: commit confirmed → stopped session returned → cleanup
`REV`/`CLN` through a fresh lawful level-3 then level-4 append while that session still holds the
operation lease → release the lease → S7 end handoff → then the delivery phase.

### 6.3 Publication does not overwrite the workflow outcome

**A successful publication does not force `success` / exit 0.** The Run's own assessment outcome
survives, and C12 validates each of these against the actual `StepTermination` schema:

- **`policy-failed`** (exit 1) with the committed `runId`. The branch contract requires `runId` for
  `policy-failed`, which a committed Run supplies, so a Run that publishes successfully and then
  fails its policy assessment terminates `policy-failed` carrying that RunId.
- **`indeterminate`** (exit 3) with `reasonCodes`. The branch contract requires `reasonCodes`, drawn
  from the existing closed `D9ReasonCode` set — for example `VERDICT.INDETERMINATE` or
  `COVERAGE.REQUIRED_RELATION_MISSING`. A committed Run whose verdict is indeterminate stays
  indeterminate after publication.
- **An optional surface failure never resets either.** F17 already fixes that an optional effect
  failure is disclosed without rewriting the result. So an optional export or browser launch that
  fails after a `policy-failed` or `indeterminate` Run leaves that class and its
  `runId`/`reasonCodes` exactly as they were; it does not become `success`, and it does not become
  `operational-failed` unless the *required* delivery failed.
- Required delivery failure moves the class to `operational-failed` /
  `DELIVERY.REQUIRED_FAILED` / `delivery-required`, which is the one lawful overwrite, and it still
  preserves the RunId.

## 7. The historical chain-head contradiction — current-owner disposition

carrierFormat 1 §5.4 says "the chain head is in the witness"; the v8 closed witness shape has no
chain-head member. Both documents are immutable and neither is edited. The disposition belongs in
the **current** owner and is patched into security §S1 (superseded selectors) and §S6, stating that
the v8 closed witness shape governs, that the v1 sentence is retained historical prose and is not a
current claim about the witness, and that no current owner asserts interior-prefix authentication.
Old bytes are preserved exactly.

This is a **selected limit with a recorded disposition**, not a remaining gap.
