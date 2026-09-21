# Independent source investigation — empty-event predecessor and scoped standing 320

**Standing:** bounded **source investigation**, not a selected policy, wire correction, native constructor, 318 freeze, or 319 re-approval. Packet `ROOT-NOTES.md` is working questions. 317 remains reviewed **policy**, not a complete field/predicate plan or native approval. Installed product remains `fa72e50`. Prior reviews were not edited.

Python 3.12.13 `-I -B`. No product/frozen/history edits. No commit/push.

Pins **before** extract: **2625124 B, 612 members, SHA256 `44cf85926ee98fff8ca7c9e2236ed9b9713ac570d21f12db27cb68bb3af1b8f2`**, `allMembersRehashed: true`. Live tar matches. Extract rehashed **612/612**. Packet includes verified 317 source (`8ccd47a0…7292` / 210 / 433096) and 319 reference (`96222a19…32b4` / 513 / 2322720) with 265 proof/input/event/operation modules. Nested 222 r6 `5b6df2a5…1d5c`, 227 r9 `818604dd…6e44`, 229 r3 `edde8b4f…6b4e`, 265 `73c3b3f5…86df`, 279 `8b081b4f…4e9d` match prior frozen hashes. Evidence: `grok-out/field-predicate-table.json`, `grok-out/locator-citations.json`.

Preserved unchanged: 319 `19a4901d…bf5d` (5749 B); 317 `0740164f…2943` (9806 B); 316 `1ef324da…d059` (7497 B); 315 `87e3cd2d…e0e8`; 314 REVIEW `d54342fd…daca` / ADDENDUM `02a3a0bc…c8ee`. Native 318 is applying 319 SEM on new bytes; **not** approved here.

---

## Empty-event predecessor locator (read first)

**Lawful example (ROOT-NOTES):** first L-writing S4 (new T) → P2 genesis (role events) → later **equal-L empty shared-head** publication. Then old-T **target** missing. No future evaluation as a reverse index.

Call the three capsules C1 (clock-write AFTER), C2 (P2 genesis), C3 (empty-event current). D1/D2/D3 are their descriptors.

### What effect proof actually requires

227 `shape_join_model.py` `admit_shapes_and_joins` (and native 279, same diagnostics): empty `D.events` is lawful **only** with an exact **BEFORE capsule object**. Guards: `empty-event publication needs exact before image`; same store / revision+1 / `previous == digest(before)`; unchanged `eventHead`, `roles`/`staged`/`batch`/`sourceFence`; both clocks `retained`; `timeEvidence` and F/L/anchor/serial/challenge equal (`empty-event publication cannot hide a clock write`). 227 `PROOF-NODE-JOINS.md`: this is a **structural** shared-head outcome; head/time/counter/history admission remains a full shared-guard owner; shape is not head-update authority.

Native 306 `capture(budget, reference, before_ref, store)`: `before_ref` is an optional **full NodeRef**, admitted **before I/O**; SHA must equal `capsule.previous`; load is `Records` with declared `bytes`. Omitting it on an empty-event row is 279 `empty-event publication needs exact before image`. `before_ref = None` is **not** proven absence of a prior state. Store callback is `(Collection, digest, cap)`, **not** 222 `by-predecessor/H/D`.

So 279/306 **need caller-owned predecessor bytes**. They do not discover them.

### Owned locators on C3 / D3

Sources: 222 r6 `PERSISTENCE.md`; 227 `build_trust227_shapes.py` (`NativeBefore = {revision, sha256}`; `PublicationRef = {previousCapsule, sha256, bytes}`; capsule `previous` is nullable Hex64); successor schema `NativeBefore` required `{revision, sha256}` only — **no `bytes`**.

| Locator on current empty-event | What it actually names | Full predecessor NodeRef? |
|---|---|---|
| `C3.publication` | `PublicationRef` of **D3** (`previousCapsule` = hash(C2), descriptor sha256 **and** bytes). 222: descriptor lives at `I/trust/publications/by-predecessor/H/D` with H = `previousCapsule` = hash(C2). | No — locates D3, not C2 |
| `C3.previous` | bare SHA-256 of C2. 222: “predecessor consistency pin, **not** permission to search for or reinstall an older state.” 317: `load(records, capsule.previous)` is **invalid**; previous is not a records NodeRef. | No — hash only, no length |
| `D3.nativeBefore` | `{revision, sha256}` of the admitted **file being replaced**. Ordinary: revision−1 and `previousCapsule` (= hash(C2)). Restore-recovery may pin observed n instead. **No `bytes`.** | No |
| `D3.events` | **empty** | No event in this descriptor |
| `D3.operation` | `NodeRef` to `OperationInputV1`. Ordinary import is payload-metadata-**closure**, not a before capsule. Clock-write operations live on **D1**, not D3. | No |
| `D3.afterProjection` | C3 without `publication`. 265 `reconstruct(desc, pubref) = {**afterProjection, publication: pubref}` reconstructs **this** AFTER, not C2. | No |
| `by-predecessor/H/` with H = hash(C2) | 222: this directory holds **successors of C2**, i.e. **D3**, not D2. Successor census of **current** C3 uses H = hash(C3) and looks for **children**. | No |
| `by-predecessor/hash(C1)/` | Would hold D2. C3 does **not** encode hash(C1) or `D2.sha256`. | Not owned on C3 |
| Carried `eventHead` | Last event of C2 (role event). `EventRef` is a full locator; the **event chain** can be loaded. Clock-write is on C1, not C3. | Event shells, not C2 bytes |

222 reconstruction of capsule *n*: add **D(n)**’s full PublicationRef onto D(n).`afterProjection` and verify joins. D(n) lives at `by-predecessor/{hash(capsule n−1)}/{D(n).sha256}`. C3 does not encode `D2.sha256` or `{hash(C1), bytes}`. A lone D(n) does **not** prove n. Directory listing / prefix / greatest-number search is forbidden.

### Examined reverse paths that are not independent locators

**1. 317 floor discovery (OWNER “Locating consumption”).** Start at `eventHead`, follow `previous` EventRefs, find clock-write with `kind:new` and `proof == T`, load `evaluation`, take `evaluation.beforeImage` digest as H, look in `by-predecessor/H/` for the consuming descriptor, reconstruct AFTER.

On the example: that yields **C1** (first S4 AFTER), whose `beforeImage` is the **P0/P1** capsule, **not C2**. Loading `evaluation` **is** the missing old T. Even chaining a successor census of C1 to find D2 still **requires T first**. 317 already forbids standing constructors from following `descriptor → role.clock.by → clock-write.evaluation`. Out of S45 standing.

**2. Event-shell walk without loading evaluation.** `ClockWriteEventV1` always has `evaluation: NodeRef` (shape-present) and `timeEvidence` `{kind:new, proof}` or `{kind:kept}`. Capsule `beforeImage` lives **inside the evaluation record**, not on the event. 265 `bind_events` classifies `clock-write` as `NULL_KINDS` and does **not** decode evaluation. Walking events yields EventRefs + shells, not C2 bytes.

**3. Restore / continuity images.** Restore `RestoreProofV1` carries `observed.image` / `proven.image` **full NodeRefs** and ordered `PublicationRef`s; `admit_restore_proof_with_event_bindings` reconstructs forward and calls `bind_events(d, cur['roles'], cur['eventHead'], …)` with **already-owned** `cur`. Continuity carries `sourceBeforeImage` / `targetBefore.image` CapsuleImage NodeRefs. Those are **IndependentHistoricalImage** locators. They are **not** encoded on a same-store ordinary empty-event current capsule.

**Inference labeled:** after exhausting these owned edges, there is **no** independent **full** predecessor locator (NodeRef with `bytes`) for every lawful empty-event **current** capsule under S45 missing-old-T. Do not invent `records/<bare previous SHA>`. Do not use old-T `beforeImage` as a reverse index.

Empty-event **effect proof remains possible** when a caller **already has** predecessor bytes (restore chain, continuity CapsuleImage, or 306 `before_ref`). That is a different constructor. It is not discovery from C3.

### Disposition required (not chosen here)

**A — Narrow current S45 standing.** `CurrentRecoveryImage` = qualified native current `state.v1` + fence/custody + complete successor census of **hash(C3)** + D3/projection join + closed P2 shape including `timeEvidence` **locator**. It does **not** retrospectively prove this empty publication’s original unchanged-clock effect. Exact grant: “this file is the selected current capsule, D matches C, census is none/one as required, heads locators closed.” It **must not** grant 279/306 effect proof, predecessor clock equality, T admission, or generic publication authority. 306 cannot be called with a fabricated before ref.

**B — Effect proof remains mandatory even in S45.** Then an **explicit durable original-before-image locator/retention** is missing (versioned wire if a new NodeRef is added on empty-event D or C, or retained CapsuleImage of the replaced file at publish time). Until that exists, empty-event unchanged-clock **cannot** be re-proven from a lone current capsule in this scope.

Choosing A only to avoid a missing field, or B before exhausting locators, is forbidden. Locators are exhausted; **owner must pick**. This investigation does **not** pick. Neither choice is a waiver of remaining 222/215/227 guards.

---

## 265 `proof` / `bind_events` / `walk` (not standing)

`trust_event_reference.py` `bind_events`: `before_roles` / `before_head` **must** come from the owned logical base (actual before capsule, continuity source image + new local head, or proven N). The function **cannot choose** that base, establish durability, or bless role guards. Empty `events` still requires that supplied before; it then checks `afterProjection.roles/eventHead` against replay (identity). `clock-write` is `NULL_KINDS` — no evaluation load. Return standing is **`structural-bindings-only`** with `pendingAuthenticatedRoleEffects`.

`Operation.proof` → `admit_restore_proof_with_event_bindings` (restore-chain + `bind_events` per link/terminal). Return standing **`structural-restore-and-event-bindings-only`**. Predecessor images are **inputs of the proof object**, not discovered from an empty-event current file.

`Operation.walk` is the **other** helper: full graph `G.walk` plus optional prepared-outcome bindings. Standing **`structural-dependencies-and-prepared-outcome-bindings-only`**. 272-style full DFS follows every typed edge, including `role.clock.by` → evaluation. **Unsuitable for S45** (ROOT-NOTES item 2; 317 whole-path scoping). `proof` is **not** `walk`.

Physical/independent durability that can supplement `bind_events` without loading T: host current file + 222 successor census of **current** H + parent/file barrier + (for historical standing) original **direct** terminal witness on a restore chain. That is census/custody, not 279 equality. If a standing constructor **in fact** requires evaluation bytes, that is a **circular unresolved dependency**, not success. Unavailable / cycle / budget / required-missing **never** become absence.

---

## Field / predicate table (summary)

Full machine table: `grok-out/field-predicate-table.json`. **Record shape always.**

### CurrentRecoveryImage

Native `I/trust/stores/S/state.v1` under installation fence/custody (ROOT-NOTES §1). **Not** 316 `CapturedContext` (312 `bind_context` over a records callback). **Not** a caller graph.

| Field | Shape | Load target bytes? | Notes |
|---|---|---|---|
| Capsule `TrustCapsuleV1` | required | **load** current file | Physical current premise |
| `capsule.publication` | `PublicationRef` | **load D(current)** | H = previousCapsule; D(current) not D(previous) |
| `capsule.previous` | Hex64 or null | locator-only | Consistency pin; no records lookup |
| `D.nativeBefore` | `{revision,sha256}` or null | locator-only | File being replaced; no bytes |
| `D.events` | array, may be empty | load listed EventRefs **only** | Empty: zero loads; `bind_events` still needs caller before |
| `D.operation` | NodeRef | load if **this** constructor requests it | Ordinary import ≠ before capsule |
| `D.afterProjection` | required | in D bytes | Reconstruct AFTER = projection + PublicationRef; join to C |
| Successor census `by-predecessor/hash(C)/` | complete bucket | child descriptors | 0/1/fork of **current**; does not reconstruct predecessor |
| `clock.timeEvidence` | required NodeRef on P2 | **locator-only** | Target old T out of S45 scope |
| `eventHead` | EventRef or null | optional for 317 **floor discovery**, not S45 standing | Empty-event may carry prior revision head |
| `role.clock.by` → `ClockWrite.evaluation` | on role events if present | **locator-only / out of S45** | Loading evaluation is missing old T |
| 306 `before_ref` | caller NodeRef | only if caller **has** full locator | Cannot fabricate from previous SHA |

### IndependentHistoricalImage

Continuity `sourceBeforeImage` / `targetBefore.image` CapsuleImage **NodeRefs**, or restore proven-N reconstruction via ordered **PublicationRefs** plus `observed.image`/`proven.image` NodeRefs. Full locators. Separate from empty-event same-store previous SHA. Census is of **that** image digest.

### AcceptedRecoveryAuthorityForImage (S45 only)

Borrows stage-1 current or independent historical image. 317 OWNER steps 2–4.

| Field | Shape | Load target bytes? | Notes |
|---|---|---|---|
| `heads.root.admission` | NodeRef | **load** `RootAdmissionNodeV1` | Must equal epoch `acceptedAuthority` |
| `heads.root.document` + binding + `rootVersion` | required | compare to admission; load ancestry bodies/envelopes | Time-free; 229/312 |
| `RootAdmission.context.time` | required NodeRef | **locator-only** | Do not load; do not opportunistic-if-present |
| `RootAdmission.context.priorRevocationHistory` | NodeRef or null, required field | **LOAD** history node if non-null (step-4 list bytes) | Locator comes from the **admission record**. **Do not** claim equality to omitted `context.time.beforeImage.history`. **Unresolved fact:** recorded locator vs replayed before-image equality (ROOT-NOTES §3) |
| `context.incomingRevocation` | DocRef or null | load if non-null when original-edge quorum requires it | Missing is unavailable, not empty |
| parent / CoreAnchor / embedded chain | typed | **load** ancestry + inventory/manifest/root pairs | Missing parent/authorization/envelope unavailable |
| `history.admittingRoot` | required on list nodes | load RootAdmission record; `context.time` **target** not loaded | No successor-list pointer |
| image `clock.timeEvidence` target | locator on image | **locator-only** | Old T never required through this or downstream constructors |

---

## Findings

| Item | Result |
|---|---|
| Full empty-event predecessor NodeRef under S45 on a lone current capsule | **Not found** on owned edges |
| 317 evaluation.beforeImage discovery | Finds **first-S4** BEFORE/AFTER, requires missing old T, **wrong generation** for C2 |
| 306/279 empty-event | Need **caller** full before; cannot discover from D3 |
| Restore/continuity | **Have** CapsuleImage NodeRefs; different constructor |
| 265 `proof` / `bind_events` | Structural-only; no evaluation load; no standing grant; `proof` ≠ `walk` |
| `priorRevHistory` without `context.time.beforeImage` | Load recorded history locator; **do not** claim before-image equality |
| A vs B | **Owner disposition owed**; not chosen |
| 317 | Policy holds; constructor table **not** settled |
| 318 / 319 | Untouched; 318 **not** approved |

**Actionable encoding gap if B:** durable before-image NodeRef/retention for empty-event. **If A:** write the exact non-effect capability so it cannot be used as full clock/publication proof. Neither is a waiver.

---

## Remaining

Native scoped constructors, 222 unique/durable product, 317 per-constructor field lists and owed adversarial tests, 318 freeze (root applies 319 SEM), M2–M6. No migration from uninstalled format. No new field invented here.

---

## Verdicts

- [x] **320 as investigation:** archive verified; empty-event predecessor locator **absent** as a full independent NodeRef on owned current-capsule edges; 317 T-through discovery examined and rejected for S45 standing; 265 structural proof distinguished from `walk` and from standing; field table load-vs-locator; A/B disposition named without silent choice.
- [ ] **Not** policy selection, wire change, guard weakening, 318 approval, or product installation.
