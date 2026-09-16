# Bounded read-only commit recovery, and the commit-admission gate (PROPOSED v2)

**Standing.** Proposed design/reference correction. Supersedes the v1 draft in this session's v3
output, which is retained unchanged as evidence. No acceptance, readiness, application or
implementation authorization, and no self-acceptance. Authored against frozen Source25
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`.

**What changed from v1, and why.** Root supplied two concurrency schedules that defeat v1. v1 read
the tail, witness and floor once each and treated the resulting tuple as a coherent snapshot. It is
not: reading each field once does not make the tuple coherent. v1 therefore (1) diagnosed a false
carrier quarantine when an ordinary lawful later append advanced the witness past the tail between
two of the reader's own reads, and (2) could report a permanently uncommitted attempt from a stale
ledger snapshot plus a later in-memory liveness check. Both are fixed below, and both are now
covered by **executable schedule controls** rather than fixed tuples: `scratch/controls/c6-schedules.py`
interleaves a lawful writer with a reader that yields after every observation, enumerating 78653
schedules over 14 configurations.

## 1. Conclusion vocabulary and its exact public projection

Internal recovery standings are **not** public D9 classes and must never be spelled like one. In
particular the build plan's internal `indeterminate` conclusion collides with the public D9 class
`indeterminate` (exit 3); the standings below are deliberately spelled differently.

Two distinct namespaces are used, exactly as they exist today:

- **errorCode** — a member of the closed `codeVocabulary.errorCodes` in
  `docs/coop/artifacts/d9-exit-contract.v1.14.json`. No new member is introduced.
- **domainDetail.code** — a member of the single closed registry
  `docs/coop/design-corrections/public-detail-registry.v1.json`, mirrored by
  `workflows/schemas/common.schema.json#/$defs/DomainDetailCode`. No new member is introduced
  here; the one place where the registry has no fitting member is flagged in §1.1 as an owner
  decision rather than silently minted.

| Internal standing | Meaning | class / exit / errorCode | domainDetail.code |
|---|---|---|---|
| `committed-historically` | receipt, association and anchored join all present | success / 0 / — | — |
| `committed-availability-degraded` | as above, current availability is not `retained` | success for history; a *required* object unavailable during a selected operation is operational-failed / 4 / `HOST.IO_FAILURE` | `evidence.missing`, `evidence.corrupt`, `evidence.purged` or `evidence.expired` |
| `terminal-not-committed` | ledger-owned attempt phase is `settled` in the same snapshot and no receipt exists | success / 0 / — (a successful observation, not a refusal) | — |
| `unknown-attempt-open` | attempt phase is `admitted`; not terminal | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` | `PROJECT.BUSY` |
| `unknown-attempt-unobserved` | no attempt row in the snapshot; the snapshot may predate the reservation | operational-failed / 4 / `HOST.IO_FAILURE` | — (subject text only) |
| `unknown-custody` | no anchor reaches the requested sequence, or a join differs | operational-failed / 4 / `HOST.IO_FAILURE` | — (subject text only) |
| `unknown-quarantine-condition` | a **stably observed** owner quarantine condition | operational-failed / 4 / `LEDGER.CORRUPT` | see §1.1 |
| `unavailable-busy` | observations were temporally skewed, or a writer demonstrably holds the resource | operational-failed / 4 / `LEDGER.BUSY_TIMEOUT` | `PROJECT.BUSY` |
| `binding-unusable` | the requested binding names a foreign carrier or a swapped store/namespace | request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` | `RECOVERY.REFUSED` with typed subject text |

`terminal-not-committed` is the identity §5 "failed" answer for the durability-undetermined
recovery path. Reporting it as a *successful observation* rather than a refusal follows the same
pattern the project already selected for availability reporting: the query succeeded, and what it
observed is that the attempt did not commit.

### 1.1 One unresolved public-detail decision, not minted here

A journal-carrier quarantine condition (`uncertainTailLoss`, `witnesslessRestore`,
`witnessMalformed`) has **no** fitting member in the closed 191-member detail registry. Two options,
and this correction deliberately picks neither:

1. **Register one new `DomainDetailCode`** (for example `CARRIER.QUARANTINED`) with the typed
   reason as subject text. Cost: a registry change, the `SECURITY_PUBLIC_DETAIL_CODES` count moves
   off 191, and the `public-domain-details-are-a-closed-set-with-a-bounded-pending-registration-gap`
   sweep must be re-run.
2. **Travel under the existing `MIGRATION.CORRUPT`** code. Cost: `MIGRATION.CORRUPT` is about a
   store transition, so this puts **two remedies behind one code** — which the D9 contract itself
   names a defect ("two codes with the same remedy are a smell, two remedies behind one code is a
   defect").

Option 1 is the cleaner one on the contract's own rule, but it is a registry change and therefore
the owner's call. Until it is decided, the condition projects on `operational-failed / 4 /
`LEDGER.CORRUPT`` with the typed reason as subject text and no registered detail code.

## 2. The algorithm

Read-only throughout. Prohibited for the whole algorithm: the install fence; the writer lease;
`EXCLUSIVE`; any `BEGIN IMMEDIATE`; any `INSERT`/`UPDATE`/`DELETE`; witness `INIT`, `REVERT` or
`ADVANCE`; any witness write; any SC-TRUST high-water raise or copy; any quarantine-marker write;
any new execution grant; any store-binding allocation; any wait on any lock or on the writer; any
repair. Bounded to **exactly one** ledger snapshot, **at most two** journal snapshots, and **at
most four** witness and four floor reads.

### Step 0 — admission

Take the `SHARED-READ` project lease per S7 and obtain the custody-admitted store binding through
an admitted handle and the registry, never from request fields. Compute `storeGenerationDigest`. An
unregistered namespace refuses. No liveness probe of any kind is taken, and no in-memory active set
is consulted at any point.

### Step 1 — one coherent ledger snapshot, carrying the attempt phase

Open one consistent committed reader snapshot and read, **inside that single snapshot**: the
receipt; the private `CommitRecoveryAssociationV1` row; the Run manifest, object references,
availability generation and pins; **and the ledger-owned attempt phase** (§3).

- Ledger unreadable → `unavailable` (F24). Never absence. A failed read, a wrong generation or an
  empty fallback database is never absence.
- Receipt absent and phase `settled` → **`terminal-not-committed`**.
- Receipt absent and phase `admitted` → **`unknown-attempt-open`**.
- Receipt absent and no attempt row → **`unknown-attempt-unobserved`**.
- Exactly one of receipt/association present → `unknown-custody` (F23). Synthesize nothing.
- `storeGenerationDigest` or `namespaceId` mismatch → `binding-unusable` (F27).

Because the receipt and the attempt phase are owned by the same ledger and read in the same
snapshot, they are coherent by construction. That is what removes race 2 (§3).

### Step 2 — bracketed capture of the carrier observations

The tail, witness and floor are three independently timed observations. A capture makes their
mutual coherence **checkable** instead of assumed:

```
capture():
    W_before = read_witness()          # observation 1
    H_before = read_floor()            # observation 2
    J        = snapshot_journal()      # observation 3  (point-in-time consistent read)
    W_after  = read_witness()          # observation 4
    H_after  = read_floor()            # observation 5
    stableW  = (W_before == W_after)   # byte equality of the whole witness record
    stableH  = (H_before == H_after)   # byte equality of the whole floor record
    return {J, W: W_after, H: H_after, stableW, stableH}
```

**What stability buys, stated as an assumption rather than a proof.** If the witness record is
byte-identical before and after the journal snapshot, then either it was constant across the
snapshot or it changed and changed back. Changing back requires lowering `seq` or returning to
`PENDING` at the same `seq`. The append protocol never does either within an attempt (v8 §5.4:
PENDING n+1 → durable append → COMMITTED n+1, and PS05 adds "no state resets during the attempt"),
and `REVERT`/`ADVANCE` require an authorized lifecycle open, which holds the fence and therefore
cannot run concurrently with an `APPEND-WRITE` operation on the same namespace. The floor is
written only under the fence at operation start and end and is monotone except through S4.5. So
under protected custody, byte-stability across the snapshot implies the observation was coherent
with it. **This is an assumption about the writer protocol, not a cryptographic guarantee**; if a
future writer changes the witness non-monotonically within an attempt, this reasoning fails and the
protocol must be revisited.

### Step 3 — anchor selection, and the one permitted retry

Let `k = A.journalSeq` and `t` be the captured tail. Classify the capture:

| Witness state | Anchor class | Requires |
|---|---|---|
| `COMMITTED`, `seq == t`, `bodySha256 == body_sha256[t]` | `witness-committed-tail` | `stableW` |
| `PENDING`, `seq == t`, `bodySha256 == body_sha256[t]` | `witness-pending-at-tail` | `stableW`; report `witnessWouldAdvance`; perform **no** ADVANCE |
| `PENDING`, `seq == t + 1`, and `k <= H.lastSeq` | `sc-trust-floor` | `stableH` |
| `PENDING`, `seq == t + 1`, and `k > H.lastSeq` | none | `unknown-custody`, explicitly **not** invalidated (F45) |
| anything else | none | adverse candidate, see §4 |

An anchor is **usable** only when its own stability flag holds. Confirm `committed-historically`
when a usable anchor exists and there is no ordering hazard (`k <= t`).

Otherwise take **one** fresh capture — the single permitted retry. It also supplies the second tail
observation that §4 requires. If the retry yields a usable anchor with no hazard, confirm. This is
what resolves root's schedule 1: in that schedule the first capture has `stableW == false`, so the
witness anchor is unusable and no quarantine is diagnosed; the decision falls to the floor anchor
or to the retry, both of which confirm `k = 9` correctly.

**Ordering hazard.** If `k > t` after the retry: when `stableH`, `H.lastSeq >= k` and the two tails
agree, the floor proves the prefix once existed while the tail is below an observed floor — the F22
condition. Otherwise `unavailable-busy`, attributed to the **security carrier owner**. Never
`uncommitted`, and never a conclusion drawn from two different snapshots.

## 4. Which stable observations are necessary before reporting an owner quarantine condition

Root asked for this explicitly. A read-only reader may report an owner quarantine/corruption
condition **only** when all of the following hold. Otherwise the mismatch is attributed to temporal
skew and reported as `unavailable-busy`.

1. **Stable witness bracket** — the two witness reads bracketing the deciding journal snapshot are
   byte-identical (`stableW`).
2. **Stable floor bracket** — the two floor reads bracketing the same snapshot are byte-identical
   (`stableH`).
3. **Stable tail** — two journal snapshots agree on **both** the tail sequence and the tail body
   digest.
4. **Closed witness shape validated before any comparison** — the v8 §5.4 closed shape, with
   `bodySha256` present (absent is not null) and `PENDING` requiring `seq >= 1`.
5. **Carrier naming matches** — `projectKeyDigest` and `grantGeneration` equal the association's.

Conditions 1–3 apply even to conditions that look intrinsically structural. A torn read of the
witness file can look malformed, so `witnessMalformed` also requires stability before it is
reported as an owner condition. This is the conservative attribution root required:
**read-only never invents a corruption diagnosis from independently timed observations.**

The converse is also verified, so that the stability gate has not silently disabled the diagnosis:
five quiescent genuinely-adverse carriers (witness committed beyond the tail; tail below the
observed floor; foreign carrier; malformed witness sequence; floor digest contradicting the tail)
each still report `unknown-quarantine-condition` (C6 configurations Q1–Q5).

## 5. Race 2 — the ledger-owned attempt phase

v1 checked liveness after taking the ledger snapshot, so a writer that committed and exited in
between produced a false `not-committed-verified-absent`. Mere absence from an in-memory active set
is not terminal proof, and neither is any separately timed probe.

**Existing owners, traced before proposing anything.** Identity §2 already requires that
"both RequestId and ExecutionId use independent 16-byte host-CSPRNG draws, **reserved with
uniqueness checked in the corresponding operational ledger before use**". So a durable,
ledger-side ExecutionId reservation is *already* required law — the admitted phase exists. The
receipt (identity §5 step 3) and `CommitRecoveryAssociationV1` carry `executionId`. D9 fixes
`requiredTerminationIdentity: executionId` and "the settled ExecutionId is terminal". The journal
carries `operation_ref`, and `RCO`/`ICO`/`CLN`/`REV` records terminate an operation.

**What is genuinely missing.** Nothing durably records that a *particular ExecutionId* reached a
terminal state when it did **not** commit. The `executionId ↔ operationRef` map is private host
state, and its only durable home is the association row, which exists only on success. Identity §6
states `recover(ExecutionId)` "inspects the committed receipt after a lost acknowledgement" — it
has no statement at all for the absent-receipt case. That is the gap.

**Minimal new requirement.** Extend the *already required* ExecutionId ledger reservation with a
monotone phase, rather than adding a second record:

```
AttemptCustodyV1 { recordSchema: 1, storeGenerationDigest, namespaceId,
                   executionId, operationRef,
                   phase: "admitted" | "settled",
                   settledOutcome: null | "committed" | "refused" | "undetermined" }
```

Laws: written by the guarded commit facade only; `admitted → settled` is the only transition; never
reversed, never deleted, never re-opened; the settle write is ordered **after** the receipt write,
so a single coherent snapshot can never show `settled` without a receipt that was committed
earlier; and it **authorizes nothing** — settling records an outcome and never licenses a retry, so
the settled-ExecutionId-is-terminal law is preserved exactly.

**The crash case stays unknown, honestly.** A writer that dies before settling leaves `admitted`
forever, and read-only recovery reports `unknown-attempt-open` indefinitely. Settling such an
attempt requires an **authorized sweep** that may take the fence and the S7 non-blocking lease
census — which is explicitly *not* read-only work and is not specified here. Until that sweep runs,
unknown remains unknown. This is a required companion obligation, named and not discharged.

## 6. The commit-admission gate (PS05 bit states)

Root's selected wording is adopted verbatim in behaviour and modelled in
`scratch/controls/c7-gate-bits.py`: one atomic bit state, `ADMITTED = 1`, `LATCHED = 2`;
`0` preparing, `1` admitted, `2` latched before admission, `3` admitted then latched. Commit
admission is compare-exchange `0 → 1`. The observer always fetch-ORs `2`, including `1 → 3`, so a
post-admission latch cannot be lost. No state resets during the attempt. A successful gate mints
**one internal single-use permit** for the already prepared commit; it is not a reusable grant for
later effects. A latch winning at state `0` prevents the gate entirely. State `3` does **not**
revoke the already admitted attempt or relabel its outcome: it records the latch and forbids
further effect admission or retries.

Executed: 132 schedules, 0 violations, all four states observed, the permit is single-use, the
observer's fetch-OR is idempotent and never clears `ADMITTED`, and a compare-exchange from state
`2` fails.

Outcome mapping, preserving existing D9 behaviour unchanged:

| Situation | Standing | class / exit / errorCode | RunId observable |
|---|---|---|---|
| latch won before the gate (state 2) | `uncommitted` | no commit issued; a durable SEAL remains an uncommitted attempt (F36) | no |
| admitted, commit confirmed (state 1) | `committed` | success / 0 | **yes** |
| admitted then latched, commit confirmed (state 3) | `committed-delivery-failed` | operational-failed / 4 / `DELIVERY.REQUIRED_FAILED` | **yes** |
| admitted, commit error or barrier unconfirmed | `durability-undetermined` | operational-failed / 4 / `DURABILITY.COMMIT_FAILED` | **no** |

Two existing laws that are easy to lose, and are asserted by the model: a
`durability-undetermined` response **omits `runId`** while retaining `executionId`, because RunId is
externally observable only for a committed Run; and the settled ExecutionId is **terminal**, so
there is no automatic write retry and a later attempt receives a fresh ExecutionId.

### 6.1 Pending REV correlation — no new journal field

The followup's remedy requiring the post-release `REV` to record the SEAL `journalSeq` is not
implementable: the schema-3 `JournalRecord` is closed and has no sequence-valued member. The
resolution is the private `CommitRecoveryAssociationV1` plus the host's private
`executionId ↔ operationRef` map, **plus a reader rule**: *`REV` appearing after `SEAL` in sequence
order never implies the `SEAL` was refused.* The S6 linearization law constrains only the other
direction (after `REV`, no `SEAL`). No `runId` member is added to `REV`; the private association and
operation mapping plus this reader rule suffice, and no case in C6 or C7 required more.

## 7. The delivery phase after a successful commit

Root asked whether a normal successful commit that returns a stopped cleanup-only session can still
complete required rendering/delivery. **It can, as a separate phase, and it needs no authority from
that session.**

Required rendering/delivery is a read-and-materialise activity. S7 places rendering in
`SHARED-READ` mode alongside queries and doctor. It is not a brokered effect, so it draws nothing
from the closed session, and the closed session grants nothing. Explicit handoff:

1. Commit confirmed; `PublishedCommit` produced.
2. Security returns the stopped cleanup-only session, which still owns the operation lease and
   admits cleanup only.
3. Host records any cleanup `REV`/`CLN` through a fresh lawful level-3 then level-4 append while
   that stopped session still holds the operation lease.
4. Host releases the operation lease and performs the ordinary S7 end handoff.
5. Required rendering/delivery then runs as a **new `SHARED-READ` phase** over the committed
   snapshot, with no session, no effect authority and no grant reuse. Its failure is the existing
   `DELIVERY.REQUIRED_FAILED` / operational-failed / exit 4, preserving the RunId (F16).

**A latched attempt gets no workaround.** States 2 and 3 forbid starting a delivery phase.
Delivery admits no effect, and a new effect requires a fresh attempt with a fresh ExecutionId, so a
failed or latching attempt cannot reacquire authority by opening a delivery phase.

**One owner choice recorded, not settled.** For state 3 this correction selects the conservative
reading: no delivery phase is started, and the required delivery is reported failed through the
existing code while the commit stays committed and the RunId stays observable. An owner could
instead permit delivery for state 3, on the reading that disclosing an already committed Run is a
disclosure obligation rather than a new effect. S6 cancellation "refuse[s] further requests", which
is why the conservative reading was selected; the alternative is flagged for the owner.

## 8. Where this differs from the prior followup algorithm

1. **Ordering and coherence.** The followup gives a predicate over one joint observation. This
   defines the capture order, the stability brackets, the single permitted retry, and the exact
   stable observations required before any owner condition may be reported (§4).
2. **Digest rule refuted by execution.** The followup requires `body_sha256[j] == SHA256(body[j])`.
   The frozen implementation computes the domain-framed digest, so a validator implementing the
   followup literally rejects every lawful record.
3. **The anchor claim is narrowed** to `confirmed-under-retained-custody`, with
   `interior-bodies-not-authenticated` on every confirming result.
4. **A citation conflation corrected without changing its conclusion**: the followup calls the
   SC-TRUST high-water "the witness", citing carrierFormat 1 §5.4 which does use one name for both.
   v8 §5.4 separates them, and `DURABILITY_BOUNDARIES` lists `witness-write` and
   `sc-trust-high-water-copy` separately. The followup's conclusion survives under that separation.
5. **The high-water had no closed shape**; `CarrierHighWaterV1` closes that.
6. **Conclusion vocabulary** separated from the public D9 class names, with both namespaces pinned
   exactly (§1).
7. **CR-23 linearization point corrected**: callback entry is wrong; the atomic
   `preparing → commit-admitted` transition is right, which is what root already specified.
8. **CR-23 remedy (iv) is not implementable as written** (§6.1).
