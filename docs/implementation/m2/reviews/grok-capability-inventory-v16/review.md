# Capability-support inventory v16 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not source/code acceptance. Not body15 review. Prior native-relation-boundary-16 is an advisory, not a selected pair. Frozen/live/history not edited. Root remains lead.

Subject `docs/implementation/m2/capability-support-inventory-v16-subject.json` SHA-256 `6940c86d03a4af270f5f9c8535e882e1858567a6820ca89caee3b56276681756` (640 bytes). Three members pin-match: README `6c0377fe…7c3b` / 1610, `successor.json` `0b2fae23…bd04` / 787, `repository-file-inventory.v16.json` 138398 bytes `2da370ad759cf85e57d8f8881b5dca73d5d8d4a463d83dd6824298582b480438`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 15

Live lock: **13 inventory / 17 contract**. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v15.json` 137496 bytes SHA-256 `c761fd99b0b4e236323ef79d455ab31b65ec24b9ddbd88597715e9e397b6f28e`

That is this unit’s `successor.parent`. Last contract is native-runtime v4. Body15 layout is selected; `body_identity.rs` is still absent from the live tree (separate source review). The two new v16 paths are absent from v15 and from live product.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 375 inherited rows | v15 has 375 unique sorted paths; all present in v16; **0 mutated** |
| 2 new files | identical to `successor.addedFiles`; none removed |
| 377 total | 375+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; identity → contracts only; evaluator → identity+contracts; **no identity→evaluator** |
| v15 path order | subsequence of v16 (insertions at evaluator `src/` indices 56–57) |
| row shape | `{description, generated, package, path, role, standing}` |

New rows, both `opensip-evaluator`:

| Path | Role | Naming |
| --- | --- | --- |
| `capability_support.rs` | validator | snake_case, sibling of `body_identity.rs` / `plan_native.rs` |
| `capability-support-registry.json` | registry, `generated: false` | kebab closed data, **not** `capability-registry.json` (release manifests) and **not** `native-plan-registry.json` (Plan request vocabulary) |

Row text keeps grammar/source-variant/ownership **prerequisites** distinct from complete Coverage, graph admission, replay, caller ADMIT, and Plan counts as a selected-pair token. README matches the boundary-16 split: body15 owns clone frames; this owner owns fact-time syntax support and Coverage disclosures; `capabilities.rs` stays release manifests. Inventory capabilities remain ungated. No new crate, edge, or dependency TCB.

This layout does **not** accept private source/metadata bytes or implementation.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, parented at **v15**. v16 copies **before-text**, not after-text.

| v15 pointer | Stable path | v16 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/182/description` | `package.json` | **184** |

Activation must project **all selected ancestors** by **stable filepath**.

## requiredFindings

None.

## Scope / limits

No product files created here. No source, body15, Plan-native, Coverage producer, or runtime claim.
