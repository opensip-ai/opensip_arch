**Disposition: CORRECTION_REQUIRED, with one clarification bundled in.** Frozen40 matched its manifest before and after (12911 members, 0 missing, mismatched or extra). All writes went to `/private/tmp/opensip-design-corrections/claude-view-attribution-assessment.v1`, and every subprocess has finished.

## Is the algorithm fully reconstructible from the normative law?
No. The only normative wording is:
- the schema description of `viewDigests` (`execution-inputs.schema.v1.json:621`), "attributed to this cell/program/U/producer";
- contract §5's "this cell/program's returned views" (`execution-inputs-contract.v1.md:114`, `:222`).

Receipts are per stage, not per cell, so nothing records which cell returned a view. The relation filter exists only in the model (`execution_inputs_model.v1.py:1129-1159`) and the fixture builder (`execution_inputs_fixture.v3.py:226-244`). In every case below, the alternative host encoding changes only `viewDigests`, and nothing but `EXECUTION_INPUTS_VIEW_TOTALITY` refuses it:
- **One view with several relations:** the model names it on every row with a matching relation at U. The one-cell version closes a real Run with `pass`.
- **Unsupported capability with complete inventories:** the row names its returned view, not an empty set. The Run closes `indeterminate`; the empty-set encoding refuses at admission and in the Run.
- **View without a relation for the capability:** it isn't attributed to that row.
- **Same scope:** the model checks universe and relation separately, not on the same scope. Owner admission doesn't hide this: two mutated worlds close real Runs with the model's encoding (one `indeterminate`, one `pass`), and the same-scope encoding refuses. It is masked only when the foreign-universe scope carries Coverage on a supported-available row.

## Where the model contradicts explicit law
Each of these admits and closes a real Run through the maintained `full_run` driver:
- **D1:** the unsupported references row names one view carrying Coverage in two universes. This is exactly what §5 (`:240-241`) "forbids".
- **F1:** that row names a view with a foreign-universe scope that has no Coverage, against §3's "each named scope `sourceUniverse` vs binding U" (`:51`).
- **F3:** supported rows name views with scopes in two universes.

The only scope universe check is in `load_coverage`. Only supported-available accounts with Coverage reach it. So §5's claim that the derivation "already decides" this is false for unsupported-typed rows and for scopes without Coverage.

## Proposed delta (not applied anywhere)
- **Contract §3:** a normative "View attribution" paragraph:
  - universe and relation must match on the same scope;
  - unsupported rows name their returned views;
  - every scope of an attributed view must be in U, for every applicability, or refuse `EXECUTION_INPUTS_COVERAGE_DERIVE` (no new code).
- **Contract §5:** reworded to match.
- **Model and fixture builder:** implement that rule. The builder change is optional.
- **Checker:** 10 new controls with oracles.
- **Schema:** unchanged, no repin.

The patch is `correction.patch` (sha256 `f795b006…`); base and after hashes for the four files are in `delta-manifest.json`.

**Receipts.** Only the owning checker was run, on runtime copies:

| Run | Cases | Mismatches |
|---|---|---|
| Unpatched copy | 76 | 0 |
| Patched copy | 86 | 0 |
| Patched checker on unpatched model | 86 | 7, all on the new controls (D1 and F1 close real Runs) |

The 76 existing cases are field-identical across all three runs, and their 5 full-Run ids are unchanged.

**Consequences.**
- **Existing fixtures:** every view is single-scope at its binding universe, so no digest, row or Run id changes.
- **Shapes like D1, F1 and F3:** they now refuse.
- **Views whose universe and relation match fall on different scopes:** they stop being attributed, which changes their `ExecutionInputsV1` digest and Run ids.
- **Your decision:** I implemented the literal reading, where "named scope" means every scope of an attributed view. A narrower reading, Coverage-bearing scopes only, still needs the D1 fix but would leave F1 and F3 admissible.

## Scope limits
- Admission results are reference self-consistency, because the builder reuses the model. Closed-Run results use the reference driver, not an independent reconstruction.
- Worlds with symbol rows fail Run closure even unmutated (`PAYLOAD_RECORD`). Every Run-level claim was re-measured in worlds without them.
- The candidate-only cell observation is standalone only; its Plan and spec were not reminted.
- Checks that pin these four files' hashes, and text sweeps outside the owning checker, were not run.
- Not assessed: whether the producer and `planId` filters have a normative source.

Preserved failed attempts:
- my first shell call was denied;
- the closed-Run columns for symbol-row worlds failed at baseline;
- the §5 lawful split through the builder failed with `EVALUATION_VIEW_ROOTS`, because the builder captures only attributed views. It was replaced by a host-captured version.

Files are in the runtime folder:
- review.md
- review.json
- correction.patch
- delta-manifest.json
- hash-index.json
- receipts/
- tools/
