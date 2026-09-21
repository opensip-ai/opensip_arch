# Lineage retention vs marker requirement — 371

**Standing:** bounded read-only audit of current product `b3af5e85c` `installation_lineage.rs` against proposed S9.3 / companion `919d1717` and working physical 203. **Not** S9.3 acceptance, **not** a 368 defect verdict against unaccepted law, **not** implementation. 370 REVIEW/findings/ADDENDUM were **not** modified. Root’s concurrent registry/native-binding owner371 is separate. Recommendations are not acceptance. No native suites, no product edits.

---

## What 368/runtime25 actually does

`ProvisionalInstallationLineage::read_existing` walks from the **selection pair** start triple. For **every** hop it:

1. Captures `transitions/lineage/S/G/K.node` (cap 4096).
2. Decodes; rechecks the node capture even on decode failure.
3. Calls `ProvisionalStoreMarker::read_existing(fence, S)` — `stores/S/store-instance.v1`.
4. Rechecks the node after marker capture even on marker failure.
5. Pushes **both** the node capture and the marker into the retained set.

`ProvisionalStoreMarker::read_existing` treats missing/unreadable `stores/S` as **Capture/Decode error**, not a stated three-way **ABSENT**. The walk uses `?`, so any ancestor whose store root is gone **fails the entire lineage read**, even if that hop’s **node file** was captured.

That is **every-ancestor marker required**. Rechecks latch `Closed`. Conservative: no create/repair.

---

## Proposed owner rules (not accepted S9 law)

**S9.3** (`a319da39…`, heading still “proposed, not accepted”), marker paragraph: observation is **three-way** (readable / absent / unreadable). Unreadable ≠ absent. **The store a transition comes from** always exists → its marker is required. **Selected** marker is required only when the transition is **settled committed**; at LEASED/PREPARING a forward **target** may not exist; after abort GC may already have reclaimed an unpublished target — **absent target is expected**, not corruption.

**Companion** (`919d1717…`) phase table:

| Owner action | Marker requirement |
|---|---|
| REFUSE/BUSY/QUARANTINE | none |
| ABORT / ABORTED | **predecessor** marker required; **target** must be **stated**; **absent target expected** |
| RESUME-COMMIT / DONE | **both** predecessor and target **readable**; absent target at settled = corruption |

Reconstruction of a **forward** node uses **two** store-root markers of **that** transition (selected + predecessor), then `admit_node` (predecessor must exist as a **node**). Ancestor-reselect **re-opens the retained store** and reads identity from its **unchanged marker** — that store is still live as a rollback target. GC of an **aborted unpublished target** (no node) is A6. `admit_node` keys nodes by full triple; a missing **node** (not missing store) refuses.

**Working 203** (`292dbab3…`): nodes live at `transitions/lineage/S/G/K.node`, **outside every store root**, and **survive store reclamation**; lookup is never a directory census. Unobserved/unreadable node is unavailable, not absent. Physical choice; historical contracts unchanged. Not selected.

These are **not** the same requirement. Transition recovery is **phase-bound, two-store** (from/to of the **current** journal). Chain **admission** needs **nodes** for ancestry. Store **reclamation** may remove `stores/S` for a store that is no longer a live selected/rollback target while the **node** remains.

---

## Legitimate post-GC behavior

| Object | After lawful GC of an unselected/aborted store | After forward migrate, predecessor kept for possible rollback |
|---|---|---|
| Lineage **node** | aborted target: **no node** (never written). Historical chain hop: **node survives** (203). | node for predecessor **required** (`admit_node`) |
| Store **marker** | aborted unpublished target: **absent expected**. Reclaimed historical store **not** on a live reselect path: **absent allowed** as three-way ABSENT, not unreadable. | **readable required** if that store is the ancestor-reselect target |
| 368 reader today | missing `stores/S` → **walk fails** | succeeds only if every chain S still has a store root |

Post-GC **lineage evidence** is the node set plus the **currently selected** marker (pair). It is **not** “every historical `stores/S` still present.” Treating missing ancestor markers as **corruption of the node chain** over-refuses relative to 203 and relative to S9.3’s three-way/phase-bound marker law.

368 is **conservative refusal only**: it does not invent nodes, does not treat missing marker as permission to initialize, and does not scan directories. Against **proposed** S9.3/203 it is **stricter than required** for a **read-only chain walk**. It is **not** a proof that runtime25 violates accepted S9.2 (S9.2 has no instance lineage). Do not “fix” 368 in product until an accepted owner says so.

---

## Smallest correction (future owner + native reader)

Owner (with S9.3 review, still proposed):

1. Split **transition-recovery markers** (phase table: predecessor/target of **this** journal) from **chain-walk markers** (current selected S required readable; each **ancestor** hop is three-way).
2. State that a **node** at `transitions/lineage/S/G/K.node` may outlive `stores/S`; ABSENT ancestor marker after reclamation is not a missing node.
3. Ancestor-**reselect** still requires a **readable** marker on the **re-opened** retained store (companion physicalStore). GC policy must not reclaim stores that remain legal rollback targets.
4. Unreadable ≠ absent. Missing observation ≠ stated absence.

Native reader (after that owner):

- Keep capturing **every ancestor node**; fail closed on missing/unreadable/**misbound** node.
- Require **readable** marker for the **start/selected** S from the pair.
- For other hops: **state** marker observation; **ABSENT** (no `stores/S`) continues the walk; **UNREADABLE** refuses; **READABLE** must equal S and still recheck.
- Do **not** use `read_existing`’s Capture-error as the only ancestor outcome; that API is S-only “existing marker” and is the seam. A three-way observe, or a NotFound→ABSENT mapping **only** on ancestor hops, is the precise change. Do not weaken selected-S or in-flight predecessor/target recovery.

This is not a 368 patch, not S9.3 ACCEPT, and not a `stores/S` G/K header.

---

## requiredFindings

None against a frozen 370/368 unit. Gap for the **next** owner/reader only.
