# Review request: B2-B0-REFERENCE-r3 (the current discovery reference; contract successor 164)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b0-reference-r3/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing and Git queries are permitted. You may also run the staged checker:

```
python3 -I -B /tmp/opensip-implementation/b2b0-reference-r3-stage/docs/implementation/m3/config-discovery-b/b2-b-reference/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --reference /tmp/opensip-implementation/b2b0-reference-r3-stage/docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py --packages-root /Users/sb/code/opensip-ai/opensip --out <a path under /tmp/opensip-implementation/reviews/codex-b2b0-reference-r3>
```

Write its output only inside this review directory. You may also import the reference module read-only to try your own synthetic inputs.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b0-reference-r3-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b-reference-subject.json`: 1134 bytes, SHA-256 `bf2168eb694311f587d4a0ee23dddaa52d7089a409fec820ca0baad68f2ba40f`, 5 members. Rehash every member.
- **Record.** `docs/implementation/m3/config-discovery-b/b2-b-reference/successor.json`: 2964 bytes, `45008a6c43bad96b7d882aec778f605b2acbc3cd2c9c94e824b497a0b3b16660`.
- **Bases.** Product `94e5fdebd63a174694dadbb5e647063855614b77` (clean; 163 contract successors, inventory v191). Architecture `3b2a55d48c442b66d188369a4d8a9307fdaeb14b`: the B2-b plan r4 is published there.
- **Earlier rounds.** Your `codex-b2b0-reference-r1` (`/tmp/opensip-implementation/reviews/codex-b2b0-reference-r1`) raised B2B0REF-1 and B2B0REF-2. Your `codex-b2b0-reference-r2` (`/tmp/opensip-implementation/reviews/codex-b2b0-reference-r2`) found those resolved and raised B2B0REF-3 and B2B0REF-4. README's "r3 changes" section states their resolution.
- **Review support** (not subject members): `review-support/build_and_verify.py`, `verify-scratch.json`, `reproduce_b2b0ref1.*` and `reproduce_b2b0ref3_4.*`. The latter shows both of your r2 reproductions under the r2 reference and neither under r3. These show the product's real `verify_design` passing on the base lock, and with this record appended as successor 164.

## Authority

- The accepted B2-b plan r4 (`docs/implementation/m3/config-discovery-b/b2-b/PLAN-r4.md`): section 1.0, LD-B2B-3, LD-B2B-5 and LD-B2B-8, and your NBO-1 on it (the depth control). See `docs/implementation/m3/reviews/codex-b2b-plan-r4/`.
- SLM `discovery` (`docs/coop/design-corrections/security/security_lifecycle_model_v1.py`).
- The cases (`security/discovery-cases.v1.json`).
- The bound B2-a reference (contract successor 163).
- B-S1's V3 additions and the SLS bundle.
- SL S3 (SL:146-168, SL:187-250).
- `verify_design.py` `contract_successor` in the product.

## What to review

0. **Earlier rounds.**
   - **B2B0REF-3.** Is it resolved? Every entry must carry only observed evidence: `vcs` stays only on probed directories (the root, listed, probed boundaries, chain), and a pruned anchor keeps its own fields only. Are the four-reason controls with `vcs` and a hidden `.git` sufficient? Can any other annotation carry unobserved evidence?
   - **B2B0REF-4.** Is it resolved? The depth policy must come before boundary evidence, so a 257-segment directory is never probed for `opensip.json` or `vcs`. Do the config and VCS controls at 256, 257 and 258 assert exact populations?
   - Do B2B0REF-1 and B2B0REF-2 stay resolved?
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
   - The 36 controls, including NBO-1's 256, 257 and 258, the r2 reproductions and negative control, and the r3 evidence and depth controls.
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
  "subjectManifestSha256": "bf2168eb694311f587d4a0ee23dddaa52d7089a409fec820ca0baad68f2ba40f",
  "b2b0ref1To2StayResolved": true,
  "b2b0ref3Resolved": true,
  "b2b0ref4Resolved": true,
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
