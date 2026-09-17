# Plan-input inventory v29 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** source45, **not** runtime20 acceptance, **not** full X/execution-input, **not** caller ADMIT, **not** full M2. Frozen/live/history not edited. Live **26/38** (runtime19) is the frozen base and is not mutated by this review. Root activates this layout **only after** runtime20. Root remains lead. Not Claude agreement.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142, line **109**) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the contract token (line **198**) and would be refused at inventory activation.

**subjectManifestSha256** `488f8363029e8fcbbcc3b5226829ca11a6995b079bea74d661dcfd74aa4e7cb3`  
`docs/implementation/m2/plan-input-inventory-v29-subject.json` **624** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `plan-input-inventory-v29/README.md` | 1102 | `4e3578b080383f98ba6657c73422f0f91281c6d99197276ce87d9445e46e38d8` |
| `plan-input-inventory-v29/successor.json` | 621 | `1c1fea78fcf7d0ca963552867e680a540d97c387d836e78290f54d8937b1c762` |
| `repository-file-inventory.v29.json` | 150565 | `0a255a7161519352e589069566fc5cafa3e59f1ef8ac0d3d33a0cc9f3ee2ffc0` |

Prompt (context only): 1112 / `e37449fdf4aca5ffc3948e59ab1a097a940aedb571de090f83633d561e042e28`.

## Checker (`inventory_successor` 85–143)

Successor record declares **both** required true flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v28, not the v28 successor **record**. Candidate pin matches disk. `same_reference` on this assessment uses candidate path+bytes+sha256, parent path+bytes+sha256, and successor-record path+sha256.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. One sorted unique addition; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate. `addedFiles` is the single new path.

## Parent is live inventory **candidate** 28

Live lock independently **26 inventory / 38 contract** (`77114` / `6f01a356d19644b6ab9f15429b2f553894882870df1adadd2a6eb23ecc0e2e73`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v28.json` **150007** / `b67c6101369e7ae76898c6997e5dae5f97bf9dc0c00f4a0ac3a1b923a4184240`

That is `successor.parent`. Last **contract** remains runtime **v19** (`native-runtime-selection-v19/successor.json` **17397** / `05be52901aab5df654394b5c1ee1e18fa08fa05499ae47c9a9994c30cfed7eff`). Runtime **v20** is **not** in the live contract list and is not a parent of this layout.

Live and architecture trees have **no** `plan-input-fixtures.json`. Existing evaluator owners remain inherited: `view_joins.rs`, `import_joins.rs`, `stage_output.rs` (**validator**), `lib.rs` (**public-api**). This layout does not add those files.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 400 inherited rows | v28 400 unique sorted paths; all present in v29; **0 mutated** |
| 1 new file | `crates/host/tests/fixtures/plan-input-fixtures.json`; none removed |
| 401 total | 400+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v28 path order | subsequence of v29 (insertion at host fixtures **125**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New row (`generated: false`, `standing: proposed`):

- `opensip-host` `crates/host/tests/fixtures/plan-input-fixtures.json` **fixture** (kebab, sibling of `plan-capability-fixture.json` / `evaluator-parameter-fixtures.json`). Pooled Plan-scoped view/import/stage packets with Run/proof output objects absent. Host owns fixture bytes; evaluator owns shared admission checks. Not full execution-input/replay/custody; not caller ADMIT maps.

Private trial fixture (not a subject member; **not** source45 approval) has **69** cases: **42** packet-named Plan-scoped owner-admitted results + **27** `plan-*` selection/missing/tamper/limit controls.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, all parented at **v28**, selectors `/files/7|13|206|273/description`. v29 copies **before-text** on those rows. `successor_chain` (312–346) projects by **stable filepath** after the additive insert at 125.

| v28 pointer | Stable path | v29 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/206/description` | `package.json` | **207** |
| `/files/273/description` | `schemas/sources/imported-v1.schema.json` | **274** |

No override dropped. Private activation (after runtime20) must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath (7, 13, 207, 274). Do not rewrite the current 26/38 lock during this review.

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept source45, runtime20, full X/execution-input selection, reconstruction, replay, or custody. Root assent and private activation of **this** record remain pending and must wait for runtime20.
