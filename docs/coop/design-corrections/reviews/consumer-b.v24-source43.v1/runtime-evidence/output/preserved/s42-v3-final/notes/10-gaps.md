# Phase 10 — gaps, contradictions and readings under the source42 kit (runtimes source42.v1–v3)

This is my own adjudication for the source42 kit. The source41 version is preserved at `preserved/source41-v1/notes/10-gaps.md` and is history, not current evidence.

## Adjudication rules

- **Missing or contradictory law.**
  - MUST: a required record, identity or refusal cannot be determined from the kit, so two conforming hosts would disagree.
  - SHOULD: the kit determines the answer, but a normative sentence contradicts another one in a way a careful implementer could follow into a different result.
  - Advisory: wording, naming or scoping that does not change a determinate result, or an obligation the kit itself discloses.
- **Algorithm freedom is not a gap.** Where a published law fixes the result and leaves the algorithm open, the reconstruction's algorithm is a free choice and is not reported.
- **Helper bugs are not gaps.** A helper failure with a precise kit answer is corrected as a numbered HC with its original failure preserved (`tools/hc_source42.py`, HC-47..HC-53). This includes a defect in my own earlier exports and an omission in my own source42.v2 traces.
- **Evidence standard.**
  - Every item is checked against a source42 selector and, where it can be, measured by an executed vector or Run.
  - No author model, fixture, prior review or root artifact is an oracle.
  - Readings adopted where text is ambiguous are named with their measured alternative.

## MUST

None.

## SHOULD

None.

## Disposition of my own source41 results

| Result | Disposition | Selector | Measured |
|---|---|---|---|
| The 27 source41 claimed positives and their ACCEPT-RECONSTRUCTABLE recommendation | **Own helper defect found; superseded.** The exports carried `programEntry` `"tsconfig.json"` (ts-*, cmp-*) or `"Cargo.toml"` (rust-*) on `default-unit` bindings, and labelled the U-9 syntax default `explicit-plan-selection`. The published schema description refuses that shape, and my source41 enumeration admission omitted the law. This is not a design gap: the schema description has stated it since source41 and the source42 contract restates it. | `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry/description`; `enumeration-contract.v1.md` s1 lines 20-47 | `logs/s42-original.7.from_scratch.log` (unchanged helpers admit all 27; run ids identical to the source41 exports); `selfcheck/s42-prepost-matrix.json` (corrected code over those exact bytes); `runs/*~default-unit-program-entry` |
| Source41 execution-inputs view attribution (HC-42) | Tightened by the source42 text: candidate views come from complete receipts only, and a `selectedRefs` view on no receipt refuses `EXECUTION_INPUTS_SELECTED_COVER` (HC-48) | `execution-inputs-contract.v1.md` s3 line 53 | `runs/syntax-code~selected-view-not-on-receipt` |
| Source41 advisories A-c1, A-c2, A-c3, A-n1, A-n6, A-v2-1..3, A-s41-1, A-s41-2 | Carried; their owner documents are unchanged | as below | as below |
| My source42.v2 limitation "No Run negotiates target-attribution-v2 or FactBatchV3 occupancy companions; no claim is made about them" ("read but not exercised"), while R-TRACE-* stood executed | **Withdrawn as inaccurate (source42.v3, HC-53).** The charter's current incorporated correction owners make the negotiated payload selection, exact payload bytes and request/batch correlation part of the existing provider traces. The v2 traces carried frame names only, so they executed no payload law. The law is now executed in the traces and standalone vectors. Not a design gap. | charter.md line 248; native s9.1 lines 2785-2791 and s9.6 lines 2896-3018 | `traces/payload-vectors.json`; `traces/*.json#/traces/*/payloadResults`; `notes/11-provider-trace-payload-law.md` |

## Advisories

- **A-c1.** Internal refusal names that no kit owner publishes are still spelled `cb24.*`. The measured set emitted by `ref/*.py` is listed in `blind-review.json#/advisories`.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination; the successor D9 artifact is a disclosed live cross-unit obligation (native lines 3313-3327).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change (workflows s3 lines 440-449).
- **A-n1.** In the closed per-entry IndeterminateReason order, reason (3) is unreachable for entries (workflows s3 lines 402-411).
- **A-n6.** A rust unit's `languageMode` is decided by the mode table but not restated by U-4b.2 and not enforced by U-4b.5 (native lines 165-172, 741-746, 797-799, 1070-1072, 1842-1847).
- **A-v2-1.** Composition s7 does not scope typed-prefix closure to outputs explicitly (s7 line 74; s5 line 54; identity lines 597-600, 627-631).
- **A-v2-2.** `policy-derivation3` is outside the reachable output set (composition s7 lines 70, 76).
- **A-v2-3.** Identity s3 (lines 441-467) calls its digest vocabularies closed while the native and relation bundles publish their own.
- **A-s41-1.** run-termination s7.6 step 1 (line 330) names no key; the s6 key (line 173) is applied at both boundaries.
- **A-s41-2.** U-1's "an omitted value defaults to false" (native lines 656-659) reads against s1.2's `checkJs` fallback (lines 524-526, 562-563); s1.2 is applied.
- **A-s42-1 (new).** Enumeration contract s1 line 21 makes `provenance=default-unit` at most one binding per cell at `ordinal=0`. It names no refusal key, and the schema's `provenance` enum carries no such constraint. The reconstruction refuses with its own `cb24.ENUMERATION_DEFAULT_UNIT_CARDINALITY` (`runs/syntax-code~second-default-unit-binding`). A host using another internal key would refuse the same record.
- **A-s42-2 (new).**
  - Enumeration contract s1 names `ENUMERATION_BINDING_PROGRAM_ENTRY` for a non-null `default-unit` `programEntry` (lines 26, 37).
  - It does not name the key for a derived-entry mismatch or an explicit-entry mismatch against the retained `entryConfigPath`, which the schema description requires admission to compare.
  - Native U-0 (line 650) attributes a wrong root surfacing through that join to `ENUMERATION_BINDING_PROGRAM_ENTRY`, so that key is applied to all three (`runs/ts-pass~explicit-entry-not-graph-entry`).

- **A-s42-3 (new).** Enumeration contract s1 makes a syntax-only cell's default binding the one backed by the U-9 fallback unit (line 21) and reserves `explicit-plan-selection` for extra programs the Plan actually selected (line 22). No published rule or key refuses a sole syntax-only binding spelled `explicit-plan-selection` with `programEntry: null`, so the two spellings mint different `EnumerationPlanV1` digests and PlanIds for one selection.
  - **Why advisory.** The text decides it (default-unit), but nothing published enforces it, unlike the null rule for `programEntry`. That places it with A-n6, not with s39-M1: two hosts that follow line 21 agree.
  - **What the reconstruction does.** It builds `default-unit` (HC-47) and invents no refusal.
  - **Measured.** `selfcheck/s42-prepost-matrix.json`: the 4 original syntax positives (explicit spelling) and the rebuilt ones (default spelling) both ADMIT under the corrected code, with different identities.

- **A-s42v3-1 (new).** `typescript-semantic` major 2 is published only as deltas (native s9.4, lines 2879-2888) over the delivery.v2 major-1 wire, which s9.6 line 2912 retains for TS Analyze.
  - **FactBatch payload without the token.** s9.1 (lines 2785-2791) names it "historical FactBatchV2" for both majors, and the FactBatchV3 schema describes that payload as analysisOrdinal/stageId/batchIndex/candidates with no schemaVersion and no occupancyCompanions.
    - The only published FactBatchV2 closed list is rust-provider-protocol.v2 (line 411).
    - delivery.v2 still publishes the TypeScript FactBatch payload as FactBatchV1 `{facts, batchCommitment}` (lines 855, 874), and native s0's superseded-selector table (lines 114-116) does not list it.
  - **Hello schema.** No TypeScript major-2 Hello/HelloAck schema is published; HelloV3/HelloAckV3 fix `protocolMajor` 3 (native-evidence.schemas.v2.json line 4035).
  - **Why advisory.** The explicit current s9.1 sentence and the V3 schema determine the TypeScript unnegotiated payload; delivery.v2 FactBatchV1 is the major-1 payload (HelloAckV1 `protocolMajor` exactly 1). Two hosts following the current text agree.
  - **What the reconstruction does.** A TypeScript FactBatchV1-shaped payload refuses. TypeScript Hello payloads are admitted on the shared HelloV3 members with `protocolMajor` substituted, and major 2 is checked by the s9.1 text.
  - **Measured.** `traces/payload-vectors.json#SEL-ts-unnegotiated-delivery-v2-FactBatchV1-shape` refuses `cb24.FACT_BATCH_V2_SCHEMA`. Its member set equals delivery.v2 FactBatchV1's required list, so the alternative reading would admit it. See also `traces/controls.json#/helloSchemas` and the first-run failure `logs/s42v3-p3.1.phase3_traces.log`.

## Kit changes exercised, and what required invention

Law by law, the source42 deltas and their measured outcomes are in `notes/01-source42-law-deltas.md`. Nothing required inventing a record, identity or refusal outcome. Readings that needed a name, each with its alternative measured or stated:
- A-s42-1 (a key for the cardinality refusal);
- A-s42-2 (one key for all three entry joins);
- A-s42v3-1 (FactBatchV2 for TypeScript unnegotiated payloads; shared HelloV3 members for TypeScript Hello);
- the payload-law internal keys, each labelled `kit-text`, `key-name` or `cb24` in `traces/payload-vectors.json#/keyBindings`, and the reconstruction's own check order (no kit order exists; every check runs, so masked violations stay listed);
- A-s41-1, A-s41-2, A-v2-1, A-n6 (carried).
