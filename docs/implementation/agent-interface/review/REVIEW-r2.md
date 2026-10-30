# Independent re-review r2: AGENT-INTERFACE-GUIDANCE-2026-10-29-r2

**Verdict: ACCEPT-DOCUMENTATION** for the r2 subject manifest `9466233de328d1f1b8112c3ce2dc2ab313511cfceada6ab2df59be6ad15871f8`. Both r1 required findings are closed. The acceptance covers these four documentation files only.

## Route and preflight
- **Preflight result:** `ROUTE-OK R2-DEEP claude claude-opus-5-5/medium`, exit 0. I ran it exactly as given against `REVIEW-REQUEST-r2.md`.
- **Route metadata:** the launcher supplied it in the environment: `OPENSIP_AGENT_ROUTE=R2-DEEP`, `PROVIDER=claude`, `MODEL=claude-opus-5-5`, `EFFORT=medium`.
- **Independence:** the subject was written by Codex and I am Claude, so the reviewer is from a different vendor family.

## Bootstrap reads completed in this session
- **Architecture files at 4f2b6a51:**
  - `CLAUDE.md`, which is byte-identical to the worktree copy.
  - `docs/START-HERE.md`, all 47 lines.
  - `AGENT-MODEL-ROUTING.md`, all 200 lines. R2-DEEP is Claude Opus 5.5 at medium effort. Independent review must come from a different vendor family, and contract-adjacent review needs at least R2.
  - `docs/implementation/m3/IMPLEMENTATION-STATUS.md` (310 KB). I read the outline, the header, and the sections "Decisions and blockers", "Next actions", the unit register and "Work boundaries". The 7–218 "done" body consists of very long lines, and I did not read all of it.
- **Live controls:**
  - `CURRENT-STATE.json`: I extracted `coordinatorQueue2026-10-26` and `leadTransitionM5`. Its `staleKeys` entry marks `currentCandidate`, the routes and the top-level inventory fields as stale. The top-level `architectureHead` is 6f28e10, which is also stale.
  - The top of `ACTIVE-PLAN.md`, through OD-AUTO-1 and the 2026-10-26 checkpoint.
  - Neither control file mentions this task. The cache `HANDOFF.md` (sha `55dfacec…`, unchanged since r1) selects it, and `PLAN.md` is its updated plan. Those other lanes keep their own authority; I dispatched nothing and reviewed none of them.
- **Git state:**
  - Architecture main is at `4f2b6a51`. It has 10 unrelated untracked paths, which I did not touch.
  - Product is at `e97f0bd3` and clean.
  - The worktree HEAD is `7887d4e5`, with exactly 4 staged files and no unstaged or untracked changes.
  - `git diff --cached` and `git diff HEAD` both equal `patch-r2.diff`.
  - Main has made no changes between base and HEAD to `docs/implementation/README.md`, `agent-interface/` or `START-HERE.md`.

## Subject integrity
I hashed each worktree file and compared it with the copy in `subject-r2/`:

| File | Bytes | SHA-256 |
|---|---|---|
| `docs/implementation/README.md` | 3604 | `dcb20423…` |
| `agent-interface/EVALUATION.md` | 6890 | `5131229d…` |
| `agent-interface/GUIDANCE.md` | 5637 | `eefbe079…` |
| `agent-interface/README.md` | 3130 | `4e65920f…` |

- All four match `subject-r2.json` and are byte-identical to their `subject-r2/` copies.
- `GUIDANCE.md` is byte-identical to r1, so my r1 owner checks of it still apply.
- I read the agent-interface `README.md` and `EVALUATION.md` in full, plus the r1→r2 diffs and the full hunk in `docs/implementation/README.md`.

## Disposition of r1 findings

**F1 (D-372 pin): closed.**
- `docs/START-HERE.md` in the worktree is `c4b1310e…`, the D-372 applied bytes, and it is absent from the patch.
- I re-checked all 197 files in `application-subject.v46.json` (manifest `dab6e00f…`, as pinned by `application-activation.v1.json`) against the r2 worktree: zero drift. In r1 I confirmed zero drift at base and at main, and main HEAD has not moved since.
- The new navigation paragraph is in `docs/implementation/README.md`. That file is:
  - absent from the D-372 manifest;
  - absent from the product `design-lock.json`;
  - not pinned anywhere at its current bytes: no occurrence of `276c75e8…` in either repository.
- This matches the in-place precedent of the 2026-10-03 lead decision.
- `future-start-here-note.patch` exists only in the task cache and is not applied.
- No contract successor, application-manifest successor or design-lock bind is needed.

**F2 (hidden delivery gate): closed.**
- `EVALUATION.md` lines 3–9 now require a reviewed evaluation plan in the consumer delivery proposal. Retained results are required only for an agent-use benefit claim.
- It states that "no M5 completion criterion, DR-G gate or G13 report schema is changed" and that command delivery and qualification keep their owning gates.
- Read across all four files, nothing turns study results into a condition for delivery:
  - agent-interface README line 11 limits the requirement to "before claiming benefit";
  - the new navigation paragraph says the existing gates keep authority;
  - GUIDANCE line 89 applies only to proposing a public packaging contract.
- Requiring a plan only shapes the proposal document. It is within the user's request for "evaluation requirements" and is not a gate.

**A1 (`review/` link): acceptable.**
- `review/` remains the only link the checker deliberately skips.
- I ran `check_docs.py`: 23 links, 20 operations, no errors. `git diff --cached --check` was clean.
- **Integration condition:** `review/` must be created in the same commit.

**A2 (report provenance): closed.** The comparison report's SHA-256, `0231fb02…`, matches the actual file.

**A3 (scoring and trial design): closed.** The study design now requires:
- arm-blind scoring where feasible, with masking limitations disclosed;
- fresh isolated sessions for each trial;
- no conversation or answer carried over between arms;
- counterbalanced trial order, or a disclosed reason it cannot be counterbalanced.

## The five review questions, reassessed
1. **Correctness:** unchanged from r1.
   - All 20 operations are listed, and the advisory set is exactly 4.
   - The guidance on `latest`, continuation, and page boundary versus operation bound matches the owners.
   - So do the empty-result, availability and parity rules, `agentHints`, the separation of `review brief` from `review.brief`, `fit`'s advisory report over a sealed Run, and the M4/M5/M6 sequencing.
2. **Evaluation:**
   - The baseline is fair and observable.
   - It keeps zero-use trials and requires independent, now arm-blind, scoring.
   - It tracks missed evidence, total token overhead with unknown kept distinct from zero, and end-to-end latency split into cold and retained conditions.
   - Inputs are pinned and reproducible.
   - It does not touch the qualification contract's 3-warmup/7-measured benchmark rule, the 1.20×/1.25× limits or the G13 schemas, and it keeps the engine benchmark separate from agent trials.
3. **Packaging and memory:**
   - Token-budgeted packaging stays an experimental consumer proposal: no public fields, endpoint or cache shortcut, and it needs an owning contract before it could become public.
   - Persistent conversational memory and session recall stay deferred.
   - Querying grants no execution or mutation permission.
   - Nothing adds a gate or reorders the milestones.
4. **Classification:** this is correctly supplemental delivery guidance and evaluation-planning obligations, plus one navigation paragraph in an unpinned index. Documentation review, author assent and local integration are enough.
5. **Evidence:** recorded above.

## Non-blocking notes
- `EVALUATION.md` lines 15 and 17 run past the file's normal wrap width. This is cosmetic only.
- `docs/implementation/README.md` already contained stale lead and reviewer statements before this change (for example "Grok leads … Codex is unavailable"). They are out of this unit's scope.

## Limits
- This accepts documentation only. It establishes no semantic successor or binding, no implementation, benchmark or empirical benefit, no unit or release qualification, and no acceptance of any other lane. The future START-HERE note still needs a D-372 application-manifest successor before it can land.
- Everything I did was read-only. I wrote, committed or pushed nothing, ran no product tests, builds or experiments, and did not access any corpus, store, private or held-out data, or credentials.
- I did not run the D-372 probe scripts; I verified the pins with direct SHA-256 comparison.
