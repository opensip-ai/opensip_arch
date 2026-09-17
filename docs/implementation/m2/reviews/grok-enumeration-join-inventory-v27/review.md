# Enumeration-join inventory v27 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** implementation41, **not** kernel41 advisory acceptance, **not** source41, **not** reference42, **not** SOURCE38, **not** runtime-v18, **not** full Run/replay/custody/M2. Frozen/live/history not edited. Kernel41 `advisory.md`/`advisory.json` were not modified. Root remains lead. Not Claude agreement.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142, line **109**) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the **contract** token (`contract_successor` line **198**) and would be refused at inventory activation. This unit is an inventory successor, not a contract successor.

**subjectManifestSha256** `2a675c03f004df54883def7e2bdced80e0e857a0a43015fea7cd4a05316102c0`  
`docs/implementation/m2/enumeration-join-inventory-v27-subject.json` **636** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `enumeration-join-inventory-v27/README.md` | 1031 | `9a536dbd933392772965f336ef3d0ccbe7b2ff9cbdb01da6b8f49136372284c4` |
| `enumeration-join-inventory-v27/successor.json` | 729 | `cf176a75306ee3faf3238272e69b5976e0472aef08550134e5c619c7eb5aabe1` |
| `repository-file-inventory.v27.json` | 149414 | `202d9233ffa696b1c9f8b2777a3c4f76f5781a092b095be23e10bdfa148c59bc` |

Prompt (context only): 1698 / `8e270cbfca727561d512dcbbac8f7087d349f540fbd392b35e1386225cd9d99d`.

## Checker (`inventory_successor` 85–143)

Successor record declares **both** required true flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v26, not the v26 successor **record**. Candidate pin matches disk. `same_reference` on this assessment uses candidate path+bytes+sha256, parent path+bytes+sha256, and successor-record path+sha256.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. Sorted unique additions; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate.

`addedFiles` in the successor record is the same **set** of three paths. The list is not lexicographically sorted (`enumeration_join.rs` before `enumeration-registry.json`). The checker does not read that array; it computes added count from the two inventories. Not a required finding.

## Parent is live inventory **candidate** 26

Live lock independently **24 inventory / 36 contract** (`72973` / `5b17d8370e3da68b13bd17cfde5dfb1c98e54dcf349c382f88560c91a7f328cb`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v26.json` **147952** / `1a861b0cd3bc6dcbb952e2b136299bd7e3a4492f2eb488039e90e89ac740a324`

That is `successor.parent`. Last contract: runtime **v18** (`docs/implementation/m2/native-runtime-selection-v18/successor.json` **22076** / `7824be204290185b5c1197aefbb1f6477437c6591947682b31306daa0c408ad1`). Live product tree has **no** `enumeration_join.rs`, `enumeration-registry.json`, or `enumeration-join-fixtures.json`. Live evaluator `Cargo.toml` **261** / `cef1245cbfec7e96892ea2cc7ffdead83d82cf3bc425c1ea98bd106d730b2f56` still depends only on `opensip-identity`. Live identity `Cargo.toml` **750** / `876739b9d5a7be6a8aee5eb3379e6f543425d67594acf40a411af1146c73dff9` has no `opensip-*` crate dependency (toml graph is the already-installed SOURCE38 pin; unchanged by this layout).

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 396 inherited rows | v26 396 unique sorted paths; all present in v27; **0 mutated** |
| 3 new files | `enumeration_join.rs`, `enumeration-registry.json`, host `enumeration-join-fixtures.json`; none removed |
| 399 total | 396+3 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v26 path order | subsequence of v27 (insertions at evaluator **62** / **64**, host fixtures **117**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New rows (`generated: false`, `standing: proposed`):

- `opensip-evaluator` `crates/evaluator/src/enumeration_join.rs` **source** (snake_case). Derive enumeration inputs from retained Plan/snapshot/parameter/membership/native/closure/inventory bytes and produce an inert diagnostic population or complete refusal. No caller-supplied ADMIT/`bindResult` and no Run/replay/custody authority. Sibling of existing `enumeration.rs` (**algorithm**: populations from admitted Plan inputs). Layout does not accept implementation41.
- `opensip-evaluator` `crates/evaluator/src/enumeration-registry.json` **registry** (kebab, sibling of `import-registry.json` / `native-plan-registry.json` / other evaluator `*-registry.json`). Source-bound capability-kind, suffix-language, cause-carrier and fault-order tables. Not dynamic configuration and not authority to accept caller claims.
- `opensip-host` `crates/host/tests/fixtures/enumeration-join-fixtures.json` **fixture** (kebab, sibling of `enumeration-fixtures.json` / `package-fixtures.json`). Pooled complete retained-input packets plus separately labeled missing/malformed/tamper/resource controls. Exercises the public retained-input boundary, not supplied kernel maps or complete evaluator replay.

Ownership split in README matches the three rows: identity rehashes/validates inert retained records; evaluator derives native and inventory joins; host supplies bytes. Public result is an inert diagnostic. Membership discovery before Plan construction remains separate. Internal dependency directions unchanged: evaluator → identity only (inventory DAG still evaluator → contracts+identity; identity → contracts only; no reverse identity→evaluator edge).

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, all parented at **v26**, selectors `/files/7|13|202|269/description`. v27 copies **before-text** on those rows. `successor_chain` (312–346) projects by **stable filepath** after additive inserts.

| v26 pointer | Stable path | v27 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/202/description` | `package.json` | **205** |
| `/files/269/description` | `schemas/sources/imported-v1.schema.json` | **272** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath (7, 13, 205, 272).

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit (the three paths are absent from both architecture and live trees). Does not accept kernel41 implementation, SOURCE38, runtime-v18, a reference change, or the separate wN review42 of 18 selected-E39 `rawTypeErrors`. Root-stated kernel follow-up (schema-failure `False==0`, 45 boolean controls, 1402 typed-list comparisons) is context only and is not this unit. Complete reconstruction, replay, compiler providers, product workflows, and release qualification remain open. Root assent and private activation of **this** record remain pending.
