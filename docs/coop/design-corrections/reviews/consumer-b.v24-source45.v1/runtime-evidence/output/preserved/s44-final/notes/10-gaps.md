# Phase 10 — gaps, contradictions and readings under the source44 kit (runtime source44.v1; source43.v1 and source42.v1–v3 history)

This is my own adjudication for the source44 kit.
- **Scope of the change.** The source44 kit differs from source43 only in provider wire, startup and attribution owners (`notes/13-source44-provider-wire.md`). Every other item below was adjudicated on owners that are byte-identical to source43.
- **History.** The source43 version of this note is preserved at `preserved/s43-final/notes/10-gaps.md`; the source41 version at `preserved/source41-v1/notes/10-gaps.md`. Both are history, not current evidence.

## Adjudication rules

- **Missing or contradictory law.**
  - MUST: a required record, identity or refusal cannot be determined from the kit, so two conforming hosts would disagree.
  - SHOULD: the kit determines the answer, but a normative sentence contradicts another one in a way a careful implementer could follow into a different result.
  - Advisory: wording, naming or scoping that does not change a determinate result, or an obligation the kit itself discloses.
- **Algorithm freedom is not a gap.** Where a published law fixes the result and leaves the algorithm open, the reconstruction's algorithm is a free choice and is not reported. Committed record bytes are never algorithm freedom.
- **Helper bugs are not gaps.** A helper failure with a precise kit answer is corrected as a numbered HC, with its original failure preserved:
  - `tools/hc_source42.py`: HC-47..HC-53;
  - `tools/hc_source43.py`: HC-54..HC-55;
  - `tools/hc_source44.py`: HC-56..HC-58.
- **Evidence standard.**
  - Every item is checked against a current selector and, where it can be, measured by an executed vector or Run.
  - No author model, fixture, prior review or root artifact is an oracle.
  - Readings adopted where text is ambiguous are named with their measured alternative.

## MUST

- **M-s44-1. The pre-Analyze Unavailable host conversion leaves the committed closedWorld undetermined.**
  - **Law.** Native §9.7 (lines 3234–3249) and `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion` fix every member of the host-minted CoverageResultV3 except `closedWorld`. They give it as `closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown)`, a function no kit owner publishes; a kit-wide search finds the name only at those two places.
  - **What the text decides.**
    - §4.5 (lines 2208–2242) decides only `exportsClosed=closed` (every ingredient) and `deadCodeRepairEligible`.
    - The text determines `entryPointsRecognized none`, `nonliteralLoading none`, `externalConsumers unknown` and `deadCodeRepairEligible false`.
    - FR-3 (line 2771) and line 2226 support `exportsClosed unknown`.
  - **What stays open.** `dynamicDispatch` (resolved or not-applicable) and `reasons` (free strings, no vocabulary).
  - **Consequence.** These are committed `coverage2` bytes, so two conforming hosts mint different identities for the same clean terminal.
  - **Measured.** `traces/startup-vectors.json#/conversion`:
    - four candidates admit for both languages under schema, RC-1/RC-2/RC-6, the cause registry and §4.5;
    - every requested key gets four distinct `coverage2` identities;
    - the `exportsClosed closed` and `deadCodeRepairEligible true` controls refuse.
  - **Not decisive.** The workflows five-field display sentinel (lines 957–960) is a RepairPlanDescriptor display reduction, not a producer record, and it says `nonliteralLoading present`. The atom-evaluation ranking (lines 342–346) orders whole records.
  - **What the reconstruction does.** It applies reading A (`unknown`, `not-applicable`, `[]`) in the traces and labels it.
  - **Required change.** Publish closed_world_v2's result for this input, or the minted closedWorld value itself.

## SHOULD

None.

## Disposition of my own earlier results

| Result | Disposition | Selector | Measured |
|---|---|---|---|
| The 27 source41 claimed positives and their ACCEPT-RECONSTRUCTABLE recommendation | **Own helper defect found; superseded (source42, HC-47).** The exports carried non-null `programEntry` on `default-unit` bindings, which the published schema description refuses, and my source41 enumeration admission omitted that law. | `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description`; `enumeration-contract.v1.md` s1 | `logs/s42-original.7.from_scratch.log`; `selfcheck/s42-prepost-matrix.json` |
| Source41 execution-inputs view attribution (HC-42) | Tightened by the source42 text (HC-48) | `execution-inputs-contract.v1.md` s3 line 53 | `runs/syntax-code~selected-view-not-on-receipt` |
| My source42.v2 "read but not exercised" provider-trace limitation while R-TRACE-* stood executed | **Withdrawn as inaccurate (source42.v3, HC-53)** | charter.md line 248 | `notes/11-provider-trace-payload-law.md` |
| My source42.v3 R-GRAPH-QUERY standing (53 vectors) | **Superseded (source43.v1, HC-54)** | `query-projection-contract.v3.md` s2, s4, s7 | `vectors/graph-query.json#/source43ReAudit` (re-executed fresh in source44: 66 vectors, 0 failures) |
| My source43.v1 advisory A-s42v3-1 (TypeScript unnegotiated payload read as FactBatchV2; TypeScript Hello admitted on HelloV3 with `protocolMajor` substituted) | **Withdrawn (source44.v1).** The current owners publish the TypeScript historical payload (delivery.v2 FactBatchV1 with `batchCommitment`) and TypeScriptHelloV2/HelloAckV2. The helper is corrected (HC-57, HC-58). This is not a gap in the current kit. | native §9.1, §9.4; `fact-batch.schema.v3.json#/x-opensip-negotiation/whenAbsent`; `provider-handshake.schemas.v1.json` | `traces/payload-vectors.json#SEL-ts-unnegotiated-v1`, `#SEL-ts-unnegotiated-v2`; `logs/s44-original.0` |
| My source43.v1 R-TRACE-* standing (TypeScript on the protocol3 table; frame-name-only startup, coverage, terminal and cancel events) | **Superseded under the source44 owners (HC-58).** The unchanged helper exits 0 on the source44 kit and detects none of the new law. Corrected traces change three conclusions: a TypeScript Unavailable after output faults T2-23; a TypeScript ProviderFault faults; Rust modes are derived. | `typescript-protocol2-order.v1.json`; `protocol3-transitions.v1.json#/derivedObservations`; `provider-startup.schemas.v1.json`; native §9.7 | `preserved/s44-original/traces/`; `traces/*.json`; `logs/s44-p3.2` |

## Advisories

- **A-c1.** Internal refusal names that no kit owner publishes are still spelled `cb24.*`. The measured set emitted by `ref/*.py` is listed in `blind-review.json#/advisories`.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination; the successor D9 artifact is a disclosed live cross-unit obligation.
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5.
- **A-v2-1.** Composition s7 does not scope typed-prefix closure to outputs explicitly.
- **A-v2-2.** `policy-derivation3` is outside the reachable output set.
- **A-v2-3.** Identity s3 calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** Run-termination s7.6 step 1 names no key; the s6 key is applied at both boundaries.
- **A-s41-2.** U-1's "an omitted value defaults to false" reads against s1.2's `checkJs` fallback; s1.2 is applied.
- **A-s42-1.** Enumeration s1 `default-unit` cardinality names no refusal key; the reconstruction uses `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY`.
- **A-s42-2.** One key, `ENUMERATION_BINDING_PROGRAM_ENTRY`, is applied to all three entry joins. The native U-0 reference moved from line 650 to line 661 in source44 (prose shift only).
- **A-s42-3.** No published rule refuses a sole syntax-only binding spelled `explicit-plan-selection`; the reconstruction builds `default-unit`.
- **A-s43-1.** The graph response context availability when no observation is supplied is not stated (reference-harness case only).
- **A-s44-1 (new).** The return law's summary sentences say "historical FactBatchV2" for any token-absent worker:
  - `x-opensip-return-law/standing` (line 65);
  - `boundary.compilerWorkerTransport` (line 67);
  - `missingAndIncomplete.missingToken` (line 117).

  Everything else is per language (`typescript-semantic` FactBatchV1): the same document's per-mode worker rows (lines 138, 149), native §9.1 (lines 2801–2810), §9.2 (line 2883), §9.6 (lines 3065–3067), fact-batch v3 whenAbsent, occupancy-companion `x-opensip-wire` and the handshake wire law.
  - **Why advisory, not SHOULD.** The return law owns host capture, and its result is language-independent (token absent: no companion capture, occupancy unknown except exact-id ephemeral). Payload selection has explicit per-language owners, so two hosts following those owners agree.
  - **Measured.** `SEL-ts-unnegotiated-v1` ADMIT; `SEL-ts-unnegotiated-v2` REFUSE `cb24.FACT_BATCH_V1_SCHEMA`.
- **A-s44-2 (new).** `native/source-pins.v2.json` is cited as the pin authority (wire law `expectedProtocolContractSha256.rule` line 64; native §0 table header line 112; §12 line 4069) but is not a member of the frozen subject.
  - **Why advisory.** The wire law states the pinned digest, and it equals the raw SHA-256 of `rust-provider-protocol.v2.json`.
  - **Measured.** `traces/startup-vectors.json#/wireControls`; first-run control `logs/s44-p3.1`.

## Kit changes exercised, and what required invention

- **Source44 deltas.** Exercised law by law in `notes/13-source44-provider-wire.md`: per-language historical payload and batch commitment; both machines; handshake, startup, coverage, terminal and cancellation payloads; derived modes; host conversion.
- **Earlier deltas.** `notes/01-source42-law-deltas.md` (source42) and `notes/12-source43-query-contract.md` (source43).
- **Invention.** Nothing required inventing a record or refusal outcome, except that the conversion `closedWorld` value cannot be determined. That is reported as M-s44-1 with every lawful candidate measured, not invented.
- **Readings that needed a name, each with its alternative measured or stated:**
  - closedWorld reading A (M-s44-1);
  - the handshake/startup internal keys `cb24.*` (A-c1) and the reconstruction's own check order;
  - Rust `CancelledV2.observedPhase` not validated (no published worker phase vocabulary);
  - the fixture Plan and synthetic trusted descriptors (§9.7 reference scope);
  - A-s42-1, A-s42-2, A-s43-1, A-s41-1, A-s41-2, A-v2-1, A-n6 (carried).
