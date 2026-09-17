# Execution-input inventory v30 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** source46, **not** runtime acceptance, **not** full first-evaluation X/structural closure, **not** caller ADMIT, **not** full M2. Frozen/live/history not edited. Root remains lead. Not Claude agreement.

Live `inventory_successor` admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the contract token and would be refused at inventory activation.

**subjectManifestSha256** `df15517698295a578fe89fb9274fa2ef9807334fe909a71bbe13f3003047443b`  
`docs/implementation/m2/execution-input-inventory-v30-subject.json` **634** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `execution-input-inventory-v30/README.md` | 1184 | `6125c390ab06eaf222dd9d10a6bf6a0dae094c2f566c718cf2484201a96ee9a8` |
| `execution-input-inventory-v30/successor.json` | 774 | `68e4dee5fd7522bb3e45709e7313ecc6e8cfc321302e9de460a1e74d1d01396e` |
| `repository-file-inventory.v30.json` | 152687 | `487c36323deb7235453b1f22f55192d273b6f67c7143010d5a9a156c051aa6fd` |

## Checker

Successor declares both required flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v29, not the v29 successor **record**. Candidate pin matches disk.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. Four sorted unique additions; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate. `addedFiles` matches those four paths.

## Parent is live inventory **candidate** 29

Live lock independently **27 inventory / 40 contract** (`80032` / `569fd1914366490c2c385f41061ba27a475e3e6606caa2e9a4cd8f26bf81edf6`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v29.json` **150565** / `0a255a7161519352e589069566fc5cafa3e59f1ef8ac0d3d33a0cc9f3ee2ffc0`

That is `successor.parent`. Last **contract** is accepted runtime **v21** (`native-runtime-selection-v21/successor.json` **16475** / `8c005e680b223c604a51f2f8cff31021fabb7c306f9bcb417333ec8cd7bac99b`).

Live and architecture product trees have **none** of the four new paths. Inherited evaluator owners remain: `lib.rs` (**public-api**), `view_joins.rs` / `import_joins.rs` / `stage_output.rs` (**validator**), `native_owner_tests.rs` (**test**). This layout does not add `lib.rs`; wiring the bounded entry is source/runtime work, not this unit.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 401 inherited rows | v29 401 unique sorted paths; all present in v30; **0 mutated** |
| 4 new files | listed below; none removed |
| 405 total | 401+4 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v29 path order | subsequence of v30 (evaluator inserts at **66–68**, host fixture at **123**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New rows (`generated: false`, `standing: proposed`):

| Path | Package | Role |
| --- | --- | --- |
| `crates/evaluator/src/execution-registry.json` | opensip-evaluator | registry |
| `crates/evaluator/src/execution_inputs.rs` | opensip-evaluator | source |
| `crates/evaluator/src/execution_reader.rs` | opensip-evaluator | source |
| `crates/host/tests/fixtures/execution-input-fixtures.json` | opensip-host | fixture |

Naming: snake modules beside `enumeration_join.rs`; kebab registry beside `enumeration-registry.json`; kebab fixture beside `plan-input-fixtures.json` / `enumeration-join-fixtures.json`. Kernel vs reader split is the stated review boundary. Host owns fixture bytes; evaluator owns admission logic. Descriptions forbid caller ADMIT maps, Run/replay/publication authority, and ambient-store census. Not full first-evaluation structural closure.

Private 46 work exists under `/tmp` and is **not** a subject member; this review does not accept it.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, all parented at **v29**, JSON pointers `/files/7|13|207|274/description` (0-based array indices). Candidate copies **before-text** on those rows. After the four inserts, `successor_chain` must project by **stable filepath**:

| v29 pointer | Stable path | v30 pointer |
| --- | --- | --- |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** (unchanged; inserts are after 13) |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/207/description` | `package.json` | **211** |
| `/files/274/description` | `schemas/sources/imported-v1.schema.json` | **278** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath (7, 13, 211, 278). Do not rewrite the current 27/40 lock during this review.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept source46, a new runtime, full X/execution-input selection, reconstruction, replay, or custody. Kernel/reader/registry/fixture are bounded execution diagnostics only. Root assent and private activation of **this** record remain pending.
