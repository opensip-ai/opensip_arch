# Review request: B2C-PLAN-r2 (the lead's implementation plan for B2-c, the native unit instrument)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c-plan-r2/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run Cargo, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only reading, hashing, JSON parsing, Git queries and running the Python references read-only in a temporary directory are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2c-plan-r2-stage`
- **Subject file.** `subject.json`: 449 bytes, SHA-256 `e9f94322d9c1f8c59cc94f58734b981ad374512b63a4e3e78fca5ea5d2c72a42`, 1 member(s). Rehash every member.
- **Earlier round.** Your `codex-b2c-plan-r1` (REQUIRED-FINDINGS B2CPLAN-R1-RF-1 and RF-2, with NBO-1 and NBO-2) is at `/tmp/opensip-implementation/reviews/codex-b2c-plan-r1`. PLAN-r2 is r1 with those resolved; its "r2 changes" table maps each one.
- **Bases.**
  - Product `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5`, clean: inventory v200, 165 contract successors.
  - Architecture `ecd3c5a52a2faa10c91ac1ef96b62cde5a8152a0`: shared r99.

## Authority

- **Law M3-B r7** (`docs/implementation/m3/config-discovery-b/PROPOSAL-r7.md`): items 12 to 15, the unit table (line 971: B2-c), item 25's successor list and item 27's open questions.
- **NE** (`docs/v2/contracts/product-v1/native-evidence.md`): §1.2 (146-215), the `allowJs` derivation (527-545), §1.4 (619-948) and `TypeScriptConfigGraphV1` (1332-1360).
- **The B-S1 successor** (`config-discovery-b/b-s1/`): `AdmittedBoundaryInventoryV3`, and its PASSAGES for U-8.
- **The selected native reference** `config-discovery-b/b-s9/reference/native_evidence_model.py` (contract successor 81), and the native cases `docs/coop/design-corrections/native/native-cases.v2.json`.
- **The B2-a shared rule** (`b2-a-reference/reference/discovery-defaults.sx1-r1.py`, successor 163) and **the B2-b0 reference** (successor 164).
- **The public detail registry** `docs/coop/design-corrections/public-detail-registry.v1.json`, and the product's `schemas/sources/common-v4.schema.json` and generated vocabulary.
- **The bound B2-b units** and `crates/security/src/custody/discovery_rule.rs` (`pub(crate)`).
- **The B-S10 unit** (the product schema-source route).

## What to review

0. **Round 1.** Re-judge each finding.
   - **RF-1.** The withdrawn vocabulary gap, and the closed internal-to-public map pinned to the registry.
   - **RF-2.** `UnitDiscoveryV3` output in both the wrapper and the product, the member rules and the new current cases.
   - **NBO-1 and NBO-2.** The loading closure, the candidate order and grammar, and the dropped partial-settlement carrier.
1. **Scope.** Does the plan implement law item 14's B2-c scope: U-0 to U-9, the Config2 join, the scope descriptor, default selection, and the JSONC reader shared with C2? Does it claim nothing that belongs to C1, J1, B2-d or B3-b?
2. **The reference unit (B2-c0).** Is it needed, as the plan argues: the B-S9 copy's unloadable `DD` path, V1/V2-only boundary admission and the stale "must equal" wording? Is the wrapper approach (as B2-b0's) sound, with the model's bytes unedited and differences explained?
3. **The internal details (2.3).**
   - Is the closed map exactly the registry's alias rows?
   - Is reading `native.admitted-boundaries-required` as a lawfully absent `DomainDetail` under the alias rule correct?
4. **The `extends` law step (section 3).** Is the plan right that no current text fixes how an `extends` specifier resolves before the Plan? Is the recommendation sound and narrow enough? That covers the relative and package forms, data-only reads under C1's custody, refusal only when inheritance cannot settle `allowJs`, and the bounds. Is anything in it beyond what a law revision can decide?
5. **Design.**
   - The shared rule through a narrow `pub` API from security.
   - V3 as the only operational input, and the standalone lane test-only.
   - Cargo `[workspace]` through an identity function.
   - FW-01's structural check extended to `discovery.rs`.
   - The vectors over every `units-*` case and the sweeps.
   - The joint U-8 sweep through the scenario seam.
6. **Sequence and dependencies.** Can B2-c1 proceed with `allowJs` as an input while r8 is reviewed?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "e9f94322d9c1f8c59cc94f58734b981ad374512b63a4e3e78fca5ea5d2c72a42",
  "r1Rf1Resolved": true,
  "r1Rf2Resolved": true,
  "r1NbosAddressed": true,
  "implementsLawItem14Scope": true,
  "referenceUnitNeededAndSound": true,
  "v3InputAndOutput": true,
  "sharedRuleConsumedNotCopied": true,
  "internalAliasNormalizationSound": true,
  "extendsLawStepNeeded": true,
  "extendsRecommendationSound": true,
  "admittedBoundariesRequiredInternalSound": true,
  "fw01Covered": true,
  "sequenceSound": true,
  "codeWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
