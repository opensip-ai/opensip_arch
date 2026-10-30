# Independent review: AGENT-INTERFACE-GUIDANCE-2026-10-29-r1

**Verdict: REQUIRED-FINDINGS. I cannot give ACCEPT-DOCUMENTATION for this subject.**

The three new guidance docs are accurate and useful. But the scope is labelled "one unpinned navigation bullet", and that label is wrong: `docs/START-HERE.md` is pinned by the D-372 application manifest.

## Route, subject and evidence

- **Preflight (run):** `ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`, exit 0. The launcher supplied all four values: route R2-DEEP, provider claude, model claude-opus-5-5, effort medium.
- **Subject manifest:** `subject-r1.json` SHA256 is `00aa475e2184588d7012c07403e1a8958c329ae16e3e46f03bb66428d8842c8e`, which matches the pin. I hashed all four worktree files and they match the manifest's sizes and hashes:
  - `START-HERE.md`: `bfbefd1b…`
  - `EVALUATION.md`: `730ee0c5…`
  - `GUIDANCE.md`: `eefbe079…`
  - `README.md`: `d8ea53c1…`
  - The `subject-r1/` copies are byte-identical.
  - `git diff --cached` equals `patch-r1.diff` (sha `ba0dfeec…`).
- **Git heads:** the worktree HEAD is `7887d4e5`. Live architecture main has moved to `4f2b6a51`, with no changes to the subject paths. Product is at `e97f0bd3`.
- **Other checks run:**
  - The author's read-only `check_docs.py` gave 36 links, 20 operations and no errors. It deliberately skips the `review/` link, which does not exist yet.
  - I read all four subject files in full.
  - I read the owners: workflows §8, admission-and-qualification §§2–4, the build plan's milestones and command/qualification routing, and the graph-query:3 `Operation`/`AdvisoryOperation` enums.
  - I read the product `design-lock.json` paths, the D-372 `application-subject.v46.json` and `application-activation.v1.json`, COORDINATOR-DECISIONS D-372 §Documentation, and the record-hygiene `PROPOSAL.md` lead decision of 2026-10-03.
  - I read the comparison report.
- I did not read the full bootstrap chain in the architecture checkout or the live control files beyond what the task cache quoted. Those lanes are unrelated, and the route was checked against this request directly.

## Required findings

### F1 (blocking): the START-HERE edit breaks a live D-372 pin and is misclassified

- `docs/coop/design-corrections/reviews/application-subject.v46.json` lists `docs/START-HERE.md` as an applied file: sha256 `c4b1310e…`, 5243 bytes. That manifest has sha `dab6e00f…`, which is the one `application-activation.v1.json` pins.
- The activation's `bindingRule` is: *"Verify both pinned artifacts and each current applied file against the application manifest."*
- I checked all 197 applied files. There is zero drift at the base `7887d4e5` and zero drift at live main `4f2b6a51`. In the subject, `docs/START-HERE.md` is the **only** file that drifts.
- D-372 does say "New current-head/navigation/register annotations are prospectively authorized by this act" (COORDINATOR-DECISIONS.md:24168). The 2026-10-03 lead decision (`docs/implementation/m3/record-hygiene/PROPOSAL.md` §"Lead decision", lines 269–276, plus §2 line 35 for README) interprets that clause as binding through the application manifest. Under that decision, pinned files "cannot take in-place notes without changing D-372's activation subject". Such edits wait for the next application-manifest successor; only unpinned files are edited in place.
- The PLAN's statement that the bullet is "not … a selected product design-lock input" is true: `START-HERE.md` is not in `design-lock.json`. Its implied claim that the file is unpinned is false.

**Required disposition:**
- **Recommended:** remove the `START-HERE.md` hunk from this unit. Put the navigation link in an unpinned index instead. `docs/implementation/README.md` and `docs/README.md` both qualify: neither is in D-372 or the design-lock, and the 2026-10-03 errata used `docs/implementation/README.md` for exactly this. Record the START-HERE bullet as a staged note for the next D-372 application-manifest successor, alongside `staged-notes.patch`.
- **Alternative:** submit a separately reviewed application-manifest successor or activation addendum that pins the new START-HERE after-image. The lead decision rejected this route for note-only changes.

**What this finding does not require:** no product design-lock bind and no contract successor. Neither touches a selected semantic passage, schema, gate or fitness policy.

### F2 (wording): EVALUATION.md lines 3–4 read as a new delivery precondition

The text says "Future agent consumer delivery must include a reviewed evaluation plan **and retained results**." `agent-serve` is an M5 command under the build plan, which is pinned by D-372 and the design-lock. Making its delivery wait for study results would add an M5 completion criterion that the owner does not have. That would be a hidden gate or reorder, despite the "not a new DR-G gate" disclaimer.

`README.md` lines 11–12 already gives the correct scope: results are required "before claiming benefit". **Required change:** say that the consumer delivery proposal must carry a reviewed evaluation plan, and that any agent-use benefit claim requires retained results. Neither of these conditions M5 command delivery or M6 qualification.

## Assessment by question (subject to F1 and F2)

1. **Correctness of the docs.**
   - All 20 operations are listed. The advisory set is exactly `comparison.diff`, `candidate.list`, `inspection.show` and `review.brief`.
   - "Graph traversal does not seal a Run" is correct.
   - The guidance on `latest` resolution, continuation binding, the difference between a page boundary and an operation bound, "an empty page is not absence of callers", the three-way availability/incompatibility/rebuild distinction, `agentHints` not altering parity fields, and keeping the CLI `review brief` host request separate from public `review.brief` all match §8 (lines 1104–1260).
   - `fit` and its advisory report with its own sealed Run are kept and described accurately. Advice to retain provenance, Coverage, typed availability and truncation is preserved.
   - The M4 query / M5 agent-serve / M6 qualification sequence matches the build plan's routing tables.
2. **Evaluation design.**
   - **Baseline:** fair. Paired arms, same model and effort, equal source access, no seeded answers, and tool non-use is not grounds for exclusion.
   - **Coverage:** zero-use trials are retained. Missed and misused evidence is measured. Tokens are counted in total, including prompt and schema overhead, with unknown values kept distinct from zero. Latency is end-to-end, with cold and retained conditions separated. Inputs and rubrics are pinned in advance, with no post-hoc thresholds and negative results reported.
   - **Owner metrics unchanged:** the 3 warmup / 7 measured runs, the 1.20×/1.25× limits and the G13 schemas all match AQ §§2–3. Engine benchmarks are kept separate from stochastic agent trials.
3. **Context packing and memory.**
   - Token-budgeted packing stays an experimental consumer proposal, with no fields, endpoint or cache shortcut, and it needs an owning contract before it could become public.
   - Conversational memory is deferred.
   - Querying grants no execution or mutation permission.
   - Apart from F2, there is no new gate and no reorder.
4. **Classification.**
   - The three new files under `docs/implementation/agent-interface/` are supplemental and unpinned. They need no contract successor or design-lock bind; documentation review, assent and local integration are enough.
   - The START-HERE line is not unpinned (F1).

## Advisory (not blocking)

- **A1:** `README.md:6` links to `review/`, which does not exist yet. The integration commit must create `review/` at the same time, or the link breaks.
- **A2:** `README.md:32` cites an absolute local path outside the repository. Consider recording the report's SHA-256 so other readers can check provenance.
- **A3:** where feasible, require scorers who do not know which arm produced a result, beyond "independently prepared answers".

## Limitations

- This review accepts documentation only, and only after F1 and F2 are fixed in a new frozen subject that gets re-reviewed. It does not establish any runtime behaviour, empirical benefit, contract binding, qualification, or closure of an existing lane.
- I did not run the D-372 probe scripts; I compared the manifest hashes directly with read-only Python and `git show`.
- I wrote no files.
