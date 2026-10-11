# Review request: SM-SUI-SCOPE-SERIES-r1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/grok-sm-sui-scope-series-r1/`).

## Boundaries

Do not edit either repository, the stage, or any control files. Do not run the compiler, Cargo, tests, or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, or held trees. Do not use other panes and do not delegate. Read-only hashing, JSON parsing and Git queries are permitted.

## Subject

- Stage: `/tmp/opensip-implementation/sm-sui-scope-series-r1-stage`
- `subject.json`: 19496 bytes, SHA-256 `f340b938192575e863fafb523dd0ed429719f30e17c312c2ce06c8a259f127f3`, 108 members. Rehash every member.
- Bases: product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean), architecture `cfabb1182bb6c48216ffb42911d67b53bb0b4969` ( it adds the accepted HTTP fuzz series publication on top of `849ad122a`).

## What to review

Forty NEW preliminary Sui subject-scope derivations over 3318 nonempty Rust subjects drawn from 19063 original regular Sui source files. Four actors: two independent host recipes (host-a, host-b), a separate prototype worker process repeating the second implementation, and the closed actual Rust helper. Each actor ran 3 warmups and 7 measured samples.

Claims to check:

1. All 40 children produce identical complete subject arrays, scope and domain commitments, and raw CBOR bytes.
2. The raw-output, statistical, native wait4 RSS and child-priority audits pass. Recompute the per-actor median and max from the raw outputs.
3. Sui preparation is permitted by the owning accepted SP. The original 2 non-regular exclusions are retained. The original pinned input rows and the synthetic manifest / illustrative request-domain vector preparation are retained.
4. The closed eleven-read-set parent recipes, helpers and controls stay closed: no replay, no rebuild, no new recipe. All `closedExecutionPins` in `source.json` match.
5. Scope of the claim: this is not an accepted transport manifest, not a validated C2 value, and not an operational native worker. Timed reconstruction excludes input parsing. Process RSS is informational Darwin bytes, not physical scratch. Full SM12/SM14, effective L, native admission and qualification remain open.

Product, law, lock, inventory 187 and contracts 161 are unchanged. O7, D3 and D13 are closed. Native production admission is not an extra gate on this outside-product experiment.

## Output

`review.json` must carry `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`), `requiredFindings` (array), `subjectManifestSha256`, `supportingOnly`, and exactly these expected fields with your independently checked values (report the actual value if any differs, and raise a finding):

```json
{
  "subjects": 3318,
  "originalRegularSourceRows": 19063,
  "pythonChildren": 30,
  "rustHelperChildren": 10,
  "totalChildren": 40,
  "measuredActors": 4,
  "warmupsPerActor": 3,
  "measuredSamplesPerActor": 7,
  "allArraysScopeDomainAndCborMatch": true,
  "rawAuditsPassed": true,
  "originalSuiPreparationPermittedByAcceptedSP": true,
  "newCompilerSource": false,
  "newRecipeImplementation": false,
  "closedControlsRerun": false,
  "applicationExecuted": false,
  "heldOutSourceOpened": false,
  "actualAcceptedTransportManifest": false,
  "actualNativeWorker": false,
  "coverageKeysValidatedC2Values": false,
  "physicalPeakScratchMeasured": false,
  "sourceAuthentication": false,
  "nativeAdmission": false,
  "SM12FigureComplete": false,
  "SM12PlaceholderFilled": false,
  "SM14FigureComplete": false,
  "SMComplete": false,
  "effectiveL": false,
  "productChange": false,
  "productQualification": false,
  "entirePlanComplete": false,
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "f340b938192575e863fafb523dd0ed429719f30e17c312c2ce06c8a259f127f3",
  "supportingOnly": true
}
```

The lead will provide its own exact assent and run fresh design and implementation verification before an architecture-only publication. Nothing is pushed.
