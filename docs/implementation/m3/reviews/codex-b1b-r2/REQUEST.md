# Review request: B1-B-r2 (carriers, invocation mode, environment check; M3-B unit B1-b), round 2

## Round 2

Round 1 (`/tmp/opensip-implementation/reviews/codex-b1b-r1/`, your REQUIRED-FINDINGS) raised four required findings and one observation. Do not modify it. `SCOPE.md` states each resolution, its "Round 2" section lists the controls, and the evidence is a fresh full lane (`checks-r4`; r2 and r3 failed before it on my own errors and are not evidence).
- **RF-01.** Selection retains the sample its custody judgment passed on (`judge_project_object_sampled`; the legacy function wraps it with identical charges), and `judge_local` does the same. `capture_carrier` requires samples equal to that judgment before and after the read, never re-baselining. New controls interpose a rewrite and a mode change between judgment and read, for both carriers.
- **RF-02.** `capture_optional` now runs `read_capture`'s own walk, with absence lookups under each judged parent. The `AbsentObservation` keeps the judged parents' samples, and `recheck_absent` re-judges each parent (private custody, exact name, original sample) before the absence. New controls cover a wrong-custody parent, and a parent's mode change, replacement and detachment.
- **RF-03.** The pin test resolves the three constant-backed names to their values. It finds test scope by brace matching over blanked code, including `include!`s inside test modules, and checks allow attachment. Two negative controls run on a copy.
- **RF-04.**
  - Phase 1's charges are independent of the registry, and it has no effect.
  - CI local lookups are counted by the ledger.
  - The legacy charges are compared against the base product, by the same probe run on a `git archive` copy of the base.
  - Cleared-environment baselines, with complete resolution output.
  - A separate assertion of the permitted Git refusal.
- **NBO-01.** rustfmt is classified over every edited Rust file (`evidence/rustfmt-classification.json`).

Then review the whole unit again, as below.


Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b1b-r2/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys or held trees. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and these read-only offline checks are permitted:
- `python3 -I -B tools/tests/test_environment_exceptions.py` in the candidate worktree;
- `python3 -I -B tools/check_operability.py source --repository <tree>`.

## Subject

- **Stage.** `/tmp/opensip-implementation/b1b-r2-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b1-b-r2-subject.json`: 11591 bytes, SHA-256 `967257c8b5ef365993b82af7154f295ec3f1773193d9562778c3fe82ff71522f`, 51 members. Rehash every member.
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
  "subjectManifestSha256": "967257c8b5ef365993b82af7154f295ec3f1773193d9562778c3fe82ff71522f",
  "rf01CaptureBoundToJudgment": true,
  "rf02OptionalParentsJudgedAndRechecked": true,
  "rf03PinResolvesConstantsAndScope": true,
  "rf04ControlsComplete": true,
  "nbo01FormatClassified": true,
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
  "controlsCaught": 8,
  "inventoryUnchanged": 188,
  "contractSuccessorsUnchanged": 162,
  "publicApiAdded": false,
  "productionCallerAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then v189, reviewed and bound separately. Nothing is pushed.
