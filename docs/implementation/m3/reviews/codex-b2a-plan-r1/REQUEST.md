# Review request: B2A-PLAN-r1 (the lead's implementation plan for M3-B unit B2-a, the shared discovery rule)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2a-plan-r1/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate. Read-only reading, hashing, JSON parsing and Git queries are permitted. You may import the architecture's Python reference copies read-only to check a claim; write nothing.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2a-plan-r1-stage`
- **Subject file.** `subject.json`: 449 bytes, SHA-256 `50d137171573405a6f99bb8b27b928c42f5fdfd9e13ad01f6597d6a3b062c113`, 1 member(s). Rehash every member.
- **Bases.** Product `2191674d873ed7c0eb4459683dcc29cf7da42440` (clean: B1-a, B1-b and B3-a are bound, inventory v190, 162 contract successors), architecture `bf4a42f8736feede1b487e7d79c6bc065eff14cd`.
- **Authority.**
  - M3-B r5 (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`): items 13 and 14, the B2-a row of "Units after the law", and "Controls the bound design units add".
  - B-S1 (`config-discovery-b/b-s1/`): SX-1, LD-3, LD-4, LD-14, BS1-F3, the passages and "Controls owed by the implementing units".
  - NE §1.4 U-4a (NE:703-743) as B-S1 overrides it, and NE:939-940.
  - SL S3 (SL:187-250), as B-S1 overrides it.
  - The accepted discovery pruning reference correction r2 (`config-discovery-b/discovery-pruning-reference-r2/`), contract successor 124 in the product lock.
  - `docs/coop/design-corrections/discovery-defaults.py` (DD).
  - The product's `crates/host/src/configuration.rs` (`logical_path`), the inventory v190, and `design-lock.json`.

## What to review

The plan fixes how B2-a is built before any reference or code exists. Judge:
1. **Scope.** Does it match MB items 13 and 14 (U-4a), the B2-a row (the shared rule as DD's entry points, SX-1, and the DD refresh for SX-1 and D15's `memberRepositories`), and B-S1's B2-a controls?
2. **Facts.** Are section 0's facts accurate at the product base? That includes the absent path not being an inventory row, the generated V1-only types, B1-a's trailing-slash refusal, and the reference state.
3. **The reference refresh (1.1).**
   - Is a separate copy layered on the corrected pruning copy the right way to discharge BS1-F3 and LD-14?
   - Are the version moves right: DD 3, provenance and boundary inventory 3, and V2 refused at conversion?
   - Is the checker sufficient?
   - Is binding it as contract successor 163 right?
4. **The product rule (1.2).**
   - Does each function mirror the corrected reference plus SX-1?
   - Is `classify_entry` the right shape for the walker's never-open decision?
   - Are the typed outputs, and the deferral of every public row to B2-b, sound?
5. **The lead decisions.**
   - LD-B2A-1: a separate design unit before code.
   - LD-B2A-2: the provenance and boundary records stay B2-b's.
   - LD-B2A-3: no export until B2-c.
   - LD-B2A-4: entry-type independent, with a directory-only row.
   - LD-B2A-5: the CI-trace control is split between B2-a's disposition and B2-b's trace.
   - LD-B2A-6: exact bytes, with no case folding.
6. **Section 3's controls.** Are the vectors, SX-1 cases, properties, purity and mutations sufficient?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "50d137171573405a6f99bb8b27b928c42f5fdfd9e13ad01f6597d6a3b062c113",
  "scopeMatchesMBItems13And14AndB2aRow": true,
  "factsSection0Accurate": true,
  "referenceRefreshSoundAndOwedByBS1F3": true,
  "ruleMirrorsCorrectedReferencePlusSx1": true,
  "sx1AnchorExact": true,
  "ldB2A1Sound": true,
  "ldB2A2Sound": true,
  "ldB2A3Sound": true,
  "ldB2A4Sound": true,
  "ldB2A5Sound": true,
  "ldB2A6Sound": true,
  "controlsSufficient": true,
  "codeWritten": false,
  "referenceWritten": false,
  "bindingMade": false,
  "lawChanged": false,
  "productQualification": false
}
```
