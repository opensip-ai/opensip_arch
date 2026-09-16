I've corrected all seven required findings (F1–F7) and both low ones (F8, F9) in `m1-report-evidence-design-author-02/candidate/`; it is ready for root to freeze. The strict pinned check passes: exit 0, `CHECK OK`, 89 external files and 2 listings pinned, 14 subject files, subject manifest `7fe14a63…b964`. A second strict run from a fresh copy, started from `/`, gives the same result apart from two wall-clock timing fields. The result is in `check-result.json` and the input list in `candidate-inputs.json`. Nothing here is approved, and the owner changes S1–S4 are still unaccepted proposals.

**Findings**
- **F1: historical Runs stay admitted.** The recognition parameter row is now optional. New Plans get a separate pre-Plan duty instead: a Plan requesting a TypeScript or Rust language mode must carry exactly one recognition parameter.
  - **Extra owner change.** Registering the new document also needs one exact source change to `identity-model.v3.py`'s closed list of registered documents. I only found this by running it; without it, new Plans are refused `UNREGISTERED_DOCUMENT`.
  - **Executed.** The check closes real Runs built by the pinned evaluator3 reference fixture, through the real identity model:

    | Case | Result |
    |---|---|
    | Predecessor Run | Admitted by both the pinned and the proposed identity model, same run id. It reads as `not-plan-bound` from its own parameters; no flag is involved. |
    | New-Plan Run | Admitted by the proposed model. The pinned model refuses it (`PAYLOAD_PARAMETER_UNREGISTERED`), so nothing is silently upgraded. |
    | Parameter bytes lost | Refused `EVIDENCE_UNAVAILABLE` |
    | Pre-Plan duty | Refuses a compiler-mode spec without the parameter; admits syntax-only specs |
- **F2: cross-universe test callers.** Test reach now matches test origins in every universe the walk reaches. A reached universe with no test identity adds a blocker. The reviewer's C1 world now finds the test path.
- **F3: default globs.** No test origin set can be complete any more, and the `no-static-path-within-bound` state is removed from the schema. A configured jest `testMatch`/`testRegex`/`roots`/`projects` is read as data and reported. The reviewer's C2 world is now `not-found-incomplete`. Imported test executions are never origins.
- **F4: Cargo member binaries.** Rust entry points are the crate roots of every selected bin and lib target, taken from retained target ownership and crate-root data. Unresolved or ambiguous roots are named as missing coverage.
  - I ran the pinned native model: it folds the members into one workspace unit and recognizes only `src/main.rs`.
  - The correction adds `crates/app/src/main.rs`, so the reviewer's C3 trace is now `path-found`. With that root unresolved, the state becomes `partial` and the trace carries a blocker.
- **F5: patch composition.** The report patch now uses remove-members, insert-after and add operations whose preconditions are checked on the current document. Applied in both orders with a stand-in RP-DO-11 patch (removing `step-duration`), through the same applier, it gives identical results. Unmet preconditions are refused.
- **F6: coupling bounds.** Cells, target buckets and drill-down rows are byte-bounded, deterministic prefixes. Totals stay exact, and any omission adds a blocker and makes blank cells "not determined". Both new panels come after history in the report's projection priority and get only the bytes left over.

  | Dense 120-package workspace | Result |
  |---|---|
  | 4,194,304 B budget | 4,193,904 B, 3,911 of 14,280 cells omitted |
  | 200,000 B budget | 13,896 omitted |
  | Skeleton doesn't fit | No panel |
  | Inside parent07 `audit-full` | Within the report budget |
- **F7: mutants and featureMap.** New permanent fixtures kill review01's surviving mutants M4, M7 and M8. featureMap references now fully resolve, and a bogus one is refused.
  - I also ran 13 mutants over the new laws (in `mutation-results.json`, outside the check's pinned closure); all are killed at their intended point.
  - M14 survived my first mutation run, so I added a fixture where a caller sits in a universe with no test identity.
- **F8: duplicate provenance.** Cells now report observations, per-universe program edges and universe-independent source dependencies. The reviewer's C6 duplicate shows 2 observations and 1 source dependency.
- **F9: anchor versus symbol path.** Importer ownership now uses the import fact's anchor paths, per the native "enclosing fact's anchor path" law. Anchors that point to different owners go to an explicit bucket, and a symbol path outside the anchors is counted but never used for ownership.

**Limits**
- The worlds, the mock graph owner and the evaluator3 Runs are the pinned synthetic reference fixtures, not product Runs, providers, stores or a browser.
- Occupancy reconciliation is taken as given on the facts.
- The native, identity and evaluator models were executed; the query projection model was not, so the whole-view projection (S3) rests on its written law and reference function only.
- Documents the owner code reads inside the scratch copy of the owner tree are this run's own byte copies; only the compiled modules there are re-verified.
- Native's pre-Plan `admit_analysis_spec` still uses the historical v2 identity registry. I recorded that for the owners and didn't change it.
- No runtime, browser, generator, performance or Run replay qualification, and no whole-report completion claim.

Nothing outside the new author directory was edited. Parent07, subject-01 and review01 are verified unchanged by hash.
