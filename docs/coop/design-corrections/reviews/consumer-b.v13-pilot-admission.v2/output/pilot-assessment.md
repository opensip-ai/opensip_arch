# Pilot-admission.v2 — completeness audit of the TS law map

**Verdict: `PILOT-CHECKPOINT-COMPLETED`**

`reconstructionAccepted` is **false**. `rootAdmission` is **unobserved**. This is not whole-task acceptance.

v1’s `pilot-law-map.json` used grouped PASS rows with `measuredResult: "no errors; operands compared"` and several construction-only `checkingFunction`s. That is not executed admission. This checkpoint inventoried **every** `x-opensip-*` annotation on schemas selected by the TS pilot (462 annotations, 65 nested law-table rows, 36 keywords) **without filtering by existing handlers**, then reconciled each keyword to an executed checker or an inapplicable/catalog reason. Unmapped OPEN keywords: **0**. See `inventory/x-opensip-inventory.json` and `inventory/coverage-reconciliation.json`.

## First measured boundary (preserved)

`law_admit.run_all` on the v1 export refused:

`COVERAGE_SOURCE_VARIANT_MIXED_COMPLETE` on clones Coverage whose subjects mixed `.ts` with json config/lock/manifest paths.

Kit: `identity-schemas.v3.json#/x-opensip-digest-domains/scopeCapabilityLaw` — a `bodyIdentityJoin` relation under `closed-suffix-table` cannot claim `complete` over a mixed supported/unsupported scope.

Preserved bytes: `inventory/ts-before-scope-capability-correction.store.json` and `inventory/law-admit-first-run.json`.

Correction: complete clones Coverage over dialect-supported `src/index.ts`; unknown Coverage over json paths with `language-tier-unsupported` / `capability-missing`; clones-fact cell **partial**; one `execution` deficiency on the proof. Fail still dominates (five file.exists findings). Original clones L0/L1 facts, node_modules, import, ScopeDocument, config graph remain.

## walk_order hole found by a negative

Reversing file inventory rows **passed** until `walk_order` was fixed to enter `properties` on `allOf`/`then` schemas that omit `type: object`. After the fix the same mutation refuses `ORDER_OR_DUPLICATE` (`NEG-INVENTORY-ROW-ORDER`). That unexpected pass is recorded, not hidden.

## Isolated negatives (15/15 refused)

`inventory/negatives.json`. Families include uniqueness, matrix vocabulary, default caps, subject language, coverage cause, scopeCapabilityLaw (v1 bytes), TargetAttributionV2 external-package `evaluationNativeId`, selectedRefs totality, candidateSourcePaths, VCS fabricated Coverage, kind derivation, payloadSchemaDigest, native atom `evidence`, H-frame C(X) under H, inventory row order. Identities reminted where the mutated field is part of the record identity.

## Measured positive export

| | |
|---|---|
| Run | `run3:9bb6c377ff3c44e66131475005b74cafe3900ed7a37c2e0320d3b55f206db50e` |
| Store SHA-256 | `b62d7aedc9f257c56bd7a88b74739123172615e0b032af0af9ec94fd0fac62e5` |
| Proof C | `86c3c464387ccadf15645ca78551fdcb1deed3457a9bc628ebe83ff1896d08fd` claimed = derived |
| Verdict | `fail`; 5 findings; 1 execution deficiency |
| Fresh replay | `pilot_ts_fresh_replay.py` PASS |

Law map statuses are `errorCount` plus operand digests, not a boolean PASS flag as the check.

## Not done

Rust/syntax Runs, graph query, workflow vectors, original 123/8/3. Copied executed flags are not authority. D9 successor and `F-*` stay declared future/qualification.
