# Review request: B2B4-PLAN-r6 (the lead's implementation plan for B2-b4, the T2 census and margin)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4-plan-r6/`).

## Boundaries

- Do not edit either repository, the stage or control files.
- Do not run Cargo, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay** (the manifest's `heldOut: true` rows). You may read the manifest itself.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - no-follow name counting (`os.lstat`, `os.scandir`, `os.walk` with `followlinks=False`) of the **lead-readable** stores under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store/<treeDigest>/` and the overlays under `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/workspaces/`, if you want to check the plan's estimate.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b4-plan-r6-stage`
- **Subject file.** `subject.json`: 658 bytes, SHA-256 `718a0e7103e52412d8b7a65f6b1839652f7d34122fd91e8fd810875ac5620212`, 2 member(s). Rehash every member.
- **Earlier rounds.** Your `codex-b2b4-plan-r4` (ACCEPT, published at architecture `6d9bcfd9`) is at `/tmp/opensip-implementation/reviews/codex-b2b4-plan-r4`; your `codex-b2b4-plan-r5` (REQUIRED-FINDINGS: B2B4PLAN-R5-RF-1 and RF-2, with NBO-1) is at `/tmp/opensip-implementation/reviews/codex-b2b4-plan-r5`. PLAN-r6 is r5 with those resolved (its "r6 changes" table). r5 was r4 with section 2.5 (B2-b4c) and LD-B2B4-10, implementing the owner's decision recorded verbatim in `docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md` (in this subject).
- **Bases.** Product `d33df45ac0a5422efbebb43eee9c652d17ee742a`, clean: B2-b3d and B2-b4b3 are bound; inventory v198; 164 contract successors. Architecture `de2388edc19dec8c7ed2bffd0ceef2314d86cddc`: shared r98.

## Authority

- The accepted B2-b plan r4 (`docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`): section 1.4, LD-B2B-4 and the sequence.
- M3-B r5 item 12 (`docs/implementation/m3/config-discovery-b/PROPOSAL-r5.md:389-400`): the provisional caps, the 2× margin rule, and the caps' return to the law.
- The B2-b3 plan r3 (`config-discovery-b/b2-b3/PLAN-r3.md`): LD-B2B3-5 and its note that B2-b4 pins the costs from the code.
- The bound B2-b0 reference (`config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py`) and its `walker_population`.
- The product's charge sites:
  - security: `custody/discovery_walk.rs`, `custody/project_admission.rs`, `custody/project_chain.rs`;
  - platform: `filesystem/directory_open.rs`, `filesystem.rs`, `filesystem/descriptor_acl_capture.rs`, `filesystem/descriptor_filesystem.rs`, `work_reader.rs`, `work_ledger.rs`.
- The walk vectors and their tool: `crates/security/src/custody/discovery_walk_vectors.json` and `tools/security/discovery_walk_vectors.py`.
- The T2 manifest (`docs/implementation/m3/corpus/t2-corpus-manifest.draft.json`) and the acquisition record (`docs/implementation/m3/corpus/t2-acquisition-2026-10-06-r1/`).

## What to review

0. **Round 5.**
   - **RF-1.** Is it resolved by the bound receipt, the ordinary mode composing only from a current valid receipt, staleness on drift, the permitted top-level updates, and the lifecycle controls?
   - **RF-2.** Is it resolved by the closed row formats, exact coverage, the four top-level states, and the error, invalid-receipt and canary controls?
   - **NBO-1.** Are the quotation and the bases corrected?
1. **The owner record.** Is it a faithful verbatim record of the owner's answer, inferring nothing?
2. **Fidelity.** Does section 2.5 implement exactly what the owner chose: a Codex-reviewed held-out mode the lead runs without seeing contents, reporting only pass/fail and per-mille margins, reviewed before and after?
3. **Non-disclosure.**
   - Is the set of emitted fields minimal and sufficient?
   - Is anything in the record, stdout, stderr or a log able to disclose held-out content (paths, names, counts, sizes, exception text)?
   - Is the separate guarded join sound, with the ordinary path still refusing held-outs?
   - Are errors reduced to classes?
4. **Equivalence.** Are the integrity, population, model and caps the same as the lead-readable census?
5. **The controls before the run.** Are the planted-store controls sufficient?
6. **The classification.** Is `passes2x` exactly when every per-mille margin is at least 2,000 equivalent to fitting twice, given floor division?
7. **A failing entry.** Is handling a failing held-out entry sound?
8. **The rest.** Do sections 1 to 2.4 stand?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "718a0e7103e52412d8b7a65f6b1839652f7d34122fd91e8fd810875ac5620212",
  "r5Rf1Resolved": true,
  "r5Rf2Resolved": true,
  "r5NboAddressed": true,
  "ownerRecordVerbatim": true,
  "implementsTheOwnersChoice": true,
  "nothingButPermittedFieldsEmitted": true,
  "separateGuardedJoin": true,
  "errorsReducedToClasses": true,
  "sameChecksAsLeadReadableCensus": true,
  "reviewBeforeAndAfterRun": true,
  "blindRowClassificationSound": true,
  "failingHeldOutHandlingSound": true,
  "sections1To24Unchanged": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
