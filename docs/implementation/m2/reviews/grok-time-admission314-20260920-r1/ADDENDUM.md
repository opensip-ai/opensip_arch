# Addendum — continuity carry, S4.5 context.time, and tEval kind

**Standing:** separate source addendum to frozen 314 assistance. Does **not** edit `REVIEW.md`. Not a schema/product change and not native 313 review. 313 remains separate codec integration.

The tEval vs floor split in REVIEW §2 **stands**. Three REVIEW claims do **not**, as written.

---

## 1. Same-store `previous` is not the continuity carry path

REVIEW §1’s `while c.previous` loop is **same-store predecessor reconstruction only**. It does not admit a continuity target whose first capsule is revision 1 / `previous: null`, and it does not select source vs target L.

### Encoded continuity edges (227 EVENT-JOINS, 222)

`ContinuityEventV1` (required): `side` source|target, `case` forward|ancestor, `executionId`, `intentDigest`, `sourceBeforeImage` (**NodeRef**, full `{sha256,bytes}`), `sourceEventHead` (EventRef or null), `targetBefore` = `absent{absenceProof}` (forward) or `capsule{image}` (ancestor). Shape **rejects** `sourceAfterImage` and any AFTER/carrier/descriptor member — cross-store acyclicity. `sourceEventHead` must equal `sourceBeforeImage.eventHead` (null only if that image has none).

AFTER bytes are **not** on the event. 222: `TrustContinuityV1` holds `sourceBefore/sourceAfter/targetBefore/targetAfter` **raw capsule hashes** plus **immutable source-after and target-after images under the carrier**. `sourceFence` on the source AFTER is `{executionId,intentDigest,sourceBefore,by:EventRef}`. No fresh S4 in Phase B; no clock recomputation from current wall.

Forward target: new store, revision 1, `previous: null` (222: a transition creates the new store’s first capsule at revision 1). The target does not contain a same-store previous chain back to the source.

### Where the original T proof lives

Start **AdmitFloor** from the **retained CapsuleImage** that actually contributed the selected L, not from the new store’s `previous`.

| Case | Image that holds the supporting T | Then |
|---|---|---|
| Forward | `sourceBeforeImage` (event NodeRef → records, exact capsule bytes) | Reconstruct that **source** store’s establishing clock-write via that image’s `publication` (PublicationRef has `previousCapsule`, descriptor `sha256` **and** `bytes`) |
| Ancestor, L_source > L_target | source-BEFORE image | same |
| Ancestor, L_target > L_source | `targetBefore.image` | walk **that** store |
| Restore N vs n | reconstructed capsule **N** | 222: retain the proof supporting the **selected** L |

201 S9 / 222 copy/max: floors copy forward into a new store; ancestor/rollback takes the **maximum** of both stores; poisoned floors are not lowered (only S4.5 lowers F). Continuity “retaining the exact proof supporting the selected L” means: if `max(L_s, L_t)` is `L_s`, carry **source** `timeEvidence`; if `L_t`, carry **target** `timeEvidence`.

**Equal-L, different T:** both sides have the same `lastAccepted` timestamp and distinct T NodeRefs. No cited owner picks source vs target vs refuse-as-fork. 222 identity-fork language is for **signed metadata bodies** at equal version, not for two lawful T proofs of equal L. **Unresolved.** Do not invent a hash-maximum or “prefer source” rule here.

### `eventHead` and bare `previous`

REVIEW’s table “last event **of this revision**” copies 222’s member sentence and is **too strong**. 227 PROOF-NODE-JOINS: an empty-event shared-head publication keeps **unchanged** `eventHead` when no L/T advance is due. `eventHead` is the last event **still projected on this capsule**, which may predate this revision. Do not treat `start.eventHead` as this revision’s clock-write. Assumption C’s *advice* (use the establishing descriptor) stands; the wording does not.

`capsule.previous` is a **bare SHA-256**, not a NodeRef (no `bytes`). 222: it is a predecessor **consistency pin**, “not permission to search for or reinstall an older state.” NodeRef loads at `records/sha256` require declared length before allocate. **Do not** `get(records, previous)`.

Qualified capture, in order:

1. **Current file** `I/trust/stores/S/state.v1` under custody (length from the admitted file).
2. **Publication reconstruction:** `PublicationRef = {previousCapsule, sha256, bytes}`. Reconstruct capsule *n* by adding D(*n*)’s PublicationRef onto D(*n*).`afterProjection` and checking raw digest (222 predecessor-prover rule). Descriptor `bytes` bound the read. `previousCapsule` on D(*n*+1) is the SHA pin to that reconstruction.
3. **Retained CapsuleImage NodeRef** (`sourceBeforeImage`, ancestor `targetBefore.image`, restore proof images): full `{sha256,bytes}` at records. Image hash = raw capsule hash (227). Image ≠ current standing.
4. **Carrier AFTER images** for continuity completion only; events must not name them.

Not every historical raw capsule exists under `records/<hash>`. Orphans and search-by-digest are unavailable.

---

## 2. The missing-old-T exception is not a skip of every `context.time`

REVIEW §3 “missing `acceptedAuthority.context.time` bytes must not fail S4.5” **broadens** 215 D / 227. That sentence is **withdrawn**.

215 D names operations **not dependent on the old T**: read-only diagnostics, ABORT / private batch termination, retained-phase S4.5 challenge/import. “Old T” there is the **current clock’s** `timeEvidence` (the T supporting L on `beforeImage`). 227: do not traverse old T **solely because it appears in beforeImage**; prove `beforeRecord` and **accepted recovery authority independently**.

### Settled skips (S4.5 / ABORT)

- **Do not** `AdmitFloor(beforeImage, beforeImage.clock.timeEvidence)` — that is the owned missing-**old-T** exception.
- **Do not** treat that skip as “T was verified.”
- ABORT still admits numeric F/L and outside-ceremony accepted-document fields; unreadable **those** prerequisites are unavailable, not known absence.

### Settled loads (not old T)

S4.5 **does** require, and missing bytes **do** fail:

- `S45EpochInput` itself; `beforeImage` capsule image; exact `beforeRecord`.
- Epoch/challenge documents, observation, serial/window/boot as owned.
- **`acceptedAuthority` NodeRef target** (the RootAdmission **record**). Orphan authenticated root is insufficient (227 TIME-INPUT-JOINS).
- Literal **accepted-in-this-image** joins: `acceptedAuthority == beforeImage.heads.root.admission` (hash **and** length), plus document/binding/`rootVersion` (312 P2 literals). These reads do **not** load `context.time`.
- Time-free root-edge / parent-chain / 229 complete-embedded authentication (227 PROOF-NODE-JOINS: chain auth precedes S4; S4.5 is not ordinary S4 but the same time-free ancestry rule applies to proving that head).

Those are **current/proven capsule + exact accepted-root/history byte bindings**. They authorize recovery **without** claiming a complete historical `AdmitTEval` of that RootAdmission.

### Not owned as optional integrity

`OriginalContext.time` is a **required** field on ordinary/recovery RootAdmission. Absence of its **target evaluation bytes** is not the same fact as absence of the current clock’s old T.

Mode A needs that evaluation’s `beforeImage`, observation, and (V2) authority in order to re-derive original tEval. 215 D’s S4.5 exception does **not** say those historical evaluation inputs are optional. REVIEW’s “if present, optional integrity; if missing, do not fail” was inference. **Do not** classify every absent historical time input as skippable.

**Unresolved owner datum:** whether S4.5 must `AdmitTEval(acceptedAuthority.context.time)` at all.

- If **no**: do not load that target; do not call missing bytes a skip — they are **out of scope** for this operation. The independently admitted before-image head + epoch input suffice.
- If **yes**: missing target is **unavailable** (a real prerequisite), distinct from missing old T, and the exception as written is **not executable** whenever a long-lived P2 head’s original evaluation was not retained.

This addendum does **not** pick. 215 D “original recovery-authority context” on successful S4.5 is the epoch’s `acceptedAuthority` **record** plus challenge/before-record, which is loadable without following `.context.time`. That is the narrower reading. It is not a license to drop other S4.5 prerequisites.

Same split for `revocationHistory` / `admittingRoot.context.time`: do not `AdmitFloor` old T through that path; do not silently skip a missing **history node** or list DocRef.

---

## 3. S4.5 is not metadata/root tEval

REVIEW §2 mode A “successful non-report-only S4 **(or S4.5)**” as `OriginalContext.time` **over-grants**. Withdrawn for root/metadata admission.

215: the clock-floor `trust-recovery-epoch` **changes neither role states nor root authority**. “Root-ceremony recovery never doubles as floor recovery.” COMMIT: “S4 write-ahead is a separate earlier capsule revision”; `issuedAt <= tEval < notAfter` at COMMIT is that **S4** evaluation, not the epoch node. 227: S4.5-challenge cannot be cited as S4 tEval; S4.5-apply is a clock source, not a PRESENT/COMMIT evaluation.

Structural `TimeEvidenceV1` = S4 evaluation **union** epoch. Typed `OriginalContext.time` → `TimeEvidenceV1` is therefore **broader than allowed use**. Union membership is not permission to activate a head from epoch recovery.

| Use | Allowed evaluation kind |
|---|---|
| `ClockWriteEvent.evaluation` for `source: s4.5-apply` | `S45EpochInputV1` (clock revision only) |
| Capsule `clock.timeEvidence` after successful S4.5 | epoch node as **floor T** (mode B, new even equal-L) |
| `RootAdmission.context.time` / `MetadataAdmission.context.time` | **S4** evaluation (Keep allowed). Subsequent PRESENT/COMMIT still runs S4 write-ahead; Keep may preserve the epoch T as floor while `evaluation` is a fresh S4 node |

Do not grant TRUSTED-entry or catalog/revocation activation from an epoch input. After S4.5, the next metadata admission still owes a successful non-report **S4** at current observation (227 BEGIN/COMMIT current-context rule). That S4 may Keep the epoch T.

---

## What still stands / what is withdrawn

| Claim | Status |
|---|---|
| tEval vs floor are different predicates on existing wires | **Stands** |
| Start floor proof from a capsule/image, never from T alone | **Stands** |
| Same-store `previous` loop admits continuity carry | **Withdrawn** |
| `eventHead` is always this revision’s last event | **Withdrawn** (empty-event carries it) |
| Bare `previous` SHA is a records NodeRef load | **Withdrawn** |
| Missing `acceptedAuthority.context.time` must not fail S4.5 | **Withdrawn** (not the owned old-T skip) |
| Skip `AdmitFloor` on S4.5/ABORT **current-clock** old T | **Stands** |
| Accepted-in-beforeImage via head NodeRef/document/binding | **Stands** (does not load `context.time`) |
| Mode A may use S4.5 as root/metadata `OriginalContext.time` | **Withdrawn** |
| Equal-L different-T continuity selection | **Unresolved** |
| Whether S4.5 `AdmitTEval`s `acceptedAuthority.context.time` | **Unresolved** |

No code, schema, or frozen-source edits. Native 313 is not this admitter. Stop.
