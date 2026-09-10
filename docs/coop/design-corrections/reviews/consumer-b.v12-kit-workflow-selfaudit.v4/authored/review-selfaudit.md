# Review-quality self-audit of v3 workflow-scope review

**Self-audit verdict: `REVIEW_QUALITY_CORRECTIONS_APPLIED`**

**Successor workflow-scope verdict: `WORKFLOW_SCOPE_REFUSED`**

This is the same independently fresh kit-only review origin, not a new origin. It audits the v3 `WORKFLOW_SCOPE_ADMITS` (48/48 PASS) against original requirement kinds/verbs and complete owning contracts. It is not authoring, not product qualification, and not whole-consumer `ACCEPT`. Frozen Run `close_run` remains **unverified** and outside this workflow scope.

v3 `workflow-review.md` / `workflow-review.json` / probes are preserved. Consumer snapshot bytes were not modified.

First actual refusal on the 48 in-scope IDs: **`R-CONFIG-CUSTOM-MULTI-BASE`**.

## Input hashes (snapshot bytes unchanged)

| Item | Value |
|---|---|
| Snapshot manifest | `b2e92652443df230f532c7c4eef81110e27ef1be078adbd312bd1c050274f65c` **MATCH** |
| Snapshot files | **PASS 259/259**, 0 fail |
| Kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` **MATCH** |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` **MATCH** |
| Independent checker | `probes/workflow_selfaudit.py` `1d7c40a43a588d9f38ab8f87856ddaacb09ea13f776d6e833ad9561d31328fd3` |
| Results | `probes/workflow_selfaudit.results.json` `6c9521342ef61d359ef943d55ddaa6f082df36cf0ba851150556edd2275dcd56` |
| v3 review.md (preserved) | `7286cd9b6d5a5874150a0ef949317448ec01ee011574ffbe8247d1222a8f6b3f` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. No consumer helper import for expected values. C/H reminted from `identity-and-evidence.md` §3.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output/probes/workflow_selfaudit.py
```

## What v3 got right (confirmed, not authority)

Independently reminted without consumer helper:

- Repair-apply key = raw SHA-256 of `C({operation, projectId, repairPlanId, baseSnapshotId})` `206733ee…`, unequal to mutation-intent H `6a2921ca…`.
- `repairplan2:` / `comparison2:` / `baseline2:` identities remint from published H domains; comparison counts from entries.
- Pivot-only first-axis: B=false, E0=true, E4=false → `CODE-NET-NEW`, not live.
- Scope-only comparison: two scope digests unequal, policy digest equal.
- Synthesized config graph `C` digest `432d4a7f…`; js-shared base identity `b4249ca9…`; node `kind` derived from basename; nodes path-ordered.
- Unknown suffix refuses; clones negatives execute firstRefusal codes; JS body languageId `javascript` ≠ provider `typescript`.
- Candidate-only `kinds=[]`; hostCapture labeled synthetic.
- Command inventory join commandCount 45; query parity field *names* match kit; six StepTermination examples inhabit the closed class vocabulary.
- Graph projection: 3 `calls@resolved-callee` edges; neighbors/path/reach item bytes equal claimed; hopCount 1 is shortest; `file@enumerated` → `QUERY.RELATION_UNSUPPORTED`; cursor *form* `q3.<64hex>.<64hex>.<position>`; `underlyingRunAdmissionUnverified` retained.
- Multi-step envelope: two analysis steps with profiles `default` vs `fit`.

Those confirmations do **not** restore v3’s 48-PASS verdict.

## Quality boundary 1 — independence of expected derivation

v3 `probes/workflow_admit.py` imported consumer `helper.canonical` / `identity` / `evaluator` / `schema_admit` / `body_identity`. Artifact metadata and helper output are **claims under test**, not expected-value authority.

Successor implements C (UTF-8 key order, no whitespace) and `H(D,X)` from `identity-and-evidence.md` §3, exists three-valued from the published atom law, graph projection from `query-projection-contract.v3.md` §3, and config node-kind from `native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law`.

## Quality boundary 2 — vacuous and file-presence PASS

v3 `R-CONFIG-SYNTHESIZED` used `or True`. v3 custom-multi-base and js-shared PASSed if the file loaded.

Successor reminted `tsconfigGraphHash = SHA-256(C(graph))`. Synthesized and js-shared **hold**. Custom-multi-base identity, derived `kind=other` for `tsconfig.app.json`, and path order **hold**, but the original verb requires **repeated bases with retained precedence**. `extendsResolved` is `[strict, base]` then `[base]` — a diamond, not a repeated edge in one sequence (`x-opensip-order: sequence`, later-wins). **PASS withdrawn → REFUSED.**

## Quality boundary 3 — query complete owner vs aggregate counts

Original `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` observable: independently derived complete typed responses, failure envelopes, bound/cursor cases, renderer and summary joins. Owners: `query-projection-contract.v3.md` §§1–8, `graph-query.schema.json`, `workflows-and-surfaces.md` §8.

§8: `query-response` is the **complete owner-admitted GraphQueryResponseV1** (full context, items, optional termination). Host projection must be total over `parityFields`. Aggregate/count comparisons cannot substitute.

Measured on retained `query/parity.json` / `rendererParity`:

| Renderer | Required | Actual |
|---|---|---|
| json `query-response` | complete GraphQueryResponseV1 | `{operation, nItems: 2}` |
| agent | all six parity fields | `resolvedView` / `availability` / `truncated` / `totalItems` / `items`; **no** `query-response`, **no** `termination-class` |
| human | typed content of the response | scalar `view=… avail=… truncated=False total=2 items=2` |

Further retained-cursor law (not invented):

- `neighborsPaged`: `traversalCoverage=truncated-page` with `truncated=true`. Contract §5 / schema: page fullness is `truncated-page`, **`truncated=false`**. `truncated` is true iff `truncated-bound`.
- `nextCursor` `q3.1908c594….2aabcead….1` form-ok; page-2 continuation **not retained**. Independent remaining neighbor is `fact2:ae187938…`.
- SelectionHash C-domain is unpublished; this audit did **not** invent a hash recipe.
- Did **not** invent `QUERY.ENDPOINT_*`, `maxVisitedNodes` truncated-bound, or `native-evidence-unavailable` as extra required cases.

**PASS withdrawn → REFUSED.** Item-byte equality of neighbors/path/reach remains true and is not the complete owner.

## Quality boundary 4 — identity recipe vs pairwise claimed hashes

`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` is `completeRunProperty`. Observable: two retained graphs or an explicit pair vector comparing body identities. Kit: BLV is **derived**; rust `dialect.edition` is integer `{2015,2018,2021,2024}`; ownership never enters BLV.

Pair vector: two ownership maps, derived edition 2018, claimed L0 equal; 2021 map moves claimed L0; `SourceUnitOwnershipV1` required fields present. **No** retained span, `compilerBuild`, or BLV record. v3 guessed `pub fn x() {}` / `"0"*64` and still PASSed because pairwise claimed-hash equality held, recording string-edition as an implementation note.

Original record-kind and identity obligations are not waived because one isolated property held. Claimed L0 `sha256:aa8162f8…` is not independently remintable from retained preimages. **PASS withdrawn → REFUSED.**

## Quality boundary 5 — facts/Coverage vs helper agreement labels

`R-MIN-RESOLUTION-THREE-LEVELS` original: syntactic, resolved, and type, **each with qualifying and insufficient facts/Coverage**.

Retained `vectors/min-resolution.json` is `helper.evaluator.eval_atom` value labels (`qualifyingAgrees: true`). No facts, no Coverage. Independent synthetic exists law (match→true; no coverage→indeterminate; complete coverage no match→false) agrees with the stored *values*. Helper agreement flags are claims, not expected-value authority. **PASS withdrawn → REFUSED.**

`R-MIN-RESOLUTION-REPAIR-EVIDENCE` independently remints `repairplan2:90fbc873…` and binds three rungs — **PASS retained**.

## Quality boundary 6 — standing exhibition vs checklist / labels

`R-CHAIN-ZERO-CONFIG-TO-RECEIPT` (`standingRule`): exhibited by executed traces, envelopes, **and complete Runs** together, not a checklist sentence. v3 PASSed four workflow-file arrows plus `notAChecklistSentence: true`. No Run arrow, no trace arrow. Frozen Run admission is **outside this workflow scope** and must not be silently claimed. **PASS withdrawn → `WORKFLOW_SCOPE_INCOMPLETE`.**

`R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` (`standingRule`): exhibited across syntax/availability/Coverage artifacts; a single label for all four is failure. Retained vector is four narrative strings + `distinct: true`. **PASS withdrawn → REFUSED.**

Standing owner-map / cited-distinction IDs (`R-SUBSYSTEM-OWNERS`, `R-SEMANTIC-VS-OPERATIONAL-AUTHORITY`, `R-MUTATION-VS-ANALYSIS-STEPS`, `R-PROMISE-VS-AVAILABILITY`) remain PASS: those original observables *are* cited reconstruction maps.

## Overbroad refusals corrected

v3 issued **no** refusals on the 48 (all PASS). This audit does **not** refuse:

- `R-RUN-UNSUPPORTED-GRAMMAR` for `.rs` → `rust-syntax` vs kit `rs` (unknown-suffix refusal is the verb).
- `R-JS-CLONE-BODY-THROUGH-TS` for unreminted L0 (languageId vs provider is the verb).

No new schema or requirement was invented.

## Disposition vs v3

| | v3 | successor |
|---|---:|---:|
| PASS | 48 | **42** |
| REFUSED | 0 | **5** |
| WORKFLOW_SCOPE_INCOMPLETE | 0 | **1** |
| **in-scope assessed** | **48** | **48** |

Withdrawn PASSes: `R-CONFIG-CUSTOM-MULTI-BASE`, `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`, `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`, `R-MIN-RESOLUTION-THREE-LEVELS`, `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` (REFUSED); `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` (INCOMPLETE).

## 134-ID mapping (outside-scope retained)

| thisReview | Count |
|---|---:|
| in-scope-executed-PASS | 42 |
| in-scope-executed-REFUSED | 5 |
| in-scope-INCOMPLETE | 1 |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| notReached-historical-vector | 23 |
| out-of-scope-frozen-run | 24 |
| out-of-scope-frozen-run-replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Frozen Run stores remain byte-identical and **unverified** for `close_run`. Whole-consumer `ACCEPT` is **not** issued.

Successor machine-readable review: `workflow-review.json`. Self-audit machine-readable: `review-selfaudit.json`.
