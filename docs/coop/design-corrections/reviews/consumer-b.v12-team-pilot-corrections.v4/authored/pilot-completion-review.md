# Pilot completion review — existing-law remint of copied S-origin syntax-code pilot (v4)

**Verdict: `PILOT_READY_FOR_INDEPENDENT_RECHECK`**

Same THREE-AUTHOR kit-only team session. Workflow authoring remains frozen in its own branch. This is bounded authoring of the existing syntax-code pilot copied from S-origin pilot-v3, **not** independent acceptance of these newly authored bytes and **not** whole-consumer `ACCEPT` / `ROOT-ADMISSION`.

Original B12 charter (`57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec`) is ORIGINAL TASK REQUIREMENTS. Starting copied output verified against `starting-output-manifest.json` SHA-256 `384f7d34c31a5b5a06fd4132fec7ad1f7e0678af0e0e8f0c7309e2b9fde2d49a` (280 files, MATCH). Peer team-inputs SHA-256 `6be937751a008d89ae5cdd9bbc8ebd4c8be9e029c26428f5af401ea574427d5d` (MATCH).

## Peer existing-law correction applied

P4 `law-interaction-review` disposition **`RESOLVED_EXISTING_LAW`** (not a demonstrated normative contradiction):

- MUST: predicate `inputRefs` ⊆ `evaluationInputRefs` (identity-and-evidence.md §3).
- MUST: `evaluationInputRefs` = `selectedRefs` + {execution-inputs} (enumeration §7 / composition §1 / execution-inputs §7).
- MUST: `selectedRefs` domain enum excludes `rule-program`.
- PERMIT: `ProofInputRef.domain` includes `rule-program` as shared type vocabulary (deficiencies/cache keys), not a command to select it on predicates.
- Bind the program with required `proof.ruleProgramDigest` and `program-predicate.ruleProgramDigest`.

S-origin live store `8c3b68ab…` / proof `proof3:0388fb97…` was shape **B** (subset FAIL). That is an **existing-law reconstruction mistake**, preserved at `preserved-failures/syntax-code-s-origin-pilot-v3/`. No absent or contradictory norm was demonstrated. No normative edit.

Correction: `compose_proof` no longer inserts `domain=rule-program` on `predicateProofs[].inputRefs`. Checker `s3_closure` enforces the subset MUST on every predicate inputRef (the previous diagnostic skip is withdrawn). Complete proof/evidence/seal/Run reminted from selected inputs (`usedClaimedProofFields=[]`).

## Charter Phase 9 vs these graphs

Admission (schema including published keywords, retained closure, cross-record joins) then independent proof reconstruction from selected inputs, then C compare. Tamper must **admit** identity/schema/citation joins **before** the deliberate semantic disagreement is reached. Semantic replay is `notReached` when structural fails. This tamper is a whole replacement graph with reminted witness/finding3/evidence/seal/Run; selected view/facts/coverage remain. It is **not** a hidden-input or malformed graph labelled as a successful semantic negative. `--stale-hash` remains a separate control.

## Exports (reminted this pass)

| Graph | SHA-256 | bytes | Run | Proof | Structural | Semantic |
|---|---|---:|---|---|---|---|
| Positive | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` | 889218 | `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b` | `proof3:8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521` | PASS | PASS (proof/evidence/seal/run C equal) |
| Tamper | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` | 893046 | `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c` | `proof3:f8527d3d4b8f5543ac1c85c4b7d7c5153eeab4718dc038f5cc1c5827768b3d90` | PASS | REFUSE expected still `proof3:8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521` |

Positive replay exit **0**. Tamper-export exit **0**. Tamper-store replay exit **1** (semantic C unequal; structural `firstRefusal` none). Stale-hash exit **0**.

Tamper claimed verdict `fail` / atom `true` with unmatched `finding3:0c895614e41c2e8a04fe8a22e04d4e7870d2d0dc38a099dddc019c1387d03cdb`. Independent reconstruction from the same selected inputs remains `pass` / `false`. Input citations preserved (`evaluationInputRefs`, `executionInputsDigest`, view facts including file `fact2:852404c1…`). Witness digest reminted.

## L0 / L1 clone custody (unchanged selected-input identities)

| Object | Identity |
|---|---|
| file fact | `fact2:852404c12751162c8a75c1c9e67465d2be7b356602fa2f663e03fa838849a717` |
| clones L0 | `fact2:7dcdff1dcacbc89a291bc9084cd8d537a7ff9bd6fc606a794e5fe703f7f344b8` bodyIdentity `sha256:72a35a8b39ca25929a4b2f0be6ef1288ebca9192fd04ad7cce37acd372390b36` |
| clones L1 | `fact2:664472f8157073e0c71e7d12a4156b6f33cdcdba94da5da1180158b31e1cb270` bodyIdentity `sha256:874cf4bd66165db89dd7b65b2c8d5caf6bf53edaa3ca5868a9b2d1da55190426` |

Frames and preimages remain retained. Token/body custody is unchanged; only enclosing evaluator outputs reminted.

## §3 inventory

115/115 paragraphs mapped. 0 unmapped. 0 applicable paragraphs without an executed assertion. Full table: `normative-law-audit.md`. Operands: `normative-law-audit.json`.

## Original pilot property coverage (this remint)

`R-RUN-SYNTAX-CODE`, `R-RUN-NO-COMPILER-UNIT`, `R-RUN-CLONES-L0-AND-NORMALIZED`, `R-REPLAY-AFTER-ADMISSION`, `R-REPLAY-ENUM-AND-IDS`, `R-REPLAY-PREDICATE-WITNESS-VERDICT`, `R-REPLAY-NO-CALLER-TRUTH`, `R-REPLAY-COMPARE-BUNDLE`, `R-REPLAY-EXPORT`, `R-REPLAY-THREE-VALUED`, `R-REPLAY-TAMPER`, `R-HELPER-KIT-ONLY` executed against the new bytes. `R-ROOT-ADMISSION-EXPORT` export is retained; root outcome unobserved.

## notReached / unexecuted limitations

- L1 tokenisation judgment (level-spec freedom; frame/custody executed).
- `component-manifest-schemas.v11` stock schema (prose).
- ROOT-ADMISSION (charter: unobservable in this session).
- Other four Run stores not reminted (byte-frozen). Peer `OTHER_RUNS_REFUSED` stands on those exact frozen stores.
- Positive finding emission (atom is none-of-file → false). Tamper claimed outputs emit unmatched finding3.
- `close_run` / graph-query over this Run (workflow branch frozen).
- Actual host/compiler/product qualification.

A paragraph-inventory count, earlier S-origin readiness, and this author's prior review grades are **not** acceptance of these exact new bytes. Scope-ready is not whole-consumer ACCEPT.

## Frozen (byte-identical)

| Object | SHA-256 | bytes |
|---|---|---:|
| `runs/ts.store.json` | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` | 642462 |
| `runs/rust.store.json` | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` | 496105 |
| `runs/syntax-data.store.json` | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` | 476183 |
| `runs/rust-partial-clones.store.json` | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` | 494017 |
| `scope-correction-review.json` | `554ec31f8c6dd1c2e5eb039fe8992024d935faf7f1f25621ae0771b3274d9b97` | 64301 |
| `scope-correction-review.md` | `5ac6722a5b98c00ecd9668fcaedba7aae44d2bc9edd44b5c8877ae677fd0db31` | 6684 |
| `scope-reconstruct-results.json` | `38297cc654512dc236d7923d687daaccb138ec0abf6df2a30e7fe17feb794f1d` | 18250 |

Starting-manifest: 246 of 280 files unchanged. Path redirect before execution: `path-correction-record.v7.json`. Prior failed bytes retained under `preserved-failures/`.

## From-scratch commands

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/pilot_syntax_run.py
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py --tamper /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.tamper.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/scripts/replay_from_export.py --stale-hash /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/runs/syntax-code.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-team-pilot-corrections.v4/output/probes/normative_s3_audit.py
```

Measured exits: reconstruct 0, replay 0, tamperExport 0, tamperStoreReplay 1, staleHash 0, s3Audit 0.
