# Review request: B2B3D-PLAN-r2 (the lead's plan for B2-b3d, the walker storage redesign)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3d-plan-r2/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3d-plan-r2-stage`
- **Subject file.** `subject.json`: 455 bytes, SHA-256 `02c1b88377e5814be38cac3a8df4942b543c7ee2468f8ea062cd79f34418c8fa`, 1 member(s). Rehash every member.
- **Round 1.** Your `codex-b2b3d-plan-r1` (REQUIRED-FINDINGS: B2B3DPLAN-R1-RF-1 and RF-2, with NBO-1) is at `/tmp/opensip-implementation/reviews/codex-b2b3d-plan-r1`. PLAN-r2's "r2 changes" table maps each to its resolution.
- **Bases.** Product `84caf3f58d8379c9386fda42a41e5513ac81ebbb`, clean: B2-b4a and B2-b4b1 are bound, inventory is v197. Architecture `194fcad1d89f20db50491e3a574342ff608ace50`: law M3-B r6 and shared r97.

## Authority

- Law M3-B r6 item 12, the walker-storage bullet (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`; `codex-m3b-r6-r2`).
- The B2-b4 plan r4, section 2.3.
- The bound B2-b3b walker plan and unit (`b2-b3/PLAN-r3.md`, `b2-b3b-r3-unit.json`), and B2B3B-R1-RF-3 (charges before allocation).
- The B2-b0 reference.
- The product's `custody/discovery_scan.rs`, `custody/discovery_walk.rs` and `custody/project_admission.rs` (`vcs_evidence`, `gitdir_target`, `trace_child`).
- Their tests, and `tools/security/discovery_census.py`.

## What to review

0. **Round 1.**
   - **RF-1.** Is it resolved: only fields holding resolved absolute paths are rebuilt, raw rejected specifications and absent paths are kept unchanged, and every record is byte-identical?
   - **RF-2.** Is it resolved: the bounded, precharged first invalid name; the listing completing; listing failures first; the `ListingConversion` controls?
   - **NBO-1.** Is it addressed by the structural trace check?
1. **The core.** Are root-relative keys sound?
   - Every core read must build relative keys.
   - Every output path stays absolute, rebuilt from the root spelling (the `/` special case kept).
   - The order must be unchanged.
   - Is anything missed?
2. **The walker.** Does the plan remove every per-entry absolute spelling?
   - `Frame`, `listed`, `verdicts`, `spell`, the scope key.
   - Is it sound to keep absolute spellings only for terminal refusal details and the test-only trace (rebuilt from a thread-local root under `cfg(test)`, with `at` passed relative to `trace_child`)?
3. **Names stored once.** Is converting in the visitor sound, with one relative path per child, the name borrowed as its last segment, and a parallel observation vector? Are charges still before every allocation?
4. **The tests.**
   - Are the test changes limited to the redesigned storage (scope keys, the exact charge counts), with every behavioral assertion, vector, trace and record expectation kept?
   - Is the scan runner's relative conversion (dropping keys outside the root) sound?
5. **The census in this unit.**
   - Is regenerating the model, pins and records with the walker sound?
   - Is it sound to retire the old probe cross-check in favor of a new lead probe as supporting evidence, with no margin claimed?
6. **Equality.** Do the population, evidence and records stay equal to the reference, through the unchanged walk and scan vectors?
7. **The new mutations and checks.** Are they sufficient?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "02c1b88377e5814be38cac3a8df4942b543c7ee2468f8ea062cd79f34418c8fa",
  "r1Rf1Resolved": true,
  "r1Rf2Resolved": true,
  "r1NboAddressed": true,
  "implementsLawR6WalkerStorage": true,
  "coreRelativeKeysSound": true,
  "recordsUnchanged": true,
  "walkerNoPerEntryAbsoluteSpelling": true,
  "namesStoredOnce": true,
  "chargesBeforeAllocationKept": true,
  "traceAndRefusalHandlingSound": true,
  "testChangesLimitedToRedesignedStorage": true,
  "censusMovesWithWalkerSound": true,
  "populationEvidenceRecordsEqualReference": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
