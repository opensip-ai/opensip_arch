# Review request: D2B-0-r2 (the successor schema materialization, D2b plan r3 sub-unit D2b-0), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b-0-r2/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds, generators or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing, Git queries, and these read-only commands:
  - `python3 -I -B tools/check_operability.py source --repository .` in the candidate worktree;
  - `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/supervisor-d/d2b-0-r2/evidence/check_d2b0_preflight.py /dev/stdout`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d2b-0-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 46093 bytes, SHA-256 `3c74788cab3b6b92b03446a3007e082ac7ba52475c64b2a4c13795c48e0edb8d`, 167 members. They are the contract successor record `d2b-0-r2/successor.json` and its candidates exactly, including round 1's `d2b-0-r1/admission-registry.json`, the architecture copy the unchanged product admission source map selects. Rehash every member.
- **Bases:** product `23b3871269c6553c96097084dd412b3aa95dec68` (the package base) and architecture `ae83833d05d956a0562e188f0ad04fc37a63944b`, unchanged from round 1.
- **Candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d2b0`, unchanged from round 1: the same nine paths, byte for byte. `product-map.json` pins them.
- **Your round 1:** `codex-d2b-0-r1`, archived at `docs/implementation/m3/reviews/codex-d2b-0-r1/`. Its verdict was REQUIRED-FINDINGS (D2B0-R1-RF-1), with productCodeAssessment ACCEPT-UNIT and amendmentLDD2B0A REJECT. Round 1's subject (`d2b-0-r1-subject.json`, `8b5f799c…`) and package are frozen history.
- **Read first:** `d2b-0-r2/SCOPE.md`'s "Round 2" section and its revised LD-D2B0-A.

## What to review

1. **The revised LD-D2B0-A against D2B0-R1-RF-1.** Check:
   - **That it is a deferral only.** It permits no hand-written carrier for either successor payload, and states that M3-D item 10 (`supervisor-d/PROPOSAL-r5.md`:381) and both accepted materialization maps' generated-carrier requirements are **not amended**.
   - **That nothing is waived:** the new sub-unit D2b-0b owes the generator's pattern-profile extension (a reviewed generator-input change), the source-map, generation-registry and options rows (LD-D2B0-1 to 4 re-made there), the regenerated carriers and the reviewed blind refresh.
   - **That D2b-0b is ordered before D2b-3 and D2b-4:** they depend on it, and it is integrated before either consumes a successor payload.
   - **Each quoted D2b plan r3 passage and its replacement.** §0's codec requirement (:54) is now left unreplaced.
   - **That every closure change is still followed by the refresh**, and that LD-D2B-2, the codecs' schema checks, protocol separation and no-serde decoding are unaffected.
2. **The carried-over assessments.** The product candidate, LD-D2B0-5 to 8, lane attempt 3 and the post-rebase check are unchanged. Confirm that your round 1 productCodeAssessment (ACCEPT-UNIT) and your judgments of them carry over.
   - Check `product-map.json` and the evidence against round 1's.
   - The r2 record's candidates now include round 1's admission-registry copy, and drop a duplicate.
   - The checks list now says that the identity `schema_registry` filter matches no test, as you noted.
3. **No regression** from round 1.

Write `review.json` as `{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "productCodeAssessment": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "amendmentLDD2B0A": "ACCEPT" | "REJECT", "subjectManifestSha256": "3c74788cab3b6b92b03446a3007e082ac7ba52475c64b2a4c13795c48e0edb8d", "requiredFindings": [...], "nonBlockingObservations": [...], "blindReceiptStaysCurrent": true | false, "generatorInputsUnchanged": true | false, "productQualification": false}`. Use ids `D2B0-R2-RF-n` and `D2B0-R2-NBO-n`. `ACCEPT-DESIGN-UNIT` requires an empty `requiredFindings` list and `amendmentLDD2B0A: "ACCEPT"`. Accepting the unit accepts the amendment.
