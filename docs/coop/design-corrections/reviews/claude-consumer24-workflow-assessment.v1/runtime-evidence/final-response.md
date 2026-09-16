I've written review.md and review.json for the 12 consumer24 items. I checked each against the frozen source37 and source38 trees using the reference interpreter. Every probe gave identical results on both trees, so none of these items was fixed between 37 and 38. There is no patch and no readiness claim; root still has to reconcile the cross-owner effects.

## Results

| Item | What I found | Confirmed severity |
|---|---|---|
| **M4** | Nothing in the normative text says how `detectorId` is derived; only reference Python sets it to `contributionId`. A baseline whose `detectorId` differs from `contributionId` passes both the schema and the owner's verifier, gets a different `baselineId` (`4c1cfa54…` vs `125ee4b7…`), and is refused at the E0 join (`EVALUATION.FINDING_JOIN_REFUSED`). | **MUST** |
| **M5** | Query output must include the full `query-response`, but the envelope schema forbids extra fields and has nowhere to put it. The reference renderer itself outputs a non-envelope object. No conforming JSON or agent query output is possible, so every one ends as `DELIVERY.REQUIRED_FAILED`. | **MUST** |
| **S5** | The `argvDigest` recipe is only in reference code (raw SHA-256 of the canonical argv array). A mismatched grant is refused rather than wrongly admitted, but independently produced test payloads get different identities. | SHOULD |
| **S6** | Three failure goldens can't form a valid failure envelope because the required `errors` field is missing. `query-latest-empty` should carry `QUERY.VIEW_UNKNOWN`. The other two have no registered detail code that fits. | SHOULD |
| **S7** | Worse than reported: the owner model sets current presence (E4) with a plain `bool()` and no absence proof (model lines 2557 and 659). When current absence is actually unknown it publishes CODE-FIXED, which the workflows prose forbids. The schema has no field value or reason code that can express "unknown". | SHOULD |
| **A6** | Raised from advisory. When several correspondence conditions apply at once, the contract gives no precedence. The reference emits only the first condition, the consumer emits all of them, and the resulting proof digests differ (`09c3c9d9…` vs `a8faa306…`). | MUST-class (only where conditions co-occur) |
| **A8** | Keeping internal keys unnamed is intended. Two public detail choices appear only in code: `QUERY.PARAMS_MALFORMED` for a query `projectId` that doesn't match the Run, and `EVALUATION.PROJECTION_INPUT_INCOMPLETE` for a detector listing that is declared but missing. | advisory |
| **A9** | The §5 outcome sentence leaves out required `evidence-kind-unavailable`; the reference and the consumer both treat it as indeterminate. | SHOULD (prose fix) |
| **A11** | The schema refuses `ENFORCED-PLATFORM:seatbelt`, although its own description and the security pattern allow it. No valid case exists today, since the truth tables have no platform entries. | advisory |
| **A12** | A CODE-NET-NEW hidden by a detector change still correctly gates, but it is labelled `code-net-new-policy-hidden`. | advisory |
| **A13** | A required-delivery failure before commit has no registered detail. The only candidate, `RENDERER_FAILED_AFTER_COMMIT`, is wrong in that case, yet the schema accepts it. | SHOULD |
| **A14** | Intended and already disclosed in the kit (source38 lines 1411–1421). No correction needed. | none |

## Where the normative text is missing (M4, S5, S7, A6, A9)
Adding the reference Python to the normative set would make the implementation the law. Each of these needs a short prose statement instead. For M4 and A6 that prose would simply write down what the reference already does, so reference runs and IDs shouldn't need regenerating. Consumer exports built on different choices would change.

## For root to reconcile
- **S6 and A13** add detail codes to the shared evaluator3 common schema and the public detail registry.
- **M5** changes the envelope schema and is tied to A13.
- **S7** changes the comparison-result schema and the comparison identities of affected entries.
- **S5 and A11** touch a registered payload schema; any byte change there alters `payloadSchemaDigest`, so a prose fix is better.

## Limits and failed attempts
- My first A11 probe was refused because `afterStep` must be an integer, not `'analyze'`. That failed result is kept in the receipts, and the retry with `afterStep=0` gave the result above.
- The test corpus is small: one consumer baseline, synthetic inputs for S7, A6 and A12, schema-only checks for M5, S6, A11 and A13, and one retained Run for A8.
- For S7 I didn't run a full comparison with an incomplete current rule. For A9 I only read the code; I didn't execute `compose`.
- Some A8 internal keys weren't probed.
- The consumer exports weren't validated against the owner references.
- I didn't read or touch the independent source38 review.

Before building review.json I rechecked the review's line numbers against the trees and corrected four that were imprecise. Input manifests matched at the start and at final verification, and I made no source edits.

Files are in `/private/tmp/opensip-design-corrections/claude-consumer24-workflow-assessment.v1/` (the probe scripts are in `probes/` and the receipts in `receipts/`):
- review.md
- review.json (sha256 `56e20523…`)
