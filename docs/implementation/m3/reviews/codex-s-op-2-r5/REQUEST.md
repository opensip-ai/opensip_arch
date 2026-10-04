Codex review: **S-OP-2 r5**, the safe event vocabulary and sink law, a contract-successor proposal for the DR-125 owners (`docs/implementation/m3/operability/PLAN.md:408`). Claude Opus 5.5 leads, and you are the single reviewer. This is a law and contract-soundness review, round 5. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r5.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- This is a law review, so run no product builds, cargo or tests. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, bounds or interleavings, use read-only scratch scripts under your review directory.

## Subject

- **The subject:** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, r5.
- **The previous revision:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r4.md`. It is byte-identical to your r4 subject (`db10e19c…`, 117,310 bytes). Your r4 review is in `/tmp/opensip-implementation/reviews/codex-s-op-2-r4/`. `PROPOSAL-r1.md` to `PROPOSAL-r3.md` are the earlier subjects.
- **Pins:** `hashes.txt` pins all five revisions and the context files. The M3 plan is now pinned as the accepted r4 bytes (`M3-PLAN-r4.md`) and the accepted r6 bytes (`M3-PLAN-r6.md`), not the live file (your SOP2-R4-NB-02).
- **The product:** `/Users/sb/code/opensip-ai/opensip`, read-only. Every cited product file is unchanged since `3d2d5b5`.

r5's "r5 changes and review responses" table maps SOP2-R4-01 to -03 and SOP2-R4-NB-01 and -02. All three required fixes follow the lead's decisions.

**R4-01: partition by source** (items 16 and 17).
- **One source per file projection.** The producer reads a one-way "file admitted" flag once. It counts each file projection in exactly one source tally: `E_pre` if the flag is clear, `E_direct` if it is set.
- **Two partitions in one snapshot.** The file writer's single atomic snapshot carries both:
  - **direct:** direct outcomes `O_direct`;
  - **pre-scope:** the pre-scope transfer count `T`, with pre-scope outcomes `O_pre`.
- **A transfer is not an outcome.**
- **At the freeze:**
  - `drain-abandoned` (direct) = `E_direct − O_direct`;
  - `drain-abandoned` (pre-scope) = `T − O_pre`;
  - `E_pre − T` counts as `unpersisted` if the flag is clear, and as `drain-abandoned` otherwise.
- **Proof.** Item 16 gives the three disjoint pre-scope classes, the non-negativity argument (`O_direct ≤ E_direct`; `O_pre ≤ T ≤ E_pre`) and the handoff pauses.

**R4-02: the marker's CAS is its admission** (item 17).
- **The writer's path.** It CASes `not-attempted → attempted`, and that CAS is the admission. Only then does it load the gate:
  - if the gate is closed, it CASes `attempted → suppressed` and issues no syscall;
  - if the gate is open, it writes and records completion by CAS.
- **A lost first CAS.** If its first CAS loses to the finalizer's `skipped`, no syscall is ever issued.
- **The finalizer's path.** `not-attempted → skipped`, then `attempted → unconfirmed`.
- **The rest.** A table gives every losing path, and the outcome meanings are defined by what the cell recorded by the freeze.

**R4-03: path suffixes** (item 13c).
- **Unchanged for every grammar:** whole-value matching and no trimming.
- **Refused only where excluded.** A trailing LF, CR or space is refused only where the grammar excludes it (identities, code members, header codes, K4–K6, K9, K10, K14, K15).
- **K12 keeps `LogicalPath`'s lawful suffixes,** encoded by rule E.
- **Controls.** C-4 and C-5 add positives; the negative identity, K1 and K14 cases stay.

## Decide

1. **Resolution.** Is each of SOP2-R4-01 to -03 resolved? Are SOP2-R4-NB-01 and -02 adequately taken up?
2. **Pre-scope partition (R4-01).**
   - Does every file projection now land in exactly one source tally, including a producer that reads the flag just before the capability is granted and pushes after the writer's first transfer pass?
   - Is each derived quantity non-negative under the stated read order (F, flag, snapshots, enqueue tallies, drop tallies)?
   - Is each pre-scope record counted exactly once?
   - Do C-7's handoff cases cover the pauses before and after the publication of `T` and before the outcome?
3. **Marker (R4-02).**
   - Is the protocol complete, with every losing path and no syscall without a won admission?
   - Are `skipped` (no admission recorded by the freeze, and never a later syscall) and `unconfirmed` (admitted, no completion recorded) defined by observable state?
   - Is the residual, an admitted marker issuing after the gate closes, correctly referred to S-OP-7?
4. **Suffixes (R4-03).** Is the per-grammar statement correct for every grammar? Do the positive and negative cases match it?
5. **New or changed text.** Did r5 introduce any new error? Does it change anything beyond its table? Does it still stay out of S-OP-1, -5, -6, -7, -9, -10 and -12, O4, O7 and O9?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"findingResolution"`: one entry for each of SOP2-R4-01 to -03;
- `"requiredFindings"`: an array, empty on acceptance. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: a single string, r5 PROPOSAL.md's sha256 as pinned in `hashes.txt`.

r5 has no verify_design subject manifest, because item 24 defers recording, so this verdict is on the successor text. The later recording unit will need its own `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. This is not an inventory unit, so give no `inventoryCandidateAssessment`.

Do not commit.
