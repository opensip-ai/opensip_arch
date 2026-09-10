This is the same origin, not a reset. I’ll read the full continuation prompt, then rebase work into the new output directory and finish the missing admission/replay path.I’ll rebase helpers onto the continuation output, then implement the missing SelectedEnumeratorRef admission and a real schema/closure/replay pipeline for one pilot Run.I’ll rebase output paths, then add a real kit-schema registry and admission engine so the pilot Run can be validated against every `$ref` and published keyword.I'll continue the same-origin session from the captured TS admission failures, rebase to the new output directory, and finish the required pilot pipeline rather than treating prior statuses as done.I'll inspect the captured TS admission failures, helper output paths, and the construction code so the four kit-selector fixes can be applied without losing original failure artifacts.I'll locate the four construction sites in the builder and related helpers, then apply the kit selectors without overwriting the original failure artifacts.I'll read the construction sites and the kit schemas for SelectedEnumeratorRef, WaiverSet, importer, and configGraphPaths so the fixes match the published shapes.I'll check remaining construction details—scope subjects, file payloads, ClosureId, AvailableProgramBinding, and native-context snapshot joins—before applying the four kit-selector fixes.I'll preserve the original TS artifacts, apply the four kit-selector construction fixes, and extend admission so nested records named by digest domains are actually validated.I'll preserve the original TS artifacts, then apply the kit-selector construction fixes and nested-record admission.Nested-record admission was resolving identity-bundle selectors incorrectly, and the TS unit used `languageFamily: typescript` instead of the kit enum `tsjs`. I'll fix both and re-run admission.Schema admission is now down to one refusal: the predicate-witness `programPredicateDigest` preimage is not retained. I'll inspect the witness construction and retain that record.TS schema admission and closure passed. Next I’ll reload the exported bytes in a fresh process, re-admit, derive the complete proof, and compare.The TS pilot pipeline passed: owning-schema admission, closure, fresh-process reload, and complete proof comparison. I’ll preserve the other original Run artifacts, then run the same pipeline on them.I'll rebase statuses onto continuation artifacts, write the continuation checkpoint, and produce an honest review that records the completed admission and replay work.Same-origin continuation of `consumer-b.v13` is finished. The first-pass **ACCEPT-RECONSTRUCTABLE** is withdrawn: `SelectedEnumeratorRef` was approximated and owning-schema admission with `$ref`s, published keywords, and joins had not actually run on the exported frames.

## What was missing, then executed

The TypeScript Run was the pilot. Original exported frames refused owning-schema admission. Those failures are preserved at `pilot/ts-original-admission-failure.json` and `pilot/original-first-pass/` (store SHA-256 `98bf22d4…`, identical to the untouched original session output).

Four kit-selector construction bugs were corrected (helper omissions, not design gaps):

| Failure | Kit selector | Correction |
|---|---|---|
| `configGraphPaths` not UTF-8 sorted | TypeScriptConfigProjectionV2 `x-opensip-order: utf8` | `["tsconfig.base.json","tsconfig.json"]` |
| WaiverSet `schemaFamily` | `opensip.product.waivers` | plural `waivers` |
| `imports.importer` | SubjectIdV1 | `symbol:src/index.ts::x` |
| enumerator `{closureId}` | SelectedEnumeratorRef | `{status:"selected", closureId}` |

Then the required pipeline actually ran: schema admission (including selected `$ref`s and `x-opensip-*`), retained closure/joins, fresh-process reload, independent complete-proof derivation and field comparison.

## Measured Runs

| Run | Admit | Close | Fresh complete-proof equal |
|---|---|---|---|
| ts | yes | yes | yes |
| rust | yes | yes | yes |
| rust-partial | yes | yes | yes (indeterminate) |
| syntax-code | yes | yes | yes |
| syntax-data | yes | yes | yes |

Fully reminted false-result graph: structural identities/joins still admitted; recomputed complete proof rejected the altered claimed verdict (`vectors/false-result-remint.json`).

Seven negatives were invoked on the admission/evaluation path; all seven produced observed refusals (`vectors/negatives-invoked.json`). Graph neighbors/path/reach/cursor/history/limit/parity were reconstructed over the admitted TS Run.

## Standing and verdict

- Continuation: `consumer-b.v13-continuation.v1`
- Kit/parent hashes unchanged: manifest `afa3abfb…`, parent `fa8cdc79…`
- Original kit and original session output were not modified
- 131 executed, 0 unexecuted, 0 failed, 3 future-qualification
- **Verdict: ACCEPT-RECONSTRUCTABLE**
- Root admission of the exported frames remains **unobserved** and is a separate later gate

Deliverables are under `/tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output`: `blind-review.md`, `blind-review.json`, `requirement-status.json`, `checkpoints/phase-12.json`, plus the retained raw stores, fresh replays, original failures, and helper corrections.
