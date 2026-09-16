# Phase 10 — gaps, contradictions and readings under the source45 kit (runtime source45.v1; source44.v1, source43.v1 and source42.v1–v3 history)

This is my own adjudication for the source45 kit.
- **Scope of the change.** The source45 kit differs from source44 in three members: `native-evidence.md`, `native/provider-startup.schemas.v1.json` and `foundation/provider-target-attribution-return.schema.v2.json` (`notes/14-source45-closed-world.md`). Every other item below was adjudicated on owners that are byte-identical to source44.
- **History.** The source44 version of this note is preserved at `preserved/s44-final/notes/10-gaps.md`; earlier versions are preserved under `preserved/`. All are history, not current evidence.

## Adjudication rules

- **Missing or contradictory law.**
  - MUST: a required record, identity or refusal cannot be determined from the kit, so two conforming hosts would disagree.
  - SHOULD: the kit determines the answer, but a normative sentence contradicts another one in a way a careful implementer could follow into a different result.
  - Advisory: wording, naming or scoping that does not change a determinate result, or an obligation the kit itself discloses.
- **Algorithm freedom is not a gap.** Where a published law fixes the result and leaves the algorithm open, the reconstruction's algorithm is a free choice and is not reported. Committed record bytes are never algorithm freedom.
- **Helper bugs are not gaps.** A helper failure with a precise kit answer is corrected as a numbered HC, with its original failure preserved:
  - `tools/hc_source42.py`: HC-47..HC-53;
  - `tools/hc_source43.py`: HC-54..HC-55;
  - `tools/hc_source44.py`: HC-56..HC-58;
  - `tools/hc_source45.py`: HC-59..HC-60.
- **Evidence standard.**
  - Every item is checked against a current selector and, where it can be, measured by an executed vector or Run.
  - No author model, fixture, prior review or root artifact is an oracle.
  - Readings adopted where text is ambiguous are named with their measured alternative.

## MUST

None. The source44 MUST M-s44-1 is resolved by the source45 bytes (below).

## SHOULD

None.

## Why the arrays are empty

Every acceptBlocking item is executed. The only design finding my source44 review raised as blocking was M-s44-1, the undetermined host-conversion `closedWorld`.
- **The kit now publishes it.** The value appears in native §9.7 (lines 3241–3261) and in `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld` (lines 59–69), and `hostConversion` (line 58) references it.
- **Measured** (`traces/startup-vectors.json#/conversion`):
  - the two owners agree, and the value admits as ClosedWorldV2;
  - the conversion mints admitted entries with stable `coverage2` identities in both languages;
  - each of my four source44 candidates now refuses `cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED`.
- **Other changed text.** The return-law change states the historical payload per language (resolving A-s44-1) and changes no key, route or join my helpers read; the payload vectors re-execute with 0 failures.
- **Search for new findings.** I re-read every selector my helpers and issues cite in the three changed members. I found no new missing, ambiguous or contradictory required law. The one residual is an editorial duplicated word (A-s45-1).

## Disposition of my own earlier results

| Result | Disposition | Selector | Measured |
|---|---|---|---|
| The 27 source41 claimed positives and their ACCEPT-RECONSTRUCTABLE recommendation | **Own helper defect found; superseded (source42, HC-47).** | `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description` | `logs/s42-original.7.from_scratch.log`; `selfcheck/s42-prepost-matrix.json` |
| Source41 execution-inputs view attribution (HC-42) | Tightened by the source42 text (HC-48) | `execution-inputs-contract.v1.md` s3 line 53 | `runs/syntax-code~selected-view-not-on-receipt` |
| My source42.v2 "read but not exercised" provider-trace limitation | **Withdrawn as inaccurate (source42.v3, HC-53)** | charter.md line 248 | `notes/11-provider-trace-payload-law.md` |
| My source42.v3 R-GRAPH-QUERY standing | **Superseded (source43.v1, HC-54)** | `query-projection-contract.v3.md` s2, s4, s7 | `vectors/graph-query.json#/source43ReAudit` (re-executed fresh in source45) |
| My source43.v1 advisory A-s42v3-1 and R-TRACE-* standing | **Withdrawn / superseded (source44.v1, HC-57, HC-58)** | native §9.1, §9.4, §9.7; `typescript-protocol2-order.v1.json` | `preserved/s44-original/traces/` |
| My source44.v1 MUST M-s44-1 (host-conversion `closedWorld` undetermined) | **Resolved by the source45 bytes.** One complete value is published for both languages: `exportsClosed unknown`, `entryPointsRecognized none`, `nonliteralLoading none`, `externalConsumers unknown`, `dynamicDispatch not-applicable`, `reasons ["no-manifest"]`, `deadCodeRepairEligible false`. It keeps every member my source44 reading found determined and settles the two open ones. My source44 reading A differs only in `reasons`. Helper corrected (HC-60). | native §9.7 lines 3241–3261; `provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion`, `hostConversionClosedWorld` | `traces/startup-vectors.json#/conversion`; `logs/s45-p3.1`; unchanged helper `logs/s45-original.1/.2` |
| My source44.v1 advisory A-s44-1 (return-law summary sentences said FactBatchV2 for any worker) | **Resolved by the source45 bytes.** Lines 65, 67 and 117 now name delivery.v2 FactBatchV1 for `typescript-semantic` and rust-provider-protocol.v2 FactBatchV2 for `rust-semantic`. | `provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/standing`, `boundary/compilerWorkerTransport`, `missingAndIncomplete/missingToken` | `traces/payload-vectors.json` (`logs/s45-p3.0`) |
| My source44.v1 report "251 of 473 retained result files are byte-identical" | **Own reporting error, corrected from retained files.** 251 is the identical count within the 347-file determinism subset. The 473-file comparison has 370 identical and 103 differing (89 process-id-bearing, 10 expected content, 4 edited helper sources). The source44 report bytes are preserved unchanged. | `preserved/s44-final/blind-review.md`; `preserved/s44-final/notes/13-source44-provider-wire.md` | `selfcheck/s45-s44-arithmetic-reconciliation.json` |

## Advisories

- **A-c1.** Internal refusal names that no kit owner publishes are still spelled `cb24.*`. The measured set is listed in `blind-review.json#/advisories`.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination; the successor D9 artifact is a disclosed live cross-unit obligation (native lines 3584–3619; source44: 3565–3600).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5.
- **A-v2-1.** Composition s7 does not scope typed-prefix closure to outputs explicitly.
- **A-v2-2.** `policy-derivation3` is outside the reachable output set.
- **A-v2-3.** Identity s3 calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** Run-termination s7.6 step 1 names no key; the s6 key is applied at both boundaries.
- **A-s41-2.** U-1's "an omitted value defaults to false" reads against s1.2's `checkJs` fallback; s1.2 is applied.
- **A-s42-1.** Enumeration s1 `default-unit` cardinality names no refusal key; the reconstruction uses `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY`.
- **A-s42-2.** One key, `ENUMERATION_BINDING_PROGRAM_ENTRY`, is applied to all three entry joins (native line 661).
- **A-s42-3.** No published rule refuses a sole syntax-only binding spelled `explicit-plan-selection`; the reconstruction builds `default-unit`.
- **A-s43-1.** The graph response context availability when no observation is supplied is not stated (reference-harness case only).
- **A-s44-2.** `native/source-pins.v2.json` is cited as the pin authority (wire law line 64; native line 112 and line 4088) but is still not a subject member. The Hello digest stays determined by the wire law.
- **A-s45-1 (new, editorial).** `provider-target-attribution-return.schema.v2.json#/x-opensip-return-law/missingAndIncomplete/missingToken` (line 117) begins "Historical the historical per-language payload (...)". The duplicated word does not change the per-language rule it states.

## Kit changes exercised, and what required invention

- **Source45 deltas.** Exercised in `notes/14-source45-closed-world.md`: the published conversion `closedWorld`, owner agreement, entry admission and identity stability, and refusal of every earlier candidate. The per-language return-law wording is re-read and the payload vectors re-executed.
- **Earlier deltas.** `notes/13-source44-provider-wire.md`, `notes/12-source43-query-contract.md`, `notes/01-source42-law-deltas.md`.
- **Invention.** Nothing required inventing a record, identity or refusal outcome.
- **Readings that needed a name, each with its alternative measured or stated:**
  - the handshake/startup internal keys `cb24.*` (A-c1) and the reconstruction's own check order;
  - Rust `CancelledV2.observedPhase` not validated (no published worker phase vocabulary);
  - the fixture Plan and synthetic trusted descriptors (§9.7 reference scope);
  - A-s42-1, A-s42-2, A-s43-1, A-s41-1, A-s41-2, A-v2-1, A-n6 (carried).
