# View-joins inventory v18 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not source/code acceptance. Advisory 18 is **not** acceptance. Frozen/live/history not edited. Root remains lead.

Subject `docs/implementation/m2/view-joins-inventory-v18-subject.json` SHA-256 `f7376661cec2e392143588e320c32fa9126e4fd8722ee1b0d7214f0cf7024001` (624 bytes). Three members pin-match: `repository-file-inventory.v18.json` 140296 / `3bc6f5b2540c507bec43987aee188253b0b7e078c309631dd90c5dc447b5b025`, README `2207908d…6ceb` / 1675, `successor.json` `57346480…1b5b` / 753. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 17

Live lock: **15 inventory / 19 contract**. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v17.json` 139302 bytes SHA-256 `cfa63f088f50c7a88bb8647792fa127b60c265df1882ae5f6081e669093b1e0f`

That is this unit’s `successor.parent`. Last contract is native-runtime v6. Coverage-producer layout is selected; `coverage.rs` is **absent** from the live tree (private source). The two new v18 paths are absent from v17 and from live product.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 379 inherited rows | v17 has 379 unique sorted paths; all present in v18; **0 mutated** |
| 2 new files | identical to `successor.addedFiles`; none removed |
| 381 total | 379+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; identity → contracts only; evaluator → identity+contracts; **no identity→evaluator** |
| v17 path order | subsequence of v18 (insertions at evaluator `src/` indices 75–76) |
| row shape | `{description, generated, package, path, role, standing}` |

New rows, both `opensip-evaluator`:

| Path | Role | Naming |
| --- | --- | --- |
| `view_joins.rs` | validator | snake_case, sibling of `coverage.rs` / `capability_support.rs` |
| `view-joins-registry.json` | registry, `generated: false` | kebab closed extract of partition/totality/ladder/closure-kind rows; **not** caller partition keys, **not** `coverage-registry.json` / `capability-support-registry.json` |

README matches the selected per-view split: retained **run/view ids** so Plan/snapshot/evidence are **rehashed**, not caller inventories or universe rows as authority; unresolved bag is **this view**; actual producer then three guards then totality; diagnostic `ViewJoinChecks`, not ADMIT or Plan-count tokens. Explicit registry extract is justified: current identity API has no arbitrary selected-document getter; extract avoids a reverse identity edge. Walk, proof-root census, Plan/native, policy/stages/findings/imports, replay, and public routing stay other owners. No new crate, edge, or dependency TCB.

This layout does **not** accept view-joins source bytes or Coverage-17 implementation.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v17**. v18 copies **before-text**, not after-text.

| v17 pointer | Stable path | v18 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/186/description` | `package.json` | **188** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created here. No view-joins source, Coverage-17 source, proof census, or runtime claim.
