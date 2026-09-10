I’ll treat this as the same kit-only session, now covering full structural admission plus independent semantic proof replay of the new syntax-pilot snapshot.I'll continue the same kit-only session: verify the v2 snapshot, then independently recheck structural admission and full semantic proof on the new syntax pilot.The v2 output directory is empty. I’ll verify the snapshot hashes, then read the prior closure review and the new pilot completion claims.Manifest SHA matches. Next I’ll hash all 245 snapshot files and pull the prior closure review plus the new pilot-completion claims.Snapshot is 245/245. Next I’ll pull kit laws, the prior checker, and the new producer/evaluator code so the independent replay isn’t driven by consumer claims.I’ll read the rest of the prior checker, identity-schema owners, and the new helper/evaluator code next.I’ll dump the new store’s claimed records next so the independent checker can remint proof bytes from kit law, not from consumer replay.I have the kit owners and the claimed graph. Next I’ll write an independent checker that re-admits structure, remints expected proof from kit law, and compares exact bytes.Writing the independent admission and replay probe next, driven from kit selectors rather than the consumer evaluator.The probe will remint from kit C/H, walk annotated digest owners (not name suffixes), and compare independent expected proof bytes.The independent remint matches every proof field except extra `evaluationInputRefs`. I’ll widen the annotated-digest walk so unexecuted owners aren’t missed, then write the review.I’ll extend the annotated-owner walk to the remaining present records (execution-inputs, inventories, payloads, native context) so those laws are actually executed.Independent remint is complete: prior evaluator-closure refusal is gone; the new first refusal is extra `evaluationInputRefs`. Writing the admission review next.**Verdict: `PILOT_REFUSED`.** This is not whole-consumer `ACCEPT` and not product qualification.

Structural admission and semantic replay were scored separately on the new syntax-code store (`0a0b2c62…`, 889618 bytes). Snapshot manifest `0a953ef9…` matched; all 245 files passed. The graph was not reminted or repaired.

| Axis | Outcome |
|---|---|
| Structural admission | **`STRUCTURAL_REFUSED`** |
| Semantic replay | **`SEMANTIC_REFUSED`** |
| Prior finding `UNSELECTED_EVALUATOR_CLOSURE` on **this** graph | **PASS** |

**Prior refusal, rechecked.** Evaluator `closure2:a8a0903d…4b0a` is now in `plan.semanticClosures` (kind=evaluator) and equals `proof.evaluatorClosure` / `seal.evaluatorClosure`. The predecessor first refusal is preserved, not relabeled accepted, at `preserved-failures/syntax-code-structural-refused/` (`2e74a6b2…`).

**First actual refusal on this graph:** `EVALUATION-INPUT-REFS-EQUALS-SELECTED-PLUS-MANIFEST` — existing incorporated law, consumer correction, not absent law.

Kit owners (`evaluator-composition-contract.v3.md` §1 and `execution-inputs-contract.v1.md` §7) require `evaluationInputRefs = selectedRefs + {execution-inputs}`. Independently recomputed `selectedRefs` has 11 members; kit-expected proof refs are 12. The claimed proof has 14: extras are `rule-program` `77b07390…` and `policy` `f7532ddc…`. Those already have their own proof/Plan fields.

**Independent expected proof** (fresh process, consumer evaluator not used as oracle):

- Verdict `pass`, atom `false`, 0 findings, 1 predicate proof
- Expected identity `proof3:0388fb97…` / C SHA-256 `8764a0ac…`
- Claimed identity `proof3:e88715da…` / C SHA-256 `2c735b76…`
- The only differing field is `evaluationInputRefs`. Adding the two extras as a diagnostic makes C and identity match the claim; that is not a waiver, and `proof3:0388fb97…` is not labeled as the consumer’s accepted case.

**Tamper.** Same Plan and selected inputs, not a replacement graph. Logical-result mutation (`verdict=fail`, atom `true`, rule `fail`) independently remints to the consumer-claimed `proof3:3a69570d…` while reconstructed expected remains `pass`/`false`. Stale-hash (digest flip only) is a different identity (`proof3:5b95c8aa…`) and is not that semantic refusal.

**Coverage on this graph (re-executed, not inherited):** 126 laws — PASS 114, REFUSED 2, N/A 8, NOT_REACHED 2 (`ROOT-ADMISSION`, L1 token-stream). `selectedRefs` totality 11, `derive_outcome` all-complete for the three requested cells, annotated `x-opensip-digest` owners 114/0 (not a `*Digest` suffix walk). Default-profile remaining matrix cells were not demanded for this explicit selection.

Deliverables are only under `/tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v2/output/`: `pilot-admission-review.md` / `.json`, `probes/pilot_admit.py`, and preserved prior reports.
