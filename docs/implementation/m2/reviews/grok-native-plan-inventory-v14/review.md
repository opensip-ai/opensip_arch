# Native-plan inventory v14 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not a dependency or unsafe-TCB selection. Does not accept source extraction from `native_universe.rs` or new Plan-join behavior. Frozen/live/history not edited. Root remains lead. Root writes native Plan next; retention source is a separate advisory.

Subject `docs/implementation/m2/native-plan-inventory-v14-subject.json` SHA-256 `9c23e1d164c083610ded4f23bd0c2d1fa1980bd415673037dc6f30c96ce97848` (626 bytes). Three members pin-match: README `95bea66b…0783` / 1333, `successor.json` `2076595c…1c90` / 825, `repository-file-inventory.v14.json` 136672 bytes `20bd2bd4085cfcd9f97b5be77b1a5d8a0948c11e835cd78ef8974cba1656814d`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 13

Live lock (`/Users/sb/code/opensip-ai/opensip/design-lock.json`): **11 inventory / 16 contract** successors. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v13.json` 135381 bytes SHA-256 `bd40aa135c4673a217c1dbcc4fbe994fe6cf7aaababd76e3740a94ed7f1a2593`

That is exactly this unit’s `successor.parent`. Last contract is native-runtime selection v3. Universe trial implementations are **not** live-installed (`crates/evaluator/src/native_universe.rs` absent from the live tree).

The three new paths are absent from v13 (0 `files[].path` rows).

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 370 inherited rows | v13 has 370 unique sorted paths; all present in v14; **0 mutated** (byte-equal row objects) |
| 3 new files | identical to `successor.addedFiles`; none removed |
| 373 total | 370+3 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; contracts remain leaf; identity → contracts only; evaluator → identity+contracts; host already lists evaluator; **no identity→evaluator** |
| v13 path order | v13 paths are a subsequence of v14 (insertions at evaluator `src/` indices 59, 61, 64) |
| row shape | every v14 file row still `{description, generated, package, path, role, standing}` |

New ownership matches the README and permitted edges — all under existing `opensip-evaluator`:

| Path | Role | Naming |
| --- | --- | --- |
| `crates/evaluator/src/native_retention.rs` | validator | snake_case, beside `native_context.rs` / `native_universe.rs` |
| `crates/evaluator/src/plan_native.rs` | validator | snake_case, beside `plan_capability.rs` |
| `crates/evaluator/src/native-plan-registry.json` | registry, `generated: false` | kebab-case closed source data, beside `native-context-registry.json` / `capability-registry.json` |

Row text keeps retention (native-frame byte walk, budgets) distinct from Plan selection and complete Run replay; Plan-native composes existing owners without execution authority. Metadata registry is embedded selected-source data, not a caller-supplied extension.

No new package, reverse edge, `build.rs`, host fixture, or dependency TCB change. Existing evaluator→identity edge suffices. Identity still cannot call evaluator.

This layout does **not** accept the future extraction of retention logic out of `native_universe.rs`, nor new Plan behavior. Exact frozen source review follows.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, all parented at **v13** bytes `bd40aa13…`. v14 copies the **parent (before) text**, not the after-text.

| v13 pointer | Stable path | v14 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/177/description` | `package.json` | **180** |

`package.json` **177 → 180** (v12 was 176; v11 was 163). Activation must project **all selected ancestors** by **stable filepath**, never stale jsonPointers or row indices.

## requiredFindings

None.

## Scope / limits

No product files created here. No runtime, native ADMIT, universe-trial install, Plan implementation, retention extraction, dependency TCB, replay, or release claim.
