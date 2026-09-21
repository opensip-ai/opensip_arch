# Independent source assistance — scoped time-proof admission 314

**Standing:** bounded source assistance while native 313 integrates 127-shape / typed-reader / V2 P2 assembly. **Not** codec approval, native 313 review, publication qualification, or product installation. Installed product remains `fa72e50`. Prior 309–312 reports were not edited (312 fully read as bounded codec correction). No new trial extract; documents are the already-verified 310 packet plus 312 successor schema. Trust those frozen hashes over live prose.

Python 3.12.13 `-I -B`. No native tests. No product/frozen edits.

Pins: 215 r14 OWNER `d8165f14…19fa`; 225 TIME-PRODUCER `804134cd…0843`; 222 PERSISTENCE `f8ddaecc…092e`; 227 TIME-INPUT-JOINS `912110ff…a2d6`, PROOF-NODE-JOINS `fd687e4e…3e10`, EVENT-JOINS `69000c34…a806`, PENDING-JOINS `a4e6262d…acaa`; 229 OWNER `f0860bf6…0f92`; 312 OWNER `aeebe5ae…076d`; successor schema `a0431300…7928`. Evidence: `grok-out/source-pins.json`.

Preserved: 309 `6a47037d…eb67`; 310 REVIEW/FOLLOWTHROUGH/ADDENDUM `fb443e04…` / `1c8c2ace…` / `6d7c499d…`; 311 `02e8228a…d1f1`; 312 `4b91fece…71ff`.

---

## What is already sufficient vs what is missing

No new wire field is required for the three questions below. The locators exist. What is missing is a **scoped admitter**: two internal proof modes over existing NodeRefs, plus a traversal policy that does not eagerly follow old T into S4.5 / safe ABORT. PENDING-JOINS item 1 already names this distinction. A generic recursive walker is an implementation obligation, not a newly discovered missing field (310 REVIEW standing; 227 TIME-INPUT-JOINS: “scope-sensitive admission is mandatory”).

Do not invent current-core/current-time substitution, universal creator equality, or a boolean `accepted:true`.

---

## 1. Establishing that retained T was consumed by a durable L-writing S4 or successful S4.5

227: TimeEvidence union membership is **not** a floor. Admissible T needs the exact successful write and its durable publication/context. T is an **upstream input** and **must not** point at its consuming clock-event, descriptor, or AFTER capsule.

### Encoded locators (start from a capsule, never from T alone)

| Locator | Collection | What it names |
|---|---|---|
| `TrustCapsuleV1.clock.timeEvidence` | records NodeRef | current T on P1/P2 (absent on P0) |
| `TrustCapsuleV1.publication` | PublicationRef | this revision’s descriptor (`previousCapsule`, sha256, bytes) |
| `TrustCapsuleV1.eventHead` | EventRef | last event **of this revision** |
| `TrustCapsuleV1.previous` | raw capsule SHA | previous capsule bytes (not a search key) |
| `PublicationDescriptorV1.events` | EventRef list | events prepared for this revision |
| `PublicationDescriptorV1.afterProjection` | capsule minus `publication` | prospective clock/heads/eventHead |
| `ClockWriteEventV1.evaluation` | NodeRef | **fresh** S4 or S4.5 input of this write (311: always present on a write) |
| `ClockWriteEventV1.timeEvidence` | `{kind:new, proof}` **or** `{kind:kept}` | new T NodeRef **only when kind is new**; **kept has no proof field** |
| Role-event `clock.kind=clock-write.by` | EventRef | earlier durable clock-write (not a T backref) |

Schema fact: S4 `kept` and S4.5-challenge are `{kind:"kept"}` only. The kept T lives on the **capsule**, not on the event. S4 `new` and S4.5-apply carry `proof` equal to the evaluation node (S4: T iff `lastAccepted` ∈ writes; S4.5-apply: always new even equal-L).

222: an evaluated import publishes the **S4 clock revision first** (own descriptor + clock-write event), then a role/head outcome whose `previous` is that clock revision. Empty-event shared-head publications exist only when **no L/T advance** is due; the establishing clock-write is then on an **earlier** revision.

### Starting roots (bounded; no store-wide search)

1. **Current native capsule** `I/trust/stores/S/state.v1` under fence/custody — for the live T.
2. **Proven historical capsule** reconstructed from an admitted PublicationRef (continuity source-BEFORE/AFTER image, or restore-recovery reconstructed N). A lone orphan descriptor does **not** start a walk (222).

From T’s NodeRef in `records/` there is **no** encoded consumer edge. That is acyclicity, not a gap. If the caller has only an orphan T, the result is **unavailable**, not a census of `clock-write` events.

### Structural walk (not 222 durability)

```
# mode B — established-floor
# start = admitted current capsule OR reconstructed proven capsule
# T    = start.clock.timeEvidence   (require P1/P2)
admit_floor(start, T, budget):
  require start.clock.timeEvidence == T
  c = start
  while c.previous is not null:
    prev = load_capsule_bytes(c.previous)          # records identity = raw SHA
    require same store; charge budget
    if prev.clock.timeEvidence != T: break
    c = prev                                       # walk to FIRST capsule that holds T
  establishing = c
  D = load_descriptor(establishing.publication)    # PublicationRef path, not listing
  require D.store/revision/previousCapsule join establishing
  CWs = [e in D.events | kind == clock-write]
  require |CWs| == 1                               # clock revision; see assumption A
  cw = CWs[0]
  if cw.source == s4:
    require "lastAccepted" in cw.writes
    require cw.timeEvidence == {kind: new, proof: T}
    require cw.evaluation == T                     # new T IS the evaluation node
    recompute S4 from T's retained observation/source (original context, not current wall)
    require lastAcceptedWrite is not None and non-report-only
  elif cw.source == s4.5-apply:
    require cw.timeEvidence == {kind: new, proof: T}
    require cw.evaluation == T                     # epoch node is new T even equal-L
    admit epoch guards (beforeRecord, challenge, acceptedAuthority-in-beforeImage)
  else: refuse                                     # challenge never establishes T
  # THEN, separately:
  admit_222_durable_current(establishing)
```

`admit_222_durable_current` is **not** the graph walk. It is 222 predecessor-keyed unique successor proof: nativeBefore/previousCapsule, original **direct** terminal witness (smallest digest among direct provers), fence, parent barrier. Structural membership of T in a descriptor is not proof that revision was durably current.

**Kept-T over later F/anchor writes:** later capsules still have `clock.timeEvidence == T`; their clock-write has `{kind:kept}` and a **different** `evaluation` NodeRef. The while-loop above skips those until the first capsule whose T appeared. That first revision must be `kind:new`.

**Continuity:** no fresh S4 in Phase B; carry exact T. Floor proof starts from the **source-side** establishing clock revision of the carried L, not from the continuity event.

**Restore:** admit N’s original time proof from the reconstructed capsule N (already independently proven). Do not start from observed n. F may be max(n,N); L’s supporting T is N’s T (222 copy/max).

### Assumptions (uncertain)

- **A.** The first capsule that holds a new T is a 222 clock-only revision whose descriptor lists exactly one `clock-write`. If a producer ever bundled the first L-write with role events in one revision, take the unique `clock-write` in that descriptor whose `timeEvidence.proof == T`. Empty-event later revisions are not establishing revisions.
- **B.** `afterProjection.clock.timeEvidence` equals the installed capsule’s T. Use the installed capsule when present; the projection is preflight, not authority.
- **C.** `eventHead` on a **role-outcome** revision is not the clock-write. Always load the descriptor of the **establishing** capsule, not `start.eventHead`.

### Encoding gap?

**None for locators** if the starting root is a capsule/PublicationRef. **Remaining law:** native 222 unique/durable publication is still unimplemented; 313 as stated does not close it. Do not treat a successful typed walk as a floor grant.

---

## 2. Fresh evaluation (tEval) vs established floor (T)

311/227: every write-bearing S4 constructs a **fresh** `S4EvaluationInput`; Keep returns the **exact old T** as `timeEvidence`. BEGIN/COMMIT re-evaluate under **current** context even when payload bytes are identical; unchanged L **keeps** original T. 225: “Keep prior timeEvidence exactly whenever L is unchanged; do not replace it merely to point at a newly evaluated operation.”

`OriginalContextV1.time` is a **required** NodeRef on ordinary/recovery `RootAdmissionNodeV1` and on `MetadataAdmissionNodeV1`. 227 PROOF-NODE-JOINS: a RootAdmission may retain the **upstream evaluation input** for original context; the S4 verifier must not need a **future** same-operation root-node hash. So `context.time` is the evaluation that supplied **tEval for that authentication edge**, which **may Keep old T**.

These are two predicates on **existing** fields. They must not be collapsed.

| Mode | Existing wire | Predicate | `lastAcceptedWrite` |
|---|---|---|---|
| **A — tEval-context** | `OriginalContext.time` (and `ClockWriteEvent.evaluation`) | Successful **non-report-only** S4 (or S4.5) evaluation at the **original** observation/source; closed shape; 312 V2 CoreAnchor/before-head joins when those bytes are V2 | **Not required.** Keep is a successful evaluation. |
| **B — established-floor** | capsule `clock.timeEvidence` | §1: L-writing S4 (`lastAccepted` ∈ writes, `kind:new`) **or** successful S4.5-apply (`kind:new` always) plus 222 durable current | Required for ordinary S4 floor; S4.5 replaces provenance of L even equal-L |

When S4 is `NewRequired`, the two NodeRefs **coincide** (evaluation is T) but the predicates still differ (successful eval vs L-write + durable publication). When Keep, they are **different NodeRefs**: `evaluation ≠ T`. Requiring `lastAcceptedWrite` on every `context.time` would refuse lawful BEGIN/COMMIT/Keep and contradict 225/227/311.

No source/kind/arithmetic change. No new schema member. Internal admitter modes `AdmitTEval(node)` vs `AdmitFloor(capsule, T)` are enough.

**Do not** point `OriginalContext.time` at the kept T in order to “prove L” — that would lose the current-context evaluation that 227 requires on BEGIN/COMMIT. Floor proof is a **separate** walk from the before-image capsule.

---

## 3. Narrow S4.5 and safe-ABORT exceptions — do not pull old T through `context.time`

215 D and 227 PROOF-NODE-JOINS already list the **non-dependent** operations: read-only diagnostics, ABORT / private batch termination, retained-phase S4.5 challenge/import. Ordinary entry, BEGIN/COMMIT, continuity, and full restore **are** dependent and still need the complete time closure.

The side path: `S45EpochInputV1.acceptedAuthority` → `RootAdmissionNodeV1` (ordinary, required `context.time`) and `revocationHistory` → list node `admittingRoot` → another `context.time`. A generic walker that runs **mode B** on every `OriginalContext.time` will demand the missing old T that the exception exists to skip. That is a **walker-policy conflict**, not a missing field. If the exception cannot run, S4.5/ABORT are not executable as owned.

### Scoped prerequisites (do not claim skipped evidence verified)

**S4.5-apply / challenge (P2 only; P0/P1 refuse before challenge):**

- Require `beforeImage.clock.phase == retained`, exact `beforeRecord == beforeImage.clock.record`.
- Admit epoch/challenge docs, observation, serial/challenge/window/boot as owned.
- `acceptedAuthority` must **equal** `beforeImage.heads.root.admission` (NodeRef hash+length). An orphan authenticated root is insufficient (227 TIME-INPUT-JOINS).
- Re-authenticate that admission **edge** (signatures, parent, 229 complete embedded chain if the parent walk reaches CoreAnchor). This is authentication, not “T was verified.”
- **Do not** run mode B on `beforeImage.clock.timeEvidence`.
- **Do not** run mode B on `acceptedAuthority.context.time` or on catalog/revocation `context.time` reached from this image.
- If those `context.time` **bytes** are present, mode A (shape + original observation integrity) is optional integrity; **missing bytes must not fail S4.5**. Unreadable **epoch/authority/challenge** prerequisites remain unavailable (not known absence).
- On success, new T = epoch node; L provenance is the epoch proof; old T is not claimed verified; L is not lowered (F may equal L).

**Safe ABORT:**

- P0/P1, never-established recovering members, known-absent accepted-document times, no accepted root: **no S4**, role-event `clock = {kind:not-required, reason:pregenesis-abort-no-time-cause}`, no time-input node. Unreadable evidence ≠ known absence.
- P2, time-dependent still-true **outside-ceremony** cause: no-source S4 using admitted numeric F/L and accepted-document fields; **no** new signed witness; may write F/anchor; **never** L or T. Do not admit old T. Do not claim T verified.
- Interrupted members keep their named exit; do not fabricate RECOVER-ABORT.
- `observed-context` is only EV-REVOKE / EV-QUORUM-OBSERVE as owned; it cannot back PRESENT/BEGIN/COMMIT/CLOCK/INSTALL/CONTINUE.

**History merge/list:** admittingRoot proves the list/authentication edge. Do not recurse mode B through `admittingRoot.context.time`. History existence is not accepted-head inference (222).

**Must never inherit the exception:** ordinary import/refresh/bootstrap, BEGIN/COMMIT, continuity (carried L), restore (N’s original T), new T1 entry. Presence of a T locator is not its admission.

### Owner conflict if the exception is not executable

If an admitter always follows `OriginalContext.time` as TimeEvidence **and** requires mode B, it contradicts 215 D / 227 PROOF-NODE-JOINS / PENDING-JOINS §1. The fix is the scoped table above, not a new optional `time` field and not a generic skip flag. A skip flag would be a “generic trust boolean.”

**Assumption D (uncertain):** whether `acceptedAuthority.context.time` for a long-lived P2 head is typically the **Keep evaluation of the last shared-head update** or the **original L-establishing T**. Either way, S4.5 must not require mode B on it. 313 should not encode a recursive floor walk here.

---

## Proposed admitter surface (for the 313 implementer)

```
enum Traversal:
  Dependent   # ordinary entry, BEGIN/COMMIT, continuity, restore
  S45         # retained-phase challenge/import
  Abort       # safe ABORT / private batch termination
  Diagnostic  # read-only; may report recorded F/L/T without claiming proof

AdmitTEval(eval_ref):          # mode A; Keep allowed
AdmitFloor(capsule, T):        # mode B; §1 walk + 222 durable current

admit(op, capsule, traversal):
  if traversal == Dependent:
    AdmitFloor(capsule, capsule.clock.timeEvidence)
    for each RootAdmission/MetadataAdmission actually used as CURRENT authority:
      AdmitTEval(node.context.time)          # may be Keep eval ≠ T
      # 312: V2 authority CoreAnchor / P2 before-head joins
  if traversal == S45:
    admit epoch/challenge + acceptedAuthority-in-beforeImage + edge crypto
    # no AdmitFloor on old T; no AdmitFloor on context.time
  if traversal == Abort:
    215 D as above; no AdmitFloor
  if traversal == Diagnostic:
    report recorded fields; do not claim AdmitFloor
```

Charge 222 work profile on every load. Fail-stop latch. No prefix fallback. No current-core substitution when AdmitTEval/AdmitFloor run (215 D, 225, 312).

---

## Findings

1. **Consumption proof has encoded paths** from a capsule/PublicationRef through previous capsules to the unique establishing `clock-write`. No new field. Kept T is on the capsule because the event’s kept branch has no `proof`. Starting from T alone is forbidden by acyclicity.
2. **tEval vs floor are already two wires** (`OriginalContext.time` / `evaluation` vs `clock.timeEvidence`). Collapse is the defect to avoid. No `lastAcceptedWrite` requirement on every evaluation.
3. **S4.5/ABORT vs old T** is a traversal-mode owner rule already written. A generic walker that follows `context.time` into mode B is the conflict that would make the exception non-executable. Do not add a skip boolean; do not propagate the exception into ordinary/continuity/restore.
4. **312 V2** closes the P0/P1 CoreAnchor **locator** for new evaluations. It does not prove a floor was published. 313 assembly is not this admitter and not 222 durability.

**Actionable encoding gap:** none for these three questions. **Actionable owner gap:** implement the scoped admitter (PENDING-JOINS §1) instead of a generic TimeEvidence DFS. **Remaining unimplemented:** 222 unique/durable native publication, fences/custody, actual crypto/TCB, 310/312 historical V1 P0/P1 unavailability, M2–M6.

---

## Verdicts

- [x] **314 as scoped admission assistance:** locators traced from frozen 215/222/225/227/229/312; two modes over existing wire; S4.5/ABORT traversal table; no invented field or creator pin.
- [ ] **Not** complete proof admission, 313 native review, 222 durability, publication, or product installation.
