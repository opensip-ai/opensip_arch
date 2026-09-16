# Independent review: report projection and fit owner candidate03 (`m1-report-projection-subject-03`)

**Verdict: CHANGES REQUIRED.** Six findings: two blocking (RPR3-1, RPR3-2) and four required (RPR3-3 to RPR3-6).

Nothing here makes a product, generator, browser or performance qualification claim. The machine-readable form is `review.json`, and all evidence is under `work/`.

**Manifest:**
- `subjectManifestSha256`: `42144cde36062b6668d8aab899af08d9d7ba97c8ecd53aad2ec82361902fe118`
- internal `subject-files.json`: `679487ef…616201`

## Subject verification

**Before review:**
- The external manifest SHA-256 matched.
- All 16 files matched by hash and byte length, with no extra or missing entries and no `__pycache__`.
- The internal `subject-files.json` lists the other 15 files.

**Strict run.** I ran the checker from a byte copy of exactly those 16 files (`work/closure`), before creating anything else there:

```
/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --subject-strict
```

- **Result:** exit 0, `passed: true` (`work/strict-check-stdout.txt`).
- **Coverage:** 73 external pins plus 1 listing; 43 metadata-v2 cases through envelope5; the historical checker passes; 117 report cases (18 accept) and 20 envelope cases.
- **Caveat:** my first attempt added `--out` under `/tmp/opensip-implementation`. The checker's own hook then refused the result write (A3), after every check had finished.

**After review:** see `work/after-verification.json`, summarised at the end.

## Closure of prior findings

| Prior | Status | Basis |
|---|---|---|
| RPR2-1 fit | Partly closed | Exact first-page request consts, total parity and the page/cursor/parity joins; Q1 → `J-ENV-FIT-PAGE`, Q2a → `J-ENV-FIT-CARRIER`, Q2b accepted. The ephemeral flag join is byte-identical (null parity). Residual: RPR3-3(a). |
| RPR2-2 page slicing | Partly closed | The projector re-issues owner queries, and embedded pages equal fresh owner answers. The exact-basis slice is refused. Residual: blocking RPR3-1. |
| RPR2-3 ledger / F03 / S01 | Partly closed | The invocation:3 ledger carrier and the deterministic policies exist. Residuals: cancellation (RPR3-3(b)); duration and F-readiness (RPR3-6). |
| RPR2-4 provenance | Mostly closed | Q3–Q6 and Q13 are refused as stated. Residual: A4. |
| RPR2-5 closure | Partly closed | The parent closure is exact (my trace). Residual: the child subprocess bypass (RPR3-4). |
| RPR2-6 passages | Closed | Seven overrides with asserted before-texts. The §9 table is a selected subset (workflows `:1370-1371`). |
| A1–A6, A9, A10 | Closed | Index bound, pointers, iterative depth, derived gains, reasons, S01 policy, integrity label, static goldens. |
| A7 | Partly closed | See RPR3-5. |
| A8 | Untested | No generator run. |
| A11 | Carried | Dirty-tree pins. |
| Review-01 findings | Closed except RPR-4 and RPR-7 | RPR-4 recurs as the duration gap (RPR3-6); RPR-7 recurs as the root budget (RPR3-2). |

## Required findings

### RPR3-1 (blocking): a complete owner page can be silently cut and admitted as `complete-page-set`

**The gap.** `check.py:434` (and `:436`) enforces `totalItems == len(items)` only when `countBasis == "exact"`. The owner law says otherwise:
- `query-projection-contract.v3.md:140`: "Completeness is `traversalCoverage=complete` and `countBasis=exact`";
- `:136`: lower-bound is reserved for owed remaining work.

**Probe G1** (`work/probes/probe_rpr3.json`), on audit-full slot 0 (a 100-row owner page, total 107):
- relabelled complete, cursor removed, continuation `complete-page-set`;
- `countBasis` set to `lower-bound`;
- items cut to 1.

Result: **accepted**. The controls are refused: the same slice with `exact` gives `J-GRAPH-COUNT` (G3), and a truncated-bound relabel gives `J-GRAPH-CONTINUATION` (G2).

This violates "never slice without accurate context/cursors". It also makes the graph `verifiedInDocument` claim `page-count-and-continuation-joins` false.

**Correction:**
- `complete` ⇒ `exact` and `totalItems == items`.
- `lower-bound` ⇒ truncated coverage with `producedItems == totalItems ≥ items`.
- `complete-page-set` only on exact complete answers.
- Add G1 and its truncated-page variant as refusal cases.

### RPR3-2 (blocking): the budget does not bound owner-valid maxima of mandatory root metadata

**The derivation uses a placeholder.** `build_owner.py:391-392` derives the 917,504 B root allowance from a construction whose `purgeDisclosure` is a placeholder. The owner shape is different:
- `PinnedPurgeDisclosure` allows 4096 pins × 256-char `pinId` (`common.schema.json`);
- the StepTermination `evidence.pinned` branch is legal on any step.

**Probe L1.** The largest owner-valid StepTermination within the 4 MiB owner codec is **4,193,710 B** (schema- and codec-valid). The author's worst root is 871,329 B.

**Probe B1** (`work/probes/probe_budget_coverage.json`) is an audit failure report:
- `kind=failure`, all panels `no-admitted-result` (**323 B** of panels);
- envelope at its boundary (4,194,016 B);
- each of the 3 recorded required steps rejected with an owner-valid 2,096,965 B pinned termination;
- every ledger join consistent.

Result: `CODEC-BYTES` at **10,489,377 B**, above `documentMaxBytes` of 9,306,112. The control with one large step is accepted (6,295,587 B).

**Why it matters.** The byte law fills panels to 4 MiB regardless of root size, so a large root plus a boundary envelope plus full panels always overflows. The ledger is mandatory, so the only outcome is delivery failure. That failure then replaces the invocation's own termination.

**Correction:**
- Derive the allowance from maxima the joins actually permit: at most 4 recorded steps per HTML command × a max-codec termination.
- Or reference ledger terminations that equal the envelope termination.
- Or define an owned bounded termination projection with omission disclosure.
- Budget panels against `documentMaxBytes − envelope − root`.
- Add B1 as an accepted or typed-boundary case, with its stated delivery outcome.

### RPR3-3 (required): the D9 aggregate lets a renderer failure replace a query refusal, and cancellation is unhandled

**(a) Renderer failure replaces the query refusal.**
- `contract.md:104` says "D9 ordering then applies as owned".
- **Probe D1:** `d9_aggregate` over [success, query request-rejected, render operational-failed] returns `RENDERER_FAILED_AFTER_COMMIT`, so the query refusal is replaced.
- The only aggregate golden is an operational tie.
- The report case `ledger-renderer-failure-overrides-query-refusal` holds only because render is never recorded in reports (`check.py:327`).
- JSON, human and agent fit envelopes have no such law or golden, which contradicts the root decision.

**(b) Interrupted terminations crash admission.**
- `report_model.py:32` `D9_ORDER` lacks `interrupted`.
- **Probe D2:** an owner-valid `{class: interrupted, signal: SIGINT}` step termination makes admission raise an **uncaught `ValueError`**.
- The ledger omits `InvocationRecord.cancellation`, so the owned before-settle → interrupted and after-settle no-reclassification laws (`workflows-and-surfaces.md:224-228`) cannot be recomputed.

**Correction:**
- State the query-refusal-plus-renderer-failure outcome and golden it per renderer, or record a root decision.
- Carry cancellation in the ledger, implement the cancellation aggregate, and add interrupted cases.

### RPR3-4 (required): fresh-source closure is bypassed through the unhooked child checker

**The launch.** `check.py:899` launches `check_metadata.py` with `-I -B`, with no pycache prefix and outside the hook.

**My whole-process trace of that child** (`work/probes/trace-summary.json`) shows governed opens absent from `source-pins.json`:
- `foundation/__pycache__/canonical.cpython-314.pyc`
- `workflows/command-inventory.v3.json`
- `metadata-v2/README.md`
- `metadata-v2/successor.json` (the child's own pin anchor)
- `implementation-boundaries-and-build-plan.md`
- `implementation-coverage.v1.json`
- `repository-file-inventory.v1.json`
- the unpinned listing of `docs/implementation/m1/metadata-v2`

**The pyc path is exploitable.** `work/probes/pyc_demo.out` shows that under `-I -B`, `spec_from_file_location` on a hash-verified source ran a header-matched stale `__pycache__` bytecode. That is exactly how `check_metadata.load` loads `canonical.py`. The architecture pyc headers do not match today, so it is not live, but the closure does not exclude it.

**The parent is sound:** 73 of 73 governed opens are pinned, and pyc lookups go only to the nonexistent prefix.

**Correction:**
- Run the historical checker in-process under the hook, or with `-X pycache_prefix=<nonexistent>` plus a child hook.
- Pin the child's full observed closure and assert trace = pins.

### RPR3-5 (required): the coverage overlay hides a real fit command-row drift

**The masking.** `check.py:937-944` treats identical *first* validator messages as equivalence. But `validate_coverage` stops at `check_implementation_planning.py:103-105`, before all per-row checks.

**Probe C1.** I neutralised only that pre-existing condition, by adding `crates/reporting/src/assets.rs` to `moduleFirstMilestone` for both. Base returns `valid`; the overlay returns **`Command metadata drift`**.

**Probe C2.** The overlay `fit` row's `parityFields` is still the 5-field inventory4 list, while inventory5 has 9. The four candidates-* disclosure fields are missing (`:145-147`).

**Correction:** fix the row, and compare full validator results with only the pre-existing condition isolated.

### RPR3-6 (required): F01–F10 and R03 duration have no closure path, so approved functionality stays unavailable indefinitely

**The obligations.** `fixtures.json#/obligations` RP-OBL-F01..F10 are absence statements with no:
- owning design unit or lane;
- milestone or gate;
- closure criterion.

`FeatureStateV1.state` is const `unavailable`, and feature states are per-command consts, with no retirement path stated.

**The coverage rows.** The reportFeatures rows R05/R06/R07/R08/R12/R23 (M4) verify "including explicit feature states where an owner is absent" (probe C3). The absence itself satisfies delivery.

**Requirements affected** (`prototype-report-inventory.md`):

| Row | Disposition | Requirement | Obligations |
|---|---|---|---|
| R05 (`:55`) | Preserve | policy/capability descriptions | F01, F08 |
| R06 (`:61`) | Preserve | recipe descriptions, selectors and parameters | F06, F07 |
| R07 (`:67`) | Change | metrics and test reachability | F09, F10 |
| R08 (`:73`) | Change | package coupling matrix | F03 |
| R12 (`:97`) | Change | entry-point trace with recognition evidence | F05 |
| R23 (`:165`) | Change | configuration disclosure | F04 |

F02 is conditional and acceptable as unavailable.

**Design readiness, not implementation.** F03 (unit membership exists natively; no query carrier) and F05 (`entryPoints` exists; not retained) are design decisions inside existing owners, not absent owners.

**R03 duration.** R03 requires "typed outcomes and duration" (`:43`). invocation:3 has no duration or timestamp field, and the report has no feature state or obligation for duration. The requirement vanishes silently (the RPR-4 class of defect).

**Correction:**
- Per obligation: owner design unit, blocker vs root-recorded deferral (at least F03 and F05 are blockers keeping AUDIT-G10 open), milestone and gate, and retirement path.
- Add a duration feature state and obligation.
- Stop absence from satisfying reportFeatures verification.

## Advisories

- **A1: slot steering.** The host can re-plan slots by asserting `descriptor-not-retained`. Probe S1 is accepted with a different plan (`check.py:413-418`).
- **A2: history count.** `priorRunsInSnapshot` is host-controlled. Probe H1 (understate the count, drop the oldest Run) is accepted, and the "recomputed" label overstates this.
- **A3: `--out`.** A path under the governed root fails with `UNPINNED-LOAD` after all checks pass (`check.py:1039`).
- **A4: graph provenance.** `page-count-and-continuation-joins` overclaims until RPR3-1 is fixed.
- **A5: history exclusion.** State in contract §7 that the baseline source Run is excluded from prior Runs (`report_model.py:243`).
- **A6: listing drift.** Listings are digested only at start; a path-membership hook does not detect later drift (TOCTOU).
- **A7: R14.** R14 says "beyond recent history", but the policy offers only the most recent Runs. Root should confirm.
- **A8: stale pyc.** Stale architecture pyc files exist for `canonical.py` and `check_implementation_planning.py`.
- **A9: generator.** Generator compatibility is unexercised (RP-OBL-G01).

## Root-decision checks

| Decision | Result |
|---|---|
| Fit `--ephemeral` preserved | **Yes.** Flag join byte-identical; null parity. |
| Sealed first-100 page from the exact Run | **Yes.** Request consts, joins, truncated-150 positive. |
| Renderers disclose truncation, cursor and availability | **Fit yes.** The static section has all nine lines (X3). Graph completeness can be falsified via RPR3-1. |
| Query failures use D9; renderer failure cannot replace them | **Partly.** See RPR3-3. |
| Graph reduction re-issues, never slices | **Projector yes; admission loophole** (RPR3-1). |
| invocation:3 ledger represented | **Yes, minus** cancellation and duration. |
| History and graph selection deterministic | **Yes, given host-asserted inputs** (A1, A2, A5). |
| minResolution | Equality with the table rung; Q5 refused. |
| Simple path | `J-GRAPH-PATH` law; Q13 refused. Shortest-path optimality is host-asserted. |
| subject3 | Independent stdlib recompute over 517 rows: **0 mismatches** (X1). |
| Integer limits | u64 max accepted, 2^64 refused `CODEC-LEXICAL` (I1/I2). |
| Depth limit | 38 = 32 + 6. |
| Byte limits | Mandatory root **not bounded** (RPR3-2). |
| Static parity goldens | **13/13** independently recomputed (X2). |
| Coverage / passage scope | Passages closed; coverage drift (RPR3-5). |
| Successor compatibility | Restorations exact; 43 metadata cases identical. |
| metadata-v2 acceptance unchanged | All 10 `metadata-v2` files equal `m1-metadata-subject-02.json`; the historical checker passes. |

## Independent evidence

**Positive:**
- The strict closure-copy check passes.
- Parent trace: 73/73 opens pinned.
- All 13 bases admit in my rebuilt context.
- X1, X2 and X3 as above.
- The G2/G3 controls are refused.
- I1 and I2 behave as expected.
- The B1 control (one large step) is accepted.
- metadata-v2 bytes are unchanged.

**Negative:**
- G1: sliced complete page accepted.
- L1 and B1: root overflow.
- D1: renderer failure replaces the query refusal; D2: uncaught crash.
- Child trace shows unpinned opens, plus the pyc demo.
- C1/C2: masked coverage drift.
- C3: absence rows satisfy verification.
- S1 and H1: host-assertion steering accepted.
- `--out` under the governed root refused.

## Untested limits

- No generator, browser, HTML, human renderer, accessibility or product code was built or run, and nothing was measured for performance. All sizes are constructions.
- The probes use the subject's mock owner, not the product query engine.
- B1's `evidence.pinned` on analysis and comparison steps is owner-schema-valid, but I have not shown a product workflow that reaches it. The finding is about the claimed worst-case derivation.
- The pyc bypass was demonstrated on a synthetic module; the architecture is read-only and was not modified.
- The workflows reference model was not rerun for the new golden.
- F-absence claims were not re-searched beyond RPR2.
- The hook was traced only for open, listdir, scandir and subprocess events.
- Author responses and session logs were not used.

## After-verification

After writing `review.json` and `review.md`, I recomputed:
- the external manifest SHA-256;
- the 16 file hashes and lengths in the frozen subject;
- directory equality and absence of `__pycache__`;
- the same checks for the closure copy.

The results are in `work/after-verification.json`. All outputs of this review are under `m1-report-projection-review-03/`. No commit or push was made.
