# Stage-output inventory v21 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not runtime acceptance, not editable source-26 approval, not stage-meta re-selection. Root remains lead. Root assent and private activation are still required.

**subjectManifestSha256** `9fe900c5583188d9f070525bbfb596341912aa53fb3838b04e242dba76790787`  
`docs/implementation/m2/stage-output-inventory-v21-subject.json` **627** bytes, 3 members pin-match, paths sorted unique.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `repository-file-inventory.v21.json` | 141841 | `617efcc566387945dc619e26768874330094f769fa3b7d973cacd8dfca0014f6` |
| `stage-output-inventory-v21/README.md` | 931 | `6483e26ff9204bf5e6cf3aeb6f5341c252f39346f6f1bde14e0b40afab47c5e6` |
| `stage-output-inventory-v21/successor.json` | 606 | `6fd448ee8261f483fe680c550fc6c742b22981aeadb45ce933f167906d590787` |

## Checker (`verify_design.py` inventory_successor 85–143)

Live `tools/verify_design.py` `inventory_successor` refuses unless the successor record has **both** `parentArtifactBytesUnchanged is True` **and** `inheritedRowsEqualByValue is True` (106–107). It then joins review `verdict`/`requiredFindings`, `inventoryCandidateAssessment` candidate/parent/`successorRecord` pins (108–113), and later root assent (114–120), and checks sorted unique additions with inherited rows equal by value (137–140). `same_reference` on the assessment requires candidate path/bytes/sha256 (`size=True`), parent path/bytes/sha256 (`size=True`), and successor record path/sha256.

This successor record declares **both** required true flags. Parent pin is the live inventory **candidate** v20, not the v20 successor **record**. Candidate pin matches disk. Added files are the singleton `crates/evaluator/src/stage_output.rs`.

## Parent is live inventory **candidate** 20

Live lock independently **18 inventory / 27 contract** (`4cb0f20f504c812ad07dc55d07db59ada4809ebcfbc9e4d1b990cce0bd4310b9` / 57141). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v20.json` 141292 / `321f3da752bc0a900c2829ce217f955daf699e60df66596f62c7ef6c2270f5a7`

That is `successor.parent`. Last contract is **stage-meta-reference-selection-v1** (`129bceca5f8e27cf3e14377453f8688b4169dd7b65aef1519f2bbdffc6880cb5` / 10621). Runtime **v12** is already in the contract chain (`8bf96d5858ef72010dcdfc9b667f584d4ae93b42b1478de63f9be5117dc379de` / 10426). Live tree has no `stage_output.rs`.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 383 inherited rows | v20 383 unique sorted paths; all present in v21; **0 mutated** (row objects equal) |
| 1 new file | `crates/evaluator/src/stage_output.rs`; none removed |
| 384 total | 383+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; evaluator still depends on contracts+identity (not reverse); no new package/edge |
| v20 path order | subsequence of v21 (insertion at evaluator `src/` index **76**) |
| packaging flags | both required true flags present |

New row: `opensip-evaluator`, `role` validator, snake_case `stage_output.rs` matching sibling validators `run_links.rs` / `view_joins.rs`, `generated: false`, `standing: proposed`. Description: recheck retained derivation-stage specifications against Plan selection, declared parameters and output domains; verify provider-owned schema tree registration and the selected portable structural meta-schema profile; inert diagnostics. Explicitly not regex compilation, instance validation, full Run admission, or replay authority.

Inherited sibling roles unchanged: `run_links.rs`/`view_joins.rs` validator; `proofs.rs` builder; `budgets.rs`/`atoms.rs` algorithm; `policy.rs` compiler.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v20**. v21 copies **before-text**. `successor_chain` (312–346) projects by **stable filepath** after additive inserts, because sorted additions shift indexes.

| v20 pointer | Stable path | v21 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/190/description` | `package.json` | **191** |

Private activation must rewrite the lock inheritance parent to this candidate and project **all three** pointers by filepath (`package.json` → `/files/191/description`).

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Editable source-26 is a separate private draft and is **not** accepted here. Stage-meta-reference-v1 remains the selected contract; this unit does not re-select it. No identity API change, no caller ADMIT, no Run/replay. Root assent and private activation of **this** record remain pending.
