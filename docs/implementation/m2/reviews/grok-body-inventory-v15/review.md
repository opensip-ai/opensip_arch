# Body-identity inventory v15 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout only. Not runtime acceptance, not dependency/unsafe-TCB selection, and not body15 source or runtime-v4 inclusion. Evolving `body_identity.rs` is not reviewed here. Frozen/live/history not edited. Root remains lead. The completed body-join advisory/correction is preserved separately and is not this unit.

Subject `docs/implementation/m2/body-identity-inventory-v15-subject.json` SHA-256 `09fe80ddd568cb9563b4c277795ddbf3aa3e4f1fef3d748f9ce5241572c7c518` (630 bytes). Three members pin-match: README `86f3dfa7…693c` / 1183, `successor.json` `54e69687…2d51` / 764, `repository-file-inventory.v15.json` 137496 bytes `c761fd99b0b4e236323ef79d455ab31b65ec24b9ddbd88597715e9e397b6f28e`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 14 (12/17)

Live lock (`/Users/sb/code/opensip-ai/opensip/design-lock.json` 41361 bytes SHA-256 `598049fe4c06edc572dba6893d7fa0a5a1035a6fa7cbed2b3f79018cb5685f89`): **12 inventory / 17 contract** successors. Native-runtime v4 is formally accepted and installed. Last inventory **candidate** is unchanged:

`docs/implementation/m2/repository-file-inventory.v14.json` 136672 bytes SHA-256 `20bd2bd4085cfcd9f97b5be77b1a5d8a0948c11e835cd78ef8974cba1656814d`

That is exactly this unit’s `successor.parent`. Last contract is `docs/implementation/m2/native-runtime-selection-v4/successor.json` `53dcc3cb…f381` / 17153. v4 parents inventory **v14**, not v15, and does not include body15. v4 install does **not** mutate the 373 inherited inventory rows.

The two new paths are absent from v14 (0 `files[].path` rows) and absent from the live tree.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 373 inherited rows | v14 has 373 unique sorted paths; all present in v15; **0 mutated** (byte-equal row objects) |
| 2 new files | identical to `successor.addedFiles`; none removed |
| 375 total | 373+2 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; contracts remain leaf; identity → contracts only; evaluator → identity+contracts; host already lists evaluator; **no identity→evaluator** |
| v14 path order | v14 paths are a subsequence of v15 (insertions at evaluator `src/` indices 51, 52) |
| row shape | every v15 file row still `{description, generated, package, path, role, standing}` |

New ownership matches the README and permitted edges — all under existing `opensip-evaluator`:

| Path | Role | Naming |
| --- | --- | --- |
| `crates/evaluator/src/body_identity.rs` | validator | snake_case, beside `native_context.rs` / `plan_native.rs` |
| `crates/evaluator/src/body-registry.json` | registry, `generated: false` | kebab-case closed source data, beside `native-plan-registry.json` / `native-context-registry.json` / `capability-registry.json` |

Row text keeps clone body-frame / normalization-map / dialect checks distinct from Plan, Coverage and complete Run admission. Metadata is explicit pinned JSON, not a caller-supplied registry and not a new dependency. No new package, reverse edge, `build.rs`, host fixture, or Cargo.toml change. Identity `crates/identity/src/closure.rs` is unchanged in this inventory; live `inspect_relation_sources` still returns `Unsupported("relation body identity owner")` and does not import evaluator.

This layout does **not** accept or install body15 source. Runtime v4 product/export/`lib.rs` contain no body owner.

## Closed metadata (layout claim; not source acceptance)

Body metadata is exactly

`/tmp/opensip-implementation/m2-body-identity-trial-15/product/crates/evaluator/src/body-registry.json` 7031 bytes SHA-256 `a9f7f2cb42407383451d398cd3e47980f7cba9f736deb009cefd999e87d7a538`

Source pins are the adjacent

`/tmp/opensip-implementation/m2-body-identity-trial-15/body-registry-sources.json` 741 bytes SHA-256 `c9b25054205aba24ee3af7313669285ec5b7eaefaf3e128c1563b10e0764e87c`

Those pins match on disk: identity-v3 `311c1feb…b68f` / 197480 (`normalizationSpecificationLaw`) and relation-payload-v2 `53380a24…be9a` / 57623 (clones row, the only `bodyIdentityJoin`; `snapshotJoins` `[]`). Reconstructing `{normalizationSpecificationLaw, clones}` equals that registry file. This is the native-plan registry pattern. The registry file is **not** a subject member and is **not** accepted as runtime/source here.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, all parented at **v14** bytes `20bd2bd4…`. v15 copies the **parent (before) text**, not the after-text.

| v14 pointer | Stable path | v15 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/180/description` | `package.json` | **182** |

`package.json` **180 → 182** (v13 was 177; v12 was 176; v11 was 163). Activation must project **all selected ancestors** by **stable filepath**, never stale jsonPointers or row indices.

## requiredFindings

None.

## Scope / limits

No product files created here. No review of evolving body code. No runtime, native ADMIT, body15 source, runtime-v4 inclusion, dependency TCB, replay, or release claim. Body-join advisory/correction remains at `/tmp/opensip-implementation/m2-grok-body-join-boundary-15` (`correction.md` `659f67ad…cdf3` / 4218, `correction.json` `b08790c7…1f9d` / 2088) and was not edited.
