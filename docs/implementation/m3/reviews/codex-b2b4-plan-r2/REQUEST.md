# Review request: B2B4-PLAN-r2 (the lead's implementation plan for B2-b4, the T2 census and margin)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b4-plan-r2/`).

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

- **Stage.** `/tmp/opensip-implementation/b2b4-plan-r2-stage`
- **Subject file.** `subject.json`: 452 bytes, SHA-256 `788de3abab231fa9e280eecf40b864cab2a46218b1c5e172b05e6921767eb1b3`, 1 member(s). Rehash every member.
- **Round 1.** Your `codex-b2b4-plan-r1` (REQUIRED-FINDINGS: B2B4PLAN-R1-RF-1 to RF-3) is at `/tmp/opensip-implementation/reviews/codex-b2b4-plan-r1`. PLAN-r2's "r2 changes" table maps each finding to its resolution.
- **Bases.** Product `02fd45c813e2b1e87b086cdef4ecac1aacfbb867`, clean: B2-b0 to B2-b3 are bound; inventory v195; 164 contract successors. Architecture `e0fe80bc56458c9d119a125dbcde5f98e526359d`: shared r95.

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

0. **Round 1.**
   - **RF-1.** Is it resolved by the composed-checkout census through the same model, the composed-workspace native vectors and the member-sum mutation?
   - **RF-2.** Is it resolved by integrity refusing a `.git` component (no T2 walk reads), the uninterrupted read envelope for the vectors with interrupted retries excluded and stated, and the controls?
   - **RF-3.** Is it resolved by the whole-file pinned closure (including `path_binding.rs` and `trust/initial_platform.rs`), the charge inventory, and the delegated-drift and planted-charge controls? Check the inventory against the code yourself.
1. **Scope.** Does the plan refine plan r4 section 1.4 without changing its gate? Is B2-b still incomplete until the all-entry margin holds?
2. **Integrity.** Is the store re-verification sound and complete: both pins recomputed from stored bytes, no-follow, the exact population (gitlink placeholders included), and refusals?
3. **Held-outs.** Is the held-out guard sound: never stat or join a held-out store, and a planted-digest control?
4. **Population.** Is reusing the walk-vector adapter and the bound reference's `walker_population` and `finish` sound, with no new rule?
5. **The cost model.**
   - Are objects and edges a true upper bound of the walker's charges?
   - Are the unknowns taken at their dearer branch: captures, the FS branch, dot entries, `.git` reads?
   - Is pinning by anchored source matches sound?
   - Is anything the walker charges missing? Check the charge sites yourself.
6. **Soundness control.** Is the native comparison on the 52 walk vectors (used no more than the model), with the three model mutations, sufficient to catch an under-counting model? Is rejecting a native walk of the stores sound?
7. **Workspaces.** Is charging a workspace as its members' sum plus the overlay root an upper bound on a real workspace walk?
8. **The failing outcome.** Is landing a failing census, with no margin claimed for a failing row and the caps returned to the law, sound? Is the B2-b4b path sound: an item-12-only amendment derived by the law's own 2× rule, the held-out headroom left open, and the cheaper-walker alternative weighed in the amendment? Is the owner question stated correctly?
9. **The estimate.** Is it labelled as an estimate and not used as evidence? Does your own check (optional) agree in order of magnitude?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "788de3abab231fa9e280eecf40b864cab2a46218b1c5e172b05e6921767eb1b3",
  "r1Rf1Resolved": true,
  "r1Rf2Resolved": true,
  "r1Rf3Resolved": true,
  "refinesPlanR4Section14": true,
  "integritySound": true,
  "heldOutsNeverRead": true,
  "populationFromBoundReference": true,
  "costModelUpperBoundSound": true,
  "constantsPinnedFromCode": true,
  "nativeSoundnessControlSufficient": true,
  "workspaceTreatmentSound": true,
  "failingCensusHandlingSound": true,
  "lawRevisionPathSound": true,
  "preCensusEstimateLabelledNotEvidence": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
