# Review request: B3A-PLAN-r1 (the lead's implementation plan for M3-B unit B3-a, grants.rs)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3a-plan-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b3a-plan-r1-stage`
- **Subject file.** `subject.json`: 448 bytes, SHA-256 `ddd2790c7cb77bebf46f55e717b276ede7134c09ff90225e6def6fad7894a3bc`, 1 member(s). Rehash every member.
- **Bases.** Product `ec70009de1490449a6173c238a7eaf0a03e106c4` (clean: B1-a and B1-b are bound, inventory v189), architecture `127a6429fd378957c9621bbb65cc73a18bcc0ad4`.
- **Authority.**
  - M3-B r5 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): item 23 and item 8's shared-flags row, and the B3-a units row.
  - SL S3 (SL:120-130), S3.1 (SL:317-331) and SL:1110.
  - SLM `storage_write_admission` (SLM:3104-3128) and the waiver rules (SLM:632-680, SLM:832-833).
  - SLS `authorizedGroupIds`.
  - NE:4276, the bounded selection fields.
  - CINV `sharedFlags`, and CH14:401.
  - The product's `crates/host/src/invocation.rs` (`RequestFlags`, `AnalysisRequest`, `Durability`), `crates/security/src/custody/project_chain.rs` (`ProjectChainPolicy`) and `crates/security/src/initial_installation.rs` (`BackupClassification`).

## What to review

The plan fixes how B3-a is built before any code exists. Judge:
1. **Scope.** Does it match MB item 23's `grants.rs` M3 scope (in scope, reserved and forbidden) and the B3-a row?
2. **Facts.** Are section 0's facts accurate at the product base?
3. **The four records.**
   - Are the constructors sound, from parsed invocation input only, with no configuration path?
   - Are the refusals right, including the existing `PROJECT.EXPLICIT_PATH_INVALID` row for the waiver without `--project`?
   - Is the applicability left to its consumers, as documented?
4. **The S3.1 choice function.** Is it an exact mirror of SLM `storage_write_admission`, in order, with the existing codes?
5. **The lead decisions.**
   - LD-B3A-1: reusing J2a's `--ephemeral` selection.
   - LD-B3A-2: the 64-group bound's public row is left to M4, without extending NE:4276.
   - LD-B3A-3: duplicates collapse.
6. **Section 3's controls.** Are they sufficient? That includes the compile-fail and pin controls for "no configuration constructor", and the S3.1 byte vectors.

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "ddd2790c7cb77bebf46f55e717b276ede7134c09ff90225e6def6fad7894a3bc",
  "scopeMatchesMBItem23AndB3aRow": true,
  "factsSection0Accurate": true,
  "recordsAndConstructorsSound": true,
  "noConfigurationConstructor": true,
  "s31ChoiceMirrorsReference": true,
  "ldB3A1Sound": true,
  "ldB3A2Sound": true,
  "ldB3A3Sound": true,
  "controlsSufficient": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
