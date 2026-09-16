# Coverage-producer inventory v17 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not source/code acceptance. Not capability-support-16 source. Advisory 17 / followup are **not** acceptance; their original bytes remain. Frozen/live/history not edited. Root remains lead.

Subject `docs/implementation/m2/coverage-producer-inventory-v17-subject.json` SHA-256 `89509a74b56842a2464f11d3d45fedf28a7d31b74e6dc2fc1f20614e459b22c2` (638 bytes). Three members pin-match: README `752010b6…9d15` / 1474, `successor.json` `97015809…bbf3` / 757, `repository-file-inventory.v17.json` 139302 bytes `cfa63f088f50c7a88bb8647792fa127b60c265df1882ae5f6081e669093b1e0f`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 16

Live lock: **14 inventory / 18 contract**. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v16.json` 138398 bytes SHA-256 `2da370ad759cf85e57d8f8881b5dca73d5d8d4a463d83dd6824298582b480438`

That is this unit’s `successor.parent`. Last contract is native-runtime v5. Capability-support layout is selected; `capability_support.rs` is **absent** from the live tree (private, not accepted). The two new v17 paths are absent from v16 and from live product.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 377 inherited rows | v16 has 377 unique sorted paths; all present in v17; **0 mutated** |
| 2 new files | identical to `successor.addedFiles`; none removed |
| 379 total | 377+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; identity → contracts only; evaluator → identity+contracts; **no identity→evaluator** |
| v16 path order | subsequence of v17 (insertions at evaluator `src/` indices 59–60) |
| row shape | `{description, generated, package, path, role, standing}` |

New rows, both `opensip-evaluator`:

| Path | Role | Naming |
| --- | --- | --- |
| `coverage.rs` | validator | snake_case, sibling of `capability_support.rs` / `plan_native.rs` |
| `coverage-registry.json` | registry, `generated: false` | kebab closed data, **not** `capability-support-registry.json` (prerequisites), **not** `native-plan-registry.json` (Plan requests), **not** `capability-registry.json` (release manifests) |

README matches the selected producer split: host-recomputed commitment/count, key/entry joins, bijection and deficiency/cause, optional source-path slice, registered schema identity; unresolved facts and dialect are host context. Distinct from the three post-admission prerequisites, view partition, inventory totality, graph/replay, and host DomainDetail presentation. Internal refusals/faults stay distinct from public codes. No caller ADMIT or Plan-count authority. No new crate, edge, or dependency TCB.

This layout does **not** accept Coverage source bytes or private-16 implementation.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v16**. v17 copies **before-text**, not after-text.

| v16 pointer | Stable path | v17 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/184/description` | `package.json` | **186** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created here. No Coverage producer source, capability-support-16 source, host presentation, or runtime claim.
