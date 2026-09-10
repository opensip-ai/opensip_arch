I'll start from the full prompt and our current TS-pilot helpers, then audit the actual admission/closure/replay path against the kit.I'll start by copying continuation.v2 into this checkpoint's output, then rebase helper paths and audit the actual TS admission/replay bodies rather than the named functions.The destination already has an output tree; I'll inspect custody and whether it's an exact continuation.v2 copy before rebasing.Output already matches continuation.v2. Next I’ll rebase write/import paths, then read the helper bodies that the TS pilot actually calls.I'll rebase Python OUT paths to this checkpoint, then read the helper bodies the TS constructors actually call.Paths are rebased. Next I’ll read the remaining helper bodies and the TS constructors they actually invoke.Core helpers are in view. Next I’ll read the TS constructors and the kit schemas those constructors actually admit.Replay currently feeds stored `subject3` records into `compose_proof` instead of deriving enumeration from retained owners. I’ll inventory the kit laws that actually apply to this TS pilot.I’ll extract the kit’s x-opensip, registry, and digest-domain laws for the TS records, then read the matching contract prose.Clones body-identity and independent subject enumeration look like real gaps. I’ll read those contract sections next and confirm what the helpers actually check.I’ll implement the missing owner checks and a corrected TS constructor so replay derives subjects from retained inventories instead of stored `subject3` lists.I’ll add the owner-check helpers and a corrected TS constructor, then wire them into close/replay.I’ll write the corrected TS constructor so inventories, cell outcomes, and independently derived subjects are actually retained.Admit and fresh replay both passed. Next I’ll measure each applicable law against the exported bytes and confirm the original TS properties are still present.I’ll write the checkpoint ledger, helper-correction record, assessments, and continuation guide from the measured TS export.**Verdict: `PILOT-CHECKPOINT-COMPLETED`.** `reconstructionAccepted` is **false**. `rootAdmission` is **unobserved**. This is not `ACCEPT-RECONSTRUCTABLE` and does not finish the original 123/8/3 reconstruction.

This checkpoint audited the actual TS admission/closure/replay **bodies** against the kit, then corrected the one TypeScript complete Run. Continuation.v2 function names, copied executed flags, and equal outputs from the same incomplete helper were not treated as implemented law.

## What was wrong in continuation.v2

`close_run` did call `compose_proof`, but replay selected subjects from stored `subject3` (one `src/index.ts`), not from retained inventories. H-identity admission accepted “object exists” without parsing the framed preimage. Clones `bodyIdentityJoin`, U-4, expected inventories, cell outcomes, and analysis-spec parameter cardinality were not executed at close.

Those are helper omissions with kit answers, not missing recipes. Failures are preserved (`pilot/continuation2-ts.store.json`, `pilot/ts-corrected-admission-failure.json` `ORDER_OR_DUPLICATE` on unsorted `inventoryRefs`, `pilot/helper-corrections-pilot-admission.json`).

## Measured TS export

| | |
|---|---|
| Run | `run3:36658b14c908d10d051535c276b845f8ec04558167d915e163548aee69d75dd9` |
| Store | `runs/ts.store.json` SHA-256 `b868de2e3f95f3167b5638f2e73d6279d15ebae9b98eedc698053ff656dca789` |
| Objects / blobs / frames | 138 / 240 / 137 |
| Schema admission + close_run | pass |
| Fresh-process replay | pass; complete proof C `8cd0293c6054ac40af21e4cff6d8f9c3497acbc8ee87b188a9dd961ddb816944` claimed = derived |
| Independently derived file subjects | all five inventoried paths; five `file.exists` findings; verdict `fail` |
| H-frames | 67 parsed; blob under H is the frame, not C(X) |

Original attached properties remain: TypeScript sources, `node_modules/left-pad` layout blobJoin, config-graph extends, imported runtime payload, ScopeDocumentV1, file-inventory totality, L0/L1 clones.

`pilot-law-map.json`: **21 PASS, 0 FAIL, 0 OPEN, 3 INAPPLICABLE** (count-at-most/all-covered/imported-atom; incoming-search; D9 host-invariant successor). Inapplicable rows are unselected on this input, not validator inflation.

## Still pending (unchanged original scope)

Rust, rust-partial, syntax-code, syntax-data, graph query, and the workflow/envelope/vector collections were **not** executed here and are **not** marked executed. Copied `requirement-status.json` flags are historical. D9 successor and `F-*` stay in their declared scope.

Durable guide: `next-work.md`. Reproducible commands are in `pilot-assessment.json` and `pilot/commands-and-checks.json`. Root independently admits these exact exported frames next.
