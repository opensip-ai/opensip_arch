# Run-links inventory v19 — corrected packaging layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Not runtime acceptance, not source/code acceptance, not approval of the original v19 successor record. Frozen original subject/successor/review bytes are **not** patched. Root remains lead. Root assent and private activation are still required.

**subjectManifestSha256** `cfdff847fcb876c0db0c7f40d82263aeb5fb38952feec947a41de89f9f621dd6`  
`docs/implementation/m2/run-links-inventory-v19-corrected-subject.json` **641** bytes, 3 members pin-match, paths sorted unique.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `repository-file-inventory.v19.json` | 140780 | `ec61d2fbee9e6fdd6000acabe263d2c455f71055b6e8843e5c973351fe9c9725` |
| `run-links-inventory-v19-corrected/README.md` | 782 | `d7dc2931479c9c84f2eaa9aa511749e41624547463eb68b7332be34641155393` |
| `run-links-inventory-v19-corrected/successor.json` | 756 | `7970af1812f001a68094aea80c6389cfe787a235d6d4a348e7f289f6747b5b82` |

## Why a new record

Selected `tools/verify_design.py` `inventory_successor` (85–143) refuses unless the successor record has **both** `parentArtifactBytesUnchanged is True` **and** `inheritedRowsEqualByValue is True` (106–107). It then joins review `verdict`/`requiredFindings`, `inventoryCandidateAssessment` candidate/parent/`successorRecord` pins (108–113), and root assent (114–120), and checks sorted unique additions with inherited rows equal by value (137–140).

Original `run-links-inventory-v19/successor.json` **566** / `52ace802…3174` has `parentArtifactBytesUnchanged: true` and **omits** `inheritedRowsEqualByValue`. Original independent ACCEPT-UNIT (`f3f24f73…1b75` / 621; review `312a55f1…9bb2` / 3793) and root `ACCEPTED-UNIT` missed that packaging field. Private `verify_design` refused **before** any live write (live inventory still 16). Those original bytes are preserved and are **not** this unit’s `successorRecord`.

This corrected record adds `inheritedRowsEqualByValue: true`. Candidate v19 **bytes unchanged**.

## Parent is live inventory **candidate** 18

Live lock independently **16 inventory / 21 contract** (`63e0e8de…766a` / 49399). Last inventory **candidate** (not the successor *record*):

`docs/implementation/m2/repository-file-inventory.v18.json` 140296 / `3bc6f5b2540c507bec43987aee188253b0b7e078c309631dd90c5dc447b5b025`

That is the corrected `successor.parent`. Last contract is runtime v8. `run_links.rs` is absent from the live tree.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 381 inherited rows | v18 381 unique sorted paths; all present in v19; **0 mutated** (row objects equal) |
| 1 new file | `crates/evaluator/src/run_links.rs`; none removed |
| 382 total | 381+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no identity→evaluator; no new package/edge |
| v18 path order | subsequence of v19 (insertion at evaluator `src/` index **74**) |
| packaging flags | `parentArtifactBytesUnchanged: true` and `inheritedRowsEqualByValue: true` |

New row: `opensip-evaluator` validator, snake_case `run_links.rs`, `generated: false`. Description: separate **pre-native** Run root/config/grant/VCS joins and **later** proof-selected view/coverage/finding evidence roots; not full walk, predicate addressing, policy/stage/import, or replay. Source 19 is **not** accepted here.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v18**. v19 copies **before-text**.

| v18 pointer | Stable path | v19 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/188/description` | `package.json` | **189** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created here. Original v19 successor/subject/review not rewritten. No run-links source, caller ADMIT, or Run/replay claim. Root assent and private activation of **this** corrected record remain pending.
