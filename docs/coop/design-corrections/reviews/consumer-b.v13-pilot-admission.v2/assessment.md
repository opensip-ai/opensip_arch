This is a completeness audit of the previous TS pilot-law-map, not a new subject. I’ll copy v1, rebase helpers, then inventory every kit annotation before reconciling coverage.v2 already has an output tree. I’ll confirm it’s an exact v1 copy, then rebase helper paths.Paths are rebased. Next I’ll extract every `x-opensip-*` annotation from schemas the TS pilot actually selects, including nested law tables.I’ll read the nested law tables that previous PASS rows never executed, then reconcile them against the actual checker bodies.Clones complete Coverage over JSON paths likely violates `scopeCapabilityLaw`. I’ll add executed registry checkers, then run them against the current export.Positive graph is clean. Next I’ll run isolated negatives for each newly executed law family, reminting identities where the mutated field is part of the identity.The row-order negative passed because `walk_order` only entered object properties when `type==object`. I’ll fix that so `allOf`/`then` order annotations actually run.**Verdict: `PILOT-CHECKPOINT-COMPLETED`.** `reconstructionAccepted` is **false**. `rootAdmission` is **unobserved**. This is not whole-task acceptance.

v1’s law map was a selected list of familiar checks with `measuredResult: "no errors; operands compared"` and construction-only `checkingFunction`s. That is not executed admission.

## Completeness inventory (unfiltered)

Every `x-opensip-*` annotation on schemas selected by the TS pilot was extracted with full values and nested law tables: **462 annotations, 65 nested table rows, 36 keywords** in `inventory/x-opensip-inventory.json`. Coverage reconciliation maps each keyword to an executed checker or an inapplicable/catalog reason. **Unmapped OPEN: 0.** Prose joins are in `inventory/prose-joins.json`. The v1 map is preserved as `inventory/previous-v1-pilot-law-map.json`.

## First real refusal (preserved, then corrected)

`law_admit` on the v1 export refused clones Coverage that claimed `complete` over mixed `.ts` and json paths (`COVERAGE_SOURCE_VARIANT_MIXED_COMPLETE`). Kit: `identity-schemas.v3.json#/x-opensip-digest-domains/scopeCapabilityLaw`. Bytes kept in `inventory/ts-before-scope-capability-correction.store.json`.

Correction: complete clones Coverage on `src/index.ts`; unknown Coverage on json paths with `language-tier-unsupported` / `capability-missing`; clones-fact cell **partial**; one execution deficiency. Fail still dominates (five `file.exists` findings). node_modules, import, ScopeDocument, config graph, and L0/L1 clones were not removed.

A second hole showed up only as a negative: reversing file inventory rows **passed** until `walk_order` was fixed to apply `x-opensip-order` under `allOf`/`then` even when `type` is omitted. After the fix the same mutation refuses `ORDER_OR_DUPLICATE`.

## Isolated negatives

**15/15 refused** (`inventory/negatives.json`): uniqueness, matrix vocabulary, default caps, subject language, coverage cause, scopeCapabilityLaw, TargetAttributionV2 external-package `evaluationNativeId`, selectedRefs totality, candidateSourcePaths, fabricated VCS Coverage, kind derivation, payloadSchemaDigest, native atom `evidence`, H-frame C(X) under H, inventory row order.

## Measured positive

| | |
|---|---|
| Run | `run3:9bb6c377ff3c44e66131475005b74cafe3900ed7a37c2e0320d3b55f206db50e` |
| Store | `b62d7aedc9f257c56bd7a88b74739123172615e0b032af0af9ec94fd0fac62e5` |
| Proof C | `86c3c464387ccadf15645ca78551fdcb1deed3457a9bc628ebe83ff1896d08fd` claimed = derived |
| Fresh replay | PASS |

Revised `pilot-law-map.json` records `errorCount` and operand digests, not a boolean as the check. **23 PASS, 0 FAIL, 0 OPEN, 4 INAPPLICABLE** (repair imported-requirement-law, FactBatch occupancy return, syntax-only grammar registry, count-at-most/incoming-search).

Rust/syntax Runs, query/workflow vectors, and the rest of 123/8/3 remain pending. Guide: `next-work.md`.
