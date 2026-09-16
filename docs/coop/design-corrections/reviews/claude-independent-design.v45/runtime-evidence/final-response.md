# Source45 review: ACCEPT

**Verdict: ACCEPT.** There is no MUST issue, no SHOULD issue, no blocker and no new advisory. This is source-level acceptance only: it grants no blind reconstruction, application, readiness, implementation authorization or product qualification. Every child command finished and the builder reports no gaps.

**Deliverables:**
- `/private/tmp/opensip-design-corrections/claude-independent-design.v45/review.json`, sha256 `427ae73e715799a5a1375d231d8d5e1022c7eb11c95555b4cf9fd93f79af1f6c`
- `/private/tmp/opensip-design-corrections/claude-independent-design.v45/review.md`, sha256 `841e5163565564395bd52c237f4daf4a82b31d6e5c452743082f870ef07d5f3c`

## Subject
- **Manifest and archive:** manifest `8b4efbb0…` and archive `9536ebe3…` match the header; `verifiedManifest` is true. All 12,920 members (738,315,211 bytes) verify on my copies.
- **Parent and delta:** parent44 `e873c8db…` is declared and verified; the delta is exactly 14 changed, 1 added, 0 removed.
- **Pins:** all 6,264 pin entries match.
- **Copies:** all three working copies re-verified unchanged at the end.

## The correction: pre-analysis `closedWorld`
- **What was missing.** Source44 §9.7 named `closed_world_v2` without publishing its output, so the exact record existed only in the Python helper.
- **What source45 publishes.** The complete record in §9.7 (lines 3241–3261) and as the startup-law member `hostConversionClosedWorld`. It is scoped to this conversion, stated for both languages, and explicitly proves nothing about the absence of dynamic loading or dispatch.
- **Derivation from law, without the helper.** §4.5 and the registered `ClosedWorldV2` schema force three fields: `exportsClosed` unknown, `entryPointsRecognized` none, `deadCodeRepairEligible` false. The other four (`nonliteralLoading` none, `dynamicDispatch` not-applicable, `externalConsumers` unknown, `reasons` ["no-manifest"]) are lawful enum values fixed by the new publication, not forced by §4.5. None of them can enable closed exports or dead-code repair.
- **Both languages, same bytes.** Every minted TS (2 stages) and Rust (1 stage) entry carries exactly the published record and is admitted. The entries and their coverage2 ids are byte-identical to what source44 minted, so no identity changes.
- **Corrected boundary.** The model now copies the published law.
  - Mutating that law in-process on source45 is caught by the updated cases; the equivalent helper mutation on source44 was not caught, which is the gap closed.
  - On a scratch copy, the checker refuses a mutated law member, §9.7 record or helper, each with its exact fault. It passes unmutated and after restore.
- **Consumer effect.** The workflows repair gate stays refused when the only records are pre-analysis conversions. Its non-authoritative display summary can then show `nonliteralLoading: none`; this is recorded as an observation, not a defect.
- **Other changes.**
  - `native-cases` is a whitespace reindent plus two existing cases gaining `closedWorld` expectations. All 125 fixtures and 477 case ids are unchanged, and no case was added.
  - The historical-batch wording is clarified per language in three places. Schema shapes are unchanged; one duplicated word ("Historical the historical") remains.

## Advisories and prior findings
- **ADV42-01: retained, non-blocking.** Its owner files are byte-identical 44→45 and the measurements are unchanged. It remains correctly scoped as a verification obligation for `crates/host/src/analysis.rs`.
- **ADV44-01: retained, non-blocking.** v13 binds the two changed normative inputs (native-evidence.md and the startup schema) and keeps v8–v12 byte-identical. The protocol3 table and fact-batch v3 are still unbound, and neither changed.
- **S40-01 and ADV40-01:** remain resolved.
- **All 46 prior findings, advisories and observations** have current dispositions.
- **Source44 reference limits still apply (OBS45-10).** The reference trusts host inputs, does not check every descriptor field or cancel correlation, recomputes no commitments and exercises no process or compiler. The new probes are a measured subset, not proof.

## Checks
- **Reference groups:** all six pass, and every group output is byte-equal to root, codex and my source44 receipts. 15 of 17 evaluator children are byte-equal to root; the other two differ only in path fields.
- **Planning and inventory:** 322 mappings and 54 planned failure cases; 198 files in 20 packages.
- **Probes:** the 10 ported scope probes and the 162-row startup re-execution are identical to source44. The 130-row wire probe was not re-run because none of its owners changed; it stands as named unchanged-44 basis.
- **Package22:** 34/34. It was rebuilt from package15 plus the native-v2 overlay, with 17 exports, 7 queries and 9 membership probes. All 17 RunIds equal source44 and nothing was reminted. Four TS normalization-map negatives are executed; the Rust negative and partial and/or/not helper are unexercised, count/all are unimplemented and two-binding qualification is incomplete. All 30 grades stay PENDING.

## Rows and obligations
- **107 rows:** 34 new-45 and 73 unchanged-44. Every unchanged-44 row names its governing owners, and those owners are checked byte-identical. Every row has `appliedByThisReview` and `finalApplicationOutcomeGranted` false.
- **TCB-SCOPE-01:** assessed once with 13 dependent rows; not rejected.
- **Obligations:** all 32 gates and 54 recovery cases stay unperformed, and condition 5 is not met. D9 remains a mandatory future implementation obligation. Final application needs a new, different Claude origin.

## Limitations (disclosed in the review)
- **Read map.** Section 9.7 and the startup law were read by full range plus complete diffs, and `native-cases` was compared by parsed structure rather than read as its 57,096-line text diff.
- **Scratch pins.** The checker mutation probe regenerated pins only inside a scratch copy.
- **Harness.** One shell listing was denied and two broad glob searches timed out; each was replaced by exact-path reads.
- **Probe attempts.** No probe attempt failed. The one builder crash was my porting error (reading a key source44 rows don't have); I fixed it and rebuilt.
