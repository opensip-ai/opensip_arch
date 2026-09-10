# Workflow-scope independent review

**Verdict: `WORKFLOW_SCOPE_INCOMPLETE`**

Same fresh-origin kit-only team session, **REVIEWER** of another actor's V-origin workflow snapshot. This session authored the syntax-code **pilot** examples, not this snapshot. This is not independent acceptance of that pilot, and no prior positive or negative grade is authority.

Not whole-consumer ACCEPT. Not ROOT-ADMISSION. Frozen Run `close_run` remains unlabeled unverified.

## Custody

| Object | SHA-256 / result |
|---|---|
| snapshot-manifest.json | `93926c8f2dbf1b45ab06e3479ad4e06ebf40405de0eef4a6a5ef6a040d773999` MATCH 285/285 |
| original-consumer-charter.txt | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` |
| kit consumer-input-manifest.json | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |
| source path (provenance only, not read) | `consumer-b.v12-team-workflow-corrections.v3/output` |

Isolated execution copy: `output/isolated-work` with hardcoded author ROOT/OUT/KIT/requirements redirected **before** any consumer-code run. Path-only diff of 21 `.py` files: `output/path-correction-record.json` (`allPathOnly=true`). Original snapshot and five frozen Run stores were not rewritten.

Independent probe: `output/probes/independent_measure.py` using `/tmp/opensip-architecture-review-env/bin/python -I -B`. Expected values derived from kit recipes and reviewer-chosen inputs (`Entry.main` / `Lib.helper` / `Lib.leaf`), not from consumer fixtures or key-presence assertions. Author `workflow_correct_test.py` / `query_charter_test.py` both exited 0 as helper self-consistency only, not expected-value authority.

## Verdict

46 of the established 48 workflow-scope IDs are **executed** under their original kinds. Two remain **INCOMPLETE**:

1. `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` — charter requires reconstruction over **already admitted retained Run(s)**. The author marks this incomplete pending `close_run`. Independent measurement agrees. Algorithmic adapter coverage is not Run admission and is not reported as a completed public wrapper.
2. `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` — arrows join config/envelopes/traces to frozen store hashes with `closeRun=pending`. The standing requirement is exhibited by executed traces, envelopes, **and complete Runs** together.

Missing/contradictory normative law: **none**. Adapter gaps below are **existing-law reconstruction** misses on the query helper, recorded as remaining binding under the already-incomplete query ID.

## Query law coverage (full charter paragraph now supplied)

The full original query paragraph (charter lines 209–212) was omitted from an earlier condensed handoff and is now actually supplied. Conclusions are reassessed without changing source semantics or inventing extra per-language Run demands.

| Owner | Law | Independent status |
|---|---|---|
| contract §1 | projectId equals admitted Run; view {runId}|{snapshotId}|{latest:true}; resolvedView {runId} only; latest from host.latestRunId never static bytes; snapshot uniqueness via host.runsForSnapshot; factViewDigests admitted or QUERY.FACT_VIEW_UNAVAILABLE | **algorithmic-measured**; synthetic close_run; admitted-Run pending |
| contract §2 | vertex domain = inventory ∪ projected endpoints; malformed→PARAMS_MALFORMED; package without PMP or >1 match→ENDPOINT_AMBIGUOUS; zero match→ENDPOINT_UNKNOWN | **reconstruction-gap**; package without packageManifestPath was admitted (success) instead of QUERY.ENDPOINT_AMBIGUOUS. Endpoint unknown/malformed measured PASS. |
| contract §3 | graph-projectable table; file@enumerated QUERY.RELATION_UNSUPPORTED; imports without TargetAttributionV1 omitted; UTF-8 tuple order | **algorithmic-measured**; reviewer facts Entry.main→Lib.helper/Lib.leaf; weaker rung request refused |
| contract §4 | closed params; neighbors/path/reach units; BFS fact2 order; includeStart default false; shortest hop-count path | **algorithmic-measured** |
| contract §5 | page fullness truncated-page truncated=false; operation bound truncated-bound truncated=true; continuation view.runId; cache ignored; cursor q3.runHex.sel.pos; completeness=required → QUERY.COMPLETENESS_UNMET | **algorithmic-measured** |
| contract §6 | totalItems qualified by countBasis; GraphEvidenceDisclosure; native-evidence-unavailable only when no selected view matches relation@rung; advisory const false | **reconstruction-gap**; empty neighbors with selected matching view2 still emitted native-evidence-unavailable (over-disclosure vs §6). No-selected-view case correctly discloses. |
| contract §7 | failure kind=failure nonempty errors no run field; host.requestId req1_+32hex precondition; schemaMajor≠3 SCHEMA_MAJOR_UNSUPPORTED; availability purged/expired/unavailable/corrupt refuse HOST.IO_FAILURE | **algorithmic-measured** |
| contract §8 | execute_graph_query(request, run, objects, blobs, host) requires close_run then projects from admitted views/payloads; traverse_projected_graph algorithmic only | **remaining-binding**; close_run required PASS (without it QUERY.VIEW_UNKNOWN). Wrapper still takes caller projected_edges and does not project from objects/blobs. Public wrapper not completed. |
| workflows-and-surfaces §8 | six parity fields resolved-view/availability/truncated/total-items/termination-class/query-response; query-response is complete GraphQueryResponseV1; compact QueryResult items=page count, truncated=context flag, completenessMet iff countBasis=exact, nextCursor iff context token | **reconstruction-gap**; six-field exact projections PASS on human/json/agent. Helper does not emit CommandEnvelope.query QueryResult / completenessMet. Independently derived QueryResult from context is well-formed; consumer does not produce it. |
| charter query paragraph | three operations over already admitted retained Run(s); retain executable vectors; pagination after newer latest or cache loss; evidence limitations ≠ stored-edge completion; operation bounds vs page; malformed/mismatched + lawful failure envelopes with synthetic host.requestId; complete parity with compact summary joins | **INCOMPLETE**; algorithmic cases exist; admitted-Run measured results do not. Frozen stores: no calls@resolved-callee; TS imports@resolved-target without TargetAttributionV1. Record executed only when retained vectors AND measured results exist over admitted Runs. |
| graph-query.schema.json major3 | GraphQueryRequestV1 / GraphQueryResponseV1 / CommandEnvelope failure inhabitance | **algorithmic-measured**; independently produced request/response/failure stock-valid |

Independent query first measurements (reviewer inputs, synthetic `close_run` labeled): three operations PASS; canonical UTF-8 order PASS; `file@enumerated` → `QUERY.RELATION_UNSUPPORTED` PASS; page fullness `truncated-page`/`truncated=false` PASS; operation bound `truncated-bound`/`truncated=true` PASS; `completeness=required` → `QUERY.COMPLETENESS_UNMET` PASS; historical pagination after newer `host.latestRunId` PASS; `{latest:true}` mismatch → `QUERY.VIEW_UNKNOWN` PASS; continuation requires `view.runId` PASS; `host.cache` ignored PASS; six-field human/json/agent exact projections PASS; wrapper without `close_run` → `QUERY.VIEW_UNKNOWN` PASS; `traverse_projected_graph` labeled `algorithmic` PASS; query does not seal a Run PASS.

Remaining adapter work (not a completed public wrapper):

- `execute_graph_query` still takes caller `projected_edges` instead of projecting from retained `objects`/`blobs` (contract §8).
- Compact `QueryResult` (`completenessMet`, page `items`, `nextCursor` join) is not implemented in the helper. Independently derived from response context; consumer does not emit it.
- Empty neighbors with a **selected** matching view still emit `native-evidence-unavailable` (contract §6 over-disclosure).
- Package endpoint without `packageManifestPath` was admitted (contract §2 requires `QUERY.ENDPOINT_AMBIGUOUS`).

Frozen-store probe (no fabricated edges): none of the five stores contain `calls@resolved-callee`. TS has `imports@resolved-target` without observed `TargetAttributionV1`. Do not treat a stale frozen hash as an accepted flag; a later corrected Run may supersede `2e74a6b2…`.

## Previously withdrawn grades, reassessed

| ID | Prior selfaudit | This review |
|---|---|---|
| R-CONFIG-CUSTOM-MULTI-BASE | refused (no repeated later-wins) | **executed** — sequence `[base, strict, base]`; digest `e434c76f…` independently reminted |
| R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE | refused (identity not remintable) | **executed as standalone identity recipe** — independent FACT-IDENTITY L0 `sha256:82e8a6b5…`; ownership excluded from BLV; edition change changes identity. Not a close_run-admitted rust Run property |
| R-MIN-RESOLUTION-THREE-LEVELS | refused (no facts/Coverage) | **executed** — `eval_atom` true/indeterminate, true/false, true/false at syntactic/resolved/type. Placeholder fact2 ids noted, not used as a refusal of the predicates |
| R-EMPTY-PARTIAL-UNAVAILABLE-MISSING | refused (narrative strings) | **executed** — four distinct records; inventories schema-valid |
| R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR | incomplete / refused parity | **INCOMPLETE** — do not restore executed |
| R-CHAIN-ZERO-CONFIG-TO-RECEIPT | incomplete | **INCOMPLETE** |

## All 48 dispositions

| ID | Kind | Disposition | Artifact |
|---|---|---|---|
| `R-ENVELOPE-CONFIG-INPUT` | schemaEnvelope | **executed** | `envelopes/config-input.json` |
| `R-ENVELOPE-EXTERNAL-INPUT` | schemaEnvelope | **executed** | `envelopes/retained-external-input.json` |
| `R-ENVELOPE-HOST-INVALID` | schemaEnvelope | **executed** | `envelopes/host-invalid-internal.json` |
| `R-ENVELOPE-PRODUCER-BOUNDARY` | schemaEnvelope | **executed** | `envelopes/producer-boundary.json` |
| `R-PUBLIC-FROM-INTERNAL-REFUSAL` | schemaEnvelope | **executed** | `envelopes/public-from-internal.json` |
| `R-PINNED-PURGE` | schemaEnvelope | **executed** | `envelopes/pinned-purge.json` |
| `R-PURGE-REPLAY-OUTPUT-FAILURE` | schemaEnvelope | **executed** | `envelopes/purge-replay-output-failure.json` |
| `R-FAILURE-ENVELOPES-D9` | schemaEnvelope | **executed** | `envelopes/failure-d9-complete.json` |
| `R-PUBLIC-TERMINATION-EXAMPLES` | schemaEnvelope | **executed** | `envelopes/public-termination.json` |
| `R-D9-EXTENSION-PRECEDENCE` | schemaEnvelope | **executed** | `vectors/d9-extension-precedence.json` |
| `R-SINGLE-STEP` | schemaEnvelope | **executed** | `envelopes/single-step.json` |
| `R-MULTI-STEP-DIFFERENT-SELECTIONS` | schemaEnvelope | **executed** | `envelopes/multi-step.json` |
| `R-INVOCATION-DISCLOSURE` | schemaEnvelope | **executed** | `envelopes/invocation-disclosure.json` |
| `R-DURABLE-RECEIPT-AVAILABILITY` | schemaEnvelope | **executed** | `envelopes/receipt-availability.json` |
| `R-CONFIG-SYNTHESIZED` | standaloneConfigVector | **executed** | `vectors/config-synthesized.json` |
| `R-CONFIG-CUSTOM-MULTI-BASE` | standaloneConfigVector | **executed** | `vectors/config-custom-multi-base.json` |
| `R-CONFIG-JS-SHARED-BASE` | standaloneConfigVector | **executed** | `vectors/config-js-shared-base.json` |
| `R-MUTATION-REPLAY-SCOPE` | standaloneCanonicalVector | **executed** | `vectors/mutation-replay-scope.json` |
| `R-REPAIR-DESCRIPTOR` | standaloneCanonicalVector | **executed** | `vectors/repair-descriptor.json` |
| `R-REPAIR-APPLY-KEY` | standaloneCanonicalVector | **executed** | `vectors/repair-apply-key.json` |
| `R-REPAIR-AUTHORITY-PER-TARGET` | standaloneCanonicalVector | **executed** | `vectors/repair-authority-per-target.json` |
| `R-MIN-RESOLUTION-THREE-LEVELS` | standaloneCanonicalVector | **executed** | `vectors/min-resolution.json` |
| `R-MIN-RESOLUTION-REPAIR-EVIDENCE` | standaloneCanonicalVector | **executed** | `vectors/min-resolution-repair-evidence.json` |
| `R-RUN-UNSUPPORTED-GRAMMAR` | standaloneCanonicalVector | **executed** | `vectors/unsupported-grammar.json` |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | standaloneCanonicalVector | **executed** | `vectors/hidden-mismatch.json` |
| `R-CLONES-NEGATIVE-VECTORS` | standaloneCanonicalVector | **executed** | `vectors/clones-negatives.json` |
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | completeRunProperty | **executed** | `vectors/rust-body-identity-pair.json` |
| `R-JS-CLONE-BODY-THROUGH-TS` | standaloneCanonicalVector | **executed** | `vectors/js-body-through-ts.json` |
| `R-REPLAY-THREE-VALUED` | evaluatorReplay | **executed** | `vectors/replay-three-valued.json` |
| `R-CMP-EMPTY-RESULT` | standaloneCanonicalVector | **executed** | `vectors/comparison-empty-result.json` |
| `R-CMP-MISSING` | standaloneCanonicalVector | **executed** | `vectors/comparison-missing.json` |
| `R-CMP-EVIDENCE-CHANGED` | standaloneCanonicalVector | **executed** | `vectors/comparison-evidence-changed.json` |
| `R-SCOPE-POLICY-ONLY-COMPARISON` | standaloneCanonicalVector | **executed** | `vectors/comparison-scope-policy-only.json` |
| `R-PIVOT-ONLY-FINGERPRINTS` | standaloneCanonicalVector | **executed** | `vectors/pivot-only-fingerprints.json` |
| `R-E0-VS-E1-E3` | standaloneCanonicalVector | **executed** | `vectors/baseline-e0-e3.json` |
| `R-BASELINE-AUDIT` | standaloneCanonicalVector | **executed** | `vectors/baseline-audit.json` |
| `R-TEST-PREP-REPAIR-AUTH` | standaloneCanonicalVector | **executed** | `vectors/test-prep-repair-authorization.json` |
| `R-MULTI-UNIT-MISSING-CAPS` | standaloneConfigVector | **executed** | `vectors/multi-unit-missing-caps.json` |
| `R-CANDIDATE-ONLY-CLONES` | standaloneConfigVector | **executed** | `vectors/candidate-only-clones.json` |
| `R-HOST-CAPTURED-VS-CANDIDATE` | standaloneCanonicalVector | **executed** | `vectors/host-captured-vs-candidate.json` |
| `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` | standingRule | **INCOMPLETE** | `vectors/chain-zero-config-to-receipt.json` |
| `R-SUBSYSTEM-OWNERS` | standingRule | **executed** | `vectors/subsystem-owners.json` |
| `R-PROMISE-VS-AVAILABILITY` | standingRule | **executed** | `vectors/promise-vs-availability.json` |
| `R-SEMANTIC-VS-OPERATIONAL-AUTHORITY` | standingRule | **executed** | `vectors/semantic-vs-operational.json` |
| `R-MUTATION-VS-ANALYSIS-STEPS` | standingRule | **executed** | `vectors/mutation-vs-analysis-steps.json` |
| `R-DETECTOR-COMPAT-FILE` | standaloneCanonicalVector | **executed** | `vectors/detector-compat-file.json` |
| `R-EMPTY-PARTIAL-UNAVAILABLE-MISSING` | standingRule | **executed** | `vectors/empty-partial-unavailable-missing.json` |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | standaloneCanonicalVector | **INCOMPLETE** | `query/graph-query-bundle.json` |

Measurement, expected derivation, and owner selectors for every ID are in `workflow-review.json#/all48Disposition`.

Standalone vs whole-Run: `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` is original kind `completeRunProperty` exhibited here as a reminted identity pair, not as a property of a `close_run`-admitted rust graph. `R-REPLAY-THREE-VALUED` is original kind `evaluatorReplay` exhibited as a standalone Kleene vector, not whole-Run semantic replay. Frozen completeRun / evaluatorReplay IDs remain out of this workflow scope.

## 134 original ID mapping

| reviewedScope | Count |
|---|---:|
| in-scope-executed | 46 |
| out-of-scope-frozen-run | 24 |
| standing-of-consumer-continuation-not-re-executed-here | 24 |
| notReached-historical-vector | 22 |
| out-of-scope-frozen-run-replay | 12 |
| futureQualification | 3 |
| in-scope-INCOMPLETE | 2 |
| measured-standalone-outside-established-48 | 1 |
| **total** | **134** |

`R-IMPORTED-OBSERVATION-BOUNDARY` is a phase-6 standalone vector present in the snapshot and measured here, but it is not a member of the established 48. It is mapped `measured-standalone-outside-established-48` so this review does not call it `notReached` after reading it.

## Remaining final binding

See `remainingDependencies` in the JSON. Precise remaining work from actual code and existing laws:

1. Implement/retain `close_run` over exported object table + all blob/frame bytes of a complete positive (identity-and-evidence §3). This is frozen-Run work, not invented query law.
2. Bind `execute_graph_query(request, run, objects, blobs, host)` so step 4 projects from admitted views, retained TargetAttributionV1, and retained payloads — not caller-authored edges.
3. If the admitted graph still lacks a projectable binary rung, refuse `QUERY.RELATION_UNSUPPORTED` / disclose `native-evidence-unavailable` rather than fabricating `calls` facts.
4. Emit compact `QueryResult` summary joins and keep six-field parity.
5. Join executed traces/envelopes to that admitted Run for `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`.

A successor corrected Run may supersede current frozen hashes. Do not keep a stale hash as an accepted flag.

## Unexecuted limits

- Frozen Run close_run / identity-and-evidence §3 closure admission / semantic proof replay are out of this workflow-scope review.
- Algorithmic query cases used labeled synthetic close_run and independently chosen projected edges. That is not retained Run admission.
- Real OS/compiler/product/cryptographic qualification remains futureQualification. Synthetic host.requestId / availability / latestRunId / runsForSnapshot / testBounds observations are explicit.
- R-OBJECT-TABLE-FRAMES and R-FROM-SCRATCH-COMMAND for complete Runs are notReached in this workflow-scope review.
- Min-resolution fact2/coverage2 IDs are placeholder hex, not H-derived. Atom evaluation over those local ids still held.
- Public wrapper is not completed except remaining final binding work listed under remainingDependencies.
- No whole-consumer ACCEPT. No root admission.

## Author claims

The author self-verdict is `WORKFLOWS_INCOMPLETE` with the same two incomplete IDs. This review independently remeasured rather than adopting that grade. Agreement on INCOMPLETE for those two IDs is a measurement result, not a waiver.

