# Authored correction for PS-01 and PS-04

Custody first: the nine frozen planning inputs are **unmodified** (all hashes re-verified), frozen25 is intact (12869 members, 0 mismatches), and my prior `findings.json` is preserved untouched. All work is in `scratch/`.

---

## Change surface

| File | Status | Before | After |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | changed | 78397 B / `af16dcc6…` | 82985 B / `3bd626a7a0f2efd3…` |
| `store-instance-lineage.v1.json` | **new** | — | 30224 B / `4dd6291fbf526010…` |
| `report-asset-binding.v1.json` | **new** | — | 22929 B / `7752aeeba5e310e3…` |

The other **eight inputs are byte-identical**. Plan edits are confined to frozen lines **239–261** (PS-01) and **591–619** (PS-04). Both generated blocks are byte-identical to frozen input, so root's CR-19 F32 regeneration does not collide; I touched nothing in PS-02/03/05/06/07/08 territory.

---

## PS-01 — minimal S9 owner successor + private lineage companion

**Withdrawn.** The plan now says outright that current S9 *cannot* express the validation, and names why: the two records are closed with 11 and 20 members, and `registry` is a `NamespaceList` of strings.

**Successor shape (S9.3, proposed).** A private `StoreInstanceLineageV1` row joined to the existing public journal by its `intentDigest` — a member that record already has. The public journal never references the companion. No member is added to `InstallationTransitionIntentV1`, `InstallationTransitionJournalV1`, `NamespaceList`, `RootV1/V2`, `JournalRecord`, any envelope body or the catalog. `NamespaceList` stays an array of strings: the row is **installation-scoped and carries no namespace list**, because S9.2 already binds the covered namespaces as `leaseSet` under `registryDigest`. No D9 code is minted — refusals reuse `TRANSITION.CURRENT_STORE_MISMATCH` / `CURRENT_SCHEMA_MISMATCH` and the existing `MIGRATION.CORRUPT` quarantine.

**I inspected S9.2 before asserting anything about the counter.** The numeric generation is **not monotonic** — `store-rollback` and `core-rollback` re-select a retained earlier generation — and the plan now says so. The generation and state-schema transitions stay entirely the owner's; the companion only records which instance was selected.

**The rollback rule root specified, and how associations join.** S9 line 654 says rollback "re-selects the retained old store", so that store keeps its **original** `storeInstanceId`. The active `(namespaceId, storeInstanceId, storeGeneration, stateSchema)` tuple is then byte-identical to the pre-migration tuple, so `storeGenerationDigest` is byte-identical and **every pre-migration association joins by plain binary equality — no lineage walk, no row rewrite**. Associations in the abandoned forward store keep their own digest and are reached only through the lineage row or reported unavailable: F35 in the reverse direction. A newly created or restored physical store gets a fresh identity and imports no authority, floors or grants.

Executed property (`check_store_instance_lineage.py`):

```
beforeMigration        1131162e4447...
afterMigration         cc4df6c9d8ff...
afterRollback          1131162e4447...   rollbackRestoresDigest: true
afterRestoreNewInstance f34c0f1b1097... restoreDoesNotImpersonate: true
```

**Specified for implementation:** exact closed schema (11 members, one admitted null with the frozen witness "present-as-null" discipline); owning modules — all **existing** inventory rows, so no inventory row and no generated-section change; location (store-root marker + lifecycle transition store); canonical digest recipe; eight ordered successor obligations; and crash association folded into `recover_transition_journal`'s existing first-act order with no new state or action.

**Canonical digest recipe — one real correction beyond the brief.** Security S2 assigns "everything with a `schemaVersion`" to the foundation product-profile canonicalizer, so the record can never enter `opensip-metadata-canonical.1`. `storeGenerationDigest` is a **raw-artifact** SHA-256 over those canonical bytes, never `H(domain, descriptor)` — which is what keeps root's "no new H-domain" true rather than merely asserted. I also added the guard that **adding any member changes every historical digest**, so the record is frozen at V1 and a new member needs a V2 plus a digest-preserving bridge.

**Three axes separated**, as asked: logical `stateSchema` {1,2} (owner), physical carrier format (the separate carrier coauthor — explicitly *not* in the binding, for the digest reason above, joined by `(storeInstanceId, storeGeneration)`), and the random instance identity.

---

## PS-04 — smallest sufficient anchor

**Withdrawn**, with the reason in the prose: the only published per-member listing is the DR-103 *component* manifest (`kind` vocabulary `component`), the catalog row commits only `{platform, archiveProfileId, archiveDigest, sha256}`, and S9.1 calls the core release manifest schema 2 **prospective**.

**Selected: a build-embedded `HostAssetPinV1` constant in the host binary** holding the exact length and raw SHA-256 of the private asset manifest. I established compatibility from sources rather than accepting it:

- identity §1 lines 18–21 already place the authenticated host in the **TCB** — so trust reduces to bytes already trusted, and per-file signing cannot be stronger than the binary that checks it;
- S9.1 lines 701–702 already prefer "the copy **embedded in the signed core release** (TR-CORE namespace)" over a standalone document for exactly this class of metadata — the pattern is precedent, not invention;
- G3 requires signed offline assets with no ambient download, and the pin needs no catalog at render time;
- S5 lines 306–313 already state that whole-install-root substitution is undetected, so adding signing metadata *inside* that root does not move the boundary.

**TR-CORE cited, not the component path.** I verified TR-CORE is a required root role in both closed root schemas. Install-time provenance stays there; **load-time** integrity is the pin. The core-release-manifest dependency is named honestly as *not published in candidate25* and *not required* for asset integrity — a future core manifest binding would be additive audit convenience only. Four alternatives (ninth `closure2.kind`, component TreeCommitment reuse, a new signed asset manifest, render-time catalog lookup) are recorded with their rejection reasons.

**Concrete behavior:** closed `HostAssetPinV1` and `ReportAssetManifestV1`; canonical-path rules with regular-files-only and no symlink traversal; a seven-step ordered load path (length-bounded read → digest equality → parse → projection compatibility → per-member digest); and validation performed **only when an asset-consuming renderer is selected**, so absent assets never affect human/JSON/agent/SARIF. Failure uses only members of the **closed** D9 v1.14 vocabulary: `operational-failed` / 4 / `faultCause=delivery-required` / `DELIVERY.REQUIRED_FAILED`, with `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` and RunId retention after commit, otherwise no RunId invented. No package manager, no network, no producer kind, and no silent downgrade of a required HTML request.

---

## Executed controls

| Control | Result |
|---|---|
| `check_repository_file_inventory --check` | PASS — 198 paths, chapter matches (unchanged) |
| `check_implementation_planning --check` | PASS — 320 mappings, 38 cases (unchanged) |
| `check_store_instance_lineage` | **PASS** — 0 structural failures, **11/11 negative controls detected**, digest-continuity property holds |
| `check_report_asset_binding` | **PASS** — 0 structural failures, **17/17 admission vectors** |

The negative controls detect enum widening, opening the record, unbounding the generation, dropping the join key, duplicating the binding, unknown owning modules, a dropped operation rule, minting a D9 code, widening the public intent, and turning `NamespaceList` into objects. I did not rerun unrelated suites for a prose-and-schema change.

---

## Limitations

Both companions are **proposed** successor deltas — unaccepted, unfrozen, no readiness. No product code exists; every named owning module is an existing inventory row, which is why no inventory or generated-section change was needed. The lineage control models digest continuity with a **stand-in canonicalizer** (the real one is identity §3's); the asset control models admission and the pin check only and establishes nothing about browser behavior, release builds or signing. Whole-install-root substitution stays undetected in both corrections — frozen25's existing stated bound, not a new weakness. COV-03 and the separately active carrier/migration/read-only-anchor work remain open; both companions name their required joins rather than assuming that work.

One optional follow-up for root's own regeneration pass, deliberately not done here to stay patchable: `crates/reporting/src/assets.rs`'s inventory description still reads "bound by the signed host release artifact", which is not false but is now less precise than the pin. Changing it would force a chapter-14 generated-block regeneration alongside root's PS-07 edit.

Original blind123/8/3 and application review remain pending. This is authored work and needs another substantive review on newly frozen bytes — not my own sign-off.
