# Independent review — project-registry owner371 r2

**Verdict: `NEEDS-CHANGES`**

Frozen OWNER/REFERENCE only. **Not** selected law, **not** five-member `StoreGenerationBindingV1`, **not** S9.3, **not** OS/crash qualification, **not** product runtime approval. Archive `3b081888…2674` / **202988 B / 63 members**; every `subject.json` member rehashed before use (0 mismatches). Normative candidate `registry-draft.md` `41f91028…2165` / 22136 B. Priors preserved: registry r1 `14ef7883…026c`, retention371 `42e82ed9…499f`, binding370 `304f4430…6b9a`. No product/architecture edits.

Independent replay (fresh `grok-out/replay-*`, scripts refuse overwrite of extract): **211/211** reference cases, results **byte-equal** author `2eee78ca…fb09`; **23/23** jsonschema+extra-rule checks (Python 3.12.13, jsonschema 4.25.1, `-I -B`); capacity max wrapper **320555** bytes, six journal states match author; six compiled pure-model faults detected after baseline pass. README’s “independent schema checks” are root’s library cross-check, not this peer run; this peer run still passed. No native suites.

---

## T1–T8 on revised bytes

| T | r2 |
|---|---|
| T1 Dual projections | **Resolved in prose:** `RegistryDocument` (all four statuses) ≠ `RegisteredNamespaceList` (ACTIVE∪RETIRED → S9 `registry`/`registryDigest`/`leaseSet`) ≠ `RegistryStartGate` (zero RESERVED + prior slot retired). Gate applies even to same-schema core-update. Model `namespace_list` refuses if any RESERVED rather than a separate `start_gate()`; acceptable only if the S9 list is never projected until the gate passes. |
| T2 RETIRED census | **Resolved as explicit NEW choice.** Trace: ACTIVE N1 + RETIRED N2 with missing/unreadable `writer.lease` ⇒ `store migrate` **unavailable**, never BUSY, never omit N2. |
| T3 one-to-one | **Resolved as live** ProjectId↔N; historical ProjectId + fresh N via authorized adoption; N never reused. |
| T4 post-fence | **Resolved in prose:** handoff demotes registry FD to row provenance; ordinary context must not reread `I/project-registry.v1` or reacquire the fence for it; retain root/marker/namespace handles + lease; same-schema `selection.pair` replace tolerated. |
| T5 crash prefixes | **Partial.** 25 `recovery-prefix-*` cases exist; observations are **supplied tokens**, not native reachability (see required findings). |
| T6 ABANDONED retention | **Resolved:** lifetime retention; no implied per-N GC; abandoned N does not occupy a different new N. |
| T7 birth | **Resolved as NEW gate**, including first-use refusal without Linux BTIME. Not identity §2 inherited. |
| T8 4096 vs 65536 | **Resolved:** this profile’s cap; generic `maxItems` unchanged; 320555 independently reproduced. Placeholders are not authenticated journal identities. |

Dispositions correctly refuse to promote 370 recommendations to inherited owner authority.

---

## Initial namespace footprint (root extra)

Specified: after **durable RESERVED**, publish `I/host/projects/N` as a **0700** directory containing **exactly two empty regular files** `writer.lease` and `readers.lease` at **0600**, prepared under an unpublished same-parent temp name, **atomic no-replace** onto a **positively absent** final name, then marker create-new, then ACTIVE. Recovery completion requires the **RESERVED row + root join + this complete two-file footprint** together; incomplete/foreign/symlink/extra-entry/unreadable ⇒ unavailable, no repair/deletion. Unpublished temps are not scan-adopted.

**Challenge:** Empty files are valid flock inodes; publishing them is **lock-carrier initialization**, not holding a lease. That is not a revival of SQLite `project_registry`. It **is** a new physical owner (draft says so). Still missing an explicit sentence that flock on **RESERVED or ABANDONED** N lease files is **lease-on-unregistered-namespace** (S7), never BUSY-as-admission. `complete-initial` in the model is a **label**; it does not check two names, emptiness, or modes. Dest-exists / extra-entry behavior is prose-only. Conservative and right-shaped if those sentences are added; not a native proof.

---

## Required: adoption marker vs ordinary create-new

**Ordinary first-use** (draft steps 1–4): marker **absent**; RESERVED → namespace footprint → **create-new** marker → ACTIVE. If a marker is already present, that is one-sided; ordinary create-new must not overwrite.

**Explicit adoption** may start with an **exact** 92-byte marker **copied from an admitted portable bundle** at the **new** root, plus a **fresh** N. Completion must **reconfirm that marker’s durability** (file+parent barriers, untracked, exact bytes, matching reserved ProjectId) and **must not create-new**. r2 adoption paragraph allocates fresh N and forbids foreign leases/credentials; it **does not** state this marker clause.

**`reservation_completion('absent','exact',…)`** returns `publish-namespace`, `reconfirm-marker-durability`, `publish-ACTIVE`. That sequence is the **adoption-shaped** completion, but the case is also named `recovery-prefix-absent-exact` as if it were an ordinary crash prefix. **Ordinary order never yields exact marker before the namespace directory.** Therefore RESERVED + exact marker + absent namespace is **explicit recovery / adoption completion**, not a lawful ordinary first-use crash continuation. Auto-continuing it as ordinary recovery could activate a copied marker without bundle admission.

**Concrete correction:** (1) Ordinary recovery: if marker is exact and namespace is absent, **refuse ordinary crash-continue**; require independently authorized recovery/adoption. (2) Adoption completion clause: bundle-admitted exact marker at target; never create-new; reconfirm durability; publish fresh-N footprint from positive absence; then RESERVED→ACTIVE. (3) Label model `recovery-prefix-*` as **supplied observation grids**, not reachability of native crashes. (4) Optional: `start_gate()` separate from `namespace_list()`; explicit unregistered-lease on RESERVED/ABANDONED files.

No opaque-`projectKey` revival detected. Envelope/marker/eight-candidate/missing-registry≠empty/T1–T4,T6–T8 prose are otherwise aligned with the r1 advisory once the adoption/prefix split is written.

---

## requiredFindings

1. Distinct **adoption reservation/completion** clause: exact pre-existing admitted-bundle marker; durability reconfirm; **no create-new**.
2. **RESERVED + exact marker + absent namespace** is not an ordinary first-use crash prefix; recovery-prefix names are not native reachability proofs.

Not acceptance. Root authors the next freeze for independent review before implementation.
