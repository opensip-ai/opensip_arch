# Advisory — independent full S/G/K evidence (not 357/358 approval)

**Standing:** source-and-ownership adjudication only. Not a review of unfrozen 357, not 358 product approval, not selected-I/current authority. Frozen 356 REVIEW `d620c9af…e74d` (6171 B) was read (no ADDENDUM) and is **unchanged**, as are 355 `84afca9a…286d` and the selection-boundary advisory `a5947b69…8ba3`. Unfrozen 357 product bytes were **not** inspected. No candidate/frozen/history edits. No store header or SQLite schema is invented here.

Pinned copies used: 203 `292dbab3…e5ac`; 127 `a0431300…7928`; inventory v32 `105a260d…b72e`; 201 PSL `physical-store-layout.v1.md` `bae44db6…a3ae` (13687 B); frozen-356 `storage/store_root.rs` `11f04d2c…36c3`; `commit-recovery-plan.v1.json` `cbaac9b1…cbb5` (schema standing: **author design only**). 203 and PSL remain **working/prospective** layout text; 127 is private schema.

---

## 1. What storage actually encodes at the store root

**Marker (storage, S only).** PSL §“Store marker bytes and publication”: `stores/S/store-instance.v1` is exact product-canonical JSON `{"schemaVersion":1,"storeInstanceId":"S"}`, read cap **128**, closed two members, raw==canonical, ~72 bytes when valid. Directory name is **not** identity; name/marker mismatch is unavailable. Frozen 356 `store_root.rs` implements that codec (`MARKER_NAME`, `MARKER_LIMIT=128`, two-field decode, compare to **expected** S). 127 `StoreMarkerV1` is the same two-member shape; its root230 note places that type as an unsigned marker in **trust `records/H`**, a **different path/owner** from `stores/S/store-instance.v1`.

**That file has no `storeGeneration` and no `stateSchema`.** PSL says this encoding is **not** a change to `StoreGenerationBindingV1`. 356 `store_root.rs` comment: expected S must come from an admitted binding in a **future host facade**; the private syntax type is not that binding.

**358 proposal is therefore the right storage next step, and it does not close G/K:** storage-owned marker observation under the same native fence (357 is only the planned prefix-capture mechanism), fixed leaf `store-instance.v1`, cap 128, compare **S** to the already-claimed instance, retain the original capture and ancestor edges. No security→storage; no storage→lifecycle. Storage already depends on security; host may also capture-then-decode as in 356. Do **not** use public `observe_bound_operational_file` (355/354: supplied root, `into_parts`). 356 tests still call that API; that is **not** the native join.

---

## 2. Where G and K actually live (not in the marker)

| Source | Standing | What it is | Independent of `selection.pair`? | Supplies G/K? |
|---|---|---|---|---|
| `stores/S/store-instance.v1` | PSL + frozen 356 storage | Two-member marker | Yes (storage path) | **S only** |
| `selection.pair` | 203 working; 354/356 codec | Five-member claim C+S+G+K | No — this **is** the claim | Not independent |
| 127 `StoreBinding` on capsule/current | private 127; 344 `native_current` admits 3-member `{storeInstanceId,storeGeneration,stateSchema}` at `trust/stores/S/state.v1` | Security/trust owner | Yes — different file/owner than the pair | **S+G+K**, security not storage |
| `StoreGenerationBindingV1` | PSL + commit-recovery-plan **author design**: `{schemaVersion, namespaceId, storeInstanceId, storeGeneration, stateSchema}` | Logical five-member object; `storeGenerationDigest` = SHA-256(canonical bytes) | Digest appears on ledger **association** rows, not as plaintext G/K | Digest check **if** N+S+G+K are already in hand; **not** a store-root file |
| Ledger `storeGenerationDigest` | frozen 356 `ledger_store.rs` / `recovery.rs` | hex64 field | Yes as a digest | **Not** G or K integers |
| `transitions/lineage/S/G/K.node` | 203 working | Lifecycle node **keyed by** the triple | Path already assumes G/K | Not an independent read of live G/K |
| `trust/journal-floors/N/G.floor` | PSL/203 | Grant-generation floor | Yes | **Grant** G, explicitly **not** store generation |
| SQLite store header with G/K | — | **Not found** in these sources | — | **Do not invent** |

203 §Selection pair: “Admit **marker/full store binding** and closure before use; **the record alone proves neither**.” STP (via 203-proposal assistance) glosses the pair as core closure **plus** full store binding `(S,G,K)`. That is the **claim shape**, not a second storage file that repeats G/K.

PSL §Identity: require marker = S **and** `StoreGenerationBindingV1` to match admitted namespace/instance/generation/schema. Numeric G can **repeat across instances**; marker + full binding stay mandatory. The five-member binding is **custody-protected store metadata** obtained through an **admitted handle and registry**, not request fields (implementation-boundaries §StoreGenerationBindingV1). It is **not** specified as a leaf under `stores/S/`.

---

## 3. Hole (state it; do not fill it with a header)

**There is no independently acquired storage-owned native record that carries G and K.** Marker is S-only by PSL/127/356 `store_root.rs`. Inferring G/K from `selection.pair` would make the claim its own proof (forbidden). Ledger `storeGenerationDigest` is a digest of a **five-member** object including `namespaceId`, which the marker also lacks. Trust `StoreBinding` (three members, no namespaceId) is a **security** capsule field, not storage floor/header.

So: **marker + pair is not sufficient for full S/G/K.** Marker + **security current** StoreBinding can **compare** S/G/K without treating the pair as storage evidence. Marker + **recomputed** `StoreGenerationBindingV1` digest vs ledger can **check** a claimed N+S+G+K; it still does not **read** G/K out of storage. Neither is a new `stores/S/*.v1` header.

---

## 4. Bootstrap without circular authority

1. 351/352 fence (groups still SUPPLIED) — independent of S.
2. 356 provisional pair — **claim** C,S,G,K; not use.
3. **358** marker at `stores/<marker-S>/store-instance.v1` via 357 prefix capture under the **same** fence — independent **S**; require pair.S == marker.S. Missing marker is unavailable, not create.
4. **Security** `trust/stores/<S>/state.v1` (344) — independent **StoreBinding** S+G+K on the current capsule; require equality with pair G/K. Do not pass pair as the only `expected_store` without this comparison. If current is absent/unreadable: unavailable, not “use pair G/K”.
5. Optional later: recompute `StoreGenerationBindingV1` digest from admitted **registry N** + (S,G,K) and compare ledger `storeGenerationDigest` (storage correlation, still not a header).
6. C via 323/229; verified profile; 350 FS-name law on the **same held Files**; then **use**.

355 still does not expose `File`; storage must not bypass that with a caller path. 357 (unreviewed here) is only the descendant-prefix mechanism so `stores/S/store-instance.v1` can be captured under the native fence.

---

## 5. What follows 358

Confirm 358: **storage-owned S-only marker**, same fence, original capture retained, **not** full G/K.

After that, host join of **security current StoreBinding** (and only then core/profile/active-slot). Do not add a storage G/K file to close 203’s “full store binding” unless a later selected layout **explicitly** creates one. Inventory: host→storage allowed; security↛storage; storage↛lifecycle.

**Must not be claimed:** marker = selected store; pair G/K = storage evidence; `storeGenerationDigest` = G; journal-floor G = store G; capsule StoreBinding = storage-owned; 358 = full (S,G,K); 357/358 code approved.

---

## Verdicts

- [x] **Independent storage evidence today is S-only** (`stores/S/store-instance.v1`, cap 128, two members).
- [x] **Full G/K is not in that marker.** Independent G/K, if any, is **security** current `StoreBinding` and/or a **digest check** of design-only `StoreGenerationBindingV1` against the ledger — not a store-root header (none found).
- [x] **358 S-only marker under the 357 fence is the correct next storage step** and must not be described as closing G/K.
- [x] **Hole stated:** no storage-owned native G/K record in these sources; do not invent one.
- [ ] **Not** 357 review, 358 implementation approval, selected-I, or product installation.
