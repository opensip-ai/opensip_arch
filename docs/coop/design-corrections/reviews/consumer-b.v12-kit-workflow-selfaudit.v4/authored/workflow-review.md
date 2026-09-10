# Workflow-scope independent review (successor after self-audit)

**Verdict: `WORKFLOW_SCOPE_REFUSED`**

This is a bounded independent kit-only review of another actor’s authored workflow snapshot, after a review-quality self-audit of the v3 `WORKFLOW_SCOPE_ADMITS`. Same fresh origin, not a new origin, and **not** independent acceptance of this reviewer’s own prior authoring. Frozen Run stores were hash-verified only; their `close_run` admission is **unverified**. This is **not** whole-consumer `ACCEPT`.

First actual refusal on the 48 in-scope IDs: **`R-CONFIG-CUSTOM-MULTI-BASE`**.

## Input hashes

| Item | Value |
|---|---|
| Snapshot manifest | `b2e92652443df230f532c7c4eef81110e27ef1be078adbd312bd1c050274f65c` **MATCH** |
| Snapshot files | **PASS 259/259**, 0 fail |
| Kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| `requirements.json` | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| Independent checker | `probes/workflow_selfaudit.py` `1d7c40a43a588d9f38ab8f87856ddaacb09ea13f776d6e833ad9561d31328fd3` |
| Results | `probes/workflow_selfaudit.results.json` `6c9521342ef61d359ef943d55ddaa6f082df36cf0ba851150556edd2275dcd56` |

Python: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Source metadata names `/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v1/output` — that actor directory was **not** read. Snapshot bytes were not reminted. Consumer helper was **not** used as expected-value oracle.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-selfaudit.v4/output/probes/workflow_selfaudit.py
```

## 134-ID mapping (outside-scope retained)

| thisReview | Count |
|---|---:|
| in-scope-executed-PASS | **42** |
| in-scope-executed-REFUSED | **5** |
| in-scope-INCOMPLETE | **1** |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| historical vector notReached | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

Full rows: `workflow-review.json#/original134`. Copied historical claims are not accepted by copy.

## First actual refusal

**`R-CONFIG-CUSTOM-MULTI-BASE`** (`standaloneConfigVector`).

Original: custom-named project config inheriting from multiple ordered bases, **including repeated bases with retained precedence**. Owner: `TypeScriptConfigGraphV1.nodes[].extendsResolved` is a **sequence** (later entry wins); repeated edges are retained.

Independently reminted `C(graph)` digest `d255328620db516fcf9fd557bc05b27971a14fa494c49fb6d57b9efd582989a9` **matches** claimed `d255328620db516fcf9fd557bc05b27971a14fa494c49fb6d57b9efd582989a9`. Node kinds derive from basename (`tsconfig.app.json` → `other`). Nodes are path-ordered. Entry extends `[tsconfig.strict.json, tsconfig.base.json]` — multiple ordered distinct bases. **No node’s `extendsResolved` contains a repeated edge.** A diamond in which `tsconfig.base.json` is reached from two parents is not the required repeated-base sequence.

v3 PASSed on file presence. That grade is withdrawn.

## Other in-scope refusals

### `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`

Independently projected **3** `calls@resolved-callee` edges; neighbors/path/reach **item bytes equal** claimed; hopCount **1** is shortest; `file@enumerated` refuses `QUERY.RELATION_UNSUPPORTED`; failure envelope is CommandEnvelope `kind=failure` with no `run` field; cursor form ok; `underlyingRunAdmissionUnverified` retained.

Unmet complete owner (`query-projection-contract.v3.md` §§1–8 + `workflows-and-surfaces.md` §8):

- json `query-response` is `{operation: graph.neighbors, nItems: 2}`, not complete GraphQueryResponseV1.
- agent renderer omits `query-response` and `termination-class`.
- human renderer is aggregate counts, not typed response content.
- `neighborsPaged`: `traversalCoverage=truncated-page` with `truncated=true` (law: page fullness ⇒ `truncated=false`).
- `nextCursor` retained; page-2 continuation **not** retained. Independent remaining neighbor: `fact2:ae187938251decc58da9159520daef3516f0086c99e9b0377ba401e087dbb29f`.

v3 aggregate runId/availability/truncated/totalItems/nItems comparison is withdrawn as a substitute for full parity.

Did **not** invent `QUERY.ENDPOINT_*`, visited-node cap, or `native-evidence-unavailable` cases.

### `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`

`completeRunProperty`. Two ownership maps, derived edition 2018, claimed L0 equal; 2021 moves claimed L0. **No retained span / compilerBuild / BLV.** Kit identity recipe is not remintable from this pair vector. Pairwise claimed-hash stability of a non-kit encoding does not satisfy the property. v3 implementation-note waiver is withdrawn.

### `R-MIN-RESOLUTION-THREE-LEVELS`

Retained vector is helper `eval_atom` value labels, not qualifying/insufficient facts/Coverage at three levels. Independent synthetic exists law still yields indeterminate / false / true as published. Helper `qualifyingAgrees` flags are claims under test.

### `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING`

`standingRule`. Four narrative strings are not exhibition across syntax/availability/Coverage artifacts.

## In-scope incomplete (not a silent Run claim)

**`R-CHAIN-ZERO-CONFIG-TO-RECEIPT`** (`standingRule`): original exhibition is traces, envelopes, **and complete Runs** together, not a checklist sentence. Retained four arrows are workflow files only (`notAChecklistSentence: true` is itself a flag). Frozen Run admission stays **out of scope / unverified**. This ID is `WORKFLOW_SCOPE_INCOMPLETE`, not a `close_run` claim.

## In-scope PASS (42) — selected current owners

Repair/comparison/baseline H remints, mutation-intent inequality, pivot/scope/E0–E3 classifications, synthesized and js-shared config identities, candidate-only cells, host-capture synthetic label, clones negatives with firstRefusal, JS languageId vs provider, unknown-suffix refusal, multi-unit missing advertised clones, inventory join (45), six StepTermination examples, CommandEnvelope failure shapes + D9 exit join, single-step and multi-step (default vs fit) InvocationRecords, durable receipt/availability nested records, detector listing-file vs manifest-body, three-valued exists vector `indeterminate`, repair-evidence plan identity bound to three rungs, test/prep/repair authorization envelopes, cited standing owner maps.

Per-ID selectors: `workflow-review.json#/scope48`.

## Frozen Runs

Five stores match `frozen-run-hashes.json` byte-for-byte. That is **not** Run admission.

## Limitations (not waivers)

1. Frozen Run `close_run` / other-Run replay remain out of scope.
2. `ROOT-ADMISSION` of exported frames was not performed.
3. Real host/OS/compiler/crypto is future qualification.
4. SelectionHash C-domain is unpublished; form was checked; a hash recipe was not invented.
5. Whole-consumer `ACCEPT` is **not** issued.

Genuinely absent/contradictory kit laws: **none**. Existing-law implementation misses are listed in `workflow-review.json#/implementationMissesVsAbsentLaw` and are not treated as missing design.
