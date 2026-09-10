I’ll add a real candidate-only full-Run fixture and checker, then record v8 dispositions for the v7 advice without rewriting that history. First I’ll read how clones-near is actually admitted and how check-replay already covers imports.clones-near is actually `SUPPORTED-DESIGN` under `syntax-only`, so I can compose from the public file fixture’s admitted syntax universe and remint Plan/cells/spec—no fake TypeScript universe.Candidate-only is now a public full-Run path. v7 is unchanged. Core M3/schema/I/E were not edited. Not a Run.

## Candidate full-Run (S2)

New files: `evaluator_candidate_fixture.v3.py`, `check-candidate-replay.v3.py`. They compose the public file fixture’s **admitted syntax universe** and remint Plan/spec/cells. Matrix cell is `clones-near @ syntax-only` (`SUPPORTED-DESIGN`). No TypeScript universe on a syntax-only request. `near_candidate_kw` is still join-only, not a full Run.

`check-candidate-replay.v3.py` **4/4**:

| Case | Result |
|---|---|
| complete-empty | `close_run` ADMIT, verdict `pass` |
| group-bearing | ADMIT, `authority=candidate-only` |
| missing required | retained unavailable envelope, `indeterminate`, `provider-unavailable` |
| group `authority=fact` | `EXECUTION_INPUTS_CANDIDATE_GROUP` |

Reconstruct still reads group/source bodies from blobs with `groups={}`.

Helper: selected+U unavailable keeps a non-null `stageOrdinal` so a retained unavailable envelope is schema-valid. v6 **52** still `mismatches []`; execution-replay **8** still PASS.

## v7 advice (dispositions only)

- **S1:** Join category `native-work-incomplete`; originating `provider-unavailable` is what the proof carries. No new field.
- **S3:** Not a valid-case bug. No second walk.
- **A1:** Named join key not needed; `close_run` is complete replay.
- **A2:** Withdrawn. `check-replay.v3.py` already has nonempty runtime/test/history import graphs.
- **A3:** Host-derived selectedRefs is the law while stages are view-only. Host product work is out of scope.

Reports: `/tmp/opensip-design-corrections/grok-execution-inputs.v8/review.md`, `review.json`, `check-candidate-replay.stdout.json`. Root can freeze this required path.
