# Review request: B2-A-REFERENCE-r1 (the B2-a reference refresh; contract successor 163)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2a-reference-r1/`).

## Boundaries

Do not edit either repository, the stage or the control files. Do not run Cargo, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing and Git queries are permitted. You may also run these read-only Python checks:
- the staged checker: `python3 -I -B /tmp/opensip-implementation/b2a-reference-r1-stage/docs/implementation/m3/config-discovery-b/b2-a-reference/evidence/check.py --architecture /Users/sb/code/opensip-ai/opensip_arch --candidate /tmp/opensip-implementation/b2a-reference-r1-stage/docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py --packages-root /Users/sb/code/opensip-ai/opensip --out <a path under /tmp/opensip-implementation/reviews/codex-b2a-reference-r1>`. Write its output only inside this review directory, and do not add it to the review files beyond citing it;
- importing the reference copies to spot-check a claim.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2a-reference-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-a-reference-subject.json`: 1345 bytes, SHA-256 `b38bac53199550302039bf08cd5f06a2dcbe2c9a4e0220830ac05bbc1b9f1e5d`, 6 members. Rehash every member.
- **Record.** `docs/implementation/m3/config-discovery-b/b2-a-reference/successor.json`: 3003 bytes, `43f1fbbf223153aab78c5920439922bfbe9da2085bccf00593744bceea932541`.
- **Bases.** Product `2191674d873ed7c0eb4459683dcc29cf7da42440` (clean; 162 contract successors, inventory v190). Architecture `ccb8b07cc43ba5debc77c600b1f77e06611cf47b`: the B2-a plan r1 is published there.
- **Review support** (not subject members): `review-support/build_and_verify.py` and `verify-scratch.json`. These show the product's real `verify_design` passing on the base lock and with this record appended as successor 163, using synthetic review and assent served in memory.

## Authority

- The accepted B2-a plan r1 (`docs/implementation/m3/config-discovery-b/b2-a/PLAN-r1.md`), section 1.1 and LD-B2A-1, and your plan review's NBO-1 (`docs/implementation/m3/reviews/codex-b2a-plan-r1/`).
- B-S1: SX-1, LD-3, LD-4, LD-14 and BS1-F3; its passages (SL:195, SL:205; NE:714, NE:719, NE:730-731, NE:939-940); and its SLS fragment `b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json`.
- The accepted pruning correction r2 (`discovery-pruning-reference-r2/`, contract successor 124) and its copy.
- DD (`docs/coop/design-corrections/discovery-defaults.py`).
- `tools/verify_design.py` `contract_successor` in the product.

## What to review

1. **The copy.** Is `discovery-defaults.sx1-r1.py` exactly the pruning copy plus the changes in README's table?
   - Check with `author.py`'s asserted replacements and the AST comparison.
   - Is each change what its cited text requires?
   - Is `_custody_state` exact: only `""` and member roots, the outermost anchor, and exact bytes?
   - Does `classify_path` keep the pruning correction's outermost-across-all-reasons rule, now with SX-1?
2. **The V3 converter.**
   - Members are relative, UTF-8 sorted, and not boundaries or prefixes.
   - V1 and V2 refuse at conversion, under DD's two-lane rule.
   - The output validates against B-S1's `AdmittedBoundaryInventoryV3`.
3. **NBO-1.** `PRUNED_TREE_ROW_VERSION` moves to 3, and the checker asserts it.
4. **The checker.**
   - Are the 49 pruning controls unchanged on both copies?
   - Are the 21 SX-1 and 7 V3 controls sufficient, and is the AST confinement correct?
   - Do `checks.json`'s results agree with a rerun?
5. **The record.**
   - Parents are accepted bases, earlier successor candidates or the selected inventory, sorted.
   - There are no passage overrides.
   - The candidates cover the subject exactly.
   - DD and the pruning copy are untouched.
   - Is binding it as contract successor 163 right?
6. **Scope.** No product code, no SLM or native-model refresh, no schema change and no qualification.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-DESIGN-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "b38bac53199550302039bf08cd5f06a2dcbe2c9a4e0220830ac05bbc1b9f1e5d",
  "implementsPlanR1Section11": true,
  "discharges_BS1F3_LD14": true,
  "layeredOnPruningCopyUnchanged": true,
  "sx1AnchorExactAndOutermost": true,
  "v3ConverterMatchesSlsFragment": true,
  "versionMovesRight": true,
  "nbo1Applied": true,
  "checkerSufficient": true,
  "astDiffConfined": true,
  "ddAndPruningCopyUntouched": true,
  "bindsAsContractSuccessor163": true,
  "passageOverridesNone": true,
  "productCodeChanged": false,
  "productQualification": false
}
```

The lead then gives its own assent, publishes the architecture record, and makes the separate product lock commit binding successor 163 with fresh verify_design. Nothing is pushed.
