# ADDENDUM — 370 acceptedLaws vs physical profile; registry prerequisite; bootstrap G/K

**Standing:** scope clarification only. REVIEW.md (`304f4430…6b9a`, 11002 B) and findings.json (`b2a3d1e2…49cd`, 3495 B) are **unchanged**. Recommendation, not owner acceptance, not a header, not source edits. Runtime25 code acceptance is **not** owner-law acceptance.

---

## 1. What `acceptedLaws` did and did not accept

The REVIEW `acceptedLaws` bullet that names an S-only two-member product-canonical JSON marker and three-way readable/absent/unreadable observations **cited** proposed S9.3 prose, private 358, and (elsewhere) unselected physical201. That citation must not be read as selected **physical encoding/profile**.

**Selected logical instance/binding laws** (lock / S9.2 / recovery-plan schema / identity §2): closed 11/20 transition records; `NamespaceList` of strings; pair law; five-member `StoreGenerationBindingV1` shape and digest; obtain-through-handle-and-registry obligation; ProjectId **name** PROJECT-ID-V1 and marker/registry **agreement** law; independent `C.store` as a three-member **comparison**, not the five-field binding.

**Still unselected physical encoding/profile:** `stores/S/store-instance.v1` two-member JSON codec and path grammar; three-way marker observation as **native** profile; `transitions/lineage/S/G/K.node`; PSL 201 locators; working 203. Those are 358/367/368 **code** and unselected layout text. S9.3 remains proposed. Runtime25 integrating that code does **not** make those encodings S9 owner law.

findings.json `acceptedLaws[2]` has the same citation mix; this addendum qualifies it. The JSON file is not rewritten.

---

## 2. Registry carrier: optional vs prerequisite

A **logical** five-field **view** (compose `{1,N,S,G,K}` in memory under an already-admitted handle) does **not** require a new native registry table. N can be the admitted namespace string already in hand.

**Actual native registry/root admission** has **no selected physical bridge**: S9.2 registry is strings only; historical nine-field `project_registry` (opaque `projectKey`) is not a lock input and must not be revived; physical201 adopted **locator only**. Therefore a revised native registry carrier (PROJECT-ID-V1 marker bytes + one-to-one namespace/root, without opaque-key/`newRoot` rules) is a **prerequisite** for native registry/root admission, not an optional extra on that path.

---

## 3. Bootstrap counterexample (root `cases-to-resolve.md`)

Deriving G/K **solely** from independently decoded `C.store` creates an admission cycle: the first per-store current record cannot exist until a binding exists whose G/K source is that same not-yet-created record.

**Recommendation:** authorized **creation** of the first current is a distinct act. G/K for that act come from the **admitted transition intent** (`toStoreGeneration` / `toStateSchema`) plus newly allocated S and the already-admitted N — not from `C.store`. A failed ordinary **read** of current remains unavailable and grants **no** initialization. After current exists, later **reads** may compare `C.store` to the binding; they still do not mint it. Historical/retained stores need an explicit authorized selection of one full S/G/K, never “equal numeric G/K” and never “today’s selected store.”

This does not choose persisted-bytes vs derived-view, and does not accept S9.3.

---

## 4. Lineage roots: no invented transition intent

Sections 1–3 above are the previously accepted addendum (SHA256 `a07f5dc466d682c0771ace8fa3ebc3fb4fdf0eac1a8cfb4423dedbf6f3e0ff03`, 3397 B). This section only qualifies §3’s “admitted transition intent” wording for **first current**.

S9.3 **Lineage roots** (still proposed as S9 law; cited here as the counterexample’s scope, not as accepted owner-law): a root is created by an authorized local act **outside any transition** — installation, or an authorized evidence restore or portable adoption. It allocates a fresh `storeInstanceId`, replaces any copied marker before first publication, imports no node/floor/grant/local-commit authority from the source. **No transition is invented to give it an `intentDigest`.**

Therefore §3 must not be read as requiring a synthetic `InstallationTransitionIntentV1` for those roots. G/K for that first current come from the **authorized root-creation act’s admitted schema/generation** (the same pair-law domains S9.2 already uses for `to` values) plus newly allocated S and already-admitted N — not from `C.store`, and not from an invented intent/journal. Ordinary later transitions still use a real admitted intent; they are a different case. Failed ordinary current **read** remains unavailable and grants no initialization.
