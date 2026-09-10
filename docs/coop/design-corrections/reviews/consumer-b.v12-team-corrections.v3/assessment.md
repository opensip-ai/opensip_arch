I’ll continue in the v3 team copy: verify kit and team-input hashes, read the new structural refusal and its notReached limits, then complete only the syntax-code pilot’s admission and fresh-process proof replay.The structural refusal is the evaluator closure missing from `plan.semanticClosures`. Next I’ll read the cited law, the peer’s notReached limits, and the remaining applicable joins.I'll pick up the bounded v3 pilot from path-correction and predecessor preservation, then implement the remaining structural joins and a full proof replay.I'll read the structural refusal, the current pilot helper, and the kit laws that still apply to this syntax-code graph.Path correction and predecessor stores are in place. Next I’ll read the pilot builder and the kit laws that still need to be joined.The builder still omits the evaluator from `plan.semanticClosures`. I’ll read the rest of the graph construction and the kit contracts that govern it.I’ll pull the remaining kit contracts for execution-inputs, closure membership, and component-manifest so the rebuild matches the actual owners.I’ll implement the remaining joins in helpers first: evaluator membership, execution-input derivation, component-manifest retention, and an annotated-owner walk.I’ll clean the annotated-owner walker, then wire it into graph load and the pilot builder.I’ll update the pilot builder next: evaluator membership, view-only stage outputs, native-coverage totality, and derived cell outcomes.I’ll rebuild the syntax-code graph now and treat any admission failures as remaining work, not as a relabel of the old store.The builder produced a new Run identity. Next I’ll run a fresh-process proof replay and a discriminating tamper against the exported store.I’ll write the reconstruction record and the bounded pilot-completion review, listing remaining obligations instead of claiming whole-consumer acceptance.**Verdict: `PILOT_READY_FOR_VALIDATOR_RECHECK`**

This is not whole-consumer acceptance and not `ACCEPT-RECONSTRUCTABLE`. The peer structural refusal was an existing membership law, not a new gap: `evaluation-seal.evaluatorClosure` must be in `plan.semanticClosures`. That omission is corrected on a **new** identity graph. Old bytes were not relabeled as accepted.

## What changed

The evaluator is now a Plan-selected semantic closure (direct member). Detector is selected as an extra closure. The dependent graph was reminted:

| Record | NEW | Structural-refused predecessor |
|---|---|---|
| Run | `run3:1ee613d2fd191b215e2f7ab56662ab70616ce303a55bd29f596299f481690081` | `run3:f2542b3a…` |
| Plan | `plan2:61407daf2c6f656c5258e1616907ae949fed63a1f4f6511572c395cfc6326471` | `plan2:e3965f2f…` |
| Proof | `proof3:e88715da47e0c07c715c580a8061c3c7df888ed82d1e08d17b3bc8582577e86b` | `proof3:59d3b680…` |
| Store | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` (889618 bytes, 90 blobs) | `2e74a6b2…` (867956, 79 blobs) |

Snapshot `snapshot2:f50135a27d89a1fa…` is unchanged (same `hello.rs`). Both failed predecessors remain:

- original: `preserved-failures/syntax-code-original/` `8b0f6d82…`
- structural-refused: `preserved-failures/syntax-code-structural-refused/` `2e74a6b2…`

Also joined for this exact pilot, rather than treating peer PASS rows as admission: view-only stage outputs, `selectedRefs` exact totality, `derive_outcome` joined to all three required cells (`complete`), native coverage accounts for every matrix pair of the requested capabilities, component-manifest stored-byte join without v11 stock inhabitance, and an annotated-owner digest/order/membership walk (103 hits).

## Fresh-process proof

Replay over the exported store: `proofCompareEqual` true, derived verdict `pass`, atom `false`, expected proof C SHA-256 `2c735b76…`. Tamper changes the claimed logical result (verdict/atom/rule outcome) with citations preserved: stale-hash C inequality is recorded separately from semantic refusal (`tamperedProofId` `proof3:3a69570d…`).

Other four Run stores and scope-v2 outputs were not rewritten.

## Remaining obligations

- Independent validator recheck; this walk is not root admission.
- `ROOT-ADMISSION` was not performed.
- `component-manifest-schemas.v11` remains `CANDIDATE-NOT-APPLIED`; stock inhabitance and signature-envelope verification are not claimed.
- L1 token-stream tokenization was not executed.
- This Plan explicitly requests three capabilities. Default-profile remaining syntax-only matrix cells are not cells of this Plan.
- Unexecuted original requirements outside this pilot stay visible.

Reviews: `pilot-completion-review.md` (`049c8e6f…`) and `pilot-completion-review.json` (`458fa912…`). Exact graph bytes, reconstruction script, and before/after hashes are under `output/runs/syntax-code.*`.
