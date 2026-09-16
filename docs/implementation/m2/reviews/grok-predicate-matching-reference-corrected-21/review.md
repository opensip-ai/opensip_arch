# Predicate-matching reference selection v1-corrected — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not Rust, runtime, schema-wire, helper-behavior, full Run, replay, or live install. Original 04bf ACCEPT is archived; root declined assent on that packaging. This corrected subject still needs root assent and private activation.

**subjectManifestSha256** `01b8e3d2b36b5a83c9ade19e2ca05ebc2e41fabf2cedbb093ad4868bf9f56d04`  
`docs/implementation/m2/predicate-matching-reference-selection-v1-corrected-subject.json` **2308** bytes, **10/10** files, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/predicate-matching-reference-selection-v1-corrected/successor.json` **7531** / `619372006fe9c4e1aa134450f792b4f99280301dec41c809fed9385ecd7463c9`. Candidates (9) equal the subject minus that record.

## What this unit is

Packaging correction of unselected original 04bf. Same seven original candidate files (helper, checker, original README, evidence) at the original directory, byte-identical to original successor candidates. Adds corrected README and `current-schema-account.json`. Adds accepted parent current identity-v3 **311c** (197480) plus the **same** description override already recorded on historical a76c. Retains a76c, identity-and-evidence line 1272, and glob line 79: **four** overrides. `previousCandidate` is original successor `006c225d…1fc6` and is **not** a parent.

No helper, runtime, schema-wire, or source-behavior change. Inherited source-selection-v2 line-380 interruption remains in the unchanged workflow candidate. Original README still describes the predecessor’s three overrides; the corrected README states four.

## Pins

Parents (7), sorted unique, disk-exact. Versus original successor: **one added** parent (`identity.v3.schema.json` 311c); none removed; six shared pins identical.

| Parent | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/coop/design-corrections/foundation/glob-pattern-contract.v1.md` | 3946 | `9b12ef44…8ba0` |
| `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | 196987 | `a76c9e2f…db21` |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | 142811 | `be37023f…66dc` |
| `docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json` | 197480 | `311c1feb…b68f` |
| `docs/implementation/m1/source-selection-v2/successor.json` | 34488 | `8bd78b83…2819` |
| `docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py` | 158555 | `619d6e3c…41e6` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | 135448 | `c82404f3…d31f` |

Corrected directory has exactly three files (README, account, successor). Original directory’s eight files include the previousCandidate successor record, which this subject does not re-list.

## Overrides (4; no collision)

Each `before` is unique and exact on its parent pin; no parent already holds `after`. Keys `(parent path, selector)` are unique. Two description overrides share jsonPointer `/$defs/program-predicate/description` and identical before/after **by value**, on **different** pins (a76c vs 311c). That is the explicit dual bind, not a collision and not silent inheritance.

Original three overrides are a subset of these four. The only new override is 311c description.

Physical schema bytes unchanged: 311c `predicateId` remains `$ref: Text` (1–4096, no digit pattern) and still says “shortest decimal” on disk.

## Current alias

`urn:opensip:product-v1:identity:v3` maps to 311c in source-selection-v2 `current-dispatch.json`, `source-map.json`, and `generation-source-map.json`. Live `schemas/sources/identity-v3.schema.json` is byte-identical to 311c.

## Original candidate equality and prior helper evidence

The seven original successor candidates are pin-equal in this record and in `current-schema-account.json`. Helper/checker/result bytes are therefore the original 04bf set. Frozen `evidence/result.json` `a73be80b…e533` and archived independent reproduction `independent-result.json` `af1170fd…0983` (Python 3.12.13 / UCD 15.0.0: 609978 glob pairs, 0 mismatches, 1732 changed; 23 ASCII / 805 Unicode controls, 804 changed; 7 round-trips; interruption preserved) are not re-run here.

Archived original review `docs/implementation/m2/reviews/grok-predicate-matching-reference-21-original/` matches this reviewer’s 04bf `review.md`/`review.json`/`followup-current-schema.*`. `root-disposition.json` records root read both, **declined assent**, and left 04bf unselected.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, not Rust glob, not policy/predicate owner implementation, not live overlay. Independently observed live lock: **18** inventory / **22** contract, last contract `native-runtime-selection-v9`; predicate-matching not selected. (Prompt stated 17/22; inventory v20 is now present. Not a defect in this unit.) Root assent and private activation remain next.
