# Review request: M3-B-r8 (law: item 14a, the pre-Plan TypeScript configuration graph and effective allowJs)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-m3b-r8-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run Cargo, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- Read-only reading, hashing, JSON parsing and Git queries are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/m3b-r8-stage`
- **Subject file.** `subject.json`: 440 bytes, SHA-256 `108f1b2db8fedc45612733ba2c7e9911298a2835a2ef173658be1908d3e770b2`, 1 member(s). Rehash every member.
- **The candidate.** `PROPOSAL-r8.md` is the live law (`docs/implementation/m3/config-discovery-b/PROPOSAL.md`, r7 as you accepted it in `codex-m3b-r7-r1`) with one addition: item 14a, its successor row S10 in item 25, its "r8 changes" section and one "Not claimed" line. Diff it against the live `PROPOSAL.md` yourself.
- **Bases.**
  - Product `01c73e2d54e037e3e41adc2f5d97df854552921e`, clean: B2-c0 and B2-c1 are bound; 166 contract successors; inventory v201.
  - Architecture `c7108e3f066a0a5d306e7e080a9790fc40f3e32d`: shared r100.

## Authority

- The accepted B2-c plan r2 (`config-discovery-b/b2-c/PLAN-r2.md`), section 3 (the law step and its recommendation), with your reviews `codex-b2c-plan-r1` (NBO-2) and `codex-b2c-plan-r2`.
- NE (`docs/v2/contracts/product-v1/native-evidence.md`): §1.2 (146-215), the `allowJs` derivation (527-545), U-4a's pruned-read sentence (735-741), U-1 (619-948), `TypeScriptConfigGraphV1` (1332-1360).
- Law items 14 and 15.
- The public detail registry (`docs/coop/design-corrections/public-detail-registry.v1.json`) and its alias rule.
- B-S9 (the `CONFIG.INVALID` remedy route) and B-S10 (the product vocabulary route).

## What to review

1. **Need and scope.**
   - Is a law step needed? No current text fixes pre-Plan `extends` resolution, and the reference takes `allowJs` as a trusted observation.
   - Does r8 change only item 14a, S10 and the one "Not claimed" line?
2. **Reading.** JSONC, duplicate keys, the bounds, the fields read, and the shape of `extends`.
3. **Resolution.**
   - The path and package candidate orders, and the npm name and subpath grammar.
   - Nothing outside the project root, and no `exports` conditions.
   - Is anything ambiguous, or able to name two different files for one specifier?
4. **Read set versus descent.** Is treating a read inside `node_modules` as a read-set access (NE:735-741), not discovery descent (U-4a), sound?
5. **Custody and links.** Is the custody and symbolic-link rule sound before and after C1?
6. **Effective `allowJs`.** Does it match NE:527-545 exactly?
7. **Refusals.**
   - Is refusing on any unresolved edge right?
   - Are the four internal keys well formed?
   - Is one new public record with alias rows justified against the alias rule, rather than reusing an existing detail?
   - The D9 row and the subject.
8. **S10.** Is a contract successor the right route for the registry record, the aliases, the product vocabulary and the remedy?
9. **C2.** Is one shared function for C2's projection and graph right?

## Output

`review.json` must carry `nonBlockingObservations` and the following, with your independently checked values:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "108f1b2db8fedc45612733ba2c7e9911298a2835a2ef173658be1908d3e770b2",
  "onlyItem14aS10AndNotClaimedLine": true,
  "lawStepNeeded": true,
  "readingAndBoundsSound": true,
  "candidateOrderAndGrammarExplicit": true,
  "readSetNotDescentSound": true,
  "custodyAndSymlinkRuleSound": true,
  "effectiveAllowJsMatchesNe": true,
  "refusalsAndAliasesSound": true,
  "oneNewPublicRecordJustified": true,
  "successorS10Sound": true,
  "sharedWithC2": true,
  "codeWritten": false,
  "bindingMade": false,
  "productQualification": false
}
```
