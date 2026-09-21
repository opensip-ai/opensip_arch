# Cumulative native inventory v55 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Parent is **selected inventory32**, not unselected 53/54. Not source 366/367/368 acceptance, not TCB, not runtime/source-policy, not five-member binding, not current authority, not writers, not M2–M6, not product installation. Inventories **33–54** remain frozen/unselected; this unit does **not** retroactively approve them. Frozen/live/history not edited. Root assent and live `inventory_successor` activation are **not** manufactured. Product remains `fa72e50`.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is **`ACCEPT`**. `ACCEPT-DESIGN-UNIT` is the contract token and would be refused. Those independent-review tokens are used here. The fifth pin (`assent`) remains root’s; this file is not that pin.

**subjectManifestSha256** `8da30746898d2b3f87b79f47147fdfabadc14ea49401a37b8cafd634f57fadcc`  
`docs/implementation/m2/cumulative-native-inventory-v55-subject.json` **640** B, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `cumulative-native-inventory-v55/README.md` | 2246 | `5d900f09ee13b514f5ba65ab36f42fdf832ba1c1c387f605823103f71464162e` |
| `cumulative-native-inventory-v55/successor.json` | 19428 | `34a8e089f173ea713c62017282f64d21636f6b11f9c8aa6a255ae9e6c8f33308` |
| `repository-file-inventory.v55.json` | 276439 | `093d0da499be1f96b47d4c146d45f04dd69af6fe216d4b72e64ea0e10e9c8e35` |

Prior 368 REVIEW `f03f5e31…da78` (5976 B, no addendum), 367 REVIEW/ADDENDUM, and 54 REVIEW/review.json (`NEEDS-CHANGES`, SHA `3ff38b0c…0292`) were read and are **unchanged**.

---

## Checker (`inventory_successor` 86–142) — logical five-pin

| Requirement | This unit |
| --- | --- |
| `parent` is a selected base input | **Yes** — live lock last candidate is v32 `105a260d…b72e` / 154945 B (30 successors) |
| candidate path ≠ parent | **Yes** |
| `record.parent` / `record.candidate` match those pins (with size) | **Yes** |
| `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` | **both true** (declared and independently observed) |
| packages / pendingDecisions equal parent | **Yes** — 20 packages/DAG; **9** pending-decision strings identical to v32 |
| sorted unique additions; inherited rows unmutated | **288** added; **0** mutated; **0** removed |
| independent review tokens | this file: `ACCEPT-UNIT` / assessment `ACCEPT` / `requiredFindings: []` |
| root `assent` | **not written**; activation **not** performed |

This is the 54-review fix: the missing flag is present, and the parent is selected32 rather than unselected53. Historical 54 subject/review remain `NEEDS-CHANGES` on disk.

---

## Candidate rows

| Claim | Check |
| --- | --- |
| 409 inherited from selected32 | all present; **0** mutated |
| 288 new files | exact `successor.addedFiles` |
| 697 total | 409+288 |
| Unselected54’s 693 rows | all present in v55 **by value**; plus **4** lineage paths |
| 20 packages / DAG | identical to v32 |
| 9 pending decisions | identical to v32 (not v54’s 11) |
| Frozen 368 | **583/583** product files listed; **0** unlisted; **114** planned future |
| Generated/tooling | five `generated: true` tables under `crates/security/src/generated/`; `tools/generate_security_tables.py` + helpers inherited as builder/schema/registry |

The four paths beyond unselected54: `installation_lineage.rs` (host composition), `lineage.rs` (lifecycle codec), `lineage/tests.rs`, `lineage-node367.json` (565-case fixture). Descriptions keep namespace/budget/authorization/native uniqueness **open**.

Entire **288** (not only those four): package split host 6 / lifecycle 6 / platform 13 / security 244 / storage 10 / tooling 9. Roles: fixture 134, validator 52, test 43, adapter 11, store 9, registry 8, service 7, composition 6, codec 5, builder 5, algorithm 4, module 2, schema 2. Trust-module extraction 60 remains **22** non-test + **38** `role: test` (including `admitted_recovery_proposals.rs` and `admitted_platform_decisions.rs`). Snake_case `.rs`; kebab `.json`; no `*_factory` rename.

---

## Unresolved obligations (not selected32 policy)

v54 had two extra `pendingDecisions` strings (origins 211/218). v55 does **not** add them to the selected nine. They are copied **verbatim** into `successor.unselectedObligationsCarried` with standing `UNRESOLVED; retained outside selected inventory policy, not discharged or activated by layout`. Independent match to v54’s extra pending entries: **true**. Not silently resolved or dropped.

---

## Description overrides

Four live `inventoryPassageInheritance` entries remain parented at **v32**. Stored rows equal v32 (lock `before` is the row text; lock `after` is selected meaning):

| v32 pointer | Stable path | v55 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/215/description` | `package.json` | **494** |
| `/files/282/description` | `schemas/sources/imported-v1.schema.json` | **561** |

Activation must rewrite inheritance parent to this candidate and project those four pointers by filepath.

---

## requiredFindings

None.

---

## Scope / limits

No product files created. Does not accept 366/367/368 algorithms, native 368 qualification, unselected 33–54, five-member store binding, current authority, writers, or M2–M6. Does not install this inventory. Root assent on this exact subject remains required before activation.
