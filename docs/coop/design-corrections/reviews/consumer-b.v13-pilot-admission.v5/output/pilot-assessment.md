# consumer-b.v13-pilot-admission.v5

**Verdict:** `PILOT-CHECKPOINT-COMPLETED`  
**reconstructionAccepted:** false  
**rootAdmission:** unobserved  
Whole-task `ACCEPT-RECONSTRUCTABLE` remains prohibited. Original 123 + 8 standing + 3 `F-*` items are unchanged and still required afterward.

This checkpoint finishes the original TypeScript complete-Run **full structural admission** and **complete per-field prose derivation** before any expansion.

## A. One full structural entrypoint

`closure.structural_admit(st, run_id)` is the same function for the original positive, an exported fresh reload, and the reminted semantic negative. It is not schema admission alone.

It executes, in order: published schema/`x-opensip-*` keywords; an explicitly selected Run (not prefix uniqueness); Plan/snapshot/evidence/seal/proof joins; capability-manifest recompute; native context/universe H-frames and TypeScript field joins; fact relation-registry laws; view totality/partition and `coverage_view_use`; producer and retained `CoverageResultV3` admission; U-4, enumeration, execution-inputs, and `law_admit.run_all`; grammar-capability applicability from the actual universe domain.

`closure.semantic_replay` is a separate stage. `close_run` is structural THEN semantic, so a structurally valid false claim can reach replay.

## B. Native-evidence prose vs every retained native instance

Account: `inventory/native-prose-account.json`.

- 17 registered `(relation, rung)` pairs from the relation registry.
- 13 pairs have a CoverageResultV3 in this graph (14 coverage2 rows because clones has two partitions). Fact-free entries (calls/types/reachability/declares/literal/control-flow/unresolved-edge, …) are judged the same way as entries with facts.
- 4 pairs have no Coverage instance; inapplicability operands are recorded, not treated as malformed-input refusals: `vcs-change@vcs-reported`, `references@syntactic-name-match`, `calls@syntactic-callee-name`, `types@annotated`.
- 10 fact2 records; TypeScript native context and universe retained.
- Grammar-capability-registry is **inapplicable**: this graph’s universe domain is `native.semantic-universe.typescript.v2`, not syntax.

RC-0, RC-1, RC-2, RC-4, RC-5, RC-6, §4.1a commitment/key-scope/`payloadSchemaDigest`, §4.5 `deadCodeRepairEligible`, and §2.4 libSelection→component membership run at **producer input** (`make_coverage`) and again from **retained bytes**.

First full-graph RC-1 refusal on the v4-positive bytes is preserved: `inventory/v5-first-rc1-structural-refusal.json` against `inventory/v5-before-rc1.store.json`. The builder’s extra Coverage loop had minted non-resolved rungs as `state=complete, attempted=True`. Kit selector: native-evidence.md §4.3 RC-1. After remint, those entries use the published not-applicable defaults.

## C. Mechanical field account

`prose-law-account.json`: **170** schema fields of the selected output records (proof-bundle, predicateProofs/ruleResults entry shapes, finding + nested correspondence/subject, semantic-evidence, evaluation-seal, run, predicate-witness, evaluation-subject, policy-derivation, ExecutionInputsV1). **0** `field='*'`. **0** unaccounted paths. **170** executed claimed-vs-derived (or retained-input) comparisons with actual C bytes. Complete proof C equal; `outputMismatches` empty.

## D. Selected Run derivation

Replay follows `run3:f7525dc7bd003dedd4b67aed1c67a460502c24b5e75a7c3050fd1a28fc20213e` and that Run’s Plan/Evidence/proof/seal references. Proof C `91b449ff37674a10032896ea47e9025696b3cf5e981d72f86f1549ab4584a3a2`. Verdict fail/fail. 5 subjects, 5 findings, 5 witnesses. Original TS attached properties retained (node_modules/bare imports, configuration/dependency graph, ScopeDocument, imported payload, inventory/file facts, exact/normalized clone bodies). Claimed graph is not rewritten during validation.

## E. Exact exports and the semantic negative

| Graph | Path | Store SHA-256 | Structural | Semantic |
|---|---|---|---|---|
| Positive | `runs/ts.store.json` | `f71af38af2d90acaf6846b04e92463791cf81b82619185e6b5576717c767f5ae` | `structural_admit` pass | `semantic_replay` pass |
| Negative | `runs/ts-semantic-negative.store.json` | `ff65d146660a80a4217b1f3135f5f6164672c8822ffda2cf2edf0ab23181bb17` | **same** `structural_admit` pass | **same** `semantic_replay` refuse |

Both exports carry `objectTable`, all blobs, and frames. Each was round-tripped in a fresh process.

Negative mutation: `finding.severity error → note`, then reminted finding/proof/evidence/seal/run. Structural admission did not fail on missing metadata, absent bytes, or stale identities. Semantic refuse is complete-C mismatch (`findingIds` / reminted finding): claimed proof digest `bea89606…`, derived `91b449ff…` (the positive proof).

Bounded native/prose controls (`inventory/native-prose-controls.json`) all passed: RC-6 complete∧¬exhaustive; RC-1 non-resolved `state=complete`; §4.1a commitment mismatch; lib name whose `lib.dom.d.ts` is not retained; grammar inapplicability is **not** a refusal.

## F. Exact schema tracing preserved

v4 exact matching remains at `inventory/v4-exact-matching.json`. After the RC-1 remint, v4 required-occurrence instance ids were stale (`inventory/v5-stale-required-after-rc1-remint.json`, 517 missing). Required occurrences were re-derived from the current graph (still 1245 conditions, new instance ids). Current exact result: **1245 required, 5024 traces, 0 missing**. Omit-one-field and cross-document-pointer negatives still leave OPEN.

## Executed / inferred / unexecuted / limited

**Executed:** full structural function; native Coverage/context prose comparisons including no-fact entries; mechanical per-field C; selected-Run complete replay; exact positive+negative exports; exact 4-tuple schema tracing.

**Inferred:** ASCII compiler `lib` names, the Unicode default-lowercase fold coincides with `str.lower()` (stated in code against native-evidence.md §2.4).

**Unexecuted this turn:** rust and syntax complete Runs; graph-query/workflow collections; unused atom ops on this program (`count-at-most`, `all-covered`, `none`); remaining identity-and-evidence.md contiguous read beyond selected joins; the whole original 123/8/3 set.

**Limited:** no product implementation; no real OS/compiler/crypto/storage qualification; root admission unobserved.

## Helper corrections (kit selectors, not new design gaps)

See `pilot/helper-corrections-v5.json`. Principal items: RC-1 extra_cov mint; structural/semantic split; field-account wildcards; schema-only negative; Run selection; omitted RC-0/2/6/§4.1a/lib joins.
