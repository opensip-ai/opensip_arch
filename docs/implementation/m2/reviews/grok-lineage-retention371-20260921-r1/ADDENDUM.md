# ADDENDUM — ancestor-store lookup vs node predecessor links

**Standing:** retention follow-up only. REVIEW.md (`42e82ed9…499f`, 6416 B) is **unchanged**. Recommendation, not S9.3 acceptance, not a 368 patch.

---

## Is any intermediate ancestor **store** required for lineage-only traversal?

**Recommendation: no.** Full-triple **predecessor node** links suffice. Native markers are required only for **selected / opened rollback / transition-endpoint** stores.

S9.3 (still proposed) is **ambiguous**:

> “Every lookup uses the whole triple, whose instance component is read from the store-root **marker** of the store concerned: a numeric pair alone never identifies a node…”

**Reading A (over-broad):** forming any node key requires opening that store and reading its marker → every ancestor `stores/S` must exist.

**Reading B (endpoint-scoped):** when the **transition has a store in hand** (from/to/selected), S is taken from **that store’s marker**, never from a numeric (G,K) pair, because a retained branch may share the pair. When the **node already carries** `(S,G,K)` in `predecessor`, the walk follows **nodes**, not store roots.

Companion v3→v4 resolves the intended scope: “the instance component is read from the store-root MARKER of **the store the transition actually selects**.” Ancestor-reselect “uses the retained **selected** marker and the **verified chain from the current node**.” `admit_node` requires the predecessor **node**, not a live ancestor store. Working 203: nodes sit **outside** store roots and **survive reclamation**; lookup is never a directory census.

So: **lineage-only traversal** = decode current node, follow `predecessor` triples via `transitions/lineage/S/G/K.node`. Open `stores/S` only for (1) the **currently selected** store from the pair, (2) a store being **re-opened** as ancestor-reselect/rollback target, (3) the **from/to endpoints** of an in-flight transition per the phase table. Unrelated historical `stores/S` need not be observed.

368’s every-ancestor `ProvisionalStoreMarker::read_existing` remains **conservative refusal**, not required by this reading.

---

## NotFound is not store-root ABSENT

Three-way observation is of the **store root**, then the marker leaf:

| Positive observation | Kind |
|---|---|
| `stores/S` directory **missing** (parent `stores/` observed; name S absent) | store-root **ABSENT** |
| `stores/S` **present**, marker leaf missing/malformed | **UNREADABLE** (root observed, marker not admissible) |
| capture **NotFound on the marker leaf alone**, without a stated directory observation | **not** classified; must not be recorded as ABSENT |

`ProvisionalStoreMarker::read_existing` maps any capture failure to error. A future reader must **not** treat leaf-NotFound as “no store.” Unreadable ≠ absent. Missing observation ≠ stated absence.

This does not authorize GC of stores that remain legal rollback endpoints, and does not accept S9.3.
