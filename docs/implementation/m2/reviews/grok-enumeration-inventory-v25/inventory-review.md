# Enumeration inventory v25 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Layout only. Not SOURCE34 source acceptance. Not runtime16. Not full enumeration. Not Run/replay. Frozen/live/history not edited. Root remains lead. Not Claude agreement.

**subjectManifestSha256** `d0ded1e9fc78a114e19312ed446ebd008cc01009410739a1c7f39f8c5fa5c3b6`  
`docs/implementation/m2/enumeration-inventory-v25-subject.json` **625** bytes, **3** members, sorted unique, **0** pin mismatches.

## Parent is live inventory-24 **candidate**

Live lock: **22 inventory / 31 contract** (`66066` / `116fefcc033b2b7b2a441c6b55f414b581bada8586a3b3745ec39e0e445514e3`). Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v24.json` **146038** / `332d47aaee98a234abe5e76f99f607ed01927dab1640df12f95ed7678f55bcb6`

That is this unit’s `successor.parent` (bytes and sha256 match). Last contract is `native-runtime-selection-v15/successor.json`. Selection of this inventory **must wait** for pending runtime16 r2 review/activation, so the frozen 22/31 base stays. This layout does not select itself.

`crates/evaluator/src/enumeration.rs` is **already** a v24 planned row. This unit adds only the host fixture.

## Candidate assessment: **ACCEPT**

Successor flags **both required true**: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`.

| Claim | Check |
| --- | --- |
| 392 inherited rows | v24 has 392 unique sorted paths; all present in v25; **0** mutated |
| 1 new file | identical to `successor.addedFiles`; none removed |
| 393 total | 392+1 |
| 20 packages / DAG | `packages` (20) and `pendingDecisions` (9) identical; no new package |
| v24 path order | subsequence of v25 |
| row shape | `{description, generated, package, path, role, standing}` |

New row:

| Path | Package | Role | Index |
| --- | --- | --- | ---: |
| `crates/host/tests/fixtures/enumeration-fixtures.json` | opensip-host | fixture, `generated: false`, standing `proposed` | lexicographic among host tests fixtures |

Fixture standing: pooled projection/admission regression inputs; fixture success grants no native/Run/replay/custody authority. Does not implement package parse or full `admit_enumeration`.

## Description overrides — project by **stable file path**

Live lock has **4** `inventoryPassageInheritance` rows parented at **v24**. After this candidate, inherit ancestor meaning onto v25 by filepath (not hardcoded “four” as a v24 index freeze).

| Source | Stable path | v24 index | v25 index |
| --- | --- | ---: | ---: |
| live inheritance | `apps/cli/src/bootstrap.rs` | 7 | **7** |
| live inheritance | `apps/report/package.json` | 13 | **13** |
| live inheritance | `package.json` | 199 | **200** |
| live inheritance | `schemas/sources/imported-v1.schema.json` | 266 | **267** |

v24 and v25 **row descriptions are equal** on those four paths. Activation must emit inheritance against the **v25** pin with projected `/files/{index}/description` selectors (7, 13, 200, 267).

## requiredFindings

None.

## Scope / limits

No product files created here. Does not accept SOURCE34, runtime16, complete enumeration, native admission, or live write. Base remains frozen 22/31 until runtime16 r2 can select.
