# Trust-modules inventory v54 — additive cumulative layout review

**Verdict: `NEEDS-CHANGES`**

Layout packaging only. Not source 366/367 acceptance, not runtime/source-policy, not TCB, not five-member binding, not current authority, not writers, not M2–M6, not product installation. This unit **does not** accept unselected inventories 33–53. Frozen/live/history not edited. Source **367** (lifecycle reader) is outside this review. No native tests. Root remains lead. Not Claude agreement.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. `ACCEPT-DESIGN-UNIT` is the contract token and would be refused at inventory activation. This record is **not** that acceptance: the successor JSON omits a required preservation flag.

**subjectManifestSha256** `55ea8c216525a9482901469a727be2cc692f1267a7bcb26bf8ec982a750d1f7a`  
`docs/implementation/m2/trust-modules-inventory-v54-subject.json` **631** B, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `repository-file-inventory.v54.json` | 275021 | `c282d92b35c5c829b7bcaef9e3f2bd7df728f3842ded4e998fe5912d67cbb399` |
| `trust-modules-inventory-v54/README.md` | 2464 | `0030ca105364464017fbce10914faf69eff41c5ae83a16a12756f7b6b6289e98` |
| `trust-modules-inventory-v54/successor.json` | 4400 | `354f73e649a5a3a9f875bf70404e54ac29340761d74fc308e7b06099af59594e` |

Prior 366 REVIEW `0d875631…dcf5`, 365 REVIEW `0d1e8a10…9f57`, 364 REVIEW `d93e0f3f…4f37`, ADDENDUM `39e812a1…5eac`, and CORRECTION-REVIEW `0a65bc79…b1d7` were read and are **unchanged**.

---

## Checker (`inventory_successor` 85–143)

Successor parent pin is unselected **v53 candidate** `b3f96d6a…100d` / 248598 B, not the v53 successor **record**. Candidate pin matches disk. Selected ancestor pin is live inventory **v32** `105a260d…b72e` / 154945 B.

`inheritedRowsEqualByValue` is **true** and independently verified (633 inherited rows equal by value; 0 mutated; 0 removed). `packageDependencyGraphUnchanged` and `pendingDecisionsInheritedUnchanged` are true (20 packages, 11 pending decisions, identical to v53 and v52).

`parentArtifactBytesUnchanged` is **absent**. Parent artifact bytes **are** independently unchanged. Live checker line 106 still requires the declared flag. Parent **v53** successor.json has that flag; v54 dropped it.

Live lock last inventory successor remains **v32** (30 inventory successors). v53 is not a selected base input, so this record cannot activate against the live lock even after the flag is added, until 33–53 are separately accepted.

---

## Candidate rows

| Claim | Check |
| --- | --- |
| 633 inherited from 53 | all present; **0** mutated |
| 60 new files | exact `successor.addedFiles`; all under `crates/security/src/trust/`; none removed |
| 693 total | 633+60 |
| 20 packages / DAG | identical to v53 and v52 |
| 11 pending decisions | identical to v53 and v52 |
| Frozen 366 | **579/579** product files listed; **0** unlisted; **114** planned future (same 114 as v53 vs 365, plus the 60 new which 366 contains) |
| Selected 32 | 409 rows; cumulative delta **284** paths; **0** selected rows removed or mutated |
| Generated/tooling | 14 generated tables + `tools/generate_security_tables.py` and helpers **inherited unchanged**; none of the 60 new rows is `generated: true` |
| Naming | all 60 are snake_case `.rs`; no kebab JSON added; no `*_factory.rs` rename |

Inventory roles on the 60 additions: **22** non-test (18 `validator` + `codec` `metadata.rs` + `store` `retained_metadata_index.rs` + `algorithm` `retained_trust_graph.rs` + `composition` `root_payload.rs`) and **38** `role: test`. Filename-only split is 24/36 because `admitted_recovery_proposals.rs` and `admitted_platform_decisions.rs` are test helpers without `_tests` suffix: inventory `role: test`; `root_payload.rs` declares `mod … { include!(…) }` then `#[cfg(test)] use …`. That matches the 366 source account. Descriptions keep codec / root-envelope / retained graph / recovery / profile-revocation owners separate. Existing `ordinary_targets.rs` and other retained files are not re-owned.

`trust.rs` inherited row is **byte-equal** to v53 (`role: validator`, composition entry). README’s 8KB note is prose, not a row rewrite.

---

## Cumulative ancestors (not acceptance)

| Inventory | Rows | This review |
| --- | ---: | --- |
| Selected **v32** | 409 | live lock; four description overrides parent here |
| Unselected **v52** | 470 | parent of 53; 52→53 rows equal by value (**163** added); **not** accepted here |
| Unselected **v53** | 633 | parent of 54; 53→54 rows equal by value; **no** independent 53 `ACCEPT-UNIT` is claimed or faked |
| Proposed **v54** | 693 | this unit |

Inventories **33–53** keep unselected standing. `composition-inventory-v33` and `repository-file-inventory.v33.json` still exist; scratch inventory33-draft did not overwrite them. v53 README’s 470+163 accounting matches disk. This review does **not** treat 33–53 as approved layout units.

Four live `inventoryPassageInheritance` entries remain parented at **v32** and still project by **stable filepath** (lock `before` equals the inherited row text; lock `after` is selected meaning, not stored in the row):

| v32 pointer | Stable path | v53 index | v54 index |
| --- | --- | ---: | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 | **7** |
| `/files/13/description` | `apps/report/package.json` | 13 | **13** |
| `/files/215/description` | `package.json` | 430 | **490** |
| `/files/282/description` | `schemas/sources/imported-v1.schema.json` | 497 | **557** |

All four rows equal v32 by value. No override dropped. Activation of any later selected inventory must rewrite inheritance parent and project these four pointers by filepath.

---

## requiredFindings

1. `trust-modules-inventory-v54/successor.json` omits `parentArtifactBytesUnchanged: true`. `tools/verify_design.py` `inventory_successor` (106–107) requires both that flag and `inheritedRowsEqualByValue`. Parent v53 bytes are independently unchanged (`248598` / `b3f96d6a…100d`); the declaration is still missing. Parent unit `native-trust-inventory-v53/successor.json` declares the flag.

---

## Scope / limits

No product files created. Does not accept 366 algorithms, 367 lifecycle reader, native validation recipe, five-member store binding, current authority, writers, platform qualification, or M2–M6. Does not activate inventory. Remaining `trust.rs` / already-external owners are not a claim that all future splits are known. Root assent remains pending after the successor flag is present.
