# Reconstruction inventory v32 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** source48, **not** runtime24, **not** full M2. Frozen/live/history not edited. Root remains lead. Not Claude agreement.

Live `inventory_successor` admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the contract token and would be refused at inventory activation.

**subjectManifestSha256** `641c005332b7fe0a27aea31187ca059824f65c977a5960a4bed1b1b5a9a4d255`  
`docs/implementation/m2/reconstruction-inventory-v32-subject.json` **632** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `reconstruction-inventory-v32/README.md` | 1403 | `17bc636003269a03190e25b270fd5657acfe242c6e43953c143aedb7e92a0103` |
| `reconstruction-inventory-v32/successor.json` | 677 | `e62601d6cbab4a223a5c3276f1cd2cc08f9bc7b04f02889b34e74e4a724b960d` |
| `repository-file-inventory.v32.json` | 154945 | `105a260d966ab0cd61a11798493cd970e114aab9380c003d5eec5c27c513b72e` |

## Checker

Successor declares both required flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v31, not the v31 successor **record**. Candidate pin matches disk.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. Two sorted unique additions; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate. `addedFiles` matches those two paths.

## Parent is live inventory **candidate** 31

Live lock independently **29 inventory / 43 contract** (`85044` / `b4849af56ddba279acc2a29f444214aa46e5cb224a8fac3d6fca0abfd7c954c5`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v31.json` **153734** / `07d553e712e74d7c267cac6a4f62e1579b3654cb2c49660637900e02e8e49e00`

That is `successor.parent`. Accepted **runtime-23** (`native-runtime-selection-v23/successor.json` **17186** / `95bb1d57501fb06bc7bbf6a932fd5fe8f2508a5934471be89d4743997833b6b9`) and **reference-49** (`reconstruction-closure-reference-selection-v1/successor.json` **4344** / `54e84aed05f26bdd1f5a8744157be17447f21ec4c0c318e0eb11dae6a2b960d6`) are live **contract** records (`ACCEPTED-DESIGN-UNIT`). Last contract is that reference unit.

Live product has **neither** new path. Inherited `native_owner_tests.rs` / `full_walk.rs` remain the dispatch and private census owners. This layout adds no package or edge.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 407 inherited rows | v31 407 unique sorted paths; all present in v32; **0 mutated** |
| 2 new files | listed below; none removed |
| 409 total | 407+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical |
| v31 path order | subsequence of v32 (inserts at **75** and **134**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New rows (`generated: false`, `standing: proposed`):

| Path | Package | Role | Index |
| --- | --- | --- | ---: |
| `crates/evaluator/src/input_reconstruction.rs` | opensip-evaluator | source | 75 |
| `crates/host/tests/fixtures/reconstruction-fixtures.json` | opensip-host | fixture | 134 |

Naming: snake module beside `execution_reader.rs`; kebab fixture beside `execution-input-fixtures.json`. Evaluator owns reconstruction; host owns fixture bytes. Descriptions: no public caller map adapter; Plan-named scanner closures; occurrence lists; duplicate inventories refused before counting; not predicate truth/replay/custody.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, parented at **v31**, JSON pointers `/files/7|13|213|280/description`. Candidate copies **before-text**. After the two inserts (evaluator **75**, host fixture **134**, both after index 13), project by **stable filepath**:

| v31 pointer | Stable path | v32 pointer |
| --- | --- | --- |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/213/description` | `package.json` | **215** |
| `/files/280/description` | `schemas/sources/imported-v1.schema.json` | **282** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers (7, 13, 215, 282). Do not rewrite the current 29/43 lock during this review.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept source48, runtime24, reconstruct semantics, replay, or custody. Root assent and private activation of **this** record remain pending.
