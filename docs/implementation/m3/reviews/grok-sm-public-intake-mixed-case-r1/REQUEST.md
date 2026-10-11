# Review request: SM-PUBLIC-INTAKE-MIXED-CASE-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/grok-sm-public-intake-mixed-case-r1/`).

## Boundaries

Do not edit either repository, the stage, the isolated producer, or control files. Do not run the compiler, Cargo, tests, runners, or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing, source reading and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/sm-public-intake-mixed-case-r1-stage`
- `subject.json`: 173793 bytes, SHA-256 `5b72168b280d43ae0b5f40aefbcb80f96bf6c11ced47d121206086202701dd81`, 664 members. Rehash every member, and rehash `finalSourcePins` in the isolated producer and the `compiledCargoImage` and `closedParentImage` pins in place.

## What to review

A new outside-product module, `candidate/src/cargo/util/context/experimental_public_cache_intake/mixed_case_entry.rs`, beside the closed accepted intake (`closed-parent-reference/`, your review `grok-sm-public-intake-entry-r1`).

1. **Closed body unchanged.** `candidate/` equals `parent/` except the new module and the trailing `mod mixed_case_entry;` line in `experimental_public_cache_intake.rs`.
2. **Semantics.** Compare `intake_mixed_case` line by line with the closed `intake`. The only intended differences: the name rule admits ASCII uppercase; uniqueness is case-folded; the index cache output path is `make_dep_path(lowercased name)` from `cargo_util::registry` (confirm against stock `RegistryIndex::parse`, `src/cargo/sources/registry/index/mod.rs`, which lowers the name before `make_dep_path`); the report adds `mixedCaseIndexes`/`indexCachePathsLowercased`. Index rows must still equal the supplied name exactly, archive names keep the exact published name (stock `tarball_name`), every version still needs an archive, and all validation precedes the first output.
3. **Controls.** `mixed-case-controls-r1.log`: 7 passed, 0 failed, 2 ignored entry tests, no warnings. Retained outputs under `actual-control-outputs/` show (a) lowercase equivalence: closed and variant trees byte-identical, 140 files; (b) actual `Inflector` inputs (`inputs/`, 27 versions, anonymous, whole-checksum matched): index at `.cache/in/fl/inflector`, rows named `Inflector`, 27 `Inflector-*.crate` archives, and the closed intake refuses the same inputs; (c) three refusals (lowered name, case-folded duplicate, unsafe name) with no registry output.
4. **Scope.** No corpus resolution or typecheck, no application/script/proc-macro execution; public acquisition is not source authentication; no native admission, product change, full S-M, effective L or qualification.

Product, law, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on outside-product S-M experiments.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), and exactly these expected fields with your independently checked values (report the actual value and raise a finding if any differs):

```json
{
  "controlsPassed": 7,
  "newControlsPassed": 3,
  "closedRegressionControlsPassed": 4,
  "ignoredEntryTests": 2,
  "mixedCasePublicIndexes": 1,
  "mixedCasePublishedVersionRecords": 27,
  "mixedCaseWholeArchiveChecksumMatches": 27,
  "lowercaseEquivalenceOutputFiles": 140,
  "mixedCaseOutputFiles": 28,
  "refusalControls": 3,
  "closedIntakeRefusesMixedCase": true,
  "closedIntakeBodyUnchanged": true,
  "onlyNewModuleAndRegistrationDiffer": true,
  "indexCachePathLowercasedViaCargoMakeDepPath": true,
  "exactPublishedNameInIndexRowsAndArchiveNames": true,
  "caseFoldedDuplicateRefused": true,
  "lowercaseInputsByteIdenticalToClosedIntake": true,
  "warnings": 0,
  "publicAcquisitionPerformed": true,
  "corpusResolutionRun": false,
  "typecheckExecuted": false,
  "applicationExecuted": false,
  "buildScriptOrProcMacroExecuted": false,
  "sourceAuthentication": false,
  "nativeAdmission": false,
  "productChange": false,
  "SMComplete": false,
  "effectiveL": false,
  "productQualification": false,
  "entirePlanComplete": false,
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "5b72168b280d43ae0b5f40aefbcb80f96bf6c11ced47d121206086202701dd81",
  "supportingOnly": true
}
```

The lead will give its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
