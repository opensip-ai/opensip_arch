# Consumer24 items M4, M5, S5, S6, S7, A6, A8, A9, A11, A12, A13, A14: nonblind assessment against source37 and source38

**Standing.** This is a nonblind, bounded assessment by the same coauthor origin (f5617310…).
- It is not independent design acceptance, a blind continuation, root readiness, application or grades.
- I made no source, live, pin or planning edits, and there is no patch. Root reconciles cross-owner consequences first.
- The consumer24 report is a claim. Its exported vectors were used only as probe inputs, never as an oracle.
- The active independent source38 review runtime was not read.

## Inputs (verified at start and end)

| Input | SHA-256 | Result |
|---|---|---|
| Consumer kit manifest | `e57ef3a7…4cc3c` | 102 files exact; parent is source37 |
| Source37 manifest | `245ef613…676680` | 12,900 files exact |
| Source38 manifest | `2ddfa0db…7e5c5` | 12,904 files exact |

- Between source37 and source38, 41 files changed and 4 were added.
- Every probe ran on both frozen trees with the reference interpreter (`-I -B`).
- All twelve sections gave identical results on source37 and source38. None of these items was corrected between 37 and 38.
- Exact hashes of every selector, reference file, consumer file, probe and receipt are in `review.json` (`readHashes`, `receiptSha256`).

## Summary

| Item | Consumer | Disposition | Confirmed severity |
|---|---|---|---|
| M4 | MUST | Real gap; the derivation exists only in excluded reference Python | **MUST** |
| M5 | MUST | Real gap: contract contradicts the envelope schema | **MUST** (public query surface) |
| S5 | SHOULD | Real gap; the recipe exists only in reference Python | SHOULD |
| S6 | SHOULD | Real gap: golden/registry defects, and one golden contradicts its owner | SHOULD |
| S7 | SHOULD | Real gap; the owner reference itself publishes an unlawful CODE-FIXED | SHOULD (strengthened) |
| A6 | advisory | Real identity-bearing precedence gap; the consumer's reading also diverges from the reference | **MUST-class, bounded** (upgraded) |
| A8 | advisory | Mostly intended (internal keys); two public detail selections unstated | advisory |
| A9 | advisory | Prose under-specification; reference and consumer agree | SHOULD (upgraded) |
| A11 | advisory | Latent schema inconsistency; no lawful instance today | advisory |
| A12 | advisory | Label/prose gap; the gate decision is lawful | advisory |
| A13 | advisory | Real missing public detail | SHOULD (upgraded) |
| A14 | advisory | Intended semantic choice, disclosed in the kit | none |

## Items

### M4: `detectorId` has no normative derivation. Confirmed MUST.

**Owner selectors**
- evaluator3 `baseline-artifact.schema.json`: `DetectorClosureEntry.detectorId` and `BaselineEntry.detectorId` are bare CanonicalIdentifiers. `contributionId` sits beside them with no join between the two.
- evaluator3 `comparison-result.schema.json`: `Entry`, `DetectorDisposition`.
- workflow-projection-contract §2 line 57: emission bindings carry `contributionId`, no `detectorId`.
- workflow-projection-contract §11 line 190: the exact `{detectorId→(closureId, semanticsMajor)}` map.
- workflows-and-surfaces §2.

**Where the law actually lives.** Only in `workflow_projection_model.v3.py` (`detectorId = contributionId`, "One detector row per contributionId"), which the kit excludes.

**Probe**
- Input: the consumer's exported baseline artifact, plus a variant whose `detectorId` values are renamed while `contributionId` is kept and `baselineId` is recomputed.
- Both the schema and the owner's `verify_baseline_artifact_v3` **admit** both artifacts. The owner verifier does not enforce the derivation, so a validator is missing.
- The `baselineId`s differ (`4c1cfa54…` vs `125ee4b7…`).
- The exact E0 map join refuses the variant: `CONFIG.INVALID` / `EVALUATION.FINDING_JOIN_REFUSED`.

**Consequence.** Portable baselines diverge across conforming hosts and fail E0.

**Remedy**
- Add prose, not Python:
  - `detectorId` equals the emission-plan `contributionId` of the entry's rule binding.
  - `DetectorClosureEntry` has one row per `contributionId`, with `detectorId == contributionId`.
  - A disagreeing `(closureId, semanticsMajor)` refuses `EVALUATION.FINDING_JOIN_REFUSED`.
  - Every entry's `detectorId` is a member of `detectorClosure`.
- Add the check to baseline admission and a negative control.
- Affected files: workflows-and-surfaces §2, workflow-projection-contract §2/§3/§11, the two evaluator3 schemas (descriptions only), `verify_baseline_artifact_v3`, and check-workflow-projection.
- This codifies the reference derivation, so reference baselines are not reminted.

### M5: the query parity field `query-response` has no carrier. Confirmed MUST.

**Owner selectors**
- workflows-and-surfaces §8, lines 1055–1077 (same text in source38).
- The required-delivery law, lines 995–1005.
- command-inventory v3: the query command's `parityFields`, and the JSON renderer rule "CommandEnvelope major 3 is the parity reference".
- evaluator3 `command-envelope.schema.json`: `additionalProperties:false`; `query` holds only the compact `QueryResult`.

**Probe**
- A lawful query envelope is admitted.
- Adding `queryResponse` is refused (`additionalProperties`).
- No envelope field references `GraphQueryResponseV1`.
- The reference renderer itself emits an unpublished `{format, parity, envelope}` object, and raises `KeyError` when `query-response` is missing.

**Consequence.** No conforming JSON or agent query rendering can satisfy both the schema and the required parity field. The required-delivery law then forces `DELIVERY.REQUIRED_FAILED`, which leads straight into A13.

**Remedy**
- Preferred: add an envelope `queryResponse` field (`$ref` graph-query:3 `GraphQueryResponseV1`), required exactly when `kind=query`, keeping the existing project, termination and summary joins.
- Restate the JSON and agent `parityRule` to match.
- Alternative: publish a separate rendering record.
- Root decides whether this can stay within pre-release major 3.

### S5: the `argvDigest` recipe is unpublished. Confirmed SHOULD.

**Owner selectors**
- security-and-lifecycle lines 1065 and 1115 say only "argv digest", and line 1122 only names the field `argvDigest`. The text and line numbers are the same in source37 and source38.
- workflows-and-surfaces §7, lines 931–937.
- `RepoExecutionGrantV2.argvDigest`.
- `TestPayloadV1.argvDigest`.

**Probe**
- Three plausible recipes give three different digests for one argv.
- All four reference sites agree on raw SHA-256 of C(argv array): the workflows model (twice), the native adapter, and the checker. The security model only compares equality.

**Consequence**
- A mismatched grant fails closed: `TEST.PRINCIPAL_NOT_ADMITTED`, never a false admission.
- Independently produced test payloads, and therefore their import identities, diverge.
- Replay does not recompute the digest, so Runs are not made unclosable.

**Remedy**
- Add prose in security-and-lifecycle and workflows §7: `argvDigest` is lowercase hex raw SHA-256 of C(argv) over the exact ordered argument array. That array is the test-runner params, the host-selected preparation argv, or the adapter-recorded argv for imports.
- Avoid editing `test-execution.schema.json`: it is a registered payload schema, so any byte change alters `payloadSchemaDigest`.

### S6: three failure goldens cannot form a lawful failure envelope. Confirmed SHOULD.

**The goldens:** `doctor-report-not-producible`, `query-latest-empty`, `envelope-major-unsupported` (unchanged in source38).

**Why they fail**
- The `Golden` schema makes `domainDetail` optional, but `kind=failure` requires `errors`.
- workflows-and-surfaces says goldens include actual details (kit line 1390; source38 line 1406).

**Probe**
- All three envelopes without `errors` are refused.
- `query-latest-empty` with `QUERY.VIEW_UNKNOWN` is admitted, and that is the owner's own detail.
- No registered code fits the other two:
  - `DOCTOR.DEFECTS_FOUND` is a success detail.
  - `ENVELOPE.*` codes belong to signed security envelopes.
  - `QUERY.SCHEMA_MAJOR_UNSUPPORTED` is about the graph-query request major.

**Remedy**
- Add `domainDetail QUERY.VIEW_UNKNOWN` to `query-latest-empty`.
- Register two workflows-owned details (e.g. `DOCTOR.REPORT_NOT_PRODUCIBLE`, `OUTPUT.ENVELOPE_MAJOR_UNSUPPORTED`) and cite them in their goldens.
- Require `domainDetail` on request-rejected and operational-failed goldens unless a named route composition supplies it.
- No new D9 code. The common-schema and registry edits are cross-owner.

### S7: unknown current absence is published as CODE-FIXED. Confirmed and strengthened, SHOULD.

**Owner law vs owner schema**
- workflows-and-surfaces §3, lines 338–352: unknown roots, incomplete enumeration, disabled evaluation and exhausted budgets never establish absence.
- The schema's `PivotPresence.E4` is a non-nullable boolean, and `IndeterminateReason` has no member for unknown current absence.

**Where the owner reference breaks the law.** In source38 `workflow_projection_model.v3.py`, both `compare_admitted_v3` (line 2557) and `_derive_or_admit_presence` (line 659) set `E4 = bool(matched hit)` with no absence proof. `_presence_from_equalities` then copies E4 into unchanged pivots.

**Probe**
- Owner `classify` with B=true and E0–E4=false gives **CODE-FIXED**.
- An entry with `E4=null` is refused by the schema.
- An INDETERMINATE entry is admitted with any reason, so the schema cannot tell a right reason from a wrong one.
- The consumer's approximated INDETERMINATE is closer to the prose than the owner model.

**Consequence**
- Gating rules still reach an indeterminate verdict through `ruleDeficiencies`.
- Non-gating entries can publish a false CODE-FIXED. No gate flip was found.

**Remedy**
- Apply the pivot absence-knowledge law to E4. Otherwise classify INDETERMINATE with a new reason, e.g. `current-absence-unknown`; root decides the schema shape.
- Optionally distinguish a bound-but-unknown pivot from an unavailable one.
- Add controls.
- Affected files: comparison-result schema, workflows §3, workflow-projection-contract §12, the workflow projection model, check-workflow-projection.

### A6: correspondence precedence is unstated and identity-bearing. Upgraded to MUST-class, bounded.

**Owner text**
- Composition §4 line 46 lists the conditions unordered.
- The §9.5 table (lines 182–190) has one row per condition.
- §9.7 line 255 names "the correspondence cause" in the singular.

**Owner reference.** `correspondence()` returns the first applicable condition in a fixed order: projection-unavailable, then population-incomplete, then signature-ambiguous. It emits exactly one deficiency and that reason.

**Probe (synthetic subjects)**

| Co-occurring conditions | Owner reference returns |
|---|---|
| Empty tokens + incomplete population | projection-unavailable only |
| Incomplete population + shared signature | population-incomplete only |

The deficiency Cset digest also differs between readings: `09c3c9d9…` (first applicable only) vs `a8faa306…` (every applicable row).

**Consequence**
- When conditions co-occur, readers mint different proof3/seal3/run3 bytes, and possibly different `finding3` reasons.
- The consumer's "every applicable deficiency" choice is one such divergence from the reference.

**Remedy.** State the fixed order and "first applicable condition is the sole cause: one deficiency, `reason` = that cause". Add a co-occurrence control. This codifies the reference, so nothing is reminted.

**Limits.** This was not a full-Run probe, and consumer exports were not checked for co-occurrence.

### A8: unnamed refusal keys. Advisory, partly confirmed.

**Intended.** Internal keys are deliberately not public codes. The E0 join detail is already named in workflow-projection-contract §13.

**Unstated public details, probed on a real retained Run and in the model.** Two public detail selections appear only in reference models:

| Situation | Reference refusal | Contract text |
|---|---|---|
| Query `projectId` ≠ admitted Run | `REQUEST.PRECONDITION_FAILED` / `QUERY.PARAMS_MALFORMED` | No §7 row in source37 or source38 |
| Present but missing detector compatibility listing | `EVALUATION.PROJECTION_INPUT_INCOMPLETE` | workflows §2 says only "refuses" |

**Remedy.** Add a query §7 row and one workflows §2 sentence. No new code.

**Not probed.** The test consent relabel and native-preparation grant joins.

### A9: required evidence unavailable when the root is decided elsewhere. Upgraded to SHOULD (prose clarification).

**The ambiguity.** Composition §5 line 56 has two sentences that point different ways:
- The outcome sentence lists only population and root-blocking causes.
- The next sentence says required import obligations are assessed independently of the branch.

**Owner reference.** It makes a gating rule with a rule-level `evidence-kind-unavailable` indeterminate, unless a live finding fails it. This agrees with the consumer's choice.

**Why it matters.** A literal reader of the outcome sentence would seal a different, identity-bearing outcome.

**Evidence.** Static extraction only.

**Remedy.** Amend the §5 outcome sentence to say so.

### A11: `EnforcementValue` omits `ENFORCED-PLATFORM:<primitive>`. Advisory, latent.

**Failed first attempt (preserved).** My probe used `afterStep="analyze"` and was refused because StepId is an integer from 0 to 63.

**Retry with `afterStep=0`**
- The base params are admitted.
- `ENFORCED-PLATFORM:seatbelt` is refused by the enum.
- The security `EnforcementV1` pattern admits it.
- The truth tables contain no platform primitives (0 occurrences).

**Remedy**
- Defer the schema change and qualify the description in prose.
- A later change should reference security `EnforcementV1`.
- `test-execution.schema.json` is a registered payload schema, so changing its bytes alters `payloadSchemaDigest`.

### A12: `gateReason` label for a detector-hidden CODE-NET-NEW. Advisory.

**Probe (owner `classify`).** Both detection-hidden and policy-hidden CODE-NET-NEW entries gate as fail with `gateReason code-net-new-policy-hidden`. Only `subsequentDeltas` differs.

**Why it is only a label gap.** The gate is lawful: workflows §3 says a detector-hidden bug still gates. But §3 describes that reason only for policy, scope or waiver hiding.

**Remedy.** Define the member in prose as "not live in current because of any later axis". No enum change.

### A13: required-delivery failure before commit has no registered detail. Upgraded to SHOULD.

**Owner selectors.** workflows-and-surfaces lines 995–1010, and the after-commit failure-table row (kit line 1155; source38 line 1158).

**Probe**
- A no-detail `DELIVERY.REQUIRED_FAILED` failure envelope is refused.
- A no-Run envelope carrying `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` is admitted, so the schema does not catch a semantically false detail.

**Consequence.** M5 makes this path mandatory for every query JSON rendering.

**Remedy**
- Register a workflows detail, e.g. `DELIVERY.REQUIRED_PROJECTION_FAILED`, and state it in §8 and the failure table.
- Restrict the after-commit detail to terminations that carry a `runId`.
- The common-schema and registry edits are cross-owner.

### A14: exact-import evidence attribution. Intended semantic choice.

- workflows-and-surfaces lines 1395–1405 (kit/source37; source38 lines 1411–1421) state that evidence-change attribution is deliberately conservative.
- The same paragraph names a future evidence-pivot successor.
- The consumer's `cmp-code-det2` measurement is consistent with that disclosed law.
- No correction is needed.

## Cross-owner consequences for root

- **S6 and A13** add `DomainDetailCode` members to the shared evaluator3 common schema and the public-detail registry.
- **M5** changes the envelope schema and interacts with A13.
- **S7** changes the comparison-result schema, and comparison2 identities for affected entries.
- **S5 and A11** touch a registered payload schema document, so prefer prose.
- **M4 and A6** codify existing reference derivations, so reference fixtures and RunIds should not need reminting. Consumer exports built with different choices would change.

## Limits

- The corpus is finite:
  - one consumer baseline artifact
  - synthetic correspondence records and synthetic `classify` presences
  - schema-level envelope probes
  - one retained Run fixture
- S7 relied on source reading of `compare_admitted_v3`; I did not run a full admitted comparison with an incomplete current rule.
- A9 is static evidence only.
- Reference models were exercised as executable references. Law findings rest on normative text, and no Python is proposed for the normative set.
- No product host, renderer, platform or qualification is involved.
- Consumer exports were not validated against the owner references (root does that).

## Commands (reference interpreter `-I -B`; all exit 0)

- `probes/verify_inputs.py initial` and `probes/verify_inputs.py final`
- `probes/probe_owner_laws.py source38` and `probes/probe_owner_laws.py source37`
- `probes/probe_a11_retry.py source38` and `probes/probe_a11_retry.py source37`
- `probes/collect_hashes.py`
- `probes/build_review.py`
