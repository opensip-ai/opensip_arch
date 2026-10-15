# Review request: B2B4-PLAN-r4 (the lead's implementation plan for B2-b4, the T2 census and margin)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4-plan-r4/`).

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

- **Stage.** `/tmp/opensip-implementation/b2b4-plan-r4-stage`
- **Subject file.** `subject.json`: 452 bytes, SHA-256 `e590eb2ca6cae2426056aedf15093f94cd10b12f7679c36ab806256a12cc38f6`, 1 member(s). Rehash every member.
- **Earlier rounds.** Your `codex-b2b4-plan-r2` (ACCEPT, published at architecture `bd50e7b9`) is at `/tmp/opensip-implementation/reviews/codex-b2b4-plan-r2`. Your `codex-b2b4-plan-r3` (REQUIRED-FINDINGS: B2B4PLAN-R3-RF-1 and RF-2, with NBO-1) is at `/tmp/opensip-implementation/reviews/codex-b2b4-plan-r3`. PLAN-r4 is r3 with those resolved, stated in its "r4 changes" section. r3 was plan r2 with a lead amendment of section 2. B2-b4a is bound (product `251e315d`, inventory v196), and its census fails the margin.
- **Bases.** Product `ec2d655d264203cd392b4c690c7627766395ecdf`, clean: B2-b0 to B2-b3 are bound; inventory v195; 164 contract successors. Architecture `a84239c2ea6ca1ded1326d854daa4a98d6e87cc3`: shared r95.

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

0. **Round 3.**
   - **RF-1.** Is it resolved: the size inventory closed by rule (every `size_of` operand an anchored byte formula names), `usize` included, and the planted-formula control?
   - **RF-2.** Is option (c) reframed with derived, not assumed, residual costs, the transient spellings named, and only the successor census setting caps?
   - **NBO-1.** Are the bases labelled?

Judge the amendment, against the accepted plan r2 and B2-b4a's bound evidence (`docs/implementation/m3/config-discovery-b/b2-b4a-r2/`, including `evidence/lead-probe-real-stores.log` and `evidence/lead-probe-tree.diff`):
1. **The facts.**
   - Is the walker's charged storage bounded by item 19, X2:272 or S3, as r2 NBO-1 says?
   - Does its byte charge grow with the root spelling, with project roots spelled up to 4,096 bytes (`crates/platform/src/filesystem/path_binding.rs`, `components`)?
   - Check the charge sites.
2. **B2-b4b1.**
   - Is an affine-in-R byte model, with each formula anchored in the pinned closure, sound?
   - Are the compile-time sizes pinned natively in both crates sufficient?
   - Is the dearer branch in bytes (`FS` over the largest ACL record) sound?
   - Is the byte soundness control, evaluated at the scratch root's own length, sufficient?
   - Are the three reported root lengths sound?
3. **B2-b4b2.**
   - Are options (a), (b) and (c) complete and fairly framed?
   - Is anything missing?
   - Is the rule that caps come only from the census by the 2× rule kept?
4. **B2-b4b3** and the owner question (section 2.4): is a recommendation that changes product behavior beyond the caps raised to the owner?
5. **The rest.** Does section 1, LD-B2B4-1 to 7, stand unchanged?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "e590eb2ca6cae2426056aedf15093f94cd10b12f7679c36ab806256a12cc38f6",
  "r3Rf1Resolved": true,
  "r3Rf2Resolved": true,
  "r3NboAddressed": true,
  "r3FactsAccurate": true,
  "byteCensusSound": true,
  "sizesPinnedNatively": true,
  "affineInRootLengthSound": true,
  "byteSoundnessControlSufficient": true,
  "amendmentOptionsComplete": true,
  "capsNeverInvented": true,
  "ownerQuestionStatedCorrectly": true,
  "section1Unchanged": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
