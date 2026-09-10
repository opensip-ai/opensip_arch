# Evaluator3 cross-contract joins — three normative chapters

**Standing.** Actual Grok bounded cross-contract integration in isolated `evaluator-successor.v1`. Not final independent or blind acceptance. Not a Run. Not producer or platform qualification. Not a D9 artifact-readiness blocker. Fault-review six SHOULD items were already closed; this packet does not re-open them.

**Owned edits.** Only `native-evidence.md`, `security-and-lifecycle.md`, and `admission-and-qualification.md`. Root already retargeted current identity schema selectors to `identity-schemas.v3.json` and current Run/evidence/seal output refs to profile 3 across all five chapters; those selector edits are retained. This packet adds the profile-3 *joins* those selectors did not state.

**Not edited.** `identity-and-evidence.md`, `workflows-and-surfaces.md`, schemas, `identity-model*.py`, native/security/workflow reference models, execution-input/enumeration files, workflow v8 model/schemas/appendix. Required out-of-scope edits are listed with selector, counterexample, and required semantics.

**Verdict.** `CHAPTER_JOINS_APPLIED_WITH_REQUIRED_OUT_OF_SCOPE_EDITS`. The three chapters now dispatch current evaluator output as profile 3, keep unchanged native/input identities at major 2, distinguish complete replay from hash-only owner admission, distinguish trusted symbol census from native fact totality, distinguish candidate locators/projections from fact authority, and bind zero-config required cells as Plan-bound configuration. Counterpart source still admits empty evaluator parameters at owner admission, still patterns grant-journal `runId` as `run2:`, and still annotates the current identity chain as `evidence2/seal2/run2`. Those are not closed by chapter prose.

## What was already true (not inferred bad)

- Unchanged native/input identities remain `snapshot2`, `plan2`, `closure2`, `import2`, `fact2`, `coverage2`, `view2`, `exec-plan2`, `finding-key2`, `cache2`, `regen2`. Import wrappers stay `schemaVersion=2`.
- Historical `identity-schemas.v2.json`, `identity-model.py`, `check-identity.py`, `workflows_model.v1.py`, and `workflows/schemas/*.json` (non-evaluator3) remain byte-specific historical/harness evidence.
- Public API3 may invoke `identity-model.py` as an **explicit adapter** for those unchanged identities. Native already does: `IM.identifier("import"|"closure"|"coverage"|subject-scope)` and `IM.admit_parameter_selection`. That adapter is lawful. It is not current Run minting.
- `finding-key2` remains the fingerprint domain. Repair targets that name fingerprints are not automatically finding2 occurrences.
- Security permission tokens, lease modes, lock order, grant V2, and qualifier/history limitations are unchanged.
- Qualification G13 24-cell historical adapter remains historical. Completing a matrix lane is not evaluator required-cell accounting.
- `workflows_model.v3.py` already has no `run2`/`finding2`/`policy-derivation2`. Evaluator3 workflow schemas already refuse mixed `run[23]` prefixes.

## Chapter edits (this packet)

### native-evidence.md

- Explicit input/output dispatch: native/input stay 2; evaluator output is 3; mixed output-major graphs refuse; historical `run2`/`finding2`/`evidence2`/`seal2`/`proof2` bytes are never relabelled.
- Native `identity-model.py` import is named as an explicit profile-2 adapter. Current Run minting, cache and storage admission are `identity-model.v3.close_run` complete replay. Hash-only `identity-model.py.close_run` (prefix `run2`) is not current evaluator authority. `open_run_closure` is owner admission, not evaluator correctness.
- Generic `SubjectInventoryV1` census and the execution-inputs manifest are constituents of one intended design, not optional preview. Native `coverageTotality` for `file` remains a fact-per-path obligation and does not discharge that census.
- Candidate locators, syntax projections, and `CloneCandidateGroupV2.members` (opaque body IDs) are not fact authority and not `subject3`. Source custody is retained `CandidateProducerResultV1.sourceBodies` against Plan `candidateSourcePaths`.
- Zero-config default capability selection still requests every non-`NOT-SELECTED` cell. Evaluator3 Plan construction also commits `EnumerationPlanV1` and `EvaluatorEmissionPlanV1`. An analysis-spec with `parameters: []` is not a complete default for this evaluator. Required cells remain required when rules are disabled.
- Native `admit_coverage_result_v3` / retained owner closure is native admission, not evaluator replay.

### security-and-lifecycle.md

- Grant-journal `SEAL.runId` for a new analysis Run is `run3`. Historical schema-2 journals that already recorded `run2:` remain those bytes. The `run2:` pattern is not current Run authority. Lease/permission/revocation semantics are unchanged.
- Fingerprint-targeted repair consumes `finding-key2` of **finding3** occurrences on a **run3** evidence Run. A historical `finding2`/`run2` graph cannot become current repair, baseline, import, or installation authority by relabeling. Unmatched finding3 occurrences remain current findings; they cannot satisfy fingerprint-targeted repair. EXCLUSIVE / host-broker / `repositoryExecution=false` unchanged.
- Authoritative cache/regeneration inherit `identity-model.v3.close_run` then `admit_cache_entry`. Constructing `cache2`/`regen2` or matching a hash is not authority. Expired/revoked permission cannot be resurrected by a matching hash. Installation recovery already requires reconstructing the retained intent; a hash alone cannot authenticate a lawful scope.

### admission-and-qualification.md

- Configuration `schemaVersion=2` is the input carrier and does not select evaluator output major. Current output is profile 3.
- Zero-config Plan construction commits the two `requiredForEvaluatorMajors=[3]` parameters. They are Plan-bound configuration, not user-file fields of `product-configuration.schema.v2`. Native `default_capability_selection` requesting every non-`NOT-SELECTED` capability is not a substitute.
- Qualification required cells (`capability/mode/platform/profile/fixture`) are not evaluator Plan-bound required analysis cells. Corpus candidate locators remain candidate-only.
- `check-identity.py` is the historical `identity-model.py` harness (`run2`, hash-only `close_run`, trusted evaluator callback). Current minting is `identity-model.v3.close_run` (`check-replay.v3.py`, `check-semantic-replay.v3.py`). Synthetic graphs do not qualify a compiler.

## Measured counterpart facts

Python `/tmp/opensip-architecture-review-env/bin/python -I -B`.

| probe | result |
|---|---|
| `identity-model.v3.PREFIX['run'/'finding'/'policy-derivation'/'import']` | `run3` / `finding3` / `policy-derivation3` / `import2` |
| `identity-model.py.PREFIX['run'/'finding']` | `run2` / `finding2` |
| `identity-model.v3.admit_parameter_selection([])` | **ADMIT** `[]` |
| schema `requiredForEvaluatorMajors` | enumeration-plan `[3]`; emission-plan `[3]`; import-source-context and ScopeDocumentV1 unset |
| `native_evidence_model.v2` `IM` | loads `identity-model.py` |
| `default_capability_selection` emitted spec | `parameters: []` (line 4203) |
| `evaluator_input_model.v3.required_parameters` missing those two docs | `AdmissionError('EVALUATOR_REQUIRED_PARAMETER_MISSING:'+doc)` |
| `security-lifecycle.schemas.v1.json` `#/$defs/JournalRecord/properties/runId/pattern` | `^run2:[0-9a-f]{64}(?![\s\S])` — admits `run2:`+64hex, **refuses** `run3:`+64hex |
| `identity-model.v3.close_run` | complete semantic output replay |
| `identity-model.py.close_run` | hash-only owner admission returning `open_run_closure(...)[0]` |

Consequence: a zero-config analysis-spec with empty parameters passes native pre-Plan admission and `identity-model.v3.open_run_closure` / `admit_parameter_selection`. Complete replay then refuses at `EVALUATOR_REQUIRED_PARAMETER_MISSING`. Hash-only closure does not. That is the exact hidden-authority gap these chapters now name.

A new grant `SEAL` that names a current `run3` is schema-invalid under the live security journal pattern. The reference model writes `'run2:' + '0'*64`.

## Required out-of-scope edits

Do not treat these as “root wiring”. Each is a named semantic change.

### R1. Enforce `requiredForEvaluatorMajors=[3]` at Plan/spec admission

- **Selector.** `foundation/identity-model.v3.py` `admit_parameter_selection` (lines 92–126) and the retained-analysis-spec call at `open_run_closure` (~1694). Annotation already exists at `identity-schemas.v3.json` `#/x-opensip-payload-registry/classes/parameter/rows/foundation/enumeration-plan.schema.v1.json` and `.../evaluator-emission-plan.schema.v1.json` (`requiredForEvaluatorMajors: [3]`).
- **Counterexample.** `admit_parameter_selection([])` returns `[]`. Generic `selectionCardinality` “zero is legal” is still true for ScopeDocumentV1 / import-source-context. It is not true for evaluator major 3.
- **Required edit.** When admitting a profile-3 evaluator graph, refuse a spec that lacks exactly one enumeration-plan row and exactly one emission-plan row. Keep zero-legal for rows without `requiredForEvaluatorMajors` containing 3. Do not invent a default payload. Do not fold this into a new D9 class. Replay already refuses `EVALUATOR_REQUIRED_PARAMETER_MISSING`; owner admission must not mint a Run that only replay can see is incomplete.

### R2. Zero-config must not emit a complete-looking spec with empty parameters

- **Selector.** `native/native_evidence_model.v2.py` `default_capability_selection` line 4203: `spec = {"schemaVersion": 2, "requestedCapabilities": requested, "policyPackIds": [], "parameters": []}`.
- **Counterexample.** Helper return claims `defaultIsCompleteSelectedProduct: True` while `analysisSpec.parameters == []`. Evaluator3 cannot evaluate that spec.
- **Required edit.** Keep the helper as the capability-request producer (every non-`NOT-SELECTED` cell, `provenance=DEFAULTED`). Do **not** mint EnumerationPlanV1 here: that record needs `snapshotId` / `scopeDigest` / `membershipDigest` and is Plan-bound. Plan construction, after snapshot and membership exist, must insert the two required parameter rows. Stop implying the helper’s spec is a complete evaluator3 default. Docstring “mints no `plan2` and no `run2`” (line 4011) for a refused step must say `run3` for current output.

### R3. Current grant-journal SEAL names `run3`

- **Selector.** `security/security-lifecycle.schemas.v1.json` `#/$defs/JournalRecord/properties/runId/pattern` (line 300). `security_lifecycle_model_v1.py` line 1506 `append({'recordType': 'SEAL', 'runId': 'run2:' + '0' * 64})`.
- **Counterexample.** Pattern admits `run2:`+64hex and refuses `run3:`+64hex. A current analysis Run cannot be recorded. The synthetic SEAL always writes a `run2:` dummy.
- **Required edit.** Current SEAL records that name an analysis Run use `^run3:[0-9a-f]{64}(?![\s\S])`. Historical schema-2 journals that already contain `run2:` remain those bytes and are not re-parsed as current. No mixed `run[23]` alternation on new records. Grant admission, lease modes, and revocation are unchanged. `closure2` / `snapshot2` / `repairplan2` patterns stay.

### R4. Native current identity-chain annotations still say evidence2/seal2/run2

- **Selector.** `native/native-evidence.schemas.v2.json` `#/$defs/.../kind/x-opensip-vocabulary/movesIdentity` line 6764: `fact2 / scope2 / coverage2 / view2 / evidence2 / seal2 / run2`. Same chain in `native_evidence_model.v2.py` line 791. Matrix `enforcedAt` still says “foundation close_run” without naming v3 complete replay (`native-capability-matrix.v2.json` `capabilityIdLaw.enforcedAt`).
- **Counterexample.** Universe identity reaches current `evidence3` / `seal3` / `run3` (native-evidence.md already says that). The schema annotation still names the historical output chain as if it were current.
- **Required edit.** Current chain: `fact2 / scope2 / coverage2 / view2 / evidence3 / seal3 / run3`. Native owner admission remains `admit_coverage_result_v3` and `identity-model.v3.open_run_closure`. Complete replay remains `identity-model.v3.close_run`. Do not retarget `import2`/`fact2`/`coverage2`. Historical case notes that two tsconfigGraphHash values *would have* minted two RunIds stay valid as history.

### R5. Root workflows chapter leftover `policy-derivation2`

- **Selector.** `docs/v2/contracts/product-v1/workflows-and-surfaces.md` line 1060: “constructs policy-derivation2 from the same Plan/proof/verdict.”
- **Counterexample.** Identity §3 domain table and `identity-model.v3.PREFIX['policy-derivation']` are `policy-derivation3`. Constructing `policy-derivation2` from a `proof3`/`run3` graph is mixed output-major.
- **Required edit.** “constructs policy-derivation3 from the same Plan/proof/verdict.” Historical `policy-derivation2` bytes remain historical. Also name `workflows/schemas/evaluator3/invocation-record.schema.json` as the current invocation selector in §1 (the unprefixed `invocation-record.schema.json` description still says analysis seals `run2:`).

### R6. Execution-inputs `candidate-producer-result` domain (already specified, still unregistered)

- **Selector.** `foundation/execution-inputs-contract.v1.md` §7 items 1–5. `identity-schemas.v3.json` `#/$defs/Domain` currently has `subject-inventory`, `target-attribution`, `incoming-search` as canonical-record and does **not** contain `candidate-producer-result`.
- **Counterexample.** Candidate envelopes are accounted as host-derived typed inputs against a view-only stage (`outputDomains: ["view"]`). That is the stated interim, not an optional preview.
- **Required edit.** Exactly the five root registrations already listed in execution-inputs §7: add the domain and digest-row; do not add those domains to a view-only stage that does not produce them; reconstruct reads `CandidateProducerResultV1.sourceBodies` and Plan `candidateSourcePaths`; no unauthenticated locator map. Until that lands, host-derived accounting remains mandatory, not a preview skip.

## Intentionally not changed

- No new D9 class, error, exit, or public-detail code.
- Security S7 lock table, grant V2 truth-table effect values, S10.1/S10.2 lease and `repositoryExecution=false`, S4/S5 floors, S9 schema-1/schema-2 root compatibility.
- Native relation payload grammars, CoverageResultV3, RC-0..RC-6, clone fact modes, candidate-only near/cross-tsjs authority.
- Qualification G13 24-cell historical adapter; full-product matrix remains `SUPPORTED-DESIGN` / not `QUALIFIED` here.
- `product-configuration.schema.v2.json` remains schemaVersion=2 with no enumeration/emission user fields (those are Plan parameters).
- Historical `check-identity.py` `run2:` assertions stay harness evidence.

## Source hashes (sha256)

Edited chapters:

| file | bytes | sha256 |
|---|---|---|
| `docs/v2/contracts/product-v1/native-evidence.md` | 262500 | `5f589bf063b6ff6c2bd8abf85748378b7fbeaff3deec23d86591fd08cdcf494c` |
| `docs/v2/contracts/product-v1/security-and-lifecycle.md` | 89586 | `40cdfdcf4fb02c4ef0c103f1c3e7607215e3af72bdd127a8d2b1150c17e55c2b` |
| `docs/v2/contracts/product-v1/admission-and-qualification.md` | 26501 | `1e440b9d2fc239ff96f473890dfd8246efbaddb5a87923a3986dcf5a6f18d007` |

Beforeimages (`normative-before-evaluator3.v1`): native `bf2cf6e9fd92eba44522e0f8704f390d98ae480368b993c597871ad8d1abe499` (258500); security `7c95766ae3c2af475ca53259dff81e2009d49fb34175d2f305a144a5f2a7defe` (87644); admission `00546dbc83200e2f3439cb44ca3dccf875e7004dcbfadd63ff77a561cf0a235b` (24252).

Root-owned chapters (not edited): identity-and-evidence `14af1bf8b3d0fb7ec71ea5684f0047588d0c0fbd556768b254b36b37d8fa7b4c` (118393); workflows-and-surfaces `508efa60a1a4017ca24d281666343ced190efe17930b34876d87459881ebee71` (89533).

Counterpart source (not edited):

| file | bytes | sha256 |
|---|---|---|
| `foundation/identity-model.py` | 135671 | `12c9cc226b582adc8e34a55e8a59671f2611c46d3e27d1d8289a472d78ccacb6` |
| `foundation/identity-model.v3.py` | 137395 | `e4b8b2c070d06272066410703bd955923c18004f9b9867e774debcf4463e8d75` |
| `foundation/identity-schemas.v3.json` | 183663 | `4ed626ec932ffd480585e67c0044091b3ebda53f18447a8746a5ae377fa341de` |
| `foundation/execution-inputs-contract.v1.md` | 11095 | `7b8352801376d75cbb3b9af86ff4061766e0ef8f37530dc93f1bbc7517ae215c` |
| `foundation/evaluator-composition-contract.v3.md` | 23358 | `11fb572f2604f521753b545c350353919aa238bdde5f5f6c08168a3b496b920d` |
| `native/native_evidence_model.v2.py` | 285290 | `027dce368d7ec26dac2a8f3077d54c91028b6f72c0c3285d5de754ac3ae6dc22` |
| `native/native-evidence.schemas.v2.json` | 229766 | `f20b8353a7be50d7a0c24f413df74e35d23a4e9fc2a4ecc661235655c43c51be` |
| `security/security-lifecycle.schemas.v1.json` | 117413 | `0986123f9069bbe86f663e99d84387189590fe65aadb18ca102ecc23456d2065` |
| `security/security_lifecycle_model_v1.py` | 197996 | `4ee1dfe5f7e4a736959fb7aa0a4466af7bf14945c4bc483ca4749acd8317ea2d` |
| `workflows/workflows_model.v3.py` | 3305 | `4507c8d633c73d600ab97283c714188e56f698b4b08279f2072488cb9e818d8a` |
| `workflows/workflow-projection-contract.v3.md` | 20512 | `1caa823c6b9423f6d07f35fb5ba9cb52dbe6978ed19e5a930f80713dd235ce42` |
| `foundation/check-identity.py` | 578303 | `fd7a9b945e745160fb6f764061ec1d937a796046e814c7c3b3d546396aec0e63` |
| `foundation/check-replay.v3.py` | 16042 | `ec1833ff579b0bc0445650c8beff106c277946c3d9b484c883ba5d41a1af72ad` |
| `foundation/check-semantic-replay.v3.py` | 19474 | `49116da6fefbf6e449216605808c7fb44697cc9aa864dc8ac38fd3f640b44c01` |

Product-design contract vs reference harness: `check-identity.py` and `identity-model.py` remain the native/input identity harness. They do not establish profile-3 evaluator admission. Current public close is `identity-model.v3.close_run`.
