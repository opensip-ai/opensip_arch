I’ll close the remaining v7 comparison/presence gaps in the owned workflow files: waiver-aware pivot presence, exact detector maps, no false-absence placeholders, E2/E3 bound pivots, and envelope failure schema.I'll continue the v8 coauthor on the owned workflow3 model, starting by reading the current pivot, presence, and policy-derivation code against the eight remaining gaps.Reading the model, checker, contract, and root policy-derivation APIs next so the eight gaps can be implemented against the current code.I'll inspect replay fixtures, classify presence, envelope checks, and detector maps so the eight fixes match the actual APIs.I have the eight gaps mapped; next I’ll implement the presence law, exact detector maps, selected-view context, and the E2/E3 plus envelope controls.E0 availability was treating an unbound pivot as globally unavailable and would have marked detector-added cases indeterminate. Tightening that so only per-entry missing E0 is unavailable.Removing the duplicate `art_bool` construction that rebuilds the Boolean graph three times.All 292 checks passed. I'll confirm the v8 report, policy-derivation review, and that v7/foundation were left untouched.v8 coauthor is on the same owned workflow3 model/check/contract. Reports are only under `grok-workflow-projection.v8/`. This is still bounded projection work, not complete admission.

**Receipt:** 292/292 at `/tmp/opensip-design-corrections/grok-workflow-projection.v8/workflow-projection-check.json`. v7 remains 252/252. Passing these checks is not acceptance. Root remints still PASS `open_run_closure` and REFUSE complete semantic close; they are not claimed as owner-admission failures. Main execution v4 is still changing execution-input files and is not wired.

### Fixes

1. **Presence law.** E0–E3 now use `derive_current_matched` (occurrences + `waivedFindingIds` + `emissionBindings`). Waiver pivot: native E3 bind with `waiver_rows` keeps matched presence (`E4` true, `waivedC` true). Wrong current-as-E3 and E2-as-E3 refuse.

2. **E0 detector join.** Exact `{detectorId → (closureId, semanticsMajor)}` map, not a subset of common IDs. Extra/missing IDs and major mismatch refuse, including a reminted baseline with an extra detector.

3. **Detector change / no false-absence.** `compare_admitted` derives `detectorChanged` from that map. It does not hardcode false and does not copy E1→E0 when the map changed. Unbound changed axes stay `null`; comparison presence allows null for E1–E3. Distinguishing control: major-only detector change + measured `E0=false,E1=true` is `DETECTION-DELTA`, not `CODE-NET-NEW`.

4. **Context.** Relations come from admitted selected views / `evaluationInputRefs` only. An unselected ambient fact does not appear.

5. **E2/E3 + Boolean coverage.** Full native owner + public `close_run` graphs: scope-only E2 and waiver-only E3 bind, plus wrong-substitution refusals. `AND(false, partial-required-history)→pass` and `OR(true, partial-required-history)→fail` keep retained causes and `requiredCoverage=satisfied`. Determinate Boolean truth is not turned into an unknown-coverage regression.

6. **Envelope / shared codes.** `kind=failure` requires `errors` and **prohibits** `run`, including a schema-valid AnalysisResult. `EVALUATION.REQUIRED_OUTPUT_OMITTED`, `INPUT_REFUSED`, and `SELECTION_LIMIT` stay in the shared enums; isolated-additions prose now names them and says not to fork registration.

7. **Host `any`.** Deepcopy of host comparison metadata only. Admitted detector closure `platform` stays `any` after compare. No untrusted `compatibleWith`.

8. **Policy-derivation peer review (foundation unread-write).** Gaps are in the v8 JSON and `policy-derivation-peer-review.v8.md`.

### `derive_policy_result` / `admit_policy_result` gaps (no foundation edits)

- Thin projection from an already-replayed Run: `{schemaVersion, planId, proofBundleId, policyDigest, waiverDigest, verdict}`. Not a substitute-policy API; it does not recompute verdict under caller policy bytes.
- A different policy/waiver needs its own admitted Plan+Run. The 4-control checker remints `verdict` / `policyDigest` / `waiverDigest` only. No second real Plan, no extra/missing descriptor fields, no mixed `schemaVersion`.
- Descriptor omits snapshot, detector/emission, scope, evaluation state, execution deficiencies, and waived findings, so it cannot serve as E1/E3 evidence.
- No independent join that those digests equal the replayed Plan blobs, or that `waivedFindingIds` are the effective waiver set.
- Identifier domain is `policy-derivation3`. This projector must not mint or admit it.

Foundation, products, commit/push, and subagents were not used.
