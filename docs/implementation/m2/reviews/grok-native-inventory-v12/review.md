# Native-owners inventory v12 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not a dependency or unsafe-TCB selection. Frozen/live/history not edited. Private09 implementation is out of scope.

Subject `docs/implementation/m2/native-owners-inventory-v12-subject.json` SHA-256 `aa4586566f62947476ac0d710228a61a96443038ee90b8312eea67689300f057` (631 bytes). Three members pin-match: README `779aa140…cf0f`, `successor.json` `00089f89…1252`, `repository-file-inventory.v12.json` 134933 bytes `dd2ad2da…5678`. Unit directory has no extra or missing files. Subject paths sorted unique.

## Parent is live inventory 11

Live lock (`/Users/sb/code/opensip-ai/opensip/design-lock.json`): **9 inventory / 15 contract** successors. Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v11.json` 127200 bytes SHA-256 `0ae9d43939f924a8cdd1b7926129063c24e59c55ae58f6a72c1633b890461f62`

That is exactly this unit’s `successor.parent`. Last contract remains capability-totality reference selection. Parent artifact bytes are the accepted current inventory.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 348 inherited rows | v11 has 348 unique sorted paths; all present in v12; **0 mutated** (byte-equal row objects) |
| 21 new files | identical to `successor.addedFiles`; none removed |
| 369 total | 348+21 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; contracts remain leaf (`[]`); identity → contracts only; evaluator → identity+contracts; **host already lists evaluator and identity** |
| v11 path order | v11 paths are a subsequence of v12 (insertions only) |
| row shape | every v12 file row still `{description, generated, package, path, role, standing}` |

New ownership matches the README and permitted edges:

- **Identity (codec/validator only):** `capability_codec.rs` (CVE1, no semantic ADMIT), `relations.rs` (local ladder; native/universe remaining owner).
- **Evaluator (owners):** `capabilities.rs`, `plan_capability.rs` (pre-admission bytes join named in the row), `native_context.rs`, `unicode_case.rs` (Unicode **15** FULL default lowercase + version gate; not rustc 17), closed registries `capability-registry.json` / `native-context-registry.json` (kebab), generated `src/generated/unicode_case_tables.rs` (`generated: true`).
- **Host (dev tests/fixtures only):** `native_owner_tests.rs`, kebab fixtures. Host→evaluator already in the DAG.
- **Tooling:** `check_identity_dependencies.py`, `tools/identity/dependency-policy.json` (layout of a future identity-lane policy, **not** selected here), offline `generate_unicode_case.py` (must not run as product `build.rs`), `tools/unicode/LICENSE`, `tools/unicode/case-data/unicode-v15/{UnicodeData,SpecialCasing,DerivedCoreProperties}.txt` plus `sources.json`.

Naming: new JSON basenames are kebab-case (no `_` in `.json` names). Generated Rust is under `src/generated/`. Case data directory is `unicode-v15` with original upstream txt names. Rust modules remain snake_case; host tests `*_tests.rs`. Frozen 07/08 underscore JSON paths are **not** in this inventory.

No new package, reverse identity→evaluator edge, or `build.rs`. `unicode_case_tables.rs` is generated output checked by the offline generator, not runtime execution of retained UCD.

Data-version split is explicit in row text: casing tables/UCD **15**; NFC/normalization **16** called out as separate; **not** ambient Rust 17. This layout does **not** accept `unicode-normalization`, Hangul `unsafe`, or identity TCB.

Successor shape matches the last accepted inventory successor (`parent` / `candidate` / `addedFiles` / `inheritedRowsEqualByValue`). Standing is layout-only.

## Inherited description overrides

Live `inventoryPassageInheritance` has **3** entries, all parented at v11 bytes `0ae9d439…`. v12 copies the **parent (before) text**, not the after-text.

| v11 pointer | Stable path | v12 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | 7 |
| `/files/13/description` | `apps/report/package.json` | 13 |
| `/files/163/description` | `package.json` | **176** |

`package.json` **163 → 176**. Activation must project **all selected ancestors** by **stable filepath**, never stale jsonPointers or row indices. This candidate does not bake override after-text into inherited rows.

## requiredFindings

None.

## Scope / limits

No product files created here. No runtime, native ADMIT, Plan-capability implementation, Unicode generator execution, identity dependency policy, replay, or release claim. Next: private09 code against this layout; other Grok reviews 08 remain separate.
