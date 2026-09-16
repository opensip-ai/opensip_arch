# Source37 StepTermination admission boundary: bounded assessment

**Standing.** Actual Claude ce3, bounded source-boundary assessor. This is not independent successor acceptance, blind reconstruction or application review. Nothing was integrated, frozen, rebound or re-pinned, and no group or global suite was run. All edits exist only in `disposable/edited`.

**Source.** `candidate-subject.v37`, manifest SHA `245ef613…91676680`. The exact-path pins for all 16 key files agree (p00b).

## Verdict

**This is a real contract/schema gap at the public termination carrier. No other owning gate covers it, and nothing in the owner text makes it an intentional shape-only allowance.**

Root's observation reproduces exactly, and the gap is wider than root's four cases:
- The same retained law is broken by 13 combinations.
- All 13 are admitted at all seven schema sites that reference StepTermination:
  - both common schemas;
  - both command-envelope majors;
  - the evaluator3 graph-query response termination;
  - both invocation-record step-result terminations.
- Every identified producer emits only lawful terminations. So nothing unlawful is emitted today; the published admission contract is simply weaker than the law it says it keeps.

## Owner law

- **D9 v1.14, retained class/code legality:**
  - `causeModel.codeDerivation` (line 2623): "success / policy-failed / interrupted: no code field may be present"; indeterminate reasonCodes = map(deficiency) plus secondaries; request-rejected and operational-failed errorCode = map(cause).
  - `X1` deficiency ↔ indeterminate; `X3` faultCause≠none ↔ operational-failed; `X4` at most one cause family.
  - `causeModel.exclusivity` and `theOneException`: "a deficiency never accompanies a fault or a rejection".
  - `codeMaps.rule`: "total and injective … a golden whose code disagrees with its axes fails D6".
- **D9 `hostTerminationUnion`:** `unknownFieldPolicy: reject` with per-class variants. That union refused reasonCodes on every class except indeterminate.
- **workflows-and-surfaces §0, lines 65–66:**
  - StepTermination **succeeds** the union's field closure for major3, and "no undeclared D9 field is admitted".
  - "**Class/code/exit legality remains retained.**"
  - No other enforcement point is named.
- **§9, lines 1137–1147:** the branch contract is "(schema-enforced)". The clauses it lists are presence-only, so the text is literally true. Nothing there, or in the schema description, sets cause/code exclusivity aside for another gate.
- **§8, lines 1062–1065:** a response termination must *equal* the enclosing termination. That is equality, not legality.
- **§12, lines 1386–1388:** the host "projects the unit's existing D9 class/code into StepTermination, checks the declared exit and host faultCause".
- **native §10, lines 3068–3115:** every route "derives a StepTermination that validates against the real schema"; host-invariant → `SYSTEM.OUTCOME.ILLEGAL_STATE`. This relies on the schema to carry the law.

## Boundaries

| Boundary | APIs | What holds |
|---|---|---|
| Producer | `terminate` (workflows_model.v1.py:143), evaluator-fault `ROUTES`/`route`, native `public_termination_for` (native_evidence_model.v2.py:1038), projection output-bound termination | Lawful by construction. p01: ROUTES 24/24, public_termination_for 22/22, terminate 23/23 lawful. Each validates only against the schema. |
| Trusted host finalizer | `public_termination` (integration-host-model.py:50–75) | Derives the unique faultCause from errorCode, places reasonCodes only on indeterminate, and checks exit. So exclusivity and pairing hold by construction. It does **not** check the input code for its class: a code on success is dropped (28/28 enumerated) and request-rejected accepts fault-family codes (11). |
| Public typed envelope | command-envelope majors 2 and 3, graph-query response; `exit_code` (class-only, :222), `render`/`parity_holds` (projection), `validate_envelope` (evaluator_fault_model.v3.py:68, parity with the routed termination), `validate_pinned_purge_refusal` (:129, purge joins) | No gate applies class/code legality to a received termination. The schema is the only admission, and it admits all 13. |
| Imported / retained | invocation-record (workflows and evaluator3 invocation:3), `PAYLOAD_REGISTRY`, retained Run identity/replay closure | The invocation-record schemas admit all 13. No import kind carries a termination, and the retained Run closure holds none, so again the schema is the only admission. |

## Dispositions

- **R1: REQUIRED. Cause/code exclusivity on the carrier.**
  - faultCause may appear only on operational-failed.
  - reasonCodes may appear only on indeterminate.
  - Owner law: codeDerivation, X1, X3, X4, and the succeeded per-variant closure.
  - Discriminating cases, all admitted by baseline and refused by the edited copy:
    - root's four: success+faultCause, operational+reasonCodes, indeterminate+faultCause, ephemeral policy-failed+reasonCodes;
    - six more: success+faultCause `none`, policy-failed+faultCause, request-rejected+faultCause, request-rejected+reasonCodes, interrupted+faultCause, interrupted+reasonCodes.
- **R2: REQUIRED. operational-failed faultCause↔errorCode pairing.**
  - The successor carrier alone publishes both axes. Under codeDerivation and the injective codeMaps, a mismatched pair is a record that disagrees with itself.
  - All three probed mismatches are admitted today:
    - `HOST.IO_FAILURE`+`ledger-busy`;
    - `CONFIG.INVALID`+`host-io`;
    - `SYSTEM.OUTCOME.ILLEGAL_STATE`+`host-io`, which is the "borrowing host-io" case native §10 refuses in prose.
  - The D9 union could not enforce this because it had no faultCause field. The successor owns the surface it added.
- **A1: ADVISORY. request-rejected errorCode limited to the `rejectionCauseToErrorCode` image.**
  - This is retained law, but rejectionCause is not carried publicly, and the union never partitioned errorCode by class. It was always a host-finalizer derivation obligation (invariant-one-mapper).
  - Deliberately left out of the diff: request-rejected+`HOST.IO_FAILURE` is still admitted after the edit.
- **A2: ADVISORY.** `public_termination` should refuse a unit class/code that D9 forbids instead of dropping it (success) or passing it (request-rejected with a fault code). §12 claims only exit and faultCause checks, so this is not a contradiction.
- **A3: ADVISORY.** Add a control that the workflows and evaluator3 StepTermination definitions stay equal. They are equal before and after the edit, but no checker compares them.

## Proposed edit

The exact diff is `proposed-edits.diff` (SHA-256 `a2e3a27a3159a944d7f68ccc86e9a6cdc621aee59952fbdfd6cb05997b146a25`, 560 lines). p02 generated it from structural JSON edits, and only after a byte-exact round-trip check, so the diff holds nothing but the proposal.

1. **Both** `workflows/schemas/common.schema.json` and `workflows/schemas/evaluator3/common.schema.json`, `#/$defs/StepTermination`, identical edits:
   - success: `not.anyOf` += `required[faultCause]`.
   - policy-failed: `not.anyOf` += `required[reasonCodes]`, `required[faultCause]`.
   - request-rejected: `not` becomes `anyOf[signal, reasonCodes, faultCause]` (was `required[signal]`).
   - operational-failed: add `anyOf` of the 11 `{faultCause const, errorCode const}` pairs, in `FAULT_TO_ERROR` order including `host-invariant`→`SYSTEM.OUTCOME.ILLEGAL_STATE`; add `not required[reasonCodes]`. The existing `faultCause not none` stays.
   - indeterminate: `not.anyOf` += `required[faultCause]`.
   - interrupted: `not` becomes `anyOf[errorCode, reasonCodes, faultCause]` (was `required[errorCode]`).
   - The description gains one sentence naming X1/X3/X4/codeDerivation and the pairing.
2. **Controls.**
   - `workflow-cases.v1.json` `terminationVectors.reject` gains 12 vectors (R1 and R2 cases).
   - `check_workflows.v1.py` gains `termination.fault-pairs-equal-host-fault-map`, which asserts the schema pairs equal `M.FAULT_TO_ERROR` in order.
3. **Owner prose.** workflows-and-surfaces §9 gains one sentence saying the schema enforces retained cause/code exclusivity and the fault-map pairing.

native §10, `native-evidence.schemas.v2.json` and the historical D9 artifact are unchanged. Their claims stay true.

## Discrimination (p03 over the edited copy vs p01 baseline)

All gates pass:
- Every required-illegal case refuses at all seven sites.
- All lawful controls still admit, including all 11 fault pairs, host-invariant and a two-reason indeterminate.
- The existing refusals still refuse: unknown field, success+errorCode, faultCause `none`.
- Producer emissions are identical across 243 rows and lawful.
- The replicated pair control is true.
- Termination vectors: 9 accept and 24 reject all hold; the 12 new rejects were admitted by baseline.
- Envelope vectors are unchanged (ADMIT→ADMIT, REFUSE→REFUSE).
- Both edited schemas pass the metaschema and the array-order law.
- None of the 52 termination-shaped fixture objects changes admission.

I also inspected the existing controls that touch faultCause or reasonCodes:
- check-identity 3482–3495 and 7174–7219;
- check_workflows 1345 (`wrong-class` uses a lawful pair, so its refusal still comes from the purge join);
- check-workflow-projection 853 and 1089;
- check-query-projection 385.

All of them expect lawful pairs.

## Digest and retained-export consequence

- **Pins.** The raw digests of both common schemas change: `965474dc…`→`f73094dd…` and `4a6e5775…`→`36124787…`. Owners would need to regenerate:
  - `foundation/evaluator3-source-pins.v1.json`, `foundation/source-pins.v1.json`, `native/source-pins.v2.json`, `security/source-pins.v1.json`, `workflows/source-pins.v1.json`;
  - the generated `workflows/workflows-report.v1.json` `sourceSha256`;
  - a rebound package manifest.
  - Pins for the other three changed files would change too; I did not locate them.
- **Registered payload schema digest.** No change. No registered payload document (imported-evidence, test-execution, native-evidence.schemas.v2) references StepTermination. `payloadSchemaDigest` is the raw SHA-256 of that registered document, and those bytes are untouched.
- **Positive retained exports.** No consequence:
  - no retained Run identity or replay closure contains a termination;
  - no import payload carries one;
  - no examined positive fixture and no lawful producer emission changes.

## Preserved failures

- **p00 (exit 1).** The copies were created and byte-equal. The manifest check matched pins by path suffix and picked review-subtree copies; p00b replaced it with exact-path matching.
- **p01 run 1 (exit 1).** TypeError in the fixture scan of `probes/boundaries.py` (a non-string `class` value). I fixed the type guard and run r2 passed.
- Both receipts are retained in `receipts/`.

## Limits

- No group or global suite was run. The new check_workflows control and vectors were replicated narrowly, not executed inside the checker.
- Nothing was regenerated or rebound.
- The legality predicate is my transcription of D9. It is always reported beside actual outcomes.
- `boundaries.py` is not digest-recorded in the receipts.
- The fixture scan covers JSON only. Envelopes were probed with `kind=failure` only. The graph-query and invocation-record sites were probed at the termination pointer.
- `public_termination` was enumerated with a single detail code.
- Not assessed, because it is outside class/code legality: signal on operational-failed, and runId/coverageId/executionId placement.
- The D9 v1.14 goldens are historical union-shaped values without faultCause; they are unaffected.
- No acceptance or security claim is made, and no background child was started.
