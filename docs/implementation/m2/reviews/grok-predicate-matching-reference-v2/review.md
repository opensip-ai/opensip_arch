# Predicate-matching reference selection v2 — scoped design-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not Rust, runtime, schema-wire, helper-behavior, full Run, replay, or live install. Original 01b8 review, root assent, and private-activation failure stay preserved and unselected. This v2 subject still needs fresh root assent and private activation.

**subjectManifestSha256** `83c9007094bb95de8da1f7e569ad9e0c737db776c7f71aaa58ad40fdaf2e6033`  
`docs/implementation/m2/predicate-matching-reference-selection-v2-subject.json` **2270** bytes, **10/10** files, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/predicate-matching-reference-selection-v2/successor.json` **7502** / `99df59c0b101f580461b358869831be8e85964cab43ed190dee0c4a18f7315a8`. Candidates (9) equal the subject minus that record.

## What this unit is

The 01b8 corrected record added the 311c description override but named historical `source-selection-v2/successor.json` as an accepted parent. Private activation refused before live write: `contract parent is not an accepted base or selected inventory`. Live lock’s accepted contract record is `source-selection-v3/successor.json` **35266** / `e638c55c…4ae4`, which selects the v2-directory schema files (including 311c) and carries the same interruption passage overrides. v2 successor is only v3’s `previousCandidate`, not an accepted parent.

This v2 unit swaps that parent record. Same seven original helper/checker/evidence candidate bytes. New README + `parent-account.json`. Four passage overrides **byte-identical** to 01b8, including current 311c. `previousCandidate` is the unaccepted 01b8 successor `61937200…15a8` and is not a parent.

No helper, schema-wire, or runtime change. 600k glob corpus not re-run; frozen `result.json` `a73be80b…e533` remains the helper evidence.

## Live accepted map (18/22)

Independently rebuilt as `verify_design.py` does: sourceManifest + applicationManifest files, then inventory **candidates**, then each contract **record + candidates**. Observed live lock: **18** inventory / **22** contract, last contract `native-runtime-selection-v9`. Predicate-matching not selected. Historical `source-selection-v2/successor.json` is **not** in the accepted map. 01b8 successor is **not** in the accepted map.

All seven parents pin-match and classify:

| Parent | Class |
| --- | --- |
| `glob-pattern-contract.v1.md` `9b12ef44…` | application/source manifest |
| `identity-schemas.v3.json` a76c | application/source manifest |
| `workflows_model.v1.py` `be37023f…` | application/source manifest (not a lock.inputs row; still in both manifests) |
| `identity.v3.schema.json` 311c 197480 | contract-candidate of source-selection-v3 |
| `source-selection-v3/successor.json` `e638c55c…` | contract-record (lock #02) |
| recognition-derived `identity_model.py` 619d | contract-candidate of recognition-derived |
| `identity-and-evidence.md` `c82404f3…` | application/source manifest |

## Overrides and inherited interruption

Four overrides; `(parent path, selector)` unique; each `before` exact on its pin; no parent already holds `after`. Two description overrides share jsonPointer and text on **distinct** pins (a76c vs 311c): explicit dual bind, not a collision. Set-equal to 01b8’s four overrides.

source-selection-v3 and historical v2 interruption overrides on `workflows_model.v1.py` line 380 are **object-equal** (`required` → `results`). Checker still reads the preserved v2 record for that extract; v3 is the accepted authority and matches.

311c remains a v3 candidate at the v2-directory path. Live `schemas/sources/identity-v3.schema.json` is still 311c. Physical schema bytes still say “shortest decimal”; override is description-only.

## Original 7 candidate equality

The seven `predicate-matching-reference-selection-v1/` helper/checker/evidence/README pins equal 01b8’s seven and `parent-account.json`. Original README still describes the predecessor’s three overrides; this record is authoritative for four. Code remains under the original directory.

Archived 01b8 review `docs/implementation/m2/reviews/grok-predicate-matching-reference-corrected-21/` matches this reviewer’s `review.md`/`review.json`. Root assent `predicate-matching-reference-selection-v1-corrected-unit.json` remains `ACCEPTED-DESIGN-UNIT`. Failure trial `m2/trials/predicate-matching-reference-selection-21-corrected/` records no live write.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, not Rust glob/policy, not live overlay. Root assent and private activation are next and are not this review.
