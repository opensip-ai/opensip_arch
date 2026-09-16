# Policy-admission inventory v20 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not runtime acceptance, not glob-21 source re-acceptance, not predicate-matching reference selection, not editable policy-22 source/code approval. Root remains lead. Root assent and private activation are still required.

**subjectManifestSha256** `5bfb6510b690f4d59c767f1c62e7f375e0052503e908e69519bb914fad80689d`  
`docs/implementation/m2/policy-admission-inventory-v20-subject.json` **636** bytes, 3 members pin-match, paths sorted unique.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `repository-file-inventory.v20.json` | 141292 | `321f3da752bc0a900c2829ce217f955daf699e60df66596f62c7ef6c2270f5a7` |
| `policy-admission-inventory-v20/README.md` | 1002 | `2ec5e7c5cc1597a447e5f0e5a9fac01e255b09ad58d10d2ff7e394525c1d8e65` |
| `policy-admission-inventory-v20/successor.json` | 609 | `dfae57f885d59370cda7b2bc1db4443548bbfbbaf55dd85d5e1e9e02d1089829` |

## Checker (`verify_design.py` inventory_successor 85–143)

Successor record has **both** `parentArtifactBytesUnchanged: true` and `inheritedRowsEqualByValue: true` (106–107). Parent pin is the live inventory **candidate** v19, not an inventory successor record. Candidate pin matches disk. Added files are the singleton `crates/evaluator/src/atom-registry.json`.

Original inventory-19 successor (`52ace802…3174` / 566) that omitted `inheritedRowsEqualByValue` remains a preserved private-activation failure and is **not** this unit.

## Parent is live inventory **candidate** 19

Live lock independently **17 inventory / 22 contract** (`7b2e1d8c…eb64` / 51424). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v19.json` 140780 / `ec61d2fbee9e6fdd6000acabe263d2c455f71055b6e8843e5c973351fe9c9725`

That is `successor.parent`. Last contract is runtime **v9**. Live tree has no `atom-registry.json`, `atoms.rs`, or evaluator `policy.rs`.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 382 inherited rows | v19 382 unique sorted paths; all present in v20; **0 mutated** (row objects equal) |
| 1 new file | `crates/evaluator/src/atom-registry.json`; none removed |
| 383 total | 382+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; evaluator still depends on identity (not reverse); no new package/edge |
| v19 path order | subsequence of v20 (insertion at evaluator `src/` index **50**) |
| packaging flags | both required true flags present |

New row: `opensip-evaluator`, `role` metadata, kebab-case `atom-registry.json` matching `body-registry.json` / `coverage-registry.json` / `view-joins-registry.json` filenames, `generated: false`. Description: closed atom projection metadata for **existing planned** `policy.rs` (compiler: admit/compile + portable glob) and **later** `atoms.rs` (algorithm: evaluate atoms). Not caller-supplied evidence, Run, or replay.

Sibling JSON registries use `role: registry`; this row uses `role: metadata`. Filename and owner match the named convention. Not a required finding.

## Metadata extract (layout claim; policy-22 not accepted)

Editable trial `m2-policy-admission-trial-22` already carries a derived `atom-registry.json` (**21633** / `b1ae0b4a…eb68`) whose `source` pin is the selected evaluator-projection-registry `65f163cc…5abb` / 60005. Independently: **17/17** `relations` equal by value; `comparatorTable` equal; `portableUniverseDomains` equal `engineFamilies.portableUniverseDomains` (typescript/rust/syntax v2). That draft is **not** this unit and is **not** source/runtime approval.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v19**. v20 copies **before-text**.

| v19 pointer | Stable path | v20 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/189/description` | `package.json` | **190** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Glob-21 source review stands separately; proposed predicate-matching reference is still unselected. Editable policy-22 is not approved here. No identity API change, no Run/replay. Root assent and private activation of **this** record remain pending.
