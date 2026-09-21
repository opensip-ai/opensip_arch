# Native store-binding 387 — owner-design investigation

**Standing:** investigation only. Not a formal unit, not source acceptance, not S9.3 selection, not writers. The 372 drafts under `native-store-binding387-planning/` are **preserved unchanged**. No root assent is manufactured.

Live context (observed, not modified): product `526a186`, lock 34 inventory / 51 contract; registry-v2 and inventory58 selected; runtime29/source386 installing. Draft mentions of unreviewed 371, inventory55, and “no code move” are **historical**.

S9.3 (`security-and-lifecycle.md` line 953, “proposed, not accepted”) and `store-instance-lineage.v1.json` remain **unselected**. Codecs exist; a binding owner does not.

---

## 1. Circular dependency, and the minimum break

**Wrong join:** treat `CreationStoreBindingV1` / `C.store` as the source of G/K for first current, *or* demand a five-field `StoreGenerationBindingV1` (which contains N) in order to publish installation current.

**Counterexample A.** Empty installation, empty registry. `CreationStoreBindingV1` is closed `{storeInstanceId, storeGeneration:0, stateSchema}` (product `trust_record_shape_nodes.rs` `node_163`/`node_165`; no N). If first current required N or a five-field view, installation could never publish C, so no selected store would ever exist for later projects.

**Counterexample B.** Invent a namespace at install to fill the five-field record. That contradicts selected registry-v2: only the pristine-installation creator publishes an empty registry; emptiness is not a namespace (`owner.md` lines 32–33). Registry first-use allocates N only at an admitted **project root** (lines 35–60), not at I.

**Accepted break (already law, not a new schema):**

| Value | Source | When it exists |
| --- | --- | --- |
| Install C.store | typed **creation** declaration: fresh S, **G=0**, K∈{1,2} | empty install; **no N** |
| N | registry ACTIVE row after real first-use/adoption | later, at a project |
| Selected S | opened endpoint `stores/S/store-instance.v1` vs `selection.pair` | after install publication |
| G/K | lineage node at the **full triple**, located by the pair, independently joined | after the root node exists |
| Five-field `{schemaVersion:1,N,S,G,K}` | derived view under admitted handle | **only** after N is admitted |

`capture_head` (`native_current.rs` 129–186) already **reads** current and compares `store` to caller-supplied expected three-field binding; missing current is capture error, **not** initialize. Failed ordinary reads must not enter creation (`owner-draft` §Creation). That is existing product + draft agreement.

Implementation-boundaries 240–269 already freeze the five-field shape and say S9.2 closed records carry **no** store instance; S9.3 is the proposed successor for instance identity. Do not add N to C.store or S to the journal.

---

## 2. Proposed install-root publication order (minimum new law)

Four **separate** durable writes. Creation supplies `(S, G=0, K)` as a typed act; none of pair, node, or C may mint those values by reading another of the four.

1. **Allocate S** (32 lowercase hex, 128-bit OS CSPRNG). No pair/C/node yet.
2. **Store-root marker** `stores/S/store-instance.v1` closed `{schemaVersion:1, storeInstanceId:S}` (128-byte canonical). S9.3 prose (lines 966–969): identity persisted in the store root **before first publication**. Marker-leaf NotFound ≠ store-root ABSENT (existing storage observation).
3. **Lineage root node** `transitions/lineage/S/0/{K}.node`: predecessor and `selectedByIntentDigest` **both null**. Join node S to the **already durable** marker. Do not invent an intent.
4. **`selection.pair`** closed five-member InstallationSelectionV1 locating `(S,0,K)`. Codec already admits G≥0 (`store_selection.rs` 67–69). Pair is the publication of **selection**, not of G/K.
5. **Trust current** `trust/stores/S/state.v1` with `store` = `CreationStoreBindingV1` equal to `(S,0,K)`. C is comparison evidence after selection exists; it is never the G/K constructor.

**Lawful crash prefixes (ordinary read = unavailable, never initialize):**

| Durable set | Ordinary admission | Creation recovery |
| --- | --- | --- |
| nothing / S allocated only | pair missing → unavailable | not a store |
| marker only | unpublished; pair missing | unpublished materialization; GC-class orphan if the enclosing act aborted |
| marker+root-node, no pair | not selected | lineage exists off selection; do not write pair from the node |
| marker+node+pair, no C | `capture_head` fails | current missing ≠ mint C from pair |
| pair without matching marker | S mismatch / unavailable | contradiction; no repair from pair fields |
| C without matching pair | Store compare fails (`native_current.rs` 184–186) | not initialize |
| node G≠0 or non-null origin at install | not a creation root | refuse; do not widen G=0 |

Uncertain durability of any one write stops the act; next fence **re-observes**. Do not invent a fifth journal member or CLI.

**Ordinary five-field admission** (after a project exists): RegistryStartGate + ACTIVE N (selected overrides identity 619 / S9 917) **then** pair locate **then** endpoint marker S **then** node G/K **then** C.store compare. N never comes from pair or C.

---

## 3. Forward / same / ancestor — do **not** pretend this is selected

If and only if S9.3 + companion are later selected:

- Selection case from **admitted intent alone** (S9.2 pair law lines 906–915; companion `nodeWritingRule`).
- **Forward** node **only after durable journal COMMITTED** (`writeOrder` line 351). Reconstructible from intent + two **endpoint** markers.
- **Same-store / ancestor:** write **no** node; validate retained node; **never rewrite** predecessor/origin (S9.3 lines 1024–1028). Missing node there is QUARANTINE, not fabricate-from-this-intent (v2 defect).
- S9.2 `recover_transition_journal` **decides first** (lines 939–951). REFUSE/BUSY/QUARANTINE → companion inspects nothing.

That matrix is **proposed**. The next bounded owner can specify **install-root + ordinary admission** without selecting S9.3. It must **not** implement transition node writes from filenames.

---

## 4. Endpoint marker vs intermediate node (GC)

Proposed S9.3 (lines 982–992) plus draft §Intermediate: require a store-root marker only for a **physically selected/opened endpoint**. Ancestry follows **node full triples**. Nodes outlive store GC. Missing **node** ⇒ chain unavailable. Missing **intermediate store** after lawful reclaim ⇒ still readable ancestry, not a rollback handle.

**Product mismatch:** `installation_lineage.rs` 81–85 calls `ProvisionalStoreMarker::read_existing` on **every** hop. After GC of ancestor X, a Y→X chain that still has X’s node would fail. That walk is provisional read-only (`installation_lineage.rs` 1–3, 33–35) and must not be promoted. Selecting the endpoint rule is new owner law; 386 codecs do not change this walk.

---

## 5. Adoption / restore: no implementable owner yet

Companion `lineageRoot.creatingActs` names:

- `crates/lifecycle/src/installation.rs` — inventory58 row, **standing proposed**, **file absent** on disk.
- `crates/storage/src/backup.rs` — inventory58 row “Export and restore bounded evidence bundles without restoring trust floors…”, **standing proposed**, **file absent**.

Those are **planned names**, not selected owners. They do not specify: authorization to mint a **new** S; G/K declaration when restored evidence is **not** G=0; marker **replace-before-publish**; refusal to import nodes/floors/grants; durable prefixes.

**Do not** stretch `CreationStoreBindingV1` G=0 to a restored nonzero generation.

**Do not** conflate:

| Act | S | Lineage | Current |
| --- | --- | --- | --- |
| Install first store | fresh | new root, G=0 | CreationStoreBindingV1 |
| Same-S trust-capsule restore | **same** S | **no** new root | recover/replace C under existing selected triple |
| Evidence restore / portable adoption **new root** | **fresh** S, replace copied marker | **new** root, G/K from **that act’s** typed declaration | not CreationStoreBindingV1 unless that act independently declares G=0 |

Same-S capsule restore is a **trust-current** problem (existing read path + a publication owner still unspecified). New-root restore/adoption is a **separate** owner that does not exist. Next candidate should **exclude** it rather than stub `backup.rs`.

Registry adoption (`owner.md` 90–96) is ProjectId/N only. It does not create stores or C.

---

## 6. What the 372 drafts got right vs stale

Keep: five-field is derived not a sixth file; C.store is 3-field compare; G=0 creation must not invent N; endpoint vs intermediate; node after COMMITTED; same/ancestor preserve origin; no new H-domain/journal member/CLI; failed ordinary read ≠ create.

Stale: 371 unreviewed; inventory55 DAG; “no decoder relocation.” **Now:** identity owns pair/marker/lineage/registry codecs (386); inventory58; security still must not import lifecycle/storage; host must not mint five scalars. Option 1 from `ownership-questions.md` is the codec layout, **not** the binding constructor.

---

## 7. Bounded next owner candidate (recommended)

**In scope:** install-root publication order (§2), ordinary five-field admission without circularity, three-way marker vs missing-leaf, explicit “ordinary miss ≠ initialize,” and the product walk’s endpoint-marker defect as a **non-promotion** constraint.

**Out of scope until their own units:** S9.3/companion selection; forward/same/ancestor node matrix; adoption/new-root restore; writers; current-authority facade; native UUID qualification.

No unit verdict.
