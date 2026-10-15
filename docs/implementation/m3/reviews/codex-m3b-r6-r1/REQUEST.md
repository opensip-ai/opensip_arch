# Review request: M3-B-r6 (law: item 12's discovery ledger caps, returned by the T2 census)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-m3b-r6-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/m3b-r6-stage`
- **Subject file.** `subject.json`: 440 bytes, SHA-256 `34c1004c1fe9088ba88d7159edf7709305302a494da729308e6e6a71e203bee9`, 1 member(s). Rehash every member.
- **The candidate.** `PROPOSAL-r6.md` is the live law (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, r5 as accepted by Codex in `codex-b1b-plan-r3`) with one revision: item 12's caps and measuring bullets, a new walker-storage bullet, and the matching "Not claimed" line. Its "r6 changes" section states why and weighs the options. Diff it against the live `PROPOSAL.md` yourself.
- **Bases.** Product `84caf3f58d8379c9386fda42a41e5513ac81ebbb`, clean: B2-b4a and B2-b4b1 are bound, inventory is v197. Architecture `86362b0c88450c989badd4ecd4d222b0dc93a412`.

## Authority and evidence

- M3-B r5 item 12 (the live law), which returns the caps to this law when any T2 entry fails the 2× margin.
- The B2-b plan r4 (`b2-b/PLAN-r4.md`, LD-B2B-4) and the B2-b4 plan r4 (`b2-b4/PLAN-r4.md`, section 2.2: the options and the rule that caps come only from the census).
- The bound census units:
  - B2-b4a (`b2-b4a-r2-unit.json`, `b2-b4a-r2/`, including `evidence/lead-probe-real-stores.log`);
  - B2-b4b1 (`b2-b4b1-r2-unit.json`, `b2-b4b1-r2/`);
  - their records in the product at `84caf3f58d8379c9386fda42a41e5513ac81ebbb`: `crates/security/src/custody/discovery_census.json` and `discovery_census_vectors.json`.
- The walker (`crates/security/src/custody/discovery_walk.rs`) and `crates/platform/src/filesystem/path_binding.rs` (`components`).

## What to review

1. **Scope.** Does r6 change only item 12 (caps, measuring, walker storage) and its "Not claimed" line, and nothing else?
2. **The evidence.** Is every figure in "r6 changes" accurate against the bound census records and the probe?
3. **The options.**
   - Is the arithmetic for (a) and (b) correct by the 2× rule?
   - Is (c)'s figure clearly a labelled counterfactual and not evidence?
   - Is anything missing from the options?
4. **The recommendation (c).**
   - Is requiring a walker storage redesign sound: no per-entry absolute spelling, no listed name stored twice, population, evidence and records equal to the reference, charges before allocation?
   - Is it sound that the caps stand provisionally, with no margin claimed, until that successor's census sets them by the rule, recorded with the arithmetic?
5. **The measuring rule.**
   - Is bringing bytes into the census at R = 4,096 sound?
   - Is it sound to add each workspace's member-observation bound (item 19 with X2:272's ceilings)?
   - Is the smallest-power-of-two-at-least-2× rule sound?
   - Is the supersession of r2 NBO-1's sentence stated correctly?
6. **Owner and held-outs.**
   - Is (c), changing no product behavior beyond memory and the caps, correctly a lead decision under plan r4 section 2.4?
   - Does the held-out margin stay outstanding?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "34c1004c1fe9088ba88d7159edf7709305302a494da729308e6e6a71e203bee9",
  "onlyItem12AndItsNotClaimedLineChange": true,
  "evidenceStatedAccurately": true,
  "optionArithmeticCorrect": true,
  "counterfactualLabelledNotEvidence": true,
  "recommendationSound": true,
  "capRuleSound": true,
  "byteCensusRequirementSound": true,
  "memberObservationBoundIncluded": true,
  "walkerStorageRequirementSound": true,
  "provisionalCapsStandWithNoMarginClaimed": true,
  "heldOutMarginStillOutstanding": true,
  "ownerQuestionStatedCorrectly": true,
  "codeWritten": false,
  "bindingMade": false,
  "productQualification": false
}
```
