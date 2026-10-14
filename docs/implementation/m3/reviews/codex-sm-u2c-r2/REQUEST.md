# Review request: SM-U2C-r2 (U-2c round 2: Rust SM-5 two-part sealing and SM-7 transfer)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-sm-u2c-r2/`).

## Boundaries

Do not edit either repository, the stage, the working directories or control files. Do not run any runner, probe, receiver, image, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Permitted: read-only file reading, hashing, JSON parsing, source reading, Git queries, and extracting the evidence archive into a fresh directory under your own temporary space. You may read the working directory `/Users/sb/code/.opensip-implementation-cache/work-2026-10-14/u2c` (including the `ds/` package clones and `manifests/`), U-2b's records under `/tmp/opensip-implementation/sm-dependency-source-sets-2026-10-14` and `/tmp/opensip-implementation/sm-overlay-metadata-2026-10-14`, and the accepted spikes under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/spikes`.

## Subject

- **Stage.** `/tmp/opensip-implementation/sm-u2c-r2-stage`
- **Subject file.** `subject.json`: 11515 bytes, SHA-256 `dce3a18f069db6add330fbb914c97b0b8d2a6ca4b2f121d71cc8ef1203dcda7a`, 48 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `a49151299650642be278813941c0957e739b3eb7`.
- **Authority.**
  - S-M report plan r3: D-2 (`PLAN-r3.md:60-70`), D-3 (`:72-76`), D-9 (`:113-117`) and the U-2 row (`:123`).
  - NE §3.1-3.2 (`native-evidence.md:1650-1712`), the frame table (`:2876-2879`) and limits (`:2929-2933`).
  - The accepted typed sealing (`s-m-sealing-typed-2026-10-09`) and transfer (`s-m-transfer-2026-10-09`) series.
  - U-2b and its overlay-entry follow-on (your `codex-sm-u2b-r1` and `codex-sm-u2b-entry8-r1` ACCEPTs).
  - `LD-WORKDIR-TMP-EROSION`.

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-sm-u2c-r1`, your REQUIRED-FINDINGS) raised SM-U2C-R1-RF-01 on the SM-7 dependency fields, and NBO-01 on the repository comparison. Round 2 replaces SM-7 with the r3 series and keeps r2 as history. SM-5 and its evidence are unchanged; recheck them only for consistency with round 1. Confirm specifically:
- **RF-01.** Does r3 represent every NE §9.2 manifest, chunk and seal field, and validate the set, package and path association, contiguous chunk indexes and offsets, and the manifest digest? Are the positive and refusal controls adequate for those fields?
- **Disclosure.** Is the `manifestSha256` representation (the canonical payload without that member) disclosed as a lead representation of NE's self-referential description, without a conformance claim?
- **NBO-01.** Does the report state the exact per-row repository differences?

## What to review

1. **SM-5 (r2).**
   - Is the repository part the accepted typed probe's span verbatim?
   - Is the dependency part inside the same timed span, with a sound part split?
   - Are the dependency reads no-follow and checked against the accepted manifests, with identities computed by the reference model?
   - Does every child reproduce the accepted typed repository shape?
   - Is R8 handled per D-3 (overlay union per entry)?
2. **SM-7 (r3).**
   - Is the snapshot phase as accepted, with sealed manifests byte-equal to the accepted transfer?
   - Does the dependency phase carry and check every NE field (manifest with digest, chunks with set, package, path, index and offset, seal, echo) within NE's limits?
   - Are the package keys taken from U-2b's observations?
   - Are the receiver checks and the positive and negative controls adequate?
   - Are disclosures accurate: JSON headers with raw chunk bytes, the `manifestSha256` representation, no protocol conformance, and the receiver's refactored snapshot phase?
3. **Statistics.** Recompute medians, maxima and the R8 two-entry sums from the raw child records in the archive (or the result files), and check them against `u2c-audit-r2.json` and `REPORT.md`.
4. **Bounds.** Is each part reported against its own sourced bounds, with no invented bound, and the descriptor-bytes bound stated as absent?
5. **History and scope.**
   - Are SM-5 r1, SM-7 r1 and SM-7 r2, and the round-1 report and audit, retained and labelled as superseded with accurate reasons?
   - Are the generated-lock sets labelled as stand-ins?
   - Is it true that no S-M value, F or T, placeholder fill, admission or gate claim is made?

O7, D3 and D13 are closed, and only L-G1 remains open.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "dce3a18f069db6add330fbb914c97b0b8d2a6ca4b2f121d71cc8ef1203dcda7a",
  "sm5OneSpanTwoParts": true,
  "repositorySpanVerbatimAccepted": true,
  "repositoryControlsReproduceAccepted": true,
  "sm7SnapshotPhaseAsAccepted": true,
  "dependencyPhaseNeOrder": true,
  "dependencyNeFieldsCarriedAndChecked": true,
  "manifestDigestRepresentationDisclosed": true,
  "nbo01ExactDifferencesStated": true,
  "receiverControlsAdequate": true,
  "statisticsRecomputedFromRaw": true,
  "boundsReportedPerPart": true,
  "r8TwoEntryChildrenSums": true,
  "r1RetainedAsHistory": true,
  "generatedLockLabelled": true,
  "protocolConformanceClaimed": false,
  "sourceAuthentication": false,
  "importAdmission": false,
  "SM5PlaceholderFilled": false,
  "SM7PlaceholderFilled": false,
  "SMComplete": false,
  "LG1Met": false,
  "effectiveL": false,
  "productQualification": false
}
```

The lead will then give its own exact assent and run fresh design verification before an architecture-only publication. Nothing is pushed.
