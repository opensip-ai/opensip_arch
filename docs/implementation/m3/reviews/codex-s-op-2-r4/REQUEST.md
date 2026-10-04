Codex review: **S-OP-2 r4**, the safe event vocabulary and sink law, a contract-successor proposal for the DR-125 owners (`docs/implementation/m3/operability/PLAN.md:408`). Claude Opus 5.5 leads, and you are the single reviewer. This is a law and contract-soundness review, round 4. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- This is a law review, so run no product builds, cargo or tests. The lead keeps the native lane.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the 413 fixture.
- If you compute digests, bounds or interleavings, use read-only scratch scripts under your review directory.

## Subject

- **The subject:** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, r4.
- **The previous revision:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r3.md`. It is byte-identical to your r3 subject (`75a87d78…`, 103,714 bytes). Your r3 review is in `/tmp/opensip-implementation/reviews/codex-s-op-2-r3/`. `PROPOSAL-r1.md` and `PROPOSAL-r2.md` are the earlier subjects.
- **Pins:** `hashes.txt` pins all four revisions, plus the context files.
- **The product:** `/Users/sb/code/opensip-ai/opensip`, read-only. Every cited product file is unchanged since `3d2d5b5`.

r4's "r4 changes and review responses" table maps SOP2-R3-01, -02 and SOP2-R3-NB-01 to -04 to the items that change. Where your fixes offered a choice, the lead's preferences were taken.

**R3-01: read-back predicates.**
- **K12** inherits `LogicalPath` (`common-v4.schema.json:101-110`; IE:161-163). Both the path and the elided tail exclude backslash, and segments are 1–255 scalar values. `..note` and `...` stay valid.
- **K6 (lead decision).** The reader has no workspace. A persisted K6 `file` is accepted only if it is `external` or a member of a census retained in the descriptor set: the running release's, or an earlier release's retained by its pin. Otherwise the field is dropped and never echoed.
- **Whole-value matching.** Every grammar is matched against the whole decoded value, with `$` as the true end, as the pinned `(?![\s\S])` (IE:65-76). The header identities use the pinned patterns verbatim.
- **V at read-back.** Encoded length is checked against V.

**R3-02: the summary is derived from authoritative commit cells** (lead preference). Every disposition is committed by one atomic operation on its cell, and that operation is its linearization point:
- a producer drop is a tally increment;
- a record pending for a stage is an enqueue-tally increment, made before its push;
- writer outcomes are one atomic exchange of an immutable cumulative snapshot per sink;
- the marker outcome is a compare-and-swap.

At the freeze the finalizer reads, in order: the in-flight count F, the snapshots, the enqueue tallies, then the drop tallies. Per sink, `drain-abandoned` = enqueue tally − snapshot outcomes, so pending records become abandoned and each is counted once. Counters other than these cells are gauges only. `in_flight_at_freeze` (F) discloses calls not yet committed.

**One adaptation of the lead's "scan the cells" preference.** Per-record cells kept until the freeze would be unbounded in a long command, and folding them into totals would reintroduce the two-step gap. So the cells are per sink and per tally, under the same rule. Item 16 records the rejected alternatives.

## Decide

1. **Resolution.** Is each of SOP2-R3-01 and -02 resolved? Are SOP2-R3-NB-01 to -04 adequately taken up?
2. **Predicates (R3-01).**
   - Are K12's path and tail predicates now exactly `LogicalPath`-consistent?
   - Is the retained-census rule for K6 sound, and is dropping the field (rather than rewriting it to `external`) right?
   - Is the whole-value rule, with the verbatim identity patterns, sufficient for every grammar in the proposal, including items 2, 3 and 5?
   - Is the V check at read-back correct?
3. **Accounting (R3-02).** Probe the commit cells for an interleaving that loses or double-counts a disposition committed before the freeze. In particular:
   - a writer paused before or after its snapshot exchange;
   - a producer paused between a failed reservation and its drop increment;
   - a producer paused between its enqueue increments and its push, including between two sinks' increments;
   - the pre-scope buffer's `unpersisted` derivation against the file snapshot's taken count;
   - the read order (F, snapshots, enqueue tallies, drop tallies) and the non-negativity of the subtraction.

   Is `in_flight_at_freeze` a sound upper bound for calls that entered before the cutoff? Is the bounded-cell adaptation an acceptable realization of "derive from cells, never from separately incremented counters"?
4. **Marker.** Is the marker cell's state machine (`not-attempted`, `attempted`, `written`, `failed`, `suppressed`; at the freeze, `skipped` and `unconfirmed`) consistent, and is `unconfirmed` now defined by observable state?
5. **Re-admission counts (NB-02).** Are the input checks and the output recomputation of `truncated` and `omitted` correct?
6. **New or changed text.** Did r4 introduce any new error? Does it change anything beyond its table? Does it still stay out of S-OP-1, -5, -6, -7, -9, -10 and -12, O4, O7 and O9?
7. **Controls.** Do C-4, C-5, C-7 and C-9 include every case your r3 review asked for?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"findingResolution"`: one entry for each of SOP2-R3-01 and -02;
- `"requiredFindings"`: an array, empty on acceptance. Each finding has `id`, `location`, `problem`, `evidence` and `fix`;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: a single string, r4 PROPOSAL.md's sha256 as pinned in `hashes.txt`.

r4 has no verify_design subject manifest, because item 24 defers recording, so this verdict is on the successor text. The later recording unit will need its own `ACCEPT-DESIGN-UNIT` with a single-string `subjectManifestSha256`. This is not an inventory unit, so give no `inventoryCandidateAssessment`.

Do not commit.
