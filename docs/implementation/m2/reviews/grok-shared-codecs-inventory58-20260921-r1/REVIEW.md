# Shared store codecs inventory v58 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. Parent is **selected inventory57** (live lock last inventory candidate; **33** successors). Adds four planned identity alloc-only store-syntax modules. Does **not** accept source384/385, select S9.3 or full binding, add DAG edges, move native orchestration into identity, or qualify a platform. Frozen/live/history not edited. Root assent is **not** manufactured.

Live `inventory_successor` (`tools/verify_design.py` 86–142) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is **`ACCEPT`**. Those tokens are used here. The fifth pin (`assent`) remains root’s.

**subjectManifestSha256** `29c55690b025e571e9c778b49bad0b6ec66b32d608cc409d32e47bbe73c679a9`  
`docs/implementation/m2/shared-store-codecs-inventory-v58-subject.json` **643** B, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `repository-file-inventory.v58.json` | 280320 | `f6c3c307332bf6bf04994b2ecbf3f2796465587fcd3e9d4c5e6042e13c5d5806` |
| `shared-store-codecs-inventory-v58/README.md` | 1426 | `9fbf7037b1725eff7d39324180ce21dbe1f79ec29c72d0a96067ae4269147f5c` |
| `shared-store-codecs-inventory-v58/successor.json` | 1852 | `5d985e23cdc388b9e32157eb92dab9198d9170313d6a4adea44be746a2b415fe` |

---

## Checker (`inventory_successor` 86–142) — logical five-pin

| Requirement | This unit |
| --- | --- |
| `parent` is a selected base input | **Yes** — live last candidate v57 `f16422c6…eb1e` / **278524** B |
| candidate path ≠ parent | **Yes** |
| `record.parent` / `record.candidate` match those pins (with size) | **Yes** |
| `parentArtifactBytesUnchanged` and `inheritedRowsEqualByValue` | **both true** (declared and independently observed) |
| packages / pendingDecisions equal parent | **Yes** — 20 packages/DAG; **9** pending-decision strings identical to v57 |
| sorted unique additions; inherited rows unmutated | **4** added; **0** mutated; **0** removed |
| independent review tokens | this file: `ACCEPT-UNIT` / assessment `ACCEPT` / `requiredFindings: []` |
| root `assent` | **not written**; activation **not** performed |

Standing text may differ (v57 directory-observation caption → v58 shared-store-syntax caption). Checker excludes `standing`/`files` from policy equality.

---

## Candidate rows

| Claim | Check |
| --- | --- |
| 701 inherited from selected57 | all present; **0** mutated |
| 4 new files | exact `successor.addedFiles`, lexicographic |
| 705 total | 701+4 |
| 20 packages / DAG | identical to v57; identity depends only on contracts; security still contracts/evaluator/identity/platform |
| identity → lifecycle/storage | **none** |
| security → lifecycle/storage | **none** |
| 9 pending decisions | identical to v57 |
| identity `lib.rs` inventory row | **unchanged by value** (index 149) |
| std feature | **none** on packages |
| helper384 path | **not added** |

Added (all `package: opensip-identity`, `role: codec`, `generated: false`, `standing: proposed`):

| Path | Responsibility |
| --- | --- |
| `store_identity.rs` | shared 32-hex store-instance spelling; no FS/selection/authority |
| `store_selection.rs` | alloc-only `selection.pair` (4096 bound, five members); native capture elsewhere |
| `store_lineage.rs` | alloc-only full-triple lineage keys / 4096-byte node / bounded inspect; OS-path stays in lifecycle |
| `store_marker.rs` | pure 128-byte store-instance marker + expected-ID compare; storage keeps native capture |

Filenames are consistent `store_*` codecs in identity, paired with existing owners: lifecycle `selection.rs` / `lineage.rs` / `locations.rs` remain facade/native/OS-path; storage `store_root.rs` and `native_marker.rs` remain native capture. Tests `lifecycle/src/lineage/tests.rs` and the **565-case** fixture `lifecycle/tests/fixtures/lineage-node367.json` stay in lifecycle. Inherited those rows are byte-equal v57 (indices shift +4 after the identity insert at 157–160).

---

## Description overrides

Four live `inventoryPassageInheritance` entries are parented at **selected v57**. Stored inherited rows equal v57 (and lock `before`) by stable path. Inserting the four identity files shifts later indices only:

| Stable path | v57 index | v58 index |
| --- | ---: | ---: |
| `apps/cli/src/bootstrap.rs` | 7 | **7** |
| `apps/report/package.json` | 13 | **13** |
| `package.json` | 498 | **502** |
| `schemas/sources/imported-v1.schema.json` | 565 | **569** |

Activation must rewrite inheritance parent to this candidate and project those four pointers by filepath (`verify_design.py` 312–346). Stored row descriptions are not rewritten by this unit.

---

## Unresolved obligations (not selected57 policy)

v57 carried two extra pending-decision strings (origins 211/218). v58 copies them **verbatim** into `successor.carriedUnresolvedObligations` with standing `UNRESOLVED; retained outside selected inventory policy, not discharged or activated by layout`. Independent match to v57 texts/standing/origin: **true**. Not added to the selected nine. Not silently resolved or dropped.

---

## Author 385 / helper 384 (not this unit)

README cites private 385 **56** identity / **32** lifecycle / **96** storage tests, including original lineage-fixture bytes. Those author results **explain proposed use** and are **not** independent source acceptance, S9.3, full binding, current authority, or qualification. Source384/385 remain unreviewed; source review joins the next exact formal runtime package after this layout. Native project helper384 adds **no** inventory path.

---

## requiredFindings

None.

---

## Scope / limits

Does not install product, accept 384/385 source, grant writers, or close M2–M6. Live lock at review time: **33** inventory (v57) / **50** contract (runtime28 last). This layout does not re-judge runtime28. No Claude concurrence. Root remains lead.
