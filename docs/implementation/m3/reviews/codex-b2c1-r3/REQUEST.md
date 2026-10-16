# Review request: B2-C1-r3 (the native unit instrument; M3-B unit B2-c, sub-unit B2-c1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2c1-r3/`).

## Boundaries

- Do not edit either repository, the worktree, the stage or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree: `python3 -I -B tools/check_operability.py source --repository <tree>` and `tools/tests/test_discovery_fw01.py`;
  - `python3 -I -B tools/host/discovery_unit_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`;
  - importing the bound B2-c0 reference read-only to try your own inputs against the recorded vectors.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2c1-r3-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-c1-r3-subject.json`: 10448 bytes, SHA-256 `7c43d5d56cdc65f423c267818287b67a9edcbfb603dcd6a59da29816e7880bf9`, 47 members. Rehash every member.
- **Earlier rounds.**
  - Your `codex-b2c1-r1` (`/tmp/opensip-implementation/reviews/codex-b2c1-r1/review.json`) raised B2C1-R1-RF-1 to RF-3 and NBO-1; `SCOPE.md`'s "r2 changes" section resolves them.
  - Your `codex-b2c1-r2` (`/tmp/opensip-implementation/reviews/codex-b2c1-r2/review.json`) raised B2C1-R2-RF-1; the "r3 changes" section resolves it.
- **Bases.**
  - Product `b0154f08f9193bbf3ca368420c2dae2006c11661`, clean: 166 contract successors, inventory v200.
  - Architecture `b6e42226f103642306e8c0cd1ac2ddc1b633587a`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2c1` holds the exact bytes of `product-map.json`.

## Authority

- The B2-c plan r2, section 2.1 (Codex `codex-b2c-plan-r2`).
- B2-c0, the current native unit reference (contract successor 166; `codex-b2c0-reference-r2`).
- NE §1.4, as B-S1 and B2-c0 override it.
- Law M3-B r7 items 13 to 15.
- The public detail registry.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
0. **Round 2.** Is B2C1-R2-RF-1 resolved?
   - Grammar refusals carry the class, not the value's `repr` spelling.
   - The tool's normalization of the reference key.
   - The U+0085, U+2028 and ASCII malformed-root vectors.
   - The mutation.

   Is the lead decision sound? Python's printability follows its Unicode database, the keys are internal, and the length form is still exact.

   **Round 1.**
   - **RF-1.** The production entries require `&AdmittedBoundaries`, and `require_admitted_boundaries` refuses a missing inventory with the internal key. Is the standalone lane compiled only under `cfg(test)`, and does the source control hold that?
   - **RF-2.** Are the character-count bounds right in `discovery.rs` and the scenario admission? Are the multibyte vectors at 2049, 4096 and 4097 characters sufficient?
   - **RF-3.** Does the vocabulary loop over the defaulted rows refuse an unknown mode, recorded as a vector?
   - **NBO-1.** Is `source.json` corrected?
   - Are the three new mutations caught?
1. **Exact reproduction.** Does `discovery.rs` implement the B2-c0 reference exactly?
   - `discover_units`, including LD-B2C0-1, the subset test, the member check, explicit roots and folding, the cap, U-1 modes, U-2 folding, U-9 and U-4b order.
   - `assign_membership`, `unit_scope_descriptor` and `default_capability_selection`.

   Do the vectors cover each branch? Construct inputs where the two might differ, and check them against the reference.
2. **The security surface.**
   - Is `discovery_export.rs` a narrow, faithful mirror over the rule, with the rule called and never restated?
   - Are `discovery_rule.rs` and `custody.rs` unchanged, and so the census closure?
   - Can production code obtain an `AdmittedBoundaries` other than from security? `scenario::admitted_boundaries` is in the test seam only.
3. **The alias map and refusals.** Are they exactly the registry rows and the reference's keys, with `native.admitted-boundaries-required` internal?
4. **The scope descriptor and default selection.**
   - The bounds, the digest and the disclosure.
   - The matrix copy.
   - The selection rules, and the deferral of full spec admission to the Plan stage (`SCOPE.md`).
5. **FW-01 and purity.** Is there no I/O, process, socket, write or environment read? Is the structural check extended correctly?
6. **The decisions in `SCOPE.md`.**
   - The rule file left untouched.
   - Cargo `[workspace]` as an input.
   - `membershipDigest` not this unit's.
7. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`.
   - The security and host suites.
   - Clippy.
   - The twelve mutations, each caught.
8. **Scope.**
   - There is no caller, environment read or law change.
   - The paths are exactly the product map's.
   - Inventory v201 follows.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "7c43d5d56cdc65f423c267818287b67a9edcbfb603dcd6a59da29816e7880bf9",
  "b2c1R1Rf1Resolved": true,
  "b2c1R1Rf2Resolved": true,
  "b2c1R1Rf3Resolved": true,
  "b2c1R2Rf1Resolved": true,
  "grammarKeyDecisionSound": true,
  "implementsPlanR2Section21": true,
  "reproducesB2c0ReferenceExactly": true,
  "v3InputAndOutputSound": true,
  "memberRulesAndLd1Implemented": true,
  "sharedRuleCalledNotCopied": true,
  "ruleFileAndCensusClosureUnchanged": true,
  "admittedBoundariesUnforgeableInProduction": true,
  "aliasMapExactAndClosed": true,
  "defaultSelectionSound": true,
  "scopeDescriptorSound": true,
  "fw01Covered": true,
  "vectorsSufficient": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 12,
  "inventorySuccessorFollows": true,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "lawChanged": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the record. The product code commit follows, then inventory v201. Nothing is pushed.
