# Input-structure inventory v31 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** source47, **not** runtime acceptance, **not** full first-evaluation structural closure, **not** full M2. Frozen/live/history not edited. Root remains lead. Not Claude agreement.

Live `inventory_successor` admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the contract token and would be refused at inventory activation.

**subjectManifestSha256** `f282369b2815036e6853d9f57321ad94365aed1ee3daa148e898769b331970b4`  
`docs/implementation/m2/input-structure-inventory-v31-subject.json` **634** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `input-structure-inventory-v31/README.md` | 1237 | `5d9cd8dd2a226f24ce4182595e4f02d7a88584919f60a5f8c54be3c260e74be8` |
| `input-structure-inventory-v31/successor.json` | 686 | `3e640d2ec1ae23d3cff6ae5bca44d81c83155509ddfbda739500a9e4d62fc77f` |
| `repository-file-inventory.v31.json` | 153734 | `07d553e712e74d7c267cac6a4f62e1579b3654cb2c49660637900e02e8e49e00` |

## Checker

Successor declares both required flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v30, not the v30 successor **record**. Candidate pin matches disk.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. Two sorted unique additions; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate. `addedFiles` matches those two paths.

## Parent is live inventory **candidate** 30

Live lock independently **28 inventory / 41 contract** (`82055` / `de519f814e7370dd8f75db3e4d93ab45868c67c3b6d670711f0d9274e6710ca0`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v30.json` **152687** / `487c36323deb7235453b1f22f55192d273b6f67c7143010d5a9a156c051aa6fd`

That is `successor.parent`. Last **contract** is accepted runtime **v22** (`native-runtime-selection-v22/successor.json` **16495** / `15601e17c019cdd882568897f8d43832902e372dd8f392ca30aeec41d243911f`).

Live product has **neither** new fixture. Inherited owners remain: `policy.rs` / `full_walk.rs` / `run_links.rs` (evaluator compilation and Run walk), `closure.rs` (identity structural callback), `native_owner_tests.rs` (host dispatch). This layout adds **no** production source path, package, or edge.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 405 inherited rows | v30 405 unique sorted paths; all present in v31; **0 mutated** |
| 2 new files | listed below; none removed |
| 407 total | 405+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical |
| v30 path order | subsequence of v31 (inserts at **127** and **132**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New rows (`generated: false`, `standing: proposed`, package `opensip-host`, role **fixture**):

| Path | Index |
| --- | ---: |
| `crates/host/tests/fixtures/input-structure-fixtures.json` | 127 |
| `crates/host/tests/fixtures/plan-policy-fixtures.json` | 132 |

Naming: kebab JSON beside `plan-input-fixtures.json` / `execution-input-fixtures.json`. Host owns fixture bytes; evaluator owns compilation/structural laws. Descriptions: Plan-only policy/waiver (no claimed Run/proof/program input); structural controls for missing bytes, reminted sidecars, resource bounds, exact selection, and unselected historical outputs. Not predicate truth, reconstruction, replay, or custody.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, parented at **v30**, JSON pointers `/files/7|13|211|278/description`. Candidate copies **before-text**. After the two host-fixture inserts (both after index 13), project by **stable filepath**:

| v30 pointer | Stable path | v31 pointer |
| --- | --- | --- |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/211/description` | `package.json` | **213** |
| `/files/278/description` | `schemas/sources/imported-v1.schema.json` | **280** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers (7, 13, 213, 280). Do not rewrite the current 28/41 lock during this review.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept source47, a new runtime, full first-evaluation structural admission, replay, or custody. Root assent and private activation of **this** record remain pending.
