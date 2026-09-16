# Run-links inventory v19 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not source/code acceptance (private-19 source is not requested). Frozen/live/history not edited. Root remains lead.

Subject `docs/implementation/m2/run-links-inventory-v19-subject.json` SHA-256 `f3f24f7302ec49879ca580e1d0161324014d410cdeebb44b2705e59b6f5e1b75` (621 bytes). Three members pin-match: `repository-file-inventory.v19.json` 140780 / `ec61d2fbee9e6fdd6000acabe263d2c455f71055b6e8843e5c973351fe9c9725`, README `8ce90c02…755a` / 984, `successor.json` `52ace802…3174` / 566. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory **candidate** 18

Last inventory **candidate** (not the inventory successor *record*):

`docs/implementation/m2/repository-file-inventory.v18.json` 140296 bytes SHA-256 `3bc6f5b2540c507bec43987aee188253b0b7e078c309631dd90c5dc447b5b025`

That is this unit’s `successor.parent`. Independently observed live lock: **16 inventory / 21 contract**; last contract `native-runtime-selection-v8/successor.json`. README still says 16/20, inventory18/runtimev7, “runtimev8 review pending”. v8 is already the last live contract, so the README’s “install v8 before this layout” ordering is already satisfied; the count/label in README is stale. Parent inventory pin is exact. `run_links.rs` is absent from the live tree.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 381 inherited rows | v18 has 381 unique sorted paths; all present in v19; **0 mutated** |
| 1 new file | identical to `successor.addedFiles`; none removed |
| 382 total | 381+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; identity → contracts only; evaluator → identity+contracts; **no identity→evaluator**; no new identity API or metadata file |
| v18 path order | subsequence of v19 (insertion at evaluator `src/` index **74**) |
| row shape | `{description, generated, package, path, role, standing}` |

New row:

| Path | Package | Role | Naming |
| --- | --- | --- | --- |
| `crates/evaluator/src/run_links.rs` | `opensip-evaluator` | validator, `generated: false` | snake_case, sibling of `plan_capability.rs`; **not** `replay.rs` |

Row text: rehash Run root cross-links, configuration/grant/VCS, and **separately** proof-selected view/coverage/finding evidence roots; preserve **phase order**; diagnostics do not establish full walk, predicate program addressing, policy/stage/import admission, or replay.

That matches selected `open_run_closure` **1651–1687** (pre-native: snapshot/plan/evidence/seal/proof/execution, capability bytes + `admit_capability_manifest`, grant, VCS) and **1808–1828** (proof-selected view/coverage roots and finding evidence membership). Predicate addressing starts at **1832** and is excluded, as is walk (1650), native (1689), policy/stages (1757–1794), import admission, and replay. Existing `plan_capability.rs` owns capability-byte admission; this owner composes it. No caller ADMIT. Two APIs in one file, order preserved.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v18**. v19 copies **before-text**, not after-text.

| v18 pointer | Stable path | v19 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/188/description` | `package.json` | **189** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created here. No run-links source, walk/`OwnerJoin`, view-18 source, or replay claim. README live-lock labels (16/20, v7, v8 pending) lag the independently observed 16/21 with v8 already last contract; they do not change the parent inventory pin.
