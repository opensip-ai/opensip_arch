# Import-joins inventory v22 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not runtime acceptance, not editable source-27 approval, not stage-output-26 re-acceptance. Root remains lead. Root assent and private activation are still required.

**subjectManifestSha256** `a9471098e7651a74d3b580141016854d18c6b1e6645fa04e9ccf1e4b02727267`  
`docs/implementation/m2/import-joins-inventory-v22-subject.json` **628** bytes, 3 members pin-match, paths sorted unique.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `import-joins-inventory-v22/README.md` | 1052 | `0767dc57724ec04a4354588bc6709e37ad54739f8233a78a65f046a55c3b95b1` |
| `import-joins-inventory-v22/successor.json` | 716 | `84cd736d37aa0d329f0e06e00da9f54e3b551c6eb1c27f993434acde542b3dcd` |
| `repository-file-inventory.v22.json` | 143331 | `f13eed68a5c70f58b3571e4712657a64702ed3522affeed7852afff1b1722376` |

## Checker (`verify_design.py` inventory_successor 85–143)

Live `tools/verify_design.py` `inventory_successor` refuses unless the successor record has **both** `parentArtifactBytesUnchanged is True` **and** `inheritedRowsEqualByValue is True` (106–107). It then joins review `verdict`/`requiredFindings`, `inventoryCandidateAssessment` candidate/parent/`successorRecord` pins (108–113), and later root assent (114–120), and checks sorted unique additions with inherited rows equal by value (137–140). `same_reference` on the assessment requires candidate path/bytes/sha256 (`size=True`), parent path/bytes/sha256 (`size=True`), and successor record path/sha256.

This successor record declares **both** required true flags. Parent pin is the live inventory **candidate** v21, not the v21 successor **record**. Candidate pin matches disk. Added files are the sorted triple `crates/evaluator/src/import-registry.json`, `crates/evaluator/src/import_joins.rs`, `crates/host/tests/fixtures/import-joins-fixtures.json`.

## Parent is live inventory **candidate** 21

Live lock independently **19 inventory / 28 contract** (`f1d12e90731ce9b0c4dec0f51bf446c85a14b8058d0248c299676b9f9c11ae74` / 59148). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v21.json` 141841 / `617efcc566387945dc619e26768874330094f769fa3b7d973cacd8dfca0014f6`

That is `successor.parent`. Last contract is runtime **v13** (`454f88352059c2e370b83aaebbb33366d0e95027af4a22ccf99ce9fe42823216` / 10918). Runtime **v12** and **stage-meta-reference-v1** remain in the contract chain. Live tree has `stage_output.rs` and **no** `import_joins.rs` / `import-registry.json` / `import-joins-fixtures.json`. Planned `crates/host/src/imports.rs` is also absent from live; its inherited inventory row remains `role` service (I/O).

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 384 inherited rows | v21 384 unique sorted paths; all present in v22; **0 mutated** (row objects equal) |
| 3 new files | registry + `import_joins.rs` + host fixture; none removed |
| 387 total | 384+3 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; evaluator still depends on contracts+identity (not reverse); no new package/edge |
| v21 path order | subsequence of v22 (insertions at evaluator `src/` **64–65** and host fixtures **111**) |
| packaging flags | both required true flags present |

New rows (`generated: false`, `standing: proposed`):

- `opensip-evaluator` **registry** `import-registry.json` (kebab, sibling of `coverage-registry.json` / `view-joins-registry.json`). Description: closed parameter-row names, document/selector/digest bindings and evaluator-required flags derived from selected identity schema/admission sources; not caller-selected.
- `opensip-evaluator` **validator** `import_joins.rs` (snake_case, sibling of `run_links.rs` / `view_joins.rs` / `stage_output.rs`). Description: retained import source correspondence, snapshot/source-map digests, VCS/build consumability and global analysis parameter selection; inert diagnostics; not evidence acquisition, imported payload execution, full Run, or replay.
- `opensip-host` **fixture** `import-joins-fixtures.json` (kebab, sibling of `native-context-fixtures.json`). Description: separate bounded cases so each hostile-input parser stays within the existing per-document 4 MiB limit; does not relax production limits.

Inherited `crates/host/src/imports.rs` remains `role` service. Identity `lib.rs` / `Cargo.toml` inherited equal; no new identity API or identity→evaluator edge. Live `native-context-fixtures.json` is still **3736129** bytes under `MAX_BYTES = 4 * 1024 * 1024`; that inventory row is unchanged.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v21**. v22 copies **before-text**. `successor_chain` (312–346) projects by **stable filepath** after additive inserts.

| v21 pointer | Stable path | v22 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/191/description` | `package.json` | **194** |

Private activation must rewrite the lock inheritance parent to this candidate and project **all three** pointers by filepath (`package.json` → `/files/194/description`).

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Editable source-27 is a separate private draft and is **not** accepted here. Frozen stage-output-26 source/runtime units remain separate. No identity API change, no caller ADMIT, no Run/replay. Root assent and private activation of **this** record remain pending.
