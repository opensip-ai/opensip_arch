CODEX2 review: M3-C r2, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 2. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r2.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run is using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests or schedules, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. Both files are untracked in arch until acceptance.
- `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r2 law. It is the subject of `subjectSha256`.
- `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r1.md`, the r1 bytes you reviewed (`ff9a5e8d…`), kept for diffing.

Your r1 review is at `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r1/`. The product is `/Users/sb/code/opensip-ai/opensip` at main `30c5db1`, read-only.

## What r2 changes

The "r2 changes" table at the top of PROPOSAL.md maps each finding to its change.

1. **C-R1, ordering (items 16 and 17).** The pre-Plan order is now a fifteen-step table. Each step names what it consumes and the governing text:
   - **The complete analysis-spec** is constructed once and admitted at **step 11**. That comes after sealing (8), the imports (9) and context and universe binding (10), and before the prospective Plan (12) and `plan2` (13).
   - **`EnumerationPlanV1`** is built from the admitted snapshot, boundaries, scope, `UnitMembershipV1`, closures, contexts and universes (`enumeration-contract.v1.md:13-24`, `:83-96`). It never names `planId` or `analysisSpecDigest` (`:15`).
   - **`admit_enumeration`** takes the Plan and PlanId (`:164`), so it runs at step 14, beside the host's `check_plan_pack`.
   - **A step 6 selection precheck** applies NE:4278's order to `requestedCapabilities` alone and mints nothing. It must agree with step 11 (C4-T18). C4-T17 pins the spec bytes: admitted, retained and Plan-bound bytes are identical, with no placeholder.
2. **C-R2, the extraction profile (item 12).** **CRATE-ARCHIVE-1** is a bounded decoder for what Cargo's package writer emits. Cited from docs.rs `latest`:
   - Cargo's `tar` function, `cargo_package/mod.rs:861-944`: `GzBuilder…filename` (:871-874), `Header::new_gnu` (:899), files only, through `append_data` (:910, :934);
   - tar's `builder.rs`: `append_data` (:213-223), `prepare_header_path` and the `L` / `././@LongLink` NUL-terminated record (:836-896), and `finish`'s 1,024 zero bytes (:561-567).

   The profile admits only type `0` and type `L`, under strict long-name rules, with effective-path validation after decoding, and with bounds counted as bytes are produced. An authenticated archive outside the profile is recorded **missing** under DS-6, with a disclosed omission. It is not a `mismatch`, and nothing of it is partially extracted. C3-T6 holds the negative controls and C3-T6a the positive ones. H-DEP runs the decoder at pin time (item 15). R6 asks the C3a implementer to confirm the profile against the pinned Cargo 1.95.0 sources.
3. **C-R3, the observation (item 13).** The wrapper's observation is exactly `{schemaVersion: 1, kind: <wrapper kind>, window: null, population: null, selection: null, revisionRange: null}`, retained and hashed. C3-T22 covers both kinds.
4. **C-R4, the DAG ("Units").** The DAG is recomputed with M3P:198's durations, integration edges, and C2b as a 5-day hard XL part. **M3P's 26-day host chain no longer holds:**
   - **29 days** with C4a unsplit;
   - **28 days** with the recommended split into C4a and an S-sized C4c (prepared-import wiring).

   Each figure states its K2, O2_selected and X12d-lead-set conditions. X12d beside H adds no delay only if its serialized X9 lead set completes inside H's window. M3P-C and the owner flag O-4 carry this.
5. **Non-blocking observations:**
   - **C-N1:** item 1's capture session, under which bootstrap configuration, marker and manifest reads are reused, never re-read, and a change refuses (C1-T24);
   - **C-N2:** item 5's examples are now risk estimates, and S-R must specify its recipe and bounds;
   - **C-N3:** the gate requires M3-L accepted, NIJ-1 (with X-2's disposition) comes before C3a, and R3 before C3c.

## Decide

1. **C-R1.** Does the new order make every input exist before it is consumed?
   - Is step 11's construction consistent with COMP:9, `enumeration-contract.v1.md:13-24`, `:83-96` and `:164`, and NE:4276-4278?
   - Is the step 6 precheck lawful, and does C4-T18 guarantee it cannot diverge from the authoritative admission?
2. **C-R2.** Does CRATE-ARCHIVE-1 admit Cargo's actual output, including long paths, while refusing links, special members, pax and sparse records, ambiguous long names, traversal and duplicates, with explicit bounds?
   - Is "authenticated but outside the profile, so missing (DS-6)" a sound disposition against NE:1666 and NE:1681-1684, NE:1693-1697 and NE:1795-1801?
   - Is anything Cargo emits still excluded?
3. **C-R3.** Is item 13's observation preimage now exact?
4. **C-R4.** Check the recomputed table and both figures, with their conditions. Is the split into C4a and C4c sound, and are the integration edges complete?
5. **C-N1 to C-N3.** Are they adequately absorbed?
6. **Regressions.** Did any r2 edit contradict r1 decisions that you accepted? Those are the walk, the read set, VCS, closures, the detector, the import join, PO, the harness recipes, X12d and the L consistency.

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The contract successors (CRC-1, CR-1, NIJ-1, VCS-1, S-B, S-R, T2-DEP) need `ACCEPT-DESIGN-UNIT` reviews of their own. X12d and the C code units are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Do not commit.
