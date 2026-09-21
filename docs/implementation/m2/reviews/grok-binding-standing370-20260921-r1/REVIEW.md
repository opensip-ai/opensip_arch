# Binding / source-standing gap — 370

**Standing:** read-only source-standing audit completing the per-item application46 gap that SOURCE-NOTE362 left open. **Not** design-unit acceptance, **not** S9.3 upgrade, **not** a native header, **not** current authority, **not** implementation authorization. Runtime25 materialization (`6abaa71e6` / `b3af5e85c`) is root work; this report does not treat live source as owner acceptance. Recommendation is not code.

SOURCE-NOTE362 (`772694b0…0cb8`) correctly held that application46 ACCEPT of after-image bytes does not upgrade a heading that still says “proposed.” This audit inspects the **dispositions and owner text**, not membership alone.

---

## Pins (independently rehashed)

| Artifact | SHA256 | Bytes | Lock input? |
|---|---|---:|---|
| Live `design-lock.json` | `987bfd47…a25c` | 89104 | — (changed since 362’s `64b3f3e5…` by inventory55; owner hashes below still match) |
| application-subject.v46 | `dab6e00f…43f7` | 126405 | approvals.applicationManifest |
| application-review.v46 | `375b2e9d…5eb4` ACCEPT | 186003 | yes |
| root-application46 assessment | `e59b2ff7…e238` | 5479 | yes; `implementationAuthorized: false` |
| activation.v1 | `faf90047…c4a8` | 758 | design acceptance only |
| S9 `security-and-lifecycle.md` | `a319da39…d9d6` | 119915 | yes; app46 after-image |
| `store-instance-lineage.v1.json` | `919d1717…5210` | 68487 | yes; app46 after-image |
| implementation-boundaries | `8e6e8bab…d33b` | 112850 | yes |
| commit-recovery-plan | `cbaac9b1…cbb5` | 49633 | yes |
| identity-and-evidence.md | `c82404f3…b31f` | 135448 | yes; app46 after-image |
| resolved-inputs.v2.json | `0114205a…8f43` | 107615 | **no** |
| coop `02-domain-model.md` | `2e7dd9ad…f6dc` | 16437 | **no** |
| lifecycle-carrier.contract.v2 | `0d087667…fc02` | 19518 | **no** |

Application46 scoped-owner rows (DR-201–205) are ACCEPT-DESIGN of those subjects; none of them is a separate “S9.3 is now S9 law” disposition. `implementationAuthorized` remains false on manifest, assent, and activation.

---

## What is accepted law vs still proposed

**Accepted (selected lock / S9.2 / recovery-plan schema):**

- InstallationTransitionIntentV1 11 members and JournalV1 20 members are closed; neither carries store instance identity. S9.2 `registry` is `NamespaceList` of strings (lineage companion A1–A3).
- S9.2 schema/store pair law is published reference behavior (A4/A4b): same schema keeps the store; schema change selects a new store.
- `StoreGenerationBindingV1` is exactly `{schemaVersion:1, namespaceId, storeInstanceId, storeGeneration, stateSchema}`. Digest is SHA-256 of those canonical bytes; V1 is frozen; adding a member needs V2 plus a bridge that preserves old digests (boundaries 240–262; recovery-plan `storeGenerationBindingSchema`).
- The security guard must obtain that binding **through an admitted handle and registry, not from request fields** (boundaries 257–258).
- Store-root marker is S-only; three-way readable / absent / unreadable (S9.3 prose; 358). Independent `C.store` is three-member `StoreBinding` — necessary provisional comparison, **not** the five-field binding (358 ADDENDUM).
- Identity §2 (lock input): ProjectId **retains PROJECT-ID-V1** (`prj1-` + 64 lowercase hex); untracked `.opensip/project-id.v1` and private host registry must agree; missing both is first use; unilateral or contradictory presence refuses.

**Proposed, not accepted S9 law:**

- Locked S9 heading line 953 is still `### S9.3 Private store-instance lineage (successor; proposed, not accepted)`.
- Companion `919d1717` standing: “Proposed minimal successor … Requires its own substantive review on newly frozen bytes.”
- Boundaries 266–287: “Current S9 cannot express this validation … That successor must be frozen and reviewed; **it is not accepted here.**”
- Working physical owner 203 (unselected). PSL 201 is **not** a current lock input.

Accepting those after-image files did **not** silently accept S9.3. PS-01’s withdrawn claim (that S9 already validated the instance tuple) remains withdrawn.

---

## Native five-field acquisition (the missing contract)

Selected sources **do not** define a `stores/S` G/K header. Marker cannot carry G/K. `NamespaceList` cannot carry G/K. Ledger stores only `storeGenerationDigest`, not plaintext G/K. Inventing such a header and calling it existing design is forbidden.

**Legitimate alternatives (normative choice, not yet made):**

1. **Derived canonical view (recommended smallest path):** under one admitted handle, compose `{1, N, S, G, K}` from independently admitted owners: N from the **one** registry/root binding that also feeds leases/journal/floor/ledger; S from the three-way marker; G/K from independently decoded security current `StoreBinding` (and, only after S9.3 is accepted, from a lineage triple). Canonicalize once; digest for ledger correlation. No sixth native file.
2. **Persisted five-field bytes** as custody-protected metadata: **not** specified on any selected physical path. Would be a **new** owner, not a discovery of PSL/203.

Boundaries “custody-protected store metadata” + “obtain through handle and registry” are **ambiguous** between (1) and (2). That ambiguity is the owner-correction target. Practical 344/358/359/361/368 joins already do three-field comparisons; they must not be promoted to (1) without the explicit owner.

**Failure/absence/unavailable:** unreadable marker ≠ absent; missing required parent is unavailable unless first-creation absence was admitted; missing five-field binding is unavailable, not “use pair G/K.” Read-only observations never create directories, markers, registry rows, or bindings. Restart/index-rebuild: binding survives if owners survive (boundaries 264–265). Restore/adoption: S9.3 (still proposed) replaces any copied marker before first publication so a restored store cannot impersonate its source. Move: identity §2 — authenticated registry move, no live writer.

**Implications for `ProvisionalInstallationRecords` / `Trust` / `Lineage`:** they remain provisional. Pair + marker S + `C.store` + file lineage nodes are **not** `StoreGenerationBindingV1`. They must not mint namespace/registry/handle authority. A later join can consume them as **inputs** to a derived view only after the owner exists.

---

## PROJECT-ID-V1 inheritance (marker encoding is specified)

Do **not** report marker bytes as wholly unspecified.

Exact historical owner: `docs/coop/artifacts/resolved-inputs.v2.json#/projectIdContract` (`0114205a…`, 107615 B). `markerBytes` is ASCII `opensip-project-id-v1` LF + `prj1-`+64 lowercase hex + LF — **not JSON**. Independently: all-zero ProjectId yields **92** bytes, SHA-256 `1a791d57d6d4c0e137dd08d81d7d076a18a5a93a967a0b82ec176597c13a7ef1`. Protocol: up to **eight** independent CSPRNG candidates; atomic registry reservation; then marker create-new + fsync marker and parent; then ACTIVE. Crash: drop uncommitted reservation or complete an exact matching marker; any other pre-existing bytes refuse. Callers never supply ProjectId.

`docs/coop/architecture/02-domain-model.md` lines 130–147 (**BINDING, IMPLEMENTABLE_UNEXECUTED**) restates allocation/marker/registry pairing and **links that file**. Current identity §2 **retains the name PROJECT-ID-V1** and the agreement/first-use/refusal law, but **does not cite `#/projectIdContract`**. Identity cites `resolved-inputs.v2.json` for **planId** encoding, not for ProjectId marker bytes.

**Inheritance contradiction:** the only selected lock text (identity §2) keeps the **name and agreement law**; the **byte recipe and eight-candidate protocol** live in a non-lock, non-app46 file. Domain-model is also not a lock input. Native product still has no codec that admits those 92-byte marker contents. The next owner should **pin `projectIdContract` (or copy its `markerBytes`/allocation rules into a lock-selected successor)** rather than re-specify from memory — and must not treat identity’s silence as “encoding unknown.”

---

## Registry carrier bridge (separate; do not revive opaque-key)

Historical `lifecycle-carrier.contract.v2.json` / `.schema.v2.sql` (not lock inputs; status PROPOSED): `project_registry` has **nine** closed fields (`projectKey`, `namespaceId`, `platform`, `rootPathBytesHex`, `deviceId`, `inodeId`, `birthSeconds`, `birthNanoseconds`, `status`). `projectKey` is an **opaque** 1–1024 UTF-8 host key; `lifecycle_project_root_verified` forbids taking identity from `.opensip`. That is **no repository marker authority**.

Physical201 (historical layout copy, not lock input) **adopts only the locator** (`I/host`, `I/host/projects/N`) and states: “Adopting this locator does **not** revive the historical registry’s superseded identity or lease protocol.” Opaque `projectKey` / four-field epoch / `newRoot` callback rules are **not** current identity §2.

**No selected source** supplies the native revised registry carrier that would store PROJECT-ID-V1 beside namespace UUID and prove marker/registry/root agreement on `prj1-` bytes. S9.2 `NamespaceList` is still strings only. That bridge is a **separate** successor from five-field store acquisition. Mixing opaque `projectKey` into a new unit would accidentally revive superseded identity.

---

## Smallest exact next owner unit (recommendation only)

One **explicit** successor (or two tightly joined ones), newly frozen and independently reviewed:

1. **S9.3 law:** either accept the existing `+`-only insertion as S9 text after review of newly frozen bytes, or keep it proposed — do not leave “accepted file / proposed heading” ambiguous.
2. **Native acquisition of `StoreGenerationBindingV1`:** derived canonical five-field view under one admitted handle; no `stores/S` G/K header; N from one registry/root binding; S from three-way marker; G/K from independent current `StoreBinding` (lineage triple only if/when S9.3 is accepted). Unavailable ≠ absent ≠ pair fallback. Read-only never creates. Preserve V1 digest and all closed public records.
3. **Optionally, separately:** pin `resolved-inputs.v2.json#/projectIdContract` (or equivalent lock-selected copy of `markerBytes` + eight-candidate protocol) and a **revised** registry carrier that agrees with `.opensip/project-id.v1` on PROJECT-ID-V1 — **without** opaque `projectKey` / historical `newRoot` semantics.

Practical implementation (368 file lineage, 358 S-only marker, 344 `C.store`) can remain provisional inputs. Unresolved normative choices: derived view vs persisted five-field bytes; S9.3 accept vs keep-proposed; ProjectId contract pin vs identity-only name retention.

---

## requiredFindings

None against a design-unit under review: this **is** the gap report. Runtime25/368 code is not rejected for lacking this owner; they already disclosed the gap. Do not implement from this recommendation without a frozen successor and independent review.
