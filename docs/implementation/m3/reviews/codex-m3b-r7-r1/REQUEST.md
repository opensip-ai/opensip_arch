# Review request: M3-B-r7 (law: the recording revision of item 12's discovery ledger caps)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-m3b-r7-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/m3b-r7-stage`
- **Subject file.** `subject.json`: 440 bytes, SHA-256 `fa285053e588e1a0713deb307e94f9dc343565a60cdb4909862f9f203ab6e737`, 1 member(s). Rehash every member.
- **The candidate.** `PROPOSAL-r7.md` is the live law (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, r6 as you accepted it in `codex-m3b-r6-r2`) with one recording revision. Item 12's caps bullet records the caps, and the "Not claimed" line follows. Its "r7 changes" section gives the inputs and the arithmetic. Diff it against the live `PROPOSAL.md` yourself.
- **Bases.** Product `79c816096310711663104a5e9217717718f8f510`, clean: B2-b3d is bound. Architecture `230c7df884a5584911aab0daf9af03369fd5cb78`.

## Authority and evidence

- Law M3-B r6 item 12: the rule (the smallest power of two at least twice the largest censused entry, bytes at R = 4,096) and the requirement that the caps be written in by a recording revision that shows the arithmetic.
- The bound B2-b3d unit (`config-discovery-b/b2-b3d-r2-unit.json`, `b2-b3d-r2/`), including its lead probe evidence.
- The census record in the product at `79c816096310711663104a5e9217717718f8f510`: `crates/security/src/custody/discovery_census.json`.

## What to review

1. **Scope.** Does r7 only record the caps (item 12's caps bullet, its "r7 changes" section and the "Not claimed" line), deciding nothing new?
2. **The inputs.** Are the largest objects, edges and bytes (at R = 4,096) exactly the bound census record's maxima over the lead-readable repository entries and workspace rows?
3. **The arithmetic.** Does r6's rule give 2^22 objects, 2^21 edges and 2^30 bytes? Are the stated margins right?
4. **Outstanding.** Do workspace full-ledger margins (until B3-b's bound) and the held-out margin stay outstanding?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "fa285053e588e1a0713deb307e94f9dc343565a60cdb4909862f9f203ab6e737",
  "recordingRevisionOnly": true,
  "onlyItem12CapsAndNotClaimedLineChange": true,
  "inputsMatchBoundCensus": true,
  "arithmeticByR6Rule": true,
  "capsRecorded": {
    "objects": 4194304,
    "edges": 2097152,
    "bytes": 1073741824
  },
  "workspaceAndHeldOutStillOutstanding": true,
  "codeWritten": false,
  "bindingMade": false,
  "productQualification": false
}
```
