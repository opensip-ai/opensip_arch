# Pilot full review (successor of fresh-export-admission.v1)

**Verdict: `PILOT_FULL_ADMITS`**

Same P5 data-only kit origin. This is not a new fresh origin and not whole-consumer ACCEPT. Semantic replay was executed on two new exact stores. Real host/compiler/crypto qualification is not claimed.

Predecessor all-six structural refusals are **historical** and were not assumed to apply to these bytes.

## Input custody

| Item | SHA-256 | Result |
|---|---|---|
| original 80-file kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS |
| parent frozen subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | PASS |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | PASS |
| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | PASS |
| **new** export-manifest.json | `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f` | PASS |
| exports/syntax-code.store.json | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` (889218 bytes) | PASS |
| exports/syntax-code.tamper.store.json | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` (893046 bytes) | PASS |

Claimed RunIds:

- positive: `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`
- tamper: `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c`

Stores were not reminted. Checker copied from predecessor output with mechanical path redirects; predecessor sources and diffs are under `predecessor/`.

## Per-graph status

| Graph | Structural | Semantic | First failure |
|---|---|---|---|
| syntax-code (positive) | ADMIT | **REPLAY_MATCH** | none |
| syntax-code.tamper | ADMIT | **REPLAY_REFUSE** (required negative) | `REPLAY_PROOF_MISMATCH` after structural admit |

Tamper identities, schema, citations, and native/closure joins **admitted** before the logical disagreement was counted. That disagreement is therefore a valid semantic negative, not a structural mask.

### Positive — independently derived proof equals retained claim

From Plan-selected EnumerationPlanV1 + file inventories, one subject was derived: `subject3:8bf8bec7…a3ab` (`hello.rs`, syntax universe, kind=file). No claimed `selectedSubjectIds` were used as population.

Atom `none` of `file@enumerated` with filter `subject eq hello.rs`: a retained `file` fact with `path=hello.rs` is a known match, so **none = false** (identity §4 table). `emitWhen` is false → no finding. Gating rule with no live finding → rule outcome `pass`, sealed verdict `pass`.

Complete proof C SHA-256 `eb2a3bd6…ae71` equals the retained proof. Enclosing identities equal the claimed Run:

- proof3 `8b21407c…a521`
- evidence3 `4746de6f…925b`
- seal3 `df983e7b…c713`
- run3 `4b58935a…ff7b`

L0-verbatim and L1-lexical clone body frames were retained and re-hashed under their actual `normalisationLevel` (not a global invented body law).

### Tamper — structural admit, then semantic refuse

Independently derived proof is the **same** as the positive (`none=false`, verdict `pass`, no findings, proof C `eb2a3bd6…ae71`).

Retained claimed proof disagrees:

- claimed verdict `fail` vs derived `pass`
- claimed finding `finding3:0c895614…3cdb` vs derived none
- claimed proof C `2d2df6df…c9da`
- claimed Run `run3:8e81be4e…b49c` vs derived `run3:4b58935a…ff7b`

Mismatches: `PROOF_C_MISMATCH`, `VERDICT_MISMATCH`, `FINDING_IDS_MISMATCH`, `PREDICATE_PROOFS_MISMATCH`, and therefore evidence/seal/Run identity mismatches. Count/verdict-only comparison was not used.

## Helper correction (kit-only)

Predecessor Run-closure treated every prose `required` flag on `component-manifest-schemas.v11.json` as a Run refusal (`stableId` missing).

**Original failure:** `COMPONENT_MANIFEST_REQUIRED_FIELD` / `stableId`.

**Kit selector:** security-and-lifecycle.md **S1** — delivery selector is `manifestSchema.platforms[]` (`os`, `arch`, `tree` TreeCommitment, `entrypoint`) plus RJ-3. `stableId` uniqueness is host install-registry admission against a live index, which is not a retained Run operand.

**Correction:** Run-closure admits stored manifest bytes under the metadata profile, requires `kind=component`, forbids embedded signatures, and projects `type=file` TreeCommitment rows onto `closure.tree`. Install-registry `stableId` is not a Run-closure join.

## Original Phase 5 / Phase 9 pilot requirement map

Executed on these two stores (not a claim that all 134 consumer IDs are done):

| ID | Kind | Status on this pair |
|---|---|---|
| R-RUN-SYNTAX-CODE | complete Run | executed (syntax-only, no TS/Rust compilation unit) |
| R-RUN-NO-COMPILER-UNIT | property | executed |
| R-RUN-CLONES-L0-AND-NORMALIZED | property | executed (L0-verbatim and L1-lexical frames retained and joined) |
| R-VALIDATE-OWNING-SCHEMA | Phase 9 | executed |
| R-INDEPENDENT-CLOSURE-JOINS | Phase 9 | executed |
| R-OBJECT-TABLE-FRAMES | Phase 9 | executed (exported stores) |
| R-FROM-SCRATCH-COMMAND | Phase 9 | executed (`standalone-checker/check.py`) |
| R-REPLAY-AFTER-ADMISSION | evaluatorReplay | executed after structural admit |
| R-REPLAY-ENUM-AND-IDS | evaluatorReplay | derived subject3 from inventories |
| R-REPLAY-PREDICATE-WITNESS-VERDICT | evaluatorReplay | `none=false`, witness, verdict `pass` |
| R-REPLAY-NO-CALLER-TRUTH | evaluatorReplay | claimed proof fields not used as population/truth |
| R-REPLAY-COMPARE-BUNDLE | evaluatorReplay | complete proof C + enclosing H compared |
| R-REPLAY-EXPORT | evaluatorReplay | `replay/*.replay.json` |
| R-REPLAY-THREE-VALUED | evaluatorReplay | known match ⇒ `none` false, not indeterminate |
| R-REPLAY-TAMPER | evaluatorReplay | structural admit then semantic refuse |
| R-NEGATIVE-FIRST-REFUSAL | standing | first semantic refusal recorded; later not fabricated |
| R-HELPER-KIT-ONLY | standing | S1 correction preserved |

Not in this bounded pair: other language Runs, query reconstruction, remaining Phase 6–8 vectors, whole-consumer ACCEPT.

## Existing-law vs missing recipe

No missing or contradictory recipe was required to decide these two graphs. The tamper refusal is an **existing-law** complete-replay mismatch (composition contract §7 / identity §4). The `stableId` issue was a predecessor helper over-application, not a kit gap.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-full-review.v1/output/standalone-checker/check.py
```

or `standalone-checker/reproduce.sh`.

## Limitations

- Bounded to these two syntax-code stores. Not all 134 original reconstruction obligations.
- Graph-query reconstruction is outside this successor prompt.
- No root/product/compiler qualification.
- After a graph’s first refusal, later laws on that graph are notReached (tamper stops acceptance at replay compare; structural work had already admitted).
- Import atoms were not exercised (no Plan imports on these graphs).
- `all-covered` / incoming-search sufficiency paths were notReached (the committed rule is `none` of `file@enumerated`).
