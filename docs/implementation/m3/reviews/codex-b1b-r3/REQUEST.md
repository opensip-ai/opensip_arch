# Review request: B1-B-r3 (carriers, invocation mode, environment check; M3-B unit B1-b), round 3

## Round 3

Round 2 (`/tmp/opensip-implementation/reviews/codex-b1b-r2/`, your REQUIRED-FINDINGS) accepted round 1's RF-01 and RF-02 and raised two findings. Do not modify it. `SCOPE.md`'s "Round 3" section states each resolution, and the evidence is a fresh full lane (`checks-r5`).
- **R2-RF-01.** The pin test records every real `include!` edge on blanked code, with its test scope, and resolves whole-test files to a fixed point. One production-reachable inclusion makes a file production. New negative controls cover a production inclusion added beside the test one, and include text in comments and literals.
- **R2-RF-02, the zero lookup count.** A test-only counter of local-carrier lookups (`LOCAL_LOOKUPS`) is 0 in CI and 2 interactively. A new lane mutation that performs and ignores a charged CI lookup is caught.
- **R2-RF-02, the composition.** `ScenarioHome::compose_analysis_carriers` sits in security's existing test-only `scenario` seam, so there is no production facade. The host test drives it with the real resolver and X12 admission. For a refused project-layer pack, it shows no registry capture, a byte-identical registry (no RESERVED row), unchanged members (no lease or journal) and a released writer. The bundled pack is admitted and captured.

Then review the whole unit again, as below.


Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1b-r3/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/check_operability.py source --repository <tree>`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1b-r3-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-b-r3-subject.json`: 12046 bytes, SHA-256 `4d4b0bc303525ec2734b2f2ff09a098c0e95207cb4eedfbdfb35e89ce49394f5`, 53 members. Rehash every member.
- **Bases.**
  - Product `c0151bc6b7fdb6db9157124fa068c8be5061f5d4`, clean: B1-a and v188 are bound.
  - Architecture `b98932720200253f671814d9cb728ba0615c1085`.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b1b` holds the exact bytes of `product-map.json`.
- **Counts.** Inventory 188 and contract successors 162 are unchanged. v189 follows acceptance.

## Authority

- The accepted plan `config-discovery-b/b1-b/PLAN-r3.md`, and M3-B r5 (`PROPOSAL-r5.md`): items 2, 3 and 9, and item 9's exact exception list. You accepted both in `codex-b1b-plan-r3`.
- X2 r9: item 3a and its order decision, item 3 and item 9.
- AQ section 1.1.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit and two new lead decisions:
- **LD-B1B-4:** no public facade, so the hostile-environment control is split by crate.
- **LD-B1B-5:** the children are ignored tests, so no child-marker variable is needed, and the code's list is r5's minus that unused allowance.

Judge:
1. **The carriers against X2 item 3a and plan r3.**
   - Capture from the descriptor selection judged.
   - The 4 MiB bound and ledger charges.
   - Absence observations and their recheck under the fence.
   - CI never probing local.
   - Refusal subjects on the existing row, with no new code.
2. **The legacy path.** Is it untouched in reads, charges, refusals, rechecks and latching? Does the two-phase API enforce item 3a's order for the analysis path, with the session and gate wrappers mirroring the legacy ones?
3. **`capture_optional` and `recheck_absent`.** Positive absence, rechecked; nothing created; otherwise exactly `capture`.
4. **The invocation mode.** One type (B1A-FU-1); the rule; the observation; no environment; no caller.
5. **The environment check.**
   - Do the per-crate `clippy.toml` files scope it to host and security?
   - Are the thirteen allows on exactly r5's seventeen sites?
   - Is the pin test exact and correct?
   - Does LD-B1B-5's narrower list satisfy r5's "holds the list exactly"?
   - Is the operability `stdio` row for `invocation_mode.rs` right?
6. **The evidence.**
   - `evidence/checks.json`, `test-comparison.json` and `controls.json`: equal failure sets for both crates, Clippy, rustfmt with its declared base-dirty exclusions, the tools tests, the census, verify_design, the four mutations and two planted reads, each caught.
   - Do the new tests cover plan r3 section 2? That includes the legacy-compatibility ledger control and the hostile-environment children (LD-B1B-4).
7. **Scope.** There is no public API, CLI wiring, discovery or qualification, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "4d4b0bc303525ec2734b2f2ff09a098c0e95207cb4eedfbdfb35e89ce49394f5",
  "r2Rf01IncludeConfinementExact": true,
  "r2Rf02ZeroLookupCountedAndCompositionShown": true,
  "r1FindingsStayResolved": true,
  "implementsPlanR3": true,
  "captureFromJudgedDescriptors": true,
  "absenceObservationsRechecked": true,
  "ciNeverProbesLocal": true,
  "legacyPathUnchanged": true,
  "twoPhaseOrderEnforced": true,
  "optionalGlobalCaptureSound": true,
  "invocationModeUnifiedAndPure": true,
  "environmentListExactPerR5": true,
  "ldB1B4Sound": true,
  "ldB1B5Sound": true,
  "refusalsNoNewCode": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 9,
  "inventoryUnchanged": 188,
  "contractSuccessorsUnchanged": 162,
  "publicApiAdded": false,
  "productionCallerAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then v189, reviewed and bound separately. Nothing is pushed.
