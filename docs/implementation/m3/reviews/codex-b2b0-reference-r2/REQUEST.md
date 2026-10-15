# Review request: B2-B0-REFERENCE-r2 (the current discovery reference; contract successor 164)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b0-reference-r2/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing and Git queries are permitted. You may also run the staged checker:

```
python3 -I -B /tmp/opensip-implementation/b2b0-reference-r2-stage/docs/implementation/m3/config-discovery-b/b2-b-reference/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --reference /tmp/opensip-implementation/b2b0-reference-r2-stage/docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py --packages-root /Users/sb/code/opensip-ai/opensip --out <a path under /tmp/opensip-implementation/reviews/codex-b2b0-reference-r2>
```

Write its output only inside this review directory. You may also import the reference module read-only to try your own synthetic inputs.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b0-reference-r2-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b-reference-subject.json`: 1134 bytes, SHA-256 `b719004114567045dff9f6853397b49251b9ff4f12bc737e1c99d514a5cff63e`, 5 members. Rehash every member.
- **Record.** `docs/implementation/m3/config-discovery-b/b2-b-reference/successor.json`: 2908 bytes, `183d67fda32aa2a8c32af8555c19ffcce71b16a67ee1651604320dd33df83f2c`.
- **Bases.** Product `94e5fdebd63a174694dadbb5e647063855614b77` (clean; 163 contract successors, inventory v191). Architecture `3b2a55d48c442b66d188369a4d8a9307fdaeb14b`: the B2-b plan r4 is published there.
- **Round 1.** Your `codex-b2b0-reference-r1` (REQUIRED-FINDINGS: B2B0REF-1 and B2B0REF-2) is at `/tmp/opensip-implementation/reviews/codex-b2b0-reference-r1`. README's "r2 changes" section states the resolution.
- **Review support** (not subject members): `review-support/build_and_verify.py`, `verify-scratch.json`, `reproduce_b2b0ref1.py` and `reproduce_b2b0ref1.json`. The last shows both B2B0REF-1 reproductions leaking under the r1 reference and not under r2. These show the product's real `verify_design` passing on the base lock, and with this record appended as successor 164.

## Authority

- The accepted B2-b plan r4 (`docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`): section 1.0, LD-B2B-3, LD-B2B-5 and LD-B2B-8, and your NBO-1 on it (the depth control). See `docs/implementation/m3/reviews/codex-b2b-plan-r4/`.
- SLM `discovery` (`docs/coop/design-corrections/security/security_lifecycle_model_v1.py`).
- The cases (`security/discovery-cases.v1.json`).
- The bound B2-a reference (contract successor 163).
- B-S1's V3 additions and the SLS bundle.
- SL S3 (SL:146-168, SL:187-250).
- `verify_design.py` `contract_successor` in the product.

## What to review

0. **Round 1.**
   - **B2B0REF-1.** Is it resolved? Upward evidence must be only pass one's walked rows and the explicit path, not below the root. Pass two's `cwd` must be the root, with the upward fields from pass one, and nothing upward may enter the downward population. Can you still make a `cwd`, an `explicitResolved` or an `accountHome` leak?
   - **B2B0REF-2.** Is it resolved? Every exception must fail the checker, the exact coverage counts must hold, and the injected-fault negative control must fail.
1. **The rule swap.**
   - Does replacing SLM's `DD` global with the bound B2-a copy run SLM's algorithm with the corrected rule and SX-1?
   - Is SLM left unedited?
   - Is the historical mode separate?
2. **`walker_population`.** Does it implement plan r4's rules exactly?
   - The upward population.
   - Automatic, parent-first: pruning before boundaries; a pruned anchor is its own entry only; a boundary is a directory other than the root, entered with its `opensip.json` only; the 256-segment listing bound, with marker-name-only observation at 257 and nothing deeper.
   - Explicit and config, parent-first chains: chain `Cargo.toml` and `opensip.json`; a boundary stop; a pruned-prefix stop; the root's subtree under the automatic rule; nothing else.
   - Can you construct an input where the population includes a path the walker could not observe, or omits one it would observe?
3. **`current`.**
   - The two passes.
   - A refusal before `finish` standing as it is.
   - The root and source equality.
4. **V3.**
   - `project_v3` and the pending field.
   - `shape_fill` being shape-only and never emitted.
   - `boundary_inventory_v3`.
5. **The checker.**
   - The three-stage replay of the 64 discovery cases, with the 4 boundary-model cases listed.
   - The difference rule.
   - The two cases whose `vendor/lib` is removed by the explicit or config population.
   - The population property.
   - V3 validation of all 64 results and of 35 inventories.
   - The 26 controls, including NBO-1's 256, 257 and 258, and the r2 reproductions and negative control.
   - Do `checks.json`'s results agree with a rerun?
6. **The record.**
   - Parents are accepted bases or earlier successor candidates, sorted.
   - There are no overrides.
   - The candidates cover the subject.
   - It binds as successor 164.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "b719004114567045dff9f6853397b49251b9ff4f12bc737e1c99d514a5cff63e",
  "b2b0ref1Resolved": true,
  "b2b0ref2Resolved": true,
  "implementsPlanR4Section10": true,
  "slmUneditedAndRuleSwapSound": true,
  "walkerPopulationMatchesPlanR4": true,
  "pruningPrecedenceHeld": true,
  "parentFirstChainHeld": true,
  "depthPopulationSound": true,
  "twoPassRuleSound": true,
  "v3ProjectionAndPendingFieldSound": true,
  "shapeFillNeverEmitted": true,
  "boundaryInventoryComplete": true,
  "checkerSufficient": true,
  "caseDifferencesExplained": true,
  "bindsAsContractSuccessor164": true,
  "passageOverridesNone": true,
  "productCodeChanged": false,
  "productQualification": false
}
```

The lead then gives its own assent, publishes the architecture record, and makes the separate product lock commit binding successor 164. Nothing is pushed.
