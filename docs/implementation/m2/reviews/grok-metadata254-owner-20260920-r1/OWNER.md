# Source/owner assistance — next recovery metadata admission (254)

**Standing:** bounded owner map for the next recovery **catalog/component-manifest body and join** step. **Not** review approval, implementation readiness, or a 253 re-review. 253 remains archived (`dcb6b43b…3169`). No product/candidate/prior-review edits.

Read-only sources: frozen primary 251 at `/tmp/opensip-implementation/m2-authenticated-command-reference-251/candidate` and retained 215 `/tmp/opensip-implementation/m2-trust-owner-draft-215/OWNER.md` (`780a6dd5…0d60`). Preserve one `Operation`. Reuse existing validators; do not invent another schema.

215 staging order **B.5** already requires: authenticate the applicable **new-root** catalog, revocation and every other signed member; validate complete typed member availability, **shapes, identities and the exact role/payload joins**. 253 closed only signature quorums + finite key union. Bodies and those joins are this step.

---

## 1. Component manifest — existing schema and admitter

**Latest schema/patch owner (do not fork):**

| Item | Path | SHA256 prefix |
|---|---|---|
| Design-contract v11 | `docs/coop/artifacts/component-manifest-schemas.v11.json` | `1c0b8868…` |
| Status | `CANDIDATE-NOT-APPLIED`, `binds: NOTHING` | — |
| Patch owner | DR-103 / that artifact’s `repairLog` (v10→v11 targeted ops only) | — |
| Signing preimage owner | ID-DEP-1 / `opensip.metadata.manifest.1` | envelope routes |
| Compatibility windows | **DR-111** per-surface matrix; `manifestSchemaVersion` is a **bare integer**, not a range | v11 `manifestSchema.fields[0]` |

v11 is a **design-contract**, not a Draft 2020-12 JSON Schema. Admission identity is sha256 of **stored bytes**; signing preimage is canonical JSON (ID-DEP-1), declared not defined in v11.

**Reserved binding points (populating is RJ-6 / `RESERVED_FIELD_POPULATED` until the named DR closes):**

- `stateMigration` — DR-124 / DR-106 / DR-109 / DR-113
- `updateData` (update/rollback/repair/revocation metadata) — **DR-110**, DR-112
- `treeRootDigest` — DR-006 / EIR (do not mint a new identity recipe)
- `trustMetadata` — DR-112
- `deprecation.doctorRemediation` — DR-114
- `indexSchema.trustMetadata` — DR-112

**Executable signature admitter (reuse, do not rewrite):**

- `docs/coop/design-corrections/security/envelope_reference.py` `Verifier.verify(stored, envelope, root, 'manifest', publisher_namespace=…)` (`ea06a785…`)
- Routes: `signature-envelope-routes.v1.json` kind `manifest` → domain `opensip.metadata.manifest.1`, role `TR-COMPONENT`
- `publisher_namespace` must equal `envelope['namespace']` or omit (mismatch → `RJ-4 ENVELOPE_MISMATCH` / `publisher namespace`)
- Root for this call is the **authorized prospective replacement**, same `Operation` as 251/252/253

**Cited but not in this 251 tree:** `check-security-unit.v2.py` `admit_manifest` (v11 **subset**: required members, kind, UUID, role, name charset, root-command binding, PT tokens, path rule, reserved points, interval form) is named in `docs/coop/completion/security-completion.v2.md` §2.2. The `.py` is **absent** from this candidate. `security_unit_lib_v8.py` (`3e28bc7b…`) has `admit_root` / `admit_root_document` / `admit_policy_paths` / `merge_policy`, **not** a full v11 manifest admitter.

**Reuse for body shape (until a selected JSON Schema exists):** do not invent a parallel schema. Either (a) encode the v11 **required + reserved-null** subset as a validator that refuses populated reserved points, matching the cited `admit_manifest` subset, or (b) wait for DR-103’s reviewed JSON Schema. Compatibility windows stay DR-111.

**Missing joins (215 B.5 “identities and exact role/payload joins”):**

- Catalog `releases[].stableId` / `publisher` / `version` / `manifestDigest` / `manifestPreimageSha256` / `envelopeDigest` **equal** the admitted component’s stored sha256, `opensip.metadata.manifest.1` preimage, and envelope sha256
- Envelope `namespace` **equals** catalog `publisher` (pass that string into `Verifier.verify(..., publisher_namespace=publisher)`)
- Payload `members.manifests[]` sha256 **equals** `releases[].manifestDigest` (and path pairing already in 252 index)
- `hostCoreConstraint` interval is selected by `compatibility-selection-model.v3.py` (`7e84a9f6…`) against a lock, **not** by catalog completeness; do not fold lock selection into this recovery reader

---

## 2. Catalog — completeness, digests, platforms, version floors

**Executable shape (reuse):**

- JSON Schema: `docs/coop/completion/security-schemas.v2/catalog.schema.json` (`939ad388…`), `$id` `urn:opensip:design:catalog:1`, title **supersedes the signed half of v11 `indexSchema`**
- Already pinned as `I.CATALOG` in `trust_input_reference.py` (`13491b74…`) `PINS['catalog']`; call `primary(CATALOG, body, 'accepted-catalog-shape')` (today used for **accepted** catalog in `join_restriction`, not incoming payload catalog)
- Signatures: `Verifier.verify(..., 'catalog')` — domain `opensip.metadata.catalog.1`, role `TR-INDEX`, same prospective root as 253

**Release-to-member fields already in that schema (do not add fields):**

`releases[]` requires `stableId`, `publisher`, `sourceClass` (`first-party`|`explicitly-trusted`), `version` (SemVer), `manifestDigest`, `manifestPreimageSha256`, `envelopeDigest`, `hostCoreConstraint` `{min,max,includeMin,includeMax}`, `artifacts[]` `{platform ∈ {macos-arm64,macos-x86_64,linux-x86_64,linux-arm64}, archiveProfileId, archiveDigest, sha256}`

**Completeness joins that 252/253 do not do (unowned executable, owned by 215 B.5):**

- Every `members.manifests[]` hash appears as some `releases[].manifestDigest`
- Every `releases[].manifestDigest` in this recovery FULL payload is present as a retained manifest member (no dangling catalog row)
- `releases[].envelopeDigest` = sha256 of the selected TR-COMPONENT envelope bytes from `Index.select`
- `releases[].artifacts[].sha256` vs payload `members.artifacts[]` (252 only checks observation **hash equality** to declared artifact rows, not catalog artifact rows)
- `reservedRootCommands` vs v11 reserved-name universe (CI parity is TC-NAME-1; not this reader)

**`rootVersionRequired` / `revocationVersionRequired`:**

Present as **required integers** on the catalog schema. **No Python comparison** exists in 251 (`grep` hits only the schema and completion prose). Do **not** invent `>=`.

Owner-consistent reading for **this recovery payload** (215 “exact prospective document contexts”; “root/catalog/revocation heads and their counters are one accepted unit”):

- `catalog.rootVersionRequired` **equals** the authorized replacement `rootVersion` (exact). A catalog minted for another root version is a different prospective context, not a floor that rides forward.
- `catalog.revocationVersionRequired` **equals** the authenticated list’s `revocationVersion` for this payload (exact pairing). COMMIT anti-rollback against **accepted** `lastKnownRevocation` / catalog `snapshotVersion` remains the lifecycle owner (`security-completion.v1.md` §4.5: lower `revocationVersion` refuses; §4.6 payload with lower `snapshotVersion` after a higher accepted one refuses `PAYLOAD-NOT-ADMISSIBLE`).

Ordinary later refresh of a catalog on an already-accepted head may later define monotonic `snapshotVersion` / `revocationVersion` **≥ last accepted**; that is COMMIT/current-trust, not this staging body join. 215 defers expiry/freshness/future-time/floors to COMMIT.

---

## 3. Policy, repair, artifact — recovery FULL signed scope

**In inventory (payload2):** `root-recovery-payload.schema.v2.json` (`47bc09e5…`) — `permissionPolicies[]`, `repairMaterial` (path+sha256 **or** `{standing: absent-by-typed-absence, ridesOn: DR-110}`), `artifacts[]`. 252 already captures policy/repair **bytes** and artifact **observation hashes**; bodies/semantics pending.

**Policy (reuse):**

- Shape: `docs/coop/completion/security-schemas.v2/permission-policy.schema.json` (`3d7153d9…`) `policySchema: 1`, `policyScope` `project|global`
- Path admission: `security_unit_lib_v8.py` `admit_policy_paths` / `merge_policy` (SEC3-M2: normalized member paths; project may only **narrow**)
- Foundation host files: `host-foundation-model.v2.py` + same schema pin
- Envelope: **none** in `signature-envelope-routes.v1.json` — policies are unsigned members; do not invent a TR-* signature for them here

**Repair:** typed absence is the recovery-FULL default (`DR-110`). Presence of a repair blob is inventory-only until DR-110 designs update/rollback. Do not treat a present blob as an executable repair plan (`workflows_model.v3.py` `admit_repair_plan_v2` is evaluator repair, not payload repairMaterial).

**Artifacts:** 252 `artifactObservations` set/order/digest; `observedBytes`/custody asserted. Catalog `releases[].artifacts[]` is the **identity** join (platform + archiveDigest + sha256). Do not recapture artifact bodies in this Operation. Qualification of archives is not this slice.

**Index already reusable:** `trust_metadata_index_reference.py` `Index` / `select` (`be87c4c3…`) — listed-path pairing, NFC casefold aliases, file-parent rule, preimage check. 252 already uses this; next step **loads bodies through `select` then `primary(schema, …)`**, still on the same `op.index` / `op.input_work`.

---

## 4. Additional `rootChain` entries (after replacement self-ROOT and held RECOVERY pass)

**Do not** authenticate those extra pairs with the prospective replacement or the **current** revocation union.

215:

- B.3: replacement possession uses **its own** root-key threshold; authorization replaces only the old-root-key **continuity half** for this act
- B.5–B.6: prospective catalog/list/members under the **authorized new root**
- Ordinary continuity (before a head): **complete** admitted immutable core embedded chain from **index-zero** to final head, never a shorter prefix or payload-supplied anchor (`OWNER.md` A and §95)
- Historical clock proofs: recheck against **original** authentication context, not later head/expiry/list (`OWNER.md` ~117)
- Per-payload `rootChain` max 64 is **not** a lifetime history bound (`OWNER.md` §133)

**Existing chain machinery (wrong to call with current union / prospective-as-prev for historical prefixes):**

- `envelope_reference.py` `Verifier.admit_signed_root_chain(state, presented, t_eval, wall, revoked_keys=())` — each link: `verify` under **prev** and under **new**, then `admit_root_chain`
- `security_lifecycle_model_v1.py` `verify_root_chain` / `admit_root_chain` (S5): **both** previous-root threshold **and** new-root threshold; `previousRootVersion == prev.rootVersion` and `rootVersion == prev+1`; intermediate **expiry never consulted**; **final** unexpired at `t_eval`; `revoked_keys` subtracted from **both** old and new signer sets

Using 253’s incoming-key union as `revoked_keys` on historical links would apply **later** revocations to **earlier** proofs — forbidden by 215. Using the replacement as `prev` for a payload-supplied older root would treat recovery as ordinary TUF chaining.

**253 already did the non-auth treatment:** extra pairs → `unresolvedRootPairs`; pending `other-root-chain-context-admission`. Keep that. Next metadata step must **not** flip those paths to `Verifier.verify(..., replacement, 'root')`.

**If** a later owner authenticates embedded/historical links, reuse `admit_signed_root_chain` with:

- `state.acceptedRoot` = the **historical predecessor document** for that link (or 229 embedded-head producer, `OWNER.md` §142 — 215 notes earlier 215 models received an **asserted** authority root and did **not** implement that producer)
- `revoked_keys` = the revocation context **admitted with that original proof**, not the prospective union
- `t_eval`/`wall` **not** smuggled in from COMMIT; 215 defers TRUSTED-entry time predicates

Until that 229/chain owner exists, extra `rootChain` rows stay unresolved inventory, not authenticated history. Zero unresolved paths is still not a staging grant (253).

---

## Genuinely unowned / do not invent

| Boundary | Status |
|---|---|
| Full v11 JSON Schema + `admit_manifest` executable | Cited (`security-completion.v2.md` §2.2); **checker not in 251 tree** |
| Catalog `rootVersionRequired` / `revocationVersionRequired` comparison | Schema only; no function. Prefer **exact** pairing to this payload’s replacement/list; do not add `>=` |
| Catalog `releases[]` ↔ retained manifests/envelopes/artifacts | 215 B.5; not in 252/253 |
| Incoming catalog vs **accepted** anti-rollback (`snapshotVersion`, `lastKnownRevocation`) | COMMIT/current-trust |
| Historical extra-root cryptographic admission | 229/S5 owner; 253 unresolved only |
| Artifact body custody / archive qualification | Pending; observations only |
| Repair semantics | DR-110 typed absence |
| Policy as signed envelope | No route; unsigned member + v8 merge |
| Command-to-closure semantic join | Still pending (251/252) |

Keep **one** `Operation`: catalog/manifest `primary(...)` and `Verifier.verify` must run on the same `op` as 252 `prepare` and 253 `prepare` (capture already paid; 253 showed recapture charges edges only).

This is not a ceremony proposal and not an implementation claim. Root implements/tests against these existing mechanisms.
