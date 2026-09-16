All 12 items are resolved in my own copy of source38. Workflow-projection, query-projection, current-profile, composition, replay, comparison-knowledge, semantic-replay, evaluator-faults, workflows-v1 and integration all pass on the final tree. One focused checker, the security owner launcher, did not run (explained below). There are two measured gaps I did not close (R1, R2), plus three major-version decisions that are yours.

**Scope and custody.** The copy is independent. At start the parent matched its manifest `2ddfa0db…`, all 12,904 files. At the end it still matched for every touched and dependency file.
- 21 files changed; nothing added or removed.
- Full diff: `diffs/source38-to-corrected.diff`, 2,048 lines.
- No Python was made normative; every rule is in the prose and schemas.
- No pins, planning, grades, commit or push.

**Focused checks on the final tree** (baseline on the unmodified copy → final):

| Checker | Baseline | Final |
|---|---|---|
| workflow-projection | 493 | 585 |
| query-projection | 193 | 202 |
| current-profile | 22 (run read-only on the parent) | 36 |
| composition | 20 | 30 |
| replay | 68 (run read-only on the parent) | 73 |
| comparison-knowledge, semantic-replay (30), evaluator-faults (41), workflows-v1, integration (412) | pass | pass |

The security owner launcher did not execute: its source-pin check refuses because the 21 changed files are pinned. I ran its body through a separately labelled driver that skips that check; all 464 cases and 11 sweeps hold. That is not a pin-valid pass, so it needs a rerun after you update pins.

**What changed**
- **M4:** `detectorId` is the emission `contributionId`, with one row per contribution. Baseline admission now enforces this after recomputing `baselineId`. A self-consistent renamed baseline, which was accepted before, is now refused. One old checker fixture relied on an extra non-contributing detector row; it now tests that admission refuses it.
- **M5:** Nine commands emit `kind=query`, but only the `query` command has a full graph response, so a globally required field would have broken the other eight.
  - I added an explicit `querySurface` selector. `graph-query-response` requires `queryResponse` (the complete `GraphQueryResponseV1`). `command-owned-summary` forbids it, and so do non-query envelope kinds.
  - The JSON rendering is the envelope itself and the agent rendering adds `agentHints`; parity is recovered from each rendering.
  - This is checked on a retained, admitted graph-query Run.
- **S5:** `argvDigest` is the lowercase-hex SHA-256 of the canonical JSON of the exact ordered argv array. A shell-joined, repeated or reordered surrogate is refused through `admit_test_execution`.
- **S6 / A13:** Three new details are registered in the registry and both common schemas: `DOCTOR.REPORT_NOT_PRODUCIBLE`, `OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED` and `DELIVERY.REQUIRED_PROJECTION_FAILED`.
  - `query-latest-empty` now uses `QUERY.VIEW_UNKNOWN`, and failure goldens must carry a detail. All v3 failure goldens now build valid failure envelopes.
  - The after-commit renderer detail requires a `runId`; the new pre-commit detail forbids one.
- **S7:** Presence is now true, false or unknown on every side.
  - False means either the side doesn't select the fingerprint (rule disabled or path out of scope), or a complete evaluation proved absence. The baseline records per-rule absence knowledge at adoption.
  - I built the counterexample first. On admitted Runs, partial-inventory and budget-exhausted current Runs produced CODE-FIXED. They now produce INDETERMINATE `current-absence-unknown`, for gating and non-gating rules. Complete removal still gives CODE-FIXED, and a known CODE-NET-NEW still fails.
  - My first version treated out-of-scope fingerprints as unknown. An existing control (`wider-scope-does-not-false-absent-unselected-current-paths`) caught that, which is why "not selected" now counts as false.
- **A6 / A9:** The precedence and gating rules are written into the composition contract. Both are tested on synthetic compositions and on complete replayed Runs. The reference behaviour is identical before and after.
- **A8:** Two public refusal routes are now written down: query `projectId` mismatch → `QUERY.PARAMS_MALFORMED`, and a present-but-invalid detector listing → `EVALUATION.PROJECTION_INPUT_INCOMPLETE`.
- **A11:** Truth table v9 has no platform-primitive row, so `ENFORCED-PLATFORM` can't be claimed in this profile.
- **A12:** The existing hidden gate reason is defined to cover any later axis; no new value.
- **A14:** Deliberately left unchanged, with the reason recorded.

**Decisions needed from you**
- **Schema and identity changes inside the current majors:**
  - A `kind=query` envelope without `querySurface` is now refused. It was accepted before, so this is breaking.
  - The baseline gains a required `absenceKnowledge` field, so every `baselineId` changes (measured: `f2ab44c6…→44951dfd…`, `4dcd1081…→191da4dd…`).
  - Every measured `comparisonResultId` changes as well.
  - You decide whether this stays a pre-release correction or needs a major bump. Historical subjects were not rewritten.
- **R1 (S7, measured, not fixed):** under complete enumeration, a subject that becomes unmatched through a signature collision still yields CODE-FIXED. The verdict is indeterminate for gating rules but `pass` for non-gating ones. A guard would contradict the selected projection contract §12 example (empty baseline with an unmatched finding, then a pivot-only CODE-NET-NEW), so it needs your call.
- **R2 (M5-type, measured):** the other eight query-class commands have parity fields with no envelope carrier. I also saw, without checking further, that the query-step operation type has no operation for `recommend` or `policy-test`.
- **Integration:** pins for all 21 files, and merging with the native coauthor's edits in shared paragraphs and files. The main overlaps are `workflows-and-surfaces.md`, both common schemas, the registry and the composition contract.

**Failed attempts, all kept in receipts:**
- `check-carrier-v3.py` needs arguments I didn't have, so it wasn't used.
- A probe path was wrong; I reran it on the unmodified tree.
- workflow-projection crashed once on the old baseline fixture.
- workflow-projection later failed two controls: the scope discriminator above, and a text match broken by line wrapping.
- One edit script partially applied because a text anchor was missing backticks; a resume script finished it.
- I replaced three weak or tautological controls I had written, one of them after it had already passed without testing what its name claimed.

**Limits:** synthetic fixtures admitted through `close_run`; the human rendering is a reference parity projection, not UI; no product host or qualification; consumer24's exports were not revalidated.

Files are in `/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/`:
- `review.md`
- `review.json` (sha256 `8ac9063c…`)
