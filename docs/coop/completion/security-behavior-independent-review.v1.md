# Independent security behavior review v1

**OBJECT — six model/evidence defects require correction.** The original external replay passed **1203/1203** (1198 authored cases and five local probes). That result does not resolve the counterexamples below. This review requests design-evidence repairs, not production qualification.

Reviewer: Codex `security_behavior_review`, independent of the eight subject files. The subject manifest SHA-256 is `d48a171ff132a18dae0c4a97d39d3c11bd38ac5eb9afdb936eb60a04bc0333b5`. Every declared pin matched before and after inspection. No subject bytes or register records were changed.

Exact subject hashes, source hashes, replay hash, complete probe inputs/results, and repairs are retained in [the review JSON](security-behavior-independent-review.v1.json).

## SBR-1 — Recovery closes cleanup without running retained inverses after completed reversible effects

A completed RCO suppresses the CRASH inverse branch, then CRASH appends CLN. Later CLEANUP sees cln=true and cannot run the retained inverse. The returned CLOSED claim is false even within the reference design model.

**Required repair:** Recover pending outcome records separately from generation cleanup. Before CLN, run every still-available reversible inverse including completed RCO requests; retain outcome history and explicitly record cleanup success or bound-exhaustion residual. Add completed-RCO/revocation/crash and death-mid-cleanup golden schedules.

Authority: `permission-truth-tables.v9 $.linearization.transitions L-3/L-7 and $.raceSemantics.races R-6`. Locations: `security-behavior-model.v1.py:49`, `security-behavior-model.v1.py:60`.

## SBR-2 — All 260 crash-prefix cases permit a vacuous empty journal and FX-7 never compares paired results

Each crash case expects only retryCount=0. The invariant loop omits durable-prefix preservation, terminal outcome for every recovered intent, and mandatory cleanup. An empty journal with no initiated effects passes all current crash assertions. Clock-perturbed cases only rerun those projections; they do not assert journal/decision equality to the baseline. Retaining actual results in a report is not an assertion.

**Required repair:** Independently author expected durable before/after journals and outcomes for each cut, or independently derive them from an explicit normative transition oracle separate from model code. Assert preserved durable prefix, intent terminalization, residual/cleanup obligations, and complete normalized output equality across clock/delay variants. Keep platform axes labeled as model axes.

Authority: `permission-truth-tables.v9 $.acceptanceEvidenceFixtureClasses.classes FX-4 and FX-7`. Locations: `security-behavior-author.v1.py:34`, `security-behavior-check.v1.py:25`.

## SBR-3 — OC-4 golden contradicts the no-check refusal rule; OC-4/OC-5 verification is circular

The shipped OC-4 golden contains a check result and passes; a zero-check OC-4 is rejected by both model and schema. The reader converts the asserted outcome into refused/fault inputs, so those outcomes authorize themselves regardless of independently observed invocation/report events.

**Required repair:** Allow the legal empty-check refusal branch and reject an OC-4 report containing executed-check results. In the reference execution model, derive refusal from a recorded pre-check invocation refusal and derive fault from independent report construction/required-consent-write/output-sink failure events. Require checksExecuted=0 for refusal. Do not infer those predicates from the claimed outcome. For a reader lacking those events, state the verification limit explicitly and verify all observable structural constraints; retain no-output OC-5 as an execution result rather than inventing an emitted report.

Authority: `doctor-contract.v4 $.outcomeStructure.outcomeClasses OC-4/OC-5 and $.outcomeStructure.derivationRule`. Locations: `security-behavior-author.v1.py:189`, `security-behavior-author.v1.py:220`, `security-behavior-model.v1.py:234`, `security-behavior-model.v1.py:245`.

## SBR-4 — Full doctor reports bypass host scope closure and schema validation is disconnected from reader acceptance

A full report with an extra member in the closed host consent scope passes both reader and schema. The standalone host validator checks closure but is never applied to embedded report consent records. The reader also accepts empty consent records and wrong environment types; the checker only uses schema failure as a side assertion when the expected projection says accepted, leaving the public accepted result inconsistent with the claimed full reader validation.

**Required repair:** Compose structural schema validation and doctor semantic checks in one acceptance path. Apply the closed host scope schema to every relevant embedded consent record while allowing additions only at doctor v4 extension positions. Exercise all required fields/types, closed nested additions, and legal optional additions through the complete report path. Malformed JSON values should return a refusal, not raise during unchecked iteration.

Authority: `doctor-contract.v4 $.stableMachineSchema and host-effect-authorization.v25 $.authorizationRecord.consentRecordsScopeShape`. Locations: `security-behavior-author.v1.py:188`, `security-behavior-model.v1.py:244`, `security-behavior-check.v1.py:18`.

## SBR-5 — Full host records can grant preview-excluded actions despite actor-level refusal cases

Changing full denied IN_PROCESS and CA-2 records to GRANTED with matching consent authorization/execution/outcome passes. Domain membership and projection equality do not establish that resolution is legal. The actor model rejects those same acts, but no composition connects it to full records.

**Required repair:** Derive the allowed resolution from explicit accepted contract/admission context, invocation consent, actual-versus-bound attempt, actor/class/subtype/platform, and exclusions; compare the record against that decision. The synthetic context may remain for model inspection but must enumerate its actual scope and cannot override preview exclusions. Add coherent forbidden-grant mutations across both authorization and consent projections, and retain valid denied attempted-act records.

Authority: `host-effect-authorization.v25 $.failClosed and $.authorizationRecord.closedMembers resolution; doctor-actor-join-integration-contract.v8 actor split`. Locations: `security-behavior-model.v1.py:192`, `security-behavior-model.v1.py:202`.

## SBR-6 — The claimed full host envelope validator accepts malformed endpoint domains and missing mandatory result

A CA-4 endpointSet object instead of an enumerated endpoint array passes when both projections match. Removing the required consent result member also passes. Similar checks cover selected fields, not the claimed complete envelope.

**Required repair:** Validate the complete consent record required member set and all authorization/scope field domains before equality checks. Require endpointSet array/null by action class, validate its entries, enforce class-specific nullability, and validate residual objects. Compose with SBR-4 so full report and pair validation agree; preserve lawful doctor optional additions.

Authority: `host-effect-authorization.v25 $.authorizationRecord.closedMembers endpointSet and $.authorizationRecord.doctorV4FieldMapping; doctor-contract.v4 $.consentModel.mandatoryPostReport`. Locations: `security-behavior-model.v1.py:190`, `security-behavior-model.v1.py:212`, `security-behavior-model.v1.py:217`.

## Scope and useful evidence

The authoring script never imports the reference model. Continuation truth-table expectations are separately expressed. The package honestly labels synthetic admissions, local-only ambient probes, modeled journal schedules, and crypto observations; those limits are not review defects.

The high-water, restore witness, redaction successor, obsolete BLK condition, and final structural-ceiling joins remain explicit integration work and were not converted into additional findings. Typed absences for in-host execution, replay, and repair remain absences.

SHOULD: cover the v25 legal differing-record-id cross-reference branch and legal additive members at evidence/environment/consent positions. The closed host scope must remain closed.

Replay: `/tmp/opensip-architecture-review-env/bin/python -B docs/coop/completion/security-behavior-check.v1.py --report /tmp/security-behavior-independent-report.v1.json`. Independent probe source is `/tmp/security-behavior-review-probes.v1.py`; complete inputs/results are embedded in the review JSON.

No automatic acceptance, SATISFIED status, or register disposition is asserted.
