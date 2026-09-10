I’ll review the three allowed normative chapters against the evaluator3 identity/census changes, then make only those chapter edits plus a report in a new output folder.I'll continue the bounded evaluator3 contract-join work: read the three editable chapters against current identity/source, then make only those chapter edits and write the report.Native-evidence already differs from the beforeimage; I'll diff all five chapters and read identity section 4 plus the task prompt.Root already retargeted schema selectors; I’ll pull remaining diffs and hunt for leftover Run2/finding2 authority in the three chapters.Security and admission hashes differ at equal size — I'll extract those diffs and read identity §4.Schema selectors already moved to v3. Next I’ll scan the three chapters and counterpart APIs for remaining profile-3 joins.Admission and security still look profile-2 in places. I’ll read execution-input/enumeration contracts and the native/security join points next.I have the join points. Next I’ll edit the three chapters and pin the out-of-scope source gaps with exact selectors.Applying the three chapter edits at the join points.Chapters are in place. Next I’ll write the join report with hashes, measured counterexamples, and the exact out-of-scope edits.Bounded evaluator3 contract joins are in the three allowed chapters. This is not independent acceptance.

**Edited only**
- `docs/v2/contracts/product-v1/native-evidence.md`
- `docs/v2/contracts/product-v1/security-and-lifecycle.md`
- `docs/v2/contracts/product-v1/admission-and-qualification.md`

Root’s v3 schema-selector and current Run/evidence/seal retargeting is kept. These edits add the joins those selectors did not state: current output is profile 3; native/input identities stay 2; `identity-model.py` is an explicit import2/native adapter, not current Run minting; `identity-model.v3.close_run` is complete replay; symbol census and the execution-inputs manifest are constituents, not preview; candidate locators are not fact authority; zero-config still requests every non-`NOT-SELECTED` cell, but evaluator3 also requires Plan-bound `EnumerationPlanV1` and `EvaluatorEmissionPlanV1`; security repair/import/installation cannot treat historical `run2`/`finding2` as current authority; cache/regen hash is not authority. Permission/lease semantics and qualifier limits are unchanged. No new D9 code.

**Measured source gaps (not closed by chapter prose)**

| id | fact | required edit (out of scope) |
|---|---|---|
| R1 | `identity-model.v3.admit_parameter_selection([])` **ADMITs** | Enforce `requiredForEvaluatorMajors=[3]` at Plan/spec admission |
| R2 | `default_capability_selection` emits `parameters: []` | Plan construction inserts the two parameters after snapshot/membership |
| R3 | grant-journal `runId` pattern admits `run2:`, refuses `run3:` | Current SEAL names `run3`; historical `run2` journals stay those bytes |
| R4 | native schema still annotates `evidence2/seal2/run2` | Current chain `evidence3/seal3/run3` |
| R5 | workflows chapter still says `policy-derivation2` (line 1060) | `policy-derivation3`; current invocation schema is evaluator3 |
| R6 | `candidate-producer-result` domain still unregistered | Exactly execution-inputs §7’s five root registrations |

Replay already refuses missing enumerator/emission parameters (`EVALUATOR_REQUIRED_PARAMETER_MISSING`). Hash-only owner admission does not. That is the hidden-authority split.

Report: `/tmp/opensip-design-corrections/grok-evaluator3-contract-joins.v1/review.md` and `review.json`.

Chapter hashes: native `5f589bf063b6ff6c2bd8abf85748378b7fbeaff3deec23d86591fd08cdcf494c`, security `40cdfdcf4fb02c4ef0c103f1c3e7607215e3af72bdd127a8d2b1150c17e55c2b`, admission `1e440b9d2fc239ff96f473890dfd8246efbaddb5a87923a3986dcf5a6f18d007`.
