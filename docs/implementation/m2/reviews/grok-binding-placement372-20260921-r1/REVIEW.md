# Advisory — native binding codec/producer placement (372)

**Standing:** architecture placement only. **Not** S9.3 selection, **not** whole binding acceptance, **not** code approval of `/tmp/.../project_registry.rs`. 371r4 OWNER/REFERENCE and registry-selection-v1 formal REVIEW/review.json are **unchanged**. Registry-selection-v1 is ACCEPT-DESIGN-UNIT pending root lock compose; this report does not assume it is live.

---

## Constraint (inventory55 DAG)

`opensip-security` → contracts, evaluator, identity, platform. **Not** lifecycle, storage, or host. Storage → security. Lifecycle → security and storage. Host → all. A security constructor that `use`s `opensip_lifecycle::DecodedSelectionV1` / `inspect_supplied_lineage` or `opensip_storage::ProvisionalStoreMarker` is a **forbidden edge** (and a cycle with lifecycle→security). Host-supplied `bool` / trait-impl “I verified the marker” is fake authority.

Today: fence/capture in **security**; selection + lineage **decode/walk** in **lifecycle**; native S-marker **capture** in **storage**; composites in **host**. Those suffice for provisional 356–368 comparisons. They cannot be imported as-is into security’s authoritative binding producer.

---

## Recommendation (option 1, no new DAG edge)

| Kind | Owner | Notes |
|---|---|---|
| Inert codecs | **identity** (`no_std` canonical/schema already) | Closed decode + extra-rules + product-profile canonical bytes for: registry document, 92-byte marker, `selection.pair`, lineage node, **five-field binding view** (digest = `raw_sha256` of those five canonical fields). Values are **not** custody. |
| Native producers | **security** | Under `InstallationReadFence`, capture registry/root/marker/node/current; decode via identity; construct a **private** binding type (no public fields, no public constructor, no trait for host to implement). |
| Orchestration | lifecycle / storage | Re-export identity codecs if existing `DecodedSelectionV1` / `ProvisionalStoreMarker` APIs must keep names; keep publication/journal/SQLite mechanics. Byte-preserving physical move of current lifecycle modules is a **separate** 365-style review. |
| Composites | host | Consume security’s opaque session/binding; do not mint scalars. |

Identity already depends only on contracts (inventory). Adding codec files there adds **no** DAG edge. Lifecycle/storage/security already depend on identity.

**Reject option 3** unless the capability type is owned and constructed only in security (or identity+security) from fence captures. A host `impl BindingProof` is an escape.

**Prototype 373** (`project_registry.rs`, `f3bb0fb6…`, 10940 B) is shaped as an identity module (`crate::{canonical_bytes, parse_json}`, alloc-only, complete-document decode, “NOT custody”). Placement sketch only — **not** product, **not** authority, **not** this review’s source approval. A later codec review must match selected registry-selection-v1 schema/model (five-member rows, `allocationKind`, extra-rules), not a drift copy.

---

## Bootstrap (mandatory join)

`CreationStoreBindingV1` is closed **S / G=0 / K**, **no N** (127 schema). Installation C.store is store/install scoped. An **empty** registry (no project) **must not** invent N or a five-field view to create first current. Five-field `{1,N,S,G,K}` exists only after a **real** admitted namespace.

Do **not** take G/K for first current from C.store (self-cycle). Forward transition: G/K from admitted **intent target** + fresh S + that transition’s registry/lease scope. Lineage **roots** (install / authorized restore / adoption): G/K from that act’s typed declaration; **no invented intent**. Do not widen `CreationStoreBindingV1`’s G=0 const to smuggle restore G. Capsule rollback inside S ≠ new lineage root.

---

## Concrete gaps before a freeze of 372

1. **Codec move plan** (identity files + lifecycle/storage re-exports) as its own byte-preservation unit; do not sneak it into registry-selection lock compose.
2. **Security producer API**: private type; latch-on-failure; no public `from_parts(N,S,G,K)`; host cannot forge.
3. **Creation vs existing-store admission** as distinct typed contexts (372 draft already says this; still needs selected publication order: pair / current / root / lineage).
4. **Shared budget** on all native captures (not only caller `max_nodes`).
5. **Post-fence** retain store/node owners + lease; registry/pair FDs are provenance only (aligns with registry-selection overrides).
6. Registry-selection-v1 **lock successor** is a **prerequisite** for native registry capture; do not wire 373 into product first.

---

## requiredFindings

None against a frozen unit (this is advisory). Do not implement from this note without a later selected 372 owner.
