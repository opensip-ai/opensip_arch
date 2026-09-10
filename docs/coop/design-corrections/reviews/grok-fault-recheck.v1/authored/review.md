# Evaluator-fault corrections — bounded recheck of six SHOULD findings

**Standing.** Read-only peer review of root corrections to the six SHOULD items in LIVE `grok-evaluator-fault-review.v1` (`/tmp/opensip-design-corrections/grok-evaluator-fault-review.v1/review.md`). Source `evaluator-successor.v1`. Not whole-source independent or blind acceptance. Not a Run. Not producer qualification. Atom files were not edited. Workflow files were not edited. The mandatory LIVE D9 successor artifact remains a carried obligation; it is not rediscovered here as a design-level blocker.

**Verdict.** `SIX_SHOULD_CLOSED_WITH_RESIDUALS`. Each of the six original SHOULD claims is substantively closed by schema, model, checker, and (where applicable) owner-carrier equality. `check-evaluator-faults.v3.py` reports `passed: true`, `count: 38` (24 route ADMIT + 2 owner-carrier ADMIT + 12 REFUSE). No invented D9 class, error code, faultCause, or exit pairing on the 24 rows. Remaining items below are residuals and owner-disjoint advisories, not reopenings of the six claims.

## Sources (sha256)

| file | bytes | sha256 |
|---|---|---|
| `foundation/evaluator-fault-observation.schema.v3.json` | 16920 | `b9a74548277c882a36bb30b412b994495dcd8f0141d67981cb57927c0660da3d` |
| `foundation/evaluator_fault_model.v3.py` | 4444 | `d6ff2c1b94a411a890cd179e849b67afb65307e89c834dcd3ca5b021a40143c6` |
| `foundation/check-evaluator-faults.v3.py` | 4575 | `8b22ba3c750b0865ee7854ac1aeeba26fde04480440bc574258eb866f3141a9d` |
| `foundation/evaluator-fault-contract.v3.md` | 7703 | `f0574987d0a2854115989c5320188facca6471ec04e6f8738f55a78a312c62ae` |
| `foundation/canonical.py` | 5892 | `9e7563c7831eb17b4ac3887b8539ed702ee7f37f0f17fc3e2eb14d422629f279` |
| `foundation/identity-model.v3.py` | 137361 | `90eae742bfc52b5cb0c04f67f1c652b94097117779a4ffa839f7208bcdcff33e` |
| `native/native-evidence.schemas.v2.json` | 229766 | `f20b8353a7be50d7a0c24f413df74e35d23a4e9fc2a4ecc661235655c43c51be` |
| `native/native_evidence_model.v2.py` | 285290 | `027dce368d7ec26dac2a8f3077d54c91028b6f72c0c3285d5de754ac3ae6dc22` |
| `public-detail-registry.v1.json` | 57082 | `eedbc44e5c7692c69e897136e9e852546c6480f84d67690bb6c523d8a59f858f` |
| `workflows/schemas/evaluator3/common.schema.json` | 56291 | `030ba6d89112de6806307be3f67c3dd01465f331ad3de9a1efa283013fe5030d` |
| `workflows/schemas/evaluator3/command-envelope.schema.json` | 7374 | `25b39278bbf70539e8e7d42da525c20e5fa0f45cf2b601271ac5f93d997a4d4e` |
| `workflows/schemas/common.schema.json` | 47400 | `be08b209904921dc126b0485000a2b8c5b225f41aa3b04d27789048330c07dd3` |

Checker: `/tmp/opensip-architecture-review-env/bin/python -I -B foundation/check-evaluator-faults.v3.py` → `passed: true`, 38 rows.

## Disposition of the six SHOULD

### S1 schema pair closure — CLOSED

`allOf` now includes an `anyOf` of 24 `{condition, origin}` const pairs. That set equals `x-opensip-routes` keys (24=24, measured).

Counterexamples from the original review now fail `C.validate` before `route()`:

- `promised-bytes-lost:provider-return` → `ValidationError` (`is not valid under any of the given schemas`)
- `input-identity-invalid:evidence-store` → same

Checker cases `unknown-origin-pair` and `invalid-bytes-are-not-loss` assert that schema refusal.

### S2 owner-carrier remedy/subject — CLOSED

`owner_observation` requires a typed owner exception, maps `evidence.missing` / `evidence.regeneration-mismatch`, then `C.equal_typed` of the **entire** routed termination against `exception.termination`.

Measured against identity-model.v3:

| carrier | condition/origin | `equal_typed` | remedy | subject |
|---|---|---|---|---|
| `EvidenceUnavailable('retained:fixture')` | `promised-bytes-lost:evidence-store` | true | `Restore the exact retained closure bytes or report their unavailability.` | `retained:fixture` |
| `RegenerationMismatch('retained:fixture')` | `complete-replay-mismatch:retained-regeneration` | true | `Retain the sealed Run and investigate the differing regeneration result.` | `retained:fixture` |

Schema remedies for those two routes are those identity strings verbatim. Checker ADMITs both owner carriers and REFUSEs an invented remedy (`owner-carrier-remedy-mismatch` / `EVALUATOR_FAULT_OWNER_CARRIER`).

### S3 explicit native origin map — CLOSED as specified

`x-opensip-native-origin-map` is present:

- `external-configuration` → `external-configuration`
- `external-specification` → `externally-supplied-spec`
- `host-internal` → `host-generated-internal-layer`
- `release-declaration` → `authenticated-release-declaration`
- `provider-return` → `producer-boundary`

All map values are members of native `possibleOrigins`. Evaluator-only origins with no native producer equivalent remain unmapped: `evidence-store`, `host-pre-plan`, `host-serialization`, `retained-regeneration`.

Passing evaluator spellings into `public_termination_for` still refuses `native.public-route-origin-not-possible` (measured for `external-specification`, `host-internal`, `provider-return`). Contract states that passing evaluator spellings to the native helper is not supported. Native `externally-supplied-spec` still uses `domainDetail: null`; this boundary still supplies `EVALUATION.INPUT_REFUSED`. That difference remains stated, not silently equated.

### S4 required replay reference — CLOSED

`complete-replay-mismatch` is in the schema `if` that requires `reference` type string `minLength: 1`. Both origins refuse `reference: null` (`None is not of type 'string'`). Empty string also refuses (`'' should be non-empty`). Routed retained-regeneration detail carries `subject: retained:fixture`. Checker covers both origins.

### S5 omission detail — CLOSED

`required-output-pointer-omitted:provider-return` now projects:

- D9: `PROVIDER.PROTOCOL_VIOLATION` / `provider-protocol` (unchanged)
- detail: `EVALUATION.REQUIRED_OUTPUT_OMITTED`
- subject: the required reference

`EVALUATION.REQUIRED_OUTPUT_OMITTED` is in `public-detail-registry.v1.json` (owner identity), `workflows/schemas/common.schema.json#/$defs/DomainDetailCode`, and `workflows/schemas/evaluator3/common.schema.json#/$defs/DomainDetailCode`. It is a DomainDetail, not a new D9 error/exit code.

### S6 measured output bound — CLOSED as specified

`output-bound-exceeded` now requires a `limit` object `{field, observed, maximum}`. Null limit is schema-refused. Routed detail subject is `proof.predicates:100001>100000` on the checker observation. `observed == maximum` is model-refused (`EVALUATOR_FAULT_NOT_OVER_LIMIT`) for both selection-limit and output-bound. Contract states that sibling integer inequality is a reference admission rule because standard JSON Schema cannot express it without `$data`.

## MUST

None against D9 class, error code, faultCause, or exit pairing of the 24 rows.

## Remaining findings

These do **not** reopen the six original SHOULD titles. They are exact leftovers after the stated corrections.

1. **R1 — `observed <= maximum` remains schema-valid.** `output-bound-exceeded` with `limit.observed == limit.maximum` (`100000==100000`) JSON-Schema ADMITs; only `route()` raises `EVALUATOR_FAULT_NOT_OVER_LIMIT`. Same for selection-limit (`64==64`), already in the 38 controls. Root documented the JSON Schema limit. Residual of S6’s “consider closing in schema,” not a missing measurement.

2. **R2 — native origin map is annotation, not an executed adapter.** `route()` does not read `x-opensip-native-origin-map` and does not call `public_termination_for`. Evaluator origin strings still cannot be fed to the native helper. This is the stated “before wiring” posture, not a spelling-split regression. Residual: the map can drift from native `possibleOrigins` without a checker.

3. **R3 — pair lists are duplicated.** `anyOf` and `x-opensip-routes` currently match (24=24), but the checker does not assert that equality. An extra `anyOf` branch without a route row would schema-admit and then `EVALUATOR_FAULT_ORIGIN`. Weaker than original S1 (illegal pairs now fail schema).

## Advisory (not this unit’s remaining SHOULD)

- Workflow owner is separately prohibiting a valid Run on a failure envelope and updating code-list prose. `kind=failure` still only `required: [errors]`; it does not `not: required: [run]`. A placeholder `run: {schemaVersion:3}` still fails AnalysisResult `oneOf`, not an explicit failure/run exclusion. Isolated-additions **description** in evaluator3 common still omits `EVALUATION.INPUT_REFUSED`, `EVALUATION.SELECTION_LIMIT`, and `EVALUATION.REQUIRED_OUTPUT_OMITTED` even though all three are in that enum. Do not treat those as fault-unit reopenings.
- `evaluator_composition_model.v3.py` still raises `AdmissionError('EVALUATION.OUTPUT_BOUND_EXCEEDED')` as a string, not via this observation. Out of the four-file unit.
- `limit.field` remains an open 1–256 string.
- Checker diagnostics remain one synthetic blob `{"owner":"synthetic-boundary-control","decisions":["original"]}` for every route. Hash custody is shown; content is not interpreted. Owner-carrier tests now pass live `EvidenceUnavailable` / `RegenerationMismatch` objects into `owner_observation`.

## Coverage limits

Read the four current fault files, identity carriers, native public-route origins, public-detail registry, and evaluator3/common DomainDetail enums. Executed the required Python checker and targeted probes of the six original counterexamples. Did not execute a host, reconstruct a Run, re-qualify a producer, or treat 38 passing controls as whole-source acceptance. Did not edit atom, workflow, or native sources.
