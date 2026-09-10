# Pilot completion review — syntax-code Run (consumer-b.v12 team v3)

**Verdict: `PILOT_READY_FOR_VALIDATOR_RECHECK`**

This is not whole-consumer acceptance, not `ACCEPT-RECONSTRUCTABLE`, and not root admission. Peer structural grades and the 63 prior PASS rows are claims, not a waiver of original norms. The original 123 reconstruction IDs plus standing and future IDs remain visible; this pass executed only the bounded syntax-code pilot.

## Standing and custody

| Object | SHA-256 | Result |
|---|---|---|
| kit `consumer-input-manifest.json` | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | matches expected |
| parent frozen SHA | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | matches expected |
| 80 subject files | as listed in `hash-verification.json` | PASS 80/80; kit bytes not edited |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| peer `closure-review.json` | `30d967aace2e248cf70d00560ae56b6b2d2edf749ca27607f245fc58d0c5383a` | PASS vs `team-inputs.json` |
| peer `closure-review.md` | `e6c326fb5929564fb9d8680944cbc62c4c075b0f3ce1bf8baf8e0a42f1253f38` | PASS |
| peer `structural_admit.py` | `8de222540b12d63471d93d9b6f59643cd034b4478db585dcd9ecf51077a24423` | PASS |
| peer `structural_admit.results.json` | `14c75cf6c40adb8996eac7b84902e2a34fe7da6f1900370cd879641bbc3b11d1` | PASS |

Write root is only `consumer-b.v12-team-corrections.v3/output`. Scope-v2 workflow/vector outputs and the other four Run stores were not rewritten.

## Peer structural refusal (existing law)

Selector: `identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership`. Direct member `evaluation-seal.evaluatorClosure` must be in `plan.semanticClosures`. Extra closures may be selected; omitting a direct member is not permitted.

Measured on the structurally refused predecessor (`2e74a6b2…`): evaluator `closure2:2a9cfd92…ccec` retained and equal to `proof.evaluatorClosure`, absent from `plan.semanticClosures` (`UNSELECTED_EVALUATOR_CLOSURE`). That predecessor is kept at `preserved-failures/syntax-code-structural-refused/`. The original failing store remains at `preserved-failures/syntax-code-original/` (`8b0f6d82…`). Neither was relabeled as accepted.

Peer `NOT_REACHED` that this pass owns for the pilot: `EXECUTION-INPUTS-OUTCOME-DERIVE` and `SEMANTIC-PROOF-EVALUATION` (complete proof replay). `ROOT-ADMISSION` remains not performed.

## Mechanical path correction

Copied helper/scripts originally hardcoded v2 absolute `OUT`/`KIT` paths. Before executing copied scripts those literals were redirected into this v3 copy. Record: `path-correction-record.v3.json` (SHA `5e381f922f4861f9c7aa5d0169869ff2d6f591492bd4d5b8f8f8ed7700a89704`; rewritten 17, unchanged 13). Scope-v2 JSON artifacts were not rewritten by that pass.

## Semantic corrections (not a relabel)

1. `plan.semanticClosures` now selects provider, evaluator (direct member), detector (extra; emission-plan `detectorClosure`), and grammar (extra; also `selectedThroughOtherInput` via `plan.nativeContextDigests`).
2. Stage `outputDomains` is the reference fixture `["view"]`. Receipt `outputRefs` are view-only. Inventories are `hostDerivedRefs`. `selectedRefs` is exact totality: complete-receipt views ∪ view `coverageIds` ∪ cell-outcome inventory digests.
3. `CellProgramOutcomeV1.state` is derived (`derive_outcome`) then joined to the host row. All three required cells derived `complete`.
4. Native coverage accounts cover every matrix pair of the requested cells: clones-fact `clones@normalized-body-hash`; inventory `file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported` (`inapplicable-vcs` because VCS `kind=none`); syntax `declares|literal|control-flow@syntactic`.
5. Component-manifest bodies are retained C-encoded synthetic observations: `SHA-256(stored bytes) = closure.manifestDigest`; projected `type=file` rows equal `closure.tree`; version/name/selected kind join the closure. `component-manifest-schemas.v11` is `DESIGN-CONTRACT-CANDIDATE` / `CANDIDATE-NOT-APPLIED` / binds NOTHING — stock inhabitance is not claimed. Signature envelopes are not verified. `DetectorManifestV1` does not occupy `manifestDigest`.
6. Annotated-owner admission walks `x-opensip-digest` / `x-opensip-order` / `closureMembership` on the records this graph actually contains (103 digest-field hits on this export). A name-heuristic `*Digest` walk is not the law used.

The entire dependent identity graph was reminted. New bytes were not labeled as the old Run.

## NEW export identities

| Record | NEW | Predecessor (structural-refused) |
|---|---|---|
| Run | `run3:1ee613d2fd191b215e2f7ab56662ab70616ce303a55bd29f596299f481690081` | `run3:f2542b3a…` |
| Plan | `plan2:61407daf2c6f656c5258e1616907ae949fed63a1f4f6511572c395cfc6326471` | `plan2:e3965f2f…` |
| Proof | `proof3:e88715da47e0c07c715c580a8061c3c7df888ed82d1e08d17b3bc8582577e86b` | `proof3:59d3b680…` |
| Snapshot | `snapshot2:f50135a27d89a1fa20bd4534f45d0e9f1633379a683b47c70dcec907e46911cd` | unchanged (hello.rs / source inventory unchanged) |
| Evaluator closure | `closure2:a8a0903d…4b0a` ∈ `plan.semanticClosures` | retained but unselected |
| Store SHA-256 | `0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36` (889618 bytes, 90 blobs) | `2e74a6b2…` (867956, 79 blobs) |

Exact graph bytes: `runs/syntax-code.store.json`. Reconstruction script: `scripts/pilot_syntax_run.py`. Before/after: `runs/syntax-code.before-after.json`. Reconstruction record: `runs/syntax-code.reconstruction-results.json`.

## From-scratch commands and measured outcomes

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output/scripts/pilot_syntax_run.py
# measured: exit 0; all listed stock schema checks stockOk; builder closureOk true
# NEW run3:1ee613d2…  plan2:61407daf…  proof3:e88715da…

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output/runs/syntax-code.store.json
# measured: exit 0; proofCompareEqual true; closureOk true; firstRefusal null
# expectedProofId == claimedProofId proof3:e88715da…
# proof C SHA-256 2c735b764b6728a7d832841071324c4c8fadf658eb999fe4db5afeb47f876357
# derivedVerdict pass; derivedAtomValue false; findingCount 0
# annotated digest-field hits 103; derive_outcome[0..2] all-complete:complete
# evaluator direct member selected; selectedRefs totality 11; stage outputDomains view-only

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output/scripts/replay_from_export.py \
  --tamper \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v3/output/runs/syntax-code.store.json
# measured: exit 0; citationsPreserved true
# stale-hash control: C(tampered) != C(claimed) true (not treated as semantic replay)
# semantic replay: independently reconstructed expected proof remains verdict=pass / atom=false
# tampered claim verdict=fail; reminted tamperedProofId proof3:3a69570d…
# expected C != tampered C; refused true
```

Full proof is derived from exported selected inputs, not saved truth flags. Tamper changes the claimed logical result (verdict, atom value, rule outcome) and still exercises the full comparison; a stale-hash C inequality is recorded separately from semantic refusal after structurally valid input admission.

## Applicable-law assessment (this exact pilot)

| Law / owner | Applicability | Result |
|---|---|---|
| closureMembership direct evaluator in `plan.semanticClosures` | applicable | PASS (evaluator selected) |
| equalToDirect proof.evaluatorClosure = seal.evaluatorClosure | applicable | PASS |
| enumerator/view/stage producer = provider and selected | applicable | PASS |
| extra detector selected (emission-plan binds it) | extra allowed | PASS |
| grammar kind + tree retention | applicable | PASS |
| ExecutionInputs selectedRefs exact totality | applicable | PASS (11 refs) |
| stage outputDomains view-only; inventories host-derived | applicable | PASS |
| `derive_outcome` join to host rows | applicable | PASS (three required cells complete) |
| native coverage account totality for requested capabilities | applicable | PASS (7 accounts) |
| VCS `kind=none` → vcs-change `inapplicable-vcs` | applicable | PASS |
| annotated `x-opensip-digest` preimage on graph records | applicable | PASS (103 hits) |
| relation payload registry + C digest + ladder | applicable (file, declares, clones, control-flow) | PASS |
| component-manifest stored-bytes join | applicable | PASS as synthetic observation |
| component-manifest v11 stock inhabitance | owner is CANDIDATE-NOT-APPLIED | not claimed |
| TypeScript/Rust native-context snapshotJoins | not on this graph | N/A |
| import payloads / finding-fingerprint | no imports, no findings | N/A |
| L1 token-stream tokenization judgment | level-spec freedom | NOT executed |
| SEMANTIC-PROOF-EVALUATION (complete expected proof from selected inputs) | applicable; owned this pass | PASS (fresh process) |
| logical-result tamper vs reconstructed expected proof | applicable | PASS (semantic refuse) |
| ROOT-ADMISSION | not demanded this pass | NOT performed |
| real crypto / OS / compiler enforcement | not demanded | NOT performed |

## Frozen this pass (unchanged)

| Store | SHA-256 |
|---|---|
| `runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| `runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| `runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| `runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |
| `scope-correction-review.json` | `554ec31f8c6dd1c2e5eb039fe8992024d935faf7f1f25621ae0771b3274d9b97` |
| `scope-correction-review.md` | `5ac6722a5b98c00ecd9668fcaedba7aae44d2bc9edd44b5c8877ae677fd0db31` |
| `scope-reconstruct-results.json` | `38297cc654512dc236d7923d687daaccb138ec0abf6df2a30e7fe17feb794f1d` |

## Remaining obligations

These are not waived. They keep this verdict a recheck request, not acceptance.

1. Independent validator recheck of this NEW graph. This consumer walk is not root admission.
2. `ROOT-ADMISSION` over exact exported frames was not performed.
3. `component-manifest-schemas.v11` remains `CANDIDATE-NOT-APPLIED`. There is no sealed applied JSON Schema for the component-manifest body in the kit. Stock inhabitance is not claimed. Signature-envelope / catalog association is not verified (real crypto is not demanded).
4. L1 token-stream tokenization judgment was not executed; level-specification bytes are retained.
5. This analysis-spec explicitly requests three capabilities (`clones-fact`, `inventory`, `syntax`). Default-profile remaining syntax-only matrix cells (`imports` / `references` / `calls` / `types` / `reachability` / `unresolved-edge` UNSUPPORTED-TYPED, and `clones-near` candidate-only) are not cells of this Plan. `R-RUN-SYNTAX-CODE` asks inventory and syntax/clone facts, which this graph carries. If a later review requires `default_capability_selection` completeness, that work is still open.
6. Other four Run stores, scope-v2 envelopes/vectors/query, and unexecuted original requirements outside this pilot remain visible and unverified by this pass.
7. Whole-consumer `ACCEPT-RECONSTRUCTABLE` is not issued.

Python used: `/tmp/opensip-architecture-review-env/bin/python -I -B`.
