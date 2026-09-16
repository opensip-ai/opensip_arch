# Nonblind source-gap assessment: V23-S1, V23-S2 and V23-S3 on frozen candidate36

All three findings are **real** and **SHOULD-level**:
- **V23-S1:** a source inconsistency.
- **V23-S2:** a source inconsistency, not a lawful scope distinction.
- **V23-S3:** a narrow missing recipe.

**My source36 acceptance must reopen.** One coherent successor fixes all three. It was rehearsed only in a
disposable copy, and it deliberately leaves one schema's bytes unchanged, because editing them would
strand retained evidence.

**Standing.**
- Actual Claude, source-review origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`.
- This is a bounded **nonblind** gap assessment. It is **not blind consumer B**,
  **not the final application review**, not fresh-blind standing, and not acceptance of any successor.
- My candidate36 technical ACCEPT (`review.json` `fa1b7f48…`) is historical evidence of that review. It is
  not a resolution of these findings.
- Nothing here grants an application outcome, architecture readiness, activation or implementation
  authority.

**Provenance.**
- **Original dispatch.** It ran in this runtime and labelled the input an *interim* captured consumer report;
  that label is kept as historical dispatch. That process ended with a progress-only response while my p04
  rehearsal was still running, and wrote no assessment.
- **Completion.** It ran under `claude-consumer23-gap-assessment.v2`: same origin, not a new independent
  origin, and the previous CLI process had ended.
- **Report bytes.** They hash to `77cfab1f…`. Root states these bytes are the completed original blind
  consumer23 final report and that its final three SHOULD equal this input. I verified only my copy's
  digest, and neither contacted the consumer nor read its outputs.
- **Subject.** Manifest `a729406b…`, read-only.
- **Expected law.** I wrote `expected-before-probes.json` before any probe ran; file time versus the first
  probe start, asserted by b02. It held for all three findings.

| Finding | Classification | Severity | Correction |
|---|---|---|---|
| V23-S1 | Real source inconsistency | SHOULD: same class, exit and errorCode; different DomainDetail and remedy | Request-side endpoint `$def`, plus contract, model and controls |
| V23-S2 | Real source inconsistency inside native, against the D9 owner | SHOULD: whole-Run reasonCodes diverge for three deficiencies; class and exit unchanged | Three §10 cells, a one-mapping paragraph, model, native case; schema bytes unchanged |
| V23-S3 | Real but narrow normative gap (missing recipe) | SHOULD (small) | Publish the availability-to-detail mapping, plus controls |

---

## 1. V23-S1: package endpoint without `packageManifestPath`

**Selectors.**
- `workflows/query-projection-contract.v3.md`:
  - §2 "Fault precedence" steps 1–2 (lines 43–47);
  - §7 rows at lines 165 and 167;
  - §8 steps 1 and 5.
- `workflows/schemas/evaluator3/graph-query.schema.json#/$defs/GraphEndpoint` `allOf[0]` (kind=package ⇒ required
  `packageManifestPath`). It is referenced by request params `endpoint`/`start`/`target` **and** by response rows.
- `public-detail-registry.v1.json`: both `QUERY.ENDPOINT_AMBIGUOUS` and `QUERY.PARAMS_MALFORMED` select the
  contract and the schema.
- `query_projection_model.v3.py`: `_validate_request` (schema first) → `effective_params` →
  `parse_endpoint_syntax`; `inventory_vertices`.

**Observed on frozen36** (`receipts/p01-s1-endpoint.json`):

| Route | `{kind: package, nativeSubjectId: app}` with no coordinate |
|---|---|
| raw `GraphEndpoint` and `GraphQueryRequestV1` schema | refused |
| public `execute_graph_query` | `REQUEST.PRECONDITION_FAILED` / **`QUERY.PARAMS_MALFORMED`**, valid failure envelope |
| `parse_endpoint_syntax` / `effective_params` | **`QUERY.ENDPOINT_AMBIGUOUS`** (unreachable on the public path) |
| §2 precedence | **`QUERY.ENDPOINT_AMBIGUOUS`** (step 2) |

- **Every other step-1 shape agrees on all routes.** Bad kind, bad universe, empty id, an extra property,
  and a coordinate on a non-package all give PARAMS_MALFORMED.
- **The other ENDPOINT_AMBIGUOUS clause** ("a well-formed tuple that matches more than one admitted vertex")
  can never fire in the reference. `inventory_vertices` keys vertices by the full tuple, so it could not mark
  a duplicate, a same-name/two-manifest pair, or a repeated package ambiguous. The package-coordinate clause
  is therefore the registered detail's only designed route, and closed-schema admission blocks it.

**Consumer reading.**
- It found the conflict correctly.
- Its applied reading (re-admit with a placeholder coordinate) is not published law.
- Both of its smallest-fix options are lawful.

**Recommended correction: preserve the explicit §2 distinction.** §2 is the specific endpoint law. It
deliberately separates malformed syntax from an absent coordinate, with its own registered detail and
remedy.
- **Schema.** Add `GraphRequestEndpoint`: `kind=package` may omit `packageManifestPath`, while a coordinate on
  a non-package stays forbidden. The four request params reference it; response rows keep the strict
  `GraphEndpoint`.
- **Contract.**
  - §2 step 1: a present coordinate that is not a LogicalPath is malformed.
  - §2 step 2: "whose `packageManifestPath` is absent".
  - §2: one paragraph naming the request/response split.
  - §7: row label.
  - §8 step 1: an absent coordinate passes closed admission and is refused by §2 step 2 before vertex lookup.
- **Model.** `parse_endpoint_syntax`: absent ⇒ ENDPOINT_AMBIGUOUS; present but empty or non-string ⇒
  PARAMS_MALFORMED.
- **Controls:**
  - `closed-request-admission-leaves-absent-package-coordinate-to-section-2`;
  - `response-graph-endpoint-still-requires-package-coordinate`;
  - `package-endpoint-without-coordinate-is-endpoint-ambiguous` (public wrapper, real admitted Run, envelope
    validated);
  - `empty-package-coordinate-is-params-malformed`;
  - `package-coordinate-on-file-endpoint-is-params-malformed`.

**Measured on the corrected rehearsal** (`receipts/p05-successor-rehearsal2.json`):
- The request schema admits the absent coordinate and the response endpoint still refuses it.
- A wrapper call without a Run reaches the Run check (`QUERY.VIEW_UNKNOWN`), which proves closed admission
  passed.
- The real-Run control gives `QUERY.ENDPOINT_AMBIGUOUS`.
- An empty coordinate gives PARAMS_MALFORMED.
- The query checker passes **131/131**.

**Lawful alternative.** Keep the schema and publish that an absent coordinate is a closed-schema refusal
(PARAMS_MALFORMED).
- It needs no schema or planning-input change for S1.
- But ENDPOINT_AMBIGUOUS would then have no reachable graph route, and §2 step 2 and the §7 row must be
  rewritten.

**Cross-owner effects.**
- Owners changed: the workflows query contract, the graph-query schema, the query model and the query checker.
- `graph-query.schema.json` is a planning layer4 normative input.
- No retained Run commits its digest (`receipts/s04-retained-schema-digests.json`).
- The detail registry and D9 are unchanged.
- No 107-row owner is a query file.

## 2. V23-S2: native §10 `VERDICT.INDETERMINATE` versus D9 whole-Run reasonCodes

**Selectors.**
- `docs/v2/contracts/product-v1/native-evidence.md` §10, column "Existing code", rows
  `language-tier-unsupported` (2907), `confidence-floor-unmet` (2909) and `required-relation-missing` (2910).
- The same file, §10 "inherits `d9-exit-contract.v1.14.json` **unchanged**" (3051), and §4.6 "the **public D9
  termination** of the Run or step … still the §10 class/code columns" (2148–2153).
- `docs/coop/artifacts/d9-exit-contract.v1.14.json`:
  - `codeMaps.deficiencyToReasonCode` ("total and injective");
  - `causeModel.codeDerivation`;
  - goldens `analysis-required-coverage-missing`, `analysis-language-tier-unsupported`,
    `analysis-confidence-floor-unmet` and `repair-verification-indeterminate`.
- The evaluator3 `common.schema.json#/$defs/D9Deficiency` description.
- `workflows-and-surfaces.md` lines 783–796.
- `native-evidence.schemas.v2.json` `publicD9Termination`.
- `native_evidence_model.v2.py` `run_termination` (3668), `D9_MAP` and `d9_map`.

**Observed on frozen36** (`receipts/p02-s2-d9.json`):

| Deficiency | D9 member | D9 owner code | §10 Existing code | model `run_termination` | `d9_map` |
|---|---|---|---|---|---|
| input-closure-incomplete, resolution-incomplete, external-consumers-unknown, derivation-policy-unmet | no | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE |
| provider-unavailable | yes | COVERAGE.PROVIDER_UNAVAILABLE | same | same | refused (key is `provider-unavailable/capability-missing`) |
| language-tier-unsupported | yes | **COVERAGE.LANGUAGE_TIER_UNSUPPORTED** | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE | refused |
| budget-exhausted | yes | COVERAGE.BUDGET_EXHAUSTED | COVERAGE.BUDGET_EXHAUSTED | **VERDICT.INDETERMINATE** | COVERAGE.BUDGET_EXHAUSTED |
| confidence-floor-unmet | yes | **COVERAGE.CONFIDENCE_FLOOR_UNMET** | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE | refused |
| required-relation-missing | yes | **COVERAGE.REQUIRED_RELATION_MISSING** | VERDICT.INDETERMINATE | VERDICT.INDETERMINATE | refused |

**Why this is not a per-requirement versus whole-Run distinction.** Every relevant owner sentence was
matched verbatim, and together they allow only one mapping:
- A per-requirement outcome carries a `DeficiencyV2` value and **no D9 code** (§4.6: "never `D9Deficiency`").
- `D9Deficiency` "still carries every whole-Run and comparison-step termination", and "the public D9 route for
  a Run carrying such a requirement is still native §10's" (workflows-and-surfaces).
- §4.6 names the §10 columns as that termination.
- §10 says it inherits D9 unchanged.
- D9 derives `reasonCodes = [map(deficiency)] + secondaries`.
- The D9Deficiency description sends only the **four native-only** outcomes to indeterminate with the
  existing code.

Treating the §10 column as a per-requirement route would invent a distinction the sources refute.

**Consumer reading.**
- It found the conflict correctly and applied the right reading: the D9 exit contract governs whole-Run
  terminations.
- Its first fix option would invent the distinction above.
- Its second option (align the three codes) is correct.

**Budget mapping mismatch.** On the deficient-entry route, `run_termination` maps `budget-exhausted` to
VERDICT.INDETERMINATE. Every other source gives COVERAGE.BUDGET_EXHAUSTED: §10, `D9_MAP[budget-exhausted]`,
`stage_authority("budget-exhausted")` and D9 `codeMaps`. The published sources agree; the model contradicts
them. The same model change corrects it.

**Recommended correction.**
- **`native-evidence.md` §10:**
  - `language-tier-unsupported` → `COVERAGE.LANGUAGE_TIER_UNSUPPORTED`;
  - `confidence-floor-unmet` → `COVERAGE.CONFIDENCE_FLOOR_UNMET`;
  - `required-relation-missing` → `COVERAGE.REQUIRED_RELATION_MISSING`;
  - one paragraph saying the column *is* D9 `codeMaps.deficiencyToReasonCode` for D9Deficiency members, and
    `verdict-indeterminate` for the four native-only outcomes (one mapping);
  - a disclosure that the `publicD9Termination` annotation in `native-evidence.schemas.v2.json` keeps an
    incomplete older three-code parenthetical, that §10 governs, and why the annotation's bytes stay
    unchanged (next subsection).
- **`native_evidence_model.v2.py`:** `D9_DEFICIENCY_REASON_CODE` mirrors the D9 map, and `run_termination`
  uses it.
- **`native-cases.v2.json`:** new case `run-termination-derives-the-d9-exit-contract-reason-code-for-each-deficiency`,
  covering five D9 members and one native-only outcome.
- **Not changed:** any D9 class, exit or reason code, `D9Deficiency`, `DomainDetailCode`, or `D9_MAP` key.
  check-integration requires `D9_MAP` keys to be registered details, which these deficiencies are not.

**Measured on the corrected rehearsal.**
- The model equals D9 for all nine deficiencies.
- The kit's §10 rows read the three COVERAGE codes.
- Native passes **376/376**, including the new case.
- check-identity's projection control still holds.

### Correction to my own first patch

My first patch (`v1 successor-patch/successor-v23-gaps.patch`, `8222d978…`) also rewrote the
`publicD9Termination` text *inside* `native-evidence.schemas.v2.json`. The rehearsal showed this is not a text-only
change:
- **Fixture guard.** check-identity's `v20-native-view-fixture-declares-current-registered-schemas` failed,
  because a native-cases fixture declares the document's old digest (`receipts/s01-p04-status.json`,
  `receipts/s03-digest-bearers.json`).
- **Retained Runs.** All **13** package13 retained Runs commit that registered schema document's digest,
  18–48 times each (`receipts/s04-retained-schema-digests.json`).
- **Replay.** Replaying them against owners carrying that edit refuses every positive Run with
  `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT:native/native-evidence.schemas.v2.json` (variant A).

The recommended v2 patch therefore leaves those bytes unchanged and discloses the stale annotation in §10.
Correcting the annotation belongs to a schema-document successor with its own registration.

### Helper-versus-full-D9 limitations (still open, not corrected here)

- **One code only.** `run_termination` returns a single reason code, chosen by native `PRECEDENCE_V2`. D9 derives an
  ordered `reasonCodes` list with `secondaryDeficiencies`; golden `analysis-multiple-deficiencies` has two
  codes.
- **No IDs or reduction.** The helper emits no `runId` or `coverageId` and performs no cross-family reduction
  (faultCause > rejectionCause > deficiency). Those remain host/D9 derivation duties.
- **`d9_map` is detail-keyed, not a code map.** It refuses `provider-unavailable` and the three corrected
  deficiencies, which is consistent with check-integration.
- **Proof-cause selection is out of scope.** Only the deficiency-to-reason-code map is fixed. How an evaluator
  proof cause such as `required-cell-unsatisfied` selects a whole-Run D9Deficiency is not decided here.

**Cross-owner effects.**
- **Owners changed:** native contract §10, the native model and native cases.
- **Unchanged:** the D9 artifact (it is the governing map) and workflows-and-surfaces.
- **Planning:** `native-evidence.md` is a planning layer4 normative input.
- **Rows:** **15** of the 107 rows own `native-evidence.md` and must be re-read by a successor review: AR-07,
  AR-12, AR-13, AR-16, FW-01, FW-02, FW-03, FW-04, FW-08, FW-10, DR-004, DR-007, DR-011-R01, DR-011-R05 and
  DR-011-R08.

## 3. V23-S3: detail for availability `unavailable`

**Selectors.**
- `workflows/query-projection-contract.v3.md` §7 availability paragraph (line 160) and table (lines 173–174,
  which cover only missing and corrupt retained bytes).
- `identity-and-evidence.md` §5, which lists the availability states and delegates the graph selector to query §7.
- `foundation/identity-schemas.v3.json` `availability.state` enum.
- `public-detail-registry.v1.json` evidence.* records: no meaning text, and no `evidence.unavailable`.
- `query_projection_model.v3.py` `AVAIL_REFUSE`; `foundation/identity-model.v3.py` `EvidenceUnavailable`.

**Observed through the public wrapper over a real admitted Run** (`receipts/p03-s3-availability.json`):

| Trusted availability | Outcome |
|---|---|
| omitted / `retained` / `partial` | not refused by the observation (query succeeds) |
| `expired` | operational-failed / HOST.IO_FAILURE / host-io / `evidence.expired` |
| `purged` | … / `evidence.purged` |
| `corrupt` | … / `evidence.corrupt` |
| `unavailable` | … / **`evidence.missing`** |

- Every refusal carries a valid StepTermination and failure envelope.
- **No published sentence or control names the `unavailable` mapping.** Existing controls cover `purged`
  and `expired` only.
- **The identity owner's own termination** for required retained evidence that cannot be supplied is
  `evidence.missing`, with remedy "…or report their unavailability". That supports the model's choice but
  does not publish it.

**Consumer reading.** Correct and conservative: it invented no detail.

**Recommended correction** (no new detail code, no model change):
- **Query §7 paragraph:** `purged`, `expired`, `corrupt` and `unavailable` refuse with HOST.IO_FAILURE (host-io)
  and, respectively, `evidence.purged`, `evidence.expired`, `evidence.corrupt` and `evidence.missing`. There
  is no `evidence.unavailable` member, and `retained` and `partial` do not refuse by themselves.
- **§7 table:** one row per refusing state.
- **Controls:**
  - `host-availability-unavailable-refuses-evidence-missing`;
  - `host-availability-corrupt-refuses-evidence-corrupt`;
  - `host-availability-partial-does-not-refuse-by-itself`.
- **Measured:** all pass on the rehearsal.

## 4. The recommended successor (one coherent patch)

**Patch** `successor-patch/successor-v23-gaps.v2.patch` in the completion runtime, sha256 `cd16d3ab…`:
- **Files.** 7 files, +232 / −14: `graph-query.schema.json`, `query-projection-contract.v3.md`,
  `query_projection_model.v3.py`, `check-query-projection.v3.py`, `native-evidence.md`,
  `native_evidence_model.v2.py` and `native-cases.v2.json`.
- **Supersedes** the v1 patch.

**Also owed outside the patch:**
- Re-seal the five pin ledgers. The rehearsal needed three passes because the ledgers pin each other, and pins
  were still sealed after every suite.
- Commit the regenerated `workflows-report.v1.json` and `native-evidence-report.v2.json`; both change.
- **A successor planning input layer.** `native-evidence.md` and `graph-query.schema.json` are pinned by
  `implementation-normative-inputs.v4.json`, `implementation-coverage.v1.json` and
  `implementation-planning-sources.v1.json`, so **layer4 cannot be retained**. On the rehearsal
  `check_implementation_planning` exits 1 with "Planning source changed: query". This is the expected
  consequence, not a patch defect; `check_repository_file_inventory` passes.
- A fresh review of the exact successor bytes.

**Rehearsal of the recommended patch** (disposable kit; frozen36 drift 0):

| Suite | Result |
|---|---|
| check-query-projection | exit 0, **131/131**, all 8 new controls pass |
| native | exit 0, **376/376**, new case passes, pins verified |
| foundation reference (includes check-identity) | exit 0, passed, pins valid |
| evaluator3 launcher | exit 0, **16/16** children, pins valid |
| integration | exit 0, 412 passed |
| security | exit 0 |
| workflows reference | exit 0, passed, pins valid |
| package13 13 Runs, `open_run_closure` + `close_run` | same outcomes as on frozen36 |
| planning: inventory / implementation-planning | 0 / **1** (owed planning layer, above) |

## 5. Does source36 acceptance reopen?

**Yes.** My source36 ACCEPT stated no new MUST or SHOULD. These three confirmed, consumer-visible defects in
published candidate36 law are SHOULD-level issues that review did not find. It therefore cannot stand as
final design acceptance of the affected surfaces.
- The record stays historical and unedited. It made no contrary claim about these surfaces.
- **No MUST is raised:** class, exit, errorCode, soundness and D9 vocabulary are unaffected.
- Design acceptance can be claimed again only after a successor that carries the patch, re-sealed pins,
  regenerated reports and a successor planning input layer, and a fresh review of its exact bytes.

**Carried unchanged:**
- TCB-SCOPE-01 as **one** shared assumption over **13** dependent rows: not closed, no qualification.
- **28** condition-2 obligations.
- **32** product gates, 0 performed; condition 5 **NOT MET**.
- **54** planned recovery cases, 0 executed.
- **30** residual proposals PENDING.
- The D9 obligation on DR-007 and DR-011-R08.
- No final application, architecture-readiness, activation or implementation authority.

## 6. Execution record

Interpreter for every command: `/tmp/opensip-architecture-review-env/bin/python -I -B`. Each command's receipt
records command, exit, stdout/stderr digests and start time.

- **Original runtime (v1):**
  - p01, p02 and p03 on frozen36;
  - **p04**, the first rehearsal. It applied the v1 patch; query 131/131 and native 376/376 passed; foundation
    **failed one** check (the fixture guard above). It was **stopped** during the evaluator3 launcher when the
    previous CLI process ended, and never wrote its summary.
  - **b01**, the original builder, executed on completion: **exit 1** on the missing p04 summary, receipt
    retained.
- **Completion runtime (v2):**
  - **s01**: p04 status from file metadata.
  - **s02**: bounded 11-minute poll concluding **p04 not active**.
  - **s03**: digest bearers of every changed file.
  - **s04**: retained-Run schema digests.
  - **p05**: variant A (the v1 schema edit strands package13) and variant B (the recommended patch, all suites).
  - **s05**: bounded wait.
  - **b02**: first run **exit 1** on my own mistaken S1 gate, then corrected.
  - **i01**: invariants.

## 7. Limits

- Source and reference assessment only. No product implementation, qualification or readiness.
- **Measurement basis.**
  - S1 and S3 were measured on the reference query model, S3 over the query checker's own synthetic admitted
    Run.
  - S2 was measured on the native reference helpers and the D9 artifact.
  - No retained product Run, blind reconstruction or consumer helper was used.
- Only V23-S1, V23-S2 and V23-S3 were assessed.
- The successor was rehearsed only in disposable copies. Root owns real re-sealing, regeneration, the
  planning layer and freezing.
- Choosing to preserve the §2 distinction (S1) is a normative judgement between two lawful corrections; the
  alternative is recorded.
- The helper-versus-full-D9 limitations above remain open.

**Additional observations (advisory):**
- The multi-vertex ENDPOINT_AMBIGUOUS clause is unreachable.
- An unregistered availability value (`not-a-state`) is silently ignored.
- `traverse_projected_graph` performs no endpoint syntax admission; it is a documented internal helper.

## 8. Probe errors and slips kept

- A progress message first called the captured report verdict ACCEPT before I read the field. It is
  CHANGES_REQUIRED, and no artifact relied on the slip.
- My v1 patch included the native schema annotation edit. The rehearsal exposed its fixture and retained-Run
  consequences, and the v2 patch supersedes it.
- p04 was stopped when the previous process ended, and b01 then failed on its missing summary. Both receipts
  are retained.
- b02 first expected ENDPOINT_AMBIGUOUS from a wrapper call without a Run. That call is correctly refused
  `QUERY.VIEW_UNKNOWN` after closed admission. The gate now asserts the measured values, and the refusal is
  proved by the real-Run control.
