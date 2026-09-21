# Pure registry codec inventory v56 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Parent is **selected inventory55** (live lock last candidate; 31 successors), not unselected 33–54. Not source 373/374 acceptance, not runtime26, not TCB, not five-member binding, not current authority, not writers, not M2–M6, not product installation. Frozen/live/history not edited. Root assent and live `inventory_successor` activation are **not** manufactured.

Live `inventory_successor` (`tools/verify_design.py` 86–142) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is **`ACCEPT`**. Those tokens are used here. The fifth pin (`assent`) remains root’s.

**subjectManifestSha256** `b6ce51e260aa2d7cb5e139be23c8229e46bc8bed9f56d97ad71101ac2e6902fb`  
`docs/implementation/m2/project-registry-inventory-v56-subject.json` **637** B, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `project-registry-inventory-v56/README.md` | 1283 | `18e89b35389056291f61e4da05aa5da58e15156e025820ba5a82a52c448c7a83` |
| `project-registry-inventory-v56/successor.json` | 1763 | `1b36f755f54a0c4b0e357d33fc51642976f664058ed24a7c6ff4d7f9663513e4` |
| `repository-file-inventory.v56.json` | 277494 | `8935bf9d1f02a7486feba7250586c6d3e0ab8ad4e029d9f4b8571a74b2d8786c` |

Prior inventory55 REVIEW `14ef27a6…7bc9` / review.json `9c7d41f5…0292` and 373/374 reviews in sibling folders were read and are **unchanged**.

---

## Checker (`inventory_successor` 86–142) — logical five-pin

| Requirement | This unit |
| --- | --- |
| `parent` is a selected base input | **Yes** — live lock last candidate is v55 `093d0da4…8e35` / 276439 B (31 successors) |
| candidate path ≠ parent | **Yes** |
| `record.parent` / `record.candidate` match those pins (with size) | **Yes** |
| `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` | **both true** (declared and independently observed) |
| packages / pendingDecisions equal parent | **Yes** — 20 packages/DAG; **9** pending-decision strings identical to v55 |
| sorted unique additions; inherited rows unmutated | **2** added; **0** mutated; **0** removed |
| independent review tokens | this file: `ACCEPT-UNIT` / assessment `ACCEPT` / `requiredFindings: []` |
| root `assent` | **not written**; activation **not** performed |

---

## Candidate rows

| Claim | Check |
| --- | --- |
| 697 inherited from selected55 | all present; **0** mutated |
| 2 new files | exact `successor.addedFiles` |
| 699 total | 697+2 |
| 20 packages / DAG | identical to v55; identity still depends only on contracts; security still contracts/evaluator/identity/platform |
| 9 pending decisions | identical to v55 |
| identity `lib.rs` inventory row | **unchanged by value**; export-only content change is the 374 source candidate, not this layout row |

Added: `crates/identity/src/project_registry.rs` (`role: codec`) and `crates/identity/src/project_registry_tests.rs` (`role: test`). Descriptions state complete-document/marker syntax only; no filesystem, registration, entropy, leases, mutation, recovery, or authority.

---

## Description overrides

Four live `inventoryPassageInheritance` entries are parented at **selected v55**. Stored inherited rows equal v55 (and lock `before`) by stable path. Inserting the two identity files shifts later indices only:

| Stable path | v55 index | v56 index |
| --- | ---: | ---: |
| `apps/cli/src/bootstrap.rs` | 7 | **7** |
| `apps/report/package.json` | 13 | **13** |
| `package.json` | 494 | **496** |
| `schemas/sources/imported-v1.schema.json` | 561 | **563** |

Activation must rewrite inheritance parent to this candidate and project those four pointers by filepath (`verify_design.py` 312–346). Stored row descriptions are not rewritten by this unit.

---

## Unresolved obligations (not selected55 policy)

v55 carried two extra pending-decision strings (origins 211/218). v56 copies them **verbatim** into `successor.carriedUnresolvedObligations` with standing `UNRESOLVED; retained outside selected inventory policy, not discharged or activated by layout`. Independent match to v55 `unselectedObligationsCarried` texts/standing/origin: **true**. Not added to the selected nine. Not silently resolved or dropped.

---

## requiredFindings

None.

---

## Scope / limits

No product files created. Does not accept 373 codec law, 374 public exports/tests, runtime26, unselected 33–54, five-member store binding, current authority, writers, or M2–M6. Does not install this inventory. Root assent on this exact subject remains required before activation. Root will separately perform the runtime26 formal join after actual review.
