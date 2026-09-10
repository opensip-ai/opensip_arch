# Evaluator-fault boundary — bounded coauthor peer review

**Standing.** Read-only review of isolated `evaluator-successor.v1` evaluator-fault files against owner D9 / evaluator3 common + command-envelope, identity `EvidenceUnavailable` / `RegenerationMismatch`, and native `x-opensip-public-route-registry`. Not whole-source independent acceptance. Not blind-consumer evidence. Not a Run. Execution-input v3 source was not edited. The mandatory LIVE D9 successor artifact is a carried obligation already settled elsewhere; this review does not publish or alter it.

**Verdict.** `ISOLATED_REFERENCE_SOUND_WITH_GAPS`. The 24 condition/origin rows mint owner-valid `StepTermination` and `command-envelope:3` failure envelopes. `check-evaluator-faults.v3.py` reports `passed: true`, `count: 33`. Public DomainDetail codes used by the table are members of both `workflows/schemas/common.schema.json` and `workflows/schemas/evaluator3/common.schema.json`. Pointer-omission, promised-byte loss, and invalid supplied bytes are different routes. Retained regeneration stays on identity’s `HOST.IO_FAILURE` / `evidence.regeneration-mismatch` carrier; a live evaluator contradiction is `host-invariant`. Output-bound uses `OUTPUT.SERIALIZATION_FAILED` / `output-serialization`, not `HOST.IO_FAILURE`.

Gaps below are concrete. None of them is a D9 class/exit invention. Root acceptance is not assumed.

## Sources read (sha256)

| file | bytes | sha256 |
|---|---|---|
| `foundation/evaluator-fault-observation.schema.v3.json` | 10944 | `e883b07c0ef49228ff77564cfcb5e559dedcde4e9a8c5bf3e5e8cce8ed060205` |
| `foundation/evaluator_fault_model.v3.py` | 3280 | `deef35d0ccdc803d1870202a3bb186736e9d67b88dfc21b6ea00233ad821319d` |
| `foundation/check-evaluator-faults.v3.py` | 3572 | `2eef4b9636cc70477624832ff7d0a29477f0595ef12080b01a8a7eec851331f9` |
| `foundation/evaluator-fault-contract.v3.md` | 6020 | `9ba213ff4258c870a6a27581ac206b4d3de7c7b1b7465f14b4c1f0c6e556fbeb` |
| `foundation/canonical.py` | 5892 | `9e7563c7831eb17b4ac3887b8539ed702ee7f37f0f17fc3e2eb14d422629f279` |
| `foundation/identity-model.v3.py` | 137361 | `90eae742bfc52b5cb0c04f67f1c652b94097117779a4ffa839f7208bcdcff33e` |
| `native/native-evidence.schemas.v2.json` | 229766 | `f20b8353a7be50d7a0c24f413df74e35d23a4e9fc2a4ecc661235655c43c51be` |
| `native/native_evidence_model.v2.py` | 285290 | `027dce368d7ec26dac2a8f3077d54c91028b6f72c0c3285d5de754ac3ae6dc22` |
| `public-detail-registry.v1.json` | 56928 | `03cf3b89ae266d6d6d0a654e4c3f8dc3ca07ee3575f87e775881af4f280414f5` |
| `workflows/schemas/evaluator3/common.schema.json` | 56245 | `fbc53e61b88497332507e3510110882a7782d6e9581166e142c53588aedd80a8` |
| `workflows/schemas/evaluator3/command-envelope.schema.json` | 7374 | `25b39278bbf70539e8e7d42da525c20e5fa0f45cf2b601271ac5f93d997a4d4e` |
| `workflows/schemas/common.schema.json` | 47354 | `5ffdb3e9f26eed561c894ea7a9dd9bc66035cff6c461e904d34ef5d664c662ad` |
| `workflows/workflow_projection_model.v3.py` | 80845 | `d1985f1b1e2cd4e0277cbc351b3767532f7b64b14f80595079fd9118bf30e6e2` |

Checker: `/tmp/opensip-architecture-review-env/bin/python -I -B foundation/check-evaluator-faults.v3.py` → `passed: true`, 33 rows (24 route ADMIT + 7 REFUSE + 2 owner-carrier ADMIT).

## What holds

- Closed table is 24 keys. Operational-failed rows carry a non-`none` `faultCause`; request-rejected rows do not. Exit codes are the inherited 0/1/2/3/4/130 map.
- Envelope parity refuses `exitCode=2` on an operational-failed termination, a swapped public `errors[0].code`, and a swapped `termination.errorCode`. `kind=failure` without `errors` is refused by command-envelope3 (`'errors' is a required property`).
- Diagnostic custody is raw SHA-256 of caller-supplied bytes. The synthetic control blob is `{"owner":"synthetic-boundary-control","decisions":["original"]}`; origin is never parsed out of that text.
- `promised-bytes-lost:provider-return` and `input-identity-invalid:evidence-store` refuse `EVALUATOR_FAULT_ORIGIN` in the model (loss is not invalid bytes; invalid bytes are not store loss).
- `complete-replay-mismatch:host-internal` is `SYSTEM.OUTCOME.ILLEGAL_STATE` / `host-invariant` / `HOST.INVARIANT_VIOLATED`, not `HOST.IO_FAILURE`.
- `output-bound-exceeded:host-serialization` is `OUTPUT.SERIALIZATION_FAILED` / `output-serialization` / `EVALUATION.OUTPUT_BOUND_EXCEEDED`.
- Used details `{CONFIG.INVALID, EVALUATION.INPUT_REFUSED, EVALUATION.OUTPUT_BOUND_EXCEEDED, EVALUATION.SELECTION_LIMIT, HOST.INVARIANT_VIOLATED, evidence.missing, evidence.regeneration-mismatch}` are in both common DomainDetailCode enums. `EVALUATION.INPUT_REFUSED` and `EVALUATION.SELECTION_LIMIT` are identity-owned in `public-detail-registry.v1.json`.

## MUST

None against D9 class, error code, faultCause, or exit pairing of the 24 rows. The LIVE D9 successor artifact is out of scope.

## SHOULD

1. **JSON Schema admits illegal pairs; only the Python table refuses.** `C.validate` of `{condition: promised-bytes-lost, origin: provider-return, reference: "retained:fixture", limit: null, diagnosticDigest: <matching>}` succeeds. `route()` then raises `EVALUATOR_FAULT_ORIGIN`. Same for `input-identity-invalid:evidence-store`. Pair closure lives in `x-opensip-routes` (annotation) plus `ROUTES` lookup, matching native `possibleOrigins` being helper-enforced rather than JSON-Schema-enforced. If “schema admission” is claimed for the 24 pairs, encode them as `anyOf` const pairs so `C.validate` itself refuses.

2. **Owner-carrier controls are a false full-DomainDetail pass.** Checker ADMITs `owner-carrier-promised-bytes-lost` and `owner-carrier-complete-replay-mismatch` by comparing `class`, `errorCode`, `faultCause`, and `domainDetail.code` only. Remedies differ:
   - loss: fault `"Restore the referenced promised evidence bytes or rerun the producing stage."` vs identity `EvidenceUnavailable` `"Restore the exact retained closure bytes or report their unavailability."`
   - replay: fault `"Preserve the disagreement and regenerate from admitted retained inputs; do not reuse the mismatching Run."` vs identity `RegenerationMismatch` `"Retain the sealed Run and investigate the differing regeneration result."`
   Compare the whole `domainDetail` or stop saying the existing carriers agree as records.

3. **Origin vocabulary is not native’s.** Overlap with native `possibleOrigins` is only `external-configuration`. Fault uses `external-specification`, `host-internal`, `release-declaration`, `provider-return`; native uses `externally-supplied-spec`, `host-generated-internal-layer`, `authenticated-release-declaration`, `producer-boundary`. `public_termination_for` will refuse these fault origin strings (`native.public-route-origin-not-possible`). Publish an explicit map before wiring. Native `externally-supplied-spec` also sets `domainDetail: null` and `envelopeDetail: native.capability-spec-invalid`; this unit always supplies `EVALUATION.INPUT_REFUSED`. That last difference is stated in the contract (“native may omit a domain detail; this boundary supplies its own”); the spelling split is not.

4. **`complete-replay-mismatch` does not require a reference.** Schema `allOf` requires nonempty `reference` only for `required-output-pointer-omitted` and `promised-bytes-lost`. `complete-replay-mismatch:retained-regeneration` with `reference: null` schema-validates and routes to `evidence.regeneration-mismatch` **without** `subject`. Identity `RegenerationMismatch(run_id)` always sets `subject` to the Run id. Require the reference (the Run id) on both replay origins.

5. **Public detail collapses omitted required output into `EVALUATION.INPUT_REFUSED`.** `required-output-pointer-omitted:provider-return` is correctly `PROVIDER.PROTOCOL_VIOLATION` / `provider-protocol`, but `domainDetail.code` is `EVALUATION.INPUT_REFUSED`. Distinguishing omission from malformed input then depends on retained observation bytes, which the public envelope does not copy. Keep the D9 code; give omission its own registered detail or put the condition name in `subject` by construction.

6. **Output-bound observation carries no numeric bound.** Selection-limit requires `{field, observed, maximum}` with `observed > maximum` in the model. `output-bound-exceeded` forces `limit: null`. The minted detail is only code + remedy; no field/count. Selection-limit `observed == maximum` is schema-valid (`{"field":"selectedPrograms","observed":64,"maximum":64}`) and only the model raises `EVALUATOR_FAULT_NOT_OVER_LIMIT`. Mirror that bound object onto output-bound, and consider closing `observed > maximum` in schema if JSON Schema can express it without `$data`.

## Advisory

- Checker diagnostics are one synthetic blob for every route. Hash custody is demonstrated; content is not. The suite does not pass a live `EvidenceUnavailable` / `RegenerationMismatch` exception into `route()` — it builds a matching observation by hand. Adapter from owner exception → observation remains root registration work.
- `limit.field` is an open 1–256 string, not the published bound names.
- `kind=failure` requires `errors` and does not `not: required: [run]`. A placeholder `run` was refused as an invalid AnalysisResult, not as “failure must not carry a Run.” Forbidding `run` on failure would match “no substitute Run.”
- `evaluator3/common.schema.json` isolated-additions prose still omits `EVALUATION.INPUT_REFUSED` / `EVALUATION.SELECTION_LIMIT` even though both enums contain them. `workflow-projection-contract.v3.md` appendix likewise omits those two identity-owned codes.
- `evaluator_composition_model.v3.py` still raises `AdmissionError('EVALUATION.OUTPUT_BOUND_EXCEEDED')` as a string, not via this observation. Out of this four-file unit.

## Coverage limits

Read the four fault files plus the owner registries named above. Did not execute a host, reconstruct a Run, or re-qualify D9. Did not treat checker `count: 33` as acceptance. Did not review execution-input v3 in this turn. Origin-law assessment is table comparison plus the two identity carriers, not a walk of every native `public_termination_for` key.
