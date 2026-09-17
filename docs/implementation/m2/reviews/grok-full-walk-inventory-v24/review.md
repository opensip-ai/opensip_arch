# Full-walk inventory v24 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not runtime acceptance, not editable source-32 approval, not advisory-31 acceptance. Root remains lead. Root assent and private activation are still required.

**subjectManifestSha256** `3544854abf782b396ada1a308295b075a5fe69c8ebacfaca13b093ad475d27d9`  
`docs/implementation/m2/full-walk-inventory-v24-subject.json` **622** bytes, 3 members pin-match, paths sorted unique.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `full-walk-inventory-v24/README.md` | 1245 | `be75e2d5d7b8c2baec9772cdf8a717336283ddce9955f634b204cdd1a9a6f954` |
| `full-walk-inventory-v24/successor.json` | 661 | `9b6d39926eff227f5a16b652b821a520578defa8865cf4fba07fc0b845ad605d` |
| `repository-file-inventory.v24.json` | 146038 | `332d47aaee98a234abe5e76f99f607ed01927dab1640df12f95ed7678f55bcb6` |

## Checker (`verify_design.py` inventory_successor 85–143)

Live `tools/verify_design.py` `inventory_successor` refuses unless the successor record has **both** `parentArtifactBytesUnchanged is True` **and** `inheritedRowsEqualByValue is True` (106–107). It then joins review `verdict`/`requiredFindings`, `inventoryCandidateAssessment` candidate/parent/`successorRecord` pins (108–113), and later root assent (114–120), and checks sorted unique additions with inherited rows equal by value (137–140). `same_reference` on the assessment requires candidate path/bytes/sha256 (`size=True`), parent path/bytes/sha256 (`size=True`), and successor record path/sha256.

This successor record declares **both** required true flags. Parent pin is the live inventory **candidate** v23, not the v23 successor **record**. Candidate pin matches disk. Added files are the sorted pair `crates/evaluator/src/full_walk.rs`, `crates/host/tests/fixtures/full-walk-fixtures.json`.

## Parent is live inventory **candidate** 23

Live lock independently **21 inventory / 31 contract** (`c1f770572a13c55f455b237b1dcaa861e011a17765244721c32329f5142c41f8` / 64971). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v23.json` 144797 / `ecf2d46f74f4cbe56fbff3f3ea5c89eb6a3a95cdc8f8942662e3f983a6be54cd`

That is `successor.parent`. Last contract is runtime **v15** (`0e69f1ec50f01e5013856da7db8eec5dd92c124f43bd52667a435ef1928fcc08` / 11169). Live tree has `import_payloads.rs` and **no** `full_walk.rs` / `full-walk-fixtures.json`. Inherited `crates/identity/src/closure.rs` remains the identity validator (callback seam). Inherited `crates/evaluator/src/replay.rs` remains the separate ReplayedRun owner. Evaluator still depends on contracts+identity; identity does not reverse.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 390 inherited rows | v23 390 unique sorted paths; all present in v24; **0 mutated** |
| 2 new files | `full_walk.rs` + host fixture; none removed |
| 392 total | 390+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v23 path order | subsequence of v24 (insertions at evaluator `src/` **63** and host fixtures **114**) |
| packaging flags | both required true flags present |

New rows (`generated: false`, `standing: proposed`):

- `opensip-evaluator` **validator** `full_walk.rs` (snake_case). Description: fixed retained structural Run composition and selected semantic owners in reference order; derive native-frame/universe/capability census from actual traversal; callers cannot supply callbacks, registries, census, or an admission flag; explicit independent walk, owner-invocation, and per-owner limits; diagnostic counts only; evaluation/replay and publication custody remain separate.
- `opensip-host` **fixture** `full-walk-fixtures.json` (kebab, sibling of `import-payload-fixtures.json`). Shared object/blob pools; existing per-document parser cap; default diagnostic refusal and separate resource-boundary checks; does not qualify native compilers or complete replay.

Live `native-context-fixtures.json` **3736129** and `import-payload-fixtures.json` **3085386** remain under `MAX_BYTES = 4 * 1024 * 1024`; those inventory rows are unchanged.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, parented at **v23**. v24 copies **before-text**. `successor_chain` (312–346) projects by **stable filepath** after additive inserts.

| v23 pointer | Stable path | v24 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/197/description` | `package.json` | **199** |
| `/files/264/description` | `schemas/sources/imported-v1.schema.json` | **266** |

Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Editable source-32 and advisory-31 are **not** accepted here. No identity API change, no caller ADMIT, no ReplayedRun, no publication token. Root assent and private activation of **this** record remain pending.
