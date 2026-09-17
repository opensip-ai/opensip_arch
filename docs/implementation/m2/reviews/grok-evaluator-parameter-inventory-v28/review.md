# Evaluator-parameter inventory v28 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout packaging only. **Not** implementation43, **not** kernel41 freeze, **not** runtime-v18/v19, **not** source41, **not** reference42, **not** full Run/replay/custody/M2. Frozen/live/history not edited. Parameters-43 `advisory.md`/`advisory.json` were not modified. Root remains lead. Not Claude agreement.

Live `inventory_successor` (`opensip/tools/verify_design.py` 86–142, line **109**) admits additive layout only when independent review `verdict` is **`ACCEPT-UNIT`**, `requiredFindings` is `[]`, and `inventoryCandidateAssessment.verdict` is `ACCEPT`. That is the token used here. `ACCEPT-DESIGN-UNIT` is the contract token (line **198**) and would be refused at inventory activation.

**subjectManifestSha256** `466cbdefb82a15b8c3d64da8c32995d1ad91245ed9205adc94b4e5ad5098fb91`  
`docs/implementation/m2/evaluator-parameter-inventory-v28-subject.json` **641** bytes, **3** members, paths sorted unique, **0** pin mismatches.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `evaluator-parameter-inventory-v28/README.md` | 901 | `4fd95c6c007e6fa3ae31960d5a892ce00dd1b68b6e9a5f48ec65f142b51bafb2` |
| `evaluator-parameter-inventory-v28/successor.json` | 630 | `014bde7078ea8196ad4381f2cdf5cd0ae22d2f62bcb919ae2b9703c4dea95e4d` |
| `repository-file-inventory.v28.json` | 150007 | `b67c6101369e7ae76898c6997e5dae5f97bf9dc0c00f4a0ac3a1b923a4184240` |

Prompt (context only): 1587 / `a637678967f56ca7c4d6af8e1c27ccfc525522fae138c7989257d8fb92c996c8`.

## Checker (`inventory_successor` 85–143)

Successor record declares **both** required true flags: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. Parent pin is the live inventory **candidate** v27, not the v27 successor **record**. Candidate pin matches disk. `same_reference` on this assessment uses candidate path+bytes+sha256, parent path+bytes+sha256, and successor-record path+sha256.

Parent vs candidate: same keys except `standing` and `files`; `packages` (20) and `pendingDecisions` (9) identical. One sorted unique addition; inherited rows equal by value (0 mutated, 0 removed). Parent path list is a subsequence of the candidate. `addedFiles` is the single new path.

## Parent is live inventory **candidate** 27

Live lock independently **25 inventory / 37 contract** (`75079` / `813aa62f39230b654ca6856266d292be6c83eae070f7a2748e6bb9e4e9a5b4ac`). Last inventory **candidate**:

`docs/implementation/m2/repository-file-inventory.v27.json` **149414** / `202d9233ffa696b1c9f8b2777a3c4f76f5781a092b095be23e10bdfa148c59bc`

That is `successor.parent`. Last **runtime** selection remains v18 (`native-runtime-selection-v18/successor.json` **22076** / `7824be204290185b5c1197aefbb1f6477437c6591947682b31306daa0c408ad1`, contract index 35). Last **contract successor** is enumeration-locator-totality-reference-selection-v1 (`3210` / `fdeff745cc1b40477b2f2fbe3692ce8c86ea99910a75705ec7c792c3f27cfa7c`, index 36). Runtime 19 is not live.

Live product has **no** `evaluator-parameter-fixtures.json`. Live `policy.rs` is still the 16386-byte glob/`inspect_policy_program` owner (no 43 export). This layout does not add `policy.rs` or `atom-registry.json`; those remain inherited evaluator **compiler** / **metadata** rows.

Parameters-43 advisory required finding (`parameters-43-inherits-unaccepted-enumeration-kernel-41`) is a tracked freeze prerequisite, not a product-code fault of this layout. Frozen 41 kernel **52825** / `ce09cc8265de603ac81a8f4c0dd2f1ca89da5e01385f59a4913a78e99be8f49f` matches the 43-inherited join; this review does **not** demand rebase to the earlier 51742 advisory copy. Source41 is under separate wN review; runtime19 is pending. This unit does not accept 43 source or runtime.

## Candidate assessment: **ACCEPT**

| Claim | Check |
| --- | --- |
| 399 inherited rows | v27 399 unique sorted paths; all present in v28; **0 mutated** |
| 1 new file | `crates/host/tests/fixtures/evaluator-parameter-fixtures.json`; none removed |
| 400 total | 399+1 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no new package/edge |
| v27 path order | subsequence of v28 (insertion at host fixtures **118**) |
| packaging flags | both required true flags present |
| row shape | `{path, package, role, description, generated, standing}` |

New row (`generated: false`, `standing: proposed`):

- `opensip-host` `crates/host/tests/fixtures/evaluator-parameter-fixtures.json` **fixture** (kebab, sibling of `enumeration-join-fixtures.json` / `package-fixtures.json`). Pooled Plan/spec/parameter/policy/emission/closure packets and expected diagnostics. No host admission authority. No complete execution selection or Run replay.

README ownership split matches: evaluator implementation stays on existing `policy.rs` + source-bound atom registry; host fixture holds bytes and expected diagnostics only. Layout does not accept private implementation43 or a reference change.

Private trial fixture (not a subject member; not source acceptance) has **31** cases: **10** selected-result packets + **13** join-law refusals = **23** actual-reference result/refusal, plus **8** owner/resource controls (`unavailable`/`invalid`/`limited`). That matches the named path’s intended census. Architecture and live trees still lack the file; this unit only names it.

## Inherited description overrides

Live `inventoryPassageInheritance` has **4** entries, all parented at **v27**, selectors `/files/7|13|205|272/description`. v28 copies **before-text** on those rows. `successor_chain` (312–346) projects by **stable filepath** after the additive insert at 118.

| v27 pointer | Stable path | v28 index |
| --- | --- | ---: |
| `/files/7/description` | `apps/cli/src/bootstrap.rs` | **7** |
| `/files/13/description` | `apps/report/package.json` | **13** |
| `/files/205/description` | `package.json` | **206** |
| `/files/272/description` | `schemas/sources/imported-v1.schema.json` | **273** |

No override dropped. Private activation must rewrite the lock inheritance parent to this candidate and project **all four** pointers by filepath (7, 13, 206, 273).

## requiredFindings

None.

## Scope / limits

No product files created in this layout unit. Does not accept implementation43, SOURCE38, runtime-v18/v19, source41, or locator/reference changes. Does not reopen the 43 rebase finding as a layout defect. Complete execution-input selection, predicate reconstruction/replay, and Run/custody remain open. Root assent and private activation of **this** record remain pending.
