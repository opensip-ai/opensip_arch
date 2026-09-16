# Native-universe inventory v13 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not a dependency or unsafe-TCB selection. Does not accept private trial 10/11/12 universe code. Frozen/live/history not edited. Root remains lead.

Subject `docs/implementation/m2/native-universe-inventory-v13-subject.json` SHA-256 `088d06c697540182bf280d73caf10e73e473d8b76dde751e98dc4dad9c21160b` (634 bytes). Three members pin-match: README `3ad9be47…1621` / 1134, `successor.json` `6d6efb5d…2613` / 726, `repository-file-inventory.v13.json` 135381 bytes `bd40aa135c4673a217c1dbcc4fbe994fe6cf7aaababd76e3740a94ed7f1a2593`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 12

Live lock (`/Users/sb/code/opensip-ai/opensip/design-lock.json`): **10 inventory / 15 contract** successors. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v12.json` 134933 bytes SHA-256 `dd2ad2da0d4eef0dd135988cfade743195bd758d8c8bb290975b1d0382675678`

That is exactly this unit’s `successor.parent`. Last contract remains capability-totality reference selection. Parent artifact bytes are the accepted current inventory.

Literal `native_universe.rs` is **absent** from v11 (`0ae9d439…1f62` / 127200) and from live v12 (`dd2ad2da…5678` / 134933): 0 matches, 0 `files[].path` rows. Live product has no such file.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 369 inherited rows | v12 has 369 unique sorted paths; all present in v13; **0 mutated** (byte-equal row objects) |
| 1 new file | `crates/evaluator/src/native_universe.rs` identical to `successor.addedFiles`; none removed |
| 370 total | 369+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; contracts remain leaf (`[]`); identity → contracts only; evaluator → identity+contracts; host already lists evaluator; **no identity→evaluator** |
| v12 path order | v12 paths are a subsequence of v13 (one insertion at index 60, after `native_context.rs`, before `plan_capability.rs`) |
| row shape | every v13 file row still `{description, generated, package, path, role, standing}` |

New ownership matches the README and permitted edges:

- **Evaluator (owner):** `native_universe.rs`, `role: validator`, `generated: false`, snake_case. Binds registered universe frames; identity stays the lower-level shape/hash/retained-input owner. Adjacent inherited `native_context.rs` still says universe binding remains separate.
- **No new package, JSON registry, host fixture, or tooling path.** Existing `native-context-registry.json` and host `native_owner_tests.rs` / fixtures remain the v12 rows.
- Existing evaluator→identity edge suffices. No reverse edge, no `build.rs`, no new crate, no dependency TCB change.

Naming: one new Rust module, snake_case, under the existing evaluator package. No new JSON basename, so no kebab/underscore issue. No invented factory family.

Successor shape matches the last accepted inventory successor (`parent` / `candidate` / `addedFiles` / `inheritedRowsEqualByValue`). Standing is layout-only. Row description keeps Plan selection, complete retention, and evaluator replay distinct.

This layout does **not** accept syntax/TS/Rust diagnostic implementations (private trials 10/11/12), native ADMIT, or replay.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, all parented at **v12** bytes `dd2ad2da…`. v13 copies the **parent (before) text**, not the after-text.

| v12 pointer | Stable path | v13 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/176/description` | `package.json` | **177** |

`package.json` **176 → 177** (historical v11 index was 163). Activation must project **all selected ancestors** by **stable filepath**, never stale jsonPointers or row indices. This candidate does not bake override after-text into inherited rows.

## Independent of runtime v3

Pending `native-runtime-selection-v3` reuses the v2 **35-input** materialization map and names live v12 as its inventory parent. It does not list v13 or a universe implementation. Universe layout and runtime v3 must be bound to the live lock at their own activation times.

## requiredFindings

None.

## Scope / limits

No product files created here. No runtime, native ADMIT, trial 10/11/12 code, dependency TCB, replay, or release claim.
