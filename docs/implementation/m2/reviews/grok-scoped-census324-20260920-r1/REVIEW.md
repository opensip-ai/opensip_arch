# Independent source investigation — scoped census predicates 324

**Standing:** bounded **source investigation** of frozen `scoped-census-investigation-324`. It concretizes 321’s open current-vs-child split and corrects the blanket “never follow `operation.input.ref`” shorthand. Not a selected policy, native constructor, complete census, 323 authentication approval, or product installation. Installed product remains `fa72e50`. 323 is used **only** as unchanged 274/278/279 fixture bytes.

Python 3.12.13 `-I -B`. No product/frozen/history edits. No commit/push. Frozen probe reports were restored after independent replay.

Pins **before** extract: **2848616 B, 639 members, SHA256 `b7c3a83efb1f12bc1d408049312e65fcbf73905af0257a492373c569bc59270d`**. Extract rehashed **639/639**. Nested 321 `dd80c72a…cdb1` (620 / 2637220); nested 323 `5ba84833…421f` (2037 / 13517936 / 471 product). Packet `review321/REVIEW.md` byte-identical to live 321 (`537a71e7…54ea`). 323 REVIEW unchanged (`7b1385bc…1e26`). 227 local `shape_join_model_local.py` differs from original **only** in canonical.py path; canonical SHA `d47f25db…b442` asserted.

---

## What 324 is answering

321 left census “complete references” unsplit, nonempty current `bind_events` unresolved, and a shorthand that current standing must not walk `operation.input.ref`. ROOT-NOTES distinguishes:

- **Current C0 / D0:** predecessor **unknown**. Closed projection + typed operation/event **shells**. Not current roles as before. Not 279/306.
- **Child D1 in `by-predecessor/hash(C0)`:** logical before **is C0** (owned). Following D2 has before **C1**. 279/235 may use that actual base. They compare `timeEvidence` **locators**; they must not load T **targets**. Whole-bucket T-presence invariance applies to children too.
- Restore-child prover: original nested proof + **DIRECT** terminal (222). No self-support.
- `input.ref` is **action-dependent**, not a universal stop.

This packet does **not** implement native physical current/census. Ordinary/continuity/full restore consumers are **not** weakened.

---

## Independent probes (executed)

Scripts rerun from the extract; live reports SHA-equal frozen (`3383275e…45c6` read-scope; `db110c2b…2778` restore-scope). Frozen files restored.

| Probe | Result |
|---|---|
| Empty-event 279 with known before | **2** positives; omitting before refuses `empty-event publication needs exact before image` |
| 235 `bind_events` on those empty Ds | **0** store reads; standing `structural-bindings-only` |
| Clock-write event shell | **1** positive; evaluation target **absent ≡ malformed-present**; not in the read trace |
| Private-ceremony-termination missing `BeginBatch` | **2** refusals (`operation-capture-cap` on the required records load) — missing **non-time** bytes stay unavailable |
| Same-store `descriptor_operation` | **28** cases; reads **exactly** the OperationInput record; does **not** follow `input.ref` (actions seen: `creation`, `clock-recovery-challenge`) |
| 278 structural restore positives | **19**; result + read trace invariant if old T hashes are absent or stuffed with bogus bytes. Standing `structural-restore-and-event-bindings-only` |

**Corpus limit (labeled):** all 19 restore positives had **`timeTargets: []`** on stored capsules/clock-writes. The invariance still proves these helpers **do not follow** T locators and ignore extra unused hashes. It does **not** by itself prove a restore chain that **carries** T locators. No accidental T read appeared.

These are structural helper scopes. They do not grant current custody, clock admission, or full restore.

---

## Correction: `input.ref` is not a universal stop

`descriptor_operation` (265 `trust_input_reference.py`):

1. Always loads `OperationInputV1`.
2. If `o['store'] == d['store']`: **return** — no `input.ref` walk. Clock/S4/ordinary-import/refresh/challenge/creation shells stop here. Creation **marker** and S4 **evaluation** are **not** loaded by this helper (ROOT-NOTES still flags whether current **creation** standing needs `join_creation` separately).
3. Else require `action == continuity`, load the unique target continuity event, then:
   - **forward:** `TargetAbsenceInputV1` + `TransitionIntentInputV1` + `sourceBeforeImage` (non-time).
   - **ancestor:** `sourceBeforeImage` + `targetBefore.image` CapsuleImages + `TransitionIntentInputV1` via **`o['input']['ref']`** and E/D/S/G/K joins. Forward rev-1 **cannot** be an ordinary same-store child of C0; it may be **current** D0. Ancestor target **can** be a census child.
4. Restore-recovery: same-store path **does not** walk `RestoreProof`. `Operation.proof` / `admit_restore_proof` **does**: nested proofs, observed/proven **full** images, DIRECT terminal (`action != restore-recovery`). Calling only `descriptor_operation` on a restore child is **insufficient**. A new restore D must not self-prove N.

Clock/S4 `input.ref` (evaluation/epoch) remains **out of** this standing/census time-replay scope. Full ordinary/continuity/restore **consumers** still require their T and empty-effect befores. The child/current split must not be copied onto those consumers.

---

## Current vs child (does 279/235 suffice on a child?)

**Empty-event child of C0:** yes, **structurally**, with `before = C0`. 227/279 needs exact before image, store/revision+1/`previous==digest(C0)`, preserved eventHead/roles/staged/batch/sourceFence, retained phase, `timeEvidence` **locator** equality and F/L/anchor/serial/challenge equality. 235 empty list does no reads and still requires that owned before. Do not invent a before for **current** empty D0.

**Nonempty child of C0:** 279 empty-event guards **do not apply**. 235 `bind_events(D1, C0.roles, C0.eventHead)` is the structural event/role replay: NULL kinds (including `clock-write`) load the **event** not `evaluation`; `private-ceremony-termination` **must** load `BeginBatch`; abort-annotation must see the accepted abort in the **same** descriptor; `ordered-role-before` uses **C0**, not C1. That is enough for **structural** bindings + `pendingAuthenticatedRoleEffects`. It is not clock/crypto/authority. Missing BeginBatch ≠ missing T.

**Current D0 nonempty, unknown before:** do **not** call `bind_events` with C0 as its own before. Shell: EventRef locators, store/operation/sequence, no duplicate hashes, consecutive `previous` among listed events, first `previous` **shape** and local sequence equation, **not** compared to unknown D0-before `eventHead`; last listed == `C0.eventHead`. Empty list: `eventHead` may predate this revision. Role-effect replay stays out.

**Restore child:** 235 base is reconstructed `cur` along the proof (observed n → N), not “current roles.” Logical N vs native observed n stay distinct (222). Structural proof ≠ 222 complete closure of N including **original time proof**.

---

## Optional `commandOutcome` (242/243/265)

`PublicationDescriptorV1.commandOutcome` is **optional**. Absent: legal intermediate/historical D; cannot prove public-command completion. Present: `InputWork` / `Operation.events` / `Operation.proof` load `TrustCommandOutcomeV1` then its `OperationInputV1`. `bind_outcome` joins operation/scope/receipt only — **no** clock-evaluation edge. Using `Operation.walk` would still be full-graph DFS (wrong for S45). Optional outcome does **not** introduce a new required T target for this census.

---

## Finite field / predicate table

Machine table: `grok-out/predicate-table.json`. Summary:

| Scope | Before | 279 empty | 235 bind_events | Walk `input.ref`? |
|---|---|---|---|---|
| Current C0/D0 | unknown | **no** (would invent before) | **no** (would use current as before) | same-store: **no**; continuity current: typed intent/images/absence |
| Child D1 of C0 | C0 owned | **yes** if empty | **yes** with C0 roles/head | same-store: **no**; restore-recovery: **proof**, not this shell |
| D2 of C1 | C1 owned | same as D1 | same as D1 | same |
| Restore-recovery child | proof images | if empty, with reconstructed cur | with reconstructed cur | **RestoreProof** + nested + DIRECT terminal |
| Continuity ancestor child | target CapsuleImage | as applicable | with that image’s roles/head | **yes** TransitionIntent + both images |

Unavailable / unreadable canonical / cycle / budget / missing BeginBatch / missing required image/intent **never** become absence. Snapshot/census verdict must not change merely because a T **target** appears.

---

## Remaining owner decisions (not closed)

1. Current D0: check `roleChange` literals without `ordered-role-before`, or omit until a real before exists.
2. Current **creation** D0: whether marker/`join_creation` is in current standing (not in same-store `descriptor_operation`).
3. Exact 227 nonempty shape subset for children beyond 279-empty + 235.
4. Restore-reset 235 base: proven N vs observed n.
5. Owed adversarial tests still mostly **unrun** in this packet: orphan empty child with dangling T; nonempty child clock-write with evaluation missing; child before mismatch; cross-store intent mismatch; nested restore missing/direct-terminal cycle; complete bucket unreadable/foreign names/budget; T-presence invariance on a restore corpus that **has** T locators.
6. Physical fence/custody/complete-bucket enumeration (222). Full historical restore’s original time proof of N.

Do not select new wire. Do not treat 272 DFS or a records callback as CurrentRecoveryImage.

---

## Verdicts

- [x] **324 as investigation:** archive verified; probes independently reproduced; current vs child split holds; blanket never-follow-`input.ref` **corrected**; 279/235 suffice **structurally** for children with **known** before; current D0 still must not invent a before; `commandOutcome` adds no T target; 19 restore traces do not follow T (corpus had none).
- [ ] **Not** a complete constructor, native census, 323 auth approval, 222 restore weakening, or product installation. 321 physical qualification remains open.
