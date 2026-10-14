# Review request: B1A-PLAN-r1 (the lead's implementation plan for M3-B unit B1-a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1a-plan-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only file reading, hashing, JSON parsing, source reading and Git queries over both repositories are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1a-plan-r1-stage`
- **Subject file.** `subject.json`: 449 bytes, SHA-256 `c86c2aa060f60fc7a2d48a9aa03f3a0a35ab26ee50b7ee9f7112e63470e93b7a`, 1 members. Rehash every member.
- **Bases.** Product `95279fa8ae086f98bd221cd827f6c0efc156c0c5` (clean); architecture `0deeb0d32fbb6562b975114f806d0c3f49892b3a`.
- **Authority.**
  - M3-B r4 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): items 1 to 11, the units table (MB:870-901) and B-S9.
  - AQ §1 and §1.1.
  - PCS, PCM and its checker (`docs/coop/design-corrections/foundation/`).
  - DRC:585-597.
  - HFC §3.
  - The product's `crates/host/src/configuration.rs`, `crates/identity/src/schema_registry.rs` and `schema.rs`, `crates/host/src/schema_sources.rs`, `schemas/*.json` and `tools/verify_design.py` (`generation_sources`, `admission_sources`).

## Context

M3-L is in effect (r7), so B1-a, the first host-chain unit, may start. This is a plan only, so that design questions are settled before code.

## What to review

1. **Scope.** Does §1 match MB:875 and the B items it names? Is the B1-a/B1-b boundary right (carriers, custody, mode computation and the item 9 environment check are B1-b's)? Is the typed entry point sound?
2. **The prerequisite finding (§2).**
   - Is it true that runtime schema validation uses the admission registry set, and that `verify_design` requires `schemas/admission-registry.json` to equal an accepted architecture copy, so that PCS and the preview v1 carrier cannot be admitted at runtime without a new accepted copy?
   - Is B-S10's form (an admission-registry copy with two rows, as a contract successor bound by its own lock commit) sound, and does it follow the rust3 identity materialization precedent?
   - Are the rejected alternatives rightly rejected?
3. **Registries (§3).** Do they meet MB item 8 (generated or drift-checked, typed refusal)? Check:
   - the classification classes (DRC names), the generator tool and its drift check, and the reuse of the generated recognizer enum;
   - the empty waiver registry, and release-registry admission as an input.
4. **Refusals (§4).** No new code. Is the profile-refusal mapping to `CONFIG.INVALID` with subjects correct, given that no profile detail code exists? Is the host-invariant routing right?
5. **Vectors and tests (§5, §6).** Do they cover MB's controls and AQ:183-187, with PCM as the accepted oracle and no invented expectations?
6. **Scope discipline.** Does it choose no S-OP-5 field, no release content and no B1-b mechanics, and change no law?

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
  "subjectManifestSha256": "c86c2aa060f60fc7a2d48a9aa03f3a0a35ab26ee50b7ee9f7112e63470e93b7a",
  "scopeMatchesMB875": true,
  "b1bBoundaryCorrect": true,
  "prerequisiteFindingReal": true,
  "bS10FormSound": true,
  "registriesPerItem8": true,
  "refusalsNoNewCode": true,
  "vectorsFromAcceptedPCM": true,
  "testsCoverControls": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```

After an ACCEPT, the lead publishes the plan (architecture only), then drafts B-S10. Nothing is pushed.
